import os

os.environ["ZABBIX_DEMO"] = "true"

from fastapi.testclient import TestClient

import web_app
from anomaly import analyze_demo, benchmark, detect
from web_app import app
from zabbix_report import build_report

client = TestClient(app)


def test_demo_report():
    data = build_report()
    assert data["mode"] == "demo"
    assert data["host_count"] >= 1


def test_isolation_forest_marks_anomalies():
    data = analyze_demo()
    assert data["model"] == "IsolationForest"
    assert data["metrics"]["cpu"]["anomalies"] >= 1


def test_benchmark_has_multiple_detectors():
    data = benchmark()
    assert {
        "isolation_forest",
        "local_outlier_factor",
        "robust_zscore",
    } <= data["overall"].keys()
    assert all(0 <= row["f1"] <= 1 for row in data["overall"].values())


def test_custom_series():
    values = [10.0] * 30 + [100.0]
    rows = detect(values, contamination=0.05)
    assert any(row["anomaly"] for row in rows)


def test_rejects_non_finite_values():
    body = '{"values":[' + ",".join(["10.0"] * 24 + ["NaN"]) + "]}"
    response = client.post(
        "/anomalies/analyze",
        content=body,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 422


def test_rejects_too_short_series():
    response = client.post(
        "/anomalies/analyze",
        json={"values": [10.0] * 24},
    )
    assert response.status_code == 422


def test_rejects_unknown_input_fields():
    response = client.post(
        "/anomalies/analyze",
        json={"values": [10.0] * 25, "debug": True},
    )
    assert response.status_code == 422


def test_zabbix_upstream_failure_is_sanitized(monkeypatch):
    def failed_report():
        raise RuntimeError("private upstream detail")

    monkeypatch.setattr(web_app, "build_report", failed_report)
    response = client.get("/report")
    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Zabbix API request failed. Check the server configuration and connectivity."
    )
    assert "private upstream detail" not in response.text
