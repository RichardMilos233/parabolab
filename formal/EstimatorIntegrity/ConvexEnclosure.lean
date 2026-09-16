import Mathlib.Analysis.Convex.Slope
import Mathlib.Data.Real.Basic

/-!
# Convex extrapolation from certified point enclosures

These are deterministic consequences of `ConvexOn` for a finite real-valued
objective. The lower bounds extrapolate outside the pair of sampled points;
the chord inside that pair is not asserted to be a lower bound. Convexity of
the stochastic objective, finiteness, and correctness of the input numerical
enclosures are assumptions, not conclusions of this file.
-/

namespace EstimatorIntegrity

noncomputable section

/-- Cross-multiplied right-ray extrapolation, using a lower value at the near
endpoint and an upper value at the far endpoint. -/
private theorem convexEnclosure_right_cross_strict
    (f : ℝ → ℝ) (S : Set ℝ) (a b x lowerB upperA : ℝ)
    (hf : ConvexOn ℝ S f) (ha : a ∈ S) (hx : x ∈ S)
    (hab : a < b) (hbx : b < x)
    (hlower : lowerB ≤ f b) (hupper : f a ≤ upperA) :
    (b - a) * lowerB + (x - b) * (lowerB - upperA) ≤ (b - a) * f x := by
  nlinarith [hf.secant_mono_aux1 ha hx hab hbx,
    mul_nonneg (sub_nonneg.mpr (hab.le.trans hbx.le)) (sub_nonneg.mpr hlower),
    mul_nonneg (sub_nonneg.mpr hbx.le) (sub_nonneg.mpr hupper)]

/-- A certified secant gives a lower affine bound to the right of its sampled
pair. Its endpoint-bound orientation is essential: use `lowerB - upperA`. -/
theorem convexEnclosure_right
    (f : ℝ → ℝ) (S : Set ℝ) (a b x lowerB upperA : ℝ)
    (hf : ConvexOn ℝ S f) (ha : a ∈ S) (hx : x ∈ S)
    (hab : a < b) (hbx : b ≤ x)
    (hlower : lowerB ≤ f b) (hupper : f a ≤ upperA) :
    lowerB + (x - b) * (lowerB - upperA) / (b - a) ≤ f x := by
  rcases eq_or_lt_of_le hbx with rfl | hbx
  · simpa using hlower
  · apply le_sub_iff_add_le'.mp ((div_le_iff₀ (sub_pos.mpr hab)).mpr ?_)
    nlinarith [convexEnclosure_right_cross_strict f S a b x lowerB upperA
      hf ha hx hab hbx hlower hupper]

/-- The cross-multiplied left-ray counterpart. -/
private theorem convexEnclosure_left_cross_strict
    (f : ℝ → ℝ) (S : Set ℝ) (a b x lowerA upperB : ℝ)
    (hf : ConvexOn ℝ S f) (hx : x ∈ S) (hb : b ∈ S)
    (hxa : x < a) (hab : a < b)
    (hlower : lowerA ≤ f a) (hupper : f b ≤ upperB) :
    (b - a) * lowerA + (x - a) * (upperB - lowerA) ≤ (b - a) * f x := by
  nlinarith [hf.secant_mono_aux1 hx hb hxa hab,
    mul_nonneg (sub_nonneg.mpr (hxa.le.trans hab.le)) (sub_nonneg.mpr hlower),
    mul_nonneg (sub_nonneg.mpr hxa.le) (sub_nonneg.mpr hupper)]

/-- A certified secant gives a lower affine bound to the left of its sampled
pair. Because `x - a ≤ 0`, its slope uses `upperB - lowerA`. -/
theorem convexEnclosure_left
    (f : ℝ → ℝ) (S : Set ℝ) (a b x lowerA upperB : ℝ)
    (hf : ConvexOn ℝ S f) (hx : x ∈ S) (hb : b ∈ S)
    (hxa : x ≤ a) (hab : a < b)
    (hlower : lowerA ≤ f a) (hupper : f b ≤ upperB) :
    lowerA + (x - a) * (upperB - lowerA) / (b - a) ≤ f x := by
  rcases eq_or_lt_of_le hxa with rfl | hxa
  · simpa using hlower
  · apply le_sub_iff_add_le'.mp ((div_le_iff₀ (sub_pos.mpr hab)).mpr ?_)
    nlinarith [convexEnclosure_left_cross_strict f S a b x lowerA upperB
      hf hx hb hxa hab hlower hupper]

/-- A certified nonnegative last secant gives a constant lower bound on the
entire right exterior ray within the convexity domain. -/
theorem convexEnclosure_right_exterior
    (f : ℝ → ℝ) (S : Set ℝ) (a b x lowerB upperA : ℝ)
    (hf : ConvexOn ℝ S f) (ha : a ∈ S) (hx : x ∈ S)
    (hab : a < b) (hbx : b ≤ x)
    (hlower : lowerB ≤ f b) (hupper : f a ≤ upperA)
    (hincreasing : upperA ≤ lowerB) : lowerB ≤ f x := by
  exact (le_add_of_nonneg_right
    (div_nonneg (mul_nonneg (sub_nonneg.mpr hbx) (sub_nonneg.mpr hincreasing))
      (sub_nonneg.mpr hab.le))).trans
    (convexEnclosure_right f S a b x lowerB upperA hf ha hx hab hbx hlower hupper)

/-- A certified nonpositive first secant gives a constant lower bound on the
entire left exterior ray within the convexity domain. -/
theorem convexEnclosure_left_exterior
    (f : ℝ → ℝ) (S : Set ℝ) (a b x lowerA upperB : ℝ)
    (hf : ConvexOn ℝ S f) (hx : x ∈ S) (hb : b ∈ S)
    (hxa : x ≤ a) (hab : a < b)
    (hlower : lowerA ≤ f a) (hupper : f b ≤ upperB)
    (hdecreasing : upperB ≤ lowerA) : lowerA ≤ f x := by
  exact (le_add_of_nonneg_right
    (div_nonneg
      (mul_nonneg_of_nonpos_of_nonpos (sub_nonpos.mpr hxa) (sub_nonpos.mpr hdecreasing))
      (sub_nonneg.mpr hab.le))).trans
    (convexEnclosure_left f S a b x lowerA upperB hf hx hb hxa hab hlower hupper)

/-- On a cell between two neighboring sampled pairs, both outward secant
extrapolations are valid. Their maximum is therefore a pointwise lower
envelope. This does not formalize the numerical minimization of that envelope. -/
theorem convexEnclosure_cell_lower_envelope
    (f : ℝ → ℝ) (S : Set ℝ) (a b c d x lowerB upperA lowerC upperD : ℝ)
    (hf : ConvexOn ℝ S f) (ha : a ∈ S) (hd : d ∈ S) (hx : x ∈ S)
    (hab : a < b) (hcd : c < d) (hbx : b ≤ x) (hxc : x ≤ c)
    (hlowerB : lowerB ≤ f b) (hupperA : f a ≤ upperA)
    (hlowerC : lowerC ≤ f c) (hupperD : f d ≤ upperD) :
    max (lowerB + (x - b) * (lowerB - upperA) / (b - a))
      (lowerC + (x - c) * (upperD - lowerC) / (d - c)) ≤ f x := by
  exact max_le
    (convexEnclosure_right f S a b x lowerB upperA hf ha hx hab hbx hlowerB hupperA)
    (convexEnclosure_left f S c d x lowerC upperD hf hx hd hxc hcd hlowerC hupperD)

end

end EstimatorIntegrity
