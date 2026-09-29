from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from olist.clean import money_to_cents
from olist.model import build_fato_itens, build_fato_pedidos, validate_analytics_bases
from olist.metrics import comparable_periods, delivery_review_metrics


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
                "order_delivered_customer_date": [pd.Timestamp("2017-01-15")],
                "order_estimated_delivery_date": [pd.Timestamp("2017-01-15")],
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

        altered = fato_pedidos.copy()
        altered.loc[0, "order_price_cents"] += 1
        failed = validate_analytics_bases(fato_itens, altered)
        self.assertEqual(
            failed.set_index("check").loc["eligible_price_cents_reconciliation", "status"],
            "review",
        )
        missing_source_order = pd.concat([orders, orders.assign(order_id="order_2")], ignore_index=True)
        coverage = validate_analytics_bases(fato_itens, fato_pedidos, missing_source_order)
        self.assertEqual(
            coverage.set_index("check").loc["eligible_orders_source_coverage", "status"],
            "review",
        )

    def test_comparison_uses_same_months_and_order_grain(self):
        orders = pd.DataFrame({
            "order_id": ["a", "b", "c"],
            "is_eligible_analysis": [True, True, True],
            "order_purchase_timestamp": pd.to_datetime(["2017-02-01", "2018-02-01", "2017-11-01"]),
            "order_year": [2017, 2018, 2017],
            "order_price_cents": [10000, 20000, 100000],
        })
        result = comparable_periods(orders)
        self.assertEqual(result["pedidos"].tolist(), [1, 1])
        self.assertEqual(result["valor_itens"].tolist(), [100.0, 200.0])
        self.assertEqual(result["variacao_valor_itens"].iloc[-1], 1.0)

    def test_repeated_reviews_and_same_day_delivery(self):
        orders = pd.DataFrame({
            "order_id": ["a", "b"],
            "is_eligible_analysis": [True, True],
            "order_delivered_customer_date": pd.to_datetime(["2018-01-10 18:00", "2018-01-12 12:00"]),
            "order_estimated_delivery_date": pd.to_datetime(["2018-01-10", "2018-01-10"]),
        })
        reviews = pd.DataFrame({"order_id": ["a", "a", "b"], "review_score": [5, 4, 1]})
        result = delivery_review_metrics(orders, reviews).set_index("situacao")
        self.assertEqual(result["pedidos_com_prazo_observavel"].sum(), 2)
        self.assertEqual(result.loc["No prazo", "pedidos_com_avaliacao"], 1)
        self.assertEqual(result.loc["Atrasou", "percentual_notas_1_ou_2"], 1.0)


if __name__ == "__main__":
    unittest.main()
