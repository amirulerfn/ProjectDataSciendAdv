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

# Convert 'date' column to datetime with error handling
try:
    # Attempt to convert 'date' column with error handling
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y', errors='coerce')

    # Check for any rows where the conversion failed
    invalid_dates = df[df['date'].isna()]
    if not invalid_dates.empty:
        st.warning(f"Warning: {len(invalid_dates)} rows have invalid or missing dates.")
        st.write(invalid_dates)

except Exception as e:
    st.error(f"Error occurred during date conversion: {e}")

# Replace item_code with grades
df['item_code'] = df['item_code'].replace({118: 'A', 119: 'B', 120: 'C'})

# Visualization 1: Item Counts per Premise (with premise instead of premise_code)
grouped = df.groupby(['premise', 'item_code']).size().reset_index(name='jumlah')
result = pd.merge(grouped, df[['premise', 'premise_type', 'district']], on='premise', how='left')
result = result.drop_duplicates(subset=['premise', 'item_code'])

plt.figure(figsize=(12, 6))
sns.barplot(x='premise', y='jumlah', hue='item_code', data=result)
plt.title('Item Counts per Premise')
plt.xlabel('Premise')
plt.ylabel('Jumlah')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Visualization 2: Item Grade Counts per District
grouped_district = df.groupby(['district', 'item_code'])['item_code'].count().reset_index(name='count')

plt.figure(figsize=(12, 6))
sns.barplot(x='district', y='count', hue='item_code', data=grouped_district)
plt.title('Item Grade Counts per District')
plt.xlabel('District')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Visualization 3: Distribution of Egg Grades (Pie Chart)
grade_counts = df['item_code'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Egg Grades')
plt.show()

# Visualization 4: Box plot of 'jumlah' (counts) per district
plt.figure(figsize=(10, 6))
sns.boxplot(x='district', y='jumlah', data=result)
plt.title('Distribution of Item Counts per District')
plt.xlabel('District')
plt.ylabel('Jumlah')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Visualization 5: Average Price per Grade at Each Premise
grouped_price = df.groupby(['premise', 'item_code'])['price'].mean().reset_index()

plt.figure(figsize=(16, 8))
sns.barplot(x='premise', y='price', hue='item_code', data=grouped_price)
plt.title('Average Egg Price per Grade at Each Premise')
plt.xlabel('Premise')
plt.ylabel('Average Price')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Visualization 6: Number of Eggs per Month by Grade
df['month'] = df['date'].dt.month
monthly_egg_counts = df.groupby(['month', 'item_code'])['item_code'].count().reset_index(name='count')
monthly_egg_counts = monthly_egg_counts.sort_values(by='month')

plt.figure(figsize=(12, 6))
sns.barplot(x='month', y='count', hue='item_code', data=monthly_egg_counts, dodge=True)
plt.title('Number of Eggs per Month by Grade')
plt.xlabel('Month')
plt.ylabel('Count')
plt.xticks(
    ticks=range(0, 12),
    labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
)
plt.legend(title='Egg Grade')
plt.tight_layout()
plt.show()
