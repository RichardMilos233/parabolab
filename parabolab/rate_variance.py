"""Rate sensitivity and variance analysis tools for branching Monte Carlo.

Provides diagnostic and experimental machinery to analyze how estimator
variance Var(H) varies with the exponential branching clock rate lambda:
* Evaluating the theoretical short-horizon optimal rate lambda_theory(x) ~= |f(phi(x))|/|phi(x)|.
* Computing the strictly convex continuous variance curve via deterministic quadrature
  (or closed-form Riccati oracle for binary control).
* Running empirical Monte Carlo trials across candidate rates with exact standard errors.
* Comparing sweet-spot agreement and variance reduction across PDE families.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np

from .mechanism import Id
from .moments import MomentQuadrature
from .pde import ParabolicPDE
from .rate_optimization import (
    finite_depth_moment_derivatives_1d,
    optimize_exponential_rate_1d,
    riccati_binary_optimal_rate,
    riccati_binary_second_moment,
    short_time_rate_1d,
)
from .tree import sample_tree


@dataclass(frozen=True)
class RateVarianceSweep:
    """Outcome of a rate-variance sweep for a single PDE configuration."""

    pde: ParabolicPDE
    x: float
    t: float
    title: str
    lambda_theory: float
    optimal_rate: float
    optimal_variance: float
    diff_pct: float
    var_reduction_pct: float
    quad_rates: np.ndarray
    quad_variance: np.ndarray
    mc_rates: np.ndarray
    mc_variance: np.ndarray
    mc_stderr: np.ndarray
    mc_means: np.ndarray
    mc_stderrs: np.ndarray
    mc_nodes: np.ndarray
    curve_label: str

    def table(self) -> RateVarianceSweep:
        """Print detailed table of variance across rates for this sweep."""
        print(f"\nRate-Variance Sweep: {self.title}")
        print(f"  Theoretical lambda: {self.lambda_theory:.4f}, Optimal lambda: {self.optimal_rate:.4f} (error: {self.diff_pct:.2f}%)")
        print(f"  {'lambda':>8} | {'Recurrence Var':>14} | {'MC Var +/- SE':>24} | {'Diff (%)':>9} | {'z-score':>8}")
        print("  " + "-" * 72)
        exact_u = (
            self.pde.exact_solution(self.t, self.x)
            if self.pde.exact_solution is not None
            else 0.0
        )
        for lam, v_mc, se_mc in zip(self.mc_rates, self.mc_variance, self.mc_stderr):
            idx = int(np.argmin(np.abs(self.quad_rates - lam)))
            v_det = float(self.quad_variance[idx])
            rel_d = abs(v_mc - v_det) / v_det * 100 if v_det > 0 else 0.0
            z_score = abs(v_mc - v_det) / se_mc if se_mc > 0 else 0.0
            print(f"  {lam:8.2f} | {v_det:14.6f} | {v_mc:11.6f} +/- {se_mc:.6f} | {rel_d:8.2f}% | {z_score:7.2f}σ")
        return self

    def plot(
        self,
        ax: Optional[plt.Axes] = None,
        path: Optional[Union[str, Path]] = None,
        figsize: tuple[float, float] = (7.5, 5.5),
    ) -> RateVarianceSweep:
        """Plot the Var(H) vs lambda curve on an axes, or save to path."""
        standalone = ax is None
        if standalone:
            fig, ax = plt.subplots(figsize=figsize)

        ax.plot(self.quad_rates, self.quad_variance, color="#1f77b4", linewidth=2.2, label=self.curve_label)
        ax.errorbar(
            self.mc_rates, self.mc_variance, yerr=self.mc_stderr, fmt="o", color="#d62728",
            ecolor="#d62728", elinewidth=1.5, capsize=3.5, markersize=5,
            label=f"Empirical MC ($N = {len(self.mc_rates)} \\times$ trials)",
        )
        ax.axvline(
            self.optimal_rate, color="#2ca02c", linestyle=":", linewidth=2.0,
            label=rf"Numerical/Oracle $\lambda^* = {self.optimal_rate:.3f}$",
        )
        ax.axvline(
            self.lambda_theory, color="#ff7f0e", linestyle="--", linewidth=1.8,
            label=rf"Theoretical $\lambda_{{\mathrm{{theory}}}} = {self.lambda_theory:.3f}$",
        )

        ax.set_xlabel(r"Branching clock rate $\lambda$", fontsize=10.5)
        ax.set_ylabel(r"Estimator Variance $\mathrm{Var}(H)$", fontsize=10.5)
        ax.set_title(
            self.title + f"\n$\\lambda_{{\\mathrm{{theory}}}} = {self.lambda_theory:.4f} \\approx \\lambda^* = {self.optimal_rate:.4f}$ (error: {self.diff_pct:.2f}%)",
            fontsize=10.8, fontweight="bold", pad=7,
        )
        ax.grid(True, linestyle=":", alpha=0.55)
        ax.legend(loc="upper center", fontsize=8.0, framealpha=0.92)

        y_max = max(self.mc_variance.max() * 1.15, self.quad_variance.max() * 1.08)
        ax.set_ylim(-0.0005, y_max)

        arrow_dx = (self.quad_rates[-1] - self.quad_rates[0]) * 0.18
        arrow_dy = y_max * 0.18
        ax.annotate(
            rf"$\mathbf{{Sweet\ Spot}}$" + "\n" + rf"$\lambda^* \approx {self.optimal_rate:.3f}$" + "\n" + rf"$\mathrm{{Var}} \approx {self.optimal_variance:.2e}$",
            xy=(self.optimal_rate, self.optimal_variance),
            xytext=(self.optimal_rate + arrow_dx, self.optimal_variance + arrow_dy),
            arrowprops=dict(facecolor="#2ca02c", edgecolor="#2ca02c", arrowstyle="->", lw=1.5),
            fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.35", fc="#eefaf0", ec="#aaddbb", alpha=0.95),
        )

        if standalone:
            fig.tight_layout()
            if path is not None:
                fig.savefig(path, dpi=180)
                plt.close(fig)
        return self


class RateVarianceComparison:
    """Container comparing multiple rate-variance sweeps."""

    def __init__(self, sweeps: Sequence[RateVarianceSweep]):
        self.sweeps = list(sweeps)

    def table(self) -> RateVarianceComparison:
        """Print concise multi-panel summary comparison table."""
        print("=" * 90)
        print(f"{'Panel':<6} | {'Problem & Config':<32} | {'phi(x)':<8} | {'lambda_th':<10} | {'lambda*':<10} | {'Diff':<8} | {'Var Red vs default'}")
        print("-" * 90)
        for i, sweep in enumerate(self.sweeps):
            panel_letter = chr(ord('a') + i)
            phi_val = (
                float(sweep.pde.phi(sweep.x))
                if not hasattr(sweep.pde, "mechanism") or sweep.pde.mechanism is None
                else float(sweep.pde.mechanism.terminal(Id(), sweep.pde, sweep.x))
            )
            clean_title = sweep.title
            if clean_title.startswith(f"({panel_letter}) "):
                clean_title = clean_title[4:]
            clean_title = clean_title.replace("$", "")
            print(f"({panel_letter})    | {clean_title[:32]:<32} | {phi_val:+7.4f} | {sweep.lambda_theory:9.4f}  | {sweep.optimal_rate:9.4f}  | {sweep.diff_pct:6.2f}% | {sweep.var_reduction_pct:6.1f}%")
        print("=" * 90)
        return self

    def plot(
        self,
        path: Optional[Union[str, Path]] = None,
        figsize: tuple[float, float] = (14.0, 10.5),
    ) -> RateVarianceComparison:
        """Render multi-panel grid comparing all sweeps."""
        n = len(self.sweeps)
        if n == 1:
            nrows, ncols = 1, 1
        elif n == 2:
            nrows, ncols = 1, 2
        elif n <= 4:
            nrows, ncols = 2, 2
        else:
            ncols = 3
            nrows = (n + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows, ncols, figsize=figsize, sharex=False, sharey=False)
        ax_flat = np.atleast_1d(axes).flatten()

        for i, sweep in enumerate(self.sweeps):
            sweep.plot(ax=ax_flat[i])

        # Hide any unused subplots
        for j in range(n, len(ax_flat)):
            ax_flat[j].set_visible(False)

        fig.suptitle(
            r"$\mathrm{Var}(H)$ vs $\lambda$: Strict Convexity & Optimal Rate Generalizability" + "\n"
            r"Verifying $\lambda_{\mathrm{theory}}(x) \approx |f(\phi(x))|/|\phi(x)|$ across Different PDEs, Spatial States, and Nonlinearities",
            fontsize=13.0, fontweight="bold", y=0.992,
        )
        fig.tight_layout(rect=[0, 0, 1, 0.960])

        if path is not None:
            out_p = Path(path)
            out_p.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(out_p, dpi=180)
            plt.close(fig)
            print(f"Comparison figure successfully saved to: {out_p.resolve()}")

        return self


def sweep_rate_variance(
    pde: ParabolicPDE,
    x: float = 0.0,
    t: float = 0.0,
    *,
    title: Optional[str] = None,
    n_samples: int = 30_000,
    lambda_bracket: Optional[tuple[float, float]] = None,
    opt_bracket: Optional[tuple[float, float]] = None,
    n_mc_points: int = 16,
    n_quad_points: int = 50,
    seed: int = 20260915,
    quadrature: MomentQuadrature = MomentQuadrature(time_order=4, normal_order=4),
    mechanism=None,
    use_riccati: bool = False,
    max_depth: int = 2,
) -> RateVarianceSweep:
    """Run a deterministic and Monte Carlo rate-variance sweep for a PDE at state (t, x)."""
    if mechanism is None:
        mechanism = getattr(pde, "mechanism", None)

    # 1. Exact solution and theoretical rate
    exact_u = (
        pde.exact_solution(t, x)
        if pde.exact_solution is not None
        else float(pde.phi(x))
    )
    lam_theory = short_time_rate_1d(pde, x, mechanism=mechanism)

    # Brackets
    if lambda_bracket is None:
        lambda_bracket = (max(0.10, 0.25 * lam_theory), min(4.0, 2.5 * lam_theory))
    if opt_bracket is None:
        opt_bracket = (max(0.12, 0.35 * lam_theory), min(3.5, 2.2 * lam_theory))

    quad_rates = np.linspace(lambda_bracket[0], lambda_bracket[1], n_quad_points)
    mc_rates = np.linspace(lambda_bracket[0] * 1.15, lambda_bracket[1] * 0.98, n_mc_points)

    # 2. Optimal rate and deterministic curve
    if use_riccati:
        lam_opt = riccati_binary_optimal_rate(pde.T)
        v_opt = riccati_binary_second_moment(pde.T, lam_opt) - exact_u**2
        curve_var = np.array([
            riccati_binary_second_moment(pde.T, r) - exact_u**2 for r in quad_rates
        ])
        curve_label = r"Full-Tree Riccati Exact $\mathrm{Var}(H)$"
    else:
        opt_res = optimize_exponential_rate_1d(
            pde, t, x, max_depth=max_depth, bracket=opt_bracket,
            quadrature=quadrature, mechanism=mechanism,
        )
        lam_opt = opt_res.rate
        v_opt = opt_res.second_moment - exact_u**2
        curve_var = np.array([
            finite_depth_moment_derivatives_1d(
                pde, t, x, max_depth=max_depth, rate=r, quadrature=quadrature, mechanism=mechanism,
            ).value - exact_u**2
            for r in quad_rates
        ])
        curve_label = r"Quadrature $\mathrm{Var}(H)$ ($d^2V/d\lambda^2 > 0$)"

    # 3. Monte Carlo sampling
    mc_vars = []
    mc_se_vars = []
    mc_means = []
    mc_stderrs = []
    mc_nodes = []

    for i, lam in enumerate(mc_rates):
        rng = np.random.default_rng(seed + i * 100)
        samples = [
            sample_tree(pde, t, x, rng=rng, rate=lam, mechanism=mechanism)
            for _ in range(n_samples)
        ]
        vals = np.array([s.value for s in samples])
        nodes = np.array([s.n_nodes for s in samples])

        v = float(np.var(vals, ddof=1))
        m = float(np.mean(vals))
        se_m = float(np.std(vals, ddof=1) / math.sqrt(n_samples))
        m4 = float(np.mean((vals - m)**4))
        se_v = math.sqrt(max(0.0, (m4 - v**2) / n_samples))

        mc_vars.append(v)
        mc_se_vars.append(se_v)
        mc_means.append(m)
        mc_stderrs.append(se_m)
        mc_nodes.append(float(np.mean(nodes)))

    mc_vars_arr = np.array(mc_vars)
    mc_se_arr = np.array(mc_se_vars)

    # Error and variance reduction
    diff_pct = abs(lam_opt - lam_theory) / lam_theory * 100
    v_default = float(mc_vars_arr[np.argmin(np.abs(mc_rates - 1.0))])
    v_at_opt = float(mc_vars_arr[np.argmin(np.abs(mc_rates - lam_opt))])
    var_red_pct = max(0.0, (v_default - v_at_opt) / v_default * 100)

    pde_name = getattr(pde, "name", pde.__class__.__name__)
    sweep_title = title if title is not None else f"{pde_name} at x={x}"

    return RateVarianceSweep(
        pde=pde,
        x=x,
        t=t,
        title=sweep_title,
        lambda_theory=lam_theory,
        optimal_rate=lam_opt,
        optimal_variance=v_opt,
        diff_pct=diff_pct,
        var_reduction_pct=var_red_pct,
        quad_rates=quad_rates,
        quad_variance=curve_var,
        mc_rates=mc_rates,
        mc_variance=mc_vars_arr,
        mc_stderr=mc_se_arr,
        mc_means=np.array(mc_means),
        mc_stderrs=np.array(mc_stderrs),
        mc_nodes=np.array(mc_nodes),
        curve_label=curve_label,
    )


def compare_rate_variance(*sweeps: RateVarianceSweep) -> RateVarianceComparison:
    """Compare multiple rate-variance sweeps across PDEs or configurations."""
    return RateVarianceComparison(sweeps)
