"""Root-finding using secant method."""
import torch


def secant(func, x0, atol:float=1e-6, max_iter:int=1000):
    """Secant's method. Quadratic convergence. Finite difference variation of Newton's method.

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
        x1 = x0.clone().detach().requires_grad_(True)
    else:
        x1 = torch.tensor(x0, requires_grad=True)
    x0 = torch.zeros_like(x1, requires_grad=True)
    f0 = func(x0)
    # print(f'Starting `secant` optimization with x0={x0.item()}:')

    for i in range(max_iter):

        # print(f'Step {i: 3d}: x0={x0.item()}')
        # print(f'Step {i: 3d}: x1={x1.item()}')
        # diff = func(x0)

        f1 = func(x1)
        # print(f'Step {i: 3d}: diff={f1.item()}')
        if torch.abs(f1) < atol:
            break

        # Update value (implied volatility) using Secant method.
        # x2 = (x0 * f1 - x1 * f0) / (f1 - f0) # 1.5996 ms
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0) # 1.5473 ms
        # x2 = x1 - (x1 - x0) / (1 - f0 / f1)  # 1.5971 ms
        x0, x1, f0 = x1, x2, f1

        if torch.abs(x1 - x0) < atol:
            # break
            pass
        elif torch.isinf(x1):
            print(f'`secant` diverged!!!')
            break
        else:
            pass

    # print(f'`secant` final x1={x1.item()}')
    return x1
