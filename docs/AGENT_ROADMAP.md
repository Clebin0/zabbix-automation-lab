# Agent roadmap

1. Define common observation schema for hosts, problems, metrics, detector output, and provenance.
2. Add mocked tests for observer, anomaly analyst, and summarizer.
3. Add read-only Zabbix adapter with bounded query filters and server-side authorization.
4. Evaluate false-positive language and correlation claims using synthetic fixtures and labeled operator cases.
5. Add optional OpenClaw notifications only after identity mapping and channel allowlists exist.

No agent may alter Zabbix state or execute remediation commands in this project phase.
