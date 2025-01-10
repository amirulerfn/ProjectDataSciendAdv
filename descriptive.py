import pandas as pd

try:
  df = pd.read_csv(telur kelantan filtered.csv)
  print(df)
except FileNotFoundError:
  print("Error: File not found.")
except pd.errors.ParserError:
  print("Error: Could not parse the file. Please check the file format.")
except Exception as e:
  print(f"An unexpected error occurred: {e}")


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df = pd.read_csv('/content/telur kelantan filtered.csv')

    # Display the first few rows of the DataFrame
    print("First few rows of the DataFrame:")
    print(df.head())

    # Display basic statistics about the DataFrame
    print("\nSummary statistics:")
    print(df.describe())


    # Total premises
    print("\nTotal premises:", len(df))

    # Premises count
    premise_counts = df.groupby('premise_code').size().reset_index(name='total')
    print("\nPremise Counts:")
    print(premise_counts)

    # Visualize premise counts
    plt.figure(figsize=(10, 6))
    sns.countplot(x='premise_code', data=df)
    plt.title('Distribution of Premises')
    plt.xlabel('Premise Code')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()
    plt.show()

    # Grouped data
    grouped = df.groupby(['premise_code', 'item_code']).size().reset_index(name='jumlah')
    result = pd.merge(grouped, df[['premise_code', 'premise', 'premise_type', 'district']], on='premise_code', how='left')
    result = result.drop_duplicates(subset=['premise_code', 'item_code'])
    print("\nGrouped data with premise details:")
    print(result)


    # Visualization of item counts per premise
    plt.figure(figsize=(12, 6))
    sns.barplot(x='premise_code', y='jumlah', hue='item_code', data=result)
    plt.title('Item Counts per Premise')
    plt.xlabel('Premise Code')
    plt.ylabel('Jumlah')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


except FileNotFoundError:
    print("Error: File not found.")
except pd.errors.ParserError:
    print("Error: Could not parse the file. Please check the file format.")
except KeyError as e:
    print(f"Error: Column '{e}' not found in the CSV file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

