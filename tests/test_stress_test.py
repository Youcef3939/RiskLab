import sys
import pytest
import pandas as pd
import numpy as np

sys.path.append("../src")

from portfolio import Portfolio
from stress_test import StressTest

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
def stress_test_obj(sample_portfolio, sample_returns=None):
    """Create StressTest object."""
    if sample_returns is None:
        np.random.seed(42)
        sample_returns = pd.DataFrame(
            np.random.normal(0, 0.01, (252, len(sample_portfolio.tickers))),
            columns=sample_portfolio.tickers
        )
    return StressTest(sample_portfolio, sample_returns)

def test_apply_scenario(stress_test_obj):
    """Test that applying a scenario updates internal results."""
    scenario_name = "Market Crash"
    adjustments = {t: -0.1 for t in stress_test_obj.portfolio.tickers}
    stress_test_obj.apply_scenario(scenario_name, adjustments)
    
    summary_df = stress_test_obj.summary()
    assert scenario_name in summary_df.index

def test_summary_dataframe(stress_test_obj):
    """Test that summary returns a DataFrame."""
    stress_test_obj.apply_scenario("Base", {t: 0.0 for t in stress_test_obj.portfolio.tickers})
    
    df = stress_test_obj.summary()
    assert isinstance(df, pd.DataFrame)
    for ticker in stress_test_obj.portfolio.tickers:
        assert ticker in df.columns

def test_multiple_scenarios(stress_test_obj):
    """Test applying multiple scenarios and summarizing."""
    scenarios = {
        "Base": {t: 0.0 for t in stress_test_obj.portfolio.tickers},
        "Crash": {t: -0.1 for t in stress_test_obj.portfolio.tickers},
    }
    for name, adj in scenarios.items():
        stress_test_obj.apply_scenario(name, adj)
    
    df = stress_test_obj.summary()
    assert set(df.index) == set(scenarios.keys())