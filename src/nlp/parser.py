import pandas as pd
import re
import os


# ============================================
# Paths
# ============================================

INPUT_FILE = "data/raw/analysis.xlsx"

OUTPUT_FILE = "output/analysis_parsed.csv"

FAILURE_FILE = "output/parse_failures.csv"


# ============================================
# Load Analysis Dataset
# ============================================

analysis_df = pd.read_excel(
    INPUT_FILE,
    header=1
)


print("=" * 50)
print("Analysis Dataset Loaded")
print("=" * 50)

print("Rows :", len(analysis_df))
print("Columns:")
print(analysis_df.columns.tolist())

print("Columns:")
print(analysis_df.columns.tolist())

print("\nSample Data:")
print(analysis_df.head())


# ============================================
# Regex Pattern
# ============================================

pattern = r"(\d+)\s*Years?:?\s*([\d.]+)%"


# ============================================
# Target Columns
# ============================================

target_columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]


parsed_records = []

failed_records = []


# ============================================
# Parse Text
# ============================================


for _, row in analysis_df.iterrows():

    company_id = row["company_id"]


    for metric in target_columns:

        if metric not in analysis_df.columns:
            continue


        text = str(row[metric])


        match = re.search(pattern, text)


        if match:

            period = int(match.group(1))

            value = float(match.group(2))


            parsed_records.append(
                {
                    "company_id": company_id,
                    "metric_type": metric,
                    "period_years": period,
                    "value_pct": value
                }
            )


        else:

            failed_records.append(
                {
                    "company_id": company_id,
                    "metric_type": metric,
                    "original_text": text
                }
            )


# ============================================
# Save Parsed Output
# ============================================


parsed_df = pd.DataFrame(parsed_records)


failure_df = pd.DataFrame(failed_records)



os.makedirs(
    "output",
    exist_ok=True
)


parsed_df.to_csv(
    OUTPUT_FILE,
    index=False
)


failure_df.to_csv(
    FAILURE_FILE,
    index=False
)



print("=" * 50)
print("NLP Parsing Completed")
print("=" * 50)


print(
    "Parsed Rows:",
    len(parsed_df)
)


print(
    "Failed Rows:",
    len(failure_df)
)


print("\nGenerated Files:")

print(
    OUTPUT_FILE
)

print(
    FAILURE_FILE
)