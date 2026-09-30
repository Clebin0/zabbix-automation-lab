# Zabbix AIOps Lab

Laboratório seguro que combina automação da API Zabbix com detecção e avaliação de anomalias em métricas sintéticas.

## O que o projeto demonstra

- cliente JSON-RPC para Zabbix;
- modo demo sem credenciais corporativas;
- dashboard FastAPI;
- séries sintéticas de CPU, memória e latência;
- Isolation Forest como detector principal;
- comparação com Local Outlier Factor e robust z-score;
- precision, recall e F1 contra spikes conhecidos do dataset sintético;
- visualização das séries e dos pontos sinalizados.

## Por que comparar detectores?

Um detector de anomalia não é automaticamente bom só porque encontra pontos diferentes. Como o laboratório injeta spikes conhecidos, conseguimos comparar os detectores contra uma verdade sintética controlada.

Isso ainda não representa produção. Em ambiente real seria necessário considerar sazonalidade, janelas de manutenção, topologia, mudança de baseline e falso positivo por métrica.

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
- `GET /benchmark`
- `POST /anomalies/analyze`
- `GET /health`

## Modo live

Defina `ZABBIX_DEMO=false`, `ZABBIX_URL` e `ZABBIX_TOKEN` somente para laboratório ou infraestrutura autorizada. Prefira token read-only e menor privilégio.

## Limitações

Os dados e os incidentes esperados são sintéticos. Os parâmetros de contaminação são escolhidos para demonstração e não devem ser usados como configuração padrão de produção.
