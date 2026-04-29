# demo

from olympoly.load_data import get_cleaned_data
from olympoly.performance import country_efficiency, efficiency_trends
from olympoly.timeline import participation_trends, medal_trends, sport_popularity
from olympoly.olympics_betting.regression_model.model import train_model
from olympoly.olympics_betting.simulation import simulate_market_strategy
import pandas as pd

def run_demo():
    """Run a full demonstration of olympoly's analysis capabilities.
    
    Loads cleaned Summer Olympic data and showcases the performance
    and timeline modules with sample plots and statistics.
    """
    print("Loading cleaned Olympic data (Summer)...")
    df = get_cleaned_data(season="Summer")

    print("\n--- PERFORMANCE MODULE ---")

    print("1. Calculating top 10 most efficient countries (Medals / Athlete)...")
    efficiency_df = country_efficiency(df, min_athletes=50, plot=True)
    print(efficiency_df.head(10))

    print("\n2. Plotting United States efficiency trends over time...")
    efficiency_trends(df, country="United States", plot=True)

    print("\n--- TIMELINE MODULE ---")

    print("3. Plotting athlete participation trends by gender...")
    participation_trends(df, by_gender=True, plot=True)

    print("\n4. Plotting medal trends for the top 5 countries...")
    medal_trends(df, entity="Team", top_n=5, plot=True)

    print("\n5. Plotting the top 5 most popular sports over time...")
    sport_popularity(df, plot=True)

    print("\n--- MODELING & SIMULATION ---")

    print("6. Training predictive model...")
    
    df_model = df.copy()
    for col in df_model.columns:
        df_model[col] = df_model[col].astype(object)

    model, X_test, y_test = train_model(df_model)

    print("Model trained. Generating predictions...")
    probs = model.predict_proba(X_test)[:, 1]

    print("7. Running simple betting simulation...")
    
    sim_df = pd.DataFrame({
        "event": ["A", "B", "C", "D"],
        "price": [0.5, 0.5, 0.5, 0.5],
        "model_prob": probs[:4]
    })

    _, summary = simulate_market_strategy(sim_df, bet_size=0.1)

    print("Simulation summary:")
    print(summary)


if __name__ == "__main__":
    run_demo()