
import pandas as pd

# Load the larger BNPL dataset
file_path = "data/Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv.xlsx"
df = pd.read_excel(file_path)

# 1. Check the target column
print("\n--- DEFAULT FLAG VALUES ---")
print(df["default_flag"].value_counts().sort_index())

# 2. Check the proportion of each class
print("\n--- DEFAULT FLAG PROPORTIONS ---")
print(df["default_flag"].value_counts(normalize=True).sort_index() * 100)

# 3. Check for unexpected target values
print("\n--- UNIQUE DEFAULT FLAG VALUES ---")
print(sorted(df["default_flag"].unique()))

# 4. Check possible duplicate customer IDs
print("\n--- DUPLICATE USER IDs ---")
print(df["user_id"].duplicated().sum())

# 5. Check the risk score and customer segment
print("\n--- RISK SCORE SUMMARY ---")
print(df["risk_score"].describe())

print("\n--- CUSTOMER SEGMENT COUNTS ---")
print(df["customer_segment"].value_counts())
