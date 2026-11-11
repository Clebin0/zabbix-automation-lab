# Multi-agent architecture

## Goal

Add advisory agents to the existing Zabbix read-only observability lab. Preserve Demo as the default and preserve the current Live API's read-only contract.

## Roles

- **Observer**: reads hosts, problems, and metric series through existing read-only interfaces.
- **Anomaly analyst**: interprets outputs from Isolation Forest, LOF, and robust z-score; reports detector agreement and disagreement.
- **Correlation analyst**: groups observations by host, time window, and metric where data actually supports the relationship. No causal claims from correlation alone.
- **Incident summarizer**: produces a concise timeline, impact hypotheses, evidence, and missing data.
- **Runbook advisor**: recommends approved diagnostic steps; it does not execute them.

## Boundaries

- Agents cannot acknowledge/close problems, modify hosts, change thresholds, restart services, run commands, or call arbitrary URLs.
- Live mode requires an operator-owned Zabbix endpoint and least-privilege read-only token.
- A detected anomaly is a signal for investigation, not proof of an incident.
- Synthetic benchmark results must be labeled synthetic.

## Workflow

Read-only snapshot -> deterministic detectors -> anomaly interpretation -> correlation review -> incident summary -> human operator.

## Acceptance

Agent output identifies the source metric, host, timestamp/window, detector, severity rationale, uncertainty, and recommended next check. Missing evidence must be explicit. Existing API and detector results remain unchanged.
