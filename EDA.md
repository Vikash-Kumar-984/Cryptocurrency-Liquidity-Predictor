# Exploratory Data Analysis (EDA) Report

## 1.1. Introduction
This report details the Exploratory Data Analysis (EDA) conducted on the 2016-2017 cryptocurrency dataset. The goal was to understand data patterns, trends, and correlations to inform feature engineering for the liquidity prediction model.

## 1.2. Dataset Summary
* **Source:** Kaggle Cryptocurrency Price History (2016-2017 subset)
* **Timeframe:** 2016-01-01 to 2017-12-31
* **Total Records:** 117,144 (after cleaning and feature engineering)
* **Total Features:** 6 engineered features + 1 target variable
* **Unique Coins:** 105

## 1.3. Data Cleaning & Preprocessing
* Loaded all individual coin CSVs and concatenated them.
* Filtered data to the required 2016-2017 timeframe.
* Handled missing `Close` and `Volume` values using `ffill()` (forward-fill) on a per-coin basis to maintain time-series integrity.
* Removed all rows where `Close` price was 0 to prevent division-by-zero errors during return calculation.
* Removed rows with `NaN` values resulting from rolling window calculations.

## 1.4. Visualizations & Key Insights

#### Engineered Feature: 'Illiquidity'
* **Definition:** The **Amihud Illiquidity measure** (`|Daily Return| / Volume`) was created as the target variable. A higher score means less liquidity (higher price impact).
* **Insight:** The illiquidity metric was found to be extremely right-skewed. Most days are highly liquid (score near 0), with rare, extreme spikes of illiquidity.
* **Action:** To prevent these "too large" values from breaking the model, we "clipped" all illiquidity scores at the 99.9th percentile.

#### Correlation Analysis

* **Insight:**
    * The target `illiquidity` shows a strong positive correlation with its own lagged value (`illiquidity_lag_1`), confirming that liquidity is "sticky" (yesterday's liquidity is a good predictor of today's).
    * `illiquidity` is also positively correlated with `volatility_30d`. High volatility is linked to lower liquidity.
    * `illiquidity` has a negative correlation with `moving_avg_volume_30d`, confirming that higher average volume leads to *more* liquidity (a lower score).
