import pandas as pd


class StockScreener:

    def __init__(
        self,
        min_score=70,
        weights=None
    ):
        self.min_score = min_score

        self.weights = weights or {
            "fundamental": 0.30,
            "technical": 0.30,
            "industry": 0.15,
            "momentum": 0.15,
            "risk": 0.10
        }

    def calculate_score(self, row):

        score = (
            row.get("fundamental_score", 50)
            * self.weights["fundamental"]

            + row.get("technical_score", 50)
            * self.weights["technical"]

            + row.get("industry_score", 50)
            * self.weights["industry"]

            + row.get("momentum_score", 50)
            * self.weights["momentum"]

            + row.get("risk_score", 50)
            * self.weights["risk"]
        )

        return score

    def screen(self, df):

        result = df.copy()

        result["total_score"] = result.apply(
            self.calculate_score,
            axis=1
        )

        result = result[
            result["total_score"] >= self.min_score
        ]

        return result.sort_values(
            "total_score",
            ascending=False
        )
