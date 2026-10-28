"""Auditable evaluation on explicitly fictional, author-created support questions."""
import argparse
import json
import re
from pathlib import Path

from src.ingestion.loader import load_documents
from src.chunking.split import chunk_documents
from src.vector_store.store import create_index
from src.retrieval.search import retrieve
from src.generation.answer import answer, ABSTAIN

ROOT = Path(__file__).resolve().parents[1]

def evaluate() -> dict:
    dataset = json.loads((ROOT / "evaluation" / "golden_questions.json").read_text(encoding="utf-8"))
    index = create_index(chunk_documents(load_documents(ROOT / "data" / "source_docs")))
    hit_at_3 = abstained = answered = valid_citation = 0
    rows = []
    for item in dataset:
        hits = retrieve(item["question"], index, top_k=3)
        response = answer(item["question"], hits)
        found = {h["id"] for h in hits}
        citations = set(re.findall(r"\[source:([a-f0-9]{14})\]", response))
        sourced = response != ABSTAIN
        citation_ok = bool(citations) and citations.issubset(found)
        expected = item["expected_source"]
        hit = expected is not None and any(h["source"] == expected for h in hits)
        if expected is not None:
            hit_at_3 += int(hit)
            answered += int(sourced)
            valid_citation += int(citation_ok)
        else:
            abstained += int(not sourced)
        rows.append({
            "question": item["question"], "expected_source": expected,
            "retrieved_sources": [h["source"] for h in hits],
            "source_hit_at_3": hit if expected is not None else None,
            "answered": sourced, "citation_ids_in_retrieved_evidence": citation_ok,
            "unsupported_abstained": not sourced if expected is None else None,
        })
    n_answerable = sum(x["expected_source"] is not None for x in dataset)
    n_unsupported = len(dataset) - n_answerable
    return {
        "dataset": "fictional, author-authored customer support evaluation",
        "not_independent_benchmark": True,
        "n": len(dataset),
        "answerable": n_answerable,
        "unsupported": n_unsupported,
        "retrieval_hit_at_3": hit_at_3,
        "retrieval_recall_at_3": round(hit_at_3 / n_answerable, 4) if n_answerable else None,
        "unsupported_abstentions": abstained,
        "supported_queries_with_any_answer": answered,
        "supported_queries_with_valid_citation_ids": valid_citation,
        "limits": ("Source hit and citation-ID verification do not establish factual entailment, "
                   "end-to-end correctness, real-user effectiveness or security certification."),
        "details": rows,
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON report file")
    parser.add_argument("--strict", action="store_true", help="Fail if authored source hits or abstentions regress")
    args = parser.parse_args()
    result = evaluate()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k != "details"}, indent=2))
    if args.strict:
        if (result["retrieval_hit_at_3"] != result["answerable"] or
                result["unsupported_abstentions"] != result["unsupported"]):
            raise SystemExit("Authored fixture regression: source retrieval or abstention threshold not met")

if __name__ == "__main__":
    main()
