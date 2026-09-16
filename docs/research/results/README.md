# Research results and evidence

Status reviewed 16 September 2026. Completed certificate/profile work is
integrated into local main. The primary contribution concerns algorithms
and mathematical guarantees; timing experiments are supporting evidence.
The [research guide](../README.md) describes open questions and the
[proof registry](../proof-registry.md) sets the exact claim boundaries.

## Mathematical and implementation checkpoints

1. [Certified-rate checkpoint](certified-rate-checkpoint.md): flat and
   wave full-tree moment bounds, mean identification and global excess
   certificates, with scoped Lean coverage.
2. [Wave certificate](wave-rate-certificate.md): the numerical intervals,
   convex lower bounds and verification method for the wave root.
3. [Binary benchmark audit](binary-benchmark-audit.md): why a standard
   binary oracle cannot validate a different derivative-coded estimator,
   and how that comparison was corrected.
4. [Profile checkpoint](profile-efficiency-checkpoint.md): the optional
   weighted-grid objective, exact policy bounds and associated cost algebra.
5. [Main integration checks](integration-2026-09-16.md): code ancestry,
   Python/Lean checks and rechecked witnesses on the later source.

## Supporting performance investigations

- [Rate/proposal comparison](rate-cost-results.md), under its
  [frozen protocol](rate-cost-protocol.md).
- [Profile/reuse comparison](profile-efficiency-results.md), under its
  [frozen protocol](profile-efficiency-protocol.md).

Distinguish observed errors from expected-error inequalities and actual
timings from predicted budgets. The exact allocation comparisons in the
profile study are conditional on the frozen rates/counts and ideal
estimator; they are not confidence intervals from the replicates. Runtime
findings do not close broader algorithmic questions.

## Archived numerical artifacts

| Directory | Contents |
|---|---|
| [rate-certificate](rate-certificate/summary.json) | Flat certificate, wave moment/depth envelopes and exact witnesses |
| [wave-certificate](wave-certificate/summary.json) | Wave-root polynomial residual certificates and diagnostics |
| [profile-certificate](profile-certificate/summary.json) | Weighted-profile certificates, actual policy bounds and fixed-count loss bounds |
| [rate-cost-benchmark](rate-cost-benchmark/metadata.json) | First frozen benchmark, raw results and execution provenance |
| [profile-efficiency](profile-efficiency/metadata.json) | Profile/reuse benchmark, raw results, execution snapshot and archive audit |

The archives and protocols are preserved. A current source file may have
changed since a recorded run; the old source hashes must not be replaced
to match it. Some legacy validators also record an absolute source path.
Follow the report's snapshot requirements rather than assuming every
archived source audit can run unchanged in a different checkout.

Witness-only verification checks the stored rational inequalities with
the current checker and draws no Monte Carlo samples. The three witness
checks last passed in the integration record. Rebuilding a summary or
rerunning an experiment is a distinct operation and should use a new
output location to retain the original evidence.
