# T56 — signed-class upper-bound feasibility

## Verdict and status

**GO as a conventional theorem candidate for independent audit.** On the
same unit-torus Allen–Cahn class and exact initial-value oracle as D25,
the lower exponent has a matching randomized **query** upper bound for
`1<=d<=4s`. The construction below has deterministic data-query count

    Q_T <= C exp(2dT/(2s+d))

and uniform absolute RMS smaller than `1/4`, for all sufficiently large
`T`. Constants depend on fixed `d,s`; no numerical usefulness is claimed.
The auxiliary computation is finite but potentially enormous. In
particular, many deterministic PDE solves for fully known surrogate data
are charged as computation, not as extra queries to the unknown datum.
There is no exact PDE, phase-coordinate, derivative, or mass oracle.

The main mechanism is not closure of the mean. An actual nonlinear scalar
coordinate is constructed, its first three derivatives are proved to be
finite signed measures with uniformly bounded total variation, and a
quadratic correction about a sample-based smooth interpolant is estimated
by Monte Carlo. A finite-coefficient construction replaces ideal signed
measure sampling. The condition `d<=4s` enters exactly in the cubic
Taylor remainder.

The assertion remains a candidate in this review until independently
checked. It does not change any accepted claim, frozen source, Lean
target, code, data, or experiment. No all-dimension matching result,
arithmetic-work optimality, practical acceleration, unbiased estimator,
or publication-priority claim is made. Only this report is written.

## 1. Fixed class, oracle, and cost

Let `T^d=(R/Z)^d`, with normalized Lebesgue measure, and

    u_t=(1/2)Delta u+u-u^3,   u(0)=v.

Fix integer `s>=1` and a target `x*`. The input class is exactly

    F_signed={v in C^infinity(T^d):
      max_{|alpha|<=s} ||partial^alpha v||_infinity<=1,
      ||v||_infinity<=1/2,  min v<0<max v}.

The only unknown-input information is the exact real value `v(x)` at
charged points. No formula, Fourier coefficient, derivative, mean, or
evolved-value information is supplied. Public randomness and finite
computation on already returned values are allowed. All preprocessing
calls to `v` count. The upper procedure below has a deterministic bound
on their number; its output is bounded and generally biased.

This is the ideal query-cost model of D25. The sizes of finite arrays,
PDE meshes, arithmetic precision, and computation of coefficients can
depend very badly on `T,d,s`. They are not omitted oracle calls: their
inputs are explicit functions constructed from the charged transcript.
Their cost prevents any inference of a matching runtime bound.

We prove analytic lemmas on the larger ball `||v||_infinity<=a0`, where
`a0=7/8`. This supplies room for interpolation and finite differences.
The claimed input class itself is unchanged. Write

    nu=2*pi^2-1,
    G(z)=z/sqrt(1-z^2)  (-1<z<1),
    Psi(z)=z/sqrt(1+z^2)  (z real).

In particular `Psi=G^(-1)` and `Psi` is globally 1-Lipschitz.

## 2. What fails before the nonlinear correction

The initial mean cannot simply replace the whole datum. With

    b(t)=integral u(t),   w(t)=u(t)-b(t),

the exact mean equation is

    b'=b-b^3-R,
    R=3b integral w^2+integral w^3.                         (2.1)

For example, the smooth signed datum

    v(x)=epsilon*(cos(2*pi*x_1)+c*cos(4*pi*x_1))

has mean zero but initial mean derivative `-(3/4)c epsilon^3`.
For fixed nonzero `c` and small enough `epsilon`, it belongs to the
promised class. Thus a zero-mean rule already has the wrong mean
dynamics. T50's estimate against the scalar solution with the initial
mean has an `exp(T)||v||_infinity^3` error; on the full fixed class this
cannot certify a fixed-error upper bound as `T` grows.

The coordinate proved below gives a stronger check. For
`phi=cos(2*pi*x_1)+c*cos(4*pi*x_1)`, its third derivative at zero yields

    A(epsilon*phi)
      =-[3c/(4*(12*pi^2-2))]*epsilon^3+o(epsilon^3).      (2.2)

Indeed the linearized solution is `epsilon exp(t)P_t phi`, its mean
is zero, and the cubic coefficient in (3.5) is
`-integral_0^infinity exp(2t) integral(P_t phi)^3 dt`.
The inner integral is `(3c/4)exp(-12*pi^2*t)`. Section 4 justifies
this differentiation and Taylor remainder. For sufficiently small
fixed positive `epsilon` and `c!=0`, the two fixed profiles
`+/-epsilon*phi` have the same initial mean zero but opposite nonzero
coordinates. By (3.8), their targets tend to opposite values `+/-1`.
Thus initial mass alone cannot uniformly approximate the signed flow.

A generic finite-time Lipschitz estimate also loses the desired rate:

    ||S_Tv-S_Tg||_infinity<=exp(T)||v-g||_infinity

only gives the deterministic interpolation exponent `d/s`. Moreover,
bounded bilinear operators on `C(T^d)` cannot in general be identified
with bounded-total-variation measures on `T^d x T^d`. Section 4 proves
that property from the PDE kernels; it is not inferred from smoothness
of a functional or from the existence of an inertial manifold.

## 3. An actual nonlinear scalar coordinate

The following estimates are uniform over `||v||_infinity<=a0`.
Comparison with the scalar solution from `+/-a0` gives

    |u(t,x)|<=ell_a0(t)<1,
    1-b(t)^2 >= (1-a0^2)*exp(-2t).                         (3.1)

Here `ell_a0(t)=a0 exp(t)/sqrt(1+a0^2(exp(2t)-1))`.
The displayed lower bound follows because the exact denominator of
`1-ell_a0(t)^2` is at most `exp(2t)`.

The centered energy estimate from T50 applies to this entire ball:

    ||w(t)||_2<=a0 exp(-nu*t).                             (3.2)

Indeed, `integral (u-b)(u^3-b^3)>=0` and the unit-torus Poincare
constant is `4*pi^2`. Since `|b|<=1` and `||w||_infinity<=2`, (2.1)
now yields the useful uniform late-time bound

    |R(t)|<=5a0^2 exp(-2nu*t).                             (3.3)

Set `A_t(v)=exp(-t)G(b(t))`. The identity `G'(b)(b-b^3)=G(b)` gives

    d A_t/dt=-exp(-t)G'(b(t))R(t).                        (3.4)

Since `G'(b)=(1-b^2)^(-3/2)`, (3.1)--(3.3) prove absolute convergence of

    A(v)=G(integral v)
         -integral_0^infinity exp(-t)G'(b(t))R(t) dt.      (3.5)

More precisely, with `alpha0=2nu-2>0`,

    |A(v)-A_t(v)|<=C0 exp(-alpha0*t).                     (3.6)

For example `C0=5a0^2/[(1-a0^2)^(3/2)*(2nu-2)]` suffices.
Also `|A(v)|<=G(a0)`, since the same bound holds for every `A_t(v)`.
For spatially constant data `v=c`, the forcing `R` is zero and
`A(c)=G(c)`.

One-unit smoothing of the centered equation, as in T50, gives

    ||w(T)||_infinity<=Cw exp(-nu*T),  T>=1.               (3.7)

This does not need derivatives of the input: write
`w_t=Delta w/2+(1-u^2-ub-b^2)w+integral(u^2+ub+b^2)w`,
use (3.2), and apply the heat `L2` to `L-infinity` bound over one unit.
All constants are finite and depend only on `d,a0`.

The relation `b(T)=Psi(exp(T)A_T(v))` is exact. Consequently

    ||S_Tv-Psi(exp(T)A(v))||_infinity
       <=Cw exp(-nu*T)+C0 exp(-(2nu-3)*T).                (3.8)

This proves a uniform profile approximation, including arbitrarily close
to the separating set `A(v)=0`. It does not assume that the initial mean
determines the phase, and it does not omit the cubic mean correction.

## 4. Uniform derivatives as actual signed measures

This section proves more than a `C^3` operator-norm bound. There are
constants `K1,K2,K3`, independent of `v` in the ball, and finite signed
measures `sigma_j(v)` on `(T^d)^j` such that

    D^j A(v)[h_1,...,h_j]
      =integral product_i h_i(y_i) sigma_j(v)(dY),
    ||sigma_j(v)||_TV<=Kj,               j=1,2,3.          (4.1)

The derivatives are Frechet derivatives in `C(T^d)` with its sup norm.
Take an open slightly larger ball when applying differentiation locally;
all constants below are uniform on the displayed closed ball `a0<1`.
Equivalently one can first prove the result on every ball strictly below
1 and use `a0=7/8` for all later arguments.

### 4a. Finite-time variational kernels

Put `a(t,x)=1-3u(t,x)^2`, so `-2<=a<=1`. The first three variations
`U_j=D^jS_tv` obey, with input labels retained,

    (U_1)_t=Delta U_1/2+a U_1,
    (U_2)_t=Delta U_2/2+a U_2-6u U_1 U_1,
    (U_3)_t=Delta U_3/2+a U_3
              -6 U_1 U_1 U_1-6u sum_(3 pairs) U_2 U_1.   (4.2)

Initially `U_1(0)h=h` and `U_2(0)=U_3(0)=0`. Local Picard
differentiation gives these derivatives on every finite time interval;
boundedness of `u` allows continuation on that interval. Iterating the
positive fundamental kernel of `Delta/2+a` in (4.2) represents each
`U_j(t,x)` as a finite sum of time-integrated signed heat-tree measures
on `j` initial leaf positions. Products use disjoint labelled inputs.
This constructs the product-space measures directly.

For `0<=t<=1`, the sup over `x` of their total variation is uniformly
bounded. This follows directly from `a<=1`, `|6u|<=6`, and (4.2).
It suffices for all short-time integrals below. For positive time the
leaf measures have Lebesgue densities almost everywhere; branch times
giving a zero leaf edge form a null set. Densities may be unbounded on
diagonals, so a pointwise-density bound is not being assumed.

### 4b. One-unit heat-tree bound in a stronger mixed norm

For a fixed unweighted heat tree of duration 1 with `j` leaves, lift its
Brownian increments to `R^d`. In one coordinate, let `Sigma` be their
leaf covariance matrix. For any real vector `c`, independence on tree
edges gives

    c^T Sigma c
      =integral_0^1 sum_(groups at time r)
                      (sum_(leaves in group) c_i)^2 dr
      >= (sum_i c_i)^2/j.                                (4.3)

There are at most `j` groups, and Cauchy--Schwarz gives the last step.
Thus `Sigma-(1/j)11^T` is positive semidefinite. In distribution the
leaves equal a common Gaussian translation of variance `1/j`, plus an
independent Gaussian vector. Modulo the torus, if `rho` is the leaf law
with the root uniform, the leaf law with root `x` satisfies

    K_tree(x,dY)<=||p_(1/j)||_infinity * rho(dY).           (4.4)

Indeed, condition on the remaining Gaussian vector and bound the
common translation's heat density by its supremum. This remains true
for every branch-time configuration, even singular covariance limits.

Feynman--Kac weights are at most `exp(j)` on a tree of duration 1,
because total edge length is at most `j`. Vertex factors have magnitude
at most 6. Applying (4.4) to every tree and integrating its times proves

    M_j(1):=integral ||U_j(1,.,Y)||_infinity dY < infinity

uniformly in the datum. One may use the explicit upper bounds

    M_1(1)<=e ||p_1||_infinity,
    M_2(1)<=6e^2 ||p_(1/2)||_infinity,
    M_3(1)<=60e^3 ||p_(1/3)||_infinity.                    (4.5)

The last coefficient consists of one ternary term of size 6 and three
binary--binary terms of total size `3*36/2=54`. All heat suprema are
finite. A common dominating measure can be used instead of Lebesgue
measure during this argument; (4.4) bounds its density uniformly in
`x` before integration. Thus (4.5) does not incorrectly exchange
`sup_x` and an arbitrary integral.

For `t>=1`, variation of constants in (4.2), now integrated in this
mixed norm, yields

    M_j(t)<=C_j exp(jt),                  j=1,2,3.         (4.6)

For example the second forcing is bounded by `6M_1(t)^2`, and the
third by `6M_1(t)^3+18M_2(t)M_1(t)`. The homogeneous sup-norm
propagator costs at most `exp(t-r)`. These estimates give finite
explicit constants recursively from (4.5).

### 4c. Centered kernels decay in an integrated spatial L2 norm

Let `B_j(t,Y)=integral_x U_j(t,x,Y)` and `W_j=U_j-B_j`. Define

    N_j(t)=integral ||W_j(t,.,Y)||_2 dY.

For order zero use `M_0=1`, `N_0=||w||_2<=a0 exp(-nu*t)`, and
`B_0=b`. The homogeneous equation on mean-zero functions is

    z_t=Delta z/2+(I-Pi)(a z),

where `Pi` denotes spatial averaging. Its `L2` propagator contracts at
rate `nu`, since `a<=1` and `Pi z=0`. Moreover

    ||a-Pi a||_2<=6||w||_2.                              (4.7)

The centered `j`th equation has the additional source
`B_j(a-Pi a)+(I-Pi)F_j`, where `F_j` is the corresponding lower-order
forcing in (4.2). In `F_j`, subtract its spatially constant expression
obtained by replacing `u,U_i` by `b,B_i`. Every remaining product has
at least one factor `w` or `W_i`. Put that factor in `L2` and all
others in the integrated sup norm (4.6).

For clarity, the second forcing can be expanded as

    u U_1 U_1-b B_1 B_1
      =w U_1 U_1+b(W_1 U_1+B_1 W_1).

Its mixed `L2` norm is bounded by
`N_0 M_1^2+2M_1 N_1`. For the third forcing, telescope the three
factors of `U_1^3` and the three factors of each `u U_2 U_1` in the
same way. The total input-derivative orders in every product sum to
`j`. Induction, (4.7), and (4.6) therefore bound the entire source by
`C_j exp((j-nu)t)`.

Since `N_j(1)<=2M_j(1)`, the mean-zero propagator gives

    N_j(t)<=C_j exp((j-nu)t),  t>=1, j=1,2,3.             (4.8)

This uses scalar energy estimates for almost every input tuple `Y`
and then integration in `Y`. It is not an unproved energy estimate
in a Banach space of measures.

### 4d. Differentiating the mean correction in total variation

Differentiate the identity `R=3b integral w^2+integral w^3` through
order 3. In each term at least two centered factors remain. Put these
two factors in the mixed `L2` norms (4.8) and any remaining factor
in (4.6). All input labels are disjoint before tensor multiplication;
Cauchy--Schwarz in `x` and integration over the input labels yield
an actual product-space measure bound:

    ||D^j R(t)||_TV<=C_j exp((j-2nu)t),
                              t>=1, j=0,1,2,3.           (4.9)

The total variation of `D^i b(t)` is at most `M_i(t)`. Also

    |G^(k+1)(b(t))|<=C_k exp((2k+3)t)                    (4.10)

by (3.1). The product/chain rule for `D^q[G'(b)]` has `k<=q`
factors of mean derivatives whose derivative orders sum to `q`.
Thus its total variation is bounded by `C_q exp((3q+3)t)`.
Combining this with (4.9) gives

    ||D^j[exp(-t)G'(b(t))R(t)]||_TV
       <=C_j exp((3j+2-2nu)t),   t>=1, j=0,1,2,3.        (4.11)

All four exponents are negative: the weakest requirement is
`2nu>11`, satisfied on this unit torus. On `[0,1]`, use the bounded
pointwise total variations from 4a and the uniform gap (3.1).

Consequently the integral (3.5) and its first three derivative-measure
integrals converge uniformly in total variation. Finite-time maps are
`C^3`; their derivatives converge uniformly in operator norm as well,
so their limit is `C^3` with the claimed derivatives. The initial
term `G(integral v)` has ordinary product-Lebesgue derivative measures
and uniformly bounded coefficients. This proves (4.1), including at
the separating set `A(v)=0`.

The proof also supplies exponential tails for the derivative measures:
order `j` has rate `2nu-3j-2`. Only orders at most 3 are asserted here.
All upper constants can be selected by finite recursions: use (4.5),
the three displayed variational equations, their finitely many
product-rule terms, and elementary exponential integrals. For example
`||p_t||_infinity` is bounded by
`[(1+exp(-2*pi^2*t))/(1-exp(-2*pi^2*t))]^d`.
Consequently the later choices of `Kj`, `B`, and time thresholds can
use known upper bounds, rather than unspecified compactness constants.

## 5. A smooth surrogate from charged initial-value samples

There is a fixed construction, depending only on `d,s`, which uses the
`k^d` values on the uniform periodic grid and returns a known smooth
periodic function `g` satisfying

    ||v-g||_infinity<=Cint*k^(-s)=:delta,
    max_{|alpha|<=s} ||partial^alpha g||_infinity<=Cint.   (5.1)

One explicit construction uses a smooth nonnegative lattice partition
of unity, supported within a fixed number of grid cells. At each grid
point form the tensor Lagrange polynomial of degree at most `s-1`
in each coordinate, using nearby periodic grid values, and blend the
polynomials with that partition. Take `k` above a fixed threshold so
the local stencils have distinct lifted nodes. All needed values are
among the same `k^d` periodic samples.

To verify (5.1), Taylor-expand at the evaluation point through total
degree `s-1`. Each local polynomial reproduces this Taylor polynomial;
sample remainders are `O(k^(-s))` using only total-order derivatives
through `s`. Differentiating the fixed scaled weights gives errors
`O(k^(-(s-r)))` for order `r<=s`. This also proves a bound for the
`s`th derivatives. No derivatives of `v` are queried, and no mixed
derivatives of order exceeding `s` are assumed.

The resulting `g` is given by a finite smooth formula. Bounds for any
higher derivative of `g` are computable from that formula and `k`,
although they need not be uniform in `k`. For sufficiently large `k`,
`delta<=1/4`, so `||g||_infinity<=3/4`. The unknown residual

    r=v-g

has `||r||_infinity<=delta` and a known Lipschitz bound independent of
`k`, since `s>=1` and (5.1) bounds first derivatives.

## 6. Finite coefficient computation without a derivative/PDE oracle

The ideal quadratic expansion is

    A(v)=A(g)+DA(g)[r]+(1/2)D^2A(g)[r,r]+Rem,
    |Rem|<=K3*delta^3/6.                                 (6.1)

One must not declare the three terms available exactly. The following
finite procedure is sufficient. Given known `g`, a known residual
Lipschitz bound, and any tolerance `eta>0`, compute a scalar `c0`,
finite nodes `z_i`, and finite real coefficients `c_i,c_ij` such that

    |c0-A(g)|<=eta,
    sum_i |c_i|<=K1+eta,
    sum_ij |c_ij|<=K2+eta,
    |sum_i c_i r(z_i)-DA(g)[r]|<=eta,
    |sum_ij c_ij r(z_i)r(z_j)-D^2A(g)[r,r]|<=eta,          (6.2)

uniformly over the allowed residuals. None of the values `r(z_i)`
is used during this coefficient computation.

### 6a. Positive interpolation turns measure bounds into finite sums

Take a sufficiently fine, nonnegative smooth partition
`theta_i>=0`, `sum_i theta_i=1`, with node `z_i` close to its support.
Set `Pr=sum_i r(z_i)theta_i`. Then `||Pr||_infinity<=delta` and
`||Pr-r||_infinity` is bounded by the known Lipschitz constant times
the support diameter. Define for the moment exact coefficients

    a_i=DA(g)[theta_i],
    a_ij=D^2A(g)[theta_i,theta_j].

The measure representation (4.1), together with positivity of the
partition, proves

    sum_i |a_i|<=K1,
    sum_ij |a_ij|<=K2.                                   (6.3)

For instance sum the integrals of
`theta_i(y)theta_j(z)` against `|sigma_2|`; the sum is identically 1.
The linear interpolation error is at most `K1||r-Pr||_infinity`.
The quadratic one is at most
`2K2*delta*||r-Pr||_infinity`. Choose the support diameter to make
both smaller than the assigned fraction of `eta`.

This is why the product-space total-variation proof matters. An
operator-norm bound alone would not justify the second inequality
in (6.3).

### 6b. Finite differences use only known initial profiles

If this partition has `J` functions, approximate `a_i,a_ij` using

    [A(g+h theta_i)-A(g)]/h,

    [A(g+h theta_i+h theta_j)-A(g+h theta_i)
       -A(g+h theta_j)+A(g)]/h^2.                        (6.4)

The errors in these formulas are at most `K2 h/2` and
`(5/3)K3 h`, respectively. The latter follows by Taylor expansion
through degree 2; it also holds for `i=j`. Taking `h` small compared
with `eta/[J^2(1+K2+K3)]`, and `h<=1/32`, makes the total coefficient
error small. All perturbed profiles remain in the `7/8` ball.

Compute each scalar `A` in (6.4) to accuracy small compared with
`eta h^2/J^2`. Division by `h` or `h^2` then preserves the required
sum of coefficient errors. Further rounding to rational coefficients
can be included with an allocated sum of errors. Together with 6a,
this proves (6.2), provided scalar evaluation on a known smooth
profile is a finite calculation. That last point is verified next.

### 6c. Scalar evaluation is a finite deterministic calculation

For any explicitly known smooth datum `q` in the `7/8` ball, approximate
`A(q)` by `A_tau(q)=exp(-tau)G(integral S_tau q)`. Choose finite
`tau` from (3.6) to control the tail. To approximate the remaining mean,
one may use the ordinary periodic central-difference Laplacian and
explicit Euler time stepping. For mesh width `h_x` and step `h_t`,

    U_j^(n+1)=U_j^n
      +(h_t/(2h_x^2))*sum_(coordinate neighbors)
                              (U_neighbor^n-U_j^n)
      +h_t*(U_j^n-(U_j^n)^3).

If `h_t<=(d/h_x^2+2)^(-1)`, the update is monotone on `[-1,1]`
and fixes the constant endpoints. Hence it stays in that interval.
Its sup-norm Lipschitz factor there is at most `1+h_t`.
Consistency gives a global error bounded by
`C(q,tau)*exp(tau)*tau*(h_x^2+h_t)`, with a finite known constant
from derivatives of the smooth solution through spatial order 4
and time order 2. Bounds for those derivatives follow recursively
by differentiating the polynomial PDE and using the scalar maximum
principle/Gronwall; the required initial bounds are computable from
the explicit formula for `q`. A grid mean adds a controlled spatial
quadrature error. All these are finite calculations on `q`.

Clip the approximate mean to the known interval
`[-ell_(7/8)(tau),ell_(7/8)(tau)]`. This does not increase its error,
and bounds the Lipschitz constant of `exp(-tau)G` by a known finite
multiple of `exp(2tau)`. Thus decreasing the finite mesh and step
achieves any prescribed scalar accuracy. Evaluation/rounding errors
for the explicit datum and scalar operations can be included in the
same stability estimate. This describes a terminating finite
algorithm, not an exact solver instruction.

Every initial value used by this solver is an evaluation of `q`, whose
formula consists of `g` and the public `theta_i` with known scalar
coefficients. It never calls `v`. In particular it is unnecessary to
query the fine residual grid during the many solves in (6.4).
There can be on the order of `J^2` such solves, with extremely fine
meshes. Their time, storage, and precision costs are deliberately not
bounded by this query theorem.

### 6d. Public tolerances, measurability, and finite termination

The choices above need no exact-norm selection. The coarse coefficients
lie in `[-1/2,1/2]`; the interpolation and partition functions are fixed
scaled smooth functions. Thus their derivatives through order 4 admit
public upper bounds in terms of `d,s,k,J,h`. Use these bounds in 6c,
rather than a norm of an unknown function or an uncertified refinement
test. The tail time, finite-difference increment, PDE mesh and time step,
scalar evaluation precision, and rational rounding precision can all be
chosen from public `d,s,k,J,eta` and the uniform constants proved above.
They specify finitely many operations on the already charged coarse
transcript. No operation obtains additional initial-data information.
This is consistent with 04o's allowance for scalar arithmetic on the
returned values; it is not access to a second input oracle.

For a total definition also on off-promise bounded coarse transcripts,
one may apply a fixed smooth scalar saturation to the interpolant,
equal to the identity on `[-3/4,3/4]` and with range
`[-13/16,13/16]`. It has no effect on admissible transcripts, and all
perturbations in (6.4), with `h<=1/32`, stay in the `7/8` ball even
off promise. Public derivative bounds still follow by the chain rule.
Clipping coarse entries to `[-1/2,1/2]` similarly extends the procedure
to arbitrary real transcripts without changing a promised run.

Finite arithmetic, fixed smooth functions, and rational rounding give
Borel coefficient rules. All deterministic loops have public finite
bounds. Finite rational sampling can use uniform-integer rejection
sampling from fair bits, with success probability at least `1/2` per
attempt; it halts almost surely. A finite number of such samplings
therefore halts almost surely on every input. Random-bit rejection time
can be unbounded, but it makes no data queries and cannot increase the
cap (7.1). The final elementary scalar value `Psi(exp(T)Ahat)` may also
be rounded to absolute error `1/64`; (7.4) still gives RMS below `1/4`.

## 7. The randomized upper procedure and its error

Take the `k^d` coarse samples used to form `g`, and put `M=k^d`.
Run the finite calculation (6.2), with `eta<=1`. Write

    L1=sum_i |c_i|,   L2=sum_ij |c_ij|.

For the linear term, sample `M` independent indices with probabilities
`|c_i|/L1`; each sample returns

    Z1=L1*sign(c_i)*(v(z_i)-g(z_i)).

For the quadratic term, independently sample `M` pairs with probabilities
`|c_ij|/L2`; each returns

    Z2=L2*sign(c_ij)*(v(z_i)-g(z_i))*(v(z_j)-g(z_j)).

If a total weight is zero, its term is identically zero. These are finite
discrete distributions; rational rounding in 6b allows ordinary finite
integer sampling. Every requested `v(z_i)` is charged, even when a
repeat could have been cached. Let

    Ahat=c0+average(Z1)+(1/2)average(Z2),
    H_T=Psi(exp(T)Ahat).

The number of unknown-data queries is at most

    k^d+M+2M=4k^d                                      (7.1)

on every input and every run. Coefficients and distributions depend
only on the initial charged grid transcript. Conditional on that
transcript they are fixed, so the variance bounds and independence
used here are valid for each deterministic input.

Since `|r|<=delta`, the two sampling standard deviations are bounded by
`(K1+1)delta/sqrt(M)` and `(K2+1)delta^2/sqrt(M)`. Equations (6.1)
and (6.2), and the triangle inequality in `L2`, give

    RMS(Ahat-A(v))
      <=(K1+1)delta/sqrt(M)
          +(K2+1)delta^2/(2sqrt(M))
          +K3 delta^3/6+(5/2)eta.                        (7.2)

Put `q=s+d/2`. For `d<=4s` one has `3s>=q`; also
`2s+d/2>=q`. Thus for `k>=1`, with

    B=(K1+1)Cint+(K2+1)Cint^2/2+K3 Cint^3/6+1,

the first three terms of (7.2) are at most `B k^(-q)`.
Choose

    k>=max(k0, ceil((16B exp(T))^(1/q))),
    eta=exp(-T)/64,                                     (7.3)

where `k0` ensures the interpolation conditions and `delta<=1/4`.
Then (7.2) is less than `exp(-T)/8`.

Choose a fixed `T*>=1` so the right side of (3.8) is at most `1/16`
for every `T>=T*`. By the global Lipschitz bound for `Psi`,

    RMS(H_T-S_Tv(x*))
       <=exp(T)*RMS(Ahat-A(v))+1/16
       <3/16<1/4.                                      (7.4)

The construction and bound are uniform on the promised class. The
ceilings and fixed thresholds in (7.3) give

    Q_T<=C exp(dT/(s+d/2))
        =C exp(2dT/(2s+d)),  T>=T*.                      (7.5)

Together with accepted D25 this would give the matching asymptotic
minimax query exponent, after independent acceptance of this upper
proof. It gives an explicit deterministic cap on data calls, which is
stronger than an expected-call upper bound. It does not strengthen
D25 into a fixed-profile lower bound.

For completeness, bounded `0<=T<=T*` causes no query obstruction.
Use one fixed sufficiently fine smooth interpolant with
`exp(T*)||v-g||_infinity<=1/16`, and solve the known surrogate PDE
to error `1/16`. This has a fixed data-query count, independent of
the horizon in that bounded interval. No asymptotic rate changes.

## 8. Where the cheaper alternatives stop

A zeroth-order surrogate has a phase error `O(k^(-s))` and retains
the deterministic exponent `d/s`. A linear correction has phase
error

    O(k^(-s-d/2)+k^(-2s)),

so this proof matches the randomized integration scale only for
`d<=2s`. The quadratic correction improves the Taylor term to
`k^(-3s)`, giving exactly the required range `d<=4s`, including equality.
This is the reason the second variation is necessary in part of the
accepted D25 range.

At `d>4s`, the cubic Taylor term in this construction decays too slowly
at the proposed query scale. Higher derivatives and higher corrections
are not audited here. This is a limitation of the present upper proof,
not a lower bound against all upper algorithms. Conversely, finite
arithmetic work could be far larger than the charged query count even
inside `d<=4s`; matching information exponents does not resolve that
practical issue.

## 9. Primary-source scope and bounded search

The search used 12 purposeful queries, listed below. It targeted the
two ingredients that might invalidate or subsume the route; it was not
a publication-priority survey.

1. Kunsch and Rudolf, *Optimal confidence for Monte Carlo integration of
   smooth functions*, [primary paper](https://arxiv.org/pdf/1809.09890),
   Section 3.2, Theorems 3.5 and 3.6, and the interpolation discussion
   immediately before Theorem 3.6. They give the classical control-variate
   construction from point-sampled approximation plus residual Monte
   Carlo, and the smooth-integration exponent `s/d+1/2`. This is direct
   prior overlap for the sampling idea and rate. Their linear integration
   theorem does not supply the Allen–Cahn nonlinear coordinate, its
   product-measure derivatives, or the horizon-uniform constants here.

2. Kostianko and Zelik, *Smooth extensions for inertial manifolds of
   semilinear parabolic equations*,
   [primary paper](https://arxiv.org/pdf/2102.03473), Introduction,
   equations (1.2)--(1.4), Example 3.11, and Theorem 4.3. The paper
   explains exponential tracking/asymptotic phase and why high smoothness
   is not automatic from generic inertial-manifold existence. Its main
   result constructs smooth extensions under additional spectral-gap
   assumptions. It is background for the identified regularity obstacle,
   not a theorem providing the initial-point-query algorithm or the
   total-variation kernel estimates of Section 4.

The primary sources were opened and the cited locations read. Search
results from aggregators and expository pages were not used as proof
evidence. Zelik's earlier notes and the Kostianko--Zelik 1D
reaction--diffusion--advection paper were also opened for context; no
theorem from them is imported. No exact prior theorem for this combined
query claim was located in this bounded check. That is not evidence
that the claim is new.

Query log:

1. `randomized approximation nonlinear functionals smooth functions integration Taylor expansion complexity elliptic semilinear PDE Heinrich`
2. `reaction diffusion equation large diffusion asymptotic phase invariant manifold spatially homogeneous solutions Allen Cahn`
3. `"randomized" "nonlinear functionals" Heinrich`
4. `"Monte Carlo" "nonlinear integral equations" complexity`
5. `"asymptotic phase" "inertial manifold" "smooth" reaction diffusion`
6. `"reaction diffusion" "large diffusion" "invariant manifold" Hale`
7. `"Heinrich" "nonlinear" "complexity" "randomized" equations`
8. `"randomized" "smooth functional" "approximation" integration`
9. `"inertial manifolds" "smoothness" "spectral gap" Zelik 2024 phase`
10. `"Monte Carlo" "nonlinear functionals" "Taylor"`
11. `"randomized" "nonlinear" "separation of the main part"`
12. `"Smooth extensions for inertial manifolds" arxiv`

## 10. Independent-audit handoff

The proposed theorem is ready for a conventional independent audit;
implementation is not authorized by this report. The highest-risk
proof interfaces are precise and finite in scope:

- The common-Gaussian covariance domination (4.3)--(4.5), needed for
  the integrated sup norms of actual derivative kernels.
- The centered-kernel energy induction and the two-centered-factor
  estimate (4.8)--(4.11), including total variation rather than just
  multilinear operator norms.
- The positive-partition coefficient bound (6.3) and the finite-
  difference/known-surrogate construction, which must not be read as
  free access to `A(v)` or as querying every fine residual-grid value.
- The uniform oracle accounting `4k^d`, the equality case `d=4s`, and
  the distinction between the claimed query bound and unboundedly
  expensive finite auxiliary computation.

The derivation is theory only. No numerical test, Lean proof, executable
solver, measured timing, or reproducibility gate is claimed. The result
should stay outside the accepted ledger until these interfaces pass.

Research-role metadata: T56 was assigned the `gpt-6-astra`/`max`
research settings. This worker made no model-setting change; the exact
backend configuration is not independently exposed in its tool context.
