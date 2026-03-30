# timeline.py
"""
timeline.py - Analyze Olympics trends over time.

Functions:
- participation_trends: Athlete participation over the years, overall or by gender.
- medal_trends: Medal counts by country or sport over time.
- sport_popularity: How many athletes per sport over the years.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")


def participation_trends(df, by_gender=True, plot=True):
    """
    Analyze athlete participation over time.

    Parameters:
    - df: pandas.DataFrame with columns ['Year', 'Gender', 'ID', ...]
    - by_gender: bool, whether to split participation by gender
    - plot: bool, whether to generate a line plot

    Returns:
    - trends: pandas.DataFrame with counts of unique athletes per year (and gender if by_gender)
    """
    if by_gender:
        trends = df.groupby(['Year', 'Gender'])['ID'].nunique().reset_index()
        trends = trends.pivot(index='Year', columns='Gender', values='ID').fillna(0)
    else:
        trends = df.groupby('Year')['ID'].nunique().reset_index()
        trends.rename(columns={'ID': 'Count'}, inplace=True)

    if plot:
        trends.plot(figsize=(12, 6), marker='o')
        plt.title("Olympic Athlete Participation Over Time")
        plt.xlabel("Year")
        plt.ylabel("Number of Athletes")
        plt.show()

    return trends


def medal_trends(df, entity="Team", top_n=5, plot=True):
    """
    Analyze medal trends over time by country (Team) or sport.

    Parameters:
    - df: pandas.DataFrame with columns ['Year', 'Team', 'Sport', 'Medal']
    - entity: str, 'Team' or 'Sport' to group by
    - top_n: int, number of top entities to plot
    - plot: bool, whether to generate a line plot

    Returns:
    - trends: pandas.DataFrame with counts of medals per year per entity
    """
    medal_df = df[df['Medal'].notnull()]
    medal_counts = medal_df.groupby([entity, 'Year'])['Medal'].count().reset_index()
    
    top_entities = medal_counts.groupby(entity)['Medal'].sum().nlargest(top_n).index
    trends = medal_counts[medal_counts[entity].isin(top_entities)]
    trends = trends.pivot(index='Year', columns=entity, values='Medal').fillna(0)

    if plot:
        trends.plot(figsize=(12, 6), marker='o')
        plt.title(f"Top {top_n} {entity}s Medal Trends Over Time")
        plt.xlabel("Year")
        plt.ylabel("Number of Medals")
        plt.show()

    return trends


def sport_popularity(df, plot=True):
    """
    Analyze popularity of sports over time (number of athletes per sport).

    Parameters:
    - df: pandas.DataFrame with columns ['Year', 'Sport', 'ID']
    - plot: bool, whether to generate a line plot

    Returns:
    - trends: pandas.DataFrame with athlete counts per sport per year
    """
    trends = df.groupby(['Year', 'Sport'])['ID'].nunique().reset_index()
    trends = trends.pivot(index='Year', columns='Sport', values='ID').fillna(0)

    if plot:
        # Only plot top 5 sports by total athletes
        top_sports = trends.sum().nlargest(5).index
        trends[top_sports].plot(figsize=(12, 6), marker='o')
        plt.title("Top 5 Sports Popularity Over Time")
        plt.xlabel("Year")
        plt.ylabel("Number of Athletes")
        plt.show()

    return trends