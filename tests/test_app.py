from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"


def test_environment(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "test")
    response = client.get("/env")
    assert response.status_code == 200
    assert response.json()["environment"] == "test"

def test_config_lifecycle():
    name = "test_config"
    value = "test-value"

    response = client.post(
        "/config",
        json={"name": name, "value": value},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": name,
        "value": value,
    }

    response = client.get(f"/config/{name}")
    assert response.status_code == 200
    assert response.json() == {
        "name": name,
        "value": value,
    }

    response = client.delete(f"/config/{name}")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}

    response = client.get(f"/config/{name}")
    assert response.status_code == 404

def test_missing_config():
    response = client.get("/config/does-not-exist")
    assert response.status_code == 404
