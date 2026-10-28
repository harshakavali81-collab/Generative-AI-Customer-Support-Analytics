# Developer operations runbook

## Start

`docker compose up --build`; open http://localhost:8080. API: http://localhost:8080/api/health. Default docs and all policies are fictional.

## Basic checks

```bash
python -m pytest -q
python -m scripts.evaluate
python -m scripts.smoke_test
cd frontend && npm install && npm run build
```

In Docker: `docker compose logs --tail 100 api` (never print environment secrets). `docker compose ps` checks service state.

## Typical incidents

- **HTTP 503 /api/chat:** `ENVIRONMENT=production` but `CHAT_API_TOKEN` is not configured. Supply a securely managed token or use local development mode.
- **HTTP 403:** incorrect chat/admin token. Do not embed a shared secret in a publicly distributed JS bundle.
- **HTTP 429:** demonstration IP rate limiter triggered. Wait for the sliding 60-second window; configure production ingress enforcement separately.
- **HTTP 422:** empty/oversized question or apparent sensitive details. Ask the user to redact information; do not log their rejected input.
- **No citations / abstention:** documentation did not support answer under the current lexical retrieval/extractive thresholds. Improve approved policy documents and rerun fixtures; do not simply lower thresholds to force an answer.
- **SQLite locked:** stop competing processes or migrate persistent telemetry to a properly managed SQL service before scale. The demo uses `busy_timeout`, not distributed locks.
- **GitHub Pages deployment 403:** visit repository Settings > Pages, select GitHub Actions as build source. Source-repository workflow does not have permission to activate Pages on its own. The demo is also mirrored in the portfolio repository.

## Backups, retention and recovery

Store `instance/` outside GitHub. Export only aggregate counts via authenticated `/api/export/topics.csv`. SQLite must be backed up with its official online-backup API or a consistent snapshot, not an unsynchronized raw file copy under heavy writes. Run `POST /api/admin/retention-cleanup` periodically; startup also deletes entries older than `EVENT_RETENTION_DAYS` (30 default). An operator must separately manage volume storage, encryption, scheduled backups and restoration verification.

## User-impact policy

No real customer data or approval workflows are provided. All examples and claims should be labeled fictional. Human escalation is a message only, not a connected ticketing integration.
