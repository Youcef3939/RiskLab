"""
Example Plugin for RiskLab
Provides extra helper functions for portfolio analysis and returns.
"""

import pandas as pd


def hello_plugin():
    """Simple test function to verify plugin is loaded."""
    return "Plugin loaded successfully!"

def portfolio_summary_weights(portfolio):
    """
    Returns a dictionary of ticker: weight from the portfolio.
    
    Args:
        portfolio: Portfolio object from RiskLab.
        
    Returns:
        dict: {ticker: weight}
    """
    return dict(zip(portfolio.tickers, portfolio.data['Weight']))

def average_daily_return(returns):
    """
    Computes the mean daily return for each ticker.
    
    Args:
        returns: pd.DataFrame of daily returns for each ticker.
        
    Returns:
        pd.Series: mean daily returns
    """
    return returns.mean()

def top_n_risky_assets(rm, n=5):
    """
    Returns the top N riskiest assets based on volatility.
    
    Args:
        rm: RiskMetrics object from RiskLab.
        n: number of assets to return
        
    Returns:
        list: tickers sorted by volatility descending
    """
    vol_df = rm.volatility
    if isinstance(vol_df, dict):
        vol_series = pd.Series(vol_df)
    else:
        vol_series = vol_df
    return vol_series.sort_values(ascending=False).head(n).index.tolist()