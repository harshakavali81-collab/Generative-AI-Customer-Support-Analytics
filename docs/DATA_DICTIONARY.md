# Minimal analytics dictionary

SQLite table `events` is in `src/analytics/metrics.py`.

| Column | Type | Description | Sensitive considerations |
|---|---|---|---|
| id | integer | internal row identity | avoid exposing publicly |
| created_at | UTC ISO string | event time | usage pattern metadata |
| topic | controlled text | broad keyword-based support category | may reveal broad interests |
| answered | boolean integer | extractor returned a supported answer | may not imply correctness |
| latency_ms | integer | processing time measured inside API | not network latency |
| source_count | integer | number of retrieved evidence chunks | not proof of answer quality |
| question_length | integer | number of characters, not question text | potential metadata leakage |
| request_id | random 32-char token | correlates voluntary feedback once | short-lived pseudonymous handle |
| feedback | null/0/1 | null=unrated, 0=not helpful, 1=helpful | not satisfaction ground truth |

`/api/analytics` returns aggregate metrics; `/api/unanswered` and `/api/export/topics.csv` expose only broad topic counts. A review for data minimization is still required for real customer traffic.

**Not stored:** raw question, response text, full citations, email, phone, credit-card number, user account identifier or client IP in the SQLite event table.

Retention is configurable via `EVENT_RETENTION_DAYS` (default 30). Cleanup runs at startup and can be triggered by an admin. Operators should configure periodic cleanup for long-running services.
