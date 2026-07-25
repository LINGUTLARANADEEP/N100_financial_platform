import sys
import os

sys.path.append(os.path.abspath("."))

from src.analytics.ratios import *


def test_net_profit_margin():
    assert net_profit_margin(100, 500) == 20


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(100, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(150, 500) == 30


def test_opm_cross_check():
    calculated = operating_profit_margin(150, 500)
    assert "Mismatch" in opm_cross_check(calculated, 28)


def test_return_on_equity():
    assert return_on_equity(200, 300, 700) is not None


def test_negative_equity():
    assert return_on_equity(200, -400, 300) is None


def test_return_on_capital_employed():
    assert return_on_capital_employed(400,300,700,500) is not None


def test_return_on_assets():
    assert return_on_assets(200,1500) is not None


def test_debt_to_equity():
    assert debt_to_equity(500,300,700) > 0


def test_debt_free():
    assert debt_to_equity(0,300,700) == 0


def test_high_leverage():
    assert high_leverage_flag(6,"Technology") == True


def test_financial_sector():
    assert high_leverage_flag(6,"Financials") == False


def test_interest_coverage():
    assert interest_coverage(500,100,100) == 6


def test_debt_free_label():
    assert icr_label(None) == "Debt Free"


def test_icr_warning():
    assert icr_warning(1.2) == True


def test_net_debt():
    assert net_debt(1000,250) == 750


def test_asset_turnover():
    assert asset_turnover(5000,2500) == 2