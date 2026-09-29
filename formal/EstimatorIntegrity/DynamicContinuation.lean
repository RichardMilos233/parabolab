import Mathlib.Tactic

/-!
# Finite algebra for dynamic continuation

This module verifies only the scalar recurrence and exact rational inequalities
used by the dynamic continuation argument.  It does not encode the Jacobi
profile, the parabolic maximum principles, Hilbert-space projection,
conditional expectations, or the local stochastic representation.
-/

namespace EstimatorIntegrity

noncomputable section

/-- The radicand in one continuation step is controlled by the square of the
candidate invariant radius before adding the projection defect. -/
theorem dynamicRadicand_le_square (r t b s : ℝ)
    (hr : 0 ≤ r) (ht : 0 ≤ t) (ht_one : t ≤ 1)
    (hb : 0 ≤ b) (hs : 0 ≤ s) (hr_le : r ≤ b + s) :
    t ^ 2 * r ^ 2 + (1 - t ^ 2) * s ^ 2 ≤ (t * b + s) ^ 2 := by
  have hradius_nonneg : 0 ≤ b + s := add_nonneg hb hs
  have hr_square : r ^ 2 ≤ (b + s) ^ 2 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hr_le) (add_nonneg hr hradius_nonneg)]
  have hscaled : t ^ 2 * r ^ 2 ≤ t ^ 2 * (b + s) ^ 2 :=
    mul_le_mul_of_nonneg_left hr_square (sq_nonneg t)
  have hcross : 0 ≤ 2 * t * (1 - t) * b * s := by
    positivity
  nlinarith

/-- A single RMS update preserves the radius `b + s` when the projection
defect is `(1-t)b` and the forcing variance is `(1-t²)s²`. -/
theorem dynamicRmsStep_invariant (r t b s : ℝ)
    (hr : 0 ≤ r) (ht : 0 ≤ t) (ht_one : t ≤ 1)
    (hb : 0 ≤ b) (hs : 0 ≤ s) (hr_le : r ≤ b + s) :
    Real.sqrt (t ^ 2 * r ^ 2 + (1 - t ^ 2) * s ^ 2) + (1 - t) * b ≤
      b + s := by
  have hradicand := dynamicRadicand_le_square r t b s hr ht ht_one hb hs hr_le
  have htarget_nonneg : 0 ≤ t * b + s := add_nonneg (mul_nonneg ht hb) hs
  have hsqrt : Real.sqrt (t ^ 2 * r ^ 2 + (1 - t ^ 2) * s ^ 2) ≤
      t * b + s := Real.sqrt_le_iff.mpr ⟨htarget_nonneg, hradicand⟩
  nlinarith

/-- Finite induction for the invariant RMS radius.  This is the formal gate
used after the analytic and probabilistic arguments have supplied the scalar
one-step recurrence. -/
theorem finiteDynamicRmsRecurrence (r : ℕ → ℝ) (t b s : ℝ)
    (ht : 0 ≤ t) (ht_one : t ≤ 1) (hb : 0 ≤ b) (hs : 0 ≤ s)
    (hr_nonneg : ∀ j, 0 ≤ r j) (hr_zero : r 0 ≤ b + s)
    (hstep : ∀ j,
      r (j + 1) ≤ Real.sqrt (t ^ 2 * (r j) ^ 2 + (1 - t ^ 2) * s ^ 2) +
        (1 - t) * b) :
    ∀ j, r j ≤ b + s := by
  intro j
  induction j with
  | zero => exact hr_zero
  | succ k ih =>
      exact (hstep k).trans
        (dynamicRmsStep_invariant (r k) t b s (hr_nonneg k) ht ht_one hb hs ih)

/-- The recurrence gate with the contraction, variance, and defect parameters
named explicitly as in the continuation theorem. -/
theorem finiteDynamicRmsRecurrence_of_parameters
    (r : ℕ → ℝ) (q ν β t b s : ℝ)
    (hq : q = t ^ 2) (hν : ν = (1 - t ^ 2) * s ^ 2)
    (hβ : β = (1 - t) * b)
    (ht : 0 ≤ t) (ht_one : t ≤ 1) (hb : 0 ≤ b) (hs : 0 ≤ s)
    (hr_nonneg : ∀ j, 0 ≤ r j) (hr_zero : r 0 ≤ b + s)
    (hstep : ∀ j, r (j + 1) ≤ Real.sqrt (q * (r j) ^ 2 + ν) + β) :
    ∀ j, r j ≤ b + s := by
  subst q
  subst ν
  subst β
  exact finiteDynamicRmsRecurrence r t b s ht ht_one hb hs hr_nonneg hr_zero hstep

/-! ## Exact rational certificates for the two-dimensional interface -/

/-- The contraction exponent `μ = 31/350` times the slab length `h = 2/25`. -/
theorem dynamicMu_mul_step :
    (31 / 350 : ℝ) * (2 / 25) = 31 / 4375 := by
  norm_num

/-- Every feasible affine ratio has derivative envelope strictly below `1/2`. -/
theorem dynamicAffineDerivativeEnvelope :
    (3 / 7 : ℝ) * (1 + 2 * (2 / 21) / 35) < 1 / 2 := by
  norm_num

/-- Squared form of `sqrt(a) * a² / 400 < 1/140000` for `a = 2/21`. -/
theorem dynamicInterpolationDefect_sq :
    (2 / 21 : ℝ) ^ 5 / 160000 < (1 / 140000 : ℝ) ^ 2 := by
  norm_num

/-- Exact rational values used after applying `1 - exp (-x) ≥ x/(1+x)`
at `x = 31/4375` and at `2x`. -/
theorem dynamicDenominatorRationals :
    (31 / 4375 : ℝ) / (1 + 31 / 4375) = 31 / 4406 ∧
      (2 * (31 / 4375 : ℝ)) / (1 + 2 * (31 / 4375)) = 62 / 4437 := by
  norm_num

/-- The exact uniform RMS budget after the rational exponential lower bounds. -/
theorem dynamicFinalRmsBudget :
    (4406 / 4340000 : ℝ) + Real.sqrt (4437 / 12400000) < 1 / 50 := by
  have hresidual : (0 : ℝ) < 41197 / 2170000 := by
    norm_num
  have hsquare : (4437 / 12400000 : ℝ) < (41197 / 2170000) ^ 2 := by
    norm_num
  have hradicand : (0 : ℝ) ≤ 4437 / 12400000 := by
    norm_num
  have hsqrt : Real.sqrt (4437 / 12400000 : ℝ) < 41197 / 2170000 :=
    (Real.sqrt_lt hradicand hresidual.le).mpr hsquare
  nlinarith

end

end EstimatorIntegrity
