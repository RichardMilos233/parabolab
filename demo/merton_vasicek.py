"""Merton HJB with Vasicek stochastic rate, d = 1 reduced: MC and deep branching."""
from functools import partial
from pathlib import Path

import numpy as np

from parabolab import CodingTreeMC, DeepBranching, compare
from parabolab.library import merton_vasicek_reduced

# F_t + (1/2) F_yy + f(y, F, F_y) = 0,  F(T, y) = 1
# y = (r - theta) / eta,  dY = -kappa y dt + dW
pde = partial(merton_vasicek_reduced, T=0.1, consumption=False)
grid = np.linspace(-1.0, 1.0, 21)

if __name__ == "__main__":
    curves = [
        CodingTreeMC(n_samples=50_000, seed=0, rate=1.5).solve(pde, grid),
        DeepBranching(n_states=3000, m_samples=50_000, epochs=8000, n_jobs=8).solve(pde, grid),
    ]

    title = "Merton Vasicek stochastic rate: MC and deep branching"
    compare(pde, *curves).table().plot(Path(__file__).with_suffix(".png"), title)
