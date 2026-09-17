"""Exact checks for the static Allen--Cahn tuple-policy certificate."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction as F
import math
import random

import numpy as np
import pytest

from parabolab.library import allen_cahn_wave_1d
from parabolab.mechanism import Dx, FDeriv, Id, SemilinearMechanism
from parabolab.rate_certificate import branch_polynomial, flat_terminal_state
from parabolab.tree import sample_tree
from parabolab.tuple_certificate import (
    AllenCahnStaticTupleProposal,
    enclose_tuple_moment,
    tuple_branch_polynomial,
    tuple_policy_interval_gate,
    verify_tuple_moment_certificate,
)


def test_uniform_policy_is_exactly_the_old_raw_polynomial():
    rng = random.Random(73055)
    uniform = (F(1, 2),) * 3
    for _ in range(30):
        state = tuple(F(rng.randint(0, 12), rng.randint(1, 9)) for _ in range(6))
        assert tuple_branch_polynomial(state, uniform) == branch_polynomial(state)


def test_exact_interval_policy_gate_accepts_and_rejects():
    exact = ((F(9), F(9)), (F(1), F(1)))
    assert tuple_policy_interval_gate(exact, (F(1, 2), F(1, 2)),
                                      (F(3, 4), F(1, 4))) == -4
    broad = ((F(0), F(9)), (F(1), F(4)))
    assert tuple_policy_interval_gate(broad, (F(1, 2), F(1, 2)),
                                      (F(3, 4), F(1, 4))) > 0
    with pytest.raises(ValueError, match="normalized positive"):
        tuple_policy_interval_gate(exact, (F(1, 2), F(1, 2)), (F(3, 4), F(0)))
    with pytest.raises(ValueError, match="0 <= L_i <= U_i"):
        tuple_policy_interval_gate(((F(2), F(1)),), (F(1),), (F(1),))
    with pytest.raises(TypeError, match="exact Fraction"):
        tuple_policy_interval_gate(((0.0, F(1)),), (F(1),), (F(1),))


def test_allen_cahn_callback_checks_support_and_raw_label_order():
    proposal = AllenCahnStaticTupleProposal(("0.95", "0.8", "0.7"))
    for scalar in (1.0, -0.5, 12.0):
        for k, expected in enumerate(((0.95, 0.05), (0.8, 0.2), (0.7, 0.3))):
            code = FDeriv(scalar, k)
            labels = SemilinearMechanism.tuples(code)
            assert proposal(code, 7.0, object(), 9.0, 11, labels) == pytest.approx(expected)
    code = FDeriv(1.0, 3)
    labels = SemilinearMechanism.tuples(code)
    assert proposal(code, 0.0, 0.0, 0.1, 0, labels) == (0.5, 0.5)
    for code in (Id(), Dx(1)):
        labels = SemilinearMechanism.tuples(code)
        assert proposal(code, 0.0, 0.0, 0.1, 0, labels) == (1.0,)
    code = FDeriv(1.0, 0)
    labels = SemilinearMechanism.tuples(code)
    with pytest.raises(ValueError, match="raw Allen-Cahn"):
        proposal(code, 0.0, 0.0, 0.1, 0, tuple(reversed(labels)))


class _ChoiceRng:
    def __init__(self):
        self.exponentials = [0.2, 0.1, 5.0, 0.9, 3.0]
        self.normals = [0.1, -0.05, 0.02, -0.01, 0.0]
        self.selected_probabilities = None

    def exponential(self, scale):
        return self.exponentials.pop(0)

    def normal(self, loc, scale, size=None):
        assert size is None
        return self.normals.pop(0)

    def choice(self, n, p):
        self.selected_probabilities = tuple(p)
        return 1


def test_callback_uses_existing_sampler_inverse_probability_weight():
    pde = allen_cahn_wave_1d(0.5)
    rng = _ChoiceRng()
    proposal = AllenCahnStaticTupleProposal((F(9, 10), F(1, 2), F(1, 2)))
    sample = sample_tree(pde, 0.0, 0.3, rng=rng, rate=1.0,
                         tuple_proposal=proposal)
    phi, dphi = pde.phi, pde.phi_derivative(1)
    f2 = pde.f_derivative(2)
    expected = math.exp(0.2) * (math.exp(0.1) / 0.1)
    expected *= dphi(0.37) * math.exp(0.2)
    expected *= dphi(0.34) * math.exp(0.2)
    expected *= -0.5 * f2(phi(0.35)) * math.exp(0.2)
    assert sample.value == pytest.approx(expected, rel=1e-12)
    assert rng.selected_probabilities == pytest.approx((0.9, 0.1))


def test_flat_certificate_verifies_and_rejects_q_and_witness_tampering():
    certificate = enclose_tuple_moment(
        horizon="0.02", rate="0.75", q=("0.95",) * 3,
        family="flat", steps=24, precision_bits=50,
    )
    assert verify_tuple_moment_certificate(certificate)
    assert certificate.root_lower < certificate.root_upper

    changed_q = replace(certificate, q=(F(1, 2),) * 3)
    assert not verify_tuple_moment_certificate(changed_q)
    first = certificate.witnesses[0]
    changed_end = (first.upper_start[0], *first.upper_end[1:])
    changed_step = replace(first, upper_end=changed_end)
    changed_witness = replace(
        certificate, witnesses=(changed_step, *certificate.witnesses[1:])
    )
    assert not verify_tuple_moment_certificate(changed_witness)


def test_wave_certificate_is_upper_only_and_verifies():
    certificate = enclose_tuple_moment(
        horizon="0.01", rate="1", q=("0.5", "0.5", "0.95"),
        family="wave", steps=20, precision_bits=50,
    )
    assert certificate.lower is None
    assert certificate.root_lower is None
    assert verify_tuple_moment_certificate(certificate)


def test_independent_scipy_flat_solution_is_contained():
    from scipy.integrate import solve_ivp

    rate = 1.0
    q = np.array([0.95, 0.95, 0.95])
    initial = np.array([float(value) for value in flat_terminal_state("0.5")])

    def rhs(time, y):
        del time
        _, d, a, b, c, e = y
        branch = np.array((
            a,
            b * d,
            a * b / q[0] + d * d * c / (4 * (1 - q[0])),
            a * c / q[1] + d * d * e / (4 * (1 - q[1])),
            a * e / q[2],
            0.0,
        ))
        return rate * y + branch / rate

    solution = solve_ivp(rhs, (0.0, 0.05), initial, method="DOP853",
                         rtol=2e-12, atol=2e-14)
    assert solution.success
    certificate = enclose_tuple_moment(
        horizon="0.05", rate="1", q=("0.95",) * 3,
        family="flat", steps=100, precision_bits=60,
    )
    assert float(certificate.root_lower) <= solution.y[0, -1] <= float(certificate.root_upper)


def test_policy_requires_exact_strictly_positive_probabilities():
    with pytest.raises(TypeError, match="exact Fraction"):
        AllenCahnStaticTupleProposal((0.5, F(1, 2), F(1, 2)))
    for q in ((F(0), F(1, 2), F(1, 2)), (F(1), F(1, 2), F(1, 2))):
        with pytest.raises(ValueError, match="0 < qk < 1"):
            AllenCahnStaticTupleProposal(q)
    for boundary in (F(1, 10**400), 1 - F(1, 10**400)):
        with pytest.raises(ValueError, match="not representable"):
            AllenCahnStaticTupleProposal((boundary, F(1, 2), F(1, 2)))
