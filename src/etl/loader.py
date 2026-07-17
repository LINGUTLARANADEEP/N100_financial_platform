import pandas as pd
import sqlite3

conn = sqlite3.connect("db/nifty100.db")

files = {
    "companies": "data/processed/companies_clean.csv",
    "profitandloss": "data/raw/profitandloss.xlsx",
    "balancesheet": "data/raw/balancesheet.xlsx",
    "cashflow": "data/raw/cashflow.xlsx",
    "analysis": "data/raw/analysis.xlsx",
    "documents": "data/raw/documents.xlsx",

    "financial_ratios": "data/raw/financial_ratios.xlsx|header0",
    "sectors": "data/raw/sectors.xlsx|header0",

    "market_cap": "data/raw/market_cap.xlsx",
    "peer_groups": "data/raw/peer_groups.xlsx",
    "prosandcons": "data/raw/prosandcons.xlsx",
    "stock_prices": "data/raw/stock_prices.xlsx"
}

for table_name, file_path in files.items():

    # CSV Files
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    # Excel Files
    else:

        # financial_ratios.xlsx
        if "|header0" in file_path:

            file_path = file_path.replace("|header0", "")

            df = pd.read_excel(
                file_path,
                header=0
            )

        # All remaining Excel files
        else:

            df = pd.read_excel(
                file_path,
                header=1
            )

        # Remove empty rows
        df = df.dropna(how="all")

        # Remove unnamed columns
        df = df.loc[
            :,
            ~df.columns.astype(str).str.contains("^Unnamed")
        ]

    # Save into SQLite
    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {table_name} ({len(df)} rows)")

conn.close()

print("\nAll tables loaded successfully!")