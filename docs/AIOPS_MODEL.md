# AIOps Model Notes

## Objective

Demonstrate unsupervised anomaly detection for infrastructure metrics without using proprietary monitoring data.

## Model

`IsolationForest` is applied independently to synthetic CPU, memory and latency series. The demo intentionally injects a few unusual spikes so the model output can be inspected.

## Why unsupervised?

Operational monitoring data often has many normal observations and few reliable incident labels. This lab explores anomaly detection without pretending a fully labeled corporate dataset exists.

## Limitations

- synthetic metrics
- fixed contamination used for demonstration
- no seasonality or maintenance windows
- no dependency topology
- no incident correlation
- anomaly does not automatically mean incident

Production use would require per-metric baselines, calibration, false-positive analysis, drift monitoring, maintenance context and human validation.
