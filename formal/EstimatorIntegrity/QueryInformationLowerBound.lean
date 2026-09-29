import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Tactic

/-!
# Finite-information query lower bound

This module formalizes the finite averaging and probability-space integral
at the core of the paired hard-instance query lower bound.  The hit set is
used only pointwise, so no measurability assumption on it is needed.  Every
function that is actually integrated has an explicit integrability
hypothesis.
-/

open MeasureTheory

namespace EstimatorIntegrity

noncomputable section

/-- A common real output incurs total squared loss at least `2 * γ²` against
two targets separated by at least `2 * γ`. -/
theorem pairedSquare_lower_bound
    (y a b γ : ℝ) (hγ : 0 ≤ γ) (hsep : 2 * γ ≤ a - b) :
    2 * γ ^ 2 ≤ (y - a) ^ 2 + (y - b) ^ 2 := by
  have htwoγ : 0 ≤ 2 * γ := mul_nonneg (by norm_num) hγ
  have hab : 0 ≤ a - b := htwoγ.trans hsep
  have hsquares : (2 * γ) ^ 2 ≤ (a - b) ^ 2 :=
    (sq_le_sq₀ htwoγ hab).2 hsep
  nlinarith [sq_nonneg (2 * y - a - b)]

/-- Pointwise finite-family loss bound.  Hit indices contribute only their
nonnegative squared losses; on every no-hit index the paired outputs agree,
so `pairedSquare_lower_bound` applies. -/
theorem queryInformation_pointwise
    {Ω I : Type*} [Fintype I] [DecidableEq I]
    (hit : Ω → Finset I) (Q : Ω → ℝ)
    (Hplus Hminus : I → Ω → ℝ) (a b : I → ℝ)
    (γ : ℝ) (hγ : 0 ≤ γ)
    (hcard : ∀ ω, ((hit ω).card : ℝ) ≤ Q ω)
    (hsep : ∀ i, 2 * γ ≤ a i - b i)
    (hcouple : ∀ ω i, i ∉ hit ω → Hplus i ω = Hminus i ω) (ω : Ω) :
    2 * γ ^ 2 * ((Fintype.card I : ℝ) - Q ω) ≤
      ∑ i : I, ((Hplus i ω - a i) ^ 2 + (Hminus i ω - b i) ^ 2) := by
  let loss : I → ℝ := fun i =>
    (Hplus i ω - a i) ^ 2 + (Hminus i ω - b i) ^ 2
  have hcomp :
      (∑ i ∈ (hit ω)ᶜ, 2 * γ ^ 2) ≤ ∑ i : I, loss i := by
    calc
      (∑ i ∈ (hit ω)ᶜ, 2 * γ ^ 2) ≤ ∑ i ∈ (hit ω)ᶜ, loss i := by
        apply Finset.sum_le_sum
        intro i hi
        have hnotmem : i ∉ hit ω := by simpa using hi
        simp only [loss]
        rw [show Hminus i ω = Hplus i ω from (hcouple ω i hnotmem).symm]
        exact pairedSquare_lower_bound (Hplus i ω) (a i) (b i) γ hγ (hsep i)
      _ ≤ ∑ i : I, loss i := by
        apply Finset.sum_le_sum_of_subset_of_nonneg (Finset.subset_univ _)
        intro i _ _
        exact add_nonneg (sq_nonneg _) (sq_nonneg _)
  have hcard_nat : (hit ω).card ≤ Fintype.card I := Finset.card_le_univ _
  have hcomp_value :
      (∑ i ∈ (hit ω)ᶜ, 2 * γ ^ 2) =
        2 * γ ^ 2 * ((Fintype.card I : ℝ) - ((hit ω).card : ℝ)) := by
    rw [Finset.sum_const, nsmul_eq_mul, Finset.card_compl, Nat.cast_sub hcard_nat]
    ring
  have hcoverage :
      2 * γ ^ 2 * ((Fintype.card I : ℝ) - Q ω) ≤
        2 * γ ^ 2 * ((Fintype.card I : ℝ) - ((hit ω).card : ℝ)) := by
    apply mul_le_mul_of_nonneg_left
    · linarith [hcard ω]
    · positivity
  rw [hcomp_value] at hcomp
  exact hcoverage.trans hcomp

/-- On an arbitrary probability space, integrable paired losses bounded by
`ε²` force the expected query budget to be at least
`card I * (1 - ε² / γ²)`.  The hit map itself need not be measurable because
it is eliminated by the pointwise inequality before integration. -/
theorem queryInformation_integral_lower_bound
    {Ω I : Type*} [MeasurableSpace Ω] [Fintype I] [DecidableEq I]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (hit : Ω → Finset I) (Q : Ω → ℝ)
    (Hplus Hminus : I → Ω → ℝ) (a b : I → ℝ)
    (γ εSq : ℝ) (hγ : 0 < γ) (_hεSq : 0 ≤ εSq)
    (hQ : Integrable Q μ)
    (hcard : ∀ ω, ((hit ω).card : ℝ) ≤ Q ω)
    (hsep : ∀ i, 2 * γ ≤ a i - b i)
    (hcouple : ∀ ω i, i ∉ hit ω → Hplus i ω = Hminus i ω)
    (hplus_int : ∀ i, Integrable (fun ω => (Hplus i ω - a i) ^ 2) μ)
    (hminus_int : ∀ i, Integrable (fun ω => (Hminus i ω - b i) ^ 2) μ)
    (hplus_bound : ∀ i, (∫ ω, (Hplus i ω - a i) ^ 2 ∂μ) ≤ εSq)
    (hminus_bound : ∀ i, (∫ ω, (Hminus i ω - b i) ^ 2 ∂μ) ≤ εSq) :
    (Fintype.card I : ℝ) * (1 - εSq / γ ^ 2) ≤ ∫ ω, Q ω ∂μ := by
  let loss : I → Ω → ℝ := fun i ω =>
    (Hplus i ω - a i) ^ 2 + (Hminus i ω - b i) ^ 2
  have hloss_int : ∀ i, Integrable (loss i) μ := by
    intro i
    exact (hplus_int i).add (hminus_int i)
  have hsum_int : Integrable (fun ω => ∑ i : I, loss i ω) μ :=
    integrable_finsetSum Finset.univ (fun i _ => hloss_int i)
  have hleft_int :
      Integrable
        (fun ω => 2 * γ ^ 2 * ((Fintype.card I : ℝ) - Q ω)) μ := by
    exact ((integrable_const (μ := μ) (Fintype.card I : ℝ)).sub hQ).const_mul
      (2 * γ ^ 2)
  have hlower := integral_mono hleft_int hsum_int
    (queryInformation_pointwise hit Q Hplus Hminus a b γ hγ.le hcard hsep hcouple)
  have hleft_value :
      (∫ ω, 2 * γ ^ 2 * ((Fintype.card I : ℝ) - Q ω) ∂μ) =
        2 * γ ^ 2 * ((Fintype.card I : ℝ) - ∫ ω, Q ω ∂μ) := by
    rw [integral_const_mul,
      integral_sub (integrable_const (μ := μ) (Fintype.card I : ℝ)) hQ]
    simp
  have hsum_value :
      (∫ ω, ∑ i : I, loss i ω ∂μ) = ∑ i : I, ∫ ω, loss i ω ∂μ := by
    exact integral_finsetSum Finset.univ (fun i _ => hloss_int i)
  rw [hleft_value, hsum_value] at hlower
  have hloss_upper :
      (∑ i : I, ∫ ω, loss i ω ∂μ) ≤
        (Fintype.card I : ℝ) * (2 * εSq) := by
    calc
      (∑ i : I, ∫ ω, loss i ω ∂μ) ≤ ∑ _i : I, 2 * εSq := by
        apply Finset.sum_le_sum
        intro i _
        rw [integral_add (hplus_int i) (hminus_int i)]
        linarith [hplus_bound i, hminus_bound i]
      _ = (Fintype.card I : ℝ) * (2 * εSq) := by
        simp [nsmul_eq_mul]
  have haggregate :
      2 * γ ^ 2 * ((Fintype.card I : ℝ) - ∫ ω, Q ω ∂μ) ≤
        (Fintype.card I : ℝ) * (2 * εSq) :=
    hlower.trans hloss_upper
  have hγsq : 0 < γ ^ 2 := sq_pos_of_pos hγ
  have hscaled :
      (Fintype.card I : ℝ) - ∫ ω, Q ω ∂μ ≤
        (Fintype.card I : ℝ) * εSq / γ ^ 2 := by
    apply (le_div_iff₀ hγsq).2
    nlinarith
  calc
    (Fintype.card I : ℝ) * (1 - εSq / γ ^ 2) =
        (Fintype.card I : ℝ) - (Fintype.card I : ℝ) * εSq / γ ^ 2 := by ring
    _ ≤ ∫ ω, Q ω ∂μ := by linarith

/-- Exact `γ = 1/2`, `ε² = 1/16` specialization of the integral theorem. -/
theorem queryInformation_three_quarters
    {Ω I : Type*} [MeasurableSpace Ω] [Fintype I] [DecidableEq I]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    (hit : Ω → Finset I) (Q : Ω → ℝ)
    (Hplus Hminus : I → Ω → ℝ) (a b : I → ℝ)
    (hQ : Integrable Q μ)
    (hcard : ∀ ω, ((hit ω).card : ℝ) ≤ Q ω)
    (hsep : ∀ i, (1 : ℝ) ≤ a i - b i)
    (hcouple : ∀ ω i, i ∉ hit ω → Hplus i ω = Hminus i ω)
    (hplus_int : ∀ i, Integrable (fun ω => (Hplus i ω - a i) ^ 2) μ)
    (hminus_int : ∀ i, Integrable (fun ω => (Hminus i ω - b i) ^ 2) μ)
    (hplus_bound : ∀ i, (∫ ω, (Hplus i ω - a i) ^ 2 ∂μ) ≤ (1 / 16 : ℝ))
    (hminus_bound : ∀ i, (∫ ω, (Hminus i ω - b i) ^ 2 ∂μ) ≤ (1 / 16 : ℝ)) :
    (3 / 4 : ℝ) * (Fintype.card I : ℝ) ≤ ∫ ω, Q ω ∂μ := by
  have h := queryInformation_integral_lower_bound μ hit Q Hplus Hminus a b
    (1 / 2 : ℝ) (1 / 16 : ℝ) (by norm_num) (by norm_num) hQ hcard
    (by simpa using hsep) hcouple hplus_int hminus_int hplus_bound hminus_bound
  norm_num at h ⊢
  nlinarith

end

end EstimatorIntegrity
