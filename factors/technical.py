import pandas as pd
import numpy as np


def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    result = result.sort_values("date").reset_index(drop=True)

    result["ma5"] = result["close"].rolling(5).mean()
    result["ma10"] = result["close"].rolling(10).mean()
    result["ma20"] = result["close"].rolling(20).mean()
    result["ma60"] = result["close"].rolling(60).mean()

    delta = result["close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    result["rsi14"] = 100 - (
        100 / (1 + rs)
    )

    ema12 = result["close"].ewm(
        span=12,
        adjust=False
    ).mean()

    ema26 = result["close"].ewm(
        span=26,
        adjust=False
    ).mean()

    result["dif"] = ema12 - ema26

    result["dea"] = result["dif"].ewm(
        span=9,
        adjust=False
    ).mean()

    result["macd"] = (
        result["dif"] - result["dea"]
    ) * 2

    result["volume_ma20"] = (
        result["volume"]
        .rolling(20)
        .mean()
    )

    result["volume_ratio"] = (
        result["volume"]
        / result["volume_ma20"]
    )

    return result


def score_technical(row: pd.Series) -> float:
    score = 50.0

    close = row.get("close", 0)
    ma20 = row.get("ma20", np.nan)
    ma60 = row.get("ma60", np.nan)
    rsi = row.get("rsi14", 50)
    macd = row.get("macd", 0)
    volume_ratio = row.get("volume_ratio", 1)

    if pd.notna(ma20) and close > ma20:
        score += 10
    else:
        score -= 10

    if pd.notna(ma60) and close > ma60:
        score += 10
    else:
        score -= 10

    if 45 <= rsi <= 65:
        score += 10
    elif rsi > 80:
        score -= 15
    elif rsi < 25:
        score += 5

    if macd > 0:
        score += 10
    else:
        score -= 5

    if volume_ratio >= 1.2:
        score += 5
    elif volume_ratio < 0.5:
        score -= 5

    return float(np.clip(score, 0, 100))


def calculate_technical_score(df):
    result = calculate_technical_indicators(df)

    result["technical_score"] = result.apply(
        score_technical,
        axis=1
    )

    return result
