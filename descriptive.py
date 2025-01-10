import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Title of the Streamlit app
st.title("Telur Kelantan Data Analysis")

# Try to load the data
try:
    # Load the dataset
    df = pd.read_csv('telur kelantan filtered.csv')

    # Display the first few rows of the DataFrame
    st.subheader("First few rows of the DataFrame:")
    st.write(df.head())

    # Display basic statistics about the DataFrame
    st.subheader("Summary statistics:")
    st.write(df.describe())

    # Total premises
    st.subheader("Total Premises:")
    st.write(len(df))

    # Premises count
    premise_counts = df.groupby('premise_code').size().reset_index(name='total')
    st.subheader("Premise Counts:")
    st.write(premise_counts)

    # Visualize premise counts using Streamlit's chart
    st.subheader("Distribution of Premises:")
    plt.figure(figsize=(10, 6))
    sns.countplot(x='premise_code', data=df)
    plt.title('Distribution of Premises')
    plt.xlabel('Premise Code')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()
    st.pyplot(plt)

    # Grouped data
    grouped = df.groupby(['premise_code', 'item_code']).size().reset_index(name='jumlah')
    result = pd.merge(grouped, df[['premise_code', 'premise', 'premise_type', 'district']], on='premise_code', how='left')
    result = result.drop_duplicates(subset=['premise_code', 'item_code'])
    st.subheader("Grouped data with premise details:")
    st.write(result)

    # Visualization of item counts per premise using Streamlit's chart
    st.subheader("Item Counts per Premise:")
    plt.figure(figsize=(12, 6))
    sns.barplot(x='premise_code', y='jumlah', hue='item_code', data=result)
    plt.title('Item Counts per Premise')
    plt.xlabel('Premise Code')
    plt.ylabel('Jumlah')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)

except FileNotFoundError:
    st.error("Error: File not found.")
except pd.errors.ParserError:
    st.error("Error: Could not parse the file. Please check the file format.")

# Replace item_code with grades
df['item_code'] = df['item_code'].replace({118: 'A', 119: 'B', 120: 'C'})

# Visualization 1: Item Counts per Premise (with premise instead of premise_code)
grouped = df.groupby(['premise', 'item_code']).size().reset_index(name='jumlah')
result = pd.merge(grouped, df[['premise', 'premise_type', 'district']], on='premise', how='left')
result = result.drop_duplicates(subset=['premise', 'item_code'])

st.subheader("Item Counts per Premise (by Grade):")
plt.figure(figsize=(12, 6))
sns.barplot(x='premise', y='jumlah', hue='item_code', data=result)
plt.title('Item Counts per Premise')
plt.xlabel('Premise')
plt.ylabel('Jumlah')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(plt)

# Visualization 2: Item Grade Counts per District
grouped_district = df.groupby(['district', 'item_code'])['item_code'].count().reset_index(name='count')

st.subheader("Item Grade Counts per District:")
plt.figure(figsize=(12, 6))
sns.barplot(x='district', y='count', hue='item_code', data=grouped_district)
plt.title('Item Grade Counts per District')
plt.xlabel('District')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(plt)

# Visualization 3: Distribution of Egg Grades (Pie Chart)
grade_counts = df['item_code'].value_counts()

st.subheader("Distribution of Egg Grades:")
plt.figure(figsize=(8, 8))
plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Egg Grades')
st.pyplot(plt)

# Visualization 4: Box plot of 'jumlah' (counts) per district
st.subheader("Distribution of Item Counts per District:")
plt.figure(figsize=(10, 6))
sns.boxplot(x='district', y='jumlah', data=result)
plt.title('Distribution of Item Counts per District')
plt.xlabel('District')
plt.ylabel('Jumlah')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(plt)

# Visualization 5: Average Price per Grade at Each Premise
grouped_price = df.groupby(['premise', 'item_code'])['price'].mean().reset_index()

st.subheader("Average Egg Price per Grade at Each Premise:")
plt.figure(figsize=(16, 8))
sns.barplot(x='premise', y='price', hue='item_code', data=grouped_price)
plt.title('Average Egg Price per Grade at Each Premise')
plt.xlabel('Premise')
plt.ylabel('Average Price')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(plt)

# Visualization 6: Number of Eggs per Month by Grade
 # Convert 'date' column to datetime objects
# Convert 'date' column to datetime objects with error handling
# Extract month and year
df = pd.read_csv('telur kelantan filtered.csv')
# Inspect the date column to ensure correct format and identify any issues
st.write("Preview of date column:")
st.write(df['date'].head())  # Display first few rows of the date column
st.write("Unique date values:")
st.write(df['date'].unique())  # Show unique date values
df['date'] = df['date'].str.strip()
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y', errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Replace item_code with grades
df['item_code'] = df['item_code'].replace({118: 'A', 119: 'B', 120: 'C'})

# Group data by month and item_code, then count
monthly_egg_counts = df.groupby(['month', 'item_code'])['item_code'].count().reset_index(name='count')

# Sort the data by month
monthly_egg_counts = monthly_egg_counts.sort_values(by='month')

# Visualization 5: Egg Counts per Month by Grade
st.subheader("Egg Counts per Month by Grade:")
plt.figure(figsize=(16, 8))
sns.barplot(x='month', y='count', hue='item_code', data=monthly_egg_counts, dodge=True)
plt.title('Number of Eggs per Month by Grade')
plt.xlabel('Month')
plt.ylabel('Count')
plt.xticks(
    ticks=range(0, 12),  # Ensure ticks align with actual data indices
    labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
)
plt.legend(title='Egg Grade')
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)







