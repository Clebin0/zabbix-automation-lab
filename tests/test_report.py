import os
os.environ["ZABBIX_DEMO"]="true"
from anomaly import analyze_demo, detect
from zabbix_report import build_report

def test_demo_report():
    data=build_report()
    assert data["mode"]=="demo"
    assert data["host_count"]>=1

def test_anomaly_model_finds_points():
    data=analyze_demo()
    assert data["model"]=="IsolationForest"
    assert data["metrics"]["cpu"]["anomalies"]>=1

def test_custom_series():
    values=[10.0]*30+[100.0]
    rows=detect(values,contamination=.05)
    assert any(r["anomaly"] for r in rows)
