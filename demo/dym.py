"""Dym equation, d = 1: finite-sample non-integrability diagnostic (JEQ Fig. 6).

The specified real-extension estimator has no finite absolute first moment
at any positive exponential rate. An accurate-looking curve does not certify
convergence or a finite-variance sweet spot.
"""
from functools import partial
from pathlib import Path

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import dym_1d

# u_t + u^3 u_xxx = 0,  u(T, x) = (6x)^(2/3)
# Traveling wave solution: u(t, x) = (6x + 96(T - t))^(2/3)
pde = partial(dym_1d, T=0.01, alpha=2.0)
grid = np.linspace(1.0, 2.0, 21)

if __name__ == "__main__":
    print("Dym diagnostic: this estimator is non-integrable at every positive rate; "
          "the plotted sample errors are descriptive only.")
    curves = [
        # CodingTreeMC(
        #     n_samples=2_000_000, seed=1, rate=0.1,
        #     label="CodingTreeMC (rate=0.1, sparse)"
        # ).solve(pde, grid),
        CodingTreeMC(
            n_samples=200, seed=1, rate=1.0,
            label="CodingTreeMC (rate=1.0, standard)"
        ).solve(pde, grid),
    ]

    title = "Dym equation $d=1$: coding-tree MC rate sensitivity"
    compare(pde, *curves).table().plot(Path(__file__).with_suffix(".png"), title)
