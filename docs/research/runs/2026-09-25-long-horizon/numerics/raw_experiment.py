"""Long-horizon raw Allen--Cahn moment and wave diagnostics.

The exact rational calculations in this file certify only the explicitly
reported scalar inequalities.  ODE, optimization, sampling, and finite-
difference outputs are floating diagnostics with the limitations recorded in
their JSON artifacts.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
import time
import traceback
from typing import Callable

import numpy as np


HERE = Path(__file__).resolve().parent
RUN = HERE.parent
PROJECT = HERE.parents[4]
PROTOCOL = HERE / "protocol.json"
WAVE_PROTOCOL = HERE / "wave-protocol.json"
THEORY = RUN / "04-theory.md"
SOURCE = Path(__file__).resolve()
TREE_SOURCE = PROJECT / "parabolab" / "tree.py"
LIBRARY_SOURCE = PROJECT / "parabolab" / "library.py"
PRIOR_FLAT_SOURCE = (
    PROJECT / "docs/research/runs/2026-09-16-certified-tuple-policy/"
    "numerics/flat_explosion_check.py"
)
PRIOR_FLAT_RESULT = PRIOR_FLAT_SOURCE.with_name("flat-explosion-checks.json")

BOUNDARY_RESULT = HERE / "boundary-certificates.json"
RAW_RESULT = HERE / "raw-results.json"
RAW_SAMPLES = HERE / "raw-samples.npz"
WAVE_RESULT = HERE / "wave-results.json"
RUN_LOG = HERE / "raw-experiment.log"
VERIFY_LOG = HERE / "raw-verify.log"

RUN_DATE = "2026-09-25"
COMPLETION_DATE = "2026-09-26"
RAW_HORIZONS = (0.05, 0.1, 0.25, 0.5, 0.65, 0.7, 0.75, 0.9, 0.95, 1.0, 1.5, 2.0)
RAW_SAMPLE_HORIZONS = (0.05, 0.5, 0.7, 1.0, 1.5, 2.0)
POLICIES = (0.5, 0.95)
RAW_SAMPLE_COUNT = 4096
RAW_SAMPLE_SEED_BASE = 40260925
WAVE_HORIZONS = (0.05, 0.1, 0.25, 0.5, 0.75, 1.0)
WAVE_RATES = (0.75, 1.0, 2.0)
WAVE_POLICIES = {
    "uniform": (0.5, 0.5, 0.5),
    "static-supported": (0.95, 0.95, 0.95),
}
WAVE_DX = (0.1, 0.05)
WAVE_HALF_WIDTH = 12.0
WAVE_STOP = 1.0e12
LEFT_LIMIT = np.array((1.0, 0.0, 0.0, 4.0, 36.0, 36.0))
RIGHT_LIMIT = np.array((0.0, 0.0, 0.0, 1.0, 0.0, 36.0))

C_R = F(8)
C_RECTANGLES = 65536
C_ROUNDING_BITS = 60
C_ROUNDING_DENOMINATOR = 2**C_ROUNDING_BITS
SERIES_TERMS = 30
EXP_DEGREE = 40

A0 = F(9, 64)
B0 = F(1, 16)
C0 = F(9)
E0 = F(36)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_record(value: F) -> dict[str, str | float]:
    return {"exact": str(value), "float": float(value)}


def json_dump(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def c_polynomial(value: F) -> F:
    return A0 + B0 * value + C0 * value * value / 2 + E0 * value**3 / 6


def abs_polynomial(value: float) -> float:
    return 3.0 / 8.0 + value / 4.0 + 1.5 * value**2 + value**3


def rounded_units(value: F, *, up: bool) -> int:
    scaled = value * C_ROUNDING_DENOMINATOR
    if up:
        return -(-scaled.numerator // scaled.denominator)
    return scaled.numerator // scaled.denominator


def c_integral_enclosure() -> dict:
    """Recompute the prior exact rectangle and tail enclosure of C."""
    step = C_R / C_RECTANGLES
    lower_units = 0
    upper_units = 0
    for index in range(C_RECTANGLES + 1):
        reciprocal = 1 / c_polynomial(index * step)
        if index > 0:
            lower_units += rounded_units(reciprocal, up=False)
        if index < C_RECTANGLES:
            upper_units += rounded_units(reciprocal, up=True)
    finite_lower = step * F(lower_units, C_ROUNDING_DENOMINATOR)
    finite_upper = step * F(upper_units, C_ROUNDING_DENOMINATOR)
    tail_lower = 1 / (
        2
        * C_R**2
        * (6 + F(9, 2) / C_R + F(1, 16) / C_R**2 + F(9, 64) / C_R**3)
    )
    tail_upper = 1 / (12 * C_R**2)
    total_lower = finite_lower + tail_lower
    total_upper = finite_upper + tail_upper
    if not 0 < total_lower < total_upper:
        raise RuntimeError("invalid exact C enclosure")
    return {
        "R": str(C_R),
        "rectangles": C_RECTANGLES,
        "step": str(step),
        "rounding_bits": C_ROUNDING_BITS,
        "finite_lower": fraction_record(finite_lower),
        "finite_upper": fraction_record(finite_upper),
        "tail_lower": fraction_record(tail_lower),
        "tail_upper": fraction_record(tail_upper),
        "C_lower": fraction_record(total_lower),
        "C_upper": fraction_record(total_upper),
        "width": fraction_record(total_upper - total_lower),
    }


def alternating_atan_enclosure(x: F, terms: int = SERIES_TERMS) -> tuple[F, F]:
    partial = sum(((-1) ** n * x ** (2 * n + 1) / (2 * n + 1) for n in range(terms)), F(0))
    remainder = x ** (2 * terms + 1) / (2 * terms + 1)
    if terms % 2 == 0:
        return partial, partial + remainder
    return partial - remainder, partial


def atanh_log_enclosure(y: F, terms: int = SERIES_TERMS) -> tuple[F, F]:
    """Enclose log((1+y)/(1-y)) for 0<y<1 by a positive series."""
    partial = 2 * sum((y ** (2 * n + 1) / (2 * n + 1) for n in range(terms)), F(0))
    tail = 2 * y ** (2 * terms + 1) / ((2 * terms + 1) * (1 - y**2))
    return partial, partial + tail


def exponential_enclosure(x: F, degree: int = EXP_DEGREE) -> tuple[F, F]:
    if not 0 <= x < degree + 2:
        raise ValueError("Taylor-geometric exponential enclosure domain violated")
    term = F(1)
    lower = term
    for index in range(1, degree + 1):
        term *= x / index
        lower += term
    first_omitted = term * x / (degree + 1)
    upper = lower + first_omitted / (1 - x / (degree + 2))
    return lower, upper


def boundary_certificates(c_enclosure: dict) -> dict:
    c_lower = F(c_enclosure["C_lower"]["exact"])
    c_upper = F(c_enclosure["C_upper"]["exact"])

    atan5_lower, atan5_upper = alternating_atan_enclosure(F(1, 5))
    atan239_lower, atan239_upper = alternating_atan_enclosure(F(1, 239))
    pi_lower = 16 * atan5_lower - 4 * atan239_upper
    pi_upper = 16 * atan5_upper - 4 * atan239_lower
    log3_lower, log3_upper = atanh_log_enclosure(F(1, 2))
    tabs_lower = (3 * pi_lower - 2 * log3_upper) / 5
    tabs_upper = (3 * pi_upper - 2 * log3_lower) / 5

    z_lower = F(1980, 1000)
    z_upper = F(1981, 1000)

    def q(z: F) -> F:
        return 2 * z**2 / (1 + z**2)

    exp_q_lower = exponential_enclosure(q(z_lower))[0]
    exp_q_upper = exponential_enclosure(q(z_upper))[1]
    g_lower_positive = exp_q_lower > 1 + z_lower**2
    g_upper_negative = exp_q_upper < 1 + z_upper**2

    log_upper_target = F(1595, 1000)
    exp_log_target_lower = exponential_enclosure(log_upper_target)[0]
    log_upper_certified = exp_log_target_lower > 1 + z_upper**2
    h_upper = log_upper_target / z_lower

    sqrt_bounds = ((F(1, 2), F(875, 1000)), (F(19, 20), F(1206, 1000)), (F(1), F(1238, 1000)))
    cap_targets = {F(1, 2): F(705, 1000), F(19, 20): F(972, 1000), F(1): F(1)}
    cap_checks = []
    for policy, sqrt_upper in sqrt_bounds:
        sqrt_check = policy * c_upper < sqrt_upper**2
        cap_value = sqrt_upper * h_upper
        cap_target = cap_targets[policy]
        cap_checks.append({
            "policy": str(policy),
            "sqrt_pC_upper": fraction_record(sqrt_upper),
            "sqrt_bound_certified": sqrt_check,
            "horizon_upper": fraction_record(cap_value),
            "target": fraction_record(cap_target),
            "target_certified": cap_value < cap_target,
        })

    prior = json.loads(PRIOR_FLAT_RESULT.read_text())
    prior_c = prior["exact_certificate"]["integral_enclosure"]
    prior_match = all(
        prior_c[key]["exact"] == c_enclosure[key]["exact"]
        for key in ("finite_lower", "finite_upper", "tail_lower", "tail_upper", "C_lower", "C_upper", "width")
    )
    checks = {
        "pi_nonempty": pi_lower < pi_upper,
        "log3_nonempty": log3_lower < log3_upper,
        "Tabs_nonempty": tabs_lower < tabs_upper,
        "g_at_1p980_positive": g_lower_positive,
        "g_at_1p981_negative": g_upper_negative,
        "log_1_plus_1p981_sq_lt_1p595": log_upper_certified,
        "all_sqrt_and_cap_checks": all(
            row["sqrt_bound_certified"] and row["target_certified"] for row in cap_checks
        ),
        "prior_C_witness_exact_match": prior_match,
    }
    if not all(checks.values()):
        raise RuntimeError(f"exact boundary certificate failed: {checks}")
    return {
        "schema_version": 1,
        "run_date": RUN_DATE,
        "completion_date": COMPLETION_DATE,
        "evidence_class": "exact rational inequalities with conventional series remainder arguments",
        "C_enclosure": c_enclosure,
        "absolute_boundary": {
            "formula": "(3*pi-2*log(3))/5",
            "pi_lower": fraction_record(pi_lower),
            "pi_upper": fraction_record(pi_upper),
            "log3_lower": fraction_record(log3_lower),
            "log3_upper": fraction_record(log3_upper),
            "T_abs_lower": fraction_record(tabs_lower),
            "T_abs_upper": fraction_record(tabs_upper),
            "series_terms": SERIES_TERMS,
        },
        "common_rate_horizon": {
            "z_star_bracket": [fraction_record(z_lower), fraction_record(z_upper)],
            "sign_method": "compare exp(2*z^2/(1+z^2)) with 1+z^2 using rational Taylor bounds",
            "log_upper": fraction_record(log_upper_target),
            "h_z_star_upper": fraction_record(h_upper),
            "cap_checks": cap_checks,
            "exp_degree": EXP_DEGREE,
        },
        "checks": checks,
        "limitations": [
            "The analytical identities and uniqueness arguments are supplied by 04-theory.md.",
            "These certificates do not validate floating ODE, optimizer, Monte Carlo, or PDE outputs.",
        ],
    }


def baseline_theta_enclosure(kind: str, horizon: F) -> tuple[F, F, str]:
    if kind == "rate-1":
        rate = F(1)
        exp_lower, exp_upper = exponential_enclosure(rate * horizon)
        return (exp_lower - 1) / rate**2, (exp_upper - 1) / rate**2, "1"
    if kind == "rate-0.745":
        rate = F(149, 200)
        exp_lower, exp_upper = exponential_enclosure(rate * horizon)
        return (exp_lower - 1) / rate**2, (exp_upper - 1) / rate**2, "149/200"
    if kind == "paper-5pct":
        log_lower, log_upper = atanh_log_enclosure(F(1, 39))
        numerator = horizon**2 / 19
        return numerator / log_upper**2, numerator / log_lower**2, "log(20/19)/T"
    raise ValueError(kind)


def exact_baseline_classification(kind: str, horizon: float, policy: float,
                                  c_lower: F, c_upper: F) -> dict:
    h = F(str(horizon))
    p = F(str(policy))
    theta_lower, theta_upper, rate_exact = baseline_theta_enclosure(kind, h)
    threshold_lower = p * c_lower
    threshold_upper = p * c_upper
    if theta_upper < threshold_lower:
        classification = "finite"
    elif theta_lower >= threshold_upper:
        classification = "divergent"
    else:
        classification = "inconclusive"
    return {
        "classification": classification,
        "rate_exact": rate_exact,
        "theta_lower": fraction_record(theta_lower),
        "theta_upper": fraction_record(theta_upper),
        "pC_lower": fraction_record(threshold_lower),
        "pC_upper": fraction_record(threshold_upper),
        "rule": "finite if theta_upper<pC_lower; divergent if theta_lower>=pC_upper",
    }


def rate_value(kind: str, horizon: float) -> float:
    if kind == "rate-1":
        return 1.0
    if kind == "rate-0.745":
        return 0.745
    if kind == "paper-5pct":
        return -math.log(0.95) / horizon
    raise ValueError(kind)


def raw_threshold(rate: float, policy: float, c_value: float) -> float:
    return math.log1p(rate * rate * policy * c_value) / rate


def raw_moment_rhs(rate: float, policy: float) -> Callable[[float, np.ndarray], np.ndarray]:
    def rhs(_time: float, y: np.ndarray) -> np.ndarray:
        identity, a, b, c, e = y
        return rate * y + np.array((a, a * b / policy, a * c / policy, a * e / policy, 0.0)) / rate
    return rhs


def solve_raw_moment(rate: float, policy: float, horizon: float, rtol: float) -> dict:
    from scipy.integrate import solve_ivp

    y0 = np.array((0.25, 9.0 / 64.0, 1.0 / 16.0, 9.0, 36.0))
    solution = solve_ivp(
        raw_moment_rhs(rate, policy),
        (0.0, horizon),
        y0,
        method="DOP853",
        rtol=rtol,
        atol=rtol * 1.0e-2,
        t_eval=(horizon,),
    )
    if not solution.success or solution.y.shape != (5, 1) or not np.isfinite(solution.y).all():
        return {"success": False, "message": solution.message, "nfev": int(solution.nfev)}
    values = solution.y[:, -1]
    return {
        "success": True,
        "values": values.tolist(),
        "root_second_moment": float(values[0]),
        "nfev": int(solution.nfev),
        "rtol": rtol,
        "atol": rtol * 1.0e-2,
    }


def scalar_raw_reconstruction(rate: float, policy: float, horizon: float, rtol: float) -> dict:
    from scipy.integrate import solve_ivp

    def rhs(time_value: float, state: np.ndarray) -> np.ndarray:
        v = float(state[0])
        polynomial = 9.0 / 64.0 + v / 16.0 + 4.5 * v**2 + 6.0 * v**3
        return np.array((
            math.exp(rate * time_value) * polynomial / (rate * policy),
            polynomial / rate,
        ))

    solution = solve_ivp(
        rhs, (0.0, horizon), np.array((0.0, 0.25)), method="DOP853",
        rtol=rtol, atol=rtol * 1.0e-2, t_eval=(horizon,),
    )
    if not solution.success or not np.isfinite(solution.y).all():
        return {"success": False, "message": solution.message}
    v = float(solution.y[0, -1])
    identity_tilde = float(solution.y[1, -1])
    scale = math.exp(rate * horizon)
    reconstructed = scale * np.array((
        identity_tilde,
        9.0 / 64.0 + v / 16.0 + 4.5 * v**2 + 6.0 * v**3,
        1.0 / 16.0 + 9.0 * v + 18.0 * v**2,
        9.0 + 36.0 * v,
        36.0,
    ))
    return {
        "success": True,
        "v": v,
        "identity_after_integrating_factor": identity_tilde,
        "values": reconstructed.tolist(),
    }


def full_scalar_check(full: dict, scalar: dict) -> dict:
    if not full.get("success") or not scalar.get("success"):
        return {"available": False}
    left = np.asarray(full["values"])
    right = np.asarray(scalar["values"])
    difference = np.abs(left - right)
    return {
        "available": True,
        "max_abs_difference": float(np.max(difference)),
        "max_relative_difference": float(np.max(difference / np.maximum(1.0, np.abs(left)))),
    }


def common_mean(horizon: float) -> float:
    return 1.0 / math.sqrt(1.0 + 3.0 * math.exp(-2.0 * horizon))


def feasible_rate_interval(horizon: float, policy: float, c_value: float) -> dict:
    from scipy.optimize import brentq, minimize_scalar

    def threshold_log(log_rate: float) -> float:
        return raw_threshold(math.exp(log_rate), policy, c_value)

    maximum = minimize_scalar(
        lambda value: -threshold_log(value), bounds=(-12.0, 8.0), method="bounded",
        options={"xatol": 1.0e-13},
    )
    best_rate = math.exp(float(maximum.x))
    best_horizon = -float(maximum.fun)
    result = {"maximum_rate": best_rate, "maximum_horizon": best_horizon}
    if horizon >= best_horizon:
        result.update({"feasible": False, "reason": "horizon_at_or_above_floating_maximum"})
        return result

    def equation(log_rate: float) -> float:
        return threshold_log(log_rate) - horizon

    lower_log = brentq(equation, -30.0, math.log(best_rate), xtol=1.0e-14)
    upper_endpoint = max(math.log(best_rate) + 1.0, 2.0)
    while equation(upper_endpoint) > 0.0:
        upper_endpoint += 2.0
        if upper_endpoint > 30.0:
            raise RuntimeError("failed to bracket upper finite-rate boundary")
    upper_log = brentq(equation, math.log(best_rate), upper_endpoint, xtol=1.0e-14)
    result.update({
        "feasible": True,
        "lower_rate": math.exp(lower_log),
        "upper_rate": math.exp(upper_log),
        "lower_log_rate": lower_log,
        "upper_log_rate": upper_log,
        "boundary_status": "floating roots of the exact T2 formula using quadrature C",
    })
    return result


def optimize_raw_rate(horizon: float, policy: float, c_value: float,
                      interval: dict) -> dict:
    from scipy.optimize import minimize_scalar

    if not interval["feasible"]:
        return {"status": "infeasible", "interval": interval}
    lower = float(interval["lower_log_rate"])
    upper = float(interval["upper_log_rate"])
    margin = max(1.0e-9, (upper - lower) * 1.0e-7)
    bounds = (lower + margin, upper - margin)

    evaluations = 0
    failures = 0

    def objective(log_rate: float, rtol: float) -> float:
        nonlocal evaluations, failures
        evaluations += 1
        solved = solve_raw_moment(math.exp(log_rate), policy, horizon, rtol)
        if not solved.get("success"):
            failures += 1
            return math.inf
        return float(solved["root_second_moment"])

    first = minimize_scalar(
        lambda value: objective(value, 1.0e-8), bounds=bounds, method="bounded",
        options={"xatol": 1.0e-8, "maxiter": 160},
    )
    second = minimize_scalar(
        lambda value: objective(value, 1.0e-10), bounds=bounds, method="bounded",
        options={"xatol": 1.0e-10, "maxiter": 220},
    )
    if not first.success or not second.success or not math.isfinite(float(second.fun)):
        return {
            "status": "numerical_failure", "interval": interval,
            "first_message": first.message, "second_message": second.message,
            "evaluations": evaluations, "failed_evaluations": failures,
        }
    first_rate = math.exp(float(first.x))
    rate = math.exp(float(second.x))
    loose = solve_raw_moment(rate, policy, horizon, 1.0e-8)
    tight = solve_raw_moment(rate, policy, horizon, 1.0e-10)
    scalar = scalar_raw_reconstruction(rate, policy, horizon, 1.0e-10)
    return {
        "status": "computed",
        "interval": interval,
        "rate": rate,
        "root_second_moment": tight.get("root_second_moment"),
        "variance": (
            tight["root_second_moment"] - common_mean(horizon) ** 2
            if tight.get("success") else None
        ),
        "first_pass": {
            "xatol": 1.0e-8, "ode_rtol": 1.0e-8,
            "rate": first_rate, "root_second_moment": float(first.fun),
        },
        "refined_pass": {
            "xatol": 1.0e-10, "ode_rtol": 1.0e-10,
            "rate": rate, "root_second_moment": float(second.fun),
        },
        "refinement": {
            "rate_difference": abs(rate - first_rate),
            "objective_difference": abs(float(second.fun) - float(first.fun)),
            "same_rate_ode_tolerance_difference": (
                abs(tight["root_second_moment"] - loose["root_second_moment"])
                if tight.get("success") and loose.get("success") else None
            ),
        },
        "scalar_reconstruction_check": full_scalar_check(tight, scalar),
        "evaluations": evaluations,
        "failed_evaluations": failures,
        "evidence_class": "floating bounded scalar optimization in log(rate)",
    }


def absolute_moment_rows(tabs_lower: F, tabs_upper: F) -> tuple[list[dict], dict]:
    from scipy.integrate import quad, solve_ivp
    import mpmath as mp

    tabs_closed = (3.0 * math.pi - 2.0 * math.log(3.0)) / 5.0
    tabs_quad, tabs_quad_error = quad(
        lambda value: 1.0 / ((value + 1.5) * (value * value + 0.25)),
        0.0, math.inf, epsabs=1.0e-13, epsrel=1.0e-13, limit=300,
    )
    finite_horizons = [
        horizon for horizon in RAW_HORIZONS if F(str(horizon)) < tabs_lower
    ]
    solutions: dict[float, float] = {}
    if finite_horizons:
        solution = solve_ivp(
            lambda _time, state: np.array((abs_polynomial(float(state[0])),)),
            (0.0, max(finite_horizons)), np.array((0.0,)), method="DOP853",
            rtol=1.0e-11, atol=1.0e-13, t_eval=finite_horizons,
        )
        if not solution.success or not np.isfinite(solution.y).all():
            raise RuntimeError(f"absolute scalar ODE failed: {solution.message}")
        solutions = {
            horizon: float(value) for horizon, value in zip(finite_horizons, solution.y[0])
        }
    rows = []
    for horizon in RAW_HORIZONS:
        exact_horizon = F(str(horizon))
        if exact_horizon < tabs_lower:
            classification = "finite"
            s_value = solutions[horizon]
            delta = tabs_closed - horizon
            lower_bound = max(0.5, 1.0 / math.sqrt(2.0 * delta) - 1.0)
            rows.append({
                "horizon": horizon,
                "classification": classification,
                "s": s_value,
                "absolute_moment": 0.5 + s_value,
                "near_boundary_lower_bound": lower_bound,
            })
        elif exact_horizon >= tabs_upper:
            rows.append({
                "horizon": horizon,
                "classification": "nonintegrable",
                "s": None,
                "absolute_moment": "infinity",
            })
        else:
            rows.append({
                "horizon": horizon,
                "classification": "inconclusive_from_rational_interval",
                "s": None,
                "absolute_moment": None,
            })
    closed_binary64 = F.from_float(tabs_closed)
    quadrature_binary64 = F.from_float(tabs_quad)
    quadrature_error_lower = F.from_float(tabs_quad - tabs_quad_error)
    quadrature_error_upper = F.from_float(tabs_quad + tabs_quad_error)
    with mp.workdps(100):
        tabs_high_precision = (3 * mp.pi - 2 * mp.log(3)) / 5
        rational_lower_mp = mp.mpf(tabs_lower.numerator) / tabs_lower.denominator
        rational_upper_mp = mp.mpf(tabs_upper.numerator) / tabs_upper.denominator
        high_precision_inside = rational_lower_mp <= tabs_high_precision <= rational_upper_mp
        high_precision_record = {
            "decimal_100_digit_working_precision": mp.nstr(tabs_high_precision, 90),
            "inside_exact_rational_interval": bool(high_precision_inside),
            "distance_above_lower": mp.nstr(tabs_high_precision - rational_lower_mp, 20),
            "distance_below_upper": mp.nstr(rational_upper_mp - tabs_high_precision, 20),
            "role": "high-precision floating diagnostic; the rational series bounds are the certificate",
        }
    checks = {
        "closed_form": tabs_closed,
        "improper_quadrature": tabs_quad,
        "quadrature_reported_error": tabs_quad_error,
        "closed_minus_quadrature_abs": abs(tabs_closed - tabs_quad),
        "exact_interval_width": fraction_record(tabs_upper - tabs_lower),
        "binary64_closed_inside_exact_rational_interval": tabs_lower <= closed_binary64 <= tabs_upper,
        "binary64_quadrature_inside_exact_rational_interval": tabs_lower <= quadrature_binary64 <= tabs_upper,
        "quadrature_reported_error_interval_intersects_exact_interval": (
            quadrature_error_lower <= tabs_upper and quadrature_error_upper >= tabs_lower
        ),
        "high_precision_closed_form": high_precision_record,
        "exact_interval_midpoint_float": float((tabs_lower + tabs_upper) / 2),
        "closed_minus_exact_midpoint_abs": abs(
            tabs_closed - float((tabs_lower + tabs_upper) / 2)
        ),
        "quadrature_minus_exact_midpoint_abs": abs(
            tabs_quad - float((tabs_lower + tabs_upper) / 2)
        ),
        "closed_quadrature_agree_within_1e-12": abs(tabs_closed - tabs_quad) <= 1.0e-12,
        "closed_exact_midpoint_agree_within_1e-12": abs(
            tabs_closed - float((tabs_lower + tabs_upper) / 2)
        ) <= 1.0e-12,
        "note": (
            "The exact rational interval is narrower than binary64 spacing; "
            "the two binary64 enclosure observations are retained as false rather than "
            "treated as certificate failures. The high-precision value and quadrature "
            "error bar are separate numerical diagnostics."
        ),
    }
    return rows, checks


def flat_diagnostics(boundary: dict, run_log: list[str]) -> dict:
    from scipy.integrate import quad

    c_info = boundary["C_enclosure"]
    c_lower = F(c_info["C_lower"]["exact"])
    c_upper = F(c_info["C_upper"]["exact"])
    c_quad, c_quad_error = quad(
        lambda value: 1.0 / (9.0 / 64.0 + value / 16.0 + 4.5 * value**2 + 6.0 * value**3),
        0.0, math.inf, epsabs=1.0e-13, epsrel=1.0e-13, limit=300,
    )
    tabs_lower = F(boundary["absolute_boundary"]["T_abs_lower"]["exact"])
    tabs_upper = F(boundary["absolute_boundary"]["T_abs_upper"]["exact"])
    absolute_rows, absolute_checks = absolute_moment_rows(tabs_lower, tabs_upper)
    absolute_by_horizon = {row["horizon"]: row for row in absolute_rows}

    flat_rows = []
    baseline_kinds = ("rate-1", "rate-0.745", "paper-5pct")
    numerical_failures = []
    for policy in POLICIES:
        for horizon in RAW_HORIZONS:
            mean = common_mean(horizon)
            row = {
                "policy": policy,
                "horizon": horizon,
                "common_mean": mean,
                "common_mean_square": mean**2,
                "absolute_moment": absolute_by_horizon[horizon],
                "baselines": [],
            }
            for kind in baseline_kinds:
                rate = rate_value(kind, horizon)
                exact = exact_baseline_classification(kind, horizon, policy, c_lower, c_upper)
                threshold = raw_threshold(rate, policy, c_quad)
                floating_class = "finite" if horizon < threshold else "divergent"
                baseline = {
                    "kind": kind,
                    "rate": rate,
                    "threshold": threshold,
                    "exact_classification": exact,
                    "floating_classification": floating_class,
                    "moment": None,
                }
                if exact["classification"] != "divergent" and floating_class == "finite":
                    solved = solve_raw_moment(rate, policy, horizon, 1.0e-10)
                    scalar = scalar_raw_reconstruction(rate, policy, horizon, 1.0e-10)
                    if solved.get("success"):
                        baseline["moment"] = solved
                        baseline["variance"] = solved["root_second_moment"] - mean**2
                        baseline["scalar_reconstruction_check"] = full_scalar_check(solved, scalar)
                    else:
                        numerical_failures.append({
                            "kind": "raw_baseline_ode", "policy": policy,
                            "horizon": horizon, "rate_kind": kind, "detail": solved,
                        })
                row["baselines"].append(baseline)

            interval = feasible_rate_interval(horizon, policy, c_quad)
            optimizer = optimize_raw_rate(horizon, policy, c_quad, interval)
            row["optimizer"] = optimizer
            if optimizer["status"] == "numerical_failure":
                numerical_failures.append({
                    "kind": "raw_optimizer", "policy": policy,
                    "horizon": horizon, "detail": optimizer,
                })
            flat_rows.append(row)
            run_log.append(
                f"flat p={policy:g} T={horizon:g}: optimizer={optimizer['status']}"
            )
    thresholds = {
        "C_quadrature": c_quad,
        "C_quadrature_reported_error": c_quad_error,
        "C_quadrature_inside_exact_enclosure": float(c_lower) <= c_quad <= float(c_upper),
        "absolute": boundary["absolute_boundary"],
        "common_rate_exact_caps": boundary["common_rate_horizon"],
    }
    return {
        "flat_rows": flat_rows,
        "absolute_rows": absolute_rows,
        "absolute_checks": absolute_checks,
        "thresholds": thresholds,
        "numerical_failures": numerical_failures,
    }


def sample_raw_trees(boundary: dict, run_log: list[str]) -> tuple[list[dict], dict[str, np.ndarray], list[dict]]:
    if str(PROJECT) not in sys.path:
        sys.path.insert(0, str(PROJECT))
    from parabolab.library import allen_cahn_flat
    from parabolab.tree import sample_tree

    tabs_lower = F(boundary["absolute_boundary"]["T_abs_lower"]["exact"])
    tabs_upper = F(boundary["absolute_boundary"]["T_abs_upper"]["exact"])
    c_lower = F(boundary["C_enclosure"]["C_lower"]["exact"])
    c_upper = F(boundary["C_enclosure"]["C_upper"]["exact"])
    arrays: dict[str, np.ndarray] = {}
    rows = []
    failures = []
    for row_index, horizon in enumerate(RAW_SAMPLE_HORIZONS):
        seed = RAW_SAMPLE_SEED_BASE + row_index
        rng = np.random.default_rng(seed)
        pde = allen_cahn_flat(phi0=0.5, T=horizon)
        values = np.full(RAW_SAMPLE_COUNT, np.nan)
        nodes = np.full(RAW_SAMPLE_COUNT, -1, dtype=np.int64)
        failed = np.zeros(RAW_SAMPLE_COUNT, dtype=np.bool_)
        errors: list[dict] = []
        started = time.perf_counter()
        for sample_index in range(RAW_SAMPLE_COUNT):
            try:
                sample = sample_tree(
                    pde, 0.0, 0.0, rng=rng, rate=1.0,
                    prune_zero=True, max_depth=None, tuple_proposal=None,
                )
                values[sample_index] = sample.value
                nodes[sample_index] = sample.n_nodes
            except Exception as error:
                failed[sample_index] = True
                errors.append({
                    "sample_index": sample_index,
                    "type": type(error).__name__,
                    "message": str(error),
                })
        nonfinite = ~np.isfinite(values)
        complete = not bool(np.any(failed | nonfinite))
        variance_certificate = exact_baseline_classification(
            "rate-1", horizon, 0.5, c_lower, c_upper
        )
        variance_regime = {
            "finite": "finite",
            "divergent": "infinite",
            "inconclusive": "inconclusive",
        }[variance_certificate["classification"]]
        exact_horizon = F(str(horizon))
        if exact_horizon < tabs_lower:
            absolute_regime = "finite"
        elif exact_horizon >= tabs_upper:
            absolute_regime = "nonintegrable"
        else:
            absolute_regime = "inconclusive"
        finite_variance_certified = variance_regime == "finite"
        ordinary_clt_assumptions_available = complete and finite_variance_certified
        prefix = f"h_{str(horizon).replace('.', 'p')}"
        arrays[f"{prefix}_values"] = values
        arrays[f"{prefix}_nodes"] = nodes
        arrays[f"{prefix}_failed"] = failed
        arrays[f"{prefix}_nonfinite"] = nonfinite
        row = {
            "horizon": horizon,
            "rate": 1.0,
            "policy": "raw-uniform-existing-exact-zero-code-pruning",
            "seed": seed,
            "scheduled_samples": RAW_SAMPLE_COUNT,
            "completed_finite_samples": int(np.count_nonzero(~failed & ~nonfinite)),
            "failed_samples": int(np.count_nonzero(failed)),
            "nonfinite_samples": int(np.count_nonzero(nonfinite)),
            "all_prescheduled_roots_finite": complete,
            "variance_regime": variance_regime,
            "variance_regime_certificate": variance_certificate,
            "absolute_integrability_regime": absolute_regime,
            "finite_variance_certified": finite_variance_certified,
            "ordinary_clt_assumptions_available": ordinary_clt_assumptions_available,
            "confidence_statement": (
                "ordinary sample summaries are diagnostic only"
                if not ordinary_clt_assumptions_available else
                "finite-variance regime and complete batch; summaries remain diagnostics, not a claim that this particular sample is reliable"
            ),
            "mean": float(np.mean(values)) if complete else None,
            "sample_variance": float(np.var(values, ddof=1)) if complete else None,
            "mean_nodes": float(np.mean(nodes)) if complete else None,
            "max_nodes": int(np.max(nodes)) if complete else None,
            "root_branching_fraction": float(np.mean(nodes > 1)) if complete else None,
            "runtime_seconds": time.perf_counter() - started,
            "array_prefix": prefix,
            "errors": errors,
        }
        rows.append(row)
        if errors or np.any(nonfinite):
            failures.append({
                "kind": "raw_sampling", "horizon": horizon,
                "errors": errors, "nonfinite_indices": np.flatnonzero(nonfinite).tolist(),
            })
        run_log.append(
            f"raw sample T={horizon:g}: finite={row['completed_finite_samples']}/{RAW_SAMPLE_COUNT}, "
            f"nodes_mean={row['mean_nodes']}, finite_variance_certified={finite_variance_certified}"
        )
    return rows, arrays, failures


def wave_terminal_vector(x: np.ndarray) -> np.ndarray:
    s = 1.0 / (1.0 + np.exp(x))
    return np.vstack((
        s**2,
        s**2 * (1.0 - s) ** 2,
        s**2 * (1.0 - s**2) ** 2,
        (1.0 - 3.0 * s**2) ** 2,
        36.0 * s**2,
        np.full_like(s, 36.0),
    ))


def wave_branch_field(y: np.ndarray, policy: tuple[float, float, float]) -> np.ndarray:
    _, derivative, f0, f1, f2, f3 = y
    p0, p1, p2 = policy
    out = np.empty_like(y)
    out[0] = f0
    out[1] = f1 * derivative
    out[2] = f0 * f1 / p0 + derivative**2 * f2 / (4.0 * (1.0 - p0))
    out[3] = f0 * f2 / p1 + derivative**2 * f3 / (4.0 * (1.0 - p1))
    out[4] = f0 * f3 / p2
    out[5] = 0.0
    return out


def wave_exact_mean(remaining_time: float, x: float = 0.0) -> float:
    return -0.5 - 0.5 * math.tanh(0.75 * remaining_time - 0.5 * x)


def solve_wave_configuration(rate: float, policy_name: str,
                             policy: tuple[float, float, float], dx: float) -> dict:
    intervals = round(2.0 * WAVE_HALF_WIDTH / dx)
    x = np.linspace(-WAVE_HALF_WIDTH, WAVE_HALF_WIDTH, intervals + 1)
    y = wave_terminal_vector(x)
    reconstruction_error = float(np.max(np.abs(y - wave_terminal_vector(x))))
    root_index = intervals // 2
    hit_unit = min(WAVE_HORIZONS)
    steps_per_unit = math.ceil(hit_unit / (0.2 * dx**2))
    dt = hit_unit / steps_per_unit
    total_steps = round(max(WAVE_HORIZONS) / dt)
    hit_steps = {round(horizon / dt): horizon for horizon in WAVE_HORIZONS}
    rows_by_horizon: dict[float, dict] = {}
    max_component = float(np.max(np.abs(y)))
    minimum_component = float(np.min(y))
    stop_time = None
    stop_cause = None
    stopping_observed_max_component = None
    started = time.perf_counter()

    def rhs(state: np.ndarray, remaining_time: float) -> np.ndarray:
        staged = state.copy()
        scale = math.exp(rate * remaining_time)
        staged[:, 0] = LEFT_LIMIT * scale
        staged[:, -1] = RIGHT_LIMIT * scale
        result = np.zeros_like(staged)
        laplacian = (staged[:, 2:] - 2.0 * staged[:, 1:-1] + staged[:, :-2]) / dx**2
        result[:, 1:-1] = (
            0.5 * laplacian
            + rate * staged[:, 1:-1]
            + wave_branch_field(staged[:, 1:-1], policy) / rate
        )
        return result

    for step in range(1, total_steps + 1):
        remaining = (step - 1) * dt
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            k1 = rhs(y, remaining)
            k2 = rhs(y + 0.5 * dt * k1, remaining + 0.5 * dt)
            k3 = rhs(y + 0.5 * dt * k2, remaining + 0.5 * dt)
            k4 = rhs(y + dt * k3, remaining + dt)
            candidate = y + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        current_time = step * dt
        scale = math.exp(rate * current_time)
        candidate[:, 0] = LEFT_LIMIT * scale
        candidate[:, -1] = RIGHT_LIMIT * scale
        if not np.isfinite(candidate).all():
            stop_time = current_time
            stop_cause = "nonfinite_component"
            break
        candidate_max = float(np.max(np.abs(candidate)))
        if candidate_max > WAVE_STOP:
            stop_time = current_time
            stop_cause = "component_exceeded_1e12"
            stopping_observed_max_component = candidate_max
            break
        y = candidate
        max_component = max(max_component, candidate_max)
        minimum_component = min(minimum_component, float(np.min(y)))
        if step in hit_steps:
            horizon = hit_steps[step]
            mean = wave_exact_mean(horizon)
            expected_f3 = 36.0 * math.exp(rate * horizon)
            root_second = float(y[0, root_index])
            rows_by_horizon[horizon] = {
                "horizon": horizon,
                "status": "reached",
                "root_second_moment": root_second,
                "root_variance": root_second - mean**2,
                "exact_mean": mean,
                "maximum_field_component_through_horizon": max_component,
                "minimum_field_component_through_horizon": minimum_component,
                "f3_max_abs_error": float(np.max(np.abs(y[5] - expected_f3))),
                "f3_max_relative_error": float(np.max(np.abs(y[5] - expected_f3)) / expected_f3),
            }

    runtime = time.perf_counter() - started
    rows = []
    for horizon in WAVE_HORIZONS:
        if horizon in rows_by_horizon:
            row = rows_by_horizon[horizon]
        else:
            row = {
                "horizon": horizon,
                "status": "not_reached",
                "root_second_moment": None,
                "root_variance": None,
                "exact_mean": wave_exact_mean(horizon),
                "maximum_field_component_through_horizon": None,
                "minimum_field_component_through_horizon": None,
                "f3_max_abs_error": None,
                "f3_max_relative_error": None,
            }
        row.update({
            "rate": rate,
            "policy": policy_name,
            "probabilities": list(policy),
            "dx": dx,
            "domain": [-WAVE_HALF_WIDTH, WAVE_HALF_WIDTH],
            "points": intervals + 1,
            "dt": dt,
            "dt_over_dx_squared": dt / dx**2,
            "configuration_runtime_seconds": runtime,
            "stopping_time": stop_time,
            "stopping_cause": stop_cause,
        })
        rows.append(row)
    return {
        "rows": rows,
        "stopping_time": stop_time,
        "stopping_cause": stop_cause,
        "stopping_observed_max_component": stopping_observed_max_component,
        "last_valid_max_component": max_component,
        "last_valid_minimum_component": minimum_component,
        "runtime_seconds": runtime,
        "zero_time_reconstruction_max_abs_error": reconstruction_error,
        "dt": dt,
        "dt_over_dx_squared": dt / dx**2,
    }


def wave_diagnostics(run_log: list[str]) -> tuple[dict, list[dict]]:
    rows = []
    configurations = []
    failures = []
    for rate in WAVE_RATES:
        for policy_name, policy in WAVE_POLICIES.items():
            for dx in WAVE_DX:
                result = solve_wave_configuration(rate, policy_name, policy, dx)
                rows.extend(result.pop("rows"))
                result.update({"rate": rate, "policy": policy_name, "dx": dx})
                configurations.append(result)
                if result["stopping_cause"] is not None:
                    failures.append({
                        "kind": "wave_safety_stop", "rate": rate,
                        "policy": policy_name, "dx": dx,
                        "stopping_time": result["stopping_time"],
                        "cause": result["stopping_cause"],
                        "stopping_observed_max_component": result["stopping_observed_max_component"],
                    })
                run_log.append(
                    f"wave rate={rate:g} policy={policy_name} dx={dx:g}: "
                    f"stop={result['stopping_cause']} at {result['stopping_time']}"
                )
    keyed = {(row["rate"], row["policy"], row["horizon"], row["dx"]): row for row in rows}
    discrepancies = []
    for rate in WAVE_RATES:
        for policy_name in WAVE_POLICIES:
            for horizon in WAVE_HORIZONS:
                coarse = keyed[(rate, policy_name, horizon, 0.1)]
                fine = keyed[(rate, policy_name, horizon, 0.05)]
                if coarse["status"] == fine["status"] == "reached":
                    difference = abs(coarse["root_second_moment"] - fine["root_second_moment"])
                    discrepancies.append({
                        "rate": rate, "policy": policy_name, "horizon": horizon,
                        "status": "available", "absolute_difference": difference,
                        "relative_to_fine": difference / max(1.0, abs(fine["root_second_moment"])),
                    })
                else:
                    discrepancies.append({
                        "rate": rate, "policy": policy_name, "horizon": horizon,
                        "status": "unavailable", "coarse_status": coarse["status"],
                        "fine_status": fine["status"],
                    })
    output = {
        "schema_version": 1,
        "run_date": RUN_DATE,
        "completion_date": COMPLETION_DATE,
        "evidence_class": "floating two-mesh finite-difference diagnostic; not a divergence proof or certificate",
        "coordinate_order": ["Id", "D", "F0", "F1", "F2", "F3"],
        "rows": rows,
        "configurations": configurations,
        "mesh_discrepancies": discrepancies,
        "validation": {
            "scheduled_rows": len(rows),
            "expected_rows": len(WAVE_RATES) * len(WAVE_POLICIES) * len(WAVE_DX) * len(WAVE_HORIZONS),
            "all_dt_within_limit": all(row["dt_over_dx_squared"] <= 0.2 + 1.0e-14 for row in rows),
            "max_zero_time_reconstruction_abs_error": max(
                row["zero_time_reconstruction_max_abs_error"] for row in configurations
            ),
            "safety_stop": WAVE_STOP,
        },
        "limitations": [
            "A safety stop is a numerical failure indicator, never proof of moment divergence.",
            "Finite-domain asymptotic boundary values and floating RK4/centered differences have discretization error.",
            "Static-supported probabilities have no general dominance guarantee on wave data.",
            "The best of the three tested rates is not a continuous-rate optimum.",
        ],
    }
    return output, failures


def provenance() -> dict:
    import scipy
    import mpmath

    sources = (SOURCE, PROTOCOL, WAVE_PROTOCOL, THEORY, TREE_SOURCE, LIBRARY_SOURCE, PRIOR_FLAT_SOURCE, PRIOR_FLAT_RESULT)
    return {
        "source_sha256": {str(path.relative_to(PROJECT)): sha256(path) for path in sources},
        "environment": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "numpy_version": np.__version__,
            "scipy_version": scipy.__version__,
            "mpmath_version": mpmath.__version__,
            "platform": platform.platform(),
        },
        "commands": {
            "generate": (
                "MPLCONFIGDIR=/tmp/parabolab-mpl /opt/miniconda3/envs/parabolab/bin/python "
                "docs/research/runs/2026-09-25-long-horizon/numerics/raw_experiment.py"
            ),
            "verify": (
                "MPLCONFIGDIR=/tmp/parabolab-mpl /opt/miniconda3/envs/parabolab/bin/python "
                "docs/research/runs/2026-09-25-long-horizon/numerics/raw_experiment.py --verify"
            ),
        },
    }


def generate() -> None:
    started = time.perf_counter()
    run_log = [
        f"run_date={RUN_DATE}",
        f"completion_date={COMPLETION_DATE}",
        "Lean gate passed before implementation: aggregate 3394 jobs; 11 standard axioms; no sorry.",
    ]
    protocol = json.loads(PROTOCOL.read_text())
    wave_protocol = json.loads(WAVE_PROTOCOL.read_text())
    if not protocol.get("frozen_before_numerical_implementation"):
        raise RuntimeError("raw protocol was not frozen before numerical implementation")
    if not wave_protocol.get("frozen_before_execution"):
        raise RuntimeError("wave protocol was not frozen before execution")

    c_enclosure = c_integral_enclosure()
    boundary = boundary_certificates(c_enclosure)
    boundary["provenance"] = provenance()
    json_dump(BOUNDARY_RESULT, boundary)
    run_log.append("exact boundary certificates: passed")

    flat = flat_diagnostics(boundary, run_log)
    scalar_differences = []
    for row in flat["flat_rows"]:
        for baseline in row["baselines"]:
            check = baseline.get("scalar_reconstruction_check")
            if check and check.get("available"):
                scalar_differences.append(check["max_relative_difference"])
        check = row["optimizer"].get("scalar_reconstruction_check")
        if check and check.get("available"):
            scalar_differences.append(check["max_relative_difference"])
    maximum_scalar_difference = max(scalar_differences, default=0.0)
    if maximum_scalar_difference > 1.0e-7:
        raise RuntimeError(
            f"five-field/scalar continuation check failed: {maximum_scalar_difference}"
        )
    run_log.append(
        f"five-field/scalar max relative difference={maximum_scalar_difference:.9g}"
    )
    raw_sampling_rows, arrays, sampling_failures = sample_raw_trees(boundary, run_log)
    np.savez_compressed(RAW_SAMPLES, **arrays)

    wave, wave_failures = wave_diagnostics(run_log)
    wave["provenance"] = provenance()
    json_dump(WAVE_RESULT, wave)

    all_failures = flat["numerical_failures"] + sampling_failures + wave_failures
    implementation_corrections = [{
        "stage": "first post-run audit before final regeneration",
        "initial_source_sha256": "b8018072ea3d6d2968e3e445303ba028ad0a06766456a15ae914cf4b10a761f4",
        "initial_raw_results_sha256": "83ad4b1d1091c64ac312a6e41f4c73618b35fe94d2ab8d73a10dc2173b2920bc",
        "failed_check": "scalar reconstruction of the Id coordinate",
        "initial_max_relative_discrepancy": 1.5381308990045512,
        "cause": (
            "The first independent check incorrectly reconstructed the integrating-factor "
            "Id coordinate as 1/4+p*v. Its correct auxiliary equation is "
            "d(Id_tilde)/dt=P(v)/lambda, while dv/dt=exp(lambda*t)*P(v)/(lambda*p)."
        ),
        "scope": (
            "The primary five-field ODE, feasibility formula, optimizers, and samples were "
            "unchanged; the erroneous independent comparison was corrected and every artifact regenerated."
        ),
    }]
    raw = {
        "schema_version": 1,
        "run_date": RUN_DATE,
        "completion_date": COMPLETION_DATE,
        "scope": "raw flat long-horizon moments, rate optimization, and retained raw sampling diagnostic",
        "flat_rows": flat["flat_rows"],
        "absolute_rows": flat["absolute_rows"],
        "raw_sampling_rows": raw_sampling_rows,
        "thresholds": flat["thresholds"],
        "checks": {
            "absolute": flat["absolute_checks"],
            "five_field_scalar_comparisons": len(scalar_differences),
            "five_field_scalar_max_relative_difference": maximum_scalar_difference,
            "five_field_scalar_tolerance": 1.0e-7,
            "five_field_scalar_check_passed": maximum_scalar_difference <= 1.0e-7,
            "raw_sample_array_count": len(arrays),
            "flat_row_count": len(flat["flat_rows"]),
            "failure_count": len(all_failures),
        },
        "retained_failures": all_failures,
        "implementation_corrections": implementation_corrections,
        "artifacts": {
            "raw_samples": {"path": RAW_SAMPLES.name, "sha256": sha256(RAW_SAMPLES)},
            "boundary_certificates": {"path": BOUNDARY_RESULT.name, "sha256": sha256(BOUNDARY_RESULT)},
            "wave_results": {"path": WAVE_RESULT.name, "sha256": sha256(WAVE_RESULT)},
        },
        "provenance": provenance(),
        "limitations": [
            "Finite sampled trees and sample variance do not establish integrability.",
            "No failed or nonfinite raw root is discarded when forming a batch statistic; if one occurs, full-batch mean and variance are unavailable.",
            "Floating rate optimization is diagnostic and is restricted to the analytical finite interval.",
            "Exact rational certificates cover only their stated scalar inequalities.",
        ],
    }
    json_dump(RAW_RESULT, raw)
    run_log.extend([
        "correction_retained=initial scalar Id reconstruction check failed; corrected auxiliary equation and regenerated",
        f"retained_failure_events={len(all_failures)}",
        f"raw_results_sha256={sha256(RAW_RESULT)}",
        f"raw_samples_sha256={sha256(RAW_SAMPLES)}",
        f"wave_results_sha256={sha256(WAVE_RESULT)}",
        f"boundary_certificates_sha256={sha256(BOUNDARY_RESULT)}",
        f"total_runtime_seconds={time.perf_counter() - started:.9f}",
        "status=completed",
    ])
    RUN_LOG.write_text("\n".join(run_log) + "\n")
    print("\n".join(run_log[-8:]))


def verify() -> bool:
    checks: dict[str, bool | int | str] = {}
    try:
        boundary_saved = json.loads(BOUNDARY_RESULT.read_text())
        c_enclosure = c_integral_enclosure()
        boundary_fresh = boundary_certificates(c_enclosure)
        checks["boundary_exact_recomputed"] = all(
            boundary_saved[key] == boundary_fresh[key]
            for key in ("C_enclosure", "absolute_boundary", "common_rate_horizon", "checks")
        )
        raw = json.loads(RAW_RESULT.read_text())
        wave = json.loads(WAVE_RESULT.read_text())
        checks["raw_samples_hash"] = raw["artifacts"]["raw_samples"]["sha256"] == sha256(RAW_SAMPLES)
        checks["boundary_hash"] = raw["artifacts"]["boundary_certificates"]["sha256"] == sha256(BOUNDARY_RESULT)
        checks["wave_hash"] = raw["artifacts"]["wave_results"]["sha256"] == sha256(WAVE_RESULT)
        current_sources = provenance()["source_sha256"]
        checks["raw_source_hashes"] = raw["provenance"]["source_sha256"] == current_sources
        checks["wave_source_hashes"] = wave["provenance"]["source_sha256"] == current_sources
        checks["boundary_source_hashes"] = boundary_saved["provenance"]["source_sha256"] == current_sources
        checks["flat_rows_complete"] = len(raw["flat_rows"]) == len(POLICIES) * len(RAW_HORIZONS)
        checks["raw_sampling_rows_complete"] = len(raw["raw_sampling_rows"]) == len(RAW_SAMPLE_HORIZONS)
        checks["wave_rows_complete"] = len(wave["rows"]) == len(WAVE_RATES) * len(WAVE_POLICIES) * len(WAVE_DX) * len(WAVE_HORIZONS)
        checks["boundary_checks_passed"] = all(boundary_saved["checks"].values())
        checks["five_field_scalar_check_passed"] = raw["checks"]["five_field_scalar_check_passed"]
        checks["absolute_cross_checks_passed"] = (
            raw["checks"]["absolute"]["closed_quadrature_agree_within_1e-12"]
            and raw["checks"]["absolute"]["closed_exact_midpoint_agree_within_1e-12"]
            and raw["checks"]["absolute"]["quadrature_reported_error_interval_intersects_exact_interval"]
            and raw["checks"]["absolute"]["high_precision_closed_form"]["inside_exact_rational_interval"]
        )
        checks["wave_timestep_checks_passed"] = wave["validation"]["all_dt_within_limit"]
        with np.load(RAW_SAMPLES, allow_pickle=False) as arrays:
            checks["npz_array_count"] = len(arrays.files) == 4 * len(RAW_SAMPLE_HORIZONS)
            checks["npz_shapes"] = all(array.shape == (RAW_SAMPLE_COUNT,) for array in arrays.values())
        valid = all(value is True for value in checks.values())
    except Exception:
        checks["exception"] = traceback.format_exc()
        valid = False
    record = {"valid": valid, "checks": checks, "verified_at_completion_date": COMPLETION_DATE}
    VERIFY_LOG.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    return valid


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        if not verify():
            raise SystemExit(1)
    else:
        generate()


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        target = VERIFY_LOG if "--verify" in sys.argv else RUN_LOG
        with target.open("a") as stream:
            stream.write("status=failed\n")
            stream.write(traceback.format_exc())
        raise
