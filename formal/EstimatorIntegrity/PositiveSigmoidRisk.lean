import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.SpecialFunctions.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Tactic

/-!
# Positive sigmoid transform and probability-space risk

This module formalizes the scalar transform used in the positive-data query
upper bound.  It proves the anchored pointwise estimate, its actual integral
loss consequence on an arbitrary probability space, and the exact
`25 / 1024` bias-composition constant.

It does not formalize the PDE approximation, the height-versus-mass
interpolation estimate, iid sampling, or the sample-mean variance bound.
-/

open MeasureTheory

namespace EstimatorIntegrity

noncomputable section

/-- The positive scalar sigmoid `z / sqrt (1 + z²)`. -/
def positiveSigmoid (z : ℝ) : ℝ :=
  z / Real.sqrt (1 + z ^ 2)

/-- The positive sigmoid is continuous on the real line. -/
theorem continuous_positiveSigmoid : Continuous positiveSigmoid := by
  unfold positiveSigmoid
  apply Continuous.div continuous_id
    (continuous_const.add (continuous_id.pow 2)).sqrt
  intro z
  change Real.sqrt (1 + z ^ 2) ≠ 0
  exact ne_of_gt (Real.sqrt_pos.2 (by nlinarith [sq_nonneg z]))

/-- The sigmoid is nonnegative on the nonnegative half-line. -/
theorem positiveSigmoid_nonneg {z : ℝ} (hz : 0 ≤ z) :
    0 ≤ positiveSigmoid z := by
  exact div_nonneg hz (Real.sqrt_nonneg _)

/-- The sigmoid is at most one on the nonnegative half-line. -/
theorem positiveSigmoid_le_one {z : ℝ} (hz : 0 ≤ z) :
    positiveSigmoid z ≤ 1 := by
  unfold positiveSigmoid
  have hrad : 0 ≤ 1 + z ^ 2 := by nlinarith [sq_nonneg z]
  have hsqrt_pos : 0 < Real.sqrt (1 + z ^ 2) := Real.sqrt_pos.2 (by nlinarith [sq_nonneg z])
  apply (div_le_one hsqrt_pos).2
  nlinarith [Real.sq_sqrt hrad, Real.sqrt_nonneg (1 + z ^ 2)]

/-- The positive sigmoid is monotone when both arguments are nonnegative. -/
theorem positiveSigmoid_mono_nonneg {x z : ℝ} (hx : 0 ≤ x) (hz : 0 ≤ z)
    (hxz : x ≤ z) : positiveSigmoid x ≤ positiveSigmoid z := by
  unfold positiveSigmoid
  have hxrad : 0 ≤ 1 + x ^ 2 := by nlinarith [sq_nonneg x]
  have hzrad : 0 ≤ 1 + z ^ 2 := by nlinarith [sq_nonneg z]
  have hsx_pos : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.2 (by nlinarith [sq_nonneg x])
  have hsz_pos : 0 < Real.sqrt (1 + z ^ 2) := Real.sqrt_pos.2 (by nlinarith [sq_nonneg z])
  apply (sq_le_sq₀ (div_nonneg hx hsx_pos.le) (div_nonneg hz hsz_pos.le)).1
  rw [div_pow, div_pow, Real.sq_sqrt hxrad, Real.sq_sqrt hzrad]
  apply (div_le_div_iff₀ (by positivity) (by positivity)).2
  nlinarith [sq_nonneg x, sq_nonneg z]

/-- For nonnegative `x,z`, the change in the sigmoid is controlled by the
distance to the anchor `z`, with the denominator evaluated at that anchor. -/
theorem positiveSigmoid_anchored {x z : ℝ} (hx : 0 ≤ x) (hz : 0 ≤ z) :
    |positiveSigmoid x - positiveSigmoid z| ≤
      |x - z| / Real.sqrt (1 + z ^ 2) := by
  have hxrad : 0 ≤ 1 + x ^ 2 := by nlinarith [sq_nonneg x]
  have hzrad : 0 ≤ 1 + z ^ 2 := by nlinarith [sq_nonneg z]
  have hsx_pos : 0 < Real.sqrt (1 + x ^ 2) := Real.sqrt_pos.2 (by nlinarith [sq_nonneg x])
  have hsz_pos : 0 < Real.sqrt (1 + z ^ 2) := Real.sqrt_pos.2 (by nlinarith [sq_nonneg z])
  rcases le_total x z with hxz | hzx
  · have hmono := positiveSigmoid_mono_nonneg hx hz hxz
    rw [abs_of_nonpos (sub_nonpos.2 hmono), abs_of_nonpos (sub_nonpos.2 hxz)]
    simp only [neg_sub]
    have hsqrt_le : Real.sqrt (1 + x ^ 2) ≤ Real.sqrt (1 + z ^ 2) :=
      Real.sqrt_le_sqrt (by nlinarith [sq_nonneg x, sq_nonneg z])
    have hratio : x / Real.sqrt (1 + z ^ 2) ≤ positiveSigmoid x := by
      unfold positiveSigmoid
      exact div_le_div_of_nonneg_left hx hsx_pos hsqrt_le
    unfold positiveSigmoid at hmono ⊢
    calc
      z / Real.sqrt (1 + z ^ 2) - x / Real.sqrt (1 + x ^ 2) ≤
          z / Real.sqrt (1 + z ^ 2) - x / Real.sqrt (1 + z ^ 2) :=
        sub_le_sub_left hratio _
      _ = (z - x) / Real.sqrt (1 + z ^ 2) := by ring
  · have hmono := positiveSigmoid_mono_nonneg hz hx hzx
    rw [abs_of_nonneg (sub_nonneg.2 hmono), abs_of_nonneg (sub_nonneg.2 hzx)]
    have hsqrt_le : Real.sqrt (1 + z ^ 2) ≤ Real.sqrt (1 + x ^ 2) :=
      Real.sqrt_le_sqrt (by nlinarith [sq_nonneg x, sq_nonneg z])
    have hratio : positiveSigmoid x ≤ x / Real.sqrt (1 + z ^ 2) := by
      unfold positiveSigmoid
      exact div_le_div_of_nonneg_left hx hsz_pos hsqrt_le
    unfold positiveSigmoid at hmono ⊢
    calc
      x / Real.sqrt (1 + x ^ 2) - z / Real.sqrt (1 + z ^ 2) ≤
          x / Real.sqrt (1 + z ^ 2) - z / Real.sqrt (1 + z ^ 2) :=
        sub_le_sub_right hratio _
      _ = (x - z) / Real.sqrt (1 + z ^ 2) := by ring

/-- On a probability space, every squared loss of the transformed measurable
nonnegative random variable against a fixed real target is integrable. -/
theorem positiveSigmoid_squaredLoss_integrable
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : Ω → ℝ) (hX : Measurable X) (hX_nonneg : ∀ ω, 0 ≤ X ω) (target : ℝ) :
    Integrable (fun ω => (positiveSigmoid (X ω) - target) ^ 2) μ := by
  have hpsi_meas : Measurable (fun ω => positiveSigmoid (X ω)) :=
    continuous_positiveSigmoid.measurable.comp hX
  have hloss_meas : AEStronglyMeasurable
      (fun ω => (positiveSigmoid (X ω) - target) ^ 2) μ :=
    ((hpsi_meas.sub measurable_const).pow_const 2).aestronglyMeasurable
  refine Integrable.mono' (integrable_const ((1 + |target|) ^ 2)) hloss_meas ?_
  filter_upwards with ω
  have hnonneg := positiveSigmoid_nonneg (hX_nonneg ω)
  have hle := positiveSigmoid_le_one (hX_nonneg ω)
  have habs : |positiveSigmoid (X ω) - target| ≤ 1 + |target| := by
    calc
      |positiveSigmoid (X ω) - target| ≤
          |positiveSigmoid (X ω)| + |target| := abs_sub _ _
      _ = positiveSigmoid (X ω) + |target| := by rw [abs_of_nonneg hnonneg]
      _ ≤ 1 + |target| := by
        simpa [add_comm] using add_le_add_right hle |target|
  simp only [Real.norm_eq_abs, abs_pow]
  exact (sq_le_sq₀ (abs_nonneg _) (by positivity)).2 habs

/-- Cauchy--Schwarz on a probability space, in the exact form needed for
bias composition. -/
theorem integral_abs_le_sqrt_integral_sq
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (F : Ω → ℝ) (hF : AEStronglyMeasurable F μ)
    (hFsq : Integrable (fun ω => F ω ^ 2) μ) :
    (∫ ω, |F ω| ∂μ) ≤ Real.sqrt (∫ ω, F ω ^ 2 ∂μ) := by
  have hF_L2 : MemLp F 2 μ := (memLp_two_iff_integrable_sq hF).2 hFsq
  have habs_L2 : MemLp (fun ω => |F ω|) 2 μ := by
    simpa only [Real.norm_eq_abs] using hF_L2.norm
  have hone_L2 : MemLp (fun _ : Ω => (1 : ℝ)) 2 μ :=
    (memLp_two_iff_integrable_sq (by fun_prop)).2 (by
      simpa only [one_pow] using (integrable_const (μ := μ) (1 : ℝ)))
  have hcs := integral_mul_le_Lp_mul_Lq_of_nonneg Real.HolderConjugate.two_two
    (μ := μ) (f := fun ω => |F ω|) (g := fun _ : Ω => (1 : ℝ))
    (Filter.Eventually.of_forall fun ω => abs_nonneg (F ω))
    (Filter.Eventually.of_forall fun _ => zero_le_one)
    (by simpa using habs_L2) (by simpa using hone_L2)
  have habs_sq : (∫ ω, |F ω| ^ 2 ∂μ) = ∫ ω, F ω ^ 2 ∂μ := by
    apply integral_congr_ae
    exact Filter.Eventually.of_forall fun ω => sq_abs (F ω)
  have hcs' : (∫ ω, |F ω| ∂μ) ≤ (∫ ω, |F ω| ^ 2 ∂μ) ^ (1 / 2 : ℝ) := by
    simpa only [Real.rpow_two, mul_one, one_pow, integral_const, measureReal_def,
      measure_univ, ENNReal.toReal_one, one_smul, Real.one_rpow] using hcs
  calc
    (∫ ω, |F ω| ∂μ) ≤ (∫ ω, |F ω| ^ 2 ∂μ) ^ (1 / 2 : ℝ) := hcs'
    _ = Real.sqrt (∫ ω, F ω ^ 2 ∂μ) := by
      rw [habs_sq, ← Real.sqrt_eq_rpow]

/-- The actual transformed integral loss is bounded by the anchored raw
squared deviation on an arbitrary probability space. -/
theorem positiveSigmoid_integral_loss_le
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : Ω → ℝ) (z : ℝ) (hX : Measurable X) (hX_nonneg : ∀ ω, 0 ≤ X ω)
    (hz : 0 ≤ z) (hdev : Integrable (fun ω => (X ω - z) ^ 2) μ) :
    (∫ ω, (positiveSigmoid (X ω) - positiveSigmoid z) ^ 2 ∂μ) ≤
      (∫ ω, (X ω - z) ^ 2 ∂μ) / (1 + z ^ 2) := by
  have hloss := positiveSigmoid_squaredLoss_integrable μ X hX hX_nonneg
    (positiveSigmoid z)
  have hright : Integrable (fun ω => (X ω - z) ^ 2 / (1 + z ^ 2)) μ :=
    hdev.mul_const (1 / (1 + z ^ 2)) |>.congr (by
      filter_upwards with ω
      ring)
  calc
    (∫ ω, (positiveSigmoid (X ω) - positiveSigmoid z) ^ 2 ∂μ) ≤
        ∫ ω, (X ω - z) ^ 2 / (1 + z ^ 2) ∂μ := by
      apply integral_mono hloss hright
      intro ω
      have hanchor := positiveSigmoid_anchored (hX_nonneg ω) hz
      have hsquare := (sq_le_sq₀ (abs_nonneg _)
        (div_nonneg (abs_nonneg _) (Real.sqrt_nonneg _))).2 hanchor
      calc
        (positiveSigmoid (X ω) - positiveSigmoid z) ^ 2 =
            |positiveSigmoid (X ω) - positiveSigmoid z| ^ 2 := (sq_abs _).symm
        _ ≤ (|X ω - z| / Real.sqrt (1 + z ^ 2)) ^ 2 := hsquare
        _ = (X ω - z) ^ 2 / (1 + z ^ 2) := by
          rw [div_pow, sq_abs, Real.sq_sqrt (by nlinarith [sq_nonneg z])]
    _ = (∫ ω, (X ω - z) ^ 2 ∂μ) / (1 + z ^ 2) :=
      integral_div _ _

/-- If the transformed mean-square loss is at most `1/64` and the
deterministic target bias is at most `1/32`, then the actual total
mean-square loss is at most `25/1024`. -/
theorem positiveSigmoid_bias_composition
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (X : Ω → ℝ) (z y : ℝ) (hX : Measurable X) (hX_nonneg : ∀ ω, 0 ≤ X ω)
    (_hz : 0 ≤ z)
    (htransformed : (∫ ω, (positiveSigmoid (X ω) - positiveSigmoid z) ^ 2 ∂μ) ≤
      (1 : ℝ) / 64)
    (hbias : |y - positiveSigmoid z| ≤ (1 : ℝ) / 32) :
    (∫ ω, (positiveSigmoid (X ω) - y) ^ 2 ∂μ) ≤ (25 : ℝ) / 1024 := by
  let F : Ω → ℝ := fun ω => positiveSigmoid (X ω) - positiveSigmoid z
  let b : ℝ := positiveSigmoid z - y
  have hpsi_meas : Measurable (fun ω => positiveSigmoid (X ω)) :=
    continuous_positiveSigmoid.measurable.comp hX
  have hF_meas : Measurable F := by
    dsimp [F]
    exact hpsi_meas.sub measurable_const
  have hFsq : Integrable (fun ω => F ω ^ 2) μ := by
    simpa [F] using positiveSigmoid_squaredLoss_integrable μ X hX hX_nonneg
      (positiveSigmoid z)
  have hF_L2 : MemLp F 2 μ :=
    (memLp_two_iff_integrable_sq hF_meas.aestronglyMeasurable).2 hFsq
  have hF_int : Integrable F μ := hF_L2.integrable (by norm_num)
  have hFabs_int : Integrable (fun ω => |F ω|) μ := hF_int.abs
  have hCauchy := integral_abs_le_sqrt_integral_sq μ F
    hF_meas.aestronglyMeasurable hFsq
  have hF_mse : (∫ ω, F ω ^ 2 ∂μ) ≤ (1 : ℝ) / 64 := by
    simpa [F] using htransformed
  have hF_mse_nonneg : 0 ≤ ∫ ω, F ω ^ 2 ∂μ :=
    integral_nonneg fun ω => sq_nonneg (F ω)
  have hsqrt_le : Real.sqrt (∫ ω, F ω ^ 2 ∂μ) ≤ (1 : ℝ) / 8 := by
    nlinarith [Real.sq_sqrt hF_mse_nonneg,
      Real.sqrt_nonneg (∫ ω, F ω ^ 2 ∂μ)]
  have hFabs_mean : (∫ ω, |F ω| ∂μ) ≤ (1 : ℝ) / 8 := hCauchy.trans hsqrt_le
  have hFabs_mean_nonneg : 0 ≤ ∫ ω, |F ω| ∂μ :=
    integral_nonneg fun ω => abs_nonneg (F ω)
  have hb_abs : |b| ≤ (1 : ℝ) / 32 := by
    simpa [b, abs_sub_comm] using hbias
  have hb_sq : b ^ 2 ≤ (1 : ℝ) / 1024 := by
    have hsquare := (sq_le_sq₀ (abs_nonneg b) (by norm_num : (0 : ℝ) ≤ 1 / 32)).2 hb_abs
    nlinarith [sq_abs b]
  have hcross : 2 * |b| * (∫ ω, |F ω| ∂μ) ≤ (1 : ℝ) / 128 := by
    calc
      2 * |b| * (∫ ω, |F ω| ∂μ) ≤
          2 * ((1 : ℝ) / 32) * (∫ ω, |F ω| ∂μ) := by gcongr
      _ ≤ 2 * ((1 : ℝ) / 32) * ((1 : ℝ) / 8) := by gcongr
      _ = (1 : ℝ) / 128 := by norm_num
  have hcross_int : Integrable (fun ω => 2 * |b| * |F ω|) μ :=
    hFabs_int.const_mul (2 * |b|)
  have hconst_int : Integrable (fun _ : Ω => b ^ 2) μ := integrable_const _
  have hrhs_int : Integrable
      (fun ω => (F ω ^ 2 + 2 * |b| * |F ω|) + b ^ 2) μ :=
    (hFsq.add hcross_int).add hconst_int
  have htotal_int := positiveSigmoid_squaredLoss_integrable μ X hX hX_nonneg y
  calc
    (∫ ω, (positiveSigmoid (X ω) - y) ^ 2 ∂μ) ≤
        ∫ ω, (F ω ^ 2 + 2 * |b| * |F ω|) + b ^ 2 ∂μ := by
      apply integral_mono htotal_int hrhs_int
      intro ω
      have hpoint_cross : F ω * b ≤ |F ω| * |b| := by
        calc
          F ω * b ≤ |F ω * b| := le_abs_self _
          _ = |F ω| * |b| := abs_mul _ _
      dsimp [F, b]
      nlinarith
    _ = (∫ ω, F ω ^ 2 ∂μ) +
          2 * |b| * (∫ ω, |F ω| ∂μ) + b ^ 2 := by
      calc
        (∫ ω, (F ω ^ 2 + 2 * |b| * |F ω|) + b ^ 2 ∂μ) =
            (∫ ω, F ω ^ 2 + 2 * |b| * |F ω| ∂μ) +
              ∫ _ : Ω, b ^ 2 ∂μ := by
          simpa only [Pi.add_apply] using
            integral_add (hFsq.add hcross_int) hconst_int
        _ = ((∫ ω, F ω ^ 2 ∂μ) + ∫ ω, 2 * |b| * |F ω| ∂μ) +
              ∫ _ : Ω, b ^ 2 ∂μ := by
          rw [integral_add hFsq hcross_int]
        _ = (∫ ω, F ω ^ 2 ∂μ) +
              2 * |b| * (∫ ω, |F ω| ∂μ) + b ^ 2 := by
          rw [integral_const_mul, integral_const]
          simp [measureReal_def]
    _ ≤ (25 : ℝ) / 1024 := by
      linarith

end

end EstimatorIntegrity
