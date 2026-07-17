import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
from utils.db import run_query
from utils.pdf_report import create_pdf

# ==========================================
# PAGE HEADER
# ==========================================

st.title("📊 Nifty 100 Financial Analytics Report")

st.caption("AI-powered Financial Analytics & Investment Insights")

st.caption(
    f"📅 Report Generated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
)

companies = run_query("SELECT * FROM companies")
financial = run_query("SELECT * FROM financial_ratios")
sectors = run_query("SELECT * FROM sectors")

st.subheader("📊 Dashboard Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Companies", len(companies))

with col2:
    st.metric("Total Financial Records", len(financial))

with col3:
    st.metric(
        "Total Sectors",
        sectors["broad_sector"].nunique()
    )

st.divider()

st.subheader("📄 Generate Company Report")

company_list = companies["id"].sort_values().tolist()

selected_company = st.selectbox(
    "Select Company",
    company_list
)

company_info = run_query(
    "SELECT * FROM companies WHERE id=?",
    (selected_company,)
)

pl_df = run_query(
    "SELECT * FROM profitandloss WHERE company_id=?",
    (selected_company,)
)

bs_df = run_query(
    "SELECT * FROM balancesheet WHERE company_id=?",
    (selected_company,)
)

cf_df = run_query(
    "SELECT * FROM cashflow WHERE company_id=?",
    (selected_company,)
)

sector_df = run_query(
    "SELECT * FROM sectors WHERE company_id=?",
    (selected_company,)
)

info = company_info.iloc[0]

display_pl = pl_df.drop(
    columns=["id", "id_pnl", "company_id"],
    errors="ignore"
)

display_bs = bs_df.drop(
    columns=["id", "company_id"],
    errors="ignore"
)

display_cf = cf_df.drop(
    columns=["id", "company_id"],
    errors="ignore"
)

display_sector = sector_df.drop(
    columns=["id"],
    errors="ignore"
)

latest = display_pl.iloc[-1]
previous = display_pl.iloc[-2]

sales_change = (
    (latest["sales"]-previous["sales"])
    / previous["sales"]
) * 100

profit_change = (
    (latest["net_profit"]-previous["net_profit"])
    / previous["net_profit"]
) * 100

margin_change = (
    latest["opm_percentage"]
    - previous["opm_percentage"]
)

st.subheader("🏢 Company Overview")

st.info(f"""
**Company:** {info['company_name']}

**Website:** {info['website']}
""")

st.subheader("📈 Financial Snapshot")

c1,c2,c3 = st.columns(3)

with c1:
    st.metric(
        "Revenue",
        f"₹ {latest['sales']:,.0f} Cr",
        f"{sales_change:.2f}%"
    )

with c2:
    st.metric(
        "Net Profit",
        f"₹ {latest['net_profit']:,.0f} Cr",
        f"{profit_change:.2f}%"
    )

with c3:
    st.metric(
        "Operating Margin",
        f"{latest['opm_percentage']}%"
    )

c4,c5,c6 = st.columns(3)

with c4:
    st.metric(
        "ROE",
        f"{info['roe_percentage']}%"
    )

with c5:
    st.metric(
        "ROCE",
        f"{info['roce_percentage']}%"
    )

with c6:
    st.metric(
        "Book Value",
        f"₹ {info['book_value']}"
    )

st.link_button(
    "🌐 Visit Company Website",
    info["website"]
)

st.divider()

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Financial Statements",
    "📈 Charts",
    "🏆 Analysis",
    "🏢 Company Info"
])

# ======================================================
# TAB 1 : FINANCIAL STATEMENTS
# ======================================================

with tab1:

    st.subheader("📈 Profit & Loss History")

    st.subheader("📈 Key Insights")

    st.success(f"""
### Financial Highlights

• Sales Growth: **{sales_change:.2f}%**

• Net Profit Growth: **{profit_change:.2f}%**

• Operating Margin Change: **{margin_change:.2f}%**

• Current ROE: **{info['roe_percentage']}%**

• Current ROCE: **{info['roce_percentage']}%**
""")

    st.dataframe(
        display_pl,
        use_container_width=True,
        hide_index=True
    )

    pl_csv = display_pl.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Profit & Loss",
        pl_csv,
        f"{selected_company}_ProfitLoss.csv",
        "text/csv"
    )

    st.divider()

    st.subheader("🏦 Balance Sheet History")

    st.dataframe(
        display_bs,
        use_container_width=True,
        hide_index=True
    )

    bs_csv = display_bs.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Balance Sheet",
        bs_csv,
        f"{selected_company}_BalanceSheet.csv",
        "text/csv"
    )

    st.divider()

    st.subheader("💵 Cash Flow History")

    st.dataframe(
        display_cf,
        use_container_width=True,
        hide_index=True
    )

    cf_csv = display_cf.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Cash Flow",
        cf_csv,
        f"{selected_company}_CashFlow.csv",
        "text/csv"
    )

    st.divider()

    st.subheader("🏭 Sector Information")

    st.dataframe(
        display_sector,
        use_container_width=True,
        hide_index=True
    )
    
    # ======================================================
# TAB 2 : CHARTS
# ======================================================

with tab2:

    st.subheader("📈 Financial Charts")

    col1, col2 = st.columns(2)

    # ---------------- Sales Chart ----------------
    sales_chart = px.line(
        display_pl,
        x="year",
        y="sales",
        markers=True,
        title="📈 Sales Trend"
    )

    # ---------------- Profit Chart ----------------
    profit_chart = px.bar(
        display_pl,
        x="year",
        y="net_profit",
        title="💰 Net Profit Trend"
    )

    with col1:
        st.plotly_chart(
            sales_chart,
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            profit_chart,
            use_container_width=True
        )

    # ---------------- Margin ----------------
    margin_chart = px.line(
        display_pl,
        x="year",
        y="opm_percentage",
        markers=True,
        title="📊 Operating Margin (%)"
    )

    latest_bs = display_bs.iloc[-1]

    asset_df = pd.DataFrame({
        "Asset": [
            "Fixed Assets",
            "Investments",
            "Other Assets"
        ],
        "Value": [
            latest_bs["fixed_assets"],
            latest_bs["investments"],
            latest_bs["other_asset"]
        ]
    })

    pie = px.pie(
        asset_df,
        names="Asset",
        values="Value",
        hole=0.45,
        title="🥧 Asset Distribution"
    )

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(
            margin_chart,
            use_container_width=True
        )

    with col4:
        st.plotly_chart(
            pie,
            use_container_width=True
        )

    # ---------------- Cash Flow ----------------
    cash_chart = px.line(
        display_cf,
        x="year",
        y="net_cash_flow",
        markers=True,
        title="💵 Net Cash Flow"
    )

    st.plotly_chart(
        cash_chart,
        use_container_width=True
    )

    st.caption(
        "© 2026 Nifty 100 Financial Analytics Platform | Streamlit • SQLite • Plotly"
    )
    
    # ======================================================
# TAB 3 : ANALYSIS
# ======================================================

with tab3:

    score = 0

    # ROE
    if info["roe_percentage"] >= 20:
        score += 25
    elif info["roe_percentage"] >= 15:
        score += 15

    # ROCE
    if info["roce_percentage"] >= 20:
        score += 25
    elif info["roce_percentage"] >= 15:
        score += 15

    # Sales Growth
    if sales_change > 10:
        score += 20
    elif sales_change > 0:
        score += 10

    # Profit Growth
    if profit_change > 10:
        score += 20
    elif profit_change > 0:
        score += 10

    # Operating Margin
    if latest["opm_percentage"] >= 20:
        score += 10
    elif latest["opm_percentage"] >= 10:
        score += 5

    st.subheader("🏆 Financial Health Score")

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Overall Financial Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 40], "color": "#ff4d4d"},
                {"range": [40, 70], "color": "#ffd966"},
                {"range": [70, 100], "color": "#66cc66"}
            ],
            "threshold": {
                "line": {"color": "black", "width": 4},
                "thickness": 0.75,
                "value": score
            }
        }
    )
)
gauge.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=60, b=20)
)

st.plotly_chart(
    gauge,
    use_container_width=True
    )
if score >= 80:
        st.success("★★★★★ Excellent Company")
        recommendation = "🟢 BUY"
        rating = "A"
        risk = "🟢 Low Risk"
        
elif score >= 60:
        st.info("★★★★ Good Company")
        recommendation = "🟡 HOLD"
        rating = "B"
        risk = "🟡 Medium Risk"
else:
        st.error("★★ Weak Financials")
        recommendation = "🔴 SELL / AVOID"
        rating = "C"
        risk = "🔴 High Risk"

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Recommendation", recommendation)

    with col2:
        st.metric("Rating", rating)

    with col3:
        st.metric("Risk", risk)

    st.divider()

    st.subheader("📋 SWOT Analysis")

    strengths = []
    weaknesses = []
    opportunities = []
    threats = []

    if info["roe_percentage"] > 20:
        strengths.append("High ROE")

    if info["roce_percentage"] > 20:
        strengths.append("High ROCE")

    if sales_change > 0:
        opportunities.append("Growing Sales")

    if profit_change > 0:
        opportunities.append("Increasing Profit")

    if latest["opm_percentage"] < 10:
        weaknesses.append("Low Operating Margin")

    if profit_change < 0:
        threats.append("Declining Profit")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### ✅ Strengths")
        if strengths:
            for s in strengths:
                st.write("•", s)
        else:
            st.write("No major strengths.")

        st.write("### 🚀 Opportunities")
        if opportunities:
            for o in opportunities:
                st.write("•", o)
        else:
            st.write("No major opportunities.")

    with col2:
        st.write("### ⚠ Weaknesses")
        if weaknesses:
            for w in weaknesses:
                st.write("•", w)
        else:
            st.write("No major weaknesses.")

        st.write("### 🔴 Threats")
        if threats:
            for t in threats:
                st.write("•", t)
        else:
            st.write("No immediate threats.")
            
            
           # ======================================================
# TAB 4 : COMPANY INFO
# ======================================================

with tab4:

    st.subheader("🏢 Company Information")

    st.info(f"""
**Company Name:** {info['company_name']}

**Website:** {info['website']}
""")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "ROE",
            f"{info['roe_percentage']}%"
        )

    with col2:
        st.metric(
            "ROCE",
            f"{info['roce_percentage']}%"
        )

    with col3:
        st.metric(
            "Book Value",
            f"₹ {info['book_value']}"
        )

    st.link_button(
        "🌐 Visit Company Website",
        info["website"]
    )

    st.divider()

    st.subheader("🏭 Sector Information")

    st.dataframe(
        display_sector,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("📄 Company Financial Snapshot")

    snapshot = pd.DataFrame({
        "Metric": [
            "Revenue",
            "Net Profit",
            "Operating Margin",
            "ROE",
            "ROCE",
            "Book Value"
        ],
        "Value": [
            f"₹ {latest['sales']:,.0f} Cr",
            f"₹ {latest['net_profit']:,.0f} Cr",
            f"{latest['opm_percentage']}%",
            f"{info['roe_percentage']}%",
            f"{info['roce_percentage']}%",
            f"₹ {info['book_value']}"
        ]
    })

    st.dataframe(
        snapshot,
        use_container_width=True,
        hide_index=True
    ) 