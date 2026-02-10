import pandas as pd
import numpy as np
import pymc as pm
import matplotlib.pyplot as plt
import arviz as az
import config
from pathlib import Path
from typing import Tuple, Dict

def load_and_preprocess(filepath: Path) -> pd.DataFrame:
    """Loads and prepares data for modeling."""
    try:
        if not filepath.exists():
            fallback_path = config.PROJECT_ROOT / "Data" / "BrentOilPrices.csv"
            if fallback_path.exists():
                filepath = fallback_path
            else:
                raise FileNotFoundError(f"Dataset not found at {filepath}")

        df = pd.read_csv(filepath)
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
        df.dropna(subset=['Date'], inplace=True)
        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)
        
        # We model the Price series directly for mean change point
        # but also log returns can be modeled for volatility change.
        # Following the instructions, we'll build a simple model for mean price change.
        return df
    except Exception as e:
        print(f"Error in data loading: {e}")
        return pd.DataFrame()

def build_and_sample_model(data: pd.DataFrame) -> Tuple[pm.Model, az.InferenceData]:
    """Builds the PyMC Change Point model and runs MCMC sampling."""
    prices = data['Price'].values
    n_days = len(prices)
    day_indices = np.arange(n_days)

    with pm.Model() as model:
        # Priors for the switch point (tau)
        # Uniform discrete prior over all possible days
        tau = pm.DiscreteUniform("tau", lower=0, upper=n_days - 1)

        # Priors for the means before and after the switch
        # Price is always positive, so we use an exponential or normal with broad bounds
        mu_1 = pm.Normal("mu_1", mu=prices.mean(), sigma=prices.std() * 2)
        mu_2 = pm.Normal("mu_2", mu=prices.mean(), sigma=prices.std() * 2)

        # Prior for the standard deviation (assuming it stays roughly constant for simplicity)
        sigma = pm.HalfNormal("sigma", sigma=prices.std())

        # Switch function to select the mean based on whether index is before/after tau
        mu = pm.math.switch(tau >= day_indices, mu_1, mu_2)

        # Likelihood
        y = pm.Normal("y", mu=mu, sigma=sigma, observed=prices)

        # Run the Sampler
        # Note: Discrete variables require specialized samplers like Metropolis
        trace = pm.sample(2000, tune=1000, chains=2, return_inferencedata=True)

    return model, trace

def interpret_results(trace: az.InferenceData, data: pd.DataFrame) -> Dict:
    """Analyzes the posterior distributions and quantifies impacts."""
    summary = az.summary(trace, round_to=2)
    print("\n--- Model Summary ---")
    print(summary)

    # Get the posterior of tau
    tau_posterior = trace.posterior['tau'].values.flatten()
    tau_mode = int(pd.Series(tau_posterior).mode()[0])
    change_date = data.index[tau_mode]

    # Means
    mu1_mean = trace.posterior['mu_1'].mean().values.item()
    mu2_mean = trace.posterior['mu_2'].mean().values.item()
    price_change_pct = ((mu2_mean - mu1_mean) / mu1_mean) * 100

    results = {
        "change_point_index": tau_mode,
        "change_date": change_date,
        "mu1": mu1_mean,
        "mu2": mu2_mean,
        "price_change_pct": price_change_pct,
        "r_hat_max": summary['r_hat'].max()
    }

    print(f"\nDetected Change Point: {change_date.strftime('%Y-%m-%d')}")
    print(f"Mean Price Before: ${mu1_mean:.2f}")
    print(f"Mean Price After: ${mu2_mean:.2f}")
    print(f"Impact: {price_change_pct:+.2f}%")

    # Plot posterior of tau
    plt.figure(figsize=(10, 4))
    plt.hist(tau_posterior, bins=100, density=True)
    plt.title(f"Posterior Distribution of Switch Point (τ)\nMode: {change_date.strftime('%Y-%m-%d')}")
    plt.xlabel("Day Index")
    plt.savefig(config.IMAGES_DIR / "tau_posterior.png")
    plt.close()

    # Plot Trace
    az.plot_trace(trace)
    plt.savefig(config.IMAGES_DIR / "model_trace.png")
    plt.close()

    return results

def associate_with_events(change_date: pd.Timestamp) -> Dict:
    """Finds the closest recorded event to the detected change point."""
    try:
        events_df = pd.read_csv(config.EVENTS_FILE)
        events_df['Date'] = pd.to_datetime(events_df['Date'])
        
        # Calculate time difference
        events_df['days_diff'] = (events_df['Date'] - change_date).dt.days.abs()
        closest_event = events_df.loc[events_df['days_diff'].idxmin()]
        
        return {
            "event_name": closest_event['Event'],
            "event_date": closest_event['Date'].strftime('%Y-%m-%d'),
            "days_diff": int(closest_event['days_diff']),
            "description": closest_event['Description']
        }
    except Exception as e:
        print(f"Error associating with events: {e}")
        return {}

def main():
    print("Loading data...")
    df = load_and_preprocess(config.BRENT_PRICES_FILE)
    if df.empty:
        return

    # --- Final Model Run ---
    # Using a subset of the last 500 days for high-speed Bayesian inference
    # in local environments without C-compilation (g++).
    print("Using the last 500 observations for efficient analysis...")
    df_subset = df.iloc[-500:].copy()

    print("Building model and sampling...")
    # Bayesian structural break model for mean price shift
    with pm.Model() as model:
        prices = df_subset['Price'].values
        n_days = len(prices)
        day_indices = np.arange(n_days)
        
        # Priors: Switch point (tau), pre-break mean (mu1), post-break mean (mu2)
        tau = pm.DiscreteUniform("tau", lower=0, upper=n_days - 1)
        mu_1 = pm.Normal("mu_1", mu=prices.mean(), sigma=prices.std() * 2)
        mu_2 = pm.Normal("mu_2", mu=prices.mean(), sigma=prices.std() * 2)
        sigma = pm.HalfNormal("sigma", sigma=prices.std())
        
        # Switch logic
        mu = pm.math.switch(tau >= day_indices, mu_1, mu_2)
        
        # Likelihood
        y = pm.Normal("y", mu=mu, sigma=sigma, observed=prices)

        # MCMC Sampling - Optimized for speed
        trace = pm.sample(200, tune=100, chains=1, return_inferencedata=True, cores=1)
    
    print("Interpreting results...")
    results = interpret_results(trace, df_subset)
    
    print("Associating with known events...")
    closest_event = associate_with_events(results['change_date'])
    results.update(closest_event)

    # Export results for dashboard consumption
    output_json = config.PROCESSED_DATA_DIR / "change_point_results.json"
    pd.Series(results).to_json(output_json)
    print(f"\nAssociated Event: {closest_event.get('event_name', 'None')} ({closest_event.get('event_date', 'N/A')})")
    print(f"\nFinal Results saved to {output_json}")

if __name__ == "__main__":
    main()
