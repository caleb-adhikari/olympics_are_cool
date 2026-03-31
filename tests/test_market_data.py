# test_market_data.py
"""
Simple pytest tests for olympics_markets.market_data module.
Matches style of test_timeline.py
"""

import pandas as pd
# i added the proper path? what are we importing tho? seems like market data is not a function within the python file
from olympoly.olympics_betting.market_data import market_data


# Create sample dataset
df = pd.DataFrame({
    "market": ["kalshi", "kalshi", "kalshi", "kalshi"],
    "event": ["USA_gold", "USA_gold", "USA_gold", "USA_gold"],
    "outcome": ["YES", "NO", "YES", "NO"],
    "price": [0.6, 0.4, 0.65, 0.35],
    "timestamp": [
        "2024-07-01",
        "2024-07-01",
        "2024-07-02",
        "2024-07-02",
    ]
})


def test_validate_market_data():
    """Test validation passes on correct data"""
    market_data.validate_market_data(df)


def test_validate_market_data_invalid_price():
    """Test validation fails for invalid price"""
    bad_df = df.copy()
    bad_df.loc[0, "price"] = 1.5

    try:
        market_data.validate_market_data(bad_df)
        assert False, "Expected ValueError for invalid price"
    except ValueError:
        assert True


def test_validate_market_data_missing_column():
    """Test validation fails when column missing"""
    bad_df = df.drop(columns=["price"])

    try:
        market_data.validate_market_data(bad_df)
        assert False, "Expected ValueError for missing column"
    except ValueError:
        assert True


def test_normalize_prices():
    """Test normalization sums to 1"""
    result = market_data.normalize_prices(df)

    grouped = result.groupby(["event", "timestamp"])["normalized_price"].sum()

    for val in grouped:
        assert abs(val - 1.0) < 1e-6


def test_merge_market_data():
    """Test merging doubles dataset size"""
    merged = market_data.merge_market_data(df, df)

    assert len(merged) == len(df) * 2


def test_get_latest_prices():
    """Test latest price extraction"""
    df_copy = df.copy()
    df_copy["timestamp"] = pd.to_datetime(df_copy["timestamp"])

    latest = market_data.get_latest_prices(df_copy)

    assert len(latest) == 2  # YES and NO
    assert set(latest["outcome"]) == {"YES", "NO"}


def test_get_latest_prices_correct_date():
    """Ensure latest timestamp is selected"""
    df_copy = df.copy()
    df_copy["timestamp"] = pd.to_datetime(df_copy["timestamp"])

    latest = market_data.get_latest_prices(df_copy)

    assert all(latest["timestamp"] == pd.Timestamp("2024-07-02"))