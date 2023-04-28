import pytest
import math

from options.bsiv_scipy import *


@pytest.fixture
def call_option_data():
    S = 100
    K = 110
    r = 0.05
    t = 1
    price = 6.040088129724
    return S, K, r, t, price


@pytest.fixture
def put_option_data():
    S = 100
    K = 110
    r = 0.05
    t = 1
    price = 10.675324824803
    return S, K, r, t, price


def test_call_implied_volatility(call_option_data):
    sigma = call_implied_volatility(*call_option_data)
    assert math.isclose(sigma, 0.2, rel_tol=1e-12)


def test_put_implied_volatility(put_option_data):
    sigma = put_implied_volatility(*put_option_data)
    assert math.isclose(sigma, 0.2, rel_tol=1e-12)
