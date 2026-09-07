"""Tests for state-dependent coding tree and stochastic-rate Merton problems."""
import math
import pytest
import numpy as np

from parabolab.library import vasicek_no_consumption_exact


def test_vasicek_no_consumption_terminal():
    """At terminal time t=T, F(T, y) must equal 1.0 identically."""
    T = 0.1
    for y in [-2.0, 0.0, 1.5]:
        val = vasicek_no_consumption_exact(t=T, y=y, T=T)
        assert val == pytest.approx(1.0, abs=1e-12)


def test_vasicek_no_consumption_properties():
    """Value must be strictly positive and smoothly varying with y."""
    T = 0.1
    y_vals = np.linspace(-2.0, 2.0, 5)
    vals = [vasicek_no_consumption_exact(t=0.0, y=y, T=T) for y in y_vals]
    assert all(v > 0 for v in vals)
    # Since a1 = (1-gamma)*eta > 0, higher y (higher interest rate) gives higher terminal wealth utility
    for i in range(len(vals) - 1):
        assert vals[i + 1] > vals[i]
