# Tech Challenge Olist | Análise de E-commerce

Projeto desenvolvido para o Tech Challenge com base no **Brazilian E-Commerce Public Dataset by Olist**.
O objetivo é construir uma análise executiva para apoiar investidores e acionistas de e-commerce na leitura de desempenho comercial, eficiência logística e satisfação dos clientes.

## Objetivo do Projeto

Construir um relatório executivo com análise de dados do marketplace Olist, apresentando métricas, visualizações e recomendações fundamentadas.

A entrega final deve contemplar:

- Relatório executivo com contexto, análise e conclusões;
- Repositório GitHub com códigos e documentação;
- Apresentação executiva com storytelling;
- Vídeo de até 5 minutos em linguagem executiva;
- Recomendações baseadas nos dados analisados.

## Pergunta Norteadora

Como o desempenho das entregas se relaciona com as avaliações dos clientes e quais regiões, categorias ou etapas logísticas merecem investigação prioritária?

## Base de Dados

O projeto utiliza os nove arquivos públicos do dataset Olist:

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

## Trilhas de Análise

O projeto pode seguir uma ou mais trilhas analíticas:

| Trilha | Possíveis análises |
|---|---|
| Crescimento e Receita | Evolução de pedidos, receita, ticket médio e participação por categoria |
| Logística e SLA | Tempo de entrega, atrasos, desempenho regional e impacto nas avaliações |
| Comportamento e Pagamentos | Meios de pagamento, parcelamento, recompra e retenção |
| Satisfação do Cliente | Distribuição das notas e relação com entrega, preço e categoria |
| Oportunidades e Recomendações | Frete, rotas críticas, categorias prioritárias e ações de melhoria |

## Metodologia

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

## Métricas Sugeridas

Algumas métricas previstas para análise:

- Total de pedidos;
- Receita total;
- Ticket médio;
- Tempo médio de entrega;
- Percentual de pedidos atrasados;
- Nota média das avaliações;
- Distribuição de avaliações por categoria;
- Relação entre atraso e satisfação do cliente;
- Desempenho por estado ou região;
- Participação de categorias no volume de vendas.

## Estrutura Sugerida do Repositório

```text
Analise_Olist/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── reports/
├── presentations/
├── README.md
└── requirements.txt
```

## Status do Projeto

Em desenvolvimento.

- [ ] Organizar base de dados
- [ ] Criar dicionário de dados
- [ ] Tratar inconsistências
- [ ] Definir métricas finais
- [ ] Desenvolver análises exploratórias
- [ ] Criar visualizações
- [ ] Elaborar recomendações
- [ ] Finalizar relatório executivo
- [ ] Preparar apresentação
- [ ] Gravar vídeo final

## Entregáveis

- Relatório executivo;
- Apresentação com storytelling;
- Código documentado no GitHub;
- Vídeo de até 5 minutos;
- Recomendações de negócio baseadas nos dados.

## Autor

**Tauã Patrick Santos Silva**

Projeto acadêmico desenvolvido no contexto do Tech Challenge.
