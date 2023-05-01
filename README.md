# dFin

![Workflow status - Options package - Master branch](https://github.com/tinkei/dfin/actions/workflows/python-package.yml/badge.svg?branch=master)
![GitHub language count](https://img.shields.io/github/languages/count/tinkei/dfin)
![GitHub top language](https://img.shields.io/github/languages/top/tinkei/dfin)
![GitHub all releases](https://img.shields.io/github/downloads/tinkei/dfin/total)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/tinkei/dfin)
![GitHub last commit](https://img.shields.io/github/last-commit/tinkei/dfin)

dFin (ˈdi-fīn) is a random assortment of Quantitative Finance algorithms that are implemented to be differentiable.
For starters, risk metrics such as Option Greeks are trivially obtainable through autograd.
This also opens the door to AI/ML applications, as implied volatility can be backpropped through the equations.
Theoretical price and implied volatility can then be jointly optimized using a recommender system.

At the current stage this is only a collection of individual functions yet to be integrated together into a wider framework.



---

## Getting Started

For normal users:  
`pip install dfinance`  

Development version:  
`pip install --index-url https://test.pypi.org/simple/ --no-deps dfinance`  

For developers:  
`git clone git@github.com:tinkei/dfin.git`  
`cd dfin`  
`pip install -e .`  



---

## Example Use Cases



### (1) Compute Option Greeks

It's a no-brainer really:

```python
import torch
from dfin.options.bs_torch import call_price

if __name__ == "__main__":

    S = torch.tensor([100.], requires_grad=True)
    K = torch.tensor([110.], requires_grad=True)
    r = torch.tensor([0.05], requires_grad=True)
    t = torch.tensor([1.], requires_grad=True)
    sigma = torch.tensor([0.2], requires_grad=True)

    C = call_price(S, K, r, t, sigma)
    C.backward(retain_graph=True)
    Cdelta = torch.autograd.grad(C, S, create_graph=True)
    Cgamma = torch.autograd.grad(Cdelta, S, create_graph=True)[0]

    print(f"Theoretical price of a call option: ${C.item():.4f}")
    print(f"Gradients (Option Greeks)")
    print(f"dC/dS   (delta) : {S.grad.item():+.4f}") # ==  0.450
    print(f"d2C/dS2 (gamma) : {Cgamma.item():+.4f}") # == 0.020
    print(f"dC/dK   (N/A)   : {K.grad.item():+.4f}")
    print(f"dC/dr   (rho)   : {r.grad.item():+.4f}") # ==  38.925
    print(f"dC/dt   (theta) : {-t.grad.item():+.4f}") # == -5.904
    print(f"dC/dσ   (vega)  : {sigma.grad.item():+.4f}") # == 39.576
```



### (2) Compute Implied Volatility

I know gradient descent is nowhere near the most efficient way to compute implied volatility, but it works out-of-the-box. So why not?
Plus autograd gives us the Hessian semi-automatically so one can easily make higher-order optimization schemes work as well.

```python
import torch
from dfin.optimize import gradient_descent, lbfgs, secant, newton, halley
from dfin.options.iv_torch import call_implied_volatility

if __name__ == "__main__":

    S = torch.tensor([100.], requires_grad=False)
    K = torch.tensor([110.], requires_grad=False)
    r = torch.tensor([0.05], requires_grad=False)
    t = torch.tensor([1.], requires_grad=False)
    price = torch.tensor([6.040088129724], requires_grad=False)
    sigma0 = torch.tensor(0.5, requires_grad=True)

    sigma = call_implied_volatility(S, K, r, t, price, sigma0, optim=gradient_descent)
    print(f'Gradient descent (linear-ish convergence) : {sigma.item():+.6f}') # == 0.2
    sigma = call_implied_volatility(S, K, r, t, price, sigma0, optim=lbfgs)
    print(f'LBFGS (superlinear-ish convergence)       : {sigma.item():+.6f}') # == 0.2
    sigma = call_implied_volatility(S, K, r, t, price, sigma0, optim=secant)
    print(f"Secant method (quadratic convergence)     : {sigma.item():+.6f}") # == 0.2
    sigma = call_implied_volatility(S, K, r, t, price, sigma0, optim=newton)
    print(f"Newton's method (quadratic convergence)   : {sigma.item():+.6f}") # == 0.2
    sigma = call_implied_volatility(S, K, r, t, price, sigma0, optim=halley)
    print(f"Halley's method (cubic convergence)       : {sigma.item():+.6f}") # == 0.2
```

Performance comparison on CPU:

| Method | Time (ms) | Iterations |
| :----: | --------: | :--------: |
| Adam   | 134.52 ms |        245 |
| LBFGS  |   3.46 ms |          6 |
| Secant |   1.54 ms |          5 |
| Newton |   1.41 ms |          4 |
| Halley |   3.08 ms |          3 |
| SciPy  | 0.0751 ms |          4 |

Convenient doesn't mean fast...
Secant method (SciPy) doesn't need to evaluate analytical gradient at all.
Anyway, moving on...



### (3) Learn Volatility Smile (Smirk)

Implied volatility computed from option prices of different expiration dates and different strike prices give different values.
The result often looks like a smirk if one were to plot implied volatility against time to maturity, or a smile when plotted against strike price.
One can use ML to introduce an appropriate amount of bias to your _"fair volatility"_, given a target maturity and strike.

```python
```



### (4) Predict Theoretical Price

The quoted market price of an instrument isn't really _one_ price, but rather it is an order book of bid and ask orders.
Neither is the theoretical price necessarily the midpoint between the nearest bid and ask prices, nor is it guaranteed that the nearest bid/ask order has sufficient volume to fulfill _your_ order.
When the underlying is trending (bull or bear), demand-supply can cause implied volatilities of put and call options to diverge.
The inconvenience of market microstructure is often simplified (read: overlooked) in textbook pricing models.
For those who don't have a PhD in Financial Engineering, let AI do the heavy lifting for you.

```python
```



### (5) Why Not Both?

Traditionally one can either estimate implied volatility given the current option price, _xor_ calculate a fair option price given an estimate of implied volatility.
Why not both?
That's the reason this repository exists:
To use a recommender system to predict both variables simultaneously.

```python
```



### (6) ...

......



### (7) Profit!

Of course the whole point of this is to identify profit opportunities in the market!
Why else do you think I spend all these hours to code up this mother &ast;&ast;&ast;&ast;ing hot steaming pile of &ast;&ast;&ast;&ast;!?!?
A backtest engine will be included in future releases.



<!---

---

## TODO

- [ ] Packaging
- [ ] Documentation
- [ ] Data connectors
- [ ] Portfolio management
- [ ] Front-end dashboard
- [ ] Backtest
- [ ] Order execution
- [ ] Data governance
- [ ] Monitoring and observability

--->
