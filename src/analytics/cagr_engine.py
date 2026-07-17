import pandas as pd
from cagr import revenue_cagr

# Load dataset
df = pd.read_excel(
    "data/raw/profitandloss.xlsx",
    header=1
)

# Remove TTM rows
df = df[df["year"] != "TTM"]

# Convert sales to numeric
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

# Remove rows with missing sales
df = df.dropna(subset=["sales"])

# Sort by company and year
df = df.sort_values(["company_id", "year"])

print("========== CAGR REPORT ==========\n")

for company, group in df.groupby("company_id"):
    group = group.reset_index(drop=True)
    print(f"\n{company}")
    # Revenue CAGR - 3 Years
    if len(group) >= 4:
        value, flag = revenue_cagr(
            group.iloc[0]["sales"],
            group.iloc[3]["sales"],
            3
        )
        print(f"Revenue CAGR 3Y : {value} ({flag})")
    # Revenue CAGR - 5 Years
    if len(group) >= 6:
        value, flag = revenue_cagr(
            group.iloc[0]["sales"],
            group.iloc[5]["sales"],
            5
        )
        print(f"Revenue CAGR 5Y : {value} ({flag})")
    # Revenue CAGR - 10 Years
    if len(group) >= 11:
        value, flag = revenue_cagr(
            group.iloc[0]["sales"],
            group.iloc[10]["sales"],
            10
        )
        print(f"Revenue CAGR 10Y : {value} ({flag})")