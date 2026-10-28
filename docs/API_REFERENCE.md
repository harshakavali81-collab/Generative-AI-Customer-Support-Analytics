# SupportLens v1.1 API reference

See interactive OpenAPI docs on your local instance at `/docs`.

| Method | Route | Access | Response |
|---|---|---|---|
| GET | `/api/health` | Public | mode, number of chunks |
| GET | `/api/sources` | Public (fictional docs only) | list of source files |
| POST | `/api/chat` | Optional demo token; required in production mode | answer, citations, request ID, milliseconds |
| POST | `/api/feedback` | Same chat token | single anonymous helpful flag per response |
| GET | `/api/analytics` | Admin token if set; mandatory in production mode | counts, answer/feedback rates, topics and daily counts |
| GET | `/api/unanswered` | Admin | unanswered topic aggregates |
| GET | `/api/export/topics.csv` | Admin | topic count aggregates in CSV |
| POST | `/api/admin/retention-cleanup` | Admin | number of expired events deleted |

**Example chat request:**

```http
POST /api/chat HTTP/1.1
Content-Type: application/json

{"question": "How long do refunds take?"}
```

**Example response shape (IDs, timings vary):**

```json
{
  "answer": "Policy sentence. [source:<chunk ID>]",
  "answered": true,
  "citations": [{"id": "<chunk ID>", "source": "returns.md", "score": 0.4, "excerpt": "Policy excerpt"}],
  "latency_ms": 2,
  "request_id": "<32-character random identifier>",
  "mode": "offline-extractive"
}
```

Use `X-Chat-Token: <secret>` and `X-Admin-Token: <secret>` only when configured. Shared headers must be provided from a trusted client, not shipped embedded in public JavaScript.

**Feedback:** `{"request_id":"<returned ID>","helpful":true}`. A second rating for the same response returns HTTP 404; no message text is persisted. The API is synchronous and the current statistics are per single SQLite store, not cloud-wide metrics.
