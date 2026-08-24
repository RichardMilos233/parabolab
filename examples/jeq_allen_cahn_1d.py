"""Allen-Cahn 1D (JEQ2023 eq. (5.2)): coding-tree Monte Carlo vs exact solution.

    du/dt + (1/2) u_xx + u - u^3 = 0,  u(T, x) = -1/2 - tanh(-x/2)/2
    exact: u(t, x) = -1/2 - tanh(3(T-t)/4 - x/2)/2
"""
import argparse
import pathlib

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import allen_cahn_wave_1d

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--T", type=float, default=0.5)
    args = parser.parse_args()

    pde = allen_cahn_wave_1d(args.T)
    grid = np.linspace(-2.0, 2.0, 9)

    curves = [
        CodingTreeMC(n_samples=args.samples, seed=args.seed + int(t * 100)).solve(pde, grid, t=t)
        for t in (0.0, 0.25)
    ]

    compare(pde, *curves).table().plot(
        pathlib.Path(__file__).with_name("allen_cahn_1d.png"),
        f"Allen-Cahn (JEQ2023 eq. 5.2), coding trees, T={args.T}, N={args.samples}",
    )
