"""Training, grid evaluation and baselines for the set-to-field denoiser."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Sequence

import numpy as np
import torch

from . import corpus
from .ablation import NetConfig, build_net
from .generator import TrainingData
from .setnet import SetDenoiser
from .solver import _grid_inputs, net_on_grid, train_deep_branching

# the ablation's kept configuration (spec 2026-09-15-nn-architecture-ablation)
R5A = NetConfig(neurons=64, activation="gelu", norm="none",
                scale_input=True, scale_output=True)


@dataclass
class SetTrainResult:
    net: SetDenoiser
    losses: np.ndarray
    seconds: float


def _to_t(batch, device):
    return {k: torch.as_tensor(v, dtype=torch.float32, device=device)
            for k, v in batch.items()}


def train_set_denoiser(
    net: SetDenoiser,
    instances: Sequence[corpus.Instance],
    *,
    steps: int = 20_000,
    lr: float = 3e-4,
    weight_decay: float = 1e-4,
    batch_instances: int = 16,
    n_context: int = 500,
    n_query: int = 128,
    target: str = "n2n",
    device: str = "cpu",
    seed: int = 0,
    log_every: int = 100,
    verbose: bool = False,
) -> SetTrainResult:
    """AdamW + cosine schedule + grad-clip 1.0 on the MSE in scaled y units.

    target="n2n": the query target is the instance's independent second
    draw (unbiased for MSE, Noise2Noise); "exact": the closed-form solution
    (an upper bound, only for families with one).
    """
    if target not in ("n2n", "exact"):
        raise ValueError(f"unknown target {target!r}; use 'n2n' or 'exact'")
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    net = net.to(device).train()
    opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=weight_decay)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    key = "q_y" if target == "n2n" else "q_u"
    losses, start = [], time.perf_counter()
    instances = list(instances)
    for step in range(steps):
        idx = rng.choice(len(instances), size=min(batch_instances, len(instances)),
                         replace=False)
        batch = _to_t(corpus.collate([instances[i] for i in idx],
                                     n_context=n_context, n_query=n_query,
                                     rng=rng), device)
        _, s = net.context_stats(batch["ctx_y"])
        pred = net(batch["ctx_tx"], batch["ctx_y"], batch["ctx_se"],
                   batch["params"], batch["q_tx"])
        loss = torch.mean(((pred - batch[key]) / s) ** 2)
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite loss at step {step}")
        opt.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step()
        sched.step()
        if step % log_every == 0 or step == steps - 1:
            losses.append(float(loss.detach()))
            if verbose:
                print(f"  step {step}: loss {losses[-1]:.4e}", flush=True)
    net.eval()
    return SetTrainResult(net, np.array(losses), time.perf_counter() - start)


@torch.no_grad()
def evaluate_set_denoiser(net: SetDenoiser, instances: Sequence[corpus.Instance],
                          *, n_context: int = 500, device: str = "cpu") -> np.ndarray:
    """L1 on each instance's 101-point grid; the context is (up to n_context of)
    the instance's finite draw-0 rows in a fixed order."""
    net = net.to(device).eval()
    out = []
    for inst in instances:
        ok = np.flatnonzero(inst.finite)
        ok = np.random.default_rng(0).permutation(ok)[:n_context]
        tx = np.column_stack([inst.t, inst.x])[ok]
        _, _, q = _grid_inputs(inst.x.shape[1], 0.0,
                               corpus.FAMILIES[inst.spec.family].x_lo,
                               corpus.FAMILIES[inst.spec.family].x_hi)
        batch = _to_t({"ctx_tx": tx[None], "ctx_y": inst.y[0, ok][None],
                       "ctx_se": inst.stderr[0, ok][None],
                       "params": np.array(inst.spec.params)[None],
                       "q_tx": q[None]}, device)
        pred = net(**batch)[0].cpu().numpy()
        err = np.abs(pred - inst.u_grid)
        out.append(float(err.mean()) if np.isfinite(err).all() else float("inf"))
    return np.array(out)


def _as_training_data(inst: corpus.Instance, draw: int) -> TrainingData:
    return TrainingData(t=inst.t, x=inst.x, y=inst.y[draw],
                        stderr=inst.stderr[draw],
                        n_kept=np.full(len(inst.t), inst.spec.m_samples),
                        m_samples=inst.spec.m_samples, rate=inst.rate,
                        seconds=0.0)


def per_instance_mlp_l1(inst: corpus.Instance, *, draw: int = 0,
                        device: str = "cpu", seed: int = 0,
                        epochs: int = 3000) -> float:
    """The ablation's kept net (R5A) trained on this instance alone."""
    fam = corpus.FAMILIES[inst.spec.family]
    net = build_net(R5A, d=fam.d, seed=seed)
    train_deep_branching(net, _as_training_data(inst, draw), epochs=epochs,
                         device=device)
    # score against the instance's stored reference on the 101-grid: the
    # closed form where one exists, the FD reference otherwise (ac_phi).
    _, _, tx = _grid_inputs(fam.d, 0.0, fam.x_lo, fam.x_hi)
    try:
        pred = net_on_grid(net, tx, device=device)
    except (ValueError, RuntimeError):
        return float("inf")
    err = np.abs(pred - inst.u_grid)
    return float(err.mean()) if np.isfinite(err).all() else float("inf")


def kernel_smoother_l1(inst: corpus.Instance, *, draw: int = 0) -> float:
    """Nadaraya-Watson (Gaussian kernel on x_1) with the bandwidth chosen by
    leave-one-out on the context: the 'is attention more than smoothing'
    control."""
    ok = inst.finite
    x = inst.x[ok, 0]; y = inst.y[draw, ok]
    span = x.max() - x.min()
    bandwidths = span * np.logspace(-2.5, -0.5, 20)

    def predict(xq, h, loo=False):
        w = np.exp(-0.5 * ((xq[:, None] - x[None, :]) / h) ** 2)
        if loo:
            np.fill_diagonal(w, 0.0)
        return (w @ y) / np.maximum(w.sum(axis=1), 1e-300)

    loo = [np.mean((predict(x, h, loo=True) - y) ** 2) for h in bandwidths]
    h = bandwidths[int(np.argmin(loo))]
    pred = predict(inst.grid, h)
    return float(np.mean(np.abs(pred - inst.u_grid)))
