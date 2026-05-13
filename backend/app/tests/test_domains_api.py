from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.domain import Domain
from app.services.report_store import ReportStore


def test_create_domain_adds_domain_to_store_and_database(
    client: TestClient,
    db_session: Session,
):
    response = client.post(
        "/api/v1/domains",
        json={"name": "Example.COM", "description": "Primary mail domain"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "example.com"
    assert data["description"] == "Primary mail domain"
    assert data["reports_count"] == 0
    assert "example.com" in ReportStore.get_instance().get_domains()

    domain = db_session.query(Domain).filter(Domain.name == "example.com").first()
    assert domain is not None
    assert domain.description == "Primary mail domain"
    assert domain.active is True


def test_create_domain_rejects_duplicate(client: TestClient):
    first = client.post("/api/v1/domains", json={"name": "example.com"})
    assert first.status_code == 201

    second = client.post("/api/v1/domains", json={"name": "example.com"})

    assert second.status_code == 409
    assert second.json()["detail"] == "Domain already exists"


def test_create_domain_rejects_invalid_domain(client: TestClient):
    response = client.post("/api/v1/domains", json={"name": "bad domain"})

    assert response.status_code == 422
    assert response.json()["detail"]["name"] == "Domain name cannot contain whitespace"
