from __future__ import annotations
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_fscore_support
from sklearn.neighbors import LocalOutlierFactor

SPIKES={
    "cpu":[45,92,137,161],
    "latency_ms":[92,137],
    "memory":[45,161],
}

def generate_demo_series(seed:int=42,points:int=180):
    rng=np.random.default_rng(seed)
    t=np.arange(points)
    cpu=42+8*np.sin(t/13)+rng.normal(0,3,points)
    latency=22+3*np.sin(t/9)+rng.normal(0,1.8,points)
    memory=61+4*np.sin(t/21)+rng.normal(0,2,points)
    cpu[SPIKES["cpu"]]=[94,97,91,99]
    latency[SPIKES["latency_ms"]]=[115,150]
    memory[SPIKES["memory"]]=[93,96]
    return {"cpu":cpu.round(2).tolist(),"latency_ms":latency.round(2).tolist(),"memory":memory.round(2).tolist()}

def _rows(values,pred,scores,truth=None):
    truth=set(truth or [])
    return [{"index":i,"value":round(float(v),3),"anomaly":bool(p),"score":round(float(s),4),"injected_anomaly":i in truth} for i,(v,p,s) in enumerate(zip(values,pred,scores))]

def isolation_forest(values:list[float],contamination:float=.04,truth=None):
    x=np.asarray(values,dtype=float).reshape(-1,1)
    model=IsolationForest(n_estimators=250,contamination=contamination,random_state=42)
    raw=model.fit_predict(x)
    scores=-model.score_samples(x)
    return _rows(values,raw==-1,scores,truth)

def local_outlier_factor(values:list[float],contamination:float=.04,truth=None):
    x=np.asarray(values,dtype=float).reshape(-1,1)
    model=LocalOutlierFactor(n_neighbors=min(20,max(5,len(values)//10)),contamination=contamination)
    raw=model.fit_predict(x)
    scores=-model.negative_outlier_factor_
    return _rows(values,raw==-1,scores,truth)

def robust_zscore(values:list[float],threshold:float=3.5,truth=None):
    x=np.asarray(values,dtype=float)
    median=float(np.median(x))
    mad=float(np.median(np.abs(x-median))) or 1e-9
    z=.6745*(x-median)/mad
    return _rows(values,np.abs(z)>threshold,np.abs(z),truth)

def detect(values:list[float],contamination:float=.04):
    return isolation_forest(values,contamination)

def evaluate(rows):
    y_true=[1 if r["injected_anomaly"] else 0 for r in rows]
    y_pred=[1 if r["anomaly"] else 0 for r in rows]
    precision,recall,f1,_=precision_recall_fscore_support(y_true,y_pred,average="binary",zero_division=0)
    return {"precision":round(float(precision),3),"recall":round(float(recall),3),"f1":round(float(f1),3),"detected":sum(y_pred),"expected":sum(y_true)}

def benchmark():
    series=generate_demo_series()
    totals={"isolation_forest":[],"local_outlier_factor":[],"robust_zscore":[]}
    by_metric={}
    for metric,values in series.items():
        truth=SPIKES[metric]
        results={
            "isolation_forest":isolation_forest(values,.04,truth),
            "local_outlier_factor":local_outlier_factor(values,.04,truth),
            "robust_zscore":robust_zscore(values,3.5,truth),
        }
        by_metric[metric]={name:evaluate(rows) for name,rows in results.items()}
        for name,rows in results.items():
            totals[name].extend(rows)
    overall={name:evaluate(rows) for name,rows in totals.items()}
    return {"dataset":"synthetic-demo","truth":"injected spikes","overall":overall,"by_metric":by_metric}

def analyze_demo():
    series=generate_demo_series()
    result={}
    for metric,values in series.items():
        rows=isolation_forest(values,.04,SPIKES[metric])
        result[metric]={"points":len(rows),"anomalies":sum(1 for r in rows if r["anomaly"]),"latest":rows[-1],"series":rows}
    return {"model":"IsolationForest","dataset":"synthetic-demo","note":"Synthetic metrics for portfolio demonstration; anomaly does not automatically mean incident.","metrics":result}
