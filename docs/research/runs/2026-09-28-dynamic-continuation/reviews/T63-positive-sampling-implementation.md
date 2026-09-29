# T63: positive-query sampling implementation and bounded preflight

Date: 2026-09-28. Scope: implementation, manifest preparation and the single
bounded preflight authorized by frozen protocol02g. This report is producer
evidence, not an independent audit or root clearance for the official run.

**Result: PASS for source/manifest handoff and bounded preflight.** The v1
manifest was created before any diagnostic oracle observation. The first and
only v1 preflight attempt then made exactly655633 charged point calls and
passed every frozen check. There was no failed attempt, source correction,
official experiment, plot, or independent replay. In particular, the
336883488-call official experiment remains blocked on the protocol's explicit
root source/preflight clearance.

## Commands actually executed

Both producer phases used the required interpreter from the repository root:

```text
/opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-28-dynamic-continuation/numerics/positive_query_sampling.py prepare
/opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-28-dynamic-continuation/numerics/positive_query_sampling.py preflight
```

`prepare` completed at2026-09-28T16:05:37Z and reported zero diagnostic oracle
calls. `preflight` ran once from2026-09-28T16:05:45Z through16:05:46Z. Read-only
post-run checks parsed the source with Python `ast`, recomputed file hashes,
summed every ledger charge, counted journal record kinds and compared the342
protected paths with `initial-source-hashes.json`. No official `run` command
was issued.

## Frozen source and manifest

The only implementation source is
`numerics/positive_query_sampling.py`. Its estimator has the exact signature
`(oracle,T,n,rng)`. An AST name audit of that function found only its four
arguments, the public fixed batch size, NumPy/Python arithmetic, result/error
types and local variables. It has no width, mass, support, shift, nominal
level, profile formula or reference access. There is no zero-input shortcut:
the sampler draws and passes every point to the supplied callable.

The counting wrapper charges the full vector request before calling the
oracle. It separately stores attempted, returned and positive-return counts.
The sampler uses batches of131072 followed by the exact remainder, one
binary64 `numpy.sum` per batch, ordered `math.fsum` of batch sums, one division
by n and the hypot-based transform. An exception record retains the RNG state,
attempted/returned counts, completed batch sums/counts, traceback and replicate
identity. Official cell journals are append-only; completed cell files use a
new temporary path and atomic, no-overwrite publication. A started official
directory cannot be silently resumed.

The manifest stores HEAD
`65dca46e42db1c80cdf9ddd8eed6a415148c37f3`, Python3.11.15, NumPy2.4.6,
mpmath1.3.0 at100 decimal digits, PCG64 key conventions, all widths and exact
binary ratios, both frozen E3 integral strings, primary/cross-check references,
schedule integers, tolerances, accounting rules and scope disclaimers. It
freezes02g,02f,04q,05h,06i,06j,T46,T48,T51,T52,T58, both accepted formal
sources, E3 scalar input, the implementation and the342-hash source record.
The342 protected files had zero missing paths and zero mismatches before
prepare, at preflight entry and after preflight.

The widest stored width, for T=12 and nominal z=4, is
`0x1.5680d85176f29p-3` =0.16723793982134197 with exact ratio
6025381787692841/36028797018963968. It exceeds3/20, so the prescribed periodic
wrap case is present. Every other nonzero stored width was also checked to lie
strictly between0 and1.

## Preflight observations

The point-call ledger contains220 charged vector calls. Their individual
charges sum to655633 and the final cumulative value is655633:

| Frozen block | Calls | Result |
| --- | ---: | --- |
| Nine opaque constant tests | 393279 | 9/9 pass |
| Two actual wrapped-bump executions | 262150 | bitwise replay pass |
| Twelve cases at17 fixed points | 204 | 204/204 pass |
| Scalar Psi checks | 0 | 8/8 pass |
| Stored-width reference cross-checks | 0 | 12/12 pass |
| Design/schema recalculation | 0 | pass |

The constant means were exact in binary64 in all nine tests. Their maximum
output error against the100-digit scalar value rounded to binary64 was
1.1102230246251565e-16, below the frozen2e-15 tolerance. Counts were exactly n;
positive-return counts were n for positive constants and zero for zero.

Both wrapped runs started from entropy20260927 and spawn key `(1,0)`. Each used
batches `[131072,3]`, made131075 calls, observed21838 positive returns and
returned the same binary64 mean2.456665380691412e-05 and
output0.970118812173996. Their full initial/final PCG64 states, means, outputs,
batch records and counts agree bit-for-bit.

All204 pointwise comparisons passed. The maximum absolute difference from the
100-digit formula evaluated using the exact binary ratios of the point, width
and implemented shift was3.2526065174565133e-19, below the frozen
`1e-14 + 1e-11*abs(reference)` tolerance. There were31 recorded cases where the
binary64 oracle returned zero while the high-precision implemented-profile
reference was positive. These expected boundary/near-boundary underflows are
retained row by row in the journal; they were not converted to support hits.
The fixed points include both sides of the periodic seam and all zero-member
queries were charged.

All eight stable-Psi values passed with maximum absolute error
1.1102230246251565e-16. All twelve primary/cross-check stored-width references
passed the1e-14 empirical tolerance; the maximum difference was about
2.328e-81. This agreement is not a rigorous enclosure.

The independent schedule recalculation reproduced180 cells,18720 stochastic
outputs, maximum n=2114541 and336883488 official calls. The fixed later
replicate-index-zero replay remains30075636 calls. One preflight, one official
run and that subset replay would total367614757 calls, leaving132385243 calls
under the500-million whole-activity cap. No replay or official calls have been
spent.

## Evidence hashes

| Artifact | SHA256 |
| --- | --- |
| `numerics/positive_query_sampling.py` | `cbfda29abd7e4d62e4131502cea5d96fbfaba05c6d0eaf74a9af329f78b458b0` |
| `artifacts/positive-query-sampling/v1/execution_manifest.json` | `f89cb731baa193c140cc42b73a0db7449b49f24795d76339e9c1165846a96428` |
| `artifacts/positive-query-sampling/v1/preflight_activity.jsonl` | `876b23f230fff605c91d74b57b6cdcc8eda4521942a23f36e31844e63b0cdba0` |
| `artifacts/positive-query-sampling/v1/preflight_journal.jsonl` | `89c185bf3066283d0b6f53149b7a6db3550245db1597ebdd266d24b594aad2f1` |
| `artifacts/positive-query-sampling/v1/preflight_result.json` | `7e7327de5cd107366035774f7f109e19c6a0c5d9263cbe031aa503a1ab60aae5` |
| `artifacts/positive-query-sampling/v1/preflight.log` | `fe10f5eda0bcfbac98a27a39585cbd4de8c2127fd30322c3b858dcdd134c45e6` |

The source hash in the manifest and preflight result is unchanged. There is no
`preflight_failure.json`, no v2, and no `official/` directory.

## Scope

This work implements and checks a binary64/PCG64 numerical realization of the
specified opaque-query algorithm. The exact scalar-surrogate construction and
the binary64 oracle/PRNG execution remain distinct. No actual PDE solution was
computed, no floating-point reference or statistic was certified, and no
machine implementation of iid real sampling was proved. The preflight does not
support a novelty, minimax, practical speed, publication-priority or prize
claim.

The next permitted action is root review of the full source, manifest, complete
journal, ledger and this report. Only a root clearance record binding the v1
source, manifest and successful preflight-result hashes can unlock the official
`run` phase.
