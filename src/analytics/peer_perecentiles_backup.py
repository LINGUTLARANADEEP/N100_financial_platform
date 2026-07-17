import sqlite3
import pandas as pd

print("=" * 70)
print("DAY 18 - PEER PERCENTILES")
print("=" * 70)

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    fr.company_id,
    s.broad_sector,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.operating_profit_margin_pct,
    fr.asset_turnover,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.free_cash_flow_cr,
    fr.interest_coverage,
    fr.composite_quality_score

FROM financial_ratios fr

LEFT JOIN sectors s
ON fr.company_id = s.company_id

WHERE fr.year='Mar 2024'
"""

df = pd.read_sql(query, conn)

print(f"\nCompanies Loaded : {len(df)}")

conn.execute("""
CREATE TABLE IF NOT EXISTS peer_percentiles (

    company_id TEXT,
    broad_sector TEXT,
    metric TEXT,
    metric_value REAL,
    percentile REAL

)
""")

conn.execute("DELETE FROM peer_percentiles")

metrics = [

    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "asset_turnover",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
    "interest_coverage",
    "composite_quality_score"

]

rows = []

for sector in sorted(df["broad_sector"].dropna().unique()):

    sector_df = df[df["broad_sector"] == sector].copy()

    for metric in metrics:

        ascending = metric == "debt_to_equity"

        sector_df["percentile"] = sector_df[metric].rank(
            pct=True,
            ascending=ascending
        )

        for _, r in sector_df.iterrows():

            rows.append(

                (
                    r["company_id"],
                    sector,
                    metric,
                    r[metric],
                    round(r["percentile"], 4)
                )

            )

conn.executemany("""

INSERT INTO peer_percentiles
VALUES (?,?,?,?,?)

""", rows)

conn.commit()

print(f"\nRows Inserted : {len(rows)}")

print("\nTable Created : peer_percentiles")

conn.close()

print("\nDay 18 Peer Percentiles Completed Successfully!")