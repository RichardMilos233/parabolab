import Mathlib.Analysis.Convex.Function
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

/-!
# Weighted profiles and deterministic tuning-cost comparisons

These lemmas concern finite real-valued objectives and a continuous-budget
cost model. They do not prove stochastic integrability, sampling independence,
wall-clock concentration, or the validity of replacing integer sample counts
by real numbers. For a profile, the work-variance product below is the sum of
per-node tree costs multiplied by the weighted sum of pointwise variances, with equal
sample counts at every profile node.
-/

namespace EstimatorIntegrity

open scoped BigOperators

noncomputable section

/-- Per-profile loss in the continuous-budget model. `workVariance = cost *
variance`, and positive `budget - setup` is required for its interpretation. -/
def amortizedProfileLoss (budget setup reuse workVariance : ℝ) : ℝ :=
  reuse * workVariance / (budget - setup)

/-- Positive remaining budgets allow exact cross multiplication; positive
reuse cancels. All timing and variance inputs remain model assumptions. -/
theorem amortizedProfileLoss_lt_iff
    (budget setupA setupB reuse workA workB : ℝ)
    (hbudgetA : setupA < budget) (hbudgetB : setupB < budget)
    (hreuse : 0 < reuse) :
    amortizedProfileLoss budget setupA reuse workA <
        amortizedProfileLoss budget setupB reuse workB ↔
      workA * (budget - setupB) < workB * (budget - setupA) := by
  simp only [amortizedProfileLoss,
    div_lt_div_iff₀ (sub_pos.mpr hbudgetA) (sub_pos.mpr hbudgetB),
    mul_assoc, mul_lt_mul_iff_right₀ hreuse]

/-- When method A has the smaller work-variance product, its exact continuous
budget break-even threshold is the stated fraction. Both methods must still
have positive remaining budgets; the threshold alone is insufficient. -/
theorem amortizedProfileLoss_break_even
    (budget setupA setupB reuse workA workB : ℝ)
    (hbudgetA : setupA < budget) (hbudgetB : setupB < budget)
    (hreuse : 0 < reuse) (hwork : workA < workB) :
    amortizedProfileLoss budget setupA reuse workA <
        amortizedProfileLoss budget setupB reuse workB ↔
      (workB * setupA - workA * setupB) / (workB - workA) < budget := by
  rw [amortizedProfileLoss_lt_iff budget setupA setupB reuse workA workB
    hbudgetA hbudgetB hreuse, div_lt_iff₀ (sub_pos.mpr hwork)]
  constructor
  all_goals intro h
  all_goals nlinarith

/-- At fixed budget per reused profile, the total budget grows with `reuse`.
The threshold is valid only when that total budget covers both setup costs. -/
theorem amortizedProfileLoss_reuse_break_even
    (budgetPerProfile setupA setupB reuse workA workB : ℝ)
    (hbudget : 0 < budgetPerProfile)
    (hbudgetA : setupA < reuse * budgetPerProfile)
    (hbudgetB : setupB < reuse * budgetPerProfile)
    (hreuse : 0 < reuse) (hwork : workA < workB) :
    amortizedProfileLoss (reuse * budgetPerProfile) setupA reuse workA <
        amortizedProfileLoss (reuse * budgetPerProfile) setupB reuse workB ↔
      (workB * setupA - workA * setupB) /
        (budgetPerProfile * (workB - workA)) < reuse := by
  rw [amortizedProfileLoss_break_even (reuse * budgetPerProfile)
    setupA setupB reuse workA workB hbudgetA hbudgetB hreuse hwork,
    mul_comm budgetPerProfile (workB - workA), ← div_div, div_lt_iff₀ hbudget]

/-- Substituting the continuous count `(budget - setup) / (reuse * cost)`
into `variance / count` gives the loss model. This is a field identity; a
sampling interpretation separately requires positive costs and counts. -/
theorem continuousBudget_profileLoss
    (budget setup reuse cost variance : ℝ) :
    variance / ((budget - setup) / (reuse * cost)) =
      amortizedProfileLoss budget setup reuse (cost * variance) := by
  simp only [amortizedProfileLoss, div_div_eq_mul_div, mul_comm, mul_left_comm]

/-- Fixed nonnegative profile weights preserve convexity. Weight normalization
is unnecessary for this conclusion; the domain is explicitly convex even for
an empty profile. -/
theorem weightedProfile_convexOn {ι : Type*}
    (indices : Finset ι) (weights : ι → ℝ) (f : ι → ℝ → ℝ) (S : Set ℝ)
    (hS : Convex ℝ S) (hweights : ∀ i ∈ indices, 0 ≤ weights i)
    (hf : ∀ i ∈ indices, ConvexOn ℝ S (f i)) :
    ConvexOn ℝ S (fun rate => ∑ i ∈ indices, weights i * f i rate) := by
  refine ⟨hS, fun x hx y hy a b ha hb hab => ?_⟩
  have hsum : (∑ i ∈ indices, weights i * f i (a • x + b • y)) ≤
      ∑ i ∈ indices, (a * (weights i * f i x) + b * (weights i * f i y)) :=
    Finset.sum_le_sum (fun i hi => ((hf i hi).smul (hweights i hi)).2 hx hy ha hb hab)
  simpa only [Finset.sum_add_distrib, ← Finset.mul_sum, smul_eq_mul] using hsum

/-- Nonnegative fixed weights transfer point enclosures to a profile enclosure. -/
theorem weightedProfile_enclosure {ι : Type*}
    (indices : Finset ι) (weights lower values upper : ι → ℝ)
    (hweights : ∀ i ∈ indices, 0 ≤ weights i)
    (hinterval : ∀ i ∈ indices, lower i ≤ values i ∧ values i ≤ upper i) :
    (∑ i ∈ indices, weights i * lower i) ≤ (∑ i ∈ indices, weights i * values i) ∧
      (∑ i ∈ indices, weights i * values i) ≤ (∑ i ∈ indices, weights i * upper i) := by
  exact ⟨Finset.sum_le_sum (fun i hi =>
    mul_le_mul_of_nonneg_left (hinterval i hi).1 (hweights i hi)),
    Finset.sum_le_sum (fun i hi =>
      mul_le_mul_of_nonneg_left (hinterval i hi).2 (hweights i hi))⟩

/-- Selected-node upper bounds and comparison-node lower bounds give an
additive profile excess bound. For rate selection, instantiate both node
vectors with their respective common profile rates. -/
theorem weightedProfile_excess_le {ι : Type*}
    (indices : Finset ι) (weights selected comparison upper lower : ι → ℝ)
    (hweights : ∀ i ∈ indices, 0 ≤ weights i)
    (hupper : ∀ i ∈ indices, selected i ≤ upper i)
    (hlower : ∀ i ∈ indices, lower i ≤ comparison i) :
    (∑ i ∈ indices, weights i * selected i) -
        (∑ i ∈ indices, weights i * comparison i) ≤
      (∑ i ∈ indices, weights i * upper i) - (∑ i ∈ indices, weights i * lower i) := by
  exact sub_le_sub
    (Finset.sum_le_sum (fun i hi => mul_le_mul_of_nonneg_left (hupper i hi) (hweights i hi)))
    (Finset.sum_le_sum (fun i hi => mul_le_mul_of_nonneg_left (hlower i hi) (hweights i hi)))

/-- Subtracting the pointwise mean squares shifts the weighted second moment
by a fixed constant. Identifying these quantities with stochastic variances
requires separately established finite moments and means. -/
theorem weightedProfile_variance_shift {ι : Type*}
    (indices : Finset ι) (weights moments means : ι → ℝ) :
    (∑ i ∈ indices, weights i * (moments i - means i ^ 2)) =
      (∑ i ∈ indices, weights i * moments i) - (∑ i ∈ indices, weights i * means i ^ 2) := by
  simp only [mul_sub, Finset.sum_sub_distrib]

/-- Common pointwise means make weighted variance excess exactly equal to
weighted second-moment excess. Thus additive objective-gap bounds transfer
without evaluating the means, provided their rate invariance is established. -/
theorem weightedProfile_variance_excess_eq {ι : Type*}
    (indices : Finset ι) (weights selected comparison means : ι → ℝ) :
    (∑ i ∈ indices, weights i * (selected i - means i ^ 2)) -
        (∑ i ∈ indices, weights i * (comparison i - means i ^ 2)) =
      (∑ i ∈ indices, weights i * selected i) - (∑ i ∈ indices, weights i * comparison i) := by
  simp only [mul_sub, Finset.sum_sub_distrib, sub_sub_sub_cancel_right]

/-- Certified endpoint upper values interpolate to an upper bound at the exact
intermediate rate. The equality `hx` identifies that rate rather than rounding
it to a sampled node. For `a < b` and `a ≤ x ≤ b`, use
`weight = (x - a) / (b - a)` to obtain the usual chord formula. -/
theorem convexProfile_upper_interpolation
    (f : ℝ → ℝ) (S : Set ℝ) (a b x upperA upperB weight : ℝ)
    (hf : ConvexOn ℝ S f) (ha : a ∈ S) (hb : b ∈ S)
    (hweight : 0 ≤ weight) (hweightOne : weight ≤ 1)
    (hx : x = (1 - weight) * a + weight * b)
    (hupperA : f a ≤ upperA) (hupperB : f b ≤ upperB) :
    f x ≤ (1 - weight) * upperA + weight * upperB := by
  rw [hx]
  exact (hf.2 ha hb (sub_nonneg.mpr hweightOne) hweight (sub_add_cancel 1 weight)).trans
    (add_le_add (mul_le_mul_of_nonneg_left hupperA (sub_nonneg.mpr hweightOne))
      (mul_le_mul_of_nonneg_left hupperB hweight))

end

end EstimatorIntegrity
