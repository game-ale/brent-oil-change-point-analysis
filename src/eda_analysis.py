
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller

# Set plot style
plt.style.use('ggplot')

# Load Data
try:
    df = pd.read_csv('Data/BrentOilPrices.csv')
    print("Data loaded successfully.")
    print(df.head())
except FileNotFoundError:
    print("Error: File not found. Checking alternate path...")
    try:
        df = pd.read_csv('data/raw/BrentOilPrices.csv')
        print("Data loaded from data/raw/.")
    except FileNotFoundError:
        print("Error: Could not find dataset.")
        exit()

# Preprocessing
# Date format is 'day-month-year' e.g. 20-May-87
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
df.set_index('Date', inplace=True)
df.sort_index(inplace=True)

# Calculate Log Returns
df['Log_Returns'] = np.log(df['Price'] / df['Price'].shift(1))

# --- PLOTTING ---

# 1. Price History
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Price'], label='Brent Oil Price (USD)')
plt.title('Brent Oil Prices (1987-2022)')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.savefig('docs/images/brent_price_history.png')
plt.close()

# 2. Log Returns (Volatility)
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Log_Returns'], label='Log Returns', alpha=0.7)
plt.title('Brent Oil Price Log Returns (Volatility)')
plt.xlabel('Date')
plt.ylabel('Log Return')
plt.legend()
plt.savefig('docs/images/brent_log_returns.png')
plt.close()

# 3. Rolling Mean & Std Dev
rolling_mean = df['Price'].rolling(window=365).mean()
rolling_std = df['Price'].rolling(window=365).std()

plt.figure(figsize=(12, 6))
plt.plot(df['Price'], label='Original')
plt.plot(rolling_mean, label='Rolling Mean (1yr)')
plt.plot(rolling_std, label='Rolling Std (1yr)')
plt.title('Rolling Mean & Standard Deviation')
plt.legend()
plt.savefig('docs/images/rolling_stats.png')
plt.close()

# --- STATISTICAL TESTS ---

def adf_test(timeseries):
    print("Results of Dickey-Fuller Test:")
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)
    return dfoutput

print("\n--- ADF Test on Prices ---")
adf_res_price = adf_test(df['Price'].dropna())

print("\n--- ADF Test on Log Returns ---")
adf_res_returns = adf_test(df['Log_Returns'].dropna())

# --- SUMMARY STATISTICS ---
print("\n--- Summary Statistics ---")
print(df.describe())

# Save summary to file
with open('docs/eda_summary.txt', 'w') as f:
    f.write("Brent Oil Prices EDA Summary\n")
    f.write("============================\n\n")
    f.write("Dataset Range: {} to {}\n".format(df.index.min(), df.index.max()))
    f.write("Total Observations: {}\n\n".format(len(df)))
    
    f.write("Price Statistics:\n")
    f.write(df['Price'].describe().to_string())
    f.write("\n\n")

    f.write("ADF Test - Price (Non-Stationary?):\n")
    f.write(f"Test Statistic: {adf_res_price['Test Statistic']:.4f}\n")
    f.write(f"p-value: {adf_res_price['p-value']:.4f}\n")
    if adf_res_price['p-value'] > 0.05:
        f.write("Result: The time series is likely non-stationary (Unit Root present)\n")
    else:
        f.write("Result: The time series is likely stationary\n")
    f.write("\n")

    f.write("ADF Test - Log Returns (Stationary?):\n")
    f.write(f"Test Statistic: {adf_res_returns['Test Statistic']:.4f}\n")
    f.write(f"p-value: {adf_res_returns['p-value']:.4f}\n")
    if adf_res_returns['p-value'] > 0.05:
        f.write("Result: The time series is likely non-stationary (Unit Root present)\n")
    else:
        f.write("Result: The time series is likely stationary\n")
