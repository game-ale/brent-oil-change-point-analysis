import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller
import config
import sys
from pathlib import Path

# Set plot style
plt.style.use('ggplot')

def load_data(filepath: Path) -> pd.DataFrame:
    """Loads the Brent Oil Prices dataset.
    
    Args:
        filepath: Path to the CSV file.
        
    Returns:
        pd.DataFrame: Loaded data.
    """
    try:
        # Try finding the file in typical locations if the specific config path fails
        if not filepath.exists():
             # Fallback logic for where the user might have placed it manually in the root 'Data' folder
             # as observed in previous steps
             fallback_path = config.PROJECT_ROOT / "Data" / "BrentOilPrices.csv"
             if fallback_path.exists():
                 filepath = fallback_path
             else:
                 raise FileNotFoundError(f"Dataset not found at {filepath} or {fallback_path}")

        df = pd.read_csv(filepath)
        print(f"Data loaded successfully from {filepath}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Parses dates and calculates log returns.
    
    Args:
        df: Raw dataframe.
        
    Returns:
        pd.DataFrame: Processed dataframe with 'Log_Returns' and DateTime index.
    """
    try:
        # Date format parsing
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
        
        # Check for data quality
        initial_count = len(df)
        df.dropna(subset=['Date'], inplace=True)
        if len(df) < initial_count:
            print(f"Warning: Dropped {initial_count - len(df)} rows due to invalid dates.")

        df.set_index('Date', inplace=True)
        df.sort_index(inplace=True)

        # Calculate Log Returns
        df['Log_Returns'] = np.log(df['Price'] / df['Price'].shift(1))
        
        return df
    except KeyError as e:
        print(f"Error: Missing expected column {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        sys.exit(1)

def plot_price_history(df: pd.DataFrame, output_path: Path) -> None:
    """Plots and saves the price history."""
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Price'], label='Brent Oil Price (USD)')
    plt.title('Brent Oil Prices (1987-2022)')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.savefig(output_path)
    plt.close()

def plot_volatility(df: pd.DataFrame, output_path: Path) -> None:
    """Plots and saves the log returns (volatility)."""
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Log_Returns'], label='Log Returns', alpha=0.7)
    plt.title('Brent Oil Price Log Returns (Volatility)')
    plt.xlabel('Date')
    plt.ylabel('Log Return')
    plt.legend()
    plt.savefig(output_path)
    plt.close()

def plot_rolling_stats(df: pd.DataFrame, output_path: Path) -> None:
    """Plots and saves rolling mean and standard deviation."""
    rolling_mean = df['Price'].rolling(window=365).mean()
    rolling_std = df['Price'].rolling(window=365).std()

    plt.figure(figsize=(12, 6))
    plt.plot(df['Price'], label='Original')
    plt.plot(rolling_mean, label='Rolling Mean (1yr)')
    plt.plot(rolling_std, label='Rolling Std (1yr)')
    plt.title('Rolling Mean & Standard Deviation')
    plt.legend()
    plt.savefig(output_path)
    plt.close()

def perform_adf_test(timeseries: pd.Series) -> pd.Series:
    """Performs Augmented Dickey-Fuller test.
    
    Args:
        timeseries: Time series data to test.
        
    Returns:
        pd.Series: Test results including statistic and p-value.
    """
    dftest = adfuller(timeseries.dropna(), autolag='AIC')
    results = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        results[f'Critical Value ({key})'] = value
    return results

def save_summary(df: pd.DataFrame, price_adf: pd.Series, returns_adf: pd.Series, output_path: Path) -> None:
    """Saves summary statistics and test results to a file."""
    with open(output_path, 'w') as f:
        f.write("Brent Oil Prices EDA Summary\n")
        f.write("============================\n\n")
        f.write(f"Dataset Range: {df.index.min()} to {df.index.max()}\n")
        f.write(f"Total Observations: {len(df)}\n\n")
        
        f.write("Price Statistics:\n")
        f.write(df['Price'].describe().to_string())
        f.write("\n\n")

        f.write("ADF Test - Price (Non-Stationary?):\n")
        f.write(f"Test Statistic: {price_adf['Test Statistic']:.4f}\n")
        f.write(f"p-value: {price_adf['p-value']:.4f}\n")
        f.write(f"Result: {'Likely Non-Stationary' if price_adf['p-value'] > 0.05 else 'Likely Stationary'}\n\n")

        f.write("ADF Test - Log Returns (Stationary?):\n")
        f.write(f"Test Statistic: {returns_adf['Test Statistic']:.4f}\n")
        f.write(f"p-value: {returns_adf['p-value']:.4f}\n")
        f.write(f"Result: {'Likely Non-Stationary' if returns_adf['p-value'] > 0.05 else 'Likely Stationary'}\n")

def main():
    print("Starting EDA Analysis...")
    
    # Load
    df = load_data(config.BRENT_PRICES_FILE)
    
    # Preprocess
    df = preprocess_data(df)
    
    # Plot
    print("Generating plots...")
    plot_price_history(df, config.IMAGES_DIR / 'brent_price_history.png')
    plot_volatility(df, config.IMAGES_DIR / 'brent_log_returns.png')
    plot_rolling_stats(df, config.IMAGES_DIR / 'rolling_stats.png')
    
    # Analysis
    print("Performing statistical tests...")
    adf_res_price = perform_adf_test(df['Price'])
    adf_res_returns = perform_adf_test(df['Log_Returns'])
    
    # Save Summary
    print(f"Saving summary to {config.SUMMARY_FILE}...")
    save_summary(df, adf_res_price, adf_res_returns, config.SUMMARY_FILE)
    
    print("EDA Analysis completed successfully.")

if __name__ == "__main__":
    main()
