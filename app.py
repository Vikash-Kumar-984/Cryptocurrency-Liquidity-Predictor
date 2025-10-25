# app.py
import streamlit as st
import joblib
import numpy as np

# --- 10. Local Deployment (Streamlit) ---

# Set page title and icon
st.set_page_config(page_title="Liquidity Predictor", page_icon="💧")

# Load the trained model and scaler
# Use st.cache_resource to load only once
@st.cache_resource
def load_model():
    try:
        model = joblib.load('liquidity_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return model, scaler
    except FileNotFoundError:
        return None, None

model, scaler = load_model()

if model is None or scaler is None:
    st.error("🔴 Model or scaler files not found. Please make sure 'liquidity_model.pkl' and 'scaler.pkl' are in the same folder as 'app.py'.")
else:
    st.title("📈 Cryptocurrency Liquidity Predictor")
    st.write("This app predicts a cryptocurrency's illiquidity score for *today* based on *yesterday's* data. A **higher score** means **less liquid** (i.e., higher price impact for trades).")

    with st.form("prediction_form"):
        st.header("Enter Yesterday's Market Data")
        
        # --- Create input fields for the features ---
        # We use columns for a cleaner layout
        col1, col2 = st.columns(2)

        with col1:
            illiquidity_lag_1 = st.number_input(
                "Yesterday's Illiquidity Score", 
                min_value=0.0, 
                value=1e-9, 
                format="%.10f",
                help="The Amihud illiquidity score from yesterday."
            )
            volume_lag_1 = st.number_input(
                "Yesterday's Trade Volume (USD)", 
                min_value=0.0, 
                value=150000000.0, 
                format="%.2f",
                help="Total USD value of trades yesterday."
            )
            volatility_lag_1 = st.number_input(
                "Yesterday's 30d Volatility", 
                min_value=0.0, 
                value=0.05, 
                format="%.4f",
                help="The 30-day rolling standard deviation of daily returns, as of yesterday."
            )
            
        with col2:
            # For a simple prediction, we assume today's rolling averages
            # are the same as yesterday's.
            moving_avg_close_30d = st.number_input(
                "Yesterday's 30d Avg. Close Price", 
                min_value=0.0, 
                value=5000.0, 
                format="%.2f"
            )
            moving_avg_volume_30d = st.number_input(
                "Yesterday's 30d Avg. Volume", 
                min_value=0.0, 
                value=100000000.0, 
                format="%.2f"
            )
            # We need all 6 features for the model
            volatility_30d = volatility_lag_1
        
        # Submit button
        submitted = st.form_submit_button("Predict Liquidity")

    if submitted:
        # Create the feature array in the correct order
        features_list = [
            volatility_30d,
            moving_avg_close_30d,
            moving_avg_volume_30d,
            illiquidity_lag_1,
            volume_lag_1,
            volatility_lag_1
        ]
        
        # Convert inputs to a 2D numpy array
        input_features = np.array([features_list])
        
        # Scale the features
        input_scaled = scaler.transform(input_features)
        
        # Make prediction
        prediction = model.predict(input_scaled)
        
        st.success(f"**Predicted Illiquidity Score:** `{prediction[0]:.10f}`")
        st.info("Remember: A higher score means *less* liquidity (higher price impact).")