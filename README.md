# Tech Challenge Olist | Analise de E-commerce

Projeto desenvolvido para o Tech Challenge com base no **Brazilian E-Commerce Public Dataset by Olist**.
O objetivo é construir uma análise executiva para apoiar investidores e acionistas de e-commerce na leitura de desempenho comercial, eficiência logística e satisfação dos clientes.

## Trilha Escolhida

**Crescimento e Receita.**

A primeira versao do projeto prioriza uma entrega completa, reprodutivel e
explicavel: evolucao dos pedidos entregues, valor dos itens vendidos, ticket
medio sem frete e concentracao por categoria e UF do cliente.

Pergunta central:

> Como evoluiram os pedidos entregues e o valor dos itens na base Olist, e quais
> categorias e UFs concentram a contribuicao para esse desempenho?

## Objetivo do Projeto

Construir um relatório executivo com análise de dados do marketplace Olist, apresentando métricas, visualizações e recomendações fundamentadas.

A entrega final deve contemplar:

- Relatório executivo com contexto, análise e conclusões;
- Repositório GitHub com códigos e documentação;
- Apresentação executiva com storytelling;
- Vídeo de até 5 minutos em linguagem executiva;
- Recomendações baseadas nos dados analisados.


## Metodologia Aplicada

A análise será conduzida em etapas:

1. Definição do problema de negócio;
2. Inventário e entendimento dos dados;
3. Tratamento de dados ausentes, duplicados e inconsistentes;
4. Criação da base analítica;
5. Definição das métricas;
6. Análise exploratória e estatística;
7. Construção de visualizações;
8. Geração de recomendações executivas;
9. Preparação do relatório, apresentação e vídeo final.

Neste repositorio, a metodologia foi operacionalizada em um pipeline Python:

```text
data/raw -> auditoria -> limpeza -> fato_itens/fato_pedidos -> metricas -> graficos -> relatorio
```

## Como Executar

Instale as dependencias e rode os testes:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests
```

Execute o pipeline completo:

```bash
python scripts/run_pipeline.py
```

O pipeline gera:

- `reports/qualidade/`: inventario, nulos, chaves, relacionamentos e validacao das bases;
- `reports/tabelas/`: resumo executivo e tabelas de metricas;
- `reports/figuras/`: graficos principais;
- `data/processed/clean/` e `data/processed/analytics/`: bases tratadas e bases analiticas reproduziveis.

Os CSVs processados nao sao versionados para evitar peso desnecessario no GitHub.

## Resultados Principais do Recorte

Recorte usado na primeira versao: pedidos com `order_status = delivered` e data
de compra entre **2017-01-01** e **2018-07-31**.

| Indicador | Resultado |
|---|---:|
| Pedidos entregues no recorte | 89.860 |
| Clientes unicos no recorte | 86.960 |
| Itens vendidos no recorte | 102.738 |
| Valor dos itens vendidos | R$ 12.342.450,49 |
| Frete associado | R$ 2.045.177,88 |
| Ticket medio sem frete | R$ 137,35 |

## Cuidados Tecnicos

- O valor analisado e **valor dos itens vendidos**, nao lucro ou receita liquida.
- A base `fato_itens` tem uma linha por `order_id + order_item_id`.
- A base `fato_pedidos` tem uma linha por `order_id`.
- Pagamentos e avaliacoes foram auditados, mas nao entraram na primeira base
  comercial para evitar multiplicacao de valores.
- O teste automatizado garante que um pedido com dois itens nao tenha seu valor
  duplicado durante a modelagem.

## Documentacao da Entrega

- [Relatório executivo para gestão e investidores](docs/relatorio_executivo.md)
- [Apresentação executiva editável](presentations/olist_storytelling_executivo.pptx)
- [Roteiro do vídeo de até 5 minutos](presentations/roteiro_video_5min.md)
- [Regras de tratamento](docs/regras_tratamento.md)
- [Roteiro da entrega da Fase 1](docs/roteiro_entrega_fase1.md)
- [Relatorio final explicativo](docs/relatorio_saida_final.md)

O comparativo anual usa janeiro a julho de cada ano. A análise de entrega usa
as datas efetiva e estimada e agrega avaliações por pedido. Os arquivos
`comparativo_jan_jul.csv`, `entrega_e_avaliacao.csv` e
`metricas_vendedores_top15.csv` são gerados em `reports/tabelas/`.

O workflow do GitHub executa testes e pipeline em cada pull request.

## Entregáveis

- Relatório executivo;
- Apresentação com storytelling;
- Código documentado no GitHub;
- Vídeo de até 5 minutos;
- Recomendações de negócio baseadas nos dados.


## Base de Dados

O projeto utiliza os nove arquivos públicos do dataset Olist:

Os arquivos CSV brutos estão em `data/raw/`. Dados tratados e agregados devem
ser salvos em `data/processed/`.

| Arquivo | Descrição |
|---|---|
| `olist_orders_dataset.csv` | Status e datas das etapas dos pedidos |
| `olist_customers_dataset.csv` | Identificação e localização dos clientes |
| `olist_order_items_dataset.csv` | Itens dos pedidos, produtos, vendedores, preços e frete |
| `olist_order_payments_dataset.csv` | Meios de pagamento, parcelamento e valores |
| `olist_order_reviews_dataset.csv` | Avaliações, notas, datas e comentários |
| `olist_products_dataset.csv` | Categorias e características dos produtos |
| `olist_sellers_dataset.csv` | Identificação e localização dos vendedores |
| `olist_geolocation_dataset.csv` | Coordenadas e informações geográficas por prefixo de CEP |
| `product_category_name_translation.csv` | Tradução dos nomes das categorias |


## Estrutura do Repositório

```text
Analise_Olist/
├── data/
│   ├── raw/          # Dados brutos do dataset Olist
│   └── processed/    # Dados tratados e agregados
├── notebooks/        # Exploração e análises
├── src/              # Código reutilizável
├── reports/          # Relatórios e resultados
├── presentations/    # Materiais da apresentação
├── README.md
└── requirements.txt
```
