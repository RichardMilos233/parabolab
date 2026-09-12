"""Focused tests for opt-in terminal proposals and rate tuning."""

from __future__ import annotations

import math

import numpy as np
import pytest

from parabolab import TerminalTupleProposal
from parabolab.mechanism import FDeriv, Id
from parabolab.moments import MomentQuadrature, finite_depth_moment_1d
from parabolab.pde import ParabolicPDE
from parabolab.rate_optimization import (
    RateMomentDerivatives,
    finite_depth_moment_derivatives_1d,
    optimize_exponential_rate_1d,
)


class ScalarTerminalMechanism:
    values = {0: 1.0, 1: 2.0, 2: 4.0, 3: 0.0, 4: 1e308, 5: 1e307,
              6: math.inf, 7: math.nan}

    @classmethod
    def terminal(cls, code, pde, x):
        del pde, x
        return code.a * cls.values[code.k]


def test_terminal_proposal_scores_scalars_signs_and_duplicate_labels():
    proposal = TerminalTupleProposal(object(), mechanism=ScalarTerminalMechanism,
                                     floor_mass=0.1)
    large = (FDeriv(0.5, 1), FDeriv(-3.0, 2))
    tuples = ((FDeriv(-2.0, 0),), large, large)

    probabilities = proposal(Id(), 0.0, 3.0, 0.4, 2, tuples)

    q_star = np.array([1 / 13, 6 / 13, 6 / 13])
    np.testing.assert_allclose(probabilities, 0.9 * q_star + 0.1 / 3)
    assert probabilities[1] == probabilities[2]
    assert len(probabilities) == len(tuples)


def test_terminal_proposal_floor_zero_scores_all_zero_and_singleton():
    proposal = TerminalTupleProposal(object(), mechanism=ScalarTerminalMechanism,
                                     floor_mass=0.2)
    zero = FDeriv(1.0, 3)
    live = FDeriv(1.0, 0)

    np.testing.assert_allclose(
        proposal(Id(), 0.0, 0.0, 0.1, 0, ((zero,), (live,))),
        (0.1, 0.9),
    )
    assert proposal(Id(), 0.0, 0.0, 0.1, 0, ((zero,), (zero,))) == (0.5, 0.5)
    assert proposal(Id(), 0.0, 0.0, 0.1, 0, ((live,),)) == (1.0,)


def test_terminal_proposal_log_space_is_stable_for_huge_finite_values():
    proposal = TerminalTupleProposal(object(), mechanism=ScalarTerminalMechanism,
                                     floor_mass=0.05)
    huge = FDeriv(1.0, 4)
    less_huge = FDeriv(1.0, 5)

    probabilities = proposal(
        Id(), 0.0, 0.0, 0.1, 0,
        ((huge, huge), (less_huge, less_huge)),
    )

    assert np.all(np.isfinite(probabilities))
    assert sum(probabilities) == pytest.approx(1.0)
    np.testing.assert_allclose(
        probabilities,
        0.95 * np.array([100 / 101, 1 / 101]) + 0.025,
    )


@pytest.mark.parametrize("floor_mass", [0.0, 1.0, -0.1, math.inf, math.nan])
def test_terminal_proposal_rejects_invalid_floor(floor_mass):
    with pytest.raises(ValueError, match="floor_mass must be finite and strictly between"):
        TerminalTupleProposal(object(), mechanism=ScalarTerminalMechanism,
                              floor_mass=floor_mass)


@pytest.mark.parametrize("code", [FDeriv(1.0, 6), FDeriv(1.0, 7)])
def test_terminal_proposal_rejects_nonfinite_terminal_values(code):
    proposal = TerminalTupleProposal(object(), mechanism=ScalarTerminalMechanism)
    with pytest.raises(ValueError, match="requires finite terminal values"):
        proposal(Id(), 0.0, 0.0, 0.1, 0, ((code,), (FDeriv(1.0, 0),)))


def test_terminal_proposal_rejects_floor_underflow_to_zero():
    proposal = TerminalTupleProposal(
        object(), mechanism=ScalarTerminalMechanism,
        floor_mass=np.nextafter(0.0, 1.0),
    )
    with pytest.raises(ValueError, match="underflowed to zero"):
        proposal(
            Id(), 0.0, 0.0, 0.1, 0,
            ((FDeriv(1.0, 3),), (FDeriv(1.0, 0),)),
        )


def test_terminal_proposal_is_deterministic_and_ignores_clock_and_depth():
    proposal = TerminalTupleProposal(object(), mechanism=ScalarTerminalMechanism,
                                     floor_mass=0.1)
    tuples = ((FDeriv(1.0, 0),), (FDeriv(1.0, 1),))
    first = proposal(Id(), 0.0, 2.0, 0.01, 0, tuples)
    second = proposal(FDeriv(9.0, 2), 9.0, 2.0, 100.0, 17, tuples)
    assert first == second


class UnequalTupleMechanism:
    @staticmethod
    def tuples(code):
        del code
        return ((FDeriv(1.0, 0),), (FDeriv(1.0, 1),))

    @staticmethod
    def terminal(code, pde, x):
        del pde, x
        if isinstance(code, Id):
            return 1.0
        return (1.0, 9.0)[code.k] * code.a

    @staticmethod
    def is_identically_zero(code, pde):
        del code, pde
        return False


def control_pde() -> ParabolicPDE:
    return ParabolicPDE(
        T=0.1,
        f=lambda z: 0.0,
        f_derivatives=(),
        phi=lambda x: 1.0,
        phi_derivatives=(lambda x: 0.0,),
        name="unequal_tuple_control",
    )


def test_terminal_proposal_lowers_deterministic_second_moment_and_preserves_mean():
    pde = control_pde()
    quadrature = MomentQuadrature(time_order=6, normal_order=6)
    proposal = TerminalTupleProposal(pde, mechanism=UnequalTupleMechanism,
                                     floor_mass=0.05)
    common = dict(max_depth=1, rate=1.0, mechanism=UnequalTupleMechanism,
                  quadrature=quadrature)

    uniform_mean = finite_depth_moment_1d(pde, 0.0, 0.0, p=1.0, **common)
    proposal_mean = finite_depth_moment_1d(
        pde, 0.0, 0.0, p=1.0, tuple_proposal=proposal, **common)
    uniform_second = finite_depth_moment_1d(pde, 0.0, 0.0, p=2.0, **common)
    proposal_second = finite_depth_moment_1d(
        pde, 0.0, 0.0, p=2.0, tuple_proposal=proposal, **common)

    assert proposal_mean == pytest.approx(uniform_mean, rel=1e-13)
    assert proposal_second < uniform_second


def test_rate_optimizer_forwards_fixed_sampling_choices(monkeypatch):
    import parabolab.rate_optimization as module

    calls = []
    mechanism = object()
    proposal = object()
    quadrature = MomentQuadrature(time_order=3, normal_order=4)

    def fake_moment(pde, t, x, **kwargs):
        calls.append((pde, t, x, kwargs))
        return RateMomentDerivatives(value=kwargs["rate"], d_rate=1.0, d2_rate=2.0)

    monkeypatch.setattr(module, "finite_depth_moment_derivatives_1d", fake_moment)
    result = optimize_exponential_rate_1d(
        object(), 0.2, 0.3, max_depth=2, bracket=(0.5, 2.0), mechanism=mechanism,
        tuple_proposal=proposal, quadrature=quadrature, prune_zero=False,
    )

    assert result.rate == 0.5
    assert result.converged
    assert len(calls) == 2
    for _, _, _, kwargs in calls:
        assert kwargs["mechanism"] is mechanism
        assert kwargs["tuple_proposal"] is proposal
        assert kwargs["prune_zero"] is False
        assert kwargs["max_depth"] == 2
        assert kwargs["quadrature"] is quadrature


def test_rate_optimizer_objective_matches_same_proposal_moment():
    pde = control_pde()
    quadrature = MomentQuadrature(time_order=6, normal_order=6)
    proposal = TerminalTupleProposal(pde, mechanism=UnequalTupleMechanism,
                                     floor_mass=0.05)
    result = optimize_exponential_rate_1d(
        pde, 0.0, 0.0, max_depth=1, bracket=(0.5, 2.0),
        mechanism=UnequalTupleMechanism, tuple_proposal=proposal,
        quadrature=quadrature, prune_zero=False,
    )
    reference = finite_depth_moment_1d(
        pde, 0.0, 0.0, p=2.0, max_depth=1, rate=result.rate,
        mechanism=UnequalTupleMechanism, tuple_proposal=proposal,
        quadrature=quadrature, prune_zero=False,
    )
    derivative_value = finite_depth_moment_derivatives_1d(
        pde, 0.0, 0.0, max_depth=1, rate=result.rate,
        mechanism=UnequalTupleMechanism, tuple_proposal=proposal,
        quadrature=quadrature, prune_zero=False,
    ).value

    assert result.second_moment == pytest.approx(reference, rel=1e-12)
    assert result.second_moment == pytest.approx(derivative_value, rel=1e-12)


class ExactRateControlMechanism:
    @staticmethod
    def tuples(code):
        del code
        return ((FDeriv(1.0, 0),), (FDeriv(1.0, 1),))

    @staticmethod
    def terminal(code, pde, x):
        del pde, x
        if isinstance(code, Id):
            return 4.0
        return (2.0, 6.0)[code.k] * code.a

    @staticmethod
    def is_identically_zero(code, pde):
        del code, pde
        return False


def test_rate_optimizer_matches_exact_unequal_tuple_control():
    T = 0.1
    eps = 0.2
    pde = control_pde()
    proposal = TerminalTupleProposal(
        pde, mechanism=ExactRateControlMechanism, floor_mass=eps)
    tuples = ExactRateControlMechanism.tuples(Id())
    q = proposal(Id(), 0.0, 0.0, 0.01, 0, tuples)
    expected_q = ((1.0 + eps) / 4.0, (3.0 - eps) / 4.0)
    np.testing.assert_allclose(q, expected_q)
    J = 4.0 / q[0] + 36.0 / q[1]
    expected_rate = (-T * J + math.sqrt((T * J) ** 2 + 64.0 * J)) / 32.0

    result = optimize_exponential_rate_1d(
        pde, 0.0, 0.0, max_depth=1, bracket=(0.5, 3.0), tol=1e-10,
        mechanism=ExactRateControlMechanism, tuple_proposal=proposal,
        quadrature=MomentQuadrature(time_order=6, normal_order=6),
    )
    expected_second = math.exp(expected_rate * T) * (16.0 + T * J / expected_rate)
    mean = finite_depth_moment_1d(
        pde, 0.0, 0.0, p=1.0, max_depth=1, rate=result.rate,
        mechanism=ExactRateControlMechanism, tuple_proposal=proposal,
        quadrature=MomentQuadrature(time_order=6, normal_order=6),
    )

    assert result.converged
    assert result.rate == pytest.approx(expected_rate, rel=1e-9)
    assert result.second_moment == pytest.approx(expected_second, rel=1e-10)
    assert mean == pytest.approx(4.0 + 8.0 * T, rel=1e-12)


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"bracket": (0.0, 1.0)}, "Invalid bracket"),
        ({"bracket": (1.0, 1.0)}, "Invalid bracket"),
        ({"bracket": (1.0, math.inf)}, "Invalid bracket"),
        ({"bracket": (1.0, math.nan)}, "Invalid bracket"),
        ({"tol": 0.0}, "tol must be positive and finite"),
        ({"tol": math.inf}, "tol must be positive and finite"),
        ({"max_iter": 0}, "max_iter must be a positive integer"),
        ({"max_iter": 1.5}, "max_iter must be a positive integer"),
        ({"max_depth": -1}, "max_depth must be a non-negative integer"),
        ({"max_depth": 1.5}, "max_depth must be a non-negative integer"),
    ],
)
def test_rate_optimizer_validation(kwargs, message):
    with pytest.raises(ValueError, match=message):
        optimize_exponential_rate_1d(control_pde(), 0.0, 0.0, **kwargs)


def test_rate_optimizer_rejects_nonfinite_evaluation(monkeypatch):
    import parabolab.rate_optimization as module

    monkeypatch.setattr(
        module,
        "finite_depth_moment_derivatives_1d",
        lambda *args, **kwargs: RateMomentDerivatives(math.inf, math.nan, 1.0),
    )
    with pytest.raises(ValueError, match="Non-finite moment or derivative"):
        optimize_exponential_rate_1d(control_pde(), 0.0, 0.0)


def test_rate_optimizer_accepts_right_endpoint_as_constrained_minimum(monkeypatch):
    import parabolab.rate_optimization as module

    monkeypatch.setattr(
        module,
        "finite_depth_moment_derivatives_1d",
        lambda *args, **kwargs: RateMomentDerivatives(kwargs["rate"], -1.0, 1.0),
    )
    result = optimize_exponential_rate_1d(
        control_pde(), 0.0, 0.0, bracket=(0.5, 2.0))
    assert result.rate == 2.0
    assert result.converged
    assert result.iterations == 0
