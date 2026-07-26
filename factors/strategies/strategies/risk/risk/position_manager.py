class PositionManager:

    def __init__(
        self,
        capital=50000,
        max_single_position=0.20,
        max_total_position=0.80,
        max_trade_risk=0.01
    ):
        self.capital = capital
        self.max_single_position = max_single_position
        self.max_total_position = max_total_position
        self.max_trade_risk = max_trade_risk

    def calculate_position(
        self,
        entry_price,
        stop_price,
        confidence=1.0,
        current_total_position=0
    ):

        if entry_price <= 0:
            raise ValueError(
                "entry_price 必须大于 0"
            )

        if stop_price >= entry_price:
            raise ValueError(
                "止损价必须低于买入价"
            )

        risk_per_share = (
            entry_price - stop_price
        )

        max_risk_money = (
            self.capital
            * self.max_trade_risk
            * confidence
        )

        shares_by_risk = (
            max_risk_money
            / risk_per_share
        )

        max_position_money = (
            self.capital
            * self.max_single_position
        )

        shares_by_position = (
            max_position_money
            / entry_price
        )

        shares = min(
            shares_by_risk,
            shares_by_position
        )

        shares = int(
            shares // 100
        ) * 100

        position_money = (
            shares
            * entry_price
        )

        remaining_position = (
            self.max_total_position
            - current_total_position
        )

        max_total_money = (
            self.capital
            * max(
                remaining_position,
                0
            )
        )

        if position_money > max_total_money:

            shares = int(
                (
                    max_total_money
                    / entry_price
                )
                // 100
            ) * 100

            position_money = (
                shares
                * entry_price
            )

        return {
            "shares": shares,
            "position_money": position_money,
            "position_ratio": (
                position_money
                / self.capital
            ),
            "risk_money": (
                shares
                * risk_per_share
            )
        }
