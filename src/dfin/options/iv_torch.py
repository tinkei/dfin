"""Implementation of Implied Volatility optimization under Black-Scholes with PyTorch."""
import torch
from typing import Callable

from dfin.options.bs_torch import call_price, put_price


ObjectiveType = Callable[[torch.Tensor],torch.Tensor]
OptimizationType = Callable[[ObjectiveType, torch.Tensor], torch.Tensor]


def call_implied_volatility(S:torch.Tensor, K:torch.Tensor, r:torch.Tensor, t:torch.Tensor, price:torch.Tensor, sigma0:torch.Tensor, optim:OptimizationType, atol:float=1e-6, max_iter:int=1000) -> torch.Tensor:
    """
    Calculates the implied volatility of a European call option using the Black-Scholes model.

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
    price : torch.Tensor
        Observed price of the call option
    sigma0 : torch.Tensor
        Initial guess for volatility.
    optim : Callable
        Optimization method that takes an objective function and an initial guess as inputs.
        Imported from `dfin.optimize`.
    atol : float
        The tolerance of the optimization target. Default: 1e-6.
        Does not apply to LBFGS directly.
    max_iter : int
        The maximum number of iterations to perform backpropagation. Default: 1000.
        Does not apply to LBFGS directly.

    Returns
    -------
    torch.Tensor
        Implied volatility of the underlying asset
    """
    def bs_objective(sigma:torch.Tensor) -> torch.Tensor:
        """
        Objective function to minimize to find the implied volatility.
        """
        return call_price(S, K, r, t, sigma) - price

    # Use the Newton-Raphson method to find the root (i.e. implied volatility) of the objective function
    implied_vol = optim(bs_objective, sigma0, atol, max_iter)

    return implied_vol


def put_implied_volatility(S:torch.Tensor, K:torch.Tensor, r:torch.Tensor, t:torch.Tensor, price:torch.Tensor, sigma0:torch.Tensor, optim:OptimizationType, atol:float=1e-6, max_iter:int=1000) -> torch.Tensor:
    """
    Calculates the implied volatility of a European put option using the Black-Scholes model.

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
    price : torch.Tensor
        Observed price of the put option
    sigma0 : torch.Tensor
        Initial guess for volatility.
    optim : Callable
        Optimization method that takes an objective function and an initial guess as inputs.
        Imported from `dfin.optimize`.
    atol : float
        The tolerance of the optimization target. Default: 1e-6.
        Does not apply to LBFGS directly.
    max_iter : int
        The maximum number of iterations to perform backpropagation. Default: 1000.
        Does not apply to LBFGS directly.

    Returns
    -------
    torch.Tensor
        Implied volatility of the underlying asset
    """
    def bs_objective(sigma:torch.Tensor) -> torch.Tensor:
        """
        Objective function to minimize to find the implied volatility.
        """
        return put_price(S, K, r, t, sigma) - price

    # Use the Newton-Raphson method to find the root (i.e. implied volatility) of the objective function
    implied_vol = optim(bs_objective, sigma0, atol, max_iter)

    return implied_vol
