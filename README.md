# Análise Olist

**Tech Challenge FIAP — Pós-graduação em Análise de Dados | Fase 1**

Análise descritiva e diagnóstica do crescimento comercial e da qualidade logística no marketplace Olist. O projeto investiga como o aumento do volume de pedidos se relaciona com o cumprimento de prazos e com a experiência dos clientes, transformando os achados em uma proposta de piloto operacional de 90 dias.

## Pergunta de negócio

> Como sustentar o crescimento dos pedidos entregues e priorizar ações de qualidade logística, considerando diferenças entre regiões, categorias e avaliações dos clientes?

O recorte considera pedidos com status `delivered`, comprados entre **01/01/2017 e 31/07/2018**, com localização pela UF do cliente.

## Principais evidências

| Evidência | Resultado |
|---|---:|
| Pedidos entregues | 89.860 |
| Clientes únicos | 86.960 |
| Itens vendidos | 102.738 |
| Valor dos itens vendidos | R$ 12.342.450,49 |
| Ticket médio sem frete | R$ 137,35 |
| Crescimento dos pedidos — jan–jul/18 vs jan–jul/17 | +160,8% |
| Crescimento do valor dos itens — jan–jul/18 vs jan–jul/17 | +161,6% |
| Pedidos com atraso entre prazos observáveis | 6,8% |
| Nota média — no prazo vs atrasado | 4,28 vs 2,23 |
| Avaliações 1 ou 2 — atrasado vs no prazo | 63,7% vs 9,4% |

SP, RJ e MG concentram cerca de **63% do valor dos itens vendidos**. No Rio de Janeiro, **1.453 de 11.587 pedidos com prazo observável chegaram atrasados (12,54%)**. O indicador de **512 pedidos** corresponde à triagem de possíveis reclamações por demora no RJ, e não ao total de atrasos.

As relações são históricas e observacionais: orientam investigação, mas não demonstram causalidade.

## Proposta

O projeto recomenda um **piloto controlado de 90 dias**, com prioridade para o Rio de Janeiro e categorias volumosas:

1. diagnosticar gargalos por transportadora e vendedor;
2. revisar promessas de prazo e processos de expedição;
3. monitorar pedidos em risco e comunicar desvios de forma proativa;
4. comparar atraso e avaliações com um grupo de controle antes de escalar.

A proposta ainda não foi implementada e não há base de custos suficiente para estimar retorno financeiro.

## Reprodutibilidade

Requisitos: **Python 3.12**, Pandas e Matplotlib.

```bash
git clone https://github.com/tauapatrick1989-rgb/Analise_Olist.git
cd Analise_Olist
python -m venv .venv
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python scripts/run_pipeline.py
```

O pipeline audita as nove fontes, trata as tabelas centrais, constrói bases analíticas, reconcilia valores, calcula os indicadores e gera os relatórios e gráficos versionados.

## Estrutura

| Caminho | Finalidade |
|---|---|
| `data/raw/` | nove arquivos originais do dataset Olist |
| `data/processed/` | bases regeneráveis produzidas pelo pipeline |
| `src/olist/` | módulos de leitura, auditoria, tratamento, modelagem, métricas e logística |
| `scripts/run_pipeline.py` | execução ponta a ponta |
| `tests/` | testes de granularidade, datas, valores e denominadores |
| `reports/` | tabelas, validações e figuras reproduzíveis |
| `docs/` | metodologia, relatório executivo e documento final |
| `presentations/` | apresentação oficial do Tech Challenge |

O notebook foi removido da entrega porque o pipeline em `src/` e `scripts/` já concentra a lógica de negócio de forma reproduzível e testável.

## Materiais da entrega

- [Relatório executivo em Markdown](docs/relatorio_executivo.md)
- [Metodologia e contrato das métricas](docs/metodologia.md)
- Documento executivo em DOCX na pasta `docs/`
- Apresentação oficial em PowerPoint na pasta `presentations/`
- Vídeo oficial da apresentação, com aproximadamente 4 min 44 s

## Equipe

- Paula Cabrini Gracio
- Matheus Novais Chiappa
- Tauã Patrick Santos Silva
- Sthefany Sobrinho Ferreira Alves

## Limites de interpretação

Os dados representam um período histórico e não a operação atual da Olist. O recorte exclui pedidos não entregues. A triagem textual identifica possíveis reclamações e exige validação humana. O valor dos itens vendidos não equivale a lucro nem receita líquida. O piloto proposto deve ser validado com dados atuais, indicadores previamente definidos e informação de custos antes de qualquer expansão.

## Licença

Código sob [licença MIT](LICENSE). Os dados pertencem ao **Brazilian E-Commerce Public Dataset by Olist** e devem ser reutilizados conforme os termos da fonte original.
