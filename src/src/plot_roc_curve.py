
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score

# 1. Load the dataset
data_path = "data/Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv.xlsx"
df = pd.read_excel(data_path)

# 2. Select the model features
numeric_features = [
    "age",
    "monthly_income",
    "credit_score",
    "purchase_amount",
    "bnpl_installments",
]

categorical_features = [
    "employment_type",
    "product_category",
]

features = numeric_features + categorical_features
X = df[features]
y = df["default_flag"]

# 3. Recreate the train/validation/test split
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y,
    test_size=0.40,
    random_state=42,
    stratify=y,
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp,
)

# 4. Load the trained model
model = joblib.load("models/finrisk_model.joblib")

# 5. Predict default probabilities
y_prob = model.predict_proba(X_test)[:, 1]

# 6. Calculate ROC curve and AUC
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
auc_score = roc_auc_score(y_test, y_prob)

# 7. Draw the ROC curve
plt.figure(figsize=(8, 6))
plt.plot(
    fpr, tpr,
    label=f"FinRisk Logistic Regression (AUC = {auc_score:.3f})",
    linewidth=2,
)
plt.plot([0, 1], [0, 1], "--", label="Random classifier")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate (Recall)")
plt.title("FinRisk — ROC Curve")
plt.legend(loc="lower right")
plt.grid(alpha=0.3)
plt.tight_layout()

# Save the chart
plt.savefig("roc_curve.png", dpi=300, bbox_inches="tight")

# Print results before opening the chart
print(f"Test-set ROC-AUC: {auc_score:.4f}", flush=True)
print("ROC curve saved as roc_curve.png", flush=True)

# Display the chart
plt.show()
