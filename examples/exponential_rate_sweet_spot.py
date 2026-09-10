"""Reproducible numerical experiments on branching clock rate optimization.

Generates:
1. Panel 1: Deterministic second moment U-curves for the binary control problem
   u_t + 1/2 u_xx + u^2 = 0 against Riccati ground truth, showing the sweet spot lambda*(T)
   and contrasting it with the JCP heuristic lambda_JCP(T) = -ln(0.95)/T.
2. Panel 2: Allen-Cahn (d = 1) deterministic second moment curves across lambda,
   identifying the optimal rate lambda*(T) and evaluating empirical variance reduction.
3. Panel 3: Harry Dym equation empirical second moments across sample counts N,
   demonstrating infinite-variance pathology and non-existence of an interior sweet spot.

Outputs:
- examples/exponential_rate_sweet_spot.png
- examples/exponential_rate_sweet_spot.csv
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
from parabolab.pde import FullyNonlinearPDE1D, z_symbols
from parabolab.rate_optimization import (
    finite_depth_moment_derivatives_1d,
    optimize_exponential_rate_1d,
    riccati_binary_second_moment,
)
from parabolab.tree import jcp_rate, sample_tree


def _binary_control_pde(T: float) -> FullyNonlinearPDE1D:
    z = z_symbols(0)
    return FullyNonlinearPDE1D(
        n=0,
        f_expr=z[0] ** 2,
        phi_expr=sp.Integer(1),
        T=T,
    )


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
    lambda_grid_binary = np.linspace(0.2, 3.5, 34)

    panel1_data = {}
    for T in T_binary_list:
        pde = _binary_control_pde(T)
        opt = optimize_exponential_rate_1d(pde, 0.0, 0.0, max_depth=2, bracket=(0.2, 4.0))
        lam_jcp = jcp_rate(T)

        v_riccati = [riccati_binary_second_moment(T, lam) for lam in lambda_grid_binary]
        v_quad = [
            finite_depth_moment_derivatives_1d(pde, 0.0, 0.0, max_depth=2, rate=lam).value
            for lam in lambda_grid_binary
        ]

        panel1_data[T] = {
            "lambda_grid": lambda_grid_binary,
            "v_riccati": v_riccati,
            "v_quad": v_quad,
            "opt_rate": opt.rate,
            "opt_val": opt.second_moment,
            "lam_jcp": lam_jcp,
            "v_jcp": riccati_binary_second_moment(T, lam_jcp),
        }

        records.append({
            "experiment": "binary_control_optimum",
            "T": T,
            "optimal_rate": opt.rate,
            "optimal_second_moment": opt.second_moment,
            "jcp_rate": lam_jcp,
            "jcp_second_moment": panel1_data[T]["v_jcp"],
            "notes": "Riccati exact control",
        })

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
    fieldnames = [
        "experiment",
        "T",
        "samples",
        "rate",
        "optimal_rate",
        "optimal_second_moment",
        "jcp_rate",
        "jcp_second_moment",
        "rate_1_second_moment",
        "empirical_second_moment",
        "max_sample_magnitude",
        "notes",
    ]
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
    for idx, T in enumerate(T_binary_list):
        d = panel1_data[T]
        col = colors_p1[idx]
        ax1.plot(d["lambda_grid"], d["v_riccati"], "-", color=col, label=f"T={T:.2f} (Riccati)")
        ax1.plot(d["lambda_grid"], d["v_quad"], ":", color=col, alpha=0.7)
        ax1.plot(d["opt_rate"], d["opt_val"], "o", color=col, markersize=8, label=f"λ*={d['opt_rate']:.2f}")
        ax1.axvline(d["lam_jcp"], linestyle="--", color=col, alpha=0.4)

    ax1.set_xlabel("Branching Clock Rate $\\lambda$", fontsize=12)
    ax1.set_ylabel("Second Moment $V(T; \\lambda)$", fontsize=12)
    ax1.set_title("Binary Control ($u^2$): Riccati Ground Truth vs Quadrature", fontsize=13)
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper right", fontsize=9)

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
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("examples"),
        help="Directory to store figures and csv results.",
    )
    args = parser.parse_args()
    run_experiments(args.output_dir)
