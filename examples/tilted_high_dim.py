"""Tilted coding tree in d = 100: dimension-free majorant vs uniform tuples.

Allen-Cahn u_t + (1/2) Laplacian u + u - u^3 = 0 on R^d, d = 100, with
planar periodic data v(x) = psi(a.x), psi(s) = 1/2 + eps sin(2 pi s),
a = (1, ..., 1)/sqrt(d).  Since a.B is a standard 1-D Brownian motion, the
exact solution is u(t, x) = U(t, a.x) with U the 1-D periodic solution;
the reference is the pseudo-spectral solver of ``tilted_long_horizon``.
The samplers simulate the full 100-dimensional tree.

Compared at x0 = a/4 (a.x0 = 1/4):
  * tilted sampler, sup envelopes l_i = |a_i| 2 pi eps (l_D = 2 pi eps,
    independent of d), so its guaranteed horizon equals the 1-D one;
  * fixed-rate coding tree with UNIFORM tuples over the 1 + d tuples of
    each F_k code (the JCP/NPP mechanism), main-label probability 1/(d+1);
  * fixed-rate with a TUNED main-label probability 0.95.
For flat data, Proposition F gives the finite-variance limits
log(1 + lam^2 p tau_2)/lam; they are printed for orientation only.

Run from the repo root:  python examples/tilted_high_dim.py
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from tilted_long_horizon import reference  # noqa: E402

from parabolab.tilted import (  # noqa: E402
    SemilinearProblem,
    SupEnvelope,
    build_supersolution,
    majorant_horizon,
    sample_tilted,
)

D = 100
EPS = 0.02
TS = [0.02, 0.05, 0.1, 0.3, 0.6, 1.0, 1.2]
N = 100_000
TAU2 = 1.5301212285131  # int dz / Phi_2, flat Allen-Cahn at 1/2
OUT = Path(__file__).with_suffix("")

A = np.full(D, 1.0 / math.sqrt(D))
X0 = A / 4.0
TWO_PI = 2.0 * math.pi
FKS = (lambda z: z - z**3, lambda z: 1 - 3 * z * z, lambda z: -6 * z, lambda z: -6.0)


def problem(T: float) -> SemilinearProblem:
    return SemilinearProblem(
        T=T,
        d=D,
        fks=FKS,
        phi=lambda z: 0.5 + EPS * math.sin(TWO_PI * float(A @ z)),
        dphi=lambda z, i: A[i] * EPS * TWO_PI * math.cos(TWO_PI * float(A @ z)),
        name=f"allen_cahn_planar(d={D}, eps={EPS}, T={T})",
    )


def envelope() -> SupEnvelope:
    lo, hi = 0.5 - EPS, 0.5 + EPS
    crit = [1 / math.sqrt(3)] if lo <= 1 / math.sqrt(3) <= hi else []
    return SupEnvelope(
        phi=hi,
        f=(max(abs(z - z**3) for z in [lo, hi, *crit]),
           max(abs(1 - 3 * lo**2), abs(1 - 3 * hi**2)), 6 * hi, 6.0),
        dphi=tuple(np.abs(A) * TWO_PI * EPS),
    )


def fixed_rate(prob: SemilinearProblem, lam: float, p_main: float, n: int, seed: int):
    """Fixed-rate coding tree over the same expansion (zero codes pruned).

    F_k -> (F_0, F_{k+1}) with probability p_main; F_k -> (D_i, D_i, F_{k+2})
    with probability (1 - p_main)/d for each i; Id and D_i have one tuple.
    """
    m = len(prob.fks) - 1
    d = prob.d
    rng = np.random.default_rng(seed)
    count = [0]

    def node(code, k, s, y, i):
        # code: "I", "F" (with k), "D" (with direction i)
        count[0] += 1
        tau = rng.exponential(1.0 / lam)
        if tau >= s:
            z = y + math.sqrt(s) * rng.standard_normal(d)
            if code == "I":
                g = prob.phi(z)
            elif code == "D":
                g = prob.dphi(z, i)
            else:
                g = prob.fks[k](prob.phi(z))
            return g * math.exp(lam * s)
        z = y + math.sqrt(tau) * rng.standard_normal(d)
        r = s - tau
        dens = lam * math.exp(-lam * tau)
        if code == "I":
            return node("F", 0, r, z, -1) / dens
        if code == "D":
            return node("F", 1, r, z, -1) * node("D", 0, r, z, i) / dens
        if rng.random() < p_main:
            if k + 1 > m:
                return 0.0
            return node("F", 0, r, z, -1) * node("F", k + 1, r, z, -1) / (p_main * dens)
        j = int(rng.integers(d))
        if k + 2 > m:
            return 0.0
        q = (1.0 - p_main) / d
        return (-0.5 * node("D", 0, r, z, j) * node("D", 0, r, z, j)
                * node("F", k + 2, r, z, -1) / (q * dens))

    vals = np.empty(n)
    nodes = np.empty(n)
    t0 = time.perf_counter()
    for idx in range(n):
        count[0] = 0
        vals[idx] = node("I", 0, prob.T, X0.copy(), -1)
        nodes[idx] = count[0]
    return vals, nodes, time.perf_counter() - t0


def summarize(vals, nodes, secs, ref):
    se = float(vals.std(ddof=1) / math.sqrt(vals.size))
    order = np.sort(np.abs(vals))[::-1]
    return {
        "estimate": float(vals.mean()),
        "stderr": se,
        "z": float((vals.mean() - ref) / se) if se > 0 else float("nan"),
        "max_abs": float(order[0]),
        "top0.1pct_share_of_abs_sum": float(order[: max(1, vals.size // 1000)].sum() / order.sum()),
        "mean_nodes": float(nodes.mean()),
        "variance": float(vals.var(ddof=1)),
        "seconds": secs,
    }


def main():
    env = envelope()
    tau_sup = majorant_horizon(env)
    print(f"d={D}: l_D={env.dphi_norm:.5f}, guaranteed horizon tau_sup={tau_sup:.5f}")
    K = 0.804742342549412
    limits = {}
    for label, p in [("uniform", 1.0 / (D + 1)), ("tuned", 0.95)]:
        for lam in (1.0, 2.0):
            limits[f"{label}_rate{lam:g}"] = math.log(1 + lam * lam * p * TAU2) / lam
        limits[f"{label}_best_rate"] = K * math.sqrt(p * TAU2)
    print("flat-data L2 limits (Prop. F):", json.dumps(limits, indent=1))
    records = []
    for T in TS:
        ref = reference(T, 0.25, eps=EPS)
        prob = problem(T)
        rec = {"T": T, "reference": ref}
        theta = min(1.02, 1 + 0.5 * (math.sqrt(tau_sup / T) - 1))
        sup = build_supersolution(env, T, theta=theta)
        r = sample_tilted(prob, sup, 0.0, X0, N, seed=41)
        rec["tilted"] = summarize(r.values, r.node_counts, r.seconds, ref)
        rec["tilted"].update(theta=theta, bound=r.bound, hoeffding95=r.hoeffding_halfwidth(0.05),
                             killed=float(r.killed.mean()))
        for label, p, lam in [("uniform", 1.0 / (D + 1), 2.0), ("tuned", 0.95, 2.0)]:
            vals, nodes, secs = fixed_rate(prob, lam, p, N, seed=43)
            rec[f"{label}_rate{lam:g}"] = summarize(vals, nodes, secs, ref)
        records.append(rec)
        print(json.dumps(rec, indent=1), flush=True)
    OUT.with_suffix(".json").write_text(json.dumps({"limits": limits, "records": records}, indent=1))
    plot(records)


def plot(records):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4))
    Ts = np.array([r["T"] for r in records])
    for key, style, lab, dx in [
        ("uniform_rate2", "s", "fixed rate 2, uniform tuples (±2 s.e.)", -0.012),
        ("tuned_rate2", "^", "fixed rate 2, tuned p=0.95 (±2 s.e.)", 0.012),
    ]:
        ax.errorbar(Ts + dx, [r[key]["estimate"] - r["reference"] for r in records],
                    yerr=[2 * r[key]["stderr"] for r in records], fmt=style, ms=4,
                    capsize=2, label=lab)
    ax.errorbar(Ts, [r["tilted"]["estimate"] - r["reference"] for r in records],
                yerr=[r["tilted"]["hoeffding95"] for r in records], fmt="o", ms=5,
                capsize=3, color="C3", label="tilted (95% Hoeffding, certified)")
    ax.axhline(0.0, color="k", lw=0.8)
    ax.set_ylim(-0.2, 0.2)
    ax.set_xlabel("horizon T")
    ax.set_ylabel("estimate − reference")
    ax.set_title(f"Allen–Cahn in d = {D}, planar data 1/2 + {EPS} sin(2π a·x)")
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT.with_suffix(".png"), dpi=150)


if __name__ == "__main__":
    main()
