# Brent Oil Change Point Analysis

## Project Overview
This project analyzes the impact of major political and economic events on Brent oil prices from 1987 to 2022. By employing Bayesian Change Point detection (PyMC), we aim to identify structural breaks in price trends, quantify the effect of these events, and visualizing the insights via an interactive dashboard.

## Objectives
1.  **Identify Key Events**: Recognize major geopolitical and economic events that impacted oil prices.
2.  **Change Point Detection**: Use statistical methods (Bayesian inference) to detect structural breaks in the time series.
3.  **Quantify Impact**: Measure the magnitude of price changes associated with these events.
4.  **Interactive Dashboard**: Build a Flask/React application to visualize the analysis results.

## Data
The dataset contains daily Brent oil prices.
-   **Source**: `Data/BrentOilPrices.csv` (provided)
-   **Range**: May 20, 1987 - April 21, 2020 (Note: Dataset ends earlier than the project scope of Sep 2022).
-   **Key Fields**: `Date`, `Price`.

## Methodology
The analysis follows a structured workflow:
1.  **Data Preprocessing**: Cleaning and calculating log returns.
2.  **Exploratory Data Analysis (EDA)**: Trend, seasonality, and stationarity analysis (ADF test).
3.  **Bayesian Modeling**: Implementing a Change Point model using PyMC to detect shifts in mean and volatility.
4.  **Insight Generation**: Correlating detected changes with compiled event data.

## Project Structure
```
├── data
│   ├── raw            # Original dataset
│   └── processed      # Cleaned data and event lists (events.csv)
├── docs               # Documentation and reports
│   ├── images         # EDA plots
│   ├── data_analysis_workflow.md
│   └── interim_report.md
├── notebooks          # Jupyter notebooks for analysis (eda.ipynb)
├── src                # Source code for analysis and modeling
│   ├── config.py      # Configuration and path management
│   ├── eda_analysis.py# EDA script (Type-hinted, Modular)
│   └── test_eda.py    # Unit tests
├── dashboard          # Interactive dashboard (Backend/Frontend)
├── requirements.txt   # Python dependencies
├── .gitignore         # Git ignore file
└── README.md          # Project overview
```

## Current Status
- [x] **Task 1: Foundation & EDA** (Completed)
- [x] **Task 2: Change Point Modeling** (Completed)
- [x] **Task 3: Dashboard Development** (Completed)

## How to Run
1.  **Environment Setup**:
    -   Install dependencies: `pip install -r requirements.txt`
2.  **EDA**:
    -   Run the notebook: `jupyter notebook notebooks/eda.ipynb`
    -   Run the script: `python src/eda_analysis.py`
    -   Run tests: `python src/test_eda.py`