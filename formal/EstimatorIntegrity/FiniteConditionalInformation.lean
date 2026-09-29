import EstimatorIntegrity.BernoulliInformation
import Mathlib.InformationTheory.KullbackLeibler.ChainRule
import Mathlib.InformationTheory.KullbackLeibler.DataProcessing
import Mathlib.MeasureTheory.Integral.Bochner.SumMeasure
import Mathlib.Tactic

/-!
# Finite conditional information and binary postprocessing

This module proves conditional Bernoulli KL averaging over an actual finite
history law, its one-step and chain-rule bounds, and the testing consequence
of an actual measurable Bool-valued decision.
-/

open MeasureTheory Set Real ProbabilityTheory
open scoped ENNReal NNReal ProbabilityTheory

namespace EstimatorIntegrity

/-- The Markov kernel assigning the Bernoulli law with parameter `p h` to
history `h`. -/
noncomputable def bernoulliKernel {H : Type*} [MeasurableSpace H] [Countable H]
    [MeasurableSingletonClass H] (p : H → Set.Icc (0 : ℝ) 1) : Kernel H Bool :=
  Kernel.ofFunOfCountable fun h ↦ bernoulliBool (p h)

instance bernoulliKernel_isMarkovKernel {H : Type*} [MeasurableSpace H] [Countable H]
    [MeasurableSingletonClass H] (p : H → Set.Icc (0 : ℝ) 1) :
    IsMarkovKernel (bernoulliKernel p) := by
  constructor
  intro h
  change IsProbabilityMeasure (bernoulliBool (p h))
  infer_instance

@[simp] lemma bernoulliKernel_apply {H : Type*} [MeasurableSpace H] [Countable H]
    [MeasurableSingletonClass H] (p : H → Set.Icc (0 : ℝ) 1) (h : H) :
    bernoulliKernel p h = bernoulliBool (p h) := rfl

/-- The joint composition-product law has the expected mass on every atom. -/
lemma finiteJoint_singleton {H : Type*} [MeasurableSpace H] [Fintype H]
    [MeasurableSingletonClass H] (μ : Measure H) [IsFiniteMeasure μ]
    (p : H → Set.Icc (0 : ℝ) 1) (h : H) (b : Bool) :
    (μ ⊗ₘ bernoulliKernel p) {(h, b)} = μ {h} * bernoulliBool (p h) {b} := by
  rw [Measure.compProd_apply (measurableSet_singleton (h, b)), lintegral_fintype]
  classical
  rw [Finset.sum_eq_single h]
  · have hpre : Prod.mk h ⁻¹' ({(h, b)} : Set (H × Bool)) = {b} := by
      ext y
      simp
    rw [hpre]
    change bernoulliBool (p h) {b} * μ {h} = _
    rw [mul_comm]
  · intro x _ hx
    have hpre : Prod.mk x ⁻¹' ({(h, b)} : Set (H × Bool)) = ∅ := by
      ext y
      simp [hx]
    rw [hpre]
    simp
  · simp

private noncomputable def jointDensity {H : Type*}
    (p q : H → Set.Icc (0 : ℝ) 1) (x : H × Bool) : ℝ≥0∞ :=
  if x.2 then (unitInterval.toNNReal (p x.1) : ℝ≥0∞) /
    (unitInterval.toNNReal (q x.1) : ℝ≥0∞)
  else (unitInterval.toNNReal (unitInterval.symm (p x.1)) : ℝ≥0∞) /
    (unitInterval.toNNReal (unitInterval.symm (q x.1)) : ℝ≥0∞)

private lemma bernoulliBool_singleton (p : Set.Icc (0 : ℝ) 1) (b : Bool) :
    bernoulliBool p {b} = if b then (unitInterval.toNNReal p : ℝ≥0∞)
      else (unitInterval.toNNReal (unitInterval.symm p) : ℝ≥0∞) := by
  cases b <;> simp [bernoulliBool, ProbabilityTheory.bernoulliMeasure_def]

private lemma finiteJoint_eq_withDensity {H : Type*} [MeasurableSpace H] [Fintype H]
    [MeasurableSingletonClass H] (μ : Measure H) [IsFiniteMeasure μ]
    (p q : H → Set.Icc (0 : ℝ) 1)
    (hq : ∀ h, 0 < (q h : ℝ)) (hq1 : ∀ h, (q h : ℝ) < 1) :
    μ ⊗ₘ bernoulliKernel p =
      (μ ⊗ₘ bernoulliKernel q).withDensity (jointDensity p q) := by
  apply Measure.ext_of_singleton
  rintro ⟨h, b⟩
  rw [finiteJoint_singleton, withDensity_apply _ (measurableSet_singleton (h, b)),
    lintegral_singleton, finiteJoint_singleton]
  rw [bernoulliBool_singleton, bernoulliBool_singleton]
  cases b <;> simp only [jointDensity, Bool.false_eq_true, if_false, if_true]
  · have hq0 : (unitInterval.toNNReal (unitInterval.symm (q h)) : ℝ≥0∞) ≠ 0 := by
      exact_mod_cast (show unitInterval.toNNReal (unitInterval.symm (q h)) ≠ 0 by
        intro hz
        have := congrArg ((↑·) : ℝ≥0 → ℝ) hz
        simp only [unitInterval.coe_toNNReal, unitInterval.coe_symm_eq, NNReal.coe_zero] at this
        linarith [hq1 h])
    rw [← mul_assoc, mul_comm
      ((unitInterval.toNNReal (unitInterval.symm (p h)) : ℝ≥0∞) /
        (unitInterval.toNNReal (unitInterval.symm (q h)) : ℝ≥0∞)) (μ {h}),
      mul_assoc, ENNReal.div_mul_cancel hq0 (by simp)]
  · have hq0 : (unitInterval.toNNReal (q h) : ℝ≥0∞) ≠ 0 := by
      exact_mod_cast (show unitInterval.toNNReal (q h) ≠ 0 by
        intro hz
        have := congrArg ((↑·) : ℝ≥0 → ℝ) hz
        simp only [unitInterval.coe_toNNReal, NNReal.coe_zero] at this
        exact (hq h).ne' this)
    rw [← mul_assoc, mul_comm
      ((unitInterval.toNNReal (p h) : ℝ≥0∞) /
        (unitInterval.toNNReal (q h) : ℝ≥0∞)) (μ {h}),
      mul_assoc, ENNReal.div_mul_cancel hq0 (by simp)]

/-- Shared finite-history Bernoulli composition-products have finite KL when
the reference parameters are strictly interior. Source endpoints and
zero-mass history atoms are allowed. -/
theorem finiteConditionalKL_ne_top {H : Type*} [MeasurableSpace H] [Fintype H]
    [MeasurableSingletonClass H] (μ : Measure H) [IsProbabilityMeasure μ]
    (p q : H → Set.Icc (0 : ℝ) 1)
    (hq : ∀ h, 0 < (q h : ℝ)) (hq1 : ∀ h, (q h : ℝ) < 1) :
    InformationTheory.klDiv (μ ⊗ₘ bernoulliKernel p)
      (μ ⊗ₘ bernoulliKernel q) ≠ ∞ := by
  have hdens := finiteJoint_eq_withDensity μ p q hq hq1
  have hac : μ ⊗ₘ bernoulliKernel p ≪ μ ⊗ₘ bernoulliKernel q := by
    rw [hdens]
    exact withDensity_absolutelyContinuous _ _
  exact InformationTheory.klDiv_ne_top hac Integrable.of_finite

/-- Actual shared-history conditional KL is the probability-weighted average
of the actual conditional Bernoulli KL divergences. -/
theorem finiteConditionalKL_toReal {H : Type*} [MeasurableSpace H] [Fintype H]
    [MeasurableSingletonClass H] (μ : Measure H) [IsProbabilityMeasure μ]
    (p q : H → Set.Icc (0 : ℝ) 1)
    (hq : ∀ h, 0 < (q h : ℝ)) (hq1 : ∀ h, (q h : ℝ) < 1) :
    (InformationTheory.klDiv (μ ⊗ₘ bernoulliKernel p)
      (μ ⊗ₘ bernoulliKernel q)).toReal =
      ∑ h, μ.real {h} *
        (InformationTheory.klDiv (bernoulliBool (p h))
          (bernoulliBool (q h))).toReal := by
  have hdens := finiteJoint_eq_withDensity μ p q hq hq1
  have hac : μ ⊗ₘ bernoulliKernel p ≪ μ ⊗ₘ bernoulliKernel q := by
    rw [hdens]
    exact withDensity_absolutelyContinuous _ _
  have hmass : (μ ⊗ₘ bernoulliKernel p) univ =
      (μ ⊗ₘ bernoulliKernel q) univ := by simp
  rw [InformationTheory.toReal_klDiv_of_measure_eq hac hmass]
  rw [← MeasureTheory.integral_rnDeriv_mul_log hac]
  have hrn : (μ ⊗ₘ bernoulliKernel p).rnDeriv
      (μ ⊗ₘ bernoulliKernel q) =ᵐ[μ ⊗ₘ bernoulliKernel q]
      jointDensity p q := by
    rw [hdens]
    exact Measure.rnDeriv_withDensity _ (by fun_prop)
  have hint :
      (fun x ↦ (((μ ⊗ₘ bernoulliKernel p).rnDeriv
          (μ ⊗ₘ bernoulliKernel q) x).toReal) *
        log (((μ ⊗ₘ bernoulliKernel p).rnDeriv
          (μ ⊗ₘ bernoulliKernel q) x).toReal)) =ᵐ[μ ⊗ₘ bernoulliKernel q]
      (fun x ↦ (jointDensity p q x).toReal * log (jointDensity p q x).toReal) := by
    filter_upwards [hrn] with x hx
    rw [hx]
  rw [integral_congr_ae hint]
  rw [Measure.integral_compProd Integrable.of_finite]
  rw [integral_fintype Integrable.of_finite]
  apply Finset.sum_congr rfl
  intro h _
  congr 1
  rw [bernoulliBool_kl_toReal (hq h) (hq1 h)]
  change (∫ b, (jointDensity p q (h, b)).toReal *
    log (jointDensity p q (h, b)).toReal ∂bernoulliBool (q h)) = _
  unfold bernoulliBool
  rw [ProbabilityTheory.integral_bernoulliMeasure]
  simp [jointDensity, ENNReal.toReal_div, unitInterval.coe_symm_eq]
  field_simp [(hq h).ne', (sub_pos.mpr (hq1 h)).ne']

/-- A uniform bound on every actual conditional Bernoulli divergence bounds
the actual shared-history one-step divergence. -/
theorem finiteConditionalKL_le {H : Type*} [MeasurableSpace H] [Fintype H]
    [MeasurableSingletonClass H] (μ : Measure H) [IsProbabilityMeasure μ]
    (p q : H → Set.Icc (0 : ℝ) 1)
    (hq : ∀ h, 0 < (q h : ℝ)) (hq1 : ∀ h, (q h : ℝ) < 1)
    {B : ℝ} (hB : 0 ≤ B)
    (hstep : ∀ h, InformationTheory.klDiv (bernoulliBool (p h))
      (bernoulliBool (q h)) ≤ ENNReal.ofReal B) :
    InformationTheory.klDiv (μ ⊗ₘ bernoulliKernel p)
      (μ ⊗ₘ bernoulliKernel q) ≤ ENNReal.ofReal B := by
  have hfinite := finiteConditionalKL_ne_top μ p q hq hq1
  rw [← ENNReal.ofReal_toReal hfinite]
  apply ENNReal.ofReal_le_ofReal
  rw [finiteConditionalKL_toReal μ p q hq hq1]
  calc
    ∑ h, μ.real {h} *
        (InformationTheory.klDiv (bernoulliBool (p h))
          (bernoulliBool (q h))).toReal
      ≤ ∑ h, μ.real {h} * B := by
        apply Finset.sum_le_sum
        intro h _
        exact mul_le_mul_of_nonneg_left
          (calc
            _ ≤ (ENNReal.ofReal B).toReal :=
              ENNReal.toReal_mono (by simp) (hstep h)
            _ = B := ENNReal.toReal_ofReal hB)
          measureReal_nonneg
    _ = B := by
      rw [← Finset.sum_mul]
      simp

/-- One chain-rule step: a bound on the base-law KL plus a uniform bound on
the conditional Bernoulli KL bounds the KL of the two actual joint laws. -/
theorem finiteConditionalKL_accumulate {H : Type*} [MeasurableSpace H] [Fintype H]
    [MeasurableSingletonClass H] (μ ν : Measure H)
    [IsProbabilityMeasure μ] [IsProbabilityMeasure ν]
    (p q : H → Set.Icc (0 : ℝ) 1)
    (hq : ∀ h, 0 < (q h : ℝ)) (hq1 : ∀ h, (q h : ℝ) < 1)
    {A B : ℝ} (hA : 0 ≤ A) (hB : 0 ≤ B)
    (hbase : InformationTheory.klDiv μ ν ≤ ENNReal.ofReal A)
    (hstep : ∀ h, InformationTheory.klDiv (bernoulliBool (p h))
      (bernoulliBool (q h)) ≤ ENNReal.ofReal B) :
    InformationTheory.klDiv (μ ⊗ₘ bernoulliKernel p)
      (ν ⊗ₘ bernoulliKernel q) ≤ ENNReal.ofReal (A + B) := by
  rw [InformationTheory.klDiv_compProd_eq_add]
  calc
    InformationTheory.klDiv μ ν +
        InformationTheory.klDiv (μ ⊗ₘ bernoulliKernel p)
          (μ ⊗ₘ bernoulliKernel q)
      ≤ ENNReal.ofReal A + ENNReal.ofReal B :=
        add_le_add hbase (finiteConditionalKL_le μ p q hq hq1 hB hstep)
    _ = ENNReal.ofReal (A + B) := by rw [ENNReal.ofReal_add hA hB]

/-- The true probability that a Bool-valued decision is `true`, packaged as
a closed unit-interval parameter. -/
noncomputable def decisionTrueParameter {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] (D : Ω → Bool) : Set.Icc (0 : ℝ) 1 :=
  ⟨P.real {omega | D omega = true}, measureReal_nonneg, measureReal_le_one⟩

private lemma map_decision_eq_bernoulliBool {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] (D : Ω → Bool) (hD : Measurable D) :
    P.map D = bernoulliBool (decisionTrueParameter P D) := by
  apply Measure.ext_of_measureReal_singleton
  intro b
  cases b
  · rw [measureReal_def, Measure.map_apply hD (measurableSet_singleton false)]
    change (P {omega | D omega = false}).toReal = _
    have hfalse : {omega | D omega = false} = ({omega | D omega = true} : Set Ω)ᶜ := by
      ext omega
      cases D omega <;> simp
    rw [hfalse, ← measureReal_def, measureReal_compl]
    · simp [decisionTrueParameter, bernoulliBool]
    · exact hD (measurableSet_singleton true)
  · rw [measureReal_def, Measure.map_apply hD (measurableSet_singleton true)]
    simp [decisionTrueParameter, bernoulliBool]
    rw [← measureReal_def]
    congr 1

private lemma decision_false_real {Ω : Type*} [MeasurableSpace Ω]
    (P : Measure Ω) [IsProbabilityMeasure P] (D : Ω → Bool) (hD : Measurable D) :
    P.real {omega | D omega = false} = 1 - (decisionTrueParameter P D : ℝ) := by
  have hfalse : {omega | D omega = false} = ({omega | D omega = true} : Set Ω)ᶜ := by
    ext omega
    cases D omega <;> simp
  rw [hfalse, measureReal_compl]
  · simp [decisionTrueParameter]
  · exact hD (measurableSet_singleton true)

/-- Data processing through an actual measurable Bool decision and the
Bernoulli testing theorem give the equal-prior binary error lower bound. -/
theorem measurableDecision_testing_error {Ω : Type*} [MeasurableSpace Ω]
    (P Q : Measure Ω) [IsProbabilityMeasure P] [IsProbabilityMeasure Q]
    (D : Ω → Bool) (hD : Measurable D)
    (hkl : InformationTheory.klDiv P Q ≤ ENNReal.ofReal (1 / 12 : ℝ)) :
    (3 / 8 : ℝ) ≤
      (P.real {omega | D omega = false} + Q.real {omega | D omega = true}) / 2 := by
  let p := decisionTrueParameter P D
  let q := decisionTrueParameter Q D
  have hmapP : P.map D = bernoulliBool p := map_decision_eq_bernoulliBool P D hD
  have hmapQ : Q.map D = bernoulliBool q := map_decision_eq_bernoulliBool Q D hD
  have hmapkl : InformationTheory.klDiv (bernoulliBool p) (bernoulliBool q) ≤
      ENNReal.ofReal (1 / 12 : ℝ) := by
    rw [← hmapP, ← hmapQ]
    exact (InformationTheory.klDiv_map_le P Q hD).trans hkl
  have htest := bernoulliBool_testing_error hmapkl
  rw [decision_false_real P D hD]
  change (3 / 8 : ℝ) ≤ ((1 - (p : ℝ)) + (q : ℝ)) / 2
  exact htest

end EstimatorIntegrity
