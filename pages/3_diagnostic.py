import streamlit as st
import pandas as pd
import plotly.express as px

# Load the datasets
income_state = pd.read_csv('/content/hh_income_state.csv')
population_state = pd.read_csv('/content/population_state.csv')

# Set up the page title and layout
st.set_page_config(page_title="Kelantan Population and Income Insights", layout="wide")

# Title for the app
st.title("📊 Kelantan Population and Income Insights")

# Description of the app
st.markdown("""
    **Welcome to the Kelantan Population & Income Insights Dashboard!**  
    Explore detailed analyses of Kelantan's population changes, ethnic distribution, and income trends over time.  
    Visualize key insights from historical data, and gain valuable information for decision-making.  
""")

# --- Population Over Time ---
st.header("📈 Population of Kelantan Over Time")
# Convert 'date' to datetime in the original DataFrame to avoid warnings
population_state['date'] = pd.to_datetime(population_state['date'], errors='coerce')

# Filter data for Kelantan
kelantan_population = population_state[population_state['state'] == 'Kelantan']

# Plot the population of Kelantan over time using Plotly
fig_population = px.line(kelantan_population, x=kelantan_population['date'].dt.year, y='population',
                         title='Population of Kelantan Over Time', labels={'date': 'Year', 'population': 'Population'})

# Show the plot
st.plotly_chart(fig_population)

# --- Population Ethnicity Over Time ---
st.header("🧑‍🤝‍🧑 Ethnicity Distribution in Kelantan Over Time")
# Group data by ethnicity and year
ethnicity_population = kelantan_population.groupby(['ethnicity', kelantan_population['date'].dt.year])['population'].sum().reset_index()

# Plot the population ethnicity over time using Plotly
fig_ethnicity = px.line(ethnicity_population, x='date', y='population', color='ethnicity',
                        title='Population Ethnicity in Kelantan Over Time', labels={'date': 'Year', 'population': 'Population'})

# Show the plot
st.plotly_chart(fig_ethnicity)

# --- Income Over Time ---
st.header("💵 Mean and Median Income in Kelantan Over Time")
# Convert 'date' column to datetime objects
income_state['date'] = pd.to_datetime(income_state['date'], errors='coerce')

# Filter data for Kelantan
kelantan_income = income_state[income_state['state'] == 'Kelantan']

# Group data by year and calculate mean and median income
kelantan_income_summary = kelantan_income.groupby(kelantan_income['date'].dt.year)[['income_mean', 'income_median']].mean().reset_index()

# Plot the income trends using Plotly
fig_income = px.line(kelantan_income_summary, x='date', y=['income_mean', 'income_median'],
                     title='Mean and Median Income in Kelantan Over Time',
                     labels={'date': 'Year', 'value': 'Income (MYR)', 'variable': 'Income Type'},
                     line_shape='linear')

# Show the plot
st.plotly_chart(fig_income)
