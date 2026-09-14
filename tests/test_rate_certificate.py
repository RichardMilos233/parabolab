"""Independent mathematical controls and tampering checks for exact certificates."""

from dataclasses import replace
from fractions import Fraction as F
import math

import pytest
import sympy as sp

from parabolab.library import allen_cahn_flat
from parabolab.mechanism import Dx, FDeriv, Id, SemilinearMechanism
from parabolab.rate_certificate import (
    CertificateFailure, branch_polynomial, certify_flat_rate,
    enclose_allen_cahn_moment, flat_terminal_state,
    factorial_depth_tail_upper,
    verify_flat_rate_certificate, verify_moment_enclosure,
)


def test_polynomial_matches_actual_raw_mechanism_including_dead_alternatives():
    """Derive the symbolic polynomial independently by enumerating real tuples."""
    pde = allen_cahn_flat()
    y = sp.symbols('id d f0 f1 f2 f3')
    codes = (Id(), Dx(1), *(FDeriv(1, k) for k in range(4)))

    def normalized_moment(c):
        if SemilinearMechanism.is_identically_zero(c, pde):
            return sp.Integer(0)
        if isinstance(c, Id):
            return y[0]
        if isinstance(c, Dx):
            return y[1]
        return sp.Rational(str(c.a))**2 * y[2 + c.k]

    actual = []
    for code in codes:
        alternatives = SemilinearMechanism.tuples(code)
        actual.append(sum(len(alternatives) * sp.prod(normalized_moment(z) for z in zs)
                          for zs in alternatives))
    assert all(sp.expand(a - b) == 0 for a, b in zip(actual, branch_polynomial(y)))
    assert actual[4] == 2 * y[2] * y[5]  # F2 still samples its dead alternative.


@pytest.mark.parametrize('rate', ['0.2', '0.73', '2'])
def test_f3_analytic_survival_moment_lies_inside_enclosure(rate):
    c = enclose_allen_cahn_moment(rates=(rate, rate), steps=60)
    exact = 36 * math.exp(float(F(rate) * c.horizon))
    assert float(c.lower[5]) < exact < float(c.upper[5])
    assert c.lower[1] == c.upper[1] == 0
    assert verify_moment_enclosure(c)


def test_flat_mean_squared_is_below_certified_second_moment_and_refinement_tightens():
    pde = allen_cahn_flat(T=0.05)
    coarse = enclose_allen_cahn_moment(steps=20)
    fine = enclose_allen_cahn_moment(steps=80)
    assert pde.exact_solution(0, 0)**2 < float(fine.root_lower)
    assert coarse.root_lower < fine.root_lower < fine.root_upper < coarse.root_upper


def test_wave_has_no_claimed_lower_bound_and_has_tilted_depth_certificate():
    c = enclose_allen_cahn_moment(family='wave', rates=('0.7', '0.8'), tilt=2)
    assert c.lower is None
    assert c.depth_tail_upper(6) == c.root_upper / 128
    assert verify_moment_enclosure(c)
    with pytest.raises(ValueError, match='tilt > 1'):
        enclose_allen_cahn_moment().depth_tail_upper(3)


def test_checker_rejects_modified_upper_witness_and_lost_time():
    c = enclose_allen_cahn_moment(steps=4)
    first = c.witnesses[0]
    wrong = replace(first, upper_end=first.upper_start)
    assert not verify_moment_enclosure(replace(c, witnesses=(wrong, *c.witnesses[1:])))
    assert not verify_moment_enclosure(replace(c, witnesses=c.witnesses[:-1]))
    assert not verify_moment_enclosure(replace(c, horizon=0.05))
    assert not verify_moment_enclosure(replace(c, mechanism='reduced'))


def test_zero_horizon_returns_exact_terminal_factors():
    c = enclose_allen_cahn_moment(horizon=0)
    assert c.lower == c.upper == flat_terminal_state()
    assert not c.witnesses
    assert verify_moment_enclosure(c)


def test_equilibrium_root_has_exact_survival_moment_and_no_omitted_contribution():
    c = enclose_allen_cahn_moment(phi=1, rates=('0.73', '0.73'))
    exact = math.exp(0.73 * 0.05)
    assert float(c.root_lower) < exact < float(c.root_upper)
    assert factorial_depth_tail_upper(c, 0) == 0


def test_factorial_tail_bounds_independent_flat_cutoff_difference():
    from parabolab.moments import MomentQuadrature, finite_depth_moment_1d
    c = enclose_allen_cahn_moment(steps=300)
    pde = allen_cahn_flat(T=0.05)
    for depth in (0, 1, 2):
        cutoff = finite_depth_moment_1d(pde, 0, 0, max_depth=depth, rate=0.73,
                                       quadrature=MomentQuadrature(8, 1))
        assert float(c.root_lower) - cutoff <= float(factorial_depth_tail_upper(c, depth))
    assert factorial_depth_tail_upper(c, 8) < factorial_depth_tail_upper(c, 4)


def test_rate_certificate_covers_interval_and_reports_inconclusive_tolerance():
    c = certify_flat_rate(steps=20, max_splits=4, tolerance='0.0000000001')
    assert verify_flat_rate_certificate(c)
    assert not c.tolerance_met
    assert c.excess_bound > 0
    assert not verify_flat_rate_certificate(replace(c, cells=c.cells[1:]))
    assert not verify_flat_rate_certificate(replace(c, excess_bound=F(0)))
    assert not verify_flat_rate_certificate(replace(c, tolerance_met=True))
    assert c.outside_interval_lower == (F(73, 256), F(11, 40))
    assert c.global_lower_optimum <= c.lower_optimum


def test_global_bound_handles_equilibrium_optimum_outside_search_interval():
    c = certify_flat_rate(phi=1, steps=20, max_splits=0, tolerance='0.00001')
    # At phi=1, inf_{lambda>0} E[H²]=1 is approached as lambda tends to zero.
    assert c.global_lower_optimum == 1
    assert c.global_excess_bound == c.incumbent.root_upper - 1
    assert not c.global_tolerance_met
    assert verify_flat_rate_certificate(c)


def test_inadequate_box_budget_is_inconclusive_and_float_inputs_are_rejected():
    with pytest.raises(CertificateFailure, match='no postfixed'):
        enclose_allen_cahn_moment(max_box_iterations=1)
    with pytest.raises(TypeError, match='exact'):
        enclose_allen_cahn_moment(horizon=0.05)
