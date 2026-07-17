import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import run_query

# ==========================================
# Page Title
# ==========================================

st.title("Trend Analysis")

# ==========================================
# Load Historical Data
# ==========================================

df = run_query("""
SELECT *
FROM financial_ratios
""")

st.write(f"Companies Loaded: {df['company_id'].nunique()}")

st.divider()

# ==========================================
# Company Selection
# ==========================================

companies = sorted(df["company_id"].unique())

selected_company = st.selectbox(
    "Select Company",
    companies
)

# ==========================================
# Historical Data
# ==========================================

trend_df = df[df["company_id"] == selected_company].copy()

trend_df["year_num"] = (
    trend_df["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

trend_df = trend_df.sort_values("year_num")

trend_df["interest_coverage"] = trend_df["interest_coverage"].replace(
    [float("inf"), -float("inf")],
    pd.NA
)

latest = trend_df.iloc[-1]

# ==========================================
# Snapshot
# ==========================================

st.divider()

st.subheader("Company Snapshot")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "ROE (%)",
        f"{latest['return_on_equity_pct']:.2f}"
    )

with c2:
    if pd.notna(latest["revenue_cagr_5yr"]):
        st.metric(
            "Revenue CAGR",
            f"{latest['revenue_cagr_5yr']:.2f}%"
        )
    else:
        st.metric(
            "Revenue CAGR",
            "N/A"
        )

with c3:
    st.metric(
        "Debt / Equity",
        f"{latest['debt_to_equity']:.2f}"
    )

with c4:
    if pd.notna(latest["interest_coverage"]):
        st.metric(
            "Interest Coverage",
            f"{latest['interest_coverage']:.2f}"
        )
    else:
        st.metric(
            "Interest Coverage",
            "N/A"
        )

st.divider()

# ==========================================
# ROE Trend
# ==========================================

st.subheader("Return on Equity Trend")

fig = px.line(
    trend_df,
    x="year",
    y="return_on_equity_pct",
    markers=True,
    title="ROE Over Time"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="ROE (%)"
)

st.plotly_chart(fig, width="stretch")

# ==========================================
# Debt to Equity Trend
# ==========================================

st.subheader("Debt to Equity Trend")

fig = px.line(
    trend_df,
    x="year",
    y="debt_to_equity",
    markers=True,
    title="Debt to Equity Over Time"
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Debt / Equity"
)

st.plotly_chart(fig, width="stretch")

# ==========================================
# Interest Coverage Trend
# ==========================================

interest_df = trend_df.dropna(subset=["interest_coverage"])

st.subheader("Interest Coverage Trend")

if len(interest_df) > 1:

    fig = px.line(
        interest_df,
        x="year",
        y="interest_coverage",
        markers=True,
        title="Interest Coverage Over Time"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Interest Coverage"
    )

    st.plotly_chart(fig, width="stretch")

else:

    st.info("No historical Interest Coverage available.")

# ==========================================
# Revenue CAGR Trend
# ==========================================

revenue_df = trend_df.dropna(subset=["revenue_cagr_5yr"])

st.subheader("Revenue CAGR Trend")

if len(revenue_df) > 1:

    fig = px.line(
        revenue_df,
        x="year",
        y="revenue_cagr_5yr",
        markers=True,
        title="Revenue CAGR (5 Years)"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Revenue CAGR (%)"
    )

    st.plotly_chart(fig, width="stretch")

elif len(revenue_df) == 1:

    st.info(
        f"Only one Revenue CAGR value is available ({revenue_df.iloc[0]['revenue_cagr_5yr']:.2f}%). Historical trend cannot be plotted."
    )

else:

    st.warning("Revenue CAGR data is not available.")