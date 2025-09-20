# src/liquidity.py
import pandas as pd
from typing import Dict, Optional
from portfolio import Portfolio

class LiquidityMetrics:
    """
    Measure portfolio liquidity and simulate liquidity shocks.
    Liquidity scores range from 0 (illiquid) to 1 (highly liquid).
    """

    def __init__(self, portfolio: Portfolio, liquidity_scores: Optional[Dict[str, float]] = None):
        """
        :param portfolio: Portfolio object
        :param liquidity_scores: Optional dict of ticker -> liquidity score
        """
        self.portfolio = portfolio
        self.scores = {t: 0.5 for t in self.portfolio.tickers}
        if liquidity_scores:
            for t, v in liquidity_scores.items():
                if t in self.scores:
                    self.scores[t] = max(0.0, min(1.0, v))  
        self.scenario_results: Dict[str, float] = {}

    def set_liquidity_scores(self, scores: Dict[str, float]):
        """
        Update liquidity scores
        """
        for t, v in scores.items():
            if t in self.scores:
                self.scores[t] = max(0.0, min(1.0, v))

    def portfolio_liquidity(self) -> float:
        """
        Compute weighted average liquidity of the portfolio
        """
        total_liq = sum(self.portfolio.weights[i] * self.scores[t] 
                        for i, t in enumerate(self.portfolio.tickers))
        return round(total_liq, 4)

    def apply_scenario(self, name: str, shocks: Dict[str, float]) -> float:
        """
        Apply liquidity shock scenario and compute new portfolio liquidity.
        :param name: Scenario name
        :param shocks: Dict mapping ticker or AssetType to shock percentage (negative for drop)
        :return: portfolio liquidity under scenario
        """
        scenario_scores = self.scores.copy()

        for key, shock in shocks.items():
            if key in scenario_scores:
                scenario_scores[key] = max(0.0, min(1.0, scenario_scores[key] * (1 + shock)))
            else:
                indices = [i for i, t in enumerate(self.portfolio.asset_types) if t == key]
                for i in indices:
                    ticker = self.portfolio.tickers[i]
                    scenario_scores[ticker] = max(0.0, min(1.0, scenario_scores[ticker] * (1 + shock)))

        total_liq = sum(self.portfolio.weights[i] * scenario_scores[t] 
                        for i, t in enumerate(self.portfolio.tickers))
        self.scenario_results[name] = round(total_liq, 4)
        return self.scenario_results[name]

    def summary(self) -> pd.DataFrame:
        """
        Return all scenario results as a DataFrame
        """
        return pd.DataFrame.from_dict(self.scenario_results, orient='index', columns=['Portfolio Liquidity'])

if __name__ == "__main__":
    portfolio = Portfolio.from_csv("../data/sample_portfolio.csv")

    scores = {
        "AAPL": 0.9, "MSFT": 0.85, "TSLA": 0.7, "AMZN": 0.75,
        "GOOG": 0.8, "NVDA": 0.65, "JPM": 0.95, "XOM": 0.9
    }
    lm = LiquidityMetrics(portfolio, scores)

    print("Base Portfolio Liquidity:", lm.portfolio_liquidity())

    lm.apply_scenario("Liquidity Crunch", {"Equity": -0.2, "Bond": -0.05})
    lm.apply_scenario("Tech Rally", {"TSLA": +0.1, "NVDA": +0.05})

    print(lm.summary())