import sys
import pytest
import pandas as pd

sys.path.append("../src")

from portfolio import Portfolio

@pytest.fixture
def sample_csv(tmp_path):
    """Creates a temporary CSV file for testing."""
    data = pd.DataFrame({
        "Ticker": ["AAPL", "GOOGL", "TSLA"],
        "Weight": [0.4, 0.35, 0.25]
    })
    file_path = tmp_path / "sample_portfolio.csv"
    data.to_csv(file_path, index=False)
    return file_path

@pytest.fixture
def portfolio(sample_csv):
    """Returns a Portfolio object loaded from CSV."""
    return Portfolio.from_csv(sample_csv)

def test_portfolio_load(portfolio):
    """Test that the portfolio loads correctly."""
    assert isinstance(portfolio, Portfolio)
    assert portfolio.tickers == ["AAPL", "GOOGL", "TSLA"]
    assert list(portfolio.data["Weight"]) == [0.4, 0.35, 0.25] # type: ignore

def test_portfolio_sum_weights(portfolio):
    """Test that weights sum to 1.0."""
    total_weight = portfolio.data["Weight"].sum()
    assert abs(total_weight - 1.0) < 1e-6