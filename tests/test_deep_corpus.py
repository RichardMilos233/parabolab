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


# ---------------------------------------------------------------------------
# corpus
# ---------------------------------------------------------------------------

import dataclasses
import json

from parabolab.deep import corpus


def test_families_build_picklable_factories():
    import pickle
    rng = np.random.default_rng(0)
    for key, fam in corpus.FAMILIES.items():
        assert fam.key == key
        if fam.param_sampler == "fourier":
            params = corpus.sample_fourier_params(rng)
        else:
            params = tuple(0.5 * (lo + hi) for lo, hi in fam.ranges)
        factory = fam.make_factory(params)
        pickle.dumps(factory)
        pde = factory()
        assert pde.d == fam.d
        assert pde.exact_solution is not None or fam.reference_name is not None


def test_sample_instances_is_deterministic_and_in_range():
    a = corpus.sample_instances("merton", 5, seed=2, n_states=8, m_samples=4)
    b = corpus.sample_instances("merton", 5, seed=2, n_states=8, m_samples=4)
    assert a == b
    assert [s.seed for s in a] == [2_000_000 + i for i in range(5)]
    fam = corpus.FAMILIES["merton"]
    for s in a:
        assert s.family == "merton" and s.n_draws == 2
        for p, (lo, hi) in zip(s.params, fam.ranges):
            assert lo <= p <= hi
    assert json.loads(a[0].to_json())["params"] == list(a[0].params)


def _tiny_spec(seed=7, m=4, n=8, n_draws=2):
    return corpus.InstanceSpec("ac1", (0.3, 0.5), n, m, seed, n_draws)


def test_generate_instance_shapes_and_two_independent_draws():
    inst = corpus.generate_instance(_tiny_spec())
    assert inst.t.shape == (8,) and inst.x.shape == (8, 1)
    assert inst.y.shape == (2, 8) and inst.stderr.shape == (2, 8)
    assert inst.u_exact.shape == (8,) and inst.grid.shape == (101,) \
        and inst.u_grid.shape == (101,)
    assert not np.array_equal(inst.y[0], inst.y[1])      # independent draws
    assert inst.grid[0] == -8.0 and inst.grid[-1] == 8.0
    pde = corpus.FAMILIES["ac1"].make_factory((0.3, 0.5))()
    assert inst.u_grid[50] == pytest.approx(pde.exact_solution(0.0, np.array([0.0])))
    assert inst.finite.sum() == 8
    assert inst.rate > 0


def test_corpus_roundtrip_and_mismatch(tmp_path):
    specs = [_tiny_spec(seed=1), _tiny_spec(seed=2)]
    a = corpus.load_or_generate_corpus(specs, tmp_path)
    assert corpus.instance_path(specs[0], tmp_path).exists()
    b = corpus.load_or_generate_corpus(specs, tmp_path)
    for ia, ib in zip(a, b):
        np.testing.assert_array_equal(ia.y, ib.y)
        np.testing.assert_array_equal(ia.u_grid, ib.u_grid)
        assert ia.spec == ib.spec and ia.rate == ib.rate
    bad = dataclasses.replace(specs[0], m_samples=5)   # same seed -> same file
    with pytest.raises(ValueError, match="spec"):
        corpus.load_or_generate_corpus([bad], tmp_path)


def test_corpus_skips_instances_with_too_few_finite_rows(tmp_path, capsys):
    inst = corpus.generate_instance(_tiny_spec(seed=3))
    inst.y[0, :6] = np.nan
    path = corpus.instance_path(inst.spec, tmp_path)
    path.parent.mkdir(parents=True)
    corpus._save_instance(inst, path)
    out = corpus.load_or_generate_corpus([inst.spec], tmp_path, min_finite=5)
    assert out == []
    assert "finite" in capsys.readouterr().out


def test_collate_shapes_and_nan_masking():
    inst = corpus.generate_instance(_tiny_spec(seed=4))
    inst.y[1, 2] = np.nan
    rng = np.random.default_rng(0)
    batch = corpus.collate([inst, inst], n_context=5, n_query=3, rng=rng)
    assert batch["ctx_tx"].shape == (2, 5, 2) and batch["ctx_y"].shape == (2, 5)
    assert batch["ctx_se"].shape == (2, 5) and batch["params"].shape == (2, 2)
    assert batch["q_tx"].shape == (2, 3, 2) and batch["q_y"].shape == (2, 3) \
        and batch["q_u"].shape == (2, 3)
    for key in ("ctx_tx", "ctx_y", "ctx_se", "q_tx", "q_y", "q_u"):
        assert np.isfinite(batch[key]).all()
    assert batch["params"][0].tolist() == [0.3, 0.5]


# ---------------------------------------------------------------------------
# derivative labels
# ---------------------------------------------------------------------------

from parabolab.library import merton_hjb
from parabolab.deep.families import merton_hjb_derivatives


def test_merton_derivatives_match_finite_differences():
    kw = dict(T=0.1, mu=0.04, sigma=0.15, gamma=0.6, rho=0.01)
    pde = merton_hjb(**kw)
    ux, uxx = merton_hjb_derivatives(**kw)
    h = 1e-3
    for t in (0.0, 0.05):
        for x in (110.0, 150.0, 190.0):
            u = lambda z: pde.exact_solution(t, np.array([z]))
            fd1 = (u(x + h) - u(x - h)) / (2 * h)
            fd2 = (u(x + h) - 2 * u(x) + u(x - h)) / h ** 2
            assert ux(t, np.array([x])) == pytest.approx(fd1, rel=1e-5)
            assert uxx(t, np.array([x])) == pytest.approx(fd2, rel=1e-3)


def test_instance_with_derivative_labels():
    spec = corpus.InstanceSpec("merton", (0.5, 0.03, 0.1), 40, 400, 21,
                               n_draws=1, deriv_codes=("Dx1", "Dx2"))
    inst = corpus.generate_instance(spec, n_jobs=2)
    assert inst.y.shape == (1, 40) and inst.deriv.shape == (2, 40)
    assert inst.deriv_stderr.shape == (2, 40) and inst.deriv_exact.shape == (2, 40)
    ok = inst.finite
    assert ok.sum() >= 38
    z = (inst.deriv[:, ok] - inst.deriv_exact[:, ok]) / inst.deriv_stderr[:, ok]
    assert np.abs(z).max() < 5.0   # heavy-ish tails at M = 400 (gotcha 15)
    # the labels are the right size: u_x ~ 0.1..0.3 for these parameters
    assert 0.05 < np.median(np.abs(inst.deriv_exact[0])) < 0.5


def test_default_spec_has_no_derivatives_and_roundtrips(tmp_path):
    spec = corpus.InstanceSpec("merton", (0.5, 0.03, 0.1), 8, 4, 22)
    inst = corpus.generate_instance(spec)
    assert inst.deriv is None and inst.deriv_exact is None
    assert '"deriv_codes": []' in spec.to_json()
    a = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    b = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    assert b.deriv is None
    np.testing.assert_array_equal(a.y, b.y)


def test_derivative_instance_roundtrips(tmp_path):
    spec = corpus.InstanceSpec("merton", (0.5, 0.03, 0.1), 8, 4, 23,
                               n_draws=1, deriv_codes=("Dx1",))
    a = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    b = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    np.testing.assert_array_equal(a.deriv, b.deriv)
    np.testing.assert_array_equal(a.deriv_exact, b.deriv_exact)


def test_truncated_cache_file_is_regenerated(tmp_path):
    spec = corpus.InstanceSpec("merton", (0.5, 0.03, 0.1), 8, 4, 25)
    a = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    path = corpus.instance_path(spec, tmp_path)
    data = path.read_bytes()
    path.write_bytes(data[: len(data) // 2])          # half-written npz
    b = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    np.testing.assert_array_equal(a.y, b.y)
    path.write_bytes(b"")                              # empty file
    c = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    np.testing.assert_array_equal(a.y, c.y)


def test_collate_requires_two_draws():
    inst = corpus.generate_instance(corpus.InstanceSpec("merton", (0.5, 0.03, 0.1), 8, 4, 26, n_draws=1))
    with pytest.raises(ValueError, match="n_draws"):
        corpus.collate([inst], n_context=4, n_query=2, rng=np.random.default_rng(0))


def test_loader_accepts_files_written_before_deriv_codes(tmp_path):
    """Corpora cached before the deriv_codes field existed (no key in the
    stored spec JSON) must still load as derivative-less instances."""
    spec = corpus.InstanceSpec("merton", (0.5, 0.03, 0.1), 8, 4, 24)
    inst = corpus.generate_instance(spec)
    path = corpus.instance_path(spec, tmp_path)
    path.parent.mkdir(parents=True)
    old_json = json.loads(spec.to_json()); del old_json["deriv_codes"]
    np.savez(path, spec=json.dumps(old_json, sort_keys=True), t=inst.t, x=inst.x,
             y=inst.y, stderr=inst.stderr, u_exact=inst.u_exact, grid=inst.grid,
             u_grid=inst.u_grid, rate=inst.rate)
    back = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    np.testing.assert_array_equal(back.y, inst.y)
    assert back.deriv is None


# ---------------------------------------------------------------------------
# Fourier terminal conditions and the FD reference
# ---------------------------------------------------------------------------

from parabolab.deep.families import (allen_cahn_fourier_1d, fd_reference_1d,
                                     fourier_phi_expr, fourier_phi_numpy,
                                     heat_fourier_1d)

COEFFS = (0.7, 0.5, -0.3, 0.2, 0.1, -0.4, 0.25, 0.0, 0.05)   # A, a1..a4, b1..b4


def test_fourier_phi_expr_matches_numpy():
    import sympy as sp
    from parabolab.pde import x_symbols
    expr = fourier_phi_expr(COEFFS)
    fn = sp.lambdify(x_symbols(1), expr, "math")
    xs = np.linspace(-8, 8, 7)
    np.testing.assert_allclose([fn(x) for x in xs], fourier_phi_numpy(COEFFS, xs), rtol=1e-12)


def test_heat_fourier_exact_matches_fd_reference():
    pde = heat_fourier_1d(0.3, COEFFS)
    xq = np.linspace(-8, 8, 101)
    exact = np.array([pde.exact_solution(0.0, np.array([x])) for x in xq])
    fd = fd_reference_1d(pde, xq)
    assert np.abs(fd - exact).max() < 1e-3
    assert np.abs(exact - fourier_phi_numpy(COEFFS, xq)).max() > 1e-2   # T = 0.3 actually damps


def test_fd_reference_matches_allen_cahn_wave():
    from parabolab.library import allen_cahn_nd
    pde = allen_cahn_nd(d=1, T=0.3)
    xq = np.linspace(-8, 8, 101)
    exact = np.array([pde.exact_solution(0.0, np.array([x])) for x in xq])
    assert np.abs(fd_reference_1d(pde, xq) - exact).max() < 1e-4


def test_fd_reference_rejects_gradient_nonlinearity():
    from parabolab.library import merton_hjb
    with pytest.raises(ValueError, match="deriv_map"):
        fd_reference_1d(merton_hjb(), np.linspace(100, 200, 5))


def test_allen_cahn_fourier_builder():
    pde = allen_cahn_fourier_1d(0.3, COEFFS)
    assert pde.exact_solution is None and pde.d == 1 and pde.T == 0.3
    assert float(pde.phi_mu((0,))(1.0)) == pytest.approx(fourier_phi_numpy(COEFFS, np.array([1.0]))[0])


# ---------------------------------------------------------------------------
# phi-families
# ---------------------------------------------------------------------------

def test_sample_fourier_params_normalises_amplitude():
    rng = np.random.default_rng(0)
    p = corpus.sample_fourier_params(rng)
    assert len(p) == 9
    xs = np.linspace(-8, 8, 1001)
    assert np.abs(fourier_phi_numpy(p, xs)).max() == pytest.approx(0.9, rel=1e-9)


def test_phi_family_instances_have_phi_grid_and_reference():
    specs = corpus.sample_instances("heat_phi", 2, 3, n_states=30, m_samples=200, n_draws=1)
    assert specs[0].params != specs[1].params and len(specs[0].params) == 9
    inst = corpus.generate_instance(specs[0], n_jobs=2)
    assert inst.phi_grid.shape == (101,)
    np.testing.assert_allclose(inst.phi_grid, fourier_phi_numpy(specs[0].params, inst.grid), rtol=1e-10)
    ok = inst.finite
    z = (inst.y[0, ok] - inst.u_exact[ok]) / inst.stderr[0, ok]
    assert np.mean(np.abs(z) < 4.0) >= 0.95


def test_ac_phi_uses_fd_reference():
    spec = corpus.sample_instances("ac_phi", 1, 4, n_states=8, m_samples=4, n_draws=1)[0]
    inst = corpus.generate_instance(spec)
    pde = corpus.FAMILIES["ac_phi"].make_factory(spec.params)()
    assert pde.exact_solution is None
    np.testing.assert_allclose(inst.u_grid, fd_reference_1d(pde, inst.grid), rtol=1e-12)
    np.testing.assert_allclose(inst.u_exact, fd_reference_1d(pde, inst.x[:, 0]), rtol=1e-12)


def test_phi_grid_roundtrips_and_old_files_load(tmp_path):
    spec = corpus.sample_instances("heat_phi", 1, 5, n_states=8, m_samples=4, n_draws=1)[0]
    a = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    b = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    np.testing.assert_array_equal(a.phi_grid, b.phi_grid)
    # a file without phi_grid (pre-field) still loads with phi_grid None
    path = corpus.instance_path(spec, tmp_path)
    with np.load(path, allow_pickle=False) as f:
        keep = {k: f[k] for k in f.files if k != "phi_grid"}
    np.savez(path, **keep)
    c = corpus.load_or_generate_corpus([spec], tmp_path, min_finite=1)[0]
    assert c.phi_grid is None


# ---------------------------------------------------------------------------
# benchmark families and references
# ---------------------------------------------------------------------------

from parabolab.deep import families as fam_mod


def test_new_fourier_families_build_with_expected_jets():
    expect = {"kpp_fourier_1d": 1, "expgrad_fourier_1d": 2, "tan_fourier_1d": 3,
              "cosine_fourier_1d": 5, "log_fourier_1d": 4}
    for name, n_jet in expect.items():
        pde = getattr(fam_mod, name)(0.02, COEFFS)
        assert pde.d == 1 and len(pde.deriv_map) == n_jet and pde.exact_solution is None
        assert float(pde.phi_mu((0,))(0.3)) == pytest.approx(fourier_phi_numpy(COEFFS, np.array([0.3]))[0])


def test_fd_reference_with_gradient_term_matches_advected_heat():
    """f = a u_x on the heat equation: u(0, x) = E phi(x + a T + W_T), i.e. the
    heat solution shifted by a T (check against heat_fourier_1d's closed form)."""
    import sympy as sp
    from parabolab.pde import FullyNonlinearPDEnD, z_symbols
    z = z_symbols(1)
    a, T = 3.0, 0.05
    pde = FullyNonlinearPDEnD(T=T, d=1, deriv_map=((0,), (1,)), f_expr=a * z[1],
                              phi_expr=fourier_phi_expr(COEFFS), exact_solution=None, name="adv")
    heat = heat_fourier_1d(T, COEFFS)
    xq = np.linspace(-6, 6, 61)
    ref = fd_reference_1d(pde, xq, dx=0.01)
    exact = np.array([heat.exact_solution(0.0, np.array([x + a * T])) for x in xq])
    assert np.abs(ref - exact).max() < 2e-3


def test_mc_reference_matches_closed_form():
    import functools
    factory = functools.partial(fam_mod.heat_fourier_1d, 0.3, COEFFS)
    xq = np.linspace(-8, 8, 5)
    u, se = fam_mod.mc_reference_1d(factory, xq, m_samples=4000, seed=1, n_jobs=2)
    exact = np.array([factory().exact_solution(0.0, np.array([x])) for x in xq])
    assert u.shape == se.shape == (5,)
    assert np.all(np.abs(u - exact) < 4.5 * se)


def test_benchmark_families_registered():
    for key, ref, rate in (("kpp_phi", "fd_reference_1d", None), ("expgrad_phi", "fd_reference_1d", None),
                           ("tan_phi", "mc_reference_1d", 1.0), ("cosine_phi", "mc_reference_1d", 1.0),
                           ("log_phi", "mc_reference_1d", 1.0)):
        fam = corpus.FAMILIES[key]
        assert fam.param_sampler == "fourier" and fam.reference_name == ref and fam.rate == rate


def test_mc_reference_family_instance(tmp_path):
    spec = corpus.sample_instances("tan_phi", 1, 6, n_states=8, m_samples=4, n_draws=1)[0]
    # small reference budget for the test: patch via the module constant
    corpus.MC_REFERENCE_SAMPLES, saved = 200, corpus.MC_REFERENCE_SAMPLES
    try:
        inst = corpus.generate_instance(spec, n_jobs=2)
    finally:
        corpus.MC_REFERENCE_SAMPLES = saved
    assert inst.ref_stderr is not None and inst.ref_stderr.shape == (101,)
    assert np.isfinite(inst.u_grid).all() and inst.rate == 1.0
    assert inst.u_exact.shape == (8,)          # interpolated from the grid reference
    corpus._save_instance(inst, corpus.instance_path(spec, tmp_path))
    b = corpus._load_instance(spec, corpus.instance_path(spec, tmp_path))
    np.testing.assert_array_equal(b.ref_stderr, inst.ref_stderr)


def test_family_rate_reaches_the_generator():
    spec = corpus.sample_instances("tan_phi", 1, 7, n_states=4, m_samples=2, n_draws=1)[0]
    corpus.MC_REFERENCE_SAMPLES, saved = 50, corpus.MC_REFERENCE_SAMPLES
    try:
        inst = corpus.generate_instance(spec)
    finally:
        corpus.MC_REFERENCE_SAMPLES = saved
    assert inst.rate == 1.0
