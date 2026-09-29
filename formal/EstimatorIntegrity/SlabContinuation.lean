import EstimatorIntegrity.AllenCahnBounds
import Mathlib.Tactic
import Mathlib.Topology.MetricSpace.Lipschitz

/-!
# Elementary algebra for slab continuation

This module contains only deterministic finite-dimensional and finite-family
inequalities. It does not formalize the stochastic tree construction, moment
identification, or a PDE representation theorem.
-/

namespace EstimatorIntegrity

noncomputable section

/-- Terminal absolute envelopes in coordinate order `(Id, D, F₀, F₁, F₂, F₃)`. -/
def slabTerminalEnvelope : Fin 6 → ℝ :=
  ![2 / 5, 1 / 2, 2 / 5, 1, 12 / 5, 6]

/-- Rational supersolution candidate for the six-code local moment system. -/
def slabMomentSupersolution : Fin 6 → ℝ :=
  ![1 / 4, 1 / 2, 1 / 2, 3, 12, 50]

/-- The exact coordinatewise rational postfixed-point check used by the local
Allen–Cahn moment certificate. -/
theorem slabMomentSupersolution_postfixed (i : Fin 6) :
    (21 / 16 : ℝ) * slabTerminalEnvelope i ^ 2 +
        allenCahnBranchPolynomial slabMomentSupersolution i / 21 ≤
      slabMomentSupersolution i := by
  fin_cases i <;>
    simp [slabTerminalEnvelope, slabMomentSupersolution,
      allenCahnBranchPolynomial] <;>
    norm_num

/-- Every coordinate of the rational moment box has positive slack. -/
theorem slabMomentSupersolution_postfixed_strict (i : Fin 6) :
    (21 / 16 : ℝ) * slabTerminalEnvelope i ^ 2 +
        allenCahnBranchPolynomial slabMomentSupersolution i / 21 <
      slabMomentSupersolution i := by
  fin_cases i <;>
    simp [slabTerminalEnvelope, slabMomentSupersolution,
      allenCahnBranchPolynomial] <;>
    norm_num

/-- Projection onto the symmetric interval `[-a,a]`. -/
def intervalClamp (a x : ℝ) (ha : 0 ≤ a) : ℝ :=
  Set.projIcc (-a) a (neg_le_self ha) x

/-- Clamping to `[-a,a]` cannot increase the distance to a target already in
that interval. -/
theorem intervalClamp_abs_sub_le (a x z : ℝ) (ha : 0 ≤ a) (hz : |z| ≤ a) :
    |intervalClamp a x ha - z| ≤ |x - z| := by
  have hzmem : z ∈ Set.Icc (-a) a := abs_le.mp hz
  have h := (LipschitzWith.projIcc (neg_le_self ha)).dist_le_mul x z
  rw [Set.projIcc_of_mem (neg_le_self ha) hzmem] at h
  simpa [intervalClamp, Subtype.dist_eq, Real.dist_eq] using h

/-- A finite constant-coefficient error recurrence. The deliberately coarse
factor `n * ρ^n` is convenient when one uniform slab constant is used. -/
theorem finite_error_recurrence (e : ℕ → ℝ) (ρ v : ℝ)
    (he0 : e 0 = 0) (hρ : 1 ≤ ρ) (hv : 0 ≤ v)
    (hstep : ∀ j, e (j + 1) ≤ ρ * e j + v) :
    ∀ n, e n ≤ (n : ℝ) * ρ ^ n * v := by
  intro n
  induction n with
  | zero =>
      rw [he0]
      norm_num
  | succ k ih =>
      have hρ0 : 0 ≤ ρ := zero_le_one.trans hρ
      have hpow : 1 ≤ ρ ^ (k + 1) := one_le_pow₀ hρ
      have hvpow : v ≤ ρ ^ (k + 1) * v := by
        simpa only [one_mul] using mul_le_mul_of_nonneg_right hpow hv
      calc
        e (k + 1) ≤ ρ * e k + v := hstep k
        _ ≤ ρ * ((k : ℝ) * ρ ^ k * v) + v :=
          add_le_add (mul_le_mul_of_nonneg_left ih hρ0) (le_refl v)
        _ = (k : ℝ) * ρ ^ (k + 1) * v + v := by
          rw [pow_succ]
          ring
        _ ≤ (k : ℝ) * ρ ^ (k + 1) * v + ρ ^ (k + 1) * v :=
          add_le_add (le_refl ((k : ℝ) * ρ ^ (k + 1) * v)) hvpow
        _ = (↑(k + 1) : ℝ) * ρ ^ (k + 1) * v := by
          norm_num
          ring

/-! ## Exact rational checks for the three-mode projected interface -/

/-- Absolute coefficient bounds for frequencies `1`, `3`, and `5`. -/
def projectedCoefficientBounds : Fin 3 → ℝ :=
  ![23 / 100, 3 / 1000, 1 / 20000]

theorem projectedCoefficientBounds_sum :
    ∑ i, projectedCoefficientBounds i = (4661 / 20000 : ℝ) := by
  norm_num [projectedCoefficientBounds, Fin.sum_univ_succ]

theorem projectedCoefficientBounds_weightedSum :
    projectedCoefficientBounds 0 + 3 * projectedCoefficientBounds 1 +
        5 * projectedCoefficientBounds 2 = (957 / 4000 : ℝ) := by
  simp [projectedCoefficientBounds]
  norm_num

/-- The coefficient box lies strictly inside the terminal value envelope. -/
theorem projectedCoefficientBounds_value :
    2 * (4661 / 20000 : ℝ) ^ 2 < (2 / 5 : ℝ) ^ 2 := by
  norm_num

/-- The frequency-weighted coefficient box lies strictly inside the terminal
derivative envelope using `ω² ≤ 40/21`. -/
theorem projectedCoefficientBounds_derivative :
    (80 / 21 : ℝ) * (957 / 4000 : ℝ) ^ 2 < (1 / 2 : ℝ) ^ 2 := by
  norm_num

/-- Exact upper bound for the periodic stability exponent
`γ = 1 - ω² / 2` obtained from the Poincaré estimate. -/
theorem periodicStabilityExponent_upper :
    (1 - (20 / 21 : ℝ) * (76 / 77 : ℝ) ^ 2) = 8989 / 124509 ∧
      (8989 / 124509 : ℝ) < 3 / 40 := by
  norm_num

/-- The fifty-slab amplification factor stays below the saved global factor. -/
theorem fiftySlabAmplification_upper :
    50 * (250 / 247 : ℝ) ^ 50 < 100 := by
  norm_num

/-- Exact normalized spatial `L²` MSE budget check. -/
theorem normalizedSpatialMSE_budget :
    100 * ((3 / 4 : ℝ) / 200000 + (1 / 100000000 : ℝ) ^ 2) <
      (1 / 50 : ℝ) ^ 2 := by
  norm_num

end

end EstimatorIntegrity
