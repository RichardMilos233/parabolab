"""Tilted coding tree past every fixed-rate sampler's finite-variance horizon.

Periodic Allen-Cahn on [0, 1):  u_t + u_xx / 2 + u - u^3 = 0,  u(T, x) = v(x),
v(x) = 1/2 + eps * sin(2 pi x).  For eps = 0 this is the flat case whose
absolute-integrability horizon is tau = (3 pi - 2 log 3)/5 ~ 1.4455, while every
constant-rate, fixed-first-label sampler has infinite variance for T >= 0.9955.

Compares, at x = 1/4 (the crest) over a range of T:
  * the supersolution-tilted sampler (bounded output, Hoeffding CI);
  * the original fixed-rate coding tree (rates 1 and 2);
against an independent pseudo-spectral reference (Strang splitting with the
exact reaction flow; dt-halving check reported).

Theory: docs/research/paper/01-tilted-sampler-theory.md.  Run from the repo
root:  python examples/tilted_long_horizon.py
"""

from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np

from parabolab.pde import ParabolicPDE
from parabolab.tilted import (
    SupEnvelope,
    build_supersolution,
    majorant_horizon,
    sample_tilted,
)
from parabolab.tree import sample_tree

EPS = 0.02  # tau_sup(0.02) ~ 1.2824; tau_sup(0.05) ~ 1.0132
X0 = 0.25
TS = [0.5, 0.8, 1.0, 1.1, 1.2]
N_TILTED = 200_000
N_FIXED = 200_000
OUT = Path(__file__).with_suffix("")


def periodic_pde(T: float, eps: float = EPS) -> ParabolicPDE:
    two_pi = 2 * math.pi
    return ParabolicPDE(
        T=T,
        f=lambda z: z - z**3,
        f_derivatives=(lambda z: 1 - 3 * z * z, lambda z: -6 * z, lambda z: -6.0),
        phi=lambda x: 0.5 + eps * math.sin(two_pi * x),
        phi_derivatives=(lambda x: eps * two_pi * math.cos(two_pi * x),),
        name=f"allen_cahn_periodic(eps={eps}, T={T})",
        reaction_kind="allen_cahn",
    )


def envelope(eps: float = EPS) -> SupEnvelope:
    """Exact sup envelopes: v ranges over [1/2 - eps, 1/2 + eps] within [0, 1/sqrt 3]."""
    lo, hi = 0.5 - eps, 0.5 + eps
    assert hi <= 1 / math.sqrt(3), "f is increasing on the range only below 1/sqrt(3)"
    return SupEnvelope(
        phi=hi,
        f=(hi - hi**3, max(abs(1 - 3 * lo**2), abs(1 - 3 * hi**2)), 6 * hi, 6.0),
        dphi=2 * math.pi * eps,
    )


def reference(T: float, x: float, eps: float = EPS, n: int = 256, dt: float = 1e-4) -> float:
    """Strang splitting: exact heat step in Fourier, exact reaction flow."""
    xs = np.arange(n) / n
    u = 0.5 + eps * np.sin(2 * np.pi * xs)
    k = np.fft.rfftfreq(n, d=1.0 / n)
    half_heat = np.exp(-0.5 * (2 * np.pi * k) ** 2 * dt / 2)
    steps = int(round(T / dt))
    assert abs(steps * dt - T) < 1e-12
    e2 = math.exp(2 * dt)

    for _ in range(steps):
        u = np.fft.irfft(half_heat * np.fft.rfft(u), n)
        u = u * math.exp(dt) / np.sqrt(1 + u * u * (e2 - 1))
        u = np.fft.irfft(half_heat * np.fft.rfft(u), n)
    # spectral interpolation at x
    c = np.fft.rfft(u) / n
    phase = np.exp(2j * np.pi * k * x)
    w = np.full(k.size, 2.0)
    w[0] = 1.0
    if n % 2 == 0:
        w[-1] = 1.0
    return float(np.real(np.sum(w * c * phase)))


def fixed_rate(pde, rate: float, n: int, seed: int):
    rng = np.random.default_rng(seed)
    t0 = time.perf_counter()
    vals = np.empty(n)
    nodes = np.empty(n)
    for i in range(n):
        s = sample_tree(pde, 0.0, X0, rng=rng, rate=rate)
        vals[i], nodes[i] = s.value, s.n_nodes
    return vals, nodes, time.perf_counter() - t0


def main():
    global TAU_SUP
    env = envelope()
    TAU_SUP = majorant_horizon(env)
    print(f"eps={EPS}: guaranteed horizon tau_sup={TAU_SUP:.5f}")
    records = []
    for T in TS:
        ref = reference(T, X0)
        ref_coarse = reference(T, X0, dt=2e-4)
        pde = periodic_pde(T)
        rec = {"T": T, "reference": ref, "reference_dt_halving_diff": abs(ref - ref_coarse)}
        # theta: halfway (in sqrt) to the largest admissible value
        # sqrt(tau_sup / T), capped at 1.02
        theta_max = math.sqrt(TAU_SUP / T)
        for theta in (min(1.02, 1 + 0.5 * (theta_max - 1)),):
            try:
                sup = build_supersolution(env, T, theta=theta)
            except ValueError as exc:
                rec["tilted"] = {"theta": theta, "error": str(exc)}
                continue
            r = sample_tilted(pde, sup, 0.0, X0, N_TILTED, seed=17)
            rec["tilted"] = {
                "theta": theta,
                "estimate": r.estimate,
                "stderr": r.stderr,
                "hoeffding95": r.hoeffding_halfwidth(0.05),
                "bound": r.bound,
                "theta_eff": r.theta_eff,
                "work_bound": r.work_bound,
                "mean_nodes": r.mean_nodes,
                "killed": float(r.killed.mean()),
                "variance": float(r.values.var(ddof=1)),
                "seconds": r.seconds,
            }
            break
        for rate in (1.0, 2.0):
            vals, nodes, secs = fixed_rate(pde, rate, N_FIXED, seed=29)
            # tail diagnostics: share of |sum| from top 0.1% samples
            order = np.sort(np.abs(vals))[::-1]
            rec[f"fixed_rate{rate:g}"] = {
                "estimate": float(vals.mean()),
                "stderr": float(vals.std(ddof=1) / math.sqrt(vals.size)),
                "max_abs": float(order[0]),
                "top0.1pct_share_of_abs_sum": float(order[: max(1, vals.size // 1000)].sum() / order.sum()),
                "mean_nodes": float(nodes.mean()),
                "variance": float(vals.var(ddof=1)),
                "seconds": secs,
            }
        records.append(rec)
        print(json.dumps(rec, indent=1), flush=True)
    OUT.with_suffix(".json").write_text(json.dumps(records, indent=1))
    plot(records)


def plot(records):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4))
    Ts = [r["T"] for r in records]
    ax.plot(Ts, [r["reference"] for r in records], "k-", label="spectral reference")
    for key, style, lab in [
        ("fixed_rate1", "s", "fixed rate 1 (±2 s.e.)"),
        ("fixed_rate2", "^", "fixed rate 2 (±2 s.e.)"),
    ]:
        ax.errorbar(
            np.array(Ts) + (0.006 if key.endswith("2") else -0.006),
            [r[key]["estimate"] for r in records],
            yerr=[2 * r[key]["stderr"] for r in records],
            fmt=style, ms=4, capsize=2, label=lab,
        )
    ok = [r for r in records if "estimate" in r.get("tilted", {})]
    ax.errorbar(
        [r["T"] for r in ok],
        [r["tilted"]["estimate"] for r in ok],
        yerr=[r["tilted"]["hoeffding95"] for r in ok],
        fmt="o", ms=5, capsize=3, color="C3", label="tilted (95% Hoeffding, certified)",
    )
    # log(1 + lam^2 C / 2) / lam, C = 1.530121 (tuple-policy C8, p = 1/2)
    for T_lim, lab in [(0.5682, "rate 1"), (0.7006, "rate 2")]:
        ax.axvline(T_lim, color="0.6", ls=":", lw=1)
        ax.text(T_lim, ax.get_ylim()[1], f" flat L2\n limit, {lab}", fontsize=6, va="top")
    ax.set_xlabel("horizon T")
    ax.set_ylabel(f"u(0, {X0})")
    ax.set_title(f"Periodic Allen–Cahn, v = 1/2 + {EPS} sin(2πx)")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT.with_suffix(".png"), dpi=150)


if __name__ == "__main__":
    main()
