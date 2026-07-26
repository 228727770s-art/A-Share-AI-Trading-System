import pandas as pd
import numpy as np


def score_fundamental(row: pd.Series) -> float:
    score = 50.0

    revenue_growth = row.get("revenue_growth", 0)
    profit_growth = row.get("profit_growth", 0)
    roe = row.get("roe", 0)
    gross_margin = row.get("gross_margin", 0)
    debt_ratio = row.get("debt_ratio", 50)
    pe = row.get("pe", 30)

    if revenue_growth >= 30:
        score += 15
    elif revenue_growth >= 15:
        score += 10
    elif revenue_growth >= 5:
        score += 5
    elif revenue_growth < 0:
        score -= 10

    if profit_growth >= 30:
        score += 15
    elif profit_growth >= 15:
        score += 10
    elif profit_growth >= 5:
        score += 5
    elif profit_growth < 0:
        score -= 15

    if roe >= 20:
        score += 10
    elif roe >= 12:
        score += 5
    elif roe < 5:
        score -= 5

    if gross_margin >= 40:
        score += 5
    elif gross_margin < 15:
        score -= 5

    if debt_ratio > 80:
        score -= 10
    elif debt_ratio < 50:
        score += 5

    if 0 < pe <= 20:
        score += 5
    elif pe > 60:
        score -= 10

    return float(np.clip(score, 0, 100))


def calculate_fundamental_scores(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result["fundamental_score"] = result.apply(
        score_fundamental,
        axis=1
    )

    return result
