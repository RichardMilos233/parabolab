import Mathlib.Probability.Independence.Integration
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

/-!
# Hilbert-valued sample means and profile-risk transfer

Actual Bochner-integral identities for finite averages of pairwise independent
Hilbert-valued samples, followed by dependent-across-batch risk bounds,
anchored contractions, coordinate box clipping, and bounded-linear transfer.
-/

open MeasureTheory ProbabilityTheory
open scoped BigOperators ENNReal InnerProductSpace

namespace EstimatorIntegrity.HilbertSamplingRisk

set_option autoImplicit false

noncomputable section

/-- Arithmetic mean of a `Fin n`-indexed Hilbert-valued family. -/
def sampleMean {Ω H : Type*} {n : ℕ} [NormedAddCommGroup H] [NormedSpace ℝ H]
    (Y : Fin n → Ω → H) : Ω → H :=
  fun ω => (1 / (n : ℝ)) • ∑ i, Y i ω

/-- Average of the actual Bochner means of a finite family. -/
def meanAverage {Ω H : Type*} [MeasurableSpace Ω] {n : ℕ}
    [NormedAddCommGroup H] [NormedSpace ℝ H]
    (μ : Measure Ω) (Y : Fin n → Ω → H) : H :=
  (1 / (n : ℝ)) • ∑ i, ∫ ω, Y i ω ∂μ

/-- Center a sample by its actual Bochner mean. -/
def centered {Ω H : Type*} [MeasurableSpace Ω]
    [NormedAddCommGroup H] [NormedSpace ℝ H]
    (μ : Measure Ω) (Y : Ω → H) : Ω → H :=
  fun ω => Y ω - ∫ x, Y x ∂μ

section SampleMean

variable {Ω H : Type*} [MeasurableSpace Ω]
  [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
  [MeasurableSpace H] [BorelSpace H]
  (μ : Measure Ω) [IsProbabilityMeasure μ]

theorem sample_integrable {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ) (i : Fin n) :
    Integrable (Y i) μ :=
  (hY i).integrable (by norm_num)

theorem centered_memLp (Y : Ω → H) (hY : MemLp Y 2 μ) :
    MemLp (centered μ Y) 2 μ := by
  unfold centered
  exact hY.sub (memLp_const _)

theorem centered_integrable (Y : Ω → H) (hY : MemLp Y 2 μ) :
    Integrable (centered μ Y) μ :=
  (centered_memLp μ Y hY).integrable (by norm_num)

theorem centered_sqNorm_integrable (Y : Ω → H) (hY : MemLp Y 2 μ) :
    Integrable (fun ω => ‖centered μ Y ω‖ ^ 2) μ :=
  (centered_memLp μ Y hY).integrable_norm_pow' 

theorem sample_sqNorm_integrable (Y : Ω → H) (hY : MemLp Y 2 μ) :
    Integrable (fun ω => ‖Y ω‖ ^ 2) μ :=
  hY.integrable_norm_pow'

theorem integral_centered (Y : Ω → H) (hY : MemLp Y 2 μ) :
    ∫ ω, centered μ Y ω ∂μ = 0 := by
  unfold centered
  have hc : Integrable (fun _ : Ω => ∫ x, Y x ∂μ) μ := integrable_const _
  rw [integral_sub (hY.integrable (by norm_num)) hc]
  simp

theorem sampleMean_memLp {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ) :
    MemLp (sampleMean Y) 2 μ := by
  unfold sampleMean
  have hsum := (memLp_finsetSum' Finset.univ fun i _ => hY i).const_smul
    (1 / (n : ℝ))
  exact (memLp_congr_ae (ae_of_all μ fun ω => by simp)).2 hsum

theorem sampleMean_integrable {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ) :
    Integrable (sampleMean Y) μ :=
  (sampleMean_memLp μ Y hY).integrable (by norm_num)

theorem integral_sampleMean {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ) :
    ∫ ω, sampleMean Y ω ∂μ = meanAverage μ Y := by
  unfold sampleMean meanAverage
  rw [integral_smul]
  rw [integral_finsetSum Finset.univ]
  intro i hi
  exact sample_integrable μ Y hY i

theorem sampleMean_sub_meanAverage {n : ℕ} (Y : Fin n → Ω → H)
    (ω : Ω) :
    sampleMean Y ω - meanAverage μ Y =
      (1 / (n : ℝ)) • ∑ i, centered μ (Y i) ω := by
  simp only [sampleMean, meanAverage, centered, Finset.sum_sub_distrib, smul_sub]

theorem centered_inner_integrable {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ) (i j : Fin n) :
    Integrable (fun ω => ⟪centered μ (Y i) ω, centered μ (Y j) ω⟫_ℝ) μ := by
  have hprod : Integrable
      (fun ω => ‖centered μ (Y i) ω‖ * ‖centered μ (Y j) ω‖) μ :=
    MemLp.integrable_mul (centered_memLp μ (Y i) (hY i)).norm
      (centered_memLp μ (Y j) (hY j)).norm
  apply hprod.mono'
  · exact (centered_memLp μ (Y i) (hY i)).1.inner
      (centered_memLp μ (Y j) (hY j)).1
  · filter_upwards [] with ω
    exact norm_inner_le_norm _ _

theorem centered_indep {n : ℕ} (Y : Fin n → Ω → H)
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ)
    {i j : Fin n} (hij : i ≠ j) :
    IndepFun (centered μ (Y i)) (centered μ (Y j)) μ := by
  change IndepFun (fun ω => Y i ω - ∫ x, Y i x ∂μ)
    (fun ω => Y j ω - ∫ x, Y j x ∂μ) μ
  convert (hIndep hij).comp
      (show Measurable (fun x : H => x - ∫ ω, Y i ω ∂μ) by fun_prop)
      (show Measurable (fun x : H => x - ∫ ω, Y j ω ∂μ) by fun_prop) using 1 <;>
    rfl

theorem integral_inner_centered_eq_zero {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ)
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ)
    {i j : Fin n} (hij : i ≠ j) :
    ∫ ω, ⟪centered μ (Y i) ω, centered μ (Y j) ω⟫_ℝ ∂μ = 0 := by
  have h := (centered_indep μ Y hIndep hij).integral_bilin
    (centered_integrable μ (Y i) (hY i))
    (centered_integrable μ (Y j) (hY j))
    (innerSL ℝ (E := H))
  rw [integral_centered μ (Y i) (hY i),
    integral_centered μ (Y j) (hY j)] at h
  simp only [map_zero] at h
  simpa only [← innerSL_apply_apply] using h

theorem integral_inner_centered {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ)
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ)
    (i j : Fin n) :
    (∫ ω, ⟪centered μ (Y i) ω, centered μ (Y j) ω⟫_ℝ ∂μ) =
      if i = j then ∫ ω, ‖centered μ (Y i) ω‖ ^ 2 ∂μ else 0 := by
  by_cases hij : i = j
  · subst j
    simp
  · rw [if_neg hij]
    exact integral_inner_centered_eq_zero μ Y hY hIndep hij

theorem integral_norm_sum_centered_sq {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ)
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ) :
    (∫ ω, ‖∑ i, centered μ (Y i) ω‖ ^ 2 ∂μ) =
      ∑ i, ∫ ω, ‖centered μ (Y i) ω‖ ^ 2 ∂μ := by
  classical
  calc
    (∫ ω, ‖∑ i, centered μ (Y i) ω‖ ^ 2 ∂μ) =
        ∫ ω, ∑ i, ∑ j,
          ⟪centered μ (Y i) ω, centered μ (Y j) ω⟫_ℝ ∂μ := by
      apply integral_congr_ae
      filter_upwards [] with ω
      rw [← real_inner_self_eq_norm_sq, sum_inner]
      simp_rw [inner_sum]
    _ = ∑ i, ∑ j,
        ∫ ω, ⟪centered μ (Y i) ω, centered μ (Y j) ω⟫_ℝ ∂μ := by
      rw [integral_finsetSum Finset.univ]
      · congr with i
        rw [integral_finsetSum Finset.univ]
        intro j hj
        exact centered_inner_integrable μ Y hY i j
      · intro i hi
        exact integrable_finsetSum Finset.univ fun j _ =>
          centered_inner_integrable μ Y hY i j
    _ = ∑ i, ∫ ω, ‖centered μ (Y i) ω‖ ^ 2 ∂μ := by
      apply Finset.sum_congr rfl
      intro i hi
      simp_rw [integral_inner_centered μ Y hY hIndep]
      simp

theorem sampleMean_error_memLp {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ) :
    MemLp (fun ω => sampleMean Y ω - meanAverage μ Y) 2 μ := by
  have hsum : MemLp (∑ i, centered μ (Y i)) 2 μ :=
    memLp_finsetSum' Finset.univ fun i _ => centered_memLp μ (Y i) (hY i)
  have hscaled := hsum.const_smul (1 / (n : ℝ))
  have heq : (fun ω => sampleMean Y ω - meanAverage μ Y) =
      (1 / (n : ℝ)) • ∑ i, centered μ (Y i) := by
    funext ω
    simpa only [Pi.smul_apply, Finset.sum_apply] using
      sampleMean_sub_meanAverage μ Y ω
  rw [heq]
  exact hscaled

theorem sampleMean_error_sqNorm_integrable {n : ℕ} (Y : Fin n → Ω → H)
    (hY : ∀ i, MemLp (Y i) 2 μ) :
    Integrable (fun ω => ‖sampleMean Y ω - meanAverage μ Y‖ ^ 2) μ :=
  (sampleMean_error_memLp μ Y hY).integrable_norm_pow'

/-- Exact Hilbert-valued sample-mean square-risk identity. -/
theorem integral_sampleMean_error_sq {n : ℕ} (hn : 0 < n)
    (Y : Fin n → Ω → H) (hY : ∀ i, MemLp (Y i) 2 μ)
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ) :
    (∫ ω, ‖sampleMean Y ω - meanAverage μ Y‖ ^ 2 ∂μ) =
      (1 / (n : ℝ) ^ 2) *
        ∑ i, ∫ ω, ‖Y i ω - ∫ x, Y i x ∂μ‖ ^ 2 ∂μ := by
  have hnR : (0 : ℝ) < n := by exact_mod_cast hn
  simp_rw [sampleMean_sub_meanAverage μ Y]
  simp only [norm_smul, Real.norm_eq_abs, abs_of_nonneg (by positivity :
    0 ≤ (1 / (n : ℝ))), mul_pow]
  rw [integral_const_mul, integral_norm_sum_centered_sq μ Y hY hIndep]
  simp only [centered]
  congr 1
  field_simp

/-- The actual centered second moment equals the uncentered second moment
minus the squared norm of the Bochner mean. -/
theorem integral_centered_sq_eq {Y : Ω → H} (hY : MemLp Y 2 μ) :
    (∫ ω, ‖Y ω - ∫ x, Y x ∂μ‖ ^ 2 ∂μ) =
      (∫ ω, ‖Y ω‖ ^ 2 ∂μ) - ‖∫ x, Y x ∂μ‖ ^ 2 := by
  let m : H := ∫ x, Y x ∂μ
  have hYint : Integrable Y μ := hY.integrable (by norm_num)
  have hnorm : Integrable (fun ω => ‖Y ω‖ ^ 2) μ :=
    sample_sqNorm_integrable μ Y hY
  have hinner : Integrable (fun ω => ⟪Y ω, m⟫_ℝ) μ := hYint.inner_const m
  have hconst : Integrable (fun _ : Ω => ‖m‖ ^ 2) μ := integrable_const _
  have hinter : (∫ ω, ⟪Y ω, m⟫_ℝ ∂μ) = ⟪∫ ω, Y ω ∂μ, m⟫_ℝ := by
    calc
      (∫ ω, ⟪Y ω, m⟫_ℝ ∂μ) = ∫ ω, ⟪m, Y ω⟫_ℝ ∂μ := by
        apply integral_congr_ae
        filter_upwards [] with ω
        exact real_inner_comm _ _
      _ = ⟪m, ∫ ω, Y ω ∂μ⟫_ℝ := integral_inner hYint m
      _ = ⟪∫ ω, Y ω ∂μ, m⟫_ℝ := real_inner_comm _ _
  change (∫ ω, ‖Y ω - m‖ ^ 2 ∂μ) = (∫ ω, ‖Y ω‖ ^ 2 ∂μ) - ‖m‖ ^ 2
  simp_rw [norm_sub_sq_real]
  calc
    (∫ ω, ‖Y ω‖ ^ 2 - 2 * ⟪Y ω, m⟫_ℝ + ‖m‖ ^ 2 ∂μ) =
        (∫ ω, ‖Y ω‖ ^ 2 - 2 * ⟪Y ω, m⟫_ℝ ∂μ) +
          ∫ _ : Ω, ‖m‖ ^ 2 ∂μ :=
      integral_add (hnorm.sub (hinner.const_mul 2)) hconst
    _ = ((∫ ω, ‖Y ω‖ ^ 2 ∂μ) - ∫ ω, 2 * ⟪Y ω, m⟫_ℝ ∂μ) +
          ∫ _ : Ω, ‖m‖ ^ 2 ∂μ := by
      rw [integral_sub hnorm (hinner.const_mul 2)]
    _ = (∫ ω, ‖Y ω‖ ^ 2 ∂μ) - ‖m‖ ^ 2 := by
      rw [integral_const_mul, hinter]
      simp [m]
      ring

/-- Common-mean Hilbert sample means have dimension-free risk `V/n`. -/
theorem integral_sampleMean_sub_commonMean_sq_le {n : ℕ} (hn : 0 < n)
    (Y : Fin n → Ω → H) (m : H) (V : ℝ) (_hV : 0 ≤ V)
    (hY : ∀ i, MemLp (Y i) 2 μ)
    (hIndep : Pairwise fun i j => IndepFun (Y i) (Y j) μ)
    (hMean : ∀ i, ∫ ω, Y i ω ∂μ = m)
    (hMoment : ∀ i, ∫ ω, ‖Y i ω‖ ^ 2 ∂μ ≤ V) :
    (∫ ω, ‖sampleMean Y ω - m‖ ^ 2 ∂μ) ≤ V / (n : ℝ) := by
  have hnR : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  have hmeanAvg : meanAverage μ Y = m := by
    unfold meanAverage
    simp_rw [hMean]
    rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin,
      ← Nat.cast_smul_eq_nsmul ℝ, smul_smul]
    field_simp [hnR]
    simp
  have hvar : ∀ i, (∫ ω, ‖Y i ω - ∫ x, Y i x ∂μ‖ ^ 2 ∂μ) ≤ V := by
    intro i
    rw [integral_centered_sq_eq μ (hY i), hMean i]
    nlinarith [hMoment i, sq_nonneg ‖m‖]
  rw [← hmeanAvg, integral_sampleMean_error_sq μ hn Y hY hIndep]
  calc
    (1 / (n : ℝ) ^ 2) *
          ∑ i, ∫ ω, ‖Y i ω - ∫ x, Y i x ∂μ‖ ^ 2 ∂μ ≤
        (1 / (n : ℝ) ^ 2) * ∑ _i : Fin n, V := by
      gcongr with i
      exact hvar i
    _ = V / (n : ℝ) := by
      simp only [Finset.sum_const, nsmul_eq_mul, Finset.card_univ, Fintype.card_fin]
      field_simp [hnR]

end SampleMean

section Batches

variable {Ω H : Type*} [MeasurableSpace Ω]
  [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
  [MeasurableSpace H] [BorelSpace H]
  (μ : Measure Ω) [IsProbabilityMeasure μ]

/-- Raw reconstruction from possibly dependent derivative-order batches. -/
def rawEstimator {m n : ℕ} (Y : Fin m → Fin n → Ω → H)
    (a : Fin m → ℝ) (b : H) : Ω → H :=
  (fun _ => b) + ∑ j, a j • sampleMean (Y j)

theorem norm_sum_sq_le_card_mul_sum_norm_sq {ι : Type*} [Fintype ι]
    (z : ι → H) :
    ‖∑ i, z i‖ ^ 2 ≤ (Fintype.card ι : ℝ) * ∑ i, ‖z i‖ ^ 2 := by
  have hnorm : ‖∑ i, z i‖ ≤ ∑ i, ‖z i‖ := norm_sum_le Finset.univ z
  calc
    ‖∑ i, z i‖ ^ 2 ≤ (∑ i, ‖z i‖) ^ 2 :=
      (sq_le_sq₀ (norm_nonneg _) (Finset.sum_nonneg fun _ _ => norm_nonneg _)).mpr hnorm
    _ = (∑ i, (1 : ℝ) * ‖z i‖) ^ 2 := by simp
    _ ≤ (∑ i : ι, (1 : ℝ) ^ 2) * ∑ i, ‖z i‖ ^ 2 :=
      Finset.sum_mul_sq_le_sq_mul_sq Finset.univ (fun _ : ι => (1 : ℝ)) (fun i => ‖z i‖)
    _ = (Fintype.card ι : ℝ) * ∑ i, ‖z i‖ ^ 2 := by simp

theorem norm_bias_add_sum_sq_le {m : ℕ} (bias : H) (e : Fin m → H) :
    ‖bias + ∑ j, e j‖ ^ 2 ≤
      (m + 1 : ℝ) * (‖bias‖ ^ 2 + ∑ j, ‖e j‖ ^ 2) := by
  let z : Option (Fin m) → H
    | none => bias
    | some j => e j
  have h := norm_sum_sq_le_card_mul_sum_norm_sq (H := H) z
  simpa [z, Fintype.sum_option, Fintype.card_option, Nat.cast_add,
    Nat.cast_one] using h

theorem rawEstimator_sub_eq {m n : ℕ} (Y : Fin m → Fin n → Ω → H)
    (a : Fin m → ℝ) (b c : H) (h : Fin m → H) (ω : Ω) :
    rawEstimator Y a b ω - c =
      (b + ∑ j, a j • h j - c) +
        ∑ j, a j • (sampleMean (Y j) ω - h j) := by
  simp only [rawEstimator, Pi.add_apply, Finset.sum_apply, Pi.smul_apply,
    smul_sub, Finset.sum_sub_distrib]
  abel

theorem rawEstimator_memLp {m n : ℕ} (Y : Fin m → Fin n → Ω → H)
    (a : Fin m → ℝ) (b : H)
    (hY : ∀ j i, MemLp (Y j i) 2 μ) :
    MemLp (rawEstimator Y a b) 2 μ := by
  unfold rawEstimator
  exact (memLp_const b).add (memLp_finsetSum' Finset.univ fun j _ =>
    (sampleMean_memLp μ (Y j) (hY j)).const_smul (a j))

theorem rawEstimator_aestronglyMeasurable {m n : ℕ}
    (Y : Fin m → Fin n → Ω → H) (a : Fin m → ℝ) (b : H)
    (hY : ∀ j i, MemLp (Y j i) 2 μ) :
    AEStronglyMeasurable (rawEstimator Y a b) μ :=
  (rawEstimator_memLp μ Y a b hY).1

theorem rawEstimator_sub_memLp {m n : ℕ} (Y : Fin m → Fin n → Ω → H)
    (a : Fin m → ℝ) (b c : H)
    (hY : ∀ j i, MemLp (Y j i) 2 μ) :
    MemLp (fun ω => rawEstimator Y a b ω - c) 2 μ := by
  exact (rawEstimator_memLp μ Y a b hY).sub (memLp_const c)

theorem rawEstimator_sub_sqNorm_integrable {m n : ℕ}
    (Y : Fin m → Fin n → Ω → H) (a : Fin m → ℝ) (b c : H)
    (hY : ∀ j i, MemLp (Y j i) 2 μ) :
    Integrable (fun ω => ‖rawEstimator Y a b ω - c‖ ^ 2) μ :=
  (rawEstimator_sub_memLp μ Y a b c hY).integrable_norm_pow'

theorem rawEstimator_pointwise_sq_le {m n : ℕ}
    (Y : Fin m → Fin n → Ω → H) (a : Fin m → ℝ) (b c : H)
    (h : Fin m → H) (ω : Ω) :
    ‖rawEstimator Y a b ω - c‖ ^ 2 ≤
      (m + 1 : ℝ) *
        (‖b + ∑ j, a j • h j - c‖ ^ 2 +
          ∑ j, (a j) ^ 2 * ‖sampleMean (Y j) ω - h j‖ ^ 2) := by
  rw [rawEstimator_sub_eq Y a b c h ω]
  calc
    ‖(b + ∑ j, a j • h j - c) +
        ∑ j, a j • (sampleMean (Y j) ω - h j)‖ ^ 2 ≤
      (m + 1 : ℝ) *
        (‖b + ∑ j, a j • h j - c‖ ^ 2 +
          ∑ j, ‖a j • (sampleMean (Y j) ω - h j)‖ ^ 2) :=
      norm_bias_add_sum_sq_le (H := H) _ _
    _ = _ := by
      congr 2
      apply Finset.sum_congr rfl
      intro j hj
      rw [norm_smul, Real.norm_eq_abs, mul_pow, sq_abs]

/-- Multiple batches may be mutually dependent; only within-batch pairwise
independence is used. -/
theorem rawEstimator_risk_le {m n : ℕ} (hn : 0 < n)
    (Y : Fin m → Fin n → Ω → H) (h : Fin m → H)
    (V : Fin m → ℝ) (a : Fin m → ℝ) (b c : H) (β : ℝ)
    (hβ : 0 ≤ β) (hV : ∀ j, 0 ≤ V j)
    (hY : ∀ j i, MemLp (Y j i) 2 μ)
    (hIndep : ∀ j, Pairwise fun i k => IndepFun (Y j i) (Y j k) μ)
    (hMean : ∀ j i, ∫ ω, Y j i ω ∂μ = h j)
    (hMoment : ∀ j i, ∫ ω, ‖Y j i ω‖ ^ 2 ∂μ ≤ V j)
    (hBias : ‖b + ∑ j, a j • h j - c‖ ≤ β) :
    (∫ ω, ‖rawEstimator Y a b ω - c‖ ^ 2 ∂μ) ≤
      (m + 1 : ℝ) * (β ^ 2 + ∑ j, (a j) ^ 2 * V j / (n : ℝ)) := by
  let bias : H := b + ∑ j, a j • h j - c
  have hbatchMem : ∀ j, MemLp (fun ω => sampleMean (Y j) ω - h j) 2 μ := by
    intro j
    exact (sampleMean_memLp μ (Y j) (hY j)).sub (memLp_const (h j))
  have hbatchInt : ∀ j,
      Integrable (fun ω => ‖sampleMean (Y j) ω - h j‖ ^ 2) μ := by
    intro j
    exact (hbatchMem j).integrable_norm_pow'
  have hweightedInt : ∀ j,
      Integrable (fun ω => (a j) ^ 2 * ‖sampleMean (Y j) ω - h j‖ ^ 2) μ := by
    intro j
    exact (hbatchInt j).const_mul ((a j) ^ 2)
  have hsumInt : Integrable
      (fun ω => ∑ j, (a j) ^ 2 * ‖sampleMean (Y j) ω - h j‖ ^ 2) μ :=
    integrable_finsetSum Finset.univ fun j _ => hweightedInt j
  have hbiasInt : Integrable (fun _ : Ω => ‖bias‖ ^ 2) μ := integrable_const _
  have hinsideInt : Integrable
      (fun ω => ‖bias‖ ^ 2 +
        ∑ j, (a j) ^ 2 * ‖sampleMean (Y j) ω - h j‖ ^ 2) μ :=
    hbiasInt.add hsumInt
  have hrhsInt : Integrable
      (fun ω => (m + 1 : ℝ) * (‖bias‖ ^ 2 +
        ∑ j, (a j) ^ 2 * ‖sampleMean (Y j) ω - h j‖ ^ 2)) μ :=
    hinsideInt.const_mul (m + 1 : ℝ)
  have hpoint : ∀ ω,
      ‖rawEstimator Y a b ω - c‖ ^ 2 ≤
        (m + 1 : ℝ) * (‖bias‖ ^ 2 +
          ∑ j, (a j) ^ 2 * ‖sampleMean (Y j) ω - h j‖ ^ 2) := by
    intro ω
    exact rawEstimator_pointwise_sq_le Y a b c h ω
  have hrawInt := rawEstimator_sub_sqNorm_integrable μ Y a b c hY
  calc
    (∫ ω, ‖rawEstimator Y a b ω - c‖ ^ 2 ∂μ) ≤
        ∫ ω, (m + 1 : ℝ) * (‖bias‖ ^ 2 +
          ∑ j, (a j) ^ 2 * ‖sampleMean (Y j) ω - h j‖ ^ 2) ∂μ :=
      integral_mono hrawInt hrhsInt hpoint
    _ = (m + 1 : ℝ) * (‖bias‖ ^ 2 +
        ∑ j, (a j) ^ 2 *
          ∫ ω, ‖sampleMean (Y j) ω - h j‖ ^ 2 ∂μ) := by
      rw [integral_const_mul]
      rw [integral_add hbiasInt hsumInt]
      rw [integral_finsetSum Finset.univ]
      · simp_rw [integral_const_mul]
        simp
      · intro j hj
        exact hweightedInt j
    _ ≤ (m + 1 : ℝ) * (β ^ 2 +
        ∑ j, (a j) ^ 2 * (V j / (n : ℝ))) := by
      apply mul_le_mul_of_nonneg_left _ (by positivity)
      apply add_le_add
      · exact (sq_le_sq₀ (norm_nonneg bias) hβ).mpr hBias
      · apply Finset.sum_le_sum
        intro j hj
        exact mul_le_mul_of_nonneg_left
          (integral_sampleMean_sub_commonMean_sq_le μ hn (Y j) (h j) (V j)
            (hV j) (hY j) (hIndep j) (hMean j) (hMoment j))
          (sq_nonneg (a j))
    _ = (m + 1 : ℝ) * (β ^ 2 + ∑ j, (a j) ^ 2 * V j / (n : ℝ)) := by
      congr 2
      apply Finset.sum_congr rfl
      intro j hj
      ring

end Batches

section Transfer

variable {Ω H : Type*} [MeasurableSpace Ω]
  [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
  [MeasurableSpace H] [BorelSpace H]
  (μ : Measure Ω) [IsProbabilityMeasure μ]

theorem anchored_rawEstimator_sub_memLp {m n : ℕ}
    (Y : Fin m → Fin n → Ω → H) (a : Fin m → ℝ) (b c : H)
    (hY : ∀ j i, MemLp (Y j i) 2 μ)
    (K : H → H) (hKcont : Continuous K)
    (hK : ∀ z, ‖K z - c‖ ≤ ‖z - c‖) :
    MemLp (fun ω => K (rawEstimator Y a b ω) - c) 2 μ := by
  have hraw : MemLp (fun ω => rawEstimator Y a b ω - c) 2 μ :=
    rawEstimator_sub_memLp μ Y a b c hY
  have hrawMeas : AEStronglyMeasurable (rawEstimator Y a b) μ :=
    rawEstimator_aestronglyMeasurable μ Y a b hY
  have htargetMeas : AEStronglyMeasurable
      (fun ω => K (rawEstimator Y a b ω) - c) μ :=
    (hKcont.comp_aestronglyMeasurable hrawMeas).sub aestronglyMeasurable_const
  exact hraw.mono htargetMeas (ae_of_all μ fun ω => hK _)

theorem anchored_rawEstimator_sqNorm_integrable {m n : ℕ}
    (Y : Fin m → Fin n → Ω → H) (a : Fin m → ℝ) (b c : H)
    (hY : ∀ j i, MemLp (Y j i) 2 μ)
    (K : H → H) (hKcont : Continuous K)
    (hK : ∀ z, ‖K z - c‖ ≤ ‖z - c‖) :
    Integrable (fun ω => ‖K (rawEstimator Y a b ω) - c‖ ^ 2) μ :=
  (anchored_rawEstimator_sub_memLp μ Y a b c hY K hKcont hK).integrable_norm_pow'

/-- A continuous contraction anchored at the target transfers the raw bound;
the bound is derived from the sample hypotheses. -/
theorem anchored_rawEstimator_risk_le {m n : ℕ} (hn : 0 < n)
    (Y : Fin m → Fin n → Ω → H) (h : Fin m → H)
    (V : Fin m → ℝ) (a : Fin m → ℝ) (b c : H) (β : ℝ)
    (hβ : 0 ≤ β) (hV : ∀ j, 0 ≤ V j)
    (hY : ∀ j i, MemLp (Y j i) 2 μ)
    (hIndep : ∀ j, Pairwise fun i k => IndepFun (Y j i) (Y j k) μ)
    (hMean : ∀ j i, ∫ ω, Y j i ω ∂μ = h j)
    (hMoment : ∀ j i, ∫ ω, ‖Y j i ω‖ ^ 2 ∂μ ≤ V j)
    (hBias : ‖b + ∑ j, a j • h j - c‖ ≤ β)
    (K : H → H) (hKcont : Continuous K)
    (hK : ∀ z, ‖K z - c‖ ≤ ‖z - c‖) :
    (∫ ω, ‖K (rawEstimator Y a b ω) - c‖ ^ 2 ∂μ) ≤
      (m + 1 : ℝ) * (β ^ 2 + ∑ j, (a j) ^ 2 * V j / (n : ℝ)) := by
  have hKint := anchored_rawEstimator_sqNorm_integrable μ Y a b c hY K hKcont hK
  have hrawInt := rawEstimator_sub_sqNorm_integrable μ Y a b c hY
  calc
    (∫ ω, ‖K (rawEstimator Y a b ω) - c‖ ^ 2 ∂μ) ≤
        ∫ ω, ‖rawEstimator Y a b ω - c‖ ^ 2 ∂μ := by
      apply integral_mono hKint hrawInt
      intro ω
      exact (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).mpr (hK _)
    _ ≤ (m + 1 : ℝ) * (β ^ 2 + ∑ j, (a j) ^ 2 * V j / (n : ℝ)) :=
      rawEstimator_risk_le μ hn Y h V a b c β hβ hV hY hIndep hMean hMoment hBias

end Transfer

section Box

/-- Coordinatewise clipping to a deterministic Euclidean box. -/
def boxClip {I : Type*} [Fintype I] (l u : I → ℝ)
    (z : EuclideanSpace ℝ I) : EuclideanSpace ℝ I :=
  WithLp.toLp 2 (fun i => max (l i) (min (u i) (z i)))

theorem boxClip_apply {I : Type*} [Fintype I] (l u : I → ℝ)
    (z : EuclideanSpace ℝ I) (i : I) :
    boxClip l u z i = max (l i) (min (u i) (z i)) := by
  rfl

private theorem clip_sq_le (l u c z : ℝ) (hlc : l ≤ c) (hcu : c ≤ u) :
    (max l (min u z) - c) ^ 2 ≤ (z - c) ^ 2 := by
  by_cases hlz : l ≤ z
  · by_cases hzu : z ≤ u
    · rw [min_eq_right hzu, max_eq_right hlz]
    · have huz : u ≤ z := le_of_not_ge hzu
      have hlu : l ≤ u := hlc.trans hcu
      rw [min_eq_left huz, max_eq_right hlu]
      nlinarith
  · have hzl : z ≤ l := le_of_not_ge hlz
    have hzu : z ≤ u := hzl.trans (hlc.trans hcu)
    rw [min_eq_right hzu, max_eq_left hzl]
    nlinarith

theorem boxClip_fixed {I : Type*} [Fintype I] (l u : I → ℝ)
    (c : EuclideanSpace ℝ I) (hlc : ∀ i, l i ≤ c i) (hcu : ∀ i, c i ≤ u i) :
    boxClip l u c = c := by
  ext i
  simp [boxClip, min_eq_right (hcu i), max_eq_right (hlc i)]

theorem boxClip_continuous {I : Type*} [Fintype I] (l u : I → ℝ) :
    Continuous (boxClip l u) := by
  unfold boxClip
  fun_prop

theorem boxClip_sub_sqNorm_le {I : Type*} [Fintype I] (l u : I → ℝ)
    (c z : EuclideanSpace ℝ I) (hlc : ∀ i, l i ≤ c i) (hcu : ∀ i, c i ≤ u i) :
    ‖boxClip l u z - c‖ ^ 2 ≤ ‖z - c‖ ^ 2 := by
  rw [EuclideanSpace.real_norm_sq_eq, EuclideanSpace.real_norm_sq_eq]
  apply Finset.sum_le_sum
  intro i hi
  simpa [boxClip] using clip_sq_le (l i) (u i) (c i) (z i) (hlc i) (hcu i)

theorem boxClip_sub_norm_le {I : Type*} [Fintype I] (l u : I → ℝ)
    (c z : EuclideanSpace ℝ I) (hlc : ∀ i, l i ≤ c i) (hcu : ∀ i, c i ≤ u i) :
    ‖boxClip l u z - c‖ ≤ ‖z - c‖ := by
  exact (sq_le_sq₀ (norm_nonneg _) (norm_nonneg _)).mp
    (boxClip_sub_sqNorm_le l u c z hlc hcu)

/-- Actual coordinate clipping transfers the dependent-batch raw risk. -/
theorem boxClip_rawEstimator_risk_le {Ω I : Type*} [MeasurableSpace Ω]
    [Fintype I] [MeasurableSpace (EuclideanSpace ℝ I)]
    [BorelSpace (EuclideanSpace ℝ I)]
    (μ : Measure Ω) [IsProbabilityMeasure μ]
    {m n : ℕ} (hn : 0 < n)
    (Y : Fin m → Fin n → Ω → EuclideanSpace ℝ I)
    (h : Fin m → EuclideanSpace ℝ I) (V : Fin m → ℝ)
    (a : Fin m → ℝ) (b c : EuclideanSpace ℝ I) (β : ℝ)
    (hβ : 0 ≤ β) (hV : ∀ j, 0 ≤ V j)
    (hY : ∀ j i, MemLp (Y j i) 2 μ)
    (hIndep : ∀ j, Pairwise fun i k => IndepFun (Y j i) (Y j k) μ)
    (hMean : ∀ j i, ∫ ω, Y j i ω ∂μ = h j)
    (hMoment : ∀ j i, ∫ ω, ‖Y j i ω‖ ^ 2 ∂μ ≤ V j)
    (hBias : ‖b + ∑ j, a j • h j - c‖ ≤ β)
    (l u : I → ℝ) (hlc : ∀ i, l i ≤ c i) (hcu : ∀ i, c i ≤ u i) :
    (∫ ω, ‖boxClip l u (rawEstimator Y a b ω) - c‖ ^ 2 ∂μ) ≤
      (m + 1 : ℝ) * (β ^ 2 + ∑ j, (a j) ^ 2 * V j / (n : ℝ)) := by
  exact anchored_rawEstimator_risk_le μ hn Y h V a b c β hβ hV hY hIndep hMean
    hMoment hBias (boxClip l u) (boxClip_continuous l u)
    (fun z => boxClip_sub_norm_le l u c z hlc hcu)

end Box

section LinearTransfer

variable {Ω H G : Type*} [MeasurableSpace Ω]
  [NormedAddCommGroup H] [InnerProductSpace ℝ H] [CompleteSpace H]
  [MeasurableSpace H] [BorelSpace H]
  [NormedAddCommGroup G] [NormedSpace ℝ G]
  (μ : Measure Ω) [IsProbabilityMeasure μ]

theorem boundedLinear_anchored_sub_memLp {m n : ℕ}
    (Y : Fin m → Fin n → Ω → H) (a : Fin m → ℝ) (b c : H)
    (hY : ∀ j i, MemLp (Y j i) 2 μ)
    (K : H → H) (hKcont : Continuous K)
    (hK : ∀ z, ‖K z - c‖ ≤ ‖z - c‖) (A : H →L[ℝ] G) :
    MemLp (fun ω => A (K (rawEstimator Y a b ω)) - A c) 2 μ := by
  have hbase := anchored_rawEstimator_sub_memLp μ Y a b c hY K hKcont hK
  have himage := hbase.continuousLinearMap_comp A
  exact (memLp_congr_ae (ae_of_all μ fun ω => by simp)).2 himage

theorem boundedLinear_anchored_sqNorm_integrable {m n : ℕ}
    (Y : Fin m → Fin n → Ω → H) (a : Fin m → ℝ) (b c : H)
    (hY : ∀ j i, MemLp (Y j i) 2 μ)
    (K : H → H) (hKcont : Continuous K)
    (hK : ∀ z, ‖K z - c‖ ≤ ‖z - c‖) (A : H →L[ℝ] G) :
    Integrable (fun ω => ‖A (K (rawEstimator Y a b ω)) - A c‖ ^ 2) μ :=
  (boundedLinear_anchored_sub_memLp μ Y a b c hY K hKcont hK A).integrable_norm_pow'

/-- Strong-norm risk transfer through an actual bounded linear operator. -/
theorem boundedLinear_anchored_risk_le {m n : ℕ} (hn : 0 < n)
    (Y : Fin m → Fin n → Ω → H) (h : Fin m → H)
    (V : Fin m → ℝ) (a : Fin m → ℝ) (b c : H) (β : ℝ)
    (hβ : 0 ≤ β) (hV : ∀ j, 0 ≤ V j)
    (hY : ∀ j i, MemLp (Y j i) 2 μ)
    (hIndep : ∀ j, Pairwise fun i k => IndepFun (Y j i) (Y j k) μ)
    (hMean : ∀ j i, ∫ ω, Y j i ω ∂μ = h j)
    (hMoment : ∀ j i, ∫ ω, ‖Y j i ω‖ ^ 2 ∂μ ≤ V j)
    (hBias : ‖b + ∑ j, a j • h j - c‖ ≤ β)
    (K : H → H) (hKcont : Continuous K)
    (hK : ∀ z, ‖K z - c‖ ≤ ‖z - c‖) (A : H →L[ℝ] G) :
    (∫ ω, ‖A (K (rawEstimator Y a b ω)) - A c‖ ^ 2 ∂μ) ≤
      ‖A‖ ^ 2 * (m + 1 : ℝ) *
        (β ^ 2 + ∑ j, (a j) ^ 2 * V j / (n : ℝ)) := by
  have hAint := boundedLinear_anchored_sqNorm_integrable μ Y a b c hY K hKcont hK A
  have hKint := anchored_rawEstimator_sqNorm_integrable μ Y a b c hY K hKcont hK
  have hpoint : ∀ ω,
      ‖A (K (rawEstimator Y a b ω)) - A c‖ ^ 2 ≤
        ‖A‖ ^ 2 * ‖K (rawEstimator Y a b ω) - c‖ ^ 2 := by
    intro ω
    rw [← A.map_sub]
    calc
      ‖A (K (rawEstimator Y a b ω) - c)‖ ^ 2 ≤
          (‖A‖ * ‖K (rawEstimator Y a b ω) - c‖) ^ 2 :=
        (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (norm_nonneg _) (norm_nonneg _))).mpr
          (A.le_opNorm _)
      _ = ‖A‖ ^ 2 * ‖K (rawEstimator Y a b ω) - c‖ ^ 2 := by ring
  calc
    (∫ ω, ‖A (K (rawEstimator Y a b ω)) - A c‖ ^ 2 ∂μ) ≤
        ∫ ω, ‖A‖ ^ 2 * ‖K (rawEstimator Y a b ω) - c‖ ^ 2 ∂μ := by
      apply integral_mono hAint (hKint.const_mul (‖A‖ ^ 2)) hpoint
    _ = ‖A‖ ^ 2 *
        ∫ ω, ‖K (rawEstimator Y a b ω) - c‖ ^ 2 ∂μ := by
      rw [integral_const_mul]
    _ ≤ ‖A‖ ^ 2 * ((m + 1 : ℝ) *
        (β ^ 2 + ∑ j, (a j) ^ 2 * V j / (n : ℝ))) := by
      exact mul_le_mul_of_nonneg_left
        (anchored_rawEstimator_risk_le μ hn Y h V a b c β hβ hV hY hIndep hMean
          hMoment hBias K hKcont hK)
        (sq_nonneg ‖A‖)
    _ = ‖A‖ ^ 2 * (m + 1 : ℝ) *
        (β ^ 2 + ∑ j, (a j) ^ 2 * V j / (n : ℝ)) := by ring

end LinearTransfer

end

end EstimatorIntegrity.HilbertSamplingRisk
