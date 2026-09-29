import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity

/-!
# Finite-time Riccati obstruction

This module proves the deterministic ODE barrier used by the absolute-moment
obstruction argument.  It does not formalize the heat-semigroup lower bound,
tree likelihood cancellation, moment comparison, or derivative-code chain.
-/

namespace EstimatorIntegrity

/-- A solution of the scaled Riccati equation on a closed nonnegative time
interval cannot reach a time with `a * b * T ≥ π/2`. -/
theorem scaledRiccati_time_lt_pi_div_two
    (T a b : ℝ) (z : ℝ → ℝ)
    (hT : 0 ≤ T) (ha : 0 < a) (hb : 0 < b)
    (hz_zero : z 0 = 0)
    (hz : ∀ t ∈ Set.Icc (0 : ℝ) T,
      HasDerivAt z (a * (1 + (b * z t) ^ 2)) t) :
    a * b * T < Real.pi / 2 := by
  have hF_deriv : ∀ t ∈ Set.Icc (0 : ℝ) T,
      HasDerivAt (fun x => Real.arctan (b * z x)) (a * b) t := by
    intro t ht
    have hzt := hz t ht
    have hinner : HasDerivAt (fun x => b * z x)
        (b * (a * (1 + (b * z t) ^ 2))) t := hzt.const_mul b
    have hdenom : 1 + (b * z t) ^ 2 ≠ 0 := by
      positivity
    have hF_at := hinner.arctan
    have hcoeff : 1 / (1 + (b * z t) ^ 2) *
        (b * (a * (1 + (b * z t) ^ 2))) = a * b := by
      field_simp [hdenom]
    rw [hcoeff] at hF_at
    exact hF_at
  have hlinear_deriv : ∀ t ∈ Set.Ico (0 : ℝ) T,
      HasDerivWithinAt (fun x => a * b * x) (a * b) (Set.Ici t) t := by
    intro t ht
    simpa using ((hasDerivAt_id t).const_mul (a * b)).hasDerivWithinAt
  have hF_cont : ContinuousOn (fun x => Real.arctan (b * z x))
      (Set.Icc (0 : ℝ) T) := HasDerivAt.continuousOn hF_deriv
  have hlinear_cont : ContinuousOn (fun x : ℝ => a * b * x)
      (Set.Icc (0 : ℝ) T) := (continuous_const.mul continuous_id).continuousOn
  have hinitial : Real.arctan (b * z 0) = a * b * 0 := by
    simp [hz_zero]
  have hidentity : ∀ y ∈ Set.Icc (0 : ℝ) T,
      Real.arctan (b * z y) = a * b * y :=
    eq_of_has_deriv_right_eq
      (fun t ht => (hF_deriv t (Set.mem_Icc_of_Ico ht)).hasDerivWithinAt)
      hlinear_deriv hF_cont hlinear_cont hinitial
  have hT_mem : T ∈ Set.Icc (0 : ℝ) T := ⟨hT, le_rfl⟩
  have hendpoint := hidentity T hT_mem
  rw [← hendpoint]
  exact Real.arctan_lt_pi_div_two _

/-- Normalized finite-time barrier for `z' = 1 + z²`, obtained from the
scaled theorem with `a = b = 1`. -/
theorem riccati_time_lt_pi_div_two
    (T : ℝ) (z : ℝ → ℝ) (hT : 0 ≤ T) (hz_zero : z 0 = 0)
    (hz : ∀ t ∈ Set.Icc (0 : ℝ) T, HasDerivAt z (1 + (z t) ^ 2) t) :
    T < Real.pi / 2 := by
  simpa using scaledRiccati_time_lt_pi_div_two T 1 1 z hT zero_lt_one zero_lt_one
    hz_zero (fun t ht => by simpa using hz t ht)

end EstimatorIntegrity
