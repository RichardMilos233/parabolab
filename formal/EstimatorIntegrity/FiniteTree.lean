import Mathlib.Data.ENNReal.BigOperators

namespace EstimatorIntegrity

noncomputable section

/-- A finite labelled mechanism table. Lists retain duplicate tuples. -/
structure FiniteMechanism (C : Type*) where
  tuples : C → List (List C)
  nonempty_tuples : ∀ c, tuples c ≠ []

/-- A code-indexed vector of extended nonnegative moments. -/
abbrev MomentVector (C : Type*) := C → ENNReal

/-- One algebraic step of the finite moment recursion. -/
def momentStep
    {C : Type*}
    [Fintype C]
    [DecidableEq C]
    (M : FiniteMechanism C)
    (leaf : MomentVector C)
    (branch : (c : C) → Fin (M.tuples c).length → ENNReal)
    (v : MomentVector C) : MomentVector C :=
  fun c =>
    leaf c +
      ∑ i : Fin (M.tuples c).length,
        branch c i * (((M.tuples c).get i).map v).prod

end

end EstimatorIntegrity
