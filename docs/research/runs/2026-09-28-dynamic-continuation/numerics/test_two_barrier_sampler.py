"""Meaningful deterministic and invariant tests for the frozen sampler."""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path
import tempfile
import time
import unittest

import mpmath as mp
import numpy as np

import two_barrier_sampler as sampler
import run_two_barrier as driver


class _UniformSequence:
    def __init__(self, values: list[float]) -> None:
        self._values = iter(values)

    def random(self) -> float:
        return next(self._values)


class TwoBarrierSamplerTests(unittest.TestCase):
    def test_protocol_constants(self) -> None:
        self.assertEqual(sampler.LOWER_BARRIER, 0.5)
        self.assertEqual(sampler.UPPER_BARRIER, 0.75)
        self.assertEqual(sampler.Z0, 2.0 / 3.0)
        self.assertEqual(sampler.LEAF_PROPOSAL_PROBABILITY, 8.0 / 15.0)
        self.assertEqual(1.0 - sampler.LEAF_PROPOSAL_PROBABILITY, 7.0 / 15.0)
        self.assertEqual(sampler.INVERSE_DENOMINATOR_CONSTANT, 20.0 / 9.0)

    def test_limiting_inverse_against_high_precision_formula(self) -> None:
        mp.mp.dps = 100
        event_uniforms = [
            math.nextafter(8.0 / 15.0, 1.0),
            0.75,
            0.99,
            math.nextafter(1.0, 0.0),
        ]
        for u in event_uniforms:
            with self.subTest(u=u):
                proposal = sampler.limiting_clock_proposal(_UniformSequence([u]))
                self.assertFalse(proposal.is_leaf)
                inverse = sampler.event_inverse_from_uniform(u)

                u_mp = mp.mpf(u)
                y_mp = u_mp / 2
                zeta_mp = (y_mp + mp.sqrt(y_mp * y_mp + 4 * y_mp)) / 2
                d_mp = (1 - u_mp) * (1 + zeta_mp) / (1 + zeta_mp - y_mp)
                q_mp = d_mp / (mp.mpf(20) / 9 - 3 * d_mp)
                s_mp = -mp.log(q_mp) / 2

                self.assertLessEqual(abs(proposal.zeta - float(zeta_mp)), 5.0e-15)
                self.assertLessEqual(
                    abs(proposal.remaining_time - float(s_mp)), 5.0e-14
                )
                self.assertLessEqual(abs(inverse.stable_d - float(d_mp)), 5.0e-15)
                self.assertLessEqual(abs(inverse.q_event - float(q_mp)), 5.0e-15)
                self.assertLessEqual(
                    abs(inverse.stable_d - (1.0 - inverse.zeta * inverse.zeta)),
                    5.0e-16,
                )
                self.assertAlmostEqual(
                    proposal.zeta * proposal.zeta / (1.0 + proposal.zeta),
                    u / 2.0,
                    delta=5.0e-15,
                )

    def test_leaf_and_strict_finite_horizon_rejection(self) -> None:
        leaf = sampler.limiting_clock_proposal(
            _UniformSequence([sampler.LEAF_PROPOSAL_PROBABILITY])
        )
        self.assertTrue(leaf.is_leaf)
        self.assertEqual(leaf.remaining_time, 0.0)

        event = sampler.limiting_clock_proposal(_UniformSequence([0.9]))
        below = math.nextafter(event.remaining_time, 0.0)
        above = math.nextafter(event.remaining_time, math.inf)
        self.assertFalse(event.remaining_time < below)
        self.assertTrue(event.remaining_time < above)

        accepted = sampler.sample_finite_clock(
            _UniformSequence([0.9, 0.1]), below
        )
        self.assertTrue(accepted.is_leaf)
        self.assertEqual(accepted.proposals, 2)
        self.assertEqual(accepted.rejections, 1)

    def test_time_zero_exact_shortcut_and_rng_state(self) -> None:
        expected = {
            0.0: (1.0, 0.25),
            math.pi / 2.0: (0.5, 0.375),
            math.pi: (0.0, 0.5),
        }
        for x, (z_expected, w_expected) in expected.items():
            with self.subTest(x=x):
                rng = np.random.Generator(np.random.PCG64(2026092831))
                state_before = copy.deepcopy(rng.bit_generator.state)
                root = sampler.sample_root(rng, 0.0, x)
                self.assertEqual(state_before, rng.bit_generator.state)
                self.assertAlmostEqual(root.normalized_output, z_expected, places=15)
                self.assertAlmostEqual(root.scaled_output, w_expected, places=15)
                self.assertEqual(root.nodes, 1)
                self.assertEqual(root.leaves, 1)
                self.assertEqual(root.clock_proposals, 0)
                self.assertEqual(root.clock_rejections, 0)

    def test_endpoint_constants_are_pathwise_barriers(self) -> None:
        horizons = [0.0, 0.25, 1.0, 4.0, 16.0, 64.0, 256.0]
        for endpoint_index, value in enumerate(
            [sampler.LOWER_BARRIER, sampler.UPPER_BARRIER]
        ):
            oracle = sampler.constant_initial_value(value)
            for horizon_index, horizon in enumerate(horizons):
                seed_sequence = np.random.SeedSequence(
                    2026092893,
                    spawn_key=(3, endpoint_index, horizon_index),
                )
                rng = np.random.Generator(np.random.PCG64(seed_sequence))
                expected, _ = sampler.scaled_barrier_defect(value, horizon)
                for _ in range(16):
                    root = sampler.sample_root(
                        rng, horizon, 0.0, initial_value=oracle
                    )
                    self.assertLessEqual(abs(root.scaled_output - expected), 1.0e-12)
                    sampler.validate_root_sample(root, horizon)

    def test_smooth_roots_satisfy_all_invariants(self) -> None:
        horizons = [0.25, 1.0, 4.0, 16.0, 64.0, 256.0]
        queries = [0.0, math.pi / 2.0, math.pi]
        for horizon_index, horizon in enumerate(horizons):
            for query_index, x in enumerate(queries):
                seed_sequence = np.random.SeedSequence(
                    2026092899,
                    spawn_key=(9, horizon_index, query_index),
                )
                rng = np.random.Generator(np.random.PCG64(seed_sequence))
                for _ in range(16):
                    root = sampler.sample_root(rng, horizon, x)
                    sampler.validate_root_sample(root, horizon)
                    self.assertFalse(root.coefficient_limit_substitution)

    def test_scaled_coefficients_are_stable_at_fixed_horizons(self) -> None:
        for c in [0.5, 0.625, 0.75]:
            at_zero, used_limit = sampler.scaled_barrier_defect(c, 0.0)
            self.assertFalse(used_limit)
            self.assertAlmostEqual(at_zero, 1.0 - c, places=15)
            at_256, used_limit = sampler.scaled_barrier_defect(c, 256.0)
            self.assertFalse(used_limit)
            self.assertGreater(at_256, 0.0)
            self.assertLessEqual(abs(at_256 - 0.5 * (c**-2 - 1.0)), 1.0e-15)

    def test_deadline_interrupts_without_a_truncated_root(self) -> None:
        rng = np.random.Generator(np.random.PCG64(2026092831))
        with self.assertRaises(sampler.SamplingDeadlineExceeded):
            sampler.sample_root(rng, 1.0, 0.0, deadline=time.monotonic() - 1.0)

    def test_sampler_does_not_import_reference(self) -> None:
        source = Path(sampler.__file__).read_text(encoding="utf-8")
        self.assertNotIn("two_barrier_reference", source)
        self.assertNotIn("reference-v1", source)

    def test_driver_rng_map_is_fixed_unique_and_reproducible(self) -> None:
        streams = driver.all_frozen_streams()
        self.assertEqual(len(streams), 93)
        identities = {
            (item["entropy"], tuple(item["spawn_key"])) for item in streams
        }
        self.assertEqual(len(identities), len(streams))
        for entropy, key in list(identities)[:12]:
            first = driver.make_rng(entropy, key).bit_generator.state
            second = driver.make_rng(entropy, key).bit_generator.state
            self.assertEqual(first, second)

    def test_independent_clock_cdf_endpoints_and_monotonicity(self) -> None:
        for horizon in driver.CLOCK_DIAGNOSTIC_HORIZONS:
            points = np.asarray([0.0, 0.25, 0.5, 0.75, 1.0]) * horizon
            values = [driver.independent_clock_cdf(float(horizon), float(s)) for s in points]
            self.assertAlmostEqual(values[-1], 1.0, places=15)
            self.assertTrue(all(left <= right for left, right in zip(values, values[1:])))
            self.assertGreater(values[0], 0.0)

    def test_exclusive_json_writer_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.json"
            driver.write_json_exclusive(path, {"status": "first"})
            self.assertEqual(json.loads(path.read_text())["status"], "first")
            with self.assertRaises(FileExistsError):
                driver.write_json_exclusive(path, {"status": "replacement"})

    def test_environment_and_gate_sources_are_available(self) -> None:
        environment = driver.environment_record()
        self.assertEqual(environment["python_executable"], "/opt/miniconda3/envs/parabolab/bin/python")
        self.assertEqual(environment["monotonic_clock"]["monotonic"], True)
        self.assertTrue(all(path.is_file() for path in driver.source_paths()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
