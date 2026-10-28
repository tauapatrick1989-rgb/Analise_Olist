from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import pandas as pd


MISSING_CATEGORY = "Sem categoria informada"
MISSING_CATEGORY_EN = "not_informed"


def money_to_cents(value: object) -> int | None:
    """Converta reais em centavos com arredondamento decimal comercial."""
    if pd.isna(value):
        return None
    try:
        amount = Decimal(str(value).strip()).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return None
    if not amount.is_finite():
        return None
    return int(amount * 100)


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    df = orders.copy()
    date_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    df["order_status"] = df["order_status"].str.strip().str.lower()
    return df


def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    df = customers.copy()
    df["customer_zip_code_prefix"] = df["customer_zip_code_prefix"].str.zfill(5)
    df["customer_city"] = df["customer_city"].str.strip().str.lower()
    df["customer_state"] = df["customer_state"].str.strip().str.upper()
    return df


def clean_products(products: pd.DataFrame, translation: pd.DataFrame) -> pd.DataFrame:
    df = products.merge(
        translation,
        on="product_category_name",
        how="left",
        validate="many_to_one",
    )
    df["product_category_name_display"] = df["product_category_name"].fillna(MISSING_CATEGORY)
    df["product_category_name_english"] = df["product_category_name_english"].fillna(
        MISSING_CATEGORY_EN
    )
    numeric_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def clean_items(items: pd.DataFrame) -> pd.DataFrame:
    df = items.copy()
    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")
    df["price_cents"] = df["price"].map(money_to_cents).astype("Int64")
    df["freight_cents"] = df["freight_value"].map(money_to_cents).astype("Int64")
    for column in ("price_cents", "freight_cents"):
        if df[column].isna().any() or df[column].lt(0).any():
            raise ValueError(f"Valor monetário ausente, inválido ou negativo em {column}")
    df["price"] = df["price_cents"] / 100
    df["freight_value"] = df["freight_cents"] / 100
    return df


def clean_central_tables(data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Trate as quatro tabelas usadas na modelagem, preservando as fontes."""
    return {
        "orders": clean_orders(data["orders"]),
        "customers": clean_customers(data["customers"]),
        "products": clean_products(data["products"], data["category_translation"]),
        "items": clean_items(data["items"]),
    }
