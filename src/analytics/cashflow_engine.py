import pandas as pd
from cashflow_kpis import *

df = pd.read_excel(
    "data/raw/cashflow.xlsx",
    header=1
)

print("===== CASH FLOW DATASET =====")
print(df.head())

print("\nRows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn Names")
print(df.columns.tolist())


results = []

print("\n========== CASH FLOW KPI REPORT ==========\n")

for company, group in df.groupby("company_id"):

    group = group.reset_index(drop=True)

    latest = group.iloc[-1]

    operating_cf = latest["operating_activity"]
    investing_cf = latest["investing_activity"]

    free_cf = free_cash_flow(
        operating_cf,
        investing_cf
    )

    capex_ratio = capex_intensity(
        investing_cf,
        operating_cf
    )

    fcf_ratio = fcf_conversion(
        free_cf,
        operating_cf
    )

    print(company)
    print(f"Operating CF : {operating_cf:.2f}")
    print(f"Investing CF : {investing_cf:.2f}")
    print(f"CapEx        : {abs(investing_cf):.2f}")
    print(f"Free CF      : {free_cf:.2f}")
    print(f"CapEx %      : {capex_ratio:.2f}")
    print(f"FCF Conv %   : {fcf_ratio:.2f}")
    print("-" * 40)

    results.append({
        "company": company,
        "operating_cf": operating_cf,
        "investing_cf": investing_cf,
        "free_cash_flow": free_cf,
        "capex_intensity": round(capex_ratio, 2),
        "fcf_conversion": round(fcf_ratio, 2)
    })


results_df = pd.DataFrame(results)

results_df.to_csv(
    "output/cashflow_kpis.csv",
    index=False
)

print("\n===================================")
print("Cash Flow KPI Report Saved")
print("Location : output/cashflow_kpis.csv")
print("===================================")