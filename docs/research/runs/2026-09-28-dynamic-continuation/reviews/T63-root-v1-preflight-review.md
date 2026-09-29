# T63 v1 root source review: official execution held

Status: root read all1127 source lines and the complete producer report.
The opaque sampling algorithm, prescribed sample/stream counts, stored-width
reference construction, per-point charging and successful preflight design
match02g. No official run has been authorized. The producer's PASS is a
bounded diagnostic result, not root clearance.

Frozen v1 source SHA256:
`cbfda29abd7e4d62e4131502cea5d96fbfaba05c6d0eaf74a9af329f78b458b0`.
Manifest SHA256:
`f89cb731baa193c140cc42b73a0db7449b49f24795d76339e9c1165846a96428`.
Preflight-result SHA256:
`7e7327de5cd107366035774f7f109e19c6a0c5d9263cbe031aa503a1ab60aae5`.

Two source-correspondence defects require a preserved v2 before execution:

1. `pure_estimator_elapsed_seconds` wraps the sampling call, which invokes
   a charge ledger with JSON serialization, timestamps and fsync for each
   vector. The field therefore includes accounting I/O and is not pure
   estimator time. Store raw inclusive time and separately measured
   accounting time; clearly label any subtracted estimate and distinguish
   journal/array/setup serialization. Do not assert a speed comparison.
2. A preflight sampling exception reaches an outer handler which does not
   retain the current diagnostic identity, partial batch data, attempted/
   returned observations and before/after RNG states. The first wrapped
   replay is not persisted until the second completes. In official code,
   post-estimator count assertions occur before appending the result and
   outside the inner failure-record handler. Those paths can lose the
   very context the frozen failure protocol requires.

These are identified code-path defects, not reported runtime failures.
The v1 diagnostic observations are retained as produced; no failed test,
scientific counterexample or sampling bias is inferred. T63 must archive
the exact source before changing it, keep v1 results/manifest/report, and
create a new v2 manifest before repeating the unchanged bounded preflight.
Prior v1 calls655633 remain charged. With one v2 preflight, the intended
official run and the fixed subset replay, the whole-activity plan becomes
368270390 calls under the500-million cap. No complete replay is authorized.

Root's next gate is reading the versioned diff and actual v2 preflight
evidence, including source/manifest hashes and cross-version accounting.
No user permission is required for these already authorized reversible
research corrections. No official-run clearance record exists here.
