"""Pooled training and grid evaluation for phi -> u operators (spec
2026-09-16-phi-operator-design).

``pooled_operator_rows`` keeps only finite rows whose x lies within the
instance's own sensor grid ``[grid[0], grid[-1]]``: training states are
drawn on the 10%-overtrained segment (``corpus._draw_states``), so about
17% of them fall outside the 101-point grid the terminal condition
``phi_grid`` is sampled on. ``FNO1d`` can only answer such out-of-range
queries by clamping to the boundary value, so the filter is applied for
every backbone (DeepONet, FNO1d, AttnOperator) -- all three then see
identical data.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, Sequence

import numpy as np
import torch

from . import corpus
from .settrain import per_instance_mlp_l1


def pooled_operator_rows(instances: Sequence[corpus.Instance]) -> Dict[str, np.ndarray]:
    phi = np.stack([inst.phi_grid for inst in instances])
    tx, u, idx = [], [], []
    for i, inst in enumerate(instances):
        ok = inst.finite & (inst.x[:, 0] >= inst.grid[0]) & (inst.x[:, 0] <= inst.grid[-1])
        tx.append(np.column_stack([inst.t, inst.x])[ok])
        u.append(inst.y[0, ok])
        idx.append(np.full(int(ok.sum()), i))
    return {"phi": phi, "tx": np.concatenate(tx), "u": np.concatenate(u),
            "inst_idx": np.concatenate(idx)}


def fit_operator_scalers(net, rows) -> float:
    """Fill the buffers the net has; return the pooled u std (used for the loss)."""
    u_std = float(rows["u"].std()) or 1.0
    with torch.no_grad():
        if hasattr(net, "phi_scale"):
            net.phi_scale.fill_(float(rows["phi"].std()) or 1.0)
        if hasattr(net, "in_mean"):
            mean, std = rows["tx"].mean(0), rows["tx"].std(0)
            std[std < 1e-12] = 1.0
            net.in_mean.copy_(torch.as_tensor(mean, dtype=torch.float32))
            net.in_std.copy_(torch.as_tensor(std, dtype=torch.float32))
        if hasattr(net, "out_mean"):
            net.out_mean.fill_(float(rows["u"].mean()))
            net.out_std.fill_(u_std)
    return u_std


@dataclass
class OpTrainResult:
    net: torch.nn.Module
    losses: np.ndarray
    seconds: float


def train_operator(net, instances, *, steps=20_000, batch_instances=32, n_query=64,
                   lr=1e-3, device="cpu", seed=0, log_every=100, verbose=False) -> OpTrainResult:
    rows = pooled_operator_rows(instances)
    u_std = fit_operator_scalers(net, rows)
    net = net.to(device).train()
    phi = torch.as_tensor(rows["phi"], dtype=torch.float32, device=device)
    tx = torch.as_tensor(rows["tx"], dtype=torch.float32, device=device)
    u = torch.as_tensor(rows["u"], dtype=torch.float32, device=device)
    per_inst = [np.flatnonzero(rows["inst_idx"] == i) for i in range(len(instances))]
    rng = np.random.default_rng(seed); torch.manual_seed(seed)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    losses, start = [], time.perf_counter()
    for step in range(steps):
        bi = rng.choice(len(instances), size=min(batch_instances, len(instances)), replace=False)
        qi = np.stack([rng.choice(per_inst[i], size=n_query, replace=len(per_inst[i]) < n_query) for i in bi])
        qi_t = torch.as_tensor(qi, device=device)
        pred = net(phi[torch.as_tensor(bi, device=device)], tx[qi_t])
        loss = torch.mean(((pred - u[qi_t]) / u_std) ** 2)
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite loss at step {step}")
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
        opt.step(); sched.step()
        if step % log_every == 0 or step == steps - 1:
            losses.append(float(loss.detach()))
            if verbose:
                print(f"  step {step}: loss {losses[-1]:.4e}", flush=True)
    net.eval()
    return OpTrainResult(net, np.array(losses), time.perf_counter() - start)


@torch.no_grad()
def evaluate_operator(net, instances, *, device="cpu") -> np.ndarray:
    net = net.to(device).eval()
    out = []
    for inst in instances:
        phi = torch.as_tensor(inst.phi_grid, dtype=torch.float32, device=device)[None]
        q = torch.as_tensor(np.column_stack([np.zeros_like(inst.grid), inst.grid]),
                            dtype=torch.float32, device=device)[None]
        pred = net(phi, q)[0].cpu().numpy()
        err = np.abs(pred - inst.u_grid)
        out.append(float(err.mean()) if np.isfinite(err).all() else float("inf"))
    return np.array(out)


def per_phi_baseline(inst: corpus.Instance, *, device="cpu", seed=0, epochs=3000) -> float:
    return per_instance_mlp_l1(inst, device=device, seed=seed, epochs=epochs)
