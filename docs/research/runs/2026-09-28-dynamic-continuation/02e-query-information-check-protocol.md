# Fixed protocol: query-information implementation checks

Status: proposed for independent review after the T42/T43 formal gates passed.
This is a small deterministic correspondence check, not a PDE experiment,
an empirical proof of an oracle lower bound, or evidence of novelty. The
universal argument is in 04o/T40/T41 and its precisely scoped formal parts
are in 06g/06h. No sampling benchmark or new error target is selected here.

## Prerequisites and freeze

Before implementation, root must accept an independent review of this exact
protocol. Before the first official execution, record SHA-256 values of this
protocol, the review, 04o, 05g, 06g, 06h, both Lean source files, and every new
implementation source, plus Python and package versions. Use the actual
protected project toolchain, Lean v4.33.0. Do not edit protected originals,
formal sources or previous experiment inputs. Preserve unsuccessful runs
and fixes under distinct versioned paths. No selected reruns or changed
scientific parameters after seeing results.

New implementation ownership will be limited to numerics/query_information_checks.py
and artifacts/query-information/checks-v1/, plus its delivery report. Root
will inspect implementation-to-protocol correspondence before clearing the
official run. Use /opt/miniconda3/envs/parabolab/bin/python. No random generator
is required; all finite seeds below are enumerated exactly.

## A. Exact finite oracle model

Use Python Fraction for oracle responses, outputs, probabilities, squared
losses and costs. Cells are i=0,...,K-1, with K in {1,2,3,4,6}. The public
baseline is g(i)=i/(K+1). Alternative f_(j,sigma) equals g except that its
response in cell j is g(j)+sigma, with sigma in {-1,+1}. Its assigned target
is sigma/2; the baseline assigned target is zero. These assigned targets
define an abstract information problem. They are not numerically evaluated
Allen–Cahn values, and this policy is not a PDE solver.

A seed consists of a permutation of all K cells. For every permutation,
every query cap m=0,...,K, and every miss output h in {-1,-1/2,0,1/2,1}, run
an actual adaptive evaluator. It queries cells in the seed order until it
sees a nonzero difference from the public baseline, then returns sigma/2;
otherwise it stops after m queries and returns h. Record the actual ordered
query trace and output of every run on the baseline and 2K alternatives.
The policy/evaluator receives only the oracle callable and public baseline,
permutation, cap and miss output; it must never receive the hidden j/sigma
label or the assigned target. The driver may use those labels only to build
oracles and score completed runs. The implementation may stream these exact
records into per-configuration aggregates, but must not replace execution
by the closed-form risk formula.

Verify for each executed no-hit alternative that the output and ordered
trace equal the baseline run, and that distinct visited cells do not exceed
the baseline query count. Check the finite paired-loss inequality directly
from executed losses for every seed/m/h configuration. Average all seeds
with the exact uniform permutation weight; preserve all 105 K/m/h summary
rows, including positive and negative input risks and baseline risk.

For every summary row compare the observed alternative-family mean loss to

    (1-m/K)*(h*h+1/4).

Compare it with the lower bound (1/4)*(1-m/K), with exact equality when h=0.
For each fixed alternative, also compare its permutation-averaged risk to
(1-m/K)*(h-sigma/2)^2. All differences must be exactly zero for equalities,
and all directly evaluated lower-bound slacks must be nonnegative.

Separately, for each K enumerate a randomized budget that chooses m=0 with
probability 1/4 and m=K with probability 3/4, independently of the uniform
permutation, always using h=0. Reuse the already executed m=0 and m=K, h=0
records from the main sweep; do not execute an additional simulation. Derive
its five summary rows by exact weighted aggregation of those records.
Verify baseline expected cost=3K/4, baseline risk=0, and every alternative
risk=1/16. This proves sharpness only for this finite abstract information
lemma; it is not a matching upper bound for the PDE function class.

Keep exhaustive record counts, exact summary numerators/denominators,
maximum equality discrepancies and minimum inequality slacks. There are no
statistical confidence intervals or probabilistic test thresholds here.
The fixed sweep has 25,960 seed/m/h configurations, 334,020 total oracle
runs including the baselines, and 154,030 no-hit alternative runs. These
counts must be checked; the reused budget mixture adds zero oracle runs.

## B. Scalar amplification and bump parameters

Use the one-dimensional, s=1 bump

    psi(z)=exp(-1/[z*(1-z)]) for 0<z<1, and zero otherwise.

Its conventional derivative certificate is analytic: with r=1/[z(1-z)]>=4,
|psi'|<=r^2 exp(-r)<=16 exp(-4)<1 and psi<=exp(-4)<1. Thus D=1 is a
valid bound; no grid sample is used to certify a derivative supremum.
Use a=1/8, q=2, D_s=2*pi, kappa=exp(-1/8)/sqrt(2*pi), and
delta=kappa/[32*e*4*D_s], exactly as specialized from 04o.

Compute I=integral_0^1 psi at 80 decimal digits by tanh-sinh quadrature and
independently at 100 digits by Gauss-Legendre quadrature, each split at 1/2.
The two values must agree to absolute tolerance 1e-70. This is a numerical
convergence check, not a rigorous enclosure. Use the 80-digit value for the
primary rows, and retain both precision results and their difference.

For each k in {4,8,16,32}, prescribe

    T=1+log((k+1/2)^2/(kappa*a*I)),
    mu=a*I/k^2, c=kappa*mu,
    B=c*exp(T-1),
    ell=c*exp(T-1)/sqrt(1+c^2*(exp(2*(T-1))-1)),
    background=delta*mu*exp(T).

Check the independently rearranged identities B=(k+1/2)^2/k^2 and
ell=B/sqrt(1+B^2-c^2) to combined tolerance 1e-70*(1+|target|).
Check R=exp((log(kappa*a*I)+T-1)/2) is within that tolerance of k+1/2,
so its floor is k; check T>=T0 from 04o, 1<=B<=4, 0<c<1,
ell>=1/sqrt(2), background<=1/32, and ell-background>1/2.
Preserve every prescribed row with at least 75 significant digits.

This block checks the implemented scalar and scaling formulas. Heat
minorization, comparison for the spatial PDE, smooth periodic extension,
and the universal input-class quantifiers remain conventional mathematics;
none is inferred from these four rows. No PDE discretization is performed.

## Delivery and decision rule

Produce a machine-readable manifest, complete exact finite summary, complete
four-row high-precision table, check result, elapsed time, and plain-text run
log. All equalities, inequalities and quadrature comparisons above must
pass. Stop and preserve the full failure context on a mismatch. A later fix
requires a separately recorded version and cannot overwrite a failed run.

The report must keep the finite-model sharpness separate from PDE minimax
optimality, and the scalar checks separate from PDE validation. No plot is
necessary for these small tables. Continued research on matching PDE upper
bounds proceeds independently and must first pass mathematical review.
