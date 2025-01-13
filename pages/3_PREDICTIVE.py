import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns  # For enhanced visualizations
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
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    results[name] = {
        'MAE': mean_absolute_error(y_test, y_pred),
        'MSE': mean_squared_error(y_test, y_pred)
    }

# Display results in a table
st.subheader("Model Evaluation Results")
results_df = pd.DataFrame(results).T
st.write(results_df.sort_values(by='MAE', ascending=True))

# Additional Visualization: Feature Importance
if st.checkbox("Show feature importance for Random Forest"):
    rf_model = models['Random Forest']
    feature_importances = rf_model.feature_importances_
    feature_names = ['item_code', 'month', 'premise_type', 'district']

    plt.figure(figsize=(8, 5))
    sns.barplot(x=feature_importances, y=feature_names, palette="coolwarm")
    plt.title('Feature Importance (Random Forest)', fontsize=16)
    plt.xlabel('Importance', fontsize=12)
    plt.ylabel('Feature', fontsize=12)
    plt.tight_layout()
    st.pyplot(plt)

# Sidebar Option for Model Selection
st.sidebar.subheader("Model Selection")
selected_models = st.sidebar.multiselect("Select models to display:", list(models.keys()), default=list(models.keys()))
filtered_results_df = results_df.loc[selected_models]
st.subheader("Filtered Model Results")
st.write(filtered_results_df)
