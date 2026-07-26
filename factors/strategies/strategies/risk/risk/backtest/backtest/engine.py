import pandas as pd
import numpy as np


class BacktestEngine:

    def __init__(
        self,
        initial_capital=50000,
        commission_rate=0.0003,
        stamp_tax_rate=0.0005,
        slippage_rate=0.001
    ):
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.stamp_tax_rate = stamp_tax_rate
        self.slippage_rate = slippage_rate

    def run(
        self,
        df,
        signal_column="signal"
    ):

        data = df.copy()

        data = data.sort_values(
            "date"
        ).reset_index(drop=True)

        cash = self.initial_capital
        shares = 0

        equity_curve = []

        for _, row in data.iterrows():

            price = row["close"]

            signal = row.get(
                signal_column,
                0
            )

            if signal == 1 and shares == 0:

                buy_price = (
                    price
                    * (
                        1
                        + self.slippage_rate
                    )
                )

                max_shares = int(
                    cash
                    / buy_price
                    / 100
                ) * 100

                if max_shares > 0:

                    cost = (
                        max_shares
                        * buy_price
                    )

                    commission = (
                        cost
                        * self.commission_rate
                    )

                    cash -= (
                        cost
                        + commission
                    )

                    shares = max_shares

            elif signal == -1 and shares > 0:

                sell_price = (
                    price
                    * (
                        1
                        - self.slippage_rate
                    )
                )

                revenue = (
                    shares
                    * sell_price
                )

                commission = (
                    revenue
                    * self.commission_rate
                )

                stamp_tax = (
                    revenue
                    * self.stamp_tax_rate
                )

                cash += (
                    revenue
                    - commission
                    - stamp_tax
                )

                shares = 0

            equity = (
                cash
                + shares * price
            )

            equity_curve.append(
                equity
            )

        data["equity"] = equity_curve

        data["daily_return"] = (
            data["equity"].pct_change()
        )

        data["peak"] = (
            data["equity"].cummax()
        )

        data["drawdown"] = (
            data["equity"]
            / data["peak"]
            - 1
        )

        total_return = (
            data["equity"].iloc[-1]
            / self.initial_capital
            - 1
        )

        max_drawdown = (
            data["drawdown"].min()
        )

        volatility = (
            data["daily_return"].std()
        )

        if volatility > 0:

            sharpe = (
                data["daily_return"].mean()
                / volatility
                * np.sqrt(252)
            )

        else:

            sharpe = 0

        metrics = {
            "initial_capital":
                self.initial_capital,

            "final_equity":
                data["equity"].iloc[-1],

            "total_return":
                total_return,

            "max_drawdown":
                max_drawdown,

            "sharpe":
                sharpe
        }

        return data, metrics
