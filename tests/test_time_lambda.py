import math

import numpy as np
import pytest
import matplotlib.pyplot as plt

from parabolab import compare_time_lambda, sweep_time_lambda
from parabolab.library import (
    allen_cahn_flat,
    allen_cahn_wave_1d,
    binary_control_1d,
    fisher_kpp_1d,
)
from parabolab.pde import ParabolicPDE
from parabolab.rate_optimization import riccati_binary_second_moment
from parabolab.time_lambda import _boundary


def test_allen_cahn_frozen_boundary_and_interval():
    sweep = sweep_time_lambda(allen_cahn_flat(0.5), flat_terminal=0.5)
    assert sweep.K == pytest.approx(0.765060614256551, abs=1e-12)
    assert sweep.peak_T == pytest.approx(0.703889967537839, abs=1e-12)
    assert sweep.safe_interval == pytest.approx(
        (0.804546254505281, 7.644676545699491), abs=1e-11
    )
    assert math.log1p(sweep.K * 0.745**2) / 0.745 == pytest.approx(
        0.475047736587427, abs=1e-12
    )


def test_kpp_half_closed_integral():
    sweep = sweep_time_lambda(fisher_kpp_1d(phi0=0.5), flat_terminal=0.5)
    assert sweep.K == pytest.approx(math.pi / math.sqrt(2.0), abs=1e-12)


def test_binary_boundary_matches_riccati_finiteness():
    sweep = sweep_time_lambda(binary_control_1d(), reference_T=0.5)
    lo, hi = sweep.safe_interval
    for boundary_rate in (lo, hi):
        assert math.isfinite(riccati_binary_second_moment(0.5, boundary_rate * (1 + (1e-6 if boundary_rate == lo else -1e-6))))
        assert not math.isfinite(riccati_binary_second_moment(0.5, boundary_rate * (1 - (1e-6 if boundary_rate == lo else -1e-6))))


def test_peak_equality_has_no_allowed_rate():
    base = sweep_time_lambda(allen_cahn_flat(0.5), flat_terminal=0.5)
    at_peak = sweep_time_lambda(
        allen_cahn_flat(0.5), flat_terminal=0.5, reference_T=base.peak_T
    )
    assert at_peak.safe_interval == ()


def test_unsupported_inputs_are_refused():
    with pytest.raises(ValueError, match="flat_terminal"):
        sweep_time_lambda(allen_cahn_wave_1d(), flat_terminal=0.5)
    non_polynomial = ParabolicPDE(
        T=0.5, f=math.exp, f_derivatives=lambda k: math.exp,
        phi=lambda x: 1.0,
    )
    with pytest.raises(TypeError, match="non-polynomial"):
        sweep_time_lambda(non_polynomial, flat_terminal=1.0)

    bad_flat_derivative = ParabolicPDE(
        T=0.5, f=lambda z: z**2,
        f_derivatives=(lambda z: 2.0 * z, lambda z: 2.0),
        phi=lambda x: 1.0, phi_derivatives=(lambda x: 1.0,),
    )
    with pytest.raises(ValueError, match="phi' samples"):
        sweep_time_lambda(bad_flat_derivative, flat_terminal=1.0)

    mismatched_binary = binary_control_1d()
    mismatched_binary.phi_expr = 2
    with pytest.raises(ValueError, match=r"f\(u\)=u\^2 with phi=1"):
        sweep_time_lambda(mismatched_binary)


@pytest.mark.parametrize("f, derivatives, a", [
    (lambda z: 0.0, (), 1.0),
    (lambda z: 1.0 + z, (lambda z: 1.0,), 1.0),
])
def test_equilibrium_or_linear_has_no_explosion_boundary(f, derivatives, a):
    pde = ParabolicPDE(T=0.5, f=f, f_derivatives=derivatives, phi=lambda x: a)
    sweep = sweep_time_lambda(pde, flat_terminal=a)
    assert sweep.K == math.inf
    assert sweep.safe_interval == (0.0, math.inf)
    assert np.isnan(sweep.boundary).all()


def test_invalid_quadrature_tolerance_is_rejected():
    with pytest.raises(ValueError, match="quadrature_tol"):
        sweep_time_lambda(
            allen_cahn_flat(0.5), flat_terminal=0.5, quadrature_tol=math.nan
        )


@pytest.mark.parametrize("reference_T", [1e-50, 1e-200])
def test_tiny_reference_time_roots_are_stable(reference_T):
    sweep = sweep_time_lambda(
        allen_cahn_flat(0.5), flat_terminal=0.5, reference_T=reference_T
    )
    lo, hi = sweep.safe_interval
    assert lo == pytest.approx(reference_T / sweep.K, rel=1e-12)
    assert _boundary(lo, sweep.K) == pytest.approx(reference_T, rel=1e-12)
    assert _boundary(hi, sweep.K) == pytest.approx(reference_T, rel=1e-12)


def test_plot_combined_and_individual(tmp_path):
    sweeps = [
        sweep_time_lambda(allen_cahn_flat(0.5), flat_terminal=0.5, n_points=10),
        sweep_time_lambda(binary_control_1d(), n_points=10),
    ]
    output = tmp_path / "boundaries.png"
    compare_time_lambda(*sweeps).plot(output, save_individual=True)
    assert output.exists()
    assert len(list(tmp_path.glob("boundaries_*.png"))) == 2


def test_plot_preserves_requested_lambda_range():
    sweep = sweep_time_lambda(
        binary_control_1d(), lambda_min=3.0, lambda_max=4.0, n_points=10
    )
    fig, ax = plt.subplots()
    sweep.plot(ax=ax)
    assert ax.get_xlim() == pytest.approx((3.0, 4.0))
    plt.close(fig)
