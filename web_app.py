from __future__ import annotations

import logging
import math

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from anomaly import analyze_demo, benchmark, detect
from zabbix_report import build_report

logger = logging.getLogger(__name__)
app = FastAPI(title="Zabbix AIOps Lab", version="4.1.0")


class SeriesIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    values: list[float] = Field(min_length=25, max_length=10000)
    contamination: float = Field(default=0.04, gt=0, lt=0.5, allow_inf_nan=False)

    @field_validator("values")
    @classmethod
    def values_must_be_finite(cls, values: list[float]) -> list[float]:
        if not all(math.isfinite(value) for value in values):
            raise ValueError("All metric values must be finite numbers")
        return values


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
):
    # Do not echo invalid request values or pydantic context into the response.
    detail = [
        {
            "loc": list(error.get("loc", ())),
            "msg": str(error.get("msg", "Invalid input")),
            "type": str(error.get("type", "value_error")),
        }
        for error in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"detail": detail})


@app.get("/", response_class=HTMLResponse)
def home():
    with open("frontend.html", "r", encoding="utf-8") as file:
        return file.read()


@app.get("/health")
def health():
    return {"status": "ok", "version": "4.1.0", "ml_model": "IsolationForest"}


@app.get("/report")
def report():
    try:
        return build_report()
    except RuntimeError as exc:
        logger.warning("Zabbix report request failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="Zabbix API request failed. Check the server configuration and connectivity.",
        ) from exc


@app.get("/anomalies")
def anomalies():
    return analyze_demo()


@app.get("/benchmark")
def anomaly_benchmark():
    return benchmark()


@app.post("/anomalies/analyze")
def analyze(body: SeriesIn):
    rows = detect(body.values, body.contamination)
    return {
        "model": "IsolationForest",
        "points": len(rows),
        "anomalies": sum(1 for row in rows if row["anomaly"]),
        "series": rows,
    }
