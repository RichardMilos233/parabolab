# T72: finite conditional information and actual binary postprocessing

Status: implementation complete and locally verified against fixed contract
`05j`; pending root acceptance. This is a bounded formal gate and is not a
certificate for the full signed lower bound.

## Fixed inputs

The implementation uses the exact fixed contract
`05j-finite-conditional-information-lean-contract.md` with SHA-256
`79e539057584ae13f1562cf70e266953c123bfaa31708fa92abb72284a0d54fd`.
It imports the accepted T62 source
`formal/EstimatorIntegrity/BernoulliInformation.lean` with SHA-256
`39c0096ef110e85fa8bf8a512bbc1e7b2a8d94a0a20abf3e47d723e80ec77158`.
The exact T72 source has SHA-256
`79d7eda08b513e3eadffc7296bb5db90c6783a68be7edf232f378a27dbcf91ab`.

The active formal environment is Lean 4.33.0 at commit
`d8b18978322de05a8f3dba51ef03cf5461676c17`, Lake
`5.0.0-src+d8b1897`, and Mathlib commit
`db584cd6d46c92f209a44c0f1c829460d327499d` tagged
`master-2026-08-10`.

## Actual finite joint laws

`bernoulliKernel p` is an actual Mathlib Markov kernel defined by
`Kernel.ofFunOfCountable`; its value at history `h` is definitionally the
accepted T62 measure `bernoulliBool (p h)`. The registered
`IsMarkovKernel` instance is obtained from the actual probability-measure
instance for every Bernoulli value.

`finiteJoint_singleton` proves for every history-answer atom that

```text
(mu tensor_m bernoulliKernel p) {(h,b)}
  = mu {h} * bernoulliBool (p h) {b}.
```

The proof unfolds the actual composition-product measure and its finite
integral. It does not assume a path-law formula.

The private function `jointDensity p q` is the conventional ratio `p/q` at
`true` and `(1-p)/(1-q)` at `false`. The private lemma
`finiteJoint_eq_withDensity` proves the actual measure equality

```text
mu tensor_m bernoulliKernel p
  = (mu tensor_m bernoulliKernel q).withDensity (jointDensity p q).
```

It proves equality on every joint singleton. The only cancelled quantities
are the two strictly positive reference Bernoulli masses implied by
`0 < q h < 1`. The history mass is only reassociated and is never cancelled,
so atoms with `mu {h}=0` remain covered. The source parameter stays in the
closed unit interval, so `p h=0` and `p h=1` remain covered.

## Conditional averaging and bounds

`finiteConditionalKL_ne_top` derives absolute continuity from the proved
with-density identity and finite-space integrability. It proves the actual
joint KL is not infinity.

`finiteConditionalKL_toReal` applies the actual Radon--Nikodym KL bridge,
replaces the derivative by the proved joint density almost everywhere, and
uses Mathlib's composition-product integral theorem. The finite outer
integral becomes

```text
sum_h mu.real {h} *
  (klDiv (bernoulliBool (p h)) (bernoulliBool (q h))).toReal.
```

Each inner integral is identified with the accepted T62 actual Bernoulli KL
formula. Thus conditional averaging is proved from the measures and density;
it is not an input hypothesis.

`finiteConditionalKL_le` assumes `0 <= B` and the actual pointwise ENNReal
bound on every conditional Bernoulli divergence. It converts the finite
joint divergence to its real value, applies the pointwise bound with the
nonnegative weights `mu.real {h}`, and uses that those weights sum to one.
The result is the exact actual one-step bound

```text
klDiv (mu tensor_m bernoulliKernel p)
  (mu tensor_m bernoulliKernel q) <= ENNReal.ofReal B.
```

`finiteConditionalKL_accumulate` additionally assumes `0 <= A` and
`klDiv mu nu <= ENNReal.ofReal A`. It invokes Mathlib's exact
`InformationTheory.klDiv_compProd_eq_add` identity on the two actual joint
laws, applies the proved one-step bound, and uses
`ofReal A + ofReal B = ofReal (A+B)`. This is a generic one-step composition
result; the base-law premise is not claimed to be an urn or transcript bound.

## Actual measurable decision theorem

`decisionTrueParameter P D` is exactly
`P.real {omega | D omega = true}`, packaged with the proved closed-unit-
interval bounds.

The private `map_decision_eq_bernoulliBool` proves

```text
P.map D = bernoulliBool (decisionTrueParameter P D)
```

by comparing the two actual Bool singleton masses. The `false` mass is
derived with the measurable complement identity and probability mass one.
The same proof is used independently for `Q`; either true mass may be an
endpoint.

`measurableDecision_testing_error` first applies the actual data-processing
inequality `InformationTheory.klDiv_map_le P Q hD`, rewrites the two actual
pushforward measures as the proved Bernoulli laws, and invokes T62's
`bernoulliBool_testing_error`. Its conclusion is exactly

```text
3/8 <=
  (P.real {omega | D omega = false}
    + Q.real {omega | D omega = true}) / 2.
```

The observation space is arbitrary, the decision is explicitly measurable,
and both input laws are explicitly probability measures. No Pinsker bound,
testing error, pushforward identity, or contraction coefficient is assumed.

## Contract correspondence

| Fixed requirement | Lean evidence | Correspondence |
|---|---|---|
| Actual conditional Bernoulli kernels and joint laws | `bernoulliKernel`, `finiteJoint_singleton`, private `finiteJoint_eq_withDensity` | Actual `Kernel` and `Measure.compProd`; singleton law and density identity proved |
| Joint KL finiteness | `finiteConditionalKL_ne_top` | Absolute continuity from actual with-density equality; integrability from finite space |
| Exact shared-history averaging | `finiteConditionalKL_toReal` | Actual RN integral grouped through actual composition product; all finite histories included |
| Source endpoints and zero history weights | Types `p h : Icc 0 1`; density proof never cancels `mu {h}` | Both endpoint and zero-weight cases remain in the theorem |
| Uniform one-step bound | `finiteConditionalKL_le` | Actual ENNReal KL bounded by the probability-weighted pointwise bounds |
| Chain-rule accumulation | `finiteConditionalKL_accumulate` | Mathlib exact composition-product chain rule on actual joint laws |
| Actual pushforward laws | private `map_decision_eq_bernoulliBool` | Equality proved from true and false singleton masses |
| Actual KL data processing | `measurableDecision_testing_error` | Direct use of `InformationTheory.klDiv_map_le` |
| Binary testing consequence | `measurableDecision_testing_error` | Exact `P(false)+Q(true)` orientation and `3/8` constant |

## Verification

The fresh module build was:

```text
$ cd formal
$ ~/.elan/bin/lake build EstimatorIntegrity.FiniteConditionalInformation
✔ [3511/3511] Built EstimatorIntegrity.FiniteConditionalInformation (57s)
Build completed successfully (3511 jobs).
```

The source scan found no occurrence of `sorry`, `admit`, `axiom`, or
`opaque`. The axiom harness prints every authored public declaration:

```text
bernoulliKernel
bernoulliKernel_isMarkovKernel
bernoulliKernel_apply
finiteJoint_singleton
finiteConditionalKL_ne_top
finiteConditionalKL_toReal
finiteConditionalKL_le
finiteConditionalKL_accumulate
decisionTrueParameter
measurableDecision_testing_error
```

Every declaration depends only on Mathlib's standard
`[propext, Classical.choice, Quot.sound]`. There is no additional project
assumption or unproved proof obligation. The exact axiom-harness source hash
is `3bcce0c3a0b5132f3c96da9b295e5358fce9f7bf5c66ed7643bf1a8a782f8e8e`;
the axiom output hash is
`39513032c02d390c2f144d696ff99df59989c9d2c5973c959d8bef09bbb4ae0b`.
The fresh-build log hash is
`319f930241d2260931f16e21055c802a584c1b08f653e6e3b8be13bfa21d6015`.

All 342 paths in `initial-source-hashes.json` were present and matched their
protected hashes. No entrypoint, lakefile, toolchain file, accepted source,
frozen ledger, proof, review, or numerical artifact was edited. Four failed
development attempts and their fixes are preserved under
`lean/finite-conditional-information/`.

## Boundary

No numerical call or experiment was run. This gate does not prove a uniform
layer law, adaptive fresh-cell exchangeability, transcript padding, common
private-seed simulation, an n-step urn construction, conditional parameter
arithmetic for that construction, random-stop coupling, an MSE-to-label
argument, the full D28 lower theorem, a PDE phase construction, or the D29
upper theorem. It makes no originality claim.
