"""Reproducible numerical experiments on branching clock rate optimization.

Generates:
1. Panel 1: Deterministic second moment U-curves for the binary control problem
   u_t + 1/2 u_xx + u^2 = 0 using the standard binary mechanism, distinguishing
   the full-tree Riccati optimum from the finite-depth numerical optimum
   and contrasting it with the JCP heuristic lambda_JCP(T) = -ln(0.95)/T.
2. Panel 2: Allen-Cahn (d = 1) deterministic second moment curves across lambda,
   identifying the optimal rate lambda*(T) and evaluating empirical variance reduction.
3. Panel 3: Harry Dym equation empirical second moments across sample counts N,
   demonstrating infinite-variance pathology and non-existence of an interior sweet spot.

Outputs:
- examples/exponential_rate_sweet_spot.png
- examples/exponential_rate_sweet_spot.csv

Use --binary-only --output-dir PATH for a separate corrected control report
without running the Allen-Cahn or Dym experiments.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from parabolab.library import allen_cahn_wave_1d, dym_1d
from parabolab.mechanism import Id
from parabolab.moments import MomentQuadrature
from parabolab.pde import FullyNonlinearPDE1D, z_symbols
from parabolab.rate_optimization import (
    finite_depth_moment_derivatives_1d,
    optimize_exponential_rate_1d,
    riccati_binary_second_moment,
)
from parabolab.tree import jcp_rate, sample_tree


class BinaryControlMechanism:
    """Standard binary representation of u^2 with terminal value one.

    The symbolic PDE's default derivative-coded mechanism represents the same
    PDE but has a different second moment. Pass this mechanism explicitly.
    """

    @staticmethod
    def tuples(code):
        return ((Id(), Id()),)

    @staticmethod
    def terminal(code, pde, x):
        return 1.0

    @staticmethod
    def is_identically_zero(code, pde):
        return False


def _binary_control_pde(T: float) -> FullyNonlinearPDE1D:
    z = z_symbols(0)
    return FullyNonlinearPDE1D(
        n=0,
        f_expr=z[0] ** 2,
        phi_expr=sp.Integer(1),
        T=T,
    )


def _binary_oracle_optimum(T: float, bracket=(0.2, 4.0)) -> float:
    """Numerically locate the stationary rate of the exact full-tree formula.

    The control horizons use a bracket wholly inside the finite-moment domain.
    On that domain the moment is strictly convex; its derivative has the sign
    of T*rate*(rate**2 + 1) - 2*expm1(rate*T).
    """
    lo, hi = bracket
    if not all(math.isfinite(riccati_binary_second_moment(T, rate)) for rate in bracket):
        raise ValueError("Oracle bracket must lie in the finite-moment domain")

    def stationarity(rate):
        return T * rate * (rate**2 + 1.0) - 2.0 * math.expm1(rate * T)

    if not stationarity(lo) < 0.0 < stationarity(hi):
        raise ValueError("Oracle bracket must enclose the stationary rate")
    while hi - lo > 1e-12:
        mid = (lo + hi) / 2.0
        if stationarity(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def _binary_control_experiment(T: float):
    pde = _binary_control_pde(T)
    # Spatial integration is exact with one node for this constant control.
    settings = dict(max_depth=2, mechanism=BinaryControlMechanism,
                    quadrature=MomentQuadrature(time_order=8, normal_order=1))
    opt = optimize_exponential_rate_1d(pde, 0.0, 0.0, bracket=(0.2, 4.0),
                                     tol=1e-9, **settings)
    if not opt.converged:
        raise RuntimeError(f"Binary depth-2 optimization did not converge at T={T}")
    oracle_rate = _binary_oracle_optimum(T)
    lam_jcp = jcp_rate(T)
    lambda_grid = np.linspace(0.2, 3.5, 34)
    data = {
        "lambda_grid": lambda_grid,
        "v_riccati": [riccati_binary_second_moment(T, rate) for rate in lambda_grid],
        "v_quad": [finite_depth_moment_derivatives_1d(
            pde, 0.0, 0.0, rate=rate, **settings).value for rate in lambda_grid],
        "opt_rate": opt.rate,
        "opt_val": opt.second_moment,
        "oracle_rate": oracle_rate,
        "oracle_val": riccati_binary_second_moment(T, oracle_rate),
        "lam_jcp": lam_jcp,
    }
    record = {
        "experiment": "standard_binary_control",
        "T": T,
        "mechanism": "Id -> (Id, Id); terminal=1; q=1",
        "max_depth": settings["max_depth"],
        "time_order": settings["quadrature"].time_order,
        "normal_order": settings["quadrature"].normal_order,
        "finite_depth_optimal_rate": opt.rate,
        "finite_depth_optimal_second_moment": opt.second_moment,
        "full_tree_at_finite_depth_rate": riccati_binary_second_moment(T, opt.rate),
        "full_tree_optimal_rate": oracle_rate,
        "full_tree_optimal_second_moment": data["oracle_val"],
        "jcp_rate": lam_jcp,
        "full_tree_jcp_second_moment": riccati_binary_second_moment(T, lam_jcp),
        "finite_depth_jcp_second_moment": finite_depth_moment_derivatives_1d(
            pde, 0.0, 0.0, rate=lam_jcp, **settings).value,
        "full_tree_rate_1_second_moment": riccati_binary_second_moment(T, 1.0),
        "finite_depth_d_rate": opt.d_rate,
        "notes": "Full-tree formula evaluated exactly; its stationary rate solved numerically. "
                 "Finite depth kills branches at the cutoff; comparisons must use one objective.",
    }
    return data, record


def _plot_binary_control(ax, panel_data):
    for T, color in zip(panel_data, ["tab:blue", "tab:orange", "tab:green"]):
        data = panel_data[T]
        ax.plot(data["lambda_grid"], data["v_riccati"], "-", color=color,
                label=f"T={T:.2f}: full tree")
        ax.plot(data["lambda_grid"], data["v_quad"], ":", color=color,
                label=f"T={T:.2f}: depth 2")
        ax.plot(data["oracle_rate"], data["oracle_val"], "*", color=color, markersize=11)
        ax.plot(data["opt_rate"], data["opt_val"], "o", color=color, markersize=5)
        ax.axvline(data["lam_jcp"], linestyle="--", color=color, alpha=0.4,
                   label="JCP rates" if T == next(iter(panel_data)) else None)
    ax.set_xlabel("Branching clock rate $\\lambda$")
    ax.set_ylabel("Second moment")
    ax.set_title("Standard binary control: full-tree (*) and depth-2 (o) optima")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(fontsize=8)


def run_binary_experiments(output_dir: Path):
    """Write separate artifacts; never overwrite the historical three-panel files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    panel_data, records = {}, []
    for T in (0.05, 0.10, 0.15):
        panel_data[T], record = _binary_control_experiment(T)
        records.append(record)
    csv_path = output_dir / "standard_binary_rate_audit.csv"
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    fig, ax = plt.subplots(figsize=(9, 5.2))
    _plot_binary_control(ax, panel_data)
    fig.tight_layout()
    fig.savefig(output_dir / "standard_binary_rate_audit.png", dpi=180)
    plt.close(fig)
    print(f"Corrected binary-only report saved to {output_dir}")


def run_experiments(output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "exponential_rate_sweet_spot.csv"
    png_path = output_dir / "exponential_rate_sweet_spot.png"

    print("--- Starting Exponential Rate Sweet Spot Experiments ---")
    records = []

    # ---------------------------------------------------------
    # Panel 1: Binary Control Riccati Ground Truth vs Quadrature
    # ---------------------------------------------------------
    print("Evaluating Panel 1: Binary Riccati Control...")
    T_binary_list = [0.05, 0.10, 0.15]
    panel1_data = {}
    for T in T_binary_list:
        panel1_data[T], record = _binary_control_experiment(T)
        records.append(record)

    # ---------------------------------------------------------
    # Panel 2: Allen-Cahn (d = 1) Deterministic Rate Sweet Spot
    # ---------------------------------------------------------
    print("Evaluating Panel 2: Allen-Cahn 1D...")
    T_ac_list = [0.05, 0.10, 0.20]
    lambda_grid_ac = np.linspace(0.2, 3.0, 29)

    panel2_data = {}
    for T in T_ac_list:
        pde_ac = allen_cahn_wave_1d(T=T)
        opt_ac = optimize_exponential_rate_1d(pde_ac, 0.0, 0.0, max_depth=1, bracket=(0.2, 4.0))
        lam_jcp = jcp_rate(T)

        v_quad_ac = [
            finite_depth_moment_derivatives_1d(pde_ac, 0.0, 0.0, max_depth=1, rate=lam).value
            for lam in lambda_grid_ac
        ]

        v_opt = opt_ac.second_moment
        v_jcp_eval = finite_depth_moment_derivatives_1d(pde_ac, 0.0, 0.0, max_depth=1, rate=lam_jcp).value
        v_1_eval = finite_depth_moment_derivatives_1d(pde_ac, 0.0, 0.0, max_depth=1, rate=1.0).value

        panel2_data[T] = {
            "lambda_grid": lambda_grid_ac,
            "v_quad": v_quad_ac,
            "opt_rate": opt_ac.rate,
            "opt_val": v_opt,
            "lam_jcp": lam_jcp,
            "v_jcp": v_jcp_eval,
            "v_rate_1": v_1_eval,
        }

        records.append({
            "experiment": "allen_cahn_1d_optimum",
            "T": T,
            "optimal_rate": opt_ac.rate,
            "optimal_second_moment": v_opt,
            "jcp_rate": lam_jcp,
            "jcp_second_moment": v_jcp_eval,
            "rate_1_second_moment": v_1_eval,
            "notes": "Allen-Cahn traveling wave x=0.0",
        })

    # ---------------------------------------------------------
    # Panel 3: Harry Dym Non-Integrability Across Sample Sizes
    # ---------------------------------------------------------
    print("Evaluating Panel 3: Harry Dym Pathology...")
    pde_dym = dym_1d(T=0.01)
    rates_dym = [0.2, 0.5, 1.0, 2.0, 5.0]
    sample_sizes = [1_000, 10_000, 50_000]

    panel3_data = {}
    for N in sample_sizes:
        panel3_data[N] = {"rates": rates_dym, "emp_second_moment": [], "emp_max_h": []}
        for rate in rates_dym:
            rng = np.random.default_rng(20260910 + int(rate * 100))
            h_sq = np.empty(N)
            max_val = 0.0
            for i in range(N):
                s = sample_tree(pde_dym, 0.0, 1.5, rng=rng, rate=rate)
                val_sq = s.value**2
                h_sq[i] = val_sq
                if abs(s.value) > max_val:
                    max_val = abs(s.value)

            emp_v = float(np.mean(h_sq))
            panel3_data[N]["emp_second_moment"].append(emp_v)
            panel3_data[N]["emp_max_h"].append(max_val)

            records.append({
                "experiment": "harry_dym_sample_sweep",
                "T": pde_dym.T,
                "samples": N,
                "rate": rate,
                "empirical_second_moment": emp_v,
                "max_sample_magnitude": max_val,
                "notes": "Dym x=1.5 infinite second moment",
            })

    # Save CSV
    print(f"Writing CSV report to {csv_path}...")
    fieldnames = list(dict.fromkeys(key for record in records for key in record))
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    # Plot 3-Panel Figure
    print(f"Generating publication plot to {png_path}...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.2))

    # Panel 1
    ax1 = axes[0]
    colors_p1 = ["tab:blue", "tab:orange", "tab:green"]
    _plot_binary_control(ax1, panel1_data)

    # Panel 2
    ax2 = axes[1]
    for idx, T in enumerate(T_ac_list):
        d = panel2_data[T]
        col = colors_p1[idx]
        ax2.plot(d["lambda_grid"], d["v_quad"], "-", color=col, label=f"AC T={T:.2f}")
        ax2.plot(d["opt_rate"], d["opt_val"], "o", color=col, markersize=8, label=f"λ*={d['opt_rate']:.2f}")

    ax2.set_xlabel("Branching Clock Rate $\\lambda$", fontsize=12)
    ax2.set_ylabel("Second Moment $V_{1}^{(2)}(0, 0; \\lambda)$", fontsize=12)
    ax2.set_title("Allen--Cahn (1D): Deterministic U-Curves & Sweet-Spot", fontsize=13)
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper right", fontsize=9)

    # Panel 3
    ax3 = axes[2]
    markers = ["s", "^", "o"]
    for idx, N in enumerate(sample_sizes):
        d = panel3_data[N]
        ax3.plot(d["rates"], d["emp_second_moment"], marker=markers[idx], label=f"N={N:,}")

    ax3.set_yscale("log")
    ax3.set_xlabel("Branching Clock Rate $\\lambda$", fontsize=12)
    ax3.set_ylabel("Empirical Second Moment $\\frac{1}{N}\\sum H_i^2$ (log scale)", fontsize=12)
    ax3.set_title("Harry Dym: Non-Integrability & Absence of Sweet-Spot", fontsize=13)
    ax3.grid(True, linestyle=":", alpha=0.6)
    ax3.legend(loc="upper right", fontsize=10)

    plt.tight_layout()
    plt.savefig(png_path, dpi=300)
    plt.close()
    print(f"Artifacts successfully saved to {output_dir}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary-only", action="store_true",
                        help="Run only the corrected standard-binary control.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("examples"),
        help="Directory to store figures and csv results.",
    )
    args = parser.parse_args()
    if args.binary_only:
        run_binary_experiments(args.output_dir)
    else:
        run_experiments(args.output_dir)
