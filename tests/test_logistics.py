"""Casos de negócio que protegem denominadores e granularidade da logística."""
import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from olist.clean import clean_items, money_to_cents
from olist.logistics import (
    category_delivery_times, delivery_review_metrics, prepare_delivery_orders, state_logistics,
)
from olist.model import _add_eligibility_flags


class LogisticsTests(unittest.TestCase):
    def setUp(self):
        self.orders = pd.DataFrame({
            "order_id": ["a", "b", "c", "d"],
            "customer_state": ["SP", "SP", "RJ", "RJ"],
            "is_eligible_analysis": [True, True, True, False],
            "order_purchase_timestamp": pd.to_datetime(["2018-01-01"] * 4),
            "order_delivered_customer_date": pd.to_datetime([
                "2018-01-10 18:00", "2018-01-12 12:00", None, "2018-01-12 12:00",
            ]),
            "order_estimated_delivery_date": pd.to_datetime(["2018-01-10"] * 4),
        })
        self.reviews = pd.DataFrame({
            "order_id": ["a", "a", "b", "b", "c", "d"],
            "review_score": [5, 1, 2, 1, 1, 1],
            "review_comment_title": [None] * 6,
            "review_comment_message": ["Atrasou", "Produto quebrado", "NÃO RECEBI", "Demorou", None, "Atrasou"],
        })

    def test_same_review_must_have_negative_score_and_delay_text(self):
        orders = prepare_delivery_orders(self.orders, self.reviews).set_index("order_id")
        self.assertFalse(orders.loc["a", "possible_delay_complaint"])
        self.assertTrue(orders.loc["a", "low_review"])
        self.assertTrue(orders.loc["b", "possible_delay_complaint"])
        self.assertFalse(orders.loc["c", "possible_delay_complaint"])
        self.assertNotIn("d", orders.index)

    def test_state_rates_count_orders_once_and_exclude_unknown_deadlines(self):
        orders = prepare_delivery_orders(self.orders, self.reviews)
        state = state_logistics(orders).set_index("customer_state")
        self.assertEqual(state.loc["SP", "total_pedidos"], 2)
        self.assertEqual(state.loc["SP", "pedidos_com_possivel_reclamacao"], 1)
        self.assertEqual(state.loc["SP", "taxa_atraso"], .5)
        self.assertEqual(state.loc["SP", "taxa_possivel_reclamacao"], .5)
        self.assertNotIn("RJ", state.index)
        self.assertTrue(pd.isna(orders.set_index("order_id").loc["c", "atrasou"]))

    def test_category_duration_uses_order_category_grain(self):
        orders = prepare_delivery_orders(self.orders, self.reviews)
        items = pd.DataFrame({"order_id": ["a", "a", "a", "b", "c", "d"],
                              "product_category_name_display": ["x", "x", "y", "x", "x", "x"]})
        table = category_delivery_times(items, orders).set_index("product_category_name_display")
        self.assertEqual(table.loc["x", "total_pedidos"], 2)
        self.assertEqual(table.loc["y", "total_pedidos"], 1)
        self.assertAlmostEqual(table.loc["x", "tempo_medio_dias"], (9.75 + 11.5) / 2)
        self.assertEqual(table.loc["x", "taxa_atraso"], .5)

    def test_unreviewed_orders_remain_in_deadline_denominator(self):
        reviews = self.reviews.iloc[:0]
        orders = prepare_delivery_orders(self.orders, reviews)
        summary = delivery_review_metrics(orders)
        self.assertEqual(summary.pedidos_com_prazo_observavel.sum(), 2)
        self.assertEqual(summary.pedidos_com_avaliacao.sum(), 0)
        self.assertTrue(summary.percentual_notas_1_ou_2.isna().all())

    def test_invalid_duration_is_excluded_without_erasing_deadline_status(self):
        self.orders.loc[0, "order_purchase_timestamp"] = pd.Timestamp("2018-02-01")
        orders = prepare_delivery_orders(self.orders, self.reviews).set_index("order_id")
        self.assertTrue(pd.isna(orders.loc["a", "tempo_entrega_dias"]))
        self.assertTrue(orders.loc["a", "has_observable_deadline"])

    def test_period_includes_last_nanosecond_but_not_next_day(self):
        orders = pd.DataFrame({"order_status": ["delivered"] * 2,
            "order_purchase_timestamp": pd.to_datetime(["2018-07-31 23:59:59.999999999", "2018-08-01"], format="mixed")})
        self.assertEqual(_add_eligibility_flags(orders).is_eligible_analysis.tolist(), [True, False])

    def test_invalid_money_stops_instead_of_becoming_zero(self):
        for price in (None, "inválido", "-1"):
            with self.subTest(price=price), self.assertRaises(ValueError):
                clean_items(pd.DataFrame({"shipping_limit_date": ["2018-01-01"],
                                          "price": [price], "freight_value": ["2"]}))
        self.assertTrue(pd.isna(money_to_cents("Infinity")))


if __name__ == "__main__":
    unittest.main()
