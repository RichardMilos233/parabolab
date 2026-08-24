"""Allen-Cahn (JEQ2023 eq. (5.2), d = 1) by the coding-tree Monte Carlo.

    du/dt + (1/2) u'' + u - u^3 = 0,  u(T, x) = -1/2 - tanh(-x/2)/2,
    exact (5.3): u(t,x) = -1/2 - tanh(3(T-t)/4 - x/2)/2.

Estimates u(t, x) on a small x-grid at two times, prints the table with
|estimate - exact| / stderr, and plots both times against the closed form.
This is the M1 validation script: every |err|/stderr below ~3 means the
representation and the sampler agree with the closed form.

Usage: python jeq_allen_cahn_1d.py [--samples N] [--seed S] [--T T]
"""

import argparse
import pathlib

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import allen_cahn_wave_1d


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--T", type=float, default=0.5)
    args = parser.parse_args()

    pde = allen_cahn_wave_1d(args.T)
    grid = np.linspace(-2.0, 2.0, 9)

    # One curve per time; the per-time seed offset keeps the two draws
    # independent (within a curve, estimate_profile advances seed by the
    # grid index).
    curves = [
        CodingTreeMC(n_samples=args.samples,
                     seed=args.seed + int(t * 100)).solve(pde, grid, t=t)
        for t in (0.0, 0.25)
    ]

    compare(pde, *curves).table().plot(
        pathlib.Path(__file__).with_name("allen_cahn_1d.png"),
        f"Allen-Cahn (JEQ2023 eq. 5.2), coding trees, "
        f"T={args.T}, N={args.samples}")


if __name__ == "__main__":
    main()
