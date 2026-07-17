import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    fr.company_id,
    fr.year,
    fr.sales,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.operating_profit_margin_pct,
    fr.net_profit_margin_pct,
    fr.asset_turnover,
    fr.interest_coverage,
    fr.free_cash_flow_cr,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,

    s.broad_sector,
    s.sub_sector

FROM financial_ratios fr

LEFT JOIN sectors s
ON fr.company_id = s.company_id
"""

df = pd.read_sql(query, conn)
conn.close()

os.makedirs("output", exist_ok=True)

print("=" * 70)
print("DAY 18 - PEER RANKING ENGINE")
print("=" * 70)

print("\nAvailable Sectors:\n")
print(sorted(df["broad_sector"].dropna().unique()))

sector = input("\nEnter Sector Name: ").strip()

sector_df = df[df["broad_sector"] == sector].copy()

if sector_df.empty:
    print("\n Sector not found!")
    exit()

numeric_cols = [
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "asset_turnover",
    "sales"
]

for col in numeric_cols:
    sector_df[col] = sector_df[col].fillna(0)

sector_df["score"] = (
    sector_df["return_on_equity_pct"]
    - sector_df["debt_to_equity"] * 10
    + sector_df["operating_profit_margin_pct"]
    + sector_df["asset_turnover"] * 10
)

sector_df = sector_df.sort_values(
    by="score",
    ascending=False
).reset_index(drop=True)

sector_df.insert(0, "Rank", range(1, len(sector_df) + 1))

result = sector_df[
    [
        "Rank",
        "company_id",
        "broad_sector",
        "return_on_equity_pct",
        "debt_to_equity",
        "operating_profit_margin_pct",
        "asset_turnover",
        "sales",
        "score"
    ]
]

print("\nTOP 20 COMPANIES\n")
print(result.head(20))

filename = f"output/{sector}_leaderboard.csv"
result.to_csv(filename, index=False)

print("\nLeaderboard saved successfully!")
print("File:", filename)

print("\nDay 18 Completed Successfully!")