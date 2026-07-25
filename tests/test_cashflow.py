import sys
import os

sys.path.append(os.path.abspath("."))

from src.analytics.cashflow_kpis import *


def test_free_cash_flow():
    result = free_cash_flow(1000, -350)
    assert result == 650


def test_capex_intensity():
    result = capex_intensity(-350, 5000)

    assert round(result,2) == 7.0


def test_fcf_conversion():
    result = fcf_conversion(650,800)

    assert round(result,2) == 81.25