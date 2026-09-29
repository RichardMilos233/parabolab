"""Fixed deterministic checks for the critical moment--work frontier."""

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
import traceback

os.environ.setdefault("MPLCONFIGDIR", "/tmp/parabolab-critical-frontier-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/parabolab-critical-frontier-cache")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]

OUTPUT_JSON = HERE / "critical_frontier_checks.json"
OUTPUT_LOG = HERE / "critical_frontier_execution.log"
OUTPUT_PNG = RUN_DIR / "critical-frontier.png"
OUTPUT_SVG = RUN_DIR / "critical-frontier.svg"
OUTPUT_REVIEW = RUN_DIR / "reviews" / "T25-critical-frontier-checks.md"
FINAL_OUTPUTS = (OUTPUT_JSON, OUTPUT_LOG, OUTPUT_PNG, OUTPUT_SVG, OUTPUT_REVIEW)

DPS = 80
mp.mp.dps = DPS
EXACT_TOLERANCE = mp.mpf("1e-60")
ALPHA_TEXTS = ("0.5", "1", "2")
DELTA_TEXTS = ("1e-2", "1e-4", "1e-6", "1e-8")
P_TEXT = "2"
BETA_TEXT = "0.5"

GATE_HASHES = {
    "reviews/T22-critical-moment-work-audit.md": (
        "cab149f5b1a7bea91cc9ea3e52d09ce68b1edf9cbf9b2ce3c8329ef2bedbdf4d"
    ),
    "04h-critical-moment-work.md": (
        "9750b19bab65bd1cc78bf0db6b5385a896e3a8146a8219777f808ea1279e7dd4"
    ),
    "02c-critical-frontier-protocol.md": (
        "3e6929d0c49d17f69819c3dd7854cbfab8804745103e7d4ef9831126957220cc"
    ),
    "06e-critical-work-lean.md": (
        "9195a1827c05a78a86ab08b6c6c5b7a3a88feeff01b75806a8d325ae228da068"
    ),
    "../../../../formal/EstimatorIntegrity/CriticalMomentWork.lean": (
        "2aa8eac99d548e1a4ba5e21f7c9d5aef0a6595a527a4ee9d59c49c0dba23893e"
    ),
    "lean/critical-moment-work/build.log": (
        "cb5476d3a90ba929e47e7cb54ca6dea6315c9a5ad3f7b858a57e32d4e42190e1"
    ),
    "lean/critical-moment-work/axioms.log": (
        "60d379bd383500c73b4c8aeb738732d748fd32ade4fd708f889244ef04c585e5"
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def gate_path(relative: str) -> Path:
    return (RUN_DIR / relative).resolve()


def verify_gate_hashes() -> dict[str, str]:
    observed = {relative: sha256(gate_path(relative)) for relative in GATE_HASHES}
    if observed != GATE_HASHES:
        mismatches = {
            key: {"expected": GATE_HASHES[key], "observed": observed.get(key)}
            for key in GATE_HASHES
            if observed.get(key) != GATE_HASHES[key]
        }
        raise RuntimeError(f"source or Lean gate changed before execution: {mismatches}")
    return observed


def refuse_overwrite() -> None:
    existing = [str(path) for path in FINAL_OUTPUTS if path.exists()]
    if existing:
        raise FileExistsError(f"refusing to overwrite final artifacts: {existing}")


def mp_string(value: mp.mpf) -> str:
    return mp.nstr(
        value,
        DPS,
        strip_zeros=False,
        min_fixed=-1000,
        max_fixed=1000,
    )


def git_revision() -> str | None:
    result = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def record_failure(failures: list[dict], category: str, case: dict, detail: str) -> None:
    failures.append({"category": category, "case": case, "detail": detail})


def tau_checks(failures: list[dict]) -> tuple[list[dict], dict[str, mp.mpf]]:
    rows = []
    tau_by_alpha = {}
    for alpha_text in ALPHA_TEXTS:
        alpha = mp.mpf(alpha_text)
        quadrature = mp.quad(lambda z: (1 - z**2) ** alpha, [0, 1])
        gamma_formula = (
            mp.sqrt(mp.pi)
            * mp.gamma(alpha + 1)
            / (2 * mp.gamma(alpha + mp.mpf("1.5")))
        )
        discrepancy = abs(quadrature - gamma_formula)
        passed = bool(discrepancy < EXACT_TOLERANCE)
        row = {
            "alpha": alpha_text,
            "quadrature": mp_string(quadrature),
            "gamma_formula": mp_string(gamma_formula),
            "absolute_discrepancy": mp_string(discrepancy),
            "acceptance": "absolute_discrepancy < 1e-60",
            "passed": passed,
        }
        rows.append(row)
        tau_by_alpha[alpha_text] = gamma_formula
        if not passed:
            record_failure(failures, "tau_identity", {"alpha": alpha_text}, row["acceptance"])
    return rows, tau_by_alpha


def derivative_checks(failures: list[dict]) -> list[dict]:
    rows = []
    for alpha_text in ALPHA_TEXTS:
        alpha = mp.mpf(alpha_text)
        f_alpha = lambda y: (1 + y**2) ** (-alpha)
        for order in range(13):
            direct = mp.diff(f_alpha, mp.mpf("0"), order)
            if order % 2:
                formula = mp.mpf("0")
            else:
                k = order // 2
                formula = (
                    (-1) ** k
                    * mp.factorial(2 * k)
                    * mp.rf(alpha, k)
                    / mp.factorial(k)
                )
            scaled = abs(direct - formula) / max(mp.mpf("1"), abs(formula))
            passed = bool(scaled < EXACT_TOLERANCE)
            row = {
                "alpha": alpha_text,
                "order": order,
                "direct_high_precision_differentiation": mp_string(direct),
                "closed_formula": mp_string(formula),
                "scaled_discrepancy": mp_string(scaled),
                "acceptance": "scaled_discrepancy < 1e-60",
                "passed": passed,
            }
            rows.append(row)
            if not passed:
                record_failure(
                    failures,
                    "derivative_identity",
                    {"alpha": alpha_text, "order": order},
                    row["acceptance"],
                )
    return rows


def beta_tail(alpha: mp.mpf, delta: mp.mpf) -> mp.mpf:
    complement = 1 - (1 - delta) ** 2
    return mp.mpf("0.5") * mp.betainc(alpha + 1, mp.mpf("0.5"), 0, complement)


def tail_checks_and_cusp_diagnostics(
    failures: list[dict],
) -> tuple[list[dict], list[dict], dict[tuple[str, str], mp.mpf]]:
    identity_rows = []
    diagnostic_rows = []
    tails = {}
    for alpha_text in ALPHA_TEXTS:
        alpha = mp.mpf(alpha_text)
        cusp_limit = 2**alpha / (alpha + 1)
        for delta_text in DELTA_TEXTS:
            delta = mp.mpf(delta_text)
            direct = mp.quad(
                lambda z: (1 - z**2) ** alpha,
                [1 - delta, 1],
            )
            incomplete_beta = beta_tail(alpha, delta)
            scaled = abs(direct - incomplete_beta) / max(
                mp.mpf("1"), abs(incomplete_beta)
            )
            passed = bool(scaled < EXACT_TOLERANCE)
            identity_row = {
                "alpha": alpha_text,
                "delta": delta_text,
                "direct_quadrature": mp_string(direct),
                "incomplete_beta": mp_string(incomplete_beta),
                "scaled_discrepancy": mp_string(scaled),
                "acceptance": "scaled_discrepancy < 1e-60",
                "passed": passed,
            }
            identity_rows.append(identity_row)
            tails[(alpha_text, delta_text)] = incomplete_beta
            diagnostic_rows.append(
                {
                    "alpha": alpha_text,
                    "delta": delta_text,
                    "B_over_delta_to_alpha_plus_one": mp_string(
                        incomplete_beta / delta ** (alpha + 1)
                    ),
                    "proved_limit_2_to_alpha_over_alpha_plus_one": mp_string(
                        cusp_limit
                    ),
                    "interpretation": "finite-cutoff diagnostic; not a proof of the limit",
                }
            )
            if not passed:
                record_failure(
                    failures,
                    "beta_tail_identity",
                    {"alpha": alpha_text, "delta": delta_text},
                    identity_row["acceptance"],
                )
    return identity_rows, diagnostic_rows, tails


def stable_endpoint_integrand(
    alpha: mp.mpf, tau: mp.mpf, delta: mp.mpf
) -> mp.mpf:
    tail = beta_tail(alpha, delta)
    tail_fraction = tail / tau
    negative_log_ratio = -mp.log1p(-tail_fraction)
    f_value = tau * (1 - tail_fraction)
    z = 1 - delta
    return (
        delta
        * negative_log_ratio ** (-mp.mpf("1.5"))
        * (1 - z**2) ** alpha
        / f_value
    )


def endpoint_diagnostics(
    failures: list[dict], tau_by_alpha: dict[str, mp.mpf]
) -> tuple[list[dict], list[dict], list[dict], dict[str, list[mp.mpf]]]:
    contribution_rows = []
    integrand_rows = []
    monotonicity_rows = []
    values_by_alpha = {}
    prefactor = mp.sqrt(2) / (2 * mp.sqrt(mp.pi))
    fixed_breaks = tuple(mp.mpf(text) for text in DELTA_TEXTS) + (
        mp.mpf("0.1"),
        mp.mpf("0.5"),
    )

    for alpha_text in ALPHA_TEXTS:
        alpha = mp.mpf(alpha_text)
        tau = tau_by_alpha[alpha_text]
        limiting_scaled_integrand = (alpha + 1) ** mp.mpf("1.5") * mp.sqrt(
            tau / 2**alpha
        )
        contributions = []
        for delta_text in DELTA_TEXTS:
            delta = mp.mpf(delta_text)
            points = sorted({delta, *(point for point in fixed_breaks if point > delta)})
            integral = mp.quad(
                lambda r: stable_endpoint_integrand(alpha, tau, r),
                points,
            )
            contribution = prefactor * integral
            contributions.append(contribution)
            positive = bool(contribution > 0)
            contribution_rows.append(
                {
                    "alpha": alpha_text,
                    "delta": delta_text,
                    "K_alpha_delta": mp_string(contribution),
                    "positive": positive,
                    "quadrature_variable": "r=1-z",
                    "quadrature_breaks": [mp_string(point) for point in points],
                    "interpretation": (
                        "truncated endpoint contribution; not the full S_2 mass"
                    ),
                }
            )
            if not positive:
                record_failure(
                    failures,
                    "endpoint_contribution_positivity",
                    {"alpha": alpha_text, "delta": delta_text},
                    "K_alpha(delta) must be strictly positive",
                )

            endpoint_j = stable_endpoint_integrand(alpha, tau, delta)
            integrand_rows.append(
                {
                    "alpha": alpha_text,
                    "delta": delta_text,
                    "J_times_delta_to_alpha_plus_one_over_two": mp_string(
                        endpoint_j * delta ** ((alpha + 1) / 2)
                    ),
                    "analytic_limiting_value": mp_string(limiting_scaled_integrand),
                    "acceptance_threshold": None,
                    "interpretation": (
                        "finite-cutoff asymptotic diagnostic; no residual theorem test"
                    ),
                }
            )

        increasing = all(
            right > left for left, right in zip(contributions, contributions[1:])
        )
        monotonicity_rows.append(
            {
                "alpha": alpha_text,
                "delta_order": list(DELTA_TEXTS),
                "strictly_increases_as_delta_decreases": increasing,
            }
        )
        if not increasing:
            record_failure(
                failures,
                "endpoint_contribution_monotonicity",
                {"alpha": alpha_text},
                "K_alpha(delta) must strictly increase along 1e-2,1e-4,1e-6,1e-8",
            )
        values_by_alpha[alpha_text] = contributions
    return contribution_rows, integrand_rows, monotonicity_rows, values_by_alpha


def make_figure(
    cusp_rows: list[dict], contributions_by_alpha: dict[str, list[mp.mpf]]
) -> None:
    x_values = [float(-mp.log10(mp.mpf(text))) for text in DELTA_TEXTS]
    colors = {"0.5": "#0072B2", "1": "#D55E00", "2": "#009E73"}
    predictions = {
        "0.5": "theory: finite limit",
        "1": "theory: logarithmic divergence",
        "2": "theory: power divergence",
    }
    fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.2))

    for alpha_text in ALPHA_TEXTS:
        alpha = mp.mpf(alpha_text)
        rows = [row for row in cusp_rows if row["alpha"] == alpha_text]
        ratios = [float(mp.mpf(row["B_over_delta_to_alpha_plus_one"])) for row in rows]
        limit = float(2**alpha / (alpha + 1))
        axes[0].plot(
            x_values,
            ratios,
            marker="o",
            linewidth=2,
            color=colors[alpha_text],
            label=rf"numerical $\alpha={alpha_text}$",
        )
        axes[0].axhline(
            limit,
            linestyle="--",
            linewidth=1.2,
            color=colors[alpha_text],
            alpha=0.75,
            label=rf"theory limit $\alpha={alpha_text}$",
        )

    axes[0].set_title("Complementary cusp ratio")
    axes[0].set_xlabel(r"cutoff depth $\log_{10}(1/\delta)$")
    axes[0].set_ylabel(r"$B_\alpha(\delta)/\delta^{\alpha+1}$ [dimensionless]")
    axes[0].set_xticks(x_values)
    axes[0].grid(alpha=0.25)
    axes[0].legend(frameon=False, fontsize=8, ncol=2)

    for alpha_text in ALPHA_TEXTS:
        axes[1].plot(
            x_values,
            [float(value) for value in contributions_by_alpha[alpha_text]],
            marker="o",
            linewidth=2,
            color=colors[alpha_text],
            label=rf"$\alpha={alpha_text}$; {predictions[alpha_text]}",
        )
    axes[1].set_yscale("log")
    axes[1].set_title("Truncated endpoint contribution")
    axes[1].set_xlabel(r"cutoff depth $\log_{10}(1/\delta)$")
    axes[1].set_ylabel(r"$K_\alpha(\delta)$ [dimensionless, log scale]")
    axes[1].set_xticks(x_values)
    axes[1].grid(alpha=0.25, which="both")
    axes[1].legend(frameon=False, fontsize=8)

    fig.suptitle(r"Critical moment--work diagnostics at $p=2$ (80 decimal digits)")
    fig.text(
        0.5,
        0.015,
        (
            "Fixed protocol 02c | markers: finite-cutoff numerics; dashed lines: proved cusp limits | "
            "$K_\\alpha(\\delta)$ is not the full $S_2$ mass"
        ),
        ha="center",
        fontsize=8.5,
    )
    fig.tight_layout(rect=(0, 0.065, 1, 0.94))
    fig.savefig(OUTPUT_PNG, dpi=220)
    fig.savefig(OUTPUT_SVG)
    plt.close(fig)


def environment_record() -> dict:
    return {
        "python_executable": sys.executable,
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "mpmath": mp.__version__,
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
    }


def run() -> int:
    refuse_overwrite()
    mp.mp.dps = DPS
    started = time.perf_counter()
    created_utc = datetime.now(timezone.utc).isoformat()
    observed_gate_hashes = verify_gate_hashes()
    script_hash = sha256(Path(__file__).resolve())
    failures: list[dict] = []

    tau_rows, tau_by_alpha = tau_checks(failures)
    derivative_rows = derivative_checks(failures)
    tail_rows, cusp_rows, _tails = tail_checks_and_cusp_diagnostics(failures)
    contribution_rows, integrand_rows, monotonicity_rows, contribution_values = (
        endpoint_diagnostics(failures, tau_by_alpha)
    )
    make_figure(cusp_rows, contribution_values)

    elapsed = time.perf_counter() - started
    exact_passed = all(row["passed"] for row in tau_rows + derivative_rows + tail_rows)
    structural_passed = all(row["positive"] for row in contribution_rows) and all(
        row["strictly_increases_as_delta_decreases"] for row in monotonicity_rows
    )
    status = "passed" if exact_passed and structural_passed and not failures else "failed"
    source_hashes = dict(observed_gate_hashes)
    source_hashes["numerics/check_critical_frontier.py"] = script_hash
    figure_hashes = {
        OUTPUT_PNG.name: sha256(OUTPUT_PNG),
        OUTPUT_SVG.name: sha256(OUTPUT_SVG),
    }

    payload = {
        "schema_version": 1,
        "status": status,
        "created_utc": created_utc,
        "purpose": "fixed deterministic illustrations of the reviewed critical moment/work frontier",
        "protocol": {
            "alphas": list(ALPHA_TEXTS),
            "p": P_TEXT,
            "beta": BETA_TEXT,
            "deltas": list(DELTA_TEXTS),
            "decimal_precision": DPS,
            "exact_identity_acceptance": "strictly below 1e-60",
            "outcome_dependent_tuning": False,
        },
        "provenance": {
            "command": [sys.executable, str(Path(__file__).resolve())],
            "git_revision": git_revision(),
            "source_and_gate_hashes_sha256_verified_before_numerics": source_hashes,
            "lean_gate_logs_read_before_numerics": {
                "build_log": "lean/critical-moment-work/build.log",
                "axiom_log": "lean/critical-moment-work/axioms.log",
            },
            "environment": environment_record(),
            "runtime_seconds": f"{elapsed:.9f}",
            "figure_hashes_sha256": figure_hashes,
        },
        "exact_identity_acceptance_checks": {
            "all_passed": exact_passed,
            "tau_quadrature_vs_gamma": tau_rows,
            "derivatives_orders_0_through_12": derivative_rows,
            "tail_quadrature_vs_incomplete_beta": tail_rows,
        },
        "structural_checks": {
            "all_passed": structural_passed,
            "endpoint_contribution_positivity": [
                {
                    "alpha": row["alpha"],
                    "delta": row["delta"],
                    "positive": row["positive"],
                }
                for row in contribution_rows
            ],
            "endpoint_contribution_monotonicity": monotonicity_rows,
        },
        "asymptotic_diagnostics_without_acceptance_threshold": {
            "cusp_ratios": cusp_rows,
            "scaled_endpoint_integrands": integrand_rows,
            "truncated_endpoint_contributions": contribution_rows,
            "theory_predictions_from_T22": {
                "alpha_0.5": "finite limit",
                "alpha_1": "logarithmic divergence",
                "alpha_2": "power divergence",
            },
        },
        "failures": failures,
        "scope": {
            "deterministic_not_stochastic": True,
            "K_alpha_delta_is_not_full_S2": True,
            "finite_asymptotic_ratios_are_not_convergence_proofs": True,
            "four_cutoffs_do_not_prove_integrability_or_divergence": True,
            "signed_scalar_ode_remains_globally_solvable": True,
            "diagnostic_concerns_original_tree_representation": True,
        },
    }
    with OUTPUT_JSON.open("x", encoding="utf-8") as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")

    log_payload = {
        "status": status,
        "command": payload["provenance"]["command"],
        "runtime_seconds": payload["provenance"]["runtime_seconds"],
        "decimal_precision": DPS,
        "exact_identity_checks_passed": exact_passed,
        "structural_checks_passed": structural_passed,
        "failure_count": len(failures),
        "failures": failures,
        "json": str(OUTPUT_JSON),
        "png": str(OUTPUT_PNG),
        "svg": str(OUTPUT_SVG),
        "source_and_gate_hashes_sha256": source_hashes,
        "environment": payload["provenance"]["environment"],
    }
    with OUTPUT_LOG.open("x", encoding="utf-8") as stream:
        json.dump(log_payload, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps(log_payload, indent=2, sort_keys=True))
    return 0 if status == "passed" else 1


def preserve_unexpected_failure(exc: BaseException) -> None:
    failure = {
        "status": "failed_before_completion",
        "exception_type": type(exc).__name__,
        "exception": str(exc),
        "traceback": traceback.format_exc(),
        "python_executable": sys.executable,
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    for path in (OUTPUT_LOG, OUTPUT_JSON):
        if not path.exists():
            with path.open("x", encoding="utf-8") as stream:
                json.dump(failure, stream, indent=2, sort_keys=True)
                stream.write("\n")


if __name__ == "__main__":
    try:
        raise SystemExit(run())
    except SystemExit:
        raise
    except BaseException as error:
        preserve_unexpected_failure(error)
        raise
