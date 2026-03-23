# test_timeline.py
"""
Pytest tests for olympics_data.timeline module.
"""

import pandas as pd
import pytest
from olympics_data import timeline  # replace with your actual package name

# Load the dataset (for faster testing, you could use a small CSV sample)
df = pd.read_csv("athlete_events.csv")


def test_participation_trends():
    """
    Test participation_trends function
    """
    result = timeline.participation_trends(df, by_gender=True, plot=False)
    
    # Basic checks
    assert not result.empty, "Participation trends returned empty DataFrame"
    assert any(gender in result.columns for gender in ['M', 'F']), "Gender columns missing"
    assert result.index.is_monotonic_increasing, "Years are not sorted properly"


def test_medal_trends():
    """
    Test medal_trends function
    """
    result = timeline.medal_trends(df, entity="Team", top_n=5, plot=False)
    
    # Basic checks
    assert not result.empty, "Medal trends returned empty DataFrame"
    assert result.index.is_monotonic_increasing, "Years are not sorted properly"
    assert result.shape[1] <= 5, "More than top_n columns returned"


def test_sport_popularity():
    """
    Test sport_popularity function
    """
    result = timeline.sport_popularity(df, plot=False)
    
    # Basic checks
    assert not result.empty, "Sport popularity returned empty DataFrame"
    assert result.index.is_monotonic_increasing, "Years are not sorted properly"
    assert result.shape[1] > 0, "No sports found in the data"