"""
simulation.py - Betting simulation engine for Olympics prediction markets

Simulates a trading strategy using:
- Market probabilities (prices)
- Model probabilities (historical_model or ML outputs)

NOTE:
Since we don't yet have true outcomes, we simulate outcomes using model probability.
"""

import numpy as np
import pandas as pd


def simulate_market_strategy(
    df,
    model_col="model_prob",
    market_col="price",
    edge_threshold=0.05,
    bet_size=1.0,
    bankroll=100.0,
    seed=42
):
    """
    Simulate betting strategy on prediction markets.

    Parameters:
    - df: DataFrame containing at least:
        ['event', market_col, model_col]
    - model_col: column with model probabilities
    - market_col: column with market probabilities
    - edge_threshold: minimum edge required to place a bet
    - bet_size: fraction of bankroll per bet
    - bankroll: starting capital
    - seed: randomness seed

    Returns:
    - results DataFrame
    - summary dict
    """

    np.random.seed(seed)

    df = df.copy()

    required = {"event", model_col, market_col}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required}")

    results = []
    current_bankroll = bankroll

    for _, row in df.iterrows():

        market_prob = row[market_col]
        model_prob = row[model_col]

        edge = model_prob - market_prob

        # Decide whether to bet
        if abs(edge) < edge_threshold:
            continue

        direction = "YES" if edge > 0 else "NO"

        bet_amount = current_bankroll * bet_size

        # Simulated true outcome (unknown reality)
        true_outcome = np.random.rand() < model_prob

        # Determine win
        if direction == "YES":
            win = true_outcome
        else:
            win = not true_outcome

        # Payout assumption (binary contract: win = +1, lose = -1)
        pnl = bet_amount * (1 if win else -1)

        current_bankroll += pnl

        results.append({
            "event": row["event"],
            "market_prob": market_prob,
            "model_prob": model_prob,
            "edge": edge,
            "direction": direction,
            "bet_amount": bet_amount,
            "win": win,
            "pnl": pnl,
            "bankroll": current_bankroll
        })

    results_df = pd.DataFrame(results)

    summary = {
        "final_bankroll": current_bankroll,
        "total_return": current_bankroll - bankroll,
        "roi": (current_bankroll - bankroll) / bankroll if bankroll > 0 else 0,
        "num_bets": len(results_df),
        "win_rate": results_df["win"].mean() if not results_df.empty else 0
    }

    return results_df, summary


def simulate_edge_strategy(df, threshold=0.1):
    """
    Simplified version: only counts correct edge direction (no bankroll compounding).

    Useful for debugging model quality.
    """

    df = df.copy()

    correct = 0
    total = 0

    for _, row in df.iterrows():

        edge = row["model_prob"] - row["price"]

        if abs(edge) < threshold:
            continue

        true_outcome = np.random.rand() < row["model_prob"]

        predicted = edge > 0
        actual = true_outcome

        if predicted == actual:
            correct += 1

        total += 1

    accuracy = correct / total if total > 0 else 0

    return {
        "accuracy": accuracy,
        "total_bets": total
    }

def kelly_bet_size(
    model_prob: float,
    market_prob: float,
    bankroll: float,
    fraction: float = 1.0,
    max_bet_fraction: float = 0.25,
) -> dict:
    """
    Calculate the optimal bet size using the Kelly Criterion.

    The Kelly Criterion maximizes long-run bankroll growth by sizing bets
    proportionally to edge and inversely to odds. A fractional Kelly
    (fraction < 1.0) is used in practice to reduce variance.

    Parameters
    ----------
    model_prob : float
        Your model's estimated probability of the YES outcome (0 < p < 1).
    market_prob : float
        The market's implied probability, i.e. the price (0 < p < 1).
    bankroll : float
        Current available capital.
    fraction : float
        Fractional Kelly multiplier (default 1.0 = full Kelly).
        Use 0.5 for half-Kelly, which is common in practice.
    max_bet_fraction : float
        Hard cap on bet size as a fraction of bankroll (default 0.25).
        Prevents Kelly from suggesting recklessly large bets on high-edge plays.

    Returns
    -------
    dict with keys:
        - kelly_fraction  : raw Kelly fraction of bankroll to bet
        - adjusted_fraction : after applying `fraction` multiplier and cap
        - bet_amount      : dollar amount to bet given bankroll
        - edge            : model_prob - market_prob
        - recommended     : True if a positive edge exists, False otherwise

    Examples
    --------
    >>> kelly_bet_size(model_prob=0.6, market_prob=0.45, bankroll=100.0)
    {'kelly_fraction': 0.2727..., 'adjusted_fraction': 0.25, 'bet_amount': 25.0, ...}

    Notes
    -----
    Formula: f* = (p * b - q) / b
    where b = (1 / market_prob) - 1  (decimal odds - 1)
          p = model_prob
          q = 1 - model_prob
    """
    if not (0 < model_prob < 1):
        raise ValueError(f"model_prob must be between 0 and 1, got {model_prob}")
    if not (0 < market_prob < 1):
        raise ValueError(f"market_prob must be between 0 and 1, got {market_prob}")

    edge = model_prob - market_prob

    # Decimal odds implied by market price (e.g. 0.45 price → odds of ~1.22)
    decimal_odds = (1.0 / market_prob) - 1.0
    q = 1.0 - model_prob

    # Kelly formula
    kelly_fraction = (model_prob * decimal_odds - q) / decimal_odds

    # Apply fractional Kelly and hard cap
    adjusted_fraction = min(kelly_fraction * fraction, max_bet_fraction)
    adjusted_fraction = max(adjusted_fraction, 0.0)  # no negative bets

    bet_amount = round(bankroll * adjusted_fraction, 2)

    return {
        "kelly_fraction": round(kelly_fraction, 6),
        "adjusted_fraction": round(adjusted_fraction, 6),
        "bet_amount": bet_amount,
        "edge": round(edge, 6),
        "recommended": edge > 0 and kelly_fraction > 0,
    }
