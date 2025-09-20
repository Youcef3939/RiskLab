# src/portfolio.py
import pandas as pd
from typing import List, Optional

class Portfolio:
    """
    Portfolio class for loading, normalizing, and summarizing financial portfolios.
    Works with CSVs using 'Ticker' and 'Allocation' as weight.
    """

    def __init__(self, data: Optional[pd.DataFrame] = None):
        """
        Initialize a Portfolio object.
        :param data: Optional DataFrame containing portfolio data
        """
        self.data = data
        self.tickers: List[str] = []
        self.weights: List[float] = []
        self.asset_types: List[str] = []

    @classmethod
    def from_csv(cls, path: str) -> "Portfolio":
        """
        Load portfolio from a CSV file.
        CSV should have columns: Ticker, Allocation (used as Weight), AssetType (optional)
        """
        df = pd.read_csv(path)

        df.columns = [col.strip() for col in df.columns]

        if "Allocation" in df.columns:
            df = df.rename(columns={"Allocation": "Weight"})

        portfolio = cls(df)
        portfolio._normalize()
        return portfolio

    def _normalize(self):
        """
        Normalize portfolio data: 
        - Strip whitespace
        - Fill missing asset types as 'Unknown'
        - Ensure weights sum to 1
        """
        if self.data is None:
            raise ValueError("Portfolio data is not loaded.")

        if "AssetType" not in self.data.columns:
            self.data["AssetType"] = "Unknown"
        else:
            self.data["AssetType"] = self.data["AssetType"].fillna("Unknown")

        if "Weight" not in self.data.columns:
            raise ValueError("Portfolio CSV must have a 'Weight' or 'Allocation' column.")

        total_weight = self.data["Weight"].sum()
        if total_weight == 0:
            raise ValueError("Total weight of portfolio is zero.")
        self.data["Weight"] = self.data["Weight"] / total_weight

        self.tickers = self.data["Ticker"].tolist()
        self.weights = self.data["Weight"].tolist()
        self.asset_types = self.data["AssetType"].tolist()

    def summary(self) -> pd.DataFrame:
        """
        Return a summary of the portfolio: tickers, weights, asset types.
        """
        if self.data is None:
            raise ValueError("Portfolio data is not loaded.")
        return self.data.copy()

    def __repr__(self):
        return f"<Portfolio: {len(self.tickers)} assets, Total Weight: {sum(self.weights):.2f}>"

if __name__ == "__main__":
    portfolio = Portfolio.from_csv("../data/sample_portfolio.csv")
    print(portfolio)
    print(portfolio.summary())