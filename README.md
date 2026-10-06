<div align="center">

# Zabbix AIOps Lab

**Observabilidade · Anomaly Detection · FastAPI · Zabbix API**

<img src="https://img.shields.io/badge/Python-000000?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Zabbix-000000?style=for-the-badge&logo=zabbix&logoColor=white" alt="Zabbix" />
<img src="https://img.shields.io/badge/scikit--learn-000000?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="scikit-learn" />
<img src="https://img.shields.io/badge/FastAPI-000000?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />

</div>

---

Laboratório que combina automação da API Zabbix com detecção e avaliação de anomalias em métricas sintéticas.

## O que demonstra

- cliente JSON-RPC para Zabbix;
- modo demo sem credenciais corporativas;
- dashboard FastAPI;
- séries sintéticas de CPU, memória e latência;
- Isolation Forest como detector principal;
- comparação com Local Outlier Factor e robust z-score;
- precision, recall e F1 contra spikes conhecidos;
- visualização de séries e pontos sinalizados.

## Por que comparar detectores?

Encontrar pontos diferentes não significa detectar melhor. Como o laboratório injeta spikes conhecidos, os detectores podem ser comparados contra uma verdade sintética controlada.

## Executar

~~~bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn web_app:app --reload
~~~

## API

- <code>GET /report</code>
- <code>GET /anomalies</code>
- <code>GET /benchmark</code>
- <code>POST /anomalies/analyze</code>
- <code>GET /health</code>

## Modo live

Use <code>ZABBIX_DEMO=false</code>, <code>ZABBIX_URL</code> e <code>ZABBIX_TOKEN</code> somente em infraestrutura autorizada. Prefira token read-only e menor privilégio.

## Limitações

Os dados são sintéticos. Em produção seria necessário considerar sazonalidade, manutenção, topologia, mudança de baseline e falsos positivos por métrica.

---

<div align="center">

Laboratório de observabilidade e AIOps com foco em avaliação, não só em gráficos bonitos.

</div>
