import streamlit as st
import pandas as pd

from utils.db import run_query

st.title("Stock Screener")

df = run_query("""
SELECT *
FROM financial_ratios
WHERE year='Mar 2024'
""")

st.write(f"Companies Loaded: {len(df)}")

st.divider()

st.subheader("Filters")

# ROE Filter
min_roe = st.slider(
    "Minimum ROE (%)",
    0,
    50,
    15
)

# Revenue CAGR Filter
min_cagr = st.slider(
    "Minimum Revenue CAGR (%)",
    -10,
    50,
    10
)

# Debt to Equity Filter
max_de = st.slider(
    "Maximum Debt to Equity",
    0.0,
    5.0,
    1.0
)

# Interest Coverage Filter
min_ic = st.slider(
    "Minimum Interest Coverage",
    0,
    50,
    5
)

# Apply All Filters
filtered_df = df[
    (df["return_on_equity_pct"] >= min_roe) &
    (df["revenue_cagr_5yr"] >= min_cagr) &
    (df["debt_to_equity"] <= max_de) &
    (df["interest_coverage"] >= min_ic)
]

st.write(f"Matching Companies: {len(filtered_df)}")

st.dataframe(
    filtered_df[
        [
            "company_id",
            "return_on_equity_pct",
            "revenue_cagr_5yr",
            "debt_to_equity",
            "interest_coverage",
            "composite_quality_score"
        ]
    ],
    use_container_width=True
)