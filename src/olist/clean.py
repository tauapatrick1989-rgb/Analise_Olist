from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

import pandas as pd

from .io import read_raw


MISSING_CATEGORY = "Sem categoria informada"
MISSING_CATEGORY_EN = "not_informed"


def money_to_cents(value: object) -> pd.NA | int:
    if pd.isna(value):
        return pd.NA
    try:
        amount = Decimal(str(value).strip()).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return pd.NA
    return int(amount * 100)


def clean_orders() -> pd.DataFrame:
    df = read_raw("orders")
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


def clean_customers() -> pd.DataFrame:
    df = read_raw("customers")
    df["customer_zip_code_prefix"] = df["customer_zip_code_prefix"].str.zfill(5)
    df["customer_city"] = df["customer_city"].str.strip().str.lower()
    df["customer_state"] = df["customer_state"].str.strip().str.upper()
    return df


def clean_products() -> pd.DataFrame:
    products = read_raw("products")
    translation = read_raw("category_translation")
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


def clean_items() -> pd.DataFrame:
    df = read_raw("items")
    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")
    df["price_cents"] = df["price"].map(money_to_cents).astype("Int64")
    df["freight_cents"] = df["freight_value"].map(money_to_cents).astype("Int64")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["freight_value"] = pd.to_numeric(df["freight_value"], errors="coerce")
    return df


def clean_central_tables() -> dict[str, pd.DataFrame]:
    return {
        "orders": clean_orders(),
        "customers": clean_customers(),
        "products": clean_products(),
        "items": clean_items(),
    }

