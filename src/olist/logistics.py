"""Indicadores de prazo e sinais de reclamação com uma observação por pedido."""
from __future__ import annotations

import unicodedata

import pandas as pd

# Triagem exploratória herdada da análise inicial; não é um classificador validado.
DELAY_PATTERN = (
    r"\batrasad[oa]s?\b|\batrasou\b|\bdemorou\b|\bdemora\b|\bdemorando\b|"
    r"\bnao chegou\b|\bainda nao recebi\b|\bnao recebi\b|\bfora do prazo\b|"
    r"\bprazo de entrega\b"
)


def _normalize_text(text: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", text.lower())
        if not unicodedata.combining(char)
    )


def prepare_delivery_orders(orders: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:
    """Agregue avaliações antes da junção e mantenha ausências de prazo explícitas.

    Uma possível reclamação requer nota 1 ou 2 e palavra-chave na mesma avaliação.
    Várias avaliações não multiplicam pedidos, valores ou ocorrências por UF.
    """
    result = orders.loc[orders["is_eligible_analysis"].fillna(False)].copy()
    scores = reviews.copy()
    scores["review_score"] = pd.to_numeric(scores["review_score"], errors="coerce")
    scores["review_score"] = scores["review_score"].where(scores["review_score"].between(1, 5))
    comments = (
        scores["review_comment_title"].fillna("") + " "
        + scores["review_comment_message"].fillna("")
    ).map(_normalize_text)
    scores["low_review"] = scores["review_score"].le(2)
    scores["possible_delay_complaint"] = (
        scores["low_review"] & comments.str.contains(DELAY_PATTERN, regex=True, na=False)
    )
    review_by_order = scores.groupby("order_id").agg(
        review_score_mean=("review_score", "mean"),
        low_review=("low_review", "any"),
        possible_delay_complaint=("possible_delay_complaint", "any"),
    ).reset_index()
    result = result.merge(review_by_order, on="order_id", how="left", validate="one_to_one")
    for column in ("low_review", "possible_delay_complaint"):
        result[column] = result[column].astype("boolean").fillna(False)
    result["has_review"] = result["review_score_mean"].notna()
    actual = pd.to_datetime(result["order_delivered_customer_date"], errors="coerce")
    estimated = pd.to_datetime(result["order_estimated_delivery_date"], errors="coerce")
    purchase = pd.to_datetime(result["order_purchase_timestamp"], errors="coerce")
    result["has_observable_deadline"] = actual.notna() & estimated.notna()
    days_late = (actual.dt.normalize() - estimated.dt.normalize()).dt.days
    result["dias_atraso"] = days_late.clip(lower=0)
    result["atrasou"] = days_late.gt(0).astype("boolean").where(result["has_observable_deadline"])
    elapsed = (actual - purchase).dt.total_seconds() / 86400
    result["tempo_entrega_dias"] = elapsed.where(elapsed.ge(0))
    return result


def delivery_review_metrics(orders: pd.DataFrame) -> pd.DataFrame:
    """Compare notas apenas entre avaliados; o prazo usa todas as datas observáveis."""
    observable = orders.loc[orders["has_observable_deadline"]]
    rows = []
    for late, group in observable.groupby("atrasou"):
        reviewed = group.loc[group["has_review"]]
        rows.append({
            "situacao": "Atrasou" if late else "No prazo",
            "pedidos_com_prazo_observavel": len(group),
            "pedidos_com_avaliacao": len(reviewed),
            "percentual_notas_1_ou_2": reviewed["low_review"].mean() if len(reviewed) else float("nan"),
            "nota_media": reviewed["review_score_mean"].mean(),
        })
    return pd.DataFrame(rows, columns=[
        "situacao", "pedidos_com_prazo_observavel", "pedidos_com_avaliacao",
        "percentual_notas_1_ou_2", "nota_media",
    ])


def state_logistics(orders: pd.DataFrame) -> pd.DataFrame:
    """Compare volume e incidência de atraso e de possíveis reclamações por UF.

    Todas as taxas desta tabela são frações entre zero e um. O denominador das
    taxas é o total de pedidos com prazo observável da respectiva UF.
    """
    observable = orders.loc[orders["has_observable_deadline"]].copy()
    observable["complaint_and_late"] = observable["possible_delay_complaint"] & observable["atrasou"]
    result = observable.groupby("customer_state", dropna=False).agg(
        total_pedidos=("order_id", "nunique"),
        pedidos_atrasados=("atrasou", "sum"),
        pedidos_avaliados=("has_review", "sum"),
        pedidos_com_possivel_reclamacao=("possible_delay_complaint", "sum"),
        reclamacoes_com_atraso_real=("complaint_and_late", "sum"),
    ).reset_index()
    result["taxa_atraso"] = result["pedidos_atrasados"] / result["total_pedidos"]
    result["taxa_possivel_reclamacao"] = result["pedidos_com_possivel_reclamacao"] / result["total_pedidos"]
    return result.sort_values(
        ["pedidos_com_possivel_reclamacao", "customer_state"], ascending=[False, True]
    ).reset_index(drop=True)


def category_delivery_times(items: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    """Conte cada pedido uma vez por categoria, independentemente de seus itens.

    Pedidos com várias categorias participam de cada uma; os totais entre
    categorias não devem ser somados. Durações negativas ficam fora da análise.
    """
    categories = items[["order_id", "product_category_name_display"]].drop_duplicates()
    joined = categories.merge(
        orders[["order_id", "tempo_entrega_dias", "has_observable_deadline", "atrasou"]],
        on="order_id", how="inner", validate="many_to_one",
    )
    valid = joined.loc[joined["tempo_entrega_dias"].notna()]
    result = valid.groupby("product_category_name_display", dropna=False).agg(
        total_pedidos=("order_id", "nunique"),
        tempo_medio_dias=("tempo_entrega_dias", "mean"),
        tempo_mediano_dias=("tempo_entrega_dias", "median"),
        pedidos_com_prazo_observavel=("has_observable_deadline", "sum"),
        pedidos_atrasados=("atrasou", "sum"),
    ).reset_index()
    denominator = result["pedidos_com_prazo_observavel"].replace(0, float("nan"))
    result["taxa_atraso"] = result["pedidos_atrasados"] / denominator
    return result.sort_values(
        ["tempo_medio_dias", "product_category_name_display"], ascending=[False, True]
    ).reset_index(drop=True)
