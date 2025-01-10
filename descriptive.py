import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Title of the Streamlit app
st.title("Telur Kelantan Data Analysis")

# Try to load the data
try:
    # Load the dataset
    df = pd.read_csv('/content/telur kelantan filtered.csv')

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
except KeyError as e:
    st.error(f"Error: Column '{e}' not found in the CSV file.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
