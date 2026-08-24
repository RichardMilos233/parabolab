"""Merton HJB, d = 1 (JCP2024 eq. (4.6), Table 5): fully nonlinear PDE."""
from functools import partial
from pathlib import Path

import numpy as np

from parabolab import CodingTreeMC, DeepBranching, DeepBSDE, DeepGalerkin, compare
from parabolab.library import merton_hjb

# u_t + (1/2) u_xx + f(u, u_x, u_xx) = 0
# f = -u_xx/2 - (mu^2/2 sigma^2) u_x^2/u_xx + (gamma/(1-gamma)) u_x^(1-1/gamma) - rho u
pde = partial(merton_hjb, T=0.1)
grid = np.linspace(100.0, 200.0, 27)

if __name__ == "__main__":
    curves = [
        CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid),
        DeepBranching(n_states=1000, m_samples=10_000, epochs=3000, n_jobs=8).solve(pde, grid),
        # DeepBSDE(epochs=3000, n_states=1000).solve(pde, grid),
        # DeepGalerkin(epochs=3000, n_states=1000).solve(pde, grid),
    ]

    title = "Merton HJB $d=1$: MC and deep branching"
    compare(pde, *curves).table().plot(Path(__file__).with_suffix(".png"), title)
