# Zabbix Automation Lab

Laboratório seguro para estudar automação da API do Zabbix sem expor dados de ambientes corporativos.

## Recursos
- Cliente JSON-RPC
- Autenticação por API token
- Listagem de hosts
- Consulta de problemas ativos
- Relatório JSON
- Configuração por variáveis de ambiente
- Dry-run como padrão para exemplos futuros de escrita

## Configuração
Copie `.env.example` para `.env`, use uma instância de laboratório e um token com o menor privilégio possível.

```bash
pip install -r requirements.txt
python zabbix_report.py
```

Nunca versione tokens, URLs internas, IPs privados, nomes de clientes ou screenshots de produção.