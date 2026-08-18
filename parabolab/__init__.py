"""parabolab: coding-tree Monte Carlo for fully nonlinear parabolic PDEs.

From-scratch reproduction of Nguwi, Penent & Privault:
- "A fully nonlinear Feynman-Kac formula with derivatives of arbitrary
  orders", J. Evol. Equ. 23:22 (2023)  [JEQ2023]
- "A deep branching solver for fully nonlinear partial differential
  equations", J. Comput. Phys. 499 (2024) 112712  [JCP2024]
"""

from .mc import MCResult, estimate
from .mechanism import (
    Code,
    Dx,
    FDeriv,
    FNu,
    FullyNonlinearMechanism1D,
    Id,
    SemilinearMechanism,
)
from .pde import FullyNonlinearPDE1D, ParabolicPDE, x_symbol, z_symbols
from .tree import TreeSample, default_rate, jcp_rate, sample_tree
from . import library

__all__ = [
    "Code",
    "Dx",
    "FDeriv",
    "FNu",
    "FullyNonlinearMechanism1D",
    "FullyNonlinearPDE1D",
    "Id",
    "MCResult",
    "ParabolicPDE",
    "SemilinearMechanism",
    "TreeSample",
    "default_rate",
    "estimate",
    "jcp_rate",
    "library",
    "sample_tree",
    "x_symbol",
    "z_symbols",
]
