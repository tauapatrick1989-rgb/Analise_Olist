"""Gráficos reproduzíveis das evidências usadas na narrativa executiva."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter, StrMethodFormatter
import pandas as pd

from .config import MIN_CATEGORY_ORDERS

BLUE = "#2E5D7B"


def _save(fig: plt.Figure, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def save_figures(tables: dict[str, pd.DataFrame], output_dir: Path) -> None:
    """Gere seis figuras a partir das mesmas tabelas gravadas pelo pipeline."""
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})
    monthly = tables["metricas_mensais"]
    for column, title, ylabel, filename in (
        ("pedidos", "Evolução dos pedidos entregues", "Pedidos", "evolucao_pedidos.png"),
        ("valor_itens", "Evolução do valor dos itens", "Valor dos itens em R$", "evolucao_valor_itens.png"),
    ):
        fig, ax = plt.subplots(figsize=(10, 4.5))
        ax.plot(monthly["order_month"], monthly[column], marker="o", color=BLUE)
        ax.set(title=title, xlabel="Mês da compra", ylabel=ylabel)
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", alpha=.2)
        _save(fig, output_dir / filename)

    for key, label, title, filename in (
        ("metricas_categorias_top15", "product_category_name_english", "Categorias por valor dos itens", "top_categorias_valor.png"),
        ("metricas_ufs", "customer_state", "UFs por valor dos itens", "top_ufs_valor.png"),
    ):
        top = tables[key].head(10).sort_values("valor_itens")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(top[label], top["valor_itens"], color=BLUE)
        ax.set(title=title, xlabel="Valor dos itens em R$")
        ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
        _save(fig, output_dir / filename)

    top = tables["logistica_por_uf"].head(10)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, column, title in (
        (axes[0], "pedidos_com_possivel_reclamacao", "Volume de possíveis reclamações"),
        (axes[1], "taxa_possivel_reclamacao", "Incidência nos pedidos com prazo observável"),
    ):
        ax.bar(top["customer_state"], top[column], color=BLUE)
        ax.set(title=title, xlabel="UF do cliente")
        ax.tick_params(axis="x", labelsize=9)
    axes[0].set_ylabel("Pedidos sinalizados por nota e texto")
    axes[1].yaxis.set_major_formatter(PercentFormatter(1))
    _save(fig, output_dir / "reclamacoes_por_estado.png")

    categories = tables["tempo_entrega_por_categoria"]
    top = categories.loc[categories["total_pedidos"].ge(MIN_CATEGORY_ORDERS)].head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.barh(top["product_category_name_display"], top["tempo_medio_dias"], color=BLUE)
    ax.set(title=f"Maior tempo médio de entrega por categoria com ao menos {MIN_CATEGORY_ORDERS} pedidos",
           xlabel="Dias entre compra e entrega")
    _save(fig, output_dir / "tempo_entrega_por_categoria.png")
