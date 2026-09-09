"""Deterministic moment recursion tests and Monte Carlo cross-checks."""

from __future__ import annotations

import math

import numpy as np
import pytest

from parabolab import Id, ParabolicPDE, sample_tree
from parabolab.moments import MomentQuadrature, finite_depth_moment_1d


class BinaryMechanism:
    """A one-type binary mechanism with terminal factor 1 and single tuple (Id(), Id())."""

    @staticmethod
    def tuples(code):
        return ((Id(), Id()),)

    @staticmethod
    def terminal(code, pde, x):
        return 1.0

    @staticmethod
    def is_identically_zero(code, pde):
        return False


def constant_terminal_pde(T: float = 0.2) -> ParabolicPDE:
    return ParabolicPDE(
        T=T,
        f=lambda z: 0.0,
        f_derivatives=(),
        phi=lambda x: 1.0,
        phi_derivatives=(lambda x: 0.0,),
        exact_solution=lambda t, x: 1.0,
        name="constant_terminal",
    )


def test_binary_depth_zero_second_moment_is_exp_r():
    got = finite_depth_moment_1d(
        constant_terminal_pde(T=0.2),
        0.0,
        0.0,
        p=2.0,
        max_depth=0,
        rate=1.0,
        mechanism=BinaryMechanism,
    )
    assert got == pytest.approx(math.exp(0.2), rel=1e-10)


def test_binary_depth_one_second_moment_is_exp_2r():
    got = finite_depth_moment_1d(
        constant_terminal_pde(T=0.2),
        0.0,
        0.0,
        p=2.0,
        max_depth=1,
        rate=1.0,
        mechanism=BinaryMechanism,
        quadrature=MomentQuadrature(time_order=16, normal_order=8),
    )
    assert got == pytest.approx(math.exp(0.4), rel=1e-9)


@pytest.mark.slow
def test_monte_carlo_cross_check_binary_depth_one():
    """Empirical second moment at depth 1 matches quadrature within 5 stderr."""
    pde = constant_terminal_pde(T=0.2)
    det_val = finite_depth_moment_1d(
        pde,
        0.0,
        0.0,
        p=2.0,
        max_depth=1,
        rate=1.0,
        mechanism=BinaryMechanism,
    )
    n_samples = 50_000
    rng = np.random.default_rng(20260909)
    samples_sq = np.empty(n_samples)
    for i in range(n_samples):
        s = sample_tree(
            pde,
            0.0,
            0.0,
            rng=rng,
            rate=1.0,
            mechanism=BinaryMechanism,
            max_depth=1,
        )
        samples_sq[i] = s.value**2

    mean_h2 = float(np.mean(samples_sq))
    stderr_h2 = float(np.std(samples_sq, ddof=1) / math.sqrt(n_samples))
    assert abs(mean_h2 - det_val) <= 5.0 * stderr_h2
