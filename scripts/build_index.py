"""Rebuild an offline vector index from trusted documents."""
from pathlib import Path
from src.ingestion.loader import load_documents
from src.chunking.split import chunk_documents
from src.vector_store.store import create_index
root = Path(__file__).resolve().parents[1]
index = create_index(chunk_documents(load_documents(root / "data" / "source_docs")), root / "instance" / "vectors.json")
print(f"Indexed {len(index['chunks'])} chunks into instance/vectors.json")
