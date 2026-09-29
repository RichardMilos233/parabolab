"""Independent deterministic fixtures required by frozen E5 protocol 02h."""

from __future__ import annotations

from dataclasses import asdict
import math
from typing import Any, Iterable

import numpy as np

from budget import BudgetLedger
from smooth_field import (
    ClockTree,
    Node,
    ProtocolAbort,
    SamplerSpec,
    corner_mixed_partial,
    falling_factorial,
    h2_norm_squared,
    parent_value,
    prepare_gaussian,
    real_fourier_coefficients,
    sample_given_tree,
    validate_tree,
)


COVARIANCE_RTOL = 5e-12
COVARIANCE_ATOL = 5e-13
PARTIAL_RTOL = 2e-13
PARTIAL_ATOL = 2e-14
EXACT_RTOL = 2e-14
EXACT_ATOL = 2e-14


def one_leaf_tree(branching: int, rate: float, tau: float) -> ClockTree:
    tree = ClockTree(branching, rate, tau, [Node(0, None, [], 0.0, tau, tau, 0)], [0])
    validate_tree(tree)
    return tree


def star_tree(branching: int, rate: float, tau: float, ancestral_length: float) -> ClockTree:
    if not 0.0 <= ancestral_length <= tau:
        raise ValueError("invalid star ancestral length")
    nodes = [Node(0, None, list(range(1, branching + 1)), 0.0, ancestral_length, ancestral_length)]
    terminal_length = tau - ancestral_length
    leaves: list[int] = []
    for child in range(branching):
        index = child + 1
        nodes.append(Node(index, 0, [], ancestral_length, tau, terminal_length, child))
        leaves.append(index)
    tree = ClockTree(branching, rate, tau, nodes, leaves)
    validate_tree(tree)
    return tree


def unbalanced_tree(
    branching: int,
    rate: float,
    tau: float,
    root_length: float,
    split_child_length: float,
) -> ClockTree:
    terminal_from_root = tau - root_length
    if not (0.0 <= split_child_length < terminal_from_root):
        raise ValueError("unbalanced fixture requires 0 <= c < tau-b0")
    nodes: list[Node] = []
    root = Node(0, None, [], 0.0, root_length, root_length)
    nodes.append(root)
    # Child zero is the unique internal child.
    internal_index = 1
    nodes.append(
        Node(
            internal_index,
            0,
            [],
            root_length,
            root_length + split_child_length,
            split_child_length,
        )
    )
    root.children.append(internal_index)
    next_index = 2
    leaf_nodes: list[int] = []
    for _ in range(branching):
        index = next_index
        next_index += 1
        start = root_length + split_child_length
        nodes.append(Node(index, internal_index, [], start, tau, tau - start))
        nodes[internal_index].children.append(index)
        leaf_nodes.append(index)
    for _ in range(branching - 1):
        index = next_index
        next_index += 1
        nodes.append(Node(index, 0, [], root_length, tau, terminal_from_root))
        root.children.append(index)
        leaf_nodes.append(index)
    for leaf_id, index in enumerate(leaf_nodes):
        nodes[index].leaf_id = leaf_id
    tree = ClockTree(branching, rate, tau, nodes, leaf_nodes)
    validate_tree(tree)
    return tree


def account_manual_tree(
    ledger: BudgetLedger, tree: ClockTree, label: str, *, phase: str = "preflight"
) -> None:
    identifier = {"fixture": label}
    reservation = ledger.begin_segment_reservation(phase, identifier)
    state = ledger.snapshot()
    reserved = int(state["active_segment_reservations"][reservation.reservation_id]["reserved"])
    while reserved < tree.segment_count:
        reserved += ledger.extend_segment_reservation(reservation)
    ledger.commit_segment_reservation(reservation, tree.segment_count, status="fixture_complete")


def chronological_recursion(tree: ClockTree) -> tuple[np.ndarray, list[np.ndarray | None]]:
    effective = np.empty(tree.segment_count, dtype=np.float64)
    alphas: list[np.ndarray | None] = [None] * tree.segment_count
    for node in reversed(tree.nodes):
        if not node.children:
            effective[node.index] = node.length
            continue
        child_a = np.asarray([effective[c] for c in node.children], dtype=np.float64)
        zeros = np.flatnonzero(child_a == 0.0)
        if zeros.size:
            harmonic = 0.0
            alpha = np.zeros(len(node.children), dtype=np.float64)
            alpha[int(zeros[0])] = 1.0
        else:
            minimum = float(np.min(child_a))
            harmonic = minimum / math.fsum(minimum / float(value) for value in child_a)
            alpha = harmonic / child_a
        effective[node.index] = node.length + harmonic
        alphas[node.index] = alpha
    return effective, alphas


def independent_leaf_path_matrix(tree: ClockTree) -> np.ndarray:
    matrix = np.zeros((tree.leaf_count, tree.segment_count), dtype=np.float64)
    for leaf_id, node_index in enumerate(tree.leaf_nodes):
        cursor: int | None = node_index
        while cursor is not None:
            matrix[leaf_id, cursor] = 1.0
            cursor = tree.nodes[cursor].parent
    return matrix


def independent_dense_covariance(tree: ClockTree) -> tuple[np.ndarray, np.ndarray]:
    paths = independent_leaf_path_matrix(tree)
    lengths = np.asarray([node.length for node in tree.nodes], dtype=np.float64)
    return (paths * lengths) @ paths.T, paths


def leaf_weights_from_child_alphas(tree: ClockTree, alphas: list[np.ndarray | None]) -> np.ndarray:
    incoming = np.zeros(tree.segment_count, dtype=np.float64)
    incoming[0] = 1.0
    weights = np.zeros(tree.leaf_count, dtype=np.float64)
    for node in tree.nodes:
        if node.leaf_id is not None:
            weights[node.leaf_id] = incoming[node.index]
        else:
            alpha = alphas[node.index]
            assert alpha is not None
            for position, child in enumerate(node.children):
                incoming[child] = incoming[node.index] * alpha[position]
    return weights


def edge_coefficient_residual_covariance(
    tree: ClockTree, weights: np.ndarray, kappa: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    paths = independent_leaf_path_matrix(tree)
    common_edge_coefficients = weights @ paths
    residual_coefficients = paths - common_edge_coefficients[None, :]
    lengths = np.asarray([node.length for node in tree.nodes], dtype=np.float64)
    covariance = kappa * ((residual_coefficients * lengths) @ residual_coefficients.T)
    return covariance, residual_coefficients, common_edge_coefficients


def local_parent_partial(branching: int, child_values: np.ndarray, active: set[int]) -> float:
    if not active:
        return parent_value(branching, child_values)
    complement_product = 1.0
    for index, value in enumerate(child_values):
        if index not in active:
            complement_product *= float(value)
    if branching == 3:
        return (0.5 if len(active) == 1 else 0.0) - 0.5 * complement_product
    if branching == 5:
        return (6.0 / 25.0 if len(active) == 1 else 0.0) - 0.2 * complement_product
    raise ValueError("unsupported parent")


def recursive_mixed_partial(
    tree: ClockTree, base_leaf_values: np.ndarray, selected_leaf_ids: Iterable[int]
) -> float:
    selected = set(int(i) for i in selected_leaf_ids)
    descendant_leaves: list[set[int]] = [set() for _ in tree.nodes]
    values = np.empty(tree.segment_count, dtype=np.float64)
    for node in reversed(tree.nodes):
        if node.leaf_id is not None:
            descendant_leaves[node.index] = {node.leaf_id}
            values[node.index] = base_leaf_values[node.leaf_id]
        else:
            descendant_leaves[node.index] = set().union(
                *(descendant_leaves[child] for child in node.children)
            )
            values[node.index] = parent_value(
                tree.branching,
                np.asarray([values[child] for child in node.children], dtype=np.float64),
            )

    def derivative(node_index: int, subset: set[int]) -> float:
        node = tree.nodes[node_index]
        if not subset:
            return float(values[node_index])
        if node.leaf_id is not None:
            return 1.0 if subset == {node.leaf_id} else 0.0
        child_subsets = [subset & descendant_leaves[child] for child in node.children]
        active = {position for position, child_set in enumerate(child_subsets) if child_set}
        local = local_parent_partial(
            tree.branching,
            np.asarray([values[child] for child in node.children], dtype=np.float64),
            active,
        )
        factors = [
            derivative(node.children[position], child_subsets[position]) for position in sorted(active)
        ]
        return local * math.prod(factors)

    return derivative(0, selected)


def _allclose(left: np.ndarray, right: np.ndarray) -> bool:
    return bool(np.allclose(left, right, rtol=COVARIANCE_RTOL, atol=COVARIANCE_ATOL))


def covariance_fixture_record(
    tree: ClockTree,
    kappa: float,
    label: str,
    prepared,
) -> dict[str, Any]:
    effective, alphas = chronological_recursion(tree)
    common = float(effective[0])
    weights = leaf_weights_from_child_alphas(tree, alphas)
    dense, paths = independent_dense_covariance(tree)
    residual_covariance, residual_coefficients, common_edge_coefficients = (
        edge_coefficient_residual_covariance(tree, weights, kappa)
    )
    target_residual = kappa * (
        dense - common * np.ones((tree.leaf_count, tree.leaf_count), dtype=np.float64)
    )
    edge_values = np.linspace(-0.7, 0.9, tree.segment_count, dtype=np.float64)
    leaf_values = paths @ edge_values
    aggregate_from_edges = float(common_edge_coefficients @ edge_values)
    aggregate_from_leaves = float(weights @ leaf_values)
    residual_values = residual_coefficients @ edge_values
    reconstruction = leaf_values - aggregate_from_edges
    actual_aggregate_from_edges = float(common_edge_coefficients @ prepared.edge_gaussians)
    actual_residuals_from_edges = residual_coefficients @ prepared.edge_gaussians
    checks = {
        "weights_nonnegative": bool(np.all(weights >= -COVARIANCE_ATOL)),
        "weights_sum_one": math.isclose(
            float(np.sum(weights)), 1.0, rel_tol=EXACT_RTOL, abs_tol=EXACT_ATOL
        ),
        "Cw_equals_a_one": _allclose(dense @ weights, common * np.ones(tree.leaf_count)),
        "a_lower_upper": (
            common >= tree.tau / tree.leaf_count - COVARIANCE_ATOL
            and common <= tree.tau + COVARIANCE_ATOL
        ),
        "residual_covariance_edge_map": _allclose(residual_covariance, target_residual),
        "actual_aggregate_edge_leaf_match": math.isclose(
            aggregate_from_edges,
            aggregate_from_leaves,
            rel_tol=COVARIANCE_RTOL,
            abs_tol=COVARIANCE_ATOL,
        ),
        "actual_residual_reconstruction": _allclose(residual_values, reconstruction),
        "sampled_common_variance_matches_recursion": math.isclose(
            prepared.chronological_common_variance,
            common,
            rel_tol=EXACT_RTOL,
            abs_tol=EXACT_ATOL,
        ),
        "sampled_actual_aggregate_matches_edge_map": math.isclose(
            prepared.aggregate,
            actual_aggregate_from_edges,
            rel_tol=COVARIANCE_RTOL,
            abs_tol=COVARIANCE_ATOL,
        ),
        "sampled_actual_residuals_match_edge_map": _allclose(
            prepared.residuals, actual_residuals_from_edges
        ),
        "zero_length_edges_are_exact_zero": bool(
            np.all(
                prepared.edge_gaussians[
                    np.asarray([node.length == 0.0 for node in tree.nodes], dtype=bool)
                ]
                == 0.0
            )
        ),
        "residual_covariance_symmetric": _allclose(residual_covariance, residual_covariance.T),
    }
    if not all(checks.values()):
        raise ProtocolAbort(f"covariance fixture {label} failed: {checks}")
    return {
        "label": label,
        "branching": tree.branching,
        "segment_count": tree.segment_count,
        "leaf_count": tree.leaf_count,
        "chronological_common_variance": common,
        "lower_bound": tree.tau / tree.leaf_count,
        "upper_bound": tree.tau,
        "weights": weights.tolist(),
        "dense_covariance": dense.tolist(),
        "physical_residual_covariance": residual_covariance.tolist(),
        "actual_edge_standard_normals": prepared.edge_standard_normals.tolist(),
        "actual_edge_gaussians": prepared.edge_gaussians.tolist(),
        "actual_common_aggregate": prepared.aggregate,
        "actual_leaf_path_sums": prepared.leaf_path_sums.tolist(),
        "actual_residuals": prepared.residuals.tolist(),
        "checks": checks,
    }


class MustNotCall:
    def __call__(self, x: float) -> float:
        raise AssertionError(f"opaque evaluator was called at {x!r} in n<j fixture")


def run_fixtures(ledger: BudgetLedger) -> dict[str, Any]:
    fixtures = [
        ("one_leaf", one_leaf_tree(3, 2.0, 0.5)),
        ("star_positive", star_tree(3, 2.0, 0.5, 0.2)),
        ("unbalanced", unbalanced_tree(3, 2.0, 0.5, 0.1, 0.15)),
        ("star_zero_terminal", star_tree(3, 2.0, 0.5, 0.5)),
    ]
    covariance_records: list[dict[str, Any]] = []
    for fixture_index, (label, tree) in enumerate(fixtures):
        account_manual_tree(ledger, tree, label)
        fixture_identifier = {
            "fixture": label,
            "rng_seed_sequence": [229, 41, fixture_index, 1],
        }
        ledger.charge_work("gaussian_draws", tree.segment_count, fixture_identifier)
        fixture_rng = np.random.Generator(
            np.random.PCG64DXSM(
                np.random.SeedSequence(fixture_identifier["rng_seed_sequence"])
            )
        )
        prepared = prepare_gaussian(tree, 0.1, fixture_rng, ledger, fixture_identifier)
        covariance_records.append(covariance_fixture_record(tree, 0.1, label, prepared))

    derivative_tree_3 = star_tree(3, 2.0, 0.5, 0.0)
    derivative_tree_5 = star_tree(5, 5.0, 0.1, 0.0)
    account_manual_tree(ledger, derivative_tree_3, "derivative_star_cubic")
    account_manual_tree(ledger, derivative_tree_5, "derivative_star_quintic")
    derivative_checks: list[dict[str, Any]] = []
    derivative_cases = [
        ("cubic_j3", derivative_tree_3, 0.0, (0, 1, 2), -0.5, -3.0),
        ("cubic_j2", derivative_tree_3, 0.25, (0, 1), -0.125, -0.75),
        ("quintic_j2", derivative_tree_5, 0.25, (0, 1), -0.003125, -0.0625),
    ]
    for label, tree, base, selected, expected_partial, expected_weighted in derivative_cases:
        base_values = np.full(tree.leaf_count, base, dtype=np.float64)
        corner = corner_mixed_partial(tree, base_values, selected)
        recursive = recursive_mixed_partial(tree, base_values, selected)
        weight = falling_factorial(tree.leaf_count, len(selected))
        weighted = weight * corner
        passed = (
            math.isclose(corner, recursive, rel_tol=PARTIAL_RTOL, abs_tol=PARTIAL_ATOL)
            and math.isclose(corner, expected_partial, rel_tol=PARTIAL_RTOL, abs_tol=PARTIAL_ATOL)
            and math.isclose(weighted, expected_weighted, rel_tol=PARTIAL_RTOL, abs_tol=PARTIAL_ATOL)
        )
        if not passed:
            raise ProtocolAbort(f"derivative fixture {label} failed")
        derivative_checks.append(
            {
                "label": label,
                "selected": list(selected),
                "corner_partial": corner,
                "recursive_partial": recursive,
                "falling_factorial": weight,
                "weighted_derivative": weighted,
                "expected_partial": expected_partial,
                "expected_weighted_derivative": expected_weighted,
                "explicit_no_factorial_division": True,
                "explicit_no_extra_delta_power": True,
                "passed": passed,
            }
        )

    sign_coefficients = real_fourier_coefficients(1.0, 0.1, 0.2, 0.25)
    expected_sine = 2.0 * math.exp(-2.0 * math.pi**2 * 0.1 * 0.2)
    sine_check = {
        "uniform_torus": 0.25,
        "z": 1.0,
        "sine_mode_1": float(sign_coefficients[2]),
        "expected_positive_sine_mode_1": expected_sine,
        "cosine_mode_1": float(sign_coefficients[1]),
        "passed": (
            sign_coefficients[2] > 0.0
            and math.isclose(
                float(sign_coefficients[2]), expected_sine, rel_tol=EXACT_RTOL, abs_tol=EXACT_ATOL
            )
            and abs(float(sign_coefficients[1])) <= 5e-16
        ),
    }
    if not sine_check["passed"]:
        raise ProtocolAbort("positive Fourier sine-sign fixture failed")

    nlt_tree = one_leaf_tree(3, 2.0, 0.5)
    account_manual_tree(ledger, nlt_tree, "n_less_than_j")
    nlt_identifier = {"fixture": "n_less_than_j", "rng_seed_sequence": [229, 99, 0, 1]}
    nlt_rng = np.random.Generator(np.random.PCG64DXSM(np.random.SeedSequence([229, 99, 0, 1])))
    nlt_result = sample_given_tree(
        SamplerSpec(3, 2.0, 0.5, 0.1, 2),
        nlt_tree,
        nlt_rng,
        ledger,
        "preflight",
        nlt_identifier,
        lambda x: 0.0,
        MustNotCall(),
    )
    nlt_check = {
        "leaf_count": 1,
        "derivative_order": 2,
        "opaque_calls": nlt_result.metadata["opaque_calls"],
        "array_is_exact_zero": bool(np.array_equal(nlt_result.coefficients, np.zeros(129))),
        "full_array_shape": list(nlt_result.coefficients.shape),
        "passed": (
            nlt_result.metadata["opaque_calls"] == 0
            and np.array_equal(nlt_result.coefficients, np.zeros(129))
        ),
    }
    if not nlt_check["passed"]:
        raise ProtocolAbort("n<j zero/no-query fixture failed")

    h2_constant = h2_norm_squared(np.asarray([2.0], dtype=np.float64))
    h2_cosine = h2_norm_squared(np.asarray([0.0, 3.0, 0.0], dtype=np.float64))
    h2_check = {
        "constant_example": h2_constant,
        "constant_expected": 4.0,
        "cosine_example": h2_cosine,
        "cosine_expected": 18.0,
        "passed": math.isclose(h2_constant, 4.0) and math.isclose(h2_cosine, 18.0),
    }
    if not h2_check["passed"]:
        raise ProtocolAbort("H2 normalization fixture failed")

    return {
        "tolerances": {
            "covariance_rtol": COVARIANCE_RTOL,
            "covariance_atol": COVARIANCE_ATOL,
            "partial_rtol": PARTIAL_RTOL,
            "partial_atol": PARTIAL_ATOL,
            "exact_rtol": EXACT_RTOL,
            "exact_atol": EXACT_ATOL,
        },
        "covariance_fixtures": covariance_records,
        "derivative_fixtures": derivative_checks,
        "fourier_sign_fixture": sine_check,
        "n_less_than_j_fixture": nlt_check,
        "h2_fixture": h2_check,
        "all_passed": True,
    }
