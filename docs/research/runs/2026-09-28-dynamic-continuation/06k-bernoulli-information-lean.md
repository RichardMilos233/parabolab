# T62: actual Bernoulli information gate in Lean

Status: **scoped formal PASS, pending root source review against the fixed
contract**. The module proves the first actual probability gate requested by
`05i-signed-information-lean-contract.md`. It uses Mathlib's Bernoulli measure,
Radon--Nikodym derivative, and Kullback--Leibler divergence throughout.

## Actual probability model and KL bridge

`bernoulliBool p` is exactly
`ProbabilityTheory.bernoulliMeasure true false p`. The theorem
`bernoulliBool_true` checks the argument order by proving that its real mass on
`{true}` is `p`. The exported instance
`bernoulliBool_isProbabilityMeasure` records that this wrapper is a probability
measure.

For an interior reference `q`, the private bridge
`bernoulliBool_eq_withDensity` proves the actual measure identity

```text
bernoulliBool p = (bernoulliBool q).withDensity density(p,q),
```

where the density is `p/q` at `true` and `(1-p)/(1-q)` at `false`, expressed
as quotients of the corresponding `unitInterval.toNNReal` masses. Both
denominators are proved nonzero from `0<q<1`; no absolute continuity or KL
formula is assumed.

`bernoulliBool_kl_ne_top` derives finite actual KL from that density identity,
`withDensity_absolutelyContinuous`, and finite-space integrability.
`bernoulliBool_kl_toReal` then uses
`InformationTheory.toReal_klDiv_of_measure_eq`,
`MeasureTheory.integral_rnDeriv_mul_log`, `Measure.rnDeriv_withDensity`, and
`ProbabilityTheory.integral_bernoulliMeasure` to prove

```text
(klDiv (bernoulliBool p) (bernoulliBool q)).toReal
  = p*log(p/q) + (1-p)*log((1-p)/(1-q)).
```

The source parameter is the closed unit interval, so `p=0` and `p=1` are
included. The proof uses Mathlib's actual convention `Real.log 0 = 0` and
proves the scalar log-division identity separately at both endpoints.

## Information inequalities

`bernoulliKLScalar_le_chiSq` proves

```text
D(p||q) <= (p-q)^2/(q*(1-q))
```

from `Real.log_le_sub_one_of_pos`. Its helper splits a zero numerator before
applying the positive logarithm inequality, so both source endpoints are
covered. `bernoulliBool_kl_le_chiSq` transports this result through the actual
KL formula.

`bernoulliKLScalar_pinsker` proves the closed-interval scalar inequality

```text
2*(p-q)^2 <= D(p||q)
```

for interior `q`. It constructs `D_q(x)-2*(x-q)^2`, proves continuity on
`[0,1]`, proves nonnegative second derivative on `(0,1)`, obtains convexity on
the closed interval, and proves that the derivative vanishes at `q`. Thus the
source endpoints follow from the same closed-domain convexity theorem rather
than from an assumed limiting statement.

`bernoulliBool_pinsker` covers all reference parameters under the explicit
finite actual KL hypothesis. For `q=0`, absolute continuity forces the source
mass at `true` to vanish, hence `p=0`. For `q=1`, it forces the source mass at
`false` to vanish, hence `p=1`. The strictly interior branch invokes the actual
KL formula and the proved scalar inequality. Endpoint equality is therefore
derived from actual finite divergence, not assumed.

Finally, `bernoulliBool_testing_error` takes the actual ENNReal hypothesis

```text
klDiv (bernoulliBool p) (bernoulliBool q) <= ENNReal.ofReal (1/12)
```

and proves

```text
3/8 <= ((1-p)+q)/2.
```

It first derives finiteness and a real KL upper bound, applies the actual
endpoint-aware Pinsker theorem, and closes the exact rational inequality.

## Correspondence boundary

This scoped module proves only Bernoulli KL, its elementary upper bound,
binary Pinsker, and the equal-prior binary-testing consequence. It does not
formalize the remaining fixed-weight urn law, adaptive fresh-cell
exchangeability, conditional KL chain rule, transcript padding, stopping-time
truncation, finite-prior averaging, MSE-to-label reduction, a randomized
point-query algorithm, or the signed PDE construction. Those remain the
separate G1--G11 obligations identified by T60. This result supplies no D25 or
D27 certificate and makes no novelty claim. No numerical code or experiment
was run.

## Verification

No project entrypoint, lakefile, toolchain file, accepted formal module, or
protected original file was edited. The active versions were:

```text
active toolchain: leanprover/lean4:v4.33.0
  (overridden by formal/lean-toolchain)
Lean 4.33.0, commit d8b18978322de05a8f3dba51ef03cf5461676c17
Lake 5.0.0-src+d8b1897
Mathlib commit db584cd6d46c92f209a44c0f1c829460d327499d
Mathlib tag master-2026-08-10
```

The final clean build recorded in `lean/bernoulli-information/build.log` was:

```text
$ cd formal
$ ~/.elan/bin/lake build EstimatorIntegrity.BernoulliInformation
✔ [3390/3390] Built EstimatorIntegrity.BernoulliInformation (66s)
Build completed successfully (3390 jobs).
```

The source scan for `sorry`, `admit`, `axiom`, or `opaque` returned no
matches. The axiom harness prints every authored public declaration. Every
declaration depends only on Mathlib's standard
`[propext, Classical.choice, Quot.sound]`; there is no custom axiom.

SHA-256 values for the exact verified core artifacts are:

```text
39c0096ef110e85fa8bf8a512bbc1e7b2a8d94a0a20abf3e47d723e80ec77158  formal/EstimatorIntegrity/BernoulliInformation.lean
62d770647ffd6a69d370677e7d39e769710ef9de94f97b28caf77a0dcda4114a  docs/research/runs/2026-09-28-dynamic-continuation/05i-signed-information-lean-contract.md
a22c095421d6ba5370a7b23143437f60c306fe41ca5186eb9d661f93b5018ecf  docs/research/runs/2026-09-28-dynamic-continuation/lean/bernoulli-information/BernoulliInformationAxioms.lean
eaa1aff147bff7b89ae84d6ed3d992af5465e1a66cc449113419f68c3ef9d6f7  docs/research/runs/2026-09-28-dynamic-continuation/lean/bernoulli-information/build.log
f7a29faa5425a71640da9109cc1c92a46bf5efe07db3ed8750c0f2e9c346e7e2  docs/research/runs/2026-09-28-dynamic-continuation/lean/bernoulli-information/axioms.log
aaa6b5bdff6378ed47c398ac94c974e9115d67ab44710110eb957f57660a847d  docs/research/runs/2026-09-28-dynamic-continuation/lean/bernoulli-information/source-scan.log
2df4eb17fa064e53fe5a074b8f632f8f29e1809f1dc43add7f8810d97f9af31d  docs/research/runs/2026-09-28-dynamic-continuation/lean/bernoulli-information/versions.log
18da024a72f8795d1b0d97f1e90ec4e05ad27f9dd0ee64f8671d6d30bf55f13d  docs/research/runs/2026-09-28-dynamic-continuation/lean/bernoulli-information/development.log
```

All eight failed development attempts and their fixes are preserved. The full
attempt hash manifest is `lean/bernoulli-information/final-hashes.log`.
