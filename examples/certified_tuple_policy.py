"""Generate or independently recheck static Allen--Cahn tuple certificates."""

from __future__ import annotations

import argparse
from dataclasses import asdict
from fractions import Fraction as F
import gzip
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import time

from parabolab.rate_certificate import CertificateFailure, flat_terminal_state
from parabolab.tuple_certificate import (
    TupleBoxStep,
    TupleMomentCertificate,
    enclose_tuple_moment,
    verify_tuple_moment_certificate,
)


RUN_DIRECTORY = Path("docs/research/runs/2026-09-16-certified-tuple-policy/numerics")
HORIZONS = (F(1, 20), F(1, 5), F(1, 2))
RATES = (F(3, 4), F(1))
POLICIES = {
    "uniform_baseline": (F(1, 2), F(1, 2), F(1, 2)),
    "flat_safe": (F(19, 20), F(19, 20), F(19, 20)),
    "wave_safe": (F(1, 2), F(1, 2), F(19, 20)),
    "wave_safe_nonzero": (F(1, 2), F(2, 3), F(19, 20)),
}
STEP_COUNTS = (200, 400)
PRECISION_BITS = 60


def _state(value):
    return None if value is None else tuple(map(F, value))


def _decode_certificate(data) -> TupleMomentCertificate:
    return TupleMomentCertificate(
        data["family"],
        None if data["phi"] is None else F(data["phi"]),
        F(data["horizon"]),
        F(data["rate"]),
        tuple(map(F, data["q"])),
        _state(data["lower"]),
        _state(data["upper"]),
        tuple(
            TupleBoxStep(
                F(witness["duration"]),
                tuple(map(F, witness["q"])),
                _state(witness["upper_start"]),
                _state(witness["upper_end"]),
                _state(witness["lower_start"]),
                _state(witness["lower_end"]),
            )
            for witness in data["witnesses"]
        ),
        data["precision_bits"],
        data["mechanism"],
    )


def _flat_reference(horizon: F, rate: F, q: tuple[F, F, F]) -> float:
    """Independent floating ODE diagnostic, not part of the certificate."""
    import numpy as np
    from scipy.integrate import solve_ivp

    lam = float(rate)
    probabilities = np.array(tuple(map(float, q)))
    initial = np.array(tuple(map(float, flat_terminal_state(F(1, 2)))))

    def rhs(_time, y):
        _, d, a, b, c, e = y
        q0, q1, q2 = probabilities
        branch = np.array((
            a,
            b * d,
            a * b / q0 + d * d * c / (4 * (1 - q0)),
            a * c / q1 + d * d * e / (4 * (1 - q1)),
            a * e / q2,
            0.0,
        ))
        return lam * y + branch / lam

    solution = solve_ivp(
        rhs,
        (0.0, float(horizon)),
        initial,
        method="DOP853",
        rtol=2e-12,
        atol=2e-14,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    return float(solution.y[0, -1])


def _key(family: str, policy: str, horizon: F, rate: F, steps: int) -> str:
    return f"{family}/{policy}/T={horizon}/lambda={rate}/steps={steps}"


def _verify_archive(path: Path) -> dict:
    payload = json.loads(gzip.decompress(path.read_bytes()))
    checks = []
    started = time.perf_counter()
    for record in payload["records"]:
        if record["status"] != "certified":
            continue
        certificate = _decode_certificate(record["certificate"])
        checks.append({
            "key": record["key"],
            "valid": verify_tuple_moment_certificate(certificate),
        })
    elapsed = time.perf_counter() - started
    return {
        "archive": str(path),
        "certificates_checked": len(checks),
        "all_witnesses_valid": bool(checks) and all(item["valid"] for item in checks),
        "verification_seconds": elapsed,
        "checks": checks,
    }


def _source_hashes(root: Path) -> dict[str, str]:
    paths = (
        "parabolab/tuple_certificate.py",
        "parabolab/rate_certificate.py",
        "parabolab/mechanism.py",
        "parabolab/tree.py",
        "tests/test_tuple_certificate.py",
        "examples/certified_tuple_policy.py",
        "docs/research/runs/2026-09-16-certified-tuple-policy/numerics/protocol.json",
        "docs/research/runs/2026-09-16-certified-tuple-policy/numerics/protocol-amendment-wave-q1.json",
    )
    return {
        path: hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in paths
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=RUN_DIRECTORY)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()

    if args.verify is not None:
        result = _verify_archive(args.verify)
        print(json.dumps(result, indent=2))
        if not result["all_witnesses_valid"]:
            raise SystemExit(1)
        return

    protocol_path = args.output / "protocol.json"
    amendment_path = args.output / "protocol-amendment-wave-q1.json"
    if not protocol_path.exists() or not amendment_path.exists():
        raise RuntimeError(
            "predeclared protocol and wave-q1 amendment are required before evaluation"
        )

    root = Path(__file__).resolve().parents[1]
    records = []
    certificates = {}
    setup_started = time.perf_counter()
    for family, policy_names in (
        ("flat", ("uniform_baseline", "flat_safe")),
        ("wave", ("uniform_baseline", "wave_safe")),
    ):
        for policy_name in policy_names:
            q = POLICIES[policy_name]
            for horizon in HORIZONS:
                for rate in RATES:
                    for steps in STEP_COUNTS:
                        key = _key(family, policy_name, horizon, rate, steps)
                        started = time.perf_counter()
                        try:
                            certificate = enclose_tuple_moment(
                                family=family,
                                phi=F(1, 2),
                                horizon=horizon,
                                rate=rate,
                                q=q,
                                steps=steps,
                                precision_bits=PRECISION_BITS,
                            )
                        except CertificateFailure as error:
                            records.append({
                                "key": key,
                                "family": family,
                                "policy": policy_name,
                                "horizon": str(horizon),
                                "rate": str(rate),
                                "steps": steps,
                                "status": "inconclusive",
                                "reason": str(error),
                                "setup_seconds": time.perf_counter() - started,
                            })
                            print(f"{key}: inconclusive ({error})", flush=True)
                            continue
                        certificates[key] = certificate
                        record = {
                            "key": key,
                            "family": family,
                            "policy": policy_name,
                            "horizon": str(horizon),
                            "rate": str(rate),
                            "steps": steps,
                            "status": "certified",
                            "root_lower_exact": (
                                None if certificate.root_lower is None
                                else str(certificate.root_lower)
                            ),
                            "root_upper_exact": str(certificate.root_upper),
                            "root_lower": (
                                None if certificate.root_lower is None
                                else float(certificate.root_lower)
                            ),
                            "root_upper": float(certificate.root_upper),
                            "setup_seconds": time.perf_counter() - started,
                            "certificate": asdict(certificate),
                        }
                        if family == "flat":
                            mean_squared = 1.0 / (
                                1.0 + 3.0 * math.exp(-2.0 * float(horizon))
                            )
                            record["variance_interval_diagnostic"] = {
                                "role": "noncertified because the common mean-squared reference is floating",
                                "common_solution_squared_formula": "1/(1+3*exp(-2*T))",
                                "common_solution_squared": mean_squared,
                                "lower": float(certificate.root_lower) - mean_squared,
                                "upper": float(certificate.root_upper) - mean_squared,
                            }
                        records.append(record)
                        print(
                            f"{key}: [{record_value(certificate.root_lower)}, "
                            f"{float(certificate.root_upper):.12g}]",
                            flush=True,
                        )

    # Separately predeclared amendment: a theory gate supports q1=2/3 at T=1/20.
    for rate in RATES:
        for steps in STEP_COUNTS:
            family, policy_name, horizon = "wave", "wave_safe_nonzero", F(1, 20)
            q = POLICIES[policy_name]
            key = _key(family, policy_name, horizon, rate, steps)
            started = time.perf_counter()
            try:
                certificate = enclose_tuple_moment(
                    family=family,
                    horizon=horizon,
                    rate=rate,
                    q=q,
                    steps=steps,
                    precision_bits=PRECISION_BITS,
                )
            except CertificateFailure as error:
                records.append({
                    "key": key,
                    "family": family,
                    "policy": policy_name,
                    "horizon": str(horizon),
                    "rate": str(rate),
                    "steps": steps,
                    "status": "inconclusive",
                    "reason": str(error),
                    "setup_seconds": time.perf_counter() - started,
                })
                print(f"{key}: inconclusive ({error})", flush=True)
                continue
            certificates[key] = certificate
            records.append({
                "key": key,
                "family": family,
                "policy": policy_name,
                "horizon": str(horizon),
                "rate": str(rate),
                "steps": steps,
                "status": "certified",
                "root_lower_exact": None,
                "root_upper_exact": str(certificate.root_upper),
                "root_lower": None,
                "root_upper": float(certificate.root_upper),
                "setup_seconds": time.perf_counter() - started,
                "certificate": asdict(certificate),
            })
            print(
                f"{key}: [None, {float(certificate.root_upper):.12g}]",
                flush=True,
            )
    setup_seconds = time.perf_counter() - setup_started

    verification_started = time.perf_counter()
    direct_checks = {
        key: verify_tuple_moment_certificate(certificate)
        for key, certificate in certificates.items()
    }
    verification_seconds = time.perf_counter() - verification_started
    if not all(direct_checks.values()):
        raise RuntimeError("exact witness verification failed")

    reference_started = time.perf_counter()
    references = {}
    for policy_name in ("uniform_baseline", "flat_safe"):
        q = POLICIES[policy_name]
        for horizon in HORIZONS:
            mean_squared = 1.0 / (1.0 + 3.0 * math.exp(-2.0 * float(horizon)))
            for rate in RATES:
                reference_key = (
                    f"flat/{policy_name}/T={horizon}/lambda={rate}"
                )
                try:
                    value = _flat_reference(horizon, rate, q)
                except RuntimeError as error:
                    references[reference_key] = {
                        "role": "floating noncertified diagnostic",
                        "status": "inconclusive",
                        "reason": str(error),
                    }
                    continue
                enclosures = []
                for steps in STEP_COUNTS:
                    certificate = certificates.get(
                        _key("flat", policy_name, horizon, rate, steps)
                    )
                    if certificate is None:
                        continue
                    contains = (
                        float(certificate.root_lower) <= value
                        <= float(certificate.root_upper)
                    )
                    enclosures.append({"steps": steps, "contained": contains})
                    if not contains:
                        raise RuntimeError(
                            f"independent flat reference outside {reference_key}"
                        )
                references[reference_key] = {
                    "role": "floating noncertified diagnostic",
                    "status": "completed",
                    "method": "SciPy solve_ivp DOP853, rtol=2e-12, atol=2e-14",
                    "root_second_moment": value,
                    "common_solution_squared": mean_squared,
                    "variance_reference": value - mean_squared,
                    "enclosures": enclosures,
                }
    reference_seconds = time.perf_counter() - reference_started

    comparisons = []
    for family, safe_name in (("flat", "flat_safe"), ("wave", "wave_safe")):
        for horizon in HORIZONS:
            for rate in RATES:
                for steps in STEP_COUNTS:
                    baseline = certificates.get(
                        _key(family, "uniform_baseline", horizon, rate, steps)
                    )
                    safe = certificates.get(
                        _key(family, safe_name, horizon, rate, steps)
                    )
                    comparison = {
                        "family": family,
                        "horizon": str(horizon),
                        "rate": str(rate),
                        "steps": steps,
                        "baseline_status": "certified" if baseline else "inconclusive",
                        "candidate_status": "certified" if safe else "inconclusive",
                    }
                    if baseline is not None and safe is not None:
                        if family == "flat":
                            gap = baseline.root_lower - safe.root_upper
                            comparison.update({
                                "certified_separation": gap > 0,
                                "baseline_lower_minus_candidate_upper_exact": str(gap),
                                "baseline_lower_minus_candidate_upper": float(gap),
                                "meaning": "two-sided root second-moment separation",
                            })
                        else:
                            improvement = baseline.root_upper - safe.root_upper
                            comparison.update({
                                "envelope_upper_improvement_exact": str(improvement),
                                "envelope_upper_improvement": float(improvement),
                                "meaning": (
                                    "spatial-supremum envelope comparison only; "
                                    "does not prove actual-moment reduction"
                                ),
                            })
                    comparisons.append(comparison)

    nonzero_wave_comparisons = []
    for rate in RATES:
        for steps in STEP_COUNTS:
            baseline = certificates.get(
                _key("wave", "uniform_baseline", F(1, 20), rate, steps)
            )
            candidate = certificates.get(
                _key("wave", "wave_safe_nonzero", F(1, 20), rate, steps)
            )
            comparison = {
                "horizon": "1/20",
                "rate": str(rate),
                "steps": steps,
                "baseline_status": "certified" if baseline else "inconclusive",
                "candidate_status": "certified" if candidate else "inconclusive",
                "actual_nonincrease_basis": (
                    "separate exact R>2 analytic gate from the predeclared amendment"
                ),
            }
            if baseline is not None and candidate is not None:
                difference = baseline.root_upper - candidate.root_upper
                comparison.update({
                    "envelope_upper_improvement_exact": str(difference),
                    "envelope_upper_improvement": float(difference),
                    "envelope_interpretation": (
                        "upper-envelope comparison; it does not by itself prove "
                        "the amount of actual-moment reduction"
                    ),
                })
            nonzero_wave_comparisons.append(comparison)

    payload = {
        "schema_version": 1,
        "protocol_sha256": hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
        "protocol_amendment_sha256": hashlib.sha256(amendment_path.read_bytes()).hexdigest(),
        "records": records,
    }
    packed = gzip.compress(
        json.dumps(payload, default=str, separators=(",", ":")).encode(),
        mtime=0,
    )
    archive_path = args.output / "witnesses.json.gz"
    archive_path.write_bytes(packed)
    archive_check = _verify_archive(archive_path)
    verifier = {
        "direct_all_witnesses_valid": all(direct_checks.values()),
        "direct_verification_seconds": verification_seconds,
        "roundtrip": archive_check,
    }
    (args.output / "verifier.json").write_text(
        json.dumps(verifier, indent=2) + "\n"
    )
    if not archive_check["all_witnesses_valid"]:
        raise RuntimeError("round-trip archive verification failed")

    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    import numpy
    import scipy

    summary = {
        "scope": "raw 1D Allen-Cahn static tuple policies at predeclared rates and horizons",
        "certificate": "exact rational postfixed boxes; flat two-sided, wave spatial-supremum upper only",
        "all_witnesses_valid": True,
        "certificate_counts": {
            "certified": sum(r["status"] == "certified" for r in records),
            "inconclusive": sum(r["status"] == "inconclusive" for r in records),
        },
        "comparisons": comparisons,
        "nonzero_wave_policy_comparisons": nonzero_wave_comparisons,
        "independent_flat_references": references,
        "timing_seconds": {
            "certificate_setup": setup_seconds,
            "direct_exact_verification": verification_seconds,
            "archive_roundtrip_verification": archive_check["verification_seconds"],
            "floating_references": reference_seconds,
        },
        "archive": str(archive_path),
        "archive_sha256": hashlib.sha256(packed).hexdigest(),
        "protocol_sha256": payload["protocol_sha256"],
        "protocol_amendment_sha256": payload["protocol_amendment_sha256"],
        "source_sha256": _source_hashes(root),
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": numpy.__version__,
            "scipy": scipy.__version__,
        },
        "command": (
            "MPLCONFIGDIR=/tmp/parabolab-mpl "
            "/opt/miniconda3/envs/parabolab/bin/python "
            "examples/certified_tuple_policy.py"
        ),
        "verification_command": (
            "/opt/miniconda3/envs/parabolab/bin/python "
            "examples/certified_tuple_policy.py --verify "
            "docs/research/runs/2026-09-16-certified-tuple-policy/numerics/witnesses.json.gz"
        ),
        "test_command": (
            "MPLCONFIGDIR=/tmp/parabolab-mpl "
            "/opt/miniconda3/envs/parabolab/bin/python -m pytest -q "
            "tests/test_tuple_certificate.py"
        ),
        "base_commit": revision,
        "limitations": [
            "no universal or global tuple-policy optimality claim",
            "no runtime speedup claim",
            "wave envelope comparisons do not establish actual-moment reduction",
            "the floating ODE and closed-form mean references are noncertified diagnostics",
            "a failed finite box search is inconclusive, not evidence of divergence",
            "the callback is valid only for the documented raw Allen-Cahn mechanism",
            "exact rational policies and their production float callbacks differ by roundoff",
        ],
    }
    (args.output / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({
        "certificate_counts": summary["certificate_counts"],
        "all_witnesses_valid": True,
        "timing_seconds": summary["timing_seconds"],
        "archive": str(archive_path),
    }, indent=2))


def record_value(value: F | None) -> str:
    return "None" if value is None else f"{float(value):.12g}"


if __name__ == "__main__":
    main()
