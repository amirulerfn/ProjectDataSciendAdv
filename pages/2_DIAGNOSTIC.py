import streamlit as st
import pandas as pd
import plotly.express as px

# Load the datasets
income_state = pd.read_csv('hh_income_state.csv')
population_state = pd.read_csv('population_state.csv')

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

import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit app title
st.title("Population of Kelantan by District Over Time 📊")

# Function to load and preprocess the dataset
@st.cache_data
def load_data():
    try:
        # Load the population data
        population_district = pd.read_csv('population_district.csv')

        # Convert the 'date' column to datetime objects
        population_district['date'] = pd.to_datetime(population_district['date'])

        # Filter data for Kelantan
        kelantan_population = population_district[population_district['state'] == 'Kelantan']

        # Group data by district and year, then sum the population
        kelantan_population_by_district = kelantan_population.groupby(['district', kelantan_population['date'].dt.year])['population'].sum().reset_index()
        kelantan_population_by_district.columns = ['district', 'year', 'population']  # Renaming columns for clarity
        return kelantan_population_by_district
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load the data
df = load_data()

if df is not None:
    # Create the Plotly bar chart
    fig = px.bar(df, 
                 x='district', 
                 y='population', 
                 color='year', 
                 labels={'district': 'District', 'population': 'Population', 'year': 'Year'},
                 title="Population of Kelantan by District Over Time",
                 barmode='group',  # Group bars by year
                 color_discrete_sequence=px.colors.qualitative.Set3)

    # Rotate x-axis labels for better readability
    fig.update_xaxes(tickangle=45)

    # Show the Plotly chart in Streamlit
    st.plotly_chart(fig)

else:
    st.error("Unable to load data. Please check the file path or data format.")

