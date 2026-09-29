# Draft protocol: horizon-dependent positive-class sampling

Status: root design after both fixed05h gates and root correspondence PASS.
This is not frozen, independently accepted, implemented, or executed.
No experiment may be inferred from these proposed settings. A research
review must accept the scope, counts and reference accounting before a
coding worker is dispatched. Preserve this draft if a revised protocol is
needed; retain every implementation failure and official run thereafter.

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

These inequalities can be checked using pi<4, e<3, e^2<8 and e>8/3;
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
certificate for floating-point reference values. Report the exact scalar
surrogate statistic and this conservative PDE interpretation separately.

## Fixed input family

Let psi(r)=exp(-1/[r(1-r)]) for0<r<1 and zero otherwise, and a=1/8.
Use I=integral_0^1 psi. Reuse the immutable80-digit primary I and100-digit
cross-check from E3's scalar_checks.json; do not rerun or overwrite E3.
Those quadratures agree to about82 decimal places but are not rigorous
enclosures. Their actual values and provenance must be copied into the
new manifest with the source-file hash.

Use horizons T in{12,16,20} and nominal transition levels z in{0,1/4,1,4}.
For z>0, compute the binary64 width once by rounding
sqrt(z/[a I exp(T)]) and record both its decimal value and float.hex().
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

Every stochastic estimator draws iid uniform binary64 points using the
specified PRNG, calls the opaque oracle at every drawn point, computes the
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
all five budget formulas, query accounting, stream independence, the
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
