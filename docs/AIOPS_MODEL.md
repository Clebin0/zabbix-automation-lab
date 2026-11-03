# Detectores de anomalia

O laboratório recebe uma série numérica de cada vez. Os exemplos do painel são CPU, memória e latência; cada série contém 180 pontos. O gerador combina uma curva periódica simples com ruído e injeta picos em posições conhecidas.

## Métodos comparados

- **Isolation Forest**: método usado pela rota `/anomalies` e pela visualização principal. A contaminação padrão é 0,04.
- **Local Outlier Factor**: compara a densidade local de cada observação com a de seus vizinhos.
- **Robust z-score**: usa a mediana e o desvio absoluto mediano (MAD), com limiar padrão de 3,5.

O benchmark reúne precision, recall e F1 por métrica e no conjunto agregado, usando os picos inseridos como rótulos conhecidos.

## Como interpretar

Um F1 alto neste cenário significa que o método encontrou os picos artificiais escolhidos pelo gerador. Como os picos são grandes e foram inseridos de propósito, o resultado é um teste de funcionamento, não evidência de que o mesmo método funcionará bem com telemetria real.

## Próxima evolução

O passo que agregaria mais valor é trocar a série sintética por uma janela histórica autorizada e construir baseline por host e métrica. Antes disso, o laboratório não modela sazonalidade, manutenção programada, correlação entre sinais ou topologia.
