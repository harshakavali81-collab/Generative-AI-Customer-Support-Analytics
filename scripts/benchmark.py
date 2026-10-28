"""Microbenchmark *offline lexical retrieval only*, not real API latency."""
import argparse
import json
import statistics
from time import perf_counter
from pathlib import Path
from src.ingestion.loader import load_documents
from src.chunking.split import chunk_documents
from src.vector_store.store import create_index
from src.retrieval.search import retrieve

def run(n=100):
    docs=Path(__file__).resolve().parents[1] / "data/source_docs"
    idx=create_index(chunk_documents(load_documents(docs)))
    questions=["How long is a refund?", "Where is my tracking link?", "How to reset my password?"]
    timings=[]
    for i in range(n):
        start=perf_counter()
        retrieve(questions[i%len(questions)],idx)
        timings.append((perf_counter()-start)*1000)
    timings.sort()
    return {"scope":"single-process offline lexical retrieval only; authored questions",
      "iterations":n, "median_ms":round(statistics.median(timings),4),
      "p95_ms":round(timings[min(n-1,int(n*.95))],4),
      "is_production_benchmark":False}

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--iterations",type=int,default=100)
    args=parser.parse_args()
    if not 10<=args.iterations<=10000:
        parser.error("iterations must be between 10 and 10000")
    print(json.dumps(run(args.iterations),indent=2))
