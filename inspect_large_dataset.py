
import pandas as pd

# Load the new Kaggle dataset (Excel format)
file_path = "data/Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv.xlsx"

df = pd.read_excel(file_path)

# 1. Display the first five rows
print("\n--- FIRST 5 ROWS ---")
print(df.head())

# 2. Check the dataset size
print("\n--- DATASET SHAPE ---")
print(df.shape)

# 3. Display all column names
print("\n--- COLUMN NAMES ---")
print(df.columns.tolist())

# 4. Check data types and non-missing values
print("\n--- DATASET INFORMATION ---")
df.info()

# 5. Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())
