import pandas as pd
import streamlit as st
import plotly.express as px  # For interactive visualizations
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the Streamlit app
st.title("Egg Grade Analysis 📊")

# Function to load and preprocess the dataset
@st.cache_data
def load_data():
    try:
        # Load the CSV file
        df = pd.read_csv("telur kelantan filtered.csv")
        
        # Convert date to datetime and extract month and year
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        
        # Replace item codes with grades
        df['item_code'] = df['item_code'].replace({118: 'A', 119: 'B', 120: 'C'})
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Function to plot egg counts by month
def plot_egg_counts(df):
    # Group data by month and item_code, then count
    monthly_egg_counts = df.groupby(['month', 'item_code'])['item_code'].count().reset_index(name='count')

    # Sort the data by month
    monthly_egg_counts = monthly_egg_counts.sort_values(by='month')

    # Create the bar plot
    plt.figure(figsize=(12, 6))
    sns.barplot(x='month', y='count', hue='item_code', data=monthly_egg_counts, dodge=True)
    plt.title('Number of Eggs per Month by Grade', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(
        ticks=range(0, 12),  # Ensure ticks align with actual data indices
        labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        fontsize=12, fontweight='light'
    )
    plt.legend(title='Egg Grade', fontsize=12)
    plt.tight_layout()

    # Display the plot with Streamlit's interactive features
    st.pyplot(plt)

# Load the data
df = load_data()

if df is not None:
    # Visualization 1: Distribution of premises per district with Plotly
    district_premise_counts = df.groupby('district')['premise'].count().reset_index()
    district_premise_counts.rename(columns={'premise': 'premise_count'}, inplace=True)
    fig_district_premise = px.bar(
        district_premise_counts, 
        x='district', 
        y='premise_count', 
        title="Distribution of Premises per District",
        labels={'district': 'District', 'premise_count': 'Number of Premises'},
        color='district',  # Optional: color bars by district for better visibility
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_district_premise)

    # Visualization 2: Item counts per premise
    grouped = df.groupby(['premise', 'item_code']).size().reset_index(name='count')
    fig_items = px.bar(
        grouped, 
        x='premise', 
        y='count', 
        color='item_code', 
        title="Item Counts per Premise (by Grade)",
        labels={'count': 'Count', 'premise': 'Premise', 'item_code': 'Egg Grade'},
        barmode='group'
    )
    st.plotly_chart(fig_items)

    # Visualization 3: Grade distribution with a pie chart
    st.subheader("Distribution of Egg Grades")
    grade_counts = df['item_code'].value_counts().reset_index()
    grade_counts.columns = ['Grade', 'Count']
    fig_grade = px.pie(
        grade_counts, 
        values='Count', 
        names='Grade', 
        title="Egg Grade Distribution", 
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_grade)

    # Visualization 4: Item counts per district
    grouped_district = df.groupby(['district', 'item_code'])['item_code'].count().reset_index(name='count')
    fig_district = px.bar(
        grouped_district,
        x='district',
        y='count',
        color='item_code',
        title="Item Grade Counts per District",
        labels={'district': 'District', 'count': 'Count', 'item_code': 'Egg Grade'},
        barmode='stack'
    )
    st.plotly_chart(fig_district)

    # Visualization 5: Monthly trends of egg counts
   # Visualization 5: Monthly trends of egg counts (Bar chart version)
    monthly_counts = df.groupby(['month', 'item_code'])['item_code'].count().reset_index(name='count')
    
    # Create the bar chart
    fig_monthly = px.bar(
        monthly_counts, 
        x='month', 
        y='count', 
        color='item_code', 
        title="Monthly Trends of Egg Counts by Grade",
        labels={'month': 'Month', 'count': 'Count', 'item_code': 'Egg Grade'},
        barmode='group',  # Grouped bars for each month and egg grade
        color_discrete_sequence=px.colors.qualitative.Set3  # Color scheme for the grades
    )
    
    # Display the plot
    st.plotly_chart(fig_monthly)


    # Visualization 6: Average price per grade by premise
    avg_price = df.groupby(['premise', 'item_code'])['price'].mean().reset_index()
    fig_avg_price = px.bar(
        avg_price, 
        x='premise', 
        y='price', 
        color='item_code', 
        title="Average Price per Grade at Each Premise",
        labels={'premise': 'Premise', 'price': 'Average Price', 'item_code': 'Egg Grade'},
        barmode='group'
    )
    st.plotly_chart(fig_avg_price)

    # Extra Visualization: Boxplot for price distribution by grade
    st.subheader("Price Distribution by Grade")
    fig_box = px.box(
        df, 
        x='item_code', 
        y='price', 
        color='item_code', 
        title="Price Distribution per Grade",
        labels={'item_code': 'Egg Grade', 'price': 'Price'},
    )
    st.plotly_chart(fig_box)

    # Call the function to plot egg counts by month using Seaborn
    plot_egg_counts(df)

else:
    st.error("Unable to load data. Please check the file path or data format.")
