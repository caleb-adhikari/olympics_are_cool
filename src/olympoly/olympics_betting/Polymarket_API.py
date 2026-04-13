import requests
import pandas as pd

def search_polymarket(topic):
    url = "https://gamma-api.polymarket.com/markets"
    
    params = {
        "search": topic,
        "limit": 50,
        "active": False
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    markets = []
    
    for market in data:
        markets.append({
            "question": market.get("question"),
            "outcomes": market.get("outcomes"),
            "prices": market.get("outcomePrices"),
            "volume": market.get("volume"),
            "liquidity": market.get("liquidity"),
            "active": market.get("active"),
            "tag": market.get("tags")
        })
    
    return pd.DataFrame(data)

df = search_polymarket("olympics")
print(df.head())

# Issue: seach function only returns market that are currently open. We need to be able to search for closed markets as well.