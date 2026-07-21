import pandas as pd
import os


INPUT_FILE = "output/financial_ratios.csv"

OUTPUT_FILE = "output/cashflow_intelligence.xlsx"
DISTRESS_FILE = "output/distress_alerts.csv"


# ==============================
# Helper Functions
# ==============================

def free_cash_flow(operating_activity, investing_activity):
    """
    FCF = CFO + CFI
    """
    return operating_activity + investing_activity



def capex_intensity(investing_activity, sales):

    if sales == 0:
        return None

    return (abs(investing_activity) / sales) * 100



def fcf_conversion(fcf, operating_activity):

    if operating_activity == 0:
        return None

    return (fcf / operating_activity) * 100



def cfo_quality_label(score):

    if score > 1:
        return "High Quality"

    elif score >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"



def capex_label(value):

    if value < 3:
        return "Asset Light"

    elif value <= 8:
        return "Moderate"

    else:
        return "Capital Intensive"



# ==============================
# Load Data
# ==============================

df = pd.read_csv(INPUT_FILE)


print("Loaded Financial Data")
print(df.shape)


df = df.sort_values(
    ["company_id","year"]
)



# ==============================
# Free Cash Flow
# ==============================

df["free_cash_flow"] = df.apply(
    lambda x:
    free_cash_flow(
        x["cash_from_operations_cr"],
        x["investing_activity"]
    ),
    axis=1
)



# ==============================
# CFO Quality Score
# ==============================

df["cfo_pat_ratio"] = (
    df["cash_from_operations_cr"]
    /
    df["net_profit"].replace(0,None)
)


cfo_quality = (
    df.groupby("company_id")
    .tail(5)
    .groupby("company_id")
    ["cfo_pat_ratio"]
    .mean()
    .reset_index()
)


cfo_quality.rename(
    columns={
        "cfo_pat_ratio":
        "cfo_quality_score"
    },
    inplace=True
)


cfo_quality["cfo_quality_label"] = (
    cfo_quality["cfo_quality_score"]
    .apply(cfo_quality_label)
)



# ==============================
# Latest Year Data
# ==============================

latest = (
    df.groupby("company_id")
    .tail(1)
)



# ==============================
# CapEx Intensity
# ==============================

latest["capex_intensity_pct"] = latest.apply(
    lambda x:
    capex_intensity(
        x["investing_activity"],
        x["sales"]
    ),
    axis=1
)


latest["capex_label"] = (
    latest["capex_intensity_pct"]
    .apply(capex_label)
)



# ==============================
# Distress Detection
# CFO < 0 and Financing > 0
# ==============================

latest["distress_flag"] = (
    (latest["cash_from_operations_cr"] < 0)
    &
    (latest["financing_activity"] > 0)
)



distress = latest[
    latest["distress_flag"]
]


distress[
[
"company_id",
"cash_from_operations_cr",
"financing_activity",
"net_profit"
]
].to_csv(
    DISTRESS_FILE,
    index=False
)



# ==============================
# Deleveraging Detection
# ==============================

latest["previous_borrowings"] = (
    df.groupby("company_id")
    ["borrowings"]
    .shift(1)
)


latest["deleveraging_flag"] = (
    (latest["financing_activity"] < 0)
    &
    (
        latest["borrowings"]
        <
        latest["previous_borrowings"]
    )
)



# ==============================
# Merge Final Output
# ==============================

final = latest.merge(
    cfo_quality,
    on="company_id",
    how="left"
)


final["fcf_conversion_pct"] = final.apply(
    lambda x:
    fcf_conversion(
        x["free_cash_flow"],
        x["cash_from_operations_cr"]
    ),
    axis=1
)



output = final[
[
"company_id",
"cfo_quality_score",
"cfo_quality_label",
"capex_intensity_pct",
"capex_label",
"free_cash_flow",
"fcf_conversion_pct",
"distress_flag",
"deleveraging_flag"
]
]



output.to_excel(
    OUTPUT_FILE,
    index=False
)



print("\nCash Flow Intelligence Completed")

print("Companies:",
      output["company_id"].nunique())


print("\nGenerated:")
print(OUTPUT_FILE)
print(DISTRESS_FILE)