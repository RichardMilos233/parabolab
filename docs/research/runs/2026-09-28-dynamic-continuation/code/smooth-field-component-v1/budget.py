"""Persistent E5 acquisition and work accounting.

The JSONL journal is canonical.  Each mutation is appended and fsynced before
the compact state is atomically replaced.  On restart, journal records newer
than the compact state are replayed.  Segment generation uses persistent block
reservations: a hard crash can waste reserved capacity, but cannot erase work
or allow a later process to overrun the global cap.
"""

from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Iterator
import uuid


POLICY_VERSION = "e5-budget-v1"
ORACLE_CAPS = {"preflight": 8192, "official": 245760, "replay": 864}
GLOBAL_ORACLE_CAP = 300000
GLOBAL_SEGMENT_CAP = 10_000_000
SINGLE_TREE_SEGMENT_CAP = 100_000
SEGMENT_RESERVATION_BLOCK = 1024


class BudgetError(RuntimeError):
    """Base class for persistent budget failures."""


class BudgetLimitError(BudgetError):
    """Raised before work that would exceed a frozen hard cap."""


class UnresolvedReservationError(BudgetError):
    """A prior process stopped with a live segment reservation."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def initial_state() -> dict[str, Any]:
    return {
        "version": POLICY_VERSION,
        "sequence": 0,
        "oracle_calls": {"preflight": 0, "official": 0, "replay": 0, "total": 0},
        "segments_generated": 0,
        "segments_reserved": 0,
        "active_segment_reservations": {},
        "exponential_draws": 0,
        "gaussian_draws": 0,
        "uniform_draws": 0,
        "tuple_draw_calls": 0,
        "tuple_indices_drawn": 0,
        "known_evaluator_calls": 0,
        "completed_samples": {"preflight": 0, "official": 0, "replay": 0},
        "failed_samples": {"preflight": 0, "official": 0, "replay": 0},
        "updated_utc": None,
    }


@dataclass(frozen=True)
class SegmentReservation:
    reservation_id: str
    phase: str
    identifier: dict[str, Any]


class BudgetLedger:
    """Single-writer persistent ledger guarded by an advisory file lock."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.policy_path = self.root / "budget_policy.json"
        self.journal_path = self.root / "budget_journal.jsonl"
        self.state_path = self.root / "budget_state.json"
        self.manifest_path = self.root / "budget_manifest.json"
        self.lock_path = self.root / "budget.lock"
        self._initialize_if_needed()
        self._recover_state()

    @contextmanager
    def _locked(self) -> Iterator[None]:
        with self.lock_path.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _atomic_json(self, path: Path, value: Any) -> None:
        data = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
        fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, path)
            directory_fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)

    def _append_event(self, event: dict[str, Any]) -> None:
        line = (canonical_json(event) + "\n").encode()
        with self.journal_path.open("ab", buffering=0) as handle:
            handle.write(line)
            os.fsync(handle.fileno())

    def _policy(self) -> dict[str, Any]:
        return {
            "version": POLICY_VERSION,
            "prior_e5_oracle_calls": 0,
            "oracle_caps": ORACLE_CAPS,
            "global_oracle_cap": GLOBAL_ORACLE_CAP,
            "global_generated_segment_cap": GLOBAL_SEGMENT_CAP,
            "single_tree_segment_cap": SINGLE_TREE_SEGMENT_CAP,
            "segment_reservation_block": SEGMENT_RESERVATION_BLOCK,
            "reservation_semantics": (
                "capacity is reserved and fsynced before segment generation; normal completion "
                "commits the exact generated count and releases unused capacity; an unresolved "
                "crash reservation remains charged until independent audit"
            ),
        }

    def _initialize_if_needed(self) -> None:
        with self._locked():
            if not self.policy_path.exists():
                self._atomic_json(self.policy_path, self._policy())
            else:
                policy = json.loads(self.policy_path.read_text())
                if policy != self._policy():
                    raise BudgetError("existing budget policy differs from frozen E5 policy")
            if not self.state_path.exists() and not self.journal_path.exists():
                state = initial_state()
                event = {
                    "sequence": 0,
                    "utc": utc_now(),
                    "kind": "initialize",
                    "prior_e5_oracle_calls": 0,
                    "state_after": state,
                }
                self._append_event(event)
                self._atomic_json(self.state_path, state)
            elif not self.state_path.exists() or not self.journal_path.exists():
                raise BudgetError("budget state and journal must either both exist or both be absent")

    def _apply_event(self, state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
        if event["kind"] == "initialize":
            return deepcopy(event["state_after"])
        after = event.get("state_after")
        if after is None:
            raise BudgetError(f"journal event {event.get('sequence')} has no state_after")
        return deepcopy(after)

    def _recover_state_locked(self) -> dict[str, Any]:
        state = json.loads(self.state_path.read_text())
        state_sequence = int(state["sequence"])
        recovered = state
        last_sequence = -1
        with self.journal_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.endswith("\n"):
                    raise BudgetError(f"partial journal line {line_number}")
                event = json.loads(line)
                sequence = int(event["sequence"])
                if sequence != last_sequence + 1:
                    raise BudgetError(f"nonconsecutive journal sequence at line {line_number}")
                last_sequence = sequence
                if sequence > state_sequence:
                    recovered = self._apply_event(recovered, event)
        if last_sequence < state_sequence:
            raise BudgetError("compact state is ahead of canonical journal")
        if recovered != state:
            self._atomic_json(self.state_path, recovered)
        return recovered

    def _recover_state(self) -> None:
        with self._locked():
            state = self._recover_state_locked()
            self._write_manifest_locked(state)

    def _read_state_locked(self) -> dict[str, Any]:
        """Read the compact state after constructor-time journal recovery.

        Every process recovers while holding the same lock at construction.
        Healthy mutations append and fsync the journal before atomically
        replacing this file, so rescanning the growing journal per call is
        unnecessary and would make official acquisition quadratic.
        """
        return json.loads(self.state_path.read_text())

    def _write_manifest_locked(self, state: dict[str, Any]) -> None:
        manifest = {
            "version": POLICY_VERSION,
            "updated_utc": utc_now(),
            "policy_path": str(self.policy_path),
            "policy_sha256": sha256_path(self.policy_path),
            "journal_path": str(self.journal_path),
            "journal_sha256": sha256_path(self.journal_path),
            "state_path": str(self.state_path),
            "state_sha256": sha256_path(self.state_path),
            "state_snapshot": state,
        }
        self._atomic_json(self.manifest_path, manifest)

    def snapshot(self) -> dict[str, Any]:
        with self._locked():
            state = self._read_state_locked()
            return deepcopy(state)

    def assert_no_unresolved_reservations(self) -> None:
        state = self.snapshot()
        active = state["active_segment_reservations"]
        if active:
            raise UnresolvedReservationError(
                "unresolved crash reservation(s) prevent further generation: "
                + ",".join(sorted(active))
            )

    def _mutate(self, kind: str, detail: dict[str, Any], transform) -> dict[str, Any]:
        with self._locked():
            state = self._read_state_locked()
            new_state = deepcopy(state)
            transform(new_state)
            new_state["sequence"] = int(state["sequence"]) + 1
            new_state["updated_utc"] = utc_now()
            event = {
                "sequence": new_state["sequence"],
                "utc": new_state["updated_utc"],
                "kind": kind,
                "detail": detail,
                "state_after": new_state,
            }
            self._append_event(event)
            self._atomic_json(self.state_path, new_state)
            return deepcopy(new_state)

    def charge_oracle(self, phase: str, identifier: dict[str, Any], x_hex: str) -> dict[str, Any]:
        if phase not in ORACLE_CAPS:
            raise BudgetError(f"unknown oracle phase {phase!r}")

        def transform(state: dict[str, Any]) -> None:
            phase_calls = int(state["oracle_calls"][phase])
            total_calls = int(state["oracle_calls"]["total"])
            if phase_calls + 1 > ORACLE_CAPS[phase]:
                raise BudgetLimitError(f"{phase} oracle cap {ORACLE_CAPS[phase]} reached")
            if total_calls + 1 > GLOBAL_ORACLE_CAP:
                raise BudgetLimitError(f"global oracle cap {GLOBAL_ORACLE_CAP} reached")
            state["oracle_calls"][phase] = phase_calls + 1
            state["oracle_calls"]["total"] = total_calls + 1

        return self._mutate(
            "oracle_charge_before_evaluation",
            {"phase": phase, "identifier": identifier, "x_hex": x_hex},
            transform,
        )

    def begin_segment_reservation(self, phase: str, identifier: dict[str, Any]) -> SegmentReservation:
        reservation_id = str(uuid.uuid4())

        def transform(state: dict[str, Any]) -> None:
            if state["active_segment_reservations"]:
                raise UnresolvedReservationError("another segment reservation is already active")
            remaining = GLOBAL_SEGMENT_CAP - int(state["segments_generated"])
            amount = min(SEGMENT_RESERVATION_BLOCK, remaining)
            if amount <= 0:
                raise BudgetLimitError(f"global segment cap {GLOBAL_SEGMENT_CAP} reached")
            state["active_segment_reservations"][reservation_id] = {
                "phase": phase,
                "identifier": identifier,
                "reserved": amount,
                "created_utc": utc_now(),
            }
            state["segments_reserved"] = int(state["segments_reserved"]) + amount

        self._mutate(
            "segment_reservation_begin",
            {"reservation_id": reservation_id, "phase": phase, "identifier": identifier},
            transform,
        )
        return SegmentReservation(reservation_id, phase, deepcopy(identifier))

    def extend_segment_reservation(self, reservation: SegmentReservation) -> int:
        amount_holder: list[int] = []

        def transform(state: dict[str, Any]) -> None:
            active = state["active_segment_reservations"].get(reservation.reservation_id)
            if active is None:
                raise BudgetError("cannot extend missing segment reservation")
            already = int(active["reserved"])
            if already >= SINGLE_TREE_SEGMENT_CAP:
                raise BudgetLimitError(f"single-tree segment cap {SINGLE_TREE_SEGMENT_CAP} reached")
            remaining_global = GLOBAL_SEGMENT_CAP - int(state["segments_generated"]) - int(
                state["segments_reserved"]
            )
            amount = min(
                SEGMENT_RESERVATION_BLOCK,
                SINGLE_TREE_SEGMENT_CAP - already,
                remaining_global,
            )
            if amount <= 0:
                raise BudgetLimitError("no segment capacity remains for reservation extension")
            active["reserved"] = already + amount
            state["segments_reserved"] = int(state["segments_reserved"]) + amount
            amount_holder.append(amount)

        self._mutate(
            "segment_reservation_extend",
            {"reservation_id": reservation.reservation_id},
            transform,
        )
        return amount_holder[0]

    def commit_segment_reservation(
        self,
        reservation: SegmentReservation,
        actual_generated: int,
        *,
        status: str,
        exponential_draws: int = 0,
    ) -> dict[str, Any]:
        if actual_generated < 0:
            raise BudgetError("negative generated segment count")

        def transform(state: dict[str, Any]) -> None:
            active = state["active_segment_reservations"].pop(reservation.reservation_id, None)
            if active is None:
                raise BudgetError("cannot commit missing segment reservation")
            reserved = int(active["reserved"])
            if actual_generated > reserved:
                raise BudgetError("actual generated segments exceed persistent reservation")
            state["segments_reserved"] = int(state["segments_reserved"]) - reserved
            state["segments_generated"] = int(state["segments_generated"]) + actual_generated
            state["exponential_draws"] = int(state["exponential_draws"]) + exponential_draws
            if int(state["segments_generated"]) > GLOBAL_SEGMENT_CAP:
                raise BudgetError("segment commit would violate the global cap")

        return self._mutate(
            "segment_reservation_commit",
            {
                "reservation_id": reservation.reservation_id,
                "actual_generated": actual_generated,
                "exponential_draws": exponential_draws,
                "status": status,
            },
            transform,
        )

    def charge_work(self, kind: str, amount: int, identifier: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            "exponential_draws",
            "gaussian_draws",
            "uniform_draws",
            "tuple_draw_calls",
            "tuple_indices_drawn",
            "known_evaluator_calls",
        }
        if kind not in allowed:
            raise BudgetError(f"unknown work counter {kind!r}")
        if amount < 0:
            raise BudgetError("negative work charge")

        def transform(state: dict[str, Any]) -> None:
            state[kind] = int(state[kind]) + amount

        return self._mutate(
            "work_charge_before_or_after_as_documented",
            {"counter": kind, "amount": amount, "identifier": identifier},
            transform,
        )

    def charge_work_batch(self, deltas: dict[str, int], identifier: dict[str, Any]) -> dict[str, Any]:
        allowed = {
            "exponential_draws",
            "gaussian_draws",
            "uniform_draws",
            "tuple_draw_calls",
            "tuple_indices_drawn",
            "known_evaluator_calls",
        }
        if not deltas or not set(deltas) <= allowed:
            raise BudgetError("invalid work-counter batch")
        if any(int(amount) < 0 for amount in deltas.values()):
            raise BudgetError("negative work charge")

        def transform(state: dict[str, Any]) -> None:
            for counter, amount in deltas.items():
                state[counter] = int(state[counter]) + int(amount)

        return self._mutate(
            "work_batch_charge",
            {"deltas": {key: int(value) for key, value in deltas.items()}, "identifier": identifier},
            transform,
        )

    def record_sample_status(self, phase: str, identifier: dict[str, Any], success: bool) -> dict[str, Any]:
        if phase not in ORACLE_CAPS:
            raise BudgetError(f"unknown sample phase {phase!r}")
        field = "completed_samples" if success else "failed_samples"

        def transform(state: dict[str, Any]) -> None:
            state[field][phase] = int(state[field][phase]) + 1

        return self._mutate(
            "sample_complete" if success else "sample_failure",
            {"phase": phase, "identifier": identifier},
            transform,
        )

    def refresh_manifest(self) -> dict[str, Any]:
        with self._locked():
            state = self._read_state_locked()
            self._write_manifest_locked(state)
            return json.loads(self.manifest_path.read_text())
