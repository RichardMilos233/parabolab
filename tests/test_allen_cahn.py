"""M1 exit test: Allen-Cahn vs closed forms, JEQ2023 (5.2)-(5.4).

Each point must match the exact solution within 3 * stderr at 1e5 samples
(T <= 0.5).  The default run keeps the 1e5-sample checks (a few seconds
total); the 1e6-sample confirmation is marked slow
(run with: pytest -m 'slow or not slow').
"""

import pytest

from parabolab import estimate
from parabolab.library import allen_cahn_flat, allen_cahn_wave_1d

WAVE_POINTS = [(0.0, 0.0), (0.0, 0.5), (0.25, -0.5)]


@pytest.mark.parametrize("t,x", WAVE_POINTS)
def test_traveling_wave_1e5(t, x):
    pde = allen_cahn_wave_1d(T=0.5)
    r = estimate(pde, t, x, 100_000, seed=42)
    exact = pde.exact_solution(t, x)
    assert abs(r.estimate - exact) < 3.0 * r.stderr, f"{r} vs exact {exact}"
    assert r.stderr < 5e-3  # the check must be sharp, not vacuous


def test_flat_ode_solution_1e5():
    pde = allen_cahn_flat(phi0=0.5, T=0.5)
    r = estimate(pde, 0.0, 0.0, 100_000, seed=42)
    exact = pde.exact_solution(0.0, 0.0)
    assert abs(r.estimate - exact) < 3.0 * r.stderr, f"{r} vs exact {exact}"
    assert r.stderr < 5e-3


@pytest.mark.slow
@pytest.mark.parametrize("t,x", WAVE_POINTS)
def test_traveling_wave_1e6(t, x):
    pde = allen_cahn_wave_1d(T=0.5)
    r = estimate(pde, t, x, 1_000_000, seed=7)
    exact = pde.exact_solution(t, x)
    assert abs(r.estimate - exact) < 3.0 * r.stderr, f"{r} vs exact {exact}"
    assert r.stderr < 2e-3
