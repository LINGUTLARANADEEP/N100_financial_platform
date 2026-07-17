import sqlite3
import pandas as pd
import os

print("=" * 65)
print("DAY 20 - PORTFOLIO RECOMMENDER")
print("=" * 65)

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    fr.company_id,
    fr.year,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.composite_quality_score,
    s.broad_sector,
    s.sub_sector

FROM financial_ratios fr

LEFT JOIN sectors s
ON fr.company_id = s.company_id
"""

df = pd.read_sql(query, conn)
conn.close()

print(f"\nRows Loaded : {len(df)}")

df = df[df["year"] != "TTM"].copy()

df["year_num"] = (
    df["year"]
    .str.extract(r"(\d{4})")
    .astype(float)
)

df = (
    df.sort_values("year_num", ascending=False)
      .drop_duplicates("company_id")
)

df["portfolio_score"] = (

      df["composite_quality_score"] * 0.40

    + df["return_on_equity_pct"] * 0.25

    + df["revenue_cagr_5yr"] * 0.15

    + df["pat_cagr_5yr"] * 0.10

    - df["debt_to_equity"] * 10

)

portfolio = (

    df.sort_values(
        "portfolio_score",
        ascending=False
    )

    .head(20)

)

print("\nTOP 20 PORTFOLIO\n")

print(

portfolio[
[
"company_id",
"broad_sector",
"return_on_equity_pct",
"debt_to_equity",
"revenue_cagr_5yr",
"pat_cagr_5yr",
"portfolio_score"
]

]

)

os.makedirs("output", exist_ok=True)

portfolio.to_csv(
    "output/recommended_portfolio.csv",
    index=False
)

print("\nPortfolio saved successfully.")
print("File : output/recommended_portfolio.csv")

print("\nDay 20 Completed Successfully!")