
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --------------------------------------------------
# FinRisk: BNPL Credit Risk Assessment Dashboard
# --------------------------------------------------

st.set_page_config(
    page_title="FinRisk | BNPL Credit Risk",
    page_icon="📊",
    layout="wide",
)

PROJECT_DIR = Path(__file__).resolve().parent
DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "Buy_Now_Pay_Later_BNPL_CreditRisk_Dataset.csv.xlsx"
)

MODEL_PATH = PROJECT_DIR / "models" / "finrisk_model.joblib"

st.title("FinRisk")
st.subheader("AI-Powered BNPL Credit Risk Assessment")
st.caption(
    "Educational portfolio prototype — not for real lending decisions."
)

@st.cache_data
def load_data(path):
    return pd.read_excel(path)

if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

df = load_data(DATA_PATH)
@st.cache_resource
def load_model(path):
    return joblib.load(path)

if not MODEL_PATH.exists():
    st.error("Trained model not found. Run python train_model.py first.")
    st.stop()

model = load_model(MODEL_PATH)

required_columns = [
    "default_flag",
    "age",
    "monthly_income",
    "credit_score",
    "purchase_amount",
    "bnpl_installments",
    "employment_type",
    "product_category",
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Dataset is missing columns: {missing_columns}")
    st.stop()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Dashboard Controls")

view = st.sidebar.radio(
    "Choose a view",
    ["Overview", "Explore Data", "Risk Assessment"],
)

st.sidebar.caption(
    "The dataset's default_flag is the recorded outcome, "
    "not a guarantee of future repayment."
)

# --------------------------------------------------
# Overview
# --------------------------------------------------

if view == "Overview":
    st.header("Portfolio Overview")

    total_customers = len(df)
    default_rate = df["default_flag"].mean() * 100
    avg_income = df["monthly_income"].mean()
    avg_purchase = df["purchase_amount"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Records", f"{total_customers:,}")
    c2.metric("Recorded Default Rate", f"{default_rate:.1f}%")
    c3.metric("Average Monthly Income", f"RM {avg_income:,.0f}")
    c4.metric("Average Purchase", f"RM {avg_purchase:,.2f}")

    st.info(
        "These are descriptive statistics from the supplied dataset. "
        "They do not establish that the data represents real customers."
    )

    left, right = st.columns(2)

    with left:
        st.subheader("Recorded Repayment Outcomes")

        outcome_counts = (
            df["default_flag"]
            .map({0: "Paid on time", 1: "Defaulted"})
            .fillna("Other")
            .value_counts()
        )

        fig, ax = plt.subplots()
        outcome_counts.plot(kind="bar", ax=ax)
        ax.set_xlabel("Recorded outcome")
        ax.set_ylabel("Number of records")
        ax.tick_params(axis="x", rotation=0)
        st.pyplot(fig)
        plt.close(fig)

    with right:
        st.subheader("Default Rate by Employment Type")

        employment_rate = (
            df.groupby("employment_type")["default_flag"]
            .mean()
            .mul(100)
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots()
        employment_rate.plot(kind="bar", ax=ax)
        ax.set_xlabel("Employment type")
        ax.set_ylabel("Recorded default rate (%)")
        ax.tick_params(axis="x", rotation=30)
        st.pyplot(fig)
        plt.close(fig)

# --------------------------------------------------
# Explore Data
# --------------------------------------------------

elif view == "Explore Data":
    st.header("Explore the Dataset")

    st.write("Inspect records and filter the dataset.")

    search_columns = [
        col for col in
        ["employment_type", "product_category", "location"]
        if col in df.columns
    ]

    filtered = df.copy()

    for col in search_columns:
        choices = sorted(
            filtered[col].dropna().astype(str).unique().tolist()
        )
        selected = st.multiselect(
            f"Filter by {col.replace('_', ' ').title()}",
            choices,
            default=[],
        )

        if selected:
            filtered = filtered[
                filtered[col].astype(str).isin(selected)
            ]

    st.metric("Filtered Records", f"{len(filtered):,}")
    st.dataframe(filtered.head(500), use_container_width=True)

    st.caption("Showing at most 500 rows for easier browsing.")

    st.subheader("Numeric Summary")
    st.dataframe(
        filtered.select_dtypes(include="number").describe().T,
        use_container_width=True,
    )

    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered data as CSV",
        data=csv_data,
        file_name="finrisk_filtered_data.csv",
        mime="text/csv",
    )


# --------------------------------------------------
# Risk Assessment
# --------------------------------------------------

else:
    st.header("BNPL Default Risk Assessment")

    st.warning(
        "Educational prototype only. Predictions are estimates from "
        "a dataset whose target-generation process has not been fully "
        "verified. Do not use for real lending decisions."
    )

    with st.form("customer_inputs"):
        age = st.number_input(
            "Age", min_value=18, max_value=100, value=30
        )
        monthly_income = st.number_input(
            "Monthly income (RM)",
            min_value=0.0,
            value=4000.0,
            step=100.0,
        )
        credit_score = st.number_input(
            "Credit score", min_value=0, max_value=1000, value=650
        )
        purchase_amount = st.number_input(
            "Purchase amount (RM)",
            min_value=0.0,
            value=500.0,
            step=50.0,
        )
        bnpl_installments = st.selectbox(
            "BNPL installments", [2, 3, 4, 6, 12]
        )

        employment_options = sorted(
            df["employment_type"].dropna().astype(str).unique()
        )
        employment_type = st.selectbox(
            "Employment type", employment_options
        )

        category_options = sorted(
            df["product_category"].dropna().astype(str).unique()
        )
        product_category = st.selectbox(
            "Product category", category_options
        )

        submitted = st.form_submit_button("Estimate Default Risk")

    if submitted:
        customer = pd.DataFrame([{
            "age": age,
            "monthly_income": monthly_income,
            "credit_score": credit_score,
            "purchase_amount": purchase_amount,
            "bnpl_installments": bnpl_installments,
            "employment_type": employment_type,
            "product_category": product_category,
        }])

        try:
            default_probability = float(
                model.predict_proba(customer)[0, 1]
            )

            st.subheader("Model Estimate")

            st.metric(
                "Estimated Default Probability",
                f"{default_probability:.1%}",
            )

            st.progress(default_probability)

            st.caption(
                "This is the model's estimated probability, not a "
                "verified real-world probability or lending decision."
            )

            st.subheader("Submitted Customer Information")
            st.dataframe(customer, use_container_width=True)

        except Exception as error:
            st.error(f"Prediction failed: {error}")


st.divider()
st.caption(
    "FinRisk is a student portfolio project. "
    "Its results must not be used to approve or reject real customers."
)
