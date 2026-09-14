import Mathlib.Algebra.Order.Archimedean.Real.Basic
import Mathlib.Tactic.Linarith

/-!
# Deterministic certificates for rate selection

These transfer lemmas assume finite real-valued second moments, a one-sided
truncation, numerical error bounds, and an optimization error bound. They do
not prove stochastic integrability, a truncation-tail estimate, quadrature
accuracy, existence of a minimizing rate, or identification with a PDE solution.
The candidate type is arbitrary: instantiate it with positive real rates or
with an already restricted candidate set as appropriate.
-/

namespace EstimatorIntegrity

noncomputable section

/-- A one-sided truncation requires only one tail term in the selected rate's
excess second moment. The numerical error is paid at the selected rate and at
the comparison rate. This is a conditional deterministic transfer lemma. -/
theorem rateSelection_excess_le {α : Type*}
    (M MK numerical : α → ℝ) (I : Set α) (selected comparison : α)
    (tail δ η : ℝ)
    (hselected : selected ∈ I) (hcomparison : comparison ∈ I)
    (hkilled : ∀ rate ∈ I, MK rate ≤ M rate)
    (htail : M selected ≤ MK selected + tail)
    (herror : ∀ rate ∈ I, |numerical rate - MK rate| ≤ δ)
    (hopt : ∀ rate ∈ I, numerical selected ≤ numerical rate + η) :
    M selected - M comparison ≤ tail + 2 * δ + η := by
  linarith [hkilled comparison hcomparison,
    (abs_le.mp (herror selected hselected)).1,
    (abs_le.mp (herror comparison hcomparison)).2,
    hopt comparison hcomparison]

/-- The pairwise certificate also bounds excess above the infimum, without
assuming that the objective attains a minimum on the candidate set. -/
theorem rateSelection_excess_le_inf {α : Type*}
    (M MK numerical : α → ℝ) (I : Set α) (selected : α)
    (tail δ η : ℝ)
    (hselected : selected ∈ I)
    (hkilled : ∀ rate ∈ I, MK rate ≤ M rate)
    (htail : M selected ≤ MK selected + tail)
    (herror : ∀ rate ∈ I, |numerical rate - MK rate| ≤ δ)
    (hopt : ∀ rate ∈ I, numerical selected ≤ numerical rate + η) :
    M selected - sInf (M '' I) ≤ tail + 2 * δ + η := by
  rw [sub_le_comm]
  apply le_csInf (show (M '' I).Nonempty from ⟨M selected, selected, hselected, rfl⟩)
  exact fun _ ⟨comparison, hcomparison, heq⟩ =>
    heq ▸ sub_le_comm.mp (rateSelection_excess_le M MK numerical I selected comparison
      tail δ η hselected hcomparison hkilled htail herror hopt)

/-- An incumbent upper bound and a global lower bound on the killed objective
certify excess above the infimum over the entire candidate type. For positive
rates use that positive-rate subtype as `α`; restricting `α` restricts the claim. -/
theorem upperLower_excess_le_inf {α : Type*}
    (M MK : α → ℝ) (selected : α) (upper lower : ℝ)
    (hkilled : ∀ rate, MK rate ≤ M rate)
    (hupper : M selected ≤ upper)
    (hlower : ∀ rate, lower ≤ MK rate) :
    M selected - sInf (Set.range M) ≤ upper - lower := by
  have hbound : lower ≤ sInf (Set.range M) :=
    le_csInf (show (Set.range M).Nonempty from ⟨M selected, selected, rfl⟩)
      (fun _ ⟨rate, heq⟩ => heq ▸ (hlower rate).trans (hkilled rate))
  linarith

/-- With a common mean, subtracting its square preserves the same additive
excess bound. Applying this to actual variances requires finite second moments
and a separately established rate-invariant mean. -/
theorem commonMean_variance_excess_le
    (selectedMoment comparisonMoment mean gap : ℝ)
    (hgap : selectedMoment - comparisonMoment ≤ gap) :
    (selectedMoment - mean ^ 2) - (comparisonMoment - mean ^ 2) ≤ gap := by
  linarith

/-- Interval and exterior lower bounds cover every positive rate. The exterior
bounds are assumptions here; in an application they may come from individual
tree-topology contributions. No exponential envelope is proved by this lemma. -/
theorem global_lower_of_interval_and_exterior
    (M : ℝ → ℝ) (left right lower : ℝ)
    (hinterval : ∀ rate ∈ Set.Icc left right, lower ≤ M rate)
    (hleft : ∀ rate, 0 < rate → rate < left → lower ≤ M rate)
    (hright : ∀ rate, 0 < rate → right < rate → lower ≤ M rate)
    (rate : ℝ) (hrate : 0 < rate) : lower ≤ M rate := by
  exact (lt_or_ge rate left).elim (hleft rate hrate)
    (fun hlo => (le_or_gt rate right).elim
      (fun hhi => hinterval rate ⟨hlo, hhi⟩) (hright rate hrate))

end

end EstimatorIntegrity
