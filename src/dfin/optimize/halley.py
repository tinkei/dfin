"""Root-finding using Halley's method."""
import torch


def halley(func, x0, atol:float=1e-6, max_iter:int=1000):
    """Halley's method. Cubic convergence.

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
    # print(f'Starting `halley` optimization with x0={x0.item()}:')

    for i in range(max_iter):

        # print(f'Step {i: 3d}: x0={x0.item()}')
        diff = func(x0)
        # print(f'Step {i: 3d}: diff={diff.item()}')
        if torch.abs(diff) < atol:
            break

        # Calculate the gradient and hessian of the objective function (difference in option price).
        grad = torch.autograd.grad(diff, x0, create_graph=True)
        hess = torch.autograd.grad(grad, x0, create_graph=True)
        # print(f'Step {i: 3d}: grad={grad[0].item()}')
        # print(f'Step {i: 3d}: hess={hess[0].item()}')

        # Update value (implied volatility) using Halley's method.
        x1 = x0 - 2 * diff * grad[0] / (2 * grad[0]**2 - diff * hess[0])

        if torch.abs(x1 - x0) < atol:
            x0 = x1.clone().detach().requires_grad_(True)
            # break
        elif torch.isinf(x1):
            print(f'`halley` diverged!!!')
            x0 = x1.clone().detach().requires_grad_(True)
            break
        else:
            x0 = x1.clone().detach().requires_grad_(True)

    # print(f'`halley` final x0={x0.item()}')
    return x0
