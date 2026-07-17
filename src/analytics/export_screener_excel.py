import pandas as pd
import os

print("=" * 60)
print("EXPORTING SCREENER OUTPUT")
print("=" * 60)

files = {
    "Quality Compounder": "output/quality_compounder.csv",
    "Value Pick": "output/value_pick.csv",
    "Growth Accelerator": "output/growth_accelerator.csv",
    "Dividend Champion": "output/dividend_champion.csv",
    "Debt Free Bluechip": "output/debt_free_bluechip.csv",
    "Turnaround Watch": "output/turnaround_watch.csv"
}

os.makedirs("output", exist_ok=True)

output_file = "output/screener_output.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    for sheet_name, file_path in files.items():

        if os.path.exists(file_path):

            df = pd.read_csv(file_path)

            df.to_excel(
                writer,
                sheet_name=sheet_name,
                index=False
            )

            print(f"{sheet_name} : {len(df)} companies")

        else:

            print(f"Missing file : {file_path}")

print("\nExcel generated successfully!")
print(f"Saved : {output_file}")