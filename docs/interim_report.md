# Interim Report: Brent Oil Change Point Analysis

## 1. Introduction
The objective of this project is to analyze the impact of major political and economic events on Brent oil prices from 1987 to 2022. By employing Bayesian Change Point detection, we aim to identify structural breaks in price trends and quantify the effect of these events. This report outlines the foundational work completed in Task 1, including the analysis workflow, event compilation, and initial exploratory data analysis (EDA).

## 2. Data Analysis Workflow
The analysis follows a structured five-step workflow:
1.  **Data Collection & Preprocessing**: Loading historical price data and calculating log returns to stabilize variance.
2.  **Exploratory Data Analysis (EDA)**: Investigating trends, seasonality, and stationarity.
3.  **Bayesian Change Point Modeling**: Using PyMC to detect structural breaks.
4.  **Event Association**: Correlating detected change points with geopolitical events.
5.  **Dashboard Development**: Visualizing results via an interactive Flask/React application.

Detailed documentation is available in `docs/data_analysis_workflow.md`.

## 3. Key Events
A dataset of major geopolitical and economic events affecting the oil market has been compiled. Key events include:
-   **1990**: Gulf War (Iraq invades Kuwait)
-   **2001**: 9/11 Terrorist Attacks
-   **2008**: Global Financial Crisis
-   **2014**: Oil Price Crash (Supply glut)
-   **2020**: COVID-19 Pandemic & Russia-Saudi Price War
-   **2022**: Russia-Ukraine War

The full list is available in `data/processed/events.csv`.

## 4. Exploratory Data Analysis (EDA) Findings

### Data Overview
-   **Range**: 20-May-1987 to 21-Apr-2020
    -   *Note*: The provided dataset ends in April 2020, while the project scope references September 2022. This limitation restricts analysis of the post-2020 recovery and the 2022 Russia-Ukraine war onset.
-   **Observation Count**: 8,360 daily records.

### Price Trends & Volatility
-   **Price**: The time series shows significant non-stationarity with visible trends and structural breaks (e.g., 2008 spike, 2014 crash, 2020 collapse).
-   **Volatility**: Log returns oscillate around zero but exhibit "volatility clustering," where periods of high volatility (large price swings) cluster together, particularly during crises (1991, 2008, 2014, 2020).

### Statistical Tests (ADF)
-   **Brent Oil Price**:
    -   Test Statistic: -2.0187 (p-value: 0.2785)
    -   **Result**: Fail to reject null hypothesis. The price series is **Non-Stationary**.
-   **Log Returns**:
    -   Test Statistic: -12.6031 (p-value: 0.0000)
    -   **Result**: Reject null hypothesis. The returns series is **Stationary**.

### Implications for Modeling
Since the raw price series is non-stationary, standard regression models may yield spurious results. The proposed Bayesian Change Point model is appropriate as it explicitly models the structural breaks (changes in mean/variance) that cause non-stationarity.

## 5. Next Steps
-   **Task 2**: Implement the Bayesian Change Point model in PyMC to detect the exact dates of structural breaks.
-   **Task 3**: specific focus on the 2020 crash given the data limit, or request updated data to cover 2022.
-   **Dashboard**: Begin backend API development.
