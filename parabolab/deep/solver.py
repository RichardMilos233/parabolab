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


def fit_scalers(net: DeepBranchNet, data: TrainingData) -> None:
    """Fill the net's input/output scaler buffers from the training data.

    No-op unless the net was built with scale_input / scale_output.  A
    coordinate with no spread (tau == 0 in the paper's protocol) keeps
    std = 1 so it is passed through unchanged.
    """
    finite = np.isfinite(data.y)
    with torch.no_grad():
        if net.scale_input:
            tx = np.column_stack([data.t[finite], data.x[finite]])
            mean = tx.mean(axis=0)
            std = tx.std(axis=0)
            std[std < 1e-12] = 1.0
            net.in_mean.copy_(torch.as_tensor(mean, dtype=torch.float32))
            net.in_std.copy_(torch.as_tensor(std, dtype=torch.float32))
        if net.scale_output:
            y = data.y[finite]
            std = float(y.std())
            net.out_mean.fill_(float(y.mean()))
            net.out_std.fill_(std if std >= 1e-12 else 1.0)


def train_deep_branching(
    net: DeepBranchNet,
    data: TrainingData,
    *,
    epochs: int = 3000,
    lr: float = 0.01,
    device: str = "cpu",
    log_every: int = 100,
    verbose: bool = False,
    loss: str = "mse",
    schedule: str = "multistep",
    grad_clip: Optional[float] = None,
    lbfgs_steps: int = 0,
) -> DeepBranchingResult:
    """Algorithm 2: fit net to the MC targets by full-batch Adam.

    Ablation options (defaults = the paper):
      loss        "mse" | "weighted_mse" (weights 1/stderr^2, mean 1;
                  rows with infinite stderr get weight 0)
      schedule    "multistep" (lr / 10 at P/3, 2P/3) | "cosine"
      grad_clip   clip the gradient norm before every Adam step
      lbfgs_steps full-batch L-BFGS iterations after the Adam epochs, run
                  in eval mode (BatchNorm uses its running statistics;
                  they are not updated by the polish)
    """
    if loss not in ("mse", "weighted_mse"):
        raise ValueError(f"unknown loss {loss!r}")
    if schedule not in ("multistep", "cosine"):
        raise ValueError(f"unknown schedule {schedule!r}")

    fit_scalers(net, data)
    net = net.to(device)
    finite = np.isfinite(data.y)
    tx = torch.tensor(
        np.column_stack([data.t[finite], data.x[finite]]),
        dtype=torch.float32, device=device,
    )
    y = torch.tensor(data.y[finite], dtype=torch.float32, device=device)

    if loss == "weighted_mse":
        se = data.stderr[finite].astype(float)
        ok = np.isfinite(se)
        if not ok.any():
            raise ValueError(
                "weighted_mse needs at least one state with finite stderr"
            )
        eps = 1e-3 * np.median(se[ok])
        if eps <= 0:
            positive = se[ok][se[ok] > 0]
            eps = 1e-3 * positive.min() if positive.size else 1.0
        w = np.zeros_like(se)
        w[ok] = 1.0 / np.maximum(se[ok], eps) ** 2
        w /= w.mean()
        weights = torch.tensor(w, dtype=torch.float32, device=device)

        def loss_fn(pred, target):
            return torch.mean(weights * (pred - target) ** 2)
    else:
        loss_fn = torch.nn.MSELoss()

    optimizer = torch.optim.Adam(net.parameters(), lr=lr)
    if schedule == "multistep":
        scheduler = torch.optim.lr_scheduler.MultiStepLR(
            optimizer, milestones=[epochs // 3, 2 * epochs // 3], gamma=0.1
        )
    else:
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=epochs
        )

    losses = []
    start = time.perf_counter()
    net.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        loss_val = loss_fn(net(tx), y)
        loss_val.backward()
        if grad_clip is not None:
            torch.nn.utils.clip_grad_norm_(net.parameters(), grad_clip)
        optimizer.step()
        scheduler.step()
        if epoch % log_every == 0 or epoch == epochs - 1:
            losses.append(float(loss_val.detach()))
            if verbose:
                print(f"  epoch {epoch}: loss {losses[-1]:.6f}", flush=True)

    if lbfgs_steps > 0:
        net.eval()
        lbfgs = torch.optim.LBFGS(
            net.parameters(), lr=1.0, max_iter=lbfgs_steps,
            history_size=50, line_search_fn="strong_wolfe",
        )

        def closure():
            lbfgs.zero_grad()
            l = loss_fn(net(tx), y)
            l.backward()
            return l

        lbfgs.step(closure)
        with torch.no_grad():
            losses.append(float(loss_fn(net(tx), y)))
        if verbose:
            print(f"  L-BFGS: loss {losses[-1]:.6f}", flush=True)

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
