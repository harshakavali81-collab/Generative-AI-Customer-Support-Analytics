# SupportLens AI | End-to-end RAG & Support Analytics

**Problem:** support teams need timely, consistently sourced answers and a way to spot where their help-center documentation is incomplete, without logging sensitive customer prompts.

**Approach:** authored six fictional policy articles, ingested and split them into overlapping chunks, constructed a sparse vector index, implemented cosine retrieval and citation-constrained extraction, recorded only minimal answer metadata, and exposed a React chat/analytics UI.

**Engineering decisions:** TF-IDF instead of downloading a heavy embedding model makes the default demo fast, deterministic and runnable on modest laptops. Optional remote LLM generation illustrates the additional control needed for external inference. SQLite supports a compact prototype; production would require tenant-aware persistence, isolation and access control.

**Evidence:** reproducible pytest/API tests and a curated 16-question retrieval fixture. Metrics represent only traffic generated when the demo is run. Original architecture and analytic illustration assets document the workflow, and a GitHub Actions workflow executes tests/builds.

**Outcome:** portfolio-ready codebase, documentation and an offline-first demonstration; **not** a validated production customer-service deployment. Unknown questions escalate rather than silently inventing policy.

**Relevant skills:** Python, FastAPI, React, SQL, NLP, embeddings, information retrieval, API design, data ethics, responsible AI and developer testing.

**Repository:** https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics

## Recorded verification at latest checked code revision

The [GitHub Actions run](https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics/actions/runs/40659021869) passed 32 Python regression tests and the React build. On a 16-question author-created fictional fixture, 13/13 answerable prompts retrieved the expected policy source in the top 3, 13/13 returned answers with citation IDs present among retrieved passages, and 3/3 unsupported prompts abstained. These are **fixture-level functional checks, not expert-rated factual entailment, independent hallucination benchmarking or actual customer satisfaction**.

The standalone browser demo is copied into the portfolio repository, but a successful publicly accessible HTTP deployment is not independently verified. The FastAPI service is not publicly deployed.

## Browser and container evidence

[GitHub CI run](https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics/actions/runs/40660436505): **32 Python tests passed**; React production build passed; both API and web Docker containers became healthy and served a cited chat answer through Nginx; Chromium browser E2E passed on desktop and mobile. See [actual screenshots](https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics/actions/runs/40660436505/artifacts/12803617158) and [evaluation JSON artifact](https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics/actions/runs/40660436505/artifacts/12802349853). This evidence validates a fictitious-data portfolio prototype, not a production deployment or independent answer-quality certification.
