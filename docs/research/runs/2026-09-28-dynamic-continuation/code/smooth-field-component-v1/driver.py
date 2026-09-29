#!/opt/miniconda3/envs/parabolab/bin/python
"""Command-line entry point for the frozen E5 implementation.

T99 executes only ``manifest`` and ``preflight``.  ``official`` and ``replay``
are prepared for later root-controlled use and are guarded by a byte-linked
root acceptance record.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from budget import BudgetLedger
from experiment import (
    ARTIFACT_ROOT,
    PREFLIGHT_ROOT,
    run_official,
    run_preflight,
    run_replay,
    write_manifest_and_references,
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    subcommands = result.add_subparsers(dest="command", required=True)
    subcommands.add_parser("manifest", help="write frozen source/environment/reference manifests")
    subcommands.add_parser("preflight", help="run fixtures and bounded tag-1 preflight only")

    official = subcommands.add_parser("official", help="run accepted tag-0 official suite")
    official.add_argument("--acceptance", type=Path, required=True)
    official.add_argument(
        "--output-root",
        type=Path,
        default=ARTIFACT_ROOT / "official-v1",
    )

    replay = subcommands.add_parser("replay", help="replay fixed tag-0 indices 0..7")
    replay.add_argument("--acceptance", type=Path, required=True)
    replay.add_argument("--official-directory", type=Path, required=True)
    replay.add_argument(
        "--output-root",
        type=Path,
        default=ARTIFACT_ROOT / "replay-v1",
    )

    subcommands.add_parser("budget", help="print the persistent E5 budget state")
    return result


def main(argv: list[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.command == "manifest":
        manifest, references = write_manifest_and_references()
        payload = {
            "status": "written",
            "implementation_manifest": str(manifest),
            "analytic_references": str(references),
            "official_executed": False,
        }
    elif arguments.command == "preflight":
        payload = run_preflight()
    elif arguments.command == "official":
        payload = run_official(arguments.acceptance, arguments.output_root)
    elif arguments.command == "replay":
        payload = run_replay(
            arguments.acceptance,
            arguments.official_directory,
            arguments.output_root,
        )
    elif arguments.command == "budget":
        payload = BudgetLedger(ARTIFACT_ROOT).snapshot()
    else:  # argparse makes this unreachable
        raise AssertionError(arguments.command)
    print(json.dumps(payload, sort_keys=True, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
