# T06 — Final theory, formalization and implementation correspondence review

Date: 27 September 2026. Independent research audit. This review changes no
theory, implementation or Lean file. It follows the earlier independent T01
conventional-theory review and additionally inspects the actual saved sources,
formal evidence, tests and production records.

**Verdict: pass within the stated scope.** The specialized local sampler
implements the raw six-code law used in C3/C4. The continuation driver
implements the genuinely learned, explicitly biased projection scheme in C6.
The saved Lean module proves the algebraic statements described in
`06-formalization.md`; it does not formalize C1 or the stochastic/PDE bridges.
The primary experiment records agree with their retained raw samples. No
blocking mismatch was found. This is a bounded one-dimensional stationary
benchmark, not a generic derivative-closure theorem, a fully formalized solver,
or a novelty claim for continuation.

## Sources and verification boundary

Reviewed sources:

- `numerics/slab_sampler.py`, SHA-256
  `994e892784f36930fa63649aa749985448df75887f9096f6c40c142b46ff108a`.
- `numerics/run_experiment.py`, SHA-256
  `12621c9269a62b08c7017c5adc55401d4d3818b8e4663b106ca176eb2b4e0d05`.
- Both numerical test files, the claim ledger, fixed protocol, T01/T02
  theory notes, and `06-formalization.md`.
- `formal/EstimatorIntegrity/SlabContinuation.lean`, SHA-256
  `d9f214c6c7b89b5e571f47f8c7f91125d7940dedb0834aed3cb198105acfb229`,
  its imported `allenCahnBranchPolynomial`, and the saved build/axiom logs.

The current numerical-source hashes match those in the production
provenance. The current Lean-source hash matches the successful build log.
The recorded environment is Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1 and
mpmath 1.3.0 on arm64 macOS. The test log records **29 passed in 18.98 s**.
This audit inspected those tests and independently recomputed production
statistics; it did not rerun the same test suite or rebuild Lean redundantly.

## C3/C4: actual local estimator

The implementation's code order is `(Id,Dx,F0,F1,F2,F3)`. Its terminal factors
are exactly `g`, `g'`, `g−g³`, `1−3g²`, `−6g`, and `−6`. Exponential draws use
NumPy scale `0.5`, hence rate 2. A surviving leaf moves by a Brownian increment
with variance equal to its remaining time and receives `exp(2·remaining)`.
It does not move over the unused exponential lifetime.

The normalized branch map is:

| Parent / raw label | Children | Multiplier at lifetime `τ` |
|---|---|---|
| `Id` | `F0` | `exp(2τ)/2` |
| `Dx` | `F1,Dx` | `exp(2τ)/2` |
| `Fk`, label 0 | `F0,F(k+1)` | `exp(2τ)` |
| `Fk`, label 1 | `Dx,Dx,F(k+2)` | `−exp(2τ)/2` |

The last multiplier moves the scalar `−1/2` from the child code into the
parent product. This is valid scalar normalization because the raw label
probabilities and clock law are scalar independent. It does not alter the
signed or squared functional. Squaring and first-event averaging produce
exactly the polynomial `G` in C3, including `2ae` in the `F2` row.

Every `F` branch draws a uniform binary label **before** structural-zero
handling. `F3` has two zero labels; the second label of `F2` is zero. Their
selected samples return zero. The live `F2` label retains its original
probability `1/2` and weight. A constant `F3` particle that survives to the
horizon still receives its survival weight. There is no tuple-probability
renormalization or terminal-dependent approximate pruning.

A parent draws one Brownian death position; all its children receive that
same position through array repetition. Subsequent child randomness is fresh.
The generation frames are unwound in their original contiguous child order,
so each parent multiplies exactly its own child values. Tree generation has
no depth or node cutoff. The saved node counts measure nodes actually visited
under the disclosed selected-zero optimization, not a fully generated zero
subtree that the implementation did not visit.

The tests supply scripted leaf/branch weights, a negative scalar branch, the
live/dead `F2` labels, shared birth positions, all six terminal polynomials,
and fixed-seed distribution comparisons with the existing scalar sampler.
The distribution checks are diagnostics with empirical uncertainty; their
passing does not prove a population moment bound. The C4 bound remains the
conventional Volterra/nonexplosion/representation argument plus the formal
rational witness.

The sampler itself checks finite values and the local horizon, but cannot
certify a global C¹ envelope from sampled leaves. The actual driver supplies
that missing contract structurally, as checked next.

## C5/C6: learned boundaries, projection and statistics

`stage_terminal` uses the exact Jacobi input only at stage 1. Every later
stage receives a copied, read-only coefficient vector through
`polynomial_terminal`. That callback evaluates the same three-sine function
and its analytic derivative at all leaves. The previous vector is frozen for
the entire stage. The guarded-oracle test executes this actual driver path
and fails on a late exact-input callback. Calls to the exact reference for
error assessment do not feed the fitted coefficients back into the solver.

Each stage draws the prescribed fresh uniform spatial roots and estimates
`mean(H sqrt(2) sin(nωX))`, for `n=1,3,5`. It uses the normalized spatial
measure `dx/L`. One tree may contribute to all three coordinates; their
covariance is retained and no false independence between coordinates is
assumed. The observed coefficient covariance is the sample covariance of
these three observations divided by the root count. It is an empirical
diagnostic, not a substitute for the conditional variance theorem.

Only the coefficient estimates are clipped, into the prescribed symmetric
box. Tree values remain intact. The clipped vector becomes the next actual
terminal input. The code records raw and projected coefficients, clipping
mask and distortion. This matches the proof that projection cannot increase
error relative to the true projected target inside the box. It does **not**
make the clipped estimates unbiased. The hard coefficient caps imply the
global value/derivative envelope needed by C4 on every stage outcome; the
driver additionally records and checks their deterministic bounds.

The reported per-run error is the retained coefficient error plus the known
Fourier tail, with an independent periodic-grid cross-check. The reference
coefficients and tail are evaluated by high-precision mpmath; the field names
containing `exact` refer to the analytical formula, not exact machine
arithmetic or interval evaluation. Numerical stationarity and quadrature
checks support the implementation, while the analytical tail bound remains
the proof input.

The procedure finishes every started tree. A wall-clock stop may occur between
batches; incomplete stages are archived as incomplete and cannot create a
coefficient estimate. Nonfinite roots cause failure rather than being removed
from an average. Such a failure is not converted into a successful run. The
observed primary production records contain no such failure or partial stage.

## Exact scope of the checked Lean result

The saved successful module build and axiom audit cover eleven declarations:
the weak/strict six-coordinate postfixed inequalities; scalar interval-clamp
contraction; an abstract finite scalar error recurrence; the cap sum and
frequency-weighted sum; rational squared value/derivative envelope checks;
the rational stability-exponent bound; finite amplification; and the final
rational MSE budget. The imported definition of `G` agrees with the raw
weights above. The source hash and named declarations match the saved logs.
The axiom output contains only `propext`, `Classical.choice`, and `Quot.sound`.

This scope excludes:

- C1 finite-product perturbation and geometric leaf absorption. They are
  conventional proofs in this run, **not formalized** by this module.
- C2 marked-moment differential identities and C9 infinite-moment comparison.
- Random-tree construction, nonexplosion, conditional independence, moment
  identification, the Volterra comparison and PDE-mean correspondence.
- Elliptic identities, Fourier-tail estimates, PDE energy/Poincaré stability,
  conditional Monte Carlo variance, and correctness of NumPy/SciPy evaluation.

The scalar recurrence theorem takes its one-step inequality as a hypothesis;
it does not establish that stochastic inequality. Similarly, the rational
box check does not by itself prove the stochastic moment theorem. These
boundaries are explicit in `06-formalization.md`. No end-to-end formal
verification claim is supported or needed for the bounded study.

## Production evidence and independent archive check

The reference run records all eight high-precision checks passing. The primary
slab manifest records the fixed three seeds, 50 stages per seed, 200,000 roots
per stage and horizon 4. All runs completed.

| Seed | Completed roots | Visited nodes | Final normalized spatial L² error |
|---|---:|---:|---:|
| 2026092701 | 10,000,000 | 11,798,512 | 0.00195049135 |
| 2026092702 | 10,000,000 | 11,796,012 | 0.00163539237 |
| 2026092703 | 10,000,000 | 11,797,713 | 0.00068853254 |

T06 independently read **all 150 raw archives, covering 30,000,000 roots**.
For every archive, its hash, completion flag, root cardinality, finite values,
root range, node and branch totals, terminal-code counts, raw coefficient
estimate, clipped vector, terminal-source label and admissibility checks agree
with the manifest. Recomputing the raw coefficients and the reported Fourier
error gave zero difference at the working floating precision. Covariances
were independently recomputed for stages 1, 2 and 50 of each seed. Aggregate
cost totals agree with the per-stage archives.

Clipping counts over the 150 stages were `(0,0,142)` for modes `(1,3,5)`;
projection was materially used, not an inactive implementation detail.
The largest grid-versus-Fourier error discrepancy was below `5.4e−18`.
The largest observed stage second moment was approximately `0.05998`; this is
an observed diagnostic and is not the reason the population moment bound is
accepted.

The primary manifest's run time is approximately 27.01 seconds for all three
seeds, or 8.82–9.07 seconds per seed, on the recorded host. These timers
include stage sampling, statistics and archives, but exclude the initial
high-precision `compute_reference` setup. Sampling-only times are a different
field. Neither should be described as the complete research/setup cost.

The majority comparator is reviewed at source level: rate-2 ternary branching,
common child birth position, complete trees, terminal values in `[-1,1]`, and
the bounded recursion `(a+b+c−abc)/2` match the specified separate
representation. It applies the same coefficient observations and projection.
All six prescribed comparator runs also completed. T06 independently checked
all six archives, covering 48,000 roots, against their hashes and recomputed
coefficients, projected errors, covariances, node/branch counts and terminal
counts. Every check matched. All retained majority outputs lie in `[-1,1]`.

| Seed | Horizon | Roots | Visited nodes | Normalized spatial L² error |
|---|---:|---:|---:|---:|
| 2026092711 | 0.8 | 8,000 | 291,710 | 0.00631531860 |
| 2026092711 | 2.0 | 8,000 | 34,825,778 | 0.00460446454 |
| 2026092712 | 0.8 | 8,000 | 288,353 | 0.00401599268 |
| 2026092712 | 2.0 | 8,000 | 35,030,042 | 0.00685837592 |
| 2026092713 | 0.8 | 8,000 | 288,512 | 0.00307787241 |
| 2026092713 | 2.0 | 8,000 | 35,202,698 | 0.00433564012 |

The comparator manifest records approximately 18.99 seconds after reference
setup for all six entries. Its actual sampling times are 0.149–0.160 seconds
at horizon 0.8 and 6.02–6.24 seconds at horizon 2. The run at horizon 4 was
not executed; any work quoted there is theoretical expected node work.

The optional sensitivity manifest was also inspected: seed 2026092799 used
50,000 roots per stage, completed all 50 stages, and reports final error
0.00684704965 after 2,500,000 roots and 2,949,388 visited nodes. This is a
single empirical sensitivity run. Its reduced sample count does not satisfy
the primary C7 200,000-per-stage budget, and its smaller observed error than
0.02 must not be described as a proved reduced-budget RMS guarantee. The
full raw-archive recomputation above covers the primary and majority runs;
this sensitivity paragraph reports the inspected manifest only.

## Allowed conclusion

The bounded study supports a learned short-slab feasibility result for this
specific nonconstant periodic stationary datum, with a conventional
ideal-real-arithmetic normalized spatial RMS guarantee, checked supporting
Lean algebra, and reproducible measured runs. The raw rate-2 unsplit L²
obstruction is a separately proved same-datum comparison. It does not follow
from finite samples and does not imply an all-rate or all-representation
obstruction.

Three observed errors below 0.02 do not independently establish a population
RMS or high-probability theorem. The ten-million-root budget does not give a
pointwise/sup-norm 0.02 certificate. Floating arithmetic and special-function
error have numerical checks but no rigorous accumulated error budget. The
stationary target, odd finite-dimensional interface and preset coefficient
box are substantive restrictions. Preset unequal comparator budgets and
theoretical unexecuted work at horizon 4 do not establish an optimized
equal-accuracy speedup. Continuation, projection and bounded-majority methods
have prior literature; no new general-method novelty is asserted.
