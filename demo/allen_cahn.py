"""Allen-Cahn, d = 1 (JCP2024 Table 1 / Fig. 1) -- one PDE, several methods."""
import sys
from functools import partial
from pathlib import Path

import numpy as np

from parabolab import CodingTreeMC, compare
from parabolab.library import allen_cahn_nd

# The other three methods train a network.  They are off by default so the
# script still costs a second; pass --deep to add them (about 2 min total on
# a laptop CPU at the paper's own budget -- no GPU needed, see demo/README).
DEEP = "--deep" in sys.argv


def main():
    # u_t + (1/2) u_xx + u - u^3 = 0,  u(T, x) = -1/2 - (1/2) tanh(-x/2)
    # A factory, not an instance: the parallel and network solvers rebuild the
    # PDE inside worker processes (PDE objects are not picklable).
    pde = partial(allen_cahn_nd, d=1, T=0.5)
    grid = np.linspace(-8.0, 8.0, 27)

    curves = [CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid)]

    if DEEP:
        from parabolab import DeepBranching, DeepBSDE, DeepGalerkin
        curves += [
            DeepBranching(n_states=1000, m_samples=10_000, epochs=3000,
                          n_jobs=8).solve(pde, grid),
            DeepBSDE(epochs=3000, n_states=1000).solve(pde, grid),
            DeepGalerkin(epochs=3000, n_states=1000).solve(pde, grid),
        ]

    title = "Allen-Cahn $d=1$: " + ("four methods" if DEEP
                                    else "coding-tree Monte Carlo")
    compare(pde, *curves).table().plot(Path(__file__).with_suffix(".png"),
                                       title)


# DeepBranching fans its training data out to worker processes; under spawn
# (Windows, macOS) the child re-imports this module, so the guard is not
# optional -- without it the pool spawns recursively.
if __name__ == "__main__":
    main()
