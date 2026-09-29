import Mathlib.Probability.Moments.Variance
import Mathlib.Probability.Independence.Integration
import Mathlib.Tactic
import EstimatorIntegrity.PositiveSigmoidRisk

/-!
# Positive bounded sample means

This module proves the actual mean-square error bound for a finite average of
pairwise independent, nonnegative, bounded real random variables on an
arbitrary probability space.  Integrability and the second-moment hypotheses
are derived from the pointwise range bound.
-/

open MeasureTheory ProbabilityTheory

namespace EstimatorIntegrity

noncomputable section

/-- The arithmetic mean of a `Fin n`-indexed family of real random variables. -/
def positiveSampleMean {Ω : Type*} {n : ℕ} (Y : Fin n → Ω → ℝ) : Ω → ℝ :=
  fun ω => (∑ i, Y i ω) / (n : ℝ)

/-- A pointwise bounded measurable sample is integrable. -/
theorem positiveSample_integrable
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (Y : Fin n → Ω → ℝ) (A : ℝ)
    (hYmeas : ∀ i, Measurable (Y i))
    (hYrange : ∀ i ω, 0 ≤ Y i ω ∧ Y i ω ≤ A) (i : Fin n) :
    Integrable (Y i) μ := by
  apply Integrable.of_bound (hYmeas i).aestronglyMeasurable A
  filter_upwards [] with ω
  rw [Real.norm_eq_abs, abs_of_nonneg (hYrange i ω).1]
  exact (hYrange i ω).2

/-- The range bound also supplies the `L²` hypothesis used by the variance
identity. -/
theorem positiveSample_memLp_two
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (Y : Fin n → Ω → ℝ) (A : ℝ)
    (hYmeas : ∀ i, Measurable (Y i))
    (hYrange : ∀ i ω, 0 ≤ Y i ω ∧ Y i ω ≤ A) (i : Fin n) :
    MemLp (Y i) 2 μ := by
  exact memLp_of_bounded (ae_of_all μ fun ω => hYrange i ω)
    (hYmeas i).aestronglyMeasurable 2

/-- Pairwise independence gives the product-integral identity; it is not an
assumed covariance condition. -/
theorem positiveSample_product_integral
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (Y : Fin n → Ω → ℝ) (m : ℝ)
    (hYmeas : ∀ i, Measurable (Y i))
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ)
    (hMean : ∀ i, ∫ ω, Y i ω ∂μ = m)
    {i j : Fin n} (hij : i ≠ j) :
    (∫ ω, Y i ω * Y j ω ∂μ) = m * m := by
  rw [(hIndep hij).integral_fun_mul_eq_mul_integral
    (hYmeas i).aestronglyMeasurable (hYmeas j).aestronglyMeasurable,
    hMean i, hMean j]

/-- The sample mean is measurable. -/
theorem positiveSampleMean_measurable
    {Ω : Type*} [MeasurableSpace Ω] {n : ℕ} (Y : Fin n → Ω → ℝ)
    (hYmeas : ∀ i, Measurable (Y i)) :
    Measurable (positiveSampleMean Y) := by
  unfold positiveSampleMean
  fun_prop

/-- The sample mean is integrable, derived from boundedness of every sample. -/
theorem positiveSampleMean_integrable
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (Y : Fin n → Ω → ℝ) (A : ℝ)
    (hYmeas : ∀ i, Measurable (Y i))
    (hYrange : ∀ i ω, 0 ≤ Y i ω ∧ Y i ω ≤ A) :
    Integrable (positiveSampleMean Y) μ := by
  unfold positiveSampleMean
  exact (integrable_finsetSum Finset.univ fun i _ =>
    positiveSample_integrable μ Y A hYmeas hYrange i).div_const _

/-- The actual integral of the sample mean equals the common sample mean. -/
theorem positiveSampleMean_unbiased
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (hn : 0 < n) (Y : Fin n → Ω → ℝ) (A m : ℝ)
    (hYmeas : ∀ i, Measurable (Y i))
    (hYrange : ∀ i ω, 0 ≤ Y i ω ∧ Y i ω ≤ A)
    (hMean : ∀ i, ∫ ω, Y i ω ∂μ = m) :
    ∫ ω, positiveSampleMean Y ω ∂μ = m := by
  change (∫ ω, (∑ i, Y i ω) / (n : ℝ) ∂μ) = m
  rw [integral_div]
  rw [integral_finsetSum Finset.univ fun i _ =>
    positiveSample_integrable μ Y A hYmeas hYrange i]
  simp [hMean, hn.ne']

/-- The centered squared loss of the sample mean is integrable. -/
theorem positiveSampleMean_squaredLoss_integrable
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (Y : Fin n → Ω → ℝ) (A m : ℝ)
    (hYmeas : ∀ i, Measurable (Y i))
    (hYrange : ∀ i ω, 0 ≤ Y i ω ∧ Y i ω ≤ A) :
    Integrable (fun ω => (positiveSampleMean Y ω - m) ^ 2) μ := by
  have hmeanL2 : MemLp (positiveSampleMean Y) 2 μ := by
    have hsumL2 : MemLp (∑ i, Y i) 2 μ :=
      memLp_finsetSum' Finset.univ fun i _ =>
        positiveSample_memLp_two μ Y A hYmeas hYrange i
    rw [show positiveSampleMean Y = fun ω => (n : ℝ)⁻¹ * (∑ i, Y i) ω by
      funext ω
      simp [positiveSampleMean, div_eq_mul_inv, mul_comm]]
    exact hsumL2.const_mul _
  exact (hmeanL2.sub (memLp_const m)).integrable_sq

/-- For positive, pairwise independent bounded samples, the actual sample
mean has mean-square error at most `A * m / n`. -/
theorem positiveSampleMean_mse_le
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (hn : 0 < n) (Y : Fin n → Ω → ℝ) (A m : ℝ)
    (_hA : 0 ≤ A) (hm : 0 ≤ m)
    (hYmeas : ∀ i, Measurable (Y i))
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ)
    (hYrange : ∀ i ω, 0 ≤ Y i ω ∧ Y i ω ≤ A)
    (hMean : ∀ i, ∫ ω, Y i ω ∂μ = m) :
    (∫ ω, (positiveSampleMean Y ω - m) ^ 2 ∂μ) ≤ A * m / (n : ℝ) := by
  have hYiL2 : ∀ i, MemLp (Y i) 2 μ :=
    positiveSample_memLp_two μ Y A hYmeas hYrange
  have hsum_meas : AEMeasurable (∑ i, Y i) μ := by
    fun_prop
  have hmean_meas : AEMeasurable (positiveSampleMean Y) μ :=
    (positiveSampleMean_measurable Y hYmeas).aemeasurable
  have hmean_value := positiveSampleMean_unbiased μ hn Y A m hYmeas hYrange hMean
  have hvar_each : ∀ i, variance (Y i) μ ≤ A * m := by
    intro i
    calc
      variance (Y i) μ ≤ (A - ∫ ω, Y i ω ∂μ) * ((∫ ω, Y i ω ∂μ) - 0) :=
        variance_le_sub_mul_sub (ae_of_all μ fun ω => hYrange i ω)
          (hYmeas i).aemeasurable
      _ = (A - m) * m := by rw [hMean i]; ring
      _ ≤ A * m := by nlinarith
  calc
    (∫ ω, (positiveSampleMean Y ω - m) ^ 2 ∂μ) =
        variance (positiveSampleMean Y) μ := by
      rw [variance_eq_integral hmean_meas, hmean_value]
    _ = ((n : ℝ)⁻¹) ^ 2 * variance (∑ i, Y i) μ := by
      rw [show positiveSampleMean Y = fun ω => (n : ℝ)⁻¹ * (∑ i, Y i) ω by
        funext ω
        simp [positiveSampleMean, div_eq_mul_inv, mul_comm]]
      exact variance_const_mul _ _ _
    _ = ((n : ℝ)⁻¹) ^ 2 * ∑ i, variance (Y i) μ := by
      rw [IndepFun.variance_sum (s := Finset.univ)]
      · intro i _
        exact hYiL2 i
      · intro i _ j _ hij
        exact hIndep hij
    _ ≤ ((n : ℝ)⁻¹) ^ 2 * ∑ _i : Fin n, A * m := by
      gcongr with i
      exact hvar_each i
    _ = A * m / (n : ℝ) := by
      have hnR : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
      simp only [Finset.sum_const, nsmul_eq_mul, Finset.card_univ, Fintype.card_fin]
      field_simp [hnR]

/-- For `0 < β < 1`, the scalar factor left after the sample-budget
cancellation is at most one. -/
theorem positive_rpow_one_add_le_one_add_sq
    (z β : ℝ) (hz : 0 ≤ z) (hβ0 : 0 < β) (hβ1 : β < 1) :
    z ^ (1 + β : ℝ) ≤ 1 + z ^ 2 := by
  by_cases hz1 : z ≤ 1
  · calc
      z ^ (1 + β : ℝ) ≤ 1 := Real.rpow_le_one hz hz1 (by linarith)
      _ ≤ 1 + z ^ 2 := le_add_of_nonneg_right (sq_nonneg z)
  · have hone : 1 ≤ z := le_of_not_ge hz1
    calc
      z ^ (1 + β : ℝ) ≤ z ^ (2 : ℝ) :=
        Real.rpow_le_rpow_of_exponent_le hone (by linarith)
      _ = z ^ 2 := Real.rpow_two z
      _ ≤ 1 + z ^ 2 := by linarith

/-- Exact exponent identity used to cancel the horizon-dependent sampling
budget.  Positivity of `m` is stated explicitly; the combined theorem treats
`m = 0` separately. -/
theorem positive_scaled_rpow_identity
    (T m β : ℝ) (hm : 0 < m) :
    Real.exp ((1 - β) * T) * (Real.exp T * m) ^ (1 + β : ℝ) =
      Real.exp (2 * T) * m ^ β * m := by
  rw [Real.mul_rpow (Real.exp_pos T).le hm.le]
  rw [← Real.exp_mul, Real.rpow_add hm 1 β, Real.rpow_one]
  have hexp :
      Real.exp ((1 - β) * T) * Real.exp (T * (1 + β)) = Real.exp (2 * T) := by
    rw [← Real.exp_add]
    congr 1
    ring
  rw [← mul_assoc, hexp]
  ring

/-- Algebraic budget cancellation for a positive mean.  This lemma keeps the
actual sample MSE `q` visible, rather than assuming the desired transformed
risk bound. -/
theorem positive_scaled_budget_bound
    (q nReal A m C β T : ℝ)
    (hq : q ≤ A * m / nReal) (hnReal : 0 < nReal) (hm : 0 < m)
    (hβ0 : 0 < β) (hβ1 : β < 1) (_hC : 1 ≤ C)
    (hAupper : A ≤ C * m ^ β)
    (hbudget : 64 * C * Real.exp ((1 - β) * T) ≤ nReal) :
    Real.exp (2 * T) * q / (1 + (Real.exp T * m) ^ 2) ≤ (1 / 64 : ℝ) := by
  let z := Real.exp T * m
  have hz : 0 ≤ z := mul_nonneg (Real.exp_pos T).le hm.le
  have hden : 0 < 1 + z ^ 2 := by positivity
  have hzpow : 0 ≤ z ^ (1 + β : ℝ) := Real.rpow_nonneg hz _
  have hbudget_ratio :
      C * Real.exp ((1 - β) * T) / nReal ≤ (1 / 64 : ℝ) := by
    apply (div_le_iff₀ hnReal).2
    nlinarith
  have hraw :
      Real.exp (2 * T) * (A * m / nReal) ≤
        (1 / 64 : ℝ) * z ^ (1 + β : ℝ) := by
    calc
      Real.exp (2 * T) * (A * m / nReal) ≤
          Real.exp (2 * T) * ((C * m ^ β) * m / nReal) := by
        gcongr
      _ = (C / nReal) * (Real.exp (2 * T) * m ^ β * m) := by ring
      _ = (C / nReal) *
          (Real.exp ((1 - β) * T) * z ^ (1 + β : ℝ)) := by
        rw [positive_scaled_rpow_identity T m β hm]
      _ = (C * Real.exp ((1 - β) * T) / nReal) *
          z ^ (1 + β : ℝ) := by ring
      _ ≤ (1 / 64 : ℝ) * z ^ (1 + β : ℝ) := by
        exact mul_le_mul_of_nonneg_right hbudget_ratio hzpow
  have hq_scaled :
      Real.exp (2 * T) * q ≤ (1 / 64 : ℝ) * z ^ (1 + β : ℝ) := by
    calc
      Real.exp (2 * T) * q ≤ Real.exp (2 * T) * (A * m / nReal) := by
        exact mul_le_mul_of_nonneg_left hq (Real.exp_pos _).le
      _ ≤ (1 / 64 : ℝ) * z ^ (1 + β : ℝ) := hraw
  apply (div_le_iff₀ hden).2
  calc
    Real.exp (2 * T) * q ≤ (1 / 64 : ℝ) * z ^ (1 + β : ℝ) := hq_scaled
    _ ≤ (1 / 64 : ℝ) * (1 + z ^ 2) := by
      gcongr
      exact positive_rpow_one_add_le_one_add_sq z β hz hβ0 hβ1
    _ = (1 / 64 : ℝ) * (1 + (Real.exp T * m) ^ 2) := by rfl

/-- The independent-sample MSE, after horizon scaling and division by the
anchored sigmoid denominator, is at most `1/64`. -/
theorem positiveSampleMean_scaled_mse_le
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (hn : 0 < n) (Y : Fin n → Ω → ℝ) (A m C β T : ℝ)
    (hA : 0 ≤ A) (hm : 0 ≤ m)
    (hYmeas : ∀ i, Measurable (Y i))
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ)
    (hYrange : ∀ i ω, 0 ≤ Y i ω ∧ Y i ω ≤ A)
    (hMean : ∀ i, ∫ ω, Y i ω ∂μ = m)
    (hβ0 : 0 < β) (hβ1 : β < 1) (hC : 1 ≤ C)
    (hAupper : A ≤ C * m ^ β)
    (hbudget : 64 * C * Real.exp ((1 - β) * T) ≤ (n : ℝ)) :
    (∫ ω, (Real.exp T * positiveSampleMean Y ω - Real.exp T * m) ^ 2 ∂μ) /
        (1 + (Real.exp T * m) ^ 2) ≤ (1 / 64 : ℝ) := by
  have hbase_int :=
    positiveSampleMean_squaredLoss_integrable μ Y A m hYmeas hYrange
  have hbase_mse :=
    positiveSampleMean_mse_le μ hn Y A m hA hm hYmeas hIndep hYrange hMean
  have hexp_sq : (Real.exp T) ^ 2 = Real.exp (2 * T) := by
    rw [show 2 * T = T + T by ring, Real.exp_add]
    ring
  have hscaled_eq :
      (fun ω => (Real.exp T * positiveSampleMean Y ω - Real.exp T * m) ^ 2) =
        fun ω => Real.exp (2 * T) * (positiveSampleMean Y ω - m) ^ 2 := by
    funext ω
    rw [← hexp_sq]
    ring
  rw [hscaled_eq, integral_const_mul]
  by_cases hm0 : m = 0
  · subst m
    have hbase_zero : (∫ ω, (positiveSampleMean Y ω - 0) ^ 2 ∂μ) = 0 := by
      apply le_antisymm
      · simpa using hbase_mse
      · exact integral_nonneg fun _ => sq_nonneg _
    simp only [sub_zero] at hbase_zero
    simp only [sub_zero]
    rw [hbase_zero]
    norm_num
  · exact positive_scaled_budget_bound
      (∫ ω, (positiveSampleMean Y ω - m) ^ 2 ∂μ) (n : ℝ) A m C β T
      hbase_mse (by exact_mod_cast hn) (lt_of_le_of_ne hm (Ne.symm hm0))
      hβ0 hβ1 hC hAupper hbudget

/-- The actual sigmoid-transformed MSE of the scaled independent sample mean
is at most `1/64`. -/
theorem positiveSampleMean_transformed_mse_le
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (hn : 0 < n) (Y : Fin n → Ω → ℝ) (A m C β T : ℝ)
    (hA : 0 ≤ A) (hm : 0 ≤ m)
    (hYmeas : ∀ i, Measurable (Y i))
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ)
    (hYrange : ∀ i ω, 0 ≤ Y i ω ∧ Y i ω ≤ A)
    (hMean : ∀ i, ∫ ω, Y i ω ∂μ = m)
    (hβ0 : 0 < β) (hβ1 : β < 1) (hC : 1 ≤ C)
    (hAupper : A ≤ C * m ^ β)
    (hbudget : 64 * C * Real.exp ((1 - β) * T) ≤ (n : ℝ)) :
    (∫ ω, (positiveSigmoid (Real.exp T * positiveSampleMean Y ω) -
      positiveSigmoid (Real.exp T * m)) ^ 2 ∂μ) ≤ (1 / 64 : ℝ) := by
  let X : Ω → ℝ := fun ω => Real.exp T * positiveSampleMean Y ω
  let z : ℝ := Real.exp T * m
  have hmean_meas : Measurable (positiveSampleMean Y) :=
    positiveSampleMean_measurable Y hYmeas
  have hX_meas : Measurable X := by
    dsimp [X]
    fun_prop
  have hmean_nonneg : ∀ ω, 0 ≤ positiveSampleMean Y ω := by
    intro ω
    rw [positiveSampleMean]
    exact div_nonneg (Finset.sum_nonneg fun i _ => (hYrange i ω).1)
      (Nat.cast_nonneg n)
  have hX_nonneg : ∀ ω, 0 ≤ X ω := by
    intro ω
    exact mul_nonneg (Real.exp_pos T).le (hmean_nonneg ω)
  have hz : 0 ≤ z := mul_nonneg (Real.exp_pos T).le hm
  have hbase_int :=
    positiveSampleMean_squaredLoss_integrable μ Y A m hYmeas hYrange
  have hexp_sq : (Real.exp T) ^ 2 = Real.exp (2 * T) := by
    rw [show 2 * T = T + T by ring, Real.exp_add]
    ring
  have hscaled_eq :
      (fun ω => (X ω - z) ^ 2) =
        fun ω => Real.exp (2 * T) * (positiveSampleMean Y ω - m) ^ 2 := by
    funext ω
    dsimp [X, z]
    rw [← hexp_sq]
    ring
  have hdev : Integrable (fun ω => (X ω - z) ^ 2) μ := by
    rw [hscaled_eq]
    exact hbase_int.const_mul _
  have htransform :=
    positiveSigmoid_integral_loss_le μ X z hX_meas hX_nonneg hz hdev
  dsimp [X, z] at htransform
  exact htransform.trans (positiveSampleMean_scaled_mse_le μ hn Y A m C β T
    hA hm hYmeas hIndep hYrange hMean hβ0 hβ1 hC hAupper hbudget)

/-- Full probabilistic certificate.  The deterministic PDE approximation is
represented only by the explicit bias hypothesis `hbias`; no PDE statement is
claimed here. -/
theorem positiveSampleMean_full_risk_certificate
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {n : ℕ} (hn : 0 < n) (Y : Fin n → Ω → ℝ) (A m C β T y : ℝ)
    (hA : 0 ≤ A) (hm : 0 ≤ m)
    (hYmeas : ∀ i, Measurable (Y i))
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ)
    (hYrange : ∀ i ω, 0 ≤ Y i ω ∧ Y i ω ≤ A)
    (hMean : ∀ i, ∫ ω, Y i ω ∂μ = m)
    (hβ0 : 0 < β) (hβ1 : β < 1) (hC : 1 ≤ C) (_hT : 0 ≤ T)
    (hAupper : A ≤ C * m ^ β)
    (hbudget : 64 * C * Real.exp ((1 - β) * T) ≤ (n : ℝ))
    (hbias : |y - positiveSigmoid (Real.exp T * m)| ≤ (1 / 32 : ℝ)) :
    (∫ ω, (positiveSigmoid (Real.exp T * positiveSampleMean Y ω) -
      positiveSigmoid (Real.exp T * m)) ^ 2 ∂μ) ≤ (1 / 64 : ℝ) ∧
    (∫ ω, (positiveSigmoid (Real.exp T * positiveSampleMean Y ω) - y) ^ 2 ∂μ) ≤
      (25 / 1024 : ℝ) ∧
    (∫ ω, (positiveSigmoid (Real.exp T * positiveSampleMean Y ω) - y) ^ 2 ∂μ) <
      (1 / 16 : ℝ) := by
  let X : Ω → ℝ := fun ω => Real.exp T * positiveSampleMean Y ω
  let z : ℝ := Real.exp T * m
  have hmean_meas : Measurable (positiveSampleMean Y) :=
    positiveSampleMean_measurable Y hYmeas
  have hX_meas : Measurable X := by
    dsimp [X]
    fun_prop
  have hmean_nonneg : ∀ ω, 0 ≤ positiveSampleMean Y ω := by
    intro ω
    rw [positiveSampleMean]
    exact div_nonneg (Finset.sum_nonneg fun i _ => (hYrange i ω).1)
      (Nat.cast_nonneg n)
  have hX_nonneg : ∀ ω, 0 ≤ X ω := by
    intro ω
    exact mul_nonneg (Real.exp_pos T).le (hmean_nonneg ω)
  have hz : 0 ≤ z := mul_nonneg (Real.exp_pos T).le hm
  have htransformed := positiveSampleMean_transformed_mse_le μ hn Y A m C β T
    hA hm hYmeas hIndep hYrange hMean hβ0 hβ1 hC hAupper hbudget
  have htotal := positiveSigmoid_bias_composition μ X z y hX_meas hX_nonneg hz
    (by simpa [X, z] using htransformed) (by simpa [z] using hbias)
  refine ⟨htransformed, htotal, ?_⟩
  exact lt_of_le_of_lt htotal (by norm_num)

end

end EstimatorIntegrity
