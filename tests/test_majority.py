"""Bounded ternary Allen--Cahn sampler and Solver integration."""

import dataclasses
import math
import subprocess
import sys
from types import SimpleNamespace

import numpy as np
import pytest

from parabolab import AllenCahnMajorityMC
from parabolab.library import allen_cahn_flat, allen_cahn_wave_1d, fisher_kpp_1d
from parabolab.majority import majority_branch, sample_majority


def test_branch_rule_rate_two_is_soft_majority_and_preserves_endpoints():
    assert majority_branch(1.0, 1.0, -1.0) == 1.0
    assert majority_branch(-1.0, -1.0, 1.0) == -1.0
    assert majority_branch(0.0, 0.0, 0.0) == 0.0
    assert majority_branch(1.0, 1.0, 1.0, rate=3.0) == 1.0
    assert majority_branch(-1.0, -1.0, -1.0, rate=3.0) == -1.0

    vertices = np.array(np.meshgrid(*[[-1.0, 1.0]] * 3)).reshape(3, -1).T
    for rate in (2.0, 2.5, 3.0, 10.0):
        got = majority_branch(vertices[:, 0], vertices[:, 1], vertices[:, 2], rate)
        assert np.all(got >= -1.0) and np.all(got <= 1.0)


class _StructuralRNG:
    """One branch followed by three leaves, with recorded vector draws."""

    def __init__(self):
        self.exp_sizes = []
        self.normal_sizes = []

    def exponential(self, *, scale, size):
        self.exp_sizes.append((scale, size))
        if size == 1:
            return np.array([0.25])
        assert size == 3
        return np.array([2.0, 2.0, 2.0])

    def normal(self, *, size):
        self.normal_sizes.append(size)
        if size == 1:
            return np.array([2.0])
        assert size == 3
        return np.array([1.0, 2.0, 3.0])


def test_shared_branch_position_then_three_independent_child_draws():
    terminal_positions = []

    def phi(x):
        terminal_positions.append(x)
        return 0.0

    pde = dataclasses.replace(allen_cahn_flat(T=1.0), phi=phi)
    rng = _StructuralRNG()
    result = sample_majority(pde, 0.0, 0.0, 1, rate=2.0, rng=rng, batch_size=1)

    assert rng.exp_sizes == [(0.5, 1), (0.5, 3)]
    assert rng.normal_sizes == [1, 3]
    shared_death_position = math.sqrt(0.25) * 2.0
    expected = shared_death_position + math.sqrt(0.75) * np.array([1.0, 2.0, 3.0])
    np.testing.assert_allclose(terminal_positions, expected)
    np.testing.assert_array_equal(result.values, [0.0])
    np.testing.assert_array_equal(result.node_counts, [4])
    np.testing.assert_array_equal(result.root_branched, [True])


@pytest.mark.parametrize("phi0", [0.0, 1.0])
def test_constant_terminal_fixed_points_are_exact(phi0):
    # The library constructor excludes phi0=0 only because its closed form
    # uses phi0**-2; replacing phi is enough to test the sampler fixed point.
    pde = dataclasses.replace(allen_cahn_flat(T=0.4), phi=lambda x: phi0)
    result = sample_majority(pde, 0.0, 0.0, 100, seed=4, batch_size=13)
    np.testing.assert_array_equal(result.values, phi0)


def test_negative_one_terminal_fixed_point_is_exact():
    pde = dataclasses.replace(allen_cahn_flat(T=0.4), phi=lambda x: -1.0)
    result = sample_majority(pde, 0.0, 0.0, 100, seed=5, batch_size=17)
    np.testing.assert_array_equal(result.values, -1.0)


def test_invalid_inputs_and_explicit_compatibility_marker():
    tagged = allen_cahn_flat(T=0.2)
    with pytest.raises(ValueError, match=">= 2"):
        sample_majority(tagged, 0.0, 0.0, 2, rate=1.99)
    with pytest.raises(ValueError, match="0 <= t <= T"):
        sample_majority(tagged, -0.1, 0.0, 2)
    with pytest.raises(ValueError, match="x must be finite"):
        sample_majority(tagged, 0.0, np.inf, 2)
    with pytest.raises(ValueError, match="n_samples"):
        sample_majority(tagged, 0.0, 0.0, 0)
    with pytest.raises(TypeError, match="batch_size"):
        sample_majority(tagged, 0.0, 0.0, 2, batch_size=1.5)
    with pytest.raises(ValueError, match="either rng or seed"):
        sample_majority(tagged, 0.0, 0.0, 2, seed=0, rng=np.random.default_rng(0))

    # A callback that happens to equal u-u^3 is not accepted without the tag.
    untagged = dataclasses.replace(tagged, reaction_kind=None)
    with pytest.raises(ValueError, match="reaction_kind"):
        sample_majority(untagged, 0.0, 0.0, 2, seed=0)
    with pytest.raises(ValueError, match="reaction_kind"):
        AllenCahnMajorityMC(n_samples=2).solve(fisher_kpp_1d(), [0.0])

    multidimensional = SimpleNamespace(
        reaction_kind="allen_cahn", d=2, T=0.2, phi=lambda x: 0.5
    )
    with pytest.raises(NotImplementedError, match="d = 1"):
        sample_majority(multidimensional, 0.0, 0.0, 2, seed=0)

    for bad_horizon in (math.inf, math.nan):
        bad_pde = dataclasses.replace(tagged, T=bad_horizon)
        with pytest.raises(ValueError, match="finite and positive"):
            sample_majority(bad_pde, 0.0, 0.0, 2, seed=0)


def test_observed_terminal_values_must_satisfy_the_bounded_contract():
    pde = dataclasses.replace(allen_cahn_flat(T=0.1), phi=lambda x: 1.01)
    with pytest.raises(ValueError, match=r"\[-1, 1\]"):
        sample_majority(pde, pde.T, 0.0, 2, seed=0)


def test_flat_and_wave_means_agree_broadly_with_exact_solutions():
    cases = [
        (allen_cahn_flat(T=0.5), 0.0, 2500, 20),
        (allen_cahn_wave_1d(T=0.5), 0.0, 3500, 21),
    ]
    for pde, x, n, seed in cases:
        result = sample_majority(pde, 0.0, x, n, seed=seed, batch_size=32)
        error = abs(result.estimate - pde.exact_solution(0.0, x))
        assert error <= 6.0 * result.stderr + 0.005
        assert np.all(np.abs(result.values) <= 1.0)
        assert np.all((result.node_counts - 1) % 3 == 0)


def test_solver_returns_curve_and_accepts_factory():
    grid = np.array([-1.0, 0.0, 1.0])
    solver = AllenCahnMajorityMC(
        n_samples=500, seed=9, rate=2.0, batch_size=16, label="majority"
    )
    curve = solver.solve(lambda: allen_cahn_wave_1d(T=0.25), grid)
    assert curve.label == "majority"
    np.testing.assert_array_equal(curve.grid, grid)
    assert curve.values.shape == curve.stderr.shape == (3,)
    assert curve.points == tuple(grid)
    assert curve.t == 0.0
    assert "rate=2" in curve.note and "tree nodes" in curve.note


def test_top_level_import_remains_torch_free():
    code = (
        "import sys; import parabolab; "
        "assert 'torch' not in sys.modules; "
        "assert parabolab.AllenCahnMajorityMC; print('ok')"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert "ok" in result.stdout


def test_only_scalar_allen_cahn_library_entries_are_tagged():
    assert allen_cahn_flat().reaction_kind == "allen_cahn"
    assert allen_cahn_wave_1d().reaction_kind == "allen_cahn"
    assert fisher_kpp_1d().reaction_kind is None
