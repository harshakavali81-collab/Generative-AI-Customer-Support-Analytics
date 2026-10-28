"""FastAPI: source-grounded support, protected analytics, anonymous opt-in feedback."""
import hmac
import os
import time
from collections import defaultdict, deque
from threading import Lock
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field

from src.ingestion.loader import load_documents
from src.chunking.split import chunk_documents
from src.vector_store.store import create_index
from src.retrieval.search import retrieve
from src.generation.answer import answer, ABSTAIN
from src.guardrails.rules import validate_question, suspected_injection, topic, public_citation
from src.analytics.metrics import (
    connection, record, summary, unanswered_report,
    submit_feedback, purge_old_events, aggregate_csv,
)

ROOT = Path(__file__).resolve().parents[2]
DOCS = Path(os.getenv("SUPPORT_DOCS_DIR", str(ROOT / "data" / "source_docs")))
DB = Path(os.getenv("SUPPORT_DB_PATH", str(ROOT / "instance" / "analytics.sqlite3")))
INDEX = None
buckets = defaultdict(deque)
bucket_lock = Lock()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global INDEX
    INDEX = create_index(chunk_documents(load_documents(DOCS)))
    with connection(DB):
        pass
    purge_old_events(DB, int(os.getenv("EVENT_RETENTION_DAYS", "30")))
    yield

app = FastAPI(title="SupportLens AI", version="1.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=False, allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-Admin-Token", "X-Chat-Token"])

def production() -> bool:
    return os.getenv("ENVIRONMENT", "development").lower() == "production"

def secure_equals(supplied: str | None, required: str) -> bool:
    return bool(supplied) and hmac.compare_digest(supplied, required)

@app.middleware("http")
async def policy_middleware(request: Request, call_next):
    if request.url.path == "/api/chat" and request.method == "POST":
        limit = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60" if production() else "0"))
        if limit > 0:
            # In-memory demo limiter; at multi-instance scale replace with a trusted
            # ingress / Redis limiter (proxy IP behavior must be considered).
            peer = request.client.host if request.client else "unknown"
            current = time.monotonic()
            with bucket_lock:
                queue = buckets[peer]
                while queue and current - queue[0] >= 60:
                    queue.popleft()
                limited = len(queue) >= limit
                if not limited:
                    queue.append(current)
            if limited:
                return JSONResponse({"detail": "Too many requests. Retry later."},
                                    status_code=429, headers={"Retry-After": "60"})
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
    return response

class Question(BaseModel):
    question: str = Field(min_length=1, max_length=900)

class Feedback(BaseModel):
    request_id: str = Field(min_length=32, max_length=32)
    helpful: bool

def admin(x_admin_token: str | None = Header(default=None)):
    required = os.getenv("ADMIN_TOKEN", "")
    if production() and not required:
        raise HTTPException(status_code=503, detail="Configure ADMIN_TOKEN in production")
    if required and not secure_equals(x_admin_token, required):
        raise HTTPException(status_code=403, detail="Admin access required")

def chat_access(x_chat_token: str | None = Header(default=None)):
    required = os.getenv("CHAT_API_TOKEN", "")
    if production() and not required:
        raise HTTPException(status_code=503, detail="Configure CHAT_API_TOKEN in production")
    if required and not secure_equals(x_chat_token, required):
        raise HTTPException(status_code=403, detail="Chat access required")

@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "remote-llm" if os.getenv("ENABLE_REMOTE_LLM", "false").lower()=="true" else "offline-extractive",
            "indexed_chunks": len(INDEX["chunks"]) if INDEX else 0}

@app.get("/api/sources")
def sources():
    return {"sources": sorted({c["source"] for c in INDEX["chunks"]})}

@app.post("/api/chat", dependencies=[Depends(chat_access)])
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
    rid = record(DB, topic(question), answered, elapsed, len(hits), len(question))
    return {"answer": response, "answered": answered,
            "citations": [public_citation(h) for h in hits] if answered else [],
            "latency_ms": elapsed, "request_id": rid,
            "mode": "offline-extractive" if os.getenv("ENABLE_REMOTE_LLM", "false").lower()!="true" else "remote-with-extractive-fallback"}

@app.post("/api/feedback", dependencies=[Depends(chat_access)])
def feedback(body: Feedback):
    ok = submit_feedback(DB, body.request_id, body.helpful)
    if not ok:
        raise HTTPException(status_code=404, detail="Unknown or already rated response")
    return {"saved": True, "privacy": "Anonymous rating only; no question text stored"}

@app.get("/api/analytics", dependencies=[Depends(admin)])
def analytics():
    return summary(DB)

@app.get("/api/unanswered", dependencies=[Depends(admin)])
def unanswered():
    return {"unanswered_by_topic": unanswered_report(DB),
            "privacy": "Only topic counts are retained; raw questions are not stored."}

@app.get("/api/export/topics.csv", dependencies=[Depends(admin)])
def export_topics():
    return PlainTextResponse(aggregate_csv(DB), media_type="text/csv",
                             headers={"Content-Disposition": 'attachment; filename="supportlens_topics.csv"'})

@app.post("/api/admin/retention-cleanup", dependencies=[Depends(admin)])
def retention_cleanup():
    days = int(os.getenv("EVENT_RETENTION_DAYS", "30"))
    return {"deleted_events": purge_old_events(DB, days), "retention_days": days}
