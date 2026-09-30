# Detecção de anomalias

Neste projeto eu uso séries de CPU, memória e latência para testar detecção de comportamento fora do padrão.

O detector principal é o `IsolationForest`. Também deixei Local Outlier Factor e robust z-score para ter uma referência de comparação.

Os dados de teste recebem alguns picos conhecidos. Assim fica mais fácil ver se o detector encontrou justamente os pontos alterados ou se começou a marcar coisa demais.

## O que ainda falta

O laboratório não considera:

- sazonalidade;
- janela de manutenção;
- relação entre hosts;
- correlação com incidente;
- mudanças de baseline ao longo do tempo.

Também não trato uma anomalia como incidente automaticamente. Ela é só um sinal para investigar.

O próximo passo mais útil seria trabalhar com histórico por métrica e ajustar baseline por host, em vez de usar a mesma lógica para tudo.
