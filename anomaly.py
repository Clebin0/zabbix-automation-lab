from __future__ import annotations
import numpy as np
from sklearn.ensemble import IsolationForest

def generate_demo_series(seed:int=42,points:int=180):
    rng=np.random.default_rng(seed)
    t=np.arange(points)
    cpu=42+8*np.sin(t/13)+rng.normal(0,3,points)
    latency=22+3*np.sin(t/9)+rng.normal(0,1.8,points)
    memory=61+4*np.sin(t/21)+rng.normal(0,2,points)
    spikes=[45,92,137,161]
    cpu[spikes]=[94,97,91,99]
    latency[[92,137]]=[115,150]
    memory[[45,161]]=[93,96]
    return {
      "cpu":cpu.round(2).tolist(),
      "latency_ms":latency.round(2).tolist(),
      "memory":memory.round(2).tolist(),
    }

def detect(values:list[float],contamination:float=.04):
    x=np.asarray(values,dtype=float).reshape(-1,1)
    model=IsolationForest(n_estimators=200,contamination=contamination,random_state=42)
    pred=model.fit_predict(x)
    scores=-model.score_samples(x)
    rows=[]
    for i,(value,label,score) in enumerate(zip(values,pred,scores)):
        rows.append({"index":i,"value":round(float(value),3),"anomaly":bool(label==-1),"score":round(float(score),4)})
    return rows

def analyze_demo():
    series=generate_demo_series()
    result={}
    for metric,values in series.items():
        rows=detect(values)
        result[metric]={
          "points":len(rows),
          "anomalies":sum(1 for r in rows if r["anomaly"]),
          "latest":rows[-1],
          "series":rows,
        }
    return {
      "model":"IsolationForest",
      "dataset":"synthetic-demo",
      "note":"Synthetic metrics for portfolio demonstration; thresholds are not production defaults.",
      "metrics":result,
    }
