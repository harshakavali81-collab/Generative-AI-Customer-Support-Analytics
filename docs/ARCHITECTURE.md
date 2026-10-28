# System architecture

![Architecture](images/02-system-architecture.svg)

## Document ingestion
Input is explicitly allowlisted local .md or .txt files, bounded to 256 KB each. The path scanner skips symbolic links and empty documents, and records source-relative paths and content checksums.

## Chunking and embeddings
A fixed 110-word window and 25-word overlap generate stable chunk IDs derived from document checksum, source path and start word. Pure Python TF-IDF sparse vectors are normalized and compared with cosine similarity. This is *lexical*, not pretrained semantic embedding; the latter would require an explicit change and evaluation.

## Retrieval
The query is normalized into the same vocabulary and ranked by cosine similarity. Up to four passages above the score floor are returned; unmatched queries abstain. Both the chunks and citation identifiers are carried through to the API.

## Answering
The default extractor chooses up to two well-matched sentences, using inline source IDs. This intentionally sacrifices conversational fluency for auditability. The optional remote LLM requires an environment flag and your own key; its output must contain IDs found among retrieved passages or fallback applies. Source ID validity is not factual entailment.

## Privacy and analytics
The API writes only metadata including topic, answered, elapsed time, source count, input length and UTC timestamp to SQLite. No query text is stored. An unanswered report groups broad topics rather than outputting raw private messages. A single-node SQLite database is not appropriate for high concurrency or multi-tenant production.

## API boundary
Development CORS is explicitly restricted to http://localhost:5173. Production deployments must configure HTTPS, per-user authentication and authorization, rate limiting, admin token, safe API secrets, CSRF/XSS reviews, backups and observability. `X-Admin-Token` is a simple educational gate and should be replaced with a server-verified identity system. In production, analytics deny access when token is not configured.
