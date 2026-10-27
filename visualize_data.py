
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("data/bnpl_customers_clean.csv")

# Create one figure with three charts
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Chart 1: Default distribution
df["default"].value_counts().sort_index().plot(
    kind="bar", ax=axes[0]
)
axes[0].set_title("Default Distribution")
axes[0].set_xlabel("Default (0 = No, 1 = Yes)")
axes[0].set_ylabel("Number of Customers")
axes[0].tick_params(axis="x", rotation=0)

# Chart 2: Monthly income
df["monthly_income"].plot(
    kind="hist", bins=5, edgecolor="black", ax=axes[1]
)
axes[1].set_title("Monthly Income Distribution")
axes[1].set_xlabel("Monthly Income (RM)")
axes[1].set_ylabel("Number of Customers")

# Chart 3: Existing debt by default status
df.boxplot(column="existing_debt", by="default", ax=axes[2])
axes[2].set_title("Existing Debt by Default")
axes[2].set_xlabel("Default (0 = No, 1 = Yes)")
axes[2].set_ylabel("Existing Debt (RM)")

plt.suptitle("FinRisk - BNPL Customer Analysis")
plt.tight_layout()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("data/bnpl_customers_clean.csv")

# Create one figure with three charts
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Chart 1: Default distribution
df["default"].value_counts().sort_index().plot(
    kind="bar", ax=axes[0]
)
axes[0].set_title("Default Distribution")
axes[0].set_xlabel("Default (0 = No, 1 = Yes)")
axes[0].set_ylabel("Number of Customers")
axes[0].tick_params(axis="x", rotation=0)

# Chart 2: Monthly income
df["monthly_income"].plot(
    kind="hist", bins=5, edgecolor="black", ax=axes[1]
)
axes[1].set_title("Monthly Income Distribution")
axes[1].set_xlabel("Monthly Income (RM)")
axes[1].set_ylabel("Number of Customers")

# Chart 3: Existing debt by default status
df.boxplot(column="existing_debt", by="default", ax=axes[2])
axes[2].set_title("Existing Debt by Default")
axes[2].set_xlabel("Default (0 = No, 1 = Yes)")
axes[2].set_ylabel("Existing Debt (RM)")

plt.suptitle("FinRisk - BNPL Customer Analysis")
plt.tight_layout()
plt.show()



