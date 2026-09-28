# Zabbix Automation Lab

Laboratorio seguro para estudar automacao da API do Zabbix sem expor ambientes corporativos.

## Recursos

- Cliente JSON-RPC
- Autenticacao por API token
- Modo demo com dados ficticios
- Listagem de hosts e interfaces
- Consulta de problemas recentes
- Relatorio JSON
- Dashboard web
- Exportacao via CLI
- Configuracao por variaveis de ambiente
- Testes automatizados

## Modo demo

O projeto inicia em modo demo por padrao:

```bash
pip install -r requirements.txt
uvicorn web_app:app --reload
```

Abra http://127.0.0.1:8000.

## Modo live

Copie .env.example para .env e altere:

```env
ZABBIX_DEMO=false
ZABBIX_URL=https://seu-lab/api_jsonrpc.php
ZABBIX_TOKEN=seu-token
```

Use somente ambiente de laboratorio ou infraestrutura onde voce tenha autorizacao.

## CLI

```bash
python zabbix_report.py --output report.json
```

## Testes

```bash
python -m pytest -q
```

## Seguranca

Prefira token somente leitura e menor privilegio. Nunca publique tokens, URLs internas, IPs privados, nomes de clientes, exports de producao ou screenshots com detalhes de infraestrutura real.
