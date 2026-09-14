"""Tests for the uniform solver interface (parabolab.solve).

The module is deliberately a thin facade: these tests pin the two things
that can silently go wrong -- the grid convention (which must agree with
the deep-branching evaluation grid) and the "thin wrapper" property (same
seed as the underlying library call must give identical numbers) -- plus
the torch boundary and the argument contract.
"""

import dataclasses
import subprocess
import sys
from functools import partial

import numpy as np
import pytest

from parabolab.library import allen_cahn_nd, allen_cahn_wave_1d, merton_hjb
from parabolab.profiles import estimate_profile
from parabolab.solve import (
    CodingTreeMC,
    Curve,
    DeepBranching,
    DeepBSDE,
    DeepGalerkin,
    compare,
    exact_on,
    grid_states,
)


# ------------------------------------------------------------ torch boundary

def test_importing_solve_does_not_import_torch():
    """The NN solvers import torch inside .solve(), never at module load.

    Checked in a subprocess: another test module in this session may have
    imported torch already, so an in-process sys.modules assertion proves
    nothing.
    """
    code = (
        "import sys; import parabolab.solve; "
        "bad = sorted(m for m in sys.modules if m == 'torch'); "
        "assert not bad, bad; print('ok')"
    )
    r = subprocess.run([sys.executable, "-c", code],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "ok" in r.stdout


def test_network_solver_argument_check_precedes_torch_import():
    """A bad first argument must raise before the lazy torch import."""
    pde = allen_cahn_nd(d=1, T=0.5)
    with pytest.raises(TypeError, match="factory"):
        DeepBranching(n_states=4, m_samples=2, epochs=1).solve(
            pde, np.linspace(-1.0, 1.0, 3))


# --------------------------------------------------------- the grid convention

def test_grid_states_shape_and_layout():
    pde = allen_cahn_nd(d=3, T=0.5)
    grid = np.linspace(-8.0, 8.0, 5)
    xs = grid_states(pde, grid)
    assert xs.shape == (5, 3)
    np.testing.assert_allclose(xs[:, 0], grid)
    # trailing coordinates sit at the grid midpoint, here 0
    np.testing.assert_allclose(xs[:, 1:], 0.0)


def test_grid_states_is_scalar_shaped_for_one_dimensional_pdes():
    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-2.0, 2.0, 4)
    xs = grid_states(pde, grid)
    assert xs.shape == (4, 1)
    np.testing.assert_allclose(xs[:, 0], grid)


def test_grid_states_agrees_with_deep_branching_evaluation_grid():
    """MC points and network curves must land on the SAME states.

    parabolab.profiles.last_coordinate_embedding uses the other convention
    (0, ..., 0, s); identical at d = 1, silently different beyond.  This
    test is the reason grid_states exists.
    """
    pytest.importorskip("torch")
    from parabolab.deep.solver import _grid_inputs

    pde = allen_cahn_nd(d=4, T=0.5)
    grid = np.linspace(-2.0, 6.0, 7)
    _, xs_deep, _ = _grid_inputs(4, 0.0, -2.0, 6.0, n_grid=7)
    np.testing.assert_allclose(grid_states(pde, grid), xs_deep)


# ------------------------------------------------------------------ exact_on

def test_exact_on_uses_the_same_embedding():
    pde = allen_cahn_nd(d=1, T=0.5)
    grid = np.linspace(-2.0, 2.0, 5)
    want = np.array([pde.exact_solution(0.0, np.array([s])) for s in grid])
    np.testing.assert_allclose(exact_on(pde, grid), want)


def test_exact_on_handles_scalar_pdes():
    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-2.0, 2.0, 5)
    want = np.array([pde.exact_solution(0.0, float(s)) for s in grid])
    np.testing.assert_allclose(exact_on(pde, grid), want)


def test_exact_on_returns_none_without_closed_form():
    pde = dataclasses.replace(allen_cahn_nd(d=1, T=0.5), exact_solution=None)
    assert exact_on(pde, np.linspace(-1.0, 1.0, 3)) is None


# -------------------------------------------------------------- CodingTreeMC

def test_coding_tree_mc_is_a_thin_wrapper():
    """Same seed as estimate_profile => bit-identical numbers."""
    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-2.0, 2.0, 5)
    curve = CodingTreeMC(n_samples=300, seed=7).solve(pde, grid)
    ref = estimate_profile(pde, 0.0, grid, 300, seed=7)
    np.testing.assert_array_equal(curve.values, ref.estimates)
    np.testing.assert_array_equal(curve.stderr, ref.stderrs)


def test_coding_tree_mc_accepts_instance_or_factory():
    grid = np.linspace(-1.0, 1.0, 3)
    a = CodingTreeMC(n_samples=200, seed=1).solve(allen_cahn_wave_1d(T=0.5), grid)
    b = CodingTreeMC(n_samples=200, seed=1).solve(
        partial(allen_cahn_wave_1d, T=0.5), grid)
    np.testing.assert_array_equal(a.values, b.values)


def test_coding_tree_mc_forwards_nonuniform_proposal_to_sampler():
    from parabolab.mc import estimate

    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-1.0, 1.0, 3)
    calls = []

    def proposal(code, t, x, tau, depth, tuples):
        calls.append((x, len(tuples)))
        weights = np.arange(1, len(tuples) + 1, dtype=float)
        return weights / weights.sum()

    curve = CodingTreeMC(
        n_samples=300, seed=7, rate=2.0, tuple_proposal=proposal,
        label="nonuniform q",
    ).solve(pde, grid)
    assert calls and any(n_tuples > 1 for _, n_tuples in calls)
    refs = [
        estimate(pde, 0.0, float(x), 300, seed=7 + i, rate=2.0,
                 tuple_proposal=proposal)
        for i, x in enumerate(grid)
    ]
    np.testing.assert_array_equal(curve.values, [r.estimate for r in refs])
    np.testing.assert_array_equal(curve.stderr, [r.stderr for r in refs])
    assert curve.label == "nonuniform q"


def test_tuple_proposals_reject_multiprocessing():
    from parabolab.proposals import FrozenTupleProposal

    proposal = FrozenTupleProposal({})
    with pytest.raises(ValueError, match="tuple_proposal requires n_jobs=1"):
        CodingTreeMC(n_jobs=2, tuple_proposal=proposal)
    pde = allen_cahn_wave_1d(T=0.1)
    with pytest.raises(ValueError, match="tuple_proposal requires n_jobs=1"):
        estimate_profile(pde, 0.0, [0.0], 10, n_jobs=2,
                         tuple_proposal=proposal)


def test_coding_tree_mc_handles_multidimensional_pdes():
    """d-dim PDEs evaluate phi at an array; a float raises deep in lambdify."""
    pde = merton_hjb(T=0.1)
    grid = np.linspace(100.0, 200.0, 4)
    curve = CodingTreeMC(n_samples=200, seed=0).solve(pde, grid)
    assert curve.values.shape == (4,)
    assert np.all(np.isfinite(curve.values))
    assert np.all(curve.stderr > 0)


def test_solver_custom_label():
    pde = allen_cahn_wave_1d(T=0.1)
    grid = np.linspace(-1.0, 1.0, 3)
    c1 = CodingTreeMC(n_samples=50, seed=0).solve(pde, grid)
    assert c1.label == "coding-tree MC"
    c2 = CodingTreeMC(n_samples=50, seed=0, label="custom label").solve(pde, grid)
    assert c2.label == "custom label"

    db = DeepBranching(label="custom db")
    assert db.label == "custom db"
    bsde = DeepBSDE(label="custom bsde")
    assert bsde.label == "custom bsde"
    dgm = DeepGalerkin(label="custom dgm")
    assert dgm.label == "custom dgm"


def test_coding_tree_mc_reproduces_the_closed_form_inside_error_bars():
    pde = allen_cahn_nd(d=1, T=0.5)
    grid = np.linspace(-4.0, 4.0, 9)
    curve = CodingTreeMC(n_samples=20_000, seed=0).solve(pde, grid)
    z = np.abs(curve.values - exact_on(pde, grid)) / curve.stderr
    assert z.max() < 4.0, f"max |err|/stderr = {z.max():.2f}"


def test_parallel_mc_requires_a_factory():
    pde = allen_cahn_wave_1d(T=0.5)
    with pytest.raises(TypeError, match="factory"):
        CodingTreeMC(n_samples=200, seed=0, n_jobs=2).solve(
            pde, np.linspace(-1.0, 1.0, 3))


def test_parallel_mc_is_independent_of_n_jobs():
    factory = partial(allen_cahn_nd, d=1, T=0.3)
    grid = np.linspace(-1.0, 1.0, 3)
    a = CodingTreeMC(n_samples=400, seed=2, n_jobs=2).solve(factory, grid)
    b = CodingTreeMC(n_samples=400, seed=2, n_jobs=4).solve(factory, grid)
    np.testing.assert_allclose(a.values, b.values)
    np.testing.assert_allclose(a.stderr, b.stderr)


# ---------------------------------------------------------------- comparison

def test_compare_chains_and_writes_a_figure(tmp_path):
    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-2.0, 2.0, 5)
    mc = CodingTreeMC(n_samples=300, seed=0).solve(pde, grid)
    out = tmp_path / "cmp.png"
    c = compare(pde, mc)
    assert c.table() is c
    assert c.plot(out) is c
    assert out.exists() and out.stat().st_size > 0


def test_compare_mixes_pointwise_and_functional_methods(tmp_path):
    """Error bars for MC, plain lines for the network methods.

    Uses a synthetic Curve so the branch is covered without torch.
    """
    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-2.0, 2.0, 5)
    mc = CodingTreeMC(n_samples=200, seed=0).solve(pde, grid)
    net = Curve(label="pretend net", grid=mc.grid,
                values=exact_on(pde, grid) + 0.01, seconds=0.0)
    out = tmp_path / "mix.png"
    compare(pde, mc, net).table().plot(out)
    assert out.exists() and out.stat().st_size > 0


def test_compare_l1_matches_manual_computation():
    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-2.0, 2.0, 5)
    exact = exact_on(pde, grid)
    net = Curve(label="net", grid=np.asarray(grid), values=exact + 0.25,
                seconds=0.0)
    errs = compare(pde, net).errors()
    np.testing.assert_allclose(errs["net"]["l1"], 0.25)
    np.testing.assert_allclose(errs["net"]["l2"], 0.0625)


def test_compare_without_a_closed_form_still_plots(tmp_path):
    pde = dataclasses.replace(allen_cahn_nd(d=1, T=0.5), exact_solution=None)
    grid = np.linspace(-1.0, 1.0, 3)
    curve = CodingTreeMC(n_samples=100, seed=0).solve(pde, grid)
    out = tmp_path / "noexact.png"
    compare(pde, curve).table().plot(out)
    assert out.exists() and out.stat().st_size > 0
    assert compare(pde, curve).errors() == {}


# ------------------------------------------------- the three network solvers

def test_deep_branching_runs_end_to_end():
    """Toy budget: this checks the wiring, not the training."""
    pytest.importorskip("torch")
    factory = partial(allen_cahn_nd, d=1, T=0.5)
    grid = np.linspace(-8.0, 8.0, 9)
    curve = DeepBranching(n_states=16, m_samples=8, epochs=5,
                          n_jobs=1, seed=0).solve(factory, grid)
    assert curve.grid.shape == (9,)
    assert curve.values.shape == (9,)
    assert curve.stderr is None
    assert np.all(np.isfinite(curve.values))


def test_deep_bsde_runs_end_to_end():
    pytest.importorskip("torch")
    pde = allen_cahn_nd(d=1, T=0.5)
    grid = np.linspace(-8.0, 8.0, 9)
    curve = DeepBSDE(epochs=3, n_states=32, seed=0).solve(pde, grid)
    assert curve.values.shape == (9,)
    assert np.all(np.isfinite(curve.values))


def test_deep_galerkin_runs_end_to_end():
    pytest.importorskip("torch")
    pde = allen_cahn_nd(d=1, T=0.5)
    grid = np.linspace(-8.0, 8.0, 9)
    curve = DeepGalerkin(epochs=3, n_states=32, seed=0).solve(pde, grid)
    assert curve.values.shape == (9,)
    assert np.all(np.isfinite(curve.values))


def test_network_solvers_accept_a_factory_too():
    pytest.importorskip("torch")
    factory = partial(allen_cahn_nd, d=1, T=0.5)
    grid = np.linspace(-8.0, 8.0, 5)
    curve = DeepBSDE(epochs=3, n_states=32, seed=0).solve(factory, grid)
    assert curve.values.shape == (5,)


# ------------------------------------- custom embedding, times, reference

def test_custom_embedding_reproduces_the_authors_convention():
    """last_coordinate_embedding must survive .solve() untouched.

    The JEQ figure scripts profile along (0, ..., 0, s) because that is the
    grid the authors' published CSVs live on; switching to solve.py's own
    convention would change every number for d >= 2.
    """
    from parabolab.profiles import estimate_profile, last_coordinate_embedding

    pde = allen_cahn_nd(d=5, T=0.5)
    grid = np.linspace(-8.0, 8.0, 5)
    embed = last_coordinate_embedding(5)
    curve = CodingTreeMC(n_samples=200, seed=3).solve(pde, grid, embed=embed)
    ref = estimate_profile(pde, 0.0, grid, 200, seed=3, embed=embed)
    np.testing.assert_array_equal(curve.values, ref.estimates)
    # and the states recorded on the curve are the authors' ones
    for i, s in enumerate(grid):
        np.testing.assert_allclose(curve.points[i], embed(s))


def test_custom_embedding_differs_from_the_default_beyond_one_dimension():
    from parabolab.profiles import last_coordinate_embedding

    pde = allen_cahn_nd(d=3, T=0.5)
    grid = np.linspace(-8.0, 8.0, 5)
    default = CodingTreeMC(n_samples=50, seed=0).solve(pde, grid)
    authors = CodingTreeMC(n_samples=50, seed=0).solve(
        pde, grid, embed=last_coordinate_embedding(3))
    assert not np.allclose(default.points[0], authors.points[0])


def test_exact_is_evaluated_at_the_curves_own_states():
    """A curve built with a custom embedding must not be scored on the
    default states."""
    from parabolab.profiles import last_coordinate_embedding

    pde = allen_cahn_nd(d=3, T=0.5)
    grid = np.linspace(-6.0, 6.0, 5)
    embed = last_coordinate_embedding(3)
    curve = CodingTreeMC(n_samples=50, seed=0).solve(pde, grid, embed=embed)
    want = np.array([pde.exact_solution(0.0, embed(s)) for s in grid])
    from parabolab.solve import _exact_at
    np.testing.assert_allclose(_exact_at(pde, curve), want)


def test_curves_carry_their_own_time():
    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-2.0, 2.0, 4)
    a = CodingTreeMC(n_samples=100, seed=0).solve(pde, grid, t=0.0)
    b = CodingTreeMC(n_samples=100, seed=0).solve(pde, grid, t=0.25)
    assert (a.t, b.t) == (0.0, 0.25)
    c = compare(pde, a, b)
    assert c.times == (0.0, 0.25)
    # each curve is scored against u(its own t, .)
    errs = c.errors()
    assert set(errs) == {"coding-tree MC"}      # same label, last wins
    assert np.isfinite(errs["coding-tree MC"]["l1"])


def test_compare_plots_multiple_times(tmp_path):
    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-2.0, 2.0, 4)
    a = CodingTreeMC(n_samples=100, seed=0).solve(pde, grid, t=0.0)
    b = CodingTreeMC(n_samples=100, seed=0).solve(pde, grid, t=0.25)
    out = tmp_path / "times.png"
    compare(pde, a, b).table().plot(out)
    assert out.exists() and out.stat().st_size > 0


def test_compare_plot_accepts_a_reference_overlay(tmp_path):
    pde = allen_cahn_wave_1d(T=0.5)
    grid = np.linspace(-2.0, 2.0, 5)
    mc = CodingTreeMC(n_samples=100, seed=0).solve(pde, grid)
    out = tmp_path / "ref.png"
    compare(pde, mc).plot(
        out, reference=(grid, exact_on(pde, grid), "authors' CSV"))
    assert out.exists() and out.stat().st_size > 0


def test_deep_branching_rejects_a_custom_embedding():
    factory = partial(allen_cahn_nd, d=2, T=0.5)
    from parabolab.profiles import last_coordinate_embedding
    with pytest.raises(ValueError, match="embed"):
        DeepBranching(n_states=4, m_samples=2, epochs=1).solve(
            factory, np.linspace(-1.0, 1.0, 3),
            embed=last_coordinate_embedding(2))
