"""Tests for the deep-branching network ablation harness."""

import dataclasses
import functools

import numpy as np
import pytest

torch = pytest.importorskip("torch")

import parabolab.deep as deep
from parabolab.deep import datasets
from parabolab.library import allen_cahn_nd

AC1 = functools.partial(allen_cahn_nd, d=1, T=0.5)

TINY = datasets.DatasetSpec(
    key="tiny", factory_name="allen_cahn_nd",
    factory_kwargs=(("d", 1), ("T", 0.5)),
    x_lo=-1.0, x_hi=1.0, n_states=8, m_samples=4, seed=0,
)


# ---------------------------------------------------------------------------
# datasets
# ---------------------------------------------------------------------------

def test_benchmarks_resolve_to_library_factories():
    for key, spec in datasets.BENCHMARKS.items():
        assert spec.key == key
        pde = spec.factory()()
        assert getattr(pde, "d", 1) == 1
        assert spec.x_lo < spec.x_hi


def test_load_or_generate_roundtrips_bit_identically(tmp_path):
    a = datasets.load_or_generate(TINY, tmp_path)
    assert datasets.dataset_path(TINY, tmp_path).exists()
    b = datasets.load_or_generate(TINY, tmp_path)
    for field in ("t", "x", "y", "stderr", "n_kept"):
        np.testing.assert_array_equal(getattr(a, field), getattr(b, field))
    assert b.m_samples == a.m_samples and b.rate == a.rate
    direct = deep.generate_training_data(
        AC1, n_states=8, m_samples=4, seed=0, x_lo=-1.0, x_hi=1.0)
    np.testing.assert_array_equal(a.y, direct.y)


def test_load_rejects_mismatched_spec(tmp_path):
    datasets.load_or_generate(TINY, tmp_path)
    other = dataclasses.replace(TINY, m_samples=5)   # same key/seed -> same file
    with pytest.raises(ValueError, match="spec"):
        datasets.load_or_generate(other, tmp_path)


def test_corrupt_file_is_regenerated(tmp_path):
    a = datasets.load_or_generate(TINY, tmp_path)
    datasets.dataset_path(TINY, tmp_path).write_bytes(b"not an npz")
    b = datasets.load_or_generate(TINY, tmp_path)
    np.testing.assert_array_equal(a.y, b.y)


def test_factory_is_picklable():
    import pickle
    pickle.dumps(TINY.factory())
