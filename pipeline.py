import streamlit as st
import pandas as pd
import joblib

# Load the trained pipeline
pipeline = joblib.load('rf_model_pipeline.pkl')

# Extract available options for categorical features
preprocessor = pipeline.named_steps['preprocessor']
one_hot_encoder = preprocessor.named_transformers_['cat']
categories = one_hot_encoder.categories_

# Streamlit app
st.title("Price Prediction App")

# Input fields for categorical features
item_code = st.selectbox("Select Item Code", categories[0])  # Options for item_code
premise_type = st.selectbox("Select Premise Type", categories[1])  # Options for premise_type
district = st.selectbox("Select District", categories[2])  # Options for district

# Input field for numerical feature
month = st.number_input("Enter Month (1-12)", min_value=1, max_value=12, value=1)

# Create raw input DataFrame
input_data = pd.DataFrame({
    'item_code': [item_code],
    'premise_type': [premise_type],
    'district': [district],
    'month': [month]
})

# Predict button
if st.button("Predict"):
    try:
        # Pass raw input to the pipeline
        prediction = pipeline.predict(input_data)[0]
        st.success(f"Predicted Price: {prediction:.2f}")
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
