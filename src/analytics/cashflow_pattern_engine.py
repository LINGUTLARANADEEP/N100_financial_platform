import pandas as pd
from cashflow_patterns import classify_pattern

# Load cashflow dataset
df = pd.read_excel(
    "data/raw/cashflow.xlsx",
    header=1
)

results = []

for _, row in df.iterrows():

    company = row["company_id"]
    year = row["year"]

    cfo = row["operating_activity"]
    cfi = row["investing_activity"]
    cff = row["financing_activity"]

    pattern = classify_pattern(
        cfo,
        cfi,
        cff
    )

    print(company, year, pattern["pattern"])

    results.append({

        "company_id": company,
        "year": year,

        "cfo_sign": pattern["cfo_sign"],
        "cfi_sign": pattern["cfi_sign"],
        "cff_sign": pattern["cff_sign"],

        "pattern_label": pattern["pattern"]

    })

report = pd.DataFrame(results)

report.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print("\n===================================")
print("Capital Allocation Report Saved")
print("Location : output/capital_allocation.csv")
print("===================================")