"""Vendored comparison baselines (M5).

``bsde.py`` and ``galerkin.py`` are verbatim copies (plus provenance
headers) of the deep BSDE and deep Galerkin solvers from the authors'
repository https://github.com/nguwijy/deep_branching, commit c06bef2,
MIT License (c) 2022 nguwijy.  ``adapters.py`` is ours: a thin
index-mapping + sympy->torch lambdify layer that lets both baselines run
against ``parabolab.library`` PDE definitions.
"""

from .adapters import (
    BaselineInapplicable,
    bsde_functions,
    dgm_functions,
    eval_bsde_grid,
    eval_dgm_grid,
    torch_phi,
)
from .bsde import BSDENet
from .galerkin import DGMNet

__all__ = [
    "BSDENet",
    "DGMNet",
    "BaselineInapplicable",
    "bsde_functions",
    "dgm_functions",
    "eval_bsde_grid",
    "eval_dgm_grid",
    "torch_phi",
]
