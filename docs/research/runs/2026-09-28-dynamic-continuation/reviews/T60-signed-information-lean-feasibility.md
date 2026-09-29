# T60: Lean feasibility of the signed-information lower bound

Date: 2026-09-28  
Status: **reconnaissance complete; formalization feasible, but the real probability argument is not currently a short corollary of Mathlib**

## 1. Scope and verdict

This review checks the actual Lean/Mathlib support for the probability argument accepted in D25 (`04r`) and audited in T50/T53:

1. sample a sign vector uniformly from one of the two fixed-weight layers;
2. expose at most `n = floor (K / 1024)` distinct queried signs, padding after early stopping;
3. identify the conditional sign law as sampling without replacement;
4. sum conditional Bernoulli KL bounds to obtain transcript KL at most `1/12`;
5. use Pinsker/data processing to obtain testing error at least `3/8`;
6. compare this with the `1/4` error produced by the estimator's MSE bound;
7. remove the cap by Markov truncation and conclude an expected-query lower bound.

The pinned Mathlib has a genuine measure-theoretic Kullback--Leibler divergence, a composition-product chain rule, map/kernel data processing, finite PMFs, uniform finite laws, Bernoulli measures, and Markov's inequality. It does **not** have a without-replacement urn law, a hypergeometric transcript construction, Pinsker's inequality, a probability total-variation distance, a PMF-level KL formula, or the expected-conditional-KL form of the chain rule needed to sum the one-step bounds. The last omission is an explicit TODO in Mathlib's `KullbackLeibler/ChainRule.lean`.

Therefore the D25 probability proof is formalizable in this project, but it needs new probability infrastructure. A contract that merely assumes `KL <= 1/12` would certify only the numerical tail of the proof and would omit its main mathematical content. The first sound implementation target should include the actual two uniform layers, the adaptive/padded without-replacement law, and the KL accumulation.

No Lean theorem, executable code, numerical experiment, or run artifact was created for T60.

## 2. Pinned environment inspected

- Lean: `4.33.0`, commit `d8b18978322de05a8f3dba51ef03cf5461676c17`
- Lake: `5.0.0-src+d8b1897`
- Mathlib manifest version: `v4.33.0`
- Mathlib checkout: `db584cd6d46c92f209a44c0f1c829460d327499d`
- project `lean-toolchain` SHA-256: `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b`
- project `lake-manifest.json` SHA-256: `bf1a0d7201280250cb6d2fa67302ae2ddd9efd923f524e36a2dfb51692dcb089`

The mathematical sources inspected were:

- `04r-signed-many-bump-complexity.md`, SHA-256 `4bdcb75b7ee62c40879a80cb84b0949f1a9e796d387775e5760cab04a33fa419`
- `T50-signed-many-bump-lower-bound.md`, SHA-256 `45e56dc4c5bb656cc3f3407f4e7627e772e13b013a8ca9837ffebe8f79806151`
- `T53-signed-many-bump-independent-audit.md`, SHA-256 `0c09832487dd497422e8078fadd8814957da85f1bd452d333b475a4757f11cb4`

## 3. Exact usable Mathlib API

### 3.1 Finite probability laws

The following declarations are available.

| Import | Declaration | Use here |
|---|---|---|
| `Mathlib.Probability.ProbabilityMassFunction.Basic` | `PMF.toMeasure`, `PMF.toMeasure_apply`, `PMF.toMeasure_apply_singleton`, `PMF.toMeasure_apply_finset`, `PMF.toMeasure_apply_fintype`, `PMF.toMeasure_injective`, `PMF.toMeasure_inj` | Move between a finite PMF and a probability measure. |
| `Mathlib.Probability.ProbabilityMassFunction.Constructions` | `PMF.map`, `PMF.map_apply`, `PMF.ofFinset`, `PMF.ofFinset_apply`, `PMF.ofFintype`, `PMF.ofFintype_apply` | Define explicit finite laws and deterministic pushforwards. |
| `Mathlib.Probability.ProbabilityMassFunction.Monad` | `PMF.bind`, `PMF.bind_apply`, `PMF.bind_bind`, `PMF.toMeasure_bind_apply` | Define the recursively sampled sign sequence. |
| `Mathlib.Probability.ProbabilityMassFunction.Integrals` | `PMF.integral_eq_tsum`, `PMF.integral_eq_sum` | Turn expectations on finite transcript spaces into sums. |
| `Mathlib.Probability.Distributions.Uniform` | `PMF.uniformOfFinset`, `PMF.uniformOfFinset_apply`, `PMF.uniformOfFinset_apply_of_mem`, `PMF.toMeasure_uniformOfFinset_apply`, `PMF.uniformOfFintype` | Put the actual uniform prior on a fixed-weight layer. |
| `Mathlib.Probability.Distributions.Bernoulli` | `ProbabilityTheory.bernoulliMeasure`, notation `Ber(x, y, p)`, `bernoulliMeasure_apply`, its four membership specializations, `map_bernoulliMeasure`, `integral_bernoulliMeasure` | Express each conditional next-sign law as an actual Bernoulli measure. |

`PMF.bernoulli` still exists, but is deprecated in favor of `ProbabilityTheory.bernoulliMeasure` in this pinned version. For a recursive PMF construction, `PMF.ofFintype` on `Bool` is stable and avoids relying on the deprecated name.

`PMF.toMeasure_bind_apply` states

```text
(p.bind f).toMeasure s = sum' a, p a * (f a).toMeasure s
```

for measurable `s`. There is no located packaged equality identifying PMF bind with composition by a Markov kernel, but that equality can be proved locally by measure extensionality.

### 3.2 Fixed-weight layers and counting

`Mathlib.Data.Finset.Powerset` provides

```text
Finset.mem_powersetCard
Finset.card_powersetCard (n : Nat) (s : Finset alpha) :
  (s.powersetCard n).card = Nat.choose s.card n
Finset.powersetCard_nonempty
```

Thus a sign vector can be represented by the `Finset (Fin K)` of positive cells, and the layer with exactly `m` positives can be the finite set `(Finset.univ : Finset (Fin K)).powersetCard m`. This avoids counting Boolean functions directly. `Nat.choose_succ_right_eq`, `Nat.choose_mul_succ_eq`, and the standard `Nat.choose` identities are present for the elementary ratio calculations.

A source scan found no probability distribution or theorem named for hypergeometric sampling, an urn, or sampling without replacement. The conditional-count calculation and the exchangeability theorem are project obligations.

### 3.3 Markov kernels and finite histories

The kernel layer supplies:

| Import | Declaration | Use here |
|---|---|---|
| `Mathlib.Probability.Kernel.Basic` | `Kernel.deterministic`, `Kernel.const`, `Kernel.ofFunOfCountable`, `Kernel.boolKernel` | Deterministic transcript maps, common private randomness, and a finite-history transition kernel. |
| `Mathlib.Probability.Kernel.Composition.MeasureCompProd` | measure/kernel composition product `mu tensor_m kappa` and its probability instances | Build one transcript step from a history law and a conditional answer kernel. |

`Kernel.ofFunOfCountable` has the exact shape needed for finite histories:

```text
def Kernel.ofFunOfCountable
    [MeasurableSpace alpha] [Countable alpha] [MeasurableSingletonClass alpha]
    (f : alpha -> Measure beta) : Kernel alpha beta
```

Finite domains also have `measurable_of_finite`, so measurability of functions between the finite history, sign, and decision types should be routine once those types use measurable singletons.

### 3.4 Kullback--Leibler divergence

The current KL implementation is real and usable; it is not a placeholder.

`Mathlib.InformationTheory.KullbackLeibler.Basic` provides:

```text
InformationTheory.klDiv (mu nu : Measure alpha) : ENNReal
klDiv_of_ac_of_integrable
klDiv_of_not_ac
klDiv_of_not_integrable
klDiv_self
klDiv_ne_top_iff
klDiv_eq_lintegral_klFun_of_ac
toReal_klDiv_of_measure_eq
toReal_klDiv_eq_integral_klFun
klDiv_eq_zero_iff
```

It also provides the convex integrand

```text
InformationTheory.klFun x = x * Real.log x + 1 - x
convexOn_klFun
klFun_nonneg
klFun_eq_zero_iff
```

and general Gibbs-type inequalities such as `mul_klFun_le_toReal_klDiv`, `mul_log_le_toReal_klDiv`, and `mul_log_le_klDiv`. These do not specialize KL to a finite sum or to Bernoulli measures.

`Mathlib.InformationTheory.KullbackLeibler.ChainRule` provides the exact declarations

```text
klDiv_compProd_left :
  klDiv (mu tensor_m kappa) (nu tensor_m kappa) = klDiv mu nu

klDiv_compProd_eq_add :
  klDiv (mu tensor_m kappa) (nu tensor_m eta) =
    klDiv mu nu + klDiv (mu tensor_m kappa) (mu tensor_m eta)
```

for finite base measures and Markov kernels. The source explicitly lists as a TODO the more familiar conditional form

```text
mu[fun x => klDiv (kappa x) (eta x)]
```

That missing form matters here: a pointwise bound on each conditional Bernoulli KL cannot be fed directly into `klDiv_compProd_eq_add`. One still has to prove that the second joint KL term is the finite-history average of the conditional KLs, or at least is bounded by the uniform one-step bound.

`Mathlib.InformationTheory.KullbackLeibler.DataProcessing` provides:

```text
klDiv_map_le
klDiv_trim_le
klDiv_comp_right_le
```

`klDiv_map_le` is enough to project a padded observation sequence to a deterministic decision. `klDiv_comp_right_le` is enough to discard a common randomized postprocessing kernel, including the algorithm's private seed and transcript reconstruction, once the project proves that both hypotheses use the same kernel from padded signs to the observable transcript.

### 3.5 Bernoulli KL algebra

No declaration specializing `klDiv` to `bernoulliMeasure` or a PMF was found. The basic scalar tool needed for the upper bound is available:

```text
Real.log_le_sub_one_of_pos : 0 < x -> Real.log x <= x - 1
```

This supports the standard proof

```text
KL(Ber(p) || Ber(q)) <= (p - q)^2 / (q * (1 - q))
```

under `0 < q < 1`, but the Bernoulli KL formula itself, all endpoint bookkeeping, and the bridge to `InformationTheory.klDiv` are new work.

### 3.6 Pinsker, total variation, and testing

An exhaustive name/content scan of the pinned `Mathlib/**/*.lean` found:

- no Pinsker theorem;
- no Hellinger probability divergence (the only Hellinger hits are the unrelated Hellinger--Toeplitz theorem);
- no probability total-variation-distance definition;
- no theorem in `Mathlib.Probability.Decision` connecting KL or total variation to binary testing error.

`MeasureTheory.SignedMeasure.totalVariation` exists, with `SignedMeasure.norm_le_totalVariation`, but it is the variation measure of a signed measure. Mathlib does not package the probability distance `sup_A |mu A - nu A|` or connect that construction to KL. Routing the D25 proof through signed-measure total variation would therefore add a separate bridge and does not avoid proving Pinsker.

For this project, the smallest useful missing theorem is an event form of Pinsker for probability measures,

```text
abs (mu.real A - nu.real A) <= Real.sqrt ((klDiv mu nu).toReal / 2)
```

under the appropriate measurability and finiteness hypotheses. A still smaller finite target is the same statement for a decision map into `Bool`. Either is sufficient for the `KL <= 1/12` to error `>= 3/8` step. The finite-Bool version avoids defining a global total-variation distance, but it remains a genuine Pinsker proof, not numerical algebra.

### 3.7 Markov truncation and expectations

`Mathlib.MeasureTheory.Integral.Lebesgue.Markov` provides:

```text
mul_meas_ge_le_lintegral₀
mul_meas_ge_le_lintegral
meas_ge_le_lintegral_div
```

for nonnegative `ENNReal` functions. The real-valued Bochner form is

```text
MeasureTheory.mul_meas_ge_le_integral_of_nonneg
```

with statement

```text
epsilon * mu.real {x | epsilon <= f x} <= integral f mu.
```

Together with `PMF.integral_eq_sum`, these declarations are enough for

```text
P(Q > n) <= E[Q] / n
```

after choosing a real- or `ENNReal`-valued version of the natural query count and proving its measurability/integrability. The probability union bound, complements, and real probability identities are also present (`measure_union_le`, `probReal_add_probReal_compl`, `probReal_compl_eq_one_sub`). Markov's inequality itself is not a dependency gap.

## 4. Concrete dependency-gap map

| ID | Required link in D25 | Available support | Missing project theorem/infrastructure | Risk |
|---|---|---|---|---|
| G1 | Uniform `+r` and `-r` sign layers | `Finset.powersetCard`, `card_powersetCard`, `PMF.uniformOfFinset` | Define the two layer types/laws and prove equal cardinality/nonemptiness under the arithmetic hypotheses on `K,r`. | Low--medium |
| G2 | A fresh adaptive query has the without-replacement conditional law | Finset counting and uniform finite PMFs | Prove exchangeability after an arbitrary distinct queried-index history, including feasibility of the history and the exact remaining-positive count. No urn/hypergeometric API exists. | **High** |
| G3 | Cache repeated cell queries and pad an early stop to exactly `n` distinct signs | `PMF.bind`, finite kernels, existing deterministic `EstimatorIntegrity.runOracle` | Define the cached cell-level experiment and prove its padded answer law. Existing `OracleTranscript.lean` records point queries but has no cache, random seed, sign layer, padding, or distributional theorem. | **High** |
| G4 | Convert the adaptive transcript into a common function/kernel of seed plus padded signs | `Kernel.deterministic`, `Kernel.ofFunOfCountable`, `klDiv_comp_right_le` | A simulation/factorization theorem showing locations, stopping, and label are the same postprocessing under both layer hypotheses. This is the formal version of the key T53 argument. | **High** |
| G5 | Compute and bound one-step Bernoulli KL | general `klDiv`, `bernoulliMeasure`, `Real.log_le_sub_one_of_pos` | Prove a Bernoulli KL formula and `KL <= (p-q)^2/(q(1-q))`, then discharge `q in [1/4,3/4]` and `p-q <= 2r/K`. | Medium--high |
| G6 | Sum the conditional KLs | `klDiv_compProd_eq_add` | Prove a finite/countable conditional-KL sum or upper-bound lemma. Mathlib's source explicitly marks the integral conditional form as TODO. Iteration alone does not remove this gap. | **High** |
| G7 | `KL <= 1/12` implies transcript/decision separation at most `1/sqrt(24)` | `klDiv_map_le`; real square-root arithmetic | Prove event/Bool Pinsker. No Pinsker, Hellinger alternative, or probability-TV distance exists in the pinned library. | **High** |
| G8 | Equal-prior test error is at least `(1-TV)/2`, hence at least `3/8` | probability complement identities | Define the two error events and prove the elementary binary testing identity/inequality. If G7 is stated directly for a Bool decision, this is small. | Low--medium after G7 |
| G9 | MSE at most the threshold gives sign error at most `1/4` | Markov/Chebyshev primitives and integral inequalities | Instantiate the actual estimator, target separation, and mixture prior. This is straightforward only after the random experiment is represented by a measure. | Medium |
| G10 | Uncap via `P(Q>n) <= qbar/n` and transfer labels outside that event | Markov inequality is present | Define the original and truncated random executions on a common space; prove their decisions agree on `{Q <= n}`; prove query-count measurability/integrability; combine the two hypothesis priors. | **High** |
| G11 | Pass from prior-average expected cost to one hard sign vector | finite sums/averages | Expand the uniform finite prior and extract a member at least as large as its average. | Low |

The mathematical bottleneck is the chain `G2 -> G3 -> G4 -> G6`. Pinsker (`G7`) is an independent substantial lemma. Markov truncation is library-supported analytically, but the execution coupling in `G10` is not.

## 5. Recommended formal architecture

The most direct route keeps the actual finite experiment visible and uses the existing measure KL only where it helps.

### Stage A: finite layers and canonical urn sequence

Represent a sign assignment by its positive-cell set `P : Finset (Fin K)`. Define each layer as `univ.powersetCard m`, with `m = (K +/- r)/2`, and put `PMF.uniformOfFinset` on that finite layer.

Define a length-`n` Boolean history law recursively. At history `h`, the next-positive probability is

```text
(m - countTrue h) / (K - length h).
```

Use `PMF.bind` or `Kernel.ofFunOfCountable` to extend the history. Prove that revealing distinct coordinates of a uniform layer, even when each next coordinate is chosen from the previous answers and a fixed seed, has this law. The proof should count extensions of the observed partial assignment using `Finset.card_powersetCard`; it should not postulate exchangeability as a hypothesis.

### Stage B: finite conditional KL support

Prove the following reusable finite lemmas against the actual `InformationTheory.klDiv`:

1. KL of two strictly interior Bernoulli measures has the standard two-term logarithmic formula.
2. The Bernoulli upper bound from `Real.log_le_sub_one_of_pos`.
3. For a probability measure on a finite history type and two finite-history Markov kernels, the second term in `klDiv_compProd_eq_add` is the finite weighted sum of the conditional KLs, or at least is bounded by a common pointwise bound.

The third lemma is the local finite-space replacement for Mathlib's missing conditional-KL TODO. It is preferable to introducing a second unrelated `discreteKL` unless that definition is also proved equal to `InformationTheory.klDiv`; otherwise later data processing would require a second bridge.

Iterate the chain rule for the canonical urn sequence. The common initial private-seed law contributes zero by `klDiv_self`/`klDiv_compProd_left`. The accepted arithmetic then yields the actual sequence KL bound `<= 1/12`.

### Stage C: adaptive transcript and testing

Formalize the cached, capped algorithm as a common deterministic map or Markov kernel from `(seed, paddedSigns)` to the observable transcript and decision. Prove the factorization under each layer. Then apply `klDiv_map_le` or `klDiv_comp_right_le` to transfer the urn-sequence bound to the decision.

Prove a Bool/event Pinsker lemma and derive the equal-prior lower bound on decision error. This avoids building a broad total-variation API while preserving the real logical content of Pinsker.

### Stage D: random stopping

Only after the capped experiment is complete, define the uncapped execution, its natural query count `Q`, and the execution truncated before the `(n+1)`st distinct cell. Prove equality of the two decisions on `{Q <= n}`. Apply `mul_meas_ge_le_integral_of_nonneg` or `meas_ge_le_lintegral_div` to `{n < Q}` and finish the `3/8 <= 1/4 + qbar/n` algebra.

This stage needs an explicit measurable randomized-algorithm model. The existing fuel-bounded `runOracle` theorem is useful deterministic infrastructure, but its own module correctly states that it does not encode measurability, almost-sure halting, a uniform query bound, or a bridge from arbitrary randomized algorithms.

## 6. Contract requirements for a later implementation task

A full probability contract should require all of the following outputs, rather than taking them as assumptions:

- actual uniform measures on the two fixed-weight sign layers;
- an actual capped/padded finite observation law;
- a theorem identifying its conditional next-sign probabilities under both layers;
- a theorem that adaptive locations, stopping, private seed, and final label are common postprocessing of the padded signs;
- a derived KL bound `<= 1/12` from the Bernoulli bounds and chain rule;
- a proved event/Bool Pinsker inequality and the resulting `>= 3/8` capped testing error;
- an actual measurable query-count random variable, a truncated execution, Markov's inequality, and decision agreement on `{Q <= n}`;
- finite-prior averaging to select one expensive sign vector.

It is reasonable to split these into several Lean modules and gates. It is not reasonable to call the D25 information argument formalized if the public theorem assumes the urn law, the transcript KL bound, Pinsker, or the stopping-transfer inequality.

## 7. Boundaries

This reconnaissance does not certify the PDE construction, interpolation, bump geometry, endpoint separation, or estimator-to-sign-test bridge outside the probability statements listed above. It does not change the accepted constants in `04r`, and it makes no novelty claim. It also does not claim a Lean PASS: the result is an API and dependency audit for choosing the next mathematical contract.

## 8. Reproducibility: inspected Mathlib source hashes

```text
d705844b91de690829825ff1ef8fb3f219af0d669d4ada2f97c1af015100c442  InformationTheory/KullbackLeibler/Basic.lean
7cfbfc972c134864031de87e3b5157be2d7af83e375a2c0e1cc9ff7db598678d  InformationTheory/KullbackLeibler/ChainRule.lean
c0b0fc678820191e0f3966fde601f0ff69a7d24fd7725586cfe29a66ff31cb0e  InformationTheory/KullbackLeibler/DataProcessing.lean
4ef376c0ae18ac15664d1d0a77c075f838bc0d65556ac3bc7e462d651fdae197  Probability/ProbabilityMassFunction/Basic.lean
09a7cf241524c158d4174e994e04140901630c7e0629ceee9b7ba7ec347d2cd4  Probability/ProbabilityMassFunction/Constructions.lean
94937919a3ff69070aae22a8c2741e1369e105a197c4c7bc0972ad32cd5523e6  Probability/ProbabilityMassFunction/Monad.lean
174951d99036d6995b4ac6d486de807bedb58f340aa902f02502a7216515bf63  Probability/ProbabilityMassFunction/Integrals.lean
c3492e1ba311263248302cf310f45e44d49524cfbba52d8fc27207be80a50ab9  Probability/Distributions/Uniform.lean
ecd81dad8dfd4875561c7438430ee157f8a345bdc33b637ba04cf1dd1fa02738  Probability/Distributions/Bernoulli.lean
fbdfa336f46afc20e003369788014cba91272257b4a5b5ccebc71561d051c06c  MeasureTheory/Integral/Lebesgue/Markov.lean
ffe38ab68a55fd3c24524e502afab8dad28588fb899157deae3976f24ff16b27  Data/Finset/Powerset.lean
```
