import streamlit as st
import requests
import pandas as pd
import plotly.express as px


API_URL = "http://127.0.0.1:8000"


st.title("📈 Financial Metrics Analysis")


# ==================================================
# Load Financial Metrics API
# ==================================================

try:

    response = requests.get(
        f"{API_URL}/cluster-summary/",
        timeout=10
    )


    if response.status_code == 200:


        data = response.json()


        df = pd.DataFrame(
            data["records"]
        )


        # ==================================================
        # Clean Columns
        # ==================================================

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]


        drop_cols = [

            "return_on_equity_pct.l",
            "debt_to_equity.l",
            "revenue_cagr_5yr.l",
            "free_cash_flow_cr.l",
            "operating_profit_margin_pct.l"

        ]


        df.drop(

            columns=[
                c for c in drop_cols
                if c in df.columns
            ],

            inplace=True

        )



        # ==================================================
        # Convert Numeric Columns
        # ==================================================

        numeric_cols = [

            "return_on_equity_pct",
            "debt_to_equity",
            "operating_profit_margin_pct",
            "revenue_cagr_5yr",
            "free_cash_flow_cr",
            "composite_quality_score"

        ]


        for col in numeric_cols:

            if col in df.columns:

                df[col] = pd.to_numeric(

                    df[col],

                    errors="coerce"

                )



        # ==================================================
        # Remove Summary Rows
        # ==================================================

        df = df[
            ~df.astype(str)
            .apply(
                lambda x:
                x.str.contains(
                    "mean|median",
                    case=False
                ).any(),

                axis=1
            )
        ]



        # ==================================================
        # Latest Year Data
        # ==================================================

        if "year" in df.columns:


            df = (

                df.sort_values("year")

                .groupby("company_id")

                .tail(1)

            )



        # ==================================================
        # Remove Missing Values
        # ==================================================

        df.dropna(

            subset=[

                "return_on_equity_pct",

                "debt_to_equity",

                "operating_profit_margin_pct"

            ],

            inplace=True

        )



        # ==================================================
        # Remove Extreme ROE
        # ==================================================

        df = df[

            (df["return_on_equity_pct"] < 200)

            &

            (df["return_on_equity_pct"] > -100)

        ]



        # ==================================================
        # Fetch Company Names
        # ==================================================

        try:


            company_response = requests.get(

                f"{API_URL}/companies/",

                timeout=10

            )


            if company_response.status_code == 200:


                companies = pd.DataFrame(

                    company_response.json()

                )


                df = df.merge(

                    companies[

                        [
                            "id",
                            "company_name"
                        ]

                    ],

                    left_on="company_id",

                    right_on="id",

                    how="left"

                )


                df["Company"] = (

                    df["company_name"]

                    .fillna(df["company_id"])

                )


            else:

                df["Company"] = df["company_id"]



        except:


            df["Company"] = df["company_id"]



        # ==================================================
        # KPI Cards
        # ==================================================

        col1, col2, col3 = st.columns(3)


        col1.metric(

            "Average ROE",

            f"{df['return_on_equity_pct'].mean():.2f}%"

        )


        col2.metric(

            "Average Debt/Equity",

            f"{df['debt_to_equity'].mean():.2f}"

        )


        col3.metric(

            "Avg Operating Margin",

            f"{df['operating_profit_margin_pct'].mean():.2f}%"

        )



        st.divider()



        # ==================================================
        # Insights
        # ==================================================

        st.subheader("📌 Key Insights")


        best_company = df.loc[

            df["return_on_equity_pct"].idxmax()

        ]


        st.success(

            f"""

            Highest ROE:

            {best_company['Company']}

            {best_company['return_on_equity_pct']:.2f}%

            """

        )



        low_debt = df.loc[

            df["debt_to_equity"].idxmin()

        ]


        st.info(

            f"""

            Lowest Debt Company:

            {low_debt['Company']}

            Debt/Equity:

            {low_debt['debt_to_equity']:.2f}

            """

        )



        # ==================================================
        # Table
        # ==================================================

        st.subheader(
            "Financial Metrics"
        )


        display_cols = [

            "Company",

            "year",

            "return_on_equity_pct",

            "debt_to_equity",

            "operating_profit_margin_pct",

            "free_cash_flow_cr",

            "revenue_cagr_5yr"

        ]


        available_cols = [

            c for c in display_cols

            if c in df.columns

        ]


        st.dataframe(

            df[available_cols],

            use_container_width=True

        )



        # ==================================================
        # ROE Chart
        # ==================================================

        st.subheader(
            "Return on Equity Analysis"
        )


        roe_df = df.sort_values(

            "return_on_equity_pct",

            ascending=True

        )


        fig = px.bar(

            roe_df,

            x="return_on_equity_pct",

            y="Company",

            orientation="h",

            text="return_on_equity_pct",

            title="Company ROE Comparison"

        )


        fig.update_traces(

            texttemplate="%{text:.2f}%"

        )


        st.plotly_chart(

            fig,

            use_container_width=True

        )



        # ==================================================
        # Debt vs Profitability
        # ==================================================

        st.subheader(

            "Debt vs Profitability"

        )


        df["roe_size"] = (

            df["return_on_equity_pct"]

            .abs()

        )


        fig2 = px.scatter(

            df,

            x="debt_to_equity",

            y="operating_profit_margin_pct",

            size="roe_size",

            hover_name="Company",

            hover_data=[

                "return_on_equity_pct",

                "free_cash_flow_cr"

            ],

            title="Debt Risk vs Profitability"

        )


        st.plotly_chart(

            fig2,

            use_container_width=True

        )



    else:


        st.error(
            "Financial API not responding"
        )



except Exception as e:


    st.error(

        f"Error: {e}"

    )