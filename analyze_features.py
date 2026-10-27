
import pandas as pd

file_path = "data/Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv.xlsx"
df = pd.read_excel(file_path)

# 1. Compare default rates across employment types
print("\n--- DEFAULT RATE BY EMPLOYMENT TYPE ---")
print(df.groupby("employment_type")["default_flag"].mean().sort_values(ascending=False))

# 2. Compare default rates by customer segment
print("\n--- DEFAULT RATE BY CUSTOMER SEGMENT ---")
print(df.groupby("customer_segment")["default_flag"].mean().sort_values(ascending=False))

# 3. Compare risk scores for default and non-default records
print("\n--- RISK SCORE BY DEFAULT STATUS ---")
print(df.groupby("default_flag")["risk_score"].agg(["count", "mean", "min", "max"]))

# 4. Inspect possible predictors
print("\n--- NUMERIC FEATURE CORRELATIONS WITH DEFAULT ---")
numeric_df = df.select_dtypes(include="number")
print(numeric_df.corr(numeric_only=True)["default_flag"].sort_values(ascending=False))

# 5. Check date range
print("\n--- TRANSACTION DATE RANGE ---")
print("Earliest:", df["transaction_date"].min())
print("Latest:", df["transaction_date"].max())
