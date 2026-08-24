"""Reproduce JEQ2023 Figure 1: Allen-Cahn (5.2) profiles in d dimensions.

    du/dt + (1/2) Lap u + u - u^3 = 0,
    exact (5.3): u(t, x) = -1/2 - tanh(3(T-t)/4 - sum x_i/(2 sqrt d))/2
"""
import argparse
import functools
import pathlib

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import allen_cahn_nd
from parabolab.profiles import last_coordinate_embedding

AUTHORS_LOGS = pathlib.Path(__file__).resolve().parents[2] / "coding_trees" / "logs" / "final"
T_BY_DIM = {5: 0.5, 100: 0.3}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000, help="MC samples per grid point")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--dims", type=int, nargs="+", default=[5, 100])
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()

    for d in args.dims:
        T = T_BY_DIM.get(d, 0.5)
        factory = functools.partial(allen_cahn_nd, d=d, T=T)
        pde = factory()
        grid = np.linspace(-8.0, 8.0, 10)
        print(f"=== Allen-Cahn (5.2), d={d}, T={T} ===")
        mc = CodingTreeMC(n_samples=args.samples, seed=args.seed, n_jobs=args.jobs).solve(
            factory, grid, embed=last_coordinate_embedding(d)
        )

        reference = None
        csv = AUTHORS_LOGS / f"plt_allen_cahn_jeeq_dim_{d}_coarse.csv"
        if csv.exists():
            data = np.loadtxt(csv, delimiter=",", skiprows=1)
            reference = (data[:, 0], data[:, 1], "authors' coding_trees")
            ours = np.interp(data[:, 0], grid, mc.values)
            print(f"max |ours - authors| on their grid: {np.max(np.abs(ours - data[:, 1])):.4f}")

        compare(pde, mc).table().plot(
            pathlib.Path(__file__).with_name(f"jeq_fig1_allen_cahn_d{d}.png"),
            f"JEQ2023 Fig. 1: Allen-Cahn (5.2), $d={d}$, $T={T}$",
            reference=reference,
        )
        print()
