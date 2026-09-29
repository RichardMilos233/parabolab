# Fixed two-barrier sampler experiment

Status: frozen before any corresponding sampler/reference code or data.
T29's fresh analytic Lean build passed; T34's bounded conditional-pass
clarifications are incorporated below. This studies the reviewed ideal method's floating
approximation; it is not a full finite-bit unbiasedness certificate.
The burn-in/factory candidate04n is excluded from this experiment.

## Scientific question and frozen primary cases

Does the explicit two-barrier mixed voting construction remain numerically
usable as physical T grows, for a smooth nonconstant datum whose small
equilibrium defect is measured relatively? Retain strong deterministic and
zero-query comparisons; do not infer speedup from small expected tree size.

Use u_t=u_xx/2+u-u^3 on the one-dimensional2pi torus, with

    v(x)=5/8+(1/8)cos(x),   m=1/2, M=3/4,
    query x in {0, pi/2, pi},
    T in {0, 1/4, 1, 4, 16, 64, 256},
    primary seeds {2026092831, 2026092832, 2026092833},
    N=10000 independent roots per(seed,T,x) cell.

There are63 cells and630000 primary roots. Use a fixed SeedSequence/PCG64
mapping keyed by seed, horizon index and query index, with independent cells.
Record the exact mapping and initial/final RNG states. No selected reruns,
adaptive sample size or parameter choice after observed errors.

Use numpy SeedSequence(entropy=seed, spawn_key=key), then PCG64. Indices are
zero-based in the listed order. Keys are(0,T_index,x_index) for primaries,
(1,T_index) for clock diagnostics in their three-horizon list,(2,0) for the
nonendpoint constant, and(3,endpoint_index,T_index) for endpoint diagnostics.
Use binary64. Uniforms are Generator.random draws in[0,1), with an exact zero
redrawn before using the open-interval inverse; record any such redraws
separately from limiting-clock trials. Record environment and all source/gate
hashes in an immutable execution manifest before any diagnostic execution.

The ideal relative-variance bound100/189 gives per-cell ensemble relative
RMS <=sqrt((100/189)/10000)<0.01. The empirical three-seed RMS is only a
diagnostic of three realizations. The data and space are deliberately smooth
and one-dimensional; there is no empirical arbitrary-measurable-data or
high-dimensional efficiency claim.

For strict reference D_ref and seed-specific mean Wbar_j, report each signed
relative error e_j=(Wbar_j-D_ref)/D_ref and RMS_3=sqrt(sum_j e_j^2/3), separately
at every(T,x), plus within-root dispersion. The1% ensemble target is not a
guarantee on every realized error or on the floating implementation.

## Specified stochastic mechanism and output scale

Use04l/T30's binary-OR/ternary-majority mixture and04m/T31's limiting-clock
proposal, accepting a leaf or event s<T and rejecting events s>=T. Do not
compute the finite-horizon clock through z(T) rounded to one. Rejected
proposals generate no children or spatial increments. All children have
fresh independent descendant randomness and the same branch location.

Use the stable d=(1-U)(1+zeta)/(1+zeta-U/2) form in the event inverse.
At accepted nodes Brownian increments have variance T-s; at leaves variance
T. Evaluate the periodic cosine oracle after reducing the spatial argument.
Leaves return(v-m)/(M-m); OR/majority vertices return their bounded
multiaffine values. Use an explicit evaluation stack if necessary; no
node/depth truncation may be silently substituted for a completed root.

The primary output is W=exp(2T)(1-u(T,x)) estimated through the bounded
scaled-defect return R_M*Z+R_m*(1-Z) from04m. Never form it by subtracting
the computed u from one. Report the physical defect with its scale/exponent;
the relative error is calculated from scaled values. Keep the coefficient-
limit-underflow estimate separate from all other floating errors. T<=256
also keeps the physical exp(-2T) scale representable in binary64.

For every root retain W, normalized Z, total visited nodes, leaves, binary
and ternary internal counts, total clock proposals and rejections. Assert
the pathwise counting identities and numerical range with a recorded1e-12
rounding tolerance; no silent clipping. Save per-cell raw NPZ, metadata,
source/gate hashes and RNG states. Failures remain in the record.

## Independent deterministic reference

A separate implementation must solve the scaled PDE directly:

    w=exp(2t)(1-u),
    w_t=w_xx/2+3exp(-2t)w^2-exp(-4t)w^3,
    w(0,x)=3/8-(1/8)cos(x).

Use an even Fourier/cosine Galerkin method with maximum modes16,32,64 and
quadrature grids128,256,512 respectively. The8-to-1 grid/mode ratio avoids
cubic aliasing into retained modes. Solve each with SciPy Radau and the
analytic projected Jacobian for both(rtol,atol) pairs(1e-10,1e-12) and
(1e-12,1e-14), producing six resolution/tolerance refinement runs of one
method, not six independent error certificates. Keep
all solver diagnostics and timings. Compare all prescribed times/queries;
require maximum discrepancy from the64-mode strict run <1e-8 in scaled
values. This is empirical reference convergence, not a rigorous enclosure.

Modes mean0 through K inclusive; quadrature nodes are2*pi*j/J, j=0..J-1.
The constant coefficient is the grid mean, and positive cosine coefficients
are twice the corresponding cosine-weighted mean. Each run solves once from
0 to256 with evaluation at all fixed horizons; no selected restarts.

Validate projection and its analytic Jacobian against independently written
complex-Fourier convolution, using at each K the all-nonzero vector
c_0=3/8, c_k=(-1)^k/(8*(k+1)^2), k=1..K, at t=0,1/4,4. Require max absolute
nonlinear-projection and Jacobian-entry discrepancies <=1e-10. Check constant
initial profiles1/2,5/8,3/4 against independently evaluated scalar solutions
at all fixed horizons, with max scaled discrepancy <=1e-8. Freeze these
cases and their manifest before evaluation. Diagnostic closed forms must
not import the sampler's clock/barrier helpers. The stochastic producer must not import
this reference or use evolving reference values as leaf data. AtT=0 the
explicit initial function is the exact reference.

## Comparators and interpretation

Compare relative defect error at the same points/times against:

1. The harmonic center2 r_m r_M/(r_m+r_M), requiring no spatial queries once
   the phase bounds are known; use its scaled equivalent for evaluation.
2. The scalar ODE solution initialized at the known spatial mean5/8. This
   simple problem-specific comparator uses more data than just range bounds;
   no universal pointwise certificate is attributed to it.
3. The independent deterministic solver, with matching timing scope and
   reference-resolution qualifications. This one-dimensional solver may be
   substantially faster; retain that result if observed. Predesignate the
   16-mode loose-tolerance run as comparator, provided it passes the same
   discrepancy gate. Compare one solve plus all21 query evaluations with
   each seed's total21-query sampling time. Keep six-run validation costs
   separate. This is a fixed-implementation comparison, not equal-accuracy
   optimization or evidence of general solver superiority.

The theoretical mean-node upper bound25sqrt(6)/16-1 and clock-trial bound
(15/8) times that constant are expected-value bounds, not per-sample caps or
automatic acceptance thresholds for every empirical mean. Report empirical
means, maxima and dispersion without claiming successful samples prove tail
bounds. AtT=0 the sampler and reference use the exact initial datum; the
harmonic-center and mean-ODE baselines need not equal its point values.

## Validation, safeguards and preserved outputs

Before primary execution, check range/count invariants and remaining-time
direction. Fix the following separate diagnostics, excluded from primary
totals, and record their RNG mapping before running them:

- Seed2026092891,100000 accepted finite-horizon clock outcomes after the
  rejection loop at each T in{1/4,1,4}. Preserve leaf/event indicators,
  accepted times, and proposal/rejection counts. Compare the
  empirical CDF (leaf represented at0) at s/T in{0,1/4,1/2,3/4,1} with
  exp(Lambda(s)-Lambda(T)). Use the predetermined discrepancy threshold
  sqrt(log(2/1e-6)/(2*100000)); this is a DKW-derived diagnostic threshold,
  not proof that floating draws have the exact law. Preserve all three sets.
- Seed2026092892,100000 roots for the nonendpoint constant v=5/8 at T=4,
  x=0. Compare its scaled mean with the exact scalar-ODE value using the
  predetermined absolute threshold(5/4)*sqrt(log(2/1e-6)/(2*100000)),
  derived from the width of the global scaled-output interval. It is an
  empirical check, not a floating-bias certificate.
- Seed2026092893,128 roots for each endpoint constant v=m and v=M at every
  fixed horizon, query x=0. Each completed scaled return must match its corresponding
  scalar value within1e-12. These are pathwise identity diagnostics.

The four statistical diagnostics have ideal union false-alarm bound <=4e-6;
1e-6 is per diagnostic. Failed deterministic preflight, reference convergence,
or prescribed diagnostics stop primary execution and preserve the failed
record. A versioned resolution is required; do not change seeds, thresholds,
sample sizes or scientific cases to obtain a pass.

AtT=0 return Z=(v(x)-m)/(M-m), W=1-v(x), nodes=leaves=1, binary=ternary=0,
and zero clock proposals/rejections. For positiveT each visited node uses the
clock; total proposals equal rejections plus visited nodes. Keep this
documented shortcut distinct in the raw counts. No post-outcome tuning.

The full fixed workload is731792 PDE roots including diagnostics, plus
300000 standalone accepted clocks; proposal trials are a separate count.

Allow120 seconds of monotonic elapsed sampling time per primary cell as an
operational safeguard, excluding processing/I/O. Check the deadline within
root evaluation as well as between roots; save completed roots in append-only
checkpoint chunks of at most1000, flush the completed in-memory prefix on
interruption, and mark any interrupted current root unfinished. This is an
incomplete-cell safeguard, never a substituted truncated output. If a cell
does not complete, preserve all completed roots and mark the cell incomplete;
do not report it as an N-root primary estimate or draw selected replacements.
Any implementation correction after observed failure must be versioned and
its affected evidence declared stale before a new run.

Use new numerics/two_barrier_sampler.py, a fixed driver, independent reference
module, tests, and a separate artifacts/two-barrier/ subtree. The independent
reference owns artifacts/two-barrier/reference-v1/: its reference.npz has
times shape(7,), queries shape(3,), scaled_values shape(7,3) from the strict
run; reference_summary.json reports all gates, refinements and timings, with
all six coefficient/query arrays retained separately. The stochastic producer
owns sampler-v1/ and may read this frozen reference only for execution gates
and post-sampling comparisons; its mathematical sampler must not import it. Do not alter
the existing dynamic/slab/critical-frontier code or raw data. Record Python,
library/platform versions, code and formal/theory gate hashes, commands,
random states, all cells including failures, and timing split into preflight,
sampling, per-cell processing and total run. Refuse final-artifact overwrite.

Scientific figures should separate scaled-defect values, relative errors and
node/trial diagnostics. Every curve must identify the fixed datum, number of
seeds/roots and finite queried horizons; theoretical horizontal bounds and
empirical quantities need distinct labels. No all-horizon numerical proof,
floating unbiasedness certificate, novelty, or unmeasured speedup claim.
