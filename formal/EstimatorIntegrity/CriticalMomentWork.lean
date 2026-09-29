import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.SpecialFunctions.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Tactic

/-!
# Critical moment--work inequalities

This module formalizes the real `L²` Cauchy--Schwarz estimate behind the
variance--work lower bound and the finite exponent algebra used at the
critical endpoint.  It does not formalize canonical tree measures, node
counts, endpoint series, proposal construction, or optimality.
-/

open MeasureTheory

namespace EstimatorIntegrity

/-- If `H` is square-integrable and the nonnegative cost `N` is integrable,
then `|H| * sqrt N` is integrable and its squared integral is bounded by the
product of the second moment of `H` and the mean cost. -/
theorem criticalMomentWork_integrable_and_sq_le
    {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω) (H N : Ω → ℝ)
    (hN_nonneg : ∀ ω, 0 ≤ N ω) (hH : MemLp H 2 μ) (hN : Integrable N μ) :
    Integrable (fun ω => |H ω| * Real.sqrt (N ω)) μ ∧
      (∫ ω, |H ω| * Real.sqrt (N ω) ∂μ) ^ 2 ≤
        (∫ ω, H ω ^ 2 ∂μ) * ∫ ω, N ω ∂μ := by
  have hsqrt_meas : AEStronglyMeasurable (fun ω => Real.sqrt (N ω)) μ :=
    hN.aestronglyMeasurable.aemeasurable.sqrt.aestronglyMeasurable
  have hsqrt_sq_int : Integrable (fun ω => (Real.sqrt (N ω)) ^ 2) μ := by
    convert hN using 1
    ext ω
    exact Real.sq_sqrt (hN_nonneg ω)
  have hsqrt_L2 : MemLp (fun ω => Real.sqrt (N ω)) 2 μ :=
    (memLp_two_iff_integrable_sq hsqrt_meas).2 hsqrt_sq_int
  have habs_L2 : MemLp (fun ω => |H ω|) 2 μ := by
    simpa only [Real.norm_eq_abs] using hH.norm
  have hproduct : Integrable (fun ω => |H ω| * Real.sqrt (N ω)) μ := by
    change Integrable ((fun ω => |H ω|) * fun ω => Real.sqrt (N ω)) μ
    exact habs_L2.integrable_mul hsqrt_L2
  refine ⟨hproduct, ?_⟩
  have hcs := integral_mul_le_Lp_mul_Lq_of_nonneg Real.HolderConjugate.two_two
    (μ := μ) (Filter.Eventually.of_forall fun ω => abs_nonneg (H ω))
    (Filter.Eventually.of_forall fun ω => Real.sqrt_nonneg (N ω))
    (by simpa using habs_L2) (by simpa using hsqrt_L2)
  have hHsq : (∫ ω, |H ω| ^ 2 ∂μ) = ∫ ω, H ω ^ 2 ∂μ := by
    apply integral_congr_ae
    exact Filter.Eventually.of_forall fun ω => sq_abs (H ω)
  have hNsq : (∫ ω, (Real.sqrt (N ω)) ^ 2 ∂μ) = ∫ ω, N ω ∂μ := by
    apply integral_congr_ae
    exact Filter.Eventually.of_forall fun ω => Real.sq_sqrt (hN_nonneg ω)
  simp only [Real.rpow_two] at hcs
  rw [hHsq, hNsq] at hcs
  have hproduct_nonneg : 0 ≤ ∫ ω, |H ω| * Real.sqrt (N ω) ∂μ :=
    integral_nonneg fun ω => mul_nonneg (abs_nonneg (H ω)) (Real.sqrt_nonneg (N ω))
  have hHsq_nonneg : 0 ≤ ∫ ω, H ω ^ 2 ∂μ := integral_nonneg fun ω => sq_nonneg (H ω)
  have hNint_nonneg : 0 ≤ ∫ ω, N ω ∂μ := integral_nonneg hN_nonneg
  calc
    (∫ ω, |H ω| * Real.sqrt (N ω) ∂μ) ^ 2 ≤
        ((∫ ω, H ω ^ 2 ∂μ) ^ (1 / 2 : ℝ) *
          (∫ ω, N ω ∂μ) ^ (1 / 2 : ℝ)) ^ 2 :=
      (sq_le_sq₀ hproduct_nonneg
        (mul_nonneg (Real.rpow_nonneg hHsq_nonneg _) (Real.rpow_nonneg hNint_nonneg _))).2 hcs
    _ = (∫ ω, H ω ^ 2 ∂μ) * ∫ ω, N ω ∂μ := by
      rw [← Real.sqrt_eq_rpow, ← Real.sqrt_eq_rpow, mul_pow,
        Real.sq_sqrt hHsq_nonneg, Real.sq_sqrt hNint_nonneg]

/-- The endpoint fractional-moment condition in `p` is equivalent to the
strict critical exponent bound. -/
theorem criticalExponent_lt_iff (alpha p : ℝ) (halpha : 0 < alpha) (hp : 1 < p) :
    (p - 1) / p < 1 / (alpha + 1) ↔ p < 1 + 1 / alpha := by
  have hp_pos : 0 < p := lt_trans zero_lt_one hp
  have halpha_one_pos : 0 < alpha + 1 := by linarith
  constructor
  · intro h
    have hcross : (p - 1) * (alpha + 1) < 1 * p :=
      (div_lt_div_iff₀ hp_pos halpha_one_pos).mp h
    have hcritical : (p - 1) * alpha < 1 := by nlinarith
    have hdiv : p - 1 < 1 / alpha := (lt_div_iff₀ halpha).2 hcritical
    linarith
  · intro h
    have hdiv : p - 1 < 1 / alpha := by linarith
    have hcritical : (p - 1) * alpha < 1 := (lt_div_iff₀ halpha).mp hdiv
    apply (div_lt_div_iff₀ hp_pos halpha_one_pos).2
    nlinarith

/-- Equality occurs exactly at the excluded critical exponent. -/
theorem criticalExponent_eq_iff (alpha p : ℝ) (halpha : 0 < alpha) (hp : 1 < p) :
    (p - 1) / p = 1 / (alpha + 1) ↔ p = 1 + 1 / alpha := by
  have hp_pos : 0 < p := lt_trans zero_lt_one hp
  have halpha_one_pos : 0 < alpha + 1 := by linarith
  constructor
  · intro h
    have hcross : (p - 1) * (alpha + 1) = 1 * p :=
      (div_eq_div_iff hp_pos.ne' halpha_one_pos.ne').mp h
    have hcritical : (p - 1) * alpha = 1 := by nlinarith
    have hdiv : p - 1 = 1 / alpha := (eq_div_iff halpha.ne').2 hcritical
    linarith
  · intro h
    have hdiv : p - 1 = 1 / alpha := by linarith
    have hcritical : (p - 1) * alpha = 1 := (eq_div_iff halpha.ne').mp hdiv
    apply (div_eq_div_iff hp_pos.ne' halpha_one_pos.ne').2
    nlinarith

/-- At `alpha = 1` and `p = 2`, the fractional exponent is exactly critical. -/
theorem criticalExponent_alpha_one_p_two :
    ((2 : ℝ) - 1) / 2 = 1 / ((1 : ℝ) + 1) := by
  norm_num

end EstimatorIntegrity
