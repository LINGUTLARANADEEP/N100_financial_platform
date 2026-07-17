from scorecard import *


print("Loading Reports...\n")

cashflow, stock, sector = load_reports()

print("Cashflow Columns:")
print(cashflow.columns.tolist())

print("\nStock Columns:")
print(stock.columns.tolist())

print("\nSector Columns:")
print(sector.columns.tolist())

scorecard = build_scorecard(
    cashflow,
    stock,
    sector
)

save_scorecard(scorecard)

print("\nDone.")