# Roteiro de Apresentacao | Tech Challenge Olist

## Slide 1 - Pergunta de Negocio

**Mensagem principal:** queremos entender o desempenho comercial da Olist no
recorte analisado.

Fala sugerida:

> O objetivo foi analisar a evolucao dos pedidos entregues e do valor dos itens
> vendidos, identificando quais categorias e UFs mais contribuem para o
> desempenho comercial.

## Slide 2 - Base e Recorte

**Mensagem principal:** a analise usa os dados publicos da Olist e um recorte
conservador.

Pontos:

- nove arquivos CSV auditados;
- recorte: pedidos entregues entre 2017-01-01 e 2018-07-31;
- data de referencia: data de compra;
- valor analisado: valor dos itens, separado do frete.

## Slide 3 - Evolucao Mensal

**Mensagem principal:** pedidos e valor dos itens mostram o comportamento do
desempenho ao longo do tempo.

Usar graficos:

- `reports/figuras/evolucao_pedidos.png`;
- `reports/figuras/evolucao_valor_itens.png`.

## Slide 4 - Categorias

**Mensagem principal:** parte relevante do valor esta concentrada em algumas
categorias.

Usar grafico:

- `reports/figuras/top_categorias_valor.png`.

Fala sugerida:

> A concentracao por categoria ajuda a priorizar investigacoes comerciais, mas
> nao deve ser lida como margem ou lucro, pois o dataset nao traz custos.

## Slide 5 - UFs dos Clientes

**Mensagem principal:** a distribuicao regional mostra onde esta a maior
concentracao de valor dos itens vendidos.

Usar grafico:

- `reports/figuras/top_ufs_valor.png`.

## Slide 6 - Conclusoes

Pontos sugeridos:

- o recorte contem 89.860 pedidos entregues;
- o valor dos itens vendidos foi de R$ 12,34 milhoes;
- o ticket medio sem frete foi de R$ 137,35;
- a media e maior que a mediana, indicando pedidos de alto valor puxando a
  media para cima;
- categorias e UFs concentradas devem orientar analises futuras.

## Slide 7 - Recomendacoes e Proximos Passos

Recomendacoes:

- monitorar evolucao mensal com indicadores fixos;
- aprofundar categorias lideres para entender dependencia comercial;
- cruzar, em uma segunda etapa, satisfacao e logistica com as categorias de
  maior valor;
- manter a estrutura de validacao para evitar indicadores inflados.

Fechamento:

> A principal contribuicao do projeto foi transformar uma base com multiplas
> tabelas em uma leitura comercial confiavel, reprodutivel e explicavel.

