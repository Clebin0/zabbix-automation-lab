import json, os
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
load_dotenv()
URL=os.getenv("ZABBIX_URL","")
TOKEN=os.getenv("ZABBIX_TOKEN","")

def call(method,params):
    if not URL or not TOKEN: raise RuntimeError("Configure ZABBIX_URL and ZABBIX_TOKEN")
    payload={"jsonrpc":"2.0","method":method,"params":params,"id":1}
    r=requests.post(URL,json=payload,headers={"Authorization":f"Bearer {TOKEN}","Content-Type":"application/json-rpc"},timeout=15)
    r.raise_for_status(); data=r.json()
    if "error" in data: raise RuntimeError(data["error"])
    return data["result"]

def main():
    hosts=call("host.get",{"output":["hostid","host","name"],"selectInterfaces":["ip"],"sortfield":"name"})
    problems=call("problem.get",{"output":"extend","recent":True,"sortfield":["eventid"],"sortorder":"DESC","limit":50})
    report={"generated_at":datetime.now(timezone.utc).isoformat(),"host_count":len(hosts),"problem_count":len(problems),"hosts":hosts,"problems":problems}
    print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=="__main__": main()
