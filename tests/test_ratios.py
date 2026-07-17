import sys
import os

sys.path.append(os.path.abspath("."))

from src.analytics.ratios import *

print("===== KPI UNIT TESTS =====")

# Test 1
print("\nTest 1 - NPM")
print(net_profit_margin(100,500))

# Test 2
print("\nTest 2 - Sales = 0")
print(net_profit_margin(100,0))

# Test 3
print("\nTest 3 - OPM")
print(operating_profit_margin(150,500))

# Test 4
print("\nTest 4 - OPM Cross Check")
calculated = operating_profit_margin(150,500)
print(opm_cross_check(calculated,28))

# Test 5
print("\nTest 5 - ROE")
print(return_on_equity(200,300,700))

# Test 6
print("\nTest 6 - Negative Equity")
print(return_on_equity(200,-400,300))

# Test 7
print("\nTest 7 - ROCE")
print(return_on_capital_employed(400,300,700,500))

# Test 8
print("\nTest 8 - ROA")
print(return_on_assets(200,1500))

# Test 9
print("\nTest 9 - Debt to Equity")
print(debt_to_equity(500,300,700))

# Test 10
print("\nTest 10 - Debt Free")
print(debt_to_equity(0,300,700))

# Test 11
print("\nTest 11 - High Leverage")
print(high_leverage_flag(6,"Technology"))

# Test 12
print("\nTest 12 - Financial Sector")
print(high_leverage_flag(6,"Financials"))

# Test 13
print("\nTest 13 - Interest Coverage")
print(interest_coverage(500,100,100))

# Test 14
print("\nTest 14 - Debt Free Label")
print(icr_label(None))

# Test 15
print("\nTest 15 - ICR Warning")
print(icr_warning(1.2))

# Test 16
print("\nTest 16 - Net Debt")
print(net_debt(1000,250))

# Test 17
print("\nTest 17 - Asset Turnover")
print(asset_turnover(5000,2500))