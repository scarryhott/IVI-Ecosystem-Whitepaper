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
    # Use id_token as the parameter name
    res = client.post("/login?id_token=test_token")
    print(f"Login response: {res.status_code}, {res.json()}")
    assert res.status_code == 200
    assert "status" in res.json()
    
def test_evaluate_endpoint():
    client = TestClient(app)
    # Send as query parameters
    res = client.post("/evaluate?idea_id=x&content=ok")
    print(f"Evaluate response: {res.status_code}, {res.json()}")
    assert res.status_code == 200
    assert "score" in res.json()
