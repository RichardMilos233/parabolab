import EstimatorIntegrity.BernoulliInformation
import Mathlib.Probability.ConditionalProbability
import Mathlib.Probability.Distributions.Uniform
import Mathlib.Data.Finset.Powerset
import Mathlib.Tactic

/-!
# Conditioning a uniform fixed-cardinality slice

This module constructs the actual uniform law on fixed-cardinality subsets,
conditions it on revealed positive and negative coordinates, identifies the
resulting compatible uniform law, derives the law of one unrevealed coordinate,
and proves the corresponding two-slice KL bound.

It does not formalize an adaptive multi-step transcript, stopping, padding, or
any PDE or minimax conclusion.
-/

open MeasureTheory Set ProbabilityTheory
open scoped ENNReal NNReal ProbabilityTheory

namespace EstimatorIntegrity

section UniformFiniteSet

variable {beta : Type*} [Fintype beta] [DecidableEq beta] [MeasurableSpace beta]
  [MeasurableSingletonClass beta]

private lemma measurableSet_all (s : Set beta) : MeasurableSet s := by
  exact s.toFinite.measurableSet

private lemma uniform_cond_filter (s : Finset beta) (hs : s.Nonempty)
    (p : beta → Prop) [DecidablePred p] (hp : (s.filter p).Nonempty) :
    (PMF.uniformOfFinset s hs).toMeasure[|{x | p x}] =
      (PMF.uniformOfFinset (s.filter p) hp).toMeasure := by
  apply Measure.ext_of_singleton
  intro x
  rw [PMF.toMeasure_apply_singleton _ _ (measurableSet_all {x})]
  rw [cond_apply (measurableSet_all {x | p x})]
  rw [PMF.toMeasure_uniformOfFinset_apply hs _ (measurableSet_all {x | p x})]
  simp only [PMF.uniformOfFinset_apply, Finset.mem_filter, Set.mem_ofPred_eq]
  have hs0 : (s.card : ENNReal) ≠ 0 := by exact_mod_cast hs.card_ne_zero
  have hp0 : ((s.filter p).card : ENNReal) ≠ 0 := by exact_mod_cast hp.card_ne_zero
  by_cases hpx : p x
  · have hinter : ({y | p y} : Set beta) ∩ {x} = {x} := by
      ext y
      simp only [Set.mem_inter_iff, Set.mem_ofPred_eq, Set.mem_singleton_iff]
      constructor
      · exact fun hy => hy.2
      · rintro rfl
        exact ⟨hpx, rfl⟩
    rw [hinter, PMF.toMeasure_apply_singleton _ _ (measurableSet_all {x})]
    simp only [PMF.uniformOfFinset_apply, hpx, and_self, ↓reduceIte]
    by_cases hxs : x ∈ s
    · have hevent : {y ∈ s | p y}.card = (s.filter p).card := rfl
      rw [hevent]
      simp only [hxs, ↓reduceIte, ENNReal.div_eq_inv_mul]
      simp only [true_and, if_true]
      rw [mul_comm (s.card : ENNReal)⁻¹ ((s.filter p).card : ENNReal),
        ENNReal.mul_inv (Or.inl hp0) (Or.inl (by simp)), inv_inv]
      calc
        ((s.filter p).card : ENNReal)⁻¹ * s.card * (s.card : ENNReal)⁻¹ =
            ((s.filter p).card : ENNReal)⁻¹ *
              ((s.card : ENNReal) * (s.card : ENNReal)⁻¹) := by ac_rfl
        _ = ((s.filter p).card : ENNReal)⁻¹ := by
          rw [ENNReal.mul_inv_cancel hs0 (by simp), mul_one]
    · simp [hxs]
  · have hinter : ({y | p y} : Set beta) ∩ {x} = ∅ := by
      ext y
      change (p y ∧ y = x) ↔ False
      constructor
      · rintro ⟨hy, rfl⟩
        exact (hpx hy).elim
      · exact False.elim
    rw [hinter]
    simp [hpx]

end UniformFiniteSet

section Slice

variable {alpha : Type*} [Fintype alpha] [DecidableEq alpha]
  [MeasurableSpace alpha] [MeasurableSingletonClass alpha]

/-- The finite family of `h`-element subsets of `U`. -/
def sliceFamily (U : Finset alpha) (h : Nat) : Finset (Finset alpha) :=
  U.powersetCard h

/-- The actual uniform probability measure on the `h`-element subsets of `U`.
The assumption `h <= #U` supplies, rather than postulates, nonemptiness. -/
noncomputable def uniformSlice (U : Finset alpha) (h : Nat) (hh : h <= U.card) :
    Measure (Finset alpha) :=
  (PMF.uniformOfFinset (sliceFamily U h)
    (Finset.powersetCard_nonempty_of_le hh)).toMeasure

instance uniformSlice_isProbabilityMeasure (U : Finset alpha) (h : Nat)
    (hh : h <= U.card) : IsProbabilityMeasure (uniformSlice U h hh) := by
  unfold uniformSlice
  infer_instance

/-- Every member of the fixed-cardinality slice has mass
`choose(#U,h)⁻¹`, and every other finite subset has mass zero. -/
theorem uniformSlice_singleton (U A : Finset alpha) (h : Nat)
    (hh : h ≤ U.card) :
    uniformSlice U h hh {A} =
      if A ∈ sliceFamily U h then (Nat.choose U.card h : ENNReal)⁻¹ else 0 := by
  unfold uniformSlice
  rw [PMF.toMeasure_apply_singleton _ _ (measurableSet_all {A})]
  simp [sliceFamily]

/-- The event that all revealed positives occur and all revealed negatives do
not occur. -/
def compatibleEvent (P N : Finset alpha) : Set (Finset alpha) :=
  {A | P ⊆ A ∧ Disjoint A N}

/-- The compatible members of the original slice.  This is kept as an actual
filter of the original slice so the conditioning theorem is not definitional. -/
def compatibleFamily (U : Finset alpha) (h : Nat) (P N : Finset alpha) :
    Finset (Finset alpha) :=
  (sliceFamily U h).filter fun A => P ⊆ A ∧ Disjoint A N

@[simp] theorem mem_sliceFamily {U A : Finset alpha} {h : Nat} :
    A ∈ sliceFamily U h ↔ A ⊆ U ∧ A.card = h := by
  simp [sliceFamily]

@[simp] theorem mem_compatibleFamily {U A P N : Finset alpha} {h : Nat} :
    A ∈ compatibleFamily U h P N ↔
      A ⊆ U ∧ A.card = h ∧ P ⊆ A ∧ Disjoint A N := by
  simp only [compatibleFamily, Finset.mem_filter, mem_sliceFamily]
  tauto

theorem compatibleFamily_eq_filter_sdiff (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) :
    compatibleFamily U h P N =
      ((U \ N).powersetCard h).filter (P ⊆ ·) := by
  ext A
  simp only [mem_compatibleFamily, Finset.mem_filter, Finset.mem_powersetCard]
  constructor
  · rintro ⟨A_U, hcard, hPA, hAN⟩
    exact ⟨⟨fun x hx => Finset.mem_sdiff.mpr <| ⟨A_U hx,
      Finset.disjoint_left.mp hAN hx⟩, hcard⟩, hPA⟩
  · rintro ⟨⟨hA, hcard⟩, hPA⟩
    have hAU : A ⊆ U := fun x hx => (Finset.mem_sdiff.mp (hA hx)).1
    have hAN : Disjoint A N := Finset.disjoint_left.mpr fun x hxA hxN =>
      (Finset.mem_sdiff.mp (hA hxA)).2 hxN
    exact ⟨hAU, hcard, hPA, hAN⟩

theorem compatibleFamily_card (U : Finset alpha) (h : Nat) (P N : Finset alpha)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hPh : P.card <= h) :
    (compatibleFamily U h P N).card =
      Nat.choose (U.card - (P.card + N.card)) (h - P.card) := by
  rw [compatibleFamily_eq_filter_sdiff]
  have hPdiff : P ⊆ U \ N := fun x hxP =>
    Finset.mem_sdiff.mpr ⟨hPU hxP, Finset.disjoint_left.mp hPN hxP⟩
  rw [Finset.card_filter_powersetCard_subset P (U \ N) h hPdiff hPh]
  rw [Finset.card_sdiff_of_subset hNU]
  rw [Nat.sub_sub, Nat.add_comm N.card P.card]

private theorem compatibleFamily_nonempty (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (hPU : P ⊆ U) (hNU : N ⊆ U)
    (hPN : Disjoint P N) (hPh : P.card <= h)
    (hhN : h <= U.card - N.card) :
    (compatibleFamily U h P N).Nonempty := by
  apply Finset.card_pos.mp
  rw [compatibleFamily_card U h P N hPU hNU hPN hPh]
  apply Nat.choose_pos
  have hPNcard : P.card + N.card ≤ U.card := by
    rw [← Finset.card_union_of_disjoint hPN]
    exact Finset.card_le_card (Finset.union_subset hPU hNU)
  have hsub : U.card - N.card - P.card =
      U.card - (P.card + N.card) := by omega
  calc
    h - P.card ≤ (U.card - N.card) - P.card := Nat.sub_le_sub_right hhN P.card
    _ = U.card - (P.card + N.card) := hsub

/-- The actual normalized restriction of the original uniform slice to the
revealed-sign event. -/
noncomputable def conditionedSlice (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (hh : h <= U.card) : Measure (Finset alpha) :=
  (uniformSlice U h hh)[|compatibleEvent P N]

/-- The conditioning event has the exact positive mass
`choose(m,r)/choose(K,h)`. -/
theorem uniformSlice_compatibleEvent (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (hh : h <= U.card)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hPh : P.card <= h) :
    uniformSlice U h hh (compatibleEvent P N) =
      (Nat.choose (U.card - (P.card + N.card)) (h - P.card) : ENNReal) /
        Nat.choose U.card h := by
  unfold uniformSlice sliceFamily
  rw [PMF.toMeasure_uniformOfFinset_apply (s := U.powersetCard h)
    _ _ (measurableSet_all _)]
  simp only [compatibleEvent, Set.mem_setOf_eq]
  change ((compatibleFamily U h P N).card : ENNReal) /
      (U.powersetCard h).card = _
  rw [compatibleFamily_card U h P N hPU hNU hPN hPh]
  simp [sliceFamily]

theorem uniformSlice_compatibleEvent_pos (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (hh : h <= U.card)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hPh : P.card <= h) (hhN : h <= U.card - N.card) :
    0 < uniformSlice U h hh (compatibleEvent P N) := by
  rw [uniformSlice_compatibleEvent U h P N hh hPU hNU hPN hPh]
  exact ENNReal.div_pos
    (by exact_mod_cast Nat.choose_ne_zero (by omega))
    (by simp)

/-- Conditioning the actual prior gives the actual uniform law on compatible
slice members.  The equality is proved by normalized atomic masses. -/
theorem conditionedSlice_eq_uniformCompatible (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (hh : h <= U.card)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hPh : P.card <= h) (hhN : h <= U.card - N.card) :
    conditionedSlice U h P N hh =
      (PMF.uniformOfFinset (compatibleFamily U h P N)
        (compatibleFamily_nonempty U h P N hPU hNU hPN hPh hhN)).toMeasure := by
  unfold conditionedSlice uniformSlice compatibleEvent compatibleFamily
  exact uniform_cond_filter _ _ _ _

theorem conditionedSlice_isProbabilityMeasure (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (hh : h <= U.card)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hPh : P.card <= h) (hhN : h <= U.card - N.card) :
    IsProbabilityMeasure (conditionedSlice U h P N hh) := by
  rw [conditionedSlice_eq_uniformCompatible U h P N hh hPU hNU hPN hPh hhN]
  infer_instance

/-- Coordinates that have not been revealed positive or negative. -/
def unrevealedSet (U P N : Finset alpha) : Finset alpha :=
  U \ (P ∪ N)

/-- The membership bit of coordinate `i`. -/
def nextBit (i : alpha) (A : Finset alpha) : Bool :=
  decide (i ∈ A)

theorem measurable_nextBit (i : alpha) : Measurable (nextBit i) := by
  exact measurable_of_finite _

/-- A natural-count ratio packaged as a closed unit-interval parameter. -/
noncomputable def sliceParameter (r m : Nat) (hrm : r ≤ m) : Set.Icc (0 : Real) 1 := by
  refine ⟨(r : Real) / (m : Real), div_nonneg (by positivity) (by positivity), ?_⟩
  by_cases hm : m = 0
  · have hr : r = 0 := Nat.eq_zero_of_le_zero (hm ▸ hrm)
    simp [hm, hr]
  · rw [div_le_one (by exact_mod_cast Nat.pos_of_ne_zero hm)]
    exact_mod_cast hrm

private theorem compatibleFamily_filter_mem_eq (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (i : alpha) (hiP : i ∉ P) :
    (compatibleFamily U h P N).filter (i ∈ ·) =
      compatibleFamily U h (insert i P) N := by
  ext A
  simp only [Finset.mem_filter, mem_compatibleFamily, Finset.insert_subset_iff]
  constructor
  · rintro ⟨⟨hAU, hcard, hPA, hAN⟩, hiA⟩
    exact ⟨hAU, hcard, ⟨hiA, hPA⟩, hAN⟩
  · rintro ⟨hAU, hcard, ⟨hiA, hPA⟩, hAN⟩
    exact ⟨⟨hAU, hcard, hPA, hAN⟩, hiA⟩

private theorem compatibleFamily_filter_mem_card (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (i : alpha)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hiU : i ∈ U) (hiP : i ∉ P) (hiN : i ∉ N) (hPi : P.card < h) :
    ((compatibleFamily U h P N).filter (i ∈ ·)).card =
      Nat.choose (U.card - (P.card + N.card) - 1) (h - P.card - 1) := by
  rw [compatibleFamily_filter_mem_eq U h P N i hiP]
  have hiPU : insert i P ⊆ U := Finset.insert_subset hiU hPU
  have hiPN : Disjoint (insert i P) N := by
    exact Finset.disjoint_left.mpr fun x hx hxN => by
      rw [Finset.mem_insert] at hx
      rcases hx with rfl | hxP
      · exact hiN hxN
      · exact Finset.disjoint_left.mp hPN hxP hxN
  rw [compatibleFamily_card U h (insert i P) N hiPU hNU hiPN]
  · rw [Finset.card_insert_of_notMem hiP]
    simp only [Nat.sub_sub]
    congr 2 <;> omega
  · rw [Finset.card_insert_of_notMem hiP]
    omega

private theorem compatibleFamily_filter_mem_card_zero (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (i : alpha) (hiP : i ∉ P) (hzero : h - P.card = 0) :
    ((compatibleFamily U h P N).filter (i ∈ ·)).card = 0 := by
  apply Finset.card_eq_zero.mpr
  apply Finset.filter_eq_empty_iff.mpr
  intro A hA hiA
  have hPA := (mem_compatibleFamily.mp hA).2.2.1
  have hcard := (mem_compatibleFamily.mp hA).2.1
  have hinsert : insert i P ⊆ A := Finset.insert_subset hiA hPA
  have hle := Finset.card_le_card hinsert
  rw [Finset.card_insert_of_notMem hiP, hcard] at hle
  omega

private theorem remaining_mul_true_card (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (i : alpha)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hPh : P.card ≤ h) (hhN : h ≤ U.card - N.card)
    (hi : i ∈ unrevealedSet U P N) :
    (U.card - (P.card + N.card)) *
        ((compatibleFamily U h P N).filter (i ∈ ·)).card =
      (h - P.card) * (compatibleFamily U h P N).card := by
  have hiU : i ∈ U := (Finset.mem_sdiff.mp hi).1
  have hiPN : i ∉ P ∪ N := (Finset.mem_sdiff.mp hi).2
  have hiP : i ∉ P := fun hip => hiPN (Finset.mem_union_left N hip)
  have hiN : i ∉ N := fun hin => hiPN (Finset.mem_union_right P hin)
  have hPNcard : P.card + N.card ≤ U.card := by
    rw [← Finset.card_union_of_disjoint hPN]
    exact Finset.card_le_card (Finset.union_subset hPU hNU)
  rw [compatibleFamily_card U h P N hPU hNU hPN hPh]
  by_cases hr0 : h - P.card = 0
  · rw [compatibleFamily_filter_mem_card_zero U h P N i hiP hr0, hr0]
    simp
  · have hPr : P.card < h := by omega
    rw [compatibleFamily_filter_mem_card U h P N i hPU hNU hPN hiU hiP hiN hPr]
    let m := U.card - (P.card + N.card)
    let r := h - P.card
    have hmpos : 0 < m := by
      dsimp [m]
      have hi_not_mem : i ∉ P ∪ N := hiPN
      have hproper : (P ∪ N).card < U.card := by
        apply Finset.card_lt_card
        exact (Finset.ssubset_iff_of_subset (Finset.union_subset hPU hNU)).2
          ⟨i, hiU, hi_not_mem⟩
      rw [Finset.card_union_of_disjoint hPN] at hproper
      omega
    have hrpos : 0 < r := Nat.pos_of_ne_zero hr0
    have hchoose := Nat.add_one_mul_choose_eq (m - 1) (r - 1)
    have hmone : m - 1 + 1 = m := Nat.sub_add_cancel hmpos
    have hrone : r - 1 + 1 = r := Nat.sub_add_cancel hrpos
    dsimp [m, r] at hchoose hmone hrone ⊢
    rw [hmone, hrone] at hchoose
    simpa [Nat.mul_comm] using hchoose

theorem sliceRatio_le (U : Finset alpha) (h : Nat) (P N : Finset alpha)
    (hNU : N ⊆ U) (hPh : P.card ≤ h) (hhN : h ≤ U.card - N.card) :
    h - P.card ≤ U.card - (P.card + N.card) := by
  calc
    h - P.card ≤ (U.card - N.card) - P.card :=
      Nat.sub_le_sub_right hhN P.card
    _ = U.card - (N.card + P.card) := Nat.sub_sub U.card N.card P.card
    _ = U.card - (P.card + N.card) := by rw [Nat.add_comm]

/-- The actual probability that an unrevealed coordinate is positive under the
conditioned slice is `r/m`, including the endpoint cases `r=0` and `r=m`. -/
theorem conditionedSlice_next_true (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (i : alpha) (hh : h ≤ U.card)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hPh : P.card ≤ h) (hhN : h ≤ U.card - N.card)
    (hi : i ∈ unrevealedSet U P N) :
    ((conditionedSlice U h P N hh).map (nextBit i)).real {true} =
      ((h - P.card : Nat) : Real) /
        (U.card - (P.card + N.card) : Nat) := by
  rw [measureReal_def, Measure.map_apply (measurable_nextBit i)
    (measurableSet_all {true})]
  rw [conditionedSlice_eq_uniformCompatible U h P N hh hPU hNU hPN hPh hhN]
  rw [PMF.toMeasure_uniformOfFinset_apply _ _ (measurableSet_all _)]
  simp only [Set.mem_preimage, Set.mem_singleton_iff, nextBit, decide_eq_true_eq]
  change (((((compatibleFamily U h P N).filter (i ∈ ·)).card : ENNReal) /
      (compatibleFamily U h P N).card)).toReal = _
  rw [ENNReal.toReal_div]
  · simp only [ENNReal.toReal_natCast]
    have hCpos := (compatibleFamily_nonempty U h P N hPU hNU hPN hPh hhN).card_pos
    have hmpos : 0 < U.card - (P.card + N.card) := by
      have hiU : i ∈ U := (Finset.mem_sdiff.mp hi).1
      have hiPN : i ∉ P ∪ N := (Finset.mem_sdiff.mp hi).2
      have hproper : (P ∪ N).card < U.card := by
        apply Finset.card_lt_card
        exact (Finset.ssubset_iff_of_subset (Finset.union_subset hPU hNU)).2
          ⟨i, hiU, hiPN⟩
      rw [Finset.card_union_of_disjoint hPN] at hproper
      omega
    apply (div_eq_div_iff (by exact_mod_cast hCpos.ne') (by exact_mod_cast hmpos.ne')).2
    have hcount := remaining_mul_true_card U h P N i hPU hNU hPN hPh hhN hi
    rw [Nat.mul_comm] at hcount
    exact_mod_cast hcount

/-- At the lower endpoint `r=0`, every unrevealed coordinate is false. -/
theorem conditionedSlice_next_true_zero (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (i : alpha) (hh : h ≤ U.card)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hhN : h ≤ U.card - N.card) (hi : i ∈ unrevealedSet U P N)
    (hzero : h = P.card) :
    ((conditionedSlice U h P N hh).map (nextBit i)).real {true} = 0 := by
  have hPh : P.card ≤ h := by omega
  rw [conditionedSlice_next_true U h P N i hh hPU hNU hPN hPh hhN hi]
  simp [hzero]

/-- At the upper endpoint `r=m`, every unrevealed coordinate is true. -/
theorem conditionedSlice_next_true_one (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (i : alpha) (hh : h ≤ U.card)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hPh : P.card ≤ h) (hhN : h ≤ U.card - N.card)
    (hi : i ∈ unrevealedSet U P N)
    (hfull : h - P.card = U.card - (P.card + N.card)) :
    ((conditionedSlice U h P N hh).map (nextBit i)).real {true} = 1 := by
  rw [conditionedSlice_next_true U h P N i hh hPU hNU hPN hPh hhN hi, hfull]
  have hiU : i ∈ U := (Finset.mem_sdiff.mp hi).1
  have hiPN : i ∉ P ∪ N := (Finset.mem_sdiff.mp hi).2
  have hproper : (P ∪ N).card < U.card := by
    apply Finset.card_lt_card
    exact (Finset.ssubset_iff_of_subset (Finset.union_subset hPU hNU)).2
      ⟨i, hiU, hiPN⟩
  rw [Finset.card_union_of_disjoint hPN] at hproper
  have hm : U.card - (P.card + N.card) ≠ 0 := by omega
  exact div_self (by exact_mod_cast hm)

/-- Pushing the actual conditioned law through any unrevealed membership bit
gives the actual Bernoulli law with parameter `r/m`. -/
theorem conditionedSlice_map_nextBit (U : Finset alpha) (h : Nat)
    (P N : Finset alpha) (i : alpha) (hh : h ≤ U.card)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hPh : P.card ≤ h) (hhN : h ≤ U.card - N.card)
    (hi : i ∈ unrevealedSet U P N) :
    (conditionedSlice U h P N hh).map (nextBit i) =
      bernoulliBool (sliceParameter (h - P.card) (U.card - (P.card + N.card))
        (sliceRatio_le U h P N hNU hPh hhN)) := by
  letI : IsProbabilityMeasure (conditionedSlice U h P N hh) :=
    conditionedSlice_isProbabilityMeasure U h P N hh hPU hNU hPN hPh hhN
  letI : IsProbabilityMeasure ((conditionedSlice U h P N hh).map (nextBit i)) :=
    Measure.isProbabilityMeasure_map (measurable_nextBit i).aemeasurable
  apply Measure.ext_of_measureReal_singleton
  intro b
  cases b
  · have hfalse : ({false} : Set Bool) = ({true} : Set Bool)ᶜ := by
      ext b
      cases b <;> simp
    have hmapfalse :
        ((conditionedSlice U h P N hh).map (nextBit i)).real ({true} : Set Bool)ᶜ =
          1 - ((conditionedSlice U h P N hh).map (nextBit i)).real {true} := by
      rw [measureReal_compl (measurableSet_all {true}), probReal_univ]
    have hberfalse :
        (bernoulliBool (sliceParameter (h - P.card) (U.card - (P.card + N.card))
          (sliceRatio_le U h P N hNU hPh hhN))).real ({true} : Set Bool)ᶜ =
          1 - (bernoulliBool (sliceParameter (h - P.card) (U.card - (P.card + N.card))
            (sliceRatio_le U h P N hNU hPh hhN))).real {true} := by
      rw [measureReal_compl (measurableSet_all {true}), probReal_univ]
    rw [hfalse, hmapfalse, hberfalse,
      conditionedSlice_next_true U h P N i hh hPU hNU hPN hPh hhN hi]
    simp [sliceParameter, bernoulliBool]
  · rw [conditionedSlice_next_true U h P N i hh hPU hNU hPN hPh hhN hi]
    simp [sliceParameter, bernoulliBool]

/-- The balanced two-slice size assumptions imply feasibility of the same
revealed positive and negative sets for both slice counts. -/
theorem twoSlice_feasible (U : Finset alpha) (hMinus hPlus ell : Nat)
    (P N : Finset alpha) (hord : hMinus ≤ hPlus)
    (hsum : hPlus + hMinus = U.card) (hell : ell = hPlus - hMinus)
    (hsmall : 4 * ell ≤ U.card)
    (hreveal : 8 * (P.card + N.card) ≤ U.card) :
    P.card ≤ hMinus ∧ hMinus ≤ U.card - N.card ∧
      P.card ≤ hPlus ∧ hPlus ≤ U.card - N.card := by
  have hplus : hPlus = hMinus + ell := by omega
  have hcentral : 3 * U.card ≤ 8 * hMinus := by omega
  have hPj : P.card ≤ P.card + N.card := Nat.le_add_right _ _
  have hNj : N.card ≤ P.card + N.card := Nat.le_add_left _ _
  constructor
  · omega
  constructor
  · omega
  constructor
  · omega
  · omega

/-- Arithmetic bounds for the two conditional Bernoulli parameters. -/
theorem twoSlice_ratio_bounds (U : Finset alpha) (hMinus hPlus ell : Nat)
    (P N : Finset alpha) (hK : 0 < U.card) (hord : hMinus ≤ hPlus)
    (hsum : hPlus + hMinus = U.card) (hell : ell = hPlus - hMinus)
    (hsmall : 4 * ell ≤ U.card)
    (hreveal : 8 * (P.card + N.card) ≤ U.card) :
    (1 / 4 : Real) ≤
        ((hMinus - P.card : Nat) : Real) /
          (U.card - (P.card + N.card) : Nat) ∧
      ((hMinus - P.card : Nat) : Real) /
          (U.card - (P.card + N.card) : Nat) ≤ (4 / 7 : Real) ∧
      ((hMinus - P.card : Nat) : Real) /
          (U.card - (P.card + N.card) : Nat) < (3 / 4 : Real) ∧
      (((hPlus - P.card : Nat) : Real) /
          (U.card - (P.card + N.card) : Nat) -
        ((hMinus - P.card : Nat) : Real) /
          (U.card - (P.card + N.card) : Nat)) =
          (ell : Real) / (U.card - (P.card + N.card) : Nat) ∧
      0 ≤ (((hPlus - P.card : Nat) : Real) /
          (U.card - (P.card + N.card) : Nat) -
        ((hMinus - P.card : Nat) : Real) /
          (U.card - (P.card + N.card) : Nat)) ∧
      (((hPlus - P.card : Nat) : Real) /
          (U.card - (P.card + N.card) : Nat) -
        ((hMinus - P.card : Nat) : Real) /
          (U.card - (P.card + N.card) : Nat)) ≤
          2 * (ell : Real) / U.card := by
  have hplus : hPlus = hMinus + ell := by omega
  have hcentral : 3 * U.card ≤ 8 * hMinus := by omega
  have hhalf : 2 * hMinus ≤ U.card := by omega
  have hj : P.card + N.card < U.card := by omega
  have hmposNat : 0 < U.card - (P.card + N.card) := Nat.sub_pos_of_lt hj
  have hmpos : (0 : Real) < (U.card - (P.card + N.card) : Nat) := by
    exact_mod_cast hmposNat
  have hKpos : (0 : Real) < U.card := by exact_mod_cast hK
  rcases twoSlice_feasible U hMinus hPlus ell P N hord hsum hell hsmall hreveal with
    ⟨hPminus, hMinusN, hPplus, hPlusN⟩
  have hLowerNat : U.card - (P.card + N.card) ≤ 4 * (hMinus - P.card) := by
    omega
  have hUpperNat : 7 * (hMinus - P.card) ≤
      4 * (U.card - (P.card + N.card)) := by
    omega
  have hGapNat : (hPlus - P.card) - (hMinus - P.card) = ell := by
    omega
  have hmCompare : U.card ≤ 2 * (U.card - (P.card + N.card)) := by
    omega
  have hLowerReal : ((U.card - (P.card + N.card) : Nat) : Real) ≤
      4 * ((hMinus - P.card : Nat) : Real) := by exact_mod_cast hLowerNat
  have hUpperReal : 7 * ((hMinus - P.card : Nat) : Real) ≤
      4 * ((U.card - (P.card + N.card) : Nat) : Real) := by exact_mod_cast hUpperNat
  have hmCompareReal : (U.card : Real) ≤
      2 * ((U.card - (P.card + N.card) : Nat) : Real) := by exact_mod_cast hmCompare
  have hlower : (1 / 4 : Real) ≤
      ((hMinus - P.card : Nat) : Real) /
        (U.card - (P.card + N.card) : Nat) := by
    rw [le_div_iff₀ hmpos]
    nlinarith
  have hupper : ((hMinus - P.card : Nat) : Real) /
      (U.card - (P.card + N.card) : Nat) ≤ (4 / 7 : Real) := by
    rw [div_le_iff₀ hmpos]
    nlinarith
  have hupperStrict : ((hMinus - P.card : Nat) : Real) /
      (U.card - (P.card + N.card) : Nat) < (3 / 4 : Real) := by
    linarith
  have hgap : (((hPlus - P.card : Nat) : Real) /
        (U.card - (P.card + N.card) : Nat) -
      ((hMinus - P.card : Nat) : Real) /
        (U.card - (P.card + N.card) : Nat)) =
      (ell : Real) / (U.card - (P.card + N.card) : Nat) := by
    rw [← sub_div]
    congr 1
    have hsuble : hMinus - P.card ≤ hPlus - P.card :=
      Nat.sub_le_sub_right hord P.card
    rw [← Nat.cast_sub hsuble]
    exact_mod_cast hGapNat
  have hgapNonneg : 0 ≤ (((hPlus - P.card : Nat) : Real) /
        (U.card - (P.card + N.card) : Nat) -
      ((hMinus - P.card : Nat) : Real) /
        (U.card - (P.card + N.card) : Nat)) := by
    rw [hgap]
    positivity
  have hgapLe : (((hPlus - P.card : Nat) : Real) /
        (U.card - (P.card + N.card) : Nat) -
      ((hMinus - P.card : Nat) : Real) /
        (U.card - (P.card + N.card) : Nat)) ≤
      2 * (ell : Real) / U.card := by
    rw [hgap]
    rw [div_le_div_iff₀ hmpos hKpos]
    have hellNonneg : (0 : Real) ≤ ell := by positivity
    nlinarith
  exact ⟨hlower, hupper, hupperStrict, hgap, hgapNonneg, hgapLe⟩

/-- The actual next-coordinate KL is finite because the minus-slice reference
parameter is strictly interior under the balanced-size assumptions. -/
theorem twoSlice_next_kl_ne_top (U : Finset alpha) (hMinus hPlus ell : Nat)
    (P N : Finset alpha) (i : alpha)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hK : 0 < U.card) (hord : hMinus ≤ hPlus) (hPlusK : hPlus ≤ U.card)
    (hsum : hPlus + hMinus = U.card) (hell : ell = hPlus - hMinus)
    (hsmall : 4 * ell ≤ U.card)
    (hreveal : 8 * (P.card + N.card) ≤ U.card)
    (hi : i ∈ unrevealedSet U P N) :
    InformationTheory.klDiv
      ((conditionedSlice U hPlus P N hPlusK).map (nextBit i))
      ((conditionedSlice U hMinus P N (hord.trans hPlusK)).map (nextBit i)) ≠ ∞ := by
  rcases twoSlice_feasible U hMinus hPlus ell P N hord hsum hell hsmall hreveal with
    ⟨hPminus, hMinusN, hPplus, hPlusN⟩
  rw [conditionedSlice_map_nextBit U hPlus P N i hPlusK hPU hNU hPN
      hPplus hPlusN hi,
    conditionedSlice_map_nextBit U hMinus P N i (hord.trans hPlusK) hPU hNU hPN
      hPminus hMinusN hi]
  have hb := twoSlice_ratio_bounds U hMinus hPlus ell P N hK hord hsum hell
    hsmall hreveal
  apply bernoulliBool_kl_ne_top
  · change 0 < ((hMinus - P.card : Nat) : Real) /
      (U.card - (P.card + N.card) : Nat)
    linarith [hb.1]
  · change ((hMinus - P.card : Nat) : Real) /
      (U.card - (P.card + N.card) : Nat) < 1
    linarith [hb.2.2.1]

/-- The two actual conditioned next-coordinate laws satisfy the quantitative
KL bound `64 ell^2 / (3 K^2)`. -/
theorem twoSlice_next_kl_toReal_le (U : Finset alpha) (hMinus hPlus ell : Nat)
    (P N : Finset alpha) (i : alpha)
    (hPU : P ⊆ U) (hNU : N ⊆ U) (hPN : Disjoint P N)
    (hK : 0 < U.card) (hord : hMinus ≤ hPlus) (hPlusK : hPlus ≤ U.card)
    (hsum : hPlus + hMinus = U.card) (hell : ell = hPlus - hMinus)
    (hsmall : 4 * ell ≤ U.card)
    (hreveal : 8 * (P.card + N.card) ≤ U.card)
    (hi : i ∈ unrevealedSet U P N) :
    (InformationTheory.klDiv
      ((conditionedSlice U hPlus P N hPlusK).map (nextBit i))
      ((conditionedSlice U hMinus P N (hord.trans hPlusK)).map (nextBit i))).toReal ≤
        64 * (ell : Real) ^ 2 / (3 * (U.card : Real) ^ 2) := by
  rcases twoSlice_feasible U hMinus hPlus ell P N hord hsum hell hsmall hreveal with
    ⟨hPminus, hMinusN, hPplus, hPlusN⟩
  rw [conditionedSlice_map_nextBit U hPlus P N i hPlusK hPU hNU hPN
      hPplus hPlusN hi,
    conditionedSlice_map_nextBit U hMinus P N i (hord.trans hPlusK) hPU hNU hPN
      hPminus hMinusN hi]
  have hb := twoSlice_ratio_bounds U hMinus hPlus ell P N hK hord hsum hell
    hsmall hreveal
  let pPlus : Real := ((hPlus - P.card : Nat) : Real) /
    (U.card - (P.card + N.card) : Nat)
  let pMinus : Real := ((hMinus - P.card : Nat) : Real) /
    (U.card - (P.card + N.card) : Nat)
  have hqpos : 0 < pMinus := by
    dsimp [pMinus]
    linarith [hb.1]
  have hqlt : pMinus < 1 := by
    dsimp [pMinus]
    linarith [hb.2.2.1]
  have hchi := bernoulliBool_kl_le_chiSq
    (p := sliceParameter (hPlus - P.card) (U.card - (P.card + N.card))
      (sliceRatio_le U hPlus P N hNU hPplus hPlusN))
    (q := sliceParameter (hMinus - P.card) (U.card - (P.card + N.card))
      (sliceRatio_le U hMinus P N hNU hPminus hMinusN)) hqpos hqlt
  change _ ≤ (pPlus - pMinus) ^ 2 / (pMinus * (1 - pMinus)) at hchi
  refine hchi.trans ?_
  have hlower : (1 / 4 : Real) ≤ pMinus := by
    exact hb.1
  have hupper : pMinus ≤ (4 / 7 : Real) := by
    exact hb.2.1
  have hthreequarter : pMinus ≤ (3 / 4 : Real) := by linarith
  have hden : (3 / 16 : Real) ≤ pMinus * (1 - pMinus) := by
    have hprod := mul_nonneg (sub_nonneg.mpr hlower) (sub_nonneg.mpr hthreequarter)
    nlinarith
  have hdenpos : 0 < pMinus * (1 - pMinus) := lt_of_lt_of_le (by norm_num) hden
  have hgapNonneg : 0 ≤ pPlus - pMinus := by
    exact hb.2.2.2.2.1
  have hgapLe : pPlus - pMinus ≤ 2 * (ell : Real) / U.card := by
    exact hb.2.2.2.2.2
  have hrightNonneg : 0 ≤ 2 * (ell : Real) / U.card := by positivity
  have hgapSq : (pPlus - pMinus) ^ 2 ≤
      (2 * (ell : Real) / U.card) ^ 2 := by nlinarith
  have hKne : (U.card : Real) ≠ 0 := by exact_mod_cast hK.ne'
  have hscale : (2 * (ell : Real) / U.card) ^ 2 =
      (64 * (ell : Real) ^ 2 / (3 * (U.card : Real) ^ 2)) * (3 / 16) := by
    field_simp [hKne]
    ring
  apply (div_le_iff₀ hdenpos).2
  calc
    (pPlus - pMinus) ^ 2 ≤ (2 * (ell : Real) / U.card) ^ 2 := hgapSq
    _ = (64 * (ell : Real) ^ 2 / (3 * (U.card : Real) ^ 2)) * (3 / 16) := hscale
    _ ≤ (64 * (ell : Real) ^ 2 / (3 * (U.card : Real) ^ 2)) *
        (pMinus * (1 - pMinus)) := by
      exact mul_le_mul_of_nonneg_left hden (by positivity)

end Slice

end EstimatorIntegrity
