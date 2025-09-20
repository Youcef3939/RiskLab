# src/report.py
import os
import pandas as pd
from typing import Optional
from portfolio import Portfolio
from risk_metrics import RiskMetrics
from stress_test import StressTest
from liquidity import LiquidityMetrics
from risk_matrix import RiskMatrix

class Report:
    """
    Generate combined reports for RiskLab.
    Supports CSV and Excel export into a dedicated 'reports/' folder.
    """

    def __init__(
        self,
        portfolio: Portfolio,
        risk_metrics: RiskMetrics,
        stress_test: Optional[StressTest] = None,
        liquidity_metrics: Optional[LiquidityMetrics] = None,
        risk_matrix: Optional[RiskMatrix] = None,
        output_dir: str = "../reports"
    ):
        self.portfolio = portfolio
        self.risk_metrics = risk_metrics
        self.stress_test = stress_test
        self.liquidity_metrics = liquidity_metrics
        self.risk_matrix = risk_matrix

        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_summary_tables(self) -> dict:
        """
        Returns a dictionary of all summary tables as DataFrames.
        Empty tables are replaced with a notice.
        """
        tables = {}

        tables["Portfolio"] = self.portfolio.data.copy() if not self.portfolio.data.empty else pd.DataFrame({"Notice": ["No portfolio data"]}) # type: ignore

        rm_summary = self.risk_metrics.summary()
        tables["RiskMetrics"] = pd.DataFrame(rm_summary, index=[0]) if rm_summary else pd.DataFrame({"Notice": ["No risk metrics computed"]})

        if self.stress_test:
            st_summary = self.stress_test.summary()
            tables["StressTest"] = st_summary if not st_summary.empty else pd.DataFrame({"Notice": ["No stress test results"]})
        else:
            tables["StressTest"] = pd.DataFrame({"Notice": ["No stress test module provided"]})

        if self.liquidity_metrics:
            lm_summary = self.liquidity_metrics.summary() if self.liquidity_metrics.scenario_results else pd.DataFrame({
                "Portfolio Liquidity": [self.liquidity_metrics.portfolio_liquidity()]
            }, index=["Base"])
            tables["Liquidity"] = lm_summary
        else:
            tables["Liquidity"] = pd.DataFrame({"Notice": ["No liquidity module provided"]})

        if self.risk_matrix:
            rm_df = self.risk_matrix.compute_matrix()
            tables["RiskMatrix"] = rm_df if not rm_df.empty else pd.DataFrame({"Notice": ["No risk matrix computed"]})
        else:
            tables["RiskMatrix"] = pd.DataFrame({"Notice": ["No risk matrix module provided"]})

        return tables

    def generate_csv(self, filename: str):
        """
        Export all summary tables to CSV or Excel in reports folder.
        """
        tables = self.generate_summary_tables()
        filepath = os.path.join(self.output_dir, filename)

        sheets_written = []
        if filepath.endswith(".csv"):
            for name, df in tables.items():
                out_file = filepath.replace(".csv", f"_{name}.csv")
                df.to_csv(out_file, index=True)
                sheets_written.append(name)
        elif filepath.endswith(".xlsx"):
            try:
                with pd.ExcelWriter(filepath) as writer:
                    for name, df in tables.items():
                        df.to_excel(writer, sheet_name=name, index=True)
                        sheets_written.append(name)
            except ModuleNotFoundError:
                print("openpyxl not installed. Falling back to CSV export.")
                for name, df in tables.items():
                    out_file = filepath.replace(".xlsx", f"_{name}.csv")
                    df.to_csv(out_file, index=True)
                    sheets_written.append(name)

        print(f"Report exported to {filepath}")
        print("Sheets included:", ", ".join(sheets_written))

if __name__ == "__main__":
    import numpy as np

    portfolio = Portfolio.from_csv("../data/sample_portfolio.csv")

    returns = pd.DataFrame(np.random.normal(0, 0.01, (252, len(portfolio.tickers))), columns=portfolio.tickers)

    rm = RiskMetrics(portfolio, returns)
    rm.compute_volatility(); rm.compute_var(); rm.compute_cvar(); rm.compute_sharpe()

    st = StressTest(portfolio, returns)
    st.apply_scenario("Base", {t:0.0 for t in portfolio.tickers})
    st.apply_scenario("Market Crash", {t:-0.1 for t in portfolio.tickers})

    scores = {t: 0.8 for t in portfolio.tickers}
    lm = LiquidityMetrics(portfolio, scores)
    lm.apply_scenario("Liquidity Crunch", {"Equity": -0.2, "Bond": -0.05})

    likelihoods = {t: 0.1 + 0.1*np.random.rand() for t in portfolio.tickers}
    rmat = RiskMatrix(portfolio, rm, likelihoods)

    report = Report(portfolio, rm, st, lm, rmat)
    report.generate_csv("RiskLab_Report.xlsx")