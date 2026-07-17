import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    fr.company_id,
    fr.year,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.operating_profit_margin_pct,
    fr.net_profit_margin_pct,
    fr.asset_turnover,
    fr.interest_coverage,
    fr.free_cash_flow_cr,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.sales,

    s.broad_sector,
    s.sub_sector

FROM financial_ratios fr

LEFT JOIN sectors s
ON fr.company_id = s.company_id
"""

df = pd.read_sql(query, conn)

conn.close()

print("=" * 70)
print("DAY 17 - PEER COMPARISON ENGINE")
print("=" * 70)

print("\nRows Loaded :", len(df))

print("\nAvailable Companies:")
print(df["company_id"].drop_duplicates().sort_values().head(20).tolist())

company = input("\nEnter Company ID : ").upper()

company_df = df[df["company_id"] == company]

if company_df.empty:
    print("\nCompany not found.")
    exit()

sector = company_df.iloc[0]["broad_sector"]

sector_df = df[df["broad_sector"] == sector]

print("\nCompany :", company)
print("Sector  :", sector)

metrics = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "net_profit_margin_pct",
    "asset_turnover",
    "interest_coverage",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "sales"
]

comparison = pd.DataFrame()

comparison["Metric"] = metrics

comparison["Company"] = [
    company_df[m].mean()
    for m in metrics
]

comparison["Sector Average"] = [
    sector_df[m].mean()
    for m in metrics
]

print("\n")
print(comparison)

comparison.to_csv(
    f"output/{company}_peer_comparison.csv",
    index=False
)

print("\nSaved to output folder.")