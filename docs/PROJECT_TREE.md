# Complete project structure

```text
Generative-AI-Customer-Support-Analytics/
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml                    Python/API/React/JS checks
│       └── pages.yml                 Manual standalone showcase deploy
├── data/source_docs/                Six fictional support policies
│   ├── accounts.md
│   ├── billing.md
│   ├── privacy.md
│   ├── returns.md
│   ├── shipping.md
│   └── warranty.md
├── src/
│   ├── ingestion/loader.py          Trusted file ingestion
│   ├── chunking/split.py            Sliding overlap chunks
│   ├── embeddings/vectorizer.py     Sparse TF-IDF
│   ├── vector_store/store.py        Optional local JSON persistence
│   ├── retrieval/search.py          Cosine top-k
│   ├── generation/answer.py         Source-linked extractive answer
│   ├── guardrails/rules.py          Basic input and PII checks
│   └── analytics/metrics.py         SQLite with retention / ratings
├── backend/app/main.py              API + guard/middleware
├── frontend/
│   ├── src/pages/Chat.jsx           Answers, evidence and ratings
│   ├── src/pages/Analytics.jsx      KPIs, topic charts, CSV
│   ├── src/components/Metric.jsx
│   ├── src/styles.css
│   ├── Dockerfile
│   └── nginx.conf
├── site/                            Standalone browser-only demonstration
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   └── policies.json
├── sql/analytics.sql
├── evaluation/golden_questions.json
├── scripts/
│   ├── build_index.py
│   ├── evaluate.py
│   ├── smoke_test.py
│   └── benchmark.py
├── tests/                           Regression, API and privacy checks
├── docs/
│   ├── images/                      Ten original SVG explanations
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── DATA_DICTIONARY.md
│   ├── DEPLOYMENT.md
│   ├── EVALUATION.md
│   ├── IMAGE_GALLERY.md
│   ├── MODEL_CARD.md
│   ├── PORTFOLIO_CASE_STUDY.md
│   ├── PROJECT_TREE.md
│   ├── RUNBOOK.md
│   ├── SECURITY.md
│   └── THREAT_MODEL.md
├── .env.example
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

See [system architecture](images/02-system-architecture.svg), [ingestion pipeline](images/03-ingestion-pipeline.svg), [retrieval](images/05-vector-retrieval.svg), and [decision gates](images/06-grounded-answer-flow.svg).

Source policy content is a **fictional demo**. Actual accounts, authentication, payments or customer requests are not connected.
