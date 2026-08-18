"""Reproduction checks for the JEQ2023 Section 5.1 multidimensional results.

Fast versions run at reduced budgets; @slow runs use the paper's settings
(see examples/jeq_fig1_*, jeq_fig4_*, jeq_table2_*, jeq_table5_*).
"""

import functools
import math

import numpy as np
import pytest

import parabolab as pl
from parabolab.parallel import estimate_parallel
from parabolab.profiles import estimate_profile, last_coordinate_embedding
from parabolab.tree import jcp_rate


def test_allen_cahn_d5_point_fast():
    pde = pl.library.allen_cahn_nd(d=5, T=0.5)
    x = last_coordinate_embedding(5)(2.0)
    res = pl.estimate(pde, 0.0, x, 20_000, seed=1)
    exact = pde.exact_solution(0.0, x)
    assert abs(res.estimate - exact) < 3.5 * res.stderr


def test_exponential_d5_point_fast():
    pde = pl.library.exponential_gradient_nd(d=5)
    x = last_coordinate_embedding(5)(2.0)
    res = pl.estimate(pde, 0.0, x, 20_000, seed=2)
    exact = pde.exact_solution(0.0, x)
    assert abs(res.estimate - exact) < 3.5 * res.stderr


def test_hjb_d100_point_fast():
    """20k samples at the authors' rate: z is usually < 2 but the weight
    distribution is heavy-tailed (|M(f*)| = 2e4), hence the loose bound."""
    pde = pl.library.hjb_nd()
    res = pl.estimate(pde, 0.0, np.zeros(100), 20_000, seed=1,
                      rate=jcp_rate(1.0))
    exact = pl.library.hjb_exact_u0()
    assert abs(res.estimate - exact) < 5.0 * res.stderr


def test_allen_cahn_bsde_d100_point_fast():
    pde = pl.library.allen_cahn_bsde()
    res = pl.estimate(pde, 0.0, np.zeros(100), 20_000, seed=1)
    # reference value of [19]; allow combined MC + reference slack
    assert abs(res.estimate - 0.052802) < 4.0 * res.stderr + 5e-4


@pytest.mark.slow
def test_fig1_allen_cahn_d5_profile_paper_budget():
    d, T = 5, 0.5
    factory = functools.partial(pl.library.allen_cahn_nd, d=d, T=T)
    pde = factory()
    xs = np.linspace(-8.0, 8.0, 10)
    res = estimate_profile(pde, 0.0, xs, 100_000, seed=0,
                           embed=last_coordinate_embedding(d),
                           pde_factory=factory, n_jobs=4)
    assert res.max_abs_z < 4.0


@pytest.mark.slow
def test_fig4_exponential_d5_profile_paper_budget():
    d = 5
    factory = functools.partial(pl.library.exponential_gradient_nd, d=d)
    pde = factory()
    xs = np.linspace(-4.0, 4.0, 10)
    res = estimate_profile(pde, 0.0, xs, 100_000, seed=0,
                           embed=last_coordinate_embedding(d),
                           pde_factory=factory, n_jobs=4)
    # heavy tails near the dip of the exact solution (authors' own
    # published values deviate there as well); 4.5 sigma across 10 points
    assert res.max_abs_z < 4.5


@pytest.mark.slow
def test_table5_hjb_d100_paper_budget():
    """One 1e5-sample run at the authors' rate; combined with the exact
    Cole-Hopf value.  Runs whose stderr is small (~0.004) have missed the
    heavy tail and cluster ~0.2% low (this is precisely the paper's
    published 4.580340), so allow 4 sigma."""
    res = estimate_parallel(pl.library.hjb_nd, 0.0, np.zeros(100), 100_000,
                            seed=300, rate=jcp_rate(1.0), n_jobs=4)
    exact = pl.library.hjb_exact_u0()
    assert abs(res.estimate - exact) < 4.0 * res.stderr


@pytest.mark.slow
def test_table2_allen_cahn_d100_paper_budget():
    res = estimate_parallel(pl.library.allen_cahn_bsde, 0.0, np.zeros(100),
                            1_000_000, seed=100, rate=jcp_rate(0.3),
                            n_jobs=4)
    assert abs(res.estimate - 0.052802) < 4.0 * res.stderr + 5e-4
