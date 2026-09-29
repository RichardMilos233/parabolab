import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

/-!
# Deterministic long-horizon scalar algebra

This module isolates the scalar polynomial and bounded ternary-reaction
identities used by the long-horizon estimator analysis.
-/

namespace EstimatorIntegrity

noncomputable section

/-- Polynomial in the shifted raw flat absolute-moment equation `s' = P(s)`. -/
def longHorizonPolynomial (s : ℝ) : ℝ :=
  3 / 8 + s / 4 + 3 * s ^ 2 / 2 + s ^ 3

/-- The raw scalar field factors into two positive factors on `s ≥ 0`. -/
theorem longHorizonPolynomial_factorization (s : ℝ) :
    longHorizonPolynomial s = (s + 3 / 2) * (s ^ 2 + 1 / 4) := by
  rw [longHorizonPolynomial]
  ring

/-- The raw scalar field is strictly positive on the nonnegative half-line. -/
theorem longHorizonPolynomial_pos {s : ℝ} (hs : 0 ≤ s) :
    0 < longHorizonPolynomial s := by
  rw [longHorizonPolynomial_factorization]
  positivity

/-- The exact conventional explosion-time value for the raw scalar equation. -/
def rawAbsoluteHorizon : ℝ :=
  (3 * Real.pi - 2 * Real.log 3) / 5

/-- The reciprocal partial-fraction identity used in the conventional
improper-integral calculation of `rawAbsoluteHorizon`. -/
theorem longHorizonPolynomial_reciprocal (s : ℝ) (hs : 0 ≤ s) :
    1 / longHorizonPolynomial s =
      (2 / 5) / (s + 3 / 2) + ((-2 / 5) * s + 3 / 5) / (s ^ 2 + 1 / 4) := by
  rw [longHorizonPolynomial_factorization]
  have hleft : s + 3 / 2 ≠ 0 := by positivity
  have hright : s ^ 2 + 1 / 4 ≠ 0 := by positivity
  field_simp [hleft, hright]
  ring

/-- Symmetric ternary reaction associated with a clock rate `r`. -/
def boundedReaction (r a b c : ℝ) : ℝ :=
  ((r + 1) / (3 * r)) * (a + b + c) - a * b * c / r

/-- On the diagonal the rate-scaled reaction recovers `u - u³`. -/
theorem boundedReaction_diagonal (r u : ℝ) (hr : 0 < r) :
    r * (boundedReaction r u u u - u) = u - u ^ 3 := by
  rw [boundedReaction]
  field_simp [ne_of_gt hr]
  ring

/-- The signed corner `(1,1,-1)` forces exactly the clock constraint `r ≥ 2`. -/
theorem boundedReaction_corner_le_one_iff (r : ℝ) (hr : 0 < r) :
    boundedReaction r 1 1 (-1) ≤ 1 ↔ 2 ≤ r := by
  rw [boundedReaction]
  norm_num
  have hden : 0 < 3 * r := by positivity
  have hr0 : r ≠ 0 := ne_of_gt hr
  constructor
  · intro h
    have h' := (div_le_iff₀ hden).mp h
    field_simp [hr0] at h'
    linarith
  · intro h
    apply (div_le_iff₀ hden).2
    field_simp [hr0]
    linarith

/-- At rate two the reaction is the classical symmetric ternary rule. -/
theorem boundedReaction_two (a b c : ℝ) :
    boundedReaction 2 a b c = (a + b + c - a * b * c) / 2 := by
  rw [boundedReaction]
  ring

/-- For nonzero `r`, the general reaction is a mixture of the rate-two rule
and the arithmetic mean. -/
theorem boundedReaction_convex_decomposition
    (r a b c : ℝ) (hr : r ≠ 0) :
    boundedReaction r a b c =
      (2 / r) * boundedReaction 2 a b c +
        (1 - 2 / r) * ((a + b + c) / 3) := by
  rw [boundedReaction_two, boundedReaction]
  field_simp [hr]
  ring

end

end EstimatorIntegrity
