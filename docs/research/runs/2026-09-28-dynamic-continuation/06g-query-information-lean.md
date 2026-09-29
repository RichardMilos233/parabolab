# T42: query-information lower bound Lean gate

Date: 2026-09-28. Status: **pass for the fixed probability-space integral target and its exact three-quarters corollary**.

The theory prerequisite is the conventional query lower bound in `04o-unstable-phase-query-lower-bound.md`, independently passed by T40 and T41. The fixed formal contract is `05g-query-lower-bound-lean-contract.md`. This task added no numerical code and did not import the independently assigned T43 oracle-transcript module.

## Exact formal scope

The primary theorem is `EstimatorIntegrity.queryInformation_integral_lower_bound` in `formal/EstimatorIntegrity/QueryInformationLowerBound.lean`. It quantifies over:

- an arbitrary type `Ω` with a measurable space;
- an arbitrary measure `μ : Measure Ω` carrying `IsProbabilityMeasure μ`;
- an arbitrary finite index type `I`;
- `hit : Ω → Finset I`, `Q : Ω → ℝ`, output families `Hplus Hminus : I → Ω → ℝ`, and deterministic target arrays `a b : I → ℝ`;
- real parameters `γ > 0` and `εSq ≥ 0`.

Its exact substantive hypotheses are:

```text
Integrable Q μ
card (hit ω) ≤ Q ω                                  for every ω
2*γ ≤ a i - b i                                    for every i
i ∉ hit ω → Hplus i ω = Hminus i ω                for every ω,i
Integrable (fun ω => (Hplus i ω - a i)^2) μ         for every i
Integrable (fun ω => (Hminus i ω - b i)^2) μ        for every i
∫ (Hplus i - a i)^2 dμ ≤ εSq                        for every i
∫ (Hminus i - b i)^2 dμ ≤ εSq                       for every i.
```

From these hypotheses it derives, rather than assumes,

```text
(card I : ℝ) * (1 - εSq / γ^2) ≤ ∫ ω, Q ω ∂μ.
```

This is an actual Bochner/Lebesgue integral theorem on an arbitrary probability space. It is not a finite-probability-space specialization and does not assume an expected coverage inequality. The only expected-loss premises are the integrability and integral bounds for the actual squared-loss functions specified by the contract.

The hit map has deliberately **no measurability hypothesis**. It is used only in a pointwise finite-sum inequality and is eliminated before integration; no hit indicator or hit-event probability is integrated. `Q` and every squared loss that is integrated retain explicit integrability hypotheses. A usual measurable algorithm supplies more structure, but that extra structure is unnecessary for this abstract inequality.

No bounded-output or unbiasedness premise occurs. The output functions may be arbitrary real-valued functions subject only to the stated squared-loss integrability and bounds.

## Checked declarations and proof structure

The source SHA-256 is `82422e2894fa5febb586cc6fbb23e73ae3a843d5cd84310c7be3fff38d967483`.

1. `pairedSquare_lower_bound` proves for a common real output `y` and targets separated by at least `2γ` that

   ```text
   2*γ^2 ≤ (y-a)^2 + (y-b)^2.
   ```

   The proof uses the exact paired-square identity through nonnegativity of `(2*y-a-b)^2` and the squared target separation.

2. `queryInformation_pointwise` proves for every `ω`

   ```text
   2*γ^2 * (card I - Q ω)
     ≤ Σ i, [(Hplus i ω-a i)^2 + (Hminus i ω-b i)^2].
   ```

   It first sums the paired lower bound over the finite complement of `hit ω`. Losses on hit indices are retained only through their nonnegativity. `Finset.card_compl` converts the complement count to `card I - card(hit ω)`, and the pointwise budget `card(hit ω) ≤ Q ω` gives the displayed inequality.

3. `queryInformation_integral_lower_bound` constructs the actual finite family of paired squared-loss functions, proves its integrability from the per-loss hypotheses, and applies `integral_mono` to the pointwise result. Probability normalization evaluates the integral of the cardinality constant. `integral_finsetSum` exchanges the finite sum and integral, and the two per-index MSE bounds give

   ```text
   ∫ Σ i pairedLoss i ≤ (card I) * (2*εSq).
   ```

   Division by the strictly positive `γ^2` then yields the required expected-query lower bound.

4. `queryInformation_three_quarters` specializes the primary theorem to

   ```text
   γ = 1/2,  εSq = 1/16,  1 ≤ a i - b i
   ```

   and proves exactly

   ```text
   (3/4 : ℝ) * (card I : ℝ) ≤ ∫ ω, Q ω ∂μ.
   ```

The corollary retains the same arbitrary probability space, finite index type, pointwise coupling/cardinality hypotheses, and actual squared-loss integrability hypotheses.

## Verification

The pinned project was used without changing `lean-toolchain`, `lakefile.lean`, the library entrypoint, or any existing module. The resolved environment was:

```text
Lean 4.33.0, commit d8b18978322de05a8f3dba51ef03cf5461676c17
Lake 5.0.0-src+d8b1897
Mathlib db584cd6d46c92f209a44c0f1c829460d327499d
```

After deleting only the generated build artifacts for this new module, the fresh module build command was

```text
cd formal
~/.elan/bin/lake build +EstimatorIntegrity.QueryInformationLowerBound
```

It exited `0` and reported:

```text
Built EstimatorIntegrity.QueryInformationLowerBound (64s)
Build completed successfully (3177 jobs).
```

The final build log is `lean/query-information/build.log`, SHA-256 `1ff4098781410b0b35f686c52ad4b805a448d0567f3cfbe7ebbf01908dfe4e12`.

`lean/query-information/Axioms.lean` imports the built module and runs `#print axioms` on all four exported declarations. The command exited `0`. Every declaration depends only on:

```text
[propext, Classical.choice, Quot.sound]
```

The axiom-driver source has SHA-256 `873bb484697f070ecc90b7a6c55e862a3436ca9244e3ef6f568120dde8df22e9`; its output `axioms.log` has SHA-256 `ef9f6f6493ef50cbb4018e3804f86120a1e90aed0d14281aa6fb227349511e10`.

A source scan for `sorry`, `admit`, `sorryAx`, or an `axiom` declaration returned the expected no-match exit status `1`. Its empty `source-scan.log` has SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The preserved `attempt-01.log` records the failed first elaboration pass: the local `loss` definition needed unfolding before rewriting the coupled outputs, and the constant integrable function needed explicit measure/type arguments. No hypothesis or conclusion changed. `attempt-02.log` is the first complete successful build. The final clean rebuild and axiom run were then recorded separately.

## Correspondence boundary

This module certifies the finite-information probability-space inequality only. It does not prove that an adaptive algorithm's alternative-oracle outputs couple on no-hit indices or that its visited-index cardinality is bounded by its query count; those genuine evaluator facts are the separately assigned T43 target. It also does not formalize the Allen–Cahn PDE, heat-kernel lower bound, hard bump family, spatial regularity estimates, asymptotic choice of `K`, or the bridge from arbitrary almost-surely halting measurable algorithms to a concrete evaluator.

Accordingly, this green gate does not by itself establish an end-to-end Lean proof of the PDE query lower bound. It supplies the exact integral information inequality that the conventional analytic construction and the T43 transcript theorem are intended to feed.
