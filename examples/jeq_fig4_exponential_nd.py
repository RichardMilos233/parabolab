"""Reproduce JEQ2023 Figure 4: exponential gradient nonlinearity (5.5).

    du/dt + (alpha/d) sum_i du/dx_i + (1/2) Lap u + d e^{-u} (1 - 2 e^{-u}) = 0,
    exact (5.6): u(t, x) = log(1 + (alpha (T-t) + sum x_i)^2)
"""
import argparse
import functools
import pathlib

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import exponential_gradient_nd
from parabolab.profiles import last_coordinate_embedding

AUTHORS_LOGS = pathlib.Path(__file__).resolve().parents[2] / "coding_trees" / "logs" / "final"

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000, help="MC samples per grid point")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dims", type=int, nargs="+", default=[5, 10])
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    for d in args.dims:
        factory = functools.partial(exponential_gradient_nd, d=d)
        pde = factory()
        grid = np.linspace(-4.0, 4.0, 10)
        print(f"=== exponential nonlinearity (5.5), d={d}, T={pde.T} ===")
        mc = CodingTreeMC(n_samples=args.samples, seed=args.seed, n_jobs=args.jobs).solve(
            factory, grid, embed=last_coordinate_embedding(d)
        )

        reference = None
        csv = AUTHORS_LOGS / f"plt_exponential_nonlinearity_jeeq_dim_{d}_coarse.csv"
        if csv.exists():
            data = np.loadtxt(csv, delimiter=",", skiprows=1)
            reference = (data[:, 0], data[:, 1], "authors' coding_trees")
            ours = np.interp(data[:, 0], grid, mc.values)
            print(f"max |ours - authors| on their grid: {np.max(np.abs(ours - data[:, 1])):.4f}")

        compare(pde, mc).table().plot(
            pathlib.Path(__file__).with_name(f"jeq_fig4_exponential_d{d}.png"),
            f"JEQ2023 Fig. 4: exp nonlinearity (5.5), $d={d}$",
            reference=reference,
        )
        print()
