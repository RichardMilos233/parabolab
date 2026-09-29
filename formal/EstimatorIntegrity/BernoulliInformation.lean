import Mathlib.Analysis.Convex.Deriv
import Mathlib.InformationTheory.KullbackLeibler.Basic
import Mathlib.Probability.Distributions.Bernoulli
import Mathlib.Tactic

/-!
# Bernoulli relative entropy and binary testing

This module proves the scalar and measure-theoretic Bernoulli information
inequalities needed by the signed-information lower bound.  It does not model
urn sampling, adaptive transcripts, chain-rule accumulation, or random
stopping.
-/

open MeasureTheory Set Real
open scoped ENNReal NNReal

namespace EstimatorIntegrity

/-- The Bernoulli law on `Bool` whose mass at `true` is `p`. -/
noncomputable def bernoulliBool (p : Set.Icc (0 : ℝ) 1) : Measure Bool :=
  ProbabilityTheory.bernoulliMeasure true false p

instance bernoulliBool_isProbabilityMeasure (p : Set.Icc (0 : ℝ) 1) :
    IsProbabilityMeasure (bernoulliBool p) := by
  unfold bernoulliBool
  infer_instance

private noncomputable def bernoulliDensity
    (p q : Set.Icc (0 : ℝ) 1) (b : Bool) : ℝ≥0∞ :=
  if b then (unitInterval.toNNReal p : ℝ≥0∞) /
    (unitInterval.toNNReal q : ℝ≥0∞)
  else (unitInterval.toNNReal (unitInterval.symm p) : ℝ≥0∞) /
    (unitInterval.toNNReal (unitInterval.symm q) : ℝ≥0∞)

private lemma bernoulliBool_eq_withDensity {p q : Set.Icc (0 : ℝ) 1}
    (hq : 0 < (q : ℝ)) (hq1 : (q : ℝ) < 1) :
    bernoulliBool p = (bernoulliBool q).withDensity (bernoulliDensity p q) := by
  unfold bernoulliBool bernoulliDensity
  rw [ProbabilityTheory.bernoulliMeasure_def,
    ProbabilityTheory.bernoulliMeasure_def]
  simp only [← Measure.coe_nnreal_smul]
  rw [withDensity_add_measure]
  simp only [withDensity_smul_measure, dirac_withDensity]
  simp only [if_true, Bool.false_eq_true, if_false, smul_smul]
  have hq0nn : unitInterval.toNNReal q ≠ 0 := by
    intro h
    have := congrArg ((↑·) : ℝ≥0 → ℝ) h
    simp only [unitInterval.coe_toNNReal, NNReal.coe_zero] at this
    exact hq.ne' this
  have hq0 : (unitInterval.toNNReal q : ℝ≥0∞) ≠ 0 := by
    exact_mod_cast hq0nn
  have hqσ0nn : unitInterval.toNNReal (unitInterval.symm q) ≠ 0 := by
    intro h
    have := congrArg ((↑·) : ℝ≥0 → ℝ) h
    simp only [unitInterval.coe_toNNReal, unitInterval.coe_symm_eq, NNReal.coe_zero] at this
    linarith
  have hqσ0 : (unitInterval.toNNReal (unitInterval.symm q) : ℝ≥0∞) ≠ 0 := by
    exact_mod_cast hqσ0nn
  rw [ENNReal.mul_div_cancel hq0 (by simp), ENNReal.mul_div_cancel hqσ0 (by simp)]

/-- The scalar Bernoulli relative-entropy expression, using Mathlib's
endpoint convention `Real.log 0 = 0`. -/
noncomputable def bernoulliKLScalar (p q : ℝ) : ℝ :=
  p * log p - p * log q +
    ((1 - p) * log (1 - p) - (1 - p) * log (1 - q))

lemma bernoulliKLScalar_eq_log_div {p q : ℝ} (hq : 0 < q) (hq1 : q < 1) :
    bernoulliKLScalar p q =
      p * log (p / q) + (1 - p) * log ((1 - p) / (1 - q)) := by
  unfold bernoulliKLScalar
  have hq0 : q ≠ 0 := ne_of_gt hq
  have hq10 : 1 - q ≠ 0 := ne_of_gt (sub_pos.mpr hq1)
  by_cases hp0 : p = 0
  · subst p
    simp
  by_cases hp1 : 1 - p = 0
  · have hp : p = 1 := by linarith
    subst p
    simp
  rw [Real.log_div hp0 hq0, Real.log_div hp1 hq10]
  ring

lemma continuous_bernoulliKLScalar (q : ℝ) : Continuous (fun p ↦ bernoulliKLScalar p q) := by
  unfold bernoulliKLScalar
  fun_prop

lemma hasDerivAt_bernoulliKLScalar {p q : ℝ} (hp : 0 < p) (hp1 : p < 1) :
    HasDerivAt (fun x ↦ bernoulliKLScalar x q)
      (log p - log (1 - p) - log q + log (1 - q)) p := by
  unfold bernoulliKLScalar
  have hpcomp : 1 - p ≠ 0 := ne_of_gt (sub_pos.mpr hp1)
  have hfirst : HasDerivAt (fun x : ℝ ↦ x * log x - x * log q)
      (log p + 1 - log q) p := by
    convert (Real.hasDerivAt_mul_log hp.ne').sub
      ((hasDerivAt_id p).mul_const (log q)) using 1 <;> first | rfl | ring
  have hcomp : HasDerivAt (fun x : ℝ ↦ 1 - x) (-1) p := by
    convert (hasDerivAt_const p 1).sub (hasDerivAt_id p) using 1 <;> first | rfl | ring
  have hsecond : HasDerivAt
      (fun x : ℝ ↦ (1 - x) * log (1 - x) - (1 - x) * log (1 - q))
      (-(log (1 - p) + 1) + log (1 - q)) p := by
    convert ((Real.hasDerivAt_mul_log hpcomp).comp p hcomp).sub
      (hcomp.mul_const (log (1 - q))) using 1 <;> first | rfl | ring
  convert hfirst.add hsecond using 1 <;> first | rfl | ring

/-- Scalar binary Pinsker for an interior reference parameter.  The source
parameter may be either endpoint. -/
theorem bernoulliKLScalar_pinsker {p q : ℝ}
    (hp : 0 ≤ p) (hp1 : p ≤ 1) (hq : 0 < q) (hq1 : q < 1) :
    2 * (p - q) ^ 2 ≤ bernoulliKLScalar p q := by
  let gap : ℝ → ℝ := fun x ↦ bernoulliKLScalar x q - 2 * (x - q) ^ 2
  let gap' : ℝ → ℝ := fun x ↦
    log x - log (1 - x) - log q + log (1 - q) - 4 * (x - q)
  let gap'' : ℝ → ℝ := fun x ↦ 1 / x + 1 / (1 - x) - 4
  have hgap_cont : ContinuousOn gap (Icc (0 : ℝ) 1) := by
    exact (continuous_bernoulliKLScalar q).sub
      (continuous_const.mul ((continuous_id.sub continuous_const).pow 2)) |>.continuousOn
  have hgap_deriv : ∀ x ∈ interior (Icc (0 : ℝ) 1),
      HasDerivWithinAt gap (gap' x) (interior (Icc (0 : ℝ) 1)) x := by
    intro x hx
    rw [interior_Icc] at hx
    have hsq : HasDerivAt (fun y : ℝ ↦ 2 * (y - q) ^ 2) (4 * (x - q)) x := by
      convert (hasDerivAt_const x 2).mul
        (((hasDerivAt_id x).sub_const q).pow 2) using 1 <;>
        first | rfl | (simp [id]; ring)
    have hD : HasDerivAt gap (gap' x) x := by
      dsimp [gap, gap']
      convert (hasDerivAt_bernoulliKLScalar (q := q) hx.1 hx.2).sub hsq using 1 <;>
        rfl
    exact hD.hasDerivWithinAt
  have hgap_deriv2 : ∀ x ∈ interior (Icc (0 : ℝ) 1),
      HasDerivWithinAt gap' (gap'' x) (interior (Icc (0 : ℝ) 1)) x := by
    intro x hx
    rw [interior_Icc] at hx
    have hx0 : x ≠ 0 := ne_of_gt hx.1
    have hx1 : 1 - x ≠ 0 := ne_of_gt (sub_pos.mpr hx.2)
    have hcomp : HasDerivAt (fun y : ℝ ↦ 1 - y) (-1) x := by
      convert (hasDerivAt_const x 1).sub (hasDerivAt_id x) using 1 <;> first | rfl | ring
    have hlogcomp : HasDerivAt (fun y : ℝ ↦ log (1 - y)) (-1 / (1 - x)) x := by
      convert (hasDerivAt_log hx1).comp x hcomp using 1 <;>
        first | rfl | field_simp
    have hlin : HasDerivAt (fun y : ℝ ↦ 4 * (y - q)) 4 x := by
      convert (hasDerivAt_const x 4).mul ((hasDerivAt_id x).sub_const q) using 1 <;>
        first | rfl | ring
    have hD : HasDerivAt gap' (gap'' x) x := by
      dsimp [gap', gap'']
      convert (((((hasDerivAt_log hx0).sub hlogcomp).sub
        (hasDerivAt_const x (log q))).add
        (hasDerivAt_const x (log (1 - q)))).sub hlin) using 1 <;>
        first | rfl | (field_simp; try ring)
    exact hD.hasDerivWithinAt
  have hgap_deriv2_nonneg : ∀ x ∈ interior (Icc (0 : ℝ) 1), 0 ≤ gap'' x := by
    intro x hx
    rw [interior_Icc] at hx
    have hx0 : 0 < x := hx.1
    have hx1 : 0 < 1 - x := sub_pos.mpr hx.2
    dsimp [gap'']
    field_simp
    nlinarith [sq_nonneg (2 * x - 1)]
  have hconv : ConvexOn ℝ (Icc (0 : ℝ) 1) gap :=
    convexOn_of_hasDerivWithinAt2_nonneg (convex_Icc 0 1) hgap_cont
      hgap_deriv hgap_deriv2 hgap_deriv2_nonneg
  have hqmem : q ∈ interior (Icc (0 : ℝ) 1) := by
    rw [interior_Icc]
    exact ⟨hq, hq1⟩
  have hgapq_deriv : HasDerivAt gap 0 q := by
    have hsq : HasDerivAt (fun y : ℝ ↦ 2 * (y - q) ^ 2) 0 q := by
      convert (hasDerivAt_const q 2).mul
        (((hasDerivAt_id q).sub_const q).pow 2) using 1 <;>
        first | rfl | (simp only [id_eq, sub_self, zero_mul, pow_two]; norm_num)
    have hD : HasDerivAt gap 0 q := by
      dsimp [gap]
      convert (hasDerivAt_bernoulliKLScalar (p := q) (q := q) hq hq1).sub hsq using 1 <;>
        first | rfl | simp
    exact hD
  have hmin : IsMinOn gap (Icc (0 : ℝ) 1) q := by
    apply hconv.isMinOn_of_rightDeriv_eq_zero hqmem
    exact hgapq_deriv.hasDerivWithinAt.derivWithin (uniqueDiffWithinAt_Ioi q)
  have hle := hmin ⟨hp, hp1⟩
  have hgapq : gap q = 0 := by simp [gap, bernoulliKLScalar]
  dsimp [gap] at hle hgapq
  linarith

/-- The elementary upper bound on scalar Bernoulli relative entropy. -/
theorem bernoulliKLScalar_le_chiSq {p q : ℝ}
    (hp : 0 ≤ p) (hp1 : p ≤ 1) (hq : 0 < q) (hq1 : q < 1) :
    bernoulliKLScalar p q ≤ (p - q) ^ 2 / (q * (1 - q)) := by
  have hlog : ∀ a b : ℝ, 0 ≤ a → 0 < b →
      a * log (a / b) ≤ a * (a / b - 1) := by
    intro a b ha hb
    rcases ha.eq_or_lt with ha0 | ha
    · subst a
      simp
    · exact mul_le_mul_of_nonneg_left
        (Real.log_le_sub_one_of_pos (div_pos ha hb)) ha.le
  rw [bernoulliKLScalar_eq_log_div hq hq1]
  calc
    p * log (p / q) + (1 - p) * log ((1 - p) / (1 - q))
        ≤ p * (p / q - 1) + (1 - p) * ((1 - p) / (1 - q) - 1) :=
      add_le_add (hlog p q hp hq)
        (hlog (1 - p) (1 - q) (sub_nonneg.mpr hp1) (sub_pos.mpr hq1))
    _ = (p - q) ^ 2 / (q * (1 - q)) := by
      field_simp [ne_of_gt hq, ne_of_gt (sub_pos.mpr hq1)]
      ring

theorem bernoulliBool_true (p : Set.Icc (0 : ℝ) 1) :
    (bernoulliBool p).real {true} = p := by
  unfold bernoulliBool
  simp

private lemma bernoulliBool_false (p : Set.Icc (0 : ℝ) 1) :
    (bernoulliBool p).real {false} = 1 - (p : ℝ) := by
  unfold bernoulliBool
  simp

theorem bernoulliBool_kl_ne_top {p q : Set.Icc (0 : ℝ) 1}
    (hq : 0 < (q : ℝ)) (hq1 : (q : ℝ) < 1) :
    InformationTheory.klDiv (bernoulliBool p) (bernoulliBool q) ≠ ∞ := by
  have hdens := bernoulliBool_eq_withDensity (p := p) (q := q) hq hq1
  have hac : bernoulliBool p ≪ bernoulliBool q := by
    rw [hdens]
    exact withDensity_absolutelyContinuous _ _
  exact InformationTheory.klDiv_ne_top hac Integrable.of_finite

theorem bernoulliBool_kl_toReal {p q : Set.Icc (0 : ℝ) 1}
    (hq : 0 < (q : ℝ)) (hq1 : (q : ℝ) < 1) :
    (InformationTheory.klDiv (bernoulliBool p) (bernoulliBool q)).toReal =
      (p : ℝ) * log ((p : ℝ) / (q : ℝ)) +
        (1 - (p : ℝ)) * log ((1 - (p : ℝ)) / (1 - (q : ℝ))) := by
  have hdens := bernoulliBool_eq_withDensity (p := p) (q := q) hq hq1
  have hac : bernoulliBool p ≪ bernoulliBool q := by
    rw [hdens]
    exact withDensity_absolutelyContinuous _ _
  have hmass : bernoulliBool p univ = bernoulliBool q univ := by
    simp only [measure_univ]
  rw [InformationTheory.toReal_klDiv_of_measure_eq hac hmass]
  rw [← MeasureTheory.integral_rnDeriv_mul_log hac]
  have hrn : (bernoulliBool p).rnDeriv (bernoulliBool q) =ᵐ[bernoulliBool q]
      bernoulliDensity p q := by
    rw [hdens]
    exact Measure.rnDeriv_withDensity _ (by fun_prop)
  have hint :
      (fun b ↦ ((bernoulliBool p).rnDeriv (bernoulliBool q) b).toReal *
        log ((bernoulliBool p).rnDeriv (bernoulliBool q) b).toReal) =ᵐ[bernoulliBool q]
      (fun b ↦ (bernoulliDensity p q b).toReal *
        log (bernoulliDensity p q b).toReal) := by
    filter_upwards [hrn] with b hb
    rw [hb]
  rw [integral_congr_ae hint]
  unfold bernoulliBool
  rw [ProbabilityTheory.integral_bernoulliMeasure]
  simp [bernoulliDensity, ENNReal.toReal_div, unitInterval.coe_symm_eq]
  field_simp [hq.ne', (sub_pos.mpr hq1).ne']

theorem bernoulliBool_kl_le_chiSq {p q : Set.Icc (0 : ℝ) 1}
    (hq : 0 < (q : ℝ)) (hq1 : (q : ℝ) < 1) :
    (InformationTheory.klDiv (bernoulliBool p) (bernoulliBool q)).toReal ≤
      ((p : ℝ) - (q : ℝ)) ^ 2 / ((q : ℝ) * (1 - (q : ℝ))) := by
  rw [bernoulliBool_kl_toReal hq hq1, ← bernoulliKLScalar_eq_log_div hq hq1]
  exact bernoulliKLScalar_le_chiSq p.2.1 p.2.2 hq hq1

theorem bernoulliBool_pinsker {p q : Set.Icc (0 : ℝ) 1}
    (hfinite : InformationTheory.klDiv (bernoulliBool p) (bernoulliBool q) ≠ ∞) :
    2 * ((p : ℝ) - (q : ℝ)) ^ 2 ≤
      (InformationTheory.klDiv (bernoulliBool p) (bernoulliBool q)).toReal := by
  have hac := (InformationTheory.klDiv_ne_top_iff.mp hfinite).1
  by_cases hq0 : (q : ℝ) = 0
  · have hqeq : q = (0 : Set.Icc (0 : ℝ) 1) := Subtype.ext hq0
    have hz : bernoulliBool q {true} = 0 := by
      rw [hqeq]
      simp [bernoulliBool]
    have hpz := hac hz
    have hp0 : (p : ℝ) = 0 := by
      rw [← bernoulliBool_true p]
      simp [measureReal_def, hpz]
    have hpeq : p = (0 : Set.Icc (0 : ℝ) 1) := Subtype.ext hp0
    subst p
    subst q
    simp
  · by_cases hq1e : (q : ℝ) = 1
    · have hqeq : q = (1 : Set.Icc (0 : ℝ) 1) := Subtype.ext hq1e
      have hz : bernoulliBool q {false} = 0 := by
        rw [hqeq]
        simp [bernoulliBool]
      have hpz := hac hz
      have hp1 : (p : ℝ) = 1 := by
        have hzero : (bernoulliBool p).real {false} = 0 := by
          simp [measureReal_def, hpz]
        rw [bernoulliBool_false] at hzero
        linarith
      have hpeq : p = (1 : Set.Icc (0 : ℝ) 1) := Subtype.ext hp1
      subst p
      subst q
      simp
    · have hq : 0 < (q : ℝ) := lt_of_le_of_ne q.2.1 (Ne.symm hq0)
      have hq1 : (q : ℝ) < 1 := lt_of_le_of_ne q.2.2 hq1e
      rw [bernoulliBool_kl_toReal hq hq1,
        ← bernoulliKLScalar_eq_log_div hq hq1]
      exact bernoulliKLScalar_pinsker p.2.1 p.2.2 hq hq1

theorem bernoulliBool_testing_error {p q : Set.Icc (0 : ℝ) 1}
    (hkl : InformationTheory.klDiv (bernoulliBool p) (bernoulliBool q) ≤
      ENNReal.ofReal (1 / 12 : ℝ)) :
    (3 / 8 : ℝ) ≤ ((1 - (p : ℝ)) + (q : ℝ)) / 2 := by
  have hfinite : InformationTheory.klDiv (bernoulliBool p) (bernoulliBool q) ≠ ∞ := by
    apply ne_of_lt
    exact lt_of_le_of_lt hkl ENNReal.ofReal_lt_top
  have hpin := bernoulliBool_pinsker hfinite
  have hreal :
      (InformationTheory.klDiv (bernoulliBool p) (bernoulliBool q)).toReal ≤
        (1 / 12 : ℝ) := by
    calc
      _ ≤ (ENNReal.ofReal (1 / 12 : ℝ)).toReal :=
        ENNReal.toReal_mono (by simp) hkl
      _ = (1 / 12 : ℝ) := by norm_num
  nlinarith [sq_nonneg ((p : ℝ) - (q : ℝ) - 1 / 4)]

end EstimatorIntegrity
