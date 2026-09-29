from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DATA_CLEAN = DATA_PROCESSED / "clean"
DATA_ANALYTICS = DATA_PROCESSED / "analytics"
REPORTS = PROJECT_ROOT / "reports"
REPORTS_QUALITY = REPORTS / "qualidade"
REPORTS_TABLES = REPORTS / "tabelas"
REPORTS_FIGURES = REPORTS / "figuras"

RAW_FILES = {
    "customers": "olist_customers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

CENTRAL_TABLES = ("orders", "items", "customers", "products")

ANALYSIS_START = "2017-01-01"
ANALYSIS_END = "2018-07-31"
ELIGIBLE_STATUS = "delivered"

