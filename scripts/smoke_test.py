"""Run local in-process API smoke checks without a listening server."""
import json
import os
from fastapi.testclient import TestClient
from backend.app.main import app

if __name__ == "__main__":
    if os.getenv("ENVIRONMENT", "development") == "production":
        raise SystemExit("Do not run development smoke checks against a production configuration")
    with TestClient(app) as client:
        health = client.get("/api/health")
        health.raise_for_status()
        chat = client.post("/api/chat", json={"question": "How long do refunds take?"})
        chat.raise_for_status()
        payload = chat.json()
        assert payload["answered"] and payload["citations"], "Expected a supported cited refund answer"
        assert "source:" in payload["answer"]
        feedback = client.post("/api/feedback",json={"request_id":payload["request_id"],"helpful":True})
        feedback.raise_for_status()
        analytics = client.get("/api/analytics")
        analytics.raise_for_status()
        assert analytics.json()["total_questions"] >= 1
        print(json.dumps({"health": health.json(), "chat_cited": True,
                          "feedback_saved": feedback.json()["saved"],
                          "analytics_events": analytics.json()["total_questions"]}, indent=2))
