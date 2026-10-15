from functools import partial
import math

import numpy as np
import pytest

from parabolab import TimeLambdaMCComparison, compare_time_lambda_mc, sample_tree, sweep_time_lambda_mc
from parabolab.flat_batch import flat_semilinear_leaf_values, sample_flat_batch
from parabolab.library import allen_cahn_flat, allen_cahn_wave_1d, binary_control_1d, fisher_kpp_1d


def _exact_second_moment(leaf_values, a, rate, T, steps=20_000):
    """E[H^2] from m_k' = rate m_k + 2 m_0 m_{k+1} / rate, m_k(0) = f^(k)(a)^2.

    The root ``Id`` adds m_Id(T) = e^{rate T} (a^2 + int_0^T e^{-rate u} m_0(u) du / rate).
    Classical RK4 on the codes k < K (m_K = 0) plus the root integral.
    """
    K = len(leaf_values)

    def rhs(r, y):
        m = y[:K]
        nxt = np.append(m[1:], 0.0)
        return np.append(rate * m + 2.0 * m[0] * nxt / rate, math.exp(-rate * r) * m[0])

    y = np.append(np.asarray(leaf_values, dtype=float) ** 2, 0.0)
    h = T / steps
    for i in range(steps):
        r = i * h
        k1 = rhs(r, y)
        k2 = rhs(r + h / 2, y + h / 2 * k1)
        k3 = rhs(r + h / 2, y + h / 2 * k2)
        k4 = rhs(r + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return math.exp(rate * T) * (a * a + y[K] / rate)


@pytest.mark.parametrize("factory,a,rate,T", [
    (allen_cahn_flat, 0.5, 2.0, 0.5),
    (allen_cahn_flat, 0.3, 1.0, 0.6),   # T_2(1) = 0.73 for phi = 0.3
    (lambda phi0, T: fisher_kpp_1d(T=T, phi0=phi0), 0.2, 1.5, 0.6),
])
def test_flat_mean_and_second_moment_match_exact(factory, a, rate, T):
    pde = factory(a, T=T)
    leaf = flat_semilinear_leaf_values(pde, a)
    values, nodes, exceeded = sample_flat_batch(
        leaf, a, T, rate, 400_000, np.random.default_rng(11),
    )
    assert not exceeded.any() and np.all(np.isfinite(values))
    n = len(values)
    mean_se = np.std(values) / math.sqrt(n)
    assert abs(np.mean(values) - pde.exact_solution(0.0, 0.0)) < 5 * mean_se
    squares = values * values
    second_se = np.std(squares) / math.sqrt(n)
    exact = _exact_second_moment(leaf, a, rate, T)
    assert abs(np.mean(squares) - exact) < 5 * second_se


def test_flat_value_distribution_matches_sample_tree():
    a, rate, T = 0.5, 3.0, 1.0
    pde = allen_cahn_flat(a, T=T)
    rng = np.random.default_rng(5)
    tree = np.array([sample_tree(pde, 0.0, 0.0, rng=rng, rate=rate).value for _ in range(6000)])
    flat, _, _ = sample_flat_batch(
        flat_semilinear_leaf_values(pde, a), a, T, rate, 200_000, np.random.default_rng(6),
    )
    # Zero mass: binomial comparison.
    p_tree, p_flat = np.mean(tree == 0), np.mean(flat == 0)
    assert abs(p_tree - p_flat) < 5 * math.sqrt(p_flat * (1 - p_flat) / len(tree))
    # Nonzero values: two-sample Kolmogorov-Smirnov at about the 0.1% level.
    # H has atoms (e^{rate tau} e^{rate (T - tau)} cancels tau); the two samplers
    # form products in different orders, so round before comparing.
    x = np.sort(np.round(tree[tree != 0], 9))
    y = np.sort(np.round(flat[flat != 0], 9))
    grid = np.concatenate((x, y))
    d = np.max(np.abs(np.searchsorted(x, grid, side="right") / len(x)
                      - np.searchsorted(y, grid, side="right") / len(y)))
    assert d < 1.95 * math.sqrt((len(x) + len(y)) / (len(x) * len(y)))


def test_flat_node_limit_marks_trees():
    pde = allen_cahn_flat(0.5, T=1.3)
    leaf = flat_semilinear_leaf_values(pde, 0.5)
    values, nodes, exceeded = sample_flat_batch(
        leaf, 0.5, 1.3, 6.0, 20_000, np.random.default_rng(2), max_nodes=1,
    )
    branched = nodes > 1
    assert np.array_equal(exceeded, branched)
    assert np.isnan(values[exceeded]).all()
    assert np.all(values[~exceeded] == 0.5 * math.exp(6.0 * 1.3))


@pytest.mark.parametrize("pde,a,error", [
    (binary_control_1d(T=0.5), 1.0, TypeError),
    (allen_cahn_wave_1d(T=0.5), 0.0, ValueError),
    (allen_cahn_flat(0.5), None, ValueError),
])
def test_flat_sampler_rejects_unsupported_inputs(pde, a, error):
    with pytest.raises(error):
        flat_semilinear_leaf_values(pde, a)


def test_flat_sweep_records_diagnostics_and_is_worker_independent(tmp_path):
    kwargs = dict(
        flat_terminal=0.5, lambda_min=0.5, lambda_max=8.0, n_lambda=3,
        T_min=0.2, T_max=1.3, n_T=2, n_samples=4000, seed=3, chunk_size=1500,
        sampler="flat", n_batches=8, progress=False,
    )
    factory = partial(allen_cahn_flat, 0.5)
    one = sweep_time_lambda_mc(factory, n_jobs=1, **kwargs)
    two = sweep_time_lambda_mc(factory, n_jobs=2, **kwargs)
    for name in ("variance", "max_share", "n_nonzero", "batch_variance", "total_nodes"):
        assert np.array_equal(getattr(one, name), getattr(two, name), equal_nan=True), name
    assert np.all(one.status == "complete")
    assert one.batch_variance.shape == (2, 3, 8)
    nonzero = one.n_nonzero > 0
    assert np.all((one.max_share[nonzero] > 0) & (one.max_share[nonzero] <= 1))
    assert np.isnan(one.max_share[~nonzero]).all()

    data = tmp_path / "flat.npz"
    compare_time_lambda_mc(one, one).save(data)
    loaded = TimeLambdaMCComparison.load(data)
    assert loaded.sweeps[1].sampler == "flat"
    assert np.array_equal(loaded.sweeps[0].batch_variance, one.batch_variance, equal_nan=True)
    for statistic in ("variance", "max_share", "batch_cv"):
        loaded.plot(tmp_path / f"{statistic}.png", statistic=statistic)
        assert (tmp_path / f"{statistic}.png").exists()


def test_flat_sweep_requires_flat_terminal():
    with pytest.raises(ValueError, match="flat_terminal"):
        sweep_time_lambda_mc(partial(allen_cahn_flat, 0.5), sampler="flat", progress=False)



def test_flat_exact_variance_matches_reference_and_diverges_at_T2():
    from parabolab import sweep_time_lambda
    from parabolab.time_lambda import _boundary, flat_exact_variance

    pde = allen_cahn_flat(0.5)
    leaf = flat_semilinear_leaf_values(pde, 0.5)
    K = sweep_time_lambda(pde, flat_terminal=0.5).K
    Ts = np.array([0.2, 0.5, 0.65, 0.9])
    var = flat_exact_variance(leaf, 0.5, 2.0, Ts, K=K)
    for T, v in zip(Ts[:3], var[:3]):
        exact = (_exact_second_moment(leaf, 0.5, 2.0, T)
                 - allen_cahn_flat(0.5, T=T).exact_solution(0.0, 0.0) ** 2)
        assert v == pytest.approx(exact, rel=1e-6)
    assert Ts[3] > _boundary(2.0, K) and np.isinf(var[3])


def test_plot_slices_draws_theory_against_mc(tmp_path):
    sweep = sweep_time_lambda_mc(
        partial(allen_cahn_flat, 0.5), flat_terminal=0.5, lambda_min=1.0, lambda_max=3.0,
        n_lambda=3, T_min=0.1, T_max=0.9, n_T=5, n_samples=20_000, seed=2,
        sampler="flat", progress=False,
    )
    comparison = compare_time_lambda_mc(sweep)
    comparison.plot_slices(tmp_path / "slices.png", [allen_cahn_flat(0.5)], lambdas=(1.0, 3.0))
    assert (tmp_path / "slices.png").exists()
    with pytest.raises(ValueError, match="one PDE per sweep"):
        comparison.plot_slices(None, [])
