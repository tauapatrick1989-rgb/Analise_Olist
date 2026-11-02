# Olist — crescimento e qualidade logística

**Relatório executivo do Tech Challenge FIAP — Fase 1**

## Síntese

A análise histórica do marketplace Olist mostra forte expansão do volume de pedidos e do valor dos itens vendidos, acompanhada por um risco operacional relevante: pedidos atrasados apresentam avaliações muito inferiores às entregas no prazo. O projeto transforma esse diagnóstico em uma proposta de piloto de 90 dias, com foco inicial no Rio de Janeiro e em categorias volumosas.

## Problema de negócio

**Como sustentar o crescimento dos pedidos entregues e priorizar ações de qualidade logística, considerando diferenças entre regiões, categorias e avaliações dos clientes?**

O recorte considera pedidos `delivered` comprados entre 01/01/2017 e 31/07/2018. A metodologia é descritiva e diagnóstica e utiliza uma estrutura reproduzível de tratamento, modelagem, validação e cálculo de métricas.

## Principais resultados

| Indicador | Resultado |
|---|---:|
| Pedidos entregues | 89.860 |
| Clientes únicos | 86.960 |
| Itens vendidos | 102.738 |
| Valor dos itens vendidos | R$ 12.342.450,49 |
| Ticket médio sem frete | R$ 137,35 |
| Pedidos — jan–jul/18 vs jan–jul/17 | +160,8% |
| Valor dos itens — jan–jul/18 vs jan–jul/17 | +161,6% |
| Taxa de atraso | 6,8% |
| Nota média no prazo | 4,28 |
| Nota média com atraso | 2,23 |

SP, RJ e MG concentram aproximadamente **63% do valor dos itens vendidos**. Entre os **89.852 pedidos com prazo observável**, 6.138 chegaram depois da previsão.

No Rio de Janeiro, **1.453 de 11.587 pedidos com prazo observável chegaram atrasados (12,54%)**. A triagem de avaliações sinalizou **512 possíveis reclamações por demora** no estado; portanto, esse número não deve ser confundido com a quantidade total de atrasos.

Entre os pedidos avaliados, **63,7% dos atrasados** receberam alguma nota 1 ou 2, contra **9,4% dos pedidos entregues no prazo**. A diferença é relevante para priorização, mas os dados não permitem afirmar que o atraso, isoladamente, causou a avaliação.

## Confiabilidade

O pipeline preserva os dados brutos, trabalha com granularidade explícita por item e por pedido e reconcilia preço, frete e contagens antes de gerar as métricas. Testes automatizados protegem as regras de dinheiro, datas, denominadores e duplicação de valores.

A documentação metodológica completa está em [metodologia.md](metodologia.md).

## Proposta de melhoria

Recomenda-se um **piloto controlado de 90 dias**:

1. mapear gargalos por transportadora e vendedor no RJ e em categorias volumosas;
2. revisar prazos prometidos e processos de expedição;
3. monitorar pedidos com risco de atraso e comunicar desvios ao cliente;
4. comparar taxa de atraso e avaliações com um grupo de controle;
5. decidir a ampliação somente após evidência de melhoria e análise de custos.

A proposta não representa uma solução já implementada. O dataset não contém informação suficiente para quantificar redução de custos ou retorno financeiro.

## Entregáveis

- documento executivo em DOCX para submissão acadêmica;
- apresentação oficial em PowerPoint, com 6 slides;
- vídeo de apresentação com aproximadamente 4 min 44 s;
- repositório GitHub com código, testes, dados, tabelas, gráficos e documentação.

## Equipe

Paula Cabrini Gracio · Matheus Novais Chiappa · Tauã Patrick Santos Silva · Sthefany Sobrinho Ferreira Alves
