# Relatório Executivo — Brazilian E-Commerce Public Dataset by Olist

## 1) Objetivo
Construir uma visão executiva para investidores e acionistas sobre:
- **desempenho comercial**,
- **eficiência logística** e
- **satisfação do cliente**,

com recomendações de alocação de esforço e capital para crescimento sustentável.

---

## 2) Escopo analítico (dataset Olist)
Este relatório utiliza as principais tabelas públicas do Olist:
- `olist_orders_dataset`
- `olist_order_items_dataset`
- `olist_order_payments_dataset`
- `olist_products_dataset`
- `olist_order_reviews_dataset`
- `olist_customers_dataset`
- `olist_sellers_dataset`
- `olist_geolocation_dataset`

---

## 3) Principais leituras para investidores

### 3.1 Desempenho comercial
**KPIs executivos recomendados**
- Receita bruta (GMV aproximado)
- Pedidos por mês (crescimento e sazonalidade)
- Ticket médio por pedido
- Receita por categoria de produto
- Concentração de receita (top categorias/top sellers)

**Leitura executiva**
- O modelo apresenta potencial de escala com base no volume de pedidos e diversidade de categorias.
- Há risco de concentração em subconjuntos de categorias/sellers, exigindo estratégia de diversificação de mix e parceiros.
- Sazonalidade impacta previsão de caixa e deve orientar planejamento de estoque e mídia.

### 3.2 Eficiência logística
**KPIs executivos recomendados**
- Prazo médio prometido vs. prazo real de entrega
- % de pedidos entregues em atraso
- Custo de frete por pedido e por faixa de distância
- Tempo de ciclo do pedido (compra até entrega)

**Leitura executiva**
- Atrasos logísticos são um dos principais pontos de erosão de experiência e recompra.
- Rotas longas e categorias com maior dimensão/peso tendem a pressionar margem via frete.
- Ganhos operacionais em SLA têm efeito direto em retenção, reputação e custo de atendimento.

### 3.3 Satisfação do cliente
**KPIs executivos recomendados**
- Nota média de avaliação (`review_score`)
- % de avaliações 1–2 estrelas
- Relação entre atraso de entrega e nota
- Relação entre categoria/frete e nota

**Leitura executiva**
- A satisfação é fortemente sensível à qualidade da entrega (pontualidade e previsibilidade).
- Redução de atrasos tende a melhorar avaliações e indicadores de confiança de marca.
- Categorias críticas devem receber governança de qualidade e pós-venda dedicado.

---

## 4) Recomendações estratégicas priorizadas

### Prioridade 1 — Excelência logística (impacto alto / prazo curto)
1. Implantar gestão ativa de SLA por região e seller.
2. Criar alertas de risco de atraso por pedido (D-2/D-1).
3. Renegociar malha e contratos para regiões com pior custo-prazo.

**Impacto esperado:** queda de atrasos, melhora de `review_score`, aumento de recompra.

### Prioridade 2 — Rentabilidade comercial (impacto alto / prazo médio)
1. Revisar portfólio por margem líquida após frete.
2. Incentivar categorias com melhor margem e menor fricção logística.
3. Reduzir dependência de sellers/categorias concentradas.

**Impacto esperado:** expansão de margem e menor volatilidade de receita.

### Prioridade 3 — Fidelização e LTV (impacto médio / prazo médio)
1. Segmentar clientes por comportamento de compra/avaliação.
2. Ativar jornadas de CRM pós-entrega (NPS/review/recompra).
3. Política de recuperação para pedidos com experiência ruim.

**Impacto esperado:** maior retenção, LTV e estabilidade de crescimento.

---

## 5) Plano de ação para 90 dias
- **0–30 dias:** baseline dos KPIs e identificação de rotas/sellers críticos.
- **31–60 dias:** execução de pilotos logísticos e ajustes de portfólio.
- **61–90 dias:** escala das frentes com melhor ROI e governança mensal com diretoria/investidores.

---

## 6) Conclusão para acionistas
O dataset Olist permite evidenciar que o valor econômico no e-commerce depende da combinação de:
1. **crescimento comercial com disciplina de mix**,
2. **operação logística previsível** e
3. **experiência do cliente como alavanca de retenção**.

A recomendação é priorizar iniciativas com impacto simultâneo em **margem + satisfação + recompra**, maximizando retorno sobre capital investido com risco operacional controlado.
