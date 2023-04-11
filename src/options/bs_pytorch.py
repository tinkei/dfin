import torch
from typing import Tuple

def normal_cdf(x:torch.Tensor) -> torch.Tensor:
    """
    Computes the cumulative distribution function of the standard normal distribution.

    Parameters
    ----------
    x : torch.Tensor
        Cumulative probability that the random variable X takes on a value less than or equal to x (i.e. $F(x) = P(X<=x)$)

    Returns
    -------
    torch.Tensor
        The value of the CDF at x
    """

    return (1.0 + torch.erf(x / torch.sqrt(torch.tensor([2.0])))) / 2.0


def call_price(S:torch.Tensor, K:torch.Tensor, r:torch.Tensor, t:torch.Tensor, sigma:torch.Tensor) -> torch.Tensor:
    """
    Computes the theoretical price of a European call option using the Black-Scholes formula.

    Parameters
    ----------
    S : torch.Tensor
        Current underlying price
    K : torch.Tensor
        Option strike price
    r : torch.Tensor
        Risk-free interest rate
    t : torch.Tensor
        Time to expiry
    sigma : torch.Tensor
        Volatility of the underlying asset

    Returns
    -------
    torch.Tensor
        Theoretical price of the call option
    """

    d1 = (torch.log(S / K) + (r + sigma**2 / 2) * t) / (sigma * torch.sqrt(t))
    d2 = d1 - sigma * torch.sqrt(t)

    N_d1 = normal_cdf(d1)
    N_d2 = normal_cdf(d2)

    C = S * N_d1 - K * torch.exp(-r*t) * N_d2

    return C


def put_price(S:torch.Tensor, K:torch.Tensor, r:torch.Tensor, t:torch.Tensor, sigma:torch.Tensor) -> torch.Tensor:
    """
    Computes the theoretical price of a European put option using the Black-Scholes formula.

    Parameters
    ----------
    S : torch.Tensor
        Current underlying price
    K : torch.Tensor
        Option strike price
    r : torch.Tensor
        Risk-free interest rate
    t : torch.Tensor
        Time to expiry
    sigma : torch.Tensor
        Volatility of the underlying asset

    Returns
    -------
    torch.Tensor
        Theoretical price of the call option
    """

    d1 = (torch.log(S / K) + (r + sigma**2 / 2) * t) / (sigma * torch.sqrt(t))
    d2 = d1 - sigma * torch.sqrt(t)

    N_minus_d1 = normal_cdf(-d1)
    N_minus_d2 = normal_cdf(-d2)

    P = K * torch.exp(-r*t) * N_minus_d2 - S * N_minus_d1

    return P


# def call_put_price(S:torch.Tensor, K:torch.Tensor, r:torch.Tensor, t:torch.Tensor, sigma:torch.Tensor) -> Tuple[torch.Tensor,torch.Tensor]:
# Not implemented, because the inputs need to be separate variables for each of call and put output tensors.


def get_delta(S:torch.Tensor) -> torch.Tensor:
    """
    Computes the delta of a European option using autograd.

    Parameters
    ----------
    S : torch.Tensor
        Current underlying price

    Returns
    -------
    torch.Tensor
        Delta of the option
    """
    return S.grad


def get_gamma(option:torch.Tensor, S:torch.Tensor) -> torch.Tensor:
    """
    Computes the gamma of a European option using autograd.

    Parameters
    ----------
    option : torch.Tensor
        Call or put option
    S : torch.Tensor
        Current underlying price

    Returns
    -------
    torch.Tensor
        Gamma of the option
    """
    delta = torch.autograd.grad(option, S, create_graph=True)
    return torch.autograd.grad(delta, S, create_graph=True)[0]


def get_rho(r:torch.Tensor) -> torch.Tensor:
    """
    Computes the rho of a European option using autograd.

    Parameters
    ----------
    r : torch.Tensor
        Risk-free interest rate

    Returns
    -------
    torch.Tensor
        Rho of the option
    """
    return r.grad


def get_theta(t:torch.Tensor) -> torch.Tensor:
    """
    Computes the theta of a European option using autograd.

    Parameters
    ----------
    t : torch.Tensor
        Time to expiry

    Returns
    -------
    torch.Tensor
        Theta of the option
    """
    # TODO: Investigate why theta gives opposite sign.
    return -t.grad


def get_vega(sigma:torch.Tensor) -> torch.Tensor:
    """
    Computes the vega of a European option using autograd.

    Parameters
    ----------
    sigma : torch.Tensor
        Volatility of the underlying asset

    Returns
    -------
    torch.Tensor
        Vega of the option
    """
    return sigma.grad


if __name__ == "__main__":

    # Sample use case
    # Obtain all option greeks directly from autograd!
    CS = torch.tensor([100.], requires_grad=True)
    CK = torch.tensor([110.], requires_grad=True)
    Cr = torch.tensor([0.05], requires_grad=True)
    Ct = torch.tensor([1.], requires_grad=True)
    Csigma = torch.tensor([0.2], requires_grad=True)
    PS = torch.tensor([100.], requires_grad=True)
    PK = torch.tensor([110.], requires_grad=True)
    Pr = torch.tensor([0.05], requires_grad=True)
    Pt = torch.tensor([1.], requires_grad=True)
    Psigma = torch.tensor([0.2], requires_grad=True)

    C = call_price(CS, CK, Cr, Ct, Csigma)
    P = put_price(PS, PK, Pr, Pt, Psigma)
    C.backward(retain_graph=True)
    P.backward(retain_graph=True)
    # To evaluate second derivatives, instead of using `.backward()`,
    # use `torch.autograd.grad()` to compute gradients.
    Cdelta = torch.autograd.grad(C, CS, create_graph=True)
    Pdelta = torch.autograd.grad(P, PS, create_graph=True)

    print(f"Theoretical price of a call option: ${C.item():.4f}")
    print(f"Theoretical price of a put option : ${P.item():.4f}")

    print(f"Gradients (Option Greeks):")

    print(f"dC/dS   (delta) : {CS.grad.item():+.4f}") # ==  0.450
    print(f"dP/dS   (delta) : {PS.grad.item():+.4f}") # == -0.550

    print(f"d2C/dS2 (gamma) : {torch.autograd.grad(Cdelta, CS, create_graph=True)[0].item():+.4f}") # == 0.020
    print(f"d2P/dS2 (gamma) : {torch.autograd.grad(Pdelta, PS, create_graph=True)[0].item():+.4f}") # == 0.020

    print(f"dC/dK   (N/A)   : {CK.grad.item():+.4f}")
    print(f"dP/dK   (N/A)   : {PK.grad.item():+.4f}")

    print(f"dC/dr   (rho)   : {Cr.grad.item():+.4f}") # ==  38.925
    print(f"dP/dr   (rho)   : {Pr.grad.item():+.4f}") # == -65.711

    # Why the sign is wrong?
    print(f"dC/dt   (theta) : {-Ct.grad.item():+.4f}") # == -5.904
    print(f"dP/dt   (theta) : {-Pt.grad.item():+.4f}") # == -5.904

    print(f"dC/dσ   (vega)  : {Csigma.grad.item():+.4f}") # == 39.576
    print(f"dP/dσ   (vega)  : {Psigma.grad.item():+.4f}") # == 39.576

    print(f"dC/dS - dP/dS == 1? {CS.grad.item() - PS.grad.item():.4f}")
