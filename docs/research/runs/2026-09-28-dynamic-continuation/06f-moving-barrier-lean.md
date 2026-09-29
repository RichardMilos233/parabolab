# T29: moving-barrier width Lean gate

Date: 2026-09-28. Status: **pass for the fixed analytic target and the
secondary finite moment target**.

The theory prerequisite was the independently passed T30 audit in
`reviews/T30-two-barrier-voting-audit.md` and the fixed contract in
`05f-two-barrier-lean-contract.md`. The path named `frozen-reviews/` in the
dispatch did not exist; the reviewed artifact was present under `reviews/`.
No sampler or numerical code was written in this task.

## Exact formal scope

The primary theorem is formalized for a function `l : ℝ → ℝ` that is
globally continuous and globally monotone, with the hypotheses

```text
∀ t ≥ 0, l t ≤ b
Tendsto l atTop (nhds b)
0 ≤ Δ.
```

This is the explicit global specialization allowed by the fixed contract.
For the intended scalar flow on `[0,∞)`, constant extension by `l 0` on the
negative half-line is continuous and monotone, so it supplies this interface.
The theorem's Lebesgue integral remains over `Ici 0`.

No integrability of `b - l` on `Ici 0` is assumed. No integrability of the
width `l (t + Δ) - l t` is assumed. The proof includes `Δ = 0` directly and
does not divide by `Δ`.

## Checked declarations

The source is `formal/EstimatorIntegrity/MovingBarrierWidth.lean`, SHA-256
`250cca5be42ddbe45ba157fb0cb572ec9460dcaaafefa420e125c2f1da77d11b`.

- `movingBarrier_increment_nonneg` proves
  `0 ≤ l (t + Δ) - l t` from monotonicity and `0 ≤ Δ`.
- `movingBarrier_finite_telescope` proves
  ```text
  ∫ t in 0..T, (l (t + Δ) - l t)
    = ∫ t in T..T+Δ, l t - ∫ t in 0..Δ, l t.
  ```
- `movingBarrier_finite_identity` proves, with
  `J = ∫ t in 0..Δ, (b - l t)`,
  ```text
  ∫ t in 0..T, (l (t + Δ) - l t)
    = J - ∫ t in T..T+Δ, (b - l t).
  ```
- `movingBarrier_remainder_bounds` proves for `T ≥ 0`
  ```text
  0 ≤ ∫ t in T..T+Δ, (b - l t)
    ≤ Δ * (b - l T).
  ```
- `movingBarrier_integrableOn` derives
  ```text
  IntegrableOn (fun t => l (t + Δ) - l t) (Ici 0).
  ```
- `movingBarrier_integral_eq` proves
  ```text
  ∫ t in Ici 0, (l (t + Δ) - l t)
    = ∫ t in 0..Δ, (b - l t).
  ```
- `movingBarrier_width` packages the preceding integrability and equality as
  the primary gate.

The finite telescope uses translation invariance and two adjacent-interval
splittings. The remainder bounds use positivity of `b - l` and monotonicity
of `l`. Nonnegativity of the shifted width identifies its norm integral with
its ordinary integral. The bounded-improper-integral theorem
`integrableOn_Ioi_of_intervalIntegral_norm_bounded` then derives half-line
integrability from the finite identity. Finally, the remainder is squeezed
between zero and `Δ * (b - l T)`, which tends to zero, and
`intervalIntegral_tendsto_integral_Ioi` identifies the total integral with
`J`.

After the complete primary theorem first compiled successfully in
`attempt-06.log`, `positiveInterval_relativeVariance` was added as the sole
secondary result. For `0 < A ≤ B`, `0 < μ`, `A ≤ μ ≤ B`, and

```text
s2 ≤ (A + B) * μ - A * B,
```

it proves

```text
s2 - μ^2 ≤ ((B - A)^2 / (4*A*B)) * μ^2.
```

The proof records positivity of the denominator and uses the audited square
identity. It does not claim that `μ` and `s2` are expectations or establish
an iid RMS statement.

## Verification

The pinned project was used without changing `lean-toolchain`, `lakefile.lean`,
the library entrypoint, or any existing module. The resolved environment was
Lean `4.33.1`, Lake `5.0.0-src+819816b`, and Mathlib commit
`db584cd6d46c92f209a44c0f1c829460d327499d`.

Fresh module build:

```text
cd formal
~/.elan/bin/lake build +EstimatorIntegrity.MovingBarrierWidth
```

Exit status: `0`. The build reported
`Built EstimatorIntegrity.MovingBarrierWidth (106s)` and
`Build completed successfully (3385 jobs)`. The raw log is
`lean/moving-barrier-width/build.log`, SHA-256
`55277b4d8dfb50ca256714613644c12c4c945188a6c4a994cd64afad426892e6`.

The audit file `lean/moving-barrier-width/Axioms.lean` imports the built module
and runs `#print axioms` for all eight exported declarations. Its command
exited `0`. Every declaration depends only on the ordinary Mathlib/Lean
foundational axioms

```text
[propext, Classical.choice, Quot.sound].
```

The raw output is `lean/moving-barrier-width/axioms.log`, SHA-256
`a186294f62b7ff77d2974cadd033c22f7a7fafe2be0d2b4621686adfbc9e1346`.
A source scan for `sorry`, `admit`, `sorryAx`, or an `axiom` declaration
returned `rg` exit status `1`, the expected no-match status; its empty raw log
is `lean/moving-barrier-width/source-scan.log`.

Failed development passes are preserved as `attempt-01.log` through
`attempt-05.log`. They record only Lean elaboration/proof-script corrections:
explicit measure/filter annotations, endpoint normalization, a reversed empty
interval, a typed limit congruence, and the real norm simplification. They did
not require any added hypothesis or weakened conclusion. `attempt-06.log` is
the first clean primary compile. `attempt-07-secondary.log` is the successful
secondary compile before unused interval-bound argument names were prefixed;
the final fresh Lake build contains the cleaned source.

## Correspondence boundary

The formal result certifies the abstract analytic mechanism only. It does not
formalize the scalar ODE existence theorem, convergence of its flow, the
travel-time identity `Δ = ∫_m^M 1/f`, the uniqueness shift
`ell_M(t) = ell_m(t + Δ)`, or the change of variables
`J = ∫_m^M (b-y)/f(y) dy`. Bernstein voting, random-tree construction,
PDE mild correspondence, unbiasedness, and arithmetic/runtime claims also
remain outside this module.
