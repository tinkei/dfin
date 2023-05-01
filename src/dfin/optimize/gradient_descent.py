"""Root-finding using gradient descent (adam)."""
import torch


def gradient_descent(func, x0, atol:float=1e-6, max_iter:int=1000):
    """Gradient descent (adam). Linear-ish convergence.

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

    # print(f'x0 is on device {x0.device}')
    if torch.is_tensor(x0):
        # x0.requires_grad = True
        x0 = x0.clone().detach().requires_grad_(True)
    else:
        x0 = torch.tensor(x0, requires_grad=True)
    optimizer = torch.optim.Adam([x0], lr=0.2)
    # optimizer = torch.optim.Adadelta([x0])
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
    # print(f'Starting `gradient_descent` optimization with x0={x0.item()}:')
    # print(f'x0 is on device {x0.device}')

    for i in range(max_iter):

        optimizer.zero_grad()
        # x_prev = x0.clone().detach()
        # print(f'Step {i: 3d}: x0={x0.item()}')
        diff = func(x0)
        # print(f'Step {i: 3d}: diff={diff.item()}')
        if torch.abs(diff) < atol:
            break

        # loss = torch.square(diff)
        loss = diff**2
        loss.backward()
        optimizer.step()
        if i % 10 == 9:
            scheduler.step()

        # if torch.abs(x_prev - x0) < atol:
        #     break
        # elif torch.isinf(x0):
        #     print(f'`gradient_descent` diverged!!!')
        #     break

    # print(f'`gradient_descent` final x0={x0.item()}')
    return x0
