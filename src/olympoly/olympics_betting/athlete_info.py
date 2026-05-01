# script to standardize string input with pandas function
# return athlete data

from olympoly.load_data import load_olympic_data
import re

# Function to extract words from string
def normalize(text):
    return re.findall(r'\b\w+\b', str(text).lower())

# Matching Function
def match_name(name, query, min_matches=2):
    name_words = set(normalize(name))
    query_words = set(normalize(query))
    
    return len(name_words & query_words) >= min_matches

# function to get athelete info based on input name
def get_athlete_info(athlete_name: str):
    """Look up and display Olympic history for an athlete by name.

    Parameters:
        athlete_name: Full or partial name of the athlete to search for.
    """
    df = load_olympic_data()
    df["Name"] = df["Name"].str.split(",").str[0] # Drop last name
    df_filtered = df[df["Name"].apply(lambda x: match_name(x, athlete_name))]
    print(df_filtered)
    return None

# print(get_athlete_info("Michael Jordan"))
