# Frozen protocol v1: horizon-dependent positive-class sampling

Status: root revision after independent T58 GO and completed05h/T51/T52
formal gates. The reviewed02f draft is preserved unchanged. This version
freezes implementation and bounded preflight settings. Official execution
requires root source/preflight clearance, which has not yet occurred.
No empirical result is asserted. The final section fixes numerical details
and resolves the scope clarifications identified by T58.

## Scientific question and limits

D24 supplies a biased, initial-point-only algorithm with deterministic
query count n=ceil(96 exp(T/2)) in the one-dimensional C1 class. Its
statistical risk layer is now proved in T51/T52. The PDE bias and
interpolation remain conventional. This bounded experiment asks whether
actual point sampling exhibits the predicted rare-event behavior when
positive inputs have mass of order exp(-T), and whether a fixed query
budget loses accuracy as support narrows.

It does not measure a worst-case minimax rate, publication novelty,
end-to-end bit complexity, or a speedup over a PDE solver. The smooth
profiles below depend on T. The tested family is known to the experiment
driver; the estimator receives only an opaque initial-value callable,
public horizon, public sample count and RNG. It must not access a profile
formula, mass, width, shift, or nominal transition parameter.

No empirical result from D26 or the signed D25 class is claimed. No new
unbiased branching representation is implemented. E2 already preserves
its unfavorable deterministic-solver speed comparison; this experiment
must not overwrite or obscure it.

## Conventional theory supporting the reference

Use u_t=u_xx/2+u-u^3 on the normalized unit circle, smooth periodic
0<=v<=1/2, C1,max norm<=1. In04q's polynomial-kernel construction the
constant kernel has B=1, so the height/mass constant C=3/2 is valid and
beta=1/2. For all sufficiently large T, the exact PDE solution obeys

    |S_Tv(x)-Psi(exp(T)*m)|<=1/32,
    Psi(z)=z/sqrt(1+z^2), m=integral v.

The following coarse bounds put every chosen T>=12 inside that theorem:
eta=1/64, L=1, and the small-mass cutoff in04q satisfies m0>=1/504.
Indeed its three entries are 1/2, 1/[72(e^2-1)]>1/504, and
(1/8)e^(-1)/(1+1/64)>1/504. Also kappa>1/4. Therefore

    T* <=1+log(16128)<12.

These inequalities can be checked using 3<pi<4, e<3, e^2<8 and e>8/3;
the latter lower bound follows from the first five terms of exp(1)'s
series. The experiment must not substitute the older E3 T0, which belongs
to a different lower-bound construction.

Thus the exact scalar surrogate is a useful reference with a known
class-uniform PDE bias. For any realized finite list of outputs, the
empirical RMS against the actual PDE target lies in

    [max(0,RMS_surrogate-1/32), RMS_surrogate+1/32].

This deterministic comparison is a consequence of the conventional PDE
proof and the finite Euclidean triangle inequality. It is not an
independently computed PDE solution or a rigorous interval-arithmetic
certificate for floating-point reference values. Report the computed scalar-surrogate statistic and a numerically evaluated
interpretation of this conventional PDE bound separately. The computed
reference and statistics have no certified floating-point enclosure.

## Fixed input family

Let psi(r)=exp(-1/[r(1-r)]) for0<r<1 and zero otherwise, and a=1/8.
Use I=integral_0^1 psi. Reuse the immutable80-digit primary I and100-digit
cross-check from E3's scalar_checks.json; do not rerun or overwrite E3.
Those quadratures agree to about82 decimal places but are not rigorous
enclosures. Their actual values and provenance must be copied into the
new manifest with the source-file hash.

Use horizons T in{12,16,20} and nominal transition levels z in{0,1/4,1,4}.
For z>0, compute sqrt(z/[a I_ref exp(T)]) using the frozen numerical
primary I_ref at100 decimal digits, convert once to binary64, and record
its high-precision construction, decimal value and float.hex(). This is
not a claim of correctly rounding a formula containing the exact integral I.
That stored width h defines the tested mathematical profile:

    r=(x-17/20) mod1,
    v(x)=a*h*psi(r/h).

For z=0 use v=0. The exact shift is17/20; implementation rounding and
floating evaluation are recorded, not silently treated as exact arithmetic.
The driver computes actual surrogate reference mass a*h^2*I from the
stored width, not by assuming its nominal level is attained exactly.

All widths are less than1: I>e^(-9/2)/3 and T>=12 already suffice at z<=4.
The extension is smooth. Its derivative is bounded by

    a*16*exp(-4)<1,

and its height by a*h*exp(-4)<1/2. Hence every ideal profile belongs to the
same fixed class, including zero. The largest support wraps across the
periodic boundary at the chosen shift; retain that case in diagnostics.
The oracle's binary64 evaluation approximates these smooth inputs. Record
underflow-to-zero behavior; no formal real-oracle implementation equivalence
is claimed.

## Prespecified estimators, budgets and repetitions

Every stochastic estimator draws binary64 uniform samples from separate
PCG64 streams as a numerical approximation to iid uniform real sampling, calls the opaque oracle at every drawn point, computes the
actual arithmetic sample mean, and returns Psi(exp(T)*samplemean). Use a
stable hypot-based scalar evaluation. Do not condition on hits, generate
conditional points inside support, replace iid draws by a binomial count,
stop early at a zero observation, or supply the unknown mean.

The five schedules are:

1. growing_0p125: n=ceil((1/8)exp(T/2));128replicates per seed;
2. growing_0p5: n=ceil((1/2)exp(T/2));128replicates per seed;
3. growing_2: n=ceil(2exp(T/2));128replicates per seed;
4. theorem_96: n=ceil(96exp(T/2));8replicates per seed;
5. fixed_51: n=ceil((1/8)exp(12/2))=51 at every T;128replicates per seed.

Only theorem_96 meets the proved class-uniform query budget. The smaller
constants are explicitly empirical comparisons, not new risk theorems.
The theorem schedule uses fewer replications because each run charges
millions of input calls; its uncertainty must remain visible.

Use NumPy Generator(PCG64) with three public seed roots20260928,20260929,
20260930. Derive each horizon/level/schedule/replicate stream by a fixed
SeedSequence spawn_key containing integer indices in the above displayed
orders. Record NumPy/Python versions, exact stream convention and all
before/after states. Different algorithms do not share or reuse queries.
There are180 seed/case/schedule cells and18720 estimator outputs.

Also report the three zero-query constants0,1/2,1 on exactly the same input
cases. All must remain visible, including any case where they outperform
sampling. They receive no profile-specific parameter. An additional
formula-aware reference output is not an admissible zero-query solver for
the opaque-input class and must never be labeled as one.

## Accounting and frozen execution

Before execution, freeze source, protocol, both formal sources/reports,
root correspondence records,04q/T46/T48 and the E3 scalar input file in a
new manifest. Record HEAD, Python/NumPy environment, all seeds, counts,
widths, reference values and expected total point queries. Abort preflight
if any n exceeds3000000 or total queries exceed500000000. These are
resource caps, not instructions to drop cases, lower n or reduce repetitions.
Maximum vector batch size is131072; stream batches to bound memory.

Charge every point in a vector oracle call separately, including repeated
points and all zero-input calls. The algorithm's counter must agree with
its actual oracle observations. Store every replicate's sample mean,
output, positive-return count, actual query count and RNG states. Positive
return count is an observation statistic, not a geometric support oracle.
No raw query coordinates are required in the primary archive, but the
seeds/states/source must permit replay. State honestly whether an auditor
actually replays all queries or only a fixed subset.

Persist each completed seed/case/schedule cell immediately, with output
hashes and pure estimator elapsed time. Separate setup, reference,
diagnostics, serialization and plotting time. Failed cells and exceptions
must retain context and partial files. One official fixed run is intended;
a corrected implementation requires a new version and preserves the old
failure. No selective reruns based on observed error are permitted.

## Preflight and review gates

First review the implementation source against the opaque-call interface,
all five budget formulas, query accounting, separate stream keys, the
stored-width reference formula and preservation of failed cells. Meaningful
bounded diagnostics before official execution must cover zero input,
constant input, actual batching/counts, periodic wrap, representative bump
values against high precision, stable Psi evaluation, and one small seeded
replay. They do not become a surrogate for the official rare-event run.
Numerical tolerances and diagnostic points must be frozen before data.

A separate reviewer must check the protocol before implementation. Root
must then read the source and frozen preflight evidence before explicitly
clearing official execution. This is an internal research-quality gate,
not a new request for user permission.

## Analysis and reporting

For each case and schedule report per-seed and pooled empirical bias,
MSE/RMS and zero-output frequency against the scalar reference, the
conservative PDE RMS interval above, actual queries and elapsed time.
The pooled statistic averages squared errors over all equally sized seed
replications before taking a square root. Do not average RMS values.
Show each schedule's repetition count. Sample variability is descriptive;
no confidence statement or rejection of a universal expectation theorem
follows from a single large realized error.

Plots should show RMS versus T and actual mean query count versus T, with
all zero-query and fixed-budget baselines, and the three nominal nonzero
transition levels separately. Preserve the zero case visibly. Use
standalone scientific figures, labeled axes/units, exact source references
and a scale that retains zero errors. Report negative results directly;
no success threshold authorizes removing a profile or changing a budget.

The official status means implementation/diagnostic/accounting checks ran
as specified, not that every empirical RMS met1/4. Any exceedance is
reported as data. Even a clean result only checks this finite family and
implementation, not the whole class, the asymptotic minimax rate, D26,
or a prize-level contribution.


## Frozen v1 implementation details (T58 closure)

These settings govern the implementation. They do not change the schedules,
class, theory, inputs or replication counts reviewed by T58. Preserve
02f, T58, E3 and every prior failed source/evidence version unchanged.

### Precision, oracle and summation

Use `/opt/miniconda3/envs/parabolab/bin/python`, NumPy binary64 and
mpmath with `mp.dps=100`. Copy E3's primary80-digit integral string and
100-digit Gauss-Legendre string; never rerun quadrature. For each stored
width reconstruct its EXACT real value using `float.as_integer_ratio()`
inside mpmath before computing mass, z_h and Psi(z_h). Compute reference
strings with each frozen I separately; use the primary value in all primary
statistics and record their difference as an empirical precision check.
Use the binary64 rounded reference alongside its100-digit decimal string.
No agreement here is a rigorous enclosure of the exact integral.

The mathematical shift is17/20; implementation shift is binary64 `17.0/20.0`.
Record its hex and exact binary ratio. Oracle evaluation uses NumPy
remainder(x-shift,1), divides by stored h, masks0<r<1 and evaluates
`(h/8)*exp(-1/(r*(1-r)))` only on the mask. The zero member returns zeros
but still records every requested point. Expected underflow is counted
in the diagnostics; do not substitute support knowledge for observations.

Use batches of exactly131072 points except the final remainder. Compute
one `numpy.sum(values,dtype=float64)` per batch; combine the ordered batch
sums by `math.fsum`, and divide ONCE by the exact total n. Every point has
the same weight. Output `(exp(T)*mean)/hypot(1,exp(T)*mean)` with Python
binary64 math. Inputs here keep the product finite. This is a numerical
realization of the ideal algorithm; no exact-real or iid machine bridge
is claimed. Official n values are the T58 integer table, independently
checked against100-digit ceiling evaluation before preflight.

For scalar-surrogate statistics use `math.fsum` for sums of signed errors,
squared errors and pooled squared errors. Bias=mean(output-ref),
MSE=mean((output-ref)^2), RMS=sqrt(MSE), zero frequency=count(output==0)/R.
Pool raw squared errors from all seeds, then take the square root. Retain
all per-seed statistics and R, especially theorem_96's24 pooled outputs.
All numeric PDE-interpretation intervals use plus/minus1/32 and are labeled
uncertified with respect to reference/statistic roundoff. If certified
reference and statistic errors delta_ref,delta_stat were later supplied,
the rigorous interval would enlarge by their sum. No oracle roundoff term
is needed for the deterministic finite-output triangle inequality itself.

### Stream identity, calls and failure records

For each replicate create `Generator(PCG64(SeedSequence(seed_root,
spawn_key=(T_index,z_index,schedule_index,replicate_index))))` with all
indices zero-based and displayed order in the protocol. The three roots
are20260928,20260929,20260930, kept as entropy rather than an extra key.
Record full before/after PCG64 states, NumPy/Python/mpmath versions and
platform. Do not advance official streams for diagnostics. These are
reproducible distinct keys, not a proof of independence or continuous laws.

Keep the estimator API restricted to `(oracle,T,n,rng)`; a fixed public
batch size is allowed. The actual oracle wrapper counts all requested
scalar points before evaluation and separately successful returned values.
The sampler records its observation count and positive-return count.
Complete official records must have all three query/observation counts=n.
On any exception retain attempted count, returned count, partial batch
sums/counts, RNG state, traceback and replicate identity; failed attempted
calls are charged in the activity ledger. Do not treat an absent result
as a zero observation.

Save each completed replicate into its current cell's append-only journal;
flush each record. At cell completion write arrays and metadata via a new
temporary path and atomic rename without overwriting an existing final
cell, then hash them. Save each cell immediately. Existing complete cells
are immutable. An interrupted invocation can resume only after root checks
source/manifest hashes and partial status. Resume from the next NEVER
started replicate; a partial replicate is retained and requires a separate
root decision/new version. Do not silently replay it or replace its loss.
No retries based on empirical error are allowed. New corrected source
means a new version and new manifest; old failures remain visible.

### Predetermined preflight diagnostics

Freeze the source/manifest before these diagnostics. The following work
is permitted without official-run clearance; retain every failed check.
Do not adjust a tolerance after observing a failure in the same version.

1. Nine opaque constant tests: c in{0,1/8,1/2}, n in{1,17,131075}, T=12.
   Each uses a separate diagnostic stream with entropy20260927 and key
   `(0,c_index,n_index)`. Exact counts=n, expected mean=c within1e-15,
   output within2e-15 of100-digit Psi(exp(12)*c), positive count=n for c>0
   and0 for c=0. Calls=393279. This exercises unequal last batches.
2. The actual widest wrapped bump (T=12,z=4), n=131075,T=12, diagnostic
   entropy20260927,key `(1,0)`: execute twice from the same initial state.
   Require bitwise identical mean/output/counts/final RNG state, excluding
   elapsed time. Calls=262150. Both executions must use the real oracle.
3. Each of all12 input cases is evaluated at17 points. Six base points:
   0,nextafter(0,+infinity),nextafter(shift,-infinity),shift,
   nextafter(shift,+infinity),nextafter(1,-infinity). Eleven more:
   binary64 remainder(shift+h*y,1), y in{.001,.01,.1,.25,.5,.75,.9,.99,
   .999,1,1.001}; for h=0 these are repeated shift queries, still charged.
   Calls=204. Compare with100-digit formula evaluated at the exact binary
   ratios of x,h and implemented shift, with absolute tolerance1e-14 plus
   relative tolerance1e-11. This comparison checks floating evaluation of
   the implemented shift; the exact17/20 profile has the same integral.
   Store every test point/value/reference, including endpoints, underflow
   and points on both sides of the periodic seam. Confirm0<h<1 for every
   nonzero width and h>3/20 for the widest case.
4. Pure scalar Psi checks at z={0,1e-300,1e-12,.25,1,4,1e100,1e300},
   absolute tolerance2e-15 against100-digit evaluation of the EXACT
   binary64 z. No oracle calls. Stored-width primary/cross-check surrogate
   references must agree within1e-14 (empirical, not an enclosure).
5. Independently check fixed180cells,18720outputs and336883488 official
   calls, maxn2114541. Schema/source/hash checks do not call the oracle.

One successful preflight executes655633 point calls. Count failed versions
separately; no rerun is implicit in this number. Additional empirical tests
require a versioned root decision and resource accounting.

### Total budget and audit replay

The500000000-point cap covers the WHOLE activity: official calls,
preflight, failed attempts and any replay. Each official replicate has
n<=3000000. The one intended official run uses336883488 calls. A later
independent auditor is assigned exactly replicate_index=0 of each of all
180cells, with30075636 additional calls, using archived initial RNG states
and frozen source. Require bitwise mean/output/positive-count/count/RNG
agreement in the recorded environment. Do not describe this as full replay.
Summing this subset, one preflight and one official run gives367614757
calls, leaving132385243 calls of failure/revision headroom. All remaining
stored statistics and hashes may be recomputed without oracle calls.
A whole-run replay would exceed the cap and is not authorized.

### Versioned outputs and clearance

Implementation: new `numerics/positive_query_sampling.py` only, with
producer evidence under `artifacts/positive-query-sampling/v1/` and
`reviews/T63-positive-sampling-implementation.md`. Expected phases:
`prepare` (manifest/config), `preflight` (bounded diagnostics), and
`run` (official, only after root clearance). The manifest precedes all
preflight/official observations and records every frozen source and chosen
numerical setting. Phase commands must not overwrite existing evidence.
A source revision must use a new artifact version. Plots/independent replay
are separate later tasks, not included in this producer's authorization.

The root reads the full source and all preflight failures/results before
clearing `run`. This is an internal correspondence gate, not a request for
user permission. The user's continuing research authorization covers the
bounded work. No expected-error threshold selects successful cells.
