"""Tests for proposal optimization, validation, and nonuniform tuple sampling."""

from __future__ import annotations

import math

import numpy as np
import pytest

from parabolab import Id, ParabolicPDE, estimate
from parabolab.moments import finite_depth_moment_1d
from parabolab.proposals import (
    FrozenTupleProposal,
    TuplePilotResult,
    estimate_tuple_contributions,
    oracle_ratio_bound,
    second_moment_objective,
    sqrt_optimal_probabilities,
)


def test_sqrt_proposal_attains_cauchy_schwarz_bound():
    a = np.array([1.0, 9.0, 4.0])
    q = sqrt_optimal_probabilities(a)
    np.testing.assert_allclose(q, [1 / 6, 3 / 6, 2 / 6])
    assert second_moment_objective(a, q) == pytest.approx(36.0)
    assert second_moment_objective(a, np.full(3, 1 / 3)) == pytest.approx(42.0)


def test_floor_is_a_convex_uniform_mixture():
    q = sqrt_optimal_probabilities([1.0, 9.0], floor_mass=0.2)
    np.testing.assert_allclose(q, 0.8 * np.array([0.25, 0.75]) + 0.1)
    assert q.sum() == pytest.approx(1.0)
    assert np.all(q > 0)


def test_proposal_validation_rejections():
    with pytest.raises(ValueError, match="contributions cannot be empty"):
        sqrt_optimal_probabilities([])
    with pytest.raises(ValueError, match="contributions must be non-negative"):
        sqrt_optimal_probabilities([1.0, -2.0])
    with pytest.raises(ValueError, match="contributions must be finite"):
        sqrt_optimal_probabilities([1.0, float("nan")])
    with pytest.raises(ValueError, match="contributions cannot be all zero"):
        sqrt_optimal_probabilities([0.0, 0.0])
    with pytest.raises(ValueError, match="strictly positive"):
        sqrt_optimal_probabilities([1.0, 0.0], floor_mass=0.0)
    with pytest.raises(ValueError, match="floor_mass must be in"):
        sqrt_optimal_probabilities([1.0, 2.0], floor_mass=1.0)
    with pytest.raises(ValueError, match="floor_mass must be in"):
        sqrt_optimal_probabilities([1.0, 2.0], floor_mass=-0.1)


def test_oracle_ratio_bound():
    # eta = 0, eps = 0 => bound = 1
    assert oracle_ratio_bound(0.0, floor_mass=0.0) == pytest.approx(1.0)
    # eta = 0.5, eps = 0.2 => 1/(1-0.2) * sqrt(1.5 / 0.5) = 1.25 * sqrt(3)
    expected = (1.0 / 0.8) * math.sqrt(3.0)
    assert oracle_ratio_bound(0.5, floor_mass=0.2) == pytest.approx(expected)
    with pytest.raises(ValueError, match="relative_error must be in"):
        oracle_ratio_bound(1.0)


class BinaryTwoTupleMechanism:
    """A mechanism with two tuples for Id(): (Id(),) and (Id(), Id())."""

    @staticmethod
    def tuples(code):
        return ((Id(),), (Id(), Id()))

    @staticmethod
    def terminal(code, pde, x):
        return 1.0

    @staticmethod
    def is_identically_zero(code, pde):
        return False


def test_proposal_invariant_means_on_finite_depth_control():
    """Unbiasedness: uniform and skewed proposals give statistically matching means."""
    pde = ParabolicPDE(
        T=0.15,
        f=lambda z: 0.0,
        f_derivatives=(),
        phi=lambda x: 1.0,
        phi_derivatives=(lambda x: 0.0,),
        exact_solution=lambda t, x: 1.0,
        name="finite_depth_control",
    )
    # Target value via deterministic moment at p=1 (the expectation itself)
    true_mean = finite_depth_moment_1d(
        pde, 0.0, 0.0, p=1.0, max_depth=2, rate=1.0,
        mechanism=BinaryTwoTupleMechanism,
    )

    n_samples = 40_000
    # 1. Uniform proposal
    res_uniform = estimate(
        pde, 0.0, 0.0, n_samples, seed=1234, rate=1.0,
        mechanism=BinaryTwoTupleMechanism, max_depth=2,
    )
    assert abs(res_uniform.estimate - true_mean) <= 5.0 * res_uniform.stderr

    # 2. Skewed proposal: q = (0.2, 0.8)
    def skewed_prop(code, t, x, tau, depth, tuples):
        return (0.2, 0.8)

    res_skewed = estimate(
        pde, 0.0, 0.0, n_samples, seed=5678, rate=1.0,
        mechanism=BinaryTwoTupleMechanism, max_depth=2,
        tuple_proposal=skewed_prop,
    )
    assert abs(res_skewed.estimate - true_mean) <= 5.0 * res_skewed.stderr


def test_frozen_tuple_proposal():
    key = (0, Id())
    frozen = FrozenTupleProposal({key: (0.3, 0.7)})
    q0 = frozen(Id(), 0.0, 0.0, 0.1, 0, ((Id(),), (Id(), Id())))
    assert q0 == (0.3, 0.7)
    # Fallback to uniform at depth 1
    q1 = frozen(Id(), 0.1, 0.0, 0.05, 1, ((Id(),), (Id(), Id())))
    assert q1 == (0.5, 0.5)


def test_pilot_estimator_matches_analytic_b_z():
    """Verify pilot estimated contributions B_Z against exact integrals."""
    T = 0.2
    pde = ParabolicPDE(
        T=T,
        f=lambda z: 0.0,
        f_derivatives=(),
        phi=lambda x: 1.0,
        phi_derivatives=(lambda x: 0.0,),
        exact_solution=lambda t, x: 1.0,
        name="pilot_analytic_test",
    )
    # Exact analytic values derived for continuation_depth = 0:
    # B_{Z_0} = T * exp(T)
    # B_{Z_1} = exp(2*T) - exp(T)
    exact_b0 = T * math.exp(T)
    exact_b1 = math.exp(2.0 * T) - math.exp(T)

    pilot = estimate_tuple_contributions(
        pde,
        0.0,
        0.0,
        Id(),
        n_samples=25_000,
        seed=42,
        rate=1.0,
        continuation_depth=0,
        mechanism=BinaryTwoTupleMechanism,
    )
    assert len(pilot.contributions) == 2
    assert abs(pilot.contributions[0] - exact_b0) <= 5.0 * pilot.stderr[0]
    assert abs(pilot.contributions[1] - exact_b1) <= 5.0 * pilot.stderr[1]

    # Verify sqrt optimal probabilities
    q_empirical = sqrt_optimal_probabilities(pilot.contributions)
    q_exact = sqrt_optimal_probabilities([exact_b0, exact_b1])
    np.testing.assert_allclose(q_empirical, q_exact, atol=0.05)


def test_pilot_freeze_stream_separation():
    """Frozen proposal remains identical when only evaluation seed changes."""
    pde = ParabolicPDE(
        T=0.1,
        f=lambda z: 0.0,
        f_derivatives=(),
        phi=lambda x: 1.0,
        phi_derivatives=(lambda x: 0.0,),
        exact_solution=lambda t, x: 1.0,
        name="stream_sep_test",
    )
    # Pilot run with seed 101
    pilot_101 = estimate_tuple_contributions(
        pde, 0.0, 0.0, Id(), n_samples=500, seed=101, rate=1.0,
        continuation_depth=0, mechanism=BinaryTwoTupleMechanism,
    )
    q_101 = tuple(sqrt_optimal_probabilities(pilot_101.contributions, floor_mass=0.05))

    # Evaluate with seed 202 vs seed 303: proposal remains strictly frozen
    frozen_prop = FrozenTupleProposal({(0, Id()): q_101})

    res_eval1 = estimate(
        pde, 0.0, 0.0, 1000, seed=202, rate=1.0,
        mechanism=BinaryTwoTupleMechanism, tuple_proposal=frozen_prop,
    )
    res_eval2 = estimate(
        pde, 0.0, 0.0, 1000, seed=303, rate=1.0,
        mechanism=BinaryTwoTupleMechanism, tuple_proposal=frozen_prop,
    )
    # Proposals evaluated in both runs are identical
    tuples = BinaryTwoTupleMechanism.tuples(Id())
    assert frozen_prop(Id(), 0.0, 0.0, 0.05, 0, tuples) == q_101

    # Changing pilot seed gives different estimates
    pilot_999 = estimate_tuple_contributions(
        pde, 0.0, 0.0, Id(), n_samples=500, seed=999, rate=1.0,
        continuation_depth=0, mechanism=BinaryTwoTupleMechanism,
    )
    q_999 = tuple(sqrt_optimal_probabilities(pilot_999.contributions, floor_mass=0.05))
    assert q_101 != q_999

