"""Privacy-minimal SQLite telemetry, voluntary feedback, and configurable retention."""
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    topic TEXT NOT NULL,
    answered INTEGER NOT NULL CHECK(answered IN (0,1)),
    latency_ms INTEGER NOT NULL,
    source_count INTEGER NOT NULL,
    question_length INTEGER NOT NULL,
    request_id TEXT UNIQUE,
    feedback INTEGER CHECK(feedback IN (0,1))
);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(created_at);
CREATE INDEX IF NOT EXISTS idx_events_topic ON events(topic,answered);
"""

def connection(path: str | Path):
    target = str(path)
    if target != ":memory:":
        Path(target).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(target, timeout=5)
    db.execute("PRAGMA busy_timeout=5000")
    db.executescript(SCHEMA)
    # Non-destructive migration for existing prototype databases.
    names = {row[1] for row in db.execute("PRAGMA table_info(events)")}
    if "request_id" not in names:
        db.execute("ALTER TABLE events ADD COLUMN request_id TEXT")
    if "feedback" not in names:
        db.execute("ALTER TABLE events ADD COLUMN feedback INTEGER CHECK(feedback IN (0,1))")
    db.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_events_request ON events(request_id)")
    return db

def record(path, subject: str, answered: bool, latency_ms: int,
           source_count: int, question_length: int) -> str:
    """Store no raw prompt, response, client IP or account identifier."""
    identifier = uuid.uuid4().hex
    with connection(path) as db:
        db.execute(
            "INSERT INTO events(created_at,topic,answered,latency_ms,source_count,question_length,request_id)"
            " VALUES(?,?,?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(), subject, int(answered),
             max(0, int(latency_ms)), source_count, question_length, identifier))
    return identifier

def submit_feedback(path, request_id: str, helpful: bool) -> bool:
    """One anonymous rating per random chat ID. No arbitrary query/prompt fields."""
    if len(request_id) != 32 or any(c not in "0123456789abcdef" for c in request_id):
        return False
    with connection(path) as db:
        cur = db.execute(
            "UPDATE events SET feedback = ? WHERE request_id = ? AND feedback IS NULL",
            (int(helpful), request_id))
    return cur.rowcount == 1

def purge_old_events(path, days: int = 30, now: datetime | None = None) -> int:
    if not 1 <= days <= 3650:
        raise ValueError("Retention must be between 1 and 3650 days")
    cutoff = (now or datetime.now(timezone.utc)) - timedelta(days=days)
    with connection(path) as db:
        cur = db.execute("DELETE FROM events WHERE created_at < ?", (cutoff.isoformat(),))
    return cur.rowcount

def summary(path) -> dict:
    with connection(path) as db:
        row = db.execute("""
            SELECT COUNT(*),
                   COALESCE(ROUND(AVG(answered)*100,1),0),
                   COALESCE(ROUND(AVG(latency_ms),1),0),
                   COALESCE(SUM(CASE WHEN answered=0 THEN 1 ELSE 0 END),0),
                   COALESCE(SUM(CASE WHEN feedback IS NOT NULL THEN 1 ELSE 0 END),0),
                   COALESCE(ROUND(100.0*AVG(feedback),1),0)
            FROM events
        """).fetchone()
        topics = db.execute("""
            SELECT topic,COUNT(*) AS total,
                   SUM(CASE WHEN answered=0 THEN 1 ELSE 0 END) AS unanswered
            FROM events GROUP BY topic ORDER BY total DESC
        """).fetchall()
        days = db.execute("""
            SELECT SUBSTR(created_at,1,10) AS day,COUNT(*) AS total
            FROM events GROUP BY day ORDER BY day DESC LIMIT 14
        """).fetchall()
    return {
        "total_questions": row[0], "answer_rate_pct": row[1],
        "average_latency_ms": row[2], "unanswered": row[3],
        "feedback_count": row[4], "helpful_pct": row[5],
        "topics": [{"topic": a, "total": b, "unanswered": c} for a,b,c in topics],
        "daily": [{"date": a, "total": b} for a,b in reversed(days)]
    }

def unanswered_report(path) -> list[dict]:
    with connection(path) as db:
        rows = db.execute("""
            SELECT topic, COUNT(*) FROM events WHERE answered=0
            GROUP BY topic ORDER BY COUNT(*) DESC,topic
        """).fetchall()
    return [{"topic":t,"count":c} for t,c in rows]

def aggregate_csv(path) -> str:
    """Export aggregate counts by topic, never the event table."""
    import csv
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["topic", "question_count", "unanswered_count"])
    with connection(path) as db:
        for row in db.execute("""
            SELECT topic,COUNT(*),SUM(CASE WHEN answered=0 THEN 1 ELSE 0 END)
            FROM events GROUP BY topic ORDER BY topic
        """):
            writer.writerow(row)
    return output.getvalue()
