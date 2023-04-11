"""Implementation of Black-Scholes option pricing formula with plain Python."""

import math
from typing import Tuple


def normal_cdf(x:float) -> float:
    """
    Computes the cumulative distribution function of the standard normal distribution.

    Parameters
    ----------
    x : float
        Cumulative probability that the random variable X takes on a value less than or equal to x (i.e. $F(x) = P(X<=x)$)

    Returns
    -------
    float
        The value of the CDF at x
    """

    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def call_price(S:float, K:float, r:float, t:float, sigma:float) -> float:
    """
    Computes the theoretical price of a European call option using the Black-Scholes formula.

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
    sigma : float
        Volatility of the underlying asset

    Returns
    -------
    float
        Theoretical price of the call option
    """

    d1 = (math.log(S / K) + (r + sigma**2 / 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)

    N_d1 = normal_cdf(d1)
    N_d2 = normal_cdf(d2)

    C = S * N_d1 - K * math.exp(-r*t) * N_d2

    return C


def put_price(S:float, K:float, r:float, t:float, sigma:float) -> float:
    """
    Computes the theoretical price of a European put option using the Black-Scholes formula.

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
    sigma : float
        Volatility of the underlying asset

    Returns
    -------
    float
        Theoretical price of the call option
    """

    d1 = (math.log(S / K) + (r + sigma**2 / 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)

    N_minus_d1 = normal_cdf(-d1)
    N_minus_d2 = normal_cdf(-d2)

    P = K * math.exp(-r*t) * N_minus_d2 - S * N_minus_d1

    return P


def call_put_price(S:float, K:float, r:float, t:float, sigma:float) -> Tuple[float,float]:
    """
    Computes the theoretical price of both European call and put options using the Black-Scholes formula.

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
    sigma : float
        Volatility of the underlying asset

    Returns
    -------
    Tuple[float,float]
        Theoretical price of the call and put options, respectively
    """

    d1 = (math.log(S / K) + (r + sigma**2 / 2) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)

    N_d1 = normal_cdf(d1)
    N_d2 = normal_cdf(d2)

    C = S * N_d1 - K * math.exp(-r*t) * N_d2
    P = C + K * math.exp(-r*t) - S

    return (C, P)


if __name__ == "__main__":

    # Sample use case
    C = call_price(100, 110, 0.05, 1, 0.2)
    P = put_price(100, 110, 0.05, 1, 0.2)
    print(f"Theoretical price of a call option: ${C:.4f}")
    print(f"Theoretical price of a put option : ${P:.4f}")
