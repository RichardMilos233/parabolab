"""Vectorized complete-tree samplers for the slab continuation experiment.

The raw sampler uses the six normalized Allen--Cahn codes, ordered as
``(Id, Dx, F0, F1, F2, F3)``, at the fixed exponential rate two.  It keeps
the original uniform two-label law for every ``Fk`` branch.  A selected
tuple containing ``F4`` or above is known to be zero and is short-circuited
only after its label has been drawn.

Both samplers construct every started tree without depth/node cutoffs,
clipping, rejection, or output-dependent sample counts.  Children of one
branch share their parent's Brownian death position.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np

__all__ = [
    "CODE_NAMES",
    "DX",
    "F0",
    "F1",
    "F2",
    "F3",
    "ID",
    "SlabSamples",
    "majority_sample",
    "raw_sample",
]


ID, DX, F0, F1, F2, F3 = range(6)
CODE_NAMES = ("Id", "Dx", "F0", "F1", "F2", "F3")
_RATE = 2.0
_MAX_RAW_H = 2.0 / 25.0


@dataclass(frozen=True)
class SlabSamples:
    """Per-root samples and complete-tree cost diagnostics.

    ``terminal_counts`` is the aggregate number of evaluated leaves in the
    fixed code order ``(Id, Dx, F0, F1, F2, F3)``.  Majority leaves are
    counted in the ``Id`` coordinate.
    """

    values: np.ndarray
    node_counts: np.ndarray
    root_branched: np.ndarray
    terminal_counts: np.ndarray


def _positions_array(positions) -> np.ndarray:
    out = np.asarray(positions, dtype=float)
    if out.ndim != 1:
        raise ValueError("positions must be a one-dimensional array")
    if not np.all(np.isfinite(out)):
        raise ValueError("positions must be finite")
    return out


def _horizon(h: float, *, local: bool) -> float:
    try:
        out = float(h)
    except (TypeError, ValueError) as exc:
        raise ValueError("h must be finite and nonnegative") from exc
    if not math.isfinite(out) or out < 0.0:
        raise ValueError("h must be finite and nonnegative")
    if local and out > _MAX_RAW_H:
        raise ValueError("raw slab horizon h must satisfy h <= 2/25")
    return out


def _root_code(code: int) -> int:
    if isinstance(code, (bool, np.bool_)) or not isinstance(
        code, (int, np.integer)
    ):
        raise TypeError("root_code must be an integer in 0, ..., 5")
    out = int(code)
    if out < ID or out > F3:
        raise ValueError("root_code must be an integer in 0, ..., 5")
    return out


def _draw_exponentials(rng, size: int) -> np.ndarray:
    out = np.asarray(rng.exponential(scale=0.5, size=size), dtype=float)
    if out.shape != (size,) or not np.all(np.isfinite(out)) or np.any(out < 0.0):
        raise ValueError("rng.exponential must return finite nonnegative draws")
    return out


def _draw_normals(rng, size: int) -> np.ndarray:
    out = np.asarray(rng.normal(size=size), dtype=float)
    if out.shape != (size,) or not np.all(np.isfinite(out)):
        raise ValueError("rng.normal must return finite draws")
    return out


def _draw_labels(rng, size: int) -> np.ndarray:
    out = np.asarray(rng.integers(2, size=size), dtype=np.int8)
    if out.shape != (size,) or np.any((out != 0) & (out != 1)):
        raise ValueError("rng.integers must return binary labels")
    return out


def _terminal_pair(terminal, positions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    try:
        pair = terminal(positions)
        g, gp = pair
    except (TypeError, ValueError) as exc:
        raise ValueError("terminal(x) must return the pair (g, gprime)") from exc
    g = np.asarray(g, dtype=float)
    gp = np.asarray(gp, dtype=float)
    try:
        g = np.broadcast_to(g, positions.shape)
        gp = np.broadcast_to(gp, positions.shape)
    except ValueError as exc:
        raise ValueError("terminal values must match the positions shape") from exc
    if not np.all(np.isfinite(g)) or not np.all(np.isfinite(gp)):
        raise ValueError("terminal values must be finite")
    return g, gp


def _raw_terminal_values(codes: np.ndarray, g: np.ndarray, gp: np.ndarray) -> np.ndarray:
    """Evaluate the six normalized terminal polynomials independently."""
    out = np.empty(codes.size, dtype=float)
    masks = [codes == k for k in range(6)]
    out[masks[ID]] = g[masks[ID]]
    out[masks[DX]] = gp[masks[DX]]
    out[masks[F0]] = g[masks[F0]] - g[masks[F0]] ** 3
    out[masks[F1]] = 1.0 - 3.0 * g[masks[F1]] ** 2
    out[masks[F2]] = -6.0 * g[masks[F2]]
    out[masks[F3]] = -6.0
    if not np.all(np.isfinite(out)):
        raise ValueError("normalized terminal code values must be finite")
    return out


def raw_sample(
    positions,
    h: float,
    terminal: Callable,
    rng,
    root_code: int = ID,
) -> SlabSamples:
    """Sample complete local raw coding trees at all root ``positions``.

    Parameters
    ----------
    positions:
        One-dimensional finite root positions.  Output arrays preserve this
        order and contain one record for every root.
    h:
        Local slab horizon, constrained to the certified range ``[0, 2/25]``.
    terminal:
        Vectorized callback ``terminal(x) -> (g(x), g'(x))``.  The C4
        certificate requires the global contract ``|g| <= 2/5`` and
        ``|g'| <= 1/2``.  This sampler checks finiteness of evaluated values
        but cannot certify those global bounds from finitely many leaves.
    rng:
        NumPy-compatible random generator.
    root_code:
        Integer code in the fixed order ``(Id, Dx, F0, F1, F2, F3)``.
    """
    roots = _positions_array(positions)
    h = _horizon(h, local=True)
    root_code = _root_code(root_code)
    if not callable(terminal):
        raise TypeError("terminal must be callable")

    n_roots = roots.size
    if n_roots == 0:
        return SlabSamples(
            np.empty(0, dtype=float),
            np.empty(0, dtype=np.int64),
            np.empty(0, dtype=bool),
            np.zeros(6, dtype=np.int64),
        )

    times = np.zeros(n_roots, dtype=float)
    particle_positions = roots.copy()
    codes = np.full(n_roots, root_code, dtype=np.int8)
    root_ids = np.arange(n_roots, dtype=np.int64)
    node_counts = np.zeros(n_roots, dtype=np.int64)
    terminal_counts = np.zeros(6, dtype=np.int64)
    root_branched = np.empty(n_roots, dtype=bool)
    frames = []
    first_generation = True

    while True:
        node_counts += np.bincount(root_ids, minlength=n_roots)
        remaining = h - times
        lifetimes = _draw_exponentials(rng, times.size)
        branched = lifetimes < remaining
        if first_generation:
            root_branched[:] = branched
            first_generation = False

        f_branch = branched & (codes >= F0)
        labels = np.full(times.size, -1, dtype=np.int8)
        if np.any(f_branch):
            labels[f_branch] = _draw_labels(rng, int(np.count_nonzero(f_branch)))

        # These are selected raw labels whose tuple contains F4 or above.
        # They return zero now, without renormalizing the label probability.
        structural_zero = f_branch & (
            ((labels == 0) & (codes == F3))
            | ((labels == 1) & (codes >= F2))
        )
        live_branch = branched & ~structural_zero
        leaf = ~branched

        death_positions = particle_positions.copy()
        durations = np.where(leaf, remaining, lifetimes)
        moved = (leaf | live_branch) & (durations > 0.0)
        if np.any(moved):
            death_positions[moved] += np.sqrt(durations[moved]) * _draw_normals(
                rng, int(np.count_nonzero(moved))
            )
        if not np.all(np.isfinite(death_positions[leaf | live_branch])):
            raise ValueError("Brownian death positions must be finite")

        values = np.zeros(times.size, dtype=float)
        if np.any(leaf):
            leaf_codes = codes[leaf]
            g, gp = _terminal_pair(terminal, death_positions[leaf])
            values[leaf] = np.exp(_RATE * remaining[leaf]) * _raw_terminal_values(
                leaf_codes, g, gp
            )
            terminal_counts += np.bincount(leaf_codes, minlength=6)

        live_parent_idx = np.flatnonzero(live_branch)
        if live_parent_idx.size == 0:
            frames.append((values, live_parent_idx, None, None))
            break

        parent_codes = codes[live_parent_idx]
        parent_labels = labels[live_parent_idx]
        counts = np.where(
            parent_codes == ID,
            1,
            np.where((parent_codes == DX) | (parent_labels == 0), 2, 3),
        ).astype(np.int8)
        weights = np.empty(live_parent_idx.size, dtype=float)
        taus = lifetimes[live_parent_idx]
        one_tuple = parent_codes <= DX
        positive = parent_codes >= F0
        weights[one_tuple] = np.exp(_RATE * taus[one_tuple]) / _RATE
        weights[positive & (parent_labels == 0)] = np.exp(
            _RATE * taus[positive & (parent_labels == 0)]
        )
        weights[positive & (parent_labels == 1)] = -np.exp(
            _RATE * taus[positive & (parent_labels == 1)]
        ) / 2.0

        starts = np.empty(live_parent_idx.size, dtype=np.int64)
        starts[0] = 0
        if starts.size > 1:
            np.cumsum(counts[:-1], out=starts[1:])
        child_size = int(counts.sum())
        child_codes = np.empty(child_size, dtype=np.int8)

        id_parent = parent_codes == ID
        idx = starts[id_parent]
        child_codes[idx] = F0

        dx_parent = parent_codes == DX
        idx = starts[dx_parent]
        child_codes[idx] = F1
        child_codes[idx + 1] = DX

        label_zero = positive & (parent_labels == 0)
        idx = starts[label_zero]
        child_codes[idx] = F0
        child_codes[idx + 1] = parent_codes[label_zero] + 1

        label_one = positive & (parent_labels == 1)
        idx = starts[label_one]
        child_codes[idx] = DX
        child_codes[idx + 1] = DX
        child_codes[idx + 2] = parent_codes[label_one] + 2

        frames.append((values, live_parent_idx, counts, weights))
        child_times = times[live_parent_idx] + taus
        times = np.repeat(child_times, counts)
        particle_positions = np.repeat(death_positions[live_parent_idx], counts)
        root_ids = np.repeat(root_ids[live_parent_idx], counts)
        codes = child_codes

    child_values = None
    for values, live_parent_idx, counts, weights in reversed(frames):
        if live_parent_idx.size:
            starts = np.empty(live_parent_idx.size, dtype=np.int64)
            starts[0] = 0
            if starts.size > 1:
                np.cumsum(counts[:-1], out=starts[1:])
            products = np.multiply.reduceat(child_values, starts)
            values[live_parent_idx] = weights * products
        child_values = values

    if not np.all(np.isfinite(child_values)):
        raise ValueError("raw tree values must be finite")
    return SlabSamples(child_values, node_counts, root_branched, terminal_counts)


def _phi_values(phi, positions: np.ndarray) -> np.ndarray:
    values = np.asarray(phi(positions), dtype=float)
    try:
        values = np.broadcast_to(values, positions.shape)
    except ValueError as exc:
        raise ValueError("phi values must match the positions shape") from exc
    if not np.all(np.isfinite(values)):
        raise ValueError("phi must return finite values in [-1, 1]")
    if np.any(values < -1.0) or np.any(values > 1.0):
        raise ValueError("phi must return values in [-1, 1]")
    return values


def _majority_batch(positions: np.ndarray, h: float, phi, rng) -> SlabSamples:
    n_roots = positions.size
    times = np.zeros(n_roots, dtype=float)
    particle_positions = positions.copy()
    root_ids = np.arange(n_roots, dtype=np.int64)
    node_counts = np.zeros(n_roots, dtype=np.int64)
    terminal_counts = np.zeros(6, dtype=np.int64)
    frames = []
    root_branched = None

    while True:
        node_counts += np.bincount(root_ids, minlength=n_roots)
        remaining = h - times
        lifetimes = _draw_exponentials(rng, times.size)
        branched = lifetimes < remaining
        if root_branched is None:
            root_branched = branched.copy()

        durations = np.where(branched, lifetimes, remaining)
        death_positions = particle_positions.copy()
        moved = durations > 0.0
        if np.any(moved):
            death_positions[moved] += np.sqrt(durations[moved]) * _draw_normals(
                rng, int(np.count_nonzero(moved))
            )
        if not np.all(np.isfinite(death_positions)):
            raise ValueError("Brownian death positions must be finite")

        values = np.empty(times.size, dtype=float)
        leaf = ~branched
        if np.any(leaf):
            values[leaf] = _phi_values(phi, death_positions[leaf])
            terminal_counts[ID] += np.count_nonzero(leaf)
        frames.append((branched, values))
        if not np.any(branched):
            break

        parent_times = times[branched] + lifetimes[branched]
        times = np.repeat(parent_times, 3)
        particle_positions = np.repeat(death_positions[branched], 3)
        root_ids = np.repeat(root_ids[branched], 3)

    child_values = None
    for branched, values in reversed(frames):
        if child_values is not None:
            triples = child_values.reshape(-1, 3)
            a, b, c = triples[:, 0], triples[:, 1], triples[:, 2]
            values[branched] = (a + b + c - a * b * c) / 2.0
        child_values = values

    if not np.all(np.isfinite(child_values)):
        raise ValueError("majority tree values must be finite")
    return SlabSamples(child_values, node_counts, root_branched, terminal_counts)


def _majority_batch_size(n_roots: int, h: float) -> int:
    """Choose a memory batch; this never truncates an individual tree."""
    target_expected_nodes = 500_000.0
    threshold = math.log((2.0 * target_expected_nodes + 1.0) / 3.0)
    if 4.0 * h >= threshold:
        return 1
    expected_nodes = (3.0 * math.exp(4.0 * h) - 1.0) / 2.0
    return max(1, min(n_roots, int(target_expected_nodes / expected_nodes)))


def majority_sample(positions, h: float, phi: Callable, rng) -> SlabSamples:
    """Sample complete rate-two ternary majority trees at all positions."""
    roots = _positions_array(positions)
    h = _horizon(h, local=False)
    if not callable(phi):
        raise TypeError("phi must be callable")
    n_roots = roots.size
    if n_roots == 0:
        return SlabSamples(
            np.empty(0, dtype=float),
            np.empty(0, dtype=np.int64),
            np.empty(0, dtype=bool),
            np.zeros(6, dtype=np.int64),
        )

    values = np.empty(n_roots, dtype=float)
    node_counts = np.empty(n_roots, dtype=np.int64)
    root_branched = np.empty(n_roots, dtype=bool)
    terminal_counts = np.zeros(6, dtype=np.int64)
    batch_size = _majority_batch_size(n_roots, h)
    for lo in range(0, n_roots, batch_size):
        hi = min(lo + batch_size, n_roots)
        batch = _majority_batch(roots[lo:hi], h, phi, rng)
        values[lo:hi] = batch.values
        node_counts[lo:hi] = batch.node_counts
        root_branched[lo:hi] = batch.root_branched
        terminal_counts += batch.terminal_counts
    return SlabSamples(values, node_counts, root_branched, terminal_counts)
