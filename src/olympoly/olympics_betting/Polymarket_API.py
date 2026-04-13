import requests

slugs = [
    "2026-winter-olympics-most-gold-medals",
    "2026-winter-olympics-most-medals",
    "2026-winter-olympics-ice-hockey-gold-medal-winner",
]

for slug in slugs:
    r = requests.get(
        "https://gamma-api.polymarket.com/events",
        params={"slug": slug}
    )
    data = r.json()
    print(f"\nSlug: {slug}")
    print(f"  Found: {len(data)} event(s)")
    for e in data:
        print(f"  Event URL: https://polymarket.com/event/{e.get('slug', slug)}")
        for m in e.get("markets", []):
            market_slug = m.get('slug')
            if market_slug:
                print(f"  → Market URL: https://polymarket.com/market/{market_slug}")
            else:
                condition_id = m.get('conditionId')
                print(f"  → Market (conditionId): https://polymarket.com/market?conditionId={condition_id}")