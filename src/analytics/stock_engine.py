import pandas as pd
from stock_analytics import *

df = pd.read_excel(
    "data/raw/stock_prices.xlsx",
    header=None
)

# Assign correct column names
df.columns = [
    "id",
    "company_id",
    "date",
    "open_price",
    "high_price",
    "low_price",
    "close_price",
    "volume",
    "adjusted_close"
]

# Remove duplicate header row if present
if str(df.iloc[0]["company_id"]).lower() == "company_id":
    df = df.iloc[1:].reset_index(drop=True)

# Convert adjusted_close to numeric
df["adjusted_close"] = pd.to_numeric(
    df["adjusted_close"],
    errors="coerce"
)

print("========== STOCK PRICE REPORT ==========\n")

results = []

for company, group in df.groupby("company_id"):

    prices = group["adjusted_close"].dropna().tolist()

    # Skip companies with no prices
    if len(prices) == 0:
        continue

    current = current_price(prices)
    highest = highest_price(prices)
    lowest = lowest_price(prices)

    one_year = annual_return(prices, 1)
    three_year = annual_return(prices, 3)
    five_year = annual_return(prices, 5)

    print(company)
    print(f"Current Price : {current:.2f}")
    print(f"Highest Price : {highest:.2f}")
    print(f"Lowest Price  : {lowest:.2f}")
    print(f"1 Year Return : {one_year:.2f}%")
    print(f"3 Year Return : {three_year:.2f}%")
    print(f"5 Year Return : {five_year:.2f}%")
    print("-" * 40)

    results.append({
        "Company": company,
        "Current Price": current,
        "Highest Price": highest,
        "Lowest Price": lowest,
        "1Y Return %": one_year,
        "3Y Return %": three_year,
        "5Y Return %": five_year
    })



report = pd.DataFrame(results)

report.to_csv(
    "output/stock_analytics.csv",
    index=False
)

print("\n===================================")
print("Stock Analytics Report Saved")
print("Location : output/stock_analytics.csv")
print("===================================")