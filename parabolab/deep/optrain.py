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
from typing import Dict, Sequence, Tuple

import numpy as np
import torch

from . import corpus
from .condtrain import fit_conditioned_scalers
from .generator import TrainingData, generate_training_data
from .opnet import CoeffMLP
from .settrain import per_instance_mlp_l1


def pooled_operator_rows(instances: Sequence[corpus.Instance]) -> Dict[str, np.ndarray]:
    phi = np.stack([inst.phi_grid for inst in instances])
    cond = np.stack([np.asarray(inst.spec.params, dtype=float) for inst in instances])
    tx, u, idx = [], [], []
    for i, inst in enumerate(instances):
        ok = inst.finite & (inst.x[:, 0] >= inst.grid[0]) & (inst.x[:, 0] <= inst.grid[-1])
        tx.append(np.column_stack([inst.t, inst.x])[ok])
        u.append(inst.y[0, ok])
        idx.append(np.full(int(ok.sum()), i))
    return {"phi": phi, "cond": cond, "tx": np.concatenate(tx), "u": np.concatenate(u),
            "inst_idx": np.concatenate(idx)}


def fit_operator_scalers(net, rows) -> float:
    """Fill the buffers the net has; return the pooled u std (used for the loss).

    CoeffMLP's own phi_scale/in_*/out_*/cond_* stay at identity -- its
    forward never reads them (see opnet.CoeffMLP.forward). The wrapped
    ConditionedNet core scales (t, x), u and theta through its OWN buffers
    instead, so the fitted statistics land in net.core.* there: in_*/out_*
    via condtrain.fit_conditioned_scalers (its row layout -- "tx", "u" --
    matches these rows), and param_mean/param_std (which that routine does
    not fill; ConditionedNet's other callers pass them in at construction
    time instead) from the pooled cond rows, with the same std floor as the
    outer cond_mean/cond_std path below.
    """
    u_std = float(rows["u"].std()) or 1.0
    with torch.no_grad():
        if isinstance(net, CoeffMLP):
            fit_conditioned_scalers(net.core, rows)
            mean, std = rows["cond"].mean(0), rows["cond"].std(0)
            std[std < 1e-12] = 1.0
            net.core.param_mean.copy_(torch.as_tensor(mean, dtype=torch.float32))
            net.core.param_std.copy_(torch.as_tensor(std, dtype=torch.float32))
            return u_std
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
        if hasattr(net, "cond_mean") and net.cond_mean.numel() > 0:
            mean, std = rows["cond"].mean(0), rows["cond"].std(0)
            std[std < 1e-12] = 1.0
            net.cond_mean.copy_(torch.as_tensor(mean, dtype=torch.float32))
            net.cond_std.copy_(torch.as_tensor(std, dtype=torch.float32))
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
    cond = torch.as_tensor(rows["cond"], dtype=torch.float32, device=device)
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
        bi_t = torch.as_tensor(bi, device=device)
        pred = net(phi[bi_t], cond[bi_t], tx[qi_t])
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
        cond = torch.as_tensor(np.asarray(inst.spec.params, dtype=float), dtype=torch.float32, device=device)[None]
        q = torch.as_tensor(np.column_stack([np.zeros_like(inst.grid), inst.grid]),
                            dtype=torch.float32, device=device)[None]
        pred = net(phi, cond, q)[0].cpu().numpy()
        err = np.abs(pred - inst.u_grid)
        out.append(float(err.mean()) if np.isfinite(err).all() else float("inf"))
    return np.array(out)


def per_phi_baseline(inst: corpus.Instance, *, device="cpu", seed=0, epochs=3000) -> float:
    return per_instance_mlp_l1(inst, device=device, seed=seed, epochs=epochs)


def _precheck_draws(spec: corpus.InstanceSpec, fam: corpus.Family, m_lo: int, m_hi: int,
                    n_jobs: int = 1) -> Tuple[TrainingData, TrainingData]:
    """Draw the lo/hi-budget label sets for one calibration instance on shared
    states, with INDEPENDENT tree streams.

    Both draws share the same states (``corpus._draw_states`` depends only on
    ``spec.seed``, not on the sample budget) but use distinct label seeds
    (``1000*spec.seed`` vs ``1000*spec.seed + 500``) passed straight to
    ``generate_training_data``. That keeps their per-state RNG streams
    (``np.random.SeedSequence(seed).spawn(n_states)`` inside
    ``generate_training_data``) from overlapping. Going through
    ``corpus.generate_instance`` twice (varying only ``m_samples``) does NOT
    give independence: both calls resolve to the same draw-0 seed
    ``1000*spec.seed + 0``, so the hi-budget run's first ``m_lo`` tree
    samples are bit-identical to the whole lo-budget run -- nested samples,
    not independent ones, which damps and biases the combined-stderr z-test
    toward passing.
    """
    factory = fam.make_factory(spec.params)
    ts, xs = corpus._draw_states(spec, fam)
    data_lo = generate_training_data(
        factory, n_states=spec.n_states, m_samples=m_lo, seed=1000 * spec.seed,
        rate=fam.rate, x_lo=fam.x_lo, x_hi=fam.x_hi, states=(ts, xs), n_jobs=n_jobs)
    data_hi = generate_training_data(
        factory, n_states=spec.n_states, m_samples=m_hi, seed=1000 * spec.seed + 500,
        rate=fam.rate, x_lo=fam.x_lo, x_hi=fam.x_hi, states=(ts, xs), n_jobs=n_jobs)
    return data_lo, data_hi


def calibration_precheck(family, *, n=20, n_states=200, m_lo=1000, m_hi=10_000,
                         seed=123, n_jobs=1) -> dict:
    """Check that the sampler's reported stderr is calibrated, by comparing
    labels drawn at two sample budgets (``m_lo``, ``m_hi``) on the SAME
    states (``corpus._draw_states`` derives the state draw only from
    ``spec.seed``, not ``m_samples``).

    The two label draws must be statistically INDEPENDENT given the shared
    states, or the z-test below is meaningless (nested samples agree by
    construction, not because the stderr is calibrated). ``_precheck_draws``
    guarantees this by calling ``generate_training_data`` directly with two
    label seeds, ``1000*spec.seed`` and ``1000*spec.seed + 500``, that never
    collide -- unlike two ``corpus.generate_instance`` calls differing only
    in ``m_samples``, which both land on seed ``1000*spec.seed + 0``.

    If the stderr is calibrated: (a) the two noisy estimates should mostly
    agree within a few combined stderrs -- ``frac_within_4se`` should be
    high; (b) since stderr ~ 1/sqrt(m_samples), the low-budget stderr should
    be about sqrt(m_hi/m_lo) times the high-budget one -- ``stderr_ratio``
    (median over states) should land near that value (default
    sqrt(10) ~= 3.16, checked against a 2x band).
    """
    fam = corpus.FAMILIES[family]
    specs = corpus.sample_instances(family, n, seed, n_states=n_states,
                                    m_samples=m_lo, n_draws=1)

    z_parts, ratio_parts = [], []
    n_total = 0
    for spec in specs:
        data_lo, data_hi = _precheck_draws(spec, fam, m_lo, m_hi, n_jobs=n_jobs)
        ok = (np.isfinite(data_lo.y) & np.isfinite(data_lo.stderr)
              & np.isfinite(data_hi.y) & np.isfinite(data_hi.stderr))
        n_total += ok.size
        y_lo, y_hi = data_lo.y[ok], data_hi.y[ok]
        se_lo, se_hi = data_lo.stderr[ok], data_hi.stderr[ok]
        z_parts.append(np.abs(y_lo - y_hi) / np.sqrt(se_lo ** 2 + se_hi ** 2))
        ratio_parts.append(se_lo / se_hi)
    z = np.concatenate(z_parts) if z_parts else np.array([])
    ratio = np.concatenate(ratio_parts) if ratio_parts else np.array([])

    frac_within_4se = float(np.mean(z <= 4)) if z.size else float("nan")
    stderr_ratio = float(np.median(ratio)) if ratio.size else float("nan")
    lo_bound, hi_bound = np.sqrt(10) / 2, 2 * np.sqrt(10)
    passed = bool(np.isfinite(frac_within_4se) and np.isfinite(stderr_ratio)
                  and frac_within_4se >= 0.95 and lo_bound <= stderr_ratio <= hi_bound)
    n_states_used = int(z.size)
    frac_nonfinite = 1.0 - n_states_used / n_total if n_total else float("nan")
    return {"frac_within_4se": frac_within_4se, "stderr_ratio": stderr_ratio,
            "passed": passed, "n_states_used": n_states_used,
            "frac_nonfinite": frac_nonfinite}
