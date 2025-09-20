# src/stress_test.py
import pandas as pd
import numpy as np
from typing import Dict, Optional
from portfolio import Portfolio
from risk_metrics import RiskMetrics

class StressTest:
    """
    Perform stress testing on a Portfolio.
    Apply hypothetical or historical shocks and recompute risk metrics.
    """

    def __init__(self, portfolio: Portfolio, returns: Optional[pd.DataFrame] = None):
        self.portfolio = portfolio
        self.returns = returns
        self.scenario_results: Dict[str, Dict] = {}

    def apply_scenario(self, name: str, shocks: Dict[str, float]) -> Dict[str, float]:
        """
        Apply a shock scenario to the portfolio and compute risk metrics.
        :param name: Scenario name
        :param shocks: Dict mapping Ticker or AssetType to shock percentage (e.g., -0.1 for -10%)
        :return: Dict of risk metrics under this scenario
        """
        if self.returns is not None:
            scenario_returns = self.returns.copy()
        else:
            scenario_returns = pd.DataFrame(
                np.zeros((252, len(self.portfolio.tickers))),
                columns=self.portfolio.tickers
            )

        for key, shock in shocks.items():
            if key in scenario_returns.columns:
                scenario_returns[key] = scenario_returns[key] * (1 + shock)
            else:
                indices = [i for i, t in enumerate(self.portfolio.asset_types) if t == key]
                for i in indices:
                    scenario_returns[self.portfolio.tickers[i]] = scenario_returns[self.portfolio.tickers[i]] * (1 + shock)

        rm = RiskMetrics(self.portfolio, scenario_returns)
        rm.compute_volatility()
        rm.compute_var()
        rm.compute_cvar()
        rm.compute_sharpe()
        self.scenario_results[name] = rm.summary()
        return self.scenario_results[name]

    def summary(self) -> pd.DataFrame:
        """
        Return all scenario results as a DataFrame
        """
        return pd.DataFrame(self.scenario_results).T  

if __name__ == "__main__":
    portfolio = Portfolio.from_csv("../data/sample_portfolio.csv")
    np.random.seed(42)
    tickers = portfolio.tickers

    returns = pd.DataFrame(np.random.normal(0, 0.01, (252, len(tickers))), columns=tickers)

    st = StressTest(portfolio, returns)

    st.apply_scenario("Base", {ticker: 0.0 for ticker in tickers})

    st.apply_scenario("Market Crash", {ticker: -0.10 for ticker in tickers})

    st.apply_scenario("Tech Dip", {"Equity": -0.15})

    st.apply_scenario("Bond Rally", {"Bond": 0.05})

    print(st.summary())