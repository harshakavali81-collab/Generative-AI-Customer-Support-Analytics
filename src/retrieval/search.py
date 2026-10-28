"""Cosine similarity over source-linked sparse vectors."""
from src.embeddings.vectorizer import embed, dot

def retrieve(question: str, index: dict, top_k: int = 4, min_score: float = 0.075) -> list[dict]:
    if not question.strip() or top_k < 1:
        return []
    vector = embed(question, index["idf"])
    if not vector:
        return []
    ranked = sorted(((dot(vector, vec), chunk) for vec, chunk in zip(index["vectors"], index["chunks"])),
                    key=lambda hit: (-hit[0], hit[1]["source"], hit[1]["start_word"]))
    return [{"score": round(score, 4), **chunk} for score, chunk in ranked[:top_k] if score >= min_score]
