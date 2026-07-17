import sqlite3
import pandas as pd

# Connect to SQLite
conn = sqlite3.connect("db/nifty100.db")

# Read latest financial ratios CSV
df = pd.read_csv("output/financial_ratios.csv")

# Replace table with latest data
df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print("=" * 50)
print("Financial Ratios Table Updated")
print("=" * 50)
print("Rows    :", len(df))
print("Columns :", len(df.columns))
print("=" * 50)

conn.close()