# src/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from portfolio import Portfolio
from risk_metrics import RiskMetrics
from stress_test import StressTest
from liquidity import LiquidityMetrics
from risk_matrix import RiskMatrix

portfolio = Portfolio.from_csv("../data/sample_portfolio.csv")

np.random.seed(42)
returns = pd.DataFrame(np.random.normal(0, 0.01, (252, len(portfolio.tickers))), columns=portfolio.tickers)

rm = RiskMetrics(portfolio, returns)
rm.compute_volatility()
rm.compute_var()
rm.compute_cvar()
rm.compute_sharpe()

st_test = StressTest(portfolio, returns)
scenarios = {
    "Base": {t: 0.0 for t in portfolio.tickers},
    "Market Crash": {t: -0.1 for t in portfolio.tickers},
    "Tech Dip": {t: -0.15 for t in portfolio.tickers},
    "Bond Rally": {t: 0.05 for t in portfolio.tickers},
}
for name, adjustments in scenarios.items():
    st_test.apply_scenario(name, adjustments)

scores = {t: 0.8 for t in portfolio.tickers}
lm = LiquidityMetrics(portfolio, scores)
lm.apply_scenario("Liquidity Crunch", {"Equity": -0.2, "Bond": -0.05})
lm.apply_scenario("Tech Rally", {"Equity": 0.1, "Bond": 0.02})

likelihoods = {t: 0.1 + 0.1*np.random.rand() for t in portfolio.tickers}
rmat = RiskMatrix(portfolio, rm, likelihoods)

st.set_page_config(page_title="RiskLab Dashboard", layout="wide")
st.title("📊 RiskLab Interactive Dashboard")

tabs = st.tabs(["Portfolio", "Risk Metrics", "Stress Test", "Liquidity", "Risk Matrix"])

with tabs[0]:
    st.subheader("Portfolio Overview")
    st.dataframe(portfolio.data.style.format({"Weight": "{:.2%}"}))  # type: ignore

with tabs[1]:
    st.subheader("Portfolio Risk Metrics")

    metrics_numeric = rm.summary(formatted=False)
    metrics_display = rm.summary(formatted=True)

    metrics_df = pd.DataFrame([metrics_numeric], index=["Base"])
    metrics_display_df = pd.DataFrame([metrics_display], index=["Base"])

    st.dataframe(metrics_display_df)

with tabs[2]:
    st.subheader("Stress Test Scenarios")
    st.dataframe(st_test.summary())

    scenario_df = st_test.summary().copy()
    scenario_df.reset_index(inplace=True)
    scenario_df.rename(columns={scenario_df.columns[0]: "Scenario"}, inplace=True)

    scenario_df_plot = scenario_df.melt(id_vars="Scenario", var_name="Metric", value_name="Value")
    fig = px.line(scenario_df_plot, x="Scenario", y="Value", color="Metric", markers=True)
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.subheader("Liquidity Metrics")
    liq_df = lm.summary().copy()
    st.dataframe(liq_df)

    liq_df_reset = liq_df.reset_index()
    liq_df_reset.rename(columns={liq_df_reset.columns[0]: "Scenario"}, inplace=True)

    fig_liq = px.bar(
        liq_df_reset,
        x="Scenario",
        y="Portfolio Liquidity",
        text="Portfolio Liquidity"
    )
    st.plotly_chart(fig_liq, use_container_width=True)

with tabs[4]:
    st.subheader("Risk Matrix Heatmap")
    rm_df = rmat.compute_matrix().copy()

    rm_df.columns = rm_df.columns.str.strip()

    if "RiskScore" in rm_df.columns:
        rm_values = rm_df["RiskScore"].values.reshape(-1, 1) # type: ignore
        labels = rm_df.index.tolist()
        fig_heat = px.imshow(
            rm_values,
            labels=dict(x="Risk Score", y="Ticker", color="Risk Score"),
            x=["RiskScore"],
            y=labels,
            color_continuous_scale="RdYlGn_r",
            text_auto=".4f" # type: ignore
        )
    
    elif rm_df.shape[0] == rm_df.shape[1]:
        rm_values = rm_df.values
        labels = rm_df.index.tolist()  
        fig_heat = px.imshow(
            rm_values,
            labels=dict(x="Ticker", y="Ticker", color="Risk Score"),
            x=rm_df.columns,
            y=labels,
            color_continuous_scale="RdYlGn_r",
            text_auto=".4f" # type: ignore
        )
    
    else:
        st.error("Risk matrix has an unexpected format. Showing dummy zeros.")
        rm_df["RiskScore"] = np.zeros(len(rm_df))
        rm_values = rm_df["RiskScore"].values.reshape(-1, 1) # type: ignore
        labels = rm_df.index.tolist()
        fig_heat = px.imshow(
            rm_values,
            labels=dict(x="Risk Score", y="Ticker", color="Risk Score"),
            x=["RiskScore"],
            y=labels,
            color_continuous_scale="RdYlGn_r",
            text_auto=".4f" # type: ignore
        )

    st.plotly_chart(fig_heat, use_container_width=True)