import pandas as pd

def medal_probability(df, group_cols, medal_type="Gold"):
    """
    Estimate probability of winning a specific medal given grouping columns.

    Args:
        df: pandas DataFrame
        group_cols: list (e.g., ['NOC', 'Event'])
        medal_type: 'Gold', 'Silver', 'Bronze'

    Returns:
        DataFrame with probabilities
    """
    df = df.copy()

    df['is_medal'] = (df['Medal'] == medal_type).astype(int)

    grouped = df.groupby(group_cols).agg(
        total_entries=('ID', 'count'),
        total_wins=('is_medal', 'sum')
    ).reset_index()

    grouped['probability'] = grouped['total_wins'] / grouped['total_entries']

    return grouped

def athlete_medal_probability(df):
    df = df.copy()
    df['is_medal'] = df['Medal'].notna().astype(int)

    grouped = df.groupby('Name').agg(
        appearances=('ID', 'count'),
        medals=('is_medal', 'sum')
    ).reset_index()

    grouped['probability'] = grouped['medals'] / grouped['appearances']

    return grouped

def weighted_medal_probability(df, group_cols, current_year, decay=0.9):
    df = df.copy()

    df['years_ago'] = current_year - df['Year']
    df['weight'] = decay ** df['years_ago']
    df['is_gold'] = (df['Medal'] == 'Gold').astype(int)

    grouped = df.groupby(group_cols).apply(
        lambda x: pd.Series({
            'weighted_wins': (x['is_gold'] * x['weight']).sum(),
            'weighted_total': x['weight'].sum()
        })
    ).reset_index()

    grouped['probability'] = grouped['weighted_wins'] / grouped['weighted_total']

    return grouped

