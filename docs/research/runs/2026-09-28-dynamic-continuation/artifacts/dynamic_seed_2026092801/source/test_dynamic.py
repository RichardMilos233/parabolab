from __future__ import annotations

from dataclasses import dataclass
import inspect
import math
from pathlib import Path
import sys

import numpy as np
import pytest
from scipy.optimize import minimize


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import dynamic_interface as interface
import run_dynamic as runner


@dataclass(frozen=True)
class FakeSamples:
    values: np.ndarray
    node_counts: np.ndarray
    root_branched: np.ndarray
    terminal_counts: np.ndarray


def test_sampler_hash_and_reference_gate_match_frozen_contract():
    assert runner._sha256(runner.OLD_SAMPLER) == runner.EXPECTED_SAMPLER_SHA256
    assert runner._load_raw_sampler().__name__ == "raw_sample"
    reference = runner.validate_reference()
    assert reference["convergence_max"] <= 1.0e-9
    assert len(reference["convergence_per_time"]) == 201


def test_gram_matches_identity_high_precision_quadrature_and_dense_grid():
    audit = interface.compute_gram_audit(dps=80, grid_points=262_144)
    assert audit["positive_definite"]
    assert audit["identity_quadrature_max_abs_difference"] < 1.0e-15
    assert audit["identity_grid_max_abs_difference"] < 1.0e-14
    np.testing.assert_allclose(
        audit["elliptic_identity"], interface.GRAM, rtol=0.0, atol=1.0e-17
    )
    assert audit["condition_number"] == pytest.approx(6.933463751029007)
    assert audit["not_a_rigorous_rounding_enclosure"]


@pytest.mark.parametrize(
    "raw",
    [
        (0.95, 0.95),
        (1.2, 0.7),
        (0.7, 1.2),
        (0.95, 1.05),
        (1.02, 1.02),
        (0.88, 0.88),
        (0.901, 0.999),
    ],
)
def test_metric_projection_matches_independent_slsqp_and_variational_inequality(raw):
    raw = np.asarray(raw, dtype=float)
    projected, diagnostics = interface.project_gram(raw)

    def objective(candidate):
        difference = candidate - raw
        return 0.5 * float(difference @ interface.GRAM @ difference)

    constraints = (
        {"type": "ineq", "fun": lambda c: interface.SLOPE_WIDTH - (c[1] - c[0])},
        {"type": "ineq", "fun": lambda c: interface.SLOPE_WIDTH + (c[1] - c[0])},
    )
    independent = minimize(
        objective,
        np.clip(raw, interface.LOWER, interface.UPPER),
        method="SLSQP",
        bounds=((interface.LOWER, interface.UPPER),) * 2,
        constraints=constraints,
        options={"ftol": 1.0e-14, "maxiter": 1000},
    )
    assert independent.success
    np.testing.assert_allclose(projected, independent.x, rtol=0.0, atol=2.0e-7)
    assert diagnostics["variational_inequality_minimum"] >= -2.0e-16
    assert interface.is_feasible(projected, tolerance=2.0e-14)
    again, _ = interface.project_gram(projected)
    np.testing.assert_allclose(again, projected, rtol=0.0, atol=2.0e-14)


def test_terminal_analytic_derivative_and_coefficient_normalization():
    coefficients = np.array((0.931, 0.9325))
    terminal = interface.interface_terminal(coefficients)
    points = np.array((0.13, 0.71, 2.32, 4.07))
    values, derivatives = terminal(points)
    epsilon = 1.0e-6
    numerical = (terminal(points + epsilon)[0] - terminal(points - epsilon)[0]) / (
        2.0 * epsilon
    )
    np.testing.assert_allclose(derivatives, numerical, rtol=2.0e-9, atol=2.0e-10)

    grid = np.arange(262_144, dtype=float) * interface.PERIOD / 262_144
    basis = interface.basis_values(grid)
    reconstructed = basis @ coefficients
    np.testing.assert_allclose(
        values, interface.basis_values(points) @ coefficients, rtol=0.0, atol=2.0e-16
    )
    grid_terminal = terminal(grid)[0]
    np.testing.assert_allclose(grid_terminal, reconstructed, rtol=0.0, atol=2.0e-16)
    np.testing.assert_allclose(
        basis.T @ basis / grid.size, interface.GRAM, rtol=0.0, atol=1.0e-16
    )
    g = interface.g_and_derivative(grid)[0]
    np.testing.assert_allclose(
        interface.interface_terminal((0.9, 0.9))(grid)[0],
        0.9 * g,
        rtol=0.0,
        atol=6.0e-17,
    )


def test_terminal_closure_cannot_reach_reference_or_evolving_true_solution():
    terminal = interface.interface_terminal((0.9, 0.9))
    assert terminal.__code__.co_freevars == ("frozen",)
    assert len(terminal.__closure__) == 1
    np.testing.assert_array_equal(terminal.__closure__[0].cell_contents, (0.9, 0.9))
    source = inspect.getsource(interface.interface_terminal)
    assert "reference" not in source
    assert "true" not in source


def test_complete_sample_statistics_use_bhat_then_gram_solve():
    positions = np.arange(4096, dtype=float) * interface.PERIOD / 4096
    values = interface.interface_terminal((0.94, 0.941))(positions)[0]
    samples = runner.CollectedSamples(
        positions=positions,
        values=values,
        node_counts=np.ones(positions.size, dtype=np.int64),
        root_branched=np.zeros(positions.size, dtype=bool),
        terminal_counts=np.array((positions.size, 0, 0, 0, 0, 0)),
        scheduled_roots=positions.size,
        complete=True,
        seconds=0.0,
    )
    projected, stats = runner._complete_stage_statistics(samples)
    np.testing.assert_allclose(stats["bhat"], interface.GRAM @ (0.94, 0.941), atol=2e-16)
    np.testing.assert_allclose(stats["raw_coefficients"], (0.94, 0.941), atol=3e-14)
    np.testing.assert_allclose(projected, (0.94, 0.941), atol=3e-14)


def test_small_two_stage_driver_preserves_archives_and_refuses_overwrite(tmp_path):
    terminal_priors = []

    def deterministic_sampler(positions, horizon, terminal, rng, root_code=0):
        del horizon, rng, root_code
        terminal_priors.append(terminal.__closure__[0].cell_contents.copy())
        values = np.asarray(terminal(positions)[0], dtype=float)
        return FakeSamples(
            values=values,
            node_counts=np.ones(positions.size, dtype=np.int64),
            root_branched=np.zeros(positions.size, dtype=bool),
            terminal_counts=np.array((positions.size, 0, 0, 0, 0, 0)),
        )

    output = tmp_path / "dynamic_seed_test"
    result = runner.run_seed(
        seed=123,
        output=output,
        n_roots=1000,
        stages=2,
        batch_size=250,
        max_seconds=math.inf,
        grid_points=2048,
        sampler=deterministic_sampler,
        enforce_primary=False,
    )
    assert result["status"] == "complete"
    assert result["completed_stages"] == 2
    assert len(terminal_priors) == 8
    for prior in terminal_priors[:4]:
        np.testing.assert_array_equal(prior, (0.9, 0.9))

    with np.load(output / "stage_001.npz", allow_pickle=False) as data:
        required = {
            "X",
            "H",
            "node_counts",
            "root_branch_flags",
            "terminal_counts",
            "prior_c",
            "bhat",
            "raw_c",
            "projected_c",
            "rng_state_before_stage_json",
            "rng_state_after_stage_json",
            "source_hashes_json",
            "normalized_spatial_rms_errors",
        }
        assert required <= set(data.files)
        assert data["X"].shape == data["H"].shape == (1000,)
        np.testing.assert_array_equal(data["prior_c"], (0.9, 0.9))
        assert data["normalized_spatial_rms_errors"].shape == (4,)
        assert bool(data["complete"])
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        runner.run_seed(
            seed=123,
            output=output,
            n_roots=1000,
            stages=2,
            batch_size=250,
            max_seconds=math.inf,
            grid_points=2048,
            sampler=deterministic_sampler,
            enforce_primary=False,
        )


def test_time_cap_is_checked_between_complete_batches():
    calls = 0

    def slow_sampler(positions, horizon, terminal, rng, root_code=0):
        del horizon, terminal, rng, root_code
        nonlocal calls
        calls += 1
        return FakeSamples(
            values=np.zeros(positions.size),
            node_counts=np.ones(positions.size, dtype=np.int64),
            root_branched=np.zeros(positions.size, dtype=bool),
            terminal_counts=np.array((positions.size, 0, 0, 0, 0, 0)),
        )

    rng = np.random.default_rng(1)
    samples = runner.collect_samples(
        np.linspace(0, 1, 10),
        interface.interface_terminal((0.9, 0.9)),
        rng,
        slow_sampler,
        batch_size=4,
        deadline=0.0,
    )
    assert calls == 1
    assert samples.values.size == 4
    assert not samples.complete


def test_primary_budget_and_cli_constants_are_exact():
    assert runner.PRIMARY_SEEDS == (2026092801, 2026092802, 2026092803)
    assert runner.PRIMARY_N == 100_000
    assert runner.PRIMARY_STAGES == 200
    assert runner.SLAB_H == 0.08
    assert runner.PRIMARY_TOTAL_ROOTS == 60_000_000
    assert runner.PRIMARY_N * runner.PRIMARY_STAGES * len(runner.PRIMARY_SEEDS) == 60_000_000
    assert runner.MAX_SECONDS == 7200.0
