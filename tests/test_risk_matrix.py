import sys
import pytest
import pandas as pd
import numpy as np

sys.path.append("../src")

from portfolio import Portfolio
from risk_metrics import RiskMetrics
from risk_matrix import RiskMatrix

@pytest.fixture
def sample_portfolio(tmp_path):
    """Create a sample Portfolio object."""
    data = pd.DataFrame({
        "Ticker": ["AAPL", "GOOGL", "TSLA"],
        "Weight": [0.4, 0.35, 0.25]
    })
    file_path = tmp_path / "sample_portfolio.csv"
    data.to_csv(file_path, index=False)
    return Portfolio.from_csv(file_path)

@pytest.fixture
def sample_returns(sample_portfolio):
    """Generate dummy returns for the portfolio."""
    np.random.seed(42)
    return pd.DataFrame(np.random.normal(0, 0.01, (252, len(sample_portfolio.tickers))),
                        columns=sample_portfolio.tickers)

@pytest.fixture
def sample_risk_metrics(sample_portfolio, sample_returns):
    """Compute risk metrics for the sample portfolio."""
    rm = RiskMetrics(sample_portfolio, sample_returns)
    rm.compute_volatility()
    rm.compute_var()
    rm.compute_cvar()
    rm.compute_sharpe()
    return rm

def test_risk_matrix_compute_matrix(sample_portfolio, sample_risk_metrics):
    """Test that RiskMatrix computes a DataFrame correctly."""
    likelihoods = {t: 0.1 + 0.1*np.random.rand() for t in sample_portfolio.tickers}
    rmat = RiskMatrix(sample_portfolio, sample_risk_metrics, likelihoods)
    
    df = rmat.compute_matrix()
    
    assert isinstance(df, pd.DataFrame), "Output should be a DataFrame"
    assert all(t in df.index for t in sample_portfolio.tickers)
    if "RiskScore" in df.columns:
        assert df["RiskScore"].dtype in [float, np.float64]
    else:
        assert df.shape[0] == df.shape[1]

def test_risk_matrix_values_positive(sample_portfolio, sample_risk_metrics):
    """Test that computed risk values are non-negative."""
    likelihoods = {t: 0.1 for t in sample_portfolio.tickers}
    rmat = RiskMatrix(sample_portfolio, sample_risk_metrics, likelihoods)
    df = rmat.compute_matrix()
    
    values = df.values.flatten()
    assert all(v >= 0 for v in values), "All risk values should be non-negative"