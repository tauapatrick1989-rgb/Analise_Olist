# Relatorio Final Explicativo | Tech Challenge Olist Fase 1

## 1. O Que Foi Implementado

Foi implementada uma estrutura completa para a primeira entrega do Tech
Challenge Olist, com foco na trilha **Crescimento e Receita**.

A entrega cobre:

- auditoria dos nove CSVs;
- regras de tratamento documentadas;
- limpeza das tabelas centrais;
- criacao de duas bases analiticas;
- validacao automatica para evitar duplicacao de valores;
- calculo de metricas executivas;
- geracao de tabelas e graficos;
- testes automatizados;
- documentacao para explicar o projeto.

## 2. Escolha da Trilha

A trilha recomendada e aplicada foi **Crescimento e Receita**.

Ela e a mais eficiente para esta fase porque permite demonstrar analise de
negocio, tratamento de dados, estatistica descritiva e storytelling sem entrar
em modelos preditivos ou regras complexas de logistica.

Analogia: esta trilha e como comecar avaliando o painel principal de uma loja:
quantos pedidos entraram, quanto foi vendido, quais prateleiras venderam mais e
de onde vieram os clientes. Antes de otimizar entrega, satisfacao ou
recomendacao, e preciso entender o desempenho comercial basico.

## 3. Pergunta Central

Como evoluiram os pedidos entregues e o valor dos itens na base Olist, e quais
categorias e UFs concentram a contribuicao para esse desempenho?

## 4. Recorte Analitico

| Item | Definicao |
|---|---|
| Status usado nos indicadores | `delivered` |
| Periodo | 2017-01-01 a 2018-07-31 |
| Data de referencia | `order_purchase_timestamp` |
| Valor financeiro principal | Soma de `price` dos itens |
| Localizacao | UF do cliente |
| Segmentacao | Categoria do produto |

O recorte nao apaga dados. Ele cria uma coluna de elegibilidade, permitindo
preservar o historico completo e filtrar apenas no momento dos indicadores.

## 5. Estrutura do Codigo

| Arquivo | Papel |
|---|---|
| `src/olist/config.py` | Centraliza caminhos, nomes de arquivos e recorte da analise. |
| `src/olist/io.py` | Le os CSVs preservando IDs e CEPs como texto. |
| `src/olist/audit.py` | Gera inventario, nulos, chaves e relacionamentos. |
| `src/olist/clean.py` | Limpa pedidos, clientes, produtos e itens. |
| `src/olist/model.py` | Monta `fato_itens` e `fato_pedidos`. |
| `src/olist/metrics.py` | Calcula resumo, metricas mensais, categorias, UFs e estatisticas. |
| `src/olist/visualizations.py` | Gera graficos PNG. |
| `scripts/run_pipeline.py` | Executa tudo em ordem. |
| `tests/test_modeling.py` | Testa regras criticas de dinheiro e modelagem. |

Analogia: o projeto foi organizado como uma cozinha profissional. Cada arquivo
tem uma bancada: uma para conferir ingredientes, outra para limpar, outra para
montar o prato e outra para apresentar. Isso evita misturar tudo em uma panela
so e depois nao conseguir explicar de onde veio o resultado.

## 6. Bases Analiticas

Foram criadas duas bases principais:

| Base | Granularidade | Uso |
|---|---|---|
| `fato_itens` | Uma linha por `order_id + order_item_id` | Analise de valor por produto, categoria e UF. |
| `fato_pedidos` | Uma linha por `order_id` | Contagem de pedidos, clientes e ticket medio. |

Essa separacao e essencial. No Olist, um pedido pode ter varios itens, varios
pagamentos e mais de uma avaliacao. Se tudo for juntado diretamente, o valor da
venda pode ser multiplicado sem aparecer como erro visual.

Analogia: uma compra com dois produtos e dois pagamentos nao significa quatro
produtos. Se cruzarmos tudo sem agregar antes, e como tirar fotocopia da mesma
nota e somar todas as copias.

## 7. Validacoes Realizadas

A validacao das bases analiticas retornou status `ok` nos principais controles:

| Controle | Resultado |
|---|---:|
| Chave unica em `fato_itens` | OK |
| Chave unica em `fato_pedidos` | OK |
| Reconciliacao do valor dos itens | OK |
| Reconciliacao do frete | OK |
| Contagem de pedidos elegiveis | OK |

Teste automatizado principal:

- um pedido com dois itens de R$ 10 e R$ 20 deve resultar em uma linha de
  pedido com R$ 30 em itens;
- se a modelagem duplicar para R$ 60, o teste falha.

## 8. Resultados do Recorte

| Indicador | Valor |
|---|---:|
| Pedidos entregues | 89.860 |
| Clientes unicos | 86.960 |
| Itens vendidos | 102.738 |
| Valor dos itens vendidos | R$ 12.342.450,49 |
| Frete associado | R$ 2.045.177,88 |
| Ticket medio sem frete | R$ 137,35 |

Estatistica do valor por pedido:

| Medida | Valor |
|---|---:|
| Media | R$ 137,35 |
| Mediana | R$ 86,99 |
| 1o quartil | R$ 45,90 |
| 3o quartil | R$ 149,90 |
| Maximo | R$ 13.440,00 |

Leitura executiva: a media maior que a mediana indica presenca de pedidos de
maior valor puxando a media para cima. Por isso, olhar apenas o ticket medio nao
basta; a distribuicao ajuda a interpretar o comportamento real dos pedidos.

## 9. Arquivos de Saida

| Saida | Caminho |
|---|---|
| Inventario dos CSVs | `reports/qualidade/inventory.csv` |
| Nulos por coluna | `reports/qualidade/missing_values.csv` |
| Validacao das bases | `reports/qualidade/validacao_bases_analiticas.csv` |
| Resumo executivo | `reports/tabelas/resumo_executivo.csv` |
| Metricas mensais | `reports/tabelas/metricas_mensais.csv` |
| Top categorias | `reports/tabelas/metricas_categorias_top15.csv` |
| Metricas por UF | `reports/tabelas/metricas_ufs.csv` |
| Graficos principais | `reports/figuras/` |

## 10. Proximos Passos Para a Entrega

O [relatório executivo](relatorio_executivo.md) reúne os achados e a decisão
proposta para a gestão. A [apresentação editável](../presentations/olist_storytelling_executivo.pptx)
e o [roteiro do vídeo](../presentations/roteiro_video_5min.md) estão prontos.
O vídeo precisa ser gravado e seu link inserido no README após publicação.

O aprofundamento usa comparações entre janeiro e julho de cada ano, valores
por vendedor e a associação entre prazo de entrega e avaliação. A validação
inclui cobertura dos pedidos elegíveis da fonte e interrompe o pipeline se
algum controle falhar. Os quatro testes automatizados cobrem centavos,
granularidade, comparação de períodos e múltiplas avaliações.

Recomendacao de linguagem: falar em **valor dos itens vendidos**, e nao em lucro
ou receita liquida. O dataset nao traz custos, taxas e margens para sustentar
essas conclusoes.
