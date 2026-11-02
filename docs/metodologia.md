# Metodologia da análise Olist

## 1. Objetivo

O case investiga como o crescimento dos pedidos entregues se relaciona com a qualidade logística e onde priorizar um diagnóstico operacional. A abordagem é **descritiva e diagnóstica**: descreve desempenho, compara grupos e formula uma proposta de teste. Não estima causalidade e não prevê vendas.

## 2. Fontes e recorte

O pipeline lê os nove CSVs de `data/raw/` e preserva os arquivos originais.

- Status analisado: `delivered`.
- Período de compra: 01/01/2017 a 31/07/2018, inclusive.
- Referência mensal: data da compra.
- Localização: UF do cliente.
- Comparação anual: janeiro a julho de 2017 versus janeiro a julho de 2018.

Pedidos, clientes, itens, produtos e tradução sustentam as bases comerciais. Avaliações complementam a análise de experiência. Pagamentos, vendedores e geolocalização são auditados, mas não são usados para inflar ou redefinir o valor comercial.

## 3. Tratamento e modelagem

| Elemento | Regra |
|---|---|
| Identificadores e CEPs | tratados como texto |
| Datas | conversão explícita; inválidos permanecem ausentes |
| Categoria ausente | venda preservada com rótulo de identificação |
| Preço e frete | convertidos para centavos; valores inválidos ou negativos interrompem a execução |
| Chaves | duplicidades e referências inválidas são auditadas |
| Avaliações | agregadas na granularidade do pedido antes das junções |
| Geolocalização | auditada, mas não integrada ao modelo comercial |

As bases analíticas seguem três níveis:

- `fato_itens`: uma linha por `order_id + order_item_id`;
- `fato_pedidos`: uma linha por pedido com reconciliação dos valores dos itens e do frete;
- `entregas_pedidos`: uma linha por pedido elegível, com prazo e avaliações agregadas.

Esse desenho evita duplicação de valores quando existem múltiplos itens, pagamentos ou avaliações.

## 4. Contrato das métricas

| Indicador | Regra |
|---|---|
| Pedidos entregues | `order_id` distintos no recorte elegível |
| Clientes únicos | `customer_unique_id` distintos |
| Valor dos itens | soma dos preços, sem frete |
| Ticket médio | valor dos itens / pedidos entregues |
| Atraso | entrega efetiva posterior à data estimada |
| Taxa de atraso por UF | atrasados / pedidos da UF com prazo observável |
| Avaliação baixa | pedido com alguma nota 1 ou 2 |
| Taxa de avaliação baixa | pedidos com nota 1 ou 2 / pedidos avaliados no grupo |
| Possível reclamação por demora | mesma avaliação contém nota 1 ou 2 e expressão textual de demora |
| Duração por categoria | dias entre compra e entrega, por pedido e categoria |

Pedidos entregues no mesmo dia previsto são considerados pontuais. Pedidos sem as duas datas necessárias ficam fora do denominador de atraso.

## 5. Triagem textual

A triagem procura expressões relacionadas a demora, como `atrasado`, `atrasou`, `demora`, `não chegou`, `não recebi`, `fora do prazo` e `prazo de entrega`. A nota negativa e o texto precisam ocorrer na **mesma avaliação**.

Essa regra é exploratória. Pode produzir falsos positivos e falsos negativos, portanto identifica **possíveis reclamações**, não uma classificação definitiva.

## 6. Validação e reprodutibilidade

Execute:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python scripts/run_pipeline.py
```

A execução gera três bases analíticas, dez tabelas de indicadores, seis gráficos e relatórios de auditoria. Controles de chave, referência, preço, frete, contagem de pedidos e cobertura dos pedidos elegíveis interrompem o processo quando há divergências.

O notebook foi retirado da entrega final porque a lógica analítica está concentrada no pipeline modular em `src/olist/` e `scripts/run_pipeline.py`, protegido por testes automatizados.

## 7. Limites

Os dados são históricos. O recorte não representa todo o funil de vendas. O valor dos itens não é lucro nem receita líquida. A relação entre atraso e avaliação é associativa, não causal. A recomendação de piloto deve ser validada com dados atuais e informação de custos antes de orientar investimento em escala.
