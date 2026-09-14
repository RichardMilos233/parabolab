"""Independent polynomial identities, analytic controls, and witness tampering."""

from dataclasses import replace
from fractions import Fraction as F
import math

import pytest
import sympy as sp

from parabolab.library import allen_cahn_wave_1d
from parabolab.mechanism import Dx, FDeriv, Id, SemilinearMechanism
from parabolab.rate_certificate import enclose_allen_cahn_moment
from parabolab.wave_certificate import (
    WAVE_TERMINAL_POLYNOMIALS, WaveRateCertificate, _bernstein, _diffusion,
    bernstein_absolute_bound, convex_moment_lower_bounds, enclose_wave_moment,
    verify_wave_moment_certificate, verify_wave_rate_certificate,
    wave_residual, wave_trial_polynomial,
)


def _poly(p, x):
    return sum(sp.Rational(a.numerator, a.denominator)*x**i for i,a in enumerate(p))


@pytest.fixture(scope='module')
def certificate():
    return enclose_wave_moment(degree=3, spatial_splits=1, error_steps=60)


def test_terminal_factors_match_sampler_and_coordinate_generator():
    pde = allen_cahn_wave_1d()
    codes = (Id(), Dx(1), *(FDeriv(1, k) for k in range(4)))
    for s in (F(1, 4), F(1, 2), F(3, 4)):
        x = math.log(float((1-s)/s))
        for code, p in zip(codes, WAVE_TERMINAL_POLYNOMIALS):
            assert float(_poly(p, s)) == pytest.approx(
                SemilinearMechanism.terminal(code, pde, x)**2, abs=1e-13)
    x = sp.Symbol('x', real=True)
    s = 1/(1+sp.exp(x))
    for p in WAVE_TERMINAL_POLYNOMIALS:
        assert sp.simplify(sp.diff(_poly(p, s), x, 2)/2 - _poly(_diffusion(p), s)) == 0


def test_residual_matches_independently_enumerated_sampler_polynomial():
    lam, T = F(73, 100), F(1, 20)
    trial = wave_trial_polynomial(lam, T, 2)
    residual = wave_residual(trial, lam, T)
    z, s = sp.symbols('z s')
    y = [sum(_poly(p, s)*z**n for n,p in enumerate(series)) for series in trial]
    pde = allen_cahn_wave_1d()
    codes = (Id(), Dx(1), *(FDeriv(1, k) for k in range(4)))

    def value(code):
        if SemilinearMechanism.is_identically_zero(code, pde):
            return 0
        if isinstance(code, Id):
            return y[0]
        if isinstance(code, Dx):
            return y[1]
        return sp.Rational(str(code.a))**2*y[2+code.k]

    for i,code in enumerate(codes):
        tuples = SemilinearMechanism.tuples(code)
        g = sum(len(tuples)*sp.prod(value(c) for c in zs) for zs in tuples)
        lp = s*s*(1-s)**2*sp.diff(y[i], s, 2)/2 + s*(1-s)*(1-2*s)*sp.diff(y[i], s)/2
        expected = sp.diff(y[i], z)/T - lp - lam*y[i] - g/lam
        actual = sum(_poly(p, s)*z**n for n,p in enumerate(residual[i]))
        assert sp.Poly(sp.expand(expected-actual), z, s).is_zero
        assert all(p == (F(0),) for p in residual[i][:2])


def test_bernstein_identity_and_subdivision_bound_known_signed_polynomial():
    # (1-2z)(s-s^2) has exact absolute supremum 1/4.
    series = ((F(0),F(1),F(-1)), (F(0),F(-2),F(2)))
    coefficients = _bernstein(series)
    z,s = sp.symbols('z s')
    reconstructed = sum(coefficients[i][j]*sp.binomial(1,i)*z**i*(1-z)**(1-i)
                        *sp.binomial(2,j)*s**j*(1-s)**(2-j)
                        for i in range(2) for j in range(3))
    assert sp.expand(reconstructed-(1-2*z)*(s-s*s)) == 0
    assert bernstein_absolute_bound(series, 0) == F(1,2)
    assert bernstein_absolute_bound(series, 1) == F(1,4)
    assert bernstein_absolute_bound(series, 3) == F(1,4)


def test_wave_analytic_boundaries_and_f3_survival(certificate):
    c = certificate
    assert verify_wave_moment_certificate(c)
    assert c.moment_at(0)[0] == 0 <= c.moment_at(0)[1]
    assert float(c.moment_at(1)[0]) <= math.exp(float(c.rate*c.moment_box.horizon)) <= float(c.moment_at(1)[1])
    trial_f3 = sum(float(sum(p)) for p in c.polynomial[5])
    exact_f3 = 36*math.exp(float(c.rate*c.moment_box.horizon))
    assert abs(trial_f3-exact_f3) <= float(c.error[5])
    assert allen_cahn_wave_1d(T=0.05).exact_solution(0,0)**2 < float(c.moment_at()[0])


def test_refined_trial_narrows_without_series_convergence_assumption(certificate):
    fine = enclose_wave_moment(degree=5, spatial_splits=1, error_steps=60,
                               moment_box=certificate.moment_box)
    assert verify_wave_moment_certificate(fine)
    assert fine.error[0] < certificate.error[0]/20
    a,b = certificate.moment_at()
    l,u = fine.moment_at()
    assert a < l < u < b


def test_checker_rejects_forged_initial_residual_error_and_time(certificate):
    c = certificate
    wrong_series = (((F(0),), *c.polynomial[0][1:]), *c.polynomial[1:])
    assert not verify_wave_moment_certificate(replace(c, polynomial=wrong_series))
    assert not verify_wave_moment_certificate(replace(c, residual=(F(0),)*6))
    first = c.error_steps[0]
    assert not verify_wave_moment_certificate(replace(c, error_steps=(replace(first,end=first.start),*c.error_steps[1:])))
    assert not verify_wave_moment_certificate(replace(c, error_steps=c.error_steps[:-1]))
    assert not verify_wave_moment_certificate(replace(c, rate=0.73))
    assert not verify_wave_moment_certificate(replace(c, moment_box=replace(c.moment_box,mechanism='reduced')))


def test_exact_convex_envelope_uses_extrapolation_not_chord():
    # f(x)=1+(x-2)^2. Internal chords overestimate, whereas valid rays underbound.
    points = tuple((F(x), F(1)+(F(x)-2)**2, F(1)+(F(x)-2)**2)
                   for x in ('1','1.5','2','2.5','3'))
    cells, exterior = convex_moment_lower_bounds(points)
    # In [1.5,2], the extrapolated lines cross at x=1.75 with height 7/8.
    assert min(cells) == F(7,8) <= 1
    assert exterior == (2,2)
    # Uncertain node intervals need not identify exterior slope signs.
    uncertain = tuple((x,max(F(0),l-F(1,2)),u+F(1,2)) for x,l,u in points)
    lower, rays = convex_moment_lower_bounds(uncertain)
    assert min(lower) <= 1 and rays == (0,0)
    with pytest.raises(ValueError):
        convex_moment_lower_bounds(tuple(reversed(points)))


def test_convex_envelope_interior_crossing_and_rate_identity(certificate):
    # No node attains the true minimum at x=2; the envelope crosses inside a cell.
    points = tuple((F(x), F(1)+(F(x)-2)**2, F(1)+(F(x)-2)**2)
                   for x in ('1','1.75','2.25','3'))
    cells,_ = convex_moment_lower_bounds(points)
    assert cells[1] == F(3,4) < 1
    c = certificate
    assert not verify_wave_rate_certificate(WaveRateCertificate((c,c)))
    assert not verify_wave_rate_certificate(WaveRateCertificate((c,), coordinate=F(2)))


def test_wrong_box_and_inexact_inputs_rejected():
    box = enclose_allen_cahn_moment(family='wave',rates=('.7','.8'))
    with pytest.raises(ValueError,match='moment_box'):
        enclose_wave_moment(rate=1, moment_box=box)
    with pytest.raises(TypeError,match='exact'):
        enclose_wave_moment(rate=0.73)
    with pytest.raises(ValueError):
        wave_trial_polynomial(F(1),F(0),3)
