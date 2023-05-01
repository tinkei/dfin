"""Root-finding using LBFGS."""
import math
import torch


def lbfgs(func, x0, atol:float=1e-6, max_iter:int=1000):
    """LBFGS. Superlinear convergence.

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
    optimizer = torch.optim.LBFGS([x0], tolerance_grad=min(math.sqrt(atol)/1e-2,1e-5), tolerance_change=min(atol/1e-3,1e-10), max_iter=max_iter)
    # print(f'Starting `lbfgs` optimization with x0={x0.item()}:')
    i = 0

    def closure():
        nonlocal i
        i += 1

        optimizer.zero_grad()
        # print(f'Step {i: 3d}: x0={x0.item()}')
        diff = func(x0)
        # print(f'Step {i: 3d}: diff={diff.item()}')

        loss = torch.square(diff)
        loss.backward()
        return loss

    optimizer.step(closure)

    # print(f'`lbfgs` final x0={x0.item()}')
    return x0
