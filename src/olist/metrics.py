from __future__ import annotations

import pandas as pd


def _eligible_orders(fato_pedidos: pd.DataFrame) -> pd.DataFrame:
    return fato_pedidos[fato_pedidos["is_eligible_analysis"].fillna(False)].copy()


def _eligible_items(fato_itens: pd.DataFrame) -> pd.DataFrame:
    return fato_itens[fato_itens["is_eligible_analysis"].fillna(False)].copy()


def executive_summary(fato_pedidos: pd.DataFrame, fato_itens: pd.DataFrame) -> pd.DataFrame:
    orders = _eligible_orders(fato_pedidos)
    items = _eligible_items(fato_itens)
    total_orders = orders["order_id"].nunique()
    total_price = orders["order_price"].sum()
    total_freight = orders["order_freight"].sum()
    rows = [
        ("Pedidos entregues no recorte", total_orders),
        ("Clientes unicos no recorte", orders["customer_unique_id"].nunique()),
        ("Itens vendidos no recorte", len(items)),
        ("Valor dos itens vendidos", round(float(total_price), 2)),
        ("Frete associado", round(float(total_freight), 2)),
        ("Ticket medio sem frete", round(float(total_price / total_orders), 2)),
        ("Primeiro mes do recorte", str(orders["order_month"].min())),
        ("Ultimo mes do recorte", str(orders["order_month"].max())),
    ]
    return pd.DataFrame(rows, columns=["indicador", "valor"])


def monthly_metrics(fato_pedidos: pd.DataFrame) -> pd.DataFrame:
    orders = _eligible_orders(fato_pedidos)
    result = (
        orders.groupby("order_month")
        .agg(
            pedidos=("order_id", "nunique"),
            clientes=("customer_unique_id", "nunique"),
            valor_itens=("order_price", "sum"),
            frete=("order_freight", "sum"),
        )
        .reset_index()
        .sort_values("order_month")
    )
    result["ticket_medio_sem_frete"] = result["valor_itens"] / result["pedidos"]
    return result


def category_metrics(fato_itens: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    items = _eligible_items(fato_itens)
    result = (
        items.groupby("product_category_name_english", dropna=False)
        .agg(
            pedidos=("order_id", "nunique"),
            itens=("order_item_id", "count"),
            valor_itens=("price", "sum"),
            frete=("freight_value", "sum"),
        )
        .reset_index()
        .sort_values("valor_itens", ascending=False)
    )
    total = result["valor_itens"].sum()
    result["participacao_valor"] = result["valor_itens"] / total
    return result.head(top_n)


def state_metrics(fato_pedidos: pd.DataFrame) -> pd.DataFrame:
    orders = _eligible_orders(fato_pedidos)
    result = (
        orders.groupby("customer_state", dropna=False)
        .agg(
            pedidos=("order_id", "nunique"),
            clientes=("customer_unique_id", "nunique"),
            valor_itens=("order_price", "sum"),
            frete=("order_freight", "sum"),
        )
        .reset_index()
        .sort_values("valor_itens", ascending=False)
    )
    result["participacao_valor"] = result["valor_itens"] / result["valor_itens"].sum()
    return result


def order_value_distribution(fato_pedidos: pd.DataFrame) -> pd.DataFrame:
    orders = _eligible_orders(fato_pedidos)
    values = orders["order_price"].dropna()
    stats = {
        "count": int(values.count()),
        "mean": round(float(values.mean()), 2),
        "median": round(float(values.median()), 2),
        "std": round(float(values.std()), 2),
        "min": round(float(values.min()), 2),
        "q1": round(float(values.quantile(0.25)), 2),
        "q3": round(float(values.quantile(0.75)), 2),
        "max": round(float(values.max()), 2),
    }
    return pd.DataFrame([stats])

