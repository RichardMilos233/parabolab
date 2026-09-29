"""Execute the fixed query-information implementation checks.

The finite block uses exact ``Fraction`` arithmetic and an actual oracle
evaluator.  The scalar block uses the two prescribed mpmath quadratures.
Run ``prepare`` only after source review; it freezes every protected input
before ``run`` is allowed to execute the scientific protocol.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.metadata
import itertools
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
from typing import Any, Callable, Iterable

import mpmath as mp


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
FORMAL_DIR = REPO / "formal"
ARTIFACT_DIR = RUN_DIR / "artifacts" / "query-information" / "checks-v1"
MANIFEST_PATH = ARTIFACT_DIR / "execution_manifest.json"
FINITE_PATH = ARTIFACT_DIR / "finite_summary.json"
MIXTURE_PATH = ARTIFACT_DIR / "budget_mixture_summary.json"
SCALAR_PATH = ARTIFACT_DIR / "scalar_checks.json"
RESULT_PATH = ARTIFACT_DIR / "check_result.json"
FAILURE_PATH = ARTIFACT_DIR / "failure.json"
RUN_LOG_PATH = ARTIFACT_DIR / "run.log"

PROTOCOL_PATH = RUN_DIR / "02e-query-information-check-protocol.md"
REVIEW_PATH = RUN_DIR / "reviews" / "T47-query-check-protocol-audit.md"
IMPLEMENTATION_PATH = Path(__file__).resolve()

PROTOCOL_SHA256 = "5e4fe3e20cad7e435142dcf37e343798e730286aa0547cdf7812a8b7a42e33c2"
REVIEW_SHA256 = "c2bd4343117f20a0b6b2e93e03d9773643a281a89fa4635cd433513f41ac1ffc"
LEAN_QUERY_SHA256 = "82422e2894fa5febb586cc6fbb23e73ae3a843d5cd84310c7be3fff38d967483"
LEAN_TRANSCRIPT_SHA256 = "997b4af24aeee366a170b6632969431d2bf5fc1e47dc440ecb00ead19d81c53c"

K_VALUES = (1, 2, 3, 4, 6)
MISS_OUTPUTS = (
    Fraction(-1, 1),
    Fraction(-1, 2),
    Fraction(0, 1),
    Fraction(1, 2),
    Fraction(1, 1),
)
SIGNS = (-1, 1)
EXPECTED_CONFIGURATIONS = 25_960
EXPECTED_ORACLE_RUNS = 334_020
EXPECTED_BASELINE_RUNS = 25_960
EXPECTED_ALTERNATIVE_RUNS = 308_060
EXPECTED_NO_HIT_RUNS = 154_030
EXPECTED_MAIN_ROWS = 105
EXPECTED_FIXED_ALTERNATIVE_CHECKS = 820
EXPECTED_CONFIG_PAIRED_CHECKS = 25_960
EXPECTED_MIXTURE_ROWS = 5
EXPECTED_REUSED_MIXTURE_RECORDS = 19_262

ROOT_CONTEXT: dict[str, Any] = {}


class ProtocolFailure(RuntimeError):
    """A fixed protocol check failed."""


@dataclass(frozen=True)
class Evaluation:
    output: Fraction
    trace: tuple[int, ...]

    @property
    def query_count(self) -> int:
        return len(self.trace)


class RunLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.stream = path.open("x", encoding="utf-8")

    def write(self, message: str) -> None:
        line = f"{utc_now()} {message}"
        self.stream.write(line + "\n")
        self.stream.flush()
        os.fsync(self.stream.fileno())
        print(line, flush=True)

    def close(self) -> None:
        if not self.stream.closed:
            self.stream.flush()
            os.fsync(self.stream.fileno())
            self.stream.close()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO.resolve()))


def write_json_new(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def fraction_json(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "exact": str(value),
    }


def fraction_token(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def mp_string(value: mp.mpf, digits: int = 80) -> str:
    return mp.nstr(value, n=digits, strip_zeros=False, min_fixed=-1000, max_fixed=1000)


def require(condition: bool, message: str, **context: Any) -> None:
    if condition:
        return
    ROOT_CONTEXT.clear()
    ROOT_CONTEXT.update(context)
    raise ProtocolFailure(message)


def subprocess_text(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)
    return result.stdout.strip()


def protected_inputs() -> list[Path]:
    return [
        PROTOCOL_PATH,
        REVIEW_PATH,
        RUN_DIR / "04o-unstable-phase-query-lower-bound.md",
        RUN_DIR / "05g-query-lower-bound-lean-contract.md",
        RUN_DIR / "06g-query-information-lean.md",
        RUN_DIR / "06h-oracle-transcript-lean.md",
        RUN_DIR / "reviews" / "T42-T43-root-correspondence.json",
        FORMAL_DIR / "EstimatorIntegrity" / "QueryInformationLowerBound.lean",
        FORMAL_DIR / "EstimatorIntegrity" / "OracleTranscript.lean",
        FORMAL_DIR / "lean-toolchain",
        FORMAL_DIR / "lakefile.lean",
        IMPLEMENTATION_PATH,
    ]


def prepare() -> None:
    if ARTIFACT_DIR.exists():
        raise FileExistsError("refusing to overwrite checks-v1 or a failed official attempt")
    require(sha256(PROTOCOL_PATH) == PROTOCOL_SHA256, "fixed protocol hash mismatch")
    require(sha256(REVIEW_PATH) == REVIEW_SHA256, "accepted review hash mismatch")
    require(
        sha256(FORMAL_DIR / "EstimatorIntegrity" / "QueryInformationLowerBound.lean")
        == LEAN_QUERY_SHA256,
        "T42 Lean source hash mismatch",
    )
    require(
        sha256(FORMAL_DIR / "EstimatorIntegrity" / "OracleTranscript.lean")
        == LEAN_TRANSCRIPT_SHA256,
        "T43 Lean source hash mismatch",
    )
    require((FORMAL_DIR / "lean-toolchain").read_text(encoding="utf-8").strip().endswith("v4.33.0"),
            "protected Lean toolchain is not v4.33.0")

    inputs = {relative(path): sha256(path) for path in protected_inputs()}
    elan_bin = Path.home() / ".elan" / "bin"
    environment = {
        "python_executable": sys.executable,
        "python_version": sys.version,
        "mpmath_version": importlib.metadata.version("mpmath"),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "lean_version": subprocess_text([str(elan_bin / "lean"), "--version"], FORMAL_DIR),
        "lake_version": subprocess_text([str(elan_bin / "lake"), "--version"], FORMAL_DIR),
        "mathlib_revision": subprocess_text(
            ["git", "-C", str(FORMAL_DIR / ".lake" / "packages" / "mathlib"), "rev-parse", "HEAD"],
            REPO,
        ),
    }
    manifest = {
        "schema_version": 1,
        "status": "prepared-before-official-run",
        "created_utc": utc_now(),
        "immutable_after_creation": True,
        "protocol_sha256": PROTOCOL_SHA256,
        "review_sha256": REVIEW_SHA256,
        "implementation_source": relative(IMPLEMENTATION_PATH),
        "implementation_source_sha256": sha256(IMPLEMENTATION_PATH),
        "input_hashes_sha256": inputs,
        "environment": environment,
        "commands": {
            "prepare": f"{sys.executable} {relative(IMPLEMENTATION_PATH)} prepare",
            "run": f"{sys.executable} {relative(IMPLEMENTATION_PATH)} run",
        },
        "finite_contract": {
            "K_values": list(K_VALUES),
            "miss_outputs": [fraction_json(value) for value in MISS_OUTPUTS],
            "expected_configurations": EXPECTED_CONFIGURATIONS,
            "expected_oracle_runs": EXPECTED_ORACLE_RUNS,
            "expected_no_hit_alternative_runs": EXPECTED_NO_HIT_RUNS,
            "expected_main_summary_rows": EXPECTED_MAIN_ROWS,
            "expected_mixture_rows": EXPECTED_MIXTURE_ROWS,
            "expected_reused_mixture_records": EXPECTED_REUSED_MIXTURE_RECORDS,
        },
        "scalar_contract": {
            "tanh_sinh_decimal_digits": 80,
            "gauss_legendre_decimal_digits": 100,
            "split_point": "1/2",
            "quadrature_maxdegree": 12,
            "comparison_absolute_tolerance": "1e-70",
            "k_values": [4, 8, 16, 32],
            "stored_significant_digits": 80,
            "primary_integral_input_decimal_digits": 80,
            "primary_row_arithmetic_decimal_digits": 100,
        },
        "scope": {
            "finite_abstract_assigned_targets": True,
            "pde_solver": False,
            "validates_universal_quantifiers": False,
            "random_sampling": False,
            "policy_receives_hidden_label": False,
        },
    }
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=False)
    write_json_new(MANIFEST_PATH, manifest)
    print(json.dumps({
        "status": "prepared",
        "manifest": str(MANIFEST_PATH),
        "implementation_source_sha256": manifest["implementation_source_sha256"],
    }))


def verify_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.is_file():
        raise ProtocolFailure("official manifest has not been prepared")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    current = {relative(path): sha256(path) for path in protected_inputs()}
    expected = manifest["input_hashes_sha256"]
    if current != expected:
        mismatch = {
            name: {"expected": expected.get(name), "actual": current.get(name)}
            for name in sorted(set(current) | set(expected))
            if current.get(name) != expected.get(name)
        }
        raise ProtocolFailure(f"protected input changed after freeze: {mismatch}")
    return manifest


def public_baseline(K: int) -> Callable[[int], Fraction]:
    return lambda cell: Fraction(cell, K + 1)


def alternative_oracle(K: int, hidden_cell: int, sign: int) -> Callable[[int], Fraction]:
    baseline = public_baseline(K)

    def oracle(cell: int) -> Fraction:
        return baseline(cell) + (Fraction(sign, 1) if cell == hidden_cell else Fraction(0, 1))

    return oracle


def evaluate_policy(
    oracle: Callable[[int], Fraction],
    baseline: Callable[[int], Fraction],
    permutation: tuple[int, ...],
    cap: int,
    miss_output: Fraction,
) -> Evaluation:
    """Run the policy without receiving a hidden cell, sign, or target."""
    trace: list[int] = []
    for cell in permutation[:cap]:
        response = oracle(cell)
        trace.append(cell)
        difference = response - baseline(cell)
        if difference != 0:
            if difference not in (Fraction(-1, 1), Fraction(1, 1)):
                raise ProtocolFailure(
                    f"oracle differs from public baseline by unsupported value {difference}"
                )
            return Evaluation(difference / 2, tuple(trace))
    return Evaluation(miss_output, tuple(trace))


def squared_loss(output: Fraction, target: Fraction) -> Fraction:
    return (output - target) ** 2


def digest_record(
    digest: Any,
    *,
    K: int,
    permutation: tuple[int, ...],
    cap: int,
    miss_output: Fraction,
    label: str,
    output: Fraction,
    trace: tuple[int, ...],
    target: Fraction,
    loss: Fraction,
) -> None:
    record = {
        "K": K,
        "cap": cap,
        "input": label,
        "loss": fraction_token(loss),
        "miss_output": fraction_token(miss_output),
        "output": fraction_token(output),
        "permutation": list(permutation),
        "target": fraction_token(target),
        "trace": list(trace),
    }
    digest.update(json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8"))
    digest.update(b"\n")


def new_row_accumulator(K: int) -> dict[str, Any]:
    return {
        "permutation_count": 0,
        "baseline_loss_sum": Fraction(0, 1),
        "baseline_cost_sum": Fraction(0, 1),
        "positive_loss_sum": Fraction(0, 1),
        "negative_loss_sum": Fraction(0, 1),
        "alternative_loss_sum": Fraction(0, 1),
        "alternative_loss_by_input": {
            (cell, sign): Fraction(0, 1) for cell in range(K) for sign in SIGNS
        },
        "configuration_count": 0,
        "oracle_run_count": 0,
        "no_hit_count": 0,
        "paired_check_count": 0,
        "minimum_paired_slack": None,
        "maximum_family_formula_discrepancy": Fraction(0, 1),
        "maximum_lower_bound_violation": Fraction(0, 1),
    }


def execute_finite_checks(log: RunLog) -> tuple[dict[str, Any], dict[str, Any]]:
    started = time.monotonic()
    digest = hashlib.sha256()
    accumulators: dict[tuple[int, int, Fraction], dict[str, Any]] = {}
    counts_by_K: dict[int, dict[str, int]] = {}
    total_configs = 0
    total_runs = 0
    baseline_runs = 0
    alternative_runs = 0
    no_hit_runs = 0
    paired_checks = 0

    for K in K_VALUES:
        log.write(f"finite block: K={K} enumeration started")
        baseline = public_baseline(K)
        counts = {
            "permutations": math.factorial(K),
            "configurations": 0,
            "baseline_runs": 0,
            "alternative_runs": 0,
            "oracle_runs": 0,
            "no_hit_alternative_runs": 0,
        }
        for permutation in itertools.permutations(range(K)):
            for cap in range(K + 1):
                for miss_output in MISS_OUTPUTS:
                    ROOT_CONTEXT.clear()
                    ROOT_CONTEXT.update({
                        "block": "finite",
                        "K": K,
                        "permutation": list(permutation),
                        "cap": cap,
                        "miss_output": fraction_token(miss_output),
                    })
                    key = (K, cap, miss_output)
                    acc = accumulators.setdefault(key, new_row_accumulator(K))
                    baseline_result = evaluate_policy(
                        baseline, baseline, permutation, cap, miss_output
                    )
                    require(
                        baseline_result.trace == permutation[:cap],
                        "baseline trace mismatch",
                        **ROOT_CONTEXT,
                        observed_trace=list(baseline_result.trace),
                    )
                    require(
                        baseline_result.output == miss_output,
                        "baseline output mismatch",
                        **ROOT_CONTEXT,
                        observed_output=fraction_token(baseline_result.output),
                    )
                    require(
                        len(set(baseline_result.trace)) <= baseline_result.query_count,
                        "distinct visited cells exceed baseline query count",
                        **ROOT_CONTEXT,
                    )
                    baseline_loss = squared_loss(baseline_result.output, Fraction(0, 1))
                    digest_record(
                        digest,
                        K=K,
                        permutation=permutation,
                        cap=cap,
                        miss_output=miss_output,
                        label="baseline",
                        output=baseline_result.output,
                        trace=baseline_result.trace,
                        target=Fraction(0, 1),
                        loss=baseline_loss,
                    )
                    acc["permutation_count"] += 1
                    acc["baseline_loss_sum"] += baseline_loss
                    acc["baseline_cost_sum"] += baseline_result.query_count
                    acc["configuration_count"] += 1
                    acc["oracle_run_count"] += 1
                    total_configs += 1
                    total_runs += 1
                    baseline_runs += 1
                    counts["configurations"] += 1
                    counts["baseline_runs"] += 1
                    counts["oracle_runs"] += 1

                    config_positive = Fraction(0, 1)
                    config_negative = Fraction(0, 1)
                    config_total = Fraction(0, 1)
                    config_no_hits = 0
                    baseline_visited = set(baseline_result.trace)
                    for hidden_cell in range(K):
                        for sign in SIGNS:
                            oracle = alternative_oracle(K, hidden_cell, sign)
                            result = evaluate_policy(
                                oracle, baseline, permutation, cap, miss_output
                            )
                            target = Fraction(sign, 2)
                            loss = squared_loss(result.output, target)
                            label = f"alternative:{hidden_cell}:{sign:+d}"
                            digest_record(
                                digest,
                                K=K,
                                permutation=permutation,
                                cap=cap,
                                miss_output=miss_output,
                                label=label,
                                output=result.output,
                                trace=result.trace,
                                target=target,
                                loss=loss,
                            )
                            if hidden_cell not in baseline_visited:
                                require(
                                    result.output == baseline_result.output,
                                    "no-hit alternative output differs from baseline",
                                    **ROOT_CONTEXT,
                                    hidden_cell=hidden_cell,
                                    sign=sign,
                                    alternative_output=fraction_token(result.output),
                                    baseline_output=fraction_token(baseline_result.output),
                                )
                                require(
                                    result.trace == baseline_result.trace,
                                    "no-hit alternative ordered trace differs from baseline",
                                    **ROOT_CONTEXT,
                                    hidden_cell=hidden_cell,
                                    sign=sign,
                                    alternative_trace=list(result.trace),
                                    baseline_trace=list(baseline_result.trace),
                                )
                                config_no_hits += 1
                                no_hit_runs += 1
                                counts["no_hit_alternative_runs"] += 1
                            else:
                                position = permutation.index(hidden_cell)
                                require(
                                    result.trace == permutation[: position + 1]
                                    and result.output == target,
                                    "hit alternative did not stop with its inferred signed output",
                                    **ROOT_CONTEXT,
                                    hidden_cell=hidden_cell,
                                    sign=sign,
                                    observed_trace=list(result.trace),
                                    observed_output=fraction_token(result.output),
                                )
                            if sign > 0:
                                config_positive += loss
                                acc["positive_loss_sum"] += loss
                            else:
                                config_negative += loss
                                acc["negative_loss_sum"] += loss
                            config_total += loss
                            acc["alternative_loss_sum"] += loss
                            acc["alternative_loss_by_input"][(hidden_cell, sign)] += loss
                            acc["oracle_run_count"] += 1
                            total_runs += 1
                            alternative_runs += 1
                            counts["alternative_runs"] += 1
                            counts["oracle_runs"] += 1

                    expected_no_hits = 2 * (K - cap)
                    require(
                        config_no_hits == expected_no_hits,
                        "configuration no-hit count mismatch",
                        **ROOT_CONTEXT,
                        observed=config_no_hits,
                        expected=expected_no_hits,
                    )
                    acc["no_hit_count"] += config_no_hits
                    direct_lower = Fraction(K - cap, 2)
                    paired_slack = config_total - direct_lower
                    require(
                        paired_slack >= 0,
                        "direct executed paired-loss inequality failed",
                        **ROOT_CONTEXT,
                        paired_total=fraction_token(config_total),
                        direct_lower=fraction_token(direct_lower),
                        slack=fraction_token(paired_slack),
                    )
                    family_mean = config_total / (2 * K)
                    formula = (1 - Fraction(cap, K)) * (
                        miss_output * miss_output + Fraction(1, 4)
                    )
                    family_discrepancy = abs(family_mean - formula)
                    require(
                        family_discrepancy == 0,
                        "executed alternative-family mean disagrees with exact formula",
                        **ROOT_CONTEXT,
                        observed=fraction_token(family_mean),
                        expected=fraction_token(formula),
                    )
                    lower = Fraction(1, 4) * (1 - Fraction(cap, K))
                    lower_slack = family_mean - lower
                    require(
                        lower_slack >= 0,
                        "executed alternative-family lower bound failed",
                        **ROOT_CONTEXT,
                        observed=fraction_token(family_mean),
                        lower=fraction_token(lower),
                    )
                    if miss_output == 0:
                        require(
                            lower_slack == 0,
                            "h=0 lower bound is not exact equality",
                            **ROOT_CONTEXT,
                            slack=fraction_token(lower_slack),
                        )
                    acc["paired_check_count"] += 1
                    acc["minimum_paired_slack"] = (
                        paired_slack
                        if acc["minimum_paired_slack"] is None
                        else min(acc["minimum_paired_slack"], paired_slack)
                    )
                    acc["maximum_family_formula_discrepancy"] = max(
                        acc["maximum_family_formula_discrepancy"], family_discrepancy
                    )
                    acc["maximum_lower_bound_violation"] = max(
                        acc["maximum_lower_bound_violation"], max(Fraction(0, 1), -lower_slack)
                    )
                    paired_checks += 1
        counts_by_K[K] = counts
        log.write(
            "finite block: K={} complete; configurations={} runs={} no_hit={}".format(
                K, counts["configurations"], counts["oracle_runs"],
                counts["no_hit_alternative_runs"]
            )
        )

    require(total_configs == EXPECTED_CONFIGURATIONS, "total configuration count mismatch",
            observed=total_configs, expected=EXPECTED_CONFIGURATIONS)
    require(total_runs == EXPECTED_ORACLE_RUNS, "total oracle run count mismatch",
            observed=total_runs, expected=EXPECTED_ORACLE_RUNS)
    require(baseline_runs == EXPECTED_BASELINE_RUNS, "baseline run count mismatch",
            observed=baseline_runs, expected=EXPECTED_BASELINE_RUNS)
    require(alternative_runs == EXPECTED_ALTERNATIVE_RUNS, "alternative run count mismatch",
            observed=alternative_runs, expected=EXPECTED_ALTERNATIVE_RUNS)
    require(no_hit_runs == EXPECTED_NO_HIT_RUNS, "no-hit run count mismatch",
            observed=no_hit_runs, expected=EXPECTED_NO_HIT_RUNS)
    require(paired_checks == EXPECTED_CONFIG_PAIRED_CHECKS, "paired check count mismatch",
            observed=paired_checks, expected=EXPECTED_CONFIG_PAIRED_CHECKS)

    summary_rows: list[dict[str, Any]] = []
    fixed_alternative_checks = 0
    global_max_formula_discrepancy = Fraction(0, 1)
    global_max_alternative_discrepancy = Fraction(0, 1)
    global_min_lower_slack: Fraction | None = None
    global_min_paired_slack: Fraction | None = None
    for K in K_VALUES:
        permutation_count = math.factorial(K)
        for cap in range(K + 1):
            for miss_output in MISS_OUTPUTS:
                acc = accumulators[(K, cap, miss_output)]
                require(acc["permutation_count"] == permutation_count,
                        "summary permutation count mismatch", K=K, cap=cap,
                        miss_output=fraction_token(miss_output))
                baseline_risk = acc["baseline_loss_sum"] / permutation_count
                baseline_cost = acc["baseline_cost_sum"] / permutation_count
                positive_risk = acc["positive_loss_sum"] / (permutation_count * K)
                negative_risk = acc["negative_loss_sum"] / (permutation_count * K)
                family_risk = acc["alternative_loss_sum"] / (permutation_count * 2 * K)
                formula = (1 - Fraction(cap, K)) * (
                    miss_output * miss_output + Fraction(1, 4)
                )
                lower = Fraction(1, 4) * (1 - Fraction(cap, K))
                lower_slack = family_risk - lower
                require(baseline_risk == miss_output * miss_output,
                        "baseline summary risk mismatch", K=K, cap=cap,
                        miss_output=fraction_token(miss_output))
                require(baseline_cost == cap, "baseline summary cost mismatch", K=K, cap=cap,
                        miss_output=fraction_token(miss_output))
                require(family_risk == formula, "summary family risk formula mismatch", K=K,
                        cap=cap, miss_output=fraction_token(miss_output))
                require(lower_slack >= 0, "summary family lower bound failed", K=K, cap=cap,
                        miss_output=fraction_token(miss_output))
                if miss_output == 0:
                    require(lower_slack == 0, "summary h=0 lower bound not exact", K=K, cap=cap)

                per_alternative: list[dict[str, Any]] = []
                for hidden_cell in range(K):
                    for sign in SIGNS:
                        observed = (
                            acc["alternative_loss_by_input"][(hidden_cell, sign)]
                            / permutation_count
                        )
                        expected = (1 - Fraction(cap, K)) * (
                            miss_output - Fraction(sign, 2)
                        ) ** 2
                        discrepancy = abs(observed - expected)
                        require(discrepancy == 0, "fixed-alternative averaged risk mismatch",
                                K=K, cap=cap, miss_output=fraction_token(miss_output),
                                hidden_cell=hidden_cell, sign=sign,
                                observed=fraction_token(observed), expected=fraction_token(expected))
                        per_alternative.append({
                            "hidden_cell": hidden_cell,
                            "sign": sign,
                            "observed_permutation_averaged_risk": fraction_json(observed),
                            "expected_risk": fraction_json(expected),
                            "difference": fraction_json(observed - expected),
                        })
                        fixed_alternative_checks += 1
                        global_max_alternative_discrepancy = max(
                            global_max_alternative_discrepancy, discrepancy
                        )

                global_max_formula_discrepancy = max(
                    global_max_formula_discrepancy,
                    abs(family_risk - formula),
                    acc["maximum_family_formula_discrepancy"],
                )
                global_min_lower_slack = (
                    lower_slack if global_min_lower_slack is None
                    else min(global_min_lower_slack, lower_slack)
                )
                row_paired_slack = acc["minimum_paired_slack"]
                global_min_paired_slack = (
                    row_paired_slack if global_min_paired_slack is None
                    else min(global_min_paired_slack, row_paired_slack)
                )
                summary_rows.append({
                    "K": K,
                    "cap": cap,
                    "miss_output": fraction_json(miss_output),
                    "permutation_count": permutation_count,
                    "configuration_count": acc["configuration_count"],
                    "oracle_run_count": acc["oracle_run_count"],
                    "no_hit_alternative_run_count": acc["no_hit_count"],
                    "baseline_expected_cost": fraction_json(baseline_cost),
                    "baseline_risk": fraction_json(baseline_risk),
                    "positive_input_mean_risk": fraction_json(positive_risk),
                    "negative_input_mean_risk": fraction_json(negative_risk),
                    "alternative_family_mean_risk": fraction_json(family_risk),
                    "closed_form_family_mean_risk": fraction_json(formula),
                    "family_formula_difference": fraction_json(family_risk - formula),
                    "family_lower_bound": fraction_json(lower),
                    "family_lower_bound_slack": fraction_json(lower_slack),
                    "configuration_paired_checks": acc["paired_check_count"],
                    "minimum_direct_paired_loss_slack": fraction_json(row_paired_slack),
                    "maximum_configuration_formula_discrepancy": fraction_json(
                        acc["maximum_family_formula_discrepancy"]
                    ),
                    "per_alternative_risks": per_alternative,
                })

    require(len(summary_rows) == EXPECTED_MAIN_ROWS, "main summary row count mismatch",
            observed=len(summary_rows), expected=EXPECTED_MAIN_ROWS)
    require(fixed_alternative_checks == EXPECTED_FIXED_ALTERNATIVE_CHECKS,
            "fixed-alternative comparison count mismatch",
            observed=fixed_alternative_checks, expected=EXPECTED_FIXED_ALTERNATIVE_CHECKS)
    require(global_min_lower_slack is not None and global_min_paired_slack is not None,
            "finite minima were not populated")

    finite = {
        "schema_version": 1,
        "status": "PASS",
        "arithmetic": "fractions.Fraction exact rational arithmetic",
        "evaluator_hidden_label_argument": False,
        "counts": {
            "configurations": total_configs,
            "baseline_runs": baseline_runs,
            "alternative_runs": alternative_runs,
            "oracle_runs": total_runs,
            "no_hit_alternative_runs": no_hit_runs,
            "configuration_paired_checks": paired_checks,
            "main_summary_rows": len(summary_rows),
            "fixed_alternative_permutation_risk_checks": fixed_alternative_checks,
        },
        "counts_by_K": {str(key): value for key, value in counts_by_K.items()},
        "streamed_run_record_sha256": digest.hexdigest(),
        "global_exact_statistics": {
            "maximum_family_formula_discrepancy": fraction_json(global_max_formula_discrepancy),
            "maximum_fixed_alternative_formula_discrepancy": fraction_json(
                global_max_alternative_discrepancy
            ),
            "minimum_family_lower_bound_slack": fraction_json(global_min_lower_slack),
            "minimum_direct_paired_loss_slack": fraction_json(global_min_paired_slack),
        },
        "summary_rows": summary_rows,
        "elapsed_seconds": time.monotonic() - started,
        "scope": {
            "abstract_assigned_targets": True,
            "not_pde_values": True,
            "not_universal_algorithm_validation": True,
        },
    }
    log.write(
        f"finite block PASS: {total_configs} configurations, {total_runs} runs, "
        f"{no_hit_runs} no-hit alternatives, digest={digest.hexdigest()}"
    )
    return finite, accumulators


def execute_budget_mixture(
    accumulators: dict[tuple[int, int, Fraction], dict[str, Any]], log: RunLog
) -> dict[str, Any]:
    started = time.monotonic()
    rows: list[dict[str, Any]] = []
    reused_records = 0
    for K in K_VALUES:
        permutation_count = math.factorial(K)
        low = accumulators[(K, 0, Fraction(0, 1))]
        high = accumulators[(K, K, Fraction(0, 1))]

        def average(acc: dict[str, Any], field: str) -> Fraction:
            return acc[field] / permutation_count

        baseline_cost = Fraction(1, 4) * average(low, "baseline_cost_sum") + Fraction(
            3, 4
        ) * average(high, "baseline_cost_sum")
        baseline_risk = Fraction(1, 4) * average(low, "baseline_loss_sum") + Fraction(
            3, 4
        ) * average(high, "baseline_loss_sum")
        per_alternative: list[dict[str, Any]] = []
        positive_total = Fraction(0, 1)
        negative_total = Fraction(0, 1)
        for hidden_cell in range(K):
            for sign in SIGNS:
                risk = Fraction(1, 4) * (
                    low["alternative_loss_by_input"][(hidden_cell, sign)] / permutation_count
                ) + Fraction(3, 4) * (
                    high["alternative_loss_by_input"][(hidden_cell, sign)] / permutation_count
                )
                require(risk == Fraction(1, 16), "mixture alternative risk mismatch", K=K,
                        hidden_cell=hidden_cell, sign=sign, observed=fraction_token(risk))
                per_alternative.append({
                    "hidden_cell": hidden_cell,
                    "sign": sign,
                    "risk": fraction_json(risk),
                })
                if sign > 0:
                    positive_total += risk
                else:
                    negative_total += risk
        require(baseline_cost == Fraction(3 * K, 4), "mixture baseline cost mismatch", K=K,
                observed=fraction_token(baseline_cost))
        require(baseline_risk == 0, "mixture baseline risk mismatch", K=K,
                observed=fraction_token(baseline_risk))
        reused_for_K = low["oracle_run_count"] + high["oracle_run_count"]
        expected_reused = 2 * permutation_count * (2 * K + 1)
        require(reused_for_K == expected_reused, "mixture endpoint reuse count mismatch", K=K,
                observed=reused_for_K, expected=expected_reused)
        reused_records += reused_for_K
        rows.append({
            "K": K,
            "weights": {
                "cap_0": fraction_json(Fraction(1, 4)),
                "cap_K": fraction_json(Fraction(3, 4)),
            },
            "miss_output": fraction_json(Fraction(0, 1)),
            "additional_oracle_runs": 0,
            "reused_main_sweep_records": reused_for_K,
            "baseline_expected_cost": fraction_json(baseline_cost),
            "baseline_risk": fraction_json(baseline_risk),
            "positive_input_mean_risk": fraction_json(positive_total / K),
            "negative_input_mean_risk": fraction_json(negative_total / K),
            "alternative_family_mean_risk": fraction_json(
                (positive_total + negative_total) / (2 * K)
            ),
            "per_alternative_risks": per_alternative,
        })
    require(len(rows) == EXPECTED_MIXTURE_ROWS, "mixture summary row count mismatch",
            observed=len(rows), expected=EXPECTED_MIXTURE_ROWS)
    require(reused_records == EXPECTED_REUSED_MIXTURE_RECORDS,
            "total mixture reused-record count mismatch", observed=reused_records,
            expected=EXPECTED_REUSED_MIXTURE_RECORDS)
    log.write(f"budget mixture PASS: 5 rows, {reused_records} records reused, 0 new runs")
    return {
        "schema_version": 1,
        "status": "PASS",
        "summary_rows": rows,
        "row_count": len(rows),
        "reused_main_sweep_records": reused_records,
        "additional_oracle_runs": 0,
        "elapsed_seconds": time.monotonic() - started,
        "interpretation": {
            "finite_abstract_information_lemma_sharpness": True,
            "matching_pde_upper_bound": False,
        },
    }


def bump(z: mp.mpf) -> mp.mpf:
    if z <= 0 or z >= 1:
        return mp.mpf("0")
    return mp.exp(-1 / (z * (1 - z)))


def comparison_record(actual: mp.mpf, target: mp.mpf, base_tolerance: mp.mpf) -> dict[str, Any]:
    difference = abs(actual - target)
    tolerance = base_tolerance * (1 + abs(target))
    return {
        "actual": mp_string(actual),
        "target": mp_string(target),
        "absolute_difference": mp_string(difference),
        "combined_tolerance": mp_string(tolerance),
        "passed": bool(difference <= tolerance),
    }


def execute_scalar_checks(log: RunLog) -> dict[str, Any]:
    started = time.monotonic()
    ROOT_CONTEXT.clear()
    ROOT_CONTEXT.update({"block": "scalar", "stage": "tanh-sinh-80"})
    log.write("scalar block: 80-digit tanh-sinh quadrature started")
    with mp.workdps(80):
        half = mp.mpf(1) / 2
        i80 = mp.quadts(bump, [0, half], maxdegree=12) + mp.quadts(
            bump, [half, 1], maxdegree=12
        )
        i80_text = mp_string(i80, 80)
    ROOT_CONTEXT.clear()
    ROOT_CONTEXT.update({"block": "scalar", "stage": "gauss-legendre-100"})
    log.write("scalar block: 100-digit Gauss-Legendre quadrature started")
    with mp.workdps(100):
        half = mp.mpf(1) / 2
        i100 = mp.quadgl(bump, [0, half], maxdegree=12) + mp.quadgl(
            bump, [half, 1], maxdegree=12
        )
        i100_text = mp_string(i100, 100)
        i80_primary = mp.mpf(i80_text)
        quadrature_difference = abs(i80_primary - i100)
        tolerance = mp.mpf("1e-70")
        ROOT_CONTEXT.clear()
        ROOT_CONTEXT.update({
            "block": "scalar",
            "stage": "quadrature-comparison",
            "i80": i80_text,
            "i100": i100_text,
        })
        require(quadrature_difference <= tolerance, "independent quadratures disagree",
                i80=i80_text, i100=i100_text,
                absolute_difference=mp_string(quadrature_difference, 100),
                tolerance="1e-70")

        a = mp.mpf(1) / 8
        q = mp.mpf(2)
        dimension_constant = 2 * mp.pi
        kappa = mp.exp(-mp.mpf(1) / 8) / mp.sqrt(2 * mp.pi)
        delta = kappa / (32 * mp.e * 4 * dimension_constant)
        t0 = max(
            mp.mpf(1),
            1 + q * mp.log(4) - mp.log(kappa * a * i80_primary),
        )
        derivative_peak_bound = 16 * mp.exp(-4)
        bump_sup_bound = mp.exp(-4)
        require(derivative_peak_bound < 1, "analytic derivative certificate numeric inequality failed")
        require(bump_sup_bound < 1, "analytic bump supremum numeric inequality failed")
        require(i80_primary > 0, "computed primary bump integral is not positive")

        rows: list[dict[str, Any]] = []
        identity_checks = 0
        inequality_checks = 0
        for k in (4, 8, 16, 32):
            T = 1 + mp.log((mp.mpf(k) + mp.mpf(1) / 2) ** 2 / (kappa * a * i80_primary))
            ROOT_CONTEXT.clear()
            ROOT_CONTEXT.update({
                "block": "scalar",
                "stage": "prescribed-row",
                "k": k,
                "T": mp_string(T),
            })
            mu = a * i80_primary / (mp.mpf(k) ** 2)
            c = kappa * mu
            B = c * mp.exp(T - 1)
            ell = B / mp.sqrt(1 + c**2 * (mp.exp(2 * (T - 1)) - 1))
            background = delta * mu * mp.exp(T)
            B_rearranged = (mp.mpf(k) + mp.mpf(1) / 2) ** 2 / (mp.mpf(k) ** 2)
            ell_rearranged = B / mp.sqrt(1 + B**2 - c**2)
            R = mp.exp((mp.log(kappa * a * i80_primary) + T - 1) / 2)
            R_target = mp.mpf(k) + mp.mpf(1) / 2

            B_check = comparison_record(B, B_rearranged, tolerance)
            ell_check = comparison_record(ell, ell_rearranged, tolerance)
            R_check = comparison_record(R, R_target, tolerance)
            require(B_check["passed"], "B rearranged identity failed", k=k, check=B_check)
            require(ell_check["passed"], "ell rearranged identity failed", k=k, check=ell_check)
            require(R_check["passed"], "R identity failed", k=k, check=R_check)
            require(int(mp.floor(R)) == k, "floor(R) mismatch", k=k, R=mp_string(R))
            inequalities = {
                "T_ge_T0": bool(T >= t0),
                "one_le_B": bool(1 <= B),
                "B_le_four": bool(B <= 4),
                "zero_lt_c": bool(0 < c),
                "c_lt_one": bool(c < 1),
                "ell_ge_inv_sqrt_two": bool(ell >= 1 / mp.sqrt(2)),
                "background_le_one_over_32": bool(background <= mp.mpf(1) / 32),
                "ell_minus_background_gt_one_half": bool(
                    ell - background > mp.mpf(1) / 2
                ),
            }
            require(all(inequalities.values()), "scalar inequality failed", k=k,
                    inequalities=inequalities)
            identity_checks += 3
            inequality_checks += len(inequalities) + 1  # includes floor(R)=k
            rows.append({
                "k": k,
                "T": mp_string(T),
                "mu": mp_string(mu),
                "c": mp_string(c),
                "B": mp_string(B),
                "ell": mp_string(ell),
                "background": mp_string(background),
                "ell_minus_background": mp_string(ell - background),
                "R": mp_string(R),
                "floor_R": int(mp.floor(R)),
                "B_rearranged": mp_string(B_rearranged),
                "ell_rearranged": mp_string(ell_rearranged),
                "identity_checks": {
                    "B": B_check,
                    "ell": ell_check,
                    "R": R_check,
                },
                "inequality_checks": inequalities,
            })

        result = {
            "schema_version": 1,
            "status": "PASS",
            "quadrature": {
                "integrand": "exp(-1/(z*(1-z))) on 0<z<1, zero otherwise",
                "split_point": "0.5",
                "tanh_sinh": {
                    "decimal_digits": 80,
                    "maxdegree": 12,
                    "value": i80_text,
                    "used_for_primary_rows": True,
                },
                "gauss_legendre": {
                    "decimal_digits": 100,
                    "maxdegree": 12,
                    "value": i100_text,
                    "used_for_primary_rows": False,
                },
                "absolute_difference": mp_string(quadrature_difference, 100),
                "absolute_tolerance": "1e-70",
                "passed": True,
                "rigorous_enclosure": False,
            },
            "analytic_derivative_certificate": {
                "r_lower_bound": "r=1/(z*(1-z)) >= 4",
                "derivative_bound": "|psi'| <= r^2 exp(-r) <= 16 exp(-4) < 1",
                "sixteen_exp_minus_four": mp_string(derivative_peak_bound),
                "psi_bound": "psi <= exp(-4) < 1",
                "exp_minus_four": mp_string(bump_sup_bound),
                "D": "1",
                "uses_grid_supremum": False,
            },
            "constants": {
                "a": mp_string(a),
                "q": mp_string(q),
                "D_s": mp_string(dimension_constant),
                "kappa": mp_string(kappa),
                "delta": mp_string(delta),
                "T0": mp_string(t0),
                "primary_I": i80_text,
            },
            "identity_check_count": identity_checks,
            "inequality_check_count": inequality_checks,
            "rows": rows,
            "row_count": len(rows),
            "elapsed_seconds": time.monotonic() - started,
            "scope": {
                "formula_implementation_check": True,
                "primary_integral_input_decimal_digits": 80,
                "primary_row_arithmetic_decimal_digits": 100,
                "pde_discretization": False,
                "heat_minorization_validated": False,
                "universal_input_class_validated": False,
                "digits_are_rigorously_certified": False,
            },
        }
    log.write(
        "scalar block PASS: quadratures agree within 1e-70; 4 prescribed rows passed"
    )
    return result


def run() -> int:
    if not MANIFEST_PATH.is_file():
        raise ProtocolFailure("official manifest has not been prepared")
    protected_outputs = (
        FINITE_PATH,
        MIXTURE_PATH,
        SCALAR_PATH,
        RESULT_PATH,
        FAILURE_PATH,
        RUN_LOG_PATH,
    )
    if any(path.exists() for path in protected_outputs):
        raise FileExistsError("refusing to overwrite an official or failed checks-v1 run")
    started = time.monotonic()
    log = RunLog(RUN_LOG_PATH)
    try:
        manifest = verify_manifest()
        log.write("official T49 run started from verified frozen manifest")
        finite, accumulators = execute_finite_checks(log)
        write_json_new(FINITE_PATH, finite)
        log.write(f"preserved completed finite block: {relative(FINITE_PATH)}")
        mixture = execute_budget_mixture(accumulators, log)
        write_json_new(MIXTURE_PATH, mixture)
        log.write(f"preserved completed mixture block: {relative(MIXTURE_PATH)}")
        scalar = execute_scalar_checks(log)
        write_json_new(SCALAR_PATH, scalar)
        log.write(f"preserved completed scalar block: {relative(SCALAR_PATH)}")
        elapsed = time.monotonic() - started
        log.write(f"official T49 checks PASS; elapsed_seconds={elapsed:.9f}")
        log.close()
        result = {
            "schema_version": 1,
            "status": "PASS",
            "created_utc": utc_now(),
            "elapsed_seconds": elapsed,
            "manifest_sha256": sha256(MANIFEST_PATH),
            "implementation_source_sha256": manifest["implementation_source_sha256"],
            "outputs": {
                relative(FINITE_PATH): sha256(FINITE_PATH),
                relative(MIXTURE_PATH): sha256(MIXTURE_PATH),
                relative(SCALAR_PATH): sha256(SCALAR_PATH),
                relative(RUN_LOG_PATH): sha256(RUN_LOG_PATH),
            },
            "gates": {
                "finite_status": finite["status"],
                "mixture_status": mixture["status"],
                "scalar_status": scalar["status"],
                "oracle_runs": finite["counts"]["oracle_runs"],
                "no_hit_alternative_runs": finite["counts"]["no_hit_alternative_runs"],
                "main_summary_rows": finite["counts"]["main_summary_rows"],
                "mixture_summary_rows": mixture["row_count"],
                "quadrature_passed": scalar["quadrature"]["passed"],
            },
            "interpretation": {
                "finite_abstract_model_only": True,
                "pde_experiment": False,
                "universal_lower_bound_empirically_proved": False,
                "novelty_evidence": False,
            },
        }
        write_json_new(RESULT_PATH, result)
        print(json.dumps({
            "status": "PASS",
            "oracle_runs": finite["counts"]["oracle_runs"],
            "main_rows": finite["counts"]["main_summary_rows"],
            "mixture_rows": mixture["row_count"],
            "output": str(ARTIFACT_DIR),
        }))
        return 0
    except Exception as exc:
        try:
            log.write(f"official T49 checks ERROR: {type(exc).__name__}: {exc}")
        finally:
            log.close()
        failure = {
            "schema_version": 1,
            "status": "ERROR",
            "created_utc": utc_now(),
            "elapsed_seconds": time.monotonic() - started,
            "exception_type": type(exc).__name__,
            "exception": str(exc),
            "context": ROOT_CONTEXT,
            "traceback": traceback.format_exc(),
            "manifest_sha256": sha256(MANIFEST_PATH),
            "run_log_sha256": sha256(RUN_LOG_PATH),
        }
        write_json_new(FAILURE_PATH, failure)
        raise


def status() -> None:
    payload = {
        "artifact_directory_exists": ARTIFACT_DIR.exists(),
        "manifest_exists": MANIFEST_PATH.is_file(),
        "result_exists": RESULT_PATH.is_file(),
        "failure_exists": FAILURE_PATH.is_file(),
        "protocol_sha256": sha256(PROTOCOL_PATH),
        "review_sha256": sha256(REVIEW_PATH),
        "implementation_source_sha256": sha256(IMPLEMENTATION_PATH),
    }
    print(json.dumps(payload, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("status", "prepare", "run"))
    args = parser.parse_args()
    if args.action == "status":
        status()
        return 0
    if args.action == "prepare":
        prepare()
        return 0
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
