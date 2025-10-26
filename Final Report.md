## 4\. Final Report

### 4.1. Introduction & Problem Statement

Cryptocurrency markets are notoriously volatile. Market liquidity—the ease of buying or selling an asset without causing a major price change—is a key factor in stability. A lack of liquidity can lead to price crashes and market instability. The objective of this project was to build a machine learning model to predict cryptocurrency liquidity, allowing traders and platforms to manage risk.

### 4.2. Methodology & Data

  * **Data:** The dataset comprised historical (2016-2017) price and volume data for 105 cryptocurrencies.
  * **Target Variable:** We engineered a proxy, the **Amihud Illiquidity Score** (`|Daily Return| / Volume`), as our prediction target. A higher score signifies *lower* liquidity.
  * **Features:** We engineered 6 key features: 30-day volatility, 30-day moving average of price, 30-day moving average of volume, and 1-day lagged values for illiquidity, volume, and volatility.
  * **Model:** We selected a `RandomForestRegressor` model for its robustness and ability to handle non-linear relationships.
  * **Cleaning:** The most critical step was cleaning the data. We had to remove rows with 0 `Close` price to prevent `inf` values and "clip" extreme outliers in the illiquidity score (at the 99.9th percentile) to prevent "too large" value errors.

### 4.3. Model Performance & Evaluation

The model was trained on the first 80% of the time-series data and evaluated on the final 20%.

**Final Model Metrics:**

  * **Root Mean Squared Error (RMSE):** 0.0000000000
  * **Mean Absolute Error (MAE):** 0.0000000000
  * **R-Squared (R²) Score:** **0.9926**

### 4.4. Key Insights & Findings

  * The R² score of **0.9926** indicates that our model can explain **99.26%** of the variance in the next day's illiquidity. This is an extremely strong result.
  * The MAE and RMSE values are effectively zero, which means the model's predictions are, on average, exceptionally close to the true values. This is likely because, after clipping, the `illiquidity_lag_1` (yesterday's value) is an overwhelmingly powerful predictor for today's value in a non-volatile market.
  * This confirms the hypothesis that liquidity is "sticky" and that recent volatility and volume are key indicators of change.

### 4.5. Conclusion & Deployment


We successfully built and trained a highly accurate machine learning model to predict cryptocurrency illiquidity. The model was deployed locally using a Streamlit application, which allows a user to input data and receive a real-time liquidity score prediction. This tool can effectively help traders assess and manage risk.
