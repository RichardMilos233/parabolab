# T34b — verification of the revised experiment protocol

**PASS. No remaining protocol blocker from T34.**

Checked [02d-two-barrier-experiment-protocol.md](../02d-two-barrier-experiment-protocol.md),
SHA-256
605eda24574bfb7e44dc997c185836d2a54311c18344e0be4c005674e00beda9.
This bounded reread verifies the corrections requested by
[T34](T34-two-barrier-protocol-review.md). It does not reopen the theory,
rerun the Lean gate, execute tests, or produce experimental data. T34 and
all other frozen reviews remain unchanged.

## Closure of the five conditional-pass points

1. **Time-zero output:** now explicitly returns
   $Z=(v-m)/(M-m)$, $W=1-v$, one node/leaf, no internal vertices, and zero
   clock proposals/rejections. The text correctly excludes the two analytic
   baselines from the claim of initial-value exactness.

2. **Diagnostic law and query:** the clock diagnostic explicitly counts
   100000 accepted finite-horizon outcomes after rejection at each prescribed
   horizon, retaining event/leaf indicators, accepted times and trial counts.
   Endpoint diagnostics now fix $x=0$. The full workload is correctly
   recorded as 731792 PDE roots plus 300000 accepted standalone clocks.

3. **Metric and failure gates:** seed-specific signed relative errors and
   $\operatorname{RMS}_3=\sqrt{\sum_j e_j^2/3}$ are fixed per $(T,x)$.
   The nominal 1% ideal ensemble target is distinguished from realized or
   floating errors. All prescribed preflight, reference and diagnostic
   failures stop primary execution and preserve evidence; seeds, thresholds,
   sample sizes and scientific cases cannot be changed to obtain a pass.
   The four statistical diagnostics' ideal union false-alarm bound is
   correctly stated as at most $4\cdot10^{-6}$.

4. **Timing comparison:** the 16-mode loose-tolerance run is designated in
   advance, conditional on passing the reference discrepancy gate. One
   deterministic solve and all 21 query evaluations are compared with each
   seed's full 21-query sampling time. Six-run validation costs are separate.
   The protocol expressly avoids an equal-accuracy optimization or general
   solver-superiority claim.

5. **Reference independence:** the six solves are correctly described as
   refinement runs of one method. Diagnostic closed forms may not import
   sampler clock/barrier helpers. The mathematical sampler is separated from
   the independent deterministic producer; its driver may read the frozen
   artifact for gates and post-sampling comparisons.

## Manifest, inputs, preservation and timing requirements

The revised protocol supplies the previously requested operational details:

- SeedSequence entropy and spawn keys are explicit for primaries and all
  diagnostic families, with zero-based index conventions. PCG64, binary64,
  uniform endpoints, zero redraws, RNG states, and an immutable pre-execution
  environment/source/gate manifest are specified.
- The Galerkin basis includes modes zero through $K$, with explicit periodic
  nodes and cosine normalization. Every reference solve runs once from zero
  to 256 and evaluates at the fixed horizons.
- Projection and analytic-Jacobian checks have a fixed all-mode nonzero
  coefficient vector, three fixed times, and $10^{-10}$ maximum absolute
  discrepancy threshold. The three constant-profile inputs and their
  $10^{-8}$ scaled discrepancy threshold are also fixed before evaluation.
- The 120-second deadline measures monotonic elapsed sampling time with
  processing/I/O excluded. Checks occur both within and between roots;
  append-only checkpoint chunks contain at most 1000 completed roots.
  Interrupted roots are unfinished, completed prefixes are retained, and
  incomplete cells cannot be presented as completed primary estimates.
- The independent reference artifact interface fixes the strict query array
  shape, times and queries, and retains all six coefficient/query arrays,
  gates and timings. Sampler and reference outputs have separate directories.
  Final-artifact overwrite, selective replacement, and reuse of stale
  scientifically affected evidence are prohibited.

The scientific grid, sample sizes and statistical thresholds remain those
already checked in T34. The implemented formulas and realized results still
require their own verification; this pass certifies that the reviewed
protocol is sufficiently specified to proceed to implementation without
selecting scientific parameters after observing outcomes. It supplies no
floating-unbiasedness or complete numerical-bias certificate.
