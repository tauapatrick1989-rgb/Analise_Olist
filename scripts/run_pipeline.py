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
    monthly_metrics,
    order_value_distribution,
    state_metrics,
)
from olist.model import build_fato_itens, build_fato_pedidos, validate_analytics_bases
from olist.visualizations import save_figures


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
    validation = validate_analytics_bases(fato_itens, fato_pedidos)

    save_tables(
        {
            "fato_itens": fato_itens,
            "fato_pedidos": fato_pedidos,
        },
        DATA_ANALYTICS,
    )
    validation.to_csv(REPORTS_QUALITY / "validacao_bases_analiticas.csv", index=False)

    monthly = monthly_metrics(fato_pedidos)
    categories = category_metrics(fato_itens)
    states = state_metrics(fato_pedidos)
    summary = executive_summary(fato_pedidos, fato_itens)
    distribution = order_value_distribution(fato_pedidos)

    save_tables(
        {
            "resumo_executivo": summary,
            "metricas_mensais": monthly,
            "metricas_categorias_top15": categories,
            "metricas_ufs": states,
            "distribuicao_valor_pedido": distribution,
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
