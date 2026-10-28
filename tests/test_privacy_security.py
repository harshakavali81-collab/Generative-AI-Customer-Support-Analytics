"""Regression tests for privacy boundaries and admin/chat API controls."""
from datetime import datetime, timedelta, timezone
import os

import pytest
from fastapi.testclient import TestClient

import backend.app.main as service
from src.guardrails.rules import validate_question, topic
from src.analytics.metrics import connection, record, submit_feedback, summary, purge_old_events, aggregate_csv

@pytest.fixture
def app_client(tmp_path, monkeypatch):
    monkeypatch.setattr(service, "DB", tmp_path / "secure.sqlite3")
    monkeypatch.setenv("ENVIRONMENT", "development")
    monkeypatch.delenv("ADMIN_TOKEN", raising=False)
    monkeypatch.delenv("CHAT_API_TOKEN", raising=False)
    monkeypatch.delenv("RATE_LIMIT_PER_MINUTE", raising=False)
    with TestClient(service.app) as client:
        yield client

@pytest.mark.parametrize("input_text", [
    "My email is person@example.com please help",
    "The number is 4111111111111111 can I pay?",
    "My OTP is 123456, please log in",
])
def test_block_sensitive_inputs(input_text):
    with pytest.raises(ValueError, match="Remove personal details"):
        validate_question(input_text)

def test_no_pii_in_db_and_feedback_once(app_client):
    result = app_client.post("/api/chat", json={"question": "Where is the shipping tracking link?"})
    assert result.status_code == 200
    body = result.json()
    assert len(body["request_id"]) == 32
    with connection(service.DB) as db:
        columns = {r[1] for r in db.execute("PRAGMA table_info(events)")}
        assert "question" not in columns and "client_ip" not in columns
        assert db.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 1
    saved = app_client.post("/api/feedback", json={"request_id": body["request_id"], "helpful": True})
    assert saved.status_code == 200
    assert app_client.post("/api/feedback",json={"request_id":body["request_id"],"helpful":False}).status_code==404
    assert summary(service.DB)["helpful_pct"] == 100.0
    assert "question" not in aggregate_csv(service.DB)

def test_production_chat_fails_closed(app_client, monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.delenv("CHAT_API_TOKEN",raising=False)
    assert app_client.post("/api/chat",json={"question":"How do refunds work?"}).status_code==503
    monkeypatch.setenv("CHAT_API_TOKEN", "test-secret")
    assert app_client.post("/api/chat",json={"question":"How do refunds work?"}).status_code==403
    good=app_client.post("/api/chat",headers={"X-Chat-Token":"test-secret"},
                         json={"question":"How do refunds work?"})
    assert good.status_code==200
    assert good.headers["x-content-type-options"]=="nosniff"
    assert good.headers["cache-control"]=="no-store"

def test_admin_csv_and_retention(app_client, monkeypatch):
    monkeypatch.setenv("ADMIN_TOKEN","private-admin")
    assert app_client.get("/api/export/topics.csv").status_code==403
    headers={"X-Admin-Token":"private-admin"}
    assert app_client.get("/api/export/topics.csv", headers=headers).status_code==200
    assert "topic,question_count,unanswered_count" in app_client.get("/api/export/topics.csv",headers=headers).text
    assert app_client.post("/api/admin/retention-cleanup", headers=headers).status_code==200

def test_retention_purges_old_only(tmp_path):
    path=tmp_path/"events.db"
    request_id = record(path,"refund",True,20,1,23)
    with connection(path) as db:
        old=(datetime.now(timezone.utc)-timedelta(days=100)).isoformat()
        db.execute("UPDATE events SET created_at=? WHERE request_id=?",(old,request_id))
    record(path,"account",False,10,0,12)
    assert purge_old_events(path, days=30)==1
    assert summary(path)["total_questions"]==1
    with pytest.raises(ValueError):
        purge_old_events(path, days=0)

def test_demo_limiter(app_client, monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_PER_MINUTE","1")
    with service.bucket_lock:
        service.buckets.clear()
    a=app_client.post("/api/chat",json={"question":"How long is the warranty?"})
    b=app_client.post("/api/chat",json={"question":"How long is the warranty?"})
    assert a.status_code==200
    assert b.status_code==429
    assert b.headers["retry-after"]=="60"
    with service.bucket_lock:
        service.buckets.clear()

def test_sensitive_requests_are_not_logged(app_client):
    res=app_client.post("/api/chat",json={"question":"Contact me at person@example.com"})
    assert res.status_code==422
    assert app_client.get("/api/analytics").json()["total_questions"] == 0

def test_topic_plural_matching():
    assert topic("How do I get refunds?")=="refund"
