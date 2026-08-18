"""Random coding-tree sampler, JCP2024 Algorithm 1 / JEQ2023 Definition 4.1.

TREE(t, x, c):
    tau ~ rho  (interbranching time; we use rho = Exp(rate))
    if t + tau > T:                        # leaf: horizon reached
        W ~ N(0, T - t)
        return c(u)(T, x + W) / Fbar(T - t)
    else:                                  # branch
        Z ~ Uniform(M(c))                  # a code tuple
        Xb = x + W',  W' ~ N(0, tau)       # position of the branch point
        return |M(c)| / rho(tau) * prod_{cc in Z} TREE(t + tau, Xb, cc)

This realizes the functional of JEQ2023 Definition 4.1: interior particles
contribute 1/(q_c(I_c) rho(tau)) with q_c uniform, leaves contribute
c(u)(T, X_T)/Fbar(T - t_birth), where Fbar is the survival function of rho.

Two conventions worth stressing (see docs in CLAUDE.md):

* ALL children start from the SAME branch position Xb (the parent's death
  position).  This is required by the fixed-point system (JEQ2023 eq. (4.1),
  where the product prod_z u_z(s, y) sits under a single space integral) and
  is what the authors' code does; the typesetting of JCP2024 Algorithm 1 can
  be misread as drawing a fresh W per child.
* rho = Exp(rate) means density rate*exp(-rate*tau); with numpy this is
  ``rng.exponential(scale=1/rate)`` (numpy parametrizes by the SCALE).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np

from .mechanism import Code, Id, SemilinearMechanism
from .pde import ParabolicPDE


#: Package default rate for rho = Exp(rate): the standard exponential used
#: by JEQ2023's Mathematica appendix.  Empirically (Allen-Cahn, T = 0.5) it
#: gives noticeably lower variance than the JCP2024 choice, see jcp_rate().
DEFAULT_RATE = 1.0


def default_rate(T: float) -> float:
    """Rate of rho = Exp(rate) used when none is given (currently 1.0).

    JEQ2023's Mathematica appendix uses the standard exponential, rate = 1.
    JCP2024 Remark 3.1 (v) instead uses jcp_rate(T) = -log(0.95)/T; with that
    choice trees are tiny but the rare branch events carry weights ~2e/rate,
    giving heavy tails: at T = 0.5 the empirical mean acquires a visible
    systematic deviation and the sample stderr underestimates the error
    (reproduced both by us and by the authors' own logs in
    coding_trees/logs/final/allen_cahn_jeeq_dim_1_blow_up_analysis.csv).
    """
    return DEFAULT_RATE


def jcp_rate(T: float) -> float:
    """The rho rate of JCP2024 Remark 3.1 (v): -log(0.95)/T.

    A particle spawned at time 0 then survives to the horizon with
    probability 0.95.  See default_rate() for why it is not our default.
    """
    return -math.log(0.95) / T


@dataclass
class TreeSample:
    """One realization of H together with cheap diagnostics."""

    value: float
    n_nodes: int


def sample_tree(
    pde: ParabolicPDE,
    t: float,
    x: float,
    *,
    rng: np.random.Generator,
    rate: Optional[float] = None,
    code: Code = Id(),
    mechanism=None,
    prune_zero: bool = True,
) -> TreeSample:
    """Draw one sample of H(T_{t,x,code}); E[H] = code(u)(t, x).

    Parameters
    ----------
    rate : rate of the Exp interbranching-time distribution rho
        (None -> default_rate(pde.T)).
    mechanism : None picks the PDE's own mechanism if it has one
        (FullyNonlinearPDE1D), else the semilinear mechanism.
    prune_zero : return 0 immediately for identically-zero codes (exact for
        polynomial f, see SemilinearMechanism.is_identically_zero). Pruned
        subtrees consume no randomness.
    """
    if mechanism is None:
        mechanism = getattr(pde, "mechanism", None) or SemilinearMechanism
    if rate is None:
        rate = default_rate(pde.T)
    # d-dim problems (FullyNonlinearPDEnD) pass x as an ndarray of shape (d,)
    # and may carry a diffusion sigma2 != 1 (BM variance sigma2 per unit
    # time); the scalar d = 1 path is byte-for-byte the M1/M2 behaviour.
    size = x.shape if isinstance(x, np.ndarray) else None
    sig = math.sqrt(getattr(pde, "sigma2", 1.0))
    counter = [0]
    value = _tree(pde, mechanism, t, x, code, rng, rate, prune_zero, counter,
                  size, sig)
    return TreeSample(value=value, n_nodes=counter[0])


def _tree(
    pde: ParabolicPDE,
    mech,
    t: float,
    x,
    code: Code,
    rng: np.random.Generator,
    rate: float,
    prune_zero: bool,
    counter: list,
    size=None,
    sig: float = 1.0,
) -> float:
    counter[0] += 1
    if prune_zero and mech.is_identically_zero(code, pde):
        return 0.0

    tau = rng.exponential(1.0 / rate)  # Exp(rate); numpy takes the scale
    remaining = pde.T - t

    if tau > remaining:
        # Leaf: run the Brownian motion to the horizon and evaluate the code
        # on phi; importance weight 1/Fbar(T - t) with Fbar(s) = exp(-rate*s).
        if remaining > 0.0:
            w = rng.normal(0.0, sig * math.sqrt(remaining), size=size)
        else:
            w = 0.0
        return mech.terminal(code, pde, x + w) * math.exp(rate * remaining)

    # Branch: uniform tuple from M(code), weight |M(code)| / rho(tau).
    tuples = mech.tuples(code)
    z = tuples[rng.integers(len(tuples))] if len(tuples) > 1 else tuples[0]
    # One shared branch position for all children (JEQ2023 Section 3).
    xb = x + rng.normal(0.0, sig * math.sqrt(tau), size=size)
    h = len(tuples) * math.exp(rate * tau) / rate  # = |M(c)|/rho(tau)
    for cc in z:
        h *= _tree(pde, mech, t + tau, xb, cc, rng, rate, prune_zero, counter,
                   size, sig)
    return h
