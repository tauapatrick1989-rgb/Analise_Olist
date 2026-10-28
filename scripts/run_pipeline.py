"""Ponto de entrada da análise comercial e logística do Tech Challenge Olist."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")

from olist.audit import audit_raw_files
from olist.clean import clean_central_tables
from olist.config import DATA_ANALYTICS, DATA_CLEAN, REPORTS_FIGURES, REPORTS_QUALITY, REPORTS_TABLES
from olist.io import load_raw_tables, save_tables
from olist.logistics import (
    category_delivery_times, delivery_review_metrics, prepare_delivery_orders, state_logistics,
)
from olist.metrics import (
    category_metrics, comparable_periods, executive_summary, monthly_metrics,
    order_value_distribution, seller_metrics, state_metrics,
)
from olist.model import build_fato_itens, build_fato_pedidos, validate_analytics_bases
from olist.visualizations import save_figures


def main() -> None:
    raw = load_raw_tables()
    audit = audit_raw_files(raw)
    save_tables(audit, REPORTS_QUALITY)
    for name in ("keys", "relationships"):
        if audit[name]["status"].eq("review").any():
            raise ValueError(f"Problemas na auditoria de {name}; consulte reports/qualidade")

    clean = clean_central_tables(raw)
    save_tables(clean, DATA_CLEAN)
    items = build_fato_itens(clean["orders"], clean["items"], clean["customers"], clean["products"])
    orders = build_fato_pedidos(items)
    checks = validate_analytics_bases(items, orders, clean["orders"])
    save_tables({"validacao_bases_analiticas": checks}, REPORTS_QUALITY)
    if not checks["status"].eq("ok").all():
        raise ValueError("Validação das bases analíticas falhou; consulte reports/qualidade")

    delivery = prepare_delivery_orders(orders, raw["reviews"])
    save_tables({"fato_itens": items, "fato_pedidos": orders, "entregas_pedidos": delivery}, DATA_ANALYTICS)
    tables = {
        "resumo_executivo": executive_summary(orders, items),
        "metricas_mensais": monthly_metrics(orders),
        "metricas_categorias_top15": category_metrics(items),
        "metricas_ufs": state_metrics(orders),
        "distribuicao_valor_pedido": order_value_distribution(orders),
        "comparativo_jan_jul": comparable_periods(orders),
        "metricas_vendedores_top15": seller_metrics(items),
        "entrega_e_avaliacao": delivery_review_metrics(delivery),
        "logistica_por_uf": state_logistics(delivery),
        "tempo_entrega_por_categoria": category_delivery_times(items, delivery),
    }
    save_tables(tables, REPORTS_TABLES)
    save_figures(tables, REPORTS_FIGURES)
    print(f"Pipeline concluído: {len(tables)} tabelas de indicadores e 6 gráficos.")
    print(f"Qualidade: {REPORTS_QUALITY}\nIndicadores: {REPORTS_TABLES}\nGráficos: {REPORTS_FIGURES}")


if __name__ == "__main__":
    main()
