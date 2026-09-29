# T93: actual Gaussian common-component law in Lean

Date: 2026-09-29

## Result

The fixed 05n contract is implemented in
`formal/EstimatorIntegrity/GaussianCommonComponent.lean`. The module builds
under Lean 4.33.0 and Mathlib commit
`db584cd6d46c92f209a44c0f1c829460d327499d`. The fixed contract hash is
`76af8515034e72c12dcf138dd356e6e98396c4a468af079f521260b5507529ea`; the
final source hash is
`68d4cb7a1c04720703f819d52ae2ea0667c3e7f0afd4e918506d1b3497defc19`.

The implementation works with actual random variables and Mathlib measures.
It does not replace the law by a covariance-matrix model, and it does not take
the residual/common-part independence as a hypothesis.

## Actual common-component decomposition

For a finite nonempty index type `I`, `actualCovariance mu X i j` is the
Mathlib covariance of the coordinate functions of `X`. The actual random
variables are

```text
commonPart X w omega     = sum_i w_i * X(omega,i),
residualPart X w omega i = X(omega,i) - commonPart X w omega.
```

`commonPart_hasGaussianLaw`, `residualPart_hasGaussianLaw`, and
`pair_hasGaussianLaw` obtain the Gaussian laws by applying explicit finite
continuous linear maps to the assumed `HasGaussianLaw X mu`. The coordinate
mean hypotheses give the actual mean-zero theorems for the common part and
every residual coordinate.

Under `sum_i w_i = 1` and the actual row-covariance condition, the module
proves

```text
Cov(X_i,A) = a,
Var(A) = a,
0 <= a,
Cov(Z_i,A) = 0,
Cov(Z_i,Z_j) = actualCovariance mu X i j - a.
```

The proof of `residualPart_indep_commonPart` is a whole-vector argument. It
maps `X` to the jointly Gaussian pair `(Z, fun _ : Unit => A)`, applies
`HasGaussianLaw.indepFun_of_covariance_eval` to every residual coordinate and
the singleton coordinate for `A`, then composes with evaluation at `()`. Its
conclusion is `IndepFun (residualPart X w) (commonPart X w) mu`, not a list of
coordinatewise independence statements.

`commonPart_map_eq_gaussianReal` identifies the actual scalar pushforward with
`gaussianReal 0 a.toNNReal`. No positivity assumption is used, so the
degenerate case `a = 0` remains covered. Independence then gives the actual
product pushforward in `residualCommon_map_eq_product`.

`addCommon` is the measurable function `(z,t) |-> fun i => z i + t`.
`reconstruction_law` proves the exact measure identity

```text
mu.map X
  = ((mu.map (residualPart X w)).prod (gaussianReal 0 a.toNNReal)).map addCommon.
```

The two `boundedContinuous_integrable_*` theorems prove integrability on the
original and product spaces. `boundedContinuous_expectation` then derives the
corresponding actual integral identity using `integral_map`; it does not rely
on totalized values of nonintegrable functions.

## Independent finite edge construction

For a finite edge type `E`, `edgeLeafVector Y L` is defined by the actual
finite sum

```text
edgeLeafVector Y L omega i = sum_e L(i,e) * Y_e(omega).
```

`edgeLeafVector_hasGaussianLaw` first applies
`iIndepFun.hasGaussianLaw` to the complete independent scalar edge family and
then applies the supplied coefficient linear map. Thus joint Gaussianity of
the leaf vector is derived from the edge variables.

`edgeVariables_covariance` proves the diagonal/off-diagonal formula. On the
diagonal it rewrites covariance with itself to the stated actual variance
`ell_e`; off the diagonal it extracts `IndepFun (Y e) (Y f)` from the full
family independence and uses `IndepFun.covariance_eq_zero`. Expanding both
finite sums then proves

```text
Cov(X_i,X_j) = sum_e ell_e * L(i,e) * L(j,e).
```

`edgeVariance_nonneg` derives `0 <= ell_e` from the actual variance equality;
zero variances are allowed. `edgeLeafVector_mean_zero` derives the actual
coordinate means from the centered edge variables.

`weighted_edgeCovariance` explicitly interchanges the two finite sums.
Together with the coefficient condition from fixed05n,
`edgeLeafVector_row_covariance` supplies the row-covariance premise of the
general theorem. The exported edge instantiations include whole-vector
residual/common independence, the actual product law, exact reconstruction,
and the bounded-continuous expectation identity. No covariance formula or
common-component law is assumed for the constructed leaf vector.

## Verification

The fresh module build

```text
/Users/michael/.elan/bin/lake build EstimatorIntegrity.GaussianCommonComponent
```

completed all 3648 reported jobs with exit code 0. A separate direct source
check of `EstimatorIntegrity/GaussianCommonComponent.lean` also exited 0; the
source itself sets `autoImplicit false`. Compiler output contains linter
suggestions only and no error or trust warning.

There are 47 public definitions and theorems. `Declarations.lean` records the
exact type of every one, and `Axioms.lean` applies `#print axioms` to every one.
Both audit commands exited 0. Every public declaration reports only
`propext`, `Classical.choice`, and `Quot.sound`. The direct trust scan found no
occurrence of `sorry`, `admit`, `axiom`, `native_decide`, `unsafe`,
`implemented_by`, or `ofReduceBool` in the source.

Evidence is in
`docs/research/runs/2026-09-28-dynamic-continuation/lean/gaussian-common-component/`:

- `build.log`: directly captured fresh module build, timestamps, command,
  working directory, raw combined stream, and exit code;
- `source-check.log`: directly captured source check with the same metadata;
- `Declarations.lean`, `declarations.log`: all 47 public signatures and the
  direct successful audit output;
- `Axioms.lean`, `axioms.log`: all 47 public axiom inventories and the direct
  successful audit output;
- `environment.log`, `environment.md`: pinned toolchain, revisions, commands,
  timestamps, and exit codes;
- `trust-scan.log`: directly captured forbidden-token scan;
- `source-hash.log`: direct source and fixed-contract hashes;
- `Explore.lean`, `Prototype.lean`, the development logs, and
  `failed-attempts.md`: API reconnaissance and honest failure provenance;
- `SHA256SUMS`: hashes of the final source, report, and evidence files.

Only the new module, this report, and its evidence directory were written. The
entrypoint, toolchain, Lake configuration, dependencies, earlier modules,
frozen T86/T92 artifacts, root ledgers, proofs, and numerical artifacts were
not edited.

## Exact boundary

This module proves the fixed finite-dimensional actual Gaussian law and its
independent finite-edge construction. It does not formalize the tree datatype
or inverse-variance recursion, partitions, clocks, nonexplosion, an edge
generation cost, torus wrapping, heat convolution, polynomial voting,
derivatives, Sobolev norms, Hilbert sample averaging, a PDE identity, a final
solver, query complexity, long-time complexity, bit precision, or numerical
performance. In particular, it makes no tree-recursion lower-variance or PDE
certificate claim.
