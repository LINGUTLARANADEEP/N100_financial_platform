import streamlit as st
import plotly.express as px

from utils.db import (
    get_companies,
    get_ratios
)

st.title("Company Profile")

# Load company names
companies = get_companies()["company_id"].tolist()

company = st.selectbox(
    "Select Company",
    companies
)

df = get_ratios(company)

if df.empty:
    st.error("No data found.")
    st.stop()

st.subheader(company)

# ==========================
# Latest Financial Year
# ==========================
latest = df.iloc[-1]

st.subheader("Key Metrics")

c1, c2, c3 = st.columns(3)
c4, c5, c6 = st.columns(3)

with c1:
    st.metric(
        "Revenue CAGR (5Y)",
        f"{latest['revenue_cagr_5yr']:.2f}%"
        if latest["revenue_cagr_5yr"] is not None else "N/A"
    )

with c2:
    st.metric(
        "ROE",
        f"{latest['return_on_equity_pct']:.2f}%"
    )

with c3:
    st.metric(
        "Debt / Equity",
        f"{latest['debt_to_equity']:.2f}"
    )

with c4:
    st.metric(
        "EPS",
        f"{latest['earnings_per_share']:.2f}"
    )

with c5:
    st.metric(
        "Book Value",
        f"{latest['book_value_per_share']:.2f}"
    )

with c6:
    st.metric(
        "Interest Coverage",
        f"{latest['interest_coverage']:.2f}"
    )

st.divider()
st.subheader("Profit & Loss")

pnl_cols = [
    "year",
    "sales",
    "expenses",
    "operating_profit",
    "net_profit",
    "eps"
]

st.dataframe(
    df[pnl_cols],
    use_container_width=True
)

st.subheader("Balance Sheet")

bs_cols = [
    "year",
    "equity_capital",
    "reserves",
    "borrowings",
    "total_assets",
    "total_liabilities"
]

st.dataframe(
    df[bs_cols],
    use_container_width=True
)

st.subheader("Cash Flow")

cf_cols = [
    "year",
    "operating_activity",
    "investing_activity",
    "financing_activity",
    "cash_from_operations_cr",
    "free_cash_flow_cr"
]

st.dataframe(
    df[cf_cols],
    use_container_width=True
)

st.subheader("Financial Ratios")

ratio_cols = [
    "year",
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "dividend_payout_ratio_pct"
]

st.dataframe(
    df[ratio_cols],
    use_container_width=True
)

st.subheader("Revenue & Net Profit Trend")

fig = px.bar(
    df,
    x="year",
    y=["sales", "net_profit"],
    barmode="group",
    title="Revenue and Net Profit (10 Years)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("ROE Trend")

fig = px.line(
    df,
    x="year",
    y="return_on_equity_pct",
    markers=True,
    title="Return on Equity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Debt to Equity Trend")

fig = px.line(
    df,
    x="year",
    y="debt_to_equity",
    markers=True,
    title="Debt to Equity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("Profit Margin Comparison")

fig = px.line(
    df,
    x="year",
    y=[
        "operating_profit_margin_pct",
        "net_profit_margin_pct"
    ],
    markers=True,
    title="Operating Margin vs Net Profit Margin"
)

st.plotly_chart(
    fig,
    use_container_width=True
)