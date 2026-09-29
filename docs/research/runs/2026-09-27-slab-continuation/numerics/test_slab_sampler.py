from __future__ import annotations

import math

import numpy as np
import pytest

from parabolab.majority import sample_majority
from parabolab.mechanism import Dx, FDeriv, Id
from parabolab.pde import ParabolicPDE
from parabolab.tree import sample_tree

from slab_sampler import DX, F0, F1, F2, F3, ID, majority_sample, raw_sample


class ScriptedRNG:
    def __init__(self, *, exponentials, normals=(), labels=()):
        self.exponentials = [np.asarray(x, dtype=float) for x in exponentials]
        self.normals = [np.asarray(x, dtype=float) for x in normals]
        self.labels = [np.asarray(x, dtype=np.int64) for x in labels]
        self.label_sizes = []

    @staticmethod
    def _take(queue, size, name):
        if not queue:
            raise AssertionError(f"unexpected {name} draw of size {size}")
        out = queue.pop(0)
        assert out.shape == (size,), (name, out.shape, size)
        return out.copy()

    def exponential(self, *, scale, size):
        assert scale == 0.5
        return self._take(self.exponentials, size, "exponential")

    def normal(self, *, size):
        return self._take(self.normals, size, "normal")

    def integers(self, high, *, size):
        assert high == 2
        self.label_sizes.append(size)
        return self._take(self.labels, size, "label")

    def assert_empty(self):
        assert not self.exponentials
        assert not self.normals
        assert not self.labels


def _constant_terminal(x):
    return np.full_like(x, 0.25), np.full_like(x, 0.4)


@pytest.mark.parametrize(
    ("code", "signed", "squared"),
    [
        (ID, 0.25, 0.0625),
        (DX, -0.4, 0.16),
        (F0, 15.0 / 64.0, 225.0 / 4096.0),
        (F1, 13.0 / 16.0, 169.0 / 256.0),
        (F2, -1.5, 2.25),
        (F3, -6.0, 36.0),
    ],
)
def test_six_normalized_terminal_polynomials(code, signed, squared):
    rng = ScriptedRNG(exponentials=[[1.0]])
    result = raw_sample(
        np.array([2.0]),
        0.0,
        lambda x: (np.full_like(x, 0.25), np.full_like(x, -0.4)),
        rng,
        root_code=code,
    )
    assert result.values[0] == pytest.approx(signed)
    assert result.values[0] ** 2 == pytest.approx(squared)
    assert result.node_counts.tolist() == [1]
    assert result.terminal_counts.tolist() == [int(k == code) for k in range(6)]
    rng.assert_empty()


def test_leaf_survival_and_id_branch_factor():
    leaf_rng = ScriptedRNG(exponentials=[[1.0]], normals=[[0.0]])
    leaf = raw_sample([0.0], 0.05, _constant_terminal, leaf_rng)
    assert leaf.values[0] == pytest.approx(0.25 * math.exp(0.1))
    assert not leaf.root_branched[0]
    assert leaf.node_counts.tolist() == [1]
    leaf_rng.assert_empty()

    branch_rng = ScriptedRNG(
        exponentials=[[0.01], [1.0]], normals=[[0.0], [0.0]]
    )
    branch = raw_sample([0.0], 0.05, _constant_terminal, branch_rng)
    expected = 0.5 * math.exp(0.10) * (15.0 / 64.0)
    assert branch.values[0] == pytest.approx(expected)
    assert branch.root_branched.tolist() == [True]
    assert branch.node_counts.tolist() == [2]
    assert branch.terminal_counts.tolist() == [0, 0, 1, 0, 0, 0]
    branch_rng.assert_empty()


def test_dx_children_share_the_branch_position():
    seen = []

    def terminal(x):
        seen.append(np.asarray(x).copy())
        return 0.1 * x, np.full_like(x, 0.3)

    rng = ScriptedRNG(
        exponentials=[[0.01], [1.0, 1.0]],
        normals=[[2.0], [0.0, 0.0]],
    )
    result = raw_sample([1.0], 0.05, terminal, rng, root_code=DX)
    assert len(seen) == 1
    np.testing.assert_allclose(seen[0], [1.2, 1.2])
    expected = 0.5 * math.exp(0.18) * (1.0 - 3.0 * 0.12**2) * 0.3
    assert result.values[0] == pytest.approx(expected)
    assert result.node_counts.tolist() == [3]
    assert result.terminal_counts.tolist() == [0, 1, 0, 1, 0, 0]
    rng.assert_empty()


def test_positive_and_negative_f_labels_have_exact_weights():
    positive_rng = ScriptedRNG(
        exponentials=[[0.01], [1.0, 1.0]],
        normals=[[0.0], [0.0, 0.0]],
        labels=[[0]],
    )
    positive = raw_sample([0.0], 0.05, _constant_terminal, positive_rng, F0)
    positive_expected = math.exp(0.18) * (15.0 / 64.0) * (13.0 / 16.0)
    assert positive.values[0] == pytest.approx(positive_expected)
    assert positive.terminal_counts.tolist() == [0, 0, 1, 1, 0, 0]
    positive_rng.assert_empty()

    negative_rng = ScriptedRNG(
        exponentials=[[0.01], [1.0, 1.0, 1.0]],
        normals=[[0.0], [0.0, 0.0, 0.0]],
        labels=[[1]],
    )
    negative = raw_sample([0.0], 0.05, _constant_terminal, negative_rng, F0)
    # (-e^.02/2) * (e^.08*.4)^2 * (e^.08*-1.5)
    negative_expected = 0.12 * math.exp(0.26)
    assert negative.values[0] == pytest.approx(negative_expected)
    assert negative.terminal_counts.tolist() == [0, 2, 0, 0, 1, 0]
    negative_rng.assert_empty()


def test_zero_label_is_selected_without_renormalization_or_children():
    rng = ScriptedRNG(
        exponentials=[[0.01, 0.01], [1.0, 1.0]],
        normals=[[0.0], [0.0, 0.0]],
        labels=[[0, 1]],
    )
    result = raw_sample([0.0, 1.0], 0.05, _constant_terminal, rng, F2)
    expected_live = math.exp(0.18) * (15.0 / 64.0) * -6.0
    np.testing.assert_allclose(result.values, [expected_live, 0.0])
    assert result.node_counts.tolist() == [3, 1]
    assert result.root_branched.tolist() == [True, True]
    assert result.terminal_counts.tolist() == [0, 0, 1, 0, 0, 1]
    assert rng.label_sizes == [2]
    rng.assert_empty()


def test_majority_scripted_branch_rule_and_common_birth_position():
    seen = []

    def phi(x):
        seen.append(np.asarray(x).copy())
        return 0.1 * x

    rng = ScriptedRNG(
        exponentials=[[0.01], [1.0, 1.0, 1.0]],
        normals=[[2.0], [0.0, 0.0, 0.0]],
    )
    result = majority_sample([1.0], 0.05, phi, rng)
    np.testing.assert_allclose(seen[0], [1.2, 1.2, 1.2])
    expected = (3.0 * 0.12 - 0.12**3) / 2.0
    assert result.values.tolist() == pytest.approx([expected])
    assert result.node_counts.tolist() == [4]
    assert result.root_branched.tolist() == [True]
    assert result.terminal_counts.tolist() == [3, 0, 0, 0, 0, 0]
    rng.assert_empty()


@pytest.mark.parametrize(
    ("positions", "h", "message"),
    [([np.nan], 0.05, "positions"), ([0.0], np.inf, "h"), ([0.0], -0.1, "h")],
)
def test_nonfinite_or_negative_parameters_are_rejected(positions, h, message):
    with pytest.raises(ValueError, match=message):
        raw_sample(positions, h, _constant_terminal, np.random.default_rng(0))


def test_raw_local_range_and_finite_terminal_are_enforced_without_clipping():
    with pytest.raises(ValueError, match="2/25"):
        raw_sample([0.0], 0.081, _constant_terminal, np.random.default_rng(0))
    with pytest.raises(ValueError, match="finite"):
        raw_sample(
            [0.0], 0.0, lambda x: (np.full_like(x, np.nan), x),
            np.random.default_rng(0),
        )

    result = raw_sample(
        [0.0], 0.0, lambda x: (np.full_like(x, 2.0), np.zeros_like(x)),
        np.random.default_rng(0),
    )
    assert result.values.tolist() == [2.0]


def _allen_cahn_problem(h):
    phi = lambda x: 0.2 * np.sin(x) + 0.01 * np.sin(3.0 * x)
    phi_prime = lambda x: 0.2 * np.cos(x) + 0.03 * np.cos(3.0 * x)
    pde = ParabolicPDE(
        T=h,
        f=lambda z: z - z**3,
        f_derivatives=(lambda z: 1.0 - 3.0 * z**2, lambda z: -6.0 * z, lambda z: -6.0),
        phi=phi,
        phi_derivatives=(phi_prime,),
        reaction_kind="allen_cahn",
    )
    return pde, lambda x: (phi(x), phi_prime(x))


@pytest.mark.parametrize(
    ("new_code", "old_code", "x"),
    [
        (ID, Id(), -0.7),
        (DX, Dx(), 0.4),
        (F0, FDeriv(1.0, 0), 1.1),
        (F2, FDeriv(1.0, 2), -0.2),
    ],
)
def test_raw_distribution_matches_original_sampler(new_code, old_code, x):
    h = 0.05
    n = 12_000
    pde, terminal = _allen_cahn_problem(h)
    vector = raw_sample(
        np.full(n, x), h, terminal, np.random.default_rng(3000 + new_code), new_code
    ).values
    old_rng = np.random.default_rng(9000 + new_code)
    original = np.fromiter(
        (
            sample_tree(pde, 0.0, x, rng=old_rng, rate=2.0, code=old_code).value
            for _ in range(n)
        ),
        dtype=float,
        count=n,
    )

    # The second-moment uncertainty below is an empirical diagnostic; no
    # fourth-moment confidence claim is made.  Wide fixed-seed thresholds
    # catch law changes without turning ordinary MC fluctuation into flakes.
    for left, right, floor in (
        (vector, original, 0.002),
        (vector**2, original**2, 0.003),
    ):
        se = math.sqrt(left.var(ddof=1) / n + right.var(ddof=1) / n)
        assert abs(left.mean() - right.mean()) <= 8.0 * se + floor


def test_majority_distribution_matches_existing_sampler():
    h = 0.2
    n = 12_000
    pde, terminal = _allen_cahn_problem(h)
    x = 0.45
    vector = majority_sample(
        np.full(n, x), h, lambda y: terminal(y)[0], np.random.default_rng(771)
    ).values
    original = sample_majority(
        pde, 0.0, x, n, rate=2.0, seed=991, batch_size=128
    ).values
    for left, right, floor in (
        (vector, original, 0.002),
        (vector**2, original**2, 0.002),
    ):
        se = math.sqrt(left.var(ddof=1) / n + right.var(ddof=1) / n)
        assert abs(left.mean() - right.mean()) <= 8.0 * se + floor
