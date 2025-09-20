# src/utils.py
import pandas as pd
import numpy as np

def format_percent(x, decimals=2):
    """
    Convert a float to a percentage string with specified decimals.
    Example: 0.00524 -> "0.52%"
    """
    return f"{x*100:.{decimals}f}%"

def normalize_weights(weights: pd.Series) -> pd.Series:
    """
    Normalize a Series of weights so they sum to 1.
    """
    total = weights.sum()
    if total == 0:
        raise ValueError("Sum of weights cannot be zero")
    return weights / total

def fill_unknowns(df: pd.DataFrame, column: str, default="Unknown") -> pd.DataFrame:
    """
    Fill missing values in a DataFrame column with a default value.
    """
    df[column] = df[column].fillna(default)
    return df

def weighted_sum(values: pd.Series, weights: pd.Series) -> float:
    """
    Compute the weighted sum of a series.
    """
    return np.sum(values * weights)