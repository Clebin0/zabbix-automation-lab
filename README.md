# Zabbix AIOps Lab

Laboratório seguro que combina **automação da API Zabbix** com **detecção de anomalias usando Machine Learning**.

## Recursos

- cliente JSON-RPC para Zabbix
- modo demo com hosts e problemas fictícios
- dashboard FastAPI
- geração de séries sintéticas de CPU, memória e latência
- `IsolationForest` para detecção não supervisionada de anomalias
- anomaly score por ponto
- endpoint genérico para analisar séries numéricas
- testes e GitHub Actions
- Docker

## Por que Isolation Forest?

Em operações nem sempre existe um rótulo de "incidente" para cada ponto de métrica. Isolation Forest permite demonstrar detecção não supervisionada de observações raras sem fingir que existe um dataset corporativo rotulado.

## Executar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn web_app:app --reload
```

Abra `http://127.0.0.1:8000`.

## API

- `GET /report`
- `GET /anomalies`
- `POST /anomalies/analyze`
- `GET /health`

## Modo live

Defina `ZABBIX_DEMO=false`, `ZABBIX_URL` e `ZABBIX_TOKEN` somente para laboratório ou ambiente autorizado.

## Limitações

As séries incluídas são sintéticas. A contaminação e demais parâmetros não são defaults recomendados para produção. Um AIOps real exige histórico suficiente, sazonalidade, calibração por métrica, contexto operacional e avaliação de falso positivo.
