"""Privacy-minimal SQLite event metrics; no raw question text stored."""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    topic TEXT NOT NULL,
    answered INTEGER NOT NULL CHECK(answered IN (0,1)),
    latency_ms INTEGER NOT NULL,
    source_count INTEGER NOT NULL,
    question_length INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(created_at);
CREATE INDEX IF NOT EXISTS idx_events_topic ON events(topic,answered);
"""

def connection(path: str | Path):
    target = str(path)
    if target != ":memory:":
        Path(target).parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(target, timeout=5)
    db.executescript(SCHEMA)
    return db

def record(path, subject: str, answered: bool, latency_ms: int, source_count: int, question_length: int):
    with connection(path) as db:
        db.execute("INSERT INTO events(created_at,topic,answered,latency_ms,source_count,question_length) VALUES(?,?,?,?,?,?)",
                   (datetime.now(timezone.utc).isoformat(), subject, int(answered),
                    max(0, latency_ms), source_count, question_length))

def summary(path) -> dict:
    with connection(path) as db:
        row = db.execute("SELECT COUNT(*),COALESCE(ROUND(AVG(answered)*100,1),0),COALESCE(ROUND(AVG(latency_ms),1),0),SUM(CASE WHEN answered=0 THEN 1 ELSE 0 END) FROM events").fetchone()
        topics = db.execute("SELECT topic,COUNT(*) AS total,SUM(CASE WHEN answered=0 THEN 1 ELSE 0 END) AS unanswered FROM events GROUP BY topic ORDER BY total DESC").fetchall()
        days = db.execute("SELECT SUBSTR(created_at,1,10) AS day,COUNT(*) AS total FROM events GROUP BY day ORDER BY day DESC LIMIT 14").fetchall()
    return {"total_questions": row[0], "answer_rate_pct": row[1], "average_latency_ms": row[2],
            "unanswered": row[3] or 0, "topics": [{"topic":a,"total":b,"unanswered":c} for a,b,c in topics],
            "daily": [{"date":a,"total":b} for a,b in reversed(days)]}

def unanswered_report(path) -> list[dict]:
    with connection(path) as db:
        rows = db.execute("SELECT topic, COUNT(*) FROM events WHERE answered=0 GROUP BY topic ORDER BY COUNT(*) DESC,topic").fetchall()
    return [{"topic":t,"count":c} for t,c in rows]
