import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic

namespace EstimatorIntegrity

noncomputable section

/-- The quadratic factor appearing in the second derivative of the single-event rate weight. -/
def expKernelFactor (rate s : ℝ) : ℝ :=
  (rate * s - 1) ^ 2 + 1

theorem expKernelFactor_pos (rate s : ℝ) :
    0 < expKernelFactor rate s := by
  unfold expKernelFactor
  have hsq : 0 ≤ (rate * s - 1) ^ 2 := sq_nonneg _
  linarith

theorem expKernelFactor_ge_one (rate s : ℝ) :
    1 ≤ expKernelFactor rate s := by
  unfold expKernelFactor
  have hsq : 0 ≤ (rate * s - 1) ^ 2 := sq_nonneg _
  linarith

/-- The quadratic-rational factor in the second derivative of a general tree topology weight. -/
def topologyFactor (B : ℕ) (L rate : ℝ) : ℝ :=
  (L - (B : ℝ) / rate) ^ 2 + (B : ℝ) / (rate ^ 2)

theorem topologyFactor_nonneg (B : ℕ) (L rate : ℝ) :
    0 ≤ topologyFactor B L rate := by
  unfold topologyFactor
  have hsq : 0 ≤ (L - (B : ℝ) / rate) ^ 2 := sq_nonneg _
  have hB : 0 ≤ (B : ℝ) := Nat.cast_nonneg B
  have hlam2 : 0 ≤ rate ^ 2 := sq_nonneg rate
  exact add_nonneg hsq (div_nonneg hB hlam2)

theorem topologyFactor_pos_of_pos (B : ℕ) (L rate : ℝ)
    (hL : 0 < L) (hrate : 0 < rate) :
    0 < topologyFactor B L rate := by
  unfold topologyFactor
  by_cases hB0 : B = 0
  · subst hB0
    simp only [Nat.cast_zero, zero_div, sub_zero, add_zero]
    exact sq_pos_of_ne_zero (ne_of_gt hL)
  · have hBpos : 0 < (B : ℝ) := Nat.cast_pos.mpr (Nat.pos_of_ne_zero hB0)
    have hlam2pos : 0 < rate ^ 2 := sq_pos_of_ne_zero (ne_of_gt hrate)
    have hfrac : 0 < (B : ℝ) / (rate ^ 2) := div_pos hBpos hlam2pos
    have hsq : 0 ≤ (L - (B : ℝ) / rate) ^ 2 := sq_nonneg _
    exact add_pos_of_nonneg_of_pos hsq hfrac

/-- Positive duration and rate make the topology factor strictly positive. -/
theorem topologyFactor_pos (B : ℕ) (L rate : ℝ)
    (hL : 0 < L) (hrate : 0 < rate) :
    0 < topologyFactor B L rate :=
  topologyFactor_pos_of_pos B L rate hL hrate

/-- The model rate objective representing the leading balance between branching penalty and leaf inflation. -/
def modelRateObjective (a b rate : ℝ) : ℝ :=
  a * rate + b / rate

/-- The model objective under the shorter name used in the estimator analysis. -/
def modelObjective (a b rate : ℝ) : ℝ :=
  a * rate + b / rate

/-- The AM-GM lower bound for the model rate objective. -/
theorem modelRateObjective_ge_amgm (a b rate : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hrate : 0 < rate) :
    2 * Real.sqrt (a * b) ≤ modelRateObjective a b rate := by
  unfold modelRateObjective
  have h1 : 0 ≤ (Real.sqrt (a * rate) - Real.sqrt (b / rate)) ^ 2 := sq_nonneg _
  have hpos1 : 0 < a * rate := mul_pos ha hrate
  have hpos2 : 0 < b / rate := div_pos hb hrate
  have hsq1 : (Real.sqrt (a * rate)) ^ 2 = a * rate := Real.sq_sqrt (le_of_lt hpos1)
  have hsq2 : (Real.sqrt (b / rate)) ^ 2 = b / rate := Real.sq_sqrt (le_of_lt hpos2)
  have hmul : (a * rate) * (b / rate) = a * b := by
    field_simp [ne_of_gt hrate]
  have hsqrt_mul : Real.sqrt (a * rate) * Real.sqrt (b / rate) = Real.sqrt (a * b) := by
    rw [← Real.sqrt_mul (le_of_lt hpos1), hmul]
  have hexp : (Real.sqrt (a * rate) - Real.sqrt (b / rate)) ^ 2 =
      a * rate + b / rate - 2 * Real.sqrt (a * b) := by
    calc
      (Real.sqrt (a * rate) - Real.sqrt (b / rate)) ^ 2 =
          (Real.sqrt (a * rate)) ^ 2 + (Real.sqrt (b / rate)) ^ 2 -
            2 * (Real.sqrt (a * rate) * Real.sqrt (b / rate)) := by ring
      _ = a * rate + b / rate - 2 * Real.sqrt (a * b) := by rw [hsq1, hsq2, hsqrt_mul]
  linarith

/-- The optimal rate attains the minimal objective value. -/
theorem modelRateObjective_at_optimum (a b : ℝ)
    (ha : 0 < a) (hb : 0 < b) :
    modelRateObjective a b (Real.sqrt (b / a)) = 2 * Real.sqrt (a * b) := by
  let rateStar := Real.sqrt (b / a)
  have hrateStar : 0 < rateStar := Real.sqrt_pos.2 (div_pos hb ha)
  have hbRateStar : b = a * rateStar ^ 2 := by
    dsimp [rateStar]
    rw [Real.sq_sqrt (div_nonneg hb.le ha.le)]
    field_simp [ha.ne']
  have hsqrtA : 0 < Real.sqrt a := Real.sqrt_pos.2 ha
  have haDivSqrt : a / Real.sqrt a = Real.sqrt a := by
    apply (div_eq_iff hsqrtA.ne').2
    nlinarith [Real.sq_sqrt ha.le]
  have haRateStar : a * rateStar = Real.sqrt (a * b) := by
    dsimp [rateStar]
    rw [Real.sqrt_div hb.le, Real.sqrt_mul ha.le]
    calc
      a * (Real.sqrt b / Real.sqrt a) =
          (a / Real.sqrt a) * Real.sqrt b := by ring
      _ = Real.sqrt a * Real.sqrt b := by rw [haDivSqrt]
  change modelRateObjective a b rateStar = 2 * Real.sqrt (a * b)
  calc
    modelRateObjective a b rateStar = 2 * (a * rateStar) := by
      unfold modelRateObjective
      rw [hbRateStar]
      field_simp [hrateStar.ne']
      ring
    _ = 2 * Real.sqrt (a * b) := by rw [haRateStar]

/-- AM-GM lower bound for the model objective. -/
theorem modelObjective_ge_amgm (a b rate : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hrate : 0 < rate) :
    2 * Real.sqrt (a * b) ≤ modelObjective a b rate := by
  simpa [modelObjective, modelRateObjective] using
    modelRateObjective_ge_amgm a b rate ha hb hrate

private theorem modelObjective_sub_optimum
    (a b rate : ℝ) (ha : 0 < a) (hb : 0 < b) (hrate : 0 < rate) :
    modelObjective a b rate -
        modelObjective a b (Real.sqrt (b / a)) =
      a * (rate - Real.sqrt (b / a)) ^ 2 / rate := by
  let rateStar := Real.sqrt (b / a)
  have hrateStar : 0 < rateStar := Real.sqrt_pos.2 (div_pos hb ha)
  have hbRateStar : b = a * rateStar ^ 2 := by
    dsimp [rateStar]
    rw [Real.sq_sqrt (div_nonneg hb.le ha.le)]
    field_simp [ha.ne']
  change modelObjective a b rate - modelObjective a b rateStar =
    a * (rate - rateStar) ^ 2 / rate
  unfold modelObjective
  rw [hbRateStar]
  field_simp [hrate.ne', hrateStar.ne']
  ring

/-- Equality in the AM-GM bound holds exactly at the optimal positive rate. -/
theorem modelObjective_eq_lower_bound_iff
    (a b rate : ℝ) (ha : 0 < a) (hb : 0 < b) (hrate : 0 < rate) :
    modelObjective a b rate = 2 * Real.sqrt (a * b) ↔
      rate = Real.sqrt (b / a) := by
  constructor
  · intro hvalue
    have hopt :
        modelObjective a b (Real.sqrt (b / a)) =
          2 * Real.sqrt (a * b) := by
      simpa [modelObjective, modelRateObjective] using
        modelRateObjective_at_optimum a b ha hb
    have hzero : a * (rate - Real.sqrt (b / a)) ^ 2 / rate = 0 := by
      rw [← modelObjective_sub_optimum a b rate ha hb hrate, hvalue, hopt,
        sub_self]
    have hmul : a * (rate - Real.sqrt (b / a)) ^ 2 = 0 :=
      (div_eq_zero_iff.mp hzero).resolve_right hrate.ne'
    have hsquare : (rate - Real.sqrt (b / a)) ^ 2 = 0 :=
      (mul_eq_zero.mp hmul).resolve_left ha.ne'
    nlinarith
  · rintro rfl
    simpa [modelObjective, modelRateObjective] using
      modelRateObjective_at_optimum a b ha hb

end

end EstimatorIntegrity
