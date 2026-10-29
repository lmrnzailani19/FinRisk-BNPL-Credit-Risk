
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the trained FinRisk model
model = joblib.load("models/finrisk_model.joblib")

# 2. Extract the preprocessor and classifier
preprocessor = model.named_steps["preprocessor"]
classifier = model.named_steps["classifier"]

# 3. Get the transformed feature names
feature_names = preprocessor.get_feature_names_out()

# 4. Extract Logistic Regression coefficients
coefficients = classifier.coef_[0]

# 5. Create a DataFrame of feature coefficients
importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Coefficient": coefficients
})

# 6. Sort features by coefficient
importance_df = importance_df.sort_values(
    by="Coefficient",
    ascending=True
)

print("\nFinRisk Model Coefficients:")
print(importance_df.to_string(index=False))

# 7. Plot the coefficients
plt.figure(figsize=(10, 7))

plt.barh(
    importance_df["Feature"],
    importance_df["Coefficient"]
)

plt.axvline(0, linestyle="--")
plt.xlabel("Logistic Regression Coefficient")
plt.ylabel("Feature")
plt.title("FinRisk — Model Explainability")
plt.tight_layout()

# 8. Save the chart
plt.savefig(
    "screenshots/feature_coefficients.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nChart saved to screenshots/feature_coefficients.png")

plt.show()
