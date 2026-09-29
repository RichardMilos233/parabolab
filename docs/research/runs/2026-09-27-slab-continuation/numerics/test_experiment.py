from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import mpmath as mp
import numpy as np
import pytest


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_experiment as experiment


@dataclass(frozen=True)
class FakeSamples:
    values: np.ndarray
    node_counts: np.ndarray
    root_branched: np.ndarray
    terminal_counts: np.ndarray


def test_high_precision_reference_checks_jacobi_stationarity_and_fourier_data():
    reference = experiment.compute_reference(dps=50)

    assert all(reference.record["checks"].values())
    assert 0.0 < reference.nome < 1.0 / 300.0
    np.testing.assert_array_less(reference.coefficients, experiment.CAPS)
    assert reference.tail_squared < 1.0e-16


def test_float_terminal_and_derivative_agree_with_independent_mpmath_values():
    reference = experiment.compute_reference(dps=50)
    points = np.array([0.0, 0.137 * reference.period, 0.49 * reference.period])
    values, derivatives = experiment.jacobi_terminal(points)
    with mp.workdps(60):
        m = mp.mpf(1) / 20
        amplitude = mp.sqrt(mp.mpf(2) / 21)
        kappa = mp.sqrt(mp.mpf(40) / 21)
        expected_values = []
        expected_derivatives = []
        for point in points:
            argument = kappa * mp.mpf(str(point))
            expected_values.append(amplitude * mp.ellipfun("sn", argument, m))
            expected_derivatives.append(
                amplitude
                * kappa
                * mp.ellipfun("cn", argument, m)
                * mp.ellipfun("dn", argument, m)
            )

    np.testing.assert_allclose(
        values,
        np.array(expected_values, dtype=float),
        rtol=0.0,
        atol=2.0e-15,
    )
    np.testing.assert_allclose(
        derivatives,
        np.array(expected_derivatives, dtype=float),
        rtol=0.0,
        atol=2.0e-15,
    )


def test_projection_enforces_global_value_and_derivative_contract():
    projected, mask, difference = experiment.project_coefficients([100.0, -2.0, 7.0])
    reference = experiment.compute_reference(dps=40)
    bounds = experiment.interface_bounds(projected, reference.omega)

    np.testing.assert_array_equal(projected, [0.23, -0.003, 0.00005])
    np.testing.assert_array_equal(mask, [True, True, True])
    assert np.linalg.norm(difference) > 0.0
    assert bounds["value_admissible_lt_0p4"]
    assert bounds["derivative_admissible_lt_0p5"]


def test_polynomial_terminal_freezes_coefficients_and_uses_exact_derivative():
    source = np.array([0.2, 0.001, -0.00001])
    terminal = experiment.polynomial_terminal(source, omega=1.25)
    source[:] = 0.0
    x = np.array([0.13, 0.71])
    value, derivative = terminal(x)
    epsilon = 1.0e-6
    value_plus = terminal(x + epsilon)[0]
    value_minus = terminal(x - epsilon)[0]

    assert np.max(np.abs(value)) > 0.0
    np.testing.assert_allclose(
        derivative,
        (value_plus - value_minus) / (2.0 * epsilon),
        rtol=1.0e-8,
        atol=1.0e-9,
    )


def test_actual_continuation_path_never_calls_oracle_after_stage_one(tmp_path):
    reference = experiment.compute_reference(dps=40)
    oracle_calls = 0
    sampler_calls = 0

    def guarded_oracle(x):
        nonlocal oracle_calls
        oracle_calls += 1
        if sampler_calls > 1:
            raise AssertionError("Jacobi oracle called after stage one")
        return experiment.jacobi_terminal(x)

    def deterministic_sampler(positions, horizon, terminal, rng, root_code=0):
        del horizon, rng, root_code
        nonlocal sampler_calls
        sampler_calls += 1
        values, _ = terminal(positions)
        count = len(positions)
        return FakeSamples(
            values=np.asarray(values),
            node_counts=np.ones(count, dtype=np.int64),
            root_branched=np.zeros(count, dtype=bool),
            terminal_counts=np.array([count, 0, 0, 0, 0, 0], dtype=np.int64),
        )

    result = experiment.run_slab_seed(
        seed=17,
        n_roots=12,
        stages=3,
        batch_size=12,
        output=tmp_path,
        reference=reference,
        sampler=deterministic_sampler,
        oracle=guarded_oracle,
        max_seconds=60.0,
        grid_points=256,
    )

    assert result["status"] == "complete"
    assert sampler_calls == 3
    assert oracle_calls == 1
    assert [row["terminal_source"] for row in result["stages"]] == [
        "exact_jacobi",
        "frozen_previous_projected_coefficients",
        "frozen_previous_projected_coefficients",
    ]


def test_partial_time_cap_archive_is_not_turned_into_a_coefficient_estimate(tmp_path):
    reference = experiment.compute_reference(dps=40)

    def sampler(positions, horizon, terminal, rng, root_code=0):
        del horizon, terminal, rng, root_code
        count = len(positions)
        return FakeSamples(
            values=np.zeros(count),
            node_counts=np.ones(count, dtype=np.int64),
            root_branched=np.zeros(count, dtype=bool),
            terminal_counts=np.array([count, 0, 0, 0, 0, 0], dtype=np.int64),
        )

    result = experiment.run_slab_seed(
        seed=19,
        n_roots=8,
        stages=2,
        batch_size=2,
        output=tmp_path,
        reference=reference,
        sampler=sampler,
        max_seconds=0.0,
        grid_points=64,
    )

    assert result["status"] == "incomplete_time_cap_before_stage"
    assert result["completed_stages"] == 0
    assert result["stages"] == []


def test_cli_presets_match_frozen_protocol():
    slab = experiment._parser().parse_args(["slab"])
    majority = experiment._parser().parse_args(["majority"])

    assert slab.n == 200_000
    assert slab.seeds == [2026092701, 2026092702, 2026092703]
    assert slab.stages == 50
    assert slab.batch_size == 10_000
    assert majority.n == 8_000
    assert majority.seeds == [2026092711, 2026092712, 2026092713]
    assert majority.horizons == [0.8, 2.0]
    assert majority.batch_size == 32


def test_stage_statistics_preserve_required_root_level_audit_fields(tmp_path):
    reference = experiment.compute_reference(dps=40)
    count = 5
    samples = experiment.CollectedSamples(
        positions=np.linspace(0.0, reference.period, count, endpoint=False),
        values=np.linspace(-0.2, 0.2, count),
        node_counts=np.arange(1, count + 1, dtype=np.int64),
        root_branched=np.array([False, True, False, True, False]),
        terminal_counts=np.arange(6, dtype=np.int64),
        scheduled_roots=count,
        complete=True,
        seconds=0.25,
    )
    archive = experiment._archive_stage(tmp_path, "slab", 23, "stage-001", samples)

    with np.load(tmp_path / archive["path"]) as stored:
        assert {
            "X",
            "H",
            "node_counts",
            "root_branched",
            "terminal_counts",
        } <= set(stored.files)
        np.testing.assert_array_equal(stored["X"], samples.positions)
        np.testing.assert_array_equal(stored["H"], samples.values)
        np.testing.assert_array_equal(stored["node_counts"], samples.node_counts)
        assert bool(stored["complete"])


def test_invalid_sampler_values_fail_without_deleting_roots():
    positions = np.array([0.0, 0.1])

    def sampler(positions, horizon, terminal, rng, root_code=0):
        del horizon, terminal, rng, root_code
        return FakeSamples(
            values=np.array([0.0, np.inf]),
            node_counts=np.ones(len(positions), dtype=np.int64),
            root_branched=np.zeros(len(positions), dtype=bool),
            terminal_counts=np.array([2, 0, 0, 0, 0, 0], dtype=np.int64),
        )

    with pytest.raises(FloatingPointError, match="no root is discarded"):
        experiment.collect_samples(
            positions,
            0.08,
            experiment.jacobi_terminal,
            np.random.default_rng(0),
            sampler,
            batch_size=2,
            deadline=None,
            root_code=0,
        )
