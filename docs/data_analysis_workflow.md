# Data Analysis Workflow

## 1. Analysis Steps

### Step 1: Data Collection and Preprocessing
- **Data Ingestion**: Load the daily Brent oil price dataset.
- **Data Validation**: Check for missing values, duplicates, and correct date formatting.
- **Transformation**: Calculate log returns (`ln(P_t / P_{t-1})`) to stabilize variance and ensure stationarity for certain models.

### Step 2: Exploratory Data Analysis (EDA)
- **Trend Analysis**: Plot the raw price series to identify long-term trends and obvious structural breaks.
- **Seasonality & Volatility**: Analyze price fluctuations and potential seasonal patterns.
- **Stationarity Testing**: Perform Augmented Dickey-Fuller (ADF) tests on prices and log returns.

### Step 3: Change Point Detection (Bayesian Modeling)
- **Model Selection**: Use a Bayesian Change Point model (PyMC) with a switch point mechanism.
- **Priors**:
    - `tau` (Switch Point): Discrete Uniform distribution over the time range.
    - `lambda` (Parameters): Exponential or Normal distributions for pre- and post-change parameters.
- **Inference**: Run MCMC sampling to estimate posterior distributions for `tau` and model parameters.

### Step 4: Event Association & Impact Quantification
- **Correlation**: Compare detected change points (posterior means/modes of `tau`) with the `events.csv` dataset.
- **Quantification**: Calculate the percentage change in mean price and volatility before and after each detected break.
- **Causality Assessment**: Qualitatively assess the link between events and price shifts (correlation vs. causation).

### Step 5: Dashboard Development
- **Backend (Flask)**: Serve processed data and change point results via API.
- **Frontend (React)**: Visualize the price timeline, change points, and event markers.

## 2. Assumptions

-   **Market Efficiency**: Prices reflect available information, and major events causes rapid price adjustments.
-   **Structural Breaks**: The data contains discrete shifts in parameters (mean/variance) rather than just continuous evolution.
-   **Independence**: Residuals after accounting for change points are assumed to be independent and identically distributed (i.i.d) for the basic model, though volatility clustering (ARCH/GARCH) is a known feature of financial time series.
-   **Data Completeness**: We assume the dataset is complete and accurate for the covered period, and that missing dates correspond to non-trading days.

## 3. Limitations

-   **Correlation vs. Causation**: A detected change point near an event does not prove the event caused the change. Other confounding factors (e.g., hidden economic shifts, simultaneous minor events) may be present. This analysis identifies *association*, not *causality*.
-   **Model Simplicity**: The basic change point model assumes a single or fixed number of breaks (or a specific process for them). Real-world data may have multiple, complex regime changes that a simple model might miss or oversimplify.
-   **Lag Effects**: Market reaction to events might not be instantaneous; there could be anticipation (pricing in) or delayed responses not perfectly aligned with the event date.
-   **Exogenous Factors**: The model focuses on the univariate time series of prices. It does not explicitly account for exogenous variables like production volumes, inventories, or exchange rates, except through their aggregate impact on price.

## 4. Communication Channels

Results will be communicated to stakeholders through the following formats:
-   **Investor Reports (PDF)**: High-level summaries focusing on key risk events and their quantified impact on portfolio value.
-   **Policy Briefs (Markdown/PDF)**: Detailed analysis of specific geopolitical events (e.g., sanctions) to inform government policy or strategic planning.
-   **Interactive Dashboard (Web App)**: A live tool for analysts to explore historical data, filter by event types, and visualize volatility regimes dynamically.
-   **Technical Documentation (GitHub/Docs)**: Full reproducibility guides, code documentation, and model specifications for the data science team.
