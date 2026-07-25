import sys
import os

sys.path.append(os.path.abspath("."))

from src.analytics.cagr import *


def test_normal_cagr():
    result = calculate_cagr(100, 200, 5)
    assert result is not None


def test_zero_base():
    result = calculate_cagr(0, 200, 5)
    assert result[0] is None
    assert result[1] == "ZERO_BASE"


def test_decline_to_loss():
    result = calculate_cagr(100, -50, 5)
    assert result[0] is None
    assert result[1] == "DECLINE_TO_LOSS"


def test_turnaround():
    result = calculate_cagr(-100, 200, 5)
    assert result[0] is None
    assert result[1] == "TURNAROUND"


def test_both_negative():
    result = calculate_cagr(-100, -200, 5)
    assert result[0] is None
    assert result[1] == "BOTH_NEGATIVE"

def test_insufficient_years():
    result = calculate_cagr(100, 200, 0)
    assert result[0] is None
    assert result[1] == "INSUFFICIENT"


def test_revenue_cagr():
    result = revenue_cagr(100, 180, 5)
    assert result is not None


def test_pat_cagr():
    result = pat_cagr(50, 120, 5)
    assert result is not None


def test_eps_cagr():
    result = eps_cagr(10, 25, 5)
    assert result is not None