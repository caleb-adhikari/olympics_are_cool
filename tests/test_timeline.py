# test_timeline.py
"""
Automated tests for olympics_data.timeline module.
Uses assert statements to validate outputs.
"""

import pandas as pd
from olympics_data import timeline  # replace with your actual package name


# Load a small sample of your dataset (for faster testing)
df = pd.read_csv("athlete_events.csv")

def test_participation_trends():
    """
    Test participation_trends function
    """
    result = timeline.participation_trends(df, by_gender=True, plot=False)
    
    # Checks
    assert not result.empty, "Participation trends returned empty DataFrame"
    assert 'M' in result.columns or 'F' in result.columns, "Gender columns missing"
    assert result.index.is_monotonic_increasing, "Years are not sorted properly"


def test_medal_trends():
    """
    Test medal_trends function
    """
    result = timeline.medal_trends(df, entity="Team", top_n=5, plot=False)
    
    # Checks
    assert not result.empty, "Medal trends returned empty DataFrame"
    assert result.index.is_monotonic_increasing, "Years are not sorted properly"
    assert result.shape[1] <= 5, "More than top_n columns returned"


def test_sport_popularity():
    """
    Test sport_popularity function
    """
    result = timeline.sport_popularity(df, plot=False)
    
    # Checks
    assert not result.empty, "Sport popularity returned empty DataFrame"
    assert result.index.is_monotonic_increasing, "Years are not sorted properly"
    assert result.shape[1] > 0, "No sports found in the data"


if __name__ == "__main__":
    # Run tests manually
    print("Running test_participation_trends...")
    test_participation_trends()
    print("Passed!")

    print("Running test_medal_trends...")
    test_medal_trends()
    print("Passed!")

    print("Running test_sport_popularity...")
    test_sport_popularity()
    print("Passed!")

    print("\nAll timeline tests passed successfully!")