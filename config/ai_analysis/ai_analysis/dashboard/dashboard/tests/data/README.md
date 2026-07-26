# Data

本目录用于存放行情和基本面数据。

建议：

- raw/：原始数据
- processed/：清洗数据
- backtest/：回测数据

V1.0 不将真实行情数据提交到 GitHub。

后续可以接入：

- AKShare
- Tushare
- BaoStock
- CSV
- Parquet

注意：实际接入时必须考虑数据质量、复权方式、停牌、ST、退市股票和未来函数问题。
