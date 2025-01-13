import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Title of the Streamlit app
st.title("Telur Kelantan Price Prediction 🥚")

# Load the dataset
df = pd.read_csv("telur kelantan filtered.csv")

# Display the first few rows of the dataset
st.subheader("Dataset Preview")
st.write(df.head())

# Preprocessing
# Convert date to datetime and extract useful features
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['day_of_week'] = df['date'].dt.dayofweek

# Encode categorical variables
label_encoders = {}
for col in ['premise', 'premise_type', 'state', 'district', 'item', 'unit', 'item_group', 'item_category']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Drop unnecessary columns
df.drop(['date', 'address'], axis=1, inplace=True)

# Split data into features and target
X = df[['item_code', 'month', 'premise_type', 'district']] 
y = df['price']

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize models
models = {
    'Random Forest': RandomForestRegressor(random_state=42),
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(random_state=42),
    'SVM': SVR()
}

# Train and evaluate models
results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results.append({
        'Model': name,
        'MAE': mean_absolute_error(y_test, y_pred),
        'MSE': mean_squared_error(y_test, y_pred)
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Visualization: MAE and MSE using Plotly
st.subheader("Model Evaluation by Graph")

# Combined MAE and MSE Visualization
fig = go.Figure()

# Add MAE trace
fig.add_trace(go.Bar(
    x=results_df['Model'],
    y=results_df['MAE'],
    name='MAE',
    marker_color='blue'
))

# Add MSE trace
fig.add_trace(go.Bar(
    x=results_df['Model'],
    y=results_df['MSE'],
    name='MSE',
    marker_color='orange'
))

# Update layout for the combined graph
fig.update_layout(
    title="Model Evaluation: MAE and MSE",
    xaxis_title="Model",
    yaxis_title="Error Value",
    barmode='group',
    legend_title="Metrics",
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

if st.checkbox("Show feature importance for models"):
    # Dropdown for model selection
    selected_model = st.selectbox(
        "Select a model to display feature importance:",
        ['Random Forest', 'Decision Tree', 'Linear Regression', 'SVM']
    )

    # Define feature names
    feature_names = ['item_code', 'month', 'premise_type', 'district']

    # Feature importance logic for each model
if st.checkbox("Show feature importance for models"):
    # Dropdown for model selection
    selected_model = st.selectbox(
        "Select a model to display feature importance:",
        ['Random Forest', 'Decision Tree']
    )

    # Check if the selected model supports feature importance
    if selected_model in ['Random Forest', 'Decision Tree']:
        model = models[selected_model]  # Fetch the trained model
        feature_importances = model.feature_importances_  # Get feature importance
        feature_names = ['item_code', 'month', 'premise_type', 'district']

        # Plotly bar chart for feature importance
        fig_features = px.bar(
            x=feature_importances,
            y=feature_names,
            orientation='h',
            title=f'Feature Importance ({selected_model})',
            labels={'x': 'Importance', 'y': 'Feature'}
        )

        # Update layout for better aesthetics
        fig_features.update_layout(
            xaxis_title="Importance",
            yaxis_title="Feature",
            template="plotly_white"
        )

        # Display the chart
        st.plotly_chart(fig_features, use_container_width=True)
    else:
        st.write(f"{selected_model} does not support feature importance.")



