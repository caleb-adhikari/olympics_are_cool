"""
performance.py - Analyze Olympic performance efficiency.

Functions:
- country_efficiency: Medals per athlete by country
- efficiency_trends: How efficiency changes over time
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from olympoly.load_data import load_data


def prepare_data():
    """
    Load and clean dataset for analysis.
    Prepares data for performance and timeline modules.
    """
    df = load_data()
    df_clean = df.copy()

    # Clean Medal column
    df_clean['Medal'] = df_clean['Medal'].replace('NA', pd.NA)

    # Clean numeric columns
    df_clean['Year'] = pd.to_numeric(df_clean['Year'], errors='coerce')
    df_clean['Age'] = pd.to_numeric(df_clean['Age'], errors='coerce')
    df_clean['Height'] = pd.to_numeric(df_clean['Height'], errors='coerce')
    df_clean['Weight'] = pd.to_numeric(df_clean['Weight'], errors='coerce')

    # Drop bad rows
    df_clean = df_clean.dropna(subset=['ID', 'Team', 'Year'])

    # Clean text columns
    df_clean['Team'] = df_clean['Team'].str.strip()
    df_clean['Sport'] = df_clean['Sport'].str.strip()

    return df_clean


def country_efficiency(df, min_athletes=50, plot=True):
    athletes = df.groupby('Team')['ID'].nunique()
    medals = df[df['Medal'].notnull()].groupby('Team')['Medal'].count()

    efficiency_df = pd.DataFrame({
        'Athletes': athletes,
        'Medals': medals
    }).fillna(0)

    efficiency_df = efficiency_df[efficiency_df['Athletes'] >= min_athletes]
    efficiency_df['Efficiency'] = np.where(
        efficiency_df['Athletes'] > 0,
        efficiency_df['Medals'] / efficiency_df['Athletes'],
        0
    )
    efficiency_df = efficiency_df.sort_values(by='Efficiency', ascending=False)

    if plot:
        top = efficiency_df.head(10)
        top['Efficiency'].plot(kind='bar', figsize=(10, 6))
        plt.title("Top 10 Most Efficient Countries (Medals per Athlete)")
        plt.ylabel("Medals per Athlete")
        plt.xlabel("Country")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    return efficiency_df


def efficiency_trends(df, country, plot=True):
    df_country = df[df['Team'] == country]

    athletes = df_country.groupby('Year')['ID'].nunique()
    medals = df_country[df_country['Medal'].notnull()].groupby('Year')['Medal'].count()

    trends = pd.DataFrame({
        'Athletes': athletes,
        'Medals': medals
    }).fillna(0)

    trends['Efficiency'] = np.where(
        trends['Athletes'] > 0,
        trends['Medals'] / trends['Athletes'],
        0
    )

    if plot:
        trends['Efficiency'].plot(figsize=(10, 5), marker='o')
        plt.title(f"{country} Olympic Efficiency Over Time")
        plt.xlabel("Year")
        plt.ylabel("Medals per Athlete")
        plt.grid(True)
        plt.show()

    return trends


# Test the module
if __name__ == "__main__":
    df = prepare_data()
    print(df.head())
    print(df[['Team', 'Medal']].head(10))

# Call country_efficiency to see the bar chart
    efficiency_df = country_efficiency(df, min_athletes=50, plot=True)
        # Optional: Call efficiency_trends for a specific country
    trends = efficiency_trends(df, country="China", plot=True)