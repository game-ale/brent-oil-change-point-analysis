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

- **Market Efficiency**: Prices reflect available information, and major events causes rapid price adjustments.
- **Structural Breaks**: The data contains discrete shifts in parameters (mean/variance) rather than just continuous evolution.
- **Independence**: Residuals after accounting for change points are assumed to be independent and identically distributed (i.i.d) for the basic model, though volatility clustering (ARCH/GARCH) is a known feature of financial time series.

## 3. Limitations

- **Correlation vs. Causation**: A detected change point near an event does not prove the event caused the change. Other confounding factors may be present.
- **Model Simplicity**: The basic change point model assumes a single or fixed number of breaks. Real-world data may have multiple, complex regime changes that a simple model might miss or oversimplify.
- **Lag Effects**: Market reaction to events might not be instantaneous; there could be anticipation or delayed responses not perfectly aligned with the event date.
- **Data Quality**: The analysis depends on the accuracy and completeness of the historical price data.
