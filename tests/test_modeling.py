from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from olist.clean import money_to_cents
from olist.model import build_fato_itens, build_fato_pedidos, validate_analytics_bases


class ModelingTests(unittest.TestCase):
    def test_money_to_cents_uses_two_decimal_places(self):
        self.assertEqual(money_to_cents("10"), 1000)
        self.assertEqual(money_to_cents("10.235"), 1024)
        self.assertTrue(pd.isna(money_to_cents(None)))

    def test_order_level_model_does_not_duplicate_item_values(self):
        orders = pd.DataFrame(
            {
                "order_id": ["order_1"],
                "customer_id": ["customer_1"],
                "order_status": ["delivered"],
                "order_purchase_timestamp": [pd.Timestamp("2017-01-10")],
            }
        )
        customers = pd.DataFrame(
            {
                "customer_id": ["customer_1"],
                "customer_unique_id": ["unique_1"],
                "customer_zip_code_prefix": ["01001"],
                "customer_city": ["sao paulo"],
                "customer_state": ["SP"],
            }
        )
        products = pd.DataFrame(
            {
                "product_id": ["product_1", "product_2"],
                "product_category_name": ["cat_a", "cat_b"],
                "product_category_name_english": ["cat_a", "cat_b"],
                "product_category_name_display": ["cat_a", "cat_b"],
            }
        )
        items = pd.DataFrame(
            {
                "order_id": ["order_1", "order_1"],
                "order_item_id": [1, 2],
                "product_id": ["product_1", "product_2"],
                "seller_id": ["seller_1", "seller_2"],
                "shipping_limit_date": [pd.Timestamp("2017-01-12"), pd.Timestamp("2017-01-12")],
                "price": [10.0, 20.0],
                "freight_value": [2.0, 3.0],
                "price_cents": pd.Series([1000, 2000], dtype="Int64"),
                "freight_cents": pd.Series([200, 300], dtype="Int64"),
            }
        )

        fato_itens = build_fato_itens(orders, items, customers, products)
        fato_pedidos = build_fato_pedidos(fato_itens)
        validation = validate_analytics_bases(fato_itens, fato_pedidos)

        self.assertEqual(len(fato_pedidos), 1)
        self.assertEqual(int(fato_pedidos.loc[0, "items_count"]), 2)
        self.assertEqual(float(fato_pedidos.loc[0, "order_price"]), 30.0)
        self.assertEqual(float(fato_pedidos.loc[0, "order_freight"]), 5.0)
        self.assertTrue(validation["status"].eq("ok").all())


if __name__ == "__main__":
    unittest.main()
