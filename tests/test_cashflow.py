import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from src.analytics.cashflow_kpis import *

print("===== CASH FLOW KPI TESTS =====")

print("\nTest 1 - Free Cash Flow")
fcf = free_cash_flow(1000, -350)
print(fcf)

print("\nTest 2 - CapEx Intensity")
print(capex_intensity(-350, 5000))

print("\nTest 3 - FCF Conversion")
print(fcf_conversion(fcf, 800))