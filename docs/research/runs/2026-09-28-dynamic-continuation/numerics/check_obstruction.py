"""Deterministic high-precision checks for the constant-profile examples."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

os.environ.setdefault("MPLCONFIGDIR", "/tmp/parabolab-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/parabolab-cache")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
OUTPUT_JSON = HERE / "obstruction_checks.json"
OUTPUT_PNG = RUN_DIR / "obstruction-examples.png"
OUTPUT_SVG = RUN_DIR / "obstruction-examples.svg"

DPS = 80
FAIL_THRESHOLD = mp.mpf("1e-60")
N_VALUES = (1, 2, 4, 8, 16, 32)
SIN_FRACTIONS = ("0.1", "0.5", "0.9", "0.99")
RATIONAL_TIMES = ("0", "0.1", "0.5", "0.65", "2/3")

FROZEN_T09_HASHES = {
    "numerics/dynamic_interface.py": "c15e7a4ebdd8e3838ec3302ed6bd67305fda41dfc7be8a34f3ebb55060493268",
    "numerics/run_dynamic.py": "59a006e29b6b370d9d55b3a7fb6553b5ee94e1888be2babb78422ee0ef10b8db",
    "numerics/test_dynamic.py": "3d4fc3b382f611fd51c90c666d3b88705045e846ebacd719531de0125122e673",
    "numerics/audit.log": "c744417878aad7585836aeb5fde6008dd1207f67ac3c4d1a14d1ac2da8717cdc",
    "reviews/T09-implementation.md": "86ab7b86a66751d77386170701c465ffc1ea0e65bcbd24323a7c4524dad054b9",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def mp_string(value: mp.mpf) -> str:
    return mp.nstr(value, DPS, strip_zeros=False)


def identity_record(computed: mp.mpf, expected: mp.mpf) -> dict:
    residual = abs(computed - expected)
    return {
        "computed": mp_string(computed),
        "expected": mp_string(expected),
        "absolute_residual": mp_string(residual),
        "passed_below_1e-60": bool(residual < FAIL_THRESHOLD),
    }


def git_revision() -> str | None:
    result = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def verify_frozen_t09() -> dict:
    observed = {relative: sha256(RUN_DIR / relative) for relative in FROZEN_T09_HASHES}
    if observed != FROZEN_T09_HASHES:
        raise RuntimeError("a frozen T09 file changed before the obstruction checks")
    return observed


def sine_checks() -> tuple[dict, list[mp.mpf]]:
    critical_time = mp.pi / 2
    tau_quadrature = mp.quad(lambda z: mp.sech(z), [0, 1, mp.inf])
    fraction_rows = []
    residuals = [abs(tau_quadrature - critical_time)]

    def absolute_increment(t: mp.mpf) -> mp.mpf:
        return mp.log(mp.sec(t) + mp.tan(t))

    def signed_solution(t: mp.mpf) -> mp.mpf:
        return 2 * mp.atan(mp.exp(t))

    for fraction_text in SIN_FRACTIONS:
        fraction = mp.mpf(fraction_text)
        t = fraction * critical_time
        quadrature = mp.quad(lambda s: mp.sec(s), [0, t])
        formula = absolute_increment(t)
        derivative = mp.diff(absolute_increment, t)
        derivative_expected = mp.sec(t)
        ode_derivative = mp.diff(signed_solution, t)
        ode_rhs = mp.sin(signed_solution(t))
        row = {
            "fraction_of_pi_over_2": fraction_text,
            "time": mp_string(t),
            "absolute_increment_integral_vs_log_formula": identity_record(
                quadrature, formula
            ),
            "log_formula_derivative_vs_sec": identity_record(
                derivative, derivative_expected
            ),
            "signed_solution_ode_uprime_vs_sin_u": identity_record(
                ode_derivative, ode_rhs
            ),
            "signed_solution": mp_string(signed_solution(t)),
        }
        fraction_rows.append(row)
        residuals.extend(
            (
                abs(quadrature - formula),
                abs(derivative - derivative_expected),
                abs(ode_derivative - ode_rhs),
            )
        )
    initial = signed_solution(mp.mpf("0"))
    initial_record = identity_record(initial, critical_time)
    residuals.append(abs(initial - critical_time))
    return (
        {
            "reaction": "sin(y)",
            "terminal_constant_r": mp_string(critical_time),
            "critical_time": mp_string(critical_time),
            "sech_integral_zero_to_infinity_vs_pi_over_2": identity_record(
                tau_quadrature, critical_time
            ),
            "fraction_checks": fraction_rows,
            "signed_initial_condition": initial_record,
            "endpoint_classification_from_reviewed_theorem": (
                "the canonical Id absolute moment is infinite at t=pi/2; "
                "the signed solution is global"
            ),
        },
        residuals,
    )


def rational_checks() -> tuple[dict, list[mp.mpf]]:
    critical_time = mp.mpf(2) / 3
    tau_quadrature = mp.quad(lambda z: 1 - z**2, [0, 1])
    residuals = [abs(tau_quadrature - critical_time)]
    rows = []

    def absolute_moment(t: mp.mpf) -> mp.mpf:
        return 2 * mp.sin(mp.asin(3 * t / 2) / 3)

    def signed_solution(t: mp.mpf) -> mp.mpf:
        return 2 * mp.sinh(mp.asinh(3 * t / 2) / 3)

    for time_text in RATIONAL_TIMES:
        t = critical_time if time_text == "2/3" else mp.mpf(time_text)
        z = absolute_moment(t)
        u = signed_solution(t)
        z_identity = z - z**3 / 3
        u_identity = u + u**3 / 3
        rows.append(
            {
                "time": time_text,
                "absolute_moment_z": mp_string(z),
                "signed_solution_u": mp_string(u),
                "z_minus_z_cubed_over_3_vs_t": identity_record(z_identity, t),
                "u_plus_u_cubed_over_3_vs_t": identity_record(u_identity, t),
            }
        )
        residuals.extend((abs(z_identity - t), abs(u_identity - t)))
    endpoint = absolute_moment(critical_time)
    endpoint_record = identity_record(endpoint, mp.mpf(1))
    residuals.append(abs(endpoint - 1))
    return (
        {
            "reaction": "1/(1+y^2)",
            "terminal_constant_r": "0",
            "critical_time": "2/3",
            "integral_zero_to_one_of_1_minus_z_squared_vs_2_over_3": identity_record(
                tau_quadrature, critical_time
            ),
            "time_checks": rows,
            "critical_endpoint_absolute_moment": endpoint_record,
            "critical_endpoint_derivative_intentionally_not_evaluated": True,
            "endpoint_classification_from_reviewed_theorem": (
                "the canonical Id absolute moment equals 1 at t=2/3 and is "
                "infinite only for t>2/3; the signed solution is global"
            ),
        },
        residuals,
    )


def truncation_checks() -> tuple[dict, list[mp.mpf], list[mp.mpf]]:
    rows = []
    values = []
    residuals = []
    limit = mp.mpf(2) / 3
    for n in N_VALUES:
        def reciprocal_phi(z, degree=n):
            return 1 / mp.fsum(z ** (2 * k) for k in range(degree + 1))

        quadrature = mp.quad(reciprocal_phi, [0, 1, mp.inf])
        denominator = 2 * n + 2
        angle = mp.pi / denominator
        formula = mp.pi / denominator * (mp.cot(angle) - mp.cot(3 * angle))
        residual = abs(quadrature - formula)
        excess = quadrature - limit
        rows.append(
            {
                "n": n,
                "quadrature": mp_string(quadrature),
                "cotangent_formula": mp_string(formula),
                "absolute_residual": mp_string(residual),
                "passed_below_1e-60": bool(residual < FAIL_THRESHOLD),
                "excess_above_2_over_3": mp_string(excess),
                "strictly_above_2_over_3": bool(excess > 0),
            }
        )
        values.append(quadrature)
        residuals.append(residual)
    decreasing = all(left > right for left, right in zip(values, values[1:]))
    above_limit = all(value > limit for value in values)
    return (
        {
            "phi_n": "sum_{k=0}^n z^(2k)",
            "rows": rows,
            "strictly_decreasing_on_prespecified_n_values": decreasing,
            "all_strictly_above_2_over_3": above_limit,
            "identity_is_not_in_current_lean_module": True,
        },
        values,
        residuals,
    )


def make_figure(truncation_values: list[mp.mpf]) -> None:
    blue = "#2166ac"
    orange = "#d6604d"
    shade = "#f4cccc"
    fig, axes = plt.subplots(1, 3, figsize=(14.2, 4.5), constrained_layout=False)

    sin_critical = np.pi / 2
    sin_t = np.linspace(0.0, 2.15, 700)
    sin_subcritical = np.linspace(0.0, 0.995 * sin_critical, 500)
    axes[0].plot(
        sin_t, 2 * np.arctan(np.exp(sin_t)), color=blue, lw=2, label="signed $u(t)$"
    )
    axes[0].plot(
        sin_subcritical,
        sin_critical + np.log(1 / np.cos(sin_subcritical) + np.tan(sin_subcritical)),
        color=orange,
        lw=2,
        label="absolute $W_{Id}(t)$",
    )
    axes[0].axvspan(sin_critical, sin_t[-1], color=shade, alpha=0.7)
    axes[0].axvline(sin_critical, color="black", ls="--", lw=1)
    axes[0].text(
        1.72,
        5.4,
        "$W_{Id}=\\infty$ at and after\n$t_c=\\pi/2$ (theorem)",
        ha="center",
        va="center",
        fontsize=9,
    )
    axes[0].set(title="$f(y)=\\sin y$, $r=\\pi/2$", xlabel="$t$", ylabel="value")
    axes[0].set_ylim(0, 7.2)
    axes[0].legend(loc="upper left", frameon=False)

    rational_critical = 2 / 3
    rational_t = np.linspace(0.0, 1.1, 700)
    rational_subcritical = np.linspace(0.0, rational_critical, 500)
    signed = 2 * np.sinh(np.arcsinh(1.5 * rational_t) / 3)
    absolute = 2 * np.sin(np.arcsin(1.5 * rational_subcritical) / 3)
    axes[1].plot(rational_t, signed, color=blue, lw=2, label="signed $u(t)$")
    axes[1].plot(
        rational_subcritical,
        absolute,
        color=orange,
        lw=2,
        label="absolute $W_{Id}(t)$",
    )
    axes[1].axvspan(rational_critical, rational_t[-1], color=shade, alpha=0.7)
    axes[1].axvline(rational_critical, color="black", ls="--", lw=1)
    axes[1].scatter([rational_critical], [1], color=orange, s=36, zorder=5)
    axes[1].annotate(
        "finite at $(2/3,1)$",
        xy=(rational_critical, 1),
        xytext=(0.82, 1.19),
        arrowprops={"arrowstyle": "->", "color": "#555555"},
        ha="center",
        fontsize=9,
    )
    axes[1].text(
        0.885,
        0.55,
        "$W_{Id}=\\infty$ only for\n$t>2/3$ (theorem)",
        ha="center",
        va="center",
        fontsize=9,
    )
    axes[1].set(
        title="$f(y)=1/(1+y^2)$, $r=0$", xlabel="$t$", ylabel="value", ylim=(0, 1.35)
    )
    axes[1].legend(loc="upper left", frameon=False)

    tau_values = np.array([float(value) for value in truncation_values])
    axes[2].plot(N_VALUES, tau_values, "o-", color="#4d9221", lw=2, ms=5)
    axes[2].axhline(2 / 3, color="black", ls="--", lw=1, label="limit $2/3$")
    axes[2].set_xscale("log", base=2)
    axes[2].set_xticks(N_VALUES, labels=[str(n) for n in N_VALUES])
    axes[2].set(
        title="Reciprocal-polynomial horizons",
        xlabel="truncation $n$",
        ylabel="$\\tau_n$",
    )
    axes[2].legend(frameon=False)
    axes[2].grid(alpha=0.22)

    for axis in axes:
        axis.spines[["top", "right"]].set_visible(False)
        axis.tick_params(direction="out")
    fig.subplots_adjust(left=0.055, right=0.985, top=0.84, bottom=0.22, wspace=0.28)
    fig.suptitle("Constant-profile absolute-moment illustrations", fontsize=14, y=0.96)
    fig.text(
        0.5,
        0.055,
        "Deterministic identities under the reviewed theorem; not Monte Carlo evidence of divergence.",
        ha="center",
        fontsize=10,
    )
    fig.savefig(OUTPUT_PNG, dpi=190)
    fig.savefig(OUTPUT_SVG)
    plt.close(fig)


def main() -> int:
    for path in (OUTPUT_JSON, OUTPUT_PNG, OUTPUT_SVG):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite existing output {path}")
    started = time.perf_counter()
    frozen_t09 = verify_frozen_t09()
    with mp.workdps(DPS):
        sine, sine_residuals = sine_checks()
        rational, rational_residuals = rational_checks()
        truncations, truncation_values, truncation_residuals = truncation_checks()
        residuals = sine_residuals + rational_residuals + truncation_residuals
        maximum_residual = max(residuals)
        all_identity_checks_passed = bool(
            maximum_residual < FAIL_THRESHOLD
            and truncations["strictly_decreasing_on_prespecified_n_values"]
            and truncations["all_strictly_above_2_over_3"]
        )
        if not all_identity_checks_passed:
            raise RuntimeError(
                "prespecified identity check failed; maximum residual was "
                + mp_string(maximum_residual)
            )
        make_figure(truncation_values)

    source_paths = {
        "check_obstruction.py": HERE / "check_obstruction.py",
        "02b-obstruction-check-protocol.md": RUN_DIR / "02b-obstruction-check-protocol.md",
        "04d-sharp-constant-horizon.md": RUN_DIR / "04d-sharp-constant-horizon.md",
        "06b-absolute-lean.md": RUN_DIR / "06b-absolute-lean.md",
        "T13-general-obstruction-audit.md": RUN_DIR / "reviews" / "T13-general-obstruction-audit.md",
        "lean-build.log": RUN_DIR / "lean" / "absolute-obstruction" / "build.log",
        "lean-axioms.log": RUN_DIR / "lean" / "absolute-obstruction" / "axioms.log",
    }
    record = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "description": "deterministic illustrations of reviewed constant-profile identities",
        "status": "passed",
        "all_identity_checks_passed": all_identity_checks_passed,
        "decimal_precision": DPS,
        "strict_absolute_residual_threshold": "1e-60",
        "maximum_absolute_residual": mp_string(maximum_residual),
        "sine_example": sine,
        "rational_example": rational,
        "reciprocal_polynomial_truncations": truncations,
        "scope": {
            "not_monte_carlo": True,
            "finite_checks_do_not_prove_divergence": True,
            "current_lean_proves_only_the_riccati_analytic_barrier": True,
            "series_and_tree_likelihood_bridges_remain_conventional": True,
        },
        "provenance": {
            "command": sys.argv,
            "git_revision": git_revision(),
            "python": sys.version,
            "platform": platform.platform(),
            "mpmath": mp.__version__,
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "elapsed_seconds": time.perf_counter() - started,
            "source_hashes_sha256": {
                name: sha256(path) for name, path in source_paths.items()
            },
            "frozen_t09_hashes_verified": frozen_t09,
            "figure_hashes_sha256": {
                OUTPUT_PNG.name: sha256(OUTPUT_PNG),
                OUTPUT_SVG.name: sha256(OUTPUT_SVG),
            },
        },
    }
    temporary = OUTPUT_JSON.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(record, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, OUTPUT_JSON)
    print(
        json.dumps(
            {
                "status": record["status"],
                "maximum_absolute_residual": record["maximum_absolute_residual"],
                "json": str(OUTPUT_JSON),
                "png": str(OUTPUT_PNG),
                "svg": str(OUTPUT_SVG),
                "elapsed_seconds": record["provenance"]["elapsed_seconds"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
