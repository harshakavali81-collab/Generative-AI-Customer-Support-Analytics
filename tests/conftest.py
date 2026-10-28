import pytest
from src.ingestion.loader import load_documents
from src.chunking.split import chunk_documents
from src.vector_store.store import create_index
from pathlib import Path

@pytest.fixture
def index():
    root = Path(__file__).resolve().parents[1]
    return create_index(chunk_documents(load_documents(root/"data"/"source_docs")))
