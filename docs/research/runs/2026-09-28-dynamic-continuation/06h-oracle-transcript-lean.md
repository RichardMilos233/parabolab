# T43: deterministic adaptive oracle transcript in Lean

Status: **scoped formal PASS**.  The new module implements the requested
fuel-bounded evaluator and proves observed-trace congruence by induction through
that evaluator.  It also proves the no-hit and distinct-cell-count corollaries.
This is the finite transcript component of the conventional query lower-bound
argument.  It is not a formal proof of the PDE lower bound or a novelty claim.

## Encoded model

The source is `formal/EstimatorIntegrity/OracleTranscript.lean` and is independent
of the unfinished query-information module.

- `OracleAction X` is either `stop output` or `query point`.
- `OracleHistory X = List (X × ℝ)` is explicitly reverse chronological: a new
  exact response `(point, oracle point)` is added at the head.
- `runOracle policy oracle history fuel` returns
  `Option (ℝ × List X)`.  On success, the list is the ordered chronological
  trace of queries made after the supplied initial history.
- The policy is evaluated even at fuel zero.  It may stop successfully there;
  a requested query at fuel zero returns `none`.
- At positive fuel, a query consumes one unit, records the exact oracle value,
  and recursively evaluates the resulting policy state.

Fixing one private random seed can select one deterministic `policy`.  Random
seeds and measurability are not fields hidden inside this deterministic object.

## Formal results

`runOracle_congr_of_eq_on_trace` quantifies over every natural-number fuel,
initial history, output, and trace.  If the baseline `f` run returns
`some (output, trace)` and `g point = f point` at every baseline trace point,
then the `g` run returns exactly the same output and ordered trace.

The proof is genuine induction on fuel.  In the query branch, the baseline
recursive evaluator result is exposed by an equation case split.  The successful
outer trace identifies the current query as its head and the recursive trace as
its tail.  Agreement at the head makes the next histories identical; the
induction hypothesis transfers the recursive run.  The stop branch is identical
because policy and history are shared.  The proof does not assume transcript,
stopping-decision, or output equality.

`runOracle_noHit` derives the intended coupling.  If `f` and `g` agree outside
`forbidden` and every point of the baseline trace avoids `forbidden`, the entire
successful result is unchanged.  `runOracle_noHit_queryCount` records explicitly
that the two result-derived query counts are equal.  Two alternative oracles,
such as the positive and negative hidden-bump inputs, are obtained by applying
`runOracle_noHit` separately to each alternative against the same baseline run.

For any cell label type with decidable equality and any map `cell : X → C`,
`visitedCellLabels_card_le_trace_length` proves

```text
card ((trace.map cell).toFinset) ≤ trace.length.
```

This covers a finite cell-label codomain and is slightly more general: finiteness
of the observed label set follows from the finite trace itself.

## Assumptions and coverage boundary

The theorem is pointwise and deterministic after a seed is fixed.  It is stated
for every supplied fuel and therefore does not impose one global uniform query
cap across seeds.  A conventional almost-sure-halting algorithm can have a
different finite halting length on each nonexceptional seed; selecting that fuel
is outside this module.

The following bridges remain conventional and are not claimed here: the encoding
of arbitrary measurable randomized algorithms into seed-indexed policies,
measurable integration of runs with unbounded seed-dependent stopping lengths,
simultaneous removal of exceptional null sets, the paired-loss expectation
inequality, and the complete oracle-complexity theorem.  The module also does not
formalize Allen--Cahn or any other PDE, heat minorization, nonlinear comparison,
smooth periodic bumps, derivative scaling, hard-input membership, or exponential
rate algebra.  No numerical experiment was added for this formal gate.

## Verification

The protected project files actually pin Lean and Mathlib `v4.33.0`, despite the
task dispatch mentioning `4.33.1`.  They were not modified.  The verified active
environment was:

```text
$ ~/.elan/bin/elan show
active toolchain: leanprover/lean4:v4.33.0
  (overridden by formal/lean-toolchain)

$ ~/.elan/bin/lake env lean --version
Lean (version 4.33.0, arm64-apple-darwin24.6.0,
      commit d8b18978322de05a8f3dba51ef03cf5461676c17, Release)

$ ~/.elan/bin/lake --version
Lake version 5.0.0-src+d8b1897 (Lean version 4.33.0)

$ git -C formal/.lake/packages/mathlib rev-parse HEAD
db584cd6d46c92f209a44c0f1c829460d327499d

$ git -C formal/.lake/packages/mathlib describe --tags --exact-match HEAD
master-2026-08-10
```

The manifest input revision is Mathlib `v4.33.0`.  The fresh module build was:

```text
$ cd formal
$ ~/.elan/bin/lake build EstimatorIntegrity.OracleTranscript
✔ [825/825] Built EstimatorIntegrity.OracleTranscript (7.3s)
Build completed successfully (825 jobs).
```

The source scan command

```text
rg -n '\b(sorry|admit|axiom|opaque)\b' \
  formal/EstimatorIntegrity/OracleTranscript.lean
```

returned no matches.  The axiom harness prints every authored exported
declaration and the two action constructors.  Each uses either no axioms or
only Mathlib's standard `[propext, Classical.choice, Quot.sound]`; there is no
custom axiom.

SHA-256 values for the exact verified artifacts are:

```text
997b4af24aeee366a170b6632969431d2bf5fc1e47dc440ecb00ead19d81c53c  formal/EstimatorIntegrity/OracleTranscript.lean
7a3644ab172b227aae9bdb457c912c530c2b79483fdbb1e01a405059b78a80ed  docs/research/runs/2026-09-28-dynamic-continuation/lean/oracle-transcript/build.log
51a0dacb8347a524e5d5a9c8bc00e53fa7cddbb87b7aebc6373abfe08ad9cadc  docs/research/runs/2026-09-28-dynamic-continuation/lean/oracle-transcript/axioms.log
813918bab25e08053b484b3479ca0618200d04f1a228c090370bcf42dd14c050  docs/research/runs/2026-09-28-dynamic-continuation/lean/oracle-transcript/source-scan.log
97c501ad054ff3ccbb564911ae772e234d595b564196d75708fc04b3b4a6cd42  docs/research/runs/2026-09-28-dynamic-continuation/lean/oracle-transcript/OracleTranscriptAxioms.lean
```

All failed compiler attempts and their exact fixes are retained in
`lean/oracle-transcript/attempt-01.log` through `attempt-08.log` and summarized
in `lean/oracle-transcript/development.log`.  Final build, source-scan, and axiom
outputs are preserved beside them.
