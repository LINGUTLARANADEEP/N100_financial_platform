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
        f"{API_URL}/financial-metrics/",
        timeout=10
    )


    if response.status_code == 200:


        data = response.json()


        df = pd.DataFrame(
            data["records"]
        )


        # ==================================================
        # Remove Duplicate Columns
        # ==================================================

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]



        # ==================================================
        # Convert Numeric Columns
        # ==================================================

        numeric_cols = [

            "sales",
            "operating_profit",
            "opm_percentage",
            "net_profit",
            "equity_capital",
            "borrowings",
            "total_liabilities",
            "eps"

        ]


        for col in numeric_cols:

            if col in df.columns:

                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )



        # ==================================================
        # Calculate Financial Metrics
        # ==================================================

        df["return_on_equity_pct"] = (

            df["net_profit"] /
            df["equity_capital"]

        ) * 100



        df["debt_to_equity"] = (

            df["borrowings"] /
            df["equity_capital"]

        )



        df["operating_profit_margin_pct"] = (

            df["operating_profit"] /
            df["sales"]

        ) * 100



        # ==================================================
        # Remove Infinite Values
        # ==================================================

        df.replace(
            [float("inf"), -float("inf")],
            0,
            inplace=True
        )



        # ==================================================
        # Remove Missing Data
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
        # Latest Year Data
        # ==================================================

        if "year" in df.columns:


            df = (

                df.sort_values("year")

                .groupby("company_id")

                .tail(1)

            )



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


                if "company_name" in companies.columns:


                    df = df.merge(

                        companies[

                            [

                                "company_name"

                            ]

                        ],

                        left_on="company_id",

                        right_on="company_name",

                        how="left"

                    )


                    df["Company"] = (

                        df["company_name"]

                        .fillna(df["company_id"])

                    )


                else:

                    df["Company"] = df["company_id"]



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

            "Average Operating Margin",

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

            🏆 Highest ROE Company:

            {best_company['Company']}

            ROE:

            {best_company['return_on_equity_pct']:.2f}%

            """

        )



        low_debt = df.loc[

            df["debt_to_equity"].idxmin()

        ]



        st.info(

            f"""

            💰 Lowest Debt Company:

            {low_debt['Company']}

            Debt/Equity:

            {low_debt['debt_to_equity']:.2f}

            """

        )




        # ==================================================
        # Financial Metrics Table
        # ==================================================

        st.subheader(
            "Financial Metrics"
        )


        display_cols = [

            "Company",

            "year",

            "sales",

            "net_profit",

            "return_on_equity_pct",

            "debt_to_equity",

            "operating_profit_margin_pct",

            "eps"

        ]


        available_cols = [

            col for col in display_cols

            if col in df.columns

        ]


        st.dataframe(

            df[available_cols],

            width="stretch"

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

            width="stretch"

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

                "net_profit",

                "sales"

            ],

            title="Debt Risk vs Profitability"

        )


        st.plotly_chart(

            fig2,

            width="stretch"

        )



    else:


        st.error(

            "Financial API not responding"

        )



except Exception as e:


    st.error(

        f"Error: {e}"

    )