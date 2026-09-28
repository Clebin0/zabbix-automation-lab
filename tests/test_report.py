import os
os.environ["ZABBIX_DEMO"]="true"
from zabbix_report import build_report

def test_demo_report():
    data=build_report()
    assert data["mode"]=="demo"
    assert data["host_count"]>=1
    assert "problems" in data
