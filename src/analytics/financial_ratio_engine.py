import pandas as pd
from cagr import revenue_cagr


# ==============================
# Load Dataset
# ==============================

df = pd.read_csv(
    "output/merged_financials.csv"
)


# Remove TTM rows

df = df[
    df["year"] != "TTM"
]


# ==============================
# Basic Ratios
# ==============================


# Net Profit Margin

df["net_profit_margin_pct"] = (
    df["net_profit"]
    /
    df["sales"].replace(0, None)
    *
    100
)


# Operating Profit Margin

df["operating_profit_margin_pct"] = (
    df["operating_profit"]
    /
    df["sales"].replace(0, None)
    *
    100
)


# Equity

equity = (
    df["equity_capital"]
    +
    df["reserves"]
)


# ROE

df["return_on_equity_pct"] = (
    df["net_profit"]
    /
    equity.replace(0, None)
    *
    100
)


df["return_on_equity_pct"] = (
    df["return_on_equity_pct"]
    .clip(
        lower=-100,
        upper=200
    )
)


# Debt Equity

df["debt_to_equity"] = (
    df["borrowings"]
    /
    equity.replace(0, None)
)


# Interest Coverage

df["interest_coverage"] = (

    (
        df["operating_profit"]
        +
        df["other_income"]
    )

    /

    df["interest"].replace(0,None)

)


# Asset Turnover

df["asset_turnover"] = (

    df["sales"]

    /

    df["total_assets"].replace(0,None)

)


# Free Cash Flow

df["free_cash_flow_cr"] = (

    df["operating_activity"]

    +

    df["investing_activity"]

)


# Capex

df["capex_cr"] = abs(
    df["investing_activity"]
)


# EPS

df["earnings_per_share"] = df["eps"]


# Book Value

df["book_value_per_share"] = (
    equity / 100
)


# Dividend

df["dividend_payout_ratio_pct"] = (
    df["dividend_payout"]
)


# Total Debt

df["total_debt_cr"] = (
    df["borrowings"]
)


# CFO

df["cash_from_operations_cr"] = (
    df["operating_activity"]
)



# ==============================
# CAGR Columns
# ==============================


df["revenue_cagr_5yr"] = None
df["pat_cagr_5yr"] = None
df["eps_cagr_5yr"] = None


# FLAGS

df["revenue_cagr_5yr_flag"] = None
df["pat_cagr_5yr_flag"] = None
df["eps_cagr_5yr_flag"] = None



# Sort

df = df.sort_values(
    [
        "company_id",
        "year"
    ]
)



# ==============================
# CAGR Calculation
# ==============================


for company, group in df.groupby("company_id"):


    group = (
        group
        .reset_index()
    )


    if len(group) >= 6:


        latest_index = (
            group.loc[
                len(group)-1,
                "index"
            ]
        )


        # --------------------------
        # Revenue CAGR
        # --------------------------

        revenue_value, revenue_flag = revenue_cagr(

            group.loc[0,"sales"],

            group.loc[5,"sales"],

            5

        )


        df.loc[
            latest_index,
            "revenue_cagr_5yr"
        ] = revenue_value


        df.loc[
            latest_index,
            "revenue_cagr_5yr_flag"
        ] = revenue_flag



        # --------------------------
        # PAT CAGR
        # --------------------------

        pat_value, pat_flag = revenue_cagr(

            group.loc[0,"net_profit"],

            group.loc[5,"net_profit"],

            5

        )


        df.loc[
            latest_index,
            "pat_cagr_5yr"
        ] = pat_value


        df.loc[
            latest_index,
            "pat_cagr_5yr_flag"
        ] = pat_flag



        # --------------------------
        # EPS CAGR
        # --------------------------

        eps_value, eps_flag = revenue_cagr(

            group.loc[0,"eps"],

            group.loc[5,"eps"],

            5

        )


        df.loc[
            latest_index,
            "eps_cagr_5yr"
        ] = eps_value


        df.loc[
            latest_index,
            "eps_cagr_5yr_flag"
        ] = eps_flag



# ==============================
# Latest Company Record
# ==============================


latest_df = (

    df
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
    .copy()

)



# ==============================
# Composite Quality Score
# ==============================


score_columns = [

    "return_on_equity_pct",

    "operating_profit_margin_pct",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "eps_cagr_5yr"

]


available = [

    col

    for col in score_columns

    if col in latest_df.columns

]


latest_df[available] = (

    latest_df[available]
    .fillna(0)

)



normalized = (

    latest_df[available]
    .rank(
        pct=True
    )

)



latest_df["composite_quality_score"] = (

    normalized.mean(axis=1)

    *

    100

)



# ==============================
# Merge Score
# ==============================


score_df = latest_df[

    [

        "company_id",

        "composite_quality_score"

    ]

]



if "composite_quality_score" in df.columns:

    df = df.drop(

        columns=[

            "composite_quality_score"

        ]

    )



df = df.merge(

    score_df,

    on="company_id",

    how="left"

)



# Fill only numeric columns
numeric_cols = df.select_dtypes(
    include=["float64","int64"]
).columns


numeric_cols = df.select_dtypes(
    include=["float64","int64"]
).columns


df[numeric_cols] = (
    df[numeric_cols]
    .fillna(0)
)


flag_columns = [
    "revenue_cagr_5yr_flag",
    "pat_cagr_5yr_flag",
    "eps_cagr_5yr_flag"
]


for col in flag_columns:
    if col in df.columns:
        df[col] = (
            df[col]
            .replace(0, "NOT_CALCULATED")
        )


# Keep text columns unchanged



# ==============================
# Save
# ==============================


df.to_csv(

    "output/financial_ratios.csv",

    index=False

)



print("="*50)

print("Financial Ratio Engine Completed")

print(
    "Rows:",
    len(df)
)

print(
    "Columns:",
    len(df.columns)
)

print(
    "Saved: output/financial_ratios.csv"
)

print("="*50)