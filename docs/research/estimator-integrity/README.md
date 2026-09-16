# Mathematical notes

For the current research question, start with the [research guide](../README.md).
For exact theorem status and Lean correspondence, use the
[proof registry](../proof-registry.md). This index was reviewed on
16 September 2026.

## Core arguments

- [Notation and moment recursion](notation-and-moment-theorem.md): what
  the tree functional and killed-depth moments mean.
- [Exponential-rate optimization](exponential-rate-optimization.md):
  distinguish fixed continuation, full recursive dependence and the
  leading short-time rule.
- [General rate selection](general-rate-selection.md): conditional
  minimization, cutoff consistency and quantitative objective-gap transfer.
- [Adaptive tuple proposals](adaptive-proposals.md): local square-root
  oracle, support and pilot/freeze reasoning.
- [Dym nonintegrability](dym-nonintegrability.md): a negative example for
  the specified estimator, rather than a variance-reduction benchmark.

## Frozen mathematical inputs to saved certificates

These four documents are hashed in numerical result metadata. Their
mathematical assumptions and derivations support the saved certificates;
their bytes are preserved for reproduction:

- [Six-code Allen–Cahn bounds](allen-cahn-codewise-certificate.md).
- [Rate-invariant PDE mean](allen-cahn-mean-identification.md).
- [Wave polynomial residual verification](wave-numerical-certification-route.md).
- [Weighted-profile objective and bounds](profile-rate-efficiency.md).

Their 14 September status notes are historical. In particular, the wave
route's old pending-merge statement is superseded by the
[16 September integration record](../results/integration-2026-09-16.md).
The weighted-profile objective remains an optional extension for several
starting states sharing a rate. Its cost-model sections are supporting
analysis, not the primary research objective.

For implemented results and what the actual Python checker verifies, use
the [results index](../results/README.md). Conventional mathematical
arguments and exact rational computations do not imply that Lean has
verified either the stochastic correspondence or the Python programs.

## Historical investigation and alternatives

- [Reproducibility ledger](reproducibility.md): earlier environment,
  worktree and diagnostics, explicitly distinct from current checks.
- [Secondary candidates](secondary-candidates.md): retained alternatives
  and historical literature comparisons, not mandatory future tasks.

The [documentation map](../../documentation-map.md) places these notes
alongside current APIs, reports and inactive financial research.
