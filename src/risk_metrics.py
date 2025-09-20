# src/risk_metrics.py
import numpy as np
import pandas as pd
from typing import Optional
from portfolio import Portfolio

class RiskMetrics:
    """
    Compute risk metrics for a Portfolio.
    Supported metrics: Volatility, VaR, CVaR, Sharpe Ratio.
    Automatically computes all metrics on initialization to ensure numeric values are always available.
    """

    def __init__(self, portfolio: Portfolio, returns: Optional[pd.DataFrame] = None, risk_free_rate: float = 0.0):
        self.portfolio = portfolio
        self.returns = returns
        self.risk_free_rate = risk_free_rate
        self.metrics: dict = {} 
        self.formatted_metrics: dict = {}  

        if self.returns is not None:
            self._compute_all_metrics()

    def _compute_all_metrics(self):
        """Compute all metrics and store both numeric and formatted versions."""
        self.compute_volatility()
        self.compute_var()
        self.compute_cvar()
        self.compute_sharpe()

    def compute_volatility(self) -> float:
        weights = np.array(self.portfolio.weights)
        cov_matrix = self.returns.cov() # type: ignore
        vol = np.sqrt(weights.T @ cov_matrix.values @ weights)
        self.metrics['Volatility'] = float(vol)
        self.formatted_metrics['Volatility'] = f"{vol*100:.2f}%"
        return float(vol)

    def compute_var(self, confidence: float = 0.95) -> float:
        weighted_returns = (self.returns * self.portfolio.weights).sum(axis=1) # type: ignore
        var = -np.percentile(weighted_returns, (1 - confidence) * 100)
        key = f'VaR_{int(confidence*100)}'
        self.metrics[key] = float(var)
        self.formatted_metrics[key] = f"{var*100:.2f}%"
        return float(var)

    def compute_cvar(self, confidence: float = 0.95) -> float:
        weighted_returns = (self.returns * self.portfolio.weights).sum(axis=1) # type: ignore
        var_threshold = np.percentile(weighted_returns, (1 - confidence) * 100)
        cvar = -weighted_returns[weighted_returns <= var_threshold].mean()
        key = f'CVaR_{int(confidence*100)}'
        self.metrics[key] = float(cvar)
        self.formatted_metrics[key] = f"{cvar*100:.2f}%"
        return float(cvar)

    def compute_sharpe(self) -> float:
        weighted_returns = (self.returns * self.portfolio.weights).sum(axis=1) # type: ignore
        excess_returns = weighted_returns - self.risk_free_rate / 252
        sharpe_ratio = excess_returns.mean() / excess_returns.std()
        self.metrics['Sharpe'] = float(sharpe_ratio)
        self.formatted_metrics['Sharpe'] = round(float(sharpe_ratio), 4)
        return float(sharpe_ratio)

    def summary(self, formatted: bool = True) -> dict:
        """
        Return a dictionary of metrics.
        :param formatted: True for human-readable strings (e.g., '0.36%'), False for numeric values
        """
        return self.formatted_metrics if formatted else self.metrics


if __name__ == "__main__":
    portfolio = Portfolio.from_csv("../data/sample_portfolio.csv")
    np.random.seed(42)
    tickers = portfolio.tickers
    returns = pd.DataFrame(np.random.normal(0, 0.01, (252, len(tickers))), columns=tickers)

    rm = RiskMetrics(portfolio, returns)
    print("Numeric metrics:", rm.summary(formatted=False))
    print("Formatted metrics:", rm.summary(formatted=True))