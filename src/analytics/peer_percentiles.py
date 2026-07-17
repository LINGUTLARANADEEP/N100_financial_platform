import sqlite3
import pandas as pd

print("=" * 70)
print("DAY 18 - PEER PERCENTILES")
print("=" * 70)

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    fr.company_id,
    fr.year,
    s.broad_sector,

    fr.return_on_equity_pct,
    fr.net_profit_margin_pct,
    fr.operating_profit_margin_pct,
    fr.debt_to_equity,
    fr.asset_turnover,
    fr.free_cash_flow_cr,
    fr.interest_coverage,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.eps_cagr_5yr,
    fr.composite_quality_score

FROM financial_ratios fr

LEFT JOIN sectors s
ON fr.company_id = s.company_id

WHERE fr.year='Mar 2024'
"""

df = pd.read_sql(query, conn)
percentiles = pd.read_sql("""
SELECT
    company_id,
    metric,
    percentile
FROM peer_percentiles
""", conn)

print(f"\nCompanies Loaded : {len(df)}")

# Remove the old table so the schema is recreated
conn.execute("DROP TABLE IF EXISTS peer_percentiles")

conn.execute("""
CREATE TABLE peer_percentiles (

    company_id TEXT,
    broad_sector TEXT,
    metric TEXT,
    metric_value REAL,
    percentile REAL,
    year TEXT

)
""")
conn.execute("DELETE FROM peer_percentiles")

metrics = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "operating_profit_margin_pct",
    "asset_turnover",
    "free_cash_flow_cr",
    "interest_coverage",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "debt_to_equity"
]

rows = []

for sector in sorted(df["broad_sector"].dropna().unique()):

    sector_df = df[df["broad_sector"] == sector].copy()

    if len(sector_df) == 0:
        continue

    for metric in metrics:

        # Lower Debt/Equity is better
        if metric == "debt_to_equity":

            sector_df["percentile"] = (
                1 - sector_df[metric].rank(
                    pct=True,
                    ascending=True
                ) + (1 / len(sector_df))
            )

        else:

            sector_df["percentile"] = sector_df[metric].rank(
                pct=True,
                ascending=True
            )

        sector_df["percentile"] = (
            sector_df["percentile"]
            .clip(0, 1)
            .round(4)
        )

        for _, r in sector_df.iterrows():

            rows.append(

                (
                    r["company_id"],
                    sector,
                    metric,
                    float(r[metric]) if pd.notna(r[metric]) else None,
                    float(r["percentile"]) if pd.notna(r["percentile"]) else None,
                    r["year"]
                )

            )

conn.executemany("""

INSERT INTO peer_percentiles
(
    company_id,
    broad_sector,
    metric,
    metric_value,
    percentile,
    year
)
VALUES (?,?,?,?,?,?)

""", rows)

conn.commit()

print(f"\nRows Inserted : {len(rows)}")

print(f"\nPeer Groups : {df['broad_sector'].nunique()}")

print(f"Metrics Ranked : {len(metrics)}")

print("\nTable Created : peer_percentiles")

conn.close()

print("\n" + "=" * 70)
print("DAY 18 COMPLETED SUCCESSFULLY")
print("=" * 70)           