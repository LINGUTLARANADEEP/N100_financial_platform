import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

# Count rows in financial_ratios table
df = pd.read_sql(
    """
    SELECT COUNT(*) AS total_rows
    FROM financial_ratios
    """,
    conn
)

print(df)

conn.close()