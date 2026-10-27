# Step 2: Explore BNPL dataset

import pandas as pd

# Load the BNPL dataset
df = pd.read_csv("data/bnpl_customers.csv")

# Display the first 5 rows
print("FIRST 5 CUSTOMERS:")
print(df.head())

# Check the number of rows and columns
print("\nDATASET SHAPE:")
print(df.shape)

# Check column names and data types
print("\nDATASET INFORMATION:")
df.info()

# Check for missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# Get basic statistical information
print("\nSTATISTICAL SUMMARY:")
print(df.describe())