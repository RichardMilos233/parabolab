# T95: actual derivative fields for fractional diffusion

Date: 2026-09-29. Bounded conventional research candidate, pending
separate independent audit and root acceptance. No accepted-ledger
claim is promoted by this file.

**Result:** for every fixed `0<beta<=1`, `c>0`, `tau>0`, and scalar
inward polynomial reaction, an actual smooth derivative-field sampler
exists in the same paid exact-real primitive model as D43/D44. It has
at most `j` unknown scalar acquisitions on every seed and conditional
work `C[(1+G)n+K]` for a finite `K`-coefficient output. No positive-stable,
fractional-kernel, or conditional-distribution oracle is added.

The proposed unequal-height tree inequality is correct. A stronger
harmonic-height inequality saves one population power in the inverse-
variance moment bound. Both are proved below. Every Gaussian covariance
and independence assertion is conditional on the entire tree and all
stable clocks. Stable mixtures need not have finite unconditional
covariances; no unconditional Gaussian assertion is made.

This is a sampling gate. A quantitative paid fractional known-profile
solver and matching long-time lower/composition theorem remain open
here. The analytic positive-time tail used in 04z is false for general
smooth inputs when `beta<1/2`, even for `f=0`; Section 12 supplies an
explicit example. It does not rule out a suitable weaker Gevrey solver
or polynomial overhead in time. Fractional branching, negative stable
moments, and stable random-variate simulation are classical ingredients,
not novelty claims of this note.

## 1. Scope, source locks, and inherited model

The inspected checkout HEAD was
`65dca46e42db1c80cdf9ddd8eed6a415148c37f3`. Its working tree already
contained extensive modified and untracked research, Lean, and Python
files. HEAD alone does not identify the proof inputs. The SHA256 locks
below identify the actual sources; paths are relative to
`docs/research/runs/2026-09-28-dynamic-continuation/`.

| Source | SHA256 |
| --- | --- |
| `04aa-polynomial-fields-and-linear-gaussian-preparation.md` | `433c699d951c74fa6ba19166e159069130e1340a7a319aa0334b0ba4f8a1b8a1` |
| `reviews/R20-polynomial-reaction-field-sampler-candidate.md` | `b1e42a195c67942066894d04a11c28d7ba2951a6d6730977070e424ac84542b9` |
| `reviews/R20b-continuous-domain-addendum.md` | `6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527` |
| `reviews/R21-linear-tree-common-gaussian-candidate.md` | `99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461` |
| `reviews/T91-polynomial-field-linear-gaussian-independent-audit.md` | `2f06d787fcbb631662b3be4997eb6c610e145120147a0e831d245345abde1af7` |
| `04z-all-positive-diffusivity-sharp-queries.md` | `57ef1d86ddba30ce9d54f316b0eb2dc97f407f7aeb4446a66b3103c28e0aedd4` |
| `reviews/T87-all-diffusion-sharp-query-feasibility.md` | `acd788e6ee5564778cd0663be99aab17fb61f22bdfb4b345ccade008f18feff1` |

The accepted 04aa, mandatory R20b, R21, T91, and 04z were read in
full. R20's construction and derivative/cost proof were inspected;
T87 was consulted specifically for its primitive list and explicit
Gaussian-sum constant. This task does not claim a fresh review of all
T87 or the entire earlier long-time proof chain. The run context,
current next-step/claim entries, research guide, README, applicable
ancestor instructions, and project CLAUDE.md were also inspected.
The work stays on the MC mathematical side.

Use the normalized torus `X=(R/Z)^d`, integer `d>=1`. The fixed
known real polynomial satisfies `f(-1)>=0`, `f(1)<=0`. The equation
and spectral convention are

    u_t=-c(-Delta)^beta u+f(u),
    (-Delta)^beta exp(2*pi*i*nu.x)
       =(4*pi^2*|nu|^2)^beta exp(2*pi*i*nu.x),
    nu in Z^d, with zero-mode multiplier zero.                  (1.1)

Fix real continuous `g,v` on `X`, with `||g||inf<1`, and put
`e=v-g`. The supplied known evaluator of `g` costs at most `G`
operations per lookup and makes no additional calls to `v`. Only
exact scalar values of `v` supply new unknown information; every
acquisition, including repeated spatial locations, is charged.
No bound on `||v||inf` is needed for a derivative at `g`. Taylor
evaluation at `v` separately requires the full segment `g+t e`,
`0<=t<=1`, to remain in the open unit ball of `C(X)`.

The inherited paid model charges arithmetic, comparisons,
floor/ceiling, indexing/modular operations, reads/writes,
`exp`, `log`, `sin`, `cos`, positive square roots, and exact scalar
uniform, exponential, and Gaussian draws with known parameters.
Fixed public real constants, arbitrary finite exact magnitudes,
and ideal address/integer words are allowed. These are T87's
explicit primitives. No finite-bit accuracy, numerical conditioning,
or wall-clock result is claimed.

## 2. The classical positive stable law is an actual finite program

For `0<beta<1`, let `Theta` be uniform on `(0,pi)` and `E` an
independent mean-one exponential. Kanter's positive stable variable is

    S_beta = sin(beta Theta)/(sin Theta)^(1/beta)
             * [sin((1-beta)Theta)/E]^((1-beta)/beta),
    E exp(-z S_beta)=exp(-z^beta),       z>=0.                    (2.1)

This is the Laplace normalization, not an unconverted skew-stable
characteristic-function parameterization. I checked the normalization
and factorization in N. Demni's primary research paper, pages 1--2.
Expanding that paper's `a_beta(theta)` and taking power
`(1-beta)/beta` gives (2.1). This classical factorization is a cited
input, not a newly proved stable-law identity here.
[Demni, *On positive classical and free stable laws*](https://arxiv.org/pdf/1009.4926).

For a chronological lifetime segment of length `ell>=0`, draw

    L=0                                      if ell=0,
    L=c ell                                  if beta=1,
    L=(c ell)^(1/beta) S_beta                 otherwise.         (2.2)

The second case is a separate branch, never `0^0` or a logarithm
of `sin(0)`. For `ell>0` the last case is strictly positive and
finite on the open draw supports. Its exact Laplace transform is

    E exp(-z L)=exp(-c ell z^beta).                              (2.3)

An allowed-primitive realization draws one uniform `V`, sets
`Theta=pi V`, draws `E`, and computes

    L=exp[(log(c ell))/beta + log(sin(beta Theta))
          -(log(sin Theta))/beta
          +((1-beta)/beta)
             (log(sin((1-beta)Theta))-log(E))].                 (2.4)

After public parameter preparation, each positive edge uses three
sine evaluations, five logarithms, one exponential evaluation, two
scalar random draws, and a fixed number of arithmetic, storage,
and guard operations. All logarithm arguments are positive. Powers
are implemented by the displayed `exp/log` formulas, not a new
power primitive.

If a chosen uniform presentation includes its endpoints, replace
`V=0` or `V=1` by `V=1/2`; if its exponential presentation includes
zero, replace `E=0` by `E=1`. These finite Borel guards alter only
null events. There is no retry, rejection loop, stable-series
truncation, numerical inversion, or hidden precision-dependent work.

At `beta=1/2`, (2.1) simplifies exactly to

    S_(1/2)=1/[4 E cos^2(Theta/2)].                              (2.5)

Its reciprocal mean is `4*1*(1/2)=2`, consistent with Section 6.
At `beta=1`, `S_1=1` and `L=c ell` are deterministic. These are
algebraic normalization/endpoint checks, not simulations.

## 3. Correct normalization and the fractional branching law

On each edge draw **one** scalar `L` from (2.2), shared by all
physical coordinates. Conditional on `L`, draw `D` with independent
coordinates `N(0,2L)`. Then

    E exp(i xi.D)=E exp(-L|xi|^2)
                 =exp(-c ell |xi|^(2beta)).                    (3.1)

Modulo the torus, this has Fourier multiplier
`exp(-c ell (4*pi^2*|nu|^2)^beta)`, exactly (1.1). Different edges
use independent stable clocks and Gaussian arrays. At every branch
all children start at the same parental endpoint.

Independent stable clocks in different physical coordinates would
give `exp(-c ell sum_k |xi_k|^(2beta))`, a different generator when
`d>1` and `beta<1`. The process here is subordinate Brownian motion,
a symmetric stable Levy process, not fractional Brownian motion.
The program samples finite edge endpoints, not infinite-jump paths.

Write `P_t` for the torus convolution semigroup. Adding independent
clock lengths and (2.3) gives its semigroup law. It is positive,
preserves constants, contracts the sup norm, and preserves `C(X)`.
Strong continuity follows on trigonometric polynomials from its
multipliers and then on all of `C(X)` by density and contraction.

Use the accepted R20/T91 bounded parent rule:

    B>=max(2,deg f),
    f(2t-1)=sum_i F_i binom(B,i)t^i(1-t)^(B-i),
    lambda=1+(B/2)max_i|F_i|,
    c_i=2i/B-1+F_i/lambda.                                      (3.2)

Its symmetric multiaffine cube interpolant `M` has `|M|<=1` on
`[-1,1]^B` and `lambda(M(z,...,z)-z)=f(z)`. Inward endpoint signs
and the interior nodes' distance `2/B` from the interval endpoints
give the cube bound as in T91. This construction is independent of
the spatial motion and costs finitely many public operations.

Run rate-`lambda`, exactly `B`-child branching to time `tau`, with
edge law (3.1). The chronological genealogy `T` is prepared before
unknown acquisition. Its population law is unchanged:

    E n(tau)^k<=exp(lambda tau(B^k-1)),       integer k>=1.       (3.3)

Indeed its generator on `n^k` is
`lambda n[(n+B-1)^k-n^k]<=lambda(B^k-1)n^k`. Stop at a population
threshold, use Gronwall, and use the first moment to exclude explosion;
Fatou gives (3.3). Thus no nonexplosion premise is assumed in advance.
The segment count is `(Bn-1)/(B-1)<=2n-1`. Recursive propagation
through `M` gives a multiaffine leaf polynomial `P_T` bounded by one
on its leaf cube.

For continuous `q` valued in the interval, bounded first-branch
conditioning gives

    F_t(q)=exp(-lambda t)P_t q
       +integral_0^t lambda exp(-lambda a)P_a
                  [M(F_(t-a)(q),...,F_(t-a)(q))] da.            (3.4)

Separate child independence and multiaffinity justify the nonlinear
expectation in (3.4). Its killed-semigroup variation of constants,
using (3.2), gives the mild equation (1.1). Polynomial local Lipschitz
continuity gives mild uniqueness and local existence. The constants
`-1` and `1` are a subsolution and a supersolution; comparison for
the positive semigroup (equivalently shifted-monotone Picard iteration)
uses the inward signs. The bounded interval prevents finite-time
continuation failure. Hence `F_t(q)=S_t q`, the actual PDE flow.

## 4. Unequal Gaussian heights: the partition proof works

Fix any finite rooted edge tree with `n>=1` leaves and nonnegative
finite lengths `L_e`. Root-to-leaf sums need not agree. Put

    b_e=indicator vector of terminal descendants of edge e,
    C=sum_e L_e b_e b_e^t,
    H_i=sum_(e on path to i) L_e,
    m=min_i H_i,           Hmax=max_i H_i.                       (4.1)

Give edge `e` starting height `s_e=sum_(strict ancestors of e)L`
and open interval `J_e=(s_e,s_e+L_e)`. Zero edges have empty
intervals. Away from their finitely many endpoints, any `0<h<m`
belongs to exactly one interval along every root-to-leaf path:
those intervals concatenate from `0` to `H_i>h`.

Edges simultaneously containing that height cannot be ancestors
of each other, since their intervals on a path are disjoint. Two
descendant label sets overlap only for ancestrally comparable edges.
Thus active descendant sets are disjoint and cover all leaves,
forming a partition into at most `n` blocks. This establishes the
needed nonoverlap; chronological time is not being identified with
subordinator height.

For every signed `z in R^n`, finite summation and Cauchy--Schwarz give

    z^t C z
      =integral_0^Hmax sum_(e: h in J_e)(sum_(i desc e)z_i)^2 dh
      >=integral_0^m (sum_i z_i)^2/n dh
      =(m/n)(sum_i z_i)^2.                                    (4.2)

Above `m` only a nonnegative integral was discarded. Signed `z`
is permitted. If `m=0`, this is the trivial PSD inequality.
Coincident heights and zero edges alter only the finite excluded
set. Consequently, for every such tree,

    C >= (m/n)11^t.                                            (4.3)

## 5. Conditional R21 extraction and a stronger harmonic bound

Conditional on the chronological tree and all `L_e`, generate
independent scalar `Y_e~N(0,L_e)`, using zero for a zero edge, and
let `X_i` be their leaf path sums. Apply the exact R21 recursion.
At a terminal edge put `a_e=L_e`, `A_e=Y_e`. At an internal edge,
if all child variances `a_v>0`, put

    h=(sum_v 1/a_v)^-1,       alpha_v=h/a_v.

Otherwise put `h=0`, give weight one to the first zero-variance
child, and zero to the rest. In either case,

    a_e=L_e+h,       A_e=Y_e+sum_v alpha_v A_v.                  (5.1)

All weights are nonnegative, sum to one, and satisfy
`alpha_v a_v=h`, `sum_v alpha_v^2 a_v=h`. Conditional independence
of disjoint child subtrees gives the following induction, where
`X_(e,i)` is the path sum from the start of edge `e` to leaf `i`:

    Var(A_e)=a_e,       Cov(X_(e,i),A_e)=a_e.

Expanding child convex combinations gives at the root

    A=sum_i w_i X_i,       w_i>=0,       sum_i w_i=1,
    Var(A)=a,             Cw=a1.                               (5.2)

No common-height assumption entered the induction. A zero-variance
subtree has `A_e=0` by the guarded algebra itself, without dividing
by zero or relying on an almost-sure replacement.

Let `Z_i^0=X_i-A`. The complete vector is conditionally Gaussian,
possibly singular, and

    Cov(Z_i^0,A)=0,       Cov(Z_i^0,Z_k^0)=C_ik-a.               (5.3)

Its zero cross block factors its characteristic function. Hence
`A` is independent of the entire residual vector under this
conditional law, not merely of each coordinate separately.

Use `d` conditionally independent Gaussian coordinate arrays with
the **same** clocks and weights. The physical variables are
`G=sqrt(2)A`, `Z_i=sqrt(2)Z_i^0`. Conditional on the complete
clocked tree, `G~N(0,2a I_d)` is independent of the full residual
array. Their sums recover precisely the original branching endpoint
law after clock mixing. Unconditional independence is not asserted.

Testing (4.3) on `w` yields `a>=m/n`. If all `H_i>0`, then `a>0`.
Covariance Cauchy--Schwarz with each leaf gives `a^2<=a H_i`, so

    m/n <= a <= m.                                              (5.4)

The residual covariance `C-a11^t` is PSD. If `C-b11^t` is also
PSD, testing it on `w` gives `b<=a`; thus the extracted common
variance is maximal for this conditional Gaussian problem.

A stronger bound uses `C_ik>=0` and the nonnegative weights:

    a=w^t Cw>=sum_i H_i w_i^2>=(sum_i H_i^-1)^-1.                (5.5)

The last step is weighted Cauchy--Schwarz on `sum_i w_i=1`.
The harmonic expression is at least `m/n`. The algorithm needs
neither an inverse matrix nor expanded leaf weights; `w` is a
proof device. Its nonnegativity is essential to this improvement.

## 6. Negative moments of the extracted Gaussian width

Fix a chronological genealogy with height `tau`. Every leaf path
has `sum_path ell_e=tau`. Edge-clock independence and (2.3) give

    E[exp(-z H_i)|T]=exp(-c tau z^beta),       for every i.        (6.1)

Denote this scalar clock law by `L_tau`, to distinguish it from
the PDE flow `S_tau`. Each path has the law of `L_tau`, although
different paths share edges and need not be independent. Every
path contains a positive chronological edge, so every `H_i` is
positive on the guarded finite seed support.

For real `q>0`, the Gamma integral and nonnegative Tonelli yield

    M_q:=E L_tau^-q
       =1/Gamma(q) integral_0^infinity z^(q-1)exp(-c tau z^beta) dz
       =Gamma(q/beta)/[beta Gamma(q)]*(c tau)^(-q/beta)<infinity.
                                                                    (6.2)

For `beta=1` this equals `(c tau)^-q`. Positive stable negative
moments of this form are classical; Penent--Privault (1.8), (1.10)
contain the same calculation in their subordinator normalization.
[Penent--Privault, fractional branching paper](https://arxiv.org/pdf/2106.12127).

No positive moment of a stable clock is used. Its infinite mean
when `beta<1` therefore does not invalidate the conditional Gaussian
arguments or the following bounds. The negative moment concerns the
full path law at the fixed positive time `tau`; no quantity of the
form `integral_0^tau E[L_s^-q]ds` is required. The proposed route
works for all `q>0`:

    a^-q<=n^q m^-q=n^q max_i H_i^-q<=n^q sum_i H_i^-q,
    E[a^-q|T]<=n^(q+1) M_q.                                    (6.3)

For `q>=1`, (5.5) and convexity improve this to

    a^-q<=(sum_i H_i^-1)^q<=n^(q-1)sum_i H_i^-q,
    E[a^-q|T]<=n^q M_q.                                        (6.4)

Only the common marginal law (6.1) is used. There is no leaf-clock
independence assumption. This saves one population power and suffices
for every field bound below.

Gamma is not a computational primitive and is unnecessary for the
sampler. It can also be eliminated from public envelope constants.
For integer `p>=1`, set `b=ceil(p/beta)`. Splitting the Gamma
integral at one gives

    Gamma(p/beta)<=1+(b-1)!,
    M_p<=Mbar_p:=[1+(b-1)!]/[beta (p-1)!]*(c tau)^(-p/beta).      (6.5)

The integral on `(0,1)` is at most one; on `(1,infinity)` bound
its integrand by `x^(b-1)exp(-x)`. Fixed factorial loops plus
`exp/log/ceiling` compute (6.5). At `beta=1`, use the sharper
`Mbar_p=(c tau)^-p` if desired. Preprocessing is finite for fixed
parameters, with no uniformity or small-constant assertion.

## 7. A cutoff-independent Hilbert envelope

Use the real separable Fourier Hilbert space

    r=d+1,       ||w||_r^2=sum_nu(1+|nu|^2)^r|what(nu)|^2.

As in D43, `||w||inf<=E_d||w||_r`, with
`E_d^2=1+4d 3^(d-1)`. Let `h_b` denote the torus Gaussian density
of coordinate variance `b`. Its multiplier is
`exp(-2*pi^2*b*|nu|^2)`. The common Gaussian therefore gives

    ||h_(2a)||_r^2=sum_nu(1+|nu|^2)^r exp(-8*pi^2*a*|nu|^2).

One fully elementary choice of constant is

    theta=8*pi^2,
    b0=1+sqrt(pi/theta),       b1=1+sqrt(2*pi/theta),
    H=(d+1)^(r-1)[b0^d+d*(2r/theta)^r*b1*b0^(d-1)].

For `0<a<=1`, use
`sum_k exp(-theta a k^2)<=b0 a^-1/2`,
`k^(2r)exp(-theta a k^2)<=(2r/(theta a))^r exp(-theta a k^2/2)`,
and the convexity inequality
`(1+sum_k nu_k^2)^r<=(d+1)^(r-1)(1+sum_k |nu_k|^(2r))`.
They give `||h_(2a)||_r^2<=H a^(-r-d/2)`. For `a>=1`, use
Fourier monotonicity and the bound at one. With the convenient
integer `p=r+d=2d+1`,

    ||h_(2a)||_r^2<=H(1+a^-p),       all a>0.                    (7.1)

Together (6.4), (7.1), and (3.3) imply

    E[n^(2j)||h_(2a)||_r^2|T]<=H[n^(2j)+M_p n^(2j+p)],
    E[n^(2j)||h_(2a)||_r^2]<=V_j,
    V_j:=H(1+Mbar_p)exp(lambda tau(B^(2j+p)-1)),       j>=0.       (7.2)

All constants in this chosen envelope have finite programs in the
listed primitives. The exact Gamma expression is also a valid
analytical alternative. No cutoff enters (7.2). The bound is not
uniform as `beta` or `c tau` tends to zero, nor in the degree,
branching rate, dimension, or derivative order.

## 8. Complete nonlinear translation law and the actual Frechet map

Fix the chronological tree and all stable clocks. For continuous
`F` on `X^n`, conditional independence from Section 5 gives, at a
fixed residual array `Z`,

    E_G F(x+G+Z_1,...,x+G+Z_n)
      =integral_X h_(2a)(x-u)F(u+Z_1,...,u+Z_n)du.               (8.1)

The density is even, so the orientation is correct. Every argument
is on the torus. Both sides are bounded for a fixed clocked tree;
clock mixing occurs after this conditional identity. There is no
unconditional Gaussian factorization.

With independent uniform `U in X`, define the analytical field

    F_omega(q)=h_(2a)(.-U)
                    P_T(q(U+Z_1),...,q(U+Z_n)).                (8.2)

Equation (8.1) integrates the common Gaussian through the complete
nonlinear polynomial. Section 3 then gives `E F_omega(q)=S_tau q`.
The residual covariance, heat variance, and all translated leaf
locations change consistently. Changing damping alone on old leaf
positions would not establish this identity.

For `j` distinct labels, a mixed partial of `P_T` is `2^-j` times
the signed sum over the selected `2^j` cube corners. Its absolute
value is at most one when the other leaf values are in `[-1,1]`.
Repeated-label partials vanish. Thus the actual order-`j` derivative
of (8.2), an ordered-injection sum, has the pathwise envelope

    ||D^jF_omega(q)[e_1,...,e_j]||_r
       <=n^j||h_(2a)||_r product_b ||e_b||inf.                  (8.3)

On every finite tree shape the stable formula, guarded harmonic
recursion, Gaussian generation, torus reduction, and evaluation of
continuous inputs are Borel. The map `(a,U)->h_(2a)(.-U)` is
continuous into `H^r` for `a>0`, by locally dominated Fourier
convergence. It needs no deterministic lower bound on `a` on a
fixed-population event. Countably many finite shapes and extension
by zero on the null nontermination set establish strong measurability.
Equation (7.2) supplies square-integrable envelopes, hence genuine
Bochner integrals. Only fixed tuples of directions are integrated;
no strong measurability in a nonseparable operator space is presumed.

Finite-polynomial Taylor estimates justify differentiability before
expectation. On a segment within the open cube, variation of the
order-`j` derivative is bounded by
`n^(j+1)||h_(2a)||_r||q-q0||inf`; its first-order remainder is
bounded by

    (1/2)n^(j+2)||h_(2a)||_r||q-q0||inf^2.

Both have finite expected norm by (7.2). Integrate at fixed
directions, then take the operator supremum. Induction proves
that the actual map

    S_tau:{q in C(X): ||q||inf<1}->H^r

is `C^infinity` Frechet differentiable, with derivative operator
norm at most `sqrt(V_j)`. Bounded point evaluations commute with
its Bochner expectation and identify it with the continuous PDE
flow in Section 3. For an admissible segment and `J>=1`,

    ||S_tau(g+e)-sum_(j=0)^(J-1)D^jS_tau(g)[e^j]/j!||_r
       <=sqrt(V_J)||e||inf^J/J!.                               (8.4)

Each realized field is spatially smooth because `a>0`. Repeating
the proof at any fixed integer `r>=d+1` gives every finite Sobolev
order, with order-dependent constants. This does not establish an
analytic radius or a useful quantitative Gevrey bound.

## 9. Actual tuple sample, finite real output, and hard query cap

Fix `j>=1` and box cutoff `N>=0`, with `K=(2N+1)^d`. Prepare the
whole chronology, stable clocks, Gaussian residuals, and `a`.
If `n<j`, return zero without unknown acquisition. Otherwise draw
independent uniform `U` and a uniform ordered injection
`I=(I_1,...,I_j)` of distinct labels. Cache all known values
`g(U+Z_i)` and compute the selected mixed partial `C_I` with at
most `2^j` complete parent passes, assigning signs to selected
leaves. Only known data are used, and `|C_I|<=1`.

After this preparation, acquire the selected `j` scalar values
of `v`, charging repetitions separately, and form

    z=(n)_j C_I product_(b=1)^j (v-g)(U+Z_(I_b)),
    W_j=h_(2a)(.-U)z.                                         (9.1)

Uniform injection averaging cancels the falling factorial `(n)_j`
and gives exactly (8.3)'s ordered sum. Equal directions retain
all permutation multiplicities; only Taylor coefficients divide
by `j!`. Therefore

    E W_j=D^jS_tau(g)[e,...,e],
    E||W_j||_r^2<=V_j||e||inf^(2j).                            (9.2)

The scalar coefficient and heat shift share `U` and are not
independent. The bound is pathwise before integration and retains
all coefficient/location correlations.

The actual output is the finite real Fourier array `P_N W_j`.
Its constant coefficient is `z`. For one explicitly indexed
representative of each nonzero pair `{nu,-nu}` in the box, the
cosine and sine coefficients are

    2z exp(-4*pi^2*a*|nu|^2) cos(2*pi*nu.U),
    2z exp(-4*pi^2*a*|nu|^2) sin(2*pi*nu.U).                    (9.3)

The sine sign is positive, from `cos(2*pi*nu.(x-U))`. These are
actual finite formulas for the analytical field's coefficients.
Neither an infinite heat series nor a fractional heat density is
evaluated. All modes use the same selected unknown values.

No acquisition occurs before complete finite-tree preparation.
A null seed on which chronology generation never terminates makes
zero acquisitions. Section 2's guards are finite. Thus the
all-seed acquisition cap is `j`, and the algorithm halts almost
surely for every continuous input. The finite output is Borel.
No unknown derivative, integral, Fourier, or PDE-value oracle is used.

For independent complete samples, the actual Hilbert identity is

    E||M^-1 sum_b W_(j,b)-mu_j||_r^2
      =M^-1(E||W_j||_r^2-||mu_j||_r^2)
      <=V_j||e||inf^(2j)/M,       mu_j=E W_j.                  (9.4)

Centering, independence between samples, and square integrability
justify zero cross terms. Fourier coordinates inside a sample may
be correlated. Projection contracts `H^r`, and the embedding
controls a spatial supremum inside expectation. The envelope in
(9.4) is an upper bound, not generally the exact variance.

## 10. Counted preparation is linear in the tree and finite output

The genealogy has at most `2n-1` segments and one fewer child-list
entries. A depth-first or breadth-first simulation draws one
chronological exponential per processed segment and compares it
with the remaining time. It needs no global event-sorting heap.
All scalar draws and storage are included in these counts:

1. Each edge clock takes fixed scalar work by Section 2. A postorder
   traversal computes all `a_e` and child weights with the zero guard.
   Each child list is scanned only a fixed number of times: `O(n)`.
2. Draw `d` standard Gaussian coordinates per nonzero edge and scale
   by `sqrt(L_e)`. A preorder pass accumulates path sums, a postorder
   pass accumulates `A_e`, and leaf subtraction followed by `sqrt(2)`
   scaling gives the physical residuals. Cost and storage are `O_d(n)`.
3. Initialize a leaf array and perform `j` Fisher--Yates swaps to
   sample the ordered injection. A uniform integer from the remaining
   labels uses a uniform draw, multiplication, floor, and null-endpoint
   guard. Cost is `O(n+j)`, without collision rejection.
4. Modular reduction, the known cache, and at most `2^j` parent passes
   cost `C_(B,j,d)(1+G)n`. Selected acquisitions and the falling factorial
   cost `O(j)`, with `j` fixed.
5. Enumerating and storing the `K` real entries of (9.3) costs `O_d(K)`.

After finite public preprocessing, each finite execution therefore has

    Work<=C_(B,j,d,beta)[(1+G)n+K].                             (10.1)

No complete root path is resummed separately for each leaf, no dense
matrix is formed, and no expanded leaf-weight vector is stored.
A stable endpoint's enormous or tiny exact value does not add ideal
operation cost. Such magnitudes matter for finite-bit implementation,
which is outside the model. Nor is an infinite mean stable clock
length computational time: (2.4) samples its endpoint directly.

Only the first population moment is needed for expected preparation:

    E Work<=C[(1+G)exp(lambda tau(B-1))+K]
           <=C_(f,d,beta,c,tau,j)(1+G+K).                       (10.2)

Higher moments are needed for (9.2). If arbitrary unary chains were
allowed, leaf count alone would not bound preparation; the chosen
fixed `B>=2` genealogy has exactly the required segment bound.

## 11. Exact checks and prohibited shortcuts

For a one-leaf tree `a=L`, its residual is zero, and

    E exp(-4*pi^2 L|nu|^2)
       =exp(-c tau(4*pi^2|nu|^2)^beta).

This checks the generator and the factor two in `h_(2a)`. At
`beta=1` the construction is the Gaussian one with `kappa=2c`,
including `c tau/n<=a<=c tau`.

For a star with root variance `b>=0` and positive terminal
variances `l_1,...,l_n`,

    a=b+(sum_i 1/l_i)^-1,       H_i=b+l_i,
    (sum_i H_i^-1)^-1<=a<=min_i H_i.

A zero terminal variance activates the specified guard and gives
`a=b`; if `b>0` the same bounds still apply. These are exact
unequal-height and singular-residual checks. An all-zero tree has
`a=0` and satisfies the deterministic PSD lemma, but cannot occur
at positive chronological height with `c>0` and guarded stable draws.

The proof does not permit the following substitutions:

- Independent stable clocks per coordinate for the isotropic generator.
- Independent path totals for leaves sharing ancestral segments.
- Unconditional Gaussianity or independence after clock mixing.
- New Fourier damping with unchanged old residual positions.
- Uncounted Gamma, stable-quantile, density, or covariance primitives.
- Analytic/Gevrey conclusions from separate fixed Sobolev bounds.

The exclusions `c=0`, `tau=0`, and `beta=0` are substantive. At zero
burn-in or zero diffusivity even the zero-reaction map need not send
all continuous data into `H^r`. No extension is claimed to `beta>1`,
variable diffusion, systems, gradient reactions, or arbitrary
nonpolynomial reactions.

## 12. Separate long-time gates and an analytic-tail counterexample

The field sampler does not compute a high-accuracy known-profile
continuation. A counterpart of 04z's paid solver must prove
quantitative spatial regularity/truncation, a finite algorithm for
accuracy `exp(-P)`, stability, reaction evaluation costs, and work
in scale, `P`, and time. Its Laplacian proof cannot be imported by
changing the eigenvalue symbol alone.

There is a concrete obstruction to copying its analytic-tail premise.
Fix `0<beta<1/2`, choose `2beta<eta<1`, and in one dimension take

    q(x)=delta sum_(k=1)^infinity exp(-k^eta)cos(2*pi*k*x),
    f=0.                                                       (12.1)

All derivative series converge absolutely, so `q` is smooth. For
any fixed promised order `s`, choose `delta>0` small enough for
the `C^s` unit ball and `||q||inf<=1/2`. Its mean is zero and it
is nonzero, so it changes sign. Thus it also belongs to the type
of full signed smooth input class used in 04z. At time `tau>0`
its nonzero positive-frequency coefficients are exactly

    (delta/2)exp[-k^eta-c tau(2*pi*k)^(2beta)].                  (12.2)

For every `b>0` these coefficients divided by `exp(-bk)` tend to
infinity, since `k^eta/k` and `k^(2beta)/k` tend to zero. There
is no coefficient bound `C exp(-b|k|)` with fixed positive `b`;
the solution is not spatially analytic. An `exp(-bN)` projection
tail is also impossible, because an omitted coefficient is at
most the sup norm of the tail. Embedding this datum in one
coordinate gives the same obstruction in every dimension.

This counterexample is limited. For the linear problem fractional
damping gives a stretched-exponential tail of the form
`exp(-const*N^(2beta))` with polynomial factors, and therefore a
polynomial cutoff can still attain error `exp(-P)`. The nonlinear
paid solver, its precise Gevrey class and constants, and its
same-data cost require proof. For `beta>=1/2` this linear analytic
obstruction disappears; a nonlinear solver still does not follow
from that observation alone.

The first nonzero fractional spectral gap is `c(4*pi^2)^beta>0`.
It is a useful fact, not the existing signed-prior PDE separation
theorem. Lower-bound transfer must recheck smoothing, fluctuations,
mean/nonconstant-mode coupling, nonlinear sign separation, and the
adaptive/stopping information reduction on the same input class.
The semigroup preserves spatial mean; reaction of the field average
is generally not the average of the reaction.

For arbitrary inward polynomials, `sup_[-1,1] f'` can differ from
an equilibrium's instability rate, and there may be no unstable
equilibrium. For example `f=-u` is contractive. No universal
positive long-time exponent or automatic transfer of 04z's cubic
Theta query order follows from the present sampling theorem.

## 13. Attribution, evidence record, and next gate

The conventional conclusions are the unequal-height partition
inequality; conditional R21 extraction and harmonic strengthening;
negative moments; the nonlinear field and Frechet identification;
and the finite primitive/query/work construction. The external
stable-law identity used without a new proof is the normalized
Kanter factorization (2.1). Stable scaling, Gaussian normalization,
tree geometry, mixture identity, moment bounds, and field/cost
consequences were checked directly here.

After a source pointer from the root, I inspected Penent--Privault's
primary fractional PDE paper: introduction; (1.8), (1.10) on printed
pages 6--7; Remark 4.2 on page 20; and the higher-derivative discussion
and CMS formula on pages 23--24. It already treats branching
subordinate Brownian motion, stable negative moments, and elementary
stable draws. Remark 4.2 removes the subordinator time-integrability
condition when the reaction contains no spatial derivatives. Thus
an all-beta non-gradient branching representation is not a novelty
claim here. Their spatial integration-by-parts obstruction concerns
short-edge negative moments; our `D^jS_tau(g)` differentiates initial
data and uses fixed total chronological height. This argument does
not solve their gradient-reaction obstruction.
[Penent--Privault, *Existence and probabilistic representation of the solutions of semilinear parabolic PDEs with fractional Laplacians*](https://arxiv.org/pdf/2106.12127).

Demni's research paper was read at pages 1--2 for the precise
positive-stable formula and Laplace normalization. The authored
Devroye--James paper was additionally checked in its positive-stable
section, printed pages 9--10, for normalization and endpoints. No
independent theorem from the latter is needed by this proof.
[Devroye--James, *On simulation and properties of the stable law*](https://luc.devroye.org/devroye-james-stablesurvey-2013.pdf).

Kanter's original record identifies *Stable densities under change
of scale and total variation inequalities*, Annals of Probability
3(4), 697--707 (1975), DOI 10.1214/aop/1176996309. DOI/Project Euclid
full-text openings were inaccessible. Its author-uploaded ResearchGate
landing page opened, but the PDF link returned 404. I do not claim
inspection of the original Corollary 4.1 or proof; the accessible
research text above supplies the formula used.
[Kanter original-paper record](https://www.researchgate.net/publication/38362467_Stable_Densities_Under_Change_of_Scale_and_Total_Variation_Inequalities).

Bounded searches used `Kanter 1975 positive stable random variable
sin uniform exponential formula Laplace transform`, `positive stable
random variable Kanter representation exp(-s alpha) paper pdf`, the
exact original title with `Corollary 4.1`, and its DOI with `pdf`
and `projecteuclid`. Other search snippets were not substituted for
the inspected formula. A mirror opening failed and the arXiv text
succeeded. A screenshot request was not counted as visual proof
evidence. This was not a systematic novelty search. No worldwide
priority, prize significance, or practical speed result is claimed.

The math-auto-research skill, defaults, model-routing and execution
instructions, and configured General reader profile were read.
The bounded theory-only, one-owner-file task overrides the skill's
general run/claim-ledger update workflow. Root confirmed that dispatch
explicitly requested `gpt-6-astra`, reasoning effort `max`, and
`fork_turns=none`. The serving backend and actual effort are unexposed;
reading defaults is not evidence of a model switch. No model setting
was changed by this worker.

Actual local work comprised instruction/source inspection,
`git status --short`, `git rev-parse HEAD`, targeted `rg`/`sed`/`cat`
reads, SHA256 checks, exact mathematical derivation, bounded web-paper
inspection, and writing/rereading this file. An initial search used
an incorrect guessed 04y filename and returned `No such file or
directory`; `rg --files` located its actual name. A first add-file
patch had one missing patch-prefix character, was rejected before
writing, and was replaced by a correctly generated patch. These
mechanical failures are not mathematical checks.

No numerical experiment, symbolic algebra execution, unknown-input
acquisition, implementation test, or Lean invocation was run. The
toolchain file was inspected as `leanprover/lean4:v4.33.0`; this is
not a build or formal verification. Only this new T95 file was edited
by this worker. The locked proofs, old ledgers, Lean, code, numerics,
and canvas files were not modified.

All seven source hashes in Section 1 were rechecked after writing
and still matched. The full candidate was reread, including the
factor-two normalization and elementary-envelope arithmetic. A
self-review clarified the subtree path notation and separated the
scalar clock name `L_tau` from the PDE-flow notation `S_tau`.

Independent audit should target the shared-coordinate clock, height
partition, conditional mixture, harmonic moment improvement, finite
primitive program, and genuine derivative correspondence. Root
acceptance, formalization, numerical falsification, and the two
long-time gates remain separate subsequent decisions; none is
marked complete by this candidate.
