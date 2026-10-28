"""Deterministic sliding-word chunking with source provenance."""
import hashlib
import re

def chunk_documents(documents: list[dict], size: int = 110, overlap: int = 25) -> list[dict]:
    if size < 10 or not 0 <= overlap < size:
        raise ValueError("Chunk size must be >= 10 with overlap less than size")
    chunks = []
    for document in documents:
        words = re.findall(r"\S+", document["text"])
        step = size - overlap
        for start in range(0, len(words), step):
            excerpt = " ".join(words[start:start + size])
            if not excerpt:
                continue
            uid = hashlib.sha256((document["source"] + ":" + str(start) + ":" + document["checksum"]).encode()).hexdigest()[:14]
            chunks.append({"id": uid, "source": document["source"],
                           "start_word": start, "text": excerpt})
            if start + size >= len(words):
                break
    return chunks
