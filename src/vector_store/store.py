"""Simple versioned local JSON vector store. Replace with pgvector at scale."""
import json
from pathlib import Path
from src.embeddings.vectorizer import train

def create_index(chunks: list[dict], output: str | Path | None = None) -> dict:
    index = {"version": 1, **train(chunks)}
    if output is not None:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(index, ensure_ascii=False), encoding="utf-8")
    return index

def read_index(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("version") != 1 or len(data.get("vectors", [])) != len(data.get("chunks", [])):
        raise ValueError("Invalid vector index")
    return data
