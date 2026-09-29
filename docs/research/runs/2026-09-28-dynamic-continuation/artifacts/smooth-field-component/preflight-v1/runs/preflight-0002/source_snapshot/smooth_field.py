"""Core D44 smooth-field sampler.

This module deliberately has no synthetic profile formula or analytic PDE
reference.  ``sample_field`` receives a known evaluator and an opaque charged
callable for the unknown input.  The outer experiment harness owns cells,
references, storage, and acceptance gates.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from pathlib import Path
import time
from typing import Any, Callable, Iterable, Protocol

import numpy as np

from budget import (
    BudgetLedger,
    BudgetLimitError,
    SINGLE_TREE_SEGMENT_CAP,
    SegmentReservation,
)


SCHEMA_VERSION = "smooth-field-sample-v1"
MAX_FREQUENCY = 64
COEFFICIENT_COUNT = 1 + 2 * MAX_FREQUENCY
PREFIX_LENGTHS = {4: 9, 16: 33, 64: 129}
COEFFICIENT_LAYOUT = "[constant,cos(1),sin(1),...,cos(64),sin(64)]"


class ProtocolAbort(RuntimeError):
    """A hard protocol condition stopped a sample; it is never a zero sample."""


class OutputFiniteError(ProtocolAbort):
    """Carries the raw attempted coefficient array for failure retention."""

    def __init__(self, message: str, coefficients: np.ndarray):
        super().__init__(message)
        self.coefficients = np.array(coefficients, dtype=np.float64, copy=True)


class OpaqueEvaluator(Protocol):
    def __call__(self, x: float) -> float: ...


@dataclass
class Node:
    index: int
    parent: int | None
    children: list[int]
    start: float
    end: float
    length: float
    leaf_id: int | None = None


@dataclass
class ClockTree:
    branching: int
    rate: float
    tau: float
    nodes: list[Node]
    leaf_nodes: list[int]

    @property
    def segment_count(self) -> int:
        return len(self.nodes)

    @property
    def leaf_count(self) -> int:
        return len(self.leaf_nodes)

    @property
    def internal_count(self) -> int:
        return self.segment_count - self.leaf_count


@dataclass(frozen=True)
class SamplerSpec:
    branching: int
    rate: float
    tau: float
    kappa: float
    derivative_order: int
    max_frequency: int = MAX_FREQUENCY

    def validate(self) -> None:
        if self.branching not in (3, 5):
            raise ValueError("E5 supports only the frozen branching factors 3 and 5")
        if self.rate != float(self.branching if self.branching == 5 else 2):
            raise ValueError("rate does not match the frozen cubic/quintic parent")
        if not (self.tau > 0.0 and self.kappa > 0.0):
            raise ValueError("tau and kappa must be strictly positive")
        if self.derivative_order not in (1, 2, 3):
            raise ValueError("E5 derivative order must be 1, 2, or 3")
        if self.max_frequency != MAX_FREQUENCY:
            raise ValueError("E5 always constructs the full N=64 array")


@dataclass
class GaussianPreparation:
    edge_standard_normals: np.ndarray
    edge_gaussians: np.ndarray
    leaf_path_sums: np.ndarray
    residuals: np.ndarray
    aggregate: float
    chronological_common_variance: float
    damping_variance: float
    effective_variances: np.ndarray
    child_weights: list[np.ndarray | None]


@dataclass
class SampleResult:
    coefficients: np.ndarray
    metadata: dict[str, Any]
    query_points: list[float] = field(default_factory=list)
    query_values: list[float] = field(default_factory=list)


class KnownEvaluatorCache:
    """Exact-float-key cache for the paid known evaluator work counter."""

    def __init__(
        self,
        evaluator: Callable[[float], float],
    ):
        self._evaluator = evaluator
        self._cache: dict[str, float] = {}
        self.calls = 0

    def __call__(self, x: float) -> float:
        key = float(x).hex()
        if key not in self._cache:
            self.calls += 1
            value = float(self._evaluator(float(x)))
            if not math.isfinite(value):
                raise ProtocolAbort("known evaluator returned a nonfinite value")
            self._cache[key] = value
        return self._cache[key]


def stream_identifier(seed: int, cell_index: int, sample_index: int, tag: int) -> dict[str, int]:
    return {
        "seed": int(seed),
        "cell_index": int(cell_index),
        "sample_index": int(sample_index),
        "tag": int(tag),
    }


def make_generator(identifier: dict[str, int]) -> np.random.Generator:
    seed_sequence = np.random.SeedSequence(
        [
            identifier["seed"],
            identifier["cell_index"],
            identifier["sample_index"],
            identifier["tag"],
        ]
    )
    return np.random.Generator(np.random.PCG64DXSM(seed_sequence))


def _ensure_tree_capacity(
    ledger: BudgetLedger,
    reservation: SegmentReservation,
    reserved_capacity: int,
    needed: int,
) -> int:
    while needed > reserved_capacity:
        try:
            reserved_capacity += ledger.extend_segment_reservation(reservation)
        except BudgetLimitError as exc:
            raise ProtocolAbort(str(exc)) from exc
    return reserved_capacity


def generate_clock_tree(
    spec: SamplerSpec,
    rng: np.random.Generator,
    ledger: BudgetLedger,
    phase: str,
    identifier: dict[str, Any],
) -> ClockTree:
    """Generate the complete clock genealogy in DFS preorder.

    Each segment uses one scalar ``Generator.exponential(scale=1/rate)``
    call, including terminal segments. Children are visited left to right.
    Persistent segment capacity is reserved before each block can be created.
    """

    reservation = ledger.begin_segment_reservation(phase, identifier)
    initial_state = ledger.snapshot()
    reserved_capacity = int(
        initial_state["active_segment_reservations"][reservation.reservation_id]["reserved"]
    )
    nodes: list[Node] = []
    stack: list[tuple[int | None, float, int | None]] = [(None, 0.0, None)]
    attempted_exponential_draws = 0
    status = "failed"
    try:
        while stack:
            if len(nodes) >= SINGLE_TREE_SEGMENT_CAP:
                raise ProtocolAbort(f"single-tree segment cap {SINGLE_TREE_SEGMENT_CAP} reached")
            reserved_capacity = _ensure_tree_capacity(
                ledger, reservation, reserved_capacity, len(nodes) + 1
            )
            parent, start, child_slot = stack.pop()
            attempted_exponential_draws += 1
            lifetime = float(rng.exponential(scale=1.0 / spec.rate))
            if not math.isfinite(lifetime) or lifetime < 0.0:
                raise ProtocolAbort("nonfinite or negative exponential lifetime")
            split_time = start + lifetime
            terminal = split_time >= spec.tau
            end = spec.tau if terminal else split_time
            length = end - start
            if not (math.isfinite(length) and length >= 0.0):
                raise ProtocolAbort("nonfinite or negative segment length")
            index = len(nodes)
            nodes.append(Node(index, parent, [], start, end, length))
            if parent is not None:
                assert child_slot is not None
                parent_children = nodes[parent].children
                if child_slot != len(parent_children):
                    raise ProtocolAbort("child traversal order mismatch")
                parent_children.append(index)
            if not terminal:
                for slot in range(spec.branching - 1, -1, -1):
                    stack.append((index, end, slot))
        leaf_nodes = [node.index for node in nodes if not node.children]
        for leaf_id, node_index in enumerate(leaf_nodes):
            nodes[node_index].leaf_id = leaf_id
        tree = ClockTree(spec.branching, spec.rate, spec.tau, nodes, leaf_nodes)
        validate_tree(tree)
        status = "complete"
        return tree
    except Exception:
        status = "failed_caught"
        raise
    finally:
        # A caught exception commits the exact attempted prefix. A hard process
        # crash leaves the persistent reservation unresolved and blocks resume.
        ledger.commit_segment_reservation(
            reservation,
            len(nodes),
            status=status,
            exponential_draws=attempted_exponential_draws,
        )


def validate_tree(tree: ClockTree) -> None:
    if not tree.nodes or tree.nodes[0].parent is not None:
        raise ProtocolAbort("tree has no valid root")
    if tree.segment_count > SINGLE_TREE_SEGMENT_CAP:
        raise ProtocolAbort("tree exceeds single-tree cap")
    chronological_height = np.empty(tree.segment_count, dtype=np.float64)
    for node in tree.nodes:
        if node.index < 0 or node.index >= tree.segment_count or tree.nodes[node.index] is not node:
            raise ProtocolAbort("tree node indices do not match preorder storage")
        if node.children and len(node.children) != tree.branching:
            raise ProtocolAbort("internal segment does not have frozen branching arity")
        if not node.children and node.end != tree.tau:
            raise ProtocolAbort("leaf segment does not reach tau")
        if node.parent is None:
            if node.index != 0:
                raise ProtocolAbort("only the preorder root may have no parent")
            chronological_height[node.index] = node.length
        else:
            if not 0 <= node.parent < node.index:
                raise ProtocolAbort("parent must precede child in preorder storage")
            if tree.nodes[node.parent].end != node.start:
                raise ProtocolAbort("child segment does not start at parent endpoint")
            if node.index not in tree.nodes[node.parent].children:
                raise ProtocolAbort("parent/child links disagree")
            chronological_height[node.index] = (
                chronological_height[node.parent] + node.length
            )
    expected_segments = 1 + tree.branching * tree.internal_count
    expected_leaves = 1 + (tree.branching - 1) * tree.internal_count
    if tree.segment_count != expected_segments or tree.leaf_count != expected_leaves:
        raise ProtocolAbort("full B-ary segment/leaf identity failed")
    for leaf_index in tree.leaf_nodes:
        if not math.isclose(
            float(chronological_height[leaf_index]),
            tree.tau,
            rel_tol=2e-14,
            abs_tol=2e-14,
        ):
            raise ProtocolAbort("root-to-leaf chronological length mismatch")


def parent_value(branching: int, values: np.ndarray) -> float:
    if values.shape != (branching,):
        raise ValueError("parent value receives exactly B children")
    product = float(np.prod(values, dtype=np.float64))
    if branching == 3:
        return 0.5 * (float(math.fsum(float(x) for x in values)) - product)
    if branching == 5:
        return (6.0 / 25.0) * float(math.fsum(float(x) for x in values)) - 0.2 * product
    raise ValueError("unsupported branching")


def evaluate_tree(tree: ClockTree, leaf_values: np.ndarray) -> float:
    if leaf_values.shape != (tree.leaf_count,):
        raise ValueError("leaf value shape mismatch")
    values = np.empty(tree.segment_count, dtype=np.float64)
    for node in reversed(tree.nodes):
        if node.leaf_id is not None:
            values[node.index] = leaf_values[node.leaf_id]
        else:
            child_values = np.asarray([values[c] for c in node.children], dtype=np.float64)
            values[node.index] = parent_value(tree.branching, child_values)
    return float(values[0])


def prepare_gaussian(
    tree: ClockTree,
    kappa: float,
    rng: np.random.Generator,
    ledger: BudgetLedger,
    identifier: dict[str, Any],
) -> GaussianPreparation:
    segment_count = tree.segment_count
    # Frozen zero-length policy: draw one standard normal for every segment in
    # a single vector call, then multiply by sqrt(kappa*ell). Zero edges thus
    # consume a draw but yield an exact floating zero.
    # The caller precharges all RNG work for this phase immediately before
    # entering the draw sequence.
    standard = rng.standard_normal(size=(segment_count,), dtype=np.float64)
    lengths = np.asarray([node.length for node in tree.nodes], dtype=np.float64)
    scales = np.sqrt(kappa * lengths, dtype=np.float64)
    edge_gaussians = standard * scales

    effective = np.empty(segment_count, dtype=np.float64)
    aggregates = np.empty(segment_count, dtype=np.float64)
    child_weights: list[np.ndarray | None] = [None] * segment_count
    for node in reversed(tree.nodes):
        if not node.children:
            effective[node.index] = node.length
            aggregates[node.index] = edge_gaussians[node.index]
            continue
        child_a = np.asarray([effective[c] for c in node.children], dtype=np.float64)
        if np.any(~np.isfinite(child_a)) or np.any(child_a < 0.0):
            raise ProtocolAbort("invalid child effective variance")
        zero_positions = np.flatnonzero(child_a == 0.0)
        if zero_positions.size:
            harmonic = 0.0
            alpha = np.zeros(len(node.children), dtype=np.float64)
            alpha[int(zero_positions[0])] = 1.0
        else:
            minimum = float(np.min(child_a))
            denominator = float(math.fsum(minimum / float(x) for x in child_a))
            harmonic = minimum / denominator
            alpha = harmonic / child_a
        effective[node.index] = node.length + harmonic
        aggregates[node.index] = edge_gaussians[node.index] + float(
            math.fsum(float(alpha[k]) * float(aggregates[c]) for k, c in enumerate(node.children))
        )
        child_weights[node.index] = alpha

    path_sums = np.empty(segment_count, dtype=np.float64)
    for node in tree.nodes:
        parent_sum = 0.0 if node.parent is None else path_sums[node.parent]
        path_sums[node.index] = parent_sum + edge_gaussians[node.index]
    leaf_path_sums = path_sums[np.asarray(tree.leaf_nodes, dtype=np.int64)]
    aggregate = float(aggregates[0])
    residuals = leaf_path_sums - aggregate
    common = float(effective[0])
    lower = tree.tau / tree.leaf_count
    tolerance = 5e-12 * max(1.0, tree.tau)
    if common < lower - tolerance or common > tree.tau + tolerance:
        raise ProtocolAbort("chronological common variance outside [tau/n,tau]")
    result_arrays = (standard, edge_gaussians, leaf_path_sums, residuals, effective)
    if any(np.any(~np.isfinite(array)) for array in result_arrays):
        raise ProtocolAbort("nonfinite Gaussian preparation")
    if not math.isfinite(aggregate + common):
        raise ProtocolAbort("nonfinite aggregate or common variance")
    return GaussianPreparation(
        standard,
        edge_gaussians,
        leaf_path_sums,
        residuals,
        aggregate,
        common,
        kappa * common,
        effective,
        child_weights,
    )


def falling_factorial(n: int, j: int) -> int:
    if j < 0:
        raise ValueError("negative derivative order")
    if n < j:
        return 0
    result = 1
    for value in range(n - j + 1, n + 1):
        result *= value
    return result


def corner_mixed_partial(
    tree: ClockTree,
    base_leaf_values: np.ndarray,
    selected_leaf_ids: Iterable[int],
) -> float:
    selected = tuple(int(i) for i in selected_leaf_ids)
    if len(set(selected)) != len(selected):
        raise ValueError("corner derivative requires distinct leaf labels")
    if any(i < 0 or i >= tree.leaf_count for i in selected):
        raise ValueError("selected leaf label outside tree")
    total = 0.0
    j = len(selected)
    for mask in range(1 << j):
        values = np.array(base_leaf_values, dtype=np.float64, copy=True)
        sign_product = 1.0
        for position, leaf_id in enumerate(selected):
            epsilon = 1.0 if ((mask >> position) & 1) else -1.0
            values[leaf_id] = epsilon
            sign_product *= epsilon
        total += sign_product * evaluate_tree(tree, values)
    answer = math.ldexp(total, -j)
    if not math.isfinite(answer):
        raise ProtocolAbort("nonfinite mixed corner partial")
    return answer


def real_fourier_coefficients(
    z: float,
    kappa: float,
    chronological_common_variance: float,
    uniform_torus: float,
    max_frequency: int = MAX_FREQUENCY,
) -> np.ndarray:
    if max_frequency != MAX_FREQUENCY:
        raise ValueError("the E5 sampler always emits the full N=64 array")
    frequencies = np.arange(1, max_frequency + 1, dtype=np.float64)
    damping = np.exp(
        -2.0 * np.pi**2 * kappa * chronological_common_variance * frequencies**2
    )
    angles = 2.0 * np.pi * frequencies * uniform_torus
    coefficients = np.empty(1 + 2 * max_frequency, dtype=np.float64)
    coefficients[0] = z
    coefficients[1::2] = 2.0 * z * damping * np.cos(angles)
    coefficients[2::2] = 2.0 * z * damping * np.sin(angles)
    if np.any(~np.isfinite(coefficients)):
        raise OutputFiniteError("nonfinite N=64 coefficient array", coefficients)
    return coefficients


def nested_prefix(coefficients: np.ndarray, cutoff: int) -> np.ndarray:
    if cutoff not in PREFIX_LENGTHS:
        raise ValueError("unsupported frozen cutoff")
    if coefficients.shape != (COEFFICIENT_COUNT,):
        raise ValueError("full coefficient array has wrong shape")
    return coefficients[: PREFIX_LENGTHS[cutoff]]


def h2_norm_squared(coefficients: np.ndarray) -> float:
    if coefficients.ndim != 1 or coefficients.size % 2 != 1:
        raise ValueError("real Fourier coefficient layout has odd length")
    cutoff = (coefficients.size - 1) // 2
    frequencies = np.arange(1, cutoff + 1, dtype=np.float64)
    cosines = coefficients[1::2]
    sines = coefficients[2::2]
    answer = float(
        coefficients[0] ** 2
        + 0.5 * np.sum((1.0 + frequencies**2) ** 2 * (cosines**2 + sines**2))
    )
    if not math.isfinite(answer):
        raise ProtocolAbort("nonfinite H2 norm")
    return answer


def sample_given_tree(
    spec: SamplerSpec,
    tree: ClockTree,
    rng: np.random.Generator,
    ledger: BudgetLedger,
    phase: str,
    identifier: dict[str, Any],
    known_evaluator: Callable[[float], float],
    opaque_v: OpaqueEvaluator,
) -> SampleResult:
    """Prepare and sample one fixed tree after its segments were accounted."""

    spec.validate()
    total_start = time.perf_counter()
    gaussian_start = time.perf_counter()
    draw_charges = {"gaussian_draws": tree.segment_count, "uniform_draws": 1}
    if tree.leaf_count >= spec.derivative_order:
        draw_charges["tuple_draw_calls"] = 1
        draw_charges["tuple_indices_drawn"] = spec.derivative_order
    ledger.charge_work_batch(draw_charges, identifier)
    prepared = prepare_gaussian(tree, spec.kappa, rng, ledger, identifier)
    gaussian_seconds = time.perf_counter() - gaussian_start

    uniform_torus = float(rng.random())
    if not (0.0 <= uniform_torus < 1.0):
        raise ProtocolAbort("uniform torus draw outside [0,1)")

    if tree.leaf_count < spec.derivative_order:
        coefficients = np.zeros(COEFFICIENT_COUNT, dtype=np.float64)
        total_seconds = time.perf_counter() - total_start
        return SampleResult(
            coefficients,
            {
                "schema_version": SCHEMA_VERSION,
                "identifier": identifier,
                "segment_count": tree.segment_count,
                "leaf_count": tree.leaf_count,
                "internal_count": tree.internal_count,
                "gaussian_draw_count": tree.segment_count,
                "zero_length_segment_count": sum(node.length == 0.0 for node in tree.nodes),
                "chronological_common_variance": prepared.chronological_common_variance,
                "damping_variance": prepared.damping_variance,
                "uniform_torus": uniform_torus,
                "ordered_tuple": None,
                "no_tuple_reason": "leaf_count_below_derivative_order",
                "falling_factorial": 0,
                "mixed_partial": None,
                "z": 0.0,
                "known_evaluator_calls": 0,
                "opaque_calls": 0,
                "timers_seconds": {
                    "gaussian_preparation": gaussian_seconds,
                    "known_and_corner": 0.0,
                    "acquisition": 0.0,
                    "output": 0.0,
                    "prefix_extraction": 0.0,
                    "sample_after_tree": total_seconds,
                },
                "coefficient_layout": COEFFICIENT_LAYOUT,
            },
        )

    selected = np.asarray(
        rng.choice(
            tree.leaf_count,
            size=(spec.derivative_order,),
            replace=False,
            shuffle=True,
        ),
        dtype=np.int64,
    )
    if selected.shape != (spec.derivative_order,) or len(set(map(int, selected))) != len(selected):
        raise ProtocolAbort("ordered tuple draw is not distinct with the frozen shape")

    positions = np.mod(uniform_torus + prepared.residuals, 1.0)
    known_start = time.perf_counter()
    # Reserve the whole deterministic known-evaluation pass before callback
    # entry. A failure conservatively retains unused scheduled work; opaque
    # acquisitions below are instead charged one by one exactly before entry.
    known_keys = {float(x).hex() for x in positions}
    ledger.charge_work("known_evaluator_calls", len(known_keys), identifier)
    known_cache = KnownEvaluatorCache(known_evaluator)
    base_values = np.asarray([known_cache(float(x)) for x in positions], dtype=np.float64)
    mixed_partial = corner_mixed_partial(tree, base_values, selected)
    known_seconds = time.perf_counter() - known_start

    acquisition_start = time.perf_counter()
    query_points: list[float] = []
    query_values: list[float] = []
    direction_product = 1.0
    for leaf_id in selected:
        point = float(positions[int(leaf_id)])
        value = float(opaque_v(point))
        if not math.isfinite(value):
            raise ProtocolAbort("opaque evaluator returned a nonfinite value after being charged")
        known_value = known_cache(point)
        # A cache miss here is possible only if external code changed positions;
        # retain exact work accounting rather than assuming it cannot happen.
        query_points.append(point)
        query_values.append(value)
        direction_product *= value - known_value
    acquisition_seconds = time.perf_counter() - acquisition_start

    ordered_weight = falling_factorial(tree.leaf_count, spec.derivative_order)
    z = float(ordered_weight) * mixed_partial * direction_product
    if not math.isfinite(z):
        raise ProtocolAbort("nonfinite scalar sample z")
    output_start = time.perf_counter()
    coefficients = real_fourier_coefficients(
        z,
        spec.kappa,
        prepared.chronological_common_variance,
        uniform_torus,
    )
    output_seconds = time.perf_counter() - output_start
    prefix_start = time.perf_counter()
    prefixes = {cutoff: nested_prefix(coefficients, cutoff).copy() for cutoff in (4, 16, 64)}
    prefix_seconds = time.perf_counter() - prefix_start
    if not (
        np.array_equal(prefixes[4], coefficients[:9])
        and np.array_equal(prefixes[16], coefficients[:33])
        and np.array_equal(prefixes[64], coefficients)
    ):
        raise ProtocolAbort("nested prefix identity failed")
    total_seconds = time.perf_counter() - total_start
    return SampleResult(
        coefficients,
        {
            "schema_version": SCHEMA_VERSION,
            "identifier": identifier,
            "segment_count": tree.segment_count,
            "leaf_count": tree.leaf_count,
            "internal_count": tree.internal_count,
            "gaussian_draw_count": tree.segment_count,
            "zero_length_segment_count": sum(node.length == 0.0 for node in tree.nodes),
            "chronological_common_variance": prepared.chronological_common_variance,
            "damping_variance": prepared.damping_variance,
            "uniform_torus": uniform_torus,
            "ordered_tuple": [int(x) for x in selected],
            "no_tuple_reason": None,
            "falling_factorial": ordered_weight,
            "mixed_partial": mixed_partial,
            "z": z,
            "known_evaluator_calls": known_cache.calls,
            "opaque_calls": len(query_points),
            "query_points_hex": [x.hex() for x in query_points],
            "query_values_hex": [x.hex() for x in query_values],
            "timers_seconds": {
                "gaussian_preparation": gaussian_seconds,
                "known_and_corner": known_seconds,
                "acquisition": acquisition_seconds,
                "output": output_seconds,
                "prefix_extraction": prefix_seconds,
                "sample_after_tree": total_seconds,
            },
            "coefficient_layout": COEFFICIENT_LAYOUT,
        },
        query_points,
        query_values,
    )


def sample_field(
    spec: SamplerSpec,
    rng: np.random.Generator,
    ledger: BudgetLedger,
    phase: str,
    identifier: dict[str, Any],
    known_evaluator: Callable[[float], float],
    opaque_v: OpaqueEvaluator,
) -> SampleResult:
    """Generate a complete tree before any opaque acquisition and sample it."""
    spec.validate()
    tree_start = time.perf_counter()
    tree = generate_clock_tree(spec, rng, ledger, phase, identifier)
    tree_seconds = time.perf_counter() - tree_start
    result = sample_given_tree(
        spec,
        tree,
        rng,
        ledger,
        phase,
        identifier,
        known_evaluator,
        opaque_v,
    )
    result.metadata["timers_seconds"]["tree_generation"] = tree_seconds
    result.metadata["timers_seconds"]["sample_including_tree"] = (
        tree_seconds + result.metadata["timers_seconds"]["sample_after_tree"]
    )
    timers = result.metadata["timers_seconds"]
    if any((not math.isfinite(float(value)) or float(value) < 0.0) for value in timers.values()):
        raise ProtocolAbort("invalid timer value")
    return result
