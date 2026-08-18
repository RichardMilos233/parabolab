"""Allen-Cahn (JEQ2023 eq. (5.2), d = 1) by the coding-tree Monte Carlo.

Estimates u(t, x) on a small x-grid at a couple of t values, prints a table
against the closed-form traveling wave (5.3) and saves a figure next to this
script (mirroring the style of JEQ2023 Fig. 1).

Usage:  python examples/jeq_allen_cahn_1d.py [--samples 100000] [--seed 0]
"""

import argparse
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from parabolab import estimate
from parabolab.library import allen_cahn_wave_1d


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    T = 0.5
    pde = allen_cahn_wave_1d(T)
    ts = (0.0, 0.25)
    xs = np.linspace(-2.0, 2.0, 9)

    print(f"# {pde.name}, N = {args.samples} coding-tree samples per point")
    print(f"{'t':>5} {'x':>6} {'estimate':>12} {'stderr':>10} "
          f"{'exact':>12} {'|err|/stderr':>12}")
    results = {}
    for t in ts:
        est, err = [], []
        for i, x in enumerate(xs):
            r = estimate(pde, t, float(x), args.samples,
                         seed=args.seed + 1000 * i + int(t * 100))
            exact = pde.exact_solution(t, float(x))
            z = abs(r.estimate - exact) / r.stderr
            print(f"{t:5.2f} {x:6.2f} {r.estimate:12.6f} {r.stderr:10.6f} "
                  f"{exact:12.6f} {z:12.2f}")
            est.append(r.estimate)
            err.append(r.stderr)
        results[t] = (np.array(est), np.array(err))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    x_fine = np.linspace(xs[0], xs[-1], 200)
    ax.plot(x_fine, [pde.phi(v) for v in x_fine], "k--",
            label=r"terminal $\phi = u(T,\cdot)$")
    for t, color in zip(ts, ("tab:blue", "tab:red")):
        ax.plot(x_fine, [pde.exact_solution(t, v) for v in x_fine],
                color=color, label=f"exact $u({t},\\cdot)$")
        est, err = results[t]
        ax.errorbar(xs, est, yerr=3 * err, fmt="o", mfc="none", color=color,
                    capsize=3, label=f"MC $t={t}$ ($\\pm 3$ stderr)")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$u(t, x)$")
    ax.set_title(f"Allen-Cahn (JEQ2023 eq. 5.2), coding trees, "
                 f"T={T}, N={args.samples}")
    ax.legend()
    fig.tight_layout()
    out = pathlib.Path(__file__).with_name("allen_cahn_1d.png")
    fig.savefig(out, dpi=150)
    print(f"\nfigure saved to {out}")


if __name__ == "__main__":
    main()
