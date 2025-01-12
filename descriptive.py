import pandas as pd
import streamlit as st
import plotly.express as px  # For interactive visualizations
import matplotlib.pyplot as plt
import seaborn as sns

# Title of the Streamlit app
st.title("Descriptive of Eggs In Kelantan 📊")

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

    # Visualization 5: Monthly trends of egg counts (Styled like other graphs)
    monthly_counts = df.groupby(['month', 'item_code'])['item_code'].count().reset_index(name='count')

    # Create a Plotly bar chart for the monthly trends
    fig_monthly = px.bar(
        monthly_counts,
        x='month',
        y='count',
        color='item_code',
        title="Monthly Trends of Egg Counts by Grade",
        labels={'month': 'Month', 'count': 'Count', 'item_code': 'Egg Grade'},
        color_discrete_sequence=px.colors.qualitative.Set3,
        barmode='group'  # This ensures the bars for each grade are grouped
    )

    # Update x-axis labels to show months
    fig_monthly.update_xaxes(
        tickmode='array',
        tickvals=list(range(1, 13)),  # Months from 1 to 12
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    )

    # Update layout for better styling
    fig_monthly.update_layout(
        title_font_size=18,
        title_font_family='Arial',
        title_font_color='white',
        xaxis_title='Month',
        yaxis_title='Count',
        xaxis_title_font_size=14,
        yaxis_title_font_size=14,
        xaxis_title_font_color='white',
        yaxis_title_font_color='white',
        legend_title='Egg Grade',
        legend_title_font_size=12,
        legend_font_size=12,
        plot_bgcolor='black'
    )

    # Display the Plotly chart
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

else:
    st.error("Unable to load data. Please check the file path or data format.")
