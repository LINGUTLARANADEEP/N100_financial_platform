import streamlit as st
import plotly.express as px
from utils.db import run_query

st.title("Sector Analysis")

# ----------------------------------
# Load Sector List
# ----------------------------------

sector_df = run_query("""
SELECT DISTINCT broad_sector
FROM sectors
ORDER BY broad_sector
""")

sector = st.selectbox(
    "Select Sector",
    sector_df["broad_sector"]
)

# ----------------------------------
# Load Companies
# ----------------------------------

df = run_query(f"""
SELECT
    c.company_name,
    s.company_id,
    s.broad_sector,
    s.sub_sector,
    s.market_cap_category,
    s.index_weight_pct,
    f.return_on_equity_pct,
    f.debt_to_equity,
    f.interest_coverage,
    f.revenue_cagr_5yr

FROM sectors s

JOIN companies c
ON s.company_id = c.id

LEFT JOIN financial_ratios f
ON s.company_id = f.company_id
AND f.year='Mar 2024'

WHERE s.broad_sector='{sector}'
""")

st.divider()

st.subheader("Sector Overview")

st.write("Companies :", len(df))

st.dataframe(df)

fig = px.bar(
    df,
    x="company_name",
    y="index_weight_pct",
    title="Sector Weight",
    text="index_weight_pct"
)

st.plotly_chart(fig, use_container_width=True)

top = df.sort_values(
    "return_on_equity_pct",
    ascending=False
)

fig = px.bar(
    top,
    x="company_name",
    y="return_on_equity_pct",
    color="return_on_equity_pct",
    title="Top Companies by ROE"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.pie(
    df,
    names="market_cap_category",
    title="Market Cap Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Sector Companies")

st.dataframe(
    df,
    use_container_width=True
)