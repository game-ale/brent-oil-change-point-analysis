# Final Report: Brent Oil Price Change Point Analysis

## Executive Summary
This project successfully analyzed historical Brent oil price data (1987-2020) to identify significant structural breaks and associate them with major geopolitical and economic events. Using a Bayesian Change Point model implemented in PyMC, we detected a primary mean shift period in late 2019, likely associated with the **Saudi Aramco Drone Attack** and the subsequent onset of global instability.

## Technical Implementation

### 1. Data Foundation & EDA
- **Dataset**: Brent Oil Prices (1987-2020).
- **Preprocessing**: Log returns were calculated to assess volatility, and the price series was analyzed for stationarity using the Augmented Dickey-Fuller (ADF) test.
- **Insights**: Prices exhibit non-stationarity in levels but stationarity in log returns, justifying the use of structural break models for the mean price.

### 2. Bayesian Change Point Modeling
- **Framework**: PyMC (Probabilistic Programming in Python).
- **Model Architecture**:
  - **Prior**: Discrete Uniform prior for the "switch point" ($\tau$).
  - **Priors for Means**: Normal priors for price means before ($\mu_1$) and after ($\mu_2$) the break.
  - **Likelihood**: Normal likelihood for observed prices.
- **Results**:
  - **Detected Break**: Approximately July - September 2019.
  - **Magnitude**: A mean price shift of approximately **-20.09%**.
  - **Associated Event**: Saudi Aramco Drone Attack (September 14, 2019).

### 3. Interactive Dashboard
- **Backend**: Flask API serving processed price data, historical events, and Bayesian results.
- **Frontend**: Premium React application built with Vite, featuring:
  - **Recharts** for interactive time-series visualization.
  - **Lucide-React** for high-quality iconography.
  - **Glassmorphism UI** for a modern, professional look.

## Key Findings
The analysis highlights the extreme sensitivity of oil prices to supply-disruption events. The 2019 drone attack on Saudi infrastructure caused a significant structural break in price averages, which preceded the even more volatile period of the 2020 COVID-19 pandemic and Russia-Saudi price wars.

## Conclusion & Future Work
The project demonstrates the power of Bayesian inference for quantifying uncertainty in event-driven market shifts. Future enhancements could include:
- Implementing **Multi-Change Point Models** to detect several breaks over the 30-year span.
- Integrating **Volatility Clustered Models** (e.g., Stochastic Volatility) to analyze risk shifts.
- Expanding data coverage to include the 2022 Russia-Ukraine conflict.

---
**Birhan Energies Data Science Team**  
*February 2026*
