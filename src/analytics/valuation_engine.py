import pandas as pd

# =====================================================
# Load datasets
# =====================================================

financial_df = pd.read_csv(
    "output/financial_ratios.csv"
)

market_df = pd.read_excel(
    "data/raw/market_cap.xlsx"
)

companies_df = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

sectors_df = pd.read_excel(
    "data/raw/sectors.xlsx"
)
print("=" * 50)
print("Datasets Loaded Successfully")
print("=" * 50)

print("Financial Ratios :", len(financial_df))
print("Market Cap       :", len(market_df))
print("Companies        :", len(companies_df))

print("\nCompanies Columns:")
print(companies_df.columns.tolist())
print("=" * 50)

# =====================================================
# Prepare Merge Keys
# =====================================================

financial_df["company_id"] = financial_df["company_id"].astype(str)
market_df["company_id"] = market_df["company_id"].astype(str)
companies_df["id"] = companies_df["id"].astype(str)

sectors_df["company_id"] = sectors_df["company_id"].astype(str)
# =====================================================
# Prepare year columns
# =====================================================

# Financial years look like "Mar 2024", "Dec 2012"
financial_df["year"] = (
    financial_df["year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

financial_df["year"] = pd.to_numeric(
    financial_df["year"],
    errors="coerce"
)

market_df["year"] = pd.to_numeric(
    market_df["year"],
    errors="coerce"
)

financial_df = financial_df.dropna(subset=["year"])
market_df = market_df.dropna(subset=["year"])

financial_df["year"] = financial_df["year"].astype(int)
market_df["year"] = market_df["year"].astype(int)

# Optional: verify the conversion
print("\nFinancial Years:")
print(financial_df["year"].head(10))

print("\nMarket Years:")
print(market_df["year"].head(10))

# =====================================================
# Merge Financial Ratios + Market Cap
# =====================================================

valuation_df = financial_df.merge(
    market_df,
    on=["company_id", "year"],
    how="left"
)

# Keep only rows where market valuation data exists
valuation_df = valuation_df.dropna(subset=["market_cap_crore"])

# =====================================================
# FCF Yield
# =====================================================

valuation_df["fcf_yield_pct"] = (
    valuation_df["free_cash_flow_cr"]
    / valuation_df["market_cap_crore"]
) * 100

print("=" * 50)
print("FCF Yield Calculated")
print("=" * 50)

print(
    valuation_df[
        [
            "company_id",
            "year",
            "free_cash_flow_cr",
            "market_cap_crore",
            "fcf_yield_pct"
        ]
    ].head(10)
)

print("\nRows after removing missing market data :", len(valuation_df))

print("\nAfter Market Merge :", len(valuation_df))

# =====================================================
# Merge Company Details
# =====================================================

valuation_df = valuation_df.merge(
    companies_df[
        [
            "id",
            "company_name"
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left"
)


valuation_df.drop(columns=["id"], inplace=True)
# =====================================================
# Merge Sector Details
# =====================================================

valuation_df = valuation_df.merge(
    sectors_df[
        [
            "company_id",
            "broad_sector",
            "sub_sector",
            "market_cap_category"
        ]
    ],
    on="company_id",
    how="left"
)

print("=" * 50)
print("Sector Information Added")
print("=" * 50)

print(
    valuation_df[
        [
            "company_name",
            "broad_sector",
            "sub_sector"
        ]
    ].head()
)

print("=" * 50)
print("Merged Dataset Successfully")
print("=" * 50)

print("Rows    :", len(valuation_df))
print("Columns :", len(valuation_df.columns))

print("\nColumns Available:")
print(valuation_df.columns.tolist())

print("\nFirst 5 Rows:\n")
print(valuation_df.head())
# =====================================================
# =====================================================
# Sector Median PE
# =====================================================

sector_pe = (
    valuation_df
    .groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
)

sector_pe.rename(
    columns={
        "pe_ratio": "sector_median_pe"
    },
    inplace=True
)

valuation_df = valuation_df.merge(
    sector_pe,
    on="broad_sector",
    how="left"
)

print("=" * 50)
print("Sector Median PE Calculated")
print("=" * 50)

print(
    valuation_df[
        [
            "company_name",
            "broad_sector",
            "pe_ratio",
            "sector_median_pe"
        ]
    ].head(10)
)

# =====================================================
# Valuation Classification
# =====================================================

def valuation_label(row):

    pe = row["pe_ratio"]
    median = row["sector_median_pe"]

    if pd.isna(pe) or pd.isna(median):
        return "Unknown"

    if pe < median * 0.7:
     return "Discount"

    elif pe > median * 1.5:
     return "Caution"

    else:
     return "Fair"


valuation_df["valuation_status"] = valuation_df.apply(
    valuation_label,
    axis=1
)

print("=" * 50)
print("Valuation Classification Completed")
print("=" * 50)

print(
    valuation_df[
        [
            "company_name",
            "broad_sector",
            "pe_ratio",
            "sector_median_pe",
            "valuation_status"
        ]
    ].head(20)
)

# =====================================================
# Composite Valuation Score
# =====================================================

valuation_df["valuation_score"] = 0

# PE Score (40 Marks)
valuation_df.loc[
    valuation_df["valuation_status"] == "Discount",
    "valuation_score"
] += 40

valuation_df.loc[
    valuation_df["valuation_status"] == "Fair",
    "valuation_score"
] += 20

# PB Score (20 Marks)
valuation_df.loc[
    valuation_df["pb_ratio"] < 3,
    "valuation_score"
] += 20

# EV / EBITDA Score (20 Marks)
valuation_df.loc[
    valuation_df["ev_ebitda"] < 15,
    "valuation_score"
] += 20

# FCF Yield Score (20 Marks)
valuation_df.loc[
    valuation_df["fcf_yield_pct"] > 3,
    "valuation_score"
] += 20

# =====================================================
# Investment Rating
# =====================================================

def investment_rating(score):

    if score >= 80:
        return "Strong Buy"

    elif score >= 60:
        return "Buy"

    elif score >= 40:
        return "Hold"

    else:
        return "Avoid"


valuation_df["investment_rating"] = (
    valuation_df["valuation_score"]
    .apply(investment_rating)
)

print("=" * 50)
print("Composite Valuation Score")
print("=" * 50)

print(
    valuation_df[
        [
            "company_name",
            "valuation_status",
            "valuation_score",
            "investment_rating"
        ]
    ].head(20)
)

print("=" * 50)

print("\nFinancial Company IDs")
print(financial_df["company_id"].head(10).tolist())
print(financial_df["company_id"].head(10).tolist())

print("\nMarket Company IDs")
print(market_df["company_id"].head(10).tolist())

print("\nFinancial Years")
print(sorted(financial_df["year"].unique())[:10])
# =====================================================
# Save Valuation Dataset
# =====================================================

valuation_df.to_csv(
    "output/valuation_summary.csv",
    index=False
)


valuation_df.to_excel(
    "output/valuation_summary.xlsx",
    index=False
)

flags = valuation_df[
    valuation_df["valuation_status"].isin(
        ["Caution","Discount"]
    )
]

flags.to_csv(
    "output/valuation_flags.csv",
    index=False
)

print("=" * 50)
print("Valuation Summary Saved Successfully")
print("=" * 50)

print("File Saved:")
print("output/valuation_summary.csv")
print("output/valuation_summary.xlsx")
print("output/valuation_flags.csv")
print("\nMarket Years")
print(sorted(market_df["year"].unique())[:10])

