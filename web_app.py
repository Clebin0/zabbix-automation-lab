from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from zabbix_report import build_report

app=FastAPI(title="Zabbix Automation Lab",version="2.0.0")

@app.get("/",response_class=HTMLResponse)
def home():
    with open("frontend.html","r",encoding="utf-8") as f: return f.read()

@app.get("/health")
def health(): return {"status":"ok","version":"2.0.0"}

@app.get("/report")
def report(): return build_report()
