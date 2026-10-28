# SupportLens AI | End-to-end RAG & Support Analytics

**Problem:** support teams need timely, consistently sourced answers and a way to spot where their help-center documentation is incomplete, without logging sensitive customer prompts.

**Approach:** authored six fictional policy articles, ingested and split them into overlapping chunks, constructed a sparse vector index, implemented cosine retrieval and citation-constrained extraction, recorded only minimal answer metadata, and exposed a React chat/analytics UI.

**Engineering decisions:** TF-IDF instead of downloading a heavy embedding model makes the default demo fast, deterministic and runnable on modest laptops. Optional remote LLM generation illustrates the additional control needed for external inference. SQLite supports a compact prototype; production would require tenant-aware persistence, isolation and access control.

**Evidence:** reproducible pytest/API tests and a curated 16-question retrieval fixture. Metrics represent only traffic generated when the demo is run. Original architecture and analytic illustration assets document the workflow, and a GitHub Actions workflow executes tests/builds.

**Outcome:** portfolio-ready codebase, documentation and an offline-first demonstration; **not** a validated production customer-service deployment. Unknown questions escalate rather than silently inventing policy.

**Relevant skills:** Python, FastAPI, React, SQL, NLP, embeddings, information retrieval, API design, data ethics, responsible AI and developer testing.

**Repository:** https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics
