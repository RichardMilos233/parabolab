# Prespecified dynamic continuation experiment

Written after the conventional two-dimensional proof and before its Lean gate
or any new numerical implementation. This is one bounded validation unit in
the active, open-ended research goal; finishing it will not finish that goal.

## Questions and honest comparators

1. Does the actual two-coefficient producer remain feasible at every stage and
   follow a genuinely changing solution without an intermediate solution oracle?
2. How do measured errors and complete-tree work behave from T=0.08 to T=16?
3. Is the method useful on this particular benchmark compared with returning
   the known equilibrium g, the fixed midpoint .95g, the initial datum, and a deterministic
   spectral computation? A poor comparison is a result to retain.

The mathematical statement is an ensemble normalized-spatial RMS bound below
0.02 at every grid endpoint, with N=100000 per slab. Three realizations cannot
certify this expectation, estimate rare tails reliably, or establish an
all-times confidence event. Floating-point computations and the deterministic
reference have no rigorous rounding/discretization enclosure.

## Frozen mathematical contract

- PDE: u_t=u_xx/2+u-u^3, period L=4 K(1/20)/sqrt(40/21), using the
  parameter convention for the elliptic integral and Jacobi functions.
- g=sqrt(2/21) sn(sqrt(40/21)x | 1/20); initial datum u0=0.9 g.
- h=0.08, 200 stages, T=16. Fixed seeds 2026092801, 2026092802, 2026092803.
- N=100000 fresh independent uniform spatial roots and full local raw trees
  per stage; common rate 2, original unrenormalized two-label probabilities.
- Reuse the unchanged prior `slab_sampler.py` by explicit path and SHA-256.
  Preserve its full-tree/no-cutoff semantics. No clipping, rejection, retries
  based on outputs, or optional stopping within a started tree.
- b0=g(1-g^2/a), b1=g^3/a, a=2/21. Compute the normalized Gram matrix G.
  Estimate the two moments from the same root/tree observations, solve Gc=bhat,
  then project in the G metric into .9<=c0,c1<=1,
  |c1-c0|<=2/735. Check the unconstrained point and all six closed edges.
- Initialize c=(.9,.9). Every later terminal is the preceding stored pair;
  its derivative is g' [c0+3(c1-c0)g^2/a]. The fixed basis g is allowed at
  every stage. No exact evolving u(t) is allowed in the producer.

## Ordering and acceptance

First finish and review the conventional proof. Then compile the relevant
finite Lean module, save its build and axiom evidence, and identify everything
outside formal scope. Only after that gate may numerical code be implemented
and run. Implementation workers must return mathematical discrepancies to the
researcher instead of changing the theorem, sampling law, or success criterion.

Required checks before the primary runs:

- Compare G at independent quadrature resolutions and with high-precision
  quadrature; positive definiteness and condition number must be recorded.
- Compare the polygon minimizer with an independent constrained optimization
  implementation on fixed inside/outside cases. Check its variational
  inequality and idempotence; ordinary coordinate clipping is not equivalent.
- Compare the analytic terminal derivative with an independent numerical
  derivative at representative coefficients. Feasibility's global guarantee
  comes from the proof, not a grid test.
- Check coefficient-to-function normalization and initial exact representation.
- Verify sampler source hash and the existing sampler's relevant tests. A
  source-level or runtime audit must confirm no reference solver is reachable
  from the production terminal callback.

## Independent reference

Use a deterministic odd-sine Galerkin ODE for the original PDE, with normalized
basis sqrt(2) sin(k omega x), retaining positive odd frequencies. The nonlinear
term is integrated on a periodic uniform grid sufficiently large that cubic
products of retained modes are integrated exactly in ideal arithmetic. Solve
with SciPy DOP853 at tight tolerances. Compare at least max odd modes 15, 31,
and 63 and two temporal tolerances. Also check the stationary g residual and
u_t(0)=(.9-.9^3)g^3 independently. Record initialization truncation, solver
success, elapsed time and maximum differences over all 201 grid endpoints.
Use the finest successful solution only as a numerical reference, with an
empirical reference uncertainty floor. A failed convergence check blocks
numerical accuracy headlines but not feasibility or cost reporting.

## Data and reporting

Checkpoint every completed stage to a compressed archive containing all root
positions, unmodified tree values, node counts, root-branch flags, aggregate
terminal-code counts, prior coefficients, raw moments, unconstrained estimate,
projected coefficients, RNG provenance, timings and source hashes. Do not
overwrite an existing run. Preserve partial/failed records and account for
every started/completed root. Batch size is an implementation/storage detail,
not a statistical stopping rule.

Report all 200 stages and selected endpoints 0.08, 0.4, 1.04, 2, 4, 8, 16;
1.04 is the nearest grid endpoint after 1 and is not relabelled as T=1.
Report each seed's error, the three-seed empirical RMS, mean and spread,
coefficient trajectories, projection frequency, second-moment diagnostics and
total roots/nodes/wall time. Compare equilibrium g, fixed .95g, and fixed .9g
at the same endpoints. The deterministic reference is also a performance baseline; include
its setup and solve costs and do not claim that MC wins on this one-dimensional
smooth known-equilibrium problem.

Primary budget is exactly 60 million roots across three runs. A two-hour
per-run safety cap is checked only at stage/batch boundaries after finishing
started trees; an interrupted run remains incomplete and cannot replace the
prespecified primary run. Existing research artifacts are read-only. Hash all
new artifacts and verify the initial 342 protected files remain unchanged.

## Pre-data midpoint-baseline addendum

During the conventional theory stage, before numerical implementation or any
primary data, the fixed midpoint .95g was found to satisfy the deterministic
uniform bound ||u(t)-.95g||₂<=||g||₂/20<1/60<.02 from the order band alone.
It is therefore a required baseline. This reveals that the concrete .02
continuation certificate is already dominated by prior range knowledge.
Keep all primary budgets and seeds unchanged; do not retune them to hide
this limitation. The experiment remains a mechanism/correspondence and actual
error study, not a demonstration that the .02 guarantee is competitively useful.

## Stronger theory is separate

Bernstein and analytically regular polynomial hierarchies may yield dimension
and accuracy statements beyond the degree-one experiment. They receive their
own assumptions and conventional proofs. This primary experiment does not
implement or validate a high-degree SOS projection, arbitrary dimension,
arbitrary nonlinear reaction, total-arithmetic complexity, or global optimality.
