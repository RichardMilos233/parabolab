import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Probability.Distributions.Bernoulli
import Mathlib.Probability.Kernel.Composition.CompProd
import Mathlib.Probability.Kernel.Composition.Prod

/-!
# Actual finite-depth ternary-tree second moments

This module constructs the finite-depth probability kernels used by the
subcritical ternary estimator and derives their weighted second-moment
recurrence from the kernel law.  The branch coefficient may be correlated
with the next state; the three children are independent conditional on that
single sampled coefficient/state pair.
-/

open MeasureTheory
open scoped ENNReal ProbabilityTheory unitInterval

namespace EstimatorIntegrity.FiniteTreeSecondMoment

noncomputable section

abbrev Output := ℝ × ℕ

/-- The nonnegative square of a real coefficient. -/
def coeffSq (c : ℝ) : ℝ≥0∞ := ENNReal.ofReal (c ^ 2)

theorem coeffSq_mul (x y : ℝ) : coeffSq (x * y) = coeffSq x * coeffSq y := by
  unfold coeffSq
  rw [show (x * y) ^ 2 = x ^ 2 * y ^ 2 by ring]
  rw [ENNReal.ofReal_mul (sq_nonneg x)]

@[fun_prop] theorem measurable_coeffSq : Measurable coeffSq := by
  unfold coeffSq
  fun_prop

/-- The actual leaf-count tilted square weight. -/
def weight (a z : ℝ) (x : Output) : ℝ≥0∞ :=
  coeffSq x.1 * ENNReal.ofReal (a ^ 2 * z) ^ x.2

@[fun_prop] theorem measurable_weight (a z : ℝ) : Measurable (weight a z) := by
  unfold weight coeffSq
  fun_prop

private def branchResult {S : Type*}
    (u : (ℝ × S) × ((Output × Output) × Output)) : Output :=
  (6 * u.1.1 * u.2.1.1.1 * u.2.1.2.1 * u.2.2.1,
    u.2.1.1.2 + u.2.1.2.2 + u.2.2.2)

private theorem measurable_branchResult {S : Type*} [MeasurableSpace S] :
    Measurable (branchResult (S := S)) := by
  unfold branchResult
  fun_prop

private def sourceResult (l : ℝ) : Output := ((6 / 5) * l, 1)

private theorem measurable_sourceResult : Measurable sourceResult := by
  unfold sourceResult
  fun_prop

private theorem weight_sourceResult (a z l : ℝ) :
    weight a z (sourceResult l) =
      (36 / 25 : ℝ≥0∞) * ENNReal.ofReal (a ^ 2 * z) * coeffSq l := by
  unfold weight sourceResult
  rw [coeffSq_mul]
  norm_num [coeffSq]
  have h : ENNReal.ofReal (36 / 25 : ℝ) = (36 / 25 : ℝ≥0∞) := by
    rw [ENNReal.ofReal_div_of_pos (by norm_num : (0 : ℝ) < 25)]
    norm_num
  rw [h]
  ac_rfl

private theorem weight_branchResult {S : Type*} [MeasurableSpace S]
    (a z : ℝ) (wr : ℝ × S) (x₁ x₂ x₃ : Output) :
    weight a z (branchResult (wr, ((x₁, x₂), x₃))) =
      36 * coeffSq wr.1 * weight a z x₁ * weight a z x₂ * weight a z x₃ := by
  unfold branchResult
  change weight a z (6 * wr.1 * x₁.1 * x₂.1 * x₃.1,
      x₁.2 + x₂.2 + x₃.2) = _
  unfold weight
  simp_rw [coeffSq_mul]
  norm_num [coeffSq]
  rw [pow_add, pow_add]
  ring

/-- Three conditionally independent copies of `K`, all evaluated at the same
next state carried by `(omega, r)`. -/
def childTriple {S : Type*} [MeasurableSpace S]
    (K : ProbabilityTheory.Kernel S Output) :
    ProbabilityTheory.Kernel (ℝ × S) ((Output × Output) × Output) :=
  let child := ProbabilityTheory.Kernel.prodMkLeft ℝ K
  (child ×ₖ child) ×ₖ child

theorem lintegral_childTriple {S : Type*} [MeasurableSpace S]
    (K : ProbabilityTheory.Kernel S Output)
    [ProbabilityTheory.IsMarkovKernel K]
    (a z : ℝ) (wr : ℝ × S) :
    ∫⁻ t, weight a z t.1.1 * weight a z t.1.2 * weight a z t.2
        ∂childTriple K wr =
      (∫⁻ x, weight a z x ∂K wr.2) ^ 3 := by
  let child := ProbabilityTheory.Kernel.prodMkLeft ℝ K
  have hm : Measurable (fun t : (Output × Output) × Output =>
      weight a z t.1.1 * weight a z t.1.2 * weight a z t.2) := by
    fun_prop
  rw [childTriple, ProbabilityTheory.Kernel.lintegral_prod _ _ wr hm]
  simp_rw [lintegral_const_mul _ (measurable_weight a z)]
  rw [ProbabilityTheory.Kernel.lintegral_prod child child wr]
  · change (∫⁻ b, ∫⁻ c, weight a z b * weight a z c *
        (∫⁻ x, weight a z x ∂K wr.2) ∂K wr.2 ∂K wr.2) = _
    simp_rw [mul_assoc]
    simp_rw [lintegral_const_mul _
      ((measurable_weight a z).mul_const (∫⁻ x, weight a z x ∂K wr.2))]
    simp_rw [lintegral_mul_const _ (measurable_weight a z)]
    simp only [pow_succ, pow_zero, one_mul]
    ac_rfl
  · fun_prop

/-- The branch law: sample `(omega,r)`, then an independent triple from
`K r`, and finally apply the importance-weighted ternary product. -/
def branchKernel {S : Type*} [MeasurableSpace S]
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (K : ProbabilityTheory.Kernel S Output) :
    ProbabilityTheory.Kernel S Output :=
  (branch ⊗ₖ ProbabilityTheory.Kernel.prodMkLeft S (childTriple K)).map branchResult

theorem lintegral_branchKernel {S : Type*} [MeasurableSpace S]
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (K : ProbabilityTheory.Kernel S Output)
    [ProbabilityTheory.IsMarkovKernel branch]
    [ProbabilityTheory.IsMarkovKernel K]
    (a z : ℝ) (s : S) :
    ∫⁻ x, weight a z x ∂branchKernel branch K s =
      36 * (∫⁻ wr, coeffSq wr.1 *
        (∫⁻ x, weight a z x ∂K wr.2) ^ 3 ∂branch s) := by
  letI : ProbabilityTheory.IsMarkovKernel (childTriple K) := by
    unfold childTriple
    infer_instance
  rw [branchKernel,
    ProbabilityTheory.Kernel.lintegral_map _ measurable_branchResult _
      (measurable_weight a z)]
  rw [ProbabilityTheory.Kernel.lintegral_compProd _ _ _
    (show Measurable (fun u => weight a z (branchResult u)) from
      (measurable_weight a z).comp measurable_branchResult)]
  · rw [← lintegral_const_mul]
    · apply lintegral_congr
      intro wr
      change (∫⁻ t, weight a z (branchResult (wr, t)) ∂childTriple K wr) = _
      have hw : (fun t : (Output × Output) × Output =>
          weight a z (branchResult (wr, t))) =
          fun t => 36 * coeffSq wr.1 * weight a z t.1.1 *
            weight a z t.1.2 * weight a z t.2 := by
        funext t
        rcases t with ⟨⟨x₁, x₂⟩, x₃⟩
        exact weight_branchResult a z wr x₁ x₂ x₃
      rw [hw]
      have hmul : (fun t : (Output × Output) × Output =>
          36 * coeffSq wr.1 * weight a z t.1.1 * weight a z t.1.2 * weight a z t.2) =
          fun t => (36 * coeffSq wr.1) *
            (weight a z t.1.1 * weight a z t.1.2 * weight a z t.2) := by
        funext t
        ac_rfl
      rw [hmul]
      rw [lintegral_const_mul]
      · rw [lintegral_childTriple]
        ac_rfl
      · fun_prop
    · have hF : Measurable fun r => ∫⁻ x, weight a z x ∂K r :=
        (measurable_weight a z).lintegral_kernel
      exact (measurable_coeffSq.comp measurable_fst).mul
        ((hF.comp measurable_snd).pow_const 3)

/-- The source law with its `1/q = 6/5` importance weight. -/
def sourceKernel {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ) :
    ProbabilityTheory.Kernel S Output :=
  leaf.map sourceResult

theorem lintegral_sourceKernel {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ) (a z : ℝ) (s : S) :
    ∫⁻ x, weight a z x ∂sourceKernel leaf s =
      (36 / 25 : ℝ≥0∞) * ENNReal.ofReal (a ^ 2 * z) *
        (∫⁻ l, coeffSq l ∂leaf s) := by
  rw [sourceKernel, ProbabilityTheory.Kernel.lintegral_map _ measurable_sourceResult _
    (measurable_weight a z)]
  simp_rw [weight_sourceResult]
  rw [lintegral_const_mul]
  exact measurable_coeffSq

private def chooseBranch {S : Type*} : Set (S × Bool) := {sb | sb.2 = true}

private theorem measurableSet_chooseBranch {S : Type*} [MeasurableSpace S] :
    MeasurableSet (chooseBranch (S := S)) := by
  exact measurable_snd (measurableSet_singleton true)

private def branchProbability : I :=
  ⟨(1 / 6 : ℝ), by norm_num, by norm_num⟩

/-- One recursive estimator step.  `Ber(true,false,1/6)` chooses the branch
law with probability `p=1/6` and the source law with probability `q=5/6`.
The composition-product retains the current state while making that choice. -/
def stepKernel {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (K : ProbabilityTheory.Kernel S Output) :
    ProbabilityTheory.Kernel S Output := by
  classical
  let conditional : ProbabilityTheory.Kernel (S × Bool) Output :=
    ProbabilityTheory.Kernel.piecewise measurableSet_chooseBranch
      (ProbabilityTheory.Kernel.prodMkRight Bool (branchKernel branch K))
      (ProbabilityTheory.Kernel.prodMkRight Bool (sourceKernel leaf))
  exact ((ProbabilityTheory.Kernel.const S
      (ProbabilityTheory.bernoulliMeasure true false branchProbability) ⊗ₖ conditional).map Prod.snd)

theorem lintegral_stepKernel {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (K : ProbabilityTheory.Kernel S Output)
    [ProbabilityTheory.IsMarkovKernel leaf]
    [ProbabilityTheory.IsMarkovKernel branch]
    [ProbabilityTheory.IsMarkovKernel K]
    (a z : ℝ) (s : S) :
    ∫⁻ x, weight a z x ∂stepKernel leaf branch K s =
      (5 / 6 : ℝ≥0∞) * (∫⁻ x, weight a z x ∂sourceKernel leaf s) +
        (1 / 6 : ℝ≥0∞) * (∫⁻ x, weight a z x ∂branchKernel branch K s) := by
  classical
  let conditional : ProbabilityTheory.Kernel (S × Bool) Output :=
    ProbabilityTheory.Kernel.piecewise measurableSet_chooseBranch
      (ProbabilityTheory.Kernel.prodMkRight Bool (branchKernel branch K))
      (ProbabilityTheory.Kernel.prodMkRight Bool (sourceKernel leaf))
  letI : ProbabilityTheory.IsMarkovKernel (childTriple K) := by
    unfold childTriple
    infer_instance
  letI : ProbabilityTheory.IsMarkovKernel (branchKernel branch K) := by
    unfold branchKernel
    exact ProbabilityTheory.Kernel.IsMarkovKernel.map _ measurable_branchResult
  letI : ProbabilityTheory.IsMarkovKernel (sourceKernel leaf) := by
    unfold sourceKernel
    exact ProbabilityTheory.Kernel.IsMarkovKernel.map _ measurable_sourceResult
  letI : ProbabilityTheory.IsMarkovKernel conditional := by
    dsimp only [conditional]
    infer_instance
  change ∫⁻ x, weight a z x ∂
      ((ProbabilityTheory.Kernel.const S
        (ProbabilityTheory.bernoulliMeasure true false branchProbability) ⊗ₖ conditional).map
          Prod.snd) s = _
  rw [ProbabilityTheory.Kernel.lintegral_map _ measurable_snd _ (measurable_weight a z)]
  rw [ProbabilityTheory.Kernel.lintegral_compProd _ _ _ (by fun_prop)]
  change (∫⁻ b, ∫⁻ x, weight a z x ∂conditional (s, b)
    ∂ProbabilityTheory.bernoulliMeasure true false branchProbability) = _
  dsimp only [conditional]
  rw [ProbabilityTheory.bernoulliMeasure_def, lintegral_add_measure]
  rw [lintegral_smul_measure, lintegral_smul_measure]
  rw [lintegral_dirac, lintegral_dirac]
  rw [ProbabilityTheory.Kernel.lintegral_piecewise,
    ProbabilityTheory.Kernel.lintegral_piecewise]
  simp only [chooseBranch, Set.mem_ofPred_eq, ↓reduceIte,
    Bool.false_eq_true, ProbabilityTheory.Kernel.lintegral_prodMkRight]
  have hp : unitInterval.toNNReal branchProbability = (1 / 6 : NNReal) := by
    apply Subtype.ext
    norm_num [branchProbability]
  have hq : unitInterval.toNNReal (σ branchProbability) = (5 / 6 : NNReal) := by
    apply Subtype.ext
    norm_num [branchProbability, unitInterval.symm]
  rw [hp, hq]
  simp only [ENNReal.smul_def, smul_eq_mul]
  norm_num [ENNReal.coe_div]
  ac_rfl

/-- The actual depth-`D` law.  Depth zero is killed at `(0,0)`. -/
def treeKernel {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S)) :
    ℕ → ProbabilityTheory.Kernel S Output
  | 0 => ProbabilityTheory.Kernel.deterministic (fun _ => (0, 0)) measurable_const
  | D + 1 => stepKernel leaf branch (treeKernel leaf branch D)

theorem childTriple_isMarkov {S : Type*} [MeasurableSpace S]
    (K : ProbabilityTheory.Kernel S Output) [ProbabilityTheory.IsMarkovKernel K] :
    ProbabilityTheory.IsMarkovKernel (childTriple K) := by
  unfold childTriple
  infer_instance

theorem branchKernel_isMarkov {S : Type*} [MeasurableSpace S]
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (K : ProbabilityTheory.Kernel S Output)
    [ProbabilityTheory.IsMarkovKernel branch]
    [ProbabilityTheory.IsMarkovKernel K] :
    ProbabilityTheory.IsMarkovKernel (branchKernel branch K) := by
  letI : ProbabilityTheory.IsMarkovKernel (childTriple K) := childTriple_isMarkov K
  unfold branchKernel
  exact ProbabilityTheory.Kernel.IsMarkovKernel.map _ measurable_branchResult

theorem sourceKernel_isMarkov {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    [ProbabilityTheory.IsMarkovKernel leaf] :
    ProbabilityTheory.IsMarkovKernel (sourceKernel leaf) := by
  unfold sourceKernel
  exact ProbabilityTheory.Kernel.IsMarkovKernel.map _ measurable_sourceResult

theorem stepKernel_isMarkov {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (K : ProbabilityTheory.Kernel S Output)
    [ProbabilityTheory.IsMarkovKernel leaf]
    [ProbabilityTheory.IsMarkovKernel branch]
    [ProbabilityTheory.IsMarkovKernel K] :
    ProbabilityTheory.IsMarkovKernel (stepKernel leaf branch K) := by
  classical
  letI : ProbabilityTheory.IsMarkovKernel (branchKernel branch K) :=
    branchKernel_isMarkov branch K
  letI : ProbabilityTheory.IsMarkovKernel (sourceKernel leaf) :=
    sourceKernel_isMarkov leaf
  let conditional : ProbabilityTheory.Kernel (S × Bool) Output :=
    ProbabilityTheory.Kernel.piecewise measurableSet_chooseBranch
      (ProbabilityTheory.Kernel.prodMkRight Bool (branchKernel branch K))
      (ProbabilityTheory.Kernel.prodMkRight Bool (sourceKernel leaf))
  letI : ProbabilityTheory.IsMarkovKernel conditional := by
    dsimp only [conditional]
    infer_instance
  change ProbabilityTheory.IsMarkovKernel
    ((ProbabilityTheory.Kernel.const S
      (ProbabilityTheory.bernoulliMeasure true false branchProbability) ⊗ₖ conditional).map Prod.snd)
  exact ProbabilityTheory.Kernel.IsMarkovKernel.map _ measurable_snd

theorem treeKernel_isMarkov {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    [ProbabilityTheory.IsMarkovKernel leaf]
    [ProbabilityTheory.IsMarkovKernel branch] :
    ∀ D, ProbabilityTheory.IsMarkovKernel (treeKernel leaf branch D) := by
  intro D
  induction D with
  | zero =>
      simp only [treeKernel]
      infer_instance
  | succ D ih =>
      simp only [treeKernel]
      letI := ih
      exact stepKernel_isMarkov leaf branch (treeKernel leaf branch D)

/-- Actual ENNReal weighted moment of the depth-`D` output law. -/
def weightedMoment {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (D : ℕ) (a z : ℝ) (s : S) : ℝ≥0∞ :=
  ∫⁻ x, weight a z x ∂treeKernel leaf branch D s

theorem weightedMoment_zero {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (a z : ℝ) (s : S) : weightedMoment leaf branch 0 a z s = 0 := by
  simp [weightedMoment, treeKernel, weight, coeffSq]

theorem weightedMoment_succ {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    [ProbabilityTheory.IsMarkovKernel leaf]
    [ProbabilityTheory.IsMarkovKernel branch]
    (D : ℕ) (a z : ℝ) (s : S) :
    weightedMoment leaf branch (D + 1) a z s =
      (6 / 5 : ℝ≥0∞) * ENNReal.ofReal (a ^ 2 * z) *
          (∫⁻ l, coeffSq l ∂leaf s) +
        6 * (∫⁻ wr, coeffSq wr.1 *
          (weightedMoment leaf branch D a z wr.2) ^ 3 ∂branch s) := by
  letI : ProbabilityTheory.IsMarkovKernel (treeKernel leaf branch D) :=
    treeKernel_isMarkov leaf branch D
  unfold weightedMoment
  rw [treeKernel, lintegral_stepKernel, lintegral_sourceKernel,
    lintegral_branchKernel]
  have hsource : (5 / 6 : ℝ≥0∞) * (36 / 25) = 6 / 5 := by
    apply (ENNReal.toReal_eq_toReal_iff' (x := (5 / 6 : ℝ≥0∞) * (36 / 25))
      (y := 6 / 5) (by finiteness) (by finiteness)).mp
    norm_num
  have hbranch : (1 / 6 : ℝ≥0∞) * 36 = 6 := by
    apply (ENNReal.toReal_eq_toReal_iff' (x := (1 / 6 : ℝ≥0∞) * 36)
      (y := 6) (by finiteness) (by finiteness)).mp
    norm_num
  calc
    (5 / 6 : ℝ≥0∞) *
          ((36 / 25) * ENNReal.ofReal (a ^ 2 * z) * ∫⁻ l, coeffSq l ∂leaf s) +
        (1 / 6) * (36 * ∫⁻ wr, coeffSq wr.1 *
          (∫⁻ x, weight a z x ∂treeKernel leaf branch D wr.2) ^ 3 ∂branch s) =
      ((5 / 6 : ℝ≥0∞) * (36 / 25)) * ENNReal.ofReal (a ^ 2 * z) *
          (∫⁻ l, coeffSq l ∂leaf s) +
        ((1 / 6 : ℝ≥0∞) * 36) * (∫⁻ wr, coeffSq wr.1 *
          (∫⁻ x, weight a z x ∂treeKernel leaf branch D wr.2) ^ 3 ∂branch s) := by
        ac_rfl
    _ = _ := by rw [hsource, hbranch]

private theorem radius_algebra (M C R : ℝ)
    (hM : 0 < M) (hR : 0 < R) (hC : 0 ≤ C)
    (hsmall : C * R ^ 2 ≤ 1 / 8) :
    (6 / 5 : ℝ≥0∞) * ENNReal.ofReal ((3 * R / (4 * M)) ^ 2 * (5 / 4)) *
          ENNReal.ofReal (M ^ 2) +
        6 * (ENNReal.ofReal (C ^ 2) * (ENNReal.ofReal (R ^ 2)) ^ 3) ≤
      ENNReal.ofReal (R ^ 2) := by
  apply (ENNReal.toReal_le_toReal (by finiteness) (by finiteness)).mp
  rw [ENNReal.toReal_add (by finiteness) (by finiteness)]
  simp only [ENNReal.toReal_mul, ENNReal.toReal_pow, ENNReal.toReal_div,
    ENNReal.toReal_ofNat]
  rw [ENNReal.toReal_ofReal (sq_nonneg M), ENNReal.toReal_ofReal (sq_nonneg C),
    ENNReal.toReal_ofReal (sq_nonneg R)]
  have ha : 0 ≤ (3 * R / (4 * M)) ^ 2 * (5 / 4) := by positivity
  rw [ENNReal.toReal_ofReal ha]
  have hsource :
      (6 / 5 : ℝ) * ((3 * R / (4 * M)) ^ 2 * (5 / 4)) * M ^ 2 =
        (27 / 32) * R ^ 2 := by
    field_simp [hM.ne']; ring
  have hsq : (C * R ^ 2) ^ 2 ≤ (1 / 8 : ℝ) ^ 2 :=
    (sq_le_sq₀ (mul_nonneg hC (sq_nonneg R)) (by norm_num)).mpr hsmall
  have hbranch : 6 * C ^ 2 * (R ^ 2) ^ 3 ≤ (3 / 32 : ℝ) * R ^ 2 := by
    nlinarith [hsq, sq_nonneg R]
  rw [hsource]
  nlinarith [hbranch, sq_nonneg R]

/-- Under the source and branch square-moment bounds, every finite-depth
weighted moment stays inside the radius `R²`. -/
theorem weightedMoment_uniform_bound {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    [ProbabilityTheory.IsMarkovKernel leaf]
    [ProbabilityTheory.IsMarkovKernel branch]
    (M C R : ℝ) (hM : 0 < M) (hR : 0 < R) (hC : 0 ≤ C)
    (hsmall : C * R ^ 2 ≤ 1 / 8)
    (hleaf : ∀ s, ∫⁻ l, coeffSq l ∂leaf s ≤ ENNReal.ofReal (M ^ 2))
    (hbranch : ∀ s, ∫⁻ wr, coeffSq wr.1 ∂branch s ≤ ENNReal.ofReal (C ^ 2)) :
    ∀ D s, weightedMoment leaf branch D (3 * R / (4 * M)) (5 / 4) s ≤
      ENNReal.ofReal (R ^ 2) := by
  intro D
  induction D with
  | zero =>
      intro s
      rw [weightedMoment_zero]
      exact bot_le
  | succ D ih =>
      intro s
      rw [weightedMoment_succ]
      have hchild :
          (∫⁻ wr, coeffSq wr.1 *
              (weightedMoment leaf branch D (3 * R / (4 * M)) (5 / 4) wr.2) ^ 3
            ∂branch s) ≤
            ENNReal.ofReal (C ^ 2) * (ENNReal.ofReal (R ^ 2)) ^ 3 := by
        calc
          (∫⁻ wr, coeffSq wr.1 *
              (weightedMoment leaf branch D (3 * R / (4 * M)) (5 / 4) wr.2) ^ 3
            ∂branch s) ≤
              ∫⁻ wr, coeffSq wr.1 * (ENNReal.ofReal (R ^ 2)) ^ 3 ∂branch s := by
                apply lintegral_mono
                intro wr
                exact mul_le_mul_right (pow_le_pow_left' (ih wr.2) 3) _
          _ = (∫⁻ wr, coeffSq wr.1 ∂branch s) *
              (ENNReal.ofReal (R ^ 2)) ^ 3 := by
                simpa only [Function.comp_apply] using
                  (lintegral_mul_const (μ := branch s) (ENNReal.ofReal (R ^ 2) ^ 3)
                    (measurable_coeffSq.comp measurable_fst))
          _ ≤ ENNReal.ofReal (C ^ 2) * (ENNReal.ofReal (R ^ 2)) ^ 3 := by
              exact mul_le_mul_left (hbranch s) _
      calc
        (6 / 5 : ℝ≥0∞) * ENNReal.ofReal ((3 * R / (4 * M)) ^ 2 * (5 / 4)) *
              (∫⁻ l, coeffSq l ∂leaf s) +
            6 * (∫⁻ wr, coeffSq wr.1 *
              (weightedMoment leaf branch D (3 * R / (4 * M)) (5 / 4) wr.2) ^ 3
                ∂branch s) ≤
            (6 / 5 : ℝ≥0∞) * ENNReal.ofReal ((3 * R / (4 * M)) ^ 2 * (5 / 4)) *
                ENNReal.ofReal (M ^ 2) +
              6 * (ENNReal.ofReal (C ^ 2) * (ENNReal.ofReal (R ^ 2)) ^ 3) := by
                exact add_le_add
                  (mul_le_mul_right (hleaf s)
                    ((6 / 5 : ℝ≥0∞) *
                      ENNReal.ofReal ((3 * R / (4 * M)) ^ 2 * (5 / 4))))
                  (mul_le_mul_right hchild 6)
        _ ≤ ENNReal.ofReal (R ^ 2) := radius_algebra M C R hM hR hC hsmall

theorem weightedMoment_ne_top {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    [ProbabilityTheory.IsMarkovKernel leaf]
    [ProbabilityTheory.IsMarkovKernel branch]
    (D : ℕ) (M C R : ℝ) (hM : 0 < M) (hR : 0 < R) (hC : 0 ≤ C)
    (hsmall : C * R ^ 2 ≤ 1 / 8)
    (hleaf : ∀ s, ∫⁻ l, coeffSq l ∂leaf s ≤ ENNReal.ofReal (M ^ 2))
    (hbranch : ∀ s, ∫⁻ wr, coeffSq wr.1 ∂branch s ≤ ENNReal.ofReal (C ^ 2))
    (s : S) :
    weightedMoment leaf branch D (3 * R / (4 * M)) (5 / 4) s ≠ ∞ := by
  exact ne_top_of_le_ne_top (by finiteness)
    (weightedMoment_uniform_bound leaf branch M C R hM hR hC hsmall hleaf hbranch D s)

/-- The derivative of the scalar squared-majorant map at `R²` is at most
`9/32` under the same smallness assumption. -/
theorem squaredMajorant_slope_bound (C R : ℝ) (hC : 0 ≤ C)
    (hsmall : C * R ^ 2 ≤ 1 / 8) :
    3 * (C ^ 2 / (1 / 6)) * (R ^ 2) ^ 2 ≤ 9 / 32 := by
  have hsq : (C * R ^ 2) ^ 2 ≤ (1 / 8 : ℝ) ^ 2 :=
    (sq_le_sq₀ (mul_nonneg hC (sq_nonneg R)) (by norm_num)).mpr hsmall
  norm_num only [div_eq_mul_inv]
  nlinarith [hsq]

/-- The deliberately non-sharp but summable polynomial envelope
`A_j = ∑ n, n^(2j) (4/5)^n`. -/
def leafPolynomialConstant (j : ℕ) : ℝ :=
  ∑' n : ℕ, (n : ℝ) ^ (2 * j) * (4 / 5 : ℝ) ^ n

theorem summable_leafPolynomialSeries (j : ℕ) :
    Summable (fun n : ℕ => (n : ℝ) ^ (2 * j) * (4 / 5 : ℝ) ^ n) := by
  apply summable_pow_mul_geometric_of_norm_lt_one
  norm_num

theorem leafPolynomialConstant_nonneg (j : ℕ) : 0 ≤ leafPolynomialConstant j := by
  unfold leafPolynomialConstant
  exact tsum_nonneg (fun n => by positivity)

theorem leafPolynomialConstant_ennreal_ne_top (j : ℕ) :
    ENNReal.ofReal (leafPolynomialConstant j) ≠ ∞ := by
  exact ENNReal.ofReal_ne_top

theorem leafPolynomial_term_le (j n : ℕ) :
    (n : ℝ) ^ (2 * j) * (4 / 5 : ℝ) ^ n ≤ leafPolynomialConstant j := by
  exact (summable_leafPolynomialSeries j).le_tsum n (by
    intro m hm
    positivity)

/-- Each polynomial factor is pointwise dominated by the exponential tilt. -/
theorem leafPolynomial_le_geometric (j n : ℕ) :
    (n : ℝ) ^ (2 * j) ≤ leafPolynomialConstant j * (5 / 4 : ℝ) ^ n := by
  have h := mul_le_mul_of_nonneg_right (leafPolynomial_term_le j n)
    (by positivity : 0 ≤ (5 / 4 : ℝ) ^ n)
  calc
    (n : ℝ) ^ (2 * j) =
        ((n : ℝ) ^ (2 * j) * (4 / 5 : ℝ) ^ n) * (5 / 4 : ℝ) ^ n := by
          rw [mul_assoc, ← mul_pow]
          norm_num
    _ ≤ leafPolynomialConstant j * (5 / 4 : ℝ) ^ n := h

/-- The actual polynomially weighted square on a tree outcome. -/
def polynomialWeight (j : ℕ) (a : ℝ) (x : Output) : ℝ≥0∞ :=
  ENNReal.ofReal ((x.2 : ℝ) ^ (2 * j)) * coeffSq x.1 *
    ENNReal.ofReal (a ^ 2) ^ x.2

@[fun_prop] theorem measurable_polynomialWeight (j : ℕ) (a : ℝ) :
    Measurable (polynomialWeight j a) := by
  unfold polynomialWeight coeffSq
  fun_prop

/-- The actual polynomial leaf-count moment under the depth-`D` law. -/
def polynomialMoment {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (j D : ℕ) (a : ℝ) (s : S) : ℝ≥0∞ :=
  ∫⁻ x, polynomialWeight j a x ∂treeKernel leaf branch D s

private theorem tiltedBase_factorization (a : ℝ) (n : ℕ) :
    ENNReal.ofReal (a ^ 2 * (5 / 4)) ^ n =
      ENNReal.ofReal (a ^ 2) ^ n * (5 / 4 : ℝ≥0∞) ^ n := by
  rw [ENNReal.ofReal_mul (sq_nonneg a), mul_pow]
  congr 1
  rw [ENNReal.ofReal_div_of_pos (by norm_num : (0 : ℝ) < 4)]
  norm_num

/-- General pointwise-to-integral domination for a nonnegative envelope. -/
theorem polynomialMoment_le_weightedMoment {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    (j D : ℕ) (a : ℝ) (s : S) (A : ℝ≥0∞)
    (hA : ∀ n : ℕ, ENNReal.ofReal ((n : ℝ) ^ (2 * j)) ≤
      A * (5 / 4 : ℝ≥0∞) ^ n) :
    polynomialMoment leaf branch j D a s ≤
      A * weightedMoment leaf branch D a (5 / 4) s := by
  unfold polynomialMoment weightedMoment
  calc
    (∫⁻ x, polynomialWeight j a x ∂treeKernel leaf branch D s) ≤
        ∫⁻ x, A * weight a (5 / 4) x ∂treeKernel leaf branch D s := by
          apply lintegral_mono
          intro x
          have hmul := mul_le_mul_left (hA x.2)
            (coeffSq x.1 * ENNReal.ofReal (a ^ 2) ^ x.2)
          calc
            polynomialWeight j a x =
                ENNReal.ofReal ((x.2 : ℝ) ^ (2 * j)) *
                  (coeffSq x.1 * ENNReal.ofReal (a ^ 2) ^ x.2) := by
                    unfold polynomialWeight
                    ac_rfl
            _ ≤ (A * (5 / 4 : ℝ≥0∞) ^ x.2) *
                (coeffSq x.1 * ENNReal.ofReal (a ^ 2) ^ x.2) := hmul
            _ = A * weight a (5 / 4) x := by
                unfold weight
                rw [tiltedBase_factorization]
                ac_rfl
    _ = A * (∫⁻ x, weight a (5 / 4) x ∂treeKernel leaf branch D s) := by
      rw [lintegral_const_mul A (measurable_weight a (5 / 4))]

theorem leafPolynomial_domination_ennreal (j n : ℕ) :
    ENNReal.ofReal ((n : ℝ) ^ (2 * j)) ≤
      ENNReal.ofReal (leafPolynomialConstant j) * (5 / 4 : ℝ≥0∞) ^ n := by
  calc
    ENNReal.ofReal ((n : ℝ) ^ (2 * j)) ≤
        ENNReal.ofReal (leafPolynomialConstant j * (5 / 4 : ℝ) ^ n) :=
          ENNReal.ofReal_le_ofReal (leafPolynomial_le_geometric j n)
    _ = ENNReal.ofReal (leafPolynomialConstant j) * (5 / 4 : ℝ≥0∞) ^ n := by
      rw [ENNReal.ofReal_mul (leafPolynomialConstant_nonneg j),
        ENNReal.ofReal_pow (by norm_num : (0 : ℝ) ≤ 5 / 4)]
      congr 1
      rw [ENNReal.ofReal_div_of_pos (by norm_num : (0 : ℝ) < 4)]
      norm_num

/-- Every fixed polynomial leaf-count moment of the actual finite-depth law
is bounded by the finite constant `A_j R²`. -/
theorem polynomialMoment_uniform_bound {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    [ProbabilityTheory.IsMarkovKernel leaf]
    [ProbabilityTheory.IsMarkovKernel branch]
    (j D : ℕ) (M C R : ℝ) (hM : 0 < M) (hR : 0 < R) (hC : 0 ≤ C)
    (hsmall : C * R ^ 2 ≤ 1 / 8)
    (hleaf : ∀ s, ∫⁻ l, coeffSq l ∂leaf s ≤ ENNReal.ofReal (M ^ 2))
    (hbranch : ∀ s, ∫⁻ wr, coeffSq wr.1 ∂branch s ≤ ENNReal.ofReal (C ^ 2))
    (s : S) :
    polynomialMoment leaf branch j D (3 * R / (4 * M)) s ≤
      ENNReal.ofReal (leafPolynomialConstant j) * ENNReal.ofReal (R ^ 2) := by
  calc
    polynomialMoment leaf branch j D (3 * R / (4 * M)) s ≤
        ENNReal.ofReal (leafPolynomialConstant j) *
          weightedMoment leaf branch D (3 * R / (4 * M)) (5 / 4) s :=
      polynomialMoment_le_weightedMoment leaf branch j D (3 * R / (4 * M)) s
        (ENNReal.ofReal (leafPolynomialConstant j)) (leafPolynomial_domination_ennreal j)
    _ ≤ ENNReal.ofReal (leafPolynomialConstant j) * ENNReal.ofReal (R ^ 2) := by
      exact mul_le_mul_right
        (weightedMoment_uniform_bound leaf branch M C R hM hR hC hsmall hleaf hbranch D s) _

theorem polynomialMoment_ne_top {S : Type*} [MeasurableSpace S]
    (leaf : ProbabilityTheory.Kernel S ℝ)
    (branch : ProbabilityTheory.Kernel S (ℝ × S))
    [ProbabilityTheory.IsMarkovKernel leaf]
    [ProbabilityTheory.IsMarkovKernel branch]
    (j D : ℕ) (M C R : ℝ) (hM : 0 < M) (hR : 0 < R) (hC : 0 ≤ C)
    (hsmall : C * R ^ 2 ≤ 1 / 8)
    (hleaf : ∀ s, ∫⁻ l, coeffSq l ∂leaf s ≤ ENNReal.ofReal (M ^ 2))
    (hbranch : ∀ s, ∫⁻ wr, coeffSq wr.1 ∂branch s ≤ ENNReal.ofReal (C ^ 2))
    (s : S) :
    polynomialMoment leaf branch j D (3 * R / (4 * M)) s ≠ ∞ := by
  exact ne_top_of_le_ne_top (by finiteness)
    (polynomialMoment_uniform_bound leaf branch j D M C R hM hR hC hsmall hleaf hbranch s)

end

end EstimatorIntegrity.FiniteTreeSecondMoment
