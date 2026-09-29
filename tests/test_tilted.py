import math

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.optimize import brentq

from parabolab import library
from parabolab.solve import Curve
from parabolab.tilted import (
    SemilinearProblem,
    SupEnvelope,
    TiltedSupersolutionMC,
    build_supersolution,
    sample_tilted,
)

FLAT = SupEnvelope(0.5, (3 / 8, 1 / 4, 3.0, 6.0), 0.0)
TAU_FLAT = (3 * math.pi - 2 * math.log(3)) / 5


def _F(z):
    """int_0^z dy / ((y + 3/2)(y^2 + 1/4)) by partial fractions."""
    return (
        0.4 * math.log((z + 1.5) / 1.5)
        - 0.2 * math.log((z * z + 0.25) / 0.25)
        + 1.2 * math.atan(2 * z)
    )


def _Z(t):
    """Inverse of _F: Z' = Phi(Z), Z(0) = 0, for flat Allen-Cahn at 1/2."""
    return brentq(lambda z: _F(z) - t, 0.0, 1e12, xtol=1e-14, rtol=1e-14)


def test_closed_form_horizon():
    assert _F(1e12) == pytest.approx(TAU_FLAT, abs=1e-11)
    assert quad(lambda y: 1 / ((y + 1.5) * (y * y + 0.25)), 0, 2)[0] == pytest.approx(_F(2))


def _wave_envelope():
    # phi = -1/2 - tanh(-x/2)/2 ranges over (-1, 0); f = u - u^3.
    return SupEnvelope(1.0, (2 / (3 * math.sqrt(3)), 2.0, 6.0, 6.0), 0.25)


@pytest.mark.parametrize("T,theta", [(0.5, 1.2), (1.2, 1.05)])
def test_flat_bound_matches_closed_form(T, theta):
    sup = build_supersolution(FLAT, T, theta=theta)
    closed = theta * 0.5 + _Z(theta**2 * T)
    assert sup.bound(T) == pytest.approx(closed, rel=1e-7)
    assert 1.0 < sup.theta_eff <= theta


def test_flat_beyond_fixed_rate_horizon_is_unbiased_and_bounded():
    T, theta = 1.2, 1.05  # every constant-rate sampler has infinite variance
    pde = library.allen_cahn_flat(0.5, T=T)
    sup = build_supersolution(FLAT, T, theta=theta)
    res = sample_tilted(pde, sup, 0.0, 0.0, 20_000, seed=3)
    exact = pde.exact_solution(0.0, 0.0)
    assert abs(res.estimate - exact) < 4 * res.stderr
    assert np.max(np.abs(res.values)) <= res.bound * (1 + 1e-12)
    assert res.mean_nodes <= res.work_bound
    assert abs(res.estimate - exact) < res.hoeffding_halfwidth(1e-6)


@pytest.mark.parametrize("x", [0.0, 1.5])
def test_wave_unbiased(x):
    T = 0.2
    pde = library.allen_cahn_wave_1d(T=T)
    sup = build_supersolution(_wave_envelope(), T, theta=1.2)
    res = sample_tilted(pde, sup, 0.0, x, 20_000, seed=11)
    exact = pde.exact_solution(0.0, x)
    assert abs(res.estimate - exact) < 4 * res.stderr
    assert np.max(np.abs(res.values)) <= res.bound * (1 + 1e-12)


def test_horizon_beyond_majorant_blowup_raises():
    with pytest.raises(ValueError, match="did not reach horizon"):
        build_supersolution(FLAT, 1.5, theta=1.0)


def test_theta_squared_scaling_limits_horizon():
    # W^theta_Id(T) is finite iff T < tau / theta^2.
    with pytest.raises(ValueError):
        build_supersolution(FLAT, 1.0, theta=1.25)  # tau/theta^2 = 0.925


def test_envelope_violation_is_detected():
    pde = library.allen_cahn_wave_1d(T=0.2)
    bad = SupEnvelope(0.05, (2 / (3 * math.sqrt(3)), 2.0, 6.0, 6.0), 0.25)
    sup = build_supersolution(bad, 0.2, theta=1.2)
    with pytest.raises(ValueError, match="envelope violated"):
        sample_tilted(pde, sup, 0.0, 0.0, 2_000, seed=0)


def _planar_reference(T, s0, eps, n=64, dt=1e-3):
    """1-D periodic Allen-Cahn (u_t = u_ss/2 + u - u^3), Strang splitting."""
    xs = np.arange(n) / n
    u = 0.5 + eps * np.sin(2 * np.pi * xs)
    k = np.fft.rfftfreq(n, d=1.0 / n)
    half = np.exp(-0.5 * (2 * np.pi * k) ** 2 * dt / 2)
    e2 = math.exp(2 * dt)
    for _ in range(int(round(T / dt))):
        u = np.fft.irfft(half * np.fft.rfft(u), n)
        u = u * math.exp(dt) / np.sqrt(1 + u * u * (e2 - 1))
        u = np.fft.irfft(half * np.fft.rfft(u), n)
    c = np.fft.rfft(u) / n
    w = np.full(k.size, 2.0)
    w[0] = w[-1] = 1.0
    return float(np.real(np.sum(w * c * np.exp(2j * np.pi * k * s0))))


def _planar(d, eps, T):
    a = np.full(d, 1 / math.sqrt(d))
    prob = SemilinearProblem(
        T=T, d=d,
        fks=(lambda z: z - z**3, lambda z: 1 - 3 * z * z, lambda z: -6 * z, lambda z: -6.0),
        phi=lambda z: 0.5 + eps * math.sin(2 * math.pi * float(a @ z)),
        dphi=lambda z, i: a[i] * eps * 2 * math.pi * math.cos(2 * math.pi * float(a @ z)),
    )
    lo, hi = 0.5 - eps, 0.5 + eps
    crit = [1 / math.sqrt(3)] if lo <= 1 / math.sqrt(3) <= hi else []
    sup_f = max(abs(z - z**3) for z in [lo, hi, *crit])  # f' vanishes at 1/sqrt 3
    f_env = (sup_f, max(abs(1 - 3 * lo**2), abs(1 - 3 * hi**2)), 6 * hi, 6.0)
    env = SupEnvelope(hi, f_env, tuple(np.abs(a) * 2 * math.pi * eps))
    return prob, env, a / 4


def test_supersolution_is_dimension_free():
    _, env8, _ = _planar(8, 0.1, 0.5)
    env1 = SupEnvelope(env8.phi, env8.f, 2 * math.pi * 0.1)
    s8 = build_supersolution(env8, 0.5, theta=1.05)
    s1 = build_supersolution(env1, 0.5, theta=1.05)
    assert env8.dphi_norm == pytest.approx(2 * math.pi * 0.1)
    np.testing.assert_allclose(s8.W, s1.W, rtol=1e-12)
    np.testing.assert_array_equal(s8.s, s1.s)


def test_planar_high_dim_unbiased():
    d, eps, T = 8, 0.1, 0.4
    prob, env, x0 = _planar(d, eps, T)
    ref = _planar_reference(T, 0.25, eps)
    sup = build_supersolution(env, T, theta=1.05)
    res = sample_tilted(prob, sup, 0.0, x0, 40_000, seed=13)
    assert abs(res.estimate - ref) < 4 * res.stderr
    assert np.max(np.abs(res.values)) <= res.bound * (1 + 1e-12)


def test_solver_interface_returns_curve():
    solver = TiltedSupersolutionMC(FLAT, n_samples=2_000, theta=1.2, seed=5)
    curve = solver.solve(lambda: library.allen_cahn_flat(0.5, T=0.5), np.array([0.0, 1.0]))
    assert isinstance(curve, Curve)
    assert curve.values.shape == (2,)
    assert np.all(np.isfinite(curve.stderr))
    assert "certified" in curve.note
