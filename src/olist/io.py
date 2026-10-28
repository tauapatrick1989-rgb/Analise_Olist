from __future__ import annotations

from collections.abc import Mapping
import hashlib
from pathlib import Path

import pandas as pd

from .config import DATA_RAW, RAW_FILES


DTYPE_OVERRIDES = {
    "customers": {
        "customer_id": "string",
        "customer_unique_id": "string",
        "customer_zip_code_prefix": "string",
        "customer_city": "string",
        "customer_state": "string",
    },
    "geolocation": {
        "geolocation_zip_code_prefix": "string",
        "geolocation_city": "string",
        "geolocation_state": "string",
    },
    "items": {
        "order_id": "string",
        "order_item_id": "Int64",
        "product_id": "string",
        "seller_id": "string",
        "price": "string",
        "freight_value": "string",
    },
    "payments": {
        "order_id": "string",
        "payment_sequential": "Int64",
        "payment_type": "string",
        "payment_installments": "Int64",
        "payment_value": "string",
    },
    "reviews": {
        "review_id": "string",
        "order_id": "string",
        "review_comment_title": "string",
        "review_comment_message": "string",
    },
    "orders": {
        "order_id": "string",
        "customer_id": "string",
        "order_status": "string",
    },
    "products": {
        "product_id": "string",
        "product_category_name": "string",
    },
    "sellers": {
        "seller_id": "string",
        "seller_zip_code_prefix": "string",
        "seller_city": "string",
        "seller_state": "string",
    },
    "category_translation": {
        "product_category_name": "string",
        "product_category_name_english": "string",
    },
}


def raw_path(table: str) -> Path:
    return DATA_RAW / RAW_FILES[table]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_raw(table: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(
        raw_path(table),
        dtype=DTYPE_OVERRIDES.get(table),
        keep_default_na=True,
        **kwargs,
    )


def load_raw_tables() -> dict[str, pd.DataFrame]:
    """Leia cada CSV uma vez, preservando IDs, CEPs e valores monetários."""
    return {name: read_raw(name) for name in RAW_FILES}


def save_tables(tables: Mapping[str, pd.DataFrame], output_dir: Path) -> None:
    """Grave tabelas sem índice em um diretório de saída reproduzível."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(output_dir / f"{name}.csv", index=False)
