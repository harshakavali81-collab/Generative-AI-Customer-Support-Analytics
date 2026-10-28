"""Input boundaries and minimal analytics. Not a substitute for full moderation."""
import re
from src.embeddings.vectorizer import tokens

MAX_QUESTION = 900
INJECTION = re.compile(r"(ignore (all |any )?(previous|prior|system) instructions|reveal (the )?(system|developer) prompt|override (your )?rules|act as (the )?system)", re.I)
TOPICS = {
    "refund": ("refund", "return", "money", "reimbursement"),
    "shipping": ("shipping", "delivery", "dispatch", "tracking", "courier"),
    "account": ("login", "password", "account", "sign", "security"),
    "billing": ("invoice", "billing", "payment", "card", "charge"),
    "warranty": ("warranty", "repair", "replacement", "defect"),
    "privacy": ("privacy", "data", "delete", "personal"),
}

def validate_question(question: str) -> str:
    question = question.strip()
    if not question or len(question) > MAX_QUESTION:
        raise ValueError(f"Question must contain 1 to {MAX_QUESTION} characters")
    return question

def suspected_injection(question: str) -> bool:
    return bool(INJECTION.search(question))

def topic(question: str) -> str:
    words = set(tokens(question))
    for name, terms in TOPICS.items():
        if words.intersection(terms):
            return name
    return "other"

def public_citation(hit: dict) -> dict:
    return {"id": hit["id"], "source": hit["source"], "score": hit["score"],
            "excerpt": hit["text"][:320]}
