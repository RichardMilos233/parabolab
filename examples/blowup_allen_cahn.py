"""Blow-up study (M5, spirit of JCP2024 Fig. 2): pointwise MC estimate of
the Allen-Cahn solution u(0, 0) as a function of the horizon T, d=1 and 10.

For each T in [0.05, 2.0] we run the pointwise coding-tree estimator with
several independent seeds and both rho rates:

* jcp   -- the authors' -log(0.95)/T (their blow_up_analysis notebooks),
* 1.0   -- parabolab's default (JEQ2023's standard exponential clock).

Recorded per T: estimate +/- stderr, |error| vs the exact traveling wave,
seed spread, max |H| (tail diagnostic), mean tree size.  The authors'
branch/deep-BSDE columns from coding_trees/logs/final/
allen_cahn_jeeq_dim_{1,10}_blow_up_analysis.csv are overlaid for
cross-checking.

What to look for (the FYP centerpiece):

* SHORT T: |err| is within ~2 stderr; the stderr band is an honest
  confidence interval; both rates agree.
* LARGE T: the estimate drifts SYSTEMATICALLY below the true solution
  (more negative -- exactly as in the authors' CSV) while the reported
  stderr stays deceptively small: single trees with enormous |H|
  dominate the tail that the finite sample no longer covers.
  max|H| exploding while stderr stays finite is the fingerprint that
  E[H^2] (then E[|H|]) has left the integrability window of JEQ2023
  Prop. 4.2 -- same mechanism as the Dym example's divergence at
  T = 0.1 and the HJB d=100 heavy tails documented in M2/M3.
"""

from __future__ import annotations

import argparse
import csv
import functools
import math
from pathlib import Path

import numpy as np

from parabolab.blowup import integrability_edge, sweep_T
from parabolab.library import allen_cahn_nd

AUTHORS_CSV = (
    Path(__file__).resolve().parents[2]
    / "coding_trees" / "logs" / "final"
    / "allen_cahn_jeeq_dim_{d}_blow_up_analysis.csv"
)


def authors_data(d: int):
    """(T, |branch err|, |bsde err|) from the authors' CSV, if present."""
    path = Path(str(AUTHORS_CSV).format(d=d))
    if not path.exists():
        return None
    T, be, se = [], [], []
    for row in csv.DictReader(open(path)):
        T.append(float(row["T"]))
        exact = float(row["exact"])
        be.append(abs(float(row["branch"]) - exact))
        v = row.get("deep_bsde", "")
        se.append(abs(float(v) - exact) if v else float("nan"))
    return np.array(T), np.array(be), np.array(se)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dims", type=int, nargs="+", default=[1, 10])
    p.add_argument("--samples", type=int, default=100_000)
    p.add_argument("--t-max", type=float, default=2.0)
    p.add_argument("--t-step", type=float, default=0.1)
    p.add_argument("--seeds", type=int, default=3)
    p.add_argument("--jobs", type=int, default=6)
    args = p.parse_args()

    Ts = np.arange(args.t_step, args.t_max + 1e-9, args.t_step)
    Ts = np.round(Ts, 10)

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    for d in args.dims:
        make = functools.partial(allen_cahn_nd, d)
        sweeps, edges = {}, {}
        for label, rate in (("jcp", "jcp"), ("rate=1", 1.0)):
            print(f"=== Allen-Cahn d={d}, u(0,0) vs T, rho rate {label}, "
                  f"N={args.samples}, seeds={args.seeds} ===", flush=True)
            sweeps[label] = sweep_T(
                make, Ts, n_samples=args.samples, rate=rate,
                seeds=range(args.seeds), n_jobs=args.jobs,
            )
            edges[label] = integrability_edge(sweeps[label])
            print(f"  -> integrability edge (persistent drift or "
                  f"stderr > 5% of |exact|): T ~ {edges[label]}", flush=True)

        auth = authors_data(d)

        fig, (ax1, ax2) = plt.subplots(
            2, 1, figsize=(9, 9), sharex=True,
            gridspec_kw={"height_ratios": [3, 2]},
        )
        colors = {"jcp": "tab:orange", "rate=1": "tab:blue"}
        for label, sw in sweeps.items():
            ax1.errorbar(sw.T, sw.abs_err, yerr=sw.stderr, marker="o",
                         ms=3, lw=1.2, capsize=2, color=colors[label],
                         label=f"ours, rho {label} (+/- stderr)")
            ax1.plot(sw.T, sw.seed_spread, ":", lw=1, color=colors[label],
                     label=f"seed spread ({args.seeds} seeds), {label}")
        if auth is not None:
            aT, abr, abs_ = auth
            ax1.plot(aT, abr, "k^--", ms=4, lw=0.8, alpha=0.7,
                     label="authors' branch (coding_trees CSV)")
            ax1.plot(aT, abs_, "v--", ms=4, lw=0.8, alpha=0.6,
                     color="tab:green",
                     label="authors' deep BSDE (NaN past ~0.65)" if d == 1
                     else "authors' deep BSDE")
        for label, edge in edges.items():
            if edge is not None:
                ax1.axvline(edge, color=colors[label], ls="-.", lw=1,
                            alpha=0.8,
                            label=f"integrability edge {label} (T={edge:g})")
        ax1.set_yscale("log")
        ax1.set_ylabel("|u^(0,0) - u(0,0)|")
        ax1.set_title(
            f"Allen-Cahn d={d}: pointwise MC blow-up study "
            f"(JCP2024 Fig. 2 spirit), N={args.samples:,}")
        ax1.legend(fontsize=8)
        ax1.grid(alpha=0.3)

        for label, sw in sweeps.items():
            ax2.plot(sw.T, sw.max_abs, "-", color=colors[label],
                     label=f"max |H|, {label}")
            ax2.plot(sw.T, sw.stderr * math.sqrt(args.samples), "--",
                     color=colors[label], alpha=0.6,
                     label=f"sample SD, {label}")
        ax2.set_yscale("log")
        ax2.set_xlabel("T")
        ax2.set_ylabel("tail diagnostics")
        ax2.legend(fontsize=8)
        ax2.grid(alpha=0.3)

        fig.tight_layout()
        out = f"examples/blowup_allen_cahn_d{d}.png"
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f"figure saved to {out}\n", flush=True)

        # compact cross-check table vs the authors at matching T values
        if auth is not None:
            aT, abr, _ = auth
            print(f"  cross-check vs authors' branch column (d={d}):")
            sw = sweeps["jcp"]
            for i, T in enumerate(sw.T):
                j = np.argmin(np.abs(aT - T))
                if abs(aT[j] - T) < 1e-9:
                    print(f"    T={T:.2f}  ours(jcp) |err|={sw.abs_err[i]:.2e}"
                          f"  authors |err|={abr[j]:.2e}")
            print(flush=True)


if __name__ == "__main__":
    main()
