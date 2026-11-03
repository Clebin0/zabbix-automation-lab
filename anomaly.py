from __future__ import annotations

import math

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_fscore_support
from sklearn.neighbors import LocalOutlierFactor

SPIKES = {
    "cpu": [45, 92, 137, 161],
    "latency_ms": [92, 137],
    "memory": [45, 161],
}


def _validated_array(values: list[float], minimum: int = 25) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1:
        raise ValueError("Metric series must be one-dimensional")
    if len(array) < minimum:
        raise ValueError(f"Metric series must contain at least {minimum} points")
    if not np.isfinite(array).all():
        raise ValueError("Metric series must contain only finite numbers")
    return array


def generate_demo_series(seed: int = 42, points: int = 180):
    rng = np.random.default_rng(seed)
    t = np.arange(points)
    cpu = 42 + 8 * np.sin(t / 13) + rng.normal(0, 3, points)
    latency = 22 + 3 * np.sin(t / 9) + rng.normal(0, 1.8, points)
    memory = 61 + 4 * np.sin(t / 21) + rng.normal(0, 2, points)
    cpu[SPIKES["cpu"]] = [94, 97, 91, 99]
    latency[SPIKES["latency_ms"]] = [115, 150]
    memory[SPIKES["memory"]] = [93, 96]
    return {
        "cpu": cpu.round(2).tolist(),
        "latency_ms": latency.round(2).tolist(),
        "memory": memory.round(2).tolist(),
    }


def _rows(values, pred, scores, truth=None):
    truth = set(truth or [])
    return [
        {
            "index": index,
            "value": round(float(value), 3),
            "anomaly": bool(prediction),
            "score": round(float(score), 4),
            "injected_anomaly": index in truth,
        }
        for index, (value, prediction, score) in enumerate(zip(values, pred, scores))
    ]


def isolation_forest(values: list[float], contamination: float = 0.04, truth=None):
    array = _validated_array(values)
    if not math.isfinite(contamination) or not 0 < contamination < 0.5:
        raise ValueError("contamination must be greater than 0 and less than 0.5")
    model = IsolationForest(
        n_estimators=250,
        contamination=contamination,
        random_state=42,
    )
    raw = model.fit_predict(array.reshape(-1, 1))
    scores = -model.score_samples(array.reshape(-1, 1))
    return _rows(array, raw == -1, scores, truth)


def local_outlier_factor(values: list[float], contamination: float = 0.04, truth=None):
    array = _validated_array(values)
    if not math.isfinite(contamination) or not 0 < contamination < 0.5:
        raise ValueError("contamination must be greater than 0 and less than 0.5")
    x = array.reshape(-1, 1)
    model = LocalOutlierFactor(
        n_neighbors=min(20, max(5, len(array) // 10)),
        contamination=contamination,
    )
    raw = model.fit_predict(x)
    scores = -model.negative_outlier_factor_
    return _rows(array, raw == -1, scores, truth)


def robust_zscore(values: list[float], threshold: float = 3.5, truth=None):
    array = _validated_array(values)
    if not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("threshold must be a positive finite number")
    median = float(np.median(array))
    mad = float(np.median(np.abs(array - median))) or 1e-9
    z_score = 0.6745 * (array - median) / mad
    return _rows(array, np.abs(z_score) > threshold, np.abs(z_score), truth)


def detect(values: list[float], contamination: float = 0.04):
    return isolation_forest(values, contamination)


def evaluate(rows):
    y_true = [1 if row["injected_anomaly"] else 0 for row in rows]
    y_pred = [1 if row["anomaly"] else 0 for row in rows]
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="binary",
        zero_division=0,
    )
    return {
        "precision": round(float(precision), 3),
        "recall": round(float(recall), 3),
        "f1": round(float(f1), 3),
        "detected": sum(y_pred),
        "expected": sum(y_true),
    }


def benchmark():
    series = generate_demo_series()
    totals = {
        "isolation_forest": [],
        "local_outlier_factor": [],
        "robust_zscore": [],
    }
    by_metric = {}

    for metric, values in series.items():
        truth = SPIKES[metric]
        results = {
            "isolation_forest": isolation_forest(values, 0.04, truth),
            "local_outlier_factor": local_outlier_factor(values, 0.04, truth),
            "robust_zscore": robust_zscore(values, 3.5, truth),
        }
        by_metric[metric] = {
            name: evaluate(rows) for name, rows in results.items()
        }
        for name, rows in results.items():
            totals[name].extend(rows)

    overall = {name: evaluate(rows) for name, rows in totals.items()}
    return {
        "dataset": "synthetic-demo",
        "truth": "injected spikes",
        "overall": overall,
        "by_metric": by_metric,
    }


def analyze_demo():
    series = generate_demo_series()
    result = {}
    for metric, values in series.items():
        rows = isolation_forest(values, 0.04, SPIKES[metric])
        result[metric] = {
            "points": len(rows),
            "anomalies": sum(1 for row in rows if row["anomaly"]),
            "latest": rows[-1],
            "series": rows,
        }
    return {
        "model": "IsolationForest",
        "dataset": "synthetic-demo",
        "note": (
            "Synthetic metrics for portfolio demonstration; "
            "anomaly does not automatically mean incident."
        ),
        "metrics": result,
    }
