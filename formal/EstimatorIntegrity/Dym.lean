import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Tactic

namespace EstimatorIntegrity

noncomputable section

open MeasureTheory Set
open scoped Interval

/-- The singular terminal coefficient in the Dym mechanism. -/
def dymFz0 (α x : ℝ) : ℝ :=
  8 * α ^ 2 / x

/-- Algebraic simplification of the Dym `f_{z₀}` coefficient.

The derivative and real-power identities supplying `C` are outside this
algebraic lemma. -/
theorem dym_fz0_coefficient
    (C α x : ℝ) (hx : x ≠ 0) (hC : C ^ 3 = 9 * α ^ 2) :
    (3 * C ^ 2 * (8 * C / 27)) / x = 8 * α ^ 2 / x := by
  field_simp [hx]
  nlinarith [hC]

/-- The reciprocal is not interval-integrable across the positive endpoint zero. -/
theorem one_div_not_intervalIntegrable {ε : ℝ} (hε : 0 < ε) :
    ¬IntervalIntegrable (fun x : ℝ ↦ 1 / x) volume 0 ε := by
  simpa only [one_div] using
    (show ¬IntervalIntegrable (fun x : ℝ ↦ x⁻¹) volume 0 ε by
      rw [intervalIntegrable_inv_iff]
      simp [hε.ne])

/-- Truncated integrals of `1/x` on `(0, ε)` exceed every real threshold. -/
theorem one_div_intervalIntegral_unbounded {ε : ℝ} (hε : 0 < ε) :
    ∀ M : ℝ, ∃ δ : ℝ, 0 < δ ∧ δ < ε ∧
      M ≤ ∫ x : ℝ in δ..ε, 1 / x := by
  intro M
  let K : ℝ := max M 1
  let δ : ℝ := ε / Real.exp K
  have hK : 0 < K := lt_of_lt_of_le zero_lt_one (le_max_right M 1)
  have hexp : 1 < Real.exp K := Real.one_lt_exp_iff.2 hK
  have hδ : 0 < δ := div_pos hε (Real.exp_pos K)
  have hδε : δ < ε := by
    dsimp [δ]
    apply (div_lt_iff₀ (Real.exp_pos K)).2
    nlinarith [hε, hexp]
  refine ⟨δ, hδ, hδε, ?_⟩
  rw [integral_one_div_of_pos hδ hε]
  have hratio : ε / δ = Real.exp K := by
    dsimp [δ]
    field_simp [hε.ne', Real.exp_ne_zero K]
  rw [hratio, Real.log_exp]
  exact le_max_left M 1

/-- A continuous density positive at zero preserves the reciprocal singularity.

The conclusion is the real improper-integral formulation: on one fixed
positive interval, truncations away from zero exceed every threshold. -/
theorem continuous_density_intervalIntegral_unbounded
    (g : ℝ → ℝ) (hg : Continuous g) (hg0 : 0 < g 0) :
    ∃ ε : ℝ, 0 < ε ∧ ∀ M : ℝ, ∃ δ : ℝ,
      0 < δ ∧ δ < ε ∧ M ≤ ∫ x : ℝ in δ..ε, g x / x := by
  obtain ⟨r, hr, hclose⟩ :=
    (Metric.continuousAt_iff.1 hg.continuousAt) (g 0 / 2) (by linarith)
  let ε : ℝ := r / 2
  have hε : 0 < ε := by dsimp [ε]; linarith
  have hεr : ε < r := by dsimp [ε]; linarith
  have hlocal : ∀ x ∈ Icc 0 ε, g 0 / 2 ≤ g x := by
    intro x hx
    have hdist : dist x 0 < r := by
      rw [Real.dist_eq, sub_zero, abs_of_nonneg hx.1]
      exact hx.2.trans_lt hεr
    have hnear := hclose hdist
    rw [Real.dist_eq] at hnear
    have hlower := (abs_lt.1 hnear).1
    linarith
  refine ⟨ε, hε, fun M ↦ ?_⟩
  have hc : 0 < g 0 / 2 := by linarith
  obtain ⟨δ, hδ, hδε, hM⟩ :=
    one_div_intervalIntegral_unbounded hε (M / (g 0 / 2))
  refine ⟨δ, hδ, hδε, ?_⟩
  have hδle : δ ≤ ε := hδε.le
  have hinv : IntervalIntegrable (fun x : ℝ ↦ 1 / x) volume δ ε := by
    exact intervalIntegral.intervalIntegrable_one_div
      (fun x hx ↦ by
        rw [uIcc_of_le hδle] at hx
        exact (hδ.trans_le hx.1).ne')
      continuous_id.continuousOn
  have hweighted :
      IntervalIntegrable (fun x : ℝ ↦ (g 0 / 2) * (1 / x)) volume δ ε :=
    hinv.const_mul (g 0 / 2)
  have hgdiv : IntervalIntegrable (fun x : ℝ ↦ g x / x) volume δ ε := by
    apply ContinuousOn.intervalIntegrable
    apply hg.continuousOn.div continuous_id.continuousOn
    intro x hx
    rw [uIcc_of_le hδle] at hx
    exact (hδ.trans_le hx.1).ne'
  have hscaled :
      M ≤ (g 0 / 2) * ∫ x : ℝ in δ..ε, 1 / x := by
    calc
      M = (g 0 / 2) * (M / (g 0 / 2)) := by field_simp [hc.ne']
      _ ≤ (g 0 / 2) * ∫ x : ℝ in δ..ε, 1 / x :=
        mul_le_mul_of_nonneg_left hM hc.le
  calc
    M ≤ (g 0 / 2) * ∫ x : ℝ in δ..ε, 1 / x := hscaled
    _ = ∫ x : ℝ in δ..ε, (g 0 / 2) * (1 / x) := by
      rw [intervalIntegral.integral_const_mul]
    _ ≤ ∫ x : ℝ in δ..ε, g x / x := by
      apply intervalIntegral.integral_mono_on hδle hweighted hgdiv
      intro x hx
      have hxpos : 0 < x := hδ.trans_le hx.1
      have hgx : g 0 / 2 ≤ g x := hlocal x ⟨hxpos.le, hx.2⟩
      simpa only [div_eq_mul_inv, one_mul] using
        mul_le_mul_of_nonneg_right hgx (inv_nonneg.2 hxpos.le)

end

end EstimatorIntegrity
