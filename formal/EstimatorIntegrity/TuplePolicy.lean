import EstimatorIntegrity.MomentIteration

namespace EstimatorIntegrity

/-!
# Certified tuple-policy inequalities

This file records finite algebraic and order-theoretic consequences of a
certified tuple-policy update. It makes no stochastic or asymptotic claims.
-/

/-- A certified binary allocation with `q ≥ 1 / 2` has objective at most
twice the unweighted total. -/
theorem binary_policy_improvement
    (A B q : ℝ)
    (hA : 0 ≤ A)
    (hB : 0 ≤ B)
    (hqhalf : (1 : ℝ) / 2 ≤ q)
    (hqone : q < 1)
    (hcertificate : q * (A + B) ≤ A) :
    A / q + B / (1 - q) ≤ 2 * (A + B) := by
  have hqpos : 0 < q := by linarith
  have hqcomp : 0 < 1 - q := by linarith
  have hidentity :
      (A / q + B / (1 - q) - 2 * (A + B)) * q * (1 - q) =
        (2 * q - 1) * ((A + B) * q - A) := by
    field_simp [hqpos.ne', hqcomp.ne']
    ring
  have hfactor : 0 ≤ 2 * q - 1 := by linarith
  have hgap : (A + B) * q - A ≤ 0 := by nlinarith [hcertificate]
  have hproduct : (2 * q - 1) * ((A + B) * q - A) ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos hfactor hgap
  have hscale : 0 < q * (1 - q) := mul_pos hqpos hqcomp
  have hsum_nonneg : 0 ≤ A + B := add_nonneg hA hB
  nlinarith [hidentity, hproduct, hscale, hsum_nonneg]

/-- The exact `q = 2 / 3` allocation is certified when the first contribution
dominates twice the second. -/
theorem two_thirds_policy_improvement
    (A B : ℝ)
    (hA : 0 ≤ A)
    (hB : 0 ≤ B)
    (hdominates : 2 * B ≤ A) :
    A / ((2 : ℝ) / 3) + B / (1 - (2 : ℝ) / 3) ≤ 2 * (A + B) := by
  have hcertificate : ((2 : ℝ) / 3) * (A + B) ≤ A := by
    norm_num at *
    linarith
  have hqhalf : (1 : ℝ) / 2 ≤ (2 : ℝ) / 3 := by norm_num
  have hqone : (2 : ℝ) / 3 < 1 := by norm_num
  exact binary_policy_improvement A B ((2 : ℝ) / 3)
    hA hB hqhalf hqone hcertificate

/-- Endpoint bounds specialize a binary certificate to the robust objective. -/
theorem robust_binary_policy_improvement
    (a b A B q : ℝ)
    (ha : 0 ≤ a)
    (haA : a ≤ A)
    (hB : 0 ≤ B)
    (hBb : B ≤ b)
    (hqhalf : (1 : ℝ) / 2 ≤ q)
    (hqone : q < 1)
    (hcertificate : q * (a + b) ≤ a) :
    A / q + B / (1 - q) ≤ 2 * (A + B) := by
  have hqnonneg : 0 ≤ q := by linarith
  have hqcomp : 0 ≤ 1 - q := by linarith
  have hqcoeff : -(1 - q) ≤ 0 := neg_nonpos.mpr hqcomp
  have hAterm : -(1 - q) * A ≤ -(1 - q) * a :=
    mul_le_mul_of_nonpos_left haA hqcoeff
  have hBterm : q * B ≤ q * b :=
    mul_le_mul_of_nonneg_left hBb hqnonneg
  have hABcertificate : q * (A + B) ≤ A := by
    nlinarith [hAterm, hBterm, hcertificate]
  have hA_nonneg : 0 ≤ A := ha.trans haA
  exact binary_policy_improvement A B q hA_nonneg hB hqhalf hqone hABcertificate

/-- Iteration from bottom stays below every prefixed point of a monotone map. -/
theorem prefixed_policy_bounds_iterates
    {α : Type*}
    [CompleteLattice α]
    (G : α → α)
    (hG : Monotone G)
    {v : α}
    (hv : G v ≤ v) :
    ∀ n, Nat.iterate G n ⊥ ≤ v := by
  intro n
  induction n with
  | zero => exact bot_le
  | succ n ih =>
      rw [Function.iterate_succ_apply']
      exact (hG ih).trans hv

/-- A point fixed by `F` and improved pointwise by a monotone `G` bounds the
supremum of all finite `G` iterates from bottom. -/
theorem policy_improvement_iSup
    {α : Type*}
    [CompleteLattice α]
    (F G : α → α)
    (hG : Monotone G)
    {v : α}
    (hv : F v = v)
    (himprove : G v ≤ F v) :
    (⨆ n, Nat.iterate G n ⊥) ≤ v := by
  have hGv : G v ≤ v := by simpa [hv] using himprove
  apply iSup_le
  intro n
  exact prefixed_policy_bounds_iterates G hG hGv n

end EstimatorIntegrity
