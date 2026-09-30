from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from anomaly import analyze_demo, benchmark, detect
from zabbix_report import build_report

app=FastAPI(title="Zabbix AIOps Lab",version="4.0.0")

class SeriesIn(BaseModel):
    values:list[float]=Field(min_length=25,max_length=10000)
    contamination:float=Field(default=.04,gt=0,lt=.5)

@app.get("/",response_class=HTMLResponse)
def home():
    with open("frontend.html","r",encoding="utf-8") as f: return f.read()

@app.get("/health")
def health(): return {"status":"ok","version":"4.0.0","ml_model":"IsolationForest"}

@app.get("/report")
def report(): return build_report()

@app.get("/anomalies")
def anomalies(): return analyze_demo()

@app.get("/benchmark")
def anomaly_benchmark(): return benchmark()

@app.post("/anomalies/analyze")
def analyze(body:SeriesIn):
    rows=detect(body.values,body.contamination)
    return {"model":"IsolationForest","points":len(rows),"anomalies":sum(1 for r in rows if r["anomaly"]),"series":rows}
