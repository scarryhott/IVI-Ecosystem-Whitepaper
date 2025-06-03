import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")
from fastapi.testclient import TestClient

from ivi.web import app


def test_dashboard_page():
    client = TestClient(app)
    res = client.get("/dashboard")
    assert res.status_code == 200
    assert "<html" in res.text.lower()


def test_login_stub():
    client = TestClient(app)
    # Send as JSON instead of form data
    res = client.post("/login", json={"id_token": "test_token"})
    assert res.status_code == 200
    assert "token" in res.json()

def test_evaluate_endpoint():
    client = TestClient(app)
    # Send as JSON instead of form data
    res = client.post("/evaluate", json={"idea_id": "x", "content": "ok"})
    assert res.status_code == 200
    assert "score" in res.json()
