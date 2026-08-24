"""Allen-Cahn, d = 1 (JCP2024 Table 1 / Fig. 1): one PDE, four methods."""
from functools import partial
from pathlib import Path

import numpy as np

from parabolab import CodingTreeMC, DeepBranching, DeepBSDE, DeepGalerkin, compare
from parabolab.library import allen_cahn_nd

# u_t + (1/2) u_xx + u - u^3 = 0,  u(T, x) = -1/2 - (1/2) tanh(-x/2)
pde = partial(allen_cahn_nd, d=1, T=0.5)
grid = np.linspace(-8.0, 8.0, 27)

if __name__ == "__main__":
    curves = [
        CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid),
        DeepBranching(n_states=1000, m_samples=10_000, epochs=3000, n_jobs=8).solve(pde, grid),
        DeepBSDE(epochs=3000, n_states=1000).solve(pde, grid),
        DeepGalerkin(epochs=3000, n_states=1000).solve(pde, grid),
    ]

    title = "Allen-Cahn $d=1$: four methods"
    compare(pde, *curves).table().plot(Path(__file__).with_suffix(".png"), title)
