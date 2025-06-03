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
