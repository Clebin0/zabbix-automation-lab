import os

os.environ["ZABBIX_DEMO"] = "true"

from fastapi.testclient import TestClient

import web_app
from anomaly import analyze_demo, benchmark, detect
from web_app import app
from zabbix_report import build_report

client = TestClient(app)


def test_demo_report_uses_sample_hosts():
    report = build_report()

    assert report["mode"] == "demo"
    assert report["host_count"] >= 1
    assert report["problem_count"] >= 1
    assert report["hosts"][0]["host"].startswith("LAB-")


def test_isolation_forest_marks_injected_spikes():
    result = analyze_demo()

    assert result["model"] == "IsolationForest"
    assert result["metrics"]["cpu"]["anomalies"] >= 1


def test_benchmark_compares_three_methods():
    result = benchmark()

    assert {
        "isolation_forest",
        "local_outlier_factor",
        "robust_zscore",
    } <= result["overall"].keys()
    assert all(0 <= row["f1"] <= 1 for row in result["overall"].values())


def test_custom_series_detects_an_extreme_value():
    values = [10.0] * 30 + [100.0]
    rows = detect(values, contamination=0.05)

    assert any(row["anomaly"] for row in rows)


def test_api_rejects_non_finite_values():
    body = '{"values":[' + ",".join(["10.0"] * 24 + ["NaN"]) + "]}"
    response = client.post(
        "/anomalies/analyze",
        content=body,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 422


def test_api_rejects_series_that_is_too_short():
    response = client.post(
        "/anomalies/analyze",
        json={"values": [10.0] * 24},
    )

    assert response.status_code == 422


def test_api_rejects_unknown_fields():
    response = client.post(
        "/anomalies/analyze",
        json={"values": [10.0] * 25, "debug": True},
    )

    assert response.status_code == 422


def test_falha_no_zabbix_nao_expoe_detalhes_internos(monkeypatch):
    def failed_report():
        raise RuntimeError("private upstream detail")

    monkeypatch.setattr(web_app, "build_report", failed_report)
    response = client.get("/report")

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "A consulta ao Zabbix falhou. Verifique a configuração e a conectividade."
    )
    assert "private upstream detail" not in response.text
