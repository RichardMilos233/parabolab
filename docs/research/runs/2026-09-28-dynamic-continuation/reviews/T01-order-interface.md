# T01 — order invariance and a finite convex moving interface

Date: 28 September 2026. Status: conventional theory proved below, subject to
the standard periodic Allen–Cahn existence, uniqueness, smoothing and comparison
theorems stated as analytical inputs. No numerical experiment, Lean declaration,
quadrature certificate, floating implementation or novelty claim is supplied by
this note. The construction and the degenerate endpoint audit were developed
jointly with the root researcher; this file records the detailed proof and the
computational contract. It follows the theory-first math-auto-research workflow.

## 1. Decision and exact scope

For `alpha<1`, the order interval between `alpha*g` and `g` contains a
genuinely evolving, infinite-dimensional class which admits an explicit finite
convex projection. At `alpha=1` the interval consists of g alone.
The useful coordinates are

    z = g(x)^2,                 u(t,x) = g(x) R(t,z).

For `9/10 <= alpha <= 1`, the class

    alpha <= R <= 1,       |R_z| <= 1/35,       |R_zz| <= 1/50

is invariant. A degree-n Bernstein polynomial in z satisfying finite linear
coefficient constraints lies in the same class. Every exact evolving target
has a feasible approximation with normalized spatial L2 error at most

    beta_n = (2/21)^(5/2)/(400 n) < 1/(140000 n),     n >= 1.

The degree-one member is a two-dimensional convex polygon. It contains the
exact initial data `alpha*g`, so this initial family needs no initialization
approximation. For `alpha < 1` these data evolve strictly in time on the
positive half-period. The class is deliberately structured around one
Jacobi arch and its symmetries; it is not an arbitrary periodic-data theorem.

The proof does **not** require evaluation of the unknown true flow in the
algorithm. Exact true-flow samples appear only as an approximation witness.
The producer estimates finitely many inner products from fresh local trees
and solves a known quadratic program.

An important distinction from the previous stationary three-sine construction
is that a feasible approximation of u does not imply `P_n u` is feasible, where
`P_n` denotes orthogonal projection. The correct safe error bound is therefore
the RMS recurrence in Section 10, not the old additive-tail squared recurrence.

## 2. Normalization and analytical inputs

The equation is

    u_t = (1/2) u_xx + u - u^3,       x in R/(L Z).

Use the Jacobi **parameter** `m = 1/20`, and define

    a = 2/21,       A0 = sqrt(a),       kappa = sqrt(40/21),
    K = K(sqrt(m)),                     L = 4K/kappa,
    ell = L/2,                         g(x) = A0 sn(kappa*x | m).

Here `K` is written in the modulus convention while `sn(.|m)` is written in
the parameter convention; this explicit distinction avoids changing the
underlying datum. The previous run already proves `4 < L < 5`. Direct Jacobi
identities give

    (1/2)g'' + g - g^3 = 0,
    g'^2 = g^4 - 2g^2 + C,              C = 80/441,
    0 <= g <= A0 on [0,ell],
    ||g'||_infinity = sqrt(80)/21 < 3/7 < 1/2,
    A0 < 1/3 < 2/5,                     a < 1/10,
    C = 2a - a^2 < 1/5.

The identities for sn, cn and dn used here and in Section 9 were checked
against [NIST DLMF 22.13](https://dlmf.nist.gov/22.13) and
[NIST DLMF 22.6](https://dlmf.nist.gov/22.6). All subsequent coefficient
identities follow by differentiation, and all inequalities below are analytic.

The analytical inputs are global bounded periodic solutions for bounded smooth
initial data, uniqueness, preservation of equation symmetries, the scalar
comparison principle, smoothness for positive times, and continuity under
smooth approximation on each fixed positive-time interval. These are standard
semilinear parabolic facts, not facts newly formalized in this note.

Normalize the spatial norm as

    ||v||_2^2 = (1/L) integral_0^L |v(x)|^2 dx.

For the numerical estimator, the previous local theorem is a separate input:
with raw rate 2, unchanged two-label probabilities, `0 < h <= 2/25`, and
terminal envelopes `|v| <= 2/5`, `|v'| <= 1/2`, the local Id tree is unbiased
for `S_h v` and its second moment is at most `1/4` at every starting position.
All terminals in the main polynomial constructions below are C-infinity, so
no extension of that theorem to nonsmooth terminals is needed there. The
separate cubic-spline fallback in Section 12 uses C2 terminals.

## 3. The larger order/concavity cone

First separate a simple broad invariant statement from the more structured
computational class. On `[0,ell]`, consider C2 arches v with

    alpha*g <= v <= g,        v(0) = v(ell) = 0,        v'' <= 0,

whose odd periodic extension is C2. Midpoint reflection is not needed for this
particular statement.

### 3.1 Order

The stationary function g is a supersolution. The fixed lower function
`alpha*g` satisfies

    (1/2)(alpha*g)'' + alpha*g - (alpha*g)^3
      = alpha(1-alpha^2)g^3 >= 0

on the positive half-period, so it is a subsolution. Oddness is preserved by
uniqueness and the odd reaction, giving zero Dirichlet values at 0 and ell.
Comparison on that interval proves preservation of the order interval.

### 3.2 Concavity

For positive times let `w = u_xx`. In the positive half-period,

    w_t = (1/2)w_xx + (1-3u^2)w - 6u u_x^2.

Here `u >= 0`, and the source is nonpositive. Smooth odd extension gives
`w(t,0) = w(t,ell) = 0`. The maximum principle, with the harmless bounded
zeroth-order coefficient removed by an exponential factor if necessary,
preserves `w <= 0`. Approximation or continuity at time zero handles C2 data.

### 3.3 Derivative envelope

Concavity makes `u_x` nonincreasing on `[0,ell]`. The shared zero values and
`u <= g` imply, by one-sided difference quotients,

    u_x(0) <= g'(0),            u_x(ell) >= g'(ell).

Consequently

    |u_x| <= sqrt(80)/21 < 1/2.

The upper order bound alone is not a derivative bound: concavity is essential
to this argument. The next sections construct a smaller invariant class with
finite coefficient tests, rather than claiming this whole cone has already
been approximated with the same small dimension.

### 3.4 The initial family is nonstationary

For `u(0)=alpha*g` and `alpha<1`,

    u_t(0,x) = alpha(1-alpha^2)g(x)^3 > 0,    0<x<ell.

The time derivative solves the linear equation
`(u_t)_t = (1/2)(u_t)_xx + (1-3u^2)u_t` with zero endpoint values, so the
strong maximum principle gives `u_t(t,x)>0` for every finite `t>0` and
interior x. Equivalently, semigroup order already gives monotonicity in t.
The field therefore changes in time; the stationary case is exactly
`alpha=1` within this one-parameter initial family.

## 4. A regular coordinate at both turning points

Let `R0 in C2([0,a])` and set `u0(x)=g(x)R0(g(x)^2)`. Such u0 has oddness,
half-period sign reversal and reflection symmetry about the positive peak.
All are preserved by the PDE. On the first quarter-period, `z=g(x)^2`
increases from 0 to a. Define R there by

    R(t,z) = u(t,x(z))/g(x(z)).

The symmetries make the same definition consistent on the remaining quarters.
There are no imposed extra boundary values for R at `z=0,a`.

For smooth initial R0 and positive t, R extends smoothly to both endpoints:

* At a zero of g, both u and g are smooth odd functions, g has a simple zero,
  and u/g is smooth and even. Locally z is a smooth positive constant times
  `x^2`, with an invertible smooth change of the squared coordinate.
* At the peak of g, u/g is smooth and even about the peak. The difference
  `a-z` is a smooth positive constant times the squared distance from that
  peak, again with an invertible change of squared coordinate.

The elementary smooth even-function factorization through `x^2` follows from
Taylor's formula with remainder (or repeated Hadamard factorization). Thus
the apparent degeneracies do not create a singular R for these symmetric
solutions. For merely C2 R0, use the preserving polynomial approximation in
Section 7, pass to the Allen–Cahn solution, and apply positive-time smoothing;
the derivative inequalities then pass to the limit. This supplies the C2
version without assuming unjustified differentiability at the degenerate
endpoints at time zero.

The preserving Bernstein polynomials are auxiliary approximating initial
data, not an assertion that the original R0 is already a polynomial. Each
approximant has its own exact PDE solution. Continuous dependence identifies
their limit with the solution from the original R0; positive-time smoothing
permits passage of the first and second z-derivative bounds at each positive
time. The stated initial bounds already hold at time zero.

## 5. Exact equation and endpoint maximum principle

Put

    P(z) = z^2 - 2z + C,
    A(z) = 2z P(z),
    B(z) = 5z^2 - 8z + 3C,
    f(R) = R-R^3.

The letters A0 and A(z) distinguish the fixed amplitude from the diffusion
coefficient. Since `z'=2gg'` and `z''=6z^2-8z+2C`, direct substitution gives

    R_t = A R_zz + B R_z + z f(R).                         (5.1)

On `[0,a]`, `P >= 0`, `A >= 0`, and `A(0)=A(a)=0`. The endpoint derivatives
are

    A'(0)=2C,       B(0)=3C,
    A'(a)=4a(a-1),  B(a)=2a(a-1).

The vanishing diffusion and inward drifts allow the elementary maximum
principle on the **closed** interval. At a left-endpoint maximum, the inward
derivative is nonpositive; a nonnegative drift therefore contributes a
nonpositive term. At a right-endpoint maximum, that derivative is nonnegative,
and a nonpositive drift has the same effect. At endpoints the A times second
derivative term vanishes. Interior maxima use the usual first-/second-derivative
test. A strict barrier, followed by a limit, handles equality.

This argument is applied only after the endpoint regularity above is known.
It does not silently replace the degenerate equation by one with artificial
Dirichlet or Neumann boundary conditions.

## 6. Invariance of the R class

Fix `9/10 <= alpha <= 1`. Define

    C_alpha = {R in C2([0,a]):
                 alpha <= R <= 1,
                 |R_z| <= 1/35,
                 |R_zz| <= 1/50}.

The inequalities are pointwise over the whole interval.

### 6.1 Range

Order comparison in Section 3 gives `alpha <= R <= 1`, including endpoint
limits. Alternatively, constants alpha and 1 are respectively a subsolution
and supersolution of (5.1), and B points inward at both endpoints.

In this range,

    0 <= f(R) <= 1/5,       f'(R)=1-3R^2 <= 0,       |R|<=1.

For example f is decreasing on `[9/10,1]`, and
`f(9/10)=171/1000<1/5`.

### 6.2 First derivative

For `p=R_z`, differentiation of (5.1) gives the exact equation

    p_t = A p_zz + (A'+B)p_z
          + [B'+z(1-3R^2)]p + f(R).                       (6.1)

The drift `A'+B` has endpoint values

    5C > 0,                  6a(a-1) < 0.

Its zeroth-order coefficient obeys

    B'+z(1-3R^2) <= 10z-8 <= -7,

because `z<=a<1/10`. At the barrier `p=1/35`, the reaction plus source is at
most `-7/35+1/5=0`. At `p=-1/35` it is at least `7/35-1/5=0` (in fact the
nonnegative source makes the lower barrier easier). The closed-interval
maximum principle therefore preserves `|p|<=1/35`.

### 6.3 Second derivative

For `q=R_zz`, differentiating once more gives

    q_t = A q_zz + (2A'+B)q_z
          + [A''+2B'+z(1-3R^2)]q
          + (12-6R^2)p - 6zR p^2.                        (6.2)

In particular the coefficient of p in the source is `12-6R^2`; it includes
both differentiated reaction contributions. The drift `2A'+B` has endpoint
values

    7C > 0,                  10a(a-1) < 0.

The coefficient of q satisfies

    A''+2B'+z(1-3R^2) <= 32z-24 < -20.

Using the already proved p bound,

    |(12-6R^2)p - 6zR p^2|
       <= 12/35 + 3/(5*35^2)
        = 2103/6125 < 2/5.

Thus the constants `q=+/-1/50` are upper/lower barriers, since
`20/50=2/5`. This proves invariance of C_alpha for smooth data. The C2
extension follows from Section 7 and the approximation argument in Section 4.

### 6.4 The terminal envelope and concavity

For every R in C_alpha and `v=gR(g^2)`,

    |v| <= A0 < 2/5,
    v' = g'[R+2zR_z],
    |v'| <= (3/7)(1+2a/35) = 739/1715 < 1/2.              (6.3)

This is an exact global derivative bound, independent of Monte Carlo noise.
The class in fact lies in the concavity cone. Directly,

    v''/(2g) = -(1-z)R + B R_z + A R_zz       (0<x<ell).

On `[0,a]`, `|B|<3/5` (B is decreasing there), `0<=A<1/25`, and
`(1-z)R>=(9/10)^2`. Hence

    v''/(2g) <= -81/100 + 3/175 + 1/1250 < 0.

The strict sign is only asserted inside the positive half-period; the smooth
odd extension has `v''=0` at its zeros. This confirms that the computational
class retains the intended shape as well as the order and derivative bounds.

## 7. A finite convex Bernstein hierarchy

For integer `n>=1`, let

    b_{k,n}(s) = binomial(n,k) s^k (1-s)^(n-k),
    R_c(z) = sum_{k=0}^n c_k b_{k,n}(z/a),
    v_c(x) = g(x) R_c(g(x)^2).

Define the coefficient polytope D_(n,alpha) by

    alpha <= c_k <= 1                                  (0<=k<=n),
    |c_(k+1)-c_k| <= a/(35n)                           (0<=k<n),
    |c_(k+2)-2c_(k+1)+c_k| <= a^2/[50n(n-1)]          (0<=k<n-1).

The last line is omitted when n=1. Every constraint is linear after replacing
an absolute value by its two inequalities. The polytope is compact, convex
and nonempty, containing all constant coefficient vectors in `[alpha,1]`.

Positivity and partition of unity of the Bernstein basis give the range
bound. The differentiation identities give

    R_c'  = (n/a) sum Delta c_k b_(k,n-1)(z/a),
    R_c'' = [n(n-1)/a^2] sum Delta^2 c_k b_(k,n-2)(z/a).

Therefore `R_c in C_alpha` for every feasible vector. The image

    K_(n,alpha) = {v_c : c in D_(n,alpha)}

is a compact convex subset of the `(n+1)`-dimensional linear space

    V_n = span{g, g^3, ..., g^(2n+1)}.

The dimension is exactly n+1: a polynomial in `z=g^2` which vanishes after
multiplication by g on the positive quarter-period vanishes on the whole
interval `(0,a)`, and is the zero polynomial. The constraints preserve the
odd extension, half-period sign reversal, order, concavity and envelope
(6.3) for every possible projected Monte Carlo output.

### 7.1 Feasible witness for every member of C_alpha

For an arbitrary `R in C_alpha`, take

    c_k = R(ak/n).                                      (7.1)

The range and first-difference constraints follow from the fundamental
theorem of calculus. With `d=a/n`, the second difference has the integral
representation

    R(z+2d)-2R(z+d)+R(z)
      = integral_0^d integral_0^d R''(z+s+t) ds dt.

It is at most `a^2/(50n^2)` in absolute value, which is no larger than the
coefficient constraint for `n>=2`. Thus (7.1) is feasible.

The Bernstein approximants in (7.1) converge in C2 for C2 input. Indeed the
first- and second-derivative formulas are Bernstein averages of first and
second divided differences; their integral forms and uniform continuity of
R' and R'' give the stated convergence. These approximants justify the
smooth approximation used to extend Section 6 from smooth to C2 data.

### 7.2 Uniform approximation error

For fixed `s=z/a`, let `Y~Binomial(n,s)` and write the witness polynomial as

    R_c(z) = E R(aY/n).

The first-order Taylor term has zero expectation, while `|R''|<=1/50`.
Since `Var(aY/n)=a^2 s(1-s)/n`,

    |R_c(z)-R(z)| <= a^2 s(1-s)/(100n)
                   <= a^2/(400n).

Multiplication by `|g|<=sqrt(a)` yields both a supremum and normalized L2
bound

    ||v_c-gR(g^2)||_infinity, ||v_c-gR(g^2)||_2
        <= beta_n := a^(5/2)/(400n).                     (7.2)

Here `beta_1^2=1/(5000*21^5)=1/20420505000`, hence
`beta_n < 1/(140000n)` by the exact integer comparison
`20420505000 > 140000^2`.

Because the true R stays in C_alpha, (7.2) holds for every time with one
fixed n. It is a uniform approximation result for the evolving unknown
solution. It is not a measured tail at a finite set of times or positions.

### 7.3 The two-dimensional member

For n=1,

    R_c(z)=c_0(1-z/a)+c_1 z/a,
    alpha<=c_0,c_1<=1,             |c_1-c_0|<=a/35,
    v_c=c_0 g + (c_1-c_0)g^3/a.

No second-difference condition is needed because `R_c''=0`. This small
convex polygon already has the all-time residual `beta_1<1/140000`.
The fixed residual is not zero: to request arbitrarily small error one must
increase n or establish a sharper target-dependent approximation theorem.

## 8. Computable metric projection without a flow oracle

Set

    phi_k(x)=g(x)b_(k,n)(g(x)^2/a),
    G_ik = (1/L) integral_0^L phi_i(x) phi_k(x) dx.

The Gram matrix G is positive definite by the independence argument in
Section 7. All of its inputs are known: the fixed g, its period and n.
Its entries can be computed once by deterministic special-function
integration or certified quadrature. No evolving true solution is involved.

Given a current feasible coefficient vector c, use fresh independent
uniform spatial points `X_l on [0,L)` and local raw trees `H_l` terminating
in the stored function `v_c` and its exact derivative. Form

    b_hat_k = (1/N) sum_{l=1}^N H_l phi_k(X_l).

The next coefficient vector is the unique minimizer

    minimize_d  d^T G d - 2 b_hat^T d
    subject to d in D_(n,alpha).                         (8.1)

This is a finite strictly convex quadratic program. For n=1 it is a
two-variable polygon problem. For general n it has n+1 variables and O(n)
linear inequalities. The objective is exactly the metric projection onto
K_(n,alpha) of the orthogonal coefficient estimator; it is not coordinatewise
clipping unless the metric and constraints happen to permit that operation.

The true-flow values in (7.1) prove that a close feasible element exists.
They are never supplied to (8.1). At initialization, values of the *given*
R0 may be used to form a feasible witness. In particular for `R0=alpha`,
the exact initial vector is the known constant vector `(alpha,...,alpha)`.

Finite arithmetic, quadrature error and approximate QP termination require
additional explicit tolerances in an implementation. The theorem here uses
the exact known Gram matrix and exact metric projection. Computability of
the finite problem is not a claim that those tolerances have been certified.

## 9. Independent check of the order-interval contraction constant

This section verifies the spectral constant used in the error contract.
Let

    psi(x)=sn(kappa*x | m) dn(kappa*x | m),     0<x<ell.

It is positive in the open interval and has simple zero endpoints.
Differentiating the Jacobi identities gives

    (sn*dn)'' = -(1+4m)(sn*dn) + 6m sn^2(sn*dn),
    [- (1/2) d_x^2 - 1 + 3g^2] psi = (1/7) psi.

For a compactly supported smooth w in the positive half-period, integration
by parts therefore gives the ground-state identity

    integral [ (1/2)w'^2 + (-1+3g^2-1/7)w^2 ]
      = (1/2) integral psi^2 [(w/psi)']^2 >= 0.

Density extends the inequality to `H_0^1(0,ell)`, avoiding any unsupported
boundary manipulation of `w/psi`. If u and v both lie in the order interval,
then on this half-period

    u^2+uv+v^2 >= 3alpha^2 g^2.

Consequently the difference energy has coercivity at least

    mu = 1/7 - 3(1-alpha^2)a = (2alpha^2-1)/7
         >= 31/350 > 0.                                 (9.1)

Odd extension gives the same normalized full-period inequality. Applying it
to two solution trajectories in the order interval yields

    ||S_h v-S_h w||_2 <= exp(-mu h)||v-w||_2.             (9.2)

The argument does not require p or q bounds for the contraction itself;
those bounds ensure the computational interface and approximation theorem.

## 10. The correct horizon-uniform statistical recurrence

Let the true solution be `u_j=S_(jh)u0` and the approximation use (8.1) with
fixed `0<h<=2/25`, degree n and N roots per slab. Write

    d=n+1,        rho=exp(-mu h)<1,
    sigma^2=d/(4N),
    e_j=(E||v_j-u_j||_2^2)^(1/2).

Conditional on all earlier samples, an orthonormal basis of V_n gives an
unbiased coefficient estimator of `P_n S_h v_(j-1)`. Its variance trace is
at most `d/(4N)`: apply the uniform local second-moment bound pointwise and
integrate each squared orthonormal basis function. Correlations between
coefficients from a shared tree are allowed. A Gram-coordinate computation
of (8.1) is exactly the same estimator and metric projection.

Let `Q_j=Pi_K(u_j)=Pi_K(P_n u_j)`, where `Pi_K` is the exact Hilbert metric
projection. The approximation witness proves `||Q_j-u_j||_2<=beta_n`.
Metric projection is nonexpansive, conditional centering eliminates the
cross term before projection, and (9.2) bounds the deterministic discrepancy.
Minkowski's inequality in the joint probability/spatial L2 space therefore
gives

    e_j <= sqrt(rho^2 e_(j-1)^2 + sigma^2) + beta_n.       (10.1)

The approximation defect is needed only for the deterministic true target
u_j. The random intermediate exact flow `S_h v_(j-1)` need only stay in the
order interval for contraction, and the stored terminal needs the local
moment envelope. Thus a sharper approximation theorem for an analytic true
target does not require projected terminals to preserve that stronger
all-derivative class. Preservation of C_alpha is sufficient here.

The witness `Q_n u_j` from Section 7 is generally different from both
`P_n u_j` and `Pi_K u_j`. Merely knowing that this witness is feasible does
not justify replacing (10.1) by an additive-beta_n-squared recurrence.

The scalar map on the right of (10.1) has the positive fixed point

    E_* = [beta_n + sqrt(rho^2 beta_n^2 + (1-rho^2)sigma^2)]
            / (1-rho^2)
        <= beta_n/(1-rho) + sigma/sqrt(1-rho^2).           (10.2)

It is increasing, so all times satisfy `e_j<=max(e_0,E_*)`. For exact
`u0=alpha*g`, `e_0=0`. For a general supplied `R0 in C_alpha`, the initial
Bernstein witness gives `e_0<=beta_n<=E_*`.

This is an ensemble RMS bound at slab endpoints in normalized spatial L2.
It is not a pointwise or high-probability statement, and the method is biased
by its projection. The constants do not grow with the number of slabs.
For a final shorter slab, use that slab's own recurrence; a uniform lower
bound on slab length is needed if one insists on one fixed invariant radius
with the same N and beta. Equivalently, use an equal partition of the requested
horizon or retain fixed-length checkpoints; do not silently apply the
fixed-h formula to arbitrarily tiny last slabs.

## 11. Dimension and computational cost

For a prescribed RMS tolerance epsilon, the sufficient choices

    n >= max(1, ceil[2 beta_1/(epsilon(1-rho))]),
    N >= ceil[(n+1)/(epsilon^2(1-rho^2))]                 (11.1)

make each of the two terms on the right of (10.2) at most epsilon/2.
Neither n nor N depends on the number of slabs. The number of roots up to
the checkpoint `T=Jh` is `JN`, hence linear in T at fixed tolerance and h.
The previous ternary domination bounds the expected node count per root
by `(3 exp(4h)-1)/2`; multiply it by JN for a conservative total node bound.
Setup of the known Gram matrix, terminal evaluation and QP solution are
additional costs. No wall-clock performance is claimed.

The degree-one residual is unusually small because the z interval has
length a=2/21 and the invariant curvature of R is at most 1/50. This does
not mean the true profile is stationary: it means its changing shape can be
approximated by a known two-function span. For very small epsilon, the
hierarchy makes the dimension-cost tradeoff explicit, at the conservative
rate `beta_n=O(1/n)`. An improved polynomial approximation theorem may give
better rates for smoother targets; no such improvement is required here.

## 12. Broader ratio-Lipschitz alternative, kept separate

The following independently audited fallback covers a broader class, but
with a much larger dimension for the same approximation tolerance. It is
not needed for the preceding two-dimensional construction.

Write `u=g r(t,x)` with r even and ell-periodic. Suppose

    alpha<=r<=1,       |r_x|<=eta=1/20.

For smooth r these properties are invariant. On `0<x<ell`,

    r_t=(1/2)r_xx + (g'/g)r_x + g^2(r-r^3).

The ratio extends evenly at the endpoints, so `p=r_x` has zero endpoint
values. Its equation is

    p_t=(1/2)p_xx+(g'/g)p_x
        + [(g'/g)' + g^2(1-3r^2)]p
        + 2gg'(r-r^3).

The apparent singular drift causes no problem at a nonzero extremum of p:
the maximum is interior and `p_x=0`. Its coefficient and forcing satisfy

    (g'/g)' + g^2(1-3r^2)
        <= -2+2g^2 <= -16/9,
    |2gg'(r-r^3)| <= 2/35.

The eta barriers have strict inward margin
`(16/9)(1/20)-2/35=2/63>0`. Smoothing or preserving approximation extends
the argument to the C2 terminals used below. This class gives
`|u'|<=3/7+(1/3)(1/20)=187/420<1/2`.

For an integer `M>=4`, set `Delta=ell/M` and use the centered cardinal
cubic spline

    B(s)=(4-6|s|^2+3|s|^3)/6       for |s|<=1,
         (2-|s|)^3/6              for 1<=|s|<=2,
         0                        otherwise.

The ell-periodic basis is `B_j(x)=sum_k B(x/Delta-j-kM)`. Impose the finite
convex constraints

    alpha<=c_j<=1,
    c_j=c_(-j mod M),
    |c_j-c_(j-1)|<=eta Delta.

Then `r_M=sum_j c_j B_j` is even, ell-periodic, takes values in `[alpha,1]`
and has derivative at most eta. The derivative is a partition-of-unity
average of adjacent coefficient differences divided by Delta. Thus
`v_M=g r_M` is C2 and meets the exact envelope. Symmetry leaves
`floor(M/2)+1` independent coefficients.

The feasible witness `c_j=r(j Delta)` has uniform approximation

    ||g(r-r_M)||_2 <= A0 eta Delta/sqrt(3),
    delta_M^2 < 1/(2016 M^2).

Indeed, the cardinal cubic moments are
`sum B(s-j)=1` and `sum (j-s)^2 B(s-j)=1/3`, verifiable directly on
`0<=s<=1`; apply Cauchy–Schwarz to the Lipschitz error. Use `ell<5/2` for
the displayed rational bound. The corresponding weighted-Gram projection
is again a finite convex QP, with the same statistical recurrence (10.1).

For this fallback, the local mean correspondence for C2 terminal data follows
by writing the six-field mild identities first on `[epsilon,h]`, where the
PDE solution is smooth, and sending epsilon to zero. The values and first
derivatives converge uniformly to their terminal data, and the six fields
and polynomial reactions stay bounded by the standard parabolic derivative
bound. The already established local envelope moment justifies the separate
tree expectations. This extension is unnecessary for the main polynomial
construction.

Only a uniform Lipschitz bound is assumed in this broader class. It does
not supply a uniform bound on `r_xx`, so a second-order mesh error cannot
be claimed for the whole class. If a separate bound `|r_xx|<=M2` is
available, cancellation of the first cardinal moment instead gives
`||g(r-r_M)||_2<=A0 M2 Delta^2/6`.

## 13. Claim boundary and remaining work

Conventionally established here:

1. The order/concavity cone is invariant and gives the derivative envelope.
2. The transformed C2-R class is invariant, with a detailed audit of both
   degenerate endpoints and both differentiated equations.
3. A finite convex Bernstein family lies inside that class and approximates
   every true trajectory uniformly in time with the explicit beta_n.
4. The projection is a known finite QP driven by local estimator samples,
   and its safe statistical recurrence has a horizon-independent radius.
5. The order-interval spectral constant is mu=(2alpha^2-1)/7.

Still outside the claim of completed verification:

* A Lean encoding of these analytical and stochastic statements; algebraic
  scalar lemmas alone would be only partial coverage.
* A floating producer, certified Gram evaluation, QP error accounting,
  implementation/runtime evidence, or empirical performance comparison.
* Arbitrary periodic input profiles, removal of the enforced symmetries,
  or arbitrary-jet interface closure.
* A literature-supported methodological novelty claim. The present result
  is a concrete project-specific construction and proof, not evidence that
  projection continuation, Bernstein shape preservation, or ground-state
  transforms are new techniques.

The scalar, polynomial and convex-projection interfaces are now sufficiently
specified for independent review and a subsequent theory-matched formal or
numerical implementation. Any implementation which changes the raw local
law, estimates the unknown true R instead of the stored terminal, replaces
the metric QP by unproved clipping, or omits its arithmetic error budget
would need a separate correspondence justification.

## 14. Conditional exponential refinement for an analytic true target

This appendix is a proved approximation implication, **conditional** on the
additional true-target derivative bound below. It is not used in Sections
1–11 and does not establish that derivative bound. The root researcher has
assigned its separate invariant-class audit to T02.

Use the fixed lower barrier `alpha0=9/10` in the feasible sets, allowing the
initial constant R0 to be any value in `[9/10,1]`. Suppose, in addition to
the C2 bounds already proved, that the true target satisfies

    |partial_z^k R(t,z)| <= M_k := (k!/35) 2^(k-1)
    for every k>=1, t>=0, 0<=z<=a.                        (14.1)

No such higher-derivative bounds are required of the projected polynomial
or its intermediate exact flow in the statistical recurrence.

For `n>=2`, let T_n be the Taylor polynomial of R at z=0 of degree n.
Taylor's theorem applied separately to R, R' and R'' gives

    ||T_n-R||_infinity     <= E0 := (a/35)(2a)^n,
    ||T_n'-R'||_infinity   <= E1 := ((n+1)/35)(2a)^n,
    ||T_n''-R''||_infinity <= E2 := [n(n+1)/(35a)](2a)^n.

These follow from the single bound M_(n+1); no complex-analytic extension
or evaluation of the true derivatives by the algorithm is assumed.

Set

    kappa_n = 50 E2 = 15 n(n+1)(4/21)^n,
    theta_n = kappa_n/(1+kappa_n),
    Q_n = (1-theta_n)T_n + theta_n*(19/20).               (14.2)

For n>=2, `kappa_n >= max(20E0,35E1,50E2)`. Mixing the true R with 19/20
creates range slack `theta_n/20`, first-derivative slack `theta_n/35`,
and second-derivative slack `theta_n/50`. The perturbation in replacing
R by T_n is respectively bounded by `(1-theta_n)Ej`; the definition of
theta_n makes each perturbation no larger than its slack. Consequently

    9/10<=Q_n<=1,       |Q_n'|<=1/35,       |Q_n''|<=1/50.

The function `gQ_n(g^2)` is therefore feasible in the pointwise polynomial
class of degree n. Its target error is bounded by

    delta_n <= sqrt(a)[E0+theta_n/20]
             <= sqrt(a)[2/735+(3/4)n(n+1)](4/21)^n
             <= (1/3)n(n+1)(4/21)^n
             <= (2/3)(8/21)^n.                           (14.3)

For the last inequality, `n(n+1)<=2^(n+1)` for n>=2, by induction.
This approximation is a proof witness, exactly as in Section 7. It does
not prescribe extracting true Taylor coefficients in the producer.

For an alpha-dependent lower barrier strictly larger than 9/10, replace
the anchor by `(1+alpha)/2` and choose

    kappa_n=max(2E0/(1-alpha),35E1,50E2).

The fixed anchor 19/20 would be invalid when alpha>19/20. The special
case alpha=1 is already represented exactly by the constant polynomial 1.

### 14.1 A finite convex projection for this witness

The Bernstein coefficient polytope of Section 7 is a sufficient subset of
the pointwise polynomial constraints; (14.2) is not asserted to satisfy
that particular coefficient polytope. Use instead

    P_n = {Q polynomial of degree <= n:
               9/10<=Q<=1, |Q'|<=1/35, |Q''|<=1/50
               on [0,a]}.

It is a compact convex set in n+1 coefficients. Its six pointwise
constraints are nonnegativity of the polynomials

    Q-9/10, 1-Q, 1/35-Q', 1/35+Q', 1/50-Q'', 1/50+Q''.

They admit finite semidefinite representations. A nonnegative polynomial
on `[0,a]` can be written `s0(z)+z(a-z)s1(z)` with s0,s1 sums of squares;
each sum of squares is a polynomial Gram form with a positive semidefinite
matrix. This is the univariate interval representation, not a generic
multivariate positivity relaxation; see the proof and Gram conversion in
[Stein, Ozdaglar and Parrilo, Propositions 4.1–4.2](https://web.mit.edu/asuman/Desktop/asuman/www/documents/cdc2008CE.pdf).

A sufficient finite bound for polynomials of degree <=n is
`deg(s0)<=2n`, `deg(s1)<=2n-2`. To see this without requiring optimal
degree bounds, factor the polynomial into nonnegative real linear factors
on the interval, squares of its interior real-root factors, and positive
quadratics. For example

    z = z^2/a + z(a-z)/a,
    a-z = (a-z)^2/a + z(a-z)/a.

The cone `s0+d s1`, with `d=z(a-z)`, is closed under multiplication because

    (s0+d s1)(t0+d t1)
      = (s0 t0+d^2 s1 t1) + d(s0 t1+s1 t0),

and sums/products of sums of squares remain sums of squares. Counting
factor degrees gives the displayed sufficient bound. Thus each constraint
uses known finite Gram matrices of size at most n+1 and n. Matching their
coefficients to the six polynomials is linear. The positive quadratic
metric projection objective can likewise be represented with a convex
quadratic epigraph, so this is a finite convex optimization problem.

Under (14.1), (14.3) permits n=O(log(1/epsilon)) at fixed h and mu. The
variance trace remains `(n+1)/(4N)`, and Section 10 therefore yields root
count `O(T epsilon^(-2) log(1/epsilon))` at fixed h and mu. This conditional
statement concerns root count, not certified full arithmetic runtime:
terminal/basis evaluation, Gram conditioning, semidefinite optimization,
bit complexity and approximate projection tolerances remain additional
costs. Establishing (14.1) is the outstanding analytic hypothesis of this
appendix; its approximation and projection construction do not prove it.

## 15. D5 — the same raw rate-two obstruction for the entire new class

This section extends, without changing their mechanism or measure conventions,
the earlier run's [C9 proof](../../2026-09-27-slab-continuation/04-theory.md)
and the independently reviewed proofs in
[old T01, Section 10](../../2026-09-27-slab-continuation/reviews/T01-interface-theory.md)
and [old T02, Section 9](../../2026-09-27-slab-continuation/reviews/T02-constructive-theory.md).
Those three files were read for this audit; they are not modified here.

**Claim.** Fix any terminal

    v(x)=g(x)R0(g(x)^2),       9/10<=R0<=1,

from the new C2 class (in particular any `v=alpha*g`, `9/10<=alpha<=1`).
For the unsplit original derivative-coded raw estimator with common rate
lambda=2 and its unchanged two-label probabilities 1/2, the extended Id
second moment is infinite at every starting position and every horizon
`T>=7/2`.

This is a statement about the fixed terminal v and the original full-horizon
tree. The evolving exact PDE solution is not substituted for that terminal
at intermediate times. The comparison does not assert a failure for every
rate or every proposal, or a failure of the PDE or pathwise termination.

### 15.1 The extended positive moment identities

Use `M_I,M_D,M_0,M_1,M_2,M_3` for the nonnegative extended squared moments
of `(Id,Dx,F0,F1,F2,F3)`, and put `Y_c(t,x)=exp(-2t)M_c(t,x)`. The last
field is exactly `Y_3=36`, because `f'''=-6` and its branch products vanish.

First-branch decomposition, followed by Tonelli, gives nonnegative mild
Volterra identities, valid even when moments take the value infinity.
Dropping the derivative-code contributions leaves the lower system written
formally as

    (Y_0)_t >= (1/2)(Y_0)_xx + exp(2t)Y_0Y_1,
    (Y_1)_t >= (1/2)(Y_1)_xx + exp(2t)Y_0Y_2,
    (Y_2)_t >= (1/2)(Y_2)_xx + 36exp(2t)Y_0.              (15.1)

These displays abbreviate the corresponding positive mild inequalities;
they do not take derivatives of infinite moment fields. Equivalently,
derive the identities for nonnegative tree expansions and take their
monotone limit. The scalar coefficient squares and the raw label
probabilities are exactly those of the preceding proof.

### 15.2 Uniform seed for all new terminals

Since `|v|>= (9/10)|g|` and `v^2<=g^2<=2/21`,

    f(v)^2=v^2(1-v^2)^2
       >= (81/100)(19/21)^2 g^2
        > (16/25)g^2.                                   (15.2)

The last rational comparison is
`29241/44100 > 28224/44100`. As proved in the previous run, the time-one
periodic Brownian kernel relative to ordinary Lebesgue measure dy is
strictly larger than `1/192`, and

    integral_0^L g(y)^2 dy > 1/40.

For completeness, `L<5` supplies a Gaussian image of displacement less
than 5/2, so the density is greater than `exp(-4)/3>1/192` using `e^2<8`.
Each of two intervals of length 1/5 about the positive/negative peaks has
`|g|>1/4`, because `A0>3/10` and `|g'|<1/2`; their total length is 2/5.
No normalized `dy/L` factor belongs in this heat-kernel estimate.

Keeping only the terminal heat contribution in Y_0 and using (15.2) gives

    Y_0(1,x) >= P_1[f(v)^2](x) > a0 := 1/12000            (15.3)

uniformly in x. The other restarted fields are nonnegative, so their
positive initial lower bounds may be discarded.

### 15.3 Positive Picard comparison and finite scalar explosion

Starting at time one, the heat semigroup preserves spatial constants.
Compare each Picard iterate of the spatially constant lower system with
the restarted nonnegative Volterra inequalities (15.1). Positivity gives
the comparison for every finite lower iterate, and monotone convergence
gives the lower solution up to its blow-up time, without assuming actual
moment finiteness.

With

    s(t)=(exp(2t)-exp(2))/2,

the constant lower system is

    A_s=AB,       B_s=AD,       D_s=36A,
    (A,B,D)(0)=(a0,0,0).

The letter D here names the third scalar comparison component, not the
derivative-code moment M_D. Set `Z_s=A`, `Z(0)=0`. Direct integration gives

    D=36Z,       B=18Z^2,       A=a0+6Z^3,
    Z_s=a0+6Z^3.

Its explosion time obeys

    s_* = integral_0^infinity dZ/(1/12000+6Z^3)
        <= 12000/30 + integral_(1/30)^infinity dZ/(6Z^3)
         = 400+75 = 475.                                 (15.4)

The corresponding physical time satisfies

    t_*=(1/2)log(exp(2)+2s_*) < (1/2)log(958) < 7/2.

Here `exp(2)<8`. Also `e>65/24>27/10` by the exponential series, and
`(27/10)^7=10460353203/10000000>958`. Thus the last strict inequality
uses only elementary exact bounds. Positive Picard comparison gives
`Y_0(t,x)>=A(s(t))` for all x and `1<=t<t_*`.

### 15.4 Transfer to the Id root

The Id coordinate has the exact nonnegative mild identity

    Y_I(T,x)=P_T[v^2](x)
               +(1/2) integral_0^T P_(T-r)[Y_0(r,.)](x) dr.

For any `T>=7/2`, retain just `1<=r<t_*`, where the comparison is spatially
constant. Since `dr=exp(-2r)ds>=exp(-7)ds` before t_*,

    Y_I(T,x)
       >= (1/2) integral_1^(t_*) A(s(r)) dr
       >= (exp(-7)/2) integral_0^(s_*) A(s) ds
        = (exp(-7)/2) lim_(s->s_*) Z(s)
        = infinity.

Multiplication by `exp(2T)` gives the stated divergence of M_I. This final
integral step is necessary: divergence of a descendant coordinate alone
would not establish the Id-root conclusion.

The extension uses only the uniform magnitude order in (15.2), so it
applies throughout the C2-R family, every Bernstein feasible interface,
and the pointwise polynomial family in Section 14. The later analytic
derivative conjecture is irrelevant to this obstruction. Coupled with
Sections 1–11, it gives a same-data-family comparison: controlled biased
short-slab continuation has a horizon-uniform RMS bound, while this
particular unsplit raw estimator fails to be in L2 by horizon 7/2.
