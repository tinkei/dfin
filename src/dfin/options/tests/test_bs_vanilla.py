import pytest
import math

from dfin.options.bs_vanilla import *


@pytest.fixture
def option_data():
    S = 100
    K = 110
    r = 0.05
    t = 1
    sigma = 0.2
    return S, K, r, t, sigma


def test_call_price(option_data):
    C = call_price(*option_data)
    assert math.isclose(C, 6.04, rel_tol=1e-3)


def test_put_price(option_data):
    P = put_price(*option_data)
    assert math.isclose(P, 10.68, rel_tol=1e-3)


def test_call_put_price(option_data):
    C, P = call_put_price(*option_data)
    assert math.isclose(C, 6.04, rel_tol=1e-3)
    assert math.isclose(P, 10.68, rel_tol=1e-3)


def test_put_call_parity(option_data):
    S, K, r, t, sigma = option_data
    C = call_price(*option_data)
    P = put_price(*option_data)
    C2, P2 = call_put_price(*option_data)
    assert math.isclose(C, C2, rel_tol=1e-3)
    assert math.isclose(P, P2, rel_tol=1e-3)
    assert math.isclose(C + K * math.exp(-r*t), S + P, rel_tol=1e-3)
