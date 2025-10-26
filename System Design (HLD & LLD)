### 2.1. High-Level Design (HLD)

The HLD describes the overall system architecture.

**Objective:** Create a service that can predict a cryptocurrency's liquidity score for the next day based on historical market data.

**Components:**

1.  **Data Ingestion (Colab):** A script to download, unzip, and load raw historical CSV data from the Kaggle dataset.
2.  **Data Processing & Feature Engine (Colab):** A module responsible for cleaning the data, handling 0s, and engineering all features (e.g., Amihud, moving averages, lags, volatility).
3.  **Model Training Service (Colab):** A script that loads the processed features, scales them, splits the data by time, trains the `RandomForestRegressor`, evaluates it, and saves the final `model.pkl` and `scaler.pkl`.
4.  **Prediction App (Local):** A `Streamlit` application (`app.py`) that loads the saved model/scaler, provides a UI for user input, and serves real-time predictions.

### 2.2. Low-Level Design (LLD)

The LLD describes the implementation details of each component.

**File Structure:**

```
/liquidity-project/
├── app.py                  # (Streamlit App)
├── liquidity_model.pkl     # (Saved model)
├── scaler.pkl              # (Saved scaler)
├── requirements.txt        # (pip install -r requirements.txt)
└── README.md               # (This file)
```

*(Note: The data files and training notebook remain in Google Colab, as they are not needed for deployment.)*

**Module Details:**

  * **`Training Notebook (Colab)`**

      * Loads data using `glob` and `pandas`.
      * Cleans data (handles `NaN`, `0` prices).
      * Engineers features (`illiquidity`, `volatility_30d`, lags, etc.).
      * **Clips outliers** at the 99.9th percentile to remove "too large" values.
      * Splits data into `X_train`, `y_train`, `X_test`, `y_test` using an 80/20 time-series split.
      * Trains a `RandomForestRegressor` model.
      * Saves `model.pkl` and `scaler.pkl` using `joblib`.

  * **`app.py`**

      * Loads `liquidity_model.pkl` and `scaler.pkl` using `@st.cache_resource`.
      * Creates a `st.form` with `st.number_input()` fields for the 6 required features.
      * On submit, it formats the inputs into a NumPy array, scales them using the loaded `scaler`, and calls `model.predict()` to get the illiquidity score.
      * Displays the prediction using `st.success()`.

-----
