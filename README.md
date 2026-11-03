# Zabbix Observability Lab

Laboratório de integração de leitura com a API JSON-RPC do Zabbix e comparação de métodos para sinalizar pontos fora do comportamento esperado de uma métrica.

![Painel de observabilidade](docs/screenshots/dashboard.png)

## Dois modos de execução

**Demo** é o padrão. Usa três hosts fictícios, dois problemas de exemplo e séries métricas geradas localmente. É possível abrir o painel sem acesso a um servidor Zabbix.

**Live** consulta uma instância configurada pelo operador. O cliente usa os métodos de leitura `host.get` e `problem.get`; não altera hosts, eventos ou configuração do Zabbix. Para habilitar, informe `ZABBIX_URL` e `ZABBIX_TOKEN` e defina `ZABBIX_DEMO=false`.

Use somente uma instância que você administra ou tem autorização para consultar. Prefira um token de leitura com o menor conjunto de permissões necessário.

## Experimento de anomalias

O gerador cria 180 pontos para CPU, memória e latência, com uma tendência periódica simples e ruído aleatório de semente fixa. Alguns picos são inseridos em posições conhecidas para comparar os detectores.

| Método | Papel no laboratório |
|---|---|
| Isolation Forest | Detector usado pela análise exibida no painel |
| Local Outlier Factor | Comparação baseada na densidade local |
| Robust z-score | Referência estatística baseada em mediana e MAD |

Precision, recall e F1 são calculados contra os picos que foram inseridos no próprio gerador. Isso permite conferir o comportamento neste cenário controlado, mas não mede a capacidade de detectar incidentes desconhecidos em uma infraestrutura real.

## Executar em modo demo

Requisitos: Python 3.12 ou superior.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:ZABBIX_DEMO = "true"
uvicorn web_app:app --reload
```

Abra [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Configurar a consulta ao Zabbix

Defina as variáveis no ambiente do processo ou em um arquivo `.env` local, não versionado:

```dotenv
ZABBIX_DEMO=false
ZABBIX_URL=https://zabbix.seudominio/api_jsonrpc.php
ZABBIX_TOKEN=token_de_leitura
```

O cliente usa timeout de conexão/leitura e não segue redirecionamentos. Falhas do serviço externo são registradas no log do servidor; a API não devolve detalhes internos da exceção ao navegador.

## Endpoints locais

| Método | Rota | Descrição |
|---|---|---|
| GET | `/health` | Estado e detector principal |
| GET | `/report` | Hosts e problemas retornados pelo Zabbix ou demo |
| GET | `/anomalies` | Séries demo e pontos sinalizados |
| GET | `/benchmark` | Comparação dos três detectores |
| POST | `/anomalies/analyze` | Analisar uma série numérica enviada |

A rota de análise aceita de 25 a 10.000 valores finitos por chamada. A taxa de contaminação precisa ficar entre 0 e 0,5.

## Testes

```bash
python -m pytest -q
```

Os testes exercitam os dados demo, os detectores, os limites de entrada e o tratamento de falhas da API externa. Não substituem um teste de integração contra a sua versão do Zabbix.

## Limites

As séries são univariadas e sintéticas. O experimento não considera sazonalidade real, janelas de manutenção, relação entre hosts, dependência entre métricas nem baseline por serviço. Uma anomalia é um sinal para investigação, não a confirmação de um incidente.
