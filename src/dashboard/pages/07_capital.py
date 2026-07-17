import streamlit as st
import pandas as pd
import plotly.express as px
import os

from utils.db import run_query


# ==========================================
# Page Header
# ==========================================

st.title("💰 Capital Allocation Dashboard")

st.caption(
    "Analyze how companies generate and allocate cash through operating, investing and financing activities."
)

st.divider()


# ==========================================
# Load Companies
# ==========================================

companies = run_query("""
SELECT DISTINCT company_id
FROM cashflow
ORDER BY company_id
""")

company_list = companies["company_id"].tolist()

selected_company = st.selectbox(
    "Select Company",
    company_list
)


# ==========================================
# Load Valuation Data
# ==========================================

valuation_path = "output/valuation_summary.csv"

if os.path.exists(valuation_path):

    valuation_df = pd.read_csv(
        valuation_path
    )

    valuation_df = valuation_df[
        valuation_df["company_id"] == selected_company
    ]

else:
    valuation_df = pd.DataFrame()


# ==========================================
# Load Cash Flow Data
# ==========================================

cashflow_df = run_query(f"""
SELECT *
FROM cashflow
WHERE company_id='{selected_company}'
ORDER BY year
""")


st.write(
    f"Years Available : {len(cashflow_df)}"
)


# ==========================================
# Latest Data
# ==========================================

latest = cashflow_df.iloc[-1]


if not valuation_df.empty:

    latest_valuation = (
        valuation_df
        .sort_values("year")
        .iloc[-1]
    )


else:

    latest_valuation = None



# ==========================================
# Investment Recommendation
# ==========================================

if latest_valuation is not None:

    st.divider()

    st.subheader(
        "📈 Investment Recommendation"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Investment Rating",
            latest_valuation["investment_rating"]
        )


    with col2:

        st.metric(
            "Valuation Status",
            latest_valuation["valuation_status"]
        )


    with col3:

        st.metric(
            "Valuation Score",
            latest_valuation["valuation_score"]
        )



# ==========================================
# Financial Health Indicator
# ==========================================

if latest_valuation is not None:


    st.divider()

    score = latest_valuation["valuation_score"]


    if score >= 80:

        health = "Excellent"

    elif score >= 60:

        health = "Good"

    elif score >= 40:

        health = "Average"

    else:

        health = "Weak"



    col1, col2, col3 = st.columns(3)



    with col1:

        st.metric(
            "Financial Health Score",
            score
        )


    with col2:

        st.metric(
            "Financial Health",
            health
        )


    with col3:

        st.metric(
            "Investment Decision",
            latest_valuation["investment_rating"]
        )



# ==========================================
# Investment Insights
# ==========================================

st.divider()

st.subheader(
    "💡 Investment Insights"
)



if latest_valuation is not None:


    valuation_status = (
        latest_valuation["valuation_status"]
    )


    fcf_yield = latest_valuation.get(
        "fcf_yield_pct",
        None
    )


    if fcf_yield is not None:


        if fcf_yield > 5:

            st.success(
                f"💰 Strong Free Cash Flow Yield: {fcf_yield:.2f}%"
            )

        else:

            st.warning(
                f"⚠️ Low Free Cash Flow Yield: {fcf_yield:.2f}%"
            )



    if valuation_status == "Overvalued":

        st.warning(
            "⚠️ Stock valuation is above sector benchmark. "
            "Investors should evaluate growth expectations before investing."
        )


    elif valuation_status == "Undervalued":

        st.success(
            "🟢 Stock appears undervalued compared to sector valuation."
        )



if latest["operating_activity"] > 0:

    st.success(
        "✅ Positive operating cash flow indicates strong business operations."
    )



if latest["investing_activity"] < 0:

    st.info(
        "📈 Negative investing cash flow indicates investment in future growth."
    )



if latest["financing_activity"] < 0:

    st.write(
        "💰 Negative financing cash flow may indicate debt repayment or shareholder returns."
    )



if latest["net_cash_flow"] > 0:

    st.success(
        "🟢 Positive Net Cash Flow"
    )

else:

    st.error(
        "🔴 Negative Net Cash Flow"
    )



if latest["operating_activity"] > abs(latest["investing_activity"]):

    st.info(
        "Operating Cash Flow comfortably funds investments."
    )

else:

    st.warning(
        "Investments are larger than operating cash flow."
    )



# ==========================================
# Capital Allocation KPIs
# ==========================================

st.divider()

# ==========================================
# Capital Allocation Score
# ==========================================

score = 0
score_comments = []


# Operating Cash Flow Score
if latest["operating_activity"] > 0:
    score += 30
    score_comments.append(
        "✅ Strong operating cash generation"
    )


# Free Cash Flow Score
free_cash_flow = (
    latest["operating_activity"] 
    + latest["investing_activity"]
)

if free_cash_flow > 0:
    score += 30
    score_comments.append(
        "✅ Positive free cash flow"
    )
else:
    score_comments.append(
        "⚠ Negative free cash flow"
    )


# Investment Discipline

investment_ratio = (
    abs(latest["investing_activity"])
    /
    latest["operating_activity"]
)

if investment_ratio < 0.5:

    score += 20

    score_comments.append(
        "✅ Conservative investment strategy"
    )

elif investment_ratio < 1:

    score += 15

    score_comments.append(
        "✅ Investments funded through operations"
    )

else:

    score += 5

    score_comments.append(
        "⚠ High investment requirement"
    )


# Financing Health
if latest["financing_activity"] < 0:
    score += 5
    score_comments.append(
        "⚠ Negative financing activity indicates debt repayment or shareholder returns"
    )
else:
    score += 20
    score_comments.append(
        "✅ Positive financing support"
    )
    score_comments.append(
        "✅ External funding support"
    )


st.divider()

st.subheader("🏆 Capital Allocation Score")

col1, col2 = st.columns([1,3])


with col1:

    st.metric(
        "Score",
        f"{score}/100"
    )

    st.progress(score / 100)


with col2:
    for comment in score_comments:
        st.write(comment)

# ==========================================
# Investor Summary
# ==========================================

st.divider()

st.subheader(
    "📌 Investor Summary"
)


if score >= 80:

    st.success(
        """
        🟢 Strong Capital Allocation

        The company demonstrates strong operating cash generation
        and maintains positive free cash flow.

        Capital allocation is efficient, with operating cash
        supporting future investments.
        """
    )


elif score >= 60:

    st.info(
        """
        🟡 Financially Stable Company

        The company shows healthy operations,
        but investors should monitor investment
        and financing decisions.
        """
    )


else:

    st.warning(
        """
        🔴 Weak Capital Allocation

        The company requires careful evaluation due to
        cash flow pressure and allocation risks.
        """
    )

# ==========================================
# Overall Investment Decision
# ==========================================

st.divider()

st.subheader(
    f"🎯 Overall Investment Decision - {selected_company}"
)


valuation_score = latest_valuation["valuation_score"]


overall_score = (
    valuation_score * 0.6 +
    score * 0.4
)


if overall_score >= 80:

    decision = "🟢 Strong Buy"
    message = "Strong financial position and attractive valuation."

elif overall_score >= 60:

    decision = "🟡 Buy / Hold"
    message = "Company fundamentals are good but valuation needs monitoring."

elif overall_score >= 40:

    decision = "🟠 Hold"
    message = "Mixed signals. Investors should analyze further."

else:

    decision = "🔴 Avoid"
    message = "Weak valuation and financial indicators."


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Overall Score",
        f"{overall_score:.0f}/100"
    )
    
st.progress(overall_score / 100)

with col2:

    st.metric(
        "Final Recommendation",
        decision
    )


st.info(message)

# Score Interpretation

if overall_score >= 80:

    st.success(
        "Score Range: Excellent fundamentals and attractive valuation."
    )

elif overall_score >= 60:

    st.info(
        "Score Range: Good company, but investors should monitor risks."
    )

elif overall_score >= 40:

    st.warning(
        "Score Range: Mixed financial signals. Further analysis required."
    )

else:

    st.error(
        "Score Range: Weak fundamentals and valuation concerns."
    )

st.subheader(
    "📊 Capital Allocation KPIs"
)


free_cash_flow = (
    latest["operating_activity"]
    +
    latest["investing_activity"]
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Operating Cash Flow",
        f"{latest['operating_activity']:,.0f}"
    )


with col2:

    st.metric(
        "Investing Cash Flow",
        f"{latest['investing_activity']:,.0f}"
    )


with col3:

    st.metric(
        "Financing Cash Flow",
        f"{latest['financing_activity']:,.0f}"
    )


with col4:

    st.metric(
        "Net Cash Flow",
        f"{latest['net_cash_flow']:,.0f}"
    )
    
    with col5:
        st.metric(
        "Free Cash Flow",
        f"{free_cash_flow:,.0f}"
    )
    
    
    # ==========================================
# Cash Flow Trend Chart
# ==========================================

st.divider()

plot_df = cashflow_df.copy()


# Combine duplicate years
plot_df = (
    plot_df
    .groupby("year")
    [
        [
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow"
        ]
    ]
    .sum()
    .reset_index()
)


fig = px.line(
    plot_df,
    x="year",
    y=[
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow"
    ],
    markers=True,
    title="Cash Flow Trend"
)


fig.update_layout(
    height=500,
    xaxis_title="Year",
    yaxis_title="Cash Flow Amount",
    legend_title="Cash Flow Type"
)


st.plotly_chart(
    fig,
    use_container_width=True
)


fig.update_layout(
    height=550,
    xaxis_title="Year",
    yaxis_title="Cash Flow",
    legend_title=""
)

# ==========================================
# Cash Flow Distribution
# ==========================================

st.subheader(
    "🥧 Cash Flow Distribution"
)


pie_df = pd.DataFrame({

    "Category": [
        "Operating",
        "Investing",
        "Financing"
    ],

    "Amount": [
        abs(latest["operating_activity"]),
        abs(latest["investing_activity"]),
        abs(latest["financing_activity"])
    ]

})


pie = px.pie(
    pie_df,
    names="Category",
    values="Amount",
    hole=0.45,
    title="Latest Year Cash Flow Allocation"
)


st.plotly_chart(
    pie,
    use_container_width=True
)



# ==========================================
# Cash Flow History
# ==========================================

st.divider()

st.subheader(
    "📄 Cash Flow History"
)


display_df = (
    cashflow_df
    .groupby("year")
    [
        [
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow"
        ]
    ]
    .sum()
    .reset_index()
)


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)



csv = display_df.to_csv(
    index=False
)


st.download_button(
    label="📥 Download Cash Flow Data",
    data=csv,
    file_name=f"{selected_company}_cashflow.csv",
    mime="text/csv"
)



# ==========================================
# Cash Flow Components
# ==========================================

fig = px.bar(
    cashflow_df,
    x="year",
    y=[
        "operating_activity",
        "investing_activity",
        "financing_activity"
    ],
    barmode="group",
    title="📊 Cash Flow Components"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ==========================================
# Net Cash Flow Trend
# ==========================================

fig = px.area(
    cashflow_df,
    x="year",
    y="net_cash_flow",
    title="📈 Net Cash Flow Trend"
)


st.plotly_chart(
    fig,
    use_container_width=True
)



# ==========================================
# Final Capital Allocation Summary
# ==========================================

st.divider()

st.subheader(
    "📝 Final Analysis Summary"
)


if latest["operating_activity"] > 0:

    st.write(
        "✅ Positive operating cash flow indicates healthy core business operations."
    )


if latest["investing_activity"] < 0:

    st.write(
        "📈 The company is investing in future growth."
    )


if latest["financing_activity"] < 0:

    st.write(
        "💰 The company is repaying debt or returning money to shareholders."
    )


if latest["net_cash_flow"] > 0:

    st.success(
        "Overall cash position improved during the year."
    )

else:

    st.warning(
        "Overall cash position declined during the year."
    )



# ==========================================
# Footer
# ==========================================

st.caption(
    "Nifty 100 Financial Analytics Platform | Capital Allocation Module | Sprint 4"
)