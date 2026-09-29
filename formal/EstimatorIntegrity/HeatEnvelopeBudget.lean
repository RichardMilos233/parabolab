import Mathlib.Tactic

/-!
# Finite coefficient budget for the Gaussian heat envelope

This module verifies the finite real inequalities in Section 10 of the
noncompact quadratic audit.  It does not formalize the heat-kernel calculus,
the exponential substitution, supersolution comparison, branching trees, or
the signed PDE correspondence.
-/

namespace EstimatorIntegrity

noncomputable section

/-- The time integral `I₀ = 2 / (d - 2)` used by the heat envelope. -/
def heatI0 (d : ℝ) : ℝ := 2 / (d - 2)

/-- The first time moment `I₁ = 4 / ((d - 2)(d - 4))`. -/
def heatI1 (d : ℝ) : ℝ := 4 / ((d - 2) * (d - 4))

/-- The coefficient `C = 2 + 16 d I₀`. -/
def heatEnvelopeC (d : ℝ) : ℝ := 2 + 16 * d * heatI0 d

/-- The infinite-time scalar budget `J_*`. -/
def heatEnvelopeJstar (d ε : ℝ) : ℝ :=
  2 * ε * heatI0 d + 2 * heatEnvelopeC d * ε ^ 2 * heatI1 d

/-- For real dimension parameter `d ≥ 5`, `I₀` is positive and at most `2/3`. -/
theorem heatI0_pos_le (d : ℝ) (hd : 5 ≤ d) :
    0 < heatI0 d ∧ heatI0 d ≤ 2 / 3 := by
  have hd2 : 0 < d - 2 := by
    nlinarith
  constructor
  · exact div_pos (by norm_num) hd2
  · rw [heatI0, div_le_iff₀ hd2]
    nlinarith

/-- For `d ≥ 5`, `I₁` is positive and at most `4/3`. -/
theorem heatI1_pos_le (d : ℝ) (hd : 5 ≤ d) :
    0 < heatI1 d ∧ heatI1 d ≤ 4 / 3 := by
  have hd2 : 0 < d - 2 := by
    nlinarith
  have hd4 : 0 < d - 4 := by
    nlinarith
  have hdenom : 0 < (d - 2) * (d - 4) := mul_pos hd2 hd4
  constructor
  · exact div_pos (by norm_num) hdenom
  · rw [heatI1, div_le_iff₀ hdenom]
    nlinarith [mul_nonneg (show 0 ≤ d - 5 by nlinarith)
      (show 0 ≤ d - 2 by nlinarith)]

/-- The dimension ratio used to bound `C` is at most `5/3`. -/
theorem heatDimensionRatio_le (d : ℝ) (hd : 5 ≤ d) :
    d / (d - 2) ≤ 5 / 3 := by
  have hd2 : 0 < d - 2 := by
    nlinarith
  rw [div_le_iff₀ hd2]
  nlinarith

/-- The envelope coefficient is positive and obeys the audited bound
`C ≤ 166/3`. -/
theorem heatEnvelopeC_pos_le (d : ℝ) (hd : 5 ≤ d) :
    0 < heatEnvelopeC d ∧ heatEnvelopeC d ≤ 166 / 3 := by
  have hI0 := (heatI0_pos_le d hd).1
  have hd_nonneg : 0 ≤ d := by
    nlinarith
  have hratio := heatDimensionRatio_le d hd
  have hform : heatEnvelopeC d = 2 + 32 * (d / (d - 2)) := by
    simp only [heatEnvelopeC, heatI0]
    ring
  constructor
  · simp only [heatEnvelopeC]
    positivity
  · rw [hform]
    nlinarith

/-- Under `0 < ε ≤ 1/32`, the infinite-time scalar budget lies in the
audited interval and is strictly below `1/4`. -/
theorem heatEnvelopeJstar_nonneg_le (d ε : ℝ)
    (hd : 5 ≤ d) (hε : 0 < ε) (hε_le : ε ≤ 1 / 32) :
    0 ≤ heatEnvelopeJstar d ε ∧
      heatEnvelopeJstar d ε ≤ 107 / 576 ∧
      (107 / 576 : ℝ) < 1 / 4 := by
  obtain ⟨hI0_pos, hI0_le⟩ := heatI0_pos_le d hd
  obtain ⟨hI1_pos, hI1_le⟩ := heatI1_pos_le d hd
  obtain ⟨hC_pos, hC_le⟩ := heatEnvelopeC_pos_le d hd
  have hε_nonneg : 0 ≤ ε := hε.le
  have hfirst : 2 * ε * heatI0 d ≤ 1 / 24 := by
    calc
      2 * ε * heatI0 d ≤ 2 * (1 / 32) * (2 / 3) := by
        gcongr
      _ = 1 / 24 := by norm_num
  have hsecond :
      2 * heatEnvelopeC d * ε ^ 2 * heatI1 d ≤ 83 / 576 := by
    calc
      2 * heatEnvelopeC d * ε ^ 2 * heatI1 d ≤
          2 * (166 / 3) * (1 / 32) ^ 2 * (4 / 3) := by
        gcongr
      _ = 83 / 576 := by norm_num
  constructor
  · simp only [heatEnvelopeJstar]
    exact add_nonneg
      (mul_nonneg (mul_nonneg (by norm_num) hε_nonneg) hI0_pos.le)
      (mul_nonneg
        (mul_nonneg (mul_nonneg (by norm_num) hC_pos.le) (sq_nonneg ε))
        hI1_pos.le)
  · constructor
    · simp only [heatEnvelopeJstar]
      nlinarith
    · norm_num

/-- The finite scalar expression defining `a` is nonnegative and has the
two-step upper bound used by the supersolution argument. -/
theorem heatEnvelopeA_bounds (d ε j h E a : ℝ)
    (hd : 5 ≤ d) (hε : 0 < ε) (hε_le : ε ≤ 1 / 32)
    (hj : 0 ≤ j) (hj_le : j ≤ 1 / 4)
    (hh : 0 ≤ h) (hh_le : h ≤ heatI0 d)
    (hE : 0 ≤ E) (hE_le : E ≤ 2)
    (ha : a = ε ^ 2 * (1 + heatEnvelopeC d * j + 4 * d * E * h)) :
    0 ≤ a ∧
      a ≤ 3 * heatEnvelopeC d * ε ^ 2 / 4 ∧
      3 * heatEnvelopeC d * ε ^ 2 / 4 ≤ heatEnvelopeC d * ε ^ 2 := by
  have hd_nonneg : 0 ≤ d := by
    nlinarith
  have hI0_pos := (heatI0_pos_le d hd).1
  have hC_pos := (heatEnvelopeC_pos_le d hd).1
  have hCj : heatEnvelopeC d * j ≤ heatEnvelopeC d * (1 / 4) := by
    gcongr
  have hDEh : 4 * d * E * h ≤ 8 * d * heatI0 d := by
    calc
      4 * d * E * h ≤ 4 * d * 2 * heatI0 d := by
        gcongr
      _ = 8 * d * heatI0 d := by ring
  have hidentity :
      1 + heatEnvelopeC d * (1 / 4) + 8 * d * heatI0 d =
        3 * heatEnvelopeC d / 4 := by
    simp only [heatEnvelopeC]
    ring
  have hbracket :
      1 + heatEnvelopeC d * j + 4 * d * E * h ≤
        3 * heatEnvelopeC d / 4 := by
    nlinarith
  have ha_upper : a ≤ 3 * heatEnvelopeC d * ε ^ 2 / 4 := by
    calc
      a = ε ^ 2 * (1 + heatEnvelopeC d * j + 4 * d * E * h) := ha
      _ ≤ ε ^ 2 * (3 * heatEnvelopeC d / 4) :=
        mul_le_mul_of_nonneg_left hbracket (sq_nonneg ε)
      _ = 3 * heatEnvelopeC d * ε ^ 2 / 4 := by ring
  have hlast :
      3 * heatEnvelopeC d * ε ^ 2 / 4 ≤ heatEnvelopeC d * ε ^ 2 := by
    have hCε : 0 ≤ heatEnvelopeC d * ε ^ 2 :=
      mul_nonneg hC_pos.le (sq_nonneg ε)
    nlinarith
  constructor
  · rw [ha]
    positivity
  · exact ⟨ha_upper, hlast⟩

/-- All three finite coefficient comparisons required in the differentiated
Gaussian supersolution budget. -/
theorem heatEnvelopeCoefficientBudget (d ε j h E b a δ : ℝ)
    (hd : 5 ≤ d) (hε : 0 < ε) (hε_le : ε ≤ 1 / 32)
    (hj : 0 ≤ j) (hj_le : j ≤ 1 / 4)
    (hh : 0 ≤ h) (hh_le : h ≤ heatI0 d)
    (hE : 0 ≤ E) (hE_le : E ≤ 2) (hb : 0 ≤ b)
    (ha : a = ε ^ 2 * (1 + heatEnvelopeC d * j + 4 * d * E * h))
    (hδ : δ ^ 2 ≤ 4 * ε ^ 2 * E) :
    a ≤ 3 * heatEnvelopeC d * ε ^ 2 / 4 ∧
      3 * heatEnvelopeC d * ε ^ 2 / 4 ≤ heatEnvelopeC d * ε ^ 2 ∧
      heatEnvelopeC d * ε ^ 2 * b + 4 * d * ε ^ 2 * E ≥
        a * b + d * δ ^ 2 ∧
      2 * heatEnvelopeC d * ε ^ 2 ≥ 2 * a := by
  obtain ⟨ha_nonneg, ha_three_quarters, hthree_quarters⟩ :=
    heatEnvelopeA_bounds d ε j h E a hd hε hε_le hj hj_le hh hh_le hE hE_le ha
  have hd_nonneg : 0 ≤ d := by
    nlinarith
  have ha_C : a ≤ heatEnvelopeC d * ε ^ 2 :=
    ha_three_quarters.trans hthree_quarters
  have hab : a * b ≤ heatEnvelopeC d * ε ^ 2 * b :=
    mul_le_mul_of_nonneg_right ha_C hb
  have hδ_scaled : d * δ ^ 2 ≤ d * (4 * ε ^ 2 * E) :=
    mul_le_mul_of_nonneg_left hδ hd_nonneg
  refine ⟨ha_three_quarters, hthree_quarters, ?_, ?_⟩
  · nlinarith
  · nlinarith

end

end EstimatorIntegrity
