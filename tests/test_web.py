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
    res = client.post("/login", data={"id_token": "invalid"})
    assert res.status_code == 200
    assert "status" in res.json()


def test_evaluate_endpoint():
    client = TestClient(app)
    res = client.post("/evaluate", data={"idea_id": "x", "content": "ok"})
    assert res.status_code == 200
    assert "score" in res.json()


def test_interactions_endpoint():
    client = TestClient(app)
    res = client.post(
        "/interactions",
        data={"idea_id": "x", "user": "bob", "description": "note"},
    )
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
=======
