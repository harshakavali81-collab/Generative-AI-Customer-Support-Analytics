# Security and responsible-use boundaries

- **Do not upload real customer conversations** to the fictional demo.
- The raw question is processed in memory and is not written to the analytics database. Topics and lengths may still be sensitive in some deployments; define retention and controls.
- `OPENAI_API_KEY` is a secret. Never commit it. Remote LLM mode may transmit questions to OpenAI, require consent and incur costs; it is **off** by default.
- The optional LLM cannot be considered hallucination-free: valid citation tokens do not guarantee evidence entails a claim.
- Suspicious obvious prompt-injection phrases cause refusal; real attacks may evade these filters. Do not assume production protection.
- Admin analytics endpoints require `ADMIN_TOKEN` when configured; production mode fails closed if it is absent, but chat and source listing remain public and need independent authentication/rate limiting before public release.
- Add identity, least-privilege roles, transport encryption, audit procedures, deletion policy, secret rotation, content validation and periodic security reviews before deployment to real users.
- Do not accept user-provided arbitrary file paths for ingestion. Future file uploads need malware scanning and tenant isolation.
