"""Reproduce and verify the exact nonzero-continuation wave tuple gate.

Run with Python's standard library only:
    python docs/research/runs/2026-09-16-certified-tuple-policy/wave_gate_check.py
    python docs/research/runs/2026-09-16-certified-tuple-policy/wave_gate_check.py --verify

The finite checks validate uniform moment-box witnesses and rational gate
inequalities. The stochastic comparison proof is in 09-independent-review.md.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys


RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[3]
SOURCE = PROJECT / "parabolab" / "rate_certificate.py"
OUTPUT = RUN / "wave-gate-checks.json"
RATES = (F(3, 4), F(1))
HORIZON = F(1, 20)

# Avoid importing parabolab.__init__: this finite verifier needs no NumPy.
SPEC = importlib.util.spec_from_file_location("wave_gate_uniform_certificate", SOURCE)
CERT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CERT
SPEC.loader.exec_module(CERT)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    return value


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def restore(payload):
    value = dict(payload)
    for key in ("horizon", "tilt"):
        value[key] = F(value[key])
    value["phi"] = None if value["phi"] is None else F(value["phi"])
    value["rates"] = tuple(map(F, value["rates"]))
    for key in ("lower", "upper"):
        value[key] = None if value[key] is None else tuple(map(F, value[key]))
    steps = []
    for item in value["witnesses"]:
        step = {"duration": F(item["duration"])}
        for key in ("upper_start", "upper_end", "lower_start", "lower_end"):
            step[key] = None if item[key] is None else tuple(map(F, item[key]))
        steps.append(CERT.BoxStep(**step))
    value["witnesses"] = tuple(steps)
    return CERT.MomentEnclosure(**value)


def gate_values(certificate, rate):
    if not CERT.verify_moment_enclosure(certificate):
        raise ValueError("invalid uniform all-code moment witness")
    if (certificate.family != "wave" or certificate.horizon != HORIZON
            or certificate.rates != (rate, rate) or certificate.tilt != 1):
        raise ValueError("witness does not certify the required wave/rate/horizon")
    bound = certificate.upper[3]
    alpha = rate + bound / rate
    ratio = 4 * (1 - alpha * HORIZON)
    probability = F(2, 3)
    # A >= ratio*B, so p(A+B) <= A follows from p(ratio+1) <= ratio.
    margin = ratio - probability * (ratio + 1)
    if not (0 < probability < 1 and ratio > 2 and margin > 0):
        raise ValueError("nonzero-continuation update did not pass the strict gate")
    return {
        "F1_moment_upper": str(bound),
        "alpha": str(alpha),
        "ratio_lower": str(ratio),
        "first_label_probability": str(probability),
        "gate_margin": str(margin),
        "local_improvement_per_B_lower": str(ratio / 2 - 1),
        "uniform_box_verified": True,
        "strict_gate_verified": True,
    }


def verify(record):
    if record["source_sha256"] != hashlib.sha256(SOURCE.read_bytes()).hexdigest():
        raise ValueError("certificate source has changed since the record was generated")
    if record["script_sha256"] != hashlib.sha256(Path(__file__).read_bytes()).hexdigest():
        raise ValueError("gate-check script has changed since record generation")
    if record["horizon"] != str(HORIZON) or len(record["cases"]) != len(RATES):
        raise ValueError("unexpected horizon or case count")
    for rate, case in zip(RATES, record["cases"]):
        if case["rate"] != str(rate):
            raise ValueError("unexpected rate")
        payload = case["baseline_witness"]
        if case["baseline_witness_sha256"] != digest(payload):
            raise ValueError("uniform witness hash mismatch")
        expected = gate_values(restore(payload), rate)
        if case["gate"] != expected:
            raise ValueError("recorded gate disagrees with exact recomputation")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="only verify saved witnesses")
    args = parser.parse_args()
    if args.verify:
        record = json.loads(OUTPUT.read_text())
    else:
        record = {
            "scope": "Raw uniform Allen-Cahn wave; all six codes; all spatial states",
            "horizon": str(HORIZON),
            "source": str(SOURCE.relative_to(PROJECT)),
            "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "witness_hash_encoding": "SHA-256 of sorted compact UTF-8 JSON",
            "proof": "09-independent-review.md, stronger wave control",
            "coverage": "Exact finite witness checks; analytic/stochastic proof is conventional",
            "cases": [],
        }
        for rate in RATES:
            certificate = CERT.enclose_allen_cahn_moment(
                family="wave", horizon=HORIZON, rates=(rate, rate), steps=100,
                precision_bits=48, tilt=1,
            )
            payload = encode(asdict(certificate))
            record["cases"].append({
                "rate": str(rate),
                "baseline_witness_sha256": digest(payload),
                "baseline_witness": payload,
                "gate": gate_values(certificate, rate),
            })
    verify(record)
    if not args.verify:
        OUTPUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    for case in record["cases"]:
        print(f"rate={case['rate']}: witness verified, "
              f"R={case['gate']['ratio_lower']} > 2, p1=2/3 strictly accepted")
    print(f"{'Verified' if args.verify else 'Wrote and verified'} {OUTPUT}")


if __name__ == "__main__":
    main()
