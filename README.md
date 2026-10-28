# Análise Olist | Crescimento e qualidade da entrega

Projeto de análise de dados desenvolvido para o **Tech Challenge FIAP — Fase 1**, na trilha **Crescimento e Receita**, com o *Brazilian E-Commerce Public Dataset by Olist*.

O projeto conecta desempenho comercial, concentração de vendas e experiência de entrega para apoiar uma discussão executiva com gestores, investidores e acionistas. A entrega reúne um pipeline Python reproduzível, controles de qualidade, tabelas, gráficos, relatório e apresentação.

**Destaque:** entre janeiro e julho de 2018, o valor dos itens dos pedidos entregues cresceu **161,6%** frente aos mesmos meses de 2017, com ticket quase estável. A análise também encontrou maior frequência de avaliações baixas nos pedidos atrasados. A proposta de ação é atualizar os dados e investigar a operação antes de ampliar investimentos.

[Relatório executivo](docs/relatorio_executivo.md) · [Apresentação editável](presentations/olist_storytelling_executivo.pptx) · [Roteiro do vídeo](presentations/roteiro_video_5min.md) · [Regras de tratamento](docs/regras_tratamento.md)

## Pergunta de negócio

> Como evoluíram os pedidos entregues e o valor dos itens na base Olist, onde esse valor se concentra e como o prazo de entrega se relaciona com as avaliações dos clientes?

## Principais resultados

O recorte considera pedidos com `order_status = delivered` e **data de compra entre 01/01/2017 e 31/07/2018**, inclusive. O mês de referência é o da compra, não o da entrega.

| Indicador do recorte completo | Resultado |
|---|---:|
| Pedidos entregues | 89.860 |
| Clientes únicos | 86.960 |
| Itens vendidos | 102.738 |
| Valor dos itens vendidos, sem frete | R$ 12.342.450,49 |
| Frete associado | R$ 2.045.177,88 |
| Ticket médio sem frete | R$ 137,35 |
| Mediana do valor dos itens por pedido | R$ 86,99 |

Fontes: [resumo executivo](reports/tabelas/resumo_executivo.csv) e [distribuição do valor por pedido](reports/tabelas/distribuicao_valor_pedido.csv).

### Crescimento em períodos equivalentes

| Janeiro a julho | Pedidos entregues | Valor dos itens | Ticket médio sem frete |
|---|---:|---:|---:|
| 2017 | 17.805 | R$ 2.438.756,43 | R$ 136,97 |
| 2018 | 46.432 | R$ 6.379.548,48 | R$ 137,40 |
| Variação | +160,8% | +161,6% | +0,3% |

O crescimento observado acompanha principalmente o volume de pedidos. A comparação usa janeiro a julho em ambos os anos; os totais dessa tabela não correspondem ao recorte completo de 19 meses.

Fonte: [comparativo de janeiro a julho](reports/tabelas/comparativo_jan_jul.csv).

![Evolução mensal dos pedidos entregues, por mês da compra](reports/figuras/evolucao_pedidos.png)

### Concentração do valor dos itens

- **SP, RJ e MG:** 63,0% do valor, considerando a UF do cliente.
- **Quatro categorias:** `health_beauty`, `watches_gifts`, `bed_bath_table` e `sports_leisure` somam 33,0% do valor.
- **Dez maiores vendedores por valor:** 13,6% do total, identificados por códigos anonimizados.

Essas participações ajudam a definir prioridades de investigação. Para avaliar margem ou potencial de mercado por segmento, são necessários dados adicionais.

Fontes: [UFs](reports/tabelas/metricas_ufs.csv), [categorias](reports/tabelas/metricas_categorias_top15.csv) e [vendedores](reports/tabelas/metricas_vendedores_top15.csv).

### Entrega e avaliação

Entre **89.852 pedidos com datas de entrega efetiva e estimada disponíveis**, **6.138 (6,8%)** chegaram após a data estimada.

| Situação | Pedidos com prazo observável | Pedidos avaliados | Pedidos avaliados com alguma nota 1 ou 2 | Nota média por pedido |
|---|---:|---:|---:|---:|
| No prazo | 83.714 | 83.237 | 9,4% | 4,28 |
| Atrasou | 6.138 | 5.993 | 63,7% | 2,23 |

Oito pedidos ficaram fora da análise de prazo por ausência de uma das datas. As taxas de nota consideram apenas pedidos avaliados. Quando um pedido tem várias avaliações, sua nota média é a média das notas disponíveis, e a classificação de nota baixa considera qualquer avaliação 1 ou 2.

**Interpretação:** existe uma associação entre atraso e avaliação baixa; a análise não demonstra causalidade.

Fonte: [entrega e avaliação](reports/tabelas/entrega_e_avaliacao.csv).

## Como executar

Use **Python 3.12**, versão configurada na integração contínua, e Git. As versões das dependências estão fixadas em [`requirements.txt`](requirements.txt). Os nove CSVs de entrada já estão versionados em [`data/raw/`](data/raw/).

### 1. Clonar e criar o ambiente

```bash
git clone https://github.com/tauapatrick1989-rgb/Analise_Olist.git
cd Analise_Olist
python -m venv .venv
```

Ative o ambiente no Linux/macOS:

```bash
source .venv/bin/activate
```

Ou no Windows, usando PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências e executar os testes

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests
```

### 3. Executar o pipeline

Na raiz do repositório:

```bash
python scripts/run_pipeline.py
```

O comando audita os nove CSVs, trata as tabelas centrais, constrói e valida as bases analíticas, calcula indicadores e salva tabelas e gráficos. Uma falha nos controles de `validacao_bases_analiticas.csv` interrompe a execução antes da geração dos indicadores.

| Saída | Conteúdo |
|---|---|
| `data/processed/clean/` | Pedidos, clientes, produtos e itens tratados |
| `data/processed/analytics/` | `fato_itens.csv` e `fato_pedidos.csv` |
| `reports/qualidade/` | Inventário, ausências, chaves, relacionamentos, pedidos por mês/status e validações |
| `reports/tabelas/` | Resumo, métricas mensais, categorias, UFs, vendedores, distribuição, comparativo anual e entrega/avaliação |
| `reports/figuras/` | Quatro gráficos PNG: pedidos, valor dos itens, categorias e UFs |

Os CSVs processados são gerados localmente e ignorados pelo Git. Uma nova execução regrava as saídas do pipeline. Relatórios em Markdown, apresentação e roteiros são materiais preparados separadamente; o comando gera CSVs e PNGs.

## Método e definições

O fluxo implementado é: **auditoria → tratamento → modelagem → validação → métricas → visualizações**. Os arquivos brutos são preservados. O período e o status de elegibilidade estão definidos em [`src/olist/config.py`](src/olist/config.py), e o filtro é aplicado no cálculo das métricas.

### Bases analíticas e prevenção de duplicações

| Base | Granularidade | Uso principal |
|---|---|---|
| `fato_itens` | Uma linha por `order_id + order_item_id` | Valor por categoria e vendedor |
| `fato_pedidos` | Uma linha por `order_id`, após agregar os itens | Pedidos, clientes, ticket, evolução mensal, UF e entrega |

Pedidos e itens são integrados a clientes e produtos com validação de cardinalidade. Os pagamentos são auditados e ficam fora das métricas comerciais. As avaliações são agregadas por pedido antes da junção usada na análise de entrega, evitando multiplicar observações. O ranking de vendedores usa o `seller_id` dos itens; a tabela cadastral de vendedores e a geolocalização são auditadas, sem integração às bases comerciais.

### Contrato das métricas

| Métrica | Definição |
|---|---|
| Pedidos entregues | Contagem distinta de `order_id` elegíveis por status e data de compra |
| Clientes únicos | Contagem distinta de `customer_unique_id` entre pedidos elegíveis |
| Itens vendidos | Quantidade de linhas elegíveis de `fato_itens` |
| Valor dos itens | Soma de `price` dos itens elegíveis, sem frete |
| Frete associado | Soma de `freight_value` dos itens elegíveis |
| Ticket médio sem frete | Valor dos itens dividido pela quantidade de pedidos elegíveis |
| Participação por categoria, UF ou vendedor | Valor dos itens do grupo dividido pelo valor total do recorte; os rankings exibem apenas os maiores grupos |
| Atraso | Data de entrega ao cliente posterior à data estimada, comparando dias de calendário |
| Taxa de avaliações baixas | Pedidos com alguma nota 1 ou 2 divididos pelos pedidos avaliados em cada grupo de prazo |

Datas inválidas são convertidas em ausências; IDs e CEPs são lidos como texto. Categorias ausentes ou sem tradução recebem rótulos de identificação. Os valores monetários também são convertidos para centavos, usados na reconciliação entre itens e pedidos. As regras completas estão em [`docs/regras_tratamento.md`](docs/regras_tratamento.md).

### Testes e integração contínua

Os quatro testes de [`tests/test_modeling.py`](tests/test_modeling.py) cobrem conversão para centavos, prevenção de duplicação de valores, reconciliação e cobertura dos pedidos, comparação entre meses equivalentes e múltiplas avaliações por pedido.

O pipeline verifica seis controles: chaves únicas de itens e pedidos, reconciliação de preço e frete em centavos, contagem de pedidos elegíveis e cobertura dos pedidos elegíveis da fonte. Os resultados ficam em [`validacao_bases_analiticas.csv`](reports/qualidade/validacao_bases_analiticas.csv).

O [workflow de validação](.github/workflows/validate.yml) instala as dependências, executa os testes e o pipeline e confere as saídas em pull requests e pushes para `main`.

## Dados de entrada

Fonte: **Brazilian E-Commerce Public Dataset by Olist**. Os nove arquivos estão em [`data/raw/`](data/raw/); o [inventário](reports/qualidade/inventory.csv) registra quantidade de linhas, colunas, duplicidades e hash SHA-256 de cada arquivo.

**Observação de reprodutibilidade:** os hashes do inventário versionado divergem dos arquivos atuais para `olist_order_reviews_dataset.csv` e `product_category_name_translation.csv`. A execução do pipeline recalcula esses metadados. Os indicadores foram reproduzidos na revisão.

| Arquivo | Conteúdo |
|---|---|
| `olist_orders_dataset.csv` | Status e datas das etapas dos pedidos |
| `olist_customers_dataset.csv` | Identificação e localização dos clientes |
| `olist_order_items_dataset.csv` | Produtos, vendedores, preços e frete por item |
| `olist_order_payments_dataset.csv` | Meios de pagamento, parcelamento e valores |
| `olist_order_reviews_dataset.csv` | Notas, comentários e datas das avaliações |
| `olist_products_dataset.csv` | Categorias e características dos produtos |
| `olist_sellers_dataset.csv` | Identificação e localização dos vendedores |
| `olist_geolocation_dataset.csv` | Coordenadas e informações geográficas por prefixo de CEP |
| `product_category_name_translation.csv` | Tradução dos nomes das categorias |

## Estrutura do repositório

| Caminho | Responsabilidade |
|---|---|
| [`src/olist/`](src/olist/) | Configuração, leitura, auditoria, tratamento, modelagem, métricas e gráficos |
| [`scripts/run_pipeline.py`](scripts/run_pipeline.py) | Orquestração da execução completa |
| [`tests/`](tests/) | Testes automatizados das regras críticas |
| [`data/raw/`](data/raw/) | Nove CSVs de origem |
| [`data/processed/`](data/processed/) | Destino das bases geradas localmente |
| [`reports/`](reports/) | Tabelas de qualidade, indicadores e figuras |
| [`docs/`](docs/) | Relatório executivo, método e documentação da entrega |
| [`presentations/`](presentations/) | Apresentação PowerPoint e roteiros |
| [`.github/workflows/validate.yml`](.github/workflows/validate.yml) | Validação automática no GitHub Actions |

## Materiais e situação da entrega

| Material | Disponibilidade |
|---|---|
| [Relatório executivo](docs/relatorio_executivo.md) | Disponível |
| [Apresentação executiva editável — seis slides](presentations/olist_storytelling_executivo.pptx) | Disponível |
| [Roteiro da apresentação](presentations/roteiro_apresentacao.md) | Disponível |
| [Roteiro do vídeo de até cinco minutos](presentations/roteiro_video_5min.md) | Disponível |
| Vídeo gravado | Pendente de gravação e inclusão do link |
| [Regras de tratamento](docs/regras_tratamento.md) | Disponíveis |
| [Relatório explicativo da implementação](docs/relatorio_saida_final.md) | Disponível |
| [Roteiro da entrega da Fase 1](docs/roteiro_entrega_fase1.md) | Disponível |

## Limites e próximos passos

- Os resultados usam dados históricos e o recorte comercial cobre compras de 2017 e 2018; não representam o desempenho atual da empresa.
- **Valor dos itens vendidos não equivale a receita líquida, lucro ou margem.** A base não contém os custos e taxas necessários para essas medidas.
- O filtro de pedidos entregues exclui cancelamentos e pedidos ainda não entregues, limitando a leitura do funil comercial.
- As comparações são descritivas. A associação entre atraso e avaliação não isola causas, e o projeto não inclui previsão de vendas ou estimativa de retorno de investimento.
- A recomendação do relatório é atualizar os dados, investigar atrasos nos segmentos de maior valor e avaliar um piloto com indicadores de prazo, notas, volume e custos. O diagnóstico de rotas e as causas dos atrasos dependem de aprofundamento posterior.

## Licença

O código do projeto está sob a [licença MIT](LICENSE). A fonte dos dados é o dataset público da Olist; consulte os termos da fonte original ao reutilizá-los.
