import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analytics.cagr import *

print("====== CAGR UNIT TESTS ======\n")

print("Test 1 - Normal CAGR")
print(calculate_cagr(100, 200, 5))

print("\nTest 2 - Zero Base")
print(calculate_cagr(0, 200, 5))

print("\nTest 3 - Decline to Loss")
print(calculate_cagr(100, -50, 5))

print("\nTest 4 - Turnaround")
print(calculate_cagr(-100, 200, 5))

print("\nTest 5 - Both Negative")
print(calculate_cagr(-100, -200, 5))

print("\nTest 6 - Insufficient Years")
print(calculate_cagr(100, 200, 0))

print("\nTest 7 - Revenue CAGR")
print(revenue_cagr(100, 180, 5))

print("\nTest 8 - PAT CAGR")
print(pat_cagr(50, 120, 5))

print("\nTest 9 - EPS CAGR")
print(eps_cagr(10, 25, 5))