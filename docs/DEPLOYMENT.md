# Deployment and release instructions

## Three distinct deployment targets

1. **Full local stack (supported):** Python FastAPI backend, React interface, SQLite event store. Run with `docker compose up --build` and open http://localhost:8080.
2. **Browser-only showcase:** `site/` includes a standalone lexical retrieval demo using fictional policies and session-only metrics. It does **not** use FastAPI, SQLite, remote embeddings or a hosted LLM. A copy is included in the portfolio repository at `supportlens-demo/` for its existing GitHub Pages site.
3. **Production multi-user service (not deployed):** needs secured hosting, audited auth and tenancy, verified privacy/consent agreements, secrets, load tests and real domain validation. The current stack must not be described as production-ready.

## Publish the browser-only showcase

The portfolio repository contains `supportlens-demo/`. Once the portfolio's GitHub Pages deployment completes successfully, its expected URL is:

https://harshakavali81-collab.github.io/harshavardhan-portfolio/supportlens-demo/

**Do not claim this is live until an external HTTPS check succeeds.** Source control publication alone is not hosting verification.

For a *separate* Pages site under this source repository, first visit
https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics/settings/pages
and set **Build and deployment → GitHub Actions**. Then manually dispatch the workflow at
https://github.com/harshakavali81-collab/Generative-AI-Customer-Support-Analytics/actions/workflows/pages.yml

The app's Actions token previously returned `Resource not accessible by integration` when trying to create Pages automatically. This is a repository permission boundary, not an application-code error. The workflow is manual-only to keep normal source commits from producing misleading red deployment checks.

## Local Python/React operation

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m scripts.evaluate
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
# second terminal:
cd frontend && npm install && npm run dev
```

For a Docker run, configure secrets as environment variables before launching. Don't put credentials in frontend build files or commit an .env file.

## Required safety gates before public exposure

- TLS/HTTPS behind a trustworthy ingress and health checks.
- Real per-user authorization (OIDC/session), tenant isolation, and permission-scoped analytics. The demo's shared `CHAT_API_TOKEN` and `ADMIN_TOKEN` are only one-operator controls, **not** a production identity system.
- `ENVIRONMENT=production` refuses chat access without `CHAT_API_TOKEN` and analytics without `ADMIN_TOKEN`. A browser user entering a shared token should never be considered a customer login.
- External rate limiter, WAF, trusted proxy headers, CORS restricted to known domains, secure cookie/session configuration and secret storage.
- Reviewed retention schedule, data processing agreements and backup/restore process.
- Offline evaluation on approved real questions, answer-quality human sign-off, prompt injection red-teaming, threat model validation and disaster recovery drills.

No actual cloud service credentials, real customer integration or production approval are included in this repository.

## Full-stack smoke test in continuous integration

The quality pipeline builds and starts both container images in Docker Compose, waits for service health checks, requests the React index page through Nginx, checks the FastAPI health/index status through the reverse proxy, and submits a source-cited chat question. The verification runs against **fictional** local policies and a temporary SQLite volume; the volume is deleted after the test. See `.github/workflows/ci.yml`.

These checks confirm the containers work together in a short-lived GitHub Actions test environment. They do not constitute cloud deployment, scale/load testing, end-user authentication, disaster recovery, or external availability.
