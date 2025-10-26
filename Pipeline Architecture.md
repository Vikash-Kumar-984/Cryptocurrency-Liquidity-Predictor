## 3\. Pipeline Architecture

This document describes the flow of data from raw files to a trained, predictive model (all performed in Google Colab).

1.  **Start: Raw Data Ingestion**

      * **Input:** Folder containing multiple raw `.csv` files from Kaggle.
      * **Action:** `glob.glob` finds all CSVs. `pandas.read_csv` loads and concatenates them.
      * **Output:** A single raw DataFrame.

2.  **Step 2: Preprocessing**

      * **Input:** Raw, combined DataFrame.
      * **Action:** Filters for 2016-2017. Fills `NaN` values. **Removes all rows where `Close` price is 0.**
      * **Output:** A clean DataFrame.

3.  **Step 3: Feature Engineering**

      * **Input:** Clean DataFrame.
      * **Action:** Applies a function `groupby('Symbol')` to create `daily_return`, `illiquidity`, `volatility_30d`, `moving_avg_close_30d`, `moving_avg_volume_30d`, and lagged features.
      * **Output:** A feature-rich DataFrame (contains `inf` and `NaN` values).

4.  **Step 4: Outlier & NaN Removal**

      * **Input:** Feature-rich DataFrame.
      * **Action:**
        1.  Replaces all `inf` values with `NaN`.
        2.  Drops all rows containing *any* `NaN` values.
        3.  **Clips** the `illiquidity` and `illiquidity_lag_1` columns at the 99.9th percentile to remove "too large" values.
      * **Output:** A final, clean, model-ready DataFrame.

5.  **Step 5: Model Training & Serialization**

      * **Input:** Model-ready DataFrame.
      * **Action:**
        1.  Splits data into `X` (features) and `y` (target).
        2.  `StandardScaler` is fit and applied to `X`.
        3.  Data is split 80/20 by time (no shuffle).
        4.  `RandomForestRegressor` is trained.
        5.  `joblib.dump()` saves the `model` and `scaler`.
      * **Output:** `liquidity_model.pkl` and `scaler.pkl`.

-----

