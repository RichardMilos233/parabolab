"""Tests for the multi-instance corpus (Stage 0) and its library hooks."""

import functools

import numpy as np
import pytest

torch = pytest.importorskip("torch")

import parabolab.deep as deep
from parabolab.library import allen_cahn_nd


# ---------------------------------------------------------------------------
# library hook: translated Allen-Cahn wave
# ---------------------------------------------------------------------------

def test_allen_cahn_shift_zero_is_unchanged():
    old = allen_cahn_nd(d=1, T=0.4)
    new = allen_cahn_nd(d=1, T=0.4, shift=0.0)
    assert new.name == old.name == "allen_cahn_nd(d=1, T=0.4)"
    assert new.phi_expr == old.phi_expr
    for x in (-3.0, 0.0, 2.5):
        assert new.exact_solution(0.1, np.array([x])) == old.exact_solution(0.1, np.array([x]))


def test_allen_cahn_shift_is_a_translation():
    base = allen_cahn_nd(d=1, T=0.3)
    moved = allen_cahn_nd(d=1, T=0.3, shift=1.5)
    assert moved.name == "allen_cahn_nd(d=1, T=0.3, shift=1.5)"
    for t in (0.0, 0.2):
        for x in (-2.0, 0.7, 4.0):
            # inv = 0.5 for d = 1, so shift s moves the wave by 2 s in x
            assert moved.exact_solution(t, np.array([x])) == pytest.approx(
                base.exact_solution(t, np.array([x - 3.0])), abs=1e-12)
    # terminal condition matches the exact solution at T
    phi = moved.phi_mu((0,))(0.7)          # numeric phi(x) on a FullyNonlinearPDEnD
    assert float(phi) == pytest.approx(moved.exact_solution(0.3, np.array([0.7])), abs=1e-9)


# ---------------------------------------------------------------------------
# generator hook: fixed states
# ---------------------------------------------------------------------------

AC1 = functools.partial(allen_cahn_nd, d=1, T=0.5)


def test_generator_states_hook_reproduces_default_draw():
    kw = dict(n_states=6, m_samples=20, x_lo=-2.0, x_hi=2.0)
    default = deep.generate_training_data(AC1, seed=3, **kw)
    fixed = deep.generate_training_data(
        AC1, seed=3, states=(default.t, default.x), **kw)
    np.testing.assert_array_equal(fixed.x, default.x)
    np.testing.assert_array_equal(fixed.y, default.y)
    other = deep.generate_training_data(
        AC1, seed=4, states=(default.t, default.x), **kw)
    np.testing.assert_array_equal(other.x, default.x)
    assert not np.array_equal(other.y, default.y)


def test_generator_states_hook_validates_shapes():
    with pytest.raises(ValueError):
        deep.generate_training_data(
            AC1, n_states=3, m_samples=2, x_lo=-1.0, x_hi=1.0,
            states=(np.zeros(3), np.zeros((4, 1))))
