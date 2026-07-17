import pandas as pd
from cagr import revenue_cagr
# Load merged dataset
df = pd.read_csv("output/merged_financials.csv")
# Remove TTM rows
df = df[df["year"] != "TTM"]
# Net Profit Margin %
df["net_profit_margin_pct"] = (
    df["net_profit"] / df["sales"] * 100
)

# Operating Profit Margin %
df["operating_profit_margin_pct"] = (
    df["operating_profit"] / df["sales"] * 100
)

# Return on Equity %
equity = df["equity_capital"] + df["reserves"]

df["return_on_equity_pct"] = (
    df["net_profit"] / equity * 100
)

# Debt to Equity
df["debt_to_equity"] = (
    df["borrowings"] / equity
)

# Interest Coverage
df["interest_coverage"] = (
    (df["operating_profit"] + df["other_income"])
    / df["interest"]
)

# Asset Turnover
df["asset_turnover"] = (
    df["sales"] / df["total_assets"]
)

# Free Cash Flow
df["free_cash_flow_cr"] = (
    df["operating_activity"] +
    df["investing_activity"]
)

# CapEx
df["capex_cr"] = abs(df["investing_activity"])

# EPS
df["earnings_per_share"] = df["eps"]

# Book Value Per Share
df["book_value_per_share"] = (
    (df["equity_capital"] + df["reserves"])
    / 100
)

# Dividend Payout %
df["dividend_payout_ratio_pct"] = df["dividend_payout"]

# Total Debt
df["total_debt_cr"] = df["borrowings"]

# Cash From Operations
df["cash_from_operations_cr"] = df["operating_activity"]

# Placeholder values for CAGR and Quality Score
# -----------------------------
# Revenue CAGR (5 Years)
# -----------------------------

# Initialize column
df["revenue_cagr_5yr"] = None

# Sort by company and year
df = df.sort_values(["company_id", "year"])

for company, group in df.groupby("company_id"):

    group = group.reset_index()
    # Need at least 6 years of data
    if len(group) >= 6:

        value, flag = revenue_cagr(
            group.loc[0, "sales"],
            group.loc[5, "sales"],
            5
        )
        # Store the value in the latest row
        latest_index = group.loc[len(group) - 1, "index"]
        
        print(company)
        print(group[["year", "sales"]])
        print("Latest index:", latest_index)
        print("CAGR:", value)

        df.loc[latest_index, "revenue_cagr_5yr"] = value

df["pat_cagr_5yr"] = 0
df["eps_cagr_5yr"] = 0
df["composite_quality_score"] = 0
# Save results
df.to_csv(
    "output/financial_ratios.csv",
    index=False
)
print("=" * 40)
print("Financial Ratios Generated")
print("Rows :", len(df))
print("Columns :", len(df.columns))
print("Saved : output/financial_ratios.csv")
print("=" * 40)