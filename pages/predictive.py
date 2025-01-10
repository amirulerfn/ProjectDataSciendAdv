import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Title of the Streamlit app
st.title("Telur Kelantan Price Prediction")

# Load the dataset
df = pd.read_csv("telur kelantan filtered.csv")

# Display the first few rows of the dataset
st.subheader("First few rows of the DataFrame:")
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
X = df.drop(['state','premise_code','item_code'], axis=1)
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
        'MSE': mean_squared_error(y_test, y_pred),
        'R2 Score': r2_score(y_test, y_pred)
    }

# Display results in a table
st.subheader("Model Evaluation Results:")
results_df = pd.DataFrame(results).T
st.write(results_df.sort_values(by='R2 Score', ascending=False))

# Optionally, you can show a bar plot of R2 scores for each model
st.subheader("R2 Scores Visualization:")
plt.figure(figsize=(10, 6))
results_df['R2 Score'].sort_values().plot(kind='bar', color='skyblue')
plt.title('R2 Scores of Different Models')
plt.xlabel('Model')
plt.ylabel('R2 Score')
plt.tight_layout()
st.pyplot(plt)
