import Mathlib.MeasureTheory.Integral.IntegralEqImproper
import Mathlib.Tactic

/-!
# Integrated width of a moving monotone barrier

This module proves the analytic shift identity used by the two-moving-barrier
construction.  The function is assumed continuous and monotone on all of
`ℝ`; this is the explicit global specialization of the half-line statement.
A half-line flow has such an extension by setting it equal to `l 0` on the
negative axis.

No integrability of `b - l` on the half-line is assumed.  The proof uses only
finite interval identities and a remainder squeeze.
-/

namespace EstimatorIntegrity

open Filter MeasureTheory Set
open scoped Interval Topology

noncomputable section

/-- A nonnegative shift of a globally monotone function has nonnegative
increment. -/
theorem movingBarrier_increment_nonneg
    (l : ℝ → ℝ) (hl_mono : Monotone l) (Δ : ℝ) (hΔ : 0 ≤ Δ) (t : ℝ) :
    0 ≤ l (t + Δ) - l t := by
  exact sub_nonneg.mpr (hl_mono (le_add_of_nonneg_right hΔ))

/-- Translation and two finite interval splittings give the telescoping
identity for a shifted continuous function. -/
theorem movingBarrier_finite_telescope
    (l : ℝ → ℝ) (hl_cont : Continuous l) (Δ T : ℝ) :
    (∫ t in (0 : ℝ)..T, (l (t + Δ) - l t)) =
      (∫ t in T..T + Δ, l t) - ∫ t in (0 : ℝ)..Δ, l t := by
  have hl_int : ∀ a c : ℝ, IntervalIntegrable l volume a c :=
    fun a c => hl_cont.intervalIntegrable a c
  have hshift_cont : Continuous (fun t => l (t + Δ)) :=
    hl_cont.comp (continuous_id.add continuous_const)
  have hsplit_T := intervalIntegral.integral_add_adjacent_intervals
    (hl_int 0 T) (hl_int T (T + Δ))
  have hsplit_Δ := intervalIntegral.integral_add_adjacent_intervals
    (hl_int 0 Δ) (hl_int Δ (T + Δ))
  rw [intervalIntegral.integral_sub
    (hshift_cont.intervalIntegrable 0 T) (hl_int 0 T)]
  rw [intervalIntegral.integral_comp_add_right]
  simp only [zero_add]
  linarith

/-- The truncated width integral is the initial defect-window mass minus a
translated remainder.  All integrals here are over finite intervals. -/
theorem movingBarrier_finite_identity
    (l : ℝ → ℝ) (hl_cont : Continuous l) (b Δ T : ℝ) :
    (∫ t in (0 : ℝ)..T, (l (t + Δ) - l t)) =
      (∫ t in (0 : ℝ)..Δ, (b - l t)) -
        ∫ t in T..T + Δ, (b - l t) := by
  rw [movingBarrier_finite_telescope l hl_cont Δ T]
  have hl_int : ∀ a c : ℝ, IntervalIntegrable l volume a c :=
    fun a c => hl_cont.intervalIntegrable a c
  have hbml_cont : Continuous (fun t => b - l t) :=
    continuous_const.sub hl_cont
  rw [intervalIntegral.integral_sub
      (continuous_const.intervalIntegrable 0 Δ) (hl_int 0 Δ),
    intervalIntegral.integral_sub
      (continuous_const.intervalIntegrable T (T + Δ)) (hl_int T (T + Δ))]
  simp only [intervalIntegral.integral_const, smul_eq_mul]
  ring

/-- The finite-window defect remainder is nonnegative and bounded by its
left-endpoint rectangle. -/
theorem movingBarrier_remainder_bounds
    (l : ℝ → ℝ) (hl_cont : Continuous l) (hl_mono : Monotone l)
    (b Δ T : ℝ) (hbound : ∀ t, 0 ≤ t → l t ≤ b)
    (hΔ : 0 ≤ Δ) (hT : 0 ≤ T) :
    0 ≤ (∫ t in T..T + Δ, (b - l t)) ∧
      (∫ t in T..T + Δ, (b - l t)) ≤ Δ * (b - l T) := by
  have hTTΔ : T ≤ T + Δ := le_add_of_nonneg_right hΔ
  have hdef_cont : Continuous (fun t => b - l t) := continuous_const.sub hl_cont
  have hdef_int : IntervalIntegrable (fun t => b - l t) volume T (T + Δ) :=
    hdef_cont.intervalIntegrable T (T + Δ)
  constructor
  · exact intervalIntegral.integral_nonneg hTTΔ (fun t ht => by
      exact sub_nonneg.mpr (hbound t (hT.trans ht.1)))
  · have hconst_int : IntervalIntegrable (fun _ : ℝ => b - l T) volume T (T + Δ) :=
      continuous_const.intervalIntegrable T (T + Δ)
    have hmono_int := intervalIntegral.integral_mono_on hTTΔ hdef_int hconst_int
      (fun t ht => by
        exact sub_le_sub_left (hl_mono ht.1) b)
    calc
      (∫ t in T..T + Δ, (b - l t)) ≤
          ∫ _ in T..T + Δ, (b - l T) := hmono_int
      _ = Δ * (b - l T) := by
        rw [intervalIntegral.integral_const]
        ring

/-- The shifted width is integrable on the positive half-line.  This is
derived from uniformly bounded truncated integrals; it is not an assumption. -/
theorem movingBarrier_integrableOn
    (l : ℝ → ℝ) (hl_cont : Continuous l) (hl_mono : Monotone l)
    (b Δ : ℝ) (hbound : ∀ t, 0 ≤ t → l t ≤ b) (hΔ : 0 ≤ Δ) :
    IntegrableOn (fun t => l (t + Δ) - l t) (Ici (0 : ℝ)) := by
  let h : ℝ → ℝ := fun t => l (t + Δ) - l t
  let J : ℝ := ∫ t in (0 : ℝ)..Δ, (b - l t)
  have hh_cont : Continuous h :=
    (hl_cont.comp (continuous_id.add continuous_const)).sub hl_cont
  have hh_nonneg : ∀ t, 0 ≤ h t := fun t =>
    movingBarrier_increment_nonneg l hl_mono Δ hΔ t
  have hIoi : IntegrableOn h (Ioi (0 : ℝ)) := by
    refine integrableOn_Ioi_of_intervalIntegral_norm_bounded
      (l := atTop) (b := fun T : ℝ => T) (f := h) (μ := volume) J 0 ?_ tendsto_id ?_
    · intro T
      by_cases hT : 0 ≤ T
      · exact (intervalIntegrable_iff_integrableOn_Ioc_of_le hT).mp
          (hh_cont.intervalIntegrable 0 T)
      · have hempty : Set.Ioc (0 : ℝ) T = ∅ :=
          Set.Ioc_eq_empty (not_lt_of_ge (le_of_not_ge hT))
        simp only [hempty, integrableOn_empty]
    · filter_upwards [eventually_ge_atTop (0 : ℝ)] with T hT
      have hnorm : (∫ t in (0 : ℝ)..T, ‖h t‖) = ∫ t in (0 : ℝ)..T, h t := by
        apply intervalIntegral.integral_congr
        intro t ht
        change ‖h t‖ = h t
        rw [Real.norm_eq_abs, abs_of_nonneg (hh_nonneg t)]
      rw [hnorm]
      rw [show (∫ t in (0 : ℝ)..T, h t) =
          J - ∫ t in T..T + Δ, (b - l t) by
        exact movingBarrier_finite_identity l hl_cont b Δ T]
      exact sub_le_self J
        (movingBarrier_remainder_bounds l hl_cont hl_mono b Δ T hbound hΔ hT).1
  simpa only [IntegrableOn, restrict_Ioi_eq_restrict_Ici] using hIoi

/-- The total Lebesgue integral of the shifted width equals the finite initial
defect-window mass. -/
theorem movingBarrier_integral_eq
    (l : ℝ → ℝ) (hl_cont : Continuous l) (hl_mono : Monotone l)
    (b Δ : ℝ) (hbound : ∀ t, 0 ≤ t → l t ≤ b)
    (hl_lim : Tendsto l atTop (𝓝 b)) (hΔ : 0 ≤ Δ) :
    (∫ t in Ici (0 : ℝ), (l (t + Δ) - l t)) =
      ∫ t in (0 : ℝ)..Δ, (b - l t) := by
  let h : ℝ → ℝ := fun t => l (t + Δ) - l t
  let J : ℝ := ∫ t in (0 : ℝ)..Δ, (b - l t)
  let R : ℝ → ℝ := fun T => ∫ t in T..T + Δ, (b - l t)
  have hh_Ici : IntegrableOn h (Ici (0 : ℝ)) :=
    movingBarrier_integrableOn l hl_cont hl_mono b Δ hbound hΔ
  have hh_Ioi : IntegrableOn h (Ioi (0 : ℝ)) :=
    by simpa only [IntegrableOn, restrict_Ioi_eq_restrict_Ici] using hh_Ici
  have hupper : Tendsto (fun T => Δ * (b - l T)) atTop (𝓝 0) := by
    have hconst : Tendsto (fun _ : ℝ => Δ) atTop (𝓝 Δ) := tendsto_const_nhds
    have hbsub : Tendsto (fun T => b - l T) atTop (𝓝 (b - b)) :=
      tendsto_const_nhds.sub hl_lim
    simpa only [sub_self, mul_zero] using hconst.mul hbsub
  have hR_zero : Tendsto R atTop (𝓝 0) := by
    apply squeeze_zero'
    · filter_upwards [eventually_ge_atTop (0 : ℝ)] with T hT
      exact (movingBarrier_remainder_bounds l hl_cont hl_mono b Δ T
        hbound hΔ hT).1
    · filter_upwards [eventually_ge_atTop (0 : ℝ)] with T hT
      exact (movingBarrier_remainder_bounds l hl_cont hl_mono b Δ T
        hbound hΔ hT).2
    · exact hupper
  have htrunc_J : Tendsto (fun T => ∫ t in (0 : ℝ)..T, h t) atTop (𝓝 J) := by
    have hconst : Tendsto (fun _ : ℝ => J) atTop (𝓝 J) := tendsto_const_nhds
    have hsub : Tendsto (fun T => J - R T) atTop (𝓝 J) := by
      simpa using hconst.sub hR_zero
    exact hsub.congr' (Eventually.of_forall fun T =>
      (movingBarrier_finite_identity l hl_cont b Δ T).symm)
  have hIoi_eq : (∫ t in Ioi (0 : ℝ), h t) = J :=
    tendsto_nhds_unique
      (intervalIntegral_tendsto_integral_Ioi 0 hh_Ioi tendsto_id) htrunc_J
  rw [integral_Ici_eq_integral_Ioi]
  exact hIoi_eq

/-- Combined primary gate: integrability and the exact total-width identity. -/
theorem movingBarrier_width
    (l : ℝ → ℝ) (hl_cont : Continuous l) (hl_mono : Monotone l)
    (b Δ : ℝ) (hbound : ∀ t, 0 ≤ t → l t ≤ b)
    (hl_lim : Tendsto l atTop (𝓝 b)) (hΔ : 0 ≤ Δ) :
    IntegrableOn (fun t => l (t + Δ) - l t) (Ici (0 : ℝ)) ∧
      (∫ t in Ici (0 : ℝ), (l (t + Δ) - l t)) =
        ∫ t in (0 : ℝ)..Δ, (b - l t) := by
  exact ⟨movingBarrier_integrableOn l hl_cont hl_mono b Δ hbound hΔ,
    movingBarrier_integral_eq l hl_cont hl_mono b Δ hbound hl_lim hΔ⟩

/-- A positive support interval converts the elementary second-moment bound
into the sharp relative-variance inequality.  This is purely finite moment
algebra; it does not identify `μ` or `s2` with probabilistic integrals. -/
theorem positiveInterval_relativeVariance
    (A B μ s2 : ℝ) (hA : 0 < A) (hAB : A ≤ B)
    (hμ_pos : 0 < μ) (_hμ_lower : A ≤ μ) (_hμ_upper : μ ≤ B)
    (hs2 : s2 ≤ (A + B) * μ - A * B) :
    s2 - μ ^ 2 ≤ ((B - A) ^ 2 / (4 * A * B)) * μ ^ 2 := by
  have hB : 0 < B := hA.trans_le hAB
  have hdenom : 0 < 4 * A * B := by positivity
  have hvar : s2 - μ ^ 2 ≤ ((A + B) * μ - A * B) - μ ^ 2 :=
    sub_le_sub_right hs2 (μ ^ 2)
  have hscaled := mul_le_mul_of_nonneg_right hvar hdenom.le
  have hsquare : 0 ≤ ((A + B) * μ - 2 * A * B) ^ 2 := sq_nonneg _
  have hgap :
      (4 * A * B) * (((A + B) * μ - A * B) - μ ^ 2) ≤
        (B - A) ^ 2 * μ ^ 2 := by
    nlinarith
  have hscaled' :
      (s2 - μ ^ 2) * (4 * A * B) ≤ (B - A) ^ 2 * μ ^ 2 := by
    calc
      (s2 - μ ^ 2) * (4 * A * B) ≤
          (((A + B) * μ - A * B) - μ ^ 2) * (4 * A * B) := hscaled
      _ = (4 * A * B) * (((A + B) * μ - A * B) - μ ^ 2) := by ring
      _ ≤ (B - A) ^ 2 * μ ^ 2 := hgap
  rw [show ((B - A) ^ 2 / (4 * A * B)) * μ ^ 2 =
      ((B - A) ^ 2 * μ ^ 2) / (4 * A * B) by field_simp]
  exact (le_div_iff₀ hdenom).mpr hscaled'

end

end EstimatorIntegrity
