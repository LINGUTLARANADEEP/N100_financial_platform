import pandas as pd
import os


PARSED_FILE = "output/analysis_parsed.csv"
RATIO_FILE = "output/financial_ratios.csv"

OUTPUT_FILE = "output/cagr_validation.csv"


# Load files
parsed = pd.read_csv(PARSED_FILE)
ratios = pd.read_csv(RATIO_FILE)


print("Parsed Data")
print(parsed.head())

print("\nRatio Data")
print(ratios.head())


results = []


for _, row in parsed.iterrows():

    company = row["company_id"]
    metric = row["metric_type"]
    parsed_value = row["value_pct"]


    company_ratio = ratios[
        ratios["company_id"] == company
    ]


    if company_ratio.empty:
        continue


    if metric == "compounded_sales_growth":

        computed_value = company_ratio.iloc[-1]["revenue_cagr_5yr"]


    elif metric == "compounded_profit_growth":

        computed_value = company_ratio.iloc[-1]["pat_cagr_5yr"]


    else:
        continue


    difference = abs(
        parsed_value - computed_value
    )


    status = (
        "REVIEW"
        if difference > 5
        else "OK"
    )


    results.append({

        "company_id": company,
        "metric_type": metric,
        "parsed_value": parsed_value,
        "computed_value": computed_value,
        "difference_pct": difference,
        "status": status

    })


validation = pd.DataFrame(results)


validation.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nCAGR Validation Completed")
print(validation.head())

print("\nSaved:")
print(OUTPUT_FILE)