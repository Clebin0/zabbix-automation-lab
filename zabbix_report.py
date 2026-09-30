from __future__ import annotations
import json, os
from datetime import datetime, timezone
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()
URL=os.getenv("ZABBIX_URL","")
TOKEN=os.getenv("ZABBIX_TOKEN","")
DEMO=os.getenv("ZABBIX_DEMO","true").lower()=="true"

def call(method,params):
    if DEMO:
        return demo_call(method)
    if not URL or not TOKEN:
        raise RuntimeError("Configure ZABBIX_URL and ZABBIX_TOKEN or enable ZABBIX_DEMO=true")
    payload={"jsonrpc":"2.0","method":method,"params":params,"id":1}
    headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json-rpc"}
    r=requests.post(URL,json=payload,headers=headers,timeout=15)
    r.raise_for_status()
    data=r.json()
    if "error" in data: raise RuntimeError(data["error"])
    return data["result"]

def demo_call(method):
    if method=="host.get":
        return [
          {"hostid":"10101","host":"LAB-SRV01","name":"Lab Server 01","interfaces":[{"ip":"192.0.2.10"}]},
          {"hostid":"10102","host":"LAB-PC01","name":"Lab Workstation 01","interfaces":[{"ip":"192.0.2.21"}]},
          {"hostid":"10103","host":"LAB-SW01","name":"Lab Switch 01","interfaces":[{"ip":"192.0.2.2"}]}
        ]
    if method=="problem.get":
        return [
          {"eventid":"9001","name":"High CPU utilization on LAB-SRV01","severity":"3","clock":"0"},
          {"eventid":"9002","name":"Packet loss detected on LAB-SW01","severity":"2","clock":"0"}
        ]
    return []

def build_report():
    hosts=call("host.get",{"output":["hostid","host","name"],"selectInterfaces":["ip"],"sortfield":"name"})
    problems=call("problem.get",{"output":"extend","recent":True,"sortfield":["eventid"],"sortorder":"DESC","limit":50})
    return {
      "generated_at":datetime.now(timezone.utc).isoformat(),
      "mode":"demo" if DEMO else "live",
      "host_count":len(hosts),
      "problem_count":len(problems),
      "hosts":hosts,
      "problems":problems
    }

def main():
    import argparse
    ap=argparse.ArgumentParser(description="Zabbix API reporting lab")
    ap.add_argument("--output",default="")
    args=ap.parse_args()
    report=build_report()
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if args.output:
        Path(args.output).write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")

if __name__=="__main__": main()
