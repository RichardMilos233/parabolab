# T52: positive independent sample means and full actual risk in Lean

Status: **scoped formal PASS**.  The new module proves the actual sample-mean
MSE bound from measurable pairwise independent bounded samples on an arbitrary
probability space.  It then combines this result with the frozen T51 sigmoid
module to prove the requested transformed and total integral-risk bounds.

The fixed contract was
`05h-positive-upper-bound-lean-contract.md`, SHA-256
`c0d5f17b0e13dcb131405c8bcfad3ad34b1a9f9b91b79e6902606a6f08a376a9`.
The imported frozen T51 source was
`formal/EstimatorIntegrity/PositiveSigmoidRisk.lean`, SHA-256
`3ae1d9acff2ff1f8dae63816b53f7c05eb4f5cd3f562b968d1cb7df168bf9a6d`.

## Encoded independent-sample theorem

`positiveSampleMean Y` is the pointwise arithmetic mean

```text
(sum i : Fin n, Y i omega) / (n : Real).
```

The main independent-sample theorem is
`positiveSampleMean_mse_le`.  Its quantified data are an arbitrary type
`Omega`, measurable space, measure `mu`, probability-measure instance,
positive natural `n`, and a family `Y : Fin n -> Omega -> Real`.  Its
hypotheses are:

```text
0 <= A, 0 <= m,
Measurable (Y i),
Pairwise (fun i j => IndepFun (Y i) (Y j) mu),
0 <= Y i omega <= A,
integral mu (Y i) = m.
```

No integrability, second moment, covariance cancellation, sample variance, or
finite probability-space premise is supplied.  The module derives:

* `positiveSample_integrable` from the measurable pointwise bound;
* `positiveSample_memLp_two` from the same bound;
* measurability and integrability of `positiveSampleMean`;
* `positiveSampleMean_unbiased`, the actual identity
  `integral mu positiveSampleMean = m`;
* integrability of `(positiveSampleMean-m)^2`;
* the actual bound

```text
integral mu (fun omega => (positiveSampleMean Y omega - m)^2)
  <= A*m/(n : Real).
```

`positiveSample_product_integral` exposes the required off-diagonal identity
directly from `IndepFun.integral_fun_mul_eq_mul_integral`:

```text
i != j -> integral mu (fun omega => Y i omega * Y j omega) = m*m.
```

The MSE proof uses Mathlib's `IndepFun.variance_sum` with the derived `L2`
hypotheses.  That theorem eliminates cross covariances from the supplied
pairwise `IndepFun` facts; its Mathlib proof uses the same product-integral
identity rather than an assumed covariance premise.  Each diagonal variance
is bounded by the Bhatia--Davis inequality
`Var(Y_i) <= (A-m)*m <= A*m`.  Scaling the finite variance sum by `1/n^2`
gives the result.

## Real-power and sampling-budget layer

`positive_rpow_one_add_le_one_add_sq` proves, for `z>=0` and `0<beta<1`,

```text
z^(1+beta) <= 1+z^2.
```

This is proved by splitting `z<=1` and `1<=z`, using the appropriate Mathlib
monotonicity theorem for `Real.rpow`.  It is not a hypothesis of the final
certificate.

For `m>0`, `positive_scaled_rpow_identity` proves the exact identity

```text
exp((1-beta)*T) * (exp(T)*m)^(1+beta)
  = exp(2*T) * m^beta * m.
```

The proof uses `Real.mul_rpow`, `Real.rpow_add`, and `Real.exp_add` with their
positivity obligations discharged explicitly.  The scaled sample theorem
handles `m=0` separately: the raw MSE bound has upper bound zero, while the
squared-loss integral is nonnegative, so its integral is exactly zero.  No
zero-base power cancellation is used in that branch.

`positiveSampleMean_scaled_mse_le` assumes the actual structural and budget
conditions

```text
0 < beta < 1, 1 <= C,
A <= C*m^beta,
64*C*exp((1-beta)*T) <= (n : Real),
```

and derives

```text
integral mu (fun omega =>
  (exp(T)*positiveSampleMean Y omega - exp(T)*m)^2)
  / (1+(exp(T)*m)^2) <= 1/64.
```

The proof feeds the actual sample MSE into the exact exponent identity,
cancels the stated sample budget, and then applies the proved rpow ratio.

## Combined actual risk certificate

`positiveSampleMean_transformed_mse_le` constructs the measurable nonnegative
random variable

```text
X omega = exp(T) * positiveSampleMean Y omega
```

and derives integrability of `(X-exp(T)*m)^2` from the sample theorem.  It then
applies T51's `positiveSigmoid_integral_loss_le` to obtain the actual integral
bound

```text
integral mu (fun omega =>
  (positiveSigmoid (X omega) - positiveSigmoid (exp(T)*m))^2)
  <= 1/64.
```

`positiveSampleMean_full_risk_certificate` adds the fixed contract hypotheses
`0<=T` and the explicit deterministic bias input

```text
|y-positiveSigmoid (exp(T)*m)| <= 1/32.
```

Using T51's actual integral Cauchy--Schwarz composition theorem, it returns all
three conclusions in one statement:

```text
transformed actual MSE <= 1/64,
total actual MSE       <= 25/1024,
total actual MSE       <  1/16.
```

The exact `25/1024` result is retained; the strict `1/16` fact follows from
that exact rational comparison.

## Correspondence boundary

This is a theorem about an arbitrary probability space and an actual family
of measurable pairwise independent real random variables.  It does not assume
a finite seed space.  It formalizes the independent-sample variance, scalar
scaling, sigmoid transform, and risk composition layers.

The deterministic bound
`|y-positiveSigmoid(exp(T)*m)|<=1/32` is an explicit hypothesis.  The module
does not formalize or claim the positive Allen--Cahn PDE approximation,
heat-kernel estimates, height-versus-mass interpolation, nonlinear comparison,
or uniform PDE bias.  It also does not formalize the construction of iid
uniform oracle samples or bit arithmetic; such samples conventionally provide
the measurable pairwise-independent family required here.  No numerical code
or experiment was added.

## Verification

No project entrypoint, package file, or toolchain file was edited.  The active
versions were:

```text
active toolchain: leanprover/lean4:v4.33.0
  (overridden by formal/lean-toolchain)
Lean 4.33.0, commit d8b18978322de05a8f3dba51ef03cf5461676c17
Lake 5.0.0-src+d8b1897
Mathlib commit db584cd6d46c92f209a44c0f1c829460d327499d
Mathlib tag master-2026-08-10
```

Before the final target build there was no
`.lake/build/lib/lean/EstimatorIntegrity/PositiveSampleMean.olean`.  The fresh
build recorded in `lean/positive-sample-mean/build.log` was:

```text
$ cd formal
$ ~/.elan/bin/lake build EstimatorIntegrity.PositiveSampleMean
✔ [3457/3457] Built EstimatorIntegrity.PositiveSampleMean (101s)
Build completed successfully (3457 jobs).
```

The source scan

```text
rg -n '\b(sorry|admit|axiom|opaque)\b' \
  formal/EstimatorIntegrity/PositiveSampleMean.lean
```

returned no matches.  The axiom harness prints every authored exported
declaration.  Every one depends only on Mathlib's standard
`[propext, Classical.choice, Quot.sound]`; there is no custom axiom.

SHA-256 values for the exact verified artifacts are:

```text
84cb8468f56f55dbfca243209d64a36164acbdc8625076a7d4ae46f302ca6703  formal/EstimatorIntegrity/PositiveSampleMean.lean
a1b511610dc81d8bd123173c14b6e00cb633a8d16f6dc8c251ced04faaaea71b  docs/research/runs/2026-09-28-dynamic-continuation/lean/positive-sample-mean/build.log
3e27ce5c4d97f3fb8941779a0aef09ee736166a90c5f83b6d5a41665cd60bc3a  docs/research/runs/2026-09-28-dynamic-continuation/lean/positive-sample-mean/axioms.log
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/research/runs/2026-09-28-dynamic-continuation/lean/positive-sample-mean/source-scan.log
4cfcbfd2a1c98618ddeaad4e0d88074865f58ef3aa1d163bb87504f6909a3d89  docs/research/runs/2026-09-28-dynamic-continuation/lean/positive-sample-mean/PositiveSampleMeanAxioms.lean
```

Failed attempts and their fixes are preserved in `attempt-01` through
`attempt-09` and summarized in `development.log` in the same log directory.
