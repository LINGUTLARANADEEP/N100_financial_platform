import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import run_query

# ==========================================
# Load Data
# ==========================================

st.title("Peer Comparison")

df = run_query("""
SELECT *
FROM financial_ratios
WHERE year = 'Mar 2024'
""")

st.write(f"Companies Loaded: {len(df)}")

st.divider()

# ==========================================
# Company Selection
# ==========================================

companies = sorted(df["company_id"].unique())

col1, col2 = st.columns(2)

with col1:
    company1 = st.selectbox(
        "Company 1",
        companies,
        index=0
    )

with col2:
    company2 = st.selectbox(
        "Company 2",
        companies,
        index=1
    )

# ==========================================
# Selected Company Data
# ==========================================

company1_data = df[df["company_id"] == company1].iloc[0]
company2_data = df[df["company_id"] == company2].iloc[0]

# ==========================================
# Company Comparison Table
# ==========================================

st.divider()

st.subheader("Company Comparison")

comparison = pd.DataFrame({
    "Metric": [
        "ROE (%)",
        "Revenue CAGR (5Y)",
        "Debt to Equity",
        "Interest Coverage",
        "Composite Score"
    ],

    company1: [
        round(company1_data["return_on_equity_pct"], 2),

        round(company1_data["revenue_cagr_5yr"], 2)
        if pd.notna(company1_data["revenue_cagr_5yr"])
        else "N/A",

        round(company1_data["debt_to_equity"], 2),

        round(company1_data["interest_coverage"], 2),

        round(company1_data["composite_quality_score"], 2)
    ],

    company2: [
        round(company2_data["return_on_equity_pct"], 2),

        round(company2_data["revenue_cagr_5yr"], 2)
        if pd.notna(company2_data["revenue_cagr_5yr"])
        else "N/A",

        round(company2_data["debt_to_equity"], 2),

        round(company2_data["interest_coverage"], 2),

        round(company2_data["composite_quality_score"], 2)
    ]
})

st.dataframe(
    comparison,
    use_container_width=True
)

# ==========================================
# Quick Comparison
# ==========================================

st.divider()

st.subheader("Quick Comparison")

left, right = st.columns(2)

with left:

    st.markdown(f"## {company1}")

    st.metric(
        "ROE",
        f"{company1_data['return_on_equity_pct']:.2f}%"
    )

    st.metric(
        "Revenue CAGR",
        f"{company1_data['revenue_cagr_5yr']:.2f}%"
        if pd.notna(company1_data["revenue_cagr_5yr"])
        else "N/A"
    )

    st.metric(
        "Debt / Equity",
        f"{company1_data['debt_to_equity']:.2f}"
    )

    st.metric(
        "Interest Coverage",
        f"{company1_data['interest_coverage']:.2f}"
    )

with right:

    st.markdown(f"## {company2}")

    st.metric(
        "ROE",
        f"{company2_data['return_on_equity_pct']:.2f}%"
    )

    st.metric(
        "Revenue CAGR",
        f"{company2_data['revenue_cagr_5yr']:.2f}%"
        if pd.notna(company2_data["revenue_cagr_5yr"])
        else "N/A"
    )

    st.metric(
        "Debt / Equity",
        f"{company2_data['debt_to_equity']:.2f}"
    )

    st.metric(
        "Interest Coverage",
        f"{company2_data['interest_coverage']:.2f}"
    )
st.divider()

st.subheader("Overall Comparison")

score1 = 0
score2 = 0

# ROE (Higher is better)
if company1_data["return_on_equity_pct"] > company2_data["return_on_equity_pct"]:
    score1 += 1
    roe_winner = company1
else:
    score2 += 1
    roe_winner = company2

# Revenue CAGR (Higher is better)
if pd.notna(company1_data["revenue_cagr_5yr"]) and pd.notna(company2_data["revenue_cagr_5yr"]):
    if company1_data["revenue_cagr_5yr"] > company2_data["revenue_cagr_5yr"]:
        score1 += 1
        cagr_winner = company1
    else:
        score2 += 1
        cagr_winner = company2
else:
    cagr_winner = "N/A"

# Debt to Equity (Lower is better)
if company1_data["debt_to_equity"] < company2_data["debt_to_equity"]:
    score1 += 1
    debt_winner = company1
else:
    score2 += 1
    debt_winner = company2

# Interest Coverage (Higher is better)
if company1_data["interest_coverage"] > company2_data["interest_coverage"]:
    score1 += 1
    interest_winner = company1
else:
    score2 += 1
    interest_winner = company2

st.write(f"🏆 Higher ROE: **{roe_winner}**")
st.write(f"📈 Higher Revenue CAGR: **{cagr_winner}**")
st.write(f"💰 Lower Debt/Equity: **{debt_winner}**")
st.write(f"🏦 Higher Interest Coverage: **{interest_winner}**")

if score1 > score2:
    st.success(f"Overall Winner: **{company1}** ({score1}-{score2})")
elif score2 > score1:
    st.success(f"Overall Winner: **{company2}** ({score2}-{score1})")
else:
    st.info("Overall Result: Tie")
    
# ==========================================
# Visual Comparison
# ==========================================

st.divider()

st.subheader("Visual Comparison")

# ---------- Row 1 ----------
col1, col2 = st.columns(2)

# ROE
with col1:

    roe_df = pd.DataFrame({
        "Company": [company1, company2],
        "Value": [
            company1_data["return_on_equity_pct"],
            company2_data["return_on_equity_pct"]
        ]
    })

    fig = px.bar(
        roe_df,
        x="Company",
        y="Value",
        color="Company",
        title="Return on Equity (ROE)"
    )

    st.plotly_chart(fig, use_container_width=True)

# Revenue CAGR
with col2:

    cagr_df = pd.DataFrame({
        "Company": [company1, company2],
        "Value": [
            company1_data["revenue_cagr_5yr"] if pd.notna(company1_data["revenue_cagr_5yr"]) else 0,
            company2_data["revenue_cagr_5yr"] if pd.notna(company2_data["revenue_cagr_5yr"]) else 0
        ]
    })

    fig = px.bar(
        cagr_df,
        x="Company",
        y="Value",
        color="Company",
        title="Revenue CAGR (5Y)"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------- Row 2 ----------
col3, col4 = st.columns(2)

# Debt to Equity
with col3:

    debt_df = pd.DataFrame({
        "Company": [company1, company2],
        "Value": [
            company1_data["debt_to_equity"],
            company2_data["debt_to_equity"]
        ]
    })

    fig = px.bar(
        debt_df,
        x="Company",
        y="Value",
        color="Company",
        title="Debt to Equity"
    )

    st.plotly_chart(fig, use_container_width=True)

# Interest Coverage
with col4:

    interest_df = pd.DataFrame({
        "Company": [company1, company2],
        "Value": [
            company1_data["interest_coverage"],
            company2_data["interest_coverage"]
        ]
    })

    fig = px.bar(
        interest_df,
        x="Company",
        y="Value",
        color="Company",
        title="Interest Coverage"
    )

    st.plotly_chart(fig, use_container_width=True)