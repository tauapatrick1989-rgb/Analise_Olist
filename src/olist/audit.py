from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .config import RAW_FILES
from .io import file_sha256, raw_path, read_raw


@dataclass(frozen=True)
class KeyCheck:
    table: str
    key: str


KEY_CHECKS = (
    KeyCheck("orders", "order_id"),
    KeyCheck("customers", "customer_id"),
    KeyCheck("products", "product_id"),
    KeyCheck("sellers", "seller_id"),
)


def audit_raw_files() -> dict[str, pd.DataFrame]:
    inventory_rows = []
    missing_rows = []
    key_rows = []
    status_rows = []

    loaded: dict[str, pd.DataFrame] = {}
    for table in RAW_FILES:
        path = raw_path(table)
        df = read_raw(table)
        loaded[table] = df

        inventory_rows.append(
            {
                "table": table,
                "file": path.name,
                "rows": len(df),
                "columns": len(df.columns),
                "duplicated_full_rows": int(df.duplicated().sum()),
                "sha256": file_sha256(path),
            }
        )

        for column, qty in df.isna().sum().items():
            missing_rows.append(
                {
                    "table": table,
                    "column": column,
                    "missing_rows": int(qty),
                    "missing_pct": round(float(qty) / len(df) * 100, 4) if len(df) else 0.0,
                }
            )

    for check in KEY_CHECKS:
        df = loaded[check.table]
        duplicated = int(df[check.key].duplicated().sum())
        key_rows.append(
            {
                "table": check.table,
                "key": check.key,
                "rows": len(df),
                "unique_keys": int(df[check.key].nunique(dropna=False)),
                "duplicated_keys": duplicated,
                "status": "ok" if duplicated == 0 else "review",
            }
        )

    orders = loaded["orders"].copy()
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"], errors="coerce"
    )
    month_status = (
        orders.assign(order_month=orders["order_purchase_timestamp"].dt.to_period("M").astype("string"))
        .groupby(["order_month", "order_status"], dropna=False)
        .size()
        .reset_index(name="orders")
        .sort_values(["order_month", "order_status"])
    )
    status_rows.extend(month_status.to_dict("records"))

    relationship_rows = _relationship_checks(loaded)

    return {
        "inventory": pd.DataFrame(inventory_rows),
        "missing_values": pd.DataFrame(missing_rows),
        "keys": pd.DataFrame(key_rows),
        "orders_by_month_status": pd.DataFrame(status_rows),
        "relationships": pd.DataFrame(relationship_rows),
    }


def _relationship_checks(data: dict[str, pd.DataFrame]) -> list[dict[str, object]]:
    orders = data["orders"]
    items = data["items"]
    payments = data["payments"]
    reviews = data["reviews"]
    customers = data["customers"]
    products = data["products"]

    order_ids = set(orders["order_id"].dropna())
    customer_ids = set(customers["customer_id"].dropna())
    product_ids = set(products["product_id"].dropna())

    checks = [
        ("items.order_id -> orders.order_id", items["order_id"], order_ids),
        ("payments.order_id -> orders.order_id", payments["order_id"], order_ids),
        ("reviews.order_id -> orders.order_id", reviews["order_id"], order_ids),
        ("orders.customer_id -> customers.customer_id", orders["customer_id"], customer_ids),
        ("items.product_id -> products.product_id", items["product_id"], product_ids),
    ]

    rows: list[dict[str, object]] = []
    for name, series, valid_values in checks:
        missing_ref = int((~series.isin(valid_values)).sum())
        rows.append(
            {
                "relationship": name,
                "checked_rows": int(series.notna().sum()),
                "missing_reference_rows": missing_ref,
                "status": "ok" if missing_ref == 0 else "review",
            }
        )

    for table_name, df in (("items", items), ("payments", payments), ("reviews", reviews)):
        counts = df.groupby("order_id", dropna=False).size()
        rows.append(
            {
                "relationship": f"{table_name} rows per order",
                "checked_rows": int(len(counts)),
                "missing_reference_rows": int((counts > 1).sum()),
                "status": "behavior_possible",
            }
        )

    return rows

