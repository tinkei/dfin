"""Implementation of Implied Volatility optimization under Black-Scholes with SciPy."""

from scipy.stats import norm
from scipy.optimize import newton

from options.bs_vanilla import call_price, put_price


def call_implied_volatility(S:float, K:float, r:float, t:float, price:float) -> float:
    """
    Calculates the implied volatility of a call option using the Black-Scholes model.

    Parameters
    ----------
    S : float
        Current underlying price
    K : float
        Option strike price
    r : float
        Risk-free interest rate
    t : float
        Time to expiry
    price : float
        Observed price of the call option

    Returns
    -------
    float
        Implied volatility of the underlying asset
    """
    def bs_objective(sigma):
        """
        Objective function to minimize to find the implied volatility.
        """
        return call_price(S, K, r, t, sigma) - price

    # Use the Newton-Raphson method to find the root (i.e. implied volatility) of the objective function
    implied_vol = newton(bs_objective, 0.5)

    return implied_vol


def put_implied_volatility(S:float, K:float, r:float, t:float, price:float) -> float:
    """
    Calculates the implied volatility of a put option using the Black-Scholes model.

    Parameters
    ----------
    S : float
        Current underlying price
    K : float
        Option strike price
    r : float
        Risk-free interest rate
    t : float
        Time to expiry
    price : float
        Observed price of the put option

    Returns
    -------
    float
        Implied volatility of the underlying asset
    """
    def bs_objective(sigma):
        """
        Objective function to minimize to find the implied volatility.
        """
        return put_price(S, K, r, t, sigma) - price

    # Use the Newton-Raphson method to find the root (i.e. implied volatility) of the objective function
    implied_vol = newton(bs_objective, 0.5)

    return implied_vol
