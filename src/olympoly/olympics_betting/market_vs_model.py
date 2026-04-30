import pandas as pd


def compare_market_vs_model(df_market, df_model, model_col="event"):
    """
    Merge market and model probabilities and compute edge (difference).
    """

    # -----------------------
    # Validate required columns
    # -----------------------
    if "event" not in df_market.columns:
        raise ValueError("df_market must contain 'event'")
    if "price" not in df_market.columns:
        raise ValueError("df_market must contain 'price'")
    if "model_prob" not in df_model.columns:
        raise ValueError("df_model must contain 'model_prob'")

    # -----------------------
    # Rename for consistency
    # -----------------------
    market = df_market.copy().rename(columns={"price": "market_prob"})
    model = df_model.copy()

    # If model uses different join column (e.g. NOC)
    if model_col != "event":
        model = model.rename(columns={model_col: "event"})

    # -----------------------
    # Merge
    # -----------------------
    merged = pd.merge(market, model, on="event", how="inner")

    # -----------------------
    # Compute difference
    # -----------------------
    merged["difference"] = merged["market_prob"] - merged["model_prob"]

    return merged

def calibration_summary(
    df: pd.DataFrame,
    model_col: str = "model_prob",
    market_col: str = "market_prob",
    n_bins: int = 5,
) -> pd.DataFrame:
    """
    Summarize how well model probabilities are calibrated relative to market prices.

    Splits events into probability bins and reports the average model vs.
    average market probability per bin. A well-calibrated model should show
    model and market probabilities tracking closely across bins.

    Parameters
    ----------
    df : pd.DataFrame
        A merged DataFrame — typically the output of compare_market_vs_model().
        Must contain model_col and market_col.
    model_col : str
        Column name for model probabilities (default: 'model_prob').
    market_col : str
        Column name for market probabilities (default: 'market_prob').
    n_bins : int
        Number of equal-width probability bins (default: 5).

    Returns
    -------
    pd.DataFrame with columns:
        - bin            : probability range label (e.g. '0.20 – 0.40')
        - count          : number of events in this bin
        - avg_model_prob : mean model probability in bin
        - avg_market_prob: mean market probability in bin
        - avg_edge       : mean (model - market) in bin
        - edge_std       : standard deviation of edge in bin

    Examples
    --------
    >>> merged = compare_market_vs_model(df_market, df_model)
    >>> print(calibration_summary(merged))
    """
    if model_col not in df.columns or market_col not in df.columns:
        raise ValueError(f"DataFrame must contain '{model_col}' and '{market_col}' columns.")

    df = df.copy()
    df["edge"] = df[model_col] - df[market_col]

    bin_edges = [i / n_bins for i in range(n_bins + 1)]
    bin_labels = [f"{bin_edges[i]:.2f} – {bin_edges[i+1]:.2f}" for i in range(n_bins)]

    df["bin"] = pd.cut(df[model_col], bins=bin_edges, labels=bin_labels, include_lowest=True)

    summary = (
        df.groupby("bin", observed=True)
        .agg(
            count=(model_col, "count"),
            avg_model_prob=(model_col, "mean"),
            avg_market_prob=(market_col, "mean"),
            avg_edge=("edge", "mean"),
            edge_std=("edge", "std"),
        )
        .reset_index()
    )

    summary["avg_model_prob"] = summary["avg_model_prob"].round(4)
    summary["avg_market_prob"] = summary["avg_market_prob"].round(4)
    summary["avg_edge"] = summary["avg_edge"].round(4)
    summary["edge_std"] = summary["edge_std"].round(4)

    return summary
