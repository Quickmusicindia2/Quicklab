from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_project():
    response = client.post("/api/v1/projects", json={"name": "Demo", "description": "Test project"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["name"] == "Demo"
    assert payload["status"] == "created"
