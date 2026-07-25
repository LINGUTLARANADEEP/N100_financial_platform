import sys
import os

sys.path.append(os.path.abspath("."))

from src.analytics.stock_analytics import *


def test_current_price():
    prices = [100, 120, 150]

    result = current_price(prices)

    assert result == 150


def test_highest_price():
    prices = [100, 250, 180]

    result = highest_price(prices)

    assert result == 250


def test_lowest_price():
    prices = [100, 50, 180]

    result = lowest_price(prices)

    assert result == 50


def test_annual_return():
    # 13 months data because function needs years*12 months
    prices = [
        100,100,100,100,100,100,
        100,100,100,100,100,100,
        120
    ]

    result = annual_return(prices,1)

    assert round(result,2) == 20.00


def test_annual_return_insufficient_data():

    prices = [100,110,120]

    result = annual_return(prices,1)

    assert result == 0.0