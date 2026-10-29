# ✦ SupportLens AI — Generative AI Customer Support & Analytics

**Source-grounded customer support assistant + privacy-minimal SQL analytics + React dashboard.** Built as a reproducible portfolio project for **GenAI Engineer · AI/ML Engineer · Python Developer · Product Analyst** roles.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![SupportLens AI](<docs/images/01-product-overview.svg>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

Existing published preview link: [Open browser preview](https://harshakavali81-collab.github.io/harshavardhan-portfolio/supportlens-demo/). This update does not independently verify its availability or backend deployment.

## Key Features

- Six trusted, fictional Markdown support policy documents with checksums and deterministic chunk IDs.
- Sliding 110-word chunk windows with 25-word overlap and local TF-IDF vector indexing.
- Cosine top-K retrieval with conservative answer extraction and inline `[source:<chunk-id>]` references.
- Guardrails: bounded input, known instruction-injection phrase refusal, minimum evidence overlap, human escalation for unsupported questions.
- Optional OpenAI Chat Completions (requires your own secret/API billing); falls back to extractive answers if model is unavailable or returns unrecognized citation IDs.
- FastAPI endpoints for chat, sources, health, analytics and unanswered-topic reports.
- SQLite telemetry collects **topic, answered status, response latency, citation count, length, timestamp**; **does not store raw questions**.
- Responsive React chat with evidence expanders; analytics KPI cards, trend chart and topic bars.
- Pytest regression suite, curated evaluation fixtures, Docker Compose and CI build.

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![FastAPI](https://img.shields.io/badge/FastAPI-334155?style=flat-square) ![React](https://img.shields.io/badge/React-334155?style=flat-square) ![SQL](https://img.shields.io/badge/SQL-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/ARCHITECTURE.md>)

## Local Installation & Setup Guide

Python 3.11+ and Node 20+:

```bash
git clone https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics.git
cd Generative-AI-Customer-Support-Analytics
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m uvicorn backend.app.main:app --reload
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

**Open http://localhost:5173** for chat and analytics; API is at **http://localhost:8000/docs**. To run with Docker instead, use `docker compose up --build` and visit **http://localhost:8080**. Docker is a local reference setup and does not include production authentication, quotas or backup automation.

```bash
python -m scripts.build_index
python -m scripts.evaluate
python -m pytest -q
cd frontend && npm run build
```

No key is needed for the default offline experience. Environment options are documented in [`.env.example`](.env.example); export variables into the process or use a securely managed environment file.

### Optional LLM generation

Set `ENABLE_REMOTE_LLM=true`, `OPENAI_API_KEY` and a supported `OPENAI_MODEL`. **Using this option transmits user questions and retrieved document excerpts to an external API, may incur charges, and must only be done with consent and a suitable privacy arrangement.** The fallback remains local if the call or citation validation fails. Citation-ID validation cannot guarantee that every generated assertion is supported; conduct human evaluation before production.

## Challenges & Solutions

**Repository organization:** this project uses `src/`, `backend/`, `frontend/`. Keeping those paths stable avoids breaking imports, asset links and deployment commands while the documentation follows a shared format. Project-specific technical limitations and prior release evidence are retained in [Project guide](PROJECT_GUIDE.md).

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

**Source-grounded customer support assistant + privacy-minimal SQL analytics + React dashboard.** Built as a reproducible portfolio project for **GenAI Engineer · AI/ML Engineer · Python Developer · Product Analyst** roles.

    

> **Demo integrity:** All policies describe a *fictional retailer*. The default assistant uses offline **TF-IDF sparse vector embeddings + extractive, source-cited answers**; it is not a pretrained LLM. Optional OpenAI generation is disabled unless deliberately configured. Figures labeled illustrative are not observed performance. No production customer support or real customer data is claimed.

**LIVE DEMO:** [Launch SupportLens AI — verified browser-only experience](https://harshakavali81-collab.github.io/harshavardhan-portfolio/supportlens-demo/) · [Public portfolio case study](https://harshakavali81-collab.github.io/harshavardhan-portfolio/cases/supportlens.html) · [GitHub Actions external HTTP evidence](https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics/actions/runs/40660742935). The published demo runs entirely in the visitor's browser using fictional policies; the complete FastAPI service remains local/container-tested, not publicly hosted.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `backend/` | Backend services |
| `frontend/` | Frontend interface |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `sql/` | SQL schema and analysis |
| `scripts/` | Automation scripts |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

See [LICENSE](LICENSE) for the existing terms.
