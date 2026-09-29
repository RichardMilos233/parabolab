import EstimatorIntegrity.LongHorizonAlgebra

/-!
# Deterministic long-horizon Allen--Cahn algebra

This module formalizes the scalar polynomial algebra and the bounded ternary
reaction enclosure used in the long-horizon comparison.  It does not identify
either construction with a stochastic tree or a PDE solution, and it does not
formalize the improper integral used to derive the raw absolute-moment horizon.
-/

namespace EstimatorIntegrity

noncomputable section

/-- The rate-two ternary reaction maps the cube `[-1,1]³` into `[-1,1]`. -/
theorem boundedReaction_two_mem_Icc
    {a b c : ℝ} (ha : a ∈ Set.Icc (-1 : ℝ) 1)
    (hb : b ∈ Set.Icc (-1 : ℝ) 1) (hc : c ∈ Set.Icc (-1 : ℝ) 1) :
    boundedReaction 2 a b c ∈ Set.Icc (-1 : ℝ) 1 := by
  rw [boundedReaction_two]
  constructor
  · have hab : 0 ≤ 1 - a * b := by
      nlinarith [mul_nonneg (sub_nonneg.mpr ha.2)
        (neg_le_iff_add_nonneg'.mp hb.1),
        mul_nonneg (neg_le_iff_add_nonneg'.mp ha.1) (sub_nonneg.mpr hb.2)]
    nlinarith [mul_nonneg (neg_le_iff_add_nonneg'.mp ha.1)
      (neg_le_iff_add_nonneg'.mp hb.1),
      mul_nonneg (neg_le_iff_add_nonneg'.mp hc.1) hab]
  · have hab : 0 ≤ 1 - a * b := by
      nlinarith [mul_nonneg (sub_nonneg.mpr ha.2)
        (neg_le_iff_add_nonneg'.mp hb.1),
        mul_nonneg (neg_le_iff_add_nonneg'.mp ha.1) (sub_nonneg.mpr hb.2)]
    nlinarith [mul_nonneg (sub_nonneg.mpr ha.2) (sub_nonneg.mpr hb.2),
      mul_nonneg (sub_nonneg.mpr hc.2) hab]

/-- The arithmetic mean of three points in `[-1,1]` stays in `[-1,1]`. -/
theorem ternaryAverage_mem_Icc
    {a b c : ℝ} (ha : a ∈ Set.Icc (-1 : ℝ) 1)
    (hb : b ∈ Set.Icc (-1 : ℝ) 1) (hc : c ∈ Set.Icc (-1 : ℝ) 1) :
    (a + b + c) / 3 ∈ Set.Icc (-1 : ℝ) 1 := by
  constructor
  · nlinarith [ha.1, hb.1, hc.1]
  · nlinarith [ha.2, hb.2, hc.2]

/-- Every rate `r ≥ 2` maps the cube `[-1,1]³` into `[-1,1]`. -/
theorem boundedReaction_mem_Icc
    (r : ℝ) (hr : 2 ≤ r) {a b c : ℝ}
    (ha : a ∈ Set.Icc (-1 : ℝ) 1)
    (hb : b ∈ Set.Icc (-1 : ℝ) 1) (hc : c ∈ Set.Icc (-1 : ℝ) 1) :
    boundedReaction r a b c ∈ Set.Icc (-1 : ℝ) 1 := by
  rw [boundedReaction_convex_decomposition r a b c
    (ne_of_gt (lt_of_lt_of_le zero_lt_two hr))]
  have hB := boundedReaction_two_mem_Icc ha hb hc
  have hA := ternaryAverage_mem_Icc ha hb hc
  have hr0 : 0 < r := lt_of_lt_of_le zero_lt_two hr
  have hw0 : 0 ≤ 2 / r := div_nonneg zero_le_two hr0.le
  have hw1 : 2 / r ≤ 1 := (div_le_one hr0).2 hr
  constructor
  · nlinarith [mul_nonneg hw0 (neg_le_iff_add_nonneg'.mp hB.1),
      mul_nonneg (sub_nonneg.mpr hw1) (neg_le_iff_add_nonneg'.mp hA.1)]
  · nlinarith [mul_nonneg hw0 (sub_nonneg.mpr hB.2),
      mul_nonneg (sub_nonneg.mpr hw1) (sub_nonneg.mpr hA.2)]

/-- A finite full ternary tree. -/
inductive BoundedTernaryTree (A : Type*) where
  | leaf : A → BoundedTernaryTree A
  | node : BoundedTernaryTree A → BoundedTernaryTree A →
      BoundedTernaryTree A → BoundedTernaryTree A

/-- Evaluate a finite ternary tree with bounded leaves using `boundedReaction`. -/
def BoundedTernaryTree.eval (r : ℝ) :
    BoundedTernaryTree (Set.Icc (-1 : ℝ) 1) → ℝ
  | .leaf x => x.1
  | .node left middle right =>
      boundedReaction r (eval r left) (eval r middle) (eval r right)

/-- Every finite ternary-tree evaluation is bounded whenever `r ≥ 2`. -/
theorem BoundedTernaryTree.eval_mem_Icc
    (r : ℝ) (hr : 2 ≤ r)
    (tree : BoundedTernaryTree (Set.Icc (-1 : ℝ) 1)) :
    tree.eval r ∈ Set.Icc (-1 : ℝ) 1 := by
  induction tree with
  | leaf x => exact x.2
  | node left middle right hleft hmiddle hright =>
      exact boundedReaction_mem_Icc r hr hleft hmiddle hright

end

end EstimatorIntegrity
