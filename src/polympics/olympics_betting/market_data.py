# market_data.py

"""
market_data.py - Load and process prediction market data
for Olympics-related contracts (Kalshi / Polymarket style).
"""

import pandas as pd


REQUIRED_COLUMNS = {"market", "event", "outcome", "price", "timestamp"}


def load_market_data(filepath):
    """
    Load market data from CSV.

    Expected columns:
    - market (str): platform name (e.g., kalshi, polymarket)
    - event (str): event description
    - outcome (str): outcome label (e.g., YES/NO)
    - price (float): price between 0 and 1
    - timestamp (datetime or str)

    Returns:
    - pd.DataFrame
    """
    df = pd.read_csv(filepath)

    validate_market_data(df)

    # Ensure correct types
    df["price"] = df["price"].astype(float)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    return df


def validate_market_data(df):
    """
    Validate required columns and value ranges.
    """
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if not df["price"].between(0, 1).all():
        raise ValueError("All prices must be between 0 and 1")


def normalize_prices(df):
    """
    Normalize prices so YES/NO outcomes sum to 1 per event + timestamp.

    Returns:
    - normalized DataFrame
    """
    df = df.copy()

    grouped = df.groupby(["event", "timestamp"])["price"].transform("sum")
    df["normalized_price"] = df["price"] / grouped

    return df


def merge_market_data(df1, df2):
    """
    Merge two market datasets.

    Returns:
    - combined DataFrame
    """
    combined = pd.concat([df1, df2], ignore_index=True)
    validate_market_data(combined)
    return combined


def get_latest_prices(df):
    """
    Get latest price per event + outcome.

    Returns:
    - pd.DataFrame
    """
    idx = df.groupby(["event", "outcome"])["timestamp"].idxmax()
    return df.loc[idx].reset_index(drop=True)