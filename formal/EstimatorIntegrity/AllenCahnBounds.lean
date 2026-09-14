import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Real.Basic

/-!
# Algebra for the six-code Allen–Cahn moment majorant

The coordinate order is `(Id, D, F₀, F₁, F₂, F₃)`, with scalar factors removed
from the `F` coordinates by division by their squares. The polynomial is for
the raw derivative-coded mechanism whose two-alternative rows have labelled
tuple probabilities `1/2`.
These theorems establish positivity and order preservation of the polynomial
and its vector field. They do not establish the stochastic moment recursion,
ODE existence, a comparison theorem, or the soundness of a numerical solver.
-/

namespace EstimatorIntegrity

noncomputable section

/-- Branching polynomial of the six-code raw Allen–Cahn majorant. -/
def allenCahnBranchPolynomial (y : Fin 6 → ℝ) : Fin 6 → ℝ :=
  ![y 2,
    y 3 * y 1,
    2 * y 2 * y 3 + y 1 ^ 2 * y 4 / 2,
    2 * y 2 * y 4 + y 1 ^ 2 * y 5 / 2,
    2 * y 2 * y 5,
    0]

/-- The tilted majorant vector field at a fixed rate and event tilt. -/
def allenCahnMomentField (rate tilt : ℝ) (y : Fin 6 → ℝ) : Fin 6 → ℝ :=
  fun i => rate * y i + tilt / rate * allenCahnBranchPolynomial y i

/-- Every branch term is nonnegative on the nonnegative orthant. -/
theorem allenCahnBranchPolynomial_nonneg (y : Fin 6 → ℝ)
    (hy : ∀ i, 0 ≤ y i) (i : Fin 6) :
    0 ≤ allenCahnBranchPolynomial y i := by
  exact Fin.cases (hy 2)
    (Fin.cases (mul_nonneg (hy 3) (hy 1))
      (Fin.cases
        (add_nonneg (mul_nonneg (mul_nonneg zero_le_two (hy 2)) (hy 3))
          (div_nonneg (mul_nonneg (sq_nonneg (y 1)) (hy 4)) zero_le_two))
        (Fin.cases
          (add_nonneg (mul_nonneg (mul_nonneg zero_le_two (hy 2)) (hy 4))
            (div_nonneg (mul_nonneg (sq_nonneg (y 1)) (hy 5)) zero_le_two))
          (Fin.cases (mul_nonneg (mul_nonneg zero_le_two (hy 2)) (hy 5))
            (Fin.cases (le_refl 0) (fun j => Fin.elim0 j)))))) i

/-- Componentwise ordering is preserved by the branch polynomial on the
nonnegative orthant. Nonnegativity of the larger state follows from `hyz`. -/
theorem allenCahnBranchPolynomial_mono (y z : Fin 6 → ℝ)
    (hy : ∀ i, 0 ≤ y i) (hyz : ∀ i, y i ≤ z i) (i : Fin 6) :
    allenCahnBranchPolynomial y i ≤ allenCahnBranchPolynomial z i := by
  have hquadratic : ∀ j k : Fin 6, 2 * y j * y k ≤ 2 * z j * z k :=
    fun j k => mul_le_mul (mul_le_mul_of_nonneg_left (hyz j) zero_le_two)
      (hyz k) (hy k) (mul_nonneg zero_le_two ((hy j).trans (hyz j)))
  have hcubic : ∀ j : Fin 6, y 1 ^ 2 * y j / 2 ≤ z 1 ^ 2 * z j / 2 :=
    fun j => div_le_div_of_nonneg_right
      (mul_le_mul (pow_le_pow_left₀ (hy 1) (hyz 1) 2) (hyz j)
        (hy j) (sq_nonneg (z 1))) zero_le_two
  exact Fin.cases (hyz 2)
    (Fin.cases (mul_le_mul (hyz 3) (hyz 1) (hy 1) ((hy 3).trans (hyz 3)))
      (Fin.cases (add_le_add (hquadratic 2 3) (hcubic 4))
        (Fin.cases (add_le_add (hquadratic 2 4) (hcubic 5))
          (Fin.cases (hquadratic 2 5) (Fin.cases (le_refl 0)
            (fun j => Fin.elim0 j)))))) i

/-- Nonnegative rate and tilt preserve nonnegativity of the moment field. -/
theorem allenCahnMomentField_nonneg (rate tilt : ℝ) (y : Fin 6 → ℝ)
    (hrate : 0 ≤ rate) (htilt : 0 ≤ tilt) (hy : ∀ i, 0 ≤ y i)
    (i : Fin 6) : 0 ≤ allenCahnMomentField rate tilt y i := by
  exact add_nonneg (mul_nonneg hrate (hy i))
    (mul_nonneg (div_nonneg htilt hrate) (allenCahnBranchPolynomial_nonneg y hy i))

/-- The moment field preserves componentwise ordering on nonnegative states. -/
theorem allenCahnMomentField_mono (rate tilt : ℝ) (y z : Fin 6 → ℝ)
    (hrate : 0 ≤ rate) (htilt : 0 ≤ tilt)
    (hy : ∀ i, 0 ≤ y i) (hyz : ∀ i, y i ≤ z i) (i : Fin 6) :
    allenCahnMomentField rate tilt y i ≤ allenCahnMomentField rate tilt z i := by
  exact add_le_add (mul_le_mul_of_nonneg_left (hyz i) hrate)
    (mul_le_mul_of_nonneg_left (allenCahnBranchPolynomial_mono y z hy hyz i)
      (div_nonneg htilt hrate))

/-- A whole rate interval is bounded by using its upper endpoint in the linear
term and its lower endpoint in the reciprocal branch term. -/
theorem allenCahnMomentField_interval_upper
    (rate lower upper tilt : ℝ) (y : Fin 6 → ℝ)
    (hlower : 0 < lower) (hrateLower : lower ≤ rate)
    (hrateUpper : rate ≤ upper) (htilt : 0 ≤ tilt)
    (hy : ∀ i, 0 ≤ y i) (i : Fin 6) :
    allenCahnMomentField rate tilt y i ≤
      upper * y i + tilt / lower * allenCahnBranchPolynomial y i := by
  exact add_le_add (mul_le_mul_of_nonneg_right hrateUpper (hy i))
    (mul_le_mul_of_nonneg_right
      (div_le_div_of_nonneg_left htilt hlower hrateLower)
      (allenCahnBranchPolynomial_nonneg y hy i))

/-- The exact postfixed-box inequality bounds the field by the affine-segment
slope throughout the nonnegative box and throughout the rate interval. This
is algebra only: ODE comparison and stochastic domination remain separate. -/
theorem allenCahn_postfixed_box_slope
    (rate lower upper tilt step : ℝ) (a b y : Fin 6 → ℝ)
    (hlower : 0 < lower) (hrateLower : lower ≤ rate)
    (hrateUpper : rate ≤ upper) (htilt : 0 ≤ tilt) (hstep : 0 < step)
    (hy : ∀ i, 0 ≤ y i) (hyb : ∀ i, y i ≤ b i)
    (hbox : ∀ i, a i + step *
      (upper * b i + tilt / lower * allenCahnBranchPolynomial b i) ≤ b i)
    (i : Fin 6) :
    allenCahnMomentField rate tilt y i ≤ (b i - a i) / step := by
  calc
    allenCahnMomentField rate tilt y i ≤ allenCahnMomentField rate tilt b i :=
      allenCahnMomentField_mono rate tilt y b
        (hlower.le.trans hrateLower) htilt hy hyb i
    _ ≤ upper * b i + tilt / lower * allenCahnBranchPolynomial b i :=
      allenCahnMomentField_interval_upper rate lower upper tilt b
        hlower hrateLower hrateUpper htilt (fun j => (hy j).trans (hyb j)) i
    _ ≤ (b i - a i) / step :=
      (le_div_iff₀ hstep).2
        ((mul_comm step (upper * b i + tilt / lower * allenCahnBranchPolynomial b i)) ▸
          (le_sub_iff_add_le').2 (hbox i))

end

end EstimatorIntegrity
