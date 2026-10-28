"""Reproducible evidence retrieval evaluation on authored fictional support queries."""
import json
from pathlib import Path
from src.ingestion.loader import load_documents
from src.chunking.split import chunk_documents
from src.vector_store.store import create_index
from src.retrieval.search import retrieve
from src.generation.answer import answer, ABSTAIN

root = Path(__file__).resolve().parents[1]
dataset = json.loads((root / "evaluation" / "golden_questions.json").read_text())
index = create_index(chunk_documents(load_documents(root / "data" / "source_docs")))
hits_at_3 = 0
abstained = 0
for item in dataset:
    hits = retrieve(item["question"], index, top_k=3)
    if item["expected_source"]:
        hits_at_3 += int(any(h["source"] == item["expected_source"] for h in hits))
    else:
        abstained += int(answer(item["question"], hits) == ABSTAIN)
answerable = sum(bool(x["expected_source"]) for x in dataset)
unsupported = len(dataset) - answerable
print(json.dumps({"dataset": "authored fictional support FAQs", "n": len(dataset),
 "answerable": answerable, "retrieval_hit_at_3": hits_at_3,
 "retrieval_recall_at_3": round(hits_at_3 / answerable, 4) if answerable else None,
 "unsupported": unsupported, "unsupported_abstentions": abstained}, indent=2))
