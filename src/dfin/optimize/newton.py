"""Root-finding using Newton's method."""
import torch


def newton(func, x0, atol:float=1e-6, max_iter:int=1000):
    """Newton's method. Quadratic convergence.

    Parameters
    ----------
    func : Callable
        Objective function.
    x0 : torch.Tensor
        Initial guess for root.

    Returns
    -------
    torch.Tensor
        Root.
    """

    if torch.is_tensor(x0):
        # x0.requires_grad = True
        x0 = x0.clone().detach().requires_grad_(True)
    else:
        x0 = torch.tensor(x0, requires_grad=True)
    # print(f'Starting `newton` optimization with x0={x0.item()}:')

    for i in range(max_iter):

        # print(f'Step {i: 3d}: x0={x0.item()}')
        diff = func(x0)
        # print(f'Step {i: 3d}: diff={diff.item()}')
        if torch.abs(diff) < atol:
            break

        # Calculate the gradient of the objective function (difference in option price).
        diff.backward()
        grad = x0.grad
        # print(f'Step {i: 3d}: grad={grad.item()}')

        # Update value (implied volatility) using Newton-Raphson method.
        x1 = x0 - diff / grad
        # print(f'Step {i: 3d}: x1={x1.item()}')

        if torch.abs(x1 - x0) < atol:
            x0 = x1.clone().detach().requires_grad_(True)
            # break
        elif torch.isinf(x1):
            print(f'`newton` diverged!!!')
            x0 = x1.clone().detach().requires_grad_(True)
            break
        else:
            x0 = x1.clone().detach().requires_grad_(True)

    # print(f'`newton` final x0={x0.item()}')
    return x0
