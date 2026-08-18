"""JCP2024 Tables 1/3/5 comparison columns: deep branching (ours, M4) vs
the VENDORED deep BSDE and deep Galerkin baselines (parabolab.vendor, M5).

Baseline configurations follow the authors' comparison.ipynb (deep_branching
@ c06bef2): BSDE with 1000 states, 4 time intervals, lr 1e-2 (decayed),
batchnorm, tanh; DGM with lr 1e-3 fixed, no batchnorm, 10,000 states at
paper budget.  Merton: BSDE runs the 2BSDE variant (second_order=True)
with y clipped to [0, 100] and the authors' |du/dx|-regularized driver
(their notebook cell literally carries the comment "TODO: how to deal
with negative x and y[1] properly???"); the deep Galerkin method is
INAPPLICABLE because its loss divides by the net's second derivative
(JCP2024 Section 4 d) -- reproduced here as a skip, not forced.

Default budgets are reduced (3 runs, branch M as in the M4 scripts,
DGM 1000 states); --full switches to paper budgets (10 runs, branch
M=100,000/30,000/10,000, DGM 10,000 states).  CPU by default.

Paper reference values (Tesla P100 GPU, 10 runs) are printed alongside.
"""

from __future__ import annotations

import argparse
import functools
import time

import numpy as np
import sympy as sp
import torch

import parabolab.deep as deep
from parabolab.library import allen_cahn_nd, exponential_gradient_nd, merton_hjb
from parabolab.pde import x_symbols, z_symbols
from parabolab.vendor import (
    BSDENet,
    DGMNet,
    bsde_functions,
    dgm_functions,
    eval_bsde_grid,
    eval_dgm_grid,
)


def merton_baseline_overrides():
    """The authors' regularized Merton driver/terminal condition
    (comparison.ipynb cell 21): |z1| inside the fractional power and
    |x| inside phi, so that negative intermediate values during BSDE
    training do not produce NaNs.  gamma = 0.5, so 1 - 1/gamma = -1."""
    mu, sigma, gamma, rho = 0.03, 0.1, 0.5, 0.01
    z = z_symbols(2)
    (x0,) = x_symbols(1)
    f = (
        -z[2] / 2
        - mu**2 / (2 * sigma**2) * z[1] ** 2 / z[2]
        + gamma / (1 - gamma) * sp.Abs(z[1]) ** (1 - 1 / gamma)
        - rho * z[0]
    )
    phi = sp.Abs(x0) ** (1 - gamma) / (1 - gamma)
    return f, phi


CASES = {
    "allen_cahn_d1": dict(
        table="Table 1", factory=functools.partial(allen_cahn_nd, d=1, T=0.5),
        x_lo=-8.0, x_hi=8.0, m_reduced=10_000, m_full=100_000,
        paper=dict(branch=("1.32E-03", "28m"), bsde=("4.60E-03", "101m"),
                   dgm=("1.40E-03", "53m")),
    ),
    "allen_cahn_d5": dict(
        table="Table 1", factory=functools.partial(allen_cahn_nd, d=5, T=0.5),
        x_lo=-8.0, x_hi=8.0, m_reduced=10_000, m_full=100_000,
        paper=dict(branch=("3.63E-03", "110m"), bsde=("4.71E-03", "170m"),
                   dgm=("6.83E-03", "134m")),
    ),
    "exponential_d1": dict(
        table="Table 3",
        factory=functools.partial(exponential_gradient_nd, d=1, T=0.05),
        x_lo=-4.0, x_hi=4.0, m_reduced=3_000, m_full=30_000,
        paper=dict(branch=("1.17E-02", "42m"), bsde=("1.39E-02", "101m"),
                   dgm=("2.53E-02", "61m")),
    ),
    "merton_d1": dict(
        table="Table 5", factory=merton_hjb,
        x_lo=100.0, x_hi=200.0, m_reduced=1_000, m_full=10_000,
        branch_kwargs=dict(activation="relu"),  # paper's fix, Section 4 d)
        bsde_kwargs=dict(y_lo=0.0, y_hi=100.0),  # comparison.ipynb cell 22
        overrides=merton_baseline_overrides,
        dgm_inapplicable="DGM loss divides by the net's second derivative "
                         "(JCP2024 Sec. 4 d); the authors disable it too",
        paper=dict(branch=("8.49E-03", "54m"), bsde=("1.61E+00", "184m"),
                   dgm=("n/a", "-")),
    ),
}


def grid_and_true(pde, x_lo, x_hi, n=101):
    grid = np.linspace(x_lo, x_hi, n)
    xs = np.full((n, pde.d), 0.5 * (x_lo + x_hi))
    xs[:, 0] = grid
    true = np.array([pde.exact_solution(0.0, xs[i]) for i in range(n)])
    return xs, true


def run_bsde(pde, x_lo, x_hi, xs, true, *, epochs, runs, f_expr=None,
             phi_expr=None, extra=None):
    kw = bsde_functions(pde, f_expr=f_expr, phi_expr=phi_expr)
    kw.update(extra or {})
    l1s, secs = [], []
    for seed in range(runs):
        torch.manual_seed(seed)
        model = BSDENet(x_lo=x_lo, x_hi=x_hi, epochs=epochs,
                        bsde_nb_states=1000, bsde_nb_time_intervals=4, **kw)
        t0 = time.perf_counter()
        model.train_and_eval()
        secs.append(time.perf_counter() - t0)
        pred = eval_bsde_grid(model, xs)
        l1s.append(float(np.abs(pred - true).mean()))
        print(f"    bsde run {seed}: L1 {l1s[-1]:.2e} ({secs[-1]:.0f}s)",
              flush=True)
    return np.array(l1s), np.array(secs)


def run_dgm(pde, x_lo, x_hi, xs, true, *, epochs, runs, nb_states,
            f_expr=None, phi_expr=None):
    kw = dgm_functions(pde, f_expr=f_expr, phi_expr=phi_expr)
    tx = np.column_stack([np.zeros(len(xs)), xs])
    l1s, secs = [], []
    for seed in range(runs):
        torch.manual_seed(seed)
        model = DGMNet(x_lo=x_lo, x_hi=x_hi, epochs=epochs,
                       dgm_nb_states=nb_states, **kw)
        t0 = time.perf_counter()
        model.train_and_eval()
        secs.append(time.perf_counter() - t0)
        pred = eval_dgm_grid(model, tx)
        l1s.append(float(np.abs(pred - true).mean()))
        print(f"    dgm  run {seed}: L1 {l1s[-1]:.2e} ({secs[-1]:.0f}s)",
              flush=True)
    return np.array(l1s), np.array(secs)


def fmt(l1s, secs):
    sd = f"{l1s.std(ddof=1):.2e}" if len(l1s) > 1 else "n/a"
    return f"{l1s.mean():.2e} (SD {sd}), {secs.mean():.0f}s/run"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cases", nargs="+", default=list(CASES),
                   choices=list(CASES))
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--epochs", type=int, default=3000)
    p.add_argument("--jobs", type=int, default=6)
    p.add_argument("--device", default="cpu")
    p.add_argument("--full", action="store_true",
                   help="paper budgets: 10 runs, full M, DGM 10,000 states")
    args = p.parse_args()
    runs = 10 if args.full else args.runs
    dgm_states = 10_000 if args.full else 1_000

    summary = []
    for name in args.cases:
        c = CASES[name]
        pde = c["factory"]()
        m = c["m_full"] if args.full else c["m_reduced"]
        xs, true = grid_and_true(pde, c["x_lo"], c["x_hi"])
        f_ov = phi_ov = None
        if "overrides" in c:
            f_ov, phi_ov = c["overrides"]()

        print(f"\n=== {c['table']}: {pde.name} "
              f"(runs={runs}, branch M={m}, dgm states={dgm_states}) ===",
              flush=True)

        print("  deep branching (ours):", flush=True)
        res = deep.run_experiment(
            c["factory"], x_lo=c["x_lo"], x_hi=c["x_hi"],
            n_states=1000, m_samples=m, epochs=args.epochs, n_runs=runs,
            n_jobs=args.jobs, device=args.device, keep_nets=False,
            **c.get("branch_kwargs", {}),
        )
        branch_l1 = res.l1
        branch_secs = res.datagen_seconds + res.train_seconds

        print("  deep BSDE (vendored):", flush=True)
        bsde_l1, bsde_secs = run_bsde(
            pde, c["x_lo"], c["x_hi"], xs, true, epochs=args.epochs,
            runs=runs, f_expr=f_ov, phi_expr=phi_ov,
            extra=c.get("bsde_kwargs"),
        )

        if "dgm_inapplicable" in c:
            dgm_l1 = dgm_secs = None
            print(f"  deep Galerkin: SKIPPED -- {c['dgm_inapplicable']}",
                  flush=True)
        else:
            print("  deep Galerkin (vendored):", flush=True)
            dgm_l1, dgm_secs = run_dgm(
                pde, c["x_lo"], c["x_hi"], xs, true, epochs=args.epochs,
                runs=runs, nb_states=dgm_states,
                f_expr=f_ov, phi_expr=phi_ov,
            )

        summary.append((name, c, branch_l1, branch_secs,
                        bsde_l1, bsde_secs, dgm_l1, dgm_secs))

    print("\n" + "=" * 78)
    print("SUMMARY  (L1 mean (SD), runtime/run; paper = 10 runs on P100 GPU)")
    print("=" * 78)
    for name, c, bl1, bs, sl1, ss, gl1, gs in summary:
        pp = c["paper"]
        print(f"\n{c['table']}  {name}:")
        print(f"  deep branching  ours {fmt(bl1, bs):<38} "
              f"paper {pp['branch'][0]}, {pp['branch'][1]}")
        print(f"  deep BSDE       ours {fmt(sl1, ss):<38} "
              f"paper {pp['bsde'][0]}, {pp['bsde'][1]}")
        if gl1 is None:
            print(f"  deep Galerkin   inapplicable "
                  f"(paper: {pp['dgm'][0]})")
        else:
            print(f"  deep Galerkin   ours {fmt(gl1, gs):<38} "
                  f"paper {pp['dgm'][0]}, {pp['dgm'][1]}")


if __name__ == "__main__":
    main()
