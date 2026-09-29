from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def save_figures(
    monthly: pd.DataFrame,
    categories: pd.DataFrame,
    states: pd.DataFrame,
    output_dir: Path,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")
    generated: list[Path] = []

    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(data=monthly, x="order_month", y="pedidos", marker="o", ax=ax)
    ax.set_title("Evolucao mensal de pedidos entregues")
    ax.set_xlabel("Mes da compra")
    ax.set_ylabel("Pedidos")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    path = output_dir / "evolucao_pedidos.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    generated.append(path)

    fig, ax = plt.subplots(figsize=(11, 5))
    sns.lineplot(data=monthly, x="order_month", y="valor_itens", marker="o", ax=ax)
    ax.set_title("Evolucao mensal do valor dos itens")
    ax.set_xlabel("Mes da compra")
    ax.set_ylabel("Valor dos itens (R$)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    path = output_dir / "evolucao_valor_itens.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    generated.append(path)

    fig, ax = plt.subplots(figsize=(10, 6))
    top_categories = categories.sort_values("valor_itens", ascending=True).tail(10)
    sns.barplot(data=top_categories, x="valor_itens", y="product_category_name_english", ax=ax)
    ax.set_title("Top 10 categorias por valor dos itens")
    ax.set_xlabel("Valor dos itens (R$)")
    ax.set_ylabel("Categoria")
    fig.tight_layout()
    path = output_dir / "top_categorias_valor.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    generated.append(path)

    fig, ax = plt.subplots(figsize=(10, 5))
    top_states = states.sort_values("valor_itens", ascending=False).head(10)
    sns.barplot(data=top_states, x="customer_state", y="valor_itens", ax=ax)
    ax.set_title("Top 10 UFs por valor dos itens")
    ax.set_xlabel("UF do cliente")
    ax.set_ylabel("Valor dos itens (R$)")
    fig.tight_layout()
    path = output_dir / "top_ufs_valor.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    generated.append(path)

    return generated

