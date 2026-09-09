"""Numerical study of singular endpoint integrals for the Dym coding tree.

Corroborates the analytic nonintegrability theorem (Theorem 4.1) by evaluating
deterministic truncated inverse-power integrals of Gaussian densities as the inner
cutoff epsilon -> 0.
"""

from __future__ import annotations

import csv
import math
import pathlib
import sys

# Ensure worktree's parabolab package is imported
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import numpy as np

from parabolab import Dx, FNu
from parabolab.integrability import truncated_normal_inverse_power
from parabolab.library import dym_1d


def run_experiment(
    alpha: float = 2.0,
    mean: float = 0.5,
    std: float = 1.0,
    outer: float = 1.0,
) -> None:
    # 1. Print exact singular tuple and alpha-dependent constants
    pde = dym_1d(alpha=alpha)
    f_star = FNu(1.0, (0, 0, 0, 0))
    singular_tuple = (
        FNu(1.0, (0, 0, 1, 0)),  # f_{z2}*
        FNu(1.0, (1, 0, 0, 0)),  # f_{z0}*
        Dx(2),                   # D^2
    )

    print("=== Dym Singular Mechanism Analysis ===")
    print(f"alpha = {alpha}")
    print(f"pde.f_expr = {pde.f_expr}")
    print(f"Target singular tuple in M(f*): {singular_tuple}")
    print(f"Presence in pde.mechanism.tuples(f*): {singular_tuple in pde.mechanism.tuples(f_star)}")

    c_z2 = pde.mechanism.terminal(singular_tuple[0], pde, 1.0)
    # f_{z0} = 8 * alpha^2 / x
    c_z0_num = 8.0 * (alpha**2)
    # phi''(x) = - (2 * |3*alpha|^(2/3) / 9) * |x|^(-4/3)
    phi_d2_coeff = -(2.0 * ((3.0 * abs(alpha)) ** (2.0 / 3.0))) / 9.0

    print(f"f_{{z2}} terminal constant: {c_z2} (exact: -0.5)")
    print(f"f_{{z0}} terminal formula: {c_z0_num:.4f} / x (at x=2: {c_z0_num / 2.0})")
    print(f"phi''(x) leading coefficient: {phi_d2_coeff:.6f} * |x|^(-4/3)")

    # 2. Evaluate cutoffs 1e-1 through 1e-12
    exponents = list(range(1, 13))
    cutoffs = [10.0 ** (-k) for k in exponents]

    g0 = (1.0 / (std * math.sqrt(2.0 * math.pi))) * math.exp(-(mean**2) / (2.0 * (std**2)))
    asymptotic_slope = 2.0 * g0

    rows = []
    print("\nEvaluating truncated integrals across cutoffs...")
    for eps in cutoffs:
        log_inv_eps = math.log(1.0 / eps)
        val_p1 = truncated_normal_inverse_power(mean, std, power=1.0, epsilon=eps, outer=outer)
        val_p43 = truncated_normal_inverse_power(mean, std, power=4.0 / 3.0, epsilon=eps, outer=outer)
        theory_ref = asymptotic_slope * log_inv_eps
        rows.append({
            "epsilon": eps,
            "log_inv_epsilon": log_inv_eps,
            "integral_power_1": val_p1,
            "integral_power_4_3": val_p43,
            "theoretical_asymptotic_term": theory_ref,
        })
        print(f"  eps = {eps:.1e} | log(1/eps) = {log_inv_eps:5.2f} | "
              f"I_1 = {val_p1:8.4f} | I_{{4/3}} = {val_p43:10.4f}")

    # 3. Write raw values to CSV
    out_dir = pathlib.Path(__file__).parent
    csv_path = out_dir / "dym_nonintegrability.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "epsilon",
            "log_inv_epsilon",
            "integral_power_1",
            "integral_power_4_3",
            "theoretical_asymptotic_term",
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nWrote CSV: {csv_path}")

    # 4 & 5. Plot the integrals and overlay theoretical asymptotic slope
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=150)

    log_inv_eps = [r["log_inv_epsilon"] for r in rows]
    vals_p1 = [r["integral_power_1"] for r in rows]
    vals_p43 = [r["integral_power_4_3"] for r in rows]

    # Panel 1: Inverse-first-power singularity
    ax1.plot(log_inv_eps, vals_p1, "o-", color="navy", label=r"Truncated $\int_{\epsilon < |x| < 1} |x|^{-1} g(x) dx$")
    # Shift theoretical line to align with the finest cutoff
    c_offset = vals_p1[-1] - asymptotic_slope * log_inv_eps[-1]
    theory_line = [asymptotic_slope * u + c_offset for u in log_inv_eps]
    ax1.plot(log_inv_eps, theory_line, "--", color="crimson",
             label=f"Theoretical asymptotic slope: $2 g(0) = {asymptotic_slope:.4f}$")
    ax1.set_xlabel(r"$\log(1/\epsilon)$")
    ax1.set_ylabel("Integral value")
    ax1.set_title(r"Inverse-First-Power Singularity ($f_{z_0}^* \sim 1/x$)")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(frameon=True)

    # Panel 2: Sibling inverse-4/3 singularity
    ax2.plot(cutoffs, vals_p43, "s-", color="darkgreen", label=r"Truncated $\int_{\epsilon < |x| < 1} |x|^{-4/3} g(x) dx$")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel(r"Cutoff $\epsilon$ (log scale)")
    ax2.set_ylabel("Integral value (log scale)")
    ax2.set_title(r"Sibling Singularity ($D^2 \sim |x|^{-4/3}$, algebraic $\sim \epsilon^{-1/3}$)")
    ax2.grid(True, which="both", linestyle=":", alpha=0.6)
    ax2.legend(frameon=True)

    fig.suptitle("Dym Coding Tree: Truncated Singular Endpoint Integrals", fontsize=13, fontweight="bold")
    fig.text(
        0.5, 0.01,
        "Note: This numerical evaluation corroborates, but does not prove, the tree nonintegrability theorem (Theorem 4.1).",
        ha="center", fontsize=9, style="italic", color="gray",
    )
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    png_path = out_dir / "dym_nonintegrability.png"
    plt.savefig(png_path)
    plt.close(fig)
    print(f"Wrote plot: {png_path}")


if __name__ == "__main__":
    run_experiment()
