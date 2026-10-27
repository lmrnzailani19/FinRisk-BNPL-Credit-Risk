
import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# 1. Load the dataset
file_path = "data/Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv.xlsx"
df = pd.read_excel(file_path)

# 2. Define the target
target = "default_flag"


# Candidate features for BNPL approval-time prediction
# These are provisional until their timing is verified.

numeric_features = [
    "age",
    "monthly_income",
    "credit_score",
    "purchase_amount",
    "bnpl_installments"
]

categorical_features = [
    "employment_type",
    "product_category"
]


features = numeric_features + categorical_features

X = df[features]
y = df[target]


# 4. Split into training, validation, and testing data
X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.40,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=42,
    stratify=y_temp
)


# 5. Prepare numeric and categorical features
numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

# 6. Create and train the model
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)


# 7. Evaluate candidate thresholds on validation data
y_val_prob = model.predict_proba(X_val)[:, 1]

print("\n--- DATA SPLIT ---")
print("Training records:", len(X_train))
print("Validation records:", len(X_val))
print("Testing records:", len(X_test))

print("\n--- VALIDATION THRESHOLD EXPERIMENT ---")

for threshold in [0.50, 0.40, 0.30]:
    val_predictions = (y_val_prob >= threshold).astype(int)

    print(f"\nThreshold: {threshold:.2f}")
    print(classification_report(
        y_val,
        val_predictions,
        zero_division=0
    ))
    print("Confusion matrix:")
    print(confusion_matrix(y_val, val_predictions))

# 8. Final evaluation on untouched test data
# Use 0.40 provisionally; select the final threshold
# based on validation results and your project objective.
selected_threshold = 0.40

y_test_prob = model.predict_proba(X_test)[:, 1]
y_test_pred = (y_test_prob >= selected_threshold).astype(int)

print(f"\n--- FINAL TEST RESULTS (threshold={selected_threshold:.2f}) ---")
print("Accuracy:", round(accuracy_score(y_test, y_test_pred), 4))

print("\n--- CLASSIFICATION REPORT ---")
print(classification_report(
    y_test,
    y_test_pred,
    zero_division=0
))

print("\n--- CONFUSION MATRIX ---")
print(confusion_matrix(y_test, y_test_pred))

print("\n--- ROC-AUC SCORE ---")
print(round(roc_auc_score(y_test, y_test_prob), 4))

# 9. Dummy baseline benchmark on the test set
from sklearn.dummy import DummyClassifier

dummy_model = DummyClassifier(strategy="most_frequent")
dummy_model.fit(X_train, y_train)
dummy_predictions = dummy_model.predict(X_test)

print("\n--- DUMMY BASELINE ---")
print("Accuracy:", round(
    accuracy_score(y_test, dummy_predictions), 4
))

# 10. Save the trained model
model_dir = Path("models")
model_dir.mkdir(parents=True, exist_ok=True)

model_path = model_dir / "finrisk_model.joblib"
joblib.dump(model, model_path)

print(f"\nTrained model saved to: {model_path.resolve()}")