import EstimatorIntegrity.FiniteTree

namespace EstimatorIntegrity

noncomputable section

variable {C : Type*} [Fintype C] [DecidableEq C]

/-- Picard iteration of the finite moment operator, starting from zero. -/
def picard
    (M : FiniteMechanism C)
    (leaf : MomentVector C)
    (branch : (c : C) → Fin (M.tuples c).length → ENNReal) :
    Nat → MomentVector C
  | 0 => fun _ => 0
  | n + 1 => momentStep M leaf branch (picard M leaf branch n)

theorem momentStep_mono
    (M : FiniteMechanism C)
    (leaf : MomentVector C)
    (branch : (c : C) → Fin (M.tuples c).length → ENNReal)
    {v w : MomentVector C}
    (hvw : ∀ c, v c ≤ w c) :
    ∀ c, momentStep M leaf branch v c ≤
      momentStep M leaf branch w c := by
  intro c
  unfold momentStep
  apply add_le_add_right
  apply Finset.sum_le_sum
  intro i _
  apply mul_le_mul_right
  apply List.prod_le_prod'
  intro z _
  exact hvw z

theorem picard_mono
    (M : FiniteMechanism C)
    (leaf : MomentVector C)
    (branch : (c : C) → Fin (M.tuples c).length → ENNReal) :
    Monotone (picard M leaf branch) := by
  apply monotone_nat_of_le_succ
  intro n
  induction n with
  | zero =>
      intro c
      simp only [picard]
      exact bot_le
  | succ n ih =>
      simp only [picard]
      exact momentStep_mono M leaf branch ih

theorem picard_le_prefixed
    (M : FiniteMechanism C)
    (leaf : MomentVector C)
    (branch : (c : C) → Fin (M.tuples c).length → ENNReal)
    {w : MomentVector C}
    (hw : ∀ c, momentStep M leaf branch w c ≤ w c) :
    ∀ n c, picard M leaf branch n c ≤ w c := by
  intro n
  induction n with
  | zero =>
      intro c
      simp only [picard]
      exact bot_le
  | succ n ih =>
      intro c
      simp only [picard]
      exact (momentStep_mono M leaf branch ih c).trans (hw c)

theorem picard_iSup_least
    (M : FiniteMechanism C)
    (leaf : MomentVector C)
    (branch : (c : C) → Fin (M.tuples c).length → ENNReal)
    {w : MomentVector C}
    (hw : ∀ c, momentStep M leaf branch w c ≤ w c) :
    (fun c => ⨆ n, picard M leaf branch n c) ≤ w := by
  intro c
  change (⨆ n, picard M leaf branch n c) ≤ w c
  apply iSup_le
  intro n
  exact picard_le_prefixed M leaf branch hw n c

private theorem iSup_mul_iSup_of_monotone
    (u v : Nat → ENNReal)
    (hu : Monotone u)
    (hv : Monotone v) :
    (⨆ n, u n) * (⨆ n, v n) = ⨆ n, u n * v n := by
  apply le_antisymm
  · rw [ENNReal.iSup_mul]
    apply iSup_le
    intro i
    rw [ENNReal.mul_iSup]
    apply iSup_le
    intro j
    apply le_iSup_of_le (max i j)
    apply mul_le_mul'
    · exact hu (Nat.le_max_left i j)
    · exact hv (Nat.le_max_right i j)
  · exact ENNReal.iSup_mul_le

omit [Fintype C] [DecidableEq C] in
theorem list_prod_iSup_of_monotone
    (l : List C)
    (v : Nat → MomentVector C)
    (hv : Monotone v) :
    (l.map (fun c => ⨆ n, v n c)).prod =
      ⨆ n, (l.map (v n)).prod := by
  induction l with
  | nil => simp
  | cons c l ih =>
      simp only [List.map_cons, List.prod_cons]
      rw [ih]
      apply iSup_mul_iSup_of_monotone
      · intro m n hmn
        exact hv hmn c
      · intro m n hmn
        apply List.prod_le_prod'
        exact fun z _ => hv hmn z

private theorem finset_sum_iSup_of_monotone
    {ι : Type*}
    (s : Finset ι)
    (f : ι → Nat → ENNReal)
    (hf : ∀ i, Monotone (f i)) :
    (∑ i ∈ s, ⨆ n, f i n) =
      ⨆ n, (∑ i ∈ s, f i n) := by
  classical
  induction s using Finset.induction_on with
  | empty => simp
  | @insert a s ha ih =>
      simp only [Finset.sum_insert ha]
      rw [ih]
      apply ENNReal.iSup_add_iSup_of_monotone
      · exact hf a
      · intro m n hmn
        exact Finset.sum_le_sum fun i _ => hf i hmn

theorem momentStep_iSup_picard
    (M : FiniteMechanism C)
    (leaf : MomentVector C)
    (branch : (c : C) → Fin (M.tuples c).length → ENNReal) :
    momentStep M leaf branch
        (fun c => ⨆ n, picard M leaf branch n c) =
      fun c => ⨆ n,
        momentStep M leaf branch (picard M leaf branch n) c := by
  funext c
  unfold momentStep
  rw [← ENNReal.add_iSup]
  congr 1
  simp_rw [list_prod_iSup_of_monotone
    _ (picard M leaf branch) (picard_mono M leaf branch)]
  simp_rw [ENNReal.mul_iSup]
  rw [finset_sum_iSup_of_monotone]
  intro i m n hmn
  apply mul_le_mul_right
  apply List.prod_le_prod'
  exact fun z _ => picard_mono M leaf branch hmn z

end

end EstimatorIntegrity
