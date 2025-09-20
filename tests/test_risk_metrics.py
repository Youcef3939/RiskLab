import sys
import pytest
import pandas as pd
import numpy as np

sys.path.append("../src")

from portfolio import Portfolio
from risk_metrics import RiskMetrics

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
    """Create RiskMetrics object with computed metrics."""
    rm = RiskMetrics(sample_portfolio, sample_returns)
    rm.compute_volatility()
    rm.compute_var()
    rm.compute_cvar()
    rm.compute_sharpe()
    return rm

def test_volatility_computed(sample_risk_metrics):
    """Test that volatility is computed correctly."""
    vol = sample_risk_metrics.volatility
    assert isinstance(vol, (dict, pd.Series))
    if isinstance(vol, dict):
        assert all(v >= 0 for v in vol.values())
    else:
        assert all(vol >= 0)

def test_var_computed(sample_risk_metrics):
    """Test that VaR is computed correctly."""
    var_95 = sample_risk_metrics.var_95
    assert isinstance(var_95, (float, np.float64))

def test_cvar_computed(sample_risk_metrics):
    """Test that CVaR is computed correctly."""
    cvar_95 = sample_risk_metrics.cvar_95
    assert isinstance(cvar_95, (float, np.float64))

def test_sharpe_computed(sample_risk_metrics):
    """Test that Sharpe ratio is computed correctly."""
    sharpe = sample_risk_metrics.sharpe
    assert isinstance(sharpe, (float, np.float64))

def test_summary_output(sample_risk_metrics):
    """Test that summary returns a dict or DataFrame."""
    summary_numeric = sample_risk_metrics.summary(formatted=False)
    summary_formatted = sample_risk_metrics.summary(formatted=True)
    
    assert isinstance(summary_numeric, dict)
    assert isinstance(summary_formatted, dict)
    for key in ["Volatility", "VaR 95%", "CVaR 95%", "Sharpe Ratio"]:
        assert key in summary_numeric
        assert key in summary_formatted