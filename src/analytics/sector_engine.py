import pandas as pd
from sector_analytics import *

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_excel(
    "data/raw/sectors.xlsx",
    header=None
)

# Assign proper column names
df.columns = [
    "id",
    "company_id",
    "broad_sector",
    "sub_sector",
    "index_weight_pct",
    "market_cap_category"
]

# Remove duplicate header row
if str(df.iloc[0]["company_id"]).lower() == "company_id":
    df = df.iloc[1:].reset_index(drop=True)

# Convert weight column to numeric
df["index_weight_pct"] = pd.to_numeric(
    df["index_weight_pct"],
    errors="coerce"
)

print("========== SECTOR ANALYTICS REPORT ==========\n")

results = []

for _, row in df.iterrows():

    summary = sector_summary(
        row["company_id"],
        row["broad_sector"],
        row["sub_sector"],
        row["index_weight_pct"],
        row["market_cap_category"]
    )

    print(summary["Company"])
    print(f"Broad Sector    : {summary['Broad Sector']}")
    print(f"Sub Sector      : {summary['Sub Sector']}")
    print(f"Index Weight %  : {summary['Index Weight %']:.2f}")
    print(f"Market Cap      : {summary['Market Cap']}")
    print("-" * 40)

    results.append(summary)

# Save report
report = pd.DataFrame(results)

report.to_csv(
    "output/sector_analytics.csv",
    index=False
)

print("\n==============================")
print("Sector Analytics Report Saved")
print("Location : output/sector_analytics.csv")
print("==============================")