import pandas as pd
import numpy as np
import pytest

from package_name.performance import prepare_data, country_efficiency, efficiency_trends


# -------------------------
# Fixtures
# -------------------------
@pytest.fixture
def sample_data(monkeypatch):
    """Mock dataset to avoid relying on real data."""
    
    def mock_load_data():
        return pd.DataFrame({
            'ID': [1, 2, 3, 4, 5, 6],
            'Team': ['USA', 'USA', 'China', 'China', 'China', 'USA'],
            'Year': [2000, 2000, 2000, 2004, 2004, 2004],
            'Medal': ['Gold', None, 'Silver', 'Gold', None, 'Bronze'],
            'Age': ['23', '25', '24', '26', '27', '28'],
            'Height': ['180', '175', '170', '165', '160', '185'],
            'Weight': ['75', '70', '65', '60', '55', '80'],
            'Sport': ['Swimming', 'Swimming', 'Gymnastics', 'Gymnastics', 'Gymnastics', 'Athletics']
        })

    monkeypatch.setattr("package_name.performance.load_data", mock_load_data)
    return mock_load_data()


# -------------------------
# Tests for prepare_data
# -------------------------
def test_prepare_data_types(sample_data, monkeypatch):
    df = prepare_data()

    assert pd.api.types.is_numeric_dtype(df['Year'])
    assert pd.api.types.is_numeric_dtype(df['Age'])
    assert pd.api.types.is_numeric_dtype(df['Height'])
    assert pd.api.types.is_numeric_dtype(df['Weight'])


def test_prepare_data_no_missing_keys(sample_data):
    df = prepare_data()

    assert df['ID'].isnull().sum() == 0
    assert df['Team'].isnull().sum() == 0
    assert df['Year'].isnull().sum() == 0


# -------------------------
# Tests for country_efficiency
# -------------------------
def test_country_efficiency_basic(sample_data):
    df = prepare_data()

    result = country_efficiency(df, min_athletes=1, plot=False)

    assert 'Efficiency' in result.columns
    assert (result['Efficiency'] >= 0).all()


def test_country_efficiency_calculation(sample_data):
    df = prepare_data()

    result = country_efficiency(df, min_athletes=1, plot=False)

    usa_eff = result.loc['USA', 'Efficiency']
    china_eff = result.loc['China', 'Efficiency']

    # Manual calculation:
    # USA: 3 athletes, 2 medals → 2/3
    # China: 3 athletes, 2 medals → 2/3
    assert np.isclose(usa_eff, 2/3)
    assert np.isclose(china_eff, 2/3)


def test_country_efficiency_min_athletes_filter(sample_data):
    df = prepare_data()

    result = country_efficiency(df, min_athletes=10, plot=False)

    assert result.empty


# -------------------------
# Tests for efficiency_trends
# -------------------------
def test_efficiency_trends_structure(sample_data):
    df = prepare_data()

    trends = efficiency_trends(df, country="USA", plot=False)

    assert 'Efficiency' in trends.columns
    assert 'Athletes' in trends.columns
    assert 'Medals' in trends.columns


def test_efficiency_trends_values(sample_data):
    df = prepare_data()

    trends = efficiency_trends(df, country="USA", plot=False)

    # Year 2000: 2 athletes, 1 medal → 0.5
    assert np.isclose(trends.loc[2000, 'Efficiency'], 0.5)


def test_efficiency_trends_no_country(sample_data):
    df = prepare_data()

    trends = efficiency_trends(df, country="Nonexistent", plot=False)

    assert trends.empty or (trends['Efficiency'] == 0).all()