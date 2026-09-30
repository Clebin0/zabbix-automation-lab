from fastapi.testclient import TestClient
from web_app import app
client=TestClient(app)

def test_health():
    r=client.get("/health")
    assert r.status_code==200
    assert r.json()["ml_model"]=="IsolationForest"

def test_anomalies_endpoint():
    r=client.get("/anomalies")
    assert r.status_code==200
    assert "metrics" in r.json()

def test_benchmark_endpoint():
    r=client.get("/benchmark")
    assert r.status_code==200
    assert "overall" in r.json()
