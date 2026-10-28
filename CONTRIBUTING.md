# Contributing

1. Make a feature branch from `main`.
2. Do not add genuine customer records, credentials, identity documents or production policy documents.
3. Use synthetic test fixtures and describe their limits.
4. Prefer adding a focused regression test for every parser, answer, analytics or security change.
5. Run `python -m pip install -r requirements-dev.txt`, `python -m pytest -q`, `python -m scripts.evaluate`, `python -m scripts.smoke_test`, and `cd frontend && npm install && npm run build`.
6. Never label a generated illustration a measured benchmark. Distinguish lexical retrieval hit rate from generated answer accuracy.
7. Include updated API docs, security notes and user-facing limitations as needed. Avoid sending private data to remote LLMs without documented authorization.

Pull requests should explain the technical change, link tests, and note any effect on source citations or telemetry privacy. AI-generated content must be tested and reviewed before merge.
