import streamlit as st
import pandas as pd
import plotly.express as px

from risk.position_manager import PositionManager
from strategies.stock_screener import StockScreener
from ai_analysis.analyzer import StockAnalyzer


st.set_page_config(
    page_title="A股 AI 智能交易系统",
    layout="wide"
)

st.title(
    "A股 AI 智能交易决策系统 V1.0"
)

st.warning(
    "本系统仅用于研究和交易决策辅助，不构成投资建议。"
)


st.sidebar.header(
    "账户设置"
)

capital = st.sidebar.number_input(
    "账户资金",
    min_value=10000,
    value=50000,
    step=5000
)

entry_price = st.sidebar.number_input(
    "模拟买入价",
    min_value=0.01,
    value=20.0,
    step=0.1
)

stop_loss = st.sidebar.number_input(
    "止损价",
    min_value=0.01,
    value=18.0,
    step=0.1
)

confidence = st.sidebar.slider(
    "信心系数",
    0.5,
    1.0,
    0.8
)


manager = PositionManager(
    capital=capital
)

if stop_loss < entry_price:

    result = manager.calculate_position(
        entry_price=entry_price,
        stop_price=stop_loss,
        confidence=confidence
    )

    st.header(
        "仓位管理"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "建议股数",
        result["shares"]
    )

    col2.metric(
        "建议投入",
        f'{result["position_money"]:,.0f} 元'
    )

    col3.metric(
        "仓位比例",
        f'{result["position_ratio"]:.1%}'
    )

    col4.metric(
        "最大风险",
        f'{result["risk_money"]:,.0f} 元'
    )

else:

    st.error(
        "止损价必须低于买入价"
    )


st.header(
    "模拟股票评分"
)

sample_data = pd.DataFrame({

    "symbol": [
        "示例A",
        "示例B",
        "示例C",
        "示例D"
    ],

    "fundamental_score": [
        85, 72, 60, 90
    ],

    "technical_score": [
        80, 75, 65, 70
    ],

    "industry_score": [
        90, 70, 80, 75
    ],

    "momentum_score": [
        75, 80, 65, 60
    ],

    "risk_score": [
        70, 75, 80, 65
    ]
})


screener = StockScreener()

sample_data[
    "total_score"
] = sample_data.apply(
    screener.calculate_score,
    axis=1
)

sample_data = sample_data.sort_values(
    "total_score",
    ascending=False
)

st.dataframe(
    sample_data,
    use_container_width=True
)


st.header(
    "AI 决策分析"
)

selected = st.selectbox(
    "选择股票",
    sample_data["symbol"]
)

row = sample_data[
    sample_data["symbol"]
    == selected
].iloc[0]

analyzer = StockAnalyzer()

analysis = analyzer.analyze(
    symbol=selected,
    score=row["total_score"],
    technical_score=row[
        "technical_score"
    ],
    fundamental_score=row[
        "fundamental_score"
    ],
    entry_price=entry_price,
    stop_loss=stop_loss,
    take_profit=entry_price * 1.2
)

st.json(
    analysis
)


fig = px.bar(
    sample_data,
    x="symbol",
    y="total_score",
    title="股票综合评分"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
