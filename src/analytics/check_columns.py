import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    *
FROM financial_ratios
LIMIT 5
"""

df = pd.read_sql(query, conn)

percentiles = pd.read_sql("""
SELECT
    company_id,
    metric,
    percentile
FROM peer_percentiles
""", conn)

conn.close()

percentile_df = (
    percentiles
    .pivot(
        index="company_id",
        columns="metric",
        values="percentile"
    )
    .reset_index()
)


percentile_df = percentile_df.rename(columns={
    c: f"{c}_pctile"
    for c in percentile_df.columns
    if c != "company_id"
})

df = df.merge(percentile_df, on="company_id", how="left")

print(df.columns.tolist())