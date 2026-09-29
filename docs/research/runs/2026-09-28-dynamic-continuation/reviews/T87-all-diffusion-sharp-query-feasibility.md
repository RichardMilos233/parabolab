# T87: sharp query order for every fixed positive diffusivity

Date: 2026-09-29. Theory-only proof candidate; independent review and
root correspondence are still required.

**Verdict: GO for independent audit.** A different implementation of the
fixed-time tuple sampler removes the polynomial factor from the number
of initial-value queries. It analytically integrates a common Gaussian
component of the correlated leaf positions. The resulting random
profile has a fixed Sobolev second-moment bound. Averaging in that
Hilbert space, followed by an elementary Fourier embedding, controls
the spatial supremum without multiplying by the number of retained
modes. The paid computation still has a polynomial factor in the
target horizon.

This file proposes the upper theorem below on exactly the full signed
class, every fixed `kappa>0`, and every fixed integers `d,s>=1`.
It makes no accepted-ledger change. It does not claim exact matching
operation complexity, finite-bit computation, practical speed, a new
voting representation, publication priority, or end-to-end Lean coverage.
No experiment, numerical PDE solve, unknown-input acquisition, Lean
invocation, or implementation test was performed for this task.

## 1. Exact theorem candidate

Let `X=(R/Z)^d` carry normalized Lebesgue measure and let `S_t^kappa`
be the actual real Allen--Cahn flow

    u_t=(kappa/2) Delta u+u-u^3.

Fix `kappa>0` and integers `d,s>=1`. The unknown input class is

    V={v in C^infinity(X), real and periodic:
       ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

Only exact point values of `v` are available. Every acquisition is
charged, including repetitions and preprocessing. The allowed algorithm
class is the one in 04y: measurable adaptive randomized rules with
input-independent seeds, bias allowed, and almost-sure stopping on
every promised input. The constructed upper is a member of this class;
it need not use the full available adaptivity.

Use exactly the T81/04y paid ideal model: charge each real arithmetic
operation, comparison, floor/ceiling, index/modular operation, stored-value
read/write, and `exp,log,sin,cos,positive-square-root` evaluation. Exact
uniform, exponential-clock and Gaussian draws with known parameters
are charged primitives. Complex arithmetic is finitely many real
operations. Fixed public constants, unbounded exact real magnitudes,
and ideal integer/address words are allowed. No PDE, integral, derivative,
transform, or arbitrary known-function oracle is added.

Put

    q=s+d/2,       gamma=d/q=2d/(2s+d),
    J=ceil(1+d/(2s)),       m=J-1.

There are public constants `C,A<infinity` and an explicit Borel
almost-surely halting algorithm which, for every prescribed real
`T>=2`, returns an indexed real Fourier polynomial `U_T` satisfying

    sup_(v in V) (E||U_T-S_T^kappa v||inf^2)^(1/2)<=1/8,
    Q_T<=[1+J(J-1)/2] k^d on every seed path,
    k^d<=C exp(gamma T),
    sup_(v in V) E Work_T<=C exp(gamma T)(1+T)^A.       (1.1)

The spatial supremum is inside the expectation. Its returned array
has at most `C(1+T)^(3d^2+9d)` entries, as in T84 Section 10a.
Evaluating it at any specified point has polynomial paid cost and
uses no further unknown values. The inherited bounded-horizon patch
extends the assertion to `0<=T<=2`, after increasing `C`.

Constants can depend on fixed `kappa,d,s`, and can be extremely large.
No uniformity as `kappa` tends to zero or as `d,s` grow is asserted.

Together with the separately accepted D37 lower bound in 04y, (1.1)
would imply the exact minimax query orders

    Q_point(T)=Theta(exp(gamma T)),
    Q_profile(T)=Theta(exp(gamma T))                    (1.2)

at the common RMS tolerance `1/4` and the respective output contracts
in 04y. This file proves only the new upper candidate. It does not
re-audit D37, nor promote (1.2) before independent upper review.

## 2. Inherited interfaces and the specific gap

The complete frozen T81 and T84 were read, along with R10b and T68.
The following already audited interfaces are reused without changing
their class, primitive model, or parameters.

1. From exactly `k^d` grid acquisitions, the explicit Gevrey-2 local
   interpolant `g` has

       ||g||inf<=3/4,       ||v-g||inf<=Cint k^-s,
       ||partial^alpha g||inf
                    <=B0(C0 k)^|alpha|(alpha!)^2,      (2.1)

   for `k>=k0`. Preparation costs `O_(d,s)(k^d)` and each actual
   lookup costs a fixed `Gg<=C_(d,s)` paid operations. Only derivatives
   through total order `s` of `v` are used. No common Gevrey bound is
   imposed on the unknown input.

2. T81 Section 3/T84 Sections 3--6 give the finite known-profile solver.
   For known `q0` with `||q0||inf<=1` and a fixed quantitative Gevrey
   bound at inverse scale `R>=1`, evaluation cost `Wq`, and `S,P>=1`,
   it returns an indexed real Fourier polynomial with sup error
   `exp(-P)` from `S_S^kappa q0`, and work

       C R^d [1+P+S+log(R+1)]^a0 (1+Wq),
       a0=2d^2+20d+50.                                (2.2)

   Its transforms, initialization, time panels, scalar convolution
   weights, storage, and one point evaluation are paid. A requested
   finite set of low modes can be included by increasing its public
   cutoff, as in T81 (6.2).

3. Fixed positive-time analytic smoothing and scalar comparison give
   public `A_kappa>=1,b_kappa>0` such that

       ||(I-P_N)S_1^kappa v||inf<=A_kappa exp(-b_kappa N),
       ||S_1^kappa v||inf<7/8.                        (2.3)

   Here `P_N` retains the box `|nu|inf<=N`. The strip width can depend
   on `kappa`. This holds through the critical and weak-diffusion
   regimes, with no synchronization or stable-graph assumption.

4. T81 Section 7/T84 Section 9 construct the fixed primitive-evaluable
   smooth saturation `chi`, with identity interval `[-7/8,7/8]`,
   range `[-15/16,15/16]`, and Lipschitz constant `Lchi=25`.
   If a real box-`N` polynomial has constant coefficient in `[-1,1]`
   and other real sine/cosine coefficients in `[-2,2]`, then
   `qhat=chi(p)` has a uniform Gevrey-2 norm at inverse scale
   `Rhat=NK`, `K=(2N+1)^d`, and actual evaluation cost `O_d(K)`.
   The bound holds for every completed coefficient array.

5. Actual parabolic comparison gives

       ||S_t^kappa f-S_t^kappa h||inf
                           <=exp(t)||f-h||inf          (2.4)

   for the bounded real profiles used here.

T81 estimated each retained coefficient to error `epsilon/(2K)` and
summed those errors. That imposed `k^q` proportional to `K/epsilon`.
Merely replacing that sum by a claim that `C(X)` has type two is
invalid. Nor does coefficient correlation disappear by reusing a
single tuple. Sections 3--6 give an actual smooth random-field sampler
with a Hilbert second moment independent of `N`; this changes the
sampling construction and supplies the missing justification.

## 3. Every finite tree contains a common Gaussian component

Use the rate-two ternary genealogy run only to time one. Generate its
clocks and shape first, with a fixed leaf labeling. Let `n>=1` be the
number of terminal leaves. It is finite almost surely, has
`(3n-1)/2` total nodes, and for every integer `a>=1`,

    E n^a<=exp(2(3^a-1)).                              (3.1)

These are the stopped-population/nonexplosion bounds proved in
R10b/T68; they are unchanged by `kappa`. The whole genealogy is
independent of spatial Brownian marks and the input values.

Here an edge means a particle's lifetime segment, including the initial
ancestor's segment and each terminal segment cut off at time one. In
particular the one-leaf tree has one segment of length one. For each
such `e`, let `ell_e>=0` be its time length and `a_e in {0,1}^n` the
indicator vector of its descendant terminal leaves. Conditional on
this genealogy, one coordinate of the
usual lifted leaf displacement vector has covariance `kappa C`, where

    C=sum_e ell_e a_e a_e^t.                           (3.2)

Every root-to-leaf path has length one; in particular `C_ii=1`.
The entry `C_ij` is the duration of the common ancestral path.
Zero-duration edges and simultaneous endpoint degeneracies are allowed
in this deterministic calculation.

For almost every `t in [0,1]`, the alive particles partition the
terminal leaves into sets `A_1(t),...,A_b(t)`, with `b<=n`.
For every real vector `z in R^n`,

    z^t C z
      =integral_0^1 sum_(a=1)^b (sum_(i in A_a(t)) z_i)^2 dt
      >=integral_0^1 (sum_i z_i)^2/n dt
      =(sum_i z_i)^2/n.                               (3.3)

The inequality is finite Cauchy--Schwarz on the partition, valid for
signed `z_i`. Thus

    R=C-(1/n) 11^t is positive semidefinite.            (3.4)

This is a property of every finite genealogy, not a high-probability
tree event. It does not use a lower bound on the first edge length.

Let `G` be a `d`-vector with independent centered Gaussian coordinates
of variance `kappa/n`. Independently, for each physical coordinate
sample a centered `n`-vector with covariance `kappa R`; collect these
as residual vectors `Z_1,...,Z_n in R^d`. Conditional on the tree,

    (G+Z_1,...,G+Z_n)

is centered Gaussian with covariance `kappa C` in each coordinate,
and independent physical coordinates. Its joint law is exactly that
of the original correlated Brownian leaf displacements. This follows
by multiplying the Gaussian characteristic functions: their covariance
matrices add to `kappa C`. Wrapping modulo one preserves equality of
the joint laws on the torus.

### 3a. Counted sampling, including degenerate covariance

There is a finite program to sample the residual covariance, using
only the listed primitives. Build the descendant incidence arrays and
(3.2) in at most `O(n^3)` arithmetic/index/storage operations. Form
`kappa R` and apply the following semidefinite Cholesky procedure.

At step `i`, let `D` be the remaining Schur matrix.

- If `D_ii>0`, set the pivot to `sqrt(D_ii)`, divide the remaining
  column by that pivot, and subtract its outer product from the
  remaining submatrix.
- If `D_ii=0`, set that Cholesky column to zero and do not divide.

A positive-pivot Schur complement of a positive semidefinite matrix
is positive semidefinite: substitute the minimizing first coordinate
in its quadratic form. At a zero pivot, positivity of every two by
two principal quadratic form forces `D_ij=0` for all remaining `j`;
otherwise `D_ii+2tD_ij+t^2D_jj` is negative for some sufficiently small
signed `t`. Hence the zero-column branch is exact, and the remaining
principal submatrix is still positive semidefinite. Induction gives
`kappa R=L L^t` with real finite entries. No inverse, eigensolver,
negative square root, or division by a zero pivot is used.

Each physical coordinate uses `n` independent standard Gaussian draws
and multiplication by `L`. Matrix construction/factorization costs
`O(n^3)` and Gaussian generation/multiplication costs `O_d(n^2)`.
The case `n=1` gives `R=0` and hence `Z_1=0`, with all zero-pivot
branches well defined. Zero edges in larger trees are handled by the
same rule. Exact comparisons are part of the stipulated model; this
is not a claim about numerical Cholesky with roundoff.

### 3b. Integrating the common shift preserves nonlinear coefficients

Let `h_a` be the periodic heat density of covariance `a I`, so

    h_a(x)=sum_(nu in Z^d) exp(-2*pi^2*a*|nu|^2)
                                      exp(2*pi*i*nu.x),    a>0.

For a fixed genealogy and residual Gaussian array, and any continuous
periodic `q0`, Gaussian convolution gives

    E_G P_tree(q0(x+G+Z_1),...,q0(x+G+Z_n))
      =integral_X h_(kappa/n)(x-u)
                    P_tree(q0(u+Z_1),...,q0(u+Z_n)) du.   (3.5)

The density is even, so the orientation `x-u` is correct. The whole
nonlinear leaf polynomial is inside the common-shift integral. In
particular the unselected known leaf values and the selected partial
coefficient are translated together. They are not replaced by their
separate means.

Equivalently, take one uniform `U` on `X`, independent of the residual
Gaussian array and tree. Equation (3.5) is the expectation of the
smooth profile

    h_(kappa/n)(.-U) P_tree(q0(U+Z_1),...,q0(U+Z_n)).   (3.6)

This is an importance-density identity with respect to normalized
uniform measure. The algorithm will compute only finitely many Fourier
coefficients of this profile; it never evaluates an infinite heat
series. Simply multiplying the old T81 tuple weights by a heat factor
while retaining the old leaf covariance would not satisfy (3.5).

## 4. A fixed Hilbert space controls the entire random profile

Choose the fixed integer `r=d+1` and use the real Hilbert space
`H^r(X)` with Fourier norm

    ||f||_r^2=sum_(nu in Z^d) (1+|nu|^2)^r |fhat(nu)|^2.

Its real inner product is the real part of the corresponding weighted
complex inner product. The exponent is fixed before `T` is chosen.
For any finite Fourier polynomial, Cauchy--Schwarz gives

    ||f||inf<=E_d ||f||_r,
    E_d=sqrt(1+4*d*3^(d-1)).                           (4.1)

Indeed the sum of reciprocal weights is at most this square: the
`|nu|inf=l` shell has at most `2d(3l)^(d-1)` points, and its summands
are at most `l^(-2r)`. The remaining series is bounded by
`sum_(l>=1) l^(-d-3)<=2`. The same calculation shows absolute uniform
Fourier convergence for every element of `H^r`, proves (4.1) there,
and identifies a continuous representative. This is the only
Sobolev embedding needed below; no generic assertion about `C(X)`
having type two is used. Rectangular `P_N` is a contraction in this
Hilbert norm.

There is an explicit public `C_h=C_(kappa,d,r)` such that, for every
integer `n>=1` and every `U`,

    ||h_(kappa/n)(.-U)||_r^2
      =sum_nu (1+|nu|^2)^r exp(-4*pi^2*kappa*|nu|^2/n)
      <=C_h n^(r+d/2)<=C_h n^(r+d).                   (4.2)

For completeness, this constant needs no integration primitive. Put

    theta=4*pi^2*kappa,
    b_heat=1+sqrt(pi/theta),       c_heat=1+sqrt(2*pi/theta),
    C_h=(d+1)^(r-1)
           [b_heat^d+d*(2*r/theta)^r*c_heat*b_heat^(d-1)].

The decreasing Gaussian sum satisfies
`sum_(l in Z)exp(-a*l^2)<=1+sqrt(pi/a)`. Also
`l^(2r)exp(-a*l^2)<=(2r/a)^r exp(-a*l^2/2)`.
Use `a=theta/n`, the product structure, and
`(1+sum_i nu_i^2)^r<=(d+1)^(r-1)(1+sum_i |nu_i|^(2r))`.
These inequalities give precisely the first bound in (4.2). Replacing
`n^(r+d/2)` by the larger integer power is convenient for (3.1).

## 5. Actual derivatives into the Hilbert space and tuple samples

For the finite ternary tree propagate

    M(a,b,c)=(a+b+c-abc)/2.

As proved in R10b/T68, its leaf polynomial is multiaffine and bounded
by one on `[-1,1]^n`. Every selected distinct-label mixed partial has
absolute value at most one, by its exact signed `2^j`-corner average.
Repeated leaf labels differentiate to zero. With rate two and Brownian
covariance `kappa` per unit time, the first-branch identity has reaction
`2(M(u,u,u)-u)=u-u^3` and generator `kappa Delta/2`.
Thus the usual tree expectation equals `S_1^kappa q0` for every
`q0 in C(X)` in the open unit ball.

By (3.5), the expectation of (3.6) is this same actual flow.
Equation (4.2), the cube bound and (3.1) make (3.6) Bochner integrable
in the separable Hilbert space `H^r`. Strong measurability follows on
each finite-tree event from Borel Gaussian generation and the continuous
map `U -> h_(kappa/n)(.-U)` in `H^r`; the full seed space is a
countable union of these events, apart from null nontermination.

For arbitrary fixed `j`, differentiating the finite leaf polynomial in
directions `f_1,...,f_j in C(X)` yields the ordered-injection sum

    A_(tree,j)(q0)[f_1,...,f_j]
      =h_(kappa/n)(.-U)
         sum_(I ordered distinct labels) C_I(q0,U+Z)
                            product_(a=1)^j f_a(U+Z_(I_a)). (5.1)

It vanishes if `n<j`. Its Hilbert operator norm is bounded by
`n^j ||h_(kappa/n)||_r`. Define the public constants

    V_j=C_h exp(2(3^(2j+r+d)-1)),       j>=0,
    B_j=sqrt(V_j).                                    (5.2)

Equations (3.1)--(4.2) give

    E[n^(2j)||h_(kappa/n)||_r^2]<=V_j,
    ||A_j(q0)||op<=B_j.                               (5.3)

These bounds are uniform over the open unit ball and independent of
any frequency cutoff or target accuracy.

Here `A_j(q0)[f_1,...,f_j]` is defined by the Bochner expectation of
(5.1) for each fixed tuple of directions, in the separable space
`H^r`. The uniform bound makes these values a bounded multilinear
operator. No Bochner integral in the possibly nonseparable space of
multilinear operators or Dirac evaluation functionals is assumed.

The expectations of (5.1) are genuine Frechet derivatives into `H^r`.
To see this without an exchange assumption, keep a segment from `q0`
to `q0+h` inside the open unit ball. Finite-polynomial Taylor's theorem,
with one and two additional direction labels respectively, gives
operator continuity and the derivative remainder bound

    ||A_(tree,j)(q0+h)-A_(tree,j)(q0)
                  -A_(tree,j+1)(q0)[.,...,.,h]||op
      <=(1/2) n^(j+2)||h_(kappa/n)||_r ||h||inf^2.     (5.4)

The expected right side is finite by (5.3) at order `j+2`.
Starting with (3.6), induction proves that
`S_1^kappa:C(X)_{||.||inf<1}->H^r(X)` is `C^infinity`, with
the derivative expectation (5.1), continuous in operator norm.
The embedding (4.1) and (3.5) identify this map with the actual
PDE flow, not a different regularized flow.

In particular, if `e=v-g` and the segment `g+te` stays inside that
ball, then Taylor's integral remainder gives

    ||S_1^kappa v-sum_(j=0)^(J-1)
                         D^j S_1^kappa(g)[e^j]/j!||_r
                    <=B_J ||e||inf^J/J!.              (5.5)

This bound, unlike a sup-norm remainder followed by a Dirichlet
projection bound, has no logarithmic factor depending on `N`.

### 5a. The sampled smooth field

Use the paid `g`, and generate one complete genealogy, its residual
Gaussian array from Section 3a, and an independent uniform `U`.
Set `Y_i=U+Z_i` modulo the torus. When `n>=j`, select a uniform
ordered injection `I=(I_1,...,I_j)` into its leaf labels, and compute
the actual corner partial `C_I` using the leaf values `g(Y_i)`.
All these operations occur before any new unknown acquisition.

Acquire exactly the at most `j` values `v(Y_(I_a))` and form

    Z_j^scalar=(n)_j C_I product_(a=1)^j[v(Y_(I_a))-g(Y_(I_a))],
    W_j=h_(kappa/n)(.-U) Z_j^scalar.                  (5.6)

Use zero with no residual acquisitions when `n<j`. Distinct labels
may give repeated spatial locations; every such acquisition is charged.
The conditional expectation over `I` is the sum (5.1) with all
directions equal to `e`. Equations (3.5) and (5.1)--(5.4) therefore
prove the identity in `H^r`

    E W_j=D^j S_1^kappa(g)[e,...,e].

Since `|C_I|<=1`, (4.2) proves the joint field moment

    E||W_j||_r^2<=V_j delta^(2j),
    delta=Cint k^-s.                                 (5.7)

The coefficient depends on the residual Gaussian array and the same
`U` as the kernel shift; independence between them is not asserted or
needed. The norm of the kernel is independent of its translation,
so the pathwise bound proves (5.7) with all correlations retained.

### 5b. A finite real Fourier output and its paid cost

For a requested cutoff `N`, return only `P_N W_j`. Let one member of
each pair `{nu,-nu}` be chosen by the sign of its first nonzero
coordinate. In the real basis `1,cos(2*pi*nu.x),sin(2*pi*nu.x)`,
the sample's coefficients are

    z_0=Z_j^scalar,
    z_(nu,c)=2 Z_j^scalar exp(-2*pi^2*kappa*|nu|^2/n)
                                           cos(2*pi*nu.U),
    z_(nu,s)=2 Z_j^scalar exp(-2*pi^2*kappa*|nu|^2/n)
                                           sin(2*pi*nu.U). (5.8)

The sine sign is positive because the kernel contains
`cos(2*pi*nu.(x-U))`. These are exactly the real coefficients of
the projected kernel shift, and hence return a real polynomial.
No infinite series or heat-density evaluation is required.

Compute `C_I` with at most `2^j` upward tree passes after caching
`g(Y_i)`. Partial Fisher--Yates selection, with charged uniform draws
and floors, chooses the injection; assign any unit-endpoint draw to
the last valid index. This changes no probability law and makes the
rule total. Uniform root coordinates are reduced modulo one.
The falling factorial costs `O(j)`.
Section 3a pays for the correlated residual draws. Forming (5.8) and
updating the `K=(2N+1)^d` accumulators costs `O_d(K)` operations.
Consequently, conditional on a finite tree,

    Work(sample)<=C_(d,j)[n^3+(1+Gg)n+K].             (5.9)

All matrix/storage accesses and Gaussian multiplications are included;
`d n^2` is absorbed by `C_d n^3`. By (3.1) and the actual constant
lookup bound in (2.1),

    E Work(sample)<=C_(kappa,d,s,j)(1+K).              (5.10)

The only new unknown information is the selected tuple, at most `j`
values on every seed path. On a seed whose tree preparation never
finishes, that sample makes no acquisitions. There is no genealogy
truncation, finite-difference derivative, or silently supplied PDE value.

## 6. Hilbert averaging and real-coordinate clipping

Let `W_(j,1),...,W_(j,M)` be independent copies of (5.6), conditional
on the already paid deterministic coarse transcript for the given
input. Fresh seeds are independent of it. Write `mu_j=E W_j`.
The finite Hilbert expansion gives

    E||M^-1 sum_a (P_N W_(j,a)-P_N mu_j)||_r^2
      =M^-2 sum_a E||P_N W_(j,a)-P_N mu_j||_r^2
      <=V_j delta^(2j)/M.                             (6.1)

For different copies, the cross inner-product expectation is zero by
independence, centering and Fubini; its absolute integrability follows
from the second moments. Subtracting the mean only reduces a Hilbert
second moment, and `P_N` is a contraction. This argument does not
assume independence between Fourier modes inside one sample, nor use
a type-two property of the sup-norm space. Independence between
different derivative orders is convenient but unnecessary for the
Minkowski bound below.

Coordinate clipping also causes no mode-count loss in this norm.
For a real box-`N` polynomial with coefficients `c_0,c_(nu,c),c_(nu,s)`,

    ||p||_r^2=c_0^2+(1/2) sum_(nu representatives)
                   (1+|nu|^2)^r[c_(nu,c)^2+c_(nu,s)^2]. (6.2)

If the true target coefficients lie in their clipping intervals,
projecting each raw coefficient onto its interval reduces every
squared coordinate error. Thus it reduces the complete squared
Hilbert error to that target, pointwise on every completed seed.
Clipping may introduce bias; (6.2) controls the total error directly.

## 7. Public parameters and the sharp grid size

For `T>=2`, put

    S=T-1,       epsilon=exp(-S)/(16 Lchi),
    N=max(1,ceil((S+log(32 Lchi A_kappa))/b_kappa)),
    K=(2N+1)^d.

Then `N=O_(kappa)(1+T)` and (2.3) has tail at most `epsilon/2`.
All fixed constants below depend only on the public parameters.
Set

    Cstar=1+sum_(j=1)^m sqrt(V_j) Cint^j/j!
                                      +B_J Cint^J/J!,
    k=max(k0,ceil((4 E_d Cstar/epsilon)^(1/q))),
    M=k^d.                                           (7.1)

In contrast to T81 (6.1), `K` is absent from the expression for `k`.
Positive powers and public integer counts use the permitted
`exp,log,ceiling` operations. In particular `log k=O(1+T)` and

    k^d<=C exp(gamma T).                              (7.2)

First acquire the grid values and construct the actual `g` of (2.1).
For the base solve define the public polynomial factor

    D_N=sqrt(K)*(1+d*N^2)^(r/2),
    tau=epsilon/(4 E_d D_N),       Pbase=log(1/tau).

Use the known-profile solver at time one, scale `R=k`, and precision
`Pbase`, with its cutoff at least `N`. It returns `U_base` with

    ||U_base-S_1^kappa g||inf<=tau.

Every complex Fourier coefficient of this difference has absolute
value at most `tau`; summing its `K` weighted squared coefficients
therefore gives

    ||P_N(U_base-S_1^kappa g)||_r
                             <=D_N tau=epsilon/(4E_d). (7.3)

This is a deterministic paid solve, not a free coefficient oracle.
Since `log D_N=O_(d)(log(2+T))`, the extra accuracy increases only
the polynomial work factor. The solver parameters still satisfy
`Pbase+log k=O(1+T)` and its work is `C k^d(1+T)^a0`.

For each `j=1,...,m`, generate `M` independent samples of (5.8).
Before clipping, form the finite real polynomial

    p_raw=P_N U_base
                   +sum_(j=1)^m (1/(j! M)) sum_(a=1)^M P_N W_(j,a).

The segment `g+te=(1-t)g+tv` has sup norm at most `3/4`, so (5.5)
applies. Combine (7.3), (6.1), (5.5), and `Js>=q` to obtain

    (E||p_raw-P_N S_1^kappa v||_r^2)^(1/2)
      <=epsilon/(4E_d)
          +sum_(j=1)^m sqrt(V_j) Cint^j k^(-js-d/2)/j!
          +B_J Cint^J k^(-Js)/J!
      <=epsilon/(4E_d)+Cstar k^-q
      <=epsilon/(2E_d).                              (7.4)

Here `j>=1` and `k>=1` imply `js+d/2>=q`. No derivative of `v`
above its promised order is used or acquired. The higher Taylor
derivatives are derivatives of the fixed-time flow with respect to
its continuous initial function; (5.4) proves their boundedness.

The true target's real constant coefficient belongs to `[-1,1]`
and each other real coefficient to `[-2,2]`. Project the raw
coefficients onto these intervals and call the resulting polynomial
`p`. By (6.2), (7.4) still holds with `p`. Equations (4.1), (2.3)
and Minkowski now give the strong profile error

    (E||p-S_1^kappa v||inf^2)^(1/2)
      <=E_d*(epsilon/(2E_d))+epsilon/2
      =epsilon.                                      (7.5)

The deterministic analytic tail is the only omitted-mode error.
The random profiles themselves need not have a uniform analytic
strip on every tree. Their fixed Sobolev second moments and the
contractivity of `P_N` are enough for (7.4), uniformly in the cutoff.

## 8. Actual continuation, work, queries, and totality

Set `qhat=chi(p)`, using exactly the primitive function in T81
Section 7a. Since the actual time-one target is in its identity
interval, (7.5) implies

    (E||qhat-S_1^kappa v||inf^2)^(1/2)
                      <=Lchi epsilon=exp(-S)/16.       (8.1)

Every clipped array satisfies the inherited quantitative Gevrey bound
at `Rhat=NK`, sup bound `15/16`, and evaluator cost `O_d(K)`.
Run (2.2) at time `S`, precision `Pout=T+log(16)`, and this same
known profile. The returned real indexed polynomial `U_T` has
deterministic conditional error

    ||U_T-S_S^kappa qhat||inf<=exp(-T)/16

on every completed transcript. Actual comparison (2.4), (8.1) and
Minkowski therefore prove

    (E||U_T-S_T^kappa v||inf^2)^(1/2)
                           <=1/16+exp(-T)/16<=1/8.     (8.2)

The first term includes the base-solver error, finite-order bias,
all correlated-mode sampling errors, analytic tail and saturation.
The second term pays the final nonlinear evolution error.

The grid and base solve cost `C k^d(1+T)^a0`. By (5.10), the
fixed number `m` of derivative orders costs at most
`C k^d(1+K)` in expectation. Initial frequency enumeration,
coefficient extraction, allocation, updating, and clipping are paid
and absorbed in these bounds. For the final continuation,

    Rhat<=C(1+T)^(d+1),
    Wqhat<=C(1+T)^d,       Eout<=C(1+T),

so its deterministic work is at most
`C(1+T)^(a0+d^2+2d)`. Thus

    E Work_T<=C k^d(1+T)^a0+C k^d(1+T)^d
                              +C(1+T)^(a0+d^2+2d)
              <=C exp(gamma T)(1+T)^A,                (8.3)

with, for example, `A=a0+d^2+2d+2`. The array size and its paid
evaluation bound follow from the identical final solver interface
checked in T84 Section 10a.

Every new acquisition is either one of the `k^d` coarse values or
one of at most `j` values in a tuple sample. All other known-profile
evaluations use the saved explicit formula. Hence on every seed,

    Q_T<=k^d+sum_(j=1)^m j M
         =[1+J(J-1)/2] k^d<=C exp(gamma T).           (8.4)

Sharing all `K` Fourier outputs uses the same tuple values. The
covariance factorization, tree coefficient, and tuple are prepared
before that tuple's acquisitions; a null nonterminating preparation
makes no additional acquisitions. Prior completed samples still obey
the same deterministic total cap. Work is bounded in expectation,
not deterministically in the tree size.

All matrix, branch, interpolation, trigonometric, coefficient and
solver operations are Borel finite formulas on a completed finite
tree. Pivot branches are measurable, and positive square roots and
divisions occur only where proved legitimate. The tree law is
input independent and nonexplosive; finitely many samples are
requested at each fixed `T`. Equation (5.9) has a finite expectation,
so the whole program halts almost surely and has (8.3).
The finite real array is a Borel output; its embedding into `C(X)`
is continuous, making the sup-norm loss measurable. As in T81,
assign the zero array on the null nontermination set for probability
statements; no finite program is claimed to detect that set.

For arbitrary finite off-promise responses, optionally project each
acquired value to `[-1/2,1/2]`, leaving all promised transcripts
unchanged. The explicit interpolant and fixed-count solver remain
finite formulas even if their accuracy hypotheses fail. The
genealogy/covariance preparation and all loop counts are independent
of such hypotheses. Raw coefficients can be arbitrarily large but
finite in exact arithmetic; projection gives the same uniform
continuation interface. No random regularity test or unverified
convergence stopping rule controls the final work.

For `0<=T<=2`, use the deterministic fixed grid, fixed Fourier
cutoff and fixed Euler-count patch already proved in T81 Section 11
and T84 Section 13. It has sup error at most `3/32<1/8`, constant
query count and constant work, and returns a real Fourier polynomial.
Increasing the constants in (1.1) incorporates it. No vanishing-time
use of the positive-time covariance smoothing argument is required.

## 9. What an independent audit must check

The inherited solver and saturation are unchanged; the new material
that carries the query improvement is concentrated in these gates.

- **Every finite genealogy:** the leaf covariance inequality (3.3),
  including negative coefficients, zero edges and the `n=1` case.
- **An actual sampler:** finite semidefinite Cholesky, its zero-pivot
  rule, exact Gaussian covariance and the full nonlinear identity
  (3.5). The residual covariance must be `kappa(C-11^t/n)`.
- **The full field:** the Fourier heat norm (4.2), genuine Frechet
  derivative identification (5.4), and cutoff-independent remainder
  (5.5), all in the same fixed Hilbert norm.
- **Correlations and clipping:** (6.1) uses independence only between
  separate samples; (6.2) is the exact real-coordinate norm. Check
  the factor two and positive sine sign in (5.8).
- **Cost and oracle:** the `O(n^3)` covariance work has finite
  expectation by actual population moments, base precision has only
  logarithmic dependence on its polynomial mode factor, and only
  (8.4) acquires unknown data.

The natural first formal target is the actual Hilbert mean-square
identity for independent square-integrable random elements, its
bounded-projection version and a continuous embedding bound. An
algebraic inequality supplied with abstract second-moment assumptions
would cover less. Even a full proof of that target would leave
the branching covariance, PDE derivative, interpolation, analytic
tail, finite solver and query-transcript bridges conventional.
This file is not a Lean contract or an authorization to run experiments.

## 10. Primary attribution and bounded literature scope

I opened An--Henderson--Ryzhik's primary text, checked its diffusion
convention and Section 3.1's ternary-majority renewal construction,
and opened Etheridge--Freeman--Penington's primary abstract. AHR
credits EFP for the Allen--Cahn voting representation. The present
normalization is checked in Section 5. [AHR primary text](https://arxiv.org/html/2209.03435),
[EFP primary abstract](https://arxiv.org/abs/1607.07563).

The new covariance inequality, Gaussian decomposition, elementary
Fourier norm bound and Hilbert averaging calculation are proved
directly above. No unexamined external Banach approximation or
chaining theorem is substituted for these obligations. These two
source openings are attribution checks, not a priority search for
the resulting query theorem or sampling modification. The root is
conducting a separate bounded prior-work investigation.

## 11. Read provenance, task scope, and actual activity

The parent confirmed this task was explicitly dispatched with
`model=gpt-6-astra`, `reasoning_effort=max`, and `fork_turns=none`,
matching the configured research-role request. These are requested
settings only. This worker did not issue a model-setting call;
reading the setting does not switch a model. The actual backend
identity and reasoning effort are not independently exposed by this
worker's tools. No backend attestation or usage total is fabricated.

Read completely: the math-auto-research skill, defaults, routing,
execution instructions, general profile, T81, T84, R10b, T68, 04y,
and the run's initial context. Repository README and research README
were inspected for scope; current checkpoint excerpts and D29--D39
claim passages were inspected rather than claiming a fresh audit of
their entire history. An initial combined output was truncated;
all T81/T84 material used here was subsequently read in separate
complete line ranges. The optional Jerry profile was also inspected,
but the configured profile is General. The toolchain file was read
only for context and says `leanprover/lean4:v4.33.0`.

The supplied AGENTS instruction was read from the conversation. No
filesystem AGENTS file was returned by the scoped repository search.
The existing dirty working tree was inspected before writing. Only
this dedicated T87 file is owned or changed by this task; concurrent
root/other-worker changes are not attributed to this task.

The following SHA256 values were computed from the read files.
Paths without a leading slash are relative to the repository; `run/`
abbreviates `docs/research/runs/2026-09-28-dynamic-continuation/`.

| Read path | SHA256 |
| --- | --- |
| `/Users/michael/.agents/skills/math-auto-research/SKILL.md` | `135d3e4394a3cd65d8da11336382abeb01020b412d60a4509874bd4ca70c9e12` |
| `/Users/michael/.agents/skills/math-auto-research/config/defaults.json` | `790c96ba540ede32bd8a0fd5e86d79c479365e072736ff9961575ee680cb653e` |
| `/Users/michael/.agents/skills/math-auto-research/config/profiles/general.json` | `ef04dd919d4015574ad546f8de63f3c6e3707420d9f47f36030fd022cb8f8847` |
| `/Users/michael/.agents/skills/math-auto-research/config/profiles/jerry.json` | `cd36cdda2524e8b29287829903b94da9fd90047d6e5113aba4f84c3c2b36a2a8` |
| `/Users/michael/.agents/skills/math-auto-research/references/model-routing.md` | `1f3f034cc2c73e92acfcdc65970a35ca17cff84418652fc69b6824d0bb2e3673` |
| `/Users/michael/.agents/skills/math-auto-research/references/execution.md` | `ebcee187ef41c2c47a185f47f64fb864c5a89c55f43cfc74cae87a3da0c7c987` |
| `README.md` | `8c08dda7d5a80f237a61f5810876d5e1f7a29f4a3e58376da09392ae744f9cda` |
| `docs/research/README.md` | `2be6b034d1a9f644fb55b5eb7a83298acda40ce51da9322a7e7f84967fab38af` |
| `run/00-context.md` | `5eb738da9c77731713f83c10d3df79503217b76cc1cbb9043f485fbc1b7a26d3` |
| `run/08-next.md` | `8213a4382009f496407eec675ec19104d3b41e4162cc6fd00dbc2c224b7b0022` |
| `run/03-claims.md` | `6f57bc27a58902d290aac2ad042c4457b3fd5db10558cc8042c5536c536b0ee2` |
| `run/04y-all-positive-diffusivity-profile-complexity.md` | `2a62aaec24cb762ebe8ef213ce7bbbb2dbd56e3b7ced197a851736db913d9ba8` |
| `run/reviews/T81-fixed-burnin-all-diffusion-upper-proof.md` | `d9b249ed669897df319ca712fc4ad26625fc97e1a9b32b79eacaf497b290bae5` |
| `run/reviews/T84-all-diffusion-upper-independent-audit.md` | `39cd98fcf957badbe382123bd1960eac7fb99441114c9433bd9ee0ff2d256d7d` |
| `run/reviews/R10b-finite-burnin-derivative-sampling.md` | `23683587539ef2905e0679100325808ae3f6353a3782a4bb362b2d24252034f0` |
| `run/reviews/T68-finite-burnin-sampler-independent-audit.md` | `442b446ae523b220e34ddadcf8c23b181ce60104100fd27c7e8027524840ed9f` |
| `formal/lean-toolchain` | `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b` |

Actual activity comprised read-only file searches and source/context
inspection, `git status --short`, source hashing, the two primary
source openings, the conventional derivations above, and writing and
rereading this new proof candidate. A preliminary check for the target
path returned that it did not yet exist. The first file-creation patch
was rejected for a missing patch-prefix character and made no change;
the corrected patch created the file. No accepted ledger, run config,
frozen source, Lean source, code, numerical artifact, canvas, or global
model setting was edited. The final file hash is reported in the
handoff, not embedded in the file itself.

The bounded feasibility task is complete as a conventional candidate.
Promotion still requires an independent mathematical audit and root
shared-class/source/cost correspondence. No further mathematical
assumption is proposed as a gate to the theorem above.
