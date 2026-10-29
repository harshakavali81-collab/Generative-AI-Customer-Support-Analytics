# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`CHANGELOG.md`](<../CHANGELOG.md>)
- [`CITATION.cff`](<../CITATION.cff>)
- [`CONTRIBUTING.md`](<../CONTRIBUTING.md>)
- [`LICENSE`](<../LICENSE>)
- [`README.md`](<../README.md>)
- [`SECURITY.md`](<../SECURITY.md>)
- [`backend`](<../backend>)
- [`backend/Dockerfile`](<../backend/Dockerfile>)
- [`backend/__init__.py`](<../backend/__init__.py>)
- [`backend/app`](<../backend/app>)
- [`backend/app/__init__.py`](<../backend/app/__init__.py>)
- [`backend/app/main.py`](<../backend/app/main.py>)
- [`data`](<../data>)
- [`data/source_docs`](<../data/source_docs>)
- [`data/source_docs/accounts.md`](<../data/source_docs/accounts.md>)
- [`data/source_docs/billing.md`](<../data/source_docs/billing.md>)
- [`data/source_docs/privacy.md`](<../data/source_docs/privacy.md>)
- [`data/source_docs/returns.md`](<../data/source_docs/returns.md>)
- [`data/source_docs/shipping.md`](<../data/source_docs/shipping.md>)
- [`data/source_docs/warranty.md`](<../data/source_docs/warranty.md>)
- [`docker-compose.yml`](<../docker-compose.yml>)
- [`docs`](<../docs>)
- [`docs/API_REFERENCE.md`](<../docs/API_REFERENCE.md>)
- [`docs/ARCHITECTURE.md`](<../docs/ARCHITECTURE.md>)
- [`docs/BROWSER_TESTING.md`](<../docs/BROWSER_TESTING.md>)
- [`docs/DATA_DICTIONARY.md`](<../docs/DATA_DICTIONARY.md>)
- [`docs/DEPLOYMENT.md`](<../docs/DEPLOYMENT.md>)
- [`docs/EVALUATION.md`](<../docs/EVALUATION.md>)
- [`docs/IMAGE_GALLERY.md`](<../docs/IMAGE_GALLERY.md>)
- [`docs/MODEL_CARD.md`](<../docs/MODEL_CARD.md>)
- [`docs/PORTFOLIO_CASE_STUDY.md`](<../docs/PORTFOLIO_CASE_STUDY.md>)
- [`docs/PROJECT_TREE.md`](<../docs/PROJECT_TREE.md>)
- [`docs/RUNBOOK.md`](<../docs/RUNBOOK.md>)
- [`docs/SECURITY.md`](<../docs/SECURITY.md>)
- [`docs/THREAT_MODEL.md`](<../docs/THREAT_MODEL.md>)
- [`docs/images`](<../docs/images>)
- [`docs/images/01-product-overview.svg`](<../docs/images/01-product-overview.svg>)
- [`docs/images/02-system-architecture.svg`](<../docs/images/02-system-architecture.svg>)
- [`docs/images/03-ingestion-pipeline.svg`](<../docs/images/03-ingestion-pipeline.svg>)
- [`docs/images/04-chunking-strategy.svg`](<../docs/images/04-chunking-strategy.svg>)
- [`docs/images/05-vector-retrieval.svg`](<../docs/images/05-vector-retrieval.svg>)
- [`docs/images/06-grounded-answer-flow.svg`](<../docs/images/06-grounded-answer-flow.svg>)
- [`docs/images/07-dashboard-preview.svg`](<../docs/images/07-dashboard-preview.svg>)
- [`docs/images/08-latency-trend.svg`](<../docs/images/08-latency-trend.svg>)
- [`docs/images/09-unanswered-report.svg`](<../docs/images/09-unanswered-report.svg>)
- [`docs/images/10-quality-and-privacy.svg`](<../docs/images/10-quality-and-privacy.svg>)
- [`evaluation`](<../evaluation>)
- [`evaluation/golden_questions.json`](<../evaluation/golden_questions.json>)
- [`frontend`](<../frontend>)
- [`frontend/Dockerfile`](<../frontend/Dockerfile>)
- [`frontend/index.html`](<../frontend/index.html>)
- [`frontend/nginx.conf`](<../frontend/nginx.conf>)
- [`frontend/package.json`](<../frontend/package.json>)
- [`frontend/src`](<../frontend/src>)
- [`frontend/src/App.jsx`](<../frontend/src/App.jsx>)
- [`frontend/src/components`](<../frontend/src/components>)
- [`frontend/src/components/Metric.jsx`](<../frontend/src/components/Metric.jsx>)
- [`frontend/src/main.jsx`](<../frontend/src/main.jsx>)
- [`frontend/src/pages`](<../frontend/src/pages>)
- [`frontend/src/pages/Analytics.jsx`](<../frontend/src/pages/Analytics.jsx>)
- [`frontend/src/pages/Chat.jsx`](<../frontend/src/pages/Chat.jsx>)
- [`frontend/src/styles.css`](<../frontend/src/styles.css>)
- [`frontend/vite.config.js`](<../frontend/vite.config.js>)
- [`requirements-dev.txt`](<../requirements-dev.txt>)
- [`requirements.txt`](<../requirements.txt>)
- [`scripts`](<../scripts>)
- [`scripts/__init__.py`](<../scripts/__init__.py>)
- [`scripts/benchmark.py`](<../scripts/benchmark.py>)
- [`scripts/browser_e2e.py`](<../scripts/browser_e2e.py>)
- [`scripts/build_index.py`](<../scripts/build_index.py>)
- [`scripts/check_assets.py`](<../scripts/check_assets.py>)
- [`scripts/evaluate.py`](<../scripts/evaluate.py>)
- [`scripts/smoke_test.py`](<../scripts/smoke_test.py>)
- [`site`](<../site>)
- [`site/app.js`](<../site/app.js>)
- [`site/index.html`](<../site/index.html>)
- [`site/policies.json`](<../site/policies.json>)
- [`site/styles.css`](<../site/styles.css>)
- [`sql`](<../sql>)
- [`sql/analytics.sql`](<../sql/analytics.sql>)
- [`src`](<../src>)
- [`src/__init__.py`](<../src/__init__.py>)
- [`src/analytics`](<../src/analytics>)
- [`src/analytics/__init__.py`](<../src/analytics/__init__.py>)
- [`src/analytics/metrics.py`](<../src/analytics/metrics.py>)
- [`src/chunking`](<../src/chunking>)
- [`src/chunking/__init__.py`](<../src/chunking/__init__.py>)
- [`src/chunking/split.py`](<../src/chunking/split.py>)
- [`src/embeddings`](<../src/embeddings>)
- [`src/embeddings/__init__.py`](<../src/embeddings/__init__.py>)
- [`src/embeddings/vectorizer.py`](<../src/embeddings/vectorizer.py>)
- [`src/generation`](<../src/generation>)
- [`src/generation/__init__.py`](<../src/generation/__init__.py>)
- [`src/generation/answer.py`](<../src/generation/answer.py>)
- [`src/guardrails`](<../src/guardrails>)
- [`src/guardrails/__init__.py`](<../src/guardrails/__init__.py>)
- [`src/guardrails/rules.py`](<../src/guardrails/rules.py>)
- [`src/ingestion`](<../src/ingestion>)
- [`src/ingestion/__init__.py`](<../src/ingestion/__init__.py>)
- [`src/ingestion/loader.py`](<../src/ingestion/loader.py>)
- [`src/retrieval`](<../src/retrieval>)
- [`src/retrieval/__init__.py`](<../src/retrieval/__init__.py>)
- [`src/retrieval/search.py`](<../src/retrieval/search.py>)
- [`src/vector_store`](<../src/vector_store>)
- [`src/vector_store/__init__.py`](<../src/vector_store/__init__.py>)
- [`src/vector_store/store.py`](<../src/vector_store/store.py>)
- [`tests`](<../tests>)
- [`tests/conftest.py`](<../tests/conftest.py>)
- [`tests/test_api.py`](<../tests/test_api.py>)
- [`tests/test_metrics.py`](<../tests/test_metrics.py>)
- [`tests/test_pipeline.py`](<../tests/test_pipeline.py>)
- [`tests/test_privacy_security.py`](<../tests/test_privacy_security.py>)
- [`tests/test_release_quality.py`](<../tests/test_release_quality.py>)
