"""Tests for the blow-up sweep machinery (M5) and the max|H| diagnostic."""

import functools

import numpy as np

import parabolab as pl
from parabolab.blowup import TSweep, integrability_edge, sweep_T
from parabolab.library import allen_cahn_nd, allen_cahn_wave_1d


def test_max_abs_diagnostic_serial_and_parallel_agree():
    pde = allen_cahn_wave_1d(T=0.3)
    serial = pl.estimate(pde, 0.0, 0.0, 500, seed=3, rate=1.0)
    assert np.isfinite(serial.max_abs)
    assert serial.max_abs >= abs(serial.estimate)

    factory = functools.partial(allen_cahn_nd, d=1, T=0.3)
    a = pl.estimate_parallel(factory, 0.0, np.zeros(1), 400, seed=5,
                             rate=1.0, n_jobs=1, n_chunks=4)
    b = pl.estimate_parallel(factory, 0.0, np.zeros(1), 400, seed=5,
                             rate=1.0, n_jobs=2, n_chunks=4)
    assert a.max_abs == b.max_abs  # chunking independent of n_jobs
    assert a.max_abs >= abs(a.estimate)


def test_sweep_T_short_horizons_track_exact():
    make = functools.partial(allen_cahn_nd, 1)
    sw = sweep_T(make, [0.1, 0.3], n_samples=3000, rate=1.0,
                 seeds=(0, 1), n_jobs=1, verbose=False)
    assert sw.T.shape == sw.estimate.shape == sw.exact.shape == (2,)
    for i, T in enumerate((0.1, 0.3)):
        expected = -0.5 - 0.5 * np.tanh(0.75 * T)
        np.testing.assert_allclose(sw.exact[i], expected, rtol=1e-12)
        # short horizons: well inside the integrability window
        tol = 4 * max(sw.stderr[i], sw.seed_spread[i])
        assert sw.abs_err[i] < tol
    assert (sw.max_abs > 0).all()
    assert (sw.mean_nodes >= 1).all()
    # monotone tail growth with T for this problem
    assert sw.max_abs[1] > sw.max_abs[0]


def test_sweep_T_jcp_rate_resolution():
    make = functools.partial(allen_cahn_nd, 1)
    sw = sweep_T(make, [0.5], n_samples=200, rate="jcp", seeds=(0,),
                 n_jobs=1, verbose=False)
    np.testing.assert_allclose(sw.rate[0], -np.log(0.95) / 0.5, rtol=1e-12)


def test_integrability_edge_detection():
    def mk(abs_err, stderr):
        n = len(abs_err)
        z = np.zeros(n)
        exact = np.ones(n)  # |exact| = 1: rel_tol acts on stderr directly
        est = exact + np.asarray(abs_err, dtype=float)
        return TSweep(T=np.arange(1, n + 1, dtype=float), estimate=est,
                      seed_spread=z, stderr=np.asarray(stderr, float),
                      exact=exact, max_abs=z, mean_nodes=z, seconds=z,
                      rate=z, n_samples=1, seeds=(0,))

    # persistent drift from index 2 (T=3.0)
    sw = mk([0.001, 0.001, 1.0, 2.0], [0.01, 0.01, 0.01, 0.01])
    assert integrability_edge(sw) == 3.0
    # a single excursion that recovers is not an edge
    sw = mk([0.001, 1.0, 0.001, 0.001], [0.01] * 4)
    assert integrability_edge(sw) is None
    # everything within band and precise: no edge
    sw = mk([0.001] * 4, [0.01] * 4)
    assert integrability_edge(sw) is None
    # precision loss: stderr blows past rel_tol * |exact| from T=3.0
    # even though the (huge) error bars still cover the truth
    sw = mk([0.001, 0.001, 0.02, 0.05], [0.01, 0.01, 0.2, 0.5])
    assert integrability_edge(sw) == 3.0
