import sqlite3
import pandas as pd
import yaml


with open("config/screener_config.yaml", "r") as file:
    config = yaml.safe_load(file)

filters = config["filters"]

conn = sqlite3.connect("db/nifty100.db")

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sectors = pd.read_sql(
    """
    SELECT
        company_id,
        broad_sector,
        sub_sector
    FROM sectors
    """,
    conn
)

df = financial_ratios.merge(
    sectors,
    on="company_id",
    how="left"
)

print("=" * 70)
print("SCREENER ENGINE")
print("=" * 70)

print("Original Companies :", len(df))

df = df[
    df["return_on_equity_pct"] >= filters["roe_min"]
]

print("After ROE Filter :", len(df))

financial_df = df[
    df["broad_sector"] == "Financials"
]

non_financial_df = df[
    df["broad_sector"] != "Financials"
]

non_financial_df = non_financial_df[
    non_financial_df["debt_to_equity"]
    <= filters["debt_to_equity_max"]
]

df = pd.concat(
    [financial_df, non_financial_df],
    ignore_index=True
)

print("After Debt/Equity Filter :", len(df))

df = df[
    df["free_cash_flow_cr"]
    >= filters["free_cash_flow_min"]
]

print("After Free Cash Flow Filter :", len(df))

if "revenue_cagr_5yr" in df.columns:

    df = df[
        df["revenue_cagr_5yr"]
        >= filters["revenue_cagr_5yr_min"]
    ]

    print("After Revenue CAGR Filter :", len(df))

if "pat_cagr_5yr" in df.columns:

    df = df[
        df["pat_cagr_5yr"]
        >= filters["pat_cagr_5yr_min"]
    ]

    print("After PAT CAGR Filter :", len(df))

df = df[
    df["operating_profit_margin_pct"]
    >= filters["operating_profit_margin_min"]
]

print("After OPM Filter :", len(df))

df = df[
    df["interest_coverage"]
    >= filters["interest_coverage_min"]
]

print("After Interest Coverage Filter :", len(df))

df = df[
    df["asset_turnover"]
    >= filters["asset_turnover_min"]
]

print("After Asset Turnover Filter :", len(df))


if "sales" in df.columns:

    df = df[
        df["sales"]
        >= filters["sales_min"]
    ]

    print("After Sales Filter :", len(df))


sort_column = (
    "composite_quality_score"
    if "composite_quality_score" in df.columns
    else "return_on_equity_pct"
)

df = df.sort_values(
    by=sort_column,
    ascending=False
)

print("\n")
print("=" * 70)
print("TOP SCREENER RESULTS")
print("=" * 70)

preview_columns = [
    "company_id",
    "year",
    "broad_sector",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr"
]

if "composite_quality_score" in df.columns:
    preview_columns.append("composite_quality_score")

print(df[preview_columns].head(20))


df.to_csv(
    "output/screener_day15.csv",
    index=False
)

print("\n")
print("=" * 70)
print("Day 15 Completed Successfully")
print("=" * 70)
print("Companies Remaining :", len(df))
print("Saved : output/screener_day15.csv")

conn.close()