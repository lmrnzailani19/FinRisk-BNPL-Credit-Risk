
import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("data/bnpl_customers_clean.csv")

# 1. General information
print("DATASET OVERVIEW")
print("Number of customers:", df.shape[0])
print("Number of columns:", df.shape[1])

# 2. Average monthly income
print("\nAVERAGE MONTHLY INCOME")
print(df["monthly_income"].mean())

# 3. Average existing debt
print("\nAVERAGE EXISTING DEBT")
print(df["existing_debt"].mean())

# 4. Total late payments
print("\nTOTAL LATE PAYMENTS")
print(df["late_payments"].sum())

# 5. Count customers by default status
print("\nDEFAULT DISTRIBUTION")
print(df["default"].value_counts())

# 6. Compare customers by default status
print("\nAVERAGE FINANCIAL DETAILS BY DEFAULT STATUS")
print(
    df.groupby("default")[
        ["monthly_income", "existing_debt", "late_payments"]
    ].mean()
)
