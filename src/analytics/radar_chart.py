import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

print("=" * 70)
print("DAY 19 - RADAR CHARTS")
print("=" * 70)

# Create output folder
os.makedirs("reports/radar_charts", exist_ok=True)

# Connect to SQLite
conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    fr.company_id,
    fr.return_on_equity_pct,
    fr.operating_profit_margin_pct,
    fr.debt_to_equity,
    fr.asset_turnover,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.free_cash_flow_cr,
    fr.composite_quality_score,
    s.broad_sector

FROM financial_ratios fr

LEFT JOIN sectors s
ON fr.company_id = s.company_id

WHERE fr.year='Mar 2024'
"""

df = pd.read_sql(query, conn)
conn.close()

metrics = [
    "return_on_equity_pct",
    "operating_profit_margin_pct",
    "debt_to_equity",
    "asset_turnover",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "free_cash_flow_cr",
    "composite_quality_score"
]

labels = [
    "ROE",
    "OPM",
    "D/E",
    "ATO",
    "Rev CAGR",
    "PAT CAGR",
    "FCF",
    "Score"
]

print(f"\nCompanies Loaded : {len(df)}")

count = 0

for _, row in df.iterrows():

    sector = row["broad_sector"]

    # If no peer group, compare against entire Nifty universe
    if pd.isna(sector):
        sector_df = df
        sector = "Nifty 100"
    else:
        sector_df = df[df["broad_sector"] == sector]

    company_values = []
    sector_values = []

    for metric in metrics:
        company_values.append(row[metric])
        sector_values.append(sector_df[metric].mean())

    company_values = np.nan_to_num(company_values)
    sector_values = np.nan_to_num(sector_values)

    max_vals = np.maximum(
        np.maximum(company_values, sector_values),
        1
    )

    company_plot = (company_values / max_vals) * 100
    sector_plot = (sector_values / max_vals) * 100

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    company_plot = company_plot.tolist()
    sector_plot = sector_plot.tolist()

    company_plot += company_plot[:1]
    sector_plot += sector_plot[:1]
    angles += angles[:1]

    plt.figure(figsize=(7, 7))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        company_plot,
        linewidth=2,
        label=row["company_id"]
    )

    ax.fill(
        angles,
        company_plot,
        alpha=0.25
    )

    ax.plot(
        angles,
        sector_plot,
        linestyle="--",
        linewidth=2,
        label="Sector Avg"
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_ylim(0, 100)

    plt.title(
        f"{row['company_id']} ({sector})",
        pad=20
    )

    plt.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.1)
    )

    plt.savefig(
        f"reports/radar_charts/{row['company_id']}_radar.png",
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    count += 1

print(f"\nRadar Charts Generated : {count}")

print("\nSaved to : reports/radar_charts/")

print("\nDay 19 Radar Charts Completed Successfully!")