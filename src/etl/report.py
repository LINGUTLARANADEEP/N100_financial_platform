import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("db/nifty100.db")

# Top 10 ROCE
query_roce = """
SELECT
    company_name,
    roce_percentage,
    roe_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10
"""

roce_df = pd.read_sql(query_roce, conn)

print("\nTop 10 Companies by ROCE")
print(roce_df)

roce_df.to_csv(
    "output/top10_roce_companies.csv",
    index=False
)

print("\nROCE Report saved successfully!")

# Top 10 ROE
query_roe = """
SELECT
    company_name,
    roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10
"""

roe_df = pd.read_sql(query_roe, conn)

print("\nTop 10 Companies by ROE")
print(roe_df)

roe_df.to_csv(
    "output/top10_roe_companies.csv",
    index=False
)

print("\nROE Report saved successfully!")

conn.close()