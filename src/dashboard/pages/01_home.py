import streamlit as st

st.set_page_config(layout="wide")

st.write("HOME PAGE LOADED")

import plotly.express as px

from utils.db import run_query


st.title("🏠 Home Dashboard")

# -----------------------------
# Load Latest Year Data
# -----------------------------
df = run_query("""
SELECT *
FROM financial_ratios
WHERE year='Mar 2024'
""")

sector_df = run_query("""
SELECT *
FROM sectors
""")

df = df.merge(
    sector_df,
    on="company_id",
    how="left"
)
# -----------------------------
# DEBUG
# -----------------------------

print("\n========== ROE Statistics ==========")
print(df["return_on_equity_pct"].describe())

print("\n========== Top 10 ROE Companies ==========")
print(
    df.sort_values(
        "return_on_equity_pct",
        ascending=False
    )[["company_id", "return_on_equity_pct"]].head(10)
)

print("\n========== Revenue CAGR Statistics ==========")
print(df["revenue_cagr_5yr"].describe())

print("\n========== Missing Revenue CAGR ==========")
print(df["revenue_cagr_5yr"].isna().sum())

print("\n========== Composite Score Statistics ==========")
print(df["composite_quality_score"].describe())

# -----------------------------
# KPI Cards
# -----------------------------
st.subheader("Key Performance Indicators")

c1, c2, c3 = st.columns(3)

c4, c5, c6 = st.columns(3)

with c1:
    st.metric(
        "Average ROE",
        f"{df['return_on_equity_pct'].mean():.2f}%"
    )

with c2:
    st.metric(
        "Median D/E",
        f"{df['debt_to_equity'].median():.2f}"
    )

with c3:
    st.metric(
        "Median Revenue CAGR",
        f"{df['revenue_cagr_5yr'].median():.2f}%"
    )

with c4:
    st.metric(
        "Companies",
        len(df)
    )

with c5:
    st.metric(
        "Debt Free",
        (df["debt_to_equity"] <= 0).sum()
    )

with c6:
    st.metric(
        "Average Composite Score",
        f"{df['composite_quality_score'].mean():.1f}"
    )

# -----------------------------
# Sector Distribution
# -----------------------------
st.divider()

st.subheader("Sector Distribution")

sector_counts = (
    sector_df
    .groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_counts,
    names="broad_sector",
    values="Companies",
    hole=0.5,
    title="Companies by Sector"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Top Companies
# -----------------------------
st.divider()

st.subheader("Top 5 Companies")

top5 = (
    df[
        [
            "company_id",
            "composite_quality_score",
            "return_on_equity_pct",
            "revenue_cagr_5yr"
        ]
    ]
    .sort_values(
        "composite_quality_score",
        ascending=False
    )
    .head(5)
)

st.dataframe(
    top5,
    use_container_width=True
)