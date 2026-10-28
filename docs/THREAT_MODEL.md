# Threat model for an educational support assistant

## Assets and trust boundaries
- Trusted local Markdown policies enter via a bounded allowlist loader. Only explicitly approved policy files should be indexed.
- User questions are untrusted; prompt injection and PII may be embedded in them.
- Optional remote LLM calls cross an external processing boundary and need an operator-managed key, policy and consent.
- SQLite stores event topics and anonymous feedback, not raw questions, but counts/length/timestamps may still reveal usage patterns.
- Browser/UI and backend cannot use one hard-coded shared token to establish per-user identity.

## Controls implemented in the prototype
- Small local-only document set, predictable identifiers, source-linked retrieval, minimum evidence gating and abstention.
- Question-length validation, obvious pattern-based PII checks, and suspicious instruction phrase handling.
- Fail-closed token checks for analytics and chat when running in production mode.
- Single-process, per-IP demonstration rate limiting, strict allowed CORS origin and security response headers.
- 30-day default event deletion at application startup and a manual admin cleanup endpoint.
- No persistence of raw question or generated answer text in SQLite; opt-in rating is stored as a boolean.

## Known vulnerabilities and out-of-scope safeguards
- The question regexes can miss PII, encoded numbers, injection variations, or adversarial documents.
- Lexical source match or a syntactically valid citation is not proof of factual entailment.
- Shared tokens and IP-based in-memory limits are **not suitable** as production authentication or abuse protection. Browser-side token entry is a local operator tool only.
- No robust per-tenant data isolation, managed key rotation, SSO, WAF, CSRF design, audit log pipeline, DLP scanning or external pentest.
- Source listing is deliberately public for fictional documents; real internal help-center documents require authorization.

## Next controls for a real deployment
Use a reviewed identity provider, least-privilege authorization, tenant-aware stores, full security and privacy review, a proper external rate-limiting layer, monitoring and proven backup/restore drills. Only process customer data with explicit business approval and an appropriate retention contract.
