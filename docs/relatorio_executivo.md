# Olist: crescimento e qualidade da entrega

## Sumário executivo

Entre janeiro e julho de 2018, o recorte de pedidos entregues registrou **46.432 pedidos** e **R$ 6,38 milhões em valor dos itens**, ante **17.805 pedidos** e **R$ 2,44 milhões** nos mesmos meses de 2017. As variações foram **+160,8%** e **+161,6%**, respectivamente. O valor médio dos itens por pedido ficou praticamente estável, de **R$ 136,97** para **R$ 137,40** (+0,3%). O crescimento observado acompanha sobretudo o número de pedidos.

Há também um ponto de atenção operacional. Entre **89.852 pedidos** com datas de entrega efetiva e estimada, **6.138 (6,8%)** chegaram após a data estimada. Entre pedidos com avaliação, **63,7%** dos atrasados receberam ao menos uma nota 1 ou 2, ante **9,4%** dos entregues no prazo. Essa diferença é uma **associação**, não mede o efeito causal de um atraso sobre a nota.

**Decisão proposta:** antes de investir para ampliar a operação, atualizar esses indicadores com dados recentes e investigar as rotas e os vendedores das categorias de maior valor. Se o padrão persistir, conduzir um piloto de melhoria de prazo, acompanhando a taxa de atraso, a proporção de notas 1 ou 2 e o valor dos itens dos pedidos entregues. Os dados históricos não permitem estimar margem, retorno do investimento nem resultado futuro desse piloto.

## Contexto e recorte

O desafio da FIAP pede um relatório para investidores e acionistas, com narrativa que conecte desempenho comercial, eficiência operacional e recomendações. Esta análise utiliza os nove CSVs públicos da Olist e concentra os indicadores de valor em pedidos `delivered` com compra de **01/01/2017 a 31/07/2018**. As comparações anuais usam janeiro a julho em ambos os anos. A UF é a do **cliente**. O valor financeiro é a soma do preço dos **itens**, sem frete.

| Indicador do recorte completo | Resultado |
|---|---:|
| Pedidos entregues | 89.860 |
| Clientes únicos | 86.960 |
| Itens | 102.738 |
| Valor dos itens | R$ 12.342.450,49 |
| Frete associado | R$ 2.045.177,88 |
| Valor médio dos itens por pedido | R$ 137,35 |
| Mediana do valor dos itens por pedido | R$ 86,99 |

## O que os dados mostram

### 1. A expansão foi principalmente de volume

| Janeiro a julho | Pedidos | Valor dos itens | Valor médio por pedido |
|---|---:|---:|---:|
| 2017 | 17.805 | R$ 2.438.756,43 | R$ 136,97 |
| 2018 | 46.432 | R$ 6.379.548,48 | R$ 137,40 |
| Variação | +160,8% | +161,6% | +0,3% |

Comparar sete meses equivalentes reduz a distorção de confrontar 2017 inteiro com parte de 2018. O indicador conta pedidos que foram entregues e os atribui ao mês da compra. Ele não equivale a todos os pedidos realizados no mês.

### 2. A concentração orienta onde investigar primeiro

**SP, RJ e MG** somam **63,0%** do valor dos itens no recorte. As categorias `health_beauty`, `watches_gifts`, `bed_bath_table` e `sports_leisure` somam **33,0%**. Os dez vendedores de maior valor somam **13,6%**. A distribuição geográfica descreve onde estão os clientes; sem dados externos de população, concorrência ou mercado, ela não demonstra potencial não explorado em outra UF. Os vendedores têm identificadores anonimizados.

### 3. A experiência de entrega merece atenção

| Situação | Pedidos com prazo observável | Pedidos avaliados | Percentual com nota 1 ou 2 | Nota média |
|---|---:|---:|---:|---:|
| No prazo | 83.714 | 83.237 | 9,4% | 4,28 |
| Atrasou | 6.138 | 5.993 | 63,7% | 2,23 |

O atraso compara **datas de calendário** de entrega efetiva e previsão. Oito pedidos do recorte ficaram fora dessa análise por ausência de uma das datas. Os pedidos sem avaliação permanecem na contagem de prazo e ficam fora das taxas de nota. Quando há mais de uma avaliação por pedido, a nota média é calculada por pedido e a classificação de nota baixa considera **qualquer** avaliação 1 ou 2. A relação entre atraso e nota pode refletir também outras diferenças entre os pedidos.

## Recomendação para a gestão

1. **Atualizar a base** antes de qualquer decisão de investimento: a amostra cobre compras históricas de 2017 e 2018. Recalcular os três indicadores centrais com dados recentes e conferir se a relação entre atraso e avaliação persiste.
2. **Selecionar um piloto de entrega** nas categorias e UFs de maior valor, após identificar os vendedores e rotas com maior taxa de atraso. A segmentação proposta define o universo de investigação; o recorte agregado atual ainda não identifica a causa.
3. **Definir avaliação prévia do piloto:** comparar a taxa de atraso e a proporção de avaliações 1 ou 2 com um período ou grupo comparável, acompanhando também volume de pedidos e valor dos itens. Registrar custos operacionais e margem fora desta base para decidir se uma ampliação compensa financeiramente.

## Conclusão e limites da interpretação

O recorte mostra forte aumento do número de pedidos entregues com ticket quase constante e uma associação expressiva entre atraso e avaliação baixa. Isso justifica **investigar a qualidade da entrega como condição de uma expansão responsável**. A recomendação é uma hipótese de ação a validar com dados atuais, custos e um teste controlado.

Os números não representam receita líquida, lucro, margem, NPS nem desempenho atual da empresa. Não há previsão de vendas: a série histórica é curta e o conjunto público termina em 2018. O uso de pedidos entregues exclui cancelamentos e pedidos ainda não entregues, o que limita a leitura do funil comercial.

## Fontes e rastreabilidade

- Fonte: Brazilian E-Commerce Public Dataset by Olist, nove arquivos em [`data/raw/`](../data/raw/).
- Método e definições: [`regras_tratamento.md`](regras_tratamento.md).
- Tabelas reproduzíveis: [`comparativo_jan_jul.csv`](../reports/tabelas/comparativo_jan_jul.csv), [`entrega_e_avaliacao.csv`](../reports/tabelas/entrega_e_avaliacao.csv), [`metricas_ufs.csv`](../reports/tabelas/metricas_ufs.csv), [`metricas_categorias_top15.csv`](../reports/tabelas/metricas_categorias_top15.csv), [`metricas_vendedores_top15.csv`](../reports/tabelas/metricas_vendedores_top15.csv).
- Critério acadêmico: *POSTECH – Tech Challenge – Fase 1*, pp. 2–5, material do curso.
