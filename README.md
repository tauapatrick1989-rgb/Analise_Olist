# Análise Olist

**Tech Challenge FIAP — Fase 1 | Crescimento e Receita**

Análise descritiva e diagnóstica do crescimento comercial e da qualidade da entrega no dataset público Olist. O objetivo é identificar prioridades de investigação e propor um piloto operacional com avaliação de resultados.

> Como evoluíram os pedidos entregues e o valor dos itens, como o prazo se relaciona com as avaliações e onde investigar melhorias primeiro?

[Relatório executivo](docs/relatorio_executivo.md) · [Metodologia e métricas](docs/metodologia.md) · [Notebook de leitura](notebooks/analise_atrasos_frete.ipynb) · [Apresentação](presentations/olist_storytelling_executivo.pptx)

## Resultados que orientam o case

Recorte: compras de **01/01/2017 a 31/07/2018** com status `delivered`, atribuídas ao mês da compra.

| Evidência | Resultado |
|---|---:|
| Pedidos entregues | 89.860 |
| Clientes únicos | 86.960 |
| Itens vendidos | 102.738 |
| Valor dos itens sem frete | R$ 12.342.450,49 |
| Ticket médio sem frete | R$ 137,35 |
| Crescimento dos pedidos em jan–jul de 2018 versus jan–jul de 2017 | 160,8% |
| Crescimento do valor dos itens no mesmo comparativo | 161,6% |
| Atrasos entre pedidos com prazo observável | 6,8% |
| Avaliações baixas entre pedidos avaliados atrasados versus pontuais | 63,7% versus 9,4% |

SP concentra mais possíveis reclamações por demora (603 pedidos); RJ combina volume relevante (512) com incidência superior (4,42%, ante 1,62% em SP). Os denominadores são os pedidos com prazo observável de cada UF. A identificação usa notas e palavras-chave e requer validação humana.

![Evolução mensal dos pedidos entregues](reports/figuras/evolucao_pedidos.png)

Fontes: [tabelas reproduzíveis](reports/tabelas/). Valor dos itens não equivale a lucro ou receita líquida. As relações observadas são históricas e não demonstram causalidade.

## Executar o projeto

Use **Python 3.12** e Git. Os nove CSVs de entrada já estão em `data/raw/`.

```bash
git clone https://github.com/tauapatrick1989-rgb/Analise_Olist.git
cd Analise_Olist
python -m venv .venv
```

Ative o ambiente com `source .venv/bin/activate` no Linux/macOS ou `.\.venv\Scripts\Activate.ps1` no PowerShell. Em seguida:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python scripts/run_pipeline.py
```

O pipeline inteiro funciona com Pandas e Matplotlib. Para abrir o notebook, instale as ferramentas opcionais:

```bash
python -m pip install -r requirements-notebook.txt
jupyter notebook
```

O notebook apresenta as tabelas do pipeline; não contém uma segunda implementação das regras de negócio.

## Organização

| Caminho | Finalidade |
|---|---|
| `src/olist/io.py` | Leitura única das fontes e gravação das tabelas |
| `src/olist/audit.py` | Inventário, hashes, ausências, chaves e referências |
| `src/olist/clean.py` | Tratamento de pedidos, clientes, produtos e itens |
| `src/olist/model.py` | Bases por item e pedido e reconciliação |
| `src/olist/metrics.py` | Indicadores comerciais |
| `src/olist/logistics.py` | Prazo, avaliações e triagem de possíveis reclamações |
| `src/olist/visualizations.py` | Seis gráficos das tabelas oficiais |
| `src/olist/config.py` | Caminhos, período, status e corte do ranking de categorias |
| `scripts/run_pipeline.py` | Execução das etapas em ordem |
| `tests/` | Regras críticas de dinheiro, granularidade, datas e denominadores |
| `docs/` | Relatório executivo e metodologia consolidada |
| `presentations/` | Apresentação e roteiros de fala e vídeo |

## Saídas

| Pasta | Conteúdo |
|---|---|
| `data/processed/clean/` | Quatro tabelas tratadas |
| `data/processed/analytics/` | `fato_itens`, `fato_pedidos` e `entregas_pedidos` |
| `reports/qualidade/` | Seis tabelas de auditoria e reconciliação |
| `reports/tabelas/` | Dez tabelas comerciais e logísticas, incluindo UF e duração por categoria |
| `reports/figuras/` | Quatro gráficos comerciais e dois de logística |

A execução regrava as saídas e preserva os CSVs brutos. Bases processadas são ignoradas pelo Git. O inventário é recalculado com os hashes das fontes usadas. Falhas de chaves, referências ou reconciliação interrompem o processo. Relatórios e slides são materiais editoriais preparados separadamente.

O [workflow](.github/workflows/validate.yml) executa testes e pipeline em pull requests e pushes para `main`.

## Materiais da entrega

- [Relatório executivo](docs/relatorio_executivo.md), com problema, dados, evidências e proposta.
- [Metodologia](docs/metodologia.md), com tratamento, fórmulas, denominadores e limites.
- [Apresentação editável](presentations/olist_storytelling_executivo.pptx).
- [Roteiro da apresentação](presentations/roteiro_apresentacao.md) e [roteiro do vídeo](presentations/roteiro_video_5min.md).
- Vídeo: gravação e inclusão do link ainda pendentes.

## Limites de interpretação

Os dados históricos não representam a operação atual. O recorte exclui pedidos não entregues. A triagem por texto não é uma classificação validada de reclamações. O tempo de entrega mede duração; atraso mede descumprimento da previsão. Não há custos ou margens para estimar retorno financeiro. A proposta é atualizar as evidências e testar melhorias com comparação adequada antes de escalar.

## Licença

Código sob [licença MIT](LICENSE). Os dados são do Brazilian E-Commerce Public Dataset by Olist; consulte os termos da fonte original para reutilização.
