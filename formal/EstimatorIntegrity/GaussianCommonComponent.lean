import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Independence
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Topology.ContinuousMap.Bounded.Basic
import Mathlib.Tactic

open MeasureTheory ProbabilityTheory
open scoped BigOperators BoundedContinuousFunction

set_option autoImplicit false

noncomputable section

/-!
# Actual Gaussian common-component decomposition

This file proves a finite-dimensional probability statement.  A jointly Gaussian vector whose
covariance has a constant weighted row sum splits into a residual vector and an independent
scalar Gaussian common part.  It also constructs the vector from a finite independent family of
scalar Gaussian edge variables and derives its covariance rather than assuming it.

The file deliberately contains no tree recursion, PDE, solver, query-complexity, or numerical
claim.
-/

namespace EstimatorIntegrity.GaussianCommonComponent

def commonMap {I : Type*} [Fintype I] (w : I → ℝ) : (I → ℝ) →L[ℝ] ℝ :=
  ∑ i, (w i) • (ContinuousLinearMap.proj i : (I → ℝ) →L[ℝ] ℝ)

@[simp] theorem commonMap_apply {I : Type*} [Fintype I] (w : I → ℝ) (x : I → ℝ) :
    commonMap w x = ∑ i, w i * x i := by
  simp [commonMap]

def residualMap {I : Type*} [Fintype I] (w : I → ℝ) : (I → ℝ) →L[ℝ] (I → ℝ) :=
  ContinuousLinearMap.pi fun i ↦
    (ContinuousLinearMap.proj i : (I → ℝ) →L[ℝ] ℝ) - commonMap w

@[simp] theorem residualMap_apply {I : Type*} [Fintype I] (w : I → ℝ) (x : I → ℝ)
    (i : I) : residualMap w x i = x i - ∑ j, w j * x j := by
  simp [residualMap]

def pairMap {I : Type*} [Fintype I] (w : I → ℝ) :
    (I → ℝ) →L[ℝ] ((I → ℝ) × ℝ) :=
  (residualMap w).prod (commonMap w)

@[simp] theorem pairMap_apply {I : Type*} [Fintype I] (w : I → ℝ) (x : I → ℝ) :
    pairMap w x = (fun i ↦ x i - ∑ j, w j * x j, ∑ j, w j * x j) := by
  ext <;> simp [pairMap]

def pairUnitMap {I : Type*} [Fintype I] (w : I → ℝ) :
    (I → ℝ) →L[ℝ] ((I → ℝ) × (Unit → ℝ)) :=
  (residualMap w).prod (ContinuousLinearMap.pi fun _ : Unit ↦ commonMap w)

@[simp] theorem pairUnitMap_apply {I : Type*} [Fintype I] (w : I → ℝ) (x : I → ℝ) :
    pairUnitMap w x = (fun i ↦ x i - ∑ j, w j * x j, fun _ ↦ ∑ j, w j * x j) := by
  ext <;> simp [pairUnitMap]

def addCommonMap {I : Type*} [Fintype I] : ((I → ℝ) × ℝ) →L[ℝ] (I → ℝ) :=
  ContinuousLinearMap.pi fun i ↦
    (ContinuousLinearMap.proj i : (I → ℝ) →L[ℝ] ℝ).comp
        (ContinuousLinearMap.fst ℝ (I → ℝ) ℝ) +
      ContinuousLinearMap.snd ℝ (I → ℝ) ℝ

@[simp] theorem addCommonMap_apply {I : Type*} [Fintype I] (p : (I → ℝ) × ℝ) (i : I) :
    addCommonMap p i = p.1 i + p.2 := by
  simp [addCommonMap]

def addCommon {I : Type*} [Fintype I] : (I → ℝ) × ℝ → I → ℝ :=
  fun p i ↦ p.1 i + p.2

@[simp] theorem addCommon_apply {I : Type*} [Fintype I] (p : (I → ℝ) × ℝ) (i : I) :
    addCommon p i = p.1 i + p.2 := rfl

theorem addCommon_measurable {I : Type*} [Fintype I] : Measurable (addCommon : (I → ℝ) × ℝ → I → ℝ) := by
  have hEq : (addCommon : (I → ℝ) × ℝ → I → ℝ) = addCommonMap := by
    funext p i
    simp
  rw [hEq]
  exact (addCommonMap (I := I)).continuous.measurable

def edgeMap {I E : Type*} [Fintype I] [Fintype E] (L : I → E → ℝ) :
    (E → ℝ) →L[ℝ] (I → ℝ) :=
  ContinuousLinearMap.pi fun i ↦
    ∑ e, (L i e) • (ContinuousLinearMap.proj e : (E → ℝ) →L[ℝ] ℝ)

@[simp] theorem edgeMap_apply {I E : Type*} [Fintype I] [Fintype E]
    (L : I → E → ℝ) (y : E → ℝ) (i : I) :
    edgeMap L y i = ∑ e, L i e * y e := by
  simp [edgeMap]

variable {Omega I E : Type*} [MeasurableSpace Omega] [Fintype I] [Nonempty I]
  [Fintype E]

variable (mu : Measure Omega) (X : Omega → I → ℝ) (w : I → ℝ)

def commonPart : Omega → ℝ := fun omega ↦ ∑ i, w i * X omega i

def residualPart : Omega → I → ℝ := fun omega i ↦ X omega i - commonPart X w omega

def actualCovariance (i j : I) : ℝ := cov[fun omega ↦ X omega i, fun omega ↦ X omega j; mu]

theorem commonPart_hasGaussianLaw (hX : HasGaussianLaw X mu) :
    HasGaussianLaw (commonPart X w) mu := by
  change HasGaussianLaw (fun omega ↦ ∑ i, w i * X omega i) mu
  simpa only [commonMap_apply] using hX.map_fun (commonMap w)

theorem residualPart_hasGaussianLaw (hX : HasGaussianLaw X mu) :
    HasGaussianLaw (residualPart X w) mu := by
  have hfun : residualPart X w = fun omega ↦ residualMap w (X omega) := by
    funext omega i
    simp [residualPart, commonPart]
  rw [hfun]
  exact hX.map_fun (residualMap w)

theorem pair_hasGaussianLaw (hX : HasGaussianLaw X mu) :
    HasGaussianLaw (fun omega ↦ (residualPart X w omega, commonPart X w omega)) mu := by
  change HasGaussianLaw
    (fun omega ↦ (fun i ↦ X omega i - ∑ j, w j * X omega j, ∑ j, w j * X omega j)) mu
  simpa only [pairMap_apply] using hX.map_fun (pairMap w)

section CommonComponent

variable [IsProbabilityMeasure mu]

theorem commonPart_mean_zero (hX : HasGaussianLaw X mu)
    (hMeanX : ∀ i, ∫ omega, X omega i ∂mu = 0) :
    ∫ omega, commonPart X w omega ∂mu = 0 := by
  rw [show commonPart X w = fun omega ↦ ∑ i, w i * X omega i by rfl,
    integral_finsetSum Finset.univ]
  · simp_rw [integral_const_mul, hMeanX, mul_zero]
    simp
  · intro i hi
    exact (hX.eval i).integrable.const_mul (w i)

theorem residualPart_mean_zero (hX : HasGaussianLaw X mu)
    (hMeanX : ∀ i, ∫ omega, X omega i ∂mu = 0) (i : I) :
    ∫ omega, residualPart X w omega i ∂mu = 0 := by
  change (∫ omega, X omega i - commonPart X w omega ∂mu) = 0
  rw [integral_sub (hX.eval i).integrable (commonPart_hasGaussianLaw mu X w hX).integrable,
    hMeanX, commonPart_mean_zero mu X w hX hMeanX, sub_zero]

theorem covariance_coord_commonPart (hX : HasGaussianLaw X mu)
    (a : ℝ) (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a) (i : I) :
    cov[fun omega ↦ X omega i, commonPart X w; mu] = a := by
  rw [show commonPart X w = fun omega ↦ ∑ j, w j * X omega j by rfl,
    covariance_fun_sum_right]
  · simp_rw [covariance_const_mul_right]
    exact hrow i
  · exact fun j ↦ (hX.eval j).memLp_two.const_mul (w j)
  · exact (hX.eval i).memLp_two

theorem commonPart_variance (hX : HasGaussianLaw X mu) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a) :
    Var[commonPart X w; mu] = a := by
  rw [← covariance_self (commonPart_hasGaussianLaw mu X w hX).aemeasurable]
  change cov[fun omega ↦ ∑ i, w i * X omega i, commonPart X w; mu] = a
  rw [covariance_fun_sum_left]
  · simp_rw [covariance_const_mul_left,
      covariance_coord_commonPart mu X w hX a hrow]
    rw [← Finset.sum_mul, hw, one_mul]
  · exact fun i ↦ (hX.eval i).memLp_two.const_mul (w i)
  · exact (commonPart_hasGaussianLaw mu X w hX).memLp_two

theorem commonPart_parameter_nonneg (hX : HasGaussianLaw X mu) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a) : 0 ≤ a := by
  rw [← commonPart_variance mu X w hX a hw hrow]
  exact variance_nonneg _ _

theorem covariance_residual_commonPart (hX : HasGaussianLaw X mu) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a) (i : I) :
    cov[fun omega ↦ residualPart X w omega i, commonPart X w; mu] = 0 := by
  rw [show (fun omega ↦ residualPart X w omega i) =
      (fun omega ↦ X omega i) - commonPart X w by rfl,
    covariance_sub_left (hX.eval i).memLp_two
      (commonPart_hasGaussianLaw mu X w hX).memLp_two
      (commonPart_hasGaussianLaw mu X w hX).memLp_two,
    covariance_coord_commonPart mu X w hX a hrow,
    covariance_self (commonPart_hasGaussianLaw mu X w hX).aemeasurable,
    commonPart_variance mu X w hX a hw hrow, sub_self]

theorem covariance_residual_residual (hX : HasGaussianLaw X mu) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a) (i j : I) :
    cov[fun omega ↦ residualPart X w omega i,
      fun omega ↦ residualPart X w omega j; mu] = actualCovariance mu X i j - a := by
  rw [show (fun omega ↦ residualPart X w omega i) =
      (fun omega ↦ X omega i) - commonPart X w by rfl,
    show (fun omega ↦ residualPart X w omega j) =
      (fun omega ↦ X omega j) - commonPart X w by rfl,
    covariance_sub_sub (hX.eval i).memLp_two
      (commonPart_hasGaussianLaw mu X w hX).memLp_two (hX.eval j).memLp_two
      (commonPart_hasGaussianLaw mu X w hX).memLp_two,
    covariance_coord_commonPart mu X w hX a hrow,
    show cov[commonPart X w, fun omega ↦ X omega j; mu] = a by
      rw [covariance_comm, covariance_coord_commonPart mu X w hX a hrow],
    covariance_self (commonPart_hasGaussianLaw mu X w hX).aemeasurable,
    commonPart_variance mu X w hX a hw hrow]
  simp only [actualCovariance]
  ring

theorem residualPart_indep_commonPart (hX : HasGaussianLaw X mu) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a) :
    IndepFun (residualPart X w) (commonPart X w) mu := by
  have hPairUnit : HasGaussianLaw
      (fun omega ↦ (residualPart X w omega, fun _ : Unit ↦ commonPart X w omega)) mu := by
    change HasGaussianLaw (fun omega ↦
      (fun i ↦ X omega i - ∑ j, w j * X omega j, fun _ : Unit ↦ ∑ j, w j * X omega j)) mu
    simpa only [pairUnitMap_apply] using hX.map_fun (pairUnitMap w)
  have hIndUnit := hPairUnit.indepFun_of_covariance_eval
    (fun i (_ : Unit) ↦ covariance_residual_commonPart mu X w hX a hw hrow i)
  simpa [Function.comp_def] using
    hIndUnit.comp measurable_id (measurable_pi_apply ())

theorem commonPart_map_eq_gaussianReal (hX : HasGaussianLaw X mu)
    (hMeanX : ∀ i, ∫ omega, X omega i ∂mu = 0) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a) :
    mu.map (commonPart X w) = gaussianReal 0 a.toNNReal := by
  rw [(commonPart_hasGaussianLaw mu X w hX).map_eq_gaussianReal,
    commonPart_mean_zero mu X w hX hMeanX, commonPart_variance mu X w hX a hw hrow]

theorem residualCommon_map_eq_product (hX : HasGaussianLaw X mu)
    (hMeanX : ∀ i, ∫ omega, X omega i ∂mu = 0) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a) :
    mu.map (fun omega ↦ (residualPart X w omega, commonPart X w omega)) =
      (mu.map (residualPart X w)).prod (gaussianReal 0 a.toNNReal) := by
  rw [(residualPart_indep_commonPart mu X w hX a hw hrow).map_prod_eq_prod_map_map
      (residualPart_hasGaussianLaw mu X w hX).aemeasurable
      (commonPart_hasGaussianLaw mu X w hX).aemeasurable,
    commonPart_map_eq_gaussianReal mu X w hX hMeanX a hw hrow]

theorem reconstruction_law (hX : HasGaussianLaw X mu)
    (hMeanX : ∀ i, ∫ omega, X omega i ∂mu = 0) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a) :
    mu.map X = ((mu.map (residualPart X w)).prod (gaussianReal 0 a.toNNReal)).map addCommon := by
  have hPair : AEMeasurable
      (fun omega ↦ (residualPart X w omega, commonPart X w omega)) mu :=
    (pair_hasGaussianLaw mu X w hX).aemeasurable
  have hMapMap := (addCommon_measurable (I := I)).aemeasurable.map_map_of_aemeasurable hPair
  calc
    mu.map X = mu.map (addCommon ∘ fun omega ↦
        (residualPart X w omega, commonPart X w omega)) := by
      apply Measure.map_congr
      filter_upwards [] with omega
      funext i
      simp [Function.comp_def, residualPart]
    _ = (mu.map (fun omega ↦
        (residualPart X w omega, commonPart X w omega))).map addCommon := hMapMap.symm
    _ = ((mu.map (residualPart X w)).prod (gaussianReal 0 a.toNNReal)).map addCommon := by
      rw [residualCommon_map_eq_product mu X w hX hMeanX a hw hrow]

theorem boundedContinuous_integrable_original (hX : HasGaussianLaw X mu)
    (F : (I → ℝ) →ᵇ ℝ) : Integrable (fun omega ↦ F (X omega)) mu := by
  exact (F.integrable (mu.map X)).comp_aemeasurable hX.aemeasurable

theorem boundedContinuous_integrable_product (hX : HasGaussianLaw X mu)
    (hMeanX : ∀ i, ∫ omega, X omega i ∂mu = 0) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a)
    (F : (I → ℝ) →ᵇ ℝ) :
    Integrable (fun p ↦ F (addCommon p))
      ((mu.map (residualPart X w)).prod (gaussianReal 0 a.toNNReal)) := by
  let nu := (mu.map (residualPart X w)).prod (gaussianReal 0 a.toNNReal)
  have hLaw : mu.map X = nu.map addCommon := by
    simpa [nu] using reconstruction_law mu X w hX hMeanX a hw hrow
  have hOnMap : Integrable F (nu.map addCommon) := by
    rw [← hLaw]
    exact F.integrable (mu.map X)
  exact hOnMap.comp_aemeasurable (addCommon_measurable (I := I)).aemeasurable

theorem boundedContinuous_expectation (hX : HasGaussianLaw X mu)
    (hMeanX : ∀ i, ∫ omega, X omega i ∂mu = 0) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hrow : ∀ i, ∑ j, w j * actualCovariance mu X i j = a)
    (F : (I → ℝ) →ᵇ ℝ) :
    ∫ omega, F (X omega) ∂mu =
      ∫ p, F (addCommon p) ∂((mu.map (residualPart X w)).prod
        (gaussianReal 0 a.toNNReal)) := by
  rw [← integral_map hX.aemeasurable F.continuous.aestronglyMeasurable]
  rw [reconstruction_law mu X w hX hMeanX a hw hrow]
  exact integral_map (addCommon_measurable (I := I)).aemeasurable
    F.continuous.aestronglyMeasurable

end CommonComponent

variable (Y : E → Omega → ℝ) (L : I → E → ℝ)

def edgeLeafVector : Omega → I → ℝ := fun omega i ↦ ∑ e, L i e * Y e omega

theorem edgeLeafVector_hasGaussianLaw (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (hYIndep : iIndepFun Y mu) : HasGaussianLaw (edgeLeafVector Y L) mu := by
  have hYVector : HasGaussianLaw (fun omega e ↦ Y e omega) mu :=
    hYIndep.hasGaussianLaw hYGauss
  have hfun : edgeLeafVector Y L = fun omega ↦ edgeMap L (fun e ↦ Y e omega) := by
    funext omega i
    simp [edgeLeafVector]
  rw [hfun]
  exact hYVector.map_fun (edgeMap L)

section EdgeConstruction

variable [IsProbabilityMeasure mu]

local instance : DecidableEq E := Classical.decEq E

theorem edgeLeafVector_mean_zero (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (hYMean : ∀ e, ∫ omega, Y e omega ∂mu = 0) (i : I) :
    ∫ omega, edgeLeafVector Y L omega i ∂mu = 0 := by
  rw [show (fun omega ↦ edgeLeafVector Y L omega i) =
      fun omega ↦ ∑ e, L i e * Y e omega by rfl,
    integral_finsetSum Finset.univ]
  · simp_rw [integral_const_mul, hYMean, mul_zero]
    simp
  · intro e he
    exact (hYGauss e).integrable.const_mul (L i e)

theorem edgeVariance_nonneg (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (ell : E → ℝ) (hYVar : ∀ e, Var[Y e; mu] = ell e) (e : E) : 0 ≤ ell e := by
  rw [← hYVar e]
  exact variance_nonneg _ _

theorem edgeVariables_covariance (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (hYIndep : iIndepFun Y mu) (ell : E → ℝ) (hYVar : ∀ e, Var[Y e; mu] = ell e)
    (e f : E) : cov[Y e, Y f; mu] = if e = f then ell e else 0 := by
  classical
  by_cases hef : e = f
  · subst f
    rw [if_pos rfl, covariance_self (hYGauss e).aemeasurable, hYVar]
  · rw [if_neg hef]
    exact (hYIndep.indepFun hef).covariance_eq_zero
      (hYGauss e).memLp_two (hYGauss f).memLp_two

theorem edgeLeafVector_covariance (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (hYIndep : iIndepFun Y mu) (ell : E → ℝ) (hYVar : ∀ e, Var[Y e; mu] = ell e)
    (i j : I) :
    cov[fun omega ↦ edgeLeafVector Y L omega i,
      fun omega ↦ edgeLeafVector Y L omega j; mu] =
      ∑ e, ell e * L i e * L j e := by
  classical
  rw [show (fun omega ↦ edgeLeafVector Y L omega i) =
      (fun omega ↦ ∑ e, L i e * Y e omega) by rfl,
    show (fun omega ↦ edgeLeafVector Y L omega j) =
      (fun omega ↦ ∑ f, L j f * Y f omega) by rfl,
    covariance_fun_sum_fun_sum]
  · simp_rw [covariance_const_mul_left, covariance_const_mul_right,
      edgeVariables_covariance mu Y hYGauss hYIndep ell hYVar]
    simp [mul_assoc, mul_left_comm, mul_comm]
  · exact fun e ↦ (hYGauss e).memLp_two.const_mul (L i e)
  · exact fun e ↦ (hYGauss e).memLp_two.const_mul (L j e)

theorem weighted_edgeCovariance (ell : E → ℝ) (i : I) :
    ∑ j, w j * (∑ e, ell e * L i e * L j e) =
      ∑ e, ell e * L i e * (∑ j, w j * L j e) := by
  calc
    ∑ j, w j * (∑ e, ell e * L i e * L j e) =
        ∑ j, ∑ e, w j * (ell e * L i e * L j e) := by
          apply Finset.sum_congr rfl
          intro j hj
          rw [Finset.mul_sum]
    _ = ∑ e, ∑ j, w j * (ell e * L i e * L j e) := Finset.sum_comm
    _ = ∑ e, ell e * L i e * (∑ j, w j * L j e) := by
      apply Finset.sum_congr rfl
      intro e he
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j hj
      ring

theorem edgeLeafVector_row_covariance (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (hYIndep : iIndepFun Y mu) (ell : E → ℝ) (hYVar : ∀ e, Var[Y e; mu] = ell e)
    (a : ℝ) (hcoeff : ∀ i, ∑ e, ell e * L i e * (∑ j, w j * L j e) = a)
    (i : I) :
    ∑ j, w j * actualCovariance mu (edgeLeafVector Y L) i j = a := by
  simp_rw [actualCovariance, edgeLeafVector_covariance mu Y L hYGauss hYIndep ell hYVar]
  rw [weighted_edgeCovariance w L ell i, hcoeff]

theorem edgeLeafVector_residual_indep_common (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (hYMean : ∀ e, ∫ omega, Y e omega ∂mu = 0) (hYIndep : iIndepFun Y mu)
    (ell : E → ℝ) (hYVar : ∀ e, Var[Y e; mu] = ell e) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hcoeff : ∀ i, ∑ e, ell e * L i e * (∑ j, w j * L j e) = a) :
    IndepFun (residualPart (edgeLeafVector Y L) w) (commonPart (edgeLeafVector Y L) w) mu := by
  have hrow : ∀ i : I,
      ∑ j, w j * actualCovariance mu (edgeLeafVector Y L) i j = a :=
    edgeLeafVector_row_covariance (I := I) (E := E) mu w Y L hYGauss hYIndep ell hYVar a hcoeff
  apply residualPart_indep_commonPart mu (edgeLeafVector Y L) w
    (edgeLeafVector_hasGaussianLaw mu Y L hYGauss hYIndep) a hw
  exact hrow

theorem edgeLeafVector_product_law (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (hYMean : ∀ e, ∫ omega, Y e omega ∂mu = 0) (hYIndep : iIndepFun Y mu)
    (ell : E → ℝ) (hYVar : ∀ e, Var[Y e; mu] = ell e) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hcoeff : ∀ i, ∑ e, ell e * L i e * (∑ j, w j * L j e) = a) :
    mu.map (fun omega ↦
        (residualPart (edgeLeafVector Y L) w omega, commonPart (edgeLeafVector Y L) w omega)) =
      (mu.map (residualPart (edgeLeafVector Y L) w)).prod (gaussianReal 0 a.toNNReal) := by
  have hrow : ∀ i : I,
      ∑ j, w j * actualCovariance mu (edgeLeafVector Y L) i j = a :=
    edgeLeafVector_row_covariance (I := I) (E := E) mu w Y L hYGauss hYIndep ell hYVar a hcoeff
  apply residualCommon_map_eq_product mu (edgeLeafVector Y L) w
    (edgeLeafVector_hasGaussianLaw mu Y L hYGauss hYIndep)
    (edgeLeafVector_mean_zero mu Y L hYGauss hYMean) a hw
  exact hrow

theorem edgeLeafVector_reconstruction_law (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (hYMean : ∀ e, ∫ omega, Y e omega ∂mu = 0) (hYIndep : iIndepFun Y mu)
    (ell : E → ℝ) (hYVar : ∀ e, Var[Y e; mu] = ell e) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hcoeff : ∀ i, ∑ e, ell e * L i e * (∑ j, w j * L j e) = a) :
    mu.map (edgeLeafVector Y L) =
      ((mu.map (residualPart (edgeLeafVector Y L) w)).prod
        (gaussianReal 0 a.toNNReal)).map addCommon := by
  have hrow : ∀ i : I,
      ∑ j, w j * actualCovariance mu (edgeLeafVector Y L) i j = a :=
    edgeLeafVector_row_covariance (I := I) (E := E) mu w Y L hYGauss hYIndep ell hYVar a hcoeff
  apply reconstruction_law mu (edgeLeafVector Y L) w
    (edgeLeafVector_hasGaussianLaw mu Y L hYGauss hYIndep)
    (edgeLeafVector_mean_zero mu Y L hYGauss hYMean) a hw
  exact hrow

theorem edgeLeafVector_expectation (hYGauss : ∀ e, HasGaussianLaw (Y e) mu)
    (hYMean : ∀ e, ∫ omega, Y e omega ∂mu = 0) (hYIndep : iIndepFun Y mu)
    (ell : E → ℝ) (hYVar : ∀ e, Var[Y e; mu] = ell e) (a : ℝ)
    (hw : ∑ i, w i = 1)
    (hcoeff : ∀ i, ∑ e, ell e * L i e * (∑ j, w j * L j e) = a)
    (F : (I → ℝ) →ᵇ ℝ) :
    ∫ omega, F (edgeLeafVector Y L omega) ∂mu =
      ∫ p, F (addCommon p) ∂((mu.map (residualPart (edgeLeafVector Y L) w)).prod
        (gaussianReal 0 a.toNNReal)) := by
  have hrow : ∀ i : I,
      ∑ j, w j * actualCovariance mu (edgeLeafVector Y L) i j = a :=
    edgeLeafVector_row_covariance (I := I) (E := E) mu w Y L hYGauss hYIndep ell hYVar a hcoeff
  apply boundedContinuous_expectation mu (edgeLeafVector Y L) w
    (edgeLeafVector_hasGaussianLaw mu Y L hYGauss hYIndep)
    (edgeLeafVector_mean_zero mu Y L hYGauss hYMean) a hw
    hrow F

end EdgeConstruction

end EstimatorIntegrity.GaussianCommonComponent
