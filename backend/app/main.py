"""FastAPI app: grounded responses, no raw-question telemetry."""
import os
import time
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from src.ingestion.loader import load_documents
from src.chunking.split import chunk_documents
from src.vector_store.store import create_index
from src.retrieval.search import retrieve
from src.generation.answer import answer, ABSTAIN
from src.guardrails.rules import validate_question, suspected_injection, topic, public_citation
from src.analytics.metrics import connection, record, summary, unanswered_report

ROOT = Path(__file__).resolve().parents[2]
DOCS = Path(os.getenv("SUPPORT_DOCS_DIR", str(ROOT / "data" / "source_docs")))
DB = Path(os.getenv("SUPPORT_DB_PATH", str(ROOT / "instance" / "analytics.sqlite3")))
INDEX = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global INDEX
    INDEX = create_index(chunk_documents(load_documents(DOCS)))
    with connection(DB):
        pass
    yield

app = FastAPI(title="SupportLens AI", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
                   allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type", "X-Admin-Token"])

class Question(BaseModel):
    question: str = Field(min_length=1, max_length=900)

def admin(x_admin_token: str | None = Header(default=None)):
    required = os.getenv("ADMIN_TOKEN", "")
    if required and x_admin_token != required:
        raise HTTPException(status_code=403, detail="Admin access required")
    if os.getenv("ENVIRONMENT", "development") == "production" and not required:
        raise HTTPException(status_code=503, detail="Configure ADMIN_TOKEN in production")

@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "remote-llm" if os.getenv("ENABLE_REMOTE_LLM","false").lower()=="true" else "offline-extractive",
            "indexed_chunks": len(INDEX["chunks"]) if INDEX else 0}

@app.get("/api/sources")
def sources():
    return {"sources": sorted({c["source"] for c in INDEX["chunks"]})}

@app.post("/api/chat")
def chat(body: Question):
    started = time.perf_counter()
    try:
        question = validate_question(body.question)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    flagged = suspected_injection(question)
    hits = [] if flagged else retrieve(question, INDEX)
    response = ABSTAIN if flagged else answer(question, hits)
    answered = response != ABSTAIN
    elapsed = int((time.perf_counter() - started) * 1000)
    record(DB, topic(question), answered, elapsed, len(hits), len(question))
    return {"answer": response, "answered": answered, "citations": [public_citation(h) for h in hits] if answered else [],
            "latency_ms": elapsed, "mode": "offline-extractive" if os.getenv("ENABLE_REMOTE_LLM","false").lower()!="true" else "remote-with-extractive-fallback"}

@app.get("/api/analytics", dependencies=[Depends(admin)])
def analytics():
    return summary(DB)

@app.get("/api/unanswered", dependencies=[Depends(admin)])
def unanswered():
    return {"unanswered_by_topic": unanswered_report(DB),
            "privacy": "Only topic counts are retained; raw questions are not stored."}
