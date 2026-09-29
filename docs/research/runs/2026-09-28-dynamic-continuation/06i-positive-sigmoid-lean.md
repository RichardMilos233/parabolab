# T51: positive sigmoid and actual integral risk in Lean

Status: **scoped formal PASS**.  The new module defines the actual sigmoid,
proves its analytic properties and anchored loss inequality, derives the
transformed integral risk on an arbitrary probability space, and proves the
exact `25/1024` bias-composition bound from an actual integral
Cauchy--Schwarz argument.

The frozen conventional inputs were `04q-matching-positive-query-complexity.md`,
T46 SHA-256
`6ad43f33f45739a510ea6ea968041e4332762fa3c358773ce431c57ac9e93997`,
and T48 SHA-256
`75415cdb37485b7fb9fc3aecdf733870cd1ab285fa3ce6cf24ebd12e66c26fea`.
This report makes no novelty claim.

## Encoded scalar analysis

The source is `formal/EstimatorIntegrity/PositiveSigmoidRisk.lean`.  It defines

```text
positiveSigmoid z = z / Real.sqrt (1 + z^2).
```

`continuous_positiveSigmoid` proves continuity directly from that definition;
the denominator is nonzero because `1 + z^2` is strictly positive.
`positiveSigmoid_nonneg` and `positiveSigmoid_le_one` prove that for `z>=0`
the value lies in `[0,1]`.

`positiveSigmoid_mono_nonneg` proves monotonicity without assuming it or using
concavity.  It compares the squares of the two nonnegative ratios and clears
their strictly positive squared denominators; the cross-products reduce to
`x^2<=z^2`.

`positiveSigmoid_anchored` then proves for every `x,z>=0`, including either
value being zero,

```text
|positiveSigmoid x - positiveSigmoid z|
  <= |x-z| / Real.sqrt (1+z^2).
```

The proof splits `x<=z` and `z<=x`.  Monotonicity determines the sign of the
difference, while square-root denominator ordering compares the non-anchor
ratio with a ratio having the anchor denominator.  The inequality is therefore
derived from the actual formula and is not an input premise.

## Arbitrary probability-space results

All probabilistic results take an arbitrary type `Omega`, measurable space,
measure `mu`, and `[IsProbabilityMeasure mu]`.  There is no finite-space
assumption.

`positiveSigmoid_squaredLoss_integrable` starts with a measurable pointwise
nonnegative real random variable `X` and an arbitrary fixed real target.  It
proves integrability of the squared transformed loss from measurability and the
pointwise sigmoid range: the absolute difference is bounded by
`1+|target|`, whose square is integrable under a probability measure.  It does
not assume boundedness or integrability of `X`.

`positiveSigmoid_integral_loss_le` additionally assumes `z>=0` and actual
integrability of `(X-z)^2`.  Squaring the anchored inequality and using
`sqrt(1+z^2)^2=1+z^2`, then applying integral monotonicity, proves

```text
integral mu (fun omega =>
    (positiveSigmoid (X omega) - positiveSigmoid z)^2)
  <= integral mu (fun omega => (X omega-z)^2) / (1+z^2).
```

The transformed loss is proved integrable first via the range theorem; its
integrability is not inferred circularly from the desired final bound.

`integral_abs_le_sqrt_integral_sq` is the actual probability-space
Cauchy--Schwarz result used for composition:

```text
integral mu (fun omega => |F omega|)
  <= sqrt (integral mu (fun omega => F omega^2)).
```

It constructs the `L2` memberships of `|F|` and the constant-one function and
applies Mathlib's integral Holder theorem with exponents `(2,2)`; probability
normalization reduces the constant-one second moment to one.

Finally, `positiveSigmoid_bias_composition` assumes the actual transformed MSE
is at most `1/64` and `|y-positiveSigmoid z|<=1/32`.  Cauchy--Schwarz gives
`integral |F|<=1/8`.  The proof expands the squared error pointwise, controls
the cross term by absolute values, proves every integrated term is integrable,
and obtains exactly

```text
1/64 + 2*(1/32)*(1/8) + 1/1024
  = 1/64 + 1/128 + 1/1024
  = 25/1024.
```

No RMS triangle inequality, anchor inequality, transformed variance bound, or
desired total risk bound is supplied as a hypothesis.

## Correspondence boundary

This module formalizes the scalar analytic and probability-space risk layer.
It does not formalize the positive Allen--Cahn PDE approximation, heat-kernel
mixing or minorization, nonlinear comparison, height-versus-mass interpolation,
the uniform deterministic bias certificate, iid uniform point sampling,
sample-mean unbiasedness or variance, query budgets, or the full PDE estimator.
Those PDE and interpolation inputs remain conventional from 04q/T46/T48.
The independent-sample layer belongs to T52 and is not imported here.  No code
or numerical experiment was run for this formal gate.

## Verification

The protected project configuration was not edited.  Its active versions were:

```text
$ ~/.elan/bin/elan show
active toolchain: leanprover/lean4:v4.33.0
  (overridden by formal/lean-toolchain)

$ ~/.elan/bin/lake env lean --version
Lean (version 4.33.0, arm64-apple-darwin24.6.0,
      commit d8b18978322de05a8f3dba51ef03cf5461676c17, Release)

$ ~/.elan/bin/lake --version
Lake version 5.0.0-src+d8b1897 (Lean version 4.33.0)

$ git -C formal/.lake/packages/mathlib rev-parse HEAD
db584cd6d46c92f209a44c0f1c829460d327499d

$ git -C formal/.lake/packages/mathlib describe --tags --exact-match HEAD
master-2026-08-10
```

The manifest input revision is Mathlib `v4.33.0`.  The fresh build was:

```text
$ cd formal
$ ~/.elan/bin/lake build EstimatorIntegrity.PositiveSigmoidRisk
✔ [3396/3396] Built EstimatorIntegrity.PositiveSigmoidRisk (93s)
Build completed successfully (3396 jobs).
```

The source scan command

```text
rg -n '\b(sorry|admit|axiom|opaque)\b' \
  formal/EstimatorIntegrity/PositiveSigmoidRisk.lean
```

returned no matches.  The axiom harness prints every authored exported
declaration.  Every declaration depends only on Mathlib's standard
`[propext, Classical.choice, Quot.sound]`; there is no custom axiom.

SHA-256 values for the exact verified artifacts are:

```text
3ae1d9acff2ff1f8dae63816b53f7c05eb4f5cd3f562b968d1cb7df168bf9a6d  formal/EstimatorIntegrity/PositiveSigmoidRisk.lean
da1b7b7fbb5a33eb6e8e435bd5982ddceeb2cb94af4afbf4beb95760f5781ceb  docs/research/runs/2026-09-28-dynamic-continuation/lean/positive-sigmoid/build.log
9960085251f4f4fefad98fd49ea3d89281df845ced356473c75f78f0a77ac644  docs/research/runs/2026-09-28-dynamic-continuation/lean/positive-sigmoid/axioms.log
5666dfc2e43b617f75eb6c8038ece5cb88159816fe3f040eccfb66d9ef3b597d  docs/research/runs/2026-09-28-dynamic-continuation/lean/positive-sigmoid/source-scan.log
1e0cd567a415824583e0684eb8c00d9623dc8f76871c6320affa4763c979f462  docs/research/runs/2026-09-28-dynamic-continuation/lean/positive-sigmoid/PositiveSigmoidRiskAxioms.lean
```

The failed attempts and exact fixes are retained in
`lean/positive-sigmoid/attempt-01.log` through `attempt-12.log` and summarized
in `lean/positive-sigmoid/development.log`.  Final build, source-scan, and axiom
outputs are preserved in the same directory.
