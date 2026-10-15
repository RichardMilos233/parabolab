import importlib
import math

import numpy as np
import pytest

from parabolab import (
    TimeLambdaMCComparison,
    TreeSample,
    compare_time_lambda_mc,
    sample_tree,
    sweep_time_lambda_mc,
)
from parabolab.library import binary_control_1d
from parabolab.rate_optimization import riccati_binary_second_moment


tlmc = importlib.import_module("parabolab.time_lambda_mc")


def test_mc_cell_matches_direct_sample_tree_and_uses_cell_horizon():
    calls = []

    def factory(T):
        calls.append(T)
        return binary_control_1d(T=T)

    sweep = sweep_time_lambda_mc(
        factory, lambda_min=0.8, lambda_max=1.2, n_lambda=2,
        T_min=0.05, T_max=0.1, n_T=2, n_samples=64, seed=17,
        max_nodes=None, max_cell_nodes=None, reference_T=0.075, progress=False,
    )
    rng = tlmc._cell_rng(17, 0, 0)
    direct = np.array([
        sample_tree(binary_control_1d(T=0.05), 0.0, 0.0, rng=rng, rate=0.8).value
        for _ in range(64)
    ])
    assert sweep.mean[0, 0] == np.mean(direct)
    assert sweep.variance[0, 0] == np.var(direct, ddof=1)
    assert sweep.second_moment[0, 0] == np.mean(direct * direct)
    assert sweep.completed_samples[0, 0] == 64
    assert calls == pytest.approx([0.075, 0.05, 0.1])


def test_binary_observed_second_moment_matches_finite_riccati_control():
    sweep = sweep_time_lambda_mc(
        binary_control_1d, lambda_min=0.5, lambda_max=1.0, n_lambda=2,
        T_min=0.05, T_max=0.1, n_T=2, n_samples=2_000, seed=31,
        max_nodes=None, max_cell_nodes=None, progress=False,
    )
    expected = riccati_binary_second_moment(0.1, 1.0)
    assert sweep.second_moment[1, 1] == pytest.approx(expected, rel=0.15)


def test_node_and_cell_guards_mark_whole_cell_invalid():
    node_limited = sweep_time_lambda_mc(
        binary_control_1d, lambda_min=8.0, lambda_max=9.0, n_lambda=2,
        T_min=4.0, T_max=5.0, n_T=2, n_samples=2, seed=1,
        max_nodes=1, max_cell_nodes=None, progress=False,
    )
    assert np.all(node_limited.status == "node_limit")
    assert np.isnan(node_limited.variance).all()
    assert np.all(node_limited.total_nodes == 2)

    cell_limited = sweep_time_lambda_mc(
        binary_control_1d, lambda_min=8.0, lambda_max=9.0, n_lambda=2,
        T_min=4.0, T_max=5.0, n_T=2, n_samples=2, seed=1,
        max_nodes=None, max_cell_nodes=1, progress=False,
    )
    assert np.all(cell_limited.status == "cell_budget")
    assert np.isnan(cell_limited.variance).all()


def test_overflow_and_interrupt_are_preserved_as_status(monkeypatch, tmp_path):
    def overflow(*args, **kwargs):
        raise OverflowError("synthetic overflow")

    monkeypatch.setattr(tlmc, "sample_tree", overflow)
    failed = sweep_time_lambda_mc(
        binary_control_1d, lambda_min=0.5, lambda_max=1.0, n_lambda=2,
        T_min=0.05, T_max=0.1, n_T=2, n_samples=2, progress=False,
    )
    assert np.all(failed.status == "error")
    assert "OverflowError" in failed.reason[0, 0]

    def interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(tlmc, "sample_tree", interrupt)
    partial = tmp_path / "partial.npz"
    with pytest.raises(KeyboardInterrupt):
        sweep_time_lambda_mc(
            binary_control_1d, lambda_min=0.5, lambda_max=1.0, n_lambda=2,
            T_min=0.05, T_max=0.1, n_T=2, n_samples=2,
            checkpoint_path=partial, progress=False,
        )
    loaded = TimeLambdaMCComparison.load(partial)
    assert len(loaded.sweeps) == 1
    assert loaded.sweeps[0].status[0, 0] == "interrupted"
    assert np.count_nonzero(loaded.sweeps[0].status == "pending") == 3


def test_zero_variance_save_load_and_plot(monkeypatch, tmp_path):
    monkeypatch.setattr(
        tlmc, "sample_tree", lambda *args, **kwargs: TreeSample(value=2.0, n_nodes=1),
    )
    sweep = sweep_time_lambda_mc(
        binary_control_1d, lambda_min=0.5, lambda_max=1.0, n_lambda=2,
        T_min=0.05, T_max=0.1, n_T=2, n_samples=3, progress=False,
    )
    assert np.array_equal(sweep.variance, np.zeros((2, 2)))

    data = tmp_path / "grid.npz"
    image = tmp_path / "grid.png"
    comparison = compare_time_lambda_mc(sweep).save(data)
    loaded = TimeLambdaMCComparison.load(data)
    loaded.plot(image, save_individual=True)
    assert np.array_equal(loaded.sweeps[0].variance, sweep.variance)
    assert loaded.sweeps[0].completed_samples[0, 0] == 3
    assert image.exists() and (tmp_path / "grid_1.png").exists()
    with np.load(data, allow_pickle=False) as archive:
        assert archive["status"][0, 0, 0] == "complete"


def test_default_sweep_has_no_work_guards(monkeypatch):
    def large_tree(*args, **kwargs):
        assert kwargs["max_nodes"] is None
        return TreeSample(value=1.0, n_nodes=60_000)

    monkeypatch.setattr(tlmc, "sample_tree", large_tree)
    sweep = sweep_time_lambda_mc(
        binary_control_1d, lambda_min=0.5, lambda_max=1.0, n_lambda=2,
        T_min=0.05, T_max=0.1, n_T=2, n_samples=3, progress=False,
    )
    assert sweep.max_nodes is None
    assert sweep.max_cell_nodes is None
    assert np.all(sweep.status == "complete")
    assert np.all(sweep.completed_samples == 3)
    assert np.all(sweep.total_nodes == 180_000)


@pytest.mark.parametrize("name,value", [
    ("n_lambda", 2.5), ("n_T", True), ("n_samples", 1),
])
def test_grid_counts_require_integers_at_least_two(name, value):
    kwargs = {name: value}
    with pytest.raises(ValueError, match=name):
        sweep_time_lambda_mc(binary_control_1d, progress=False, **kwargs)


def test_parallel_single_chunk_matches_serial():
    kwargs = dict(
        lambda_min=0.5, lambda_max=2.0, n_lambda=3, T_min=0.05, T_max=0.3,
        n_T=2, n_samples=50, seed=5, progress=False,
    )
    serial = sweep_time_lambda_mc(binary_control_1d, **kwargs)
    parallel = sweep_time_lambda_mc(binary_control_1d, n_jobs=2, **kwargs)
    for name in ("mean", "variance", "second_moment", "completed_samples",
                 "total_nodes", "status"):
        assert np.array_equal(getattr(parallel, name), getattr(serial, name)), name


def test_chunked_results_do_not_depend_on_worker_count(tmp_path):
    kwargs = dict(
        lambda_min=0.5, lambda_max=2.0, n_lambda=2, T_min=0.05, T_max=0.3,
        n_T=2, n_samples=60, seed=9, chunk_size=25, progress=False,
    )
    two = sweep_time_lambda_mc(binary_control_1d, n_jobs=2, **kwargs)
    three = sweep_time_lambda_mc(binary_control_1d, n_jobs=3,
                                 checkpoint_path=tmp_path / "c.npz", **kwargs)
    assert np.array_equal(two.variance, three.variance)
    assert np.all(two.completed_samples == 60)
    assert np.all(two.status == "complete")
    # Chunk streams 25 + 25 + 10 are the per-chunk seeds, concatenated in order.
    pde = binary_control_1d(T=0.05)
    direct = []
    for c, n in enumerate((25, 25, 10)):
        rng = tlmc._chunk_rng(9, 0, 1, c, 3)
        direct += [sample_tree(pde, 0.0, 0.0, rng=rng, rate=2.0).value for _ in range(n)]
    direct = np.array(direct)
    assert two.mean[0, 1] == np.mean(direct)
    assert two.variance[0, 1] == np.var(direct, ddof=1)
    loaded = TimeLambdaMCComparison.load(tmp_path / "c.npz").sweeps[0]
    assert loaded.status[0, 0] == "complete"
    assert loaded.chunk_size == 25
    assert compare_time_lambda_mc(three).save(tmp_path / "all.npz") is not None
    assert TimeLambdaMCComparison.load(tmp_path / "all.npz").sweeps[0].chunk_size == 25


def test_parallel_node_limit_marks_cell_with_serial_counts():
    kwargs = dict(
        lambda_min=8.0, lambda_max=9.0, n_lambda=2, T_min=4.0, T_max=5.0,
        n_T=2, n_samples=6, seed=1, max_nodes=1, progress=False,
    )
    chunked = sweep_time_lambda_mc(binary_control_1d, n_jobs=2, chunk_size=2, **kwargs)
    assert np.all(chunked.status == "node_limit")
    assert np.isnan(chunked.variance).all()
    assert np.all(chunked.total_nodes == 2)


def test_parallel_rejects_serial_cell_budget():
    with pytest.raises(ValueError, match="max_cell_nodes"):
        sweep_time_lambda_mc(binary_control_1d, n_jobs=2, max_cell_nodes=10,
                             progress=False)
    with pytest.raises(ValueError, match="chunk_size"):
        sweep_time_lambda_mc(binary_control_1d, n_samples=10, chunk_size=3,
                             progress=False)
