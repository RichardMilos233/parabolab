"""Post-freeze dtype supplement for the T38 raw archives.

This correction is intentionally separate from the immutable audit-v1 result.
It checks count dtypes and nonnegativity without imposing an upper bound on the
zero-redraw count, and checks Boolean flags separately.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import traceback
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
RUN_DIR = HERE.parent
REPO = HERE.parents[4]
SAMPLER_DIR = RUN_DIR / "artifacts" / "two-barrier" / "sampler-v1"
OUTPUT_DIR = RUN_DIR / "artifacts" / "two-barrier" / "figure-v2"
MANIFEST_PATH = OUTPUT_DIR / "dtype_scan_manifest.json"
RESULT_PATH = OUTPUT_DIR / "dtype_scan.json"
FAILURE_PATH = OUTPUT_DIR / "dtype_scan_failure.json"

ROOT_COUNT_FIELDS = (
    "nodes",
    "leaves",
    "binary_internal",
    "ternary_internal",
    "clock_proposals",
    "clock_rejections",
    "zero_redraws",
)
CLOCK_COUNT_FIELDS = ("proposals", "rejections", "zero_redraws")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO.resolve()))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json_new(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def raw_files() -> list[Path]:
    return sorted(path.resolve() for path in SAMPLER_DIR.rglob("*.npz"))


def prepare() -> None:
    if not OUTPUT_DIR.is_dir():
        raise RuntimeError("figure-v2 execution manifest must be prepared first")
    if MANIFEST_PATH.exists() or RESULT_PATH.exists() or FAILURE_PATH.exists():
        raise FileExistsError("refusing to overwrite dtype supplement evidence")
    files = raw_files()
    if len(files) != 648:
        raise RuntimeError(f"expected 648 raw NPZ inputs, found {len(files)}")
    inputs = {relative(path): sha256(path) for path in files}
    manifest = {
        "schema_version": 1,
        "status": "prepared-before-dtype-scan",
        "created_utc": utc_now(),
        "source": relative(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
        "raw_input_count": len(inputs),
        "raw_input_hashes_sha256": inputs,
        "scope": {
            "separate_from_frozen_audit_v1": True,
            "changes_audit_v1_check_count": False,
            "zero_redraws_is_an_unbounded_nonnegative_integer_count": True,
            "coefficient_limit_substitution_is_a_boolean_flag": True,
        },
    }
    write_json_new(MANIFEST_PATH, manifest)
    print(json.dumps({"status": "prepared", "raw_input_count": len(inputs)}))


def run() -> int:
    if not MANIFEST_PATH.is_file():
        raise RuntimeError("dtype scan manifest is missing")
    if RESULT_PATH.exists() or FAILURE_PATH.exists():
        raise FileExistsError("refusing to overwrite dtype supplement evidence")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    files = raw_files()
    current = {relative(path): sha256(path) for path in files}
    if current != manifest["raw_input_hashes_sha256"]:
        raise RuntimeError("raw inputs changed after dtype-scan manifest freeze")

    root_archives = 0
    clock_archives = 0
    root_observations = 0
    clock_observations = 0
    count_arrays_checked = 0
    boolean_arrays_checked = 0
    failures: list[dict[str, Any]] = []
    observed_dtypes: dict[str, set[str]] = {}
    zero_redraw_maximum = 0
    coefficient_true_count = 0

    try:
        for path in files:
            with np.load(path, allow_pickle=False) as archive:
                names = set(archive.files)
                if "scaled_output" in names:
                    root_archives += 1
                    size = int(archive["scaled_output"].size)
                    root_observations += size
                    for field in ROOT_COUNT_FIELDS:
                        array = archive[field]
                        count_arrays_checked += 1
                        observed_dtypes.setdefault(field, set()).add(str(array.dtype))
                        passed = np.issubdtype(array.dtype, np.integer) and bool(np.all(array >= 0))
                        if not passed:
                            failures.append({
                                "path": relative(path),
                                "field": field,
                                "dtype": str(array.dtype),
                                "minimum": int(np.min(array)),
                            })
                        if field == "zero_redraws":
                            zero_redraw_maximum = max(zero_redraw_maximum, int(np.max(array)))
                    flag = archive["coefficient_limit_substitution"]
                    boolean_arrays_checked += 1
                    observed_dtypes.setdefault("coefficient_limit_substitution", set()).add(str(flag.dtype))
                    if not np.issubdtype(flag.dtype, np.bool_):
                        failures.append({
                            "path": relative(path),
                            "field": "coefficient_limit_substitution",
                            "dtype": str(flag.dtype),
                        })
                    coefficient_true_count += int(np.sum(flag))
                elif "accepted_time" in names:
                    clock_archives += 1
                    size = int(archive["accepted_time"].size)
                    clock_observations += size
                    for field in CLOCK_COUNT_FIELDS:
                        array = archive[field]
                        count_arrays_checked += 1
                        observed_dtypes.setdefault(f"clock.{field}", set()).add(str(array.dtype))
                        passed = np.issubdtype(array.dtype, np.integer) and bool(np.all(array >= 0))
                        if not passed:
                            failures.append({
                                "path": relative(path),
                                "field": field,
                                "dtype": str(array.dtype),
                                "minimum": int(np.min(array)),
                            })
                        if field == "zero_redraws":
                            zero_redraw_maximum = max(zero_redraw_maximum, int(np.max(array)))
                    leaf = archive["is_leaf"]
                    boolean_arrays_checked += 1
                    observed_dtypes.setdefault("clock.is_leaf", set()).add(str(leaf.dtype))
                    if not np.issubdtype(leaf.dtype, np.bool_):
                        failures.append({
                            "path": relative(path),
                            "field": "is_leaf",
                            "dtype": str(leaf.dtype),
                        })
                else:
                    failures.append({"path": relative(path), "field": "archive_kind", "dtype": None})

        result = {
            "schema_version": 1,
            "status": "PASS" if not failures else "FAIL",
            "created_utc": utc_now(),
            "manifest_sha256": sha256(MANIFEST_PATH),
            "source_sha256": manifest["source_sha256"],
            "raw_input_count": len(files),
            "root_archives": root_archives,
            "clock_archives": clock_archives,
            "root_observations": root_observations,
            "clock_observations": clock_observations,
            "count_arrays_checked": count_arrays_checked,
            "boolean_arrays_checked": boolean_arrays_checked,
            "observed_dtypes": {key: sorted(value) for key, value in observed_dtypes.items()},
            "zero_redraw_maximum": zero_redraw_maximum,
            "coefficient_limit_substitution_true_count": coefficient_true_count,
            "failure_count": len(failures),
            "failures": failures,
            "interpretation": {
                "zero_redraws_upper_bound_imposed": False,
                "all_count_fields_require_integer_dtype_and_nonnegative_values": True,
                "boolean_flags_checked_separately": True,
                "part_of_original_992_checks": False,
                "mutates_raw_evidence": False,
            },
        }
        write_json_new(RESULT_PATH, result)
        print(json.dumps({
            "status": result["status"],
            "raw_inputs": len(files),
            "count_arrays": count_arrays_checked,
            "boolean_arrays": boolean_arrays_checked,
        }))
        return 0 if not failures else 3
    except Exception as exc:
        write_json_new(FAILURE_PATH, {
            "schema_version": 1,
            "status": "ERROR",
            "created_utc": utc_now(),
            "exception_type": type(exc).__name__,
            "exception": str(exc),
            "traceback": traceback.format_exc(),
        })
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "run"))
    args = parser.parse_args()
    if args.action == "prepare":
        prepare()
        return 0
    return run()


if __name__ == "__main__":
    raise SystemExit(main())
