import pytest
import math

from dfin.options.iv_scipy import *


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


def speed_comparison():

    import timeit
    from functools import partial

    S = 100
    K = 110
    r = 0.05
    t = 1
    price = 6.040088129724

    number = 5000

    times = timeit.Timer(partial(call_implied_volatility, S, K, r, t, price)).repeat(repeat=10, number=number)
    time_taken = min(times) / number
    print(f'Newton takes {time_taken*1000:.4f} ms.')



if __name__ == "__main__":

    speed_comparison()
