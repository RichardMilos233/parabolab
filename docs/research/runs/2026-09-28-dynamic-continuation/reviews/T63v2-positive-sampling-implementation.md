# T63v2: corrected positive-query evidence and bounded preflight

Date: 2026-09-28. Scope: the two evidence corrections requested by root after
reading the complete v1 source and report, followed by one versioned prepare
and one identical bounded preflight. The v1 scientific observations remain a
frozen PASS; this report does not revise them or clear the official run.

**Result: PASS for renewed root source/preflight review.** Before editing the
working implementation, the exact v1 source was copied to
`artifacts/positive-query-sampling/v1/source/positive_query_sampling.py`.
Its SHA256 is
`cbfda29abd7e4d62e4131502cea5d96fbfaba05c6d0eaf74a9af329f78b458b0`,
identical to the v1 manifest-bound source. The v1 manifest, result, journals,
logs and T63 report retain their original hashes. The corrected source uses a
new v2 artifact directory.

The single v2 preflight made exactly655633 calls and passed. Across v1 and v2,
the actual spent activity is1311266 calls. The official336883488-call
experiment, plots and30075636-call subset replay were not run.

## Commands actually executed

The source archive was created and byte-compared before editing. The only two
v2 producer commands were:

```text
/opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-28-dynamic-continuation/numerics/positive_query_sampling.py prepare
/opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-28-dynamic-continuation/numerics/positive_query_sampling.py preflight
```

`prepare` reported zero v2 diagnostic calls and froze the v2 source and
manifest. `preflight` ran once, from2026-09-28T16:16:22.752704Z through
16:16:22.835185Z. Read-only post-run checks summed both ledgers, compared all
scientific fields and RNG states between v1 and v2, parsed the final source,
checked manifest/result hash binding and rechecked all342 protected hashes.
No official `run` command was issued.

## Exact source corrections

The opaque sampler itself, schedules, stored widths, references, streams,
batching, tolerances and query accounting did not change.

1. The durable JSONL writer now measures serialization wall time. The activity
   ledger separately records its complete `charge` overhead and its JSONL
   serialization subset. Each estimator record stores the raw wall duration
   around `sample_estimator`, measured ledger-accounting time during that call,
   and `max(0,raw-accounting)`. The last value is explicitly labeled a measured
   accounting-excluded duration, not an exact pure-compute certificate. The
   source no longer uses the `pure_estimator_elapsed_seconds` label.
2. Preflight and official summaries separately aggregate setup, ledger
   accounting, ledger JSONL serialization, diagnostic/replicate journal JSONL
   serialization, run-log serialization, and cell array/metadata serialization
   where applicable. Raw wall durations are labeled as overlapping these
   counters rather than incorrectly presented as additive partitions.
3. A mutable failure context is populated before each preflight diagnostic. On
   sampler failure it retains diagnostic identity, RNG before/after, attempted,
   returned and positive counts, completed batch sums/counts from
   `SamplingFailure.partial`, measured timing and traceback. Point, scalar,
   reference and design checks likewise preserve their current identity and all
   observations available before an exception.
4. Each completed wrapped-bump execution is now appended and fsynced as its own
   journal record before the next execution starts. The pair comparison remains
   a separate record after both individual records exist.
5. Official replicate estimation and its post-estimator count assertions now
   share one exception boundary. Therefore a failed attempted/returned,
   observation or positive-count assertion writes the successful estimate,
   full before/after RNG states, all oracle counts, replicate identity, timing
   and traceback before aborting. Successful records are appended only after
   those checks pass.
6. Prior-version activity is discovered from every earlier
   `*activity.jsonl`, with cumulative values and hashes checked. The v2 manifest
   charges v1's655633 calls rather than resetting the prior total to zero.

No failure branch was triggered in this successful preflight; its completeness
is source evidence for root review. No additional empirical failure injection
or replay was performed.

## Budget and frozen inputs

The v2 manifest records v1's220-entry ledger, hash
`876b23f230fff605c91d74b57b6cdcc8eda4521942a23f36e31844e63b0cdba0`,
and prior charge655633. Its whole-activity calculation is

```text
655633 prior v1 calls
+ 655633 v2 preflight calls
+ 336883488 planned official calls
+ 30075636 planned subset replay calls
= 368270390 planned cross-version calls.
```

This leaves131729610 calls below the500-million cap. After the v2 preflight,
actual cross-version spent calls are1311266; the official and subset replay
remain merely planned.

In addition to the original theory, formal, E3 and correspondence inputs, the
v2 manifest freezes the archived v1 source, v1 manifest, ledger, journal,
result, log and original T63 report. The342 protected files still have zero
missing paths and zero mismatches. No toolchain, Lake file, formal source,
02g, T58, T51/T52 or other existing research file was changed.

## v2 preflight and parity

The v2 activity ledger again has220 entries and final cumulative charge655633.
The journal has237 rows: nine constants, two individually flushed wrapped
runs, one pair comparison,204 bump points, eight scalar-Psi checks, twelve
stored-width cross-checks and one official-design recalculation.

All fixed checks passed:

| Frozen block | Calls | Result |
| --- | ---: | --- |
| Nine opaque constant tests | 393279 | 9/9 pass |
| Two actual wrapped-bump executions | 262150 | both flushed; bitwise pair pass |
| Twelve cases at17 fixed points | 204 | 204/204 pass |
| Scalar Psi checks | 0 | 8/8 pass |
| Stored-width reference cross-checks | 0 | 12/12 pass |
| Design/schema recalculation | 0 | 180 cells,18720 outputs,336883488 calls pass |

A field-by-field parity script compared v1 and v2 while excluding only the new
timing fields and individual wrapped-record packaging. Constant records,
wrapped means/outputs/counts and complete RNG states, all204 point values and
references,31 underflow flags, scalar checks, stored-width checks and the
official-design calculation are identical. Thus the corrections changed
evidence handling, not observations or scientific claims.

## Timing evidence

The eleven sampler invocations in preflight—nine constants and two wrapped
runs—record:

| Measurement | Seconds |
| --- | ---: |
| Raw inclusive estimator-call wall time | 0.011408873833715916 |
| Measured ledger accounting during those calls | 0.0008744592778384686 |
| Measured estimator-call time excluding that accounting | 0.010534414555877447 |

The arithmetic identity `raw - accounting = excluded` held exactly in the
stored binary64 sums. This is only a measured subtraction of ledger accounting;
it is not claimed to isolate every instrumentation or operating-system cost.

The complete preflight summary separately reports setup before diagnostics
0.536794625222683s, raw diagnostic wall time0.08046970888972282s, complete
ledger accounting0.008117381948977709s, the ledger JSONL serialization subset
0.0075147864408791065s, diagnostic-journal serialization
0.01172829233109951s and run-log serialization before result write
0.0009087920188903809s. These counters overlap the raw wall measurements, as
the result states explicitly.

## Evidence hashes

| Artifact | SHA256 |
| --- | --- |
| `numerics/positive_query_sampling.py` | `81eb2b122d325eca97d144adc00380114558c5ad35a830d9d4062fa95f63df08` |
| `artifacts/positive-query-sampling/v1/source/positive_query_sampling.py` | `cbfda29abd7e4d62e4131502cea5d96fbfaba05c6d0eaf74a9af329f78b458b0` |
| `artifacts/positive-query-sampling/v2/execution_manifest.json` | `9417c6dc18b3c761ee7cdf38c4cc8ececbfc048c0869b0fea5b96acaaae47bd5` |
| `artifacts/positive-query-sampling/v2/preflight_activity.jsonl` | `b4a6be135dd3bfa73a9e66164b301bc025d0c38c6da44eb11b51d94dc20a38b1` |
| `artifacts/positive-query-sampling/v2/preflight_journal.jsonl` | `1d8d2df39aabe6a02fbf94732fd25d41be22fcd1b4cca8aaba97a6f3074a1e4d` |
| `artifacts/positive-query-sampling/v2/preflight_result.json` | `ae85c9f1712ada9697bedc472ea273bf692b2cc7c4f0813f58a63ce085380c1c` |
| `artifacts/positive-query-sampling/v2/preflight.log` | `856659e752e3a66f1bfd25cf536dd36f915ad1996967dca315d14bdbc75b9981` |
| `reviews/T63-positive-sampling-implementation.md` | `15d6aec062f2df3952a5443577be01535d320bf03968dc6ee03b1289578a1498` |

The v2 source hash agrees in the manifest and result; the result binds the
displayed manifest hash. There is no v2 `preflight_failure.json`, no v3 and no
official directory.

## Scope and next gate

This remains a binary64/PCG64 numerical realization with an uncertified scalar
reference. No actual PDE solution, exact-real/iid machine bridge, novelty,
minimax, publication-priority or prize claim is made. Root must read the v1 to
v2 source diff and complete v2 evidence before any official clearance. Only a
new root record binding the v2 source, manifest and successful preflight-result
hashes can unlock the official phase.
