from fastapi.testclient import TestClient
from web_app import app
client=TestClient(app)

def test_health():
    assert client.get("/health").status_code==200

def test_report_endpoint():
    assert client.get("/report").status_code==200
