import pandas as pd
import os


INPUT_FILE = "output/capital_allocation.csv"

CASHFLOW_FILE = "output/cashflow_intelligence.xlsx"

SUMMARY_OUTPUT = "output/capital_allocation_summary.csv"

CHANGE_OUTPUT = "output/pattern_changes.csv"


# ============================
# Load Data
# ============================

df = pd.read_csv(INPUT_FILE)

print("Capital Allocation Data Loaded")
print(df.shape)


# ============================
# Latest Year Distribution
# ============================

df["year"] = pd.to_datetime(df["year"], errors="coerce")


latest_year = df["year"].max()

latest_df = df[df["year"] == latest_year]


summary = (
    latest_df["pattern_label"]
    .value_counts()
    .reset_index()
)

summary.columns = [
    "pattern_label",
    "company_count"
]


summary.to_csv(
    SUMMARY_OUTPUT,
    index=False
)


print("\nLatest Year Pattern Distribution")
print(summary)



# ============================
# Pattern Change Detection
# ============================

df = df.sort_values(
    ["company_id", "year"]
)


df["previous_pattern"] = (
    df.groupby("company_id")["pattern_label"]
    .shift(1)
)


changes = df[
    df["previous_pattern"].notna()
    &
    (df["previous_pattern"] != df["pattern_label"])
]


pattern_changes = changes[
    [
        "company_id",
        "year",
        "previous_pattern",
        "pattern_label"
    ]
]


pattern_changes.columns = [
    "company_id",
    "year",
    "old_pattern",
    "new_pattern"
]


pattern_changes.to_csv(
    CHANGE_OUTPUT,
    index=False
)


print("\nPattern Changes:")
print(pattern_changes.head())



# ============================
# Update Cashflow Intelligence
# ============================

if os.path.exists(CASHFLOW_FILE):

    cashflow = pd.read_excel(
        CASHFLOW_FILE
    )


    latest_pattern = (
        latest_df[
            [
                "company_id",
                "pattern_label"
            ]
        ]
    )


    latest_pattern = latest_pattern.rename(
        columns={
            "pattern_label":
            "capital_allocation_label"
        }
    )


    updated = cashflow.merge(
        latest_pattern,
        on="company_id",
        how="left"
    )


    updated.to_excel(
        CASHFLOW_FILE,
        index=False
    )


    print(
        "\nUpdated cashflow_intelligence.xlsx"
    )


else:

    print(
        "cashflow_intelligence.xlsx not found"
    )



print("\nDay 32 Capital Allocation Report Completed")