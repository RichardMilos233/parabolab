import Mathlib.Data.Finset.Card
import Mathlib.Data.Real.Basic

/-!
# Finite adaptive exact-value oracle transcripts

This module gives an operational, fuel-bounded evaluator for a deterministic
adaptive point-query policy and proves its transcript-coupling property.
Fixing any private random seed selects one such deterministic policy.

The policy receives a reverse-chronological history: the most recent queried
point and exact oracle value are stored at the head.  A successful evaluator
run returns its newly queried points in chronological order.  A policy may
stop even when no fuel remains; asking for a query at zero fuel fails.

The evaluator is finite for every supplied fuel.  This file does not encode
measurability, almost-sure halting, a uniform query bound, a PDE, heat-kernel
estimates, smooth bumps, or a bridge from arbitrary randomized algorithms.
-/

namespace EstimatorIntegrity

/-- The next action selected by a deterministic point-query policy. -/
inductive OracleAction (X : Type*) where
  | stop (output : ℝ)
  | query (point : X)

/-- A reverse-chronological list of queried points and their exact values. -/
abbrev OracleHistory (X : Type*) := List (X × ℝ)

/-- Run a deterministic adaptive exact-value oracle policy for at most `fuel`
queries.  A successful result contains the output and the chronological list
of newly queried points. -/
def runOracle {X : Type*}
    (policy : OracleHistory X → OracleAction X) (oracle : X → ℝ)
    (history : OracleHistory X) : Nat → Option (ℝ × List X)
  | 0 =>
      match policy history with
      | .stop output => some (output, [])
      | .query _ => none
  | fuel + 1 =>
      match policy history with
      | .stop output => some (output, [])
      | .query point =>
          match runOracle policy oracle ((point, oracle point) :: history) fuel with
          | none => none
          | some (output, trace) => some (output, point :: trace)

/-- Observed-transcript congruence.  Agreement with the baseline oracle at
every point in the successful baseline trace forces the second run to return
the same output and the same ordered trace. -/
theorem runOracle_congr_of_eq_on_trace {X : Type*}
    (policy : OracleHistory X → OracleAction X) (f g : X → ℝ) :
    ∀ (fuel : Nat) (history : OracleHistory X) (output : ℝ) (trace : List X),
      runOracle policy f history fuel = some (output, trace) →
      (∀ point ∈ trace, g point = f point) →
      runOracle policy g history fuel = some (output, trace) := by
  intro fuel
  induction fuel with
  | zero =>
      intro history output trace hrun hagree
      cases haction : policy history with
      | stop value => simpa [runOracle, haction] using hrun
      | query point => simp [runOracle, haction] at hrun
  | succ fuel ih =>
      intro history output trace hrun hagree
      cases haction : policy history with
      | stop value => simpa [runOracle, haction] using hrun
      | query point =>
          simp only [runOracle, haction] at hrun ⊢
          cases heval : runOracle policy f ((point, f point) :: history) fuel with
          | none => simp [heval] at hrun
          | some result =>
            rcases result with ⟨tailOutput, tailTrace⟩
            simp only [heval] at hrun
            simp only [Option.some.injEq, Prod.mk.injEq] at hrun
            have htail : ∀ x ∈ tailTrace, g x = f x := by
              intro x hx
              have hxtrace : x ∈ trace := hrun.2 ▸ List.mem_cons_of_mem point hx
              exact hagree x hxtrace
            have hpoint_mem : point ∈ trace := hrun.2 ▸ List.mem_cons_self
            have hpoint : g point = f point := hagree point hpoint_mem
            have hrecursive :=
              ih ((point, f point) :: history) tailOutput tailTrace heval htail
            rw [hpoint, hrecursive]
            simpa only [Option.some.injEq, Prod.mk.injEq] using hrun

/-- If the two oracles agree outside a forbidden set and the successful
baseline trace avoids that set, then output and ordered trace are unchanged. -/
theorem runOracle_noHit {X : Type*}
    (policy : OracleHistory X → OracleAction X) (f g : X → ℝ)
    (forbidden : Set X) (fuel : Nat) (history : OracleHistory X)
    (output : ℝ) (trace : List X)
    (hrun : runOracle policy f history fuel = some (output, trace))
    (hagree : ∀ point, point ∉ forbidden → g point = f point)
    (havoid : ∀ point ∈ trace, point ∉ forbidden) :
    runOracle policy g history fuel = some (output, trace) := by
  apply runOracle_congr_of_eq_on_trace policy f g fuel history output trace hrun
  intro point hpoint
  exact hagree point (havoid point hpoint)

/-- The query count recorded by a successful or failed evaluator result. -/
def oracleQueryCount {X : Type*} : Option (ℝ × List X) → Option Nat :=
  Option.map fun result => result.2.length

/-- The no-hit coupling also preserves the query count, as it preserves the
entire successful result. -/
theorem runOracle_noHit_queryCount {X : Type*}
    (policy : OracleHistory X → OracleAction X) (f g : X → ℝ)
    (forbidden : Set X) (fuel : Nat) (history : OracleHistory X)
    (output : ℝ) (trace : List X)
    (hrun : runOracle policy f history fuel = some (output, trace))
    (hagree : ∀ point, point ∉ forbidden → g point = f point)
    (havoid : ∀ point ∈ trace, point ∉ forbidden) :
    oracleQueryCount (runOracle policy f history fuel) =
      oracleQueryCount (runOracle policy g history fuel) := by
  rw [hrun,
    runOracle_noHit policy f g forbidden fuel history output trace hrun hagree havoid]

/-- The finite set of cell labels visited by a trace. -/
def visitedCellLabels {X C : Type*} [DecidableEq C]
    (cell : X → C) (trace : List X) : Finset C :=
  (trace.map cell).toFinset

/-- A finite trace visits no more distinct cell labels than it has queries. -/
theorem visitedCellLabels_card_le_trace_length {X C : Type*} [DecidableEq C]
    (cell : X → C) (trace : List X) :
    (visitedCellLabels cell trace).card ≤ trace.length := by
  change (trace.map cell).toFinset.card ≤ trace.length
  simpa using (trace.map cell).toFinset_card_le

end EstimatorIntegrity
