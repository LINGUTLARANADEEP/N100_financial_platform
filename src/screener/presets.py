import sqlite3
import pandas as pd
import os

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
    fr.interest_coverage,
    fr.asset_turnover,
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

# ==========================================
# Keep only the latest financial record
# ==========================================

# Remove TTM rows
df = df[df["year"] != "TTM"].copy()

# Extract year number
df["year_num"] = (
    df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")
    .astype(int)
)

# Sort newest first
df = df.sort_values(
    ["company_id", "year_num"],
    ascending=[True, False]
)

# Keep latest row for each company
df = df.drop_duplicates(
    subset="company_id",
    keep="first"
)

# Remove helper column
df.drop(columns="year_num", inplace=True)

print(f"\nLatest company records : {len(df)}")

os.makedirs("output", exist_ok=True)


def save_result(filename, dataframe):
    dataframe.to_csv(f"output/{filename}.csv", index=False)
    print(f"{filename:<22}: {len(dataframe)} companies")


print("=" * 70)
print("DAY 16 - PRESET SCREENERS")
print("=" * 70)

print(f"\nRows Loaded : {len(df)}")

    # =====================================================
# QUALITY COMPOUNDER
# =====================================================

quality_compounder = df[
    (df["return_on_equity_pct"] >= 18) &
    (
        (df["debt_to_equity"] <= 1) |
        (df["broad_sector"] == "Financials")
    ) &
    (df["free_cash_flow_cr"] > 0)
].sort_values(
    by="composite_quality_score",
    ascending=False
)

save_result("quality_compounder", quality_compounder)


# =====================================================
# VALUE PICK
# =====================================================

value_pick = df[
    (
        (df["debt_to_equity"] <= 1) |
        (df["broad_sector"] == "Financials")
    ) &
    (df["return_on_equity_pct"] >= 15) &
    (df["dividend_payout_ratio_pct"] < 60) &
    (df["free_cash_flow_cr"] > 0)
].sort_values(
    by="composite_quality_score",
    ascending=False
)

save_result("value_pick", value_pick)


# =====================================================
# GROWTH ACCELERATOR
# =====================================================

growth_accelerator = df[
    (df["return_on_equity_pct"] >= 15) &
    (df["sales"] >= 5000) &
    (df["debt_to_equity"] <= 1)
].sort_values(
    by="return_on_equity_pct",
    ascending=False
)

save_result("growth_accelerator", growth_accelerator)


# =====================================================
# DIVIDEND CHAMPION
# =====================================================

dividend_champion = df[
    (df["dividend_payout_ratio_pct"] < 60) &
    (df["free_cash_flow_cr"] > 0) &
    (df["return_on_equity_pct"] >= 15)
].sort_values(
    by="free_cash_flow_cr",
    ascending=False
)

save_result("dividend_champion", dividend_champion)


# =====================================================
# DEBT FREE BLUECHIP
# =====================================================

debt_free_bluechip = df[
    (df["debt_to_equity"] == 0) &
    (df["return_on_equity_pct"] >= 12) &
    (df["sales"] >= 3000)
].sort_values(
    by="return_on_equity_pct",
    ascending=False
)

save_result("debt_free_bluechip", debt_free_bluechip)


# =====================================================
# TURNAROUND WATCH
# =====================================================

turnaround_watch = df[
    (df["operating_profit_margin_pct"] >= 10) &
    (df["free_cash_flow_cr"] > 0) &
    (df["return_on_equity_pct"] >= 12)
].sort_values(
    by="operating_profit_margin_pct",
    ascending=False
)

save_result("turnaround_watch", turnaround_watch)

large_cap_quality = df[
    (df["sales"] > 5000) &
    (df["return_on_equity_pct"] > 10)
].sort_values(
    by="return_on_equity_pct",
    ascending=False
)

save_result("large_cap_quality", large_cap_quality)

high_roe = df[
    df["return_on_equity_pct"] > 20
].sort_values(
    by="return_on_equity_pct",
    ascending=False
)

save_result("high_roe", high_roe)

low_debt = df[
    (
        (df["debt_to_equity"] < 0.5) |
        (df["broad_sector"] == "Financials")
    )
].sort_values(
    by="debt_to_equity"
)

save_result("low_debt", low_debt)

cash_rich = df[
    df["free_cash_flow_cr"] > 500
].sort_values(
    by="free_cash_flow_cr",
    ascending=False
)

save_result("cash_rich", cash_rich)

print("\n" + "=" * 70)
print("DAY 16 COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nCSV files generated inside the output folder.")