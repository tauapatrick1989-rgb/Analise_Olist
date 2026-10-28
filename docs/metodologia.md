# Metodologia da análise Olist

## Problema e abordagem

O case investiga como o crescimento dos pedidos entregues se relaciona com a qualidade da entrega e onde priorizar um diagnóstico operacional. A abordagem é descritiva e diagnóstica: descreve desempenho, compara grupos e formula uma proposta de teste. Não estima causalidade nem prevê vendas.

A trilha comercial é **Crescimento e Receita**, complementada pela análise de prazo e avaliações. A sequência de trabalho é problema de negócio, entendimento das fontes, tratamento, modelagem, validação, indicadores e recomendação.

## Fontes e recorte

O pipeline lê os nove CSVs de `data/raw/` uma única vez. Pedidos, clientes, itens, produtos e tradução sustentam as bases comerciais. Avaliações complementam a análise de experiência. Pagamentos, cadastro de vendedores e geolocalização são auditados; não são unidos diretamente aos valores comerciais.

- Status: `delivered`.
- Compra: de 01/01/2017 a 31/07/2018, inclusive; o limite final usa início do dia seguinte, exclusivo.
- Referência mensal: data da compra.
- Localização: UF do cliente.
- Comparação anual: janeiro a julho de 2017 e de 2018.
- Bases analíticas mantêm registros fora do recorte comercial com indicador de elegibilidade; os CSVs brutos permanecem intactos.

## Tratamento e validação

| Elemento | Regra aplicada |
|---|---|
| Identificadores e CEPs | Texto para preservar zeros e evitar conversões indevidas |
| Datas | Conversão com ausências explícitas para valores inválidos |
| Categoria ausente ou sem tradução | Preservar a venda com rótulo de identificação |
| Preço e frete | Conversão decimal para centavos; ausências, valores inválidos ou negativos interrompem a execução |
| Atributos físicos ausentes | Não excluir vendas da análise comercial |
| Chaves cadastrais | Auditar duplicidades e ausências; problemas interrompem o pipeline |
| Referências entre fontes | Verificar itens, pagamentos, avaliações, clientes, produtos e vendedores |
| Múltiplos itens e avaliações | Agregar na granularidade correta antes das junções |
| Geolocalização duplicada | Registrar no inventário; não usar essa fonte na modelagem comercial |

`fato_itens` contém uma linha por `order_id + order_item_id`. `fato_pedidos` agrega os centavos e mantém uma linha por `order_id`. `entregas_pedidos` contém os pedidos elegíveis com avaliações agregadas e indicadores de prazo, sem replicar valores.

A integração usa validação de cardinalidade. Seis controles reconciliam chaves, preço, frete, quantidade de pedidos e cobertura dos pedidos elegíveis da fonte. O pipeline interrompe diante de divergências; as auditorias ficam em `reports/qualidade/`.

## Contrato das métricas

| Indicador | Cálculo e denominador |
|---|---|
| Pedidos entregues | `order_id` distintos entre pedidos elegíveis |
| Clientes únicos | `customer_unique_id` distintos no recorte |
| Valor dos itens | Soma dos preços em centavos dividida por 100; não inclui frete |
| Frete | Soma do frete dos itens em centavos dividida por 100 |
| Ticket médio sem frete | Valor dos itens dividido pelos pedidos elegíveis |
| Participação de categoria, UF ou vendedor | Valor do grupo dividido pelo valor total do recorte antes de selecionar o ranking |
| Atraso | Entrega efetiva posterior à previsão em dias de calendário; entrega no mesmo dia é pontual |
| Taxa de atraso por UF | Pedidos atrasados divididos pelos pedidos da UF com ambas as datas disponíveis |
| Avaliação baixa | Pedido com qualquer nota 1 ou 2; nota média do pedido é a média das avaliações válidas de 1 a 5 |
| Taxa de avaliação baixa por situação | Pedidos com alguma nota 1 ou 2 divididos pelos pedidos avaliados em cada situação de prazo |
| Possível reclamação por demora | Alguma avaliação do pedido reúne nota 1 ou 2 e expressão de demora no título ou comentário |
| Taxa de possível reclamação por UF | Pedidos sinalizados divididos pelos pedidos da UF com prazo observável, inclusive os sem avaliação |
| Duração de entrega por categoria | Diferença entre compra e entrega em dias fracionários; uma observação por pedido e categoria |

As taxas nos CSVs são frações entre 0 e 1. Formate como percentual apenas na apresentação. Pedidos com várias categorias podem participar de mais de um grupo, por isso os totais de pedidos por categoria não são aditivos.

A duração exclui datas ausentes e intervalos negativos. A taxa de atraso por categoria usa somente pedidos com previsão observável. O ranking gráfico de duração exige ao menos 30 pedidos válidos por categoria; esse corte é um critério exploratório, não uma garantia de significância estatística.

## Triagem de possíveis reclamações

A regra preserva a abordagem exploratória do notebook original: normalização de caixa e acentos e busca por `atrasado`, `atrasada`, `atrasou`, `demorou`, `demora`, `demorando`, `não chegou`, `ainda não recebi`, `não recebi`, `fora do prazo` ou `prazo de entrega`. Flexões de plural de atrasado e atrasada também são consideradas. A nota negativa e o texto precisam ocorrer na mesma avaliação. Em seguida, o sinal é agregado por pedido.

Expressões genéricas podem produzir falsos positivos e outras formas de reclamação podem não ser identificadas. Comentários ausentes não indicam satisfação. A regra identifica **possíveis** reclamações e depende de revisão humana antes de orientar metas ou automações operacionais. Uma reclamação pode preceder uma entrega que depois ocorreu no prazo; os instantes de comentário e entrega não sustentam uma interpretação causal isolada.

## Reprodutibilidade e manutenção

Execute `python scripts/run_pipeline.py` para gerar três bases analíticas, dez tabelas de indicadores e seis gráficos. Os testes são executados com `python -m unittest discover -s tests`. O notebook apenas consulta tabelas produzidas pelo mesmo pipeline.

Os hashes do inventário são recalculados dos arquivos usados na execução. Bases tratadas e analíticas são regeneráveis e não são versionadas. O relatório executivo e a apresentação são materiais editoriais; a execução não reescreve textos nem slides.

Módulos: `io` faz leitura e gravação, `audit` audita fontes, `clean` trata tabelas centrais, `model` modela e reconcilia bases, `metrics` calcula desempenho comercial, `logistics` calcula prazo e sinais das avaliações, e `visualizations` produz figuras. O script da pasta `scripts/` orquestra essas etapas.
