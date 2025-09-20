# src/risk_matrix.py
import pandas as pd
from typing import Dict, Optional
from portfolio import Portfolio
from risk_metrics import RiskMetrics

class RiskMatrix:
    """
    Compute likelihood × impact matrix for a Portfolio.
    Impact is based on a chosen risk metric (e.g., VaR or CVaR).
    Likelihood is user-defined or defaulted.
    Produces a square matrix suitable for a heatmap.
    """

    def __init__(self, portfolio: Portfolio, risk_metrics: RiskMetrics,
                 likelihoods: Optional[Dict[str, float]] = None, impact_metric: str = "VaR_95"):
        """
        :param portfolio: Portfolio object
        :param risk_metrics: RiskMetrics object with metrics computed
        :param likelihoods: Optional dict of ticker -> likelihood (0-1)
        :param impact_metric: Risk metric to use as impact ('VaR_95' or 'CVaR_95')
        """
        self.portfolio = portfolio
        self.risk_metrics = risk_metrics
        self.impact_metric = impact_metric

        # Default likelihoods 0.1
        self.likelihoods = {t: 0.1 for t in self.portfolio.tickers}
        if likelihoods:
            for t, v in likelihoods.items():
                if t in self.likelihoods:
                    self.likelihoods[t] = max(0.0, min(1.0, v))

    def compute_matrix(self) -> pd.DataFrame:
        """
        Compute a square n x n risk matrix where each element is:
        (likelihood_ticker1 + likelihood_ticker2)/2 * impact
        """
        tickers = self.portfolio.tickers

        # Get impact from RiskMetrics summary
        impact_val = self.risk_metrics.summary().get(self.impact_metric, 0)
        if isinstance(impact_val, str) and "%" in impact_val:
            impact_val = float(impact_val.strip('%')) / 100
        impact = float(impact_val)

        # Initialize square DataFrame
        matrix = pd.DataFrame(index=tickers, columns=tickers, dtype=float)

        for t1 in tickers:
            for t2 in tickers:
                likelihood1 = self.likelihoods.get(t1, 0.1)
                likelihood2 = self.likelihoods.get(t2, 0.1)
                # Example risk score between two tickers
                matrix.loc[t1, t2] = round(((likelihood1 + likelihood2) / 2) * impact, 6)

        return matrix

if __name__ == "__main__":
    from portfolio import Portfolio
    from risk_metrics import RiskMetrics
    import numpy as np
    import pandas as pd

    portfolio = Portfolio.from_csv("../data/sample_portfolio.csv")

    np.random.seed(42)
    returns = pd.DataFrame(
        np.random.normal(0, 0.01, (252, len(portfolio.tickers))),
        columns=portfolio.tickers
    )

    rm = RiskMetrics(portfolio, returns)
    rm.compute_volatility()
    rm.compute_var()
    rm.compute_cvar()
    rm.compute_sharpe()

    likelihoods = {
        "AAPL": 0.2, "MSFT": 0.15, "TSLA": 0.25, "AMZN": 0.2,
        "GOOG": 0.1, "NVDA": 0.2, "JPM": 0.05, "XOM": 0.05
    }

    risk_matrix = RiskMatrix(portfolio, rm, likelihoods, impact_metric="VaR_95")
    matrix_df = risk_matrix.compute_matrix()
    print(matrix_df)