# T89: Hilbert sample means and profile-risk transfer in Lean

Date: 2026-09-29

## Result

The fixed05m contract is implemented in
`formal/EstimatorIntegrity/HilbertSamplingRisk.lean`. The module uses actual
Bochner integrals and actual squared Hilbert norms throughout. It compiles with
Lean 4.33.0 and Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`.

The requested implementation configuration was `gpt-5.6-sol` with `xhigh`
reasoning. Backend telemetry is not exposed to the worker, so this report does
not claim an independently observed execution model.

## Hilbert sample means

For an arbitrary probability space and a real complete inner-product space
with Borel measurable structure, `sampleMean` is the actual finite mean

```text
(1/(n:Real)) • sum_i Y_i(omega).
```

From `MemLp (Y i) 2 μ`, the module proves integrability of each sample, each
centered sample, both corresponding squared norms, the mean, and its actual
squared error. `integral_sampleMean` proves that the Bochner expectation is the
average of the individual Bochner means.

For pairwise independent samples, independence is transported through
subtraction of the deterministic means. `IndepFun.integral_bilin` is applied to
the real Hilbert inner product. Its off-diagonal integrals are zero because
both centered Bochner means are zero. Expanding the square of the finite sum
then proves

```text
integral ‖sampleMean Y - meanAverage μ Y‖² dμ
  = (1/n²) * sum_i integral ‖Y_i - integral Y_i dμ‖² dμ.
```

The separate theorem `integral_centered_sq_eq` proves

```text
integral ‖Y-integral Y‖² dμ
  = integral ‖Y‖² dμ - ‖integral Y‖².
```

With `n>0`, common means `integral Y_i=m`, and actual second-moment bounds
`integral ‖Y_i‖²<=V`, the public corollary proves

```text
integral ‖sampleMean Y-m‖² dμ <= V/n.
```

`V>=0` is explicit. No identical-distribution, bounded-sample, coordinate
independence, or ambient-dimension assumption occurs.

## Dependent derivative-order batches

`rawEstimator` is the actual function

```text
b + sum_j a_j • sampleMean(Y_j).
```

The module proves its `MemLp 2` membership, almost-everywhere strong
measurability, the `MemLp 2` property of `raw-c`, and integrability of the
actual squared loss.

The deterministic Hilbert inequality is proved by the triangle inequality and
finite scalar Cauchy--Schwarz, using an `Option (Fin m)` index for the bias plus
the `m` batch errors:

```text
‖bias + sum_j e_j‖² <= (m+1) * (‖bias‖² + sum_j ‖e_j‖²).
```

Applying the single-batch result separately, with no independence assumption
between different `j`, gives

```text
integral ‖raw-c‖² dμ
  <= (m+1) * (beta² + sum_j a_j² V_j/n).
```

The theorem is valid for `m=0`, zero weights, and zero moment bounds. The only
independence hypotheses are pairwise independence between distinct samples
inside each fixed batch.

## Anchored contraction, box clipping, and strong norm

For every continuous `K:H->H` satisfying

```text
‖K z-c‖ <= ‖z-c‖,
```

the module derives `MemLp 2` and squared-loss integrability for `K(raw)-c` by
domination. `anchored_rawEstimator_risk_le` transfers the preceding raw bound
by integrating the pointwise contraction. The final risk is not assumed as a
premise.

For finite `I`, `boxClip l u` is the actual Euclidean-space map

```text
boxClip(z)_i = max(l_i, min(u_i,z_i)).
```

If every `c_i` belongs to its interval, the module proves that clipping fixes
`c`, is continuous, and satisfies both

```text
‖boxClip(z)-c‖² <= ‖z-c‖²
‖boxClip(z)-c‖  <= ‖z-c‖.
```

The squared proof sums the scalar three-case interval inequality over actual
Euclidean coordinates. `boxClip_rawEstimator_risk_le` instantiates the general
contraction theorem. This introduces no independent-coordinate model and no
factor involving `Fintype.card I` in the statistical risk.

For any real normed space `G` and bounded linear map `A:H->G`, the module proves
`MemLp 2` and integrability of the actual strong-norm loss, followed by

```text
integral ‖A(K(raw))-A(c)‖² dμ
  <= ‖A‖² * (m+1) * (beta² + sum_j a_j² V_j/n).
```

The pointwise operator-norm inequality is squared and integrated before the
anchored risk theorem is applied.

## Verification and provenance

All accepted verification logs were captured directly at execution by
`lean/hilbert-sampling-risk/capture.sh`. Each raw log contains the exact command,
working directory, UTC timestamps, exit code, and source SHA-256, with combined
stdout/stderr between explicit delimiters.

- `final-direct-source-check.log`: direct `lake env lean` check, exit 0.
- `fresh-library-build.log`: fresh library-module build with
  `autoImplicit=false`, exit 0.
- `public-types.log`: `#print` of every public definition and theorem, exit 0.
- `public-axioms.log`: `#print axioms` for every public theorem, exit 0.
- `trust-scan.log`: no `sorry`, `admit`, custom `axiom`, `native_decide`, or
  `unsafe`, exit 0.
- `environment.log`: pinned Lean, toolchain, and Mathlib revision, exit 0.

Every public theorem reports only `propext`, `Classical.choice`, and
`Quot.sound`. The scratch-diagnostic coverage and its limits are stated in
`failed-attempts.md`. No numerical execution or oracle call was made.

## Coverage boundary

This module covers only the finite statistical bridge: Hilbert-valued sample
means, within-batch pairwise independence, dependence-retaining multi-batch
risk, anchored contractions, actual Euclidean box clipping, and bounded-linear
strong-norm transfer.

It does not formalize the random tree, Brownian covariance, positive
semidefinite factorization, heat kernel, sampling-law equality, finite leaf
work, Sobolev/Fourier identification, `S_1` differentiability, Taylor
remainder, PDE-specific clipping ranges, Gevrey saturation, final PDE
continuation, solver accuracy, oracle counts, minimax exponent, finite-bit
execution, or novelty. The reconstruction-operator norm and the actual
Fourier/Sobolev identification remain external inputs.

Only the new module, this report, and
`lean/hilbert-sampling-risk/` were written. Existing modules, the library
entrypoint, lakefiles, toolchain, dependencies, numerical artifacts, and root
claim/state files were not edited.
