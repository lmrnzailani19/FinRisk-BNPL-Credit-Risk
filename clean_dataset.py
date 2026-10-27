
import pandas as pd

# Load the original dataset
df = pd.read_csv("data/bnpl_customers.csv")

print("Original dataset shape:", df.shape)

# Check for missing values
print("\nMissing values before cleaning:")
print(df.isnull().sum())

# Count duplicate rows
print("\nDuplicate rows:", df.duplicated().sum())

# Remove duplicate rows
df = df.drop_duplicates()

# Check for invalid values
print("\nInvalid values:")
print("Age below 18:", (df["age"] < 18).sum())
print("Income at or below 0:", (df["monthly_income"] <= 0).sum())
print("Negative debt:", (df["existing_debt"] < 0).sum())
print("Invalid default labels:", (~df["default"].isin([0, 1])).sum())

# Save the cleaned dataset
df.to_csv("data/bnpl_customers_clean.csv", index=False)

print("\nCleaned dataset shape:", df.shape)
print("Cleaned dataset saved successfully!")
