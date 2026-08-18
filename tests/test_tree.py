"""Tree sampler: hand-computed weights, rng reproducibility, simple PDEs."""

import math

import numpy as np
import pytest

from parabolab import Dx, FDeriv, Id, ParabolicPDE, estimate, sample_tree
from parabolab.library import allen_cahn_wave_1d


class FakeRng:
    """Deterministic stand-in for numpy Generator.

    The queued 'normal' values are the realized draws (the requested
    standard deviation is ignored), so tree topology and positions are fully
    prescribed by the test.
    """

    def __init__(self, exponentials, normals, integers):
        self.exponentials = list(exponentials)
        self.normals = list(normals)
        self.integers_q = list(integers)

    def exponential(self, scale):
        return self.exponentials.pop(0)

    def normal(self, loc, scale, size=None):
        assert size is None, "scalar d=1 path must not request a vector"
        return self.normals.pop(0)

    def integers(self, n):
        return self.integers_q.pop(0)


def heat_pde(T=0.5):
    # f == 0: only the pure Brownian leaf contributes, u = heat semigroup.
    return ParabolicPDE(
        T=T,
        f=lambda z: 0.0,
        f_derivatives=(),
        phi=lambda x: x * x,
        phi_derivatives=(lambda x: 2.0 * x,),
        exact_solution=lambda t, x: x * x + (T - t),
        name="heat_x2",
    )


def test_hand_computed_tree_weight():
    """Force a two-generation tree and compare H against JEQ Definition 4.1.

    Topology (Allen-Cahn wave, T = 0.5, rate = 1, start (t,x) = (0, 0.3)):

      Id --tau=0.2--> branches at xb1 = 0.4 into (f*)
      f* --tau=0.1--> picks tuple #1 = (dx, dx, -1/2 f'') at xb2 = 0.35
      all three children survive to T from the SAME position xb2.
    """
    pde = allen_cahn_wave_1d(0.5)
    rate = 1.0
    rng = FakeRng(
        exponentials=[0.2, 0.1, 5.0, 0.9, 3.0],
        normals=[0.1, -0.05, 0.02, -0.01, 0.0],
        integers=[1],  # only the f* node has |M(c)| > 1
    )
    s = sample_tree(pde, 0.0, 0.3, rng=rng, rate=rate)

    phi, dphi = pde.phi, pde.phi_derivative(1)
    f2 = pde.f_derivative(2)
    # Interior weights 1/(q_c rho(tau)): Id has q=1, f* has q=1/2.
    w_id = math.exp(rate * 0.2) / rate
    w_fstar = 2.0 * math.exp(rate * 0.1) / rate
    # Leaves born at t = 0.3: weight c(u)(T, X_T) / Fbar(0.2).
    leaf_dx_1 = dphi(0.35 + 0.02) * math.exp(rate * 0.2)
    leaf_dx_2 = dphi(0.35 - 0.01) * math.exp(rate * 0.2)
    leaf_f2 = -0.5 * f2(phi(0.35 + 0.0)) * math.exp(rate * 0.2)
    expected = w_id * w_fstar * leaf_dx_1 * leaf_dx_2 * leaf_f2

    assert math.isclose(s.value, expected, rel_tol=1e-12)
    assert s.n_nodes == 5
    # every queued random number must have been consumed
    assert not rng.exponentials and not rng.normals and not rng.integers_q


def test_root_leaf_weight():
    """Root surviving to T: H = phi(x + W) / Fbar(T - t)."""
    pde = heat_pde(0.5)
    rng = FakeRng(exponentials=[9.9], normals=[0.25], integers=[])
    s = sample_tree(pde, 0.1, 1.0, rng=rng, rate=2.0)
    expected = pde.phi(1.25) * math.exp(2.0 * 0.4)
    assert math.isclose(s.value, expected, rel_tol=1e-12)
    assert s.n_nodes == 1


def test_pruned_zero_code_consumes_no_randomness():
    pde = allen_cahn_wave_1d(0.5)
    rng = FakeRng([], [], [])  # would raise on any draw
    s = sample_tree(pde, 0.0, 0.0, rng=rng, code=FDeriv(1.0, 4))
    assert s.value == 0.0
    assert s.n_nodes == 1


def test_rng_reproducibility():
    pde = allen_cahn_wave_1d(0.5)
    r1 = estimate(pde, 0.0, 0.0, 2000, seed=123)
    r2 = estimate(pde, 0.0, 0.0, 2000, seed=123)
    r3 = estimate(pde, 0.0, 0.0, 2000, seed=124)
    assert r1.estimate == r2.estimate
    assert r1.stderr == r2.stderr
    assert r1.estimate != r3.estimate


def test_heat_equation():
    """f == 0, phi = x^2: u(t, x) = x^2 + (T - t)."""
    pde = heat_pde(0.5)
    r = estimate(pde, 0.0, 1.0, 20_000, seed=0)
    exact = pde.exact_solution(0.0, 1.0)
    assert abs(r.estimate - exact) < 3.0 * r.stderr
    assert r.stderr < 0.05


def test_linear_pde():
    """f(u) = u, phi = x: u(t, x) = e^{T-t} x (Feynman-Kac with potential 1).

    Exercises interior weights, the two-tuple draw for g* (the second tuple
    prunes to zero since f'' == 0) and the survival factor.
    """
    T = 0.3
    pde = ParabolicPDE(
        T=T,
        f=lambda z: z,
        f_derivatives=(lambda z: 1.0,),
        phi=lambda x: x,
        phi_derivatives=(lambda x: 1.0,),
        exact_solution=lambda t, x: math.exp(T - t) * x,
        name="linear",
    )
    r = estimate(pde, 0.0, 1.0, 50_000, seed=1)
    exact = pde.exact_solution(0.0, 1.0)
    assert abs(r.estimate - exact) < 3.0 * r.stderr
    assert r.stderr < 0.02


def test_prune_zero_does_not_change_mean():
    """Pruning is exact: compare means with/without pruning (same tolerance)."""
    pde = allen_cahn_wave_1d(0.4)
    r_pruned = estimate(pde, 0.0, 0.0, 30_000, seed=5, prune_zero=True)
    r_full = estimate(pde, 0.0, 0.0, 30_000, seed=5, prune_zero=False)
    joint = math.hypot(r_pruned.stderr, r_full.stderr)
    assert abs(r_pruned.estimate - r_full.estimate) < 3.0 * joint
