# Evaluation plan and interpretation

Run:
```bash
python -m pytest -q
python -m scripts.evaluate
```

**Dataset:** 16 authored fictional FAQ questions in `evaluation/golden_questions.json`; 13 include an expected source and 3 are intentionally unsupported. A single source match in top 3 is counted as a retrieval hit, not as proof that the answer is correct.

**Core checks:** trusted loading, overlap/IDs, normalized vectors, retrieval, citation provenance, input limits, suspicious instruction text, source abstention, SQLite without raw text fields, API authorization and production fail-closed analytics. React build checks syntax and asset bundling.

**What not to claim:** no production precision/recall, hallucination rate, actual user satisfaction or p95 latency until measured on held-out real queries under representative load. Even a citation-valid LLM answer can still misstate a policy.

**Next tests:** manual evidence entailment labels, holdout set, semantic vs sparse benchmark, relevance thresholds by source type, adversarial instructions embedded in documents, ambiguous language and demographic fairness review, privacy retention tests, load testing and human escalation audit.
