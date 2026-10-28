# Security policy

This is a fictional educational portfolio application and is not suitable for live customer support without a formal security review.

For vulnerabilities, do not publish passwords, API keys, personal information or exploit details in public issues. Use the repository's private vulnerability reporting (if enabled) or contact the repository maintainer privately.

Security notes: [Threat model](docs/THREAT_MODEL.md), [deployment safety gates](docs/DEPLOYMENT.md), [data dictionary](docs/DATA_DICTIONARY.md).

Known prototype limitations: token-based single-operator gates, basic PII patterns, optional external LLM, single-process rate limiting, SQLite storage and missing enterprise authentication/tenant isolation.
