import pytest
import torch
import math

from dfin.options.bs_torch import *


@pytest.fixture
def option_data():
    S = torch.tensor([100.], requires_grad=True)
    K = torch.tensor([110.], requires_grad=True)
    r = torch.tensor([0.05], requires_grad=True)
    t = torch.tensor([1.], requires_grad=True)
    sigma = torch.tensor([0.2], requires_grad=True)
    return S, K, r, t, sigma


def test_call_price(option_data):
    C_tensor = call_price(*option_data)
    assert math.isclose(C_tensor.item(), 6.04, rel_tol=1e-3)


def test_put_price(option_data):
    P_tensor = put_price(*option_data)
    assert math.isclose(P_tensor, 10.68, rel_tol=1e-3)


def test_put_call_parity(option_data):
    S, K, r, t, sigma = option_data
    C = call_price(*option_data)
    P = put_price(*option_data)
    assert math.isclose((C + K * torch.exp(-r*t)).item(), (S + P).item(), rel_tol=1e-3)


def test_put_call_parity_randomized():
    size = 10
    S = torch.rand(size) * 60 + 70   # Stock price [70,130)
    K = torch.rand(size) * 100 + 50  # Strike price[50,120)
    r = torch.rand(size) * 0.1       # Interest rate [0, 0.1)
    t = torch.rand(size) * 5 + 0.1   # Time to maturity [0.1, 5.1)
    sigma = torch.rand(size) * 0.4   # Volatility [0, 0.4)

    # Compute call and put prices
    C = call_price(S, K, r, t, sigma)
    P = put_price(S, K, r, t, sigma)

    # Check that the left-hand side and right-hand side are close
    assert torch.all(torch.isclose((C + K * torch.exp(-r*t)), (P + S)))


def test_call_greeks(option_data):
    S, K, r, t, sigma = option_data
    C = call_price(*option_data)
    C.backward(retain_graph=True)
    # Cdelta = torch.autograd.grad(C, S, create_graph=True)
    assert math.isclose(get_delta(S).item(),      0.450, rel_tol=1e-3)
    assert math.isclose(get_gamma(C, S).item(),   0.020, rel_tol=1e-1)
    assert math.isclose(get_rho(r).item(),       38.925, rel_tol=1e-3)
    assert math.isclose(get_theta(t).item(),     -5.904, rel_tol=1e-3)
    assert math.isclose(get_vega(sigma).item(),  39.576, rel_tol=1e-3)


def test_put_greeks(option_data):
    S, K, r, t, sigma = option_data
    P = put_price(*option_data)
    P.backward(retain_graph=True)
    # Pdelta = torch.autograd.grad(P, S, create_graph=True)
    assert math.isclose(get_delta(S).item(),     -0.550, rel_tol=1e-3)
    assert math.isclose(get_gamma(P, S).item(),   0.020, rel_tol=1e-1)
    assert math.isclose(get_rho(r).item(),      -65.711, rel_tol=1e-3)
    assert math.isclose(get_theta(t).item(),     -0.672, rel_tol=1e-3)
    assert math.isclose(get_vega(sigma).item(),  39.576, rel_tol=1e-3)


def test_delta_sum_one(option_data):
    CS, CK, Cr, Ct, Csigma = option_data
    # Alternatively... torch.tensor(CS, requires_grad=True)
    PS, PK, Pr, Pt, Psigma = torch.clone(CS).detach().requires_grad_(True), torch.clone(CK).detach(), torch.clone(Cr).detach(), torch.clone(Ct).detach(), torch.clone(Csigma).detach()
    C = call_price(CS, CK, Cr, Ct, Csigma)
    P = put_price(PS, PK, Pr, Pt, Psigma)
    C.backward()
    P.backward()
    assert math.isclose(get_delta(CS).item(),     0.450, rel_tol=1e-3)
    assert math.isclose(get_delta(PS).item(),    -0.550, rel_tol=1e-3)
    assert math.isclose(get_delta(CS).item() - get_delta(PS).item(), 1, rel_tol=1e-3)
