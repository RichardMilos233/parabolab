# T02 — a constructive continuation interface and its limits

Status: conventional theory review, 27 September 2026. No numerical experiment,
Lean declaration, implementation, or timing measurement was run for this note.
The work follows the user’s theory → Lean → code order. The raw-tree local
moment certificate quoted below is an input supplied by the root researcher
and requires its separate T01 review; the interface analysis does not replace
that certificate.

## Decision

A concrete, non-NN learned continuation is possible for a deliberately narrow
Allen–Cahn benchmark while retaining the existing derivative-coded local
sampler. Use three orthonormal sine coefficients, estimated from fresh random
spatial locations and local raw trees, followed by coordinatewise clipping
into a fixed admissible coefficient box. This projection is biased, but its
effect on the error is controlled. A small-amplitude, periodic, stationary
Jacobi-elliptic solution supplies an exact nonconstant reference and an
analytic Fourier-tail bound.

The favorable bound is for ensemble RMS in normalized spatial L2. It is not a
pointwise 0.02 certificate. It relies on a preserved mean-zero symmetry, the
specific target’s tiny omitted Fourier tail, and the separately established
local moment bound. It is not an arbitrary-jet result or a general moving
interface benchmark.

The originally proposed piecewise-linear grid method remains a valid
function-value method only for a different monomial or majority
representation. Its elementary sup-norm Monte Carlo budget is much worse.
It should not replace the raw-tree route silently.

## 1. PDE, normalization, and semigroup bounds

Write forward elapsed time as s and let S_s be the solution map for

    u_s = (1/2) u_xx + u − u³,       x in R/(L Z).

Normalize the spatial norm by

    ||v||₂² = (1/L) integral_0^L |v(x)|² dx.

All functions used here are smooth and periodic. Bounded classical/mild
solution existence, uniqueness, regularization, integration by parts and
Poincaré’s inequality are analytical inputs, not newly formalized facts.

For any two solutions, w = u − v satisfies

    (1/2) d/ds ||w||₂²
      = −(1/2)||w_x||₂² + ||w||₂²
        − (1/L) integral w² (u² + uv + v²).

Since u² + uv + v² is nonnegative, the usual bounds are

    ||S_h a − S_h b||₂ ≤ exp(h) ||a − b||₂,
    ||S_h a − S_h b||∞ ≤ exp(h) ||a − b||∞.

The second follows equivalently from the one-sided bound f'(z) ≤ 1.

If a and b are odd and satisfy a(x+L/2) = −a(x), and similarly for b,
uniqueness preserves these symmetries because the reaction is odd. Their
difference has zero mean. With omega = 2 pi/L, Poincaré gives the stronger
bound

    ||S_h a − S_h b||₂² ≤ exp(2 gamma h) ||a − b||₂²,
    gamma = 1 − omega²/2.                                      (1)

No derivative-accuracy estimate enters (1). Derivative bounds are needed
separately to make the local raw estimator admissible.

## 2. Exact periodic nonconstant reference

Use the Jacobi parameter m = 1/20 and modulus k = sqrt(m). The notation
K(k) below uses the modulus, whereas scipy.special.ellipk and ellipj use
the parameter m. Confusing these changes the PDE reference.

Set

    K = K(1/sqrt(20)),        kappa = sqrt(40/21),
    A = sqrt(2/21),           L = 4 K/kappa,
    omega = pi kappa/(2 K),
    g(x) = A sn(kappa x, k).

The Jacobi differential equation is
sn'' = −(1+k²) sn + 2 k² sn³, so direct substitution gives

    (1/2)g'' + g − g³ = 0.

Thus u(s,x) = g(x) at every time. The period is L; g is odd and changes sign
under a half-period shift. Its global input envelopes are

    ||g||∞ = sqrt(2/21) < 2/5,
    ||g'||∞ = A kappa = sqrt(80)/21 < 1/2.                       (2)

The defining differential identities are in
[NIST DLMF 22.13](https://dlmf.nist.gov/22.13#E13). The reference is not the
whole-line tanh wave in library.py; no periodic truncation of that wave is
being assumed.

### 2.1 Explicit period and stability bounds

The positive series

    K(k) = (pi/2) sum_{n≥0} a_n m^n,
    a_n = ((1/2)_n/n!)²

has a_0 = 1, a_1 = 1/4, and a_n ≤ 1/4 for n ≥ 1. Consequently

    pi/2 ≤ K ≤ (pi/2)(1 + m/(4(1−m))) = 77 pi/152.             (3)

This uses the exact series from
[NIST DLMF 19.5.1](https://dlmf.nist.gov/19.5#E1), not a floating special
function evaluation. Hence

    (76/77) sqrt(40/21) ≤ omega ≤ sqrt(40/21),
    gamma ≤ 1 − (20/21)(76/77)²
          = 8989/124509 < 3/40.                                (4)

In particular gamma is bounded near 0.072, not 0.025. The latter would
understate the error propagation for m = 1/20.

### 2.2 Analytic nome bound

Let K' = K(sqrt(19/20)) and q = exp(−pi K'/K). The complementary elliptic
series is convergent; its terms are positive here. Keeping its first two
terms yields

    K' ≥ C + (C−1)/80,       C = log(8 sqrt(5)) = (1/2)log(320).

The series and its constants d(0) = 2 log 2 and d(1) = 2 log 2 − 1 are
given in [NIST DLMF 19.12.1–3](https://dlmf.nist.gov/19.12#E1).
Positivity also follows from d(n) = 2 integral_0^1 t^(2n)/(1+t) dt > 0.
Together with (3),

    −log q ≥ (1539/1540) log 320 − 19/770 > log 300.             (5)

The last comparison has an elementary rational proof:

    (1539/1540)log320 − 19/770 − log300
      = log(16/15) − log320/1540 − 19/770
      ≥ 1/16 − 47/1540 > 0.

Here log(1+x) ≥ x/(1+x), and log320 < log(2^9) ≤ 9. Thus

    0 < q < 1/300.                                              (6)

No computed decimal approximation to q is needed.

### 2.3 Three coefficients and omitted tail

Let e_n(x) = sqrt(2) sin(n omega x). These are orthonormal in the normalized
spatial L2 norm. The exact Fourier series is

    g = sum_{r≥0} c_{2r+1} e_{2r+1},
    c_{2r+1} = D q^(r+1/2)/(1−q^(2r+1)),
    D = 2 pi/(K sqrt(21/20)) ≤ 4 sqrt(20/21).

This follows from the sine expansion in
[NIST DLMF 22.11.1](https://dlmf.nist.gov/22.11#E1), with q and the spatial
argument normalized as in [DLMF 22.2](https://dlmf.nist.gov/22.2#E1).

For the first coefficient,

    c_1² ≤ 96000/1877421 < (23/100)².

Since c_{2r+1} ≤ c_1 q^r, it follows that

    0 < c_1 < 0.23,
    0 < c_3 < 0.23/300 < 0.003,
    0 < c_5 < 0.23/300² < 0.00005.                              (7)

Let P be the orthogonal projection onto
V = span{e_1, e_3, e_5}. For the omitted tail,

    delta² := ||g − Pg||₂²
      ≤ (320/21) q^7 / ((1−q)² (1−q²))
      ≤ 320 / (21 * 300³ * 299² * 89999)
      < 10^(−16).                                              (8)

The first denominator bound is deliberately loose but sufficient. A
supremum bound is also available from the positive coefficient series:

    delta_inf := ||g−Pg||∞
      ≤ sqrt(2) D q^(7/2)/(1−q)² < 1.5 * 10^(−8).              (9)

These estimates depend on an exact analytic reference family. No finite
sample agreement is being used to establish stationarity or the tail.

## 3. Admissible box and the local raw estimator

For c = (c_1,c_3,c_5), define the closed coordinate box

    B = [−.23,.23] × [−.003,.003] × [−.00005,.00005].

Let R be coordinatewise clipping onto B, and let v_c = sum c_n e_n.
For every c in B,

    ||v_c||∞ ≤ sqrt(2)(.23+.003+.00005)
               = sqrt(2) * .23305 < .4,
    ||v_c'||∞ ≤ sqrt(2) omega (.23+3*.003+5*.00005)
               ≤ sqrt(80/21) * .23925 < .5.                    (10)

All interfaces are smooth, odd and anti-periodic, and no derivative of a
sampled value is substituted for an unbiased derivative estimate. Their
derivatives are the exact derivatives of the stored sine polynomial.
Equation (7) places the true target coefficient vector inside B.

The local theorem supplied by the root researcher is to be cited separately:
for the original uniform-tuple derivative-coded Allen–Cahn sampler, rate 2,
h ≤ .08 and every smooth terminal v satisfying |v| ≤ .4, |v'| ≤ .5,

    E[H_h(v,x)] = S_h v(x),
    E[H_h(v,x)²] ≤ M = 1/4 uniformly in x.                     (11)

Its proposed proof uses the six normalized codes
(Id,Dx1,F0,F1,F2,F3), terminal envelope
(.4,.5,.4,1,2.4,6), inflation 1.05, and a positive Volterra supersolution
(.25,.5,.5,3,12,50). The correctness and integrability bridge of that input
are not independently re-proved here. All results below are conditional on
(11) until its review is complete.

## 4. Actual learned algorithm and conditional error proof

Use v_0 = g, the known problem input. For slab j, condition on the sigma
field F_{j−1} of every previous draw and stored coefficient vector. Draw
N_j iid pairs consisting of X_i uniform on [0,L) and a fresh complete local
raw tree H_i with terminal v_{j−1}, duration h_j and root X_i. All trees
and root locations are fresh conditional on F_{j−1}. Define

    Z_{j,n} = (1/N_j) sum_i H_i e_n(X_i),       n in {1,3,5},
    c_j = R(Z_j),
    v_j = sum_n c_{j,n} e_n.                                  (12)

The same local tree may supply all three products H_i e_n(X_i).
Coefficients within a vector need not be independent. Trees indexed by i
must be conditionally independent. Within each tree the three offspring,
where present, share one parent death position and have independent future
randomness, as required by the existing mechanism.

Write mu_j for the coefficients of P S_{h_j} v_{j−1}. Then

    E[Z_j | F_{j−1}] = mu_j,
    E[||Z_j−mu_j||² | F_{j−1}] ≤ 3M/N_j.                     (13)

For each component, the second-moment bound is M times the integral of
e_n², which is one. Summing variances proves (13); it does not require the
pointwise sum of the three e_n² to be constant.

Let c* be the coefficient vector of Pg. Since c* belongs to B,
coordinatewise clipping gives ||R(z)−c*||² ≤ ||z−c*||². Conditional
centering in (13), followed by Pythagoras, therefore gives

    E[||v_j−g||₂² | F_{j−1}]
      = E[||c_j−c*||² | F_{j−1}] + delta²
      ≤ ||mu_j−c*||² + 3M/N_j + delta²
      ≤ ||S_{h_j}v_{j−1} − g||₂² + 3M/N_j + delta²
      ≤ exp(2 gamma h_j)||v_{j−1}−g||₂² + 3M/N_j + delta².     (14)

The last step uses (1) and S_h g = g. Conditional centering is used before
clipping; claiming that the clipped coefficient estimates are unbiased
would be false. Shared learned randomness across later trees is harmless
because all statements are conditional on the fixed previous interface.

With R_j = E||v_j−g||₂² and s_j = sum_{l≤j} h_l,

    R_K ≤ exp(2 gamma T)R_0
          + sum_{j=1}^K exp(2 gamma (T−s_j))
              (3M/N_j + delta²),                             (15)

where R_0 = 0 when the exact known input g is used on the first slab.
The algorithm must never replace v_{j−1} by g on later slabs. The exact
reference is for assessment and the offline envelope proof, not an
intermediate oracle.

For a general nonstationary target, the identical argument requires
P u(s_j) to lie in the chosen box at every slab, and replaces delta² by
the true omitted tail at that time. Neither condition follows merely from
smoothness or boundedness; it must be proved or budgeted separately.

## 5. A rigorous finite-budget witness, and what it means

Take T = 4, K = 50, h = .08, M = 1/4 and N = 200,000 trees per slab.
Equations (4) and (15) imply

    sum_{j=1}^{50} exp(2 gamma (4−.08j))
      ≤ 50 exp(8 gamma) < 100.

Indeed 8 gamma < 3/5 and exp(3/5) ≤ (1−1/5)^(−3) = 125/64 < 2.
Thus

    E||v_50−g||₂² < 100(3/(4N) + 10^(−16))
                  < .0004,
    (E||v_50−g||₂²)^(1/2) < .02.                              (16)

This is an ideal-real-arithmetic mathematical budget of 10 million local
root trees. It is not measured performance or an execution authorization
to spend unlimited CPU. Floating evaluation of elliptic functions, sine,
weights and accumulation is outside (16) until separately bounded. The
margin between .00037500000001 and .0004 is available for explicit
implementation error; it must not be silently consumed.

For any periodic sine polynomial in V,

    ||v−g||∞ ≤ sqrt(6)||v−Pg||₂ + delta_inf.

Consequently the same simple bound gives a sup-norm RMS below .02 at
N = 1,200,000 trees per slab, using (9): 60 million roots. This stronger
claim uses the finite-dimensional inverse bound and is more expensive.
A pointwise or sup-norm headline cannot use the 10-million-root budget.

The complete ternary rate-2 tree dominates the raw sampler’s node work.
For a rate-lambda full ternary tree of duration h,

    E[live leaves] = exp(2 lambda h),
    E[total visited nodes] = (3 exp(2 lambda h)−1)/2.             (17)

Thus the 10-million-root witness has expected raw work bounded by
10^7 (3 exp(.32)−1)/2 nodes. This bounds tree-node operations, not seconds.
Initial elliptic input evaluations, coefficient accumulation, later
three-mode value/derivative evaluations, peak memory and all root failures
must be recorded. Batching roots changes memory use without changing the
estimator. Cutting off a difficult tree or discarding failed roots changes
the algorithm and is not licensed by this proof.

Meaningful falsification checks, to be specified before future runs:

- Verify that later slabs use only the stored learned coefficients and that
  every realized box member satisfies the deterministic global envelopes.
- Check the three distinct error observables: normalized spatial L2,
  nonzero/interface-adjacent fixed queries, and sup error. The zero at x=0
  is enforced by odd symmetry and is not an informative accuracy check.
- Preserve roots, nodes, coefficients, clipping frequency and every
  resource stop; compare with independent seeds and the analytic target.
- Include direct raw one-shot estimates where their moment theorem applies,
  and direct bounded majority as a changed-representation baseline.
- Retain the preset 1–2 CPU-hour screening cap. A stopped run is incomplete
  performance evidence, even though the idealized error theorem remains.

The target is stationary and small-amplitude. It demonstrates a genuinely
learned nonconstant continuation with the original local representation;
it does not demonstrate moving-interface accuracy, generic terminal data,
or an improvement over the best deterministic Fourier/PDE solver.

## 6. Function-value fallback: monomial tree and exact local moment

This section records the original fallback construction, which is a
different stochastic representation from SemilinearMechanism. For terminal
g with |g| ≤ 1, absorb the linear term +u and use independent rate-lambda
clocks. At root remaining duration h,

    if tau ≥ h: H = exp((1+lambda)h) g(X_h),
    if tau < h: H = −exp((1+lambda)tau)/lambda * H_1 H_2 H_3.

At a branch all three descendants start at the same X_tau and have fresh
independent future randomness. Cancellation of clock density/survival
recovers the mild equation

    u(h) = exp(h) P_h g
           − integral_0^h exp(tau) P_tau[u(h−tau)^3] d tau.

The worst-case uniform second-moment majorant obeys

    M' = (2+lambda)M + M³/lambda,       M(0)=1,

and has the exact solution

    M(h) = exp((lambda+2)h)
           / sqrt(1−(exp(2(lambda+2)h)−1)/(lambda(lambda+2))),
    h_* = log(lambda+1)/(lambda+2).                            (18)

For lambda=2, h_* = log3/4, so h=.1 and .125 are strictly admissible.
This is the sharp second-moment threshold for constant |g|=1 in this
particular monomial tree, not an original-NPP threshold. Its absolute
first-moment majorant solves A'=A+A³ and expires at log2/2. Below (18),
finite-generation killed-tree values have second moments bounded by M.
The full tree is finite almost surely by bounded-arity exponential
nonexplosion. Fatou gives a finite full-tree second moment, the killed
values are uniformly integrable, and their mean identity passes to the
full tree. Local mild uniqueness identifies the PDE solution. Equation
(17) gives the same complete-tree cost.

The existing bounded majority sampler is a better bounded-output fallback:
at rate 2, leaves return g and internal values are
(a+b+c−abc)/2. Its output is in [−1,1], so its second moment is at most one
at every horizon. This representation is established prior art; see
[Etheridge, Freeman and Penington](https://arxiv.org/abs/1607.07563) and the
repository’s prior long-horizon theory audit. Neither fallback repairs the
original derivative-code interface by itself.

## 7. Why a plain clipped grid is a weaker first demonstrator

On a periodic grid of J points and spacing Delta=L/J, let I be linear
interpolation and C scalar clipping onto [−1,1]. With a function-value
local solver, store

    v_j = I C(grid sample means of S_h v_{j−1}).

This is globally bounded and makes the next local moment bound uniform,
but C is an explicitly biased contraction. Piecewise-linear v_j is not
C1, so it is not automatically an admissible raw NPP terminal.

If eta_j is the maximum grid error of sample means relative to their
conditional expectations, and u_j is the true solution, then pathwise

    ||v_j−u_j||∞ ≤ eta_j + exp(h)||v_{j−1}−u_{j−1}||∞ + b_j,
    b_j ≤ Delta² ||u_j''||∞/8
          or Delta ||u_j'||∞/2.                               (19)

Only true-solution regularity is used for b_j. For the monomial fallback,

    E[eta_j² | previous data] ≤ J M(h)/N_j.

For bounded majority, Hoeffding and a union bound give instead

    E[eta_j² | previous data] ≤ 2(log(2J)+1)/N_j.

These are conditional, finite-sample statements; no normal confidence
interval is needed. Minkowski applied to (19) gives

    (E||v_K−u_K||∞²)^(1/2)
      ≤ exp(T)r_0 + sum_j exp(T−s_j)(sigma_j+b_j).

With equal h, this accumulates by (exp(T)−1)/(exp(h)−1), approximately
exp(T)/h. The resulting uniform epsilon=.02 budgets can be prohibitive
even though every local tree has a small expected size. A smooth Fejér
convolution preserves a value interval but adds approximation error and a
degree-dependent derivative envelope; it does not remove this sup-error
budget issue. The orthogonal coefficient proof above has the decisive
advantage that conditional variances add in squared norm.

If the raw local certificate or the coefficient-estimation implementation
cannot be discharged, a two-slab exact-interface/controlled-perturbation
experiment is still a valid diagnostic. It must be called an oracle
interface experiment and must not be reported as learned continuation.

## 8. Proof and implementation boundary

Suitable finite Lean obligations are coefficient-box contraction, the
value/derivative envelope arithmetic, the cubic energy inequality, the
abstract conditional squared-error recurrence once its analytic inputs
are hypotheses, and the explicit finite-slab budget. The special-function
identities, Fourier expansion, Poincaré/semigroup bridge, conditional raw
tree representation and numerical special-function evaluation are separate
obligations unless actually formalized.

Continuation via projections and branching is already an established
approach; [Bouchard et al.](https://arxiv.org/abs/1612.06790) is a relevant
local-polynomial/Picard baseline. This note supplies a project-specific,
falsifiable contract and a finite-budget witness conditional on the raw
moment theorem, not a claim of general methodological novelty.

## 9. T02b: the same periodic datum defeats the unsplit raw rate-2 tree

This supplementary conventional proof concerns exactly the same g and L
as Sections 2–5. It supplies a conservative second-moment obstruction for
the unsplit original raw sampler. It is not an experiment, an optimized
threshold, an absolute-integrability theorem, or a theorem about every
possible rate/proposal.

**Claim.** For the unsplit derivative-coded SemilinearMechanism with common
exponential rate lambda=2 and its original probability 1/2 for each of the
two F-code tuples, the extended root moment E[H_Id(T,x)²] is infinite for
every x and T ≥ 7/2. In particular it is infinite at T=4 for this periodic
nonconstant terminal datum. Exact pruning of a zero-valued descendant is
allowed, since it does not alter the sampled estimator. Renormalizing the
tuple probabilities after deleting a zero tuple is a different proposal
and is outside this stated comparison.

### 9.1 Positive moment system and normalization

Denote the extended nonnegative second-moment fields for
(Id,Dx1,F0,F1,F2,F3) by (M_I,M_D,M_0,M_1,M_2,M_3). Positive finite-depth
tree expansions and monotone convergence define their minimal nonnegative
mild system, even when some of its values are infinite. Squared scalar
coefficients are retained. In particular the F-code subsystem is

    (M_0)_t = (1/2)Delta M_0 + 2M_0 + M_0 M_1 + (1/4)M_D² M_2,
    (M_1)_t = (1/2)Delta M_1 + 2M_1 + M_0 M_2 + (1/4)M_D² M_3,
    (M_2)_t = (1/2)Delta M_2 + 2M_2 + M_0 M_3,
    (M_3)_t = (1/2)Delta M_3 + 2M_3,
    (M_I)_t = (1/2)Delta M_I + 2M_I + M_0/2.                  (20)

The notation in (20) abbreviates the nonnegative mild identities; it
does not assume that a global finite classical moment solution exists.
The factors M_0 M_{k+1} have coefficient 1 because 1/(lambda q)=1.
The derivative tuple coefficient is 1/4 because its F-code carries the
scalar factor −1/2, which is squared. Since f''' is the constant −6,

    M_3(t,x) = 36 exp(2t).

Let N_j = exp(−2t) M_j. After dropping the nonnegative derivative terms,
the normalized fields dominate

    (N_0)_t ≥ (1/2)Delta N_0 + exp(2t) N_0 N_1,
    (N_1)_t ≥ (1/2)Delta N_1 + exp(2t) N_0 N_2,
    (N_2)_t  = (1/2)Delta N_2 + exp(2t) N_0 N_3,
    N_3 = 36,
    (N_I)_t = (1/2)Delta N_I + N_0/2.                       (21)

Only the lower comparison for the first four fields will be needed.

### 9.2 A uniform positive seed after one unit of heat evolution

From (3), kappa < 3/2 and the elementary pi bounds,

    4 < L < 5.

For every x,y on this torus, the wrapped time-1 Brownian heat kernel has
at least one Gaussian image at distance at most L/2. Its density relative
to ordinary dy therefore satisfies

    p_1(x,y) ≥ (1/sqrt(2 pi)) exp(−L²/8)
             > (1/3) exp(−4) > 1/192.                       (22)

For the last step use exp(2) < 8. No heat discretization is used.

The terminal amplitude sqrt(2/21) is greater than 3/10, and (2) gives
|g'| < 1/2. On each interval of radius 1/10 around its positive and
negative peaks, |g| is therefore greater than 1/4. These two intervals
are disjoint. Their total length is 2/5, so

    integral_0^L g(y)² dy > (2/5)(1/16) = 1/40,
    P_1(g²)(x) > 1/7680 for every x.                         (23)

Moreover |g|² ≤ 2/21, hence

    f(g)² = g²(1−g²)² ≥ (19/21)² g² > (4/5)g².

Keeping only the terminal heat contribution in the N_0 mild equation
now gives the explicit uniform bound

    N_0(1,x) ≥ P_1[f(g)²](x) > 1/9600.                     (24)

The initial N_1 and N_2 fields at time 1 are nonnegative; we may discard
their positive lower bounds. The constant N_3 remains exactly 36.

### 9.3 A spatially constant scalar system that explodes

For t ≥ 1 define

    s(t) = (exp(2t) − exp(2))/2,       ds/dt = exp(2t).

A spatially constant subsolution has no diffusion contribution. By
positivity and the restart form of the mild equations, (21)–(24) dominate
the scalar system

    dA/ds = A B,      dB/ds = A C,      dC/ds = A E,
    E = 36,
    A(0)=1/9600,      B(0)=C(0)=0.                            (25)

This comparison can be made on the minimal nonnegative Volterra
solutions by monotone Picard iteration, so it does not presume finite
moments. In particular N_0(t,x) ≥ A(s(t)) while (25) is finite.

Put z(s) = integral_0^s A(r) dr. Integrating the triangular equations
gives

    C = 36z,       B = 18z²,       A = 1/9600 + 6z³,
    z' = 1/9600 + 6z³,            z(0)=0.                    (26)

Its finite explosion time satisfies the explicit integral bound

    s_* = integral_0^infinity dz/(1/9600 + 6z³)
         ≤ integral_0^(1/30) 9600 dz
             + integral_(1/30)^infinity dz/(6z³)
         = 320 + 75 = 395.                                  (27)

The corresponding physical time obeys

    t_* = (1/2)log(exp(2)+2s_*)
         < (1/2)log(798) < 7/2.                              (28)

The inequalities exp(2)<8, exp(2)>7 and exp(1)>5/2 suffice:
exp(7)=exp(2)^3 exp(1)>7³(5/2)>798. For example exp(2)>7 follows
from its Taylor polynomial through degree four. The bound exp(1)<11/4
(and hence exp(2)<8) follows by bounding the positive Taylor tail from
degree four by (1/24) sum_{j≥0}5^(−j)=5/96. These are exact elementary
bounds, not measured approximations.

### 9.4 Root-specific divergence, including all starting positions

It remains necessary to transfer divergence to Id; a divergent descendant
alone would not settle the requested claim. The normalized root mild
equation is

    N_I(t,x) = P_t[g²](x)
                 + (1/2) integral_0^t P_(t−r)[N_0(r,.)](x) dr.

For 1 ≤ r < t_* the uniform comparison in (25) gives N_0(r,.)≥A(s(r)).
For t<t_* it follows that

    N_I(t,x) ≥ (1/2) integral_1^t A(s(r)) dr
             ≥ (1/2)exp(−7) integral_0^(s(t)) A(v) dv
             = (1/2)exp(−7) z(s(t)).                         (29)

The middle inequality uses r<t_*<7/2 and dr=exp(−2r) ds.
Equation (26) makes the right-hand side diverge as t increases to t_*.
For any fixed t≥t_*, the same root mild integral contains the whole
interval 1≤r<t_*. The heat semigroup preserves the spatially constant
lower bound, and the integral over that interval is infinite. Thus

    N_I(t,x) = M_I(t,x) = infinity for every x and t≥t_*.

This proves the stated T≥7/2 obstruction, and hence the same-datum
T=4 comparison. It does not assert a finite first moment or a defined
ordinary variance at T=4. It does establish that the original unsplit
rate-2 raw estimator is not in L2 there, while the learned continuation
has the finite idealized error budget in Section 5 under its separately
reviewed local theorem. The lower bound is conservative and gives no
optimal raw threshold.
