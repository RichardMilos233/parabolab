"""Training loop (JCP2024 Algorithm 2 + Remark 3.1) and experiment helpers.

train_deep_branching: full-batch Adam on the MSE between v(tau_i, X_i;
theta) and the MC targets y_i, learning rate 0.01 divided by 10 after
every floor(P/3) steps, P = 3000 epochs by default.

grid_errors: the paper's error protocol -- L1/L2 errors on the 101-point
grid (x_lo + i dx, x_mid, ..., x_mid), evaluated at t = t_lo.

consistency_plot: the JCP Fig. 7 diagnostic, unique to the deep
branching method: the MC training targets are unbiased pointwise
estimates of u, so scattering them against the learned v(., .) (and the
exact solution when known) directly visualizes the consistency, or lack
thereof, of the fit.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import torch

from .generator import TrainingData
from .net import DeepBranchNet


@dataclass
class DeepBranchingResult:
    net: DeepBranchNet
    losses: np.ndarray       # loss every log_every epochs
    seconds: float


def train_deep_branching(
    net: DeepBranchNet,
    data: TrainingData,
    *,
    epochs: int = 3000,
    lr: float = 0.01,
    device: str = "cpu",
    log_every: int = 100,
    verbose: bool = False,
) -> DeepBranchingResult:
    """Algorithm 2: fit net to the MC targets by full-batch Adam."""
    net = net.to(device)
    finite = np.isfinite(data.y)
    tx = torch.tensor(
        np.column_stack([data.t[finite], data.x[finite]]),
        dtype=torch.float32, device=device,
    )
    y = torch.tensor(data.y[finite], dtype=torch.float32, device=device)

    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(
        optimizer, milestones=[epochs // 3, 2 * epochs // 3], gamma=0.1
    )
    loss_fn = torch.nn.MSELoss()

    losses = []
    start = time.perf_counter()
    net.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        loss = loss_fn(net(tx), y)
        loss.backward()
        optimizer.step()
        scheduler.step()
        if epoch % log_every == 0 or epoch == epochs - 1:
            losses.append(float(loss.detach()))
            if verbose:
                print(f"  epoch {epoch}: loss {losses[-1]:.6f}", flush=True)
    seconds = time.perf_counter() - start
    net.eval()
    return DeepBranchingResult(net=net, losses=np.array(losses),
                               seconds=seconds)


def _grid_inputs(d: int, t_val: float, x_lo: float, x_hi: float,
                 n_grid: int = 101, x_mid: Optional[float] = None):
    """The paper's evaluation grid (x_lo + i dx, x_mid, ..., x_mid)."""
    grid = np.linspace(x_lo, x_hi, n_grid)
    if x_mid is None:
        x_mid = 0.5 * (x_lo + x_hi)
    xs = np.full((n_grid, d), x_mid)
    xs[:, 0] = grid
    tx = np.column_stack([np.full(n_grid, t_val), xs])
    return grid, xs, tx


@torch.no_grad()
def net_on_grid(net: DeepBranchNet, tx: np.ndarray,
                device: str = "cpu") -> np.ndarray:
    net.eval()
    return (
        net(torch.tensor(tx, dtype=torch.float32, device=device))
        .cpu().numpy()
    )


def grid_errors(
    net: DeepBranchNet,
    pde,
    *,
    t_val: float = 0.0,
    x_lo: float,
    x_hi: float,
    n_grid: int = 101,
    device: str = "cpu",
    exact: Optional[Callable] = None,
):
    """JCP2024 error protocol: mean |err|^p over the 101-point grid.

    Returns (l1, l2, grid, predicted, true).
    """
    d = net.d
    grid, xs, tx = _grid_inputs(d, t_val, x_lo, x_hi, n_grid)
    predicted = net_on_grid(net, tx, device=device)
    exact = exact or pde.exact_solution
    true = np.array([exact(t_val, xs[i]) for i in range(n_grid)])
    err = np.abs(predicted - true)
    return float(err.mean()), float((err**2).mean()), grid, predicted, true


def consistency_plot(
    data: TrainingData,
    net: DeepBranchNet,
    pde,
    out_path,
    *,
    title: str,
    x_lo: float,
    x_hi: float,
    t_val: float = 0.0,
    device: str = "cpu",
):
    """JCP2024 Fig. 7: MC training samples vs the learned network."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    d = net.d
    grid, xs, tx = _grid_inputs(d, t_val, x_lo, x_hi)
    nn_vals = net_on_grid(net, tx, device=device)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(data.x[:, 0], data.y, "+", color="tab:blue", alpha=0.5,
            markersize=4, label="Monte Carlo samples")
    ax.plot(grid, nn_vals, color="tab:orange", lw=2,
            label="Neural network function")
    if pde.exact_solution is not None:
        true = [pde.exact_solution(t_val, xs[i]) for i in range(len(grid))]
        ax.plot(grid, true, "k--", lw=1, label="exact")
    ax.set_xlabel("$x$")
    ax.set_ylabel(f"$u({t_val}, x)$")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
