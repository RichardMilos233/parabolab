import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

namespace EstimatorIntegrity

noncomputable section

/-- The tuple-selection part of a branching estimator's second moment. -/
def secondMomentObjective {n : ℕ} (A q : Fin n → ℝ) : ℝ :=
  ∑ i, A i / q i

/-- The square-root proposal associated with positive continuation contributions. -/
def sqrtProposal {n : ℕ} (A : Fin n → ℝ) (i : Fin n) : ℝ :=
  Real.sqrt (A i) / ∑ j, Real.sqrt (A j)

private theorem sqrtSum_pos {n : ℕ} {A : Fin n → ℝ}
    (hA : ∀ i, 0 < A i) (i : Fin n) :
    0 < ∑ j, Real.sqrt (A j) := by
  have hi : Real.sqrt (A i) ≤ ∑ j, Real.sqrt (A j) := by
    exact Finset.single_le_sum
      (fun j _ ↦ Real.sqrt_nonneg (A j)) (Finset.mem_univ i)
  exact (Real.sqrt_pos.2 (hA i)).trans_le hi

theorem sqrtProposal_sum {n : ℕ} [NeZero n] (A : Fin n → ℝ)
    (hA : ∀ i, 0 < A i) :
    ∑ i, sqrtProposal A i = 1 := by
  let i : Fin n := ⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩
  have hS : 0 < ∑ j, Real.sqrt (A j) := sqrtSum_pos hA i
  unfold sqrtProposal
  rw [← Finset.sum_div, div_self hS.ne']

theorem sqrtProposal_pos {n : ℕ} (A : Fin n → ℝ)
    (hA : ∀ i, 0 < A i) :
    ∀ i, 0 < sqrtProposal A i := by
  intro i
  exact div_pos (Real.sqrt_pos.2 (hA i)) (sqrtSum_pos hA i)

/-- Cauchy--Schwarz lower bound for every positive normalized proposal. -/
theorem secondMoment_ge_oracle {n : ℕ} (A q : Fin n → ℝ)
    (hA : ∀ i, 0 < A i)
    (hq : ∀ i, 0 < q i)
    (hqsum : ∑ i, q i = 1) :
    (∑ i, Real.sqrt (A i)) ^ 2 ≤ secondMomentObjective A q := by
  have hcs := Finset.sq_sum_div_le_sum_sq_div
    Finset.univ (fun i ↦ Real.sqrt (A i)) (fun i _ ↦ hq i)
  unfold secondMomentObjective
  simpa only [hqsum, div_one, Real.sq_sqrt (hA _).le] using hcs

/-- The square-root proposal attains the Cauchy--Schwarz lower bound. -/
theorem secondMoment_sqrtProposal_eq {n : ℕ} [NeZero n]
    (A : Fin n → ℝ) (hA : ∀ i, 0 < A i) :
    secondMomentObjective A (sqrtProposal A) =
      (∑ i, Real.sqrt (A i)) ^ 2 := by
  let i₀ : Fin n := ⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩
  have hS : 0 < ∑ j, Real.sqrt (A j) := sqrtSum_pos hA i₀
  unfold secondMomentObjective sqrtProposal
  calc
    ∑ i, A i / (Real.sqrt (A i) / ∑ j, Real.sqrt (A j)) =
        ∑ i, (∑ j, Real.sqrt (A j)) * Real.sqrt (A i) := by
      apply Finset.sum_congr rfl
      intro i _
      have hi : 0 < Real.sqrt (A i) := Real.sqrt_pos.2 (hA i)
      have hi_sq : Real.sqrt (A i) ^ 2 = A i :=
        Real.sq_sqrt (hA i).le
      field_simp [hi.ne', hS.ne']
      nlinarith
    _ = (∑ i, Real.sqrt (A i)) ^ 2 := by
      rw [← Finset.mul_sum]
      ring

private theorem sqrtSum_relative_bounds {n : ℕ}
    (A Ahat : Fin n → ℝ) (η : ℝ)
    (hη : 0 ≤ η ∧ η < 1)
    (h_bounds : ∀ i,
      (1 - η) * A i ≤ Ahat i ∧ Ahat i ≤ (1 + η) * A i) :
    Real.sqrt (1 - η) * (∑ i, Real.sqrt (A i)) ≤
        ∑ i, Real.sqrt (Ahat i) ∧
      (∑ i, Real.sqrt (Ahat i)) ≤
        Real.sqrt (1 + η) * (∑ i, Real.sqrt (A i)) := by
  have hminus : 0 ≤ 1 - η := by linarith
  have hplus : 0 ≤ 1 + η := by linarith
  constructor
  · rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i _
    rw [← Real.sqrt_mul hminus]
    exact Real.sqrt_le_sqrt (h_bounds i).1
  · rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i _
    rw [← Real.sqrt_mul hplus]
    exact Real.sqrt_le_sqrt (h_bounds i).2

/-- Relative continuation-moment error gives componentwise proposal-ratio bounds. -/
theorem sqrtProposal_ratio_bounds {n : ℕ}
    (A Ahat : Fin n → ℝ) (η : ℝ)
    (hA : ∀ i, 0 < A i)
    (hAhat : ∀ i, 0 < Ahat i)
    (hη : 0 ≤ η ∧ η < 1)
    (h_bounds : ∀ i,
      (1 - η) * A i ≤ Ahat i ∧ Ahat i ≤ (1 + η) * A i) :
    ∀ i,
      Real.sqrt ((1 - η) / (1 + η)) ≤
          sqrtProposal Ahat i / sqrtProposal A i ∧
        sqrtProposal Ahat i / sqrtProposal A i ≤
          Real.sqrt ((1 + η) / (1 - η)) := by
  intro i
  have hminus : 0 < 1 - η := by linarith
  have hplus : 0 < 1 + η := by linarith
  have hsqrtminus : 0 < Real.sqrt (1 - η) := Real.sqrt_pos.2 hminus
  have hsqrtplus : 0 < Real.sqrt (1 + η) := Real.sqrt_pos.2 hplus
  have hS : 0 < ∑ j, Real.sqrt (A j) := sqrtSum_pos hA i
  have hShat : 0 < ∑ j, Real.sqrt (Ahat j) := sqrtSum_pos hAhat i
  have hq : 0 < sqrtProposal A i := sqrtProposal_pos A hA i
  have hqhat : 0 < sqrtProposal Ahat i := sqrtProposal_pos Ahat hAhat i
  have hsum := sqrtSum_relative_bounds A Ahat η hη h_bounds
  have hnum_lower :
      Real.sqrt (1 - η) * Real.sqrt (A i) ≤ Real.sqrt (Ahat i) := by
    rw [← Real.sqrt_mul hminus.le]
    exact Real.sqrt_le_sqrt (h_bounds i).1
  have hnum_upper :
      Real.sqrt (Ahat i) ≤ Real.sqrt (1 + η) * Real.sqrt (A i) := by
    rw [← Real.sqrt_mul hplus.le]
    exact Real.sqrt_le_sqrt (h_bounds i).2
  have hlower :
      (Real.sqrt (1 - η) * Real.sqrt (A i)) /
          (Real.sqrt (1 + η) * ∑ j, Real.sqrt (A j)) ≤
        sqrtProposal Ahat i := by
    unfold sqrtProposal
    exact div_le_div₀
      (Real.sqrt_nonneg _)
      hnum_lower hShat hsum.2
  have hupper :
      sqrtProposal Ahat i ≤
        (Real.sqrt (1 + η) * Real.sqrt (A i)) /
          (Real.sqrt (1 - η) * ∑ j, Real.sqrt (A j)) := by
    unfold sqrtProposal
    exact div_le_div₀
      (mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _))
      hnum_upper (mul_pos hsqrtminus hS) hsum.1
  have hlower_form :
      Real.sqrt ((1 - η) / (1 + η)) * sqrtProposal A i =
        (Real.sqrt (1 - η) * Real.sqrt (A i)) /
          (Real.sqrt (1 + η) * ∑ j, Real.sqrt (A j)) := by
    rw [Real.sqrt_div hminus.le]
    unfold sqrtProposal
    field_simp [hsqrtplus.ne', hS.ne']
  have hupper_form :
      Real.sqrt ((1 + η) / (1 - η)) * sqrtProposal A i =
        (Real.sqrt (1 + η) * Real.sqrt (A i)) /
          (Real.sqrt (1 - η) * ∑ j, Real.sqrt (A j)) := by
    rw [Real.sqrt_div hplus.le]
    unfold sqrtProposal
    field_simp [hsqrtminus.ne', hS.ne']
  constructor
  · apply (le_div_iff₀ hq).2
    rw [hlower_form]
    exact hlower
  · apply (div_le_iff₀ hq).2
    rw [hupper_form]
    exact hupper

private theorem relative_sqrt_factors_mul_eq_one (η : ℝ)
    (hη : 0 ≤ η ∧ η < 1) :
    Real.sqrt ((1 + η) / (1 - η)) *
        Real.sqrt ((1 - η) / (1 + η)) = 1 := by
  have hminus : 0 < 1 - η := by linarith
  have hplus : 0 < 1 + η := by linarith
  have hsqrtminus : 0 < Real.sqrt (1 - η) := Real.sqrt_pos.2 hminus
  have hsqrtplus : 0 < Real.sqrt (1 + η) := Real.sqrt_pos.2 hplus
  rw [Real.sqrt_div hplus.le, Real.sqrt_div hminus.le]
  field_simp [hsqrtminus.ne', hsqrtplus.ne']

/-- A multiplicatively accurate pilot square-root proposal is near-oracle. -/
theorem oracle_ratio_of_relative_error {n : ℕ}
    (A Ahat : Fin n → ℝ) (η : ℝ)
    (hA : ∀ i, 0 < A i)
    (hAhat : ∀ i, 0 < Ahat i)
    (hη : 0 ≤ η ∧ η < 1)
    (h_bounds : ∀ i,
      (1 - η) * A i ≤ Ahat i ∧ Ahat i ≤ (1 + η) * A i) :
    secondMomentObjective A (sqrtProposal Ahat) ≤
      Real.sqrt ((1 + η) / (1 - η)) *
        secondMomentObjective A (sqrtProposal A) := by
  have hk :
      0 ≤ Real.sqrt ((1 + η) / (1 - η)) := Real.sqrt_nonneg _
  have hkl := relative_sqrt_factors_mul_eq_one η hη
  unfold secondMomentObjective
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i _
  have hq : 0 < sqrtProposal A i := sqrtProposal_pos A hA i
  have hqhat : 0 < sqrtProposal Ahat i := sqrtProposal_pos Ahat hAhat i
  have hlower :=
    (sqrtProposal_ratio_bounds A Ahat η hA hAhat hη h_bounds i).1
  have hmul :
      Real.sqrt ((1 - η) / (1 + η)) * sqrtProposal A i ≤
        sqrtProposal Ahat i :=
    (le_div_iff₀ hq).1 hlower
  have hreciprocal :
      sqrtProposal A i / sqrtProposal Ahat i ≤
        Real.sqrt ((1 + η) / (1 - η)) := by
    apply (div_le_iff₀ hqhat).2
    calc
      sqrtProposal A i =
          Real.sqrt ((1 + η) / (1 - η)) *
            (Real.sqrt ((1 - η) / (1 + η)) * sqrtProposal A i) := by
              rw [← mul_assoc, hkl, one_mul]
      _ ≤ Real.sqrt ((1 + η) / (1 - η)) * sqrtProposal Ahat i :=
        mul_le_mul_of_nonneg_left hmul hk
  calc
    A i / sqrtProposal Ahat i =
        (sqrtProposal A i / sqrtProposal Ahat i) *
          (A i / sqrtProposal A i) := by
            field_simp [hq.ne', hqhat.ne']
    _ ≤ Real.sqrt ((1 + η) / (1 - η)) *
          (A i / sqrtProposal A i) :=
      mul_le_mul_of_nonneg_right hreciprocal
        (div_nonneg (hA i).le hq.le)

/-- Adding a uniform support floor costs at most `1 / (1 - ε)` in objective. -/
theorem secondMoment_uniformMixture_le {n : ℕ} [NeZero n]
    (A q : Fin n → ℝ) (ε : ℝ)
    (hA : ∀ i, 0 ≤ A i)
    (hq : ∀ i, 0 < q i)
    (hε : 0 ≤ ε ∧ ε < 1) :
    secondMomentObjective A
        (fun i ↦ (1 - ε) * q i + ε / (n : ℝ)) ≤
      (1 / (1 - ε)) * secondMomentObjective A q := by
  have hminus : 0 < 1 - ε := by linarith
  have hn_nat : 0 < n := Nat.pos_of_ne_zero (NeZero.ne n)
  have hn : 0 < (n : ℝ) := by exact_mod_cast hn_nat
  unfold secondMomentObjective
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro i _
  have hfloor : 0 ≤ ε / (n : ℝ) := div_nonneg hε.1 hn.le
  have hqmix : 0 < (1 - ε) * q i + ε / (n : ℝ) :=
    (mul_pos hminus (hq i)).trans_le (le_add_of_nonneg_right hfloor)
  have hratio :
      q i / ((1 - ε) * q i + ε / (n : ℝ)) ≤ 1 / (1 - ε) := by
    apply (div_le_div_iff₀ hqmix hminus).2
    calc
      q i * (1 - ε) = (1 - ε) * q i := mul_comm _ _
      _ ≤ (1 - ε) * q i + ε / (n : ℝ) :=
        le_add_of_nonneg_right hfloor
      _ = 1 * ((1 - ε) * q i + ε / (n : ℝ)) := by ring
  calc
    A i / ((1 - ε) * q i + ε / (n : ℝ)) =
        (q i / ((1 - ε) * q i + ε / (n : ℝ))) * (A i / q i) := by
          field_simp [(hq i).ne', hqmix.ne']
    _ ≤ (1 / (1 - ε)) * (A i / q i) :=
      mul_le_mul_of_nonneg_right hratio (div_nonneg (hA i) (hq i).le)

end

end EstimatorIntegrity
