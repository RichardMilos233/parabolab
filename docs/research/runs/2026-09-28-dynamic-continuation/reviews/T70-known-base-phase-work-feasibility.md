# T70: near-query-order computation of the known base value

Date: 2026-09-29. Research-only candidate; independent audit pending.

**Verdict: GO as a conventional Gate-A candidate for independent audit.**
For the deliberately specified coarse interpolant below, the paid
`k^d` transcript determines `g`, a constant-work ideal lookup procedure,
the fixed-tolerance mean branch, and an approximation to the actual
`H(g)` with absolute error

    eta=exp(-(T-L))/192

using at most `C k^d (1+T)^a` ideal arithmetic operations. Constants and
the finite exponent `a` depend on fixed `d,s` and the accepted analytic
constants. The assertion is for `log k<=C(1+T)`, which includes R12's
choice `k` of order `exp(T/(s+d/2))`, with `k>=k0` and `T>=T0>=L`
as in D29's large-horizon theorem. No new value of the unknown datum
is acquired after the paid coarse transcript.

This is a constructive mathematical work bound, not a measured speed
claim. The powers and constants used here are intentionally very large.
Only this new T70 file is written. D29 remains an accepted query theorem;
this candidate does not change its status, prove Gate B, or accept a
combined work theorem. No code, numerical experiment, Lean file, frozen
proof, accepted ledger, or canvas is changed.

## 1. Exact interface and the design choice

Retain the unit torus, equation

    u_t=Delta u/2+u-u^3,

the full genuinely signed unknown class in D29, and every fixed pair of
integers `d,s>=1`. In particular the unknown `v` is smooth, has sup norm
at most `1/2`, and has all total-order derivatives through `s` bounded
by one. No Gevrey or analytic promise is added to `v`.

Use the same actual graph functional from T65:

    H(q)=Pi S_Lq-Theta(Q S_Lq),       Q=I-Pi.

Here `L>=1` is fixed and public, the entire `7/8` sup ball satisfies
`||Q S_Lq||<=r/16`, and `Theta` has Lipschitz constant at most `v1` on
the required mean-zero ball. The accepted root test has derivative
lower bound `m0=63/64`. These facts are taken from frozen T65, not
reproved by a numerical approximation to the graph.

The freedom used here is to choose the public smooth local interpolation
basis in T56/T65 to be Gevrey of order two. This is a choice of the
algorithm's known formula, not a restriction on the unknown input. An
arbitrary previously selected `C^infinity` formula need not have this
work bound merely because each of its derivative bounds is finite.
Gate B must use this same `g` or repeat the interface check for its own
representation.

The work model is the common ideal model requested in R12. Charge one
unit for each unknown exact value acquisition. Charge each arithmetic
operation `+,-,*,/`, comparison, integer/index operation, floor/ceiling,
stored-value read or write, and elementary evaluation of `exp`, `log`,
`sin`, `cos`, and positive square root. Fixed public real constants are
available. Complex arithmetic below means a fixed number of real
operations. A transform, an ODE solve, arbitrary known-function
evaluation, integration, or root search is not a primitive.

Gate A is deterministic and uses no random primitive. If composed with
Gate B, the latter must state and count its own random draws. Exact
continuously distributed locations and exact oracle responses remain
idealizations. The precision estimates below control perturbations of
the calculation; they do not encode arbitrary exact oracle reals in
finitely many bits or establish a machine bit-complexity theorem.

## 2. A paid local interpolant with a quantitative representation

Choose a fixed nonnegative Gevrey-2 bump `beta`, positive on `(-1,1)`
and zero outside that interval. One explicit choice is

    beta(t)=exp(-1/(1-t^2)) for |t|<1, and zero otherwise.

Its derivatives obey `||beta^(m)||<=A C^m (m!)^2` for computable public
constants. For completeness, Cauchy's estimate for `exp(-1/z)` in a
disk of radius `c t` about positive `t` gives

    |(d/dt)^m exp(-1/t)| <= m! (c t)^(-m) exp(-c'/t).

Maximizing `t^(-m) exp(-c'/t)` and using Stirling bounds gives the
displayed Gevrey-2 estimate; composition with the fixed quadratic and
extension by zero preserve it. Thus the cutoff is smooth and flat at
its support boundary, but is not analytic there.

Normalize the translates by `sum_j beta(t-j)`. This denominator is
bounded below by a positive public constant and has at most two
nonzero terms away from boundaries. Its reciprocal is Gevrey-2 with
public constants. One direct proof differentiates `D(1/D)=1`:
after dividing by `(m!)^2`, the product coefficient has the factor
`1/binom(m,l)`. Increasing the geometric derivative constant makes
the resulting geometric sum less than one. Tensor products give a
nonnegative periodic partition with a bounded number of overlaps.

At each of the `k^d` periodic grid nodes, use a fixed tensor stencil of
degree `s-1` in each coordinate, and blend its local polynomial by
this partition at scale `1/k`. Take `k>=k0>=2s`. There are constants
depending only on `d,s` such that

    ||v-g|| <= Cint k^(-s),
    ||g||_(C^s,max) <= Cint,
    ||partial^alpha g|| <= B (C k)^(|alpha|) (alpha!)^2
                                             for every multi-index alpha. (2.1)

Only the grid values are used to construct the polynomials. The first
bound follows from the fixed-stencil interpolation remainder. It uses
only total-order derivatives through `s`: alternatively compare each
local polynomial to the total-degree `s-1` Taylor polynomial on its
fixed scaled neighborhood. The same comparison, polynomial
reproduction, and the partition identity bound the differentiated
blend through order `s`. This also covers `s=1`. The last bound follows
from the fixed-degree polynomials, bounded coefficients, bounded
overlap, and the scaled Gevrey cutoffs. It explicitly grows with both
`k` and derivative order; it is not a uniform all-order bound.

On the promised class, increasing the fixed threshold makes
`||g||<=3/4`. Periodic wraparound uses the corresponding local lifts
of each stencil. At a grid node only the centered bump is nonzero, so
the formula also interpolates the paid values there.

There are only `O_(d,s)(1)` coefficients per node. A fixed stencil
matrix converts the paid values into these coefficients in `O(k^d)`
operations and storage. Given any point `x`, compute `floor(k x_i)`,
read a bounded number of neighboring records, evaluate their
fixed-degree polynomials and cutoff weights, and add them. Therefore

    Work(g(x)) <= C_(d,s)                               (2.2)

in the stated ideal model, including every lookup and elementary
evaluation. The support test is made before the bump's division.
This is the lookup contract to transfer to T69. It is not a free
known-profile oracle. The exact-real boundary comparisons are Borel.
At deterministic rational grids, approximating these formulas to
`exp(-poly(T))` is also possible with a polynomial number of guard
digits: the partition denominator is uniformly positive, and a bump
with sufficiently negative exponent can be replaced by zero with its
absolute error included. No such finite-bit assertion is imposed on
an exact random query coordinate.

## 3. A finite known-profile solver lemma

The following lemma is the central additional claim of this candidate.
It is stated in a form sufficient for both the coarse burn-in and the
later graph-root solves.

Fix `d`, `B>=1`, and a public scale constant. Suppose a known real periodic
profile `q` satisfies `||q||<=1` and

    ||q||_(G_(c/kappa)) <= B,        kappa>=1,
    ||f||_(G_rho) := sum_alpha rho^(|alpha|)/(alpha!)^2
                                  ||partial^alpha f||.                 (3.1)

Here `alpha!` is the product of the coordinate factorials.

Let `S>=1`, `P>=1`, and set

    E=1+P+S+log(kappa+1).

If `q` has an exact evaluation procedure costing `Wq` operations in
the stated primitive model, a finite real Fourier calculation returns
`U` such that

    ||U-S_Sq|| <= exp(-P),
    Work <= C kappa^d E^a (1+Wq),                      (3.2)

for a fixed finite `a`. If the Fourier coefficients of a polynomial
`q` are already given, copying and zero-padding them replaces the
evaluation term. All array sizes, iteration counts and tolerances are
public functions of `B,d,kappa,S,P`. No exact PDE or norm oracle is
used. If only an approximate evaluator is supplied instead, its cost
at the precision in Section 4d must be included in `Wq`. A safe choice
below has spatial cutoff

    N=ceil(C kappa E^(2d+8)),
    p=ceil(C E^(d+4))                                (3.3)

as the temporal polynomial degree. Increasing fixed constants covers
small parameter values. These exponents are convenient upper bounds,
not proposed optimal ones.

The proof of (3.2) is given in Sections 4--7. It accounts separately
for spatial truncation, nonlinear aliasing, the actual startup radius,
time interpolation, fixed-point iteration, and scalar coefficient
computation. In particular no Fourier maximum principle or generic
high-order convergence slogan is used.

## 4. Uniform spatial tails, including the initial layer

### 4a. Gevrey control before a fixed smoothing time

The space in (3.1) is a Banach algebra. In the product rule the
coefficient of the product of the `beta` and `alpha-beta` summands is
`1/binom(alpha,beta)<=1`. Completeness follows from completeness of
the derivative sup norms and closure of differentiation under their
uniform limits. The heat semigroup is a contraction and is strongly
continuous in this space, by dominated convergence in the derivative
sum. The cubic mild equation is therefore a contraction on a radius
`2B` ball for a small time `h0>0` depending only on `B`.

It gives `||S_tq||_(G_(c/kappa))<=2B` for `0<=t<=h0`.
Integration by parts in a coordinate with largest Fourier index and
optimization over the derivative order imply

    |hat u(t,n)| <= C exp(-c sqrt(|n|_infinity/kappa)).

Indeed use the derivative of order
`m=floor(c sqrt(|n|_infinity/kappa))` in that coordinate; the factor
`(m!)^2/(2*pi*|n|)^m` then decreases geometrically in `m`.
Summing over lattice shells and absorbing a polynomial factor into
the exponential gives

    sum_(|n|_infinity>N) |hat u(t,n)|
          <= C kappa^d exp(-c sqrt(N/kappa))             (4.1)

on this initial interval. This is the reason for the Gevrey design
choice. Smoothness without a quantitative all-order bound would not
give (4.1) at the asserted work scale.

### 4b. Fixed-time analytic smoothing of the actual real solution

Here is a direct quantitative argument, rather than an assumption
that the initial profile is analytic. Comparison gives `||u(t)||<=1`
for every real time. For bounded real initial data of norm one,
periodic heat convolution at imaginary spatial displacement `y` has
kernel `L1` bound `exp(|y|^2/(2t))`. Work, for a short time `h1`, in
the varying complex strips `|Im z|<a sqrt(t)`.

In the Duhamel term from time `r` to `t`, shift the integration contour
to `y_r=sqrt(r/t)y`. The remaining displacement satisfies

    |y-y_r| <= a (sqrt(t)-sqrt(r)) <= a sqrt(t-r).

The heat operator between these strips therefore has norm at most
`exp(a^2/2)`. Picard iteration for `u-u^3` is a contraction on a
fixed-radius ball in the strip supremum norm when `h1` is sufficiently
small. Each iterate is holomorphic in the strip interior; uniform
limits preserve holomorphy. At `r=0` no contour shift is required.
Uniqueness on the real torus identifies the result with the actual
real PDE solution.

Restart this construction from the actual bounded profile at time
`t-h1`. For all `t>=h1`, the actual solution thus has a fixed strip
width `rho=a sqrt(h1)` and a fixed bound `R`, independent of `kappa`
and `t`. Choose `h1<=h0` to overlap the early estimate. Contour
shifting in Fourier integrals gives a tail bounded by `C exp(-cN)`
after this smoothing time. Consequently, throughout `[0,S]`,

    tau_N := sup_t ||(I-P_N)u(t)||
       <= C kappa^d exp(-c sqrt(N/kappa))+C exp(-cN).    (4.2)

The stronger tail at the fixed burn-in time will also be used later.
This smoothing statement concerns the actual real solution, whose
comparison bound was established independently of any discretization.

### 4c. Fourier projection losses are retained

Let `P_N` retain the rectangular Fourier box `|n_i|<=N`. The
one-dimensional Dirichlet kernel satisfies an `L1` bound
`C(1+log(N+1))`, obtained by integrating its bound
`C min(N+1,1/dist(x,Z))`. Taking tensor products gives

    Lambda_N := ||P_N||_(infinity->infinity)
                     <= C_d(1+log(N+1))^d.             (4.3)

Use a public upper bound for this norm in every parameter choice.
The Fourier Galerkin ODE is

    u_N'=A_N u_N+P_N(u_N-u_N^3),       A_N=Delta/2 on ran(P_N).

It does not inherit the real PDE maximum principle. Instead compare
it with `P_Nu` until its sup norm would first reach two. On this
interval `f(z)=z-z^3` has a fixed real Lipschitz constant on `[-2,2]`.
If the initial Fourier polynomial has error at most `epsilon0` from
`P_Nq`, Duhamel and real heat contraction give

    ||u_N(t)-u(t)|| <= (epsilon0+tau_N) exp(C Lambda_N S). (4.4)

Choose the right side less than `min(1/4,exp(-P)/4)`.
Then `||u_N||<=5/4`, so the bootstrap closes and the finite ODE
exists throughout `[0,S]`. Formula (3.3) permits this: its tail
exponent has order `E^(d+4)`, whereas

    log kappa + P + Lambda_N S <= C E^(d+1).

This is a deliberately conservative absorption of projector growth,
not an assertion of uniform `L-infinity` stability of `P_N`.

### 4d. Constructing the initial coefficients and cubing exactly

Choose the smallest power-of-two grid size `Q>=4N` in each coordinate, evaluate
the known `q` there, take its tensor discrete Fourier transform, and
retain the central box. For absolutely summable Fourier coefficients,
the alias formula is exact. The total coefficient error in this box
is bounded by the true Fourier tail beyond `Q-N`, because each
aliased Fourier index has a unique residue. Formula (4.1) controls
that tail. If nodal values have errors at most `epsilon_grid`, their
coefficient errors have sum at most
`(2N+1)^d epsilon_grid`; include this in `epsilon0`.

For a cubic evaluation of a polynomial supported in the `N` box,
use the smallest power-of-two grid exceeding `6N` in each coordinate, evaluate
by inverse FFT, cube the nodal values, transform back and retain the
`N` box. The cubic has support in the `3N` box, so this padding
computes its coefficients without aliasing. This is an explicit
operation count `O_d(N^d log(N+1))` for the exact polynomial cubic.
A grid of only `2N+1` nodes would not have this property.

## 5. Time analyticity and the true startup scale

Write `M=(2N+1)^d`. All time work below is on this finite Galerkin
system, after (4.4) has proved its real boundedness.

For complex time with `|arg z|<=theta<pi/2`, the periodized complex
Gaussian gives

    ||exp(z Delta/2)||_(infinity->infinity)
                              <= (sec theta)^(d/2).    (5.1)

Starting from any real Galerkin profile of norm at most two, a complex
mild Picard argument therefore gives a bounded holomorphic solution
in the forward sector

    |arg z|<theta,       0<|z|<rho_N=c_d/Lambda_N,       (5.2)

with a fixed bound `R_d`. The contraction contains the factor
`|z| Lambda_N`; the radius in (5.2) explicitly pays for projection.
The integrals are along radial segments, so their heat times remain
in the sector. This is not an analytic disk of radius independent of
the highest spatial frequency.

At the initial time a genuine disk follows instead from a crude
finite-dimensional bound. Each Fourier coefficient of a polynomial
has magnitude at most its sup norm, whence

    ||A_N||_(infinity->infinity) <= C_d N^(d+2)=D_N.

Ordinary complex ODE Picard iteration supplies a bounded analytic
disk of radius

    a_N=c_d/(D_N+Lambda_N).                            (5.3)

This is a safe radius, including negative real times. One could
improve the power using a Bernstein inequality, but no such
improvement is needed: the logarithm of its reciprocal is only
`O_d(log(N+1))`. In particular the startup proof does not treat the
Gevrey-2 initial profile as analytic data with a fixed time radius.

Let `Lambda_p<=C(1+log(p+1))` bound the Lebesgue constant of degree-p
Chebyshev-Lobatto interpolation. To see the logarithmic bound directly,
write the nodes as `cos(j*pi/p)`. The explicit cardinal-polynomial
formula bounds their absolute values at `cos(theta)` by
`C min(1,1/(p |theta-j*pi/p|))`, with the continuous limiting value
at a node. Summing over the equally spaced angles is a harmonic sum.
Set

    h=c/(Lambda_N Lambda_p),
    a=min(a_N/16,h/16).

Choose the fixed `c` small enough that `h<=min(1/100,rho_N/100)`
and for the contraction in Section 6. Use the first panel `[0,a]`;
its fixed Bernstein ellipse lies inside the genuine disk (5.3). Thereafter double time
using panels `[t,2t]` until the endpoint first lies in `[h,2h)`.
Every such panel fits in a fixed relative Bernstein ellipse in the
sector based at zero: its left edge remains positive and its far
edge has modulus at most a fixed multiple of `h`, below `rho_N`.

For the remaining interval use equally spaced panels of length in
`[h/2,h]`. This is possible since `S>=1` and the startup time is
less than a fixed small constant. For a panel starting at `b>=h`,
base (5.2) at the real time `b-h`. The relative interval then lies
between `h` and `2h`, again inside a fixed Bernstein ellipse in the
sector. This establishes a uniform ellipse parameter `varrho>1`.

Balancing the final panels avoids an arbitrarily tiny last step.
Every positive panel length is at least a public constant times
`min(a_N,h)`, so its logarithmic reciprocal is bounded by
`C(log(N+1)+log(p+1))`. The panel count satisfies

    n_pan <= C[1+log(N+1)+log(p+1)+S Lambda_N Lambda_p]
           <= C E^(d+2).                              (5.4)

On each relative ellipse the exact forcing
`F_N(t)=P_N(u_N(t)-u_N(t)^3)` has norm at most `C_d Lambda_N`.
The elementary Chebyshev contour-coefficient estimate, valid also
for Banach-valued holomorphic functions, gives the nodal interpolant
error

    ||F_N-I_p F_N|| <= C_d Lambda_N varrho^(-p).        (5.5)

One may obtain it directly by integrating the coefficients around
the ellipse, bounding them geometrically, and summing the tail and
its interpolation aliases. It has no hidden `N^(2p)` factor.

## 6. Exponential collocation with a proved stability bound

For a panel of length `ell`, let `theta_i`, `i=0,...,p`, be the
Chebyshev-Lobatto nodes on `[0,1]`, and `L_j` their cardinal
polynomials. Given an approximate starting profile `U_b`, solve
the following finite nodal fixed-point system:

    V_i = P_(theta_i ell) U_b
        + integral_0^(theta_i ell) P_(theta_i ell-r)
                  sum_j L_j(r/ell) P_N(V_j-V_j^3) dr.   (6.1)

Here `P_t` denotes the heat semigroup, not the cutoff projection.
The heat operator is applied exactly to each Fourier coefficient;
only the time dependence of the nonlinear forcing is interpolated.

On the real nodal ball `max_i||V_i||<=4`, the cubic vector field has
Lipschitz constant at most `49 Lambda_N`. Real heat contraction and
the interpolation Lebesgue constant show that the map's contraction
constant is at most

    q_ell=49 ell Lambda_N Lambda_p <= 1/4.              (6.2)

Its image remains in the ball: for `||U_b||<=2`, its norm is at most
`2+68 ell Lambda_N Lambda_p<4`. Start Picard iteration with the
linear heat values. After `O(p)` iterations its distance from the
fixed point is at most `C 4^(-c p)`. Thus no unproved nonlinear
solver, adaptive convergence test, or unbounded iteration is used.

Insert the exact Galerkin nodal values into (6.1). By (5.5) their
defect is at most `C ell Lambda_N varrho^(-p)`. Two panel solutions
with differing initial data have sensitivity at most
`1/(1-q_ell)<=exp(C ell Lambda_N Lambda_p)`. Multiplying these
factors over the panels, including the geometrically small ones,
gives at most

    exp(C S Lambda_N Lambda_p).                       (6.3)

It does not give a factor exponential in `N^2 S` or in the number
of startup panels. Summing local defects and fixed iteration errors
yields, with scalar/arithmetic perturbations of size `epsilon_alg`
per panel,

    endpoint error <= exp(C S Lambda_N Lambda_p)
       [C S Lambda_N varrho^(-p)
        +C n_pan 4^(-c p)+C n_pan epsilon_alg].         (6.4)

Since `S Lambda_N Lambda_p<=C E^(d+2)`, choose the constant in
`p=ceil(C E^(d+4))`, the Picard iteration multiple, and the public
arithmetic tolerance so that (6.4) is below `exp(-P)/4`.
The simultaneous bound by `1/4` closes the approximate-solution
bootstrap `||U_b||<=2` at every panel. If arithmetic is inexact,
choose a small extra margin inside the radius-four nodal ball;
the exact image bound above leaves more than enough room.

The proof used the large spectral stiffness only in the initial
disk and the exactly integrated heat factors. It did not assert
that a fixed-order integrator with a step independent of `N`
has exponential accuracy.

## 7. Every scalar weight and every operation is finite and counted

For Fourier index `n`, put `lambda_n=2*pi^2 |n|^2` and
`z=lambda_n ell`. The entries implementing (6.1) are

    omega_(i,j,n)=ell integral_0^(theta_i)
                         exp(-z(theta_i-r)) L_j(r) dr. (7.1)

They are diagonal in the spatial Fourier index. No dense `M` by
`M` spatial matrix is constructed.

Compute the monomial coefficients of each `L_j` by multiplying
its linear factors. For `z>0`, its moments are obtained by

    I_0=(1-exp(-z theta_i))/z,
    I_m=theta_i^m/z-(m/z) I_(m-1),       m>=1.           (7.2)

For `z=0`, use `I_m=theta_i^(m+1)/(m+1)`; for `theta_i=0`, all
weights are zero. Thus all weights can be constructed in at most
`O(M p^3)` scalar operations per panel, including every elementary
evaluation. Each Picard iterate costs

    O(M p^2 + p M log(N+1)),

for time-weight application and the dealiased cubics. There are
`O(p)` iterates and (5.4) panels. Initial grid transforms cost
`O(M log(N+1))` plus their actual known-profile evaluations. Consequently

    Work <= C n_pan M [p^3+p^2 log(N+1)]
                  +C M[log(N+1)+Wq]
          <= C kappa^d E^a(1+Wq),                    (7.3)

for a finite fixed `a`. In the exact elementary-primitive model,
enlarging constants and taking `a=2d^2+20d+50` safely overestimates
the displayed operations. Sharp powers are not claimed. A model that
charges the bit cost of implementing the elementary primitives needs
separate representation and multiplication-cost assumptions.

The exact ideal arithmetic calculation can use (7.2) directly. It
would be incorrect to infer fixed-precision numerical stability of
this monomial recurrence: small `z` causes cancellation. The required
absolute accuracy can nevertheless be bounded publicly without
exponential work in `T`:

- Chebyshev node separation is at least `c p^(-2)`. The coefficients
  of the cardinal polynomials and their construction intermediates
  have size at most `exp(C p log(p+1))`.
- The balanced panels imply that every nonzero `z` has
  `log(1/z)<=C(log(N+1)+log(p+1))`; also `log(1+z)<=C log(N+1)`.
  Applying (7.2) through order `p` therefore gives intermediate and
  sensitivity bounds at most
  `exp(C p[log(N+1)+log(p+1)])` after another polynomial factor.
  This follows as well by differentiating the finite recurrence;
  powers of `1/z` have total degree `O(p)`.
- FFT, cubic and matrix application intermediates have at most
  additional polynomial powers of `M,p` and the preceding bound.
  Real nodal profiles are bounded in the fixed ball. The cumulative
  endpoint amplification is already accounted for by (6.3).

Thus computing elementary quantities and subsequent arithmetic to
an absolute tolerance `exp(-E^b)` for a sufficiently large fixed
`b` makes their entire contribution in (6.4) smaller than its
assigned budget. This requires polynomially many guard digits in
`E`. Large negative exponential arguments may be replaced by zero
once below this absolute tolerance; the other elementary functions
are evaluated on explicit bounded or logarithmically specified
ranges. One can instead keep their exact ideal primitive evaluation,
in which case these scalar errors are zero. Neither choice assigns
unit cost to a PDE solve or hides an accuracy-dependent iteration.

This precision observation explains stability at the prescribed
absolute accuracy, but is not a bit theorem for exact input reals.
It also is not a recommendation to implement monomial moment
recurrences at ordinary machine precision. Combining (4.4), (6.4)
and the allocated scalar errors proves the solver lemma (3.2).

## 8. Burn-in, low-mode storage, and the paid branch test

Apply the solver lemma to the interpolant `g` with `kappa=k` and
`S=L`. By (2.1), its Gevrey norm at radius `c/k` is bounded by a
public constant. Its actual lookup cost is (2.2). For every target
accuracy with logarithm `O(1+T)`, the work is `C k^d poly(1+T)`.

Set, as in the accepted error contract,

    xi=min(r/64, eta/[4(1+2v1)]),
    zeta=min(r/16, eta/2).                             (8.1)

At time `L>=1` the actual solution has the fixed analytic strip
from Section 4b. Hence a cutoff `n0=ceil(C(1+T))` has tail at most
`xi/2`; increase the public constant as needed. Compute `U_L` with
error at most `xi/(4 Lambda_(n0))`, and let

    p=P_(n0) U_L.

The cutoff in the first solve is chosen at least `n0`; increasing
its fixed constant achieves this. Then

    ||p-S_Lg|| <= xi,       btilde=Pi p.                (8.2)

The mean is the stored zero Fourier coefficient, so no additional
quadrature error or unknown-input access is involved. In particular
`|btilde-Pi S_Lg|<=r/32`, as needed by T65's paid coarse test.
Computing this stronger accuracy even on a far-branch input is
allowed and still meets Gate A's total work bound.

If `|btilde|>r/2`, use the accepted scalar-comparison far branch.
Its sign decision has precisely the accepted fixed error buffer;
it needs no high-accuracy graph root. If `|btilde|<=r/2`, continue
below. This includes exact and arbitrarily close stable-interface
inputs; no numerical estimate of the unknown phase is used to
remove them from the class.

The low-degree polynomial is useful for the second part of the
computation. The true Fourier coefficients of `S_Lg` have uniformly
bounded absolute sum. Its computed low coefficients differ from
the true ones by at most the first-solve sup error each. Since
`n0^d exp(-T)` is bounded on the relevant horizon range, the
coefficient absolute sum of `p` is bounded by a public constant,
independent of `k,T`. Thus for

    wtilde=p-Pi p,

all subsequent profiles `c+wtilde`, `|c|<=r/4`, have a bounded
Gevrey norm at radius `c0/n0`. This follows directly from their
Fourier coefficients: differentiating a mode multiplies it by at
most `(2*pi*n0)^|alpha|`, and the factorial-weighted derivative
sum converges uniformly at that radius. Their initial coefficients
are already stored. No large-frequency initial formula has to be
reevaluated in the graph-root solves.

## 9. The graph root with a fully absolute error budget

Write `w=Q S_Lg`. From (8.2),

    ||wtilde-w||<=2xi,
    ||wtilde||<=r/16+2xi<=3r/32<r/8.

The accepted graph and phase facts give, for `-r/4<=c<=r/4`,

    f(c)=A(c+wtilde),
    f(Theta(wtilde))=0,       |Theta(wtilde)|<=r/8,
    f'(c)>=m0=63/64.                                  (9.1)

All these initial profiles have norm below `r`, hence below `7/8`.
Their root is bracketed with a fixed endpoint buffer. Let
`epsilon_A=m0 zeta/4`.

For each midpoint evaluation of `f`, choose the public integer

    tau>=1,    C0 exp(-(2nu-2)tau)<=epsilon_A/2,
    nu=2*pi^2-1.

It has size `O(1+T)`. For real data of norm at most `a0=7/8`, the
scalar comparison interval at time `tau` is

    [-b_tau,b_tau],
    b_tau=1/sqrt(1+(a0^(-2)-1) exp(-2tau)).

On it the derivative of `exp(-tau)G(b)`, with
`G(b)=b/sqrt(1-b^2)`, is at most `C exp(2tau)`. Solve the known
profile `c+wtilde` up to `tau` with sup error at most

    epsilon_A exp(-2tau)/(4C).                        (9.2)

Clip its computed zero coefficient to the displayed comparison
interval, which is nonexpansive relative to the true mean. Evaluate
`exp(-tau)G` with absolute scalar error at most `epsilon_A/4`.
The phase tail, PDE error after this transform, and scalar error
sum to at most `epsilon_A`. Its small distance from `+/-1` is
explicitly paid for by the factor `exp(2tau)` in (9.2).

The solver lemma applies here with `kappa=n0=O(1+T)`, `S=tau=O(1+T)`
and requested log accuracy `P=O(1+T)`. Initialization uses the stored
polynomial coefficients. Each phase evaluation therefore costs only
`poly(1+T)`, uniformly in the midpoint and the original coarse
transcript. The elementary comparison endpoint and transform use
the stated primitives. If approximated, their required absolute
guard precision is also `exp(-poly(T))`; exact ideal evaluation
avoids any ambiguity from rounding an endpoint to one.

Perform the buffered bisection from T65. At a midpoint `c`, if
`fhat>epsilon_A`, keep the lower half; if `fhat<-epsilon_A`, keep
the upper half. Otherwise (9.1) gives

    |c-Theta(wtilde)| <= 2epsilon_A/m0 = zeta/2,

and the algorithm returns that midpoint. After a public `O(1+T)`
number of halvings reducing the bracket length to `2zeta`, return
its midpoint in any case. The returned `chat` satisfies
`|chat-Theta(wtilde)|<=zeta`. Equality follows the middle branch.
Every inner call has the predetermined absolute error guarantee;
there is no unbounded sign-refinement loop.

Finally return

    h0=Pi p-chat.

The actual graph Lipschitz bound and (8.1) give

    |h0-H(g)| <= (1+2v1)xi+zeta <= 3eta/4 < eta.        (9.3)

Every budget in this calculation is absolute. In particular there
is no division by `H(g)`, `f(c)`, or the distance from the interface.
Cancellation between `Pi p` and `chat` costs the already allocated
absolute precision, and does not cause more root iterations or
more unknown-input acquisitions. The same computation is valid
when `H(g)=0` exactly.

## 10. Gate-A accounting and boundaries of the result

For the intended `log k=O(1+T)`, all work is accounted for as follows:

    paid values and local data structure:        C k^d,
    known-profile burn-in including startup:     C k^d poly(1+T),
    low-mode storage and fixed mean branch:      poly(1+T),
    at most O(1+T) graph phase solves:           poly(1+T),
    bisection, clipping and scalar output:       poly(1+T).

The result is the claimed bound `C k^d(1+T)^a` after increasing the
finite exponent. Exactly the coarse `k^d` input acquisitions are
used by this gate. Values of `g` on FFT grids and at any later
derivative-sampling leaves use saved coarse records and incur
their explicit (2.2) arithmetic cost; they are not calls to `v`.

All array sizes and loop maxima are finite public functions of the
horizon and fixed constants. Arithmetic, support tests, projections,
comparison clipping, and buffered branching are Borel in the paid
transcript. If desired, clamp coarse responses to `[-1/2,1/2]` for
a total off-promise definition. Even on a transcript not satisfying
the promise, use the same finite loop counts; the promise is needed
for accuracy and norm estimates, not to decide whether to halt.
No query of an unknown norm, derivative, phase or evolved value
appears. Gate A halts deterministically.

This establishes the stated Gate-A candidate in the shared ideal
primitive model. The following conclusions do not follow from it:

- The whole estimator still needs T69's actual derivative sampler,
  its uniform second moments, hard marked-query cap, and expected
  work bound for this same `g` and primitive model.
- Replacing the finite derivative tables by a bounded-variance
  base-phase Monte Carlo average has not been justified. The
  deterministic base computation above is a separate ingredient.
- An arbitrary smooth known formula has not been given a nearlinear
  solver. The public Gevrey basis, quantitative tails and evaluation
  representation are essential inputs to this construction.
- The constants need not be reasonable or uniform as `d` grows.
  No large-domain, practical speed, fixed-machine-precision, bit,
  code, numerical or Lean result is asserted.

The next acceptance action is an independent audit of (3.2), its
interpolation design and error budgets, followed by the root's
correspondence check against R12 and the separately frozen Gate B.
Until then T70 is a candidate and the combined work result remains
conditional. No accepted ledger is updated by this report.

## 11. Bounded literature check and provenance

Six bounded search queries were used to check relevant numerical and
regularity precedents. The following primary materials were inspected
only to the extent stated; the argument above supplies its own bounds.
This is not a worldwide novelty or priority search.

- Hochbruck and Ostermann, *Exponential integrators*, Acta Numerica
  19 (2010), author PDF, introduction and Sections 2.1--2.2, especially
  formulas (2.8)--(2.11). These describe exact semigroup convolution
  of polynomial forcing and distinguish classical from stiff order.
  They motivate the finite weights in (7.1), but no theorem there is
  claimed to supply our growing-degree, growing-cutoff work bound.
  [Primary author PDF](https://na.math.kit.edu/download/papers/acta-final.pdf).
- Zhenhao Li, *Weyl laws for open quantum maps*, Journal of Spectral
  Theory 12 (2022), published online 2023. The inspected Gevrey
  preliminaries, formulas (1.6)--(1.8), and the later explicit order-two
  cutoff give compact-support and Fourier-decay examples. The quantum
  map results are unrelated and are not imported. Section 2 above
  gives the needed elementary cutoff estimate directly.
  [Primary journal PDF](https://ems.press/content/serial-article-files/33906?nt=1).
- Trefethen, *Lecture 3: Chebyshev series* (2017), complete one-page
  author note. Its Bernstein-ellipse coefficient estimates and warning
  about monomial conditioning are relevant to Sections 5 and 7. The
  parabolic stability and complexity calculations here are additional.
  [Primary author note](https://people.maths.ox.ac.uk/~trefethen/outline3_2017.pdf).

The Utrecht institutional record for Takac, Bollerman, Doelman,
van Harten and Titi's 1996 analyticity paper was also inspected, but
its full proof was not retrieved and is not used as a black-box
theorem. The complex-strip Picard argument in Section 4b is our
explicit regularity justification. R11's inspected DeepONet example
uses a different input law and does not establish this work claim.

Dependencies read for this task include R08, R10b/T68, R11 and R12,
with T65/T56/T59 and the model already read fully in the completed
independent T67 audit. The frozen analytic input and the shared
composition contract used here have hashes

    T65-local-stable-graph-upper-proof.md
    58e862c9cfbaf0946605d30d9c8e8a37e2570c0c0719d626683f22db60fc9f81

    R12-signed-work-composition-contract.md
    390ede56727253adb0c23fb5356671f6b691b5c958ff4258d0e69ceeafd280ee

T70 is new research after that audit, not an
independent review of its own proposed solver. The requested research
role is `gpt-6-astra/max`; the available runtime does not independently
attest the backend model identity. No independent audit, experiment,
formalization or source-priority result is implied by that role label.
