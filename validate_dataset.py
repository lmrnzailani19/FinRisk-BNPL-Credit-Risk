
import pandas as pd

file_path = "data/Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv.xlsx"
df = pd.read_excel(file_path)

print("\n--- DATASET VALIDATION ---")

# 1. Check customer ID uniqueness
print("\nUnique user IDs:", df["user_id"].nunique())
print("Total rows:", len(df))
print("Repeated user IDs:", df["user_id"].duplicated().sum())

# 2. Check target values and class balance
print("\nDefault flag values:")
print(df["default_flag"].value_counts(dropna=False))

# 3. Check missing values
print("\nTotal missing cells:", df.isna().sum().sum())

# 4. Check transaction dates
print("\nEarliest transaction:", df["transaction_date"].min())
print("Latest transaction:", df["transaction_date"].max())

# 5. Check whether default status varies within repeated IDs
print("\nDistinct default labels per user:")
labels_per_user = df.groupby("user_id")["default_flag"].nunique()
print(labels_per_user.value_counts().sort_index())

# 6. Inspect repayment-related columns by default status
print("\nRepayment information by default status:")
print(
    df.groupby("default_flag")[
        ["repayment_delay_days", "missed_payments"]
    ].agg(["mean", "min", "max"])
)

# 7. Check risk-score and segment relationships
print("\nDefault rate by customer segment:")
print(df.groupby("customer_segment")["default_flag"].mean())

print("\nValidation checks complete.")


print("\n--- Sample Dataset Records ---")
print(df.head(10).to_string())

print("\n--- Risk Score by Default Flag ---")
print(df.groupby("default_flag")["risk_score"].describe())

print("\n--- Customer Segment by Default Flag ---")
print(pd.crosstab(
    df["customer_segment"],
    df["default_flag"],
    normalize="index"
).round(3))


print("\n--- Dataset File Information ---")
print("File:", "Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv.xlsx")

print("\n--- Check Risk Score and Segment Patterns ---")
print(df[[
    "default_flag",
    "risk_score",
    "customer_segment"
]].sort_values(
    "risk_score"
).head(15).to_string(index=False))

print("\n--- Highest Risk Scores ---")
print(df[[
    "default_flag",
    "risk_score",
    "customer_segment"
]].sort_values(
    "risk_score",
    ascending=False
).head(15).to_string(index=False))


print("\n--- Risk Score by Default Status ---")

print(
    df.groupby("default_flag")["risk_score"]
    .agg(["mean", "min", "max"])
    .round(2)
)

print("\n--- Customer Segment Counts by Default Status ---")

print(
    pd.crosstab(
        df["customer_segment"],
        df["default_flag"]
    )
)
