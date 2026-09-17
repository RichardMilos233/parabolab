"""Derive exact fractional flat-variance reductions from saved witnesses.

This is deterministic post-analysis of the predeclared run.  It does not
select policies or alter ``protocol.json`` or ``results.json``.  The analytic
mean identity is the conventional Allen--Cahn mean-identification result; no
claim is made that the exponential enclosure or that bridge is proved in Lean.
"""

from __future__ import annotations

from fractions import Fraction as F
import gzip
import hashlib
import json
from math import factorial
from pathlib import Path

from parabolab.tuple_certificate import (
    TupleBoxStep,
    TupleMomentCertificate,
    verify_tuple_moment_certificate,
)


HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "witnesses.json.gz"
OUTPUT = HERE / "variance-bounds.json"
LOG = HERE / "derive-variance-bounds.log"
TAYLOR_DEGREE = 30


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _state(value):
    return None if value is None else tuple(map(F, value))


def _decode(data) -> TupleMomentCertificate:
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


def exponential_enclosure(x: F, degree: int = TAYLOR_DEGREE) -> tuple[F, F]:
    """Enclose ``exp(x)`` exactly for ``0 <= x <= 1``.

    The lower bound is ``S_n = sum_{k=0}^n x^k/k!``.  Starting at term
    ``n+1``, consecutive Taylor-term ratios are at most ``x/(n+2)``;
    therefore the positive tail is at most
    ``term_{n+1} / (1 - x/(n+2))``.
    """
    if not isinstance(x, F) or not 0 <= x <= 1:
        raise ValueError("x must be an exact Fraction in [0, 1]")
    if not isinstance(degree, int) or isinstance(degree, bool) or degree < 0:
        raise ValueError("degree must be a nonnegative integer")
    lower = sum((x**k / factorial(k) for k in range(degree + 1)), F(0))
    first_omitted = x ** (degree + 1) / factorial(degree + 1)
    upper = lower + first_omitted / (1 - x / (degree + 2))
    return lower, upper


def _fraction_record(value: F) -> dict[str, str | float]:
    return {"exact": str(value), "float": float(value)}


def main() -> None:
    payload = json.loads(gzip.decompress(ARCHIVE.read_bytes()))
    flat = {}
    checked = 0
    for record in payload["records"]:
        if record["status"] != "certified" or record["family"] != "flat":
            continue
        certificate = _decode(record["certificate"])
        if not verify_tuple_moment_certificate(certificate):
            raise RuntimeError(f"invalid saved witness: {record['key']}")
        if certificate.root_lower is None:
            raise RuntimeError(f"flat witness lacks a lower bound: {record['key']}")
        flat[(record["policy"], record["horizon"], record["rate"], record["steps"])] = certificate
        checked += 1

    derived = []
    for key, baseline in sorted(flat.items(), key=lambda item: item[0][1:]):
        policy, horizon_text, rate_text, steps = key
        if policy != "uniform_baseline":
            continue
        candidate = flat.get(("flat_safe", horizon_text, rate_text, steps))
        if candidate is None:
            continue
        horizon = F(horizon_text)
        exp_lower, exp_upper = exponential_enclosure(2 * horizon)
        mean_squared_lower = exp_lower / (exp_lower + 3)
        mean_squared_upper = exp_upper / (exp_upper + 3)
        reduction_lower = baseline.root_lower - candidate.root_upper
        baseline_variance_upper = baseline.root_upper - mean_squared_lower
        if reduction_lower <= 0:
            raise RuntimeError("saved moment intervals do not certify separation")
        if baseline_variance_upper <= 0:
            raise RuntimeError("baseline variance upper bound is not positive")
        fractional_reduction_lower = reduction_lower / baseline_variance_upper
        derived.append({
            "horizon": horizon_text,
            "rate": rate_text,
            "steps": steps,
            "baseline_q": list(map(str, baseline.q)),
            "candidate_q": list(map(str, candidate.q)),
            "baseline_moment_lower": _fraction_record(baseline.root_lower),
            "baseline_moment_upper": _fraction_record(baseline.root_upper),
            "candidate_moment_lower": _fraction_record(candidate.root_lower),
            "candidate_moment_upper": _fraction_record(candidate.root_upper),
            "exp_2T_lower": _fraction_record(exp_lower),
            "exp_2T_upper": _fraction_record(exp_upper),
            "common_mean_squared_lower": _fraction_record(mean_squared_lower),
            "common_mean_squared_upper": _fraction_record(mean_squared_upper),
            "moment_reduction_lower": _fraction_record(reduction_lower),
            "baseline_variance_upper": _fraction_record(baseline_variance_upper),
            "fractional_variance_reduction_lower": _fraction_record(
                fractional_reduction_lower
            ),
        })

    result = {
        "schema_version": 1,
        "analysis_kind": "deterministic post-analysis; no policy selection data",
        "witness_archive": ARCHIVE.name,
        "witness_archive_sha256": _sha256(ARCHIVE),
        "source": Path(__file__).name,
        "source_sha256": _sha256(Path(__file__)),
        "saved_flat_witnesses_rechecked": checked,
        "all_saved_flat_witnesses_valid": True,
        "taylor_degree": TAYLOR_DEGREE,
        "exponential_tail_lemma": (
            "For 0<=x<=1, e^x is between S_n and "
            "S_n+(x^(n+1)/(n+1)!)/(1-x/(n+2)); the tail ratios are "
            "bounded by x/(n+2)."
        ),
        "mean_identity": "u^2=e^(2T)/(e^(2T)+3)",
        "fractional_bound": (
            "(baseline variance-candidate variance)/baseline variance >= "
            "(baseline moment lower-candidate moment upper)/"
            "(baseline moment upper-mean-squared lower)"
        ),
        "lean_scope": "No Lean proof is claimed for the exponential tail or mean-identification bridge.",
        "pairs": derived,
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    log_lines = [
        "command: /opt/miniconda3/envs/parabolab/bin/python "
        "docs/research/runs/2026-09-16-certified-tuple-policy/numerics/derive_variance_bounds.py",
        f"witness_archive_sha256: {result['witness_archive_sha256']}",
        f"source_sha256: {result['source_sha256']}",
        f"saved_flat_witnesses_rechecked: {checked}",
        f"certified_same-rate_pairs: {len(derived)}",
    ]
    for row in derived:
        log_lines.append(
            "T={horizon} lambda={rate} steps={steps} fractional_lower={bound}".format(
                horizon=row["horizon"],
                rate=row["rate"],
                steps=row["steps"],
                bound=row["fractional_variance_reduction_lower"]["exact"],
            )
        )
    LOG.write_text("\n".join(log_lines) + "\n")
    print(json.dumps({
        "saved_flat_witnesses_rechecked": checked,
        "certified_same_rate_pairs": len(derived),
        "fractional_lower_bounds": [
            {
                "horizon": row["horizon"],
                "rate": row["rate"],
                "steps": row["steps"],
                "lower": row["fractional_variance_reduction_lower"]["float"],
            }
            for row in derived
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
