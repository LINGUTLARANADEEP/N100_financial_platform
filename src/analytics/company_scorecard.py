import sqlite3
import pandas as pd
import os

print("=" * 70)
print("DAY 19 - COMPANY SCORECARD ENGINE")
print("=" * 70)

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    fr.company_id,
    fr.year,
    fr.sales,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.operating_profit_margin_pct,
    fr.net_profit_margin_pct,
    fr.asset_turnover,
    fr.interest_coverage,
    fr.dividend_payout_ratio_pct,
    fr.composite_quality_score,
    s.broad_sector,
    s.sub_sector

FROM financial_ratios fr

LEFT JOIN sectors s
ON fr.company_id = s.company_id
"""

df = pd.read_sql(query, conn)

conn.close()

print("\nRows Loaded :", len(df))

print("\nAvailable Companies:\n")

companies = sorted(df["company_id"].dropna().unique())

print(companies[:30], "...")

company = input("\nEnter Company ID : ").strip().upper()

company_df = df[df["company_id"] == company].copy()

if company_df.empty:
    print("\nCompany not found.")
    exit()

company_df = company_df[
    company_df["year"] != "TTM"
].copy()

# Extract year number (2024, 2023, etc.)
company_df["year_num"] = (
    company_df["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

# Latest financial year
latest = company_df.sort_values(
    by="year_num",
    ascending=False
).iloc[0]

quality = 0

if latest["return_on_equity_pct"] >= 20:
    quality += 25

if latest["debt_to_equity"] <= 0.5:
    quality += 25

if latest["free_cash_flow_cr"] > 0:
    quality += 25

if latest["asset_turnover"] > 1:
    quality += 25

growth = 0

if latest["revenue_cagr_5yr"] > 10:
    growth += 50

if latest["pat_cagr_5yr"] > 10:
    growth += 50

profitability = 0

if latest["operating_profit_margin_pct"] > 15:
    profitability += 50

if latest["net_profit_margin_pct"] > 15:
    profitability += 50

health = 0

if latest["interest_coverage"] > 3:
    health += 50

if latest["debt_to_equity"] < 1:
    health += 50

overall = (
    quality +
    growth +
    profitability +
    health
)

overall = overall / 4

if overall >= 90:
    rating = "A+"

elif overall >= 80:
    rating = "A"

elif overall >= 70:
    rating = "B+"

elif overall >= 60:
    rating = "B"

else:
    rating = "C"


scorecard = pd.DataFrame({
    "Company":[company],
    "Sector":[latest["broad_sector"]],
    "Sub Sector":[latest["sub_sector"]],
    "Quality Score":[quality],
    "Growth Score":[growth],
    "Profitability Score":[profitability],
    "Financial Health":[health],
    "Overall Score":[overall],
    "Rating":[rating]
})

os.makedirs("output", exist_ok=True)

scorecard.to_csv(
    "output/company_scorecard.csv",
    index=False
)

print("\n")
print(scorecard)

print("\nSaved : output/company_scorecard.csv")

print("\nDay 19 Completed Successfully!")