"""Exact scalar explosion checks for flat raw Allen--Cahn moments (C8)."""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import platform


HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "flat-explosion-protocol.json"
RESULT = HERE / "flat-explosion-checks.json"
R = F(8)
RECTANGLES = 65536
ROUNDING_BITS = 60
ROUNDING_DENOMINATOR = 2**ROUNDING_BITS
EXP_DEGREE = 30
TIME_GRID_DENOMINATOR = 1000
TIME_GRID_MAX = 2 * TIME_GRID_DENOMINATOR
POLICIES = (F(1, 2), F(19, 20))
RATES = (F(3, 4), F(1))
HORIZON = F(1, 2)

A0 = F(9, 64)
B0 = F(1, 16)
C0 = F(9)
E0 = F(36)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_sha256(value: object) -> str:
    packed = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(packed).hexdigest()


def _fraction_record(value: F) -> dict[str, str | float]:
    return {"exact": str(value), "float": float(value)}


def polynomial(value: F) -> F:
    """P(v)=9/64+v/16+(9/2)v^2+6v^3."""
    return A0 + B0 * value + C0 * value * value / 2 + E0 * value**3 / 6


def policy_polynomial(policy: F, value: F) -> F:
    """P_p(s) before substituting s=p*v."""
    return (
        A0
        + (B0 / policy) * value
        + (C0 / (2 * policy**2)) * value**2
        + (E0 / (6 * policy**3)) * value**3
    )


def _round_units(value: F, *, up: bool) -> int:
    scaled = value * ROUNDING_DENOMINATOR
    if up:
        return -(-scaled.numerator // scaled.denominator)
    return scaled.numerator // scaled.denominator


def integral_enclosure() -> dict:
    """Compute the finite rectangle sums and analytic tail bounds exactly."""
    step = R / RECTANGLES
    lower_units = 0
    upper_units = 0
    for index in range(RECTANGLES + 1):
        reciprocal = 1 / polynomial(index * step)
        if index > 0:
            lower_units += _round_units(reciprocal, up=False)
        if index < RECTANGLES:
            upper_units += _round_units(reciprocal, up=True)

    finite_lower = step * F(lower_units, ROUNDING_DENOMINATOR)
    finite_upper = step * F(upper_units, ROUNDING_DENOMINATOR)
    tail_lower = 1 / (
        2
        * R**2
        * (6 + F(9, 2) / R + F(1, 16) / R**2 + F(9, 64) / R**3)
    )
    tail_upper = 1 / (12 * R**2)
    total_lower = finite_lower + tail_lower
    total_upper = finite_upper + tail_upper
    if not 0 < finite_lower < finite_upper or not 0 < tail_lower < tail_upper:
        raise RuntimeError("invalid monotone rectangle or tail enclosure")
    if not total_lower < total_upper:
        raise RuntimeError("empty integral enclosure")
    return {
        "R": str(R),
        "rectangles": RECTANGLES,
        "step": str(step),
        "rounding_bits": ROUNDING_BITS,
        "finite_lower": _fraction_record(finite_lower),
        "finite_upper": _fraction_record(finite_upper),
        "tail_lower": _fraction_record(tail_lower),
        "tail_upper": _fraction_record(tail_upper),
        "C_lower": _fraction_record(total_lower),
        "C_upper": _fraction_record(total_upper),
        "width": _fraction_record(total_upper - total_lower),
    }


def exponential_enclosure(x: F) -> tuple[F, F]:
    """Degree-30 Taylor lower bound and geometric-tail upper bound."""
    if not 0 <= x <= 1:
        raise ValueError("the predeclared exponential enclosure requires 0 <= x <= 1")
    term = F(1)
    lower = term
    for index in range(1, EXP_DEGREE + 1):
        term *= x / index
        lower += term
    first_omitted = term * x / (EXP_DEGREE + 1)
    upper = lower + first_omitted / (1 - x / (EXP_DEGREE + 2))
    return lower, upper


def theta_enclosure(rate: F, time: F) -> tuple[F, F]:
    exp_lower, exp_upper = exponential_enclosure(rate * time)
    return (exp_lower - 1) / rate**2, (exp_upper - 1) / rate**2


def _classification(theta_lower: F, theta_upper: F, threshold_lower: F,
                    threshold_upper: F) -> str:
    if theta_upper < threshold_lower:
        return "finite"
    if theta_lower >= threshold_upper:
        return "divergent"
    return "inconclusive"


def _time_bracket(rate: F, threshold_lower: F, threshold_upper: F) -> tuple[F, F]:
    lower_endpoint = None
    upper_endpoint = None
    for index in range(TIME_GRID_MAX + 1):
        time = F(index, TIME_GRID_DENOMINATOR)
        if rate * time > 1:
            if upper_endpoint is None:
                raise RuntimeError("time bracket not resolved within exp-enclosure domain")
            break
        theta_lower, theta_upper = theta_enclosure(rate, time)
        if theta_upper < threshold_lower:
            lower_endpoint = time
        if upper_endpoint is None and theta_lower > threshold_upper:
            upper_endpoint = time
            break
    if lower_endpoint is None or upper_endpoint is None or lower_endpoint >= upper_endpoint:
        raise RuntimeError("failed to construct a strict explosion-time bracket")
    return lower_endpoint, upper_endpoint


def exact_certificate() -> dict:
    integral = integral_enclosure()
    c_lower = F(integral["C_lower"]["exact"])
    c_upper = F(integral["C_upper"]["exact"])

    coefficient_target = (A0, B0, C0 / 2, E0 / 6)
    coefficient_checks = []
    grid_checks = 0
    step = R / RECTANGLES
    for policy in POLICIES:
        substituted_coefficients = (
            A0,
            (B0 / policy) * policy,
            (C0 / (2 * policy**2)) * policy**2,
            (E0 / (6 * policy**3)) * policy**3,
        )
        coefficients_match = substituted_coefficients == coefficient_target
        if not coefficients_match:
            raise RuntimeError("P_p(pv)=P(v) coefficient identity failed")
        for index in range(RECTANGLES + 1):
            value = index * step
            if policy_polynomial(policy, policy * value) != polynomial(value):
                raise RuntimeError("P_p(pv)=P(v) grid identity failed")
            grid_checks += 1
        coefficient_checks.append({
            "policy": str(policy),
            "substituted_coefficients": list(map(str, substituted_coefficients)),
            "target_coefficients": list(map(str, coefficient_target)),
            "match": True,
        })

    cases = []
    for policy in POLICIES:
        threshold_lower = policy * c_lower
        threshold_upper = policy * c_upper
        for rate in RATES:
            theta_lower, theta_upper = theta_enclosure(rate, HORIZON)
            lower_time, upper_time = _time_bracket(
                rate, threshold_lower, threshold_upper
            )
            cases.append({
                "policy": str(policy),
                "rate": str(rate),
                "horizon": str(HORIZON),
                "theta_lower": _fraction_record(theta_lower),
                "theta_upper": _fraction_record(theta_upper),
                "pC_lower": _fraction_record(threshold_lower),
                "pC_upper": _fraction_record(threshold_upper),
                "classification": _classification(
                    theta_lower, theta_upper, threshold_lower, threshold_upper
                ),
                "explosion_time_lower": _fraction_record(lower_time),
                "explosion_time_upper": _fraction_record(upper_time),
                "explosion_time_width": _fraction_record(upper_time - lower_time),
                "bracket_checks": {
                    "lower_theta_upper_lt_pC_lower": (
                        theta_enclosure(rate, lower_time)[1] < threshold_lower
                    ),
                    "upper_theta_lower_gt_pC_upper": (
                        theta_enclosure(rate, upper_time)[0] > threshold_upper
                    ),
                },
            })

    expected = {
        ("1/2", "3/4"): "divergent",
        ("1/2", "1"): "finite",
        ("19/20", "3/4"): "finite",
        ("19/20", "1"): "finite",
    }
    if any(expected[(case["policy"], case["rate"])] != case["classification"]
           for case in cases):
        raise RuntimeError("predeclared classification expectation was falsified")

    return {
        "integral_enclosure": integral,
        "monotonicity": {
            "derivative": "P'(v)=1/16+9*v+18*v^2",
            "strictly_positive_for_v_ge_0": True,
            "use": "right rectangles lower-bound and left rectangles upper-bound the finite integral",
        },
        "identity": {
            "statement": "P_p(p*v)=P(v) for common proposal p",
            "coefficient_checks": coefficient_checks,
            "exact_grid_points_checked": grid_checks,
            "all_checks_passed": True,
        },
        "exponential_degree": EXP_DEGREE,
        "exponential_tail_lemma": (
            "For 0<=x<=1, e^x lies between S_30 and "
            "S_30+(x^31/31!)/(1-x/32)."
        ),
        "classification_rule": {
            "finite": "theta_upper<pC_lower",
            "divergent": "theta_lower>=pC_upper",
        },
        "cases": cases,
    }


def floating_diagnostics(c_lower: F, c_upper: F) -> dict:
    """Independent floating quadrature/log values with no proof status."""
    from scipy.integrate import quad

    c_quad, error = quad(
        lambda value: 1.0 / (
            9.0 / 64.0 + value / 16.0 + 4.5 * value**2 + 6.0 * value**3
        ),
        0.0,
        math.inf,
        epsabs=1e-13,
        epsrel=1e-13,
        limit=300,
    )
    cases = []
    for policy in POLICIES:
        for rate in RATES:
            theta = math.expm1(float(rate * HORIZON)) / float(rate**2)
            explosion_time = math.log1p(float(rate**2 * policy) * c_quad) / float(rate)
            cases.append({
                "policy": str(policy),
                "rate": str(rate),
                "theta_at_horizon": theta,
                "p_times_C": float(policy) * c_quad,
                "explosion_time": explosion_time,
            })
    return {
        "role": "floating diagnostic; no mathematical status",
        "scipy_quad_C": c_quad,
        "scipy_reported_error": error,
        "quad_inside_exact_enclosure": float(c_lower) <= c_quad <= float(c_upper),
        "cases": cases,
    }


def provenance() -> dict:
    import scipy

    environment = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "scipy": scipy.__version__,
    }
    commands = {
        "generate": (
            "MPLCONFIGDIR=/tmp/parabolab-mpl "
            "/opt/miniconda3/envs/parabolab/bin/python "
            "docs/research/runs/2026-09-16-certified-tuple-policy/numerics/"
            "flat_explosion_check.py"
        ),
        "verify": (
            "MPLCONFIGDIR=/tmp/parabolab-mpl "
            "/opt/miniconda3/envs/parabolab/bin/python "
            "docs/research/runs/2026-09-16-certified-tuple-policy/numerics/"
            "flat_explosion_check.py --verify "
            "docs/research/runs/2026-09-16-certified-tuple-policy/numerics/"
            "flat-explosion-checks.json"
        ),
    }
    sources = {
        Path(__file__).name: _sha256(Path(__file__)),
        PROTOCOL.name: _sha256(PROTOCOL),
    }
    return {
        "source_sha256": sources,
        "environment": environment,
        "environment_sha256": _json_sha256(environment),
        "commands": commands,
        "commands_sha256": _json_sha256(commands),
    }


def verify(path: Path) -> dict:
    saved = json.loads(path.read_text())
    recomputed = exact_certificate()
    current_provenance = provenance()
    exact_match = saved.get("exact_certificate") == recomputed
    source_match = saved.get("provenance", {}).get("source_sha256") == current_provenance["source_sha256"]
    environment_hash_valid = (
        saved.get("provenance", {}).get("environment_sha256")
        == _json_sha256(saved.get("provenance", {}).get("environment"))
    )
    command_hash_valid = (
        saved.get("provenance", {}).get("commands_sha256")
        == _json_sha256(saved.get("provenance", {}).get("commands"))
    )
    valid = exact_match and source_match and environment_hash_valid and command_hash_valid
    return {
        "file": str(path),
        "exact_certificate_recomputed": exact_match,
        "source_hashes_match": source_match,
        "stored_environment_hash_valid": environment_hash_valid,
        "stored_command_hash_valid": command_hash_valid,
        "valid": valid,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify is not None:
        result = verify(args.verify)
        print(json.dumps(result, indent=2))
        if not result["valid"]:
            raise SystemExit(1)
        return

    if not PROTOCOL.exists():
        raise RuntimeError("flat-explosion-protocol.json must exist before evaluation")
    exact = exact_certificate()
    integral = exact["integral_enclosure"]
    c_lower = F(integral["C_lower"]["exact"])
    c_upper = F(integral["C_upper"]["exact"])
    output = {
        "schema_version": 1,
        "scope": "C8 scalar explosion reduction for flat raw 1D Allen-Cahn moments",
        "exact_certificate": exact,
        "floating_diagnostics": floating_diagnostics(c_lower, c_upper),
        "provenance": provenance(),
        "execution_log": [
            "Protocol file existed before evaluation.",
            "Each reciprocal was rounded outward to the 2^-60 grid before summation.",
            "All P_p(pv)=P(v) coefficient and declared-grid checks passed exactly.",
            "Every finite/divergent classification used separated rational intervals.",
            "Old postfixed-box failures were not used as evidence.",
        ],
        "limitations": [
            "The scalar-reduction theorem is established in separate mathematical review.",
            "No Lean proof of the integral or exponential bounds is claimed.",
            "Floating diagnostics are not inputs to any classification.",
        ],
    }
    RESULT.write_text(json.dumps(output, indent=2) + "\n")
    verification = verify(RESULT)
    if not verification["valid"]:
        raise RuntimeError("fresh exact result failed independent recomputation")
    print(json.dumps({
        "C_lower": integral["C_lower"],
        "C_upper": integral["C_upper"],
        "width": integral["width"],
        "cases": [
            {
                "policy": case["policy"],
                "rate": case["rate"],
                "classification": case["classification"],
                "explosion_time_interval": [
                    case["explosion_time_lower"]["float"],
                    case["explosion_time_upper"]["float"],
                ],
            }
            for case in exact["cases"]
        ],
        "verification": verification,
    }, indent=2))


if __name__ == "__main__":
    main()
