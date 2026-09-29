from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_log_metric():
    payload = {"metric_type": "HbA1c", "value": "5.7%"}
    response = client.post("/api/v1/clients/cli_001/metrics", json=payload)
    assert response.status_code == 200
    assert len(response.json()["metrics"]) == 1

def test_get_metrics_not_found():
    response = client.get("/api/v1/clients/cli_nonexistent/metrics")
    assert response.status_code == 404