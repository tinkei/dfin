import pytest
import torch

from dfin.optimize import gradient_descent, lbfgs, secant, newton, halley
from dfin.options.iv_torch import call_implied_volatility, put_implied_volatility

# torch.set_default_tensor_type('torch.DoubleTensor')
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# torch.set_default_device(device)


@pytest.fixture
def call_option_data():
    S = torch.tensor([100.], requires_grad=False)
    K = torch.tensor([110.], requires_grad=False)
    r = torch.tensor([0.05], requires_grad=False)
    t = torch.tensor([1.], requires_grad=False)
    price = torch.tensor([6.040088129724], requires_grad=False)
    sigma0 = torch.tensor(0.5, requires_grad=True)
    # S = 100
    # K = 110
    # r = 0.05
    # t = 1
    # price = 6.040088129724
    return S, K, r, t, price, sigma0


@pytest.fixture
def put_option_data():
    S = torch.tensor([100.], requires_grad=False)
    K = torch.tensor([110.], requires_grad=False)
    r = torch.tensor([0.05], requires_grad=False)
    t = torch.tensor([1.], requires_grad=False)
    price = torch.tensor([10.675324824803], requires_grad=False)
    sigma0 = torch.tensor(0.5, requires_grad=True)
    # S = 100
    # K = 110
    # r = 0.05
    # t = 1
    # price = 10.675324824803
    return S, K, r, t, price, sigma0


def test_call_implied_volatility(call_option_data):

    atol = 1e-6

    print('Running `test_call_implied_volatility` with `gradient_descent`')
    sigma = call_implied_volatility(*call_option_data, optim=gradient_descent, atol=atol)
    print(f'Result of `test_call_implied_volatility` with `gradient_descent`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)

    print('Running `test_call_implied_volatility` with `lbfgs`')
    sigma = call_implied_volatility(*call_option_data, optim=lbfgs, atol=atol)
    print(f'Result of `test_call_implied_volatility` with `lbfgs`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)

    print('Running `test_call_implied_volatility` with `secant`')
    sigma = call_implied_volatility(*call_option_data, optim=secant, atol=atol)
    print(f'Result of `test_call_implied_volatility` with `secant`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)

    print('Running `test_call_implied_volatility` with `newton`')
    sigma = call_implied_volatility(*call_option_data, optim=newton, atol=atol)
    print(f'Result of `test_call_implied_volatility` with `newton`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)

    print('Running `test_call_implied_volatility` with `halley`')
    sigma = call_implied_volatility(*call_option_data, optim=halley, atol=atol)
    print(f'Result of `test_call_implied_volatility` with `halley`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)



def test_put_implied_volatility(put_option_data):

    atol = 1e-6

    print('Running `test_put_implied_volatility` with `gradient_descent`')
    sigma = put_implied_volatility(*put_option_data, optim=gradient_descent, atol=atol)
    print(f'Result of `test_put_implied_volatility` with `gradient_descent`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)

    print('Running `test_put_implied_volatility` with `lbfgs`')
    sigma = put_implied_volatility(*put_option_data, optim=lbfgs, atol=atol)
    print(f'Result of `test_put_implied_volatility` with `lbfgs`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)

    print('Running `test_put_implied_volatility` with `secant`')
    sigma = put_implied_volatility(*put_option_data, optim=secant, atol=atol)
    print(f'Result of `test_put_implied_volatility` with `secant`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)

    print('Running `test_put_implied_volatility` with `newton`')
    sigma = put_implied_volatility(*put_option_data, optim=newton, atol=atol)
    print(f'Result of `test_put_implied_volatility` with `newton`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)

    print('Running `test_put_implied_volatility` with `halley`')
    sigma = put_implied_volatility(*put_option_data, optim=halley, atol=atol)
    print(f'Result of `test_put_implied_volatility` with `halley`: {sigma.item()}')
    assert torch.isclose(sigma, torch.tensor([0.2]), rtol=1e-6, atol=atol)


def speed_comparison():

    import timeit
    from functools import partial

    S = torch.tensor([100.], requires_grad=False)
    K = torch.tensor([110.], requires_grad=False)
    r = torch.tensor([0.05], requires_grad=False)
    t = torch.tensor([1.], requires_grad=False)
    price = torch.tensor([6.040088129724], requires_grad=False)
    sigma0 = torch.tensor(0.5, requires_grad=True)
    # print(f'S is on device {S.device}')

    number = 100

    times = timeit.Timer(partial(call_implied_volatility, S, K, r, t, price, sigma0, gradient_descent)).repeat(repeat=10, number=(number//10))
    time_taken = min(times) / (number//10)
    print(f'Adam takes {time_taken*1000:.4f} ms.')

    times = timeit.Timer(partial(call_implied_volatility, S, K, r, t, price, sigma0, lbfgs)).repeat(repeat=10, number=number)
    time_taken = min(times) / number
    print(f'LBFGS takes {time_taken*1000:.4f} ms.')

    times = timeit.Timer(partial(call_implied_volatility, S, K, r, t, price, sigma0, secant)).repeat(repeat=10, number=number)
    time_taken = min(times) / number
    print(f'Secant takes {time_taken*1000:.4f} ms.')

    times = timeit.Timer(partial(call_implied_volatility, S, K, r, t, price, sigma0, newton)).repeat(repeat=10, number=number)
    time_taken = min(times) / number
    print(f'Newton takes {time_taken*1000:.4f} ms.')

    times = timeit.Timer(partial(call_implied_volatility, S, K, r, t, price, sigma0, halley)).repeat(repeat=10, number=number)
    time_taken = min(times) / number
    print(f'Halley takes {time_taken*1000:.4f} ms.')



if __name__ == "__main__":

    speed_comparison()
