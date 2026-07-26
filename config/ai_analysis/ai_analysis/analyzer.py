class StockAnalyzer:

    def analyze(
        self,
        symbol,
        score,
        technical_score,
        fundamental_score,
        entry_price,
        stop_loss,
        take_profit
    ):

        risk_reward = (
            (
                take_profit
                - entry_price
            )
            /
            (
                entry_price
                - stop_loss
            )
        )

        if score >= 80:
            confidence = "HIGH"
        elif score >= 70:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        if risk_reward >= 3:
            action = "优先关注"
        elif risk_reward >= 2:
            action = "等待合理买点"
        else:
            action = "暂不参与"

        return {
            "symbol": symbol,
            "total_score": round(score, 2),
            "technical_score":
                round(technical_score, 2),
            "fundamental_score":
                round(fundamental_score, 2),
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward":
                round(risk_reward, 2),
            "confidence": confidence,
            "action": action
        }
