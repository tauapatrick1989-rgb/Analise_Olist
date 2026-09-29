from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".matplotlib"))

from olist.audit import audit_raw_files
from olist.clean import clean_central_tables
from olist.config import DATA_ANALYTICS, DATA_CLEAN, REPORTS_FIGURES, REPORTS_QUALITY, REPORTS_TABLES
from olist.metrics import (
    category_metrics,
    executive_summary,
    comparable_periods,
    delivery_review_metrics,
    monthly_metrics,
    order_value_distribution,
    state_metrics,
    seller_metrics,
)
from olist.model import build_fato_itens, build_fato_pedidos, validate_analytics_bases
from olist.visualizations import save_figures
from olist.io import read_raw


def save_tables(tables: dict[str, object], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output_dir / f"{name}.csv", index=False)


def main() -> None:
    for path in (DATA_CLEAN, DATA_ANALYTICS, REPORTS_QUALITY, REPORTS_TABLES, REPORTS_FIGURES):
        path.mkdir(parents=True, exist_ok=True)

    audit = audit_raw_files()
    save_tables(audit, REPORTS_QUALITY)

    clean = clean_central_tables()
    save_tables(clean, DATA_CLEAN)

    fato_itens = build_fato_itens(
        orders=clean["orders"],
        items=clean["items"],
        customers=clean["customers"],
        products=clean["products"],
    )
    fato_pedidos = build_fato_pedidos(fato_itens)
    validation = validate_analytics_bases(fato_itens, fato_pedidos, clean["orders"])
    validation.to_csv(REPORTS_QUALITY / "validacao_bases_analiticas.csv", index=False)
    if not validation["status"].eq("ok").all():
        raise ValueError("Validacao das bases analiticas falhou")

    save_tables(
        {
            "fato_itens": fato_itens,
            "fato_pedidos": fato_pedidos,
        },
        DATA_ANALYTICS,
    )

    monthly = monthly_metrics(fato_pedidos)
    categories = category_metrics(fato_itens)
    states = state_metrics(fato_pedidos)
    summary = executive_summary(fato_pedidos, fato_itens)
    distribution = order_value_distribution(fato_pedidos)
    comparison = comparable_periods(fato_pedidos)
    sellers = seller_metrics(fato_itens)
    delivery_reviews = delivery_review_metrics(fato_pedidos, read_raw("reviews"))

    save_tables(
        {
            "resumo_executivo": summary,
            "metricas_mensais": monthly,
            "metricas_categorias_top15": categories,
            "metricas_ufs": states,
            "distribuicao_valor_pedido": distribution,
            "comparativo_jan_jul": comparison,
            "metricas_vendedores_top15": sellers,
            "entrega_e_avaliacao": delivery_reviews,
        },
        REPORTS_TABLES,
    )
    save_figures(monthly, categories, states, REPORTS_FIGURES)

    print("Pipeline executado com sucesso.")
    print(f"Relatorios de qualidade: {REPORTS_QUALITY}")
    print(f"Tabelas de metricas: {REPORTS_TABLES}")
    print(f"Figuras: {REPORTS_FIGURES}")


if __name__ == "__main__":
    main()
