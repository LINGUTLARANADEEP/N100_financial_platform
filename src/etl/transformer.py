import pandas as pd

companies = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

companies = companies[
    [
        "id",
        "company_name",
        "website",
        "face_value",
        "book_value",
        "roce_percentage",
        "roe_percentage"
    ]
]

companies["company_name"] = companies["company_name"].str.strip()
companies["website"] = companies["website"].str.strip()

companies["website"] = companies["website"].fillna("Not Available")
companies["face_value"] = companies["face_value"].fillna(0)
companies["book_value"] = companies["book_value"].fillna(0)
companies["roce_percentage"] = companies["roce_percentage"].fillna(0)
companies["roe_percentage"] = companies["roe_percentage"].fillna(0)

print("\nMissing Values:")
print(companies.isnull().sum())

companies.to_csv(
    "data/processed/companies_clean.csv",
    index=False
)

print("Transformation completed successfully!")
print(companies.head())