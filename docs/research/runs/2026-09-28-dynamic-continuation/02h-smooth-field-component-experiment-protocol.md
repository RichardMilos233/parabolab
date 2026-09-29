# E5 fixed protocol: actual smooth-field sampler component

Date: 2026-09-29. Status: **design frozen before implementation; no run**.
This protocol follows accepted conventional D43/D44 and specifies a later
code check of their actual sampler. Implementation/execution waits for root
acceptance of fixed05m/T89 and fixed05n/T93. Those Lean modules are finite
probability/statistics bridges; the full tree/PDE correspondence remains
conventional. E5 is not a long-horizon PDE performance experiment and must
not replace that outstanding objective.

## Question and fixed mathematical references

Check whether a finite implementation of the new field sampler reproduces
known PDE derivatives, correctly preserves the joint spatial law, and exhibits
the predicted averaging behavior without a Fourier-coordinate independence
assumption. Also measure actual tree preparation and output costs. A failed
component check prevents treating this sampler as a validated component of
a future long-T implementation.

Use the unit one-dimensional torus, u_t=(kappa/2)u_xx+u-u^D, with
D=3 or 5. Only accepted D43/D44 representations are used:

- D=3: B=3, lambda=2, M(y)=(sum y_i-product y_i)/2.
- D=5: B=5, lambda=5, M(y)=(6/25)sum y_i-(1/5)product y_i.

The quintic rule has the accepted corner values
(-1,-23/25,-1/25,1/25,23/25,1). Its diagonal satisfies
5(M(z,...,z)-z)=z-z^5. No result pending in T94 is used.

The known base g(x)=a is constant. The oracle is v(x)=a+delta e(x),
delta=1/10, with e(x)=cos(2*pi*x) or e(x)=1. The sampler receives a
known g evaluator and only an opaque scalar v evaluator; it does not receive
the unknown test profile's formula or reference derivative. Each invocation
of that v evaluator increments the charged counter, even for duplicate points
and constant profiles. Reference evaluation is separate and is not presented
as a competing zero-query algorithm.

Let m=D-1, c_tau=exp(m*tau)-1 and

    phi_tau(a)=a exp(tau) [1+c_tau a^m]^(-1/m).
    phi'_tau(a)=exp(tau) [1+c_tau a^m]^(-1-1/m).
    phi''_tau(a)=-(m+1)exp(tau)c_tau a^(m-1)
                                      [1+c_tau a^m]^(-2-1/m).

These follow by solving the scalar ODE and ordinary differentiation. For
a constant base, the first variational PDE has spatially constant potential
f'(phi_t(a)); separation of variables therefore gives the exact reference

    D S_tau(a)[delta cos(2*pi*x)]
      =delta phi'_tau(a) exp(-2*pi^2*kappa*tau) cos(2*pi*x).

Constant directions remain constant under the PDE. The order-two reference
is delta^2 phi''_tau(a). For D=3, a=0, the order-three constant-direction
reference is -3 delta^3 exp(tau)(exp(2*tau)-1), obtained by the cubic Taylor
coefficient of phi_tau. These are conventional analytic references, evaluated
numerically at high precision for comparison; their floating conversions are
not certified interval bounds.

## Twelve fixed cells and no adaptive selection

For each of kappa in {1/100,1/10}, use the following six configurations:

1. D=3, tau=1/2, a=0, j=1, e=cos(2*pi*x).
2. D=3, tau=1/2, a=1/4, j=1, e=cos(2*pi*x).
3. D=3, tau=1/2, a=1/4, j=2, e=1.
4. D=3, tau=1/2, a=0, j=3, e=1.
5. D=5, tau=1/10, a=1/4, j=1, e=cos(2*pi*x).
6. D=5, tau=1/10, a=1/4, j=2, e=1.

The expected leaf population is exp(2) in both reaction settings. Their
probabilities of at least one split are 1-exp(-1) and 1-exp(-1/2), respectively.
These fixed burn-in choices do not claim that tau itself has been extended.
Only the a=0 cosine input changes sign; do not label the whole suite a
full-signed-class or minimax test.

Use three fixed seeds 2026092901, 2026092902, 2026092903, with an explicitly
specified reproducible substream mapping by seed and cell. Generate 4096
independent field samples for every seed/cell. Report every cell, including
all zero samples when n<j and all unfavorable results. No parameter or seed
may be selected after inspecting output.

Use NumPy PCG64DXSM with SeedSequence([seed,cell_index,sample_index,tag]),
zero-based cell indices ordered first by the displayed kappa list and then
by the six configurations. Fix tag=0 for official sampling, 1 for preflight;
replay restores the original tag=0 stream. Freeze the NumPy version before
execution. This is a reproducible pseudorandom binary64 implementation,
not a literal implementation of exact real-valued random primitives.

For averaging, partition each 4096-sample sequence into nonoverlapping
consecutive batches of sizes M in {1,4,16,64,256}. Batch families for different
M and different cutoffs share data; they are not independent comparisons.

## Actual algorithm and finite outputs

Generate the whole rate-lambda B-ary clock tree up to tau before acquiring
unknown values. Use independent edge Gaussians of variance kappa ell_e.
Compute the guarded inverse-variance recursion a_v and the root common
component by postorder/preorder passes. Subtract that actual component from
all leaf sums. Use the resulting residual law and damping variance kappa a
together, as in D44. Never damp unmodified leaf samples.

For a positive harmonic sum, the algebraically equivalent stable formula
h=min(a_c)/(sum min(a_c)/a_c) is allowed; zero children must use the exact
stated zero guard. Numerical stabilization must not alter the sampling law.

Choose uniform torus U and a uniform ordered j-tuple of distinct leaves.
Compute the actual selected mixed partial C_I of the complete leaf polynomial
by its signed 2^j corner formula; compare against a separate recursive
multiaffine derivative calculation in deterministic fixtures. Cache known g
values; query v only at the j selected locations, and form

    z=(n)_j C_I product_b [v(U+Z_(I_b))-g(U+Z_(I_b))].

For n<j return zero with no acquisition. Values are reduced modulo one.
Output the real array through N=64:

    constant=z,
    cosine_nu=2z exp(-2*pi^2*kappa*a*nu^2) cos(2*pi*nu*U),
    sine_nu=2z exp(-2*pi^2*kappa*a*nu^2) sin(2*pi*nu*U).

The cutoffs N in {4,16,64} are exact nested prefixes of this same output.
No new oracle calls are made when changing cutoff. Do not clip an individual
sample, replace outliers, truncate weights, or enforce artificial frequency
independence. Store the full array and enough tree/random-stream identifiers
to replay the prespecified audit samples.

## Preflight and execution limits

Before official sampling, deterministic fixtures must cover one leaf,
a common-ancestor star, an unbalanced finite tree, zero terminal edges,
and the n<j case. Independently form small dense C matrices and verify the
recursion's weights, Cw=a1, residual covariance, a in [tau/n,tau], and
the real Fourier coefficient signs against their explicit formulas.
These are floating checks with stated tolerances, not formal matrix proofs.

A separate small Gaussian simulation may diagnose conditional joint
covariance/independence; it must not be described as proving independence.
Every Gaussian draw and node is included in work counters. Preflight may
make at most 8192 v calls in total, including failed preflight versions.

The official hard oracle cap is 245760: sum the prescribed j over all
12 cells, three seeds and 4096 samples. Actual calls can be smaller through
n<j returns. Prespecified replay covers sample indices 0 through 7 in each
seed/cell, with at most 864 additional oracle calls. All E5 activity, including
debugging and failed attempts, has a hard cap of **300000 v calls**. No extra
acquisition is permitted after that cap. E4's frozen counter and budget are
separate and must not be rewritten.

Use a safety limit of 100000 segments in one tree, 10000000 total generated
segments, 30 minutes for the official suite, and a finite-value check on every
output. Hitting any limit is an explicit incomplete/failed run, not a sample
returning zero. Save the attempted prefix and counters, abort the official
suite, and do not silently redraw or exclude the offending tree. No unbiased
full-suite claim may be made for such an incomplete run.

## Prespecified analysis

For every cell/seed, preserve raw coefficient arrays, node/leaf counts,
common variance, tuple/sample metadata, per-output oracle counts, generation
time, known-evaluator calls and cutoff-output time. Separate original-value
calls from work; finite Gaussian randomness and arithmetic are not free in
the measured runtime report.

Use the actual H^2 norm of the real array:

    ||c||^2 = c0^2 + (1/2) sum_(nu=1)^N (1+nu^2)^2
                                      (c_cos,nu^2+c_sin,nu^2).

The analytic reference has only the constant mode or cosine mode one, so it
belongs to every chosen cutoff. For each M,N report empirical mean coefficient
error, empirical squared Hilbert error of batch means, M times that error,
sample Hilbert second moments, and descriptive uncertainty across the three
fixed seeds. Compare realized per-cell means to the analytic reference and
report standardized discrepancies where the empirical variance is nonzero.
These diagnostics do not constitute confidence certificates of unbiasedness.

Check exact nested-prefix equality, realized <=j query cap, all counts,
seed reproducibility, coefficient sign conventions, and every completed
planned output. An independent auditor must read raw arrays, recompute the
norms/statistics, and replay the fixed indices. Preserve failures and zero
samples. Use standard scientific plots with units and full cell labels;
do not alter the prior E1–E4 figures or evidence.

## Interpretation and remaining long-time objective

Passing E5 would validate a bounded numerical implementation of the fixed-time
field sampler against these analytic derivatives. It would not establish
the universal Hilbert moment bound, the minimax query theorem, practical
long-T advantage, a certified spatial PDE reference, finite-bit guarantees,
or the generalized odd-power/fractional long-time theorems.

The subsequent actual long-T signed experiment still needs its own fixed
protocol, a paid known-base reconstruction and continuation implementation,
independent spatial PDE reference/refinement checks, all-query accounting,
and competitive deterministic baselines. No such implementation or result
is asserted by this document.
