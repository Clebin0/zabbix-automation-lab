# Segurança

Use a integração somente em laboratórios ou ambientes para os quais exista autorização. No modo live, crie um token com acesso somente de leitura e limite-o aos grupos de hosts necessários.

Não versione tokens, arquivos de ambiente, exports de produção, nomes de clientes, endereços internos ou capturas de tela que revelem detalhes da infraestrutura.

A aplicação consulta hosts e problemas; não executa comandos remotos nem altera configurações do Zabbix. Os dados do modo demo são fictícios e não devem ser confundidos com telemetria real.
