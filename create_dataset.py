# Step 1: dataset
import pandas as pd

data = {
    "customer_id": ["C001", "C002", "C003", "C004", "C005",
                    "C006", "C007", "C008", "C009", "C010"],
    "age": [22, 35, 28, 45, 24, 39, 31, 26, 50, 29],
    "monthly_income": [2500, 6000, 3500, 8000, 2200,
                       5500, 4200, 3000, 9000, 3800],
    "monthly_spending": [1800, 3000, 2500, 4000, 1900,
                         2800, 3200, 2100, 4500, 2600],
    "existing_debt": [500, 1000, 2500, 1500, 1200,
                      800, 2000, 1800, 1000, 2200],
    "late_payments": [0, 0, 2, 0, 3, 0, 1, 2, 0, 1],
    "transaction_frequency": [12, 25, 18, 30, 10,
                              28, 22, 15, 35, 20],
    "average_purchase": [100, 250, 150, 300, 80,
                         200, 180, 120, 400, 160],
    "default": [0, 0, 1, 0, 1, 0, 0, 1, 0, 0]
}

df = pd.DataFrame(data)

df.to_csv("data/bnpl_customers.csv", index=False)

print("Dataset created successfully!")
print(df.head())
print("Dataset shape:", df.shape)