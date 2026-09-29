from __future__ import annotations

import pandas as pd

from .config import ANALYSIS_END, ANALYSIS_START, ELIGIBLE_STATUS


def _add_eligibility_flags(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    start = pd.Timestamp(ANALYSIS_START)
    end = pd.Timestamp(ANALYSIS_END) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
    result["is_delivered"] = result["order_status"].eq(ELIGIBLE_STATUS)
    result["is_in_analysis_period"] = result["order_purchase_timestamp"].between(start, end)
    result["is_eligible_analysis"] = result["is_delivered"] & result["is_in_analysis_period"]
    result["order_month"] = result["order_purchase_timestamp"].dt.to_period("M").astype("string")
    result["order_year"] = result["order_purchase_timestamp"].dt.year.astype("Int64")
    return result


def build_fato_itens(
    orders: pd.DataFrame,
    items: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    orders_customer = orders.merge(customers, on="customer_id", how="left", validate="many_to_one")
    orders_customer = _add_eligibility_flags(orders_customer)

    fato = items.merge(orders_customer, on="order_id", how="left", validate="many_to_one")
    fato = fato.merge(products, on="product_id", how="left", validate="many_to_one")

    duplicated_key = fato.duplicated(["order_id", "order_item_id"]).sum()
    if duplicated_key:
        raise ValueError(f"fato_itens has duplicated order item keys: {duplicated_key}")

    return fato


def build_fato_pedidos(fato_itens: pd.DataFrame) -> pd.DataFrame:
    item_agg = (
        fato_itens.groupby("order_id", dropna=False)
        .agg(
            items_count=("order_item_id", "count"),
            order_price_cents=("price_cents", "sum"),
            order_freight_cents=("freight_cents", "sum"),
            order_price=("price", "sum"),
            order_freight=("freight_value", "sum"),
            customer_id=("customer_id", "first"),
            customer_unique_id=("customer_unique_id", "first"),
            customer_state=("customer_state", "first"),
            order_status=("order_status", "first"),
            order_purchase_timestamp=("order_purchase_timestamp", "first"),
            order_month=("order_month", "first"),
            order_year=("order_year", "first"),
            is_delivered=("is_delivered", "first"),
            is_in_analysis_period=("is_in_analysis_period", "first"),
            is_eligible_analysis=("is_eligible_analysis", "first"),
        )
        .reset_index()
    )

    duplicated_orders = item_agg["order_id"].duplicated().sum()
    if duplicated_orders:
        raise ValueError(f"fato_pedidos has duplicated order keys: {duplicated_orders}")

    item_agg["ticket_sem_frete"] = item_agg["order_price"]
    return item_agg


def validate_analytics_bases(fato_itens: pd.DataFrame, fato_pedidos: pd.DataFrame) -> pd.DataFrame:
    eligible_items = fato_itens[fato_itens["is_eligible_analysis"].fillna(False)]
    eligible_orders = fato_pedidos[fato_pedidos["is_eligible_analysis"].fillna(False)]

    rows = [
        {
            "check": "unique_item_key",
            "expected": 0,
            "observed": int(fato_itens.duplicated(["order_id", "order_item_id"]).sum()),
        },
        {
            "check": "unique_order_key",
            "expected": 0,
            "observed": int(fato_pedidos["order_id"].duplicated().sum()),
        },
        {
            "check": "eligible_price_cents_reconciliation",
            "expected": int(eligible_items["price_cents"].sum()),
            "observed": int(eligible_orders["order_price_cents"].sum()),
        },
        {
            "check": "eligible_freight_cents_reconciliation",
            "expected": int(eligible_items["freight_cents"].sum()),
            "observed": int(eligible_orders["order_freight_cents"].sum()),
        },
        {
            "check": "eligible_distinct_orders",
            "expected": int(eligible_items["order_id"].nunique()),
            "observed": int(len(eligible_orders)),
        },
    ]
    result = pd.DataFrame(rows)
    result["status"] = result.apply(
        lambda row: "ok" if row["expected"] == row["observed"] else "review", axis=1
    )
    return result

