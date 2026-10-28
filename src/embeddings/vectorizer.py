"""Offline sparse TF-IDF vector embeddings (no API keys or downloads needed)."""
from collections import Counter
import math
import re

STOP = set("a an and are as at be by can do does for from has have how i if in is it my of on or our the their there these this to was we what when where which who why will with you your".split())

def tokens(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    # Minimal plural normalization for common support terms (refund/refunds, return/returns).
    words = [w[:-3] + "y" if len(w) > 5 and w.endswith("ies") else
             w[:-1] if len(w) > 4 and w.endswith("s") and not w.endswith(("ss", "us", "is")) else w
             for w in words]
    return [w for w in words if len(w) > 1 and w not in STOP]

def train(chunks: list[dict]) -> dict:
    freq = Counter()
    for chunk in chunks:
        freq.update(set(tokens(chunk["text"])))
    n = len(chunks)
    idf = {term: 1.0 + math.log((n + 1) / (1 + count)) for term, count in freq.items()}
    return {"idf": idf, "vectors": [embed(c["text"], idf) for c in chunks], "chunks": chunks}

def embed(text: str, idf: dict) -> dict:
    terms = Counter(tokens(text))
    weights = {t: (1 + math.log(count)) * idf[t] for t, count in terms.items() if t in idf}
    norm = math.sqrt(sum(v*v for v in weights.values())) or 1.0
    return {t: round(v / norm, 9) for t, v in weights.items()}

def dot(left: dict, right: dict) -> float:
    return sum(value * right.get(term, 0) for term, value in left.items())
