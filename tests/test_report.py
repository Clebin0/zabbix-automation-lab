import os
os.environ["ZABBIX_DEMO"]="true"
from anomaly import analyze_demo, benchmark, detect
from zabbix_report import build_report

def test_demo_report():
    data=build_report()
    assert data["mode"]=="demo"
    assert data["host_count"]>=1

def test_isolation_forest_marks_anomalies():
    data=analyze_demo()
    assert data["model"]=="IsolationForest"
    assert data["metrics"]["cpu"]["anomalies"]>=1

def test_benchmark_has_multiple_detectors():
    data=benchmark()
    assert {"isolation_forest","local_outlier_factor","robust_zscore"} <= data["overall"].keys()
    assert all(0 <= row["f1"] <= 1 for row in data["overall"].values())

def test_custom_series():
    values=[10.0]*30+[100.0]
    rows=detect(values,contamination=.05)
    assert any(r["anomaly"] for r in rows)
