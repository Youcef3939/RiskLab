# 🧪 RISKLAB
**your financial risk assessment toolkit**
interactive, modular, and built for quants, developers, and anyone who wants to see the **real risk behind portfolios**

![alt text](<image.png>)

![Python Version](https://img.shields.io/badge/python-3.11+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-%23FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Risk Level](https://img.shields.io/badge/risk-high-red)
![Finance](https://img.shields.io/badge/finance-%F0%9F%92%B0-yellow)


---

## ⚡ overview

**RiskLab** is an **interactive python toolkit for financial risk analysis, stress testing, and visualization**

designed for quants, developers, and finance enthusiasts, RiskLab lets you **assess portfolio risk, simulate shocks, and generate actionable insights**

KEY HIGHLIGHTS:

- **risk matrix heatmaps:** likelihood x impact visualization

- **interactive streamlit dashboard:** real time portfolio risk insights

- **plug-in system:** add your own risk models and metrics

- **core metrics:** VaR, CVaR, volatility, sharpe ratio


---

## 🚀 features

### core

- load portfolios from **CSV, JSON, or APIs** (yfinance, alpaca)

- liquidity risk checks: identify oversized positions

- auto-generate **markdown/PDF risk reports**

### advanced

- **risk matrix:** visualize likelihood x impact with heatmaps

- **interactive dashboard:** upload portfolios, simulate shocks, see metrics live

- **plug-in system:** drop new `.py` files in `plugins/` to extend RiskLab

- **modular & extensible:** add metrics, visualizations, dashboards


---

## 🎯 quickstart

```python

from src.portfolio import Portfolio
from src.risk_metrics import VaR, CVaR
from src.risk_matrix import RiskMatrix
from src.report import generate_report

# Load your portfolio
portfolio = Portfolio("examples/sample_portfolio.csv")

# Compute risk metrics
var = VaR(portfolio)
cvar = CVaR(portfolio)

# Generate Risk Matrix
rm = RiskMatrix(portfolio)
rm.plot_heatmap()

# Export professional report
generate_report(portfolio, var, cvar, rm, output="examples/report.pdf")
```

then launch the dashboard

streamlit run src/dashboard.py


---

## 🏗 architecture & workflow

### architecture


+-------------------+
|  Portfolio Input  |
|  CSV / JSON / API |
+---------+---------+
          |
          v
+-------------------+
|   Portfolio Loader|
|   (src/portfolio) |
+---------+---------+
          |
          v
+-------------------+      +------------------+
|  Risk Metrics     | ---> |  Stress Testing  |
| (VaR, CVaR, etc) |      | (historical &    |
| (src/risk_metrics)|      |  custom shocks) |
+---------+---------+      +------------------+
          |
          v
+-------------------+
| Liquidity Checks  |
| (src/liquidity)   |
+---------+---------+
          |
          v
+-------------------+
|  Risk Matrix      |
| (Heatmap & JSON)  |
| (src/risk_matrix) |
+---------+---------+
          |
          v
+-------------------+      +------------------+
| Report Generator  | ---> | Plug-in System   |
| (Markdown/PDF)    |      | (src/plugins)    |
+-------------------+      +------------------+
          |
          v
+-------------------+
| Streamlit Dashboard|
|  (src/dashboard)  |
+-------------------+


### workflow

1. portfolio input

users provide a portfolio in CSV, JSON, or via APIs (e.g., yfinance)

2. portfolio loader (portfolio.py)

validates input, computes holdings, positions, and normalizes data for risk calculations

3. risk Metrics (risk_metrics.py)
calculates core metrics such as VaR, CVaR, volatility, and sharpe ratio

4. stress testing (stress_test.py)

applies historical or user-defined shocks to simulate extreme market scenarios

5. liquidity checks (liquidity.py)

flags oversized positions relative to market volume to prevent illiquidity issues

6. risk matrix (risk_matrix.py)

generates a likelihood × impact heatmap and exports data in JSON or PNG format

7. plug-in system (plugins/)

users can drop custom risk model modules here; RiskLab automatically detects and integrates them

8. report generator (report.py)

combines all computed metrics, stress tests, and risk matrices into professional Markdown or PDF reports

9. interactive dashboard (dashboard.py)

pulls all modules together in a streamlit interface for real-time portfolio exploration, risk visualization, and scenario simulation


---

## example output

![alt text](<Capture d'écran 2025-09-20 221708.png>) ![alt text](<Capture d'écran 2025-09-20 221726.png>) ![alt text](<Capture d'écran 2025-09-20 221749.png>) ![alt text](<Capture d'écran 2025-09-20 221812.png>) ![alt text](<Capture d'écran 2025-09-20 221831.png>)


---


## project structure

- data/     : # sample portfolios

- src/      : # core python package

- reports/  : # the reports generated after running the pipeline

- plugins/  : # custom risk model plug-ins

- tests/    : # unit tests

- examples/ : # jupyter notebooks and usages examples


---

## 🤝 contributing

- fork it

- branch it

- add code + tests

- sumbit a PR

follow PEP8, write clear docstrings, and make RiskLab better for eceryone!