"""API-тесты без сети: TestClient."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

PAYLOAD = {
    "idea": "CRM for dentists",
    "market_size": "large",
    "team_size": 4,
    "paying_users": 12,
    "competitors": 3,
}


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def test_health(client: TestClient) -> None:
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_criteria(client: TestClient) -> None:
    resp = client.get("/api/v1/criteria")
    assert resp.status_code == 200
    assert set(resp.json()["criteria"]) == {"market", "team", "traction", "competition"}


def test_analyze(client: TestClient) -> None:
    resp = client.post("/api/v1/analyze", json=PAYLOAD)
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["total"] == 95
    assert payload["verdict"] == "fundable"


def test_analyze_rejects_bad_market(client: TestClient) -> None:
    bad = dict(PAYLOAD, market_size="cosmic")
    resp = client.post("/api/v1/analyze", json=bad)
    assert resp.status_code == 422


@pytest.mark.integration()
def test_analyze_risky_shape(client: TestClient) -> None:
    """Интеграционный по маркеру: слабый кейс, без сети."""
    resp = client.post(
        "/api/v1/analyze",
        json={"idea": "Yet another chat", "market_size": "niche", "team_size": 1, "paying_users": 0, "competitors": 50},
    )
    assert resp.status_code == 200
    assert resp.json()["verdict"] == "risky"
