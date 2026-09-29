import Mathlib.Tactic

/-!
# Finite algebra for normalized heat-transform work bounds

This module verifies only finite-product bounds and finite-depth scalar work
recurrences.  It does not encode heat kernels, sampling laws, expectations,
tree completion, monotone convergence, or PDE representation.
-/

namespace EstimatorIntegrity

/-- A normalized finite product remains in the closed unit interval in
absolute value.  The statement includes the empty list. -/
theorem abs_scalar_mul_list_prod_le_one (z : List ℝ) (σ : ℝ)
    (hσ : |σ| ≤ 1) (hz : ∀ x ∈ z, |x| ≤ 1) :
    |σ * z.prod| ≤ 1 := by
  have hprod : |z.prod| ≤ 1 := by
    induction z with
    | nil => simp
    | cons x xs ih =>
        have hx : |x| ≤ 1 := hz x (by simp)
        have hxs : ∀ y ∈ xs, |y| ≤ 1 := by
          intro y hy
          exact hz y (by simp [hy])
        have hi := ih hxs
        rw [List.prod_cons, abs_mul]
        simpa using mul_le_mul hx hi (abs_nonneg xs.prod) (by norm_num : (0 : ℝ) ≤ 1)
  rw [abs_mul]
  simpa using mul_le_mul hσ hprod (abs_nonneg z.prod) (by norm_num : (0 : ℝ) ≤ 1)

/-- A terminal value dominated by a strictly positive envelope has normalized
magnitude at most one. -/
theorem abs_div_le_one_of_abs_le (g h : ℝ) (hh : 0 < h) (hg : |g| ≤ h) :
    |g / h| ≤ 1 := by
  rw [abs_div, abs_of_pos hh]
  exact (div_le_one hh).2 hg

/-- The four rational constants are fixed points of the affine upper
recurrence used for finite-depth nonconstant-node counts. -/
theorem heatTransformWork_fixedPoint :
    1 + (1 / 4 : ℝ) * (220 / 3 + 56) + 2 * 20 = 220 / 3 ∧
      1 + (3 / 4 : ℝ) * (220 / 3) = 56 ∧
      1 + (1 / 4 : ℝ) * (56 + 20) = 20 ∧
      1 + (3 / 4 : ℝ) * (220 / 3) = 56 := by
  norm_num

/-- Simultaneous finite-depth invariant for the four-type work recurrence.
No statement about an untruncated or infinite tree is assumed. -/
theorem finiteHeatTransformWorkInvariant
    (A B D I : ℕ → ℝ)
    (hA0 : 0 ≤ A 0 ∧ A 0 ≤ 1)
    (hB0 : 0 ≤ B 0 ∧ B 0 ≤ 1)
    (hD0 : 0 ≤ D 0 ∧ D 0 ≤ 1)
    (hI0 : 0 ≤ I 0 ∧ I 0 ≤ 1)
    (hnonneg : ∀ n, 0 ≤ A n ∧ 0 ≤ B n ∧ 0 ≤ D n ∧ 0 ≤ I n)
    (hAstep : ∀ n,
      A (n + 1) ≤ 1 + (1 / 4) * (A n + B n) + 2 * D n)
    (hBstep : ∀ n, B (n + 1) ≤ 1 + (3 / 4) * A n)
    (hDstep : ∀ n, D (n + 1) ≤ 1 + (1 / 4) * (B n + D n))
    (hIstep : ∀ n, I (n + 1) ≤ 1 + (3 / 4) * A n) :
    ∀ n, A n ≤ 220 / 3 ∧ B n ≤ 56 ∧ D n ≤ 20 ∧ I n ≤ 56 := by
  intro n
  induction n with
  | zero =>
      obtain ⟨hA0_nonneg, hB0_nonneg, hD0_nonneg, hI0_nonneg⟩ := hnonneg 0
      have hA0_le := hA0.2
      have hB0_le := hB0.2
      have hD0_le := hD0.2
      have hI0_le := hI0.2
      constructor
      · norm_num at hA0_le ⊢
        linarith
      · constructor
        · linarith
        · constructor <;> linarith
  | succ n ih =>
      obtain ⟨hA_le, hB_le, hD_le, hI_le⟩ := ih
      have hA_next := hAstep n
      have hB_next := hBstep n
      have hD_next := hDstep n
      have hI_next := hIstep n
      constructor
      · norm_num at hA_next ⊢
        nlinarith
      · constructor
        · norm_num at hB_next ⊢
          nlinarith
        · constructor
          · norm_num at hD_next ⊢
            nlinarith
          · norm_num at hI_next ⊢
            nlinarith

/-- Doubling the finite-depth Id count to include at most one constant leaf
per nonconstant node gives the audited root bound `112`. -/
theorem finiteHeatTransformTotalRootWork_le
    (I R : ℕ → ℝ) (hI : ∀ n, I n ≤ 56) (hR : ∀ n, R n ≤ 2 * I n) :
    ∀ n, R n ≤ 112 := by
  intro n
  have hI_n := hI n
  have hR_n := hR n
  nlinarith

/-- Optional scalar baseline: event probability `η ≤ 1/48` and two children
give the invariant expected-work bound `24/23` at every finite depth. -/
theorem finiteScalarBaselineWorkInvariant
    (η : ℝ) (M : ℕ → ℝ)
    (hη : 0 ≤ η) (hη_le : η ≤ 1 / 48)
    (hM0 : 0 ≤ M 0 ∧ M 0 ≤ 1)
    (hM_nonneg : ∀ n, 0 ≤ M n)
    (hstep : ∀ n, M (n + 1) ≤ 1 + 2 * η * M n) :
    ∀ n, M n ≤ 24 / 23 := by
  intro n
  induction n with
  | zero =>
      have hM0_le := hM0.2
      norm_num at hM0_le ⊢
      linarith
  | succ n ih =>
      have hM_n_nonneg := hM_nonneg n
      have hηM_nonneg : 0 ≤ η * M n := mul_nonneg hη hM_n_nonneg
      have hscale : 2 * η * M n ≤ 2 * (1 / 48) * (24 / 23) := by
        gcongr
      have hnext := hstep n
      norm_num at hscale hnext ⊢
      nlinarith [hηM_nonneg]

/-- Matched Gaussian specialization: `η ≤ 1/96` yields the sharper finite
work invariant `48/47`. -/
theorem finiteMatchedGaussianWorkInvariant
    (η : ℝ) (M : ℕ → ℝ)
    (hη : 0 ≤ η) (hη_le : η ≤ 1 / 96)
    (hM0 : 0 ≤ M 0 ∧ M 0 ≤ 1)
    (hM_nonneg : ∀ n, 0 ≤ M n)
    (hstep : ∀ n, M (n + 1) ≤ 1 + 2 * η * M n) :
    ∀ n, M n ≤ 48 / 47 := by
  intro n
  induction n with
  | zero =>
      have hM0_le := hM0.2
      norm_num at hM0_le ⊢
      linarith
  | succ n ih =>
      have hM_n_nonneg := hM_nonneg n
      have hηM_nonneg : 0 ≤ η * M n := mul_nonneg hη hM_n_nonneg
      have hscale : 2 * η * M n ≤ 2 * (1 / 96) * (48 / 47) := by
        gcongr
      have hnext := hstep n
      norm_num at hscale hnext ⊢
      nlinarith [hηM_nonneg]

end EstimatorIntegrity
