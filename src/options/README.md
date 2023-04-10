# Black-Scholes formula

![Workflow status - Options package - Master branch](https://github.com/tinkei/dfin/actions/workflows/python-package.yml/badge.svg?branch=master)

[Wikipedia](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model):
> The Black–Scholes /ˌblæk ˈʃoʊlz/ or Black–Scholes–Merton model is a mathematical model for the dynamics of a financial market containing derivative investment instruments. From the parabolic partial differential equation in the model, known as the Black–Scholes equation, one can deduce the **Black–Scholes formula**, which gives a theoretical estimate of the price of *European-style* options and shows that the option has a unique price given the risk of the security and its expected return (instead replacing the security's expected return with the risk-neutral rate).

The model assumes that the option can only be exercised at the expiration date (i.e. European option) and that there are no transaction costs or taxes. Furthermore, the underlying stock price follows a [Geometric Brownian Motion](https://en.wikipedia.org/wiki/Geometric_Brownian_motion). The formula is as follows:

$$ C = S N(d_1) - K e^{-rt} N(d_2) $$

$$ P = K e^{-rt} N(-d_2) - S N(-d_1) $$

where:

* $C$ is the price of the call option
* $P$ is the price of the put option
* $S=S_0$ is the current underlying price (stock, future, etc.)
* $K$ is the option strike price
* $r$ is the risk-free interest rate
* $t$ is the time until the option expiration
* $N$ is the cumulative distribution function of the *standard* normal distribution
* $\sigma$ is the volatility of the underlying asset, typically *annualized*
* $d_1 = \frac{\ln{\left(\frac{S}{K}\right)} + \left(r + \frac{\sigma^2}{2}\right) t}{\sigma \sqrt{t}}$
* $d_2 = d_1 - \sigma \sqrt{t} = \frac{\ln{\left(\frac{S}{K}\right)} + \left(r - \frac{\sigma^2}{2}\right) t}{\sigma \sqrt{t}}$

The formula can be validated using Put-Call Parity:

$$ C + K e^{-rt} = P + S $$

$ L.H.S. = S N(d_1) - K e^{-rt} N(d_2) + K e^{-rt} $ \
$ L.H.S. = S [1 - N(-d_1)] - K e^{-rt} [1 - N(-d_2)] + K e^{-rt} $ \
$ L.H.S. = S - S N(-d_1) - K e^{-rt} + K e^{-rt} N(-d_2) + K e^{-rt} $ \
$ L.H.S. = S - S N(-d_1) + K e^{-rt} N(-d_2) $ \
$ L.H.S. = S + P = R.H.S $
