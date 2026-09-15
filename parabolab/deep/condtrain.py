"""Pooled training, evaluation and the closed-form policy referee for the
parameter-conditioned Merton net (spec 2026-09-15-parametric-merton-net)."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, List, Sequence

import numpy as np
import torch

from . import corpus
from .ablation import build_net
from .condnet import ConditionedNet, autograd_derivatives
from .settrain import R5A, _as_training_data
from .solver import _grid_inputs, train_deep_branching

INTERIOR = (110.0, 190.0)


def pooled_rows(instances: Sequence[corpus.Instance]) -> Dict[str, np.ndarray]:
    tx, params, u, ux, uxx = [], [], [], [], []
    has_deriv = all(inst.deriv is not None for inst in instances)
    for inst in instances:
        ok = inst.finite
        tx.append(np.column_stack([inst.t, inst.x])[ok])
        params.append(np.tile(np.asarray(inst.spec.params, dtype=float), (ok.sum(), 1)))
        u.append(inst.y[0, ok])
        if has_deriv:
            ux.append(inst.deriv[0, ok]); uxx.append(inst.deriv[1, ok])
    rows = {"tx": np.concatenate(tx), "params": np.concatenate(params),
            "u": np.concatenate(u)}
    if has_deriv:
        rows["ux"], rows["uxx"] = np.concatenate(ux), np.concatenate(uxx)
    return rows


def fit_conditioned_scalers(net: ConditionedNet, rows) -> Dict[str, float]:
    with torch.no_grad():
        mean, std = rows["tx"].mean(0), rows["tx"].std(0)
        std[std < 1e-12] = 1.0
        net.in_mean.copy_(torch.as_tensor(mean, dtype=torch.float32))
        net.in_std.copy_(torch.as_tensor(std, dtype=torch.float32))
        net.out_mean.fill_(float(rows["u"].mean()))
        s = float(rows["u"].std()); net.out_std.fill_(s if s > 1e-12 else 1.0)
    return {"ux_std": float(rows["ux"].std()) if "ux" in rows else 1.0,
            "uxx_std": float(rows["uxx"].std()) if "uxx" in rows else 1.0}


@dataclass
class CondTrainResult:
    net: ConditionedNet
    losses: np.ndarray
    seconds: float


def train_conditioned(net, instances, *, steps=20_000, batch_states=4096,
                      lr=1e-3, loss_weights=(1.0, 0.0, 0.0), device="cpu",
                      seed=0, log_every=100, verbose=False) -> CondTrainResult:
    w_u, w1, w2 = loss_weights
    rows = pooled_rows(instances)
    if (w1 > 0 or w2 > 0) and "ux" not in rows:
        raise ValueError("derivative loss weights need a corpus with deriv_codes")
    stats = fit_conditioned_scalers(net, rows)
    net = net.to(device).train()
    T = {k: torch.as_tensor(v, dtype=torch.float32, device=device) for k, v in rows.items()}
    out_std = net.out_std.clone()
    rng = np.random.default_rng(seed); torch.manual_seed(seed)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=steps)
    R = len(rows["u"]); losses, start = [], time.perf_counter()
    for step in range(steps):
        idx = torch.as_tensor(rng.integers(0, R, size=min(batch_states, R)), device=device)
        tx, p = T["tx"][idx], T["params"][idx]
        if w1 > 0 or w2 > 0:
            u, ux, uxx = autograd_derivatives(lambda z: net(z, p), tx, create_graph=True)
            loss = w_u * torch.mean(((u - T["u"][idx]) / out_std) ** 2)
            loss = loss + w1 * torch.mean(((ux - T["ux"][idx]) / stats["ux_std"]) ** 2)
            loss = loss + w2 * torch.mean(((uxx - T["uxx"][idx]) / stats["uxx_std"]) ** 2)
        else:
            loss = w_u * torch.mean(((net(tx, p) - T["u"][idx]) / out_std) ** 2)
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite loss at step {step}")
        opt.zero_grad(); loss.backward(); opt.step(); sched.step()
        if step % log_every == 0 or step == steps - 1:
            losses.append(float(loss.detach()))
            if verbose:
                print(f"  step {step}: loss {losses[-1]:.4e}", flush=True)
    net.eval()
    return CondTrainResult(net, np.array(losses), time.perf_counter() - start)


def merton_policy_exact(params) -> float:
    gamma, mu, sigma = params[:3]
    return mu / (gamma * sigma**2)


def policy_from_derivatives(ux, uxx, x, mu, sigma):
    ux, uxx, x = np.asarray(ux), np.asarray(uxx), np.asarray(x)
    with np.errstate(divide="ignore", invalid="ignore"):
        return -(mu / sigma**2) * ux / (x * uxx)


def _policy_metrics(fn, inst: corpus.Instance, device: str) -> Dict[str, float]:
    fam = corpus.FAMILIES[inst.spec.family]
    grid, xg, tx = _grid_inputs(fam.d, 0.0, fam.x_lo, fam.x_hi)
    txt = torch.as_tensor(tx, dtype=torch.float32, device=device)
    u, ux, uxx = autograd_derivatives(fn, txt)
    u, ux, uxx = (v.cpu().numpy() for v in (u, ux, uxx))
    gamma, mu, sigma = inst.spec.params[:3]
    pol = policy_from_derivatives(ux, uxx, grid, mu, sigma)
    exact_pol = merton_policy_exact(inst.spec.params)
    with np.errstate(divide="ignore", invalid="ignore"):
        rel = np.abs(pol - exact_pol) / exact_pol
    interior = (grid >= INTERIOR[0]) & (grid <= INTERIOR[1])
    l1 = float(np.mean(np.abs(u - inst.u_grid)))
    f = lambda v: float(v) if np.isfinite(v) else float("inf")
    return {"l1_u": f(l1), "policy_err_interior": f(np.median(rel[interior])),
            "policy_err_full": f(np.median(rel))}


def evaluate_conditioned(net: ConditionedNet, instances, *, device="cpu") -> List[Dict[str, float]]:
    net = net.to(device).eval()
    out = []
    for inst in instances:
        p = torch.as_tensor(np.asarray(inst.spec.params, dtype=np.float32), device=device)
        fn = lambda z, p=p: net(z, p.expand(z.shape[0], -1))
        out.append(_policy_metrics(fn, inst, device))
    return out


def per_instance_baseline(inst: corpus.Instance, *, device="cpu", seed=0,
                          epochs=3000) -> Dict[str, float]:
    fam = corpus.FAMILIES[inst.spec.family]
    net = build_net(R5A, d=fam.d, seed=seed)
    train_deep_branching(net, _as_training_data(inst, 0), epochs=epochs, device=device)
    net.eval()
    return _policy_metrics(net, inst, device)
