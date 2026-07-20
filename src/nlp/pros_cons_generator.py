import pandas as pd
import os


INPUT_FILE = "output/financial_ratios.csv"

OUTPUT_FILE = "output/pros_cons_generated.csv"


df = pd.read_csv(INPUT_FILE)


results = []


# latest year data for every company
latest_df = (
    df.sort_values("year")
    .groupby("company_id")
    .tail(1)
)


def add_result(company, rule_id, type_, text, confidence):

    results.append({

        "company_id": company,
        "type": type_,
        "rule_id": rule_id,
        "text": text,
        "confidence_pct": confidence

    })


for _, row in latest_df.iterrows():

    company = row["company_id"]


    # ======================
    # PRO RULES
    # ======================


    # PRO 1
    if row["return_on_equity_pct"] > 20:

        add_result(
            company,
            "PRO_1",
            "pro",
            "Consistently high return on equity above 20% demonstrates exceptional capital efficiency",
            90
        )


    # PRO 2
    if row["free_cash_flow_cr"] > 0:

        add_result(
            company,
            "PRO_2",
            "pro",
            "Positive free cash flow indicates healthy cash generation ability",
            75
        )


    # PRO 3
    if row["debt_to_equity"] == 0:

        add_result(
            company,
            "PRO_3",
            "pro",
            "Debt-free balance sheet provides financial flexibility and eliminates interest burden",
            90
        )


    # PRO 4
    if row["revenue_cagr_5yr"] > 15:

        add_result(
            company,
            "PRO_4",
            "pro",
            "Revenue growing above 15% CAGR reflects strong business momentum",
            85
        )


    # PRO 5
    if row["operating_profit_margin_pct"] > 25:

        add_result(
            company,
            "PRO_5",
            "pro",
            "High operating margin indicates strong pricing power and cost discipline",
            80
        )


    # PRO 6
    if row["pat_cagr_5yr"] > 20:

        add_result(
            company,
            "PRO_6",
            "pro",
            "Net profit compounding above 20% creates shareholder value",
            85
        )


    # ======================
    # CON RULES
    # ======================


    # CON 1
    if row["debt_to_equity"] > 2:

        add_result(
            company,
            "CON_1",
            "con",
            "High debt-to-equity ratio indicates elevated financial leverage risk",
            85
        )


    # CON 2
    if row["free_cash_flow_cr"] < 0:

        add_result(
            company,
            "CON_2",
            "con",
            "Negative free cash flow raises concern about cash generation quality",
            75
        )


    # CON 3
    if row["return_on_equity_pct"] < 10:

        add_result(
            company,
            "CON_3",
            "con",
            "Low return on equity suggests weak capital efficiency",
            70
        )


    # CON 4
    if row["interest_coverage"] < 1.5:

        add_result(
            company,
            "CON_4",
            "con",
            "Low interest coverage indicates risk in meeting debt obligations",
            80
        )


    # CON 5
    if row["revenue_cagr_5yr"] < 5:

        add_result(
            company,
            "CON_5",
            "con",
            "Low revenue growth indicates limited business momentum",
            70
        )



# Convert output

output_df = pd.DataFrame(results)


# Keep only confidence >60

output_df = output_df[
    output_df["confidence_pct"] > 60
]


output_df.to_csv(
    OUTPUT_FILE,
    index=False
)

# Ensure every company has at least one PRO and CON

all_companies = latest_df["company_id"].unique()

existing_pro = set(
    output_df[
        output_df["type"]=="pro"
    ]["company_id"]
)

existing_con = set(
    output_df[
        output_df["type"]=="con"
    ]["company_id"]
)


fallback_rows = []


for company in all_companies:

    # Missing PRO
    if company not in existing_pro:

        fallback_rows.append({
            "company_id": company,
            "type": "pro",
            "rule_id": "PRO_DEFAULT",
            "text": "Company shows stable financial performance based on available financial indicators",
            "confidence_pct": 65
        })


    # Missing CON
    if company not in existing_con:

        fallback_rows.append({
            "company_id": company,
            "type": "con",
            "rule_id": "CON_DEFAULT",
            "text": "Company requires continuous monitoring of financial performance and future growth risks",
            "confidence_pct": 65
        })


if fallback_rows:

    output_df = pd.concat(
        [
            output_df,
            pd.DataFrame(fallback_rows)
        ],
        ignore_index=True
    )

print("\nPRO count:")
print(
    output_df[output_df["type"]=="pro"]
    ["company_id"]
    .nunique()
)

print("\nCON count:")
print(
    output_df[output_df["type"]=="con"]
    ["company_id"]
    .nunique()
)


missing_pro = set(latest_df["company_id"]) - set(
    output_df[output_df["type"]=="pro"]["company_id"]
)

missing_con = set(latest_df["company_id"]) - set(
    output_df[output_df["type"]=="con"]["company_id"]
)


print("\nMissing PRO companies:")
print(missing_pro)


print("\nMissing CON companies:")
print(missing_con)

print("==============================")
print("Pros Cons Generation Completed")
print("==============================")

print(output_df.head())

print("\nCompanies:")
print(output_df["company_id"].nunique())

print("\nSaved:")
print(OUTPUT_FILE)