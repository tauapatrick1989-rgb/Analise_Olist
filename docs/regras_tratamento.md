# Regras de Tratamento dos Dados

Este projeto usa a trilha **Crescimento e Receita** do Tech Challenge Olist.
O objetivo e analisar pedidos entregues, valor dos itens, ticket medio e
concentracao por categoria e UF.

## Principios

- Os arquivos em `data/raw/` sao a fonte bruta e nao devem ser alterados.
- A limpeza gera copias em `data/processed/clean/`.
- O recorte da analise nao apaga registros; ele cria indicadores de elegibilidade.
- Os valores financeiros sao preservados em reais e tambem convertidos para centavos.
- Valores ausentes, extremos ou fora do recorte sao documentados antes de qualquer decisao.

## Regras Aplicadas

| Situacao | Regra |
|---|---|
| IDs e CEPs | Ler como texto para preservar zeros a esquerda e evitar conversao indevida. |
| Datas | Converter com `errors="coerce"` e manter ausencias para auditoria. |
| Status | Normalizar para minusculas. O indicador principal usa `delivered`. |
| Periodo | Recorte analitico: compras de 2017-01-01 a 2018-07-31. |
| Categoria ausente | Manter a venda e exibir como `Sem categoria informada`/`not_informed`. |
| Produto sem peso ou dimensao | Nao excluir da analise comercial. |
| Preco e frete | Converter para numero e para centavos; nao preencher ausencias com zero. |
| Cliente recorrente | Nao deduplicar por `customer_unique_id`; ele e usado para contar clientes unicos. |
| Itens | Uma linha continua representando `order_id + order_item_id`. |
| Pedidos | A base de pedidos agrega os itens antes de calcular ticket medio. |
| Pagamentos e avaliacoes | Inventariados, mas nao entram na primeira versao da base comercial para evitar duplicacao. |

## Contrato de Metricas

| Indicador | Calculo |
|---|---|
| Pedidos entregues | Contagem distinta de `order_id` com status entregue e periodo elegivel. |
| Valor dos itens | Soma de `price` dos itens dos pedidos elegiveis. |
| Frete associado | Soma de `freight_value` dos itens dos pedidos elegiveis. |
| Ticket medio sem frete | Valor dos itens dividido pela quantidade de pedidos elegiveis. |
| Clientes unicos | Contagem distinta de `customer_unique_id`. |
| Participacao por categoria/UF | Valor do grupo dividido pelo valor total no mesmo universo. |

## Analogia Para Explicar

Pense no projeto como uma nota fiscal:

- A tabela de itens e a lista de produtos comprados.
- A tabela de pedidos e a capa da nota.
- A tabela de clientes diz para onde a compra foi.
- A tabela de produtos diz a familia do item.

Se juntarmos pagamentos ou avaliacoes sem cuidado, e como grampear duas copias
da mesma nota e somar tudo de novo. O codigo separa a lista de itens da capa da
nota para evitar esse erro.

