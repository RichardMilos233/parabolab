# T101: paid fractional known-profile solver and long-horizon upper

Date: 2026-09-29. Conventional proof candidate, pending independent
review and root acceptance. Requested research routing is
`gpt-6-astra/max`; actual serving backend and effort are not exposed
to this worker.

**Verdict: the paid solver gate succeeds for every fixed
`0<beta<=1`.** It supplies a same-class long-horizon **upper** bound
with `O(exp(2d T/(2s+d)))` scalar queries and that exponential times
a polynomial in `1+T` paid work. This file proves no lower bound,
matching complexity, finite-bit bound, implementation, or novelty.

The replacement for an invalid all-beta analytic spatial tail is
a stretched-exponential Fourier tail with exponent
`theta=min(1,2beta)`. A separate, cutoff-independent complex-time
semigroup bound makes the deterministic time integrator affordable.
Spatial analyticity and complex-time analyticity are different
properties; the latter does not require the former.

Only this new T101 file is changed. Frozen evidence, accepted ledgers,
run state, E4/E5, configuration, numerical code, and Lean are untouched.

## 1. Exact statement, primitive model, and source locks

Fix integers `d,s,p>=1`, real `c>0`, and `0<beta<=1`. Put

    D=2p+1,       alpha=2beta,       theta=min(1,alpha),
    eta=ceil((2d+8)/theta),
    a_solver=eta*d+5d+20,
    A_work=a_solver+ceil(d(d+2)/theta)+2,
    A_array=eta*d+ceil(d(d+1)/theta).

On the normalized unit torus `X=(R/Z)^d`, let `S_t` be the actual
bounded real solution flow of

    u_t=A u+u-u^D,       A=-c(-Delta)^beta,
    A exp(2pi i nu.x)=-a_nu exp(2pi i nu.x),
    a_nu=c(4pi^2 |nu|^2)^beta,       a_0=0.             (1.1)

The unknown initial datum belongs to exactly the signed class in
04ab:

    V={v smooth periodic real: ||v||inf<=1/2,
       max_(|mu|<=s)||partial^mu v||inf<=1,
       min v<0<max v}.                                (1.2)

There is no uniform bound above derivative order `s`, analytic
radius, mean margin, basin promise, or restriction on unstable modes.
The only acquired information about `v` is an exact scalar `v(x)`.
All acquisitions count, including preprocessing and repeated points.

Write

    q=s+d/2,       gamma=d/q=2d/(2s+d),
    J=ceil(1+d/(2s)),       m=J-1.

For every prescribed real `T>=2` there is a measurable, almost-surely
halting algorithm returning an explicitly indexed real Fourier array
`U_T`, with

    sup_(v in V) (E||U_T-S_Tv||inf^2)^(1/2)<=1/8,
    queries <=[1+J(J-1)/2] k^d on every seed,
    k^d<=C exp(gamma T),
    sup_(v in V) E Work_T<=C exp(gamma T)(1+T)^A_work. (1.3)

The spatial supremum is inside the expectation. The final array has
at most `C(1+T)^A_array` entries. Its evaluation at a prescribed
point costs polynomial work and no new query. A deterministic
constant-work patch gives error at most `3/32` for `0<=T<=2`.

Thus both point and strong-profile query infima at RMS tolerance
`1/4` have upper bound `C exp(gamma T)`. The corresponding paid-work
infima have upper bound `C exp(gamma T)(1+T)^A_work`. No `Theta`
claim is made here. Constants depend on the fixed parameters and
need not be uniform as `beta` or `c` tends to zero or as the degree
or dimension grows. Accuracy is at each prescribed horizon, not
simultaneously at every time.

Paid work charges every acquisition, arithmetic operation,
comparison, floor/ceiling, integer/index operation, stored-value
access, `exp,log,sin,cos`, positive square root, and scalar uniform,
exponential, or Gaussian draw with known parameters. Complex
arithmetic is finitely many real operations. Fixed public constants
and ideal finite integer/address words are permitted. Integration,
Fourier transforms, positive-stable draws, evolved PDE values, and
arbitrary known-function evaluations are not extra free primitives.
This is exactly the inherited exact-real model, not bit complexity.

The paid known-profile theorem used in (1.3) is the following.
Fix also public `B>=1` and `rho0>0`. If an actually evaluable real
smooth periodic `q0` satisfies

    ||q0||inf<=1,       ||q0||_(G_(rho0/R))<=B,       R>=1,
    ||q||_(G_rho)=sum_mu rho^|mu|
                               ||partial^mu q||inf/(mu!)^2,

and each lookup costs at most `Wq` actual operations, then for
`S>=0`, `P>=1` a finite deterministic algorithm gives

    ||U-S_Sq0||inf<=exp(-P),
    Work<=C R^d E^a_solver(1+Wq),
    E=1+P+S+log(R+1),
    H=ceil(C R E^eta).                               (1.4)

The output has box radius `H` and at most `(2H+1)^d` real entries.
The constant in (1.4) can also depend on `B,rho0`. The algorithm
is specified below; neither PDE values nor Fourier coefficients
of `q0` are supplied to it.

Paths in this table are relative to the current research run.

| Locked dependency | SHA256 |
| --- | --- |
| `04ab-odd-power-long-horizon-complexity.md` | `a8bd72ec33c69aae4d50126c72f6fd75ac4e1625cb08cfcef6a1b310918d18c0` |
| `04ac-fractional-fixed-time-fields.md` | `3330cccbe4fd4f666569b1f94401a7d8308d3a2ec5302f02616fd188c253ae3d` |
| `reviews/T94-odd-power-long-horizon-feasibility.md` | `2600c29a2823aefd9a69578de113bc511179d97bdfbea7eb3a6861ac28b7e1d9` |
| `reviews/T95-fractional-diffusion-field-feasibility.md` | `9bc1d42d582f75b96a4e562dacbc925cbd01151b2a3b4702c5dc2b0a1ab99d74` |
| `reviews/T97-fractional-field-independent-audit.md` | `9e38a6d166806997d9c42ab8653615edad0a47b0fc1fa81dc9e31e980f5dec90` |
| `reviews/T81-fixed-burnin-all-diffusion-upper-proof.md` | `d9b249ed669897df319ca712fc4ad26625fc97e1a9b32b79eacaf497b290bae5` |
| `reviews/T84-all-diffusion-upper-independent-audit.md` | `39cd98fcf957badbe382123bd1960eac7fb99441114c9433bd9ee0ff2d256d7d` |

The new analysis below establishes the fractional solver rather
than treating T94's Gaussian spatial or time estimates as unchanged.
T81/T84 supply the already audited finite interpolation/saturation
and scalar collocation algebra, whose relevant details are restated.
T94 supplies the odd-power bounded parent and degree-dependent
saturation thresholds. T95/T97 supply the actual fixed-time fields.

## 2. Actual real flow, domination, and invariant bounds

The fractional semigroup `P_t=exp(tA)` is a positive, constant-
preserving contraction on `C(X)`, strongly continuous there. Its
construction and normalization are T95 Section 3: one stable clock
per edge is shared across all spatial coordinates. This supplies
the isotropic multiplier in (1.1), not a sum of coordinate powers.

Local mild Picard iteration in a bounded ball of `C(X)` applies to
the polynomial `f(z)=z-z^D`. A shifted reaction makes its local
iteration order preserving. Since `f(-1)=f(1)=0`, comparison with
the constants `+/-1` keeps closed-unit initial data in that interval;
bounded continuation gives a global solution. Uniqueness follows
locally by the polynomial Lipschitz bound and then by restarts.

For two such solutions the difference has bounded real secant
potential `b(t,x)` satisfying

    1-D<=b<=1,

because `f'(z)=1-D z^(D-1)`. The positive propagator for `A+b`
is dominated by `exp(t-r)P_(t-r)`: shift by `D-1`, expand the
positive Volterra series, and bound the resulting nonnegative
potential above by `D`. The simplex series sums to the stated
exponential. Consequently

    |S_t v-S_t w|<=exp(t)P_t|v-w|,
    ||S_t v-S_t w||inf<=exp(t)||v-w||inf.             (2.1)

This argument uses positivity of the actual fractional semigroup.
It assumes no positivity of Fourier projection or of a numerical
trajectory.

Constants are annihilated by `A`. The scalar flow is therefore
exactly

    phi_t(z)=z exp(t)
       /[1+z^(2p)(exp(2pt)-1)]^(1/(2p)).             (2.2)

Comparison gives, for all inputs in (1.2),

    ||S_1v||inf<=sigma_p
      =[1+(2^(2p)-1)exp(-2p)]^(-1/(2p))<1.          (2.3)

The formula is evaluated using positive-base `exp/log` powers and
the separate value zero at `z=0`. It is independent of the spatial
diffusion, as it must be. The strict margin depends on `p`.

## 3. A uniform Wiener bound after a fixed positive time

This first new bridge uses the `j=0` part of the accepted field
proof on the **closed** unit ball. It does not extend a Frechet
domain by assertion.

The odd-power parent and branching rate are

    M(y)=(sum_(i=1)^D y_i-product_(i=1)^D y_i)/(D-1),
    lambda=D-1.                                      (3.1)

At cube corners `|M|<=1`; multiaffine interpolation proves that
bound on the cube. Also `lambda(M(z,...,z)-z)=z-z^D`.
The first-split identity identifies its bounded tree expectation
with the actual mild flow from Section 2. These are the classical
bounded branching/voting ingredients already checked in T94.

Put `r=d+1` and `ell0=r+d=2d+1`. Let `H_r` be T95's explicit
Gaussian-shell constant and set, for fixed `delta>0`,

    V_j(delta)=H_r(1+Mbar_ell0(delta))
                   exp(lambda delta(D^(2j+ell0)-1)),

where, with `b=ceil(ell0/beta)`, one allowed choice is

    Mbar_ell0(delta)
      =[1+(b-1)!]/[beta(ell0-1)!]*(c delta)^(-ell0/beta).
                                                               (3.2)

At `beta=1` the sharper value `(c delta)^(-ell0)` is available.
Every displayed constant has a finite public primitive program.

Given any `q in C(X)` with `||q||inf<=1`, T95's analytical field
at order zero is

    F_omega(q)=h_(2a)(.-U)
                   P_tree(q(U+Z_1),...,q(U+Z_n)).

The leaf polynomial is bounded by one on the **closed** cube.
Thus `||F_omega(q)||_r<=||h_(2a)||_r`, including when a leaf
value equals an endpoint. T95's measurability, common-Gaussian
translation identity, and `j=0` second-moment envelope still apply
without differentiation or an open-ball assumption. Bochner
integration and bounded point evaluation give

    S_delta q=E F_omega(q) in H^r,
    ||S_delta q||_r<=sqrt(V_0(delta)).                (3.3)

Let `W` denote the Wiener algebra, with
`||u||_W=sum_nu|uhat(nu)|`. Cauchy--Schwarz gives

    ||u||_W<=E_d||u||_r,
    E_d^2=1+4d 3^(d-1).

The second bound is the same explicit Fourier-shell bound as T95.
Accordingly

    ||S_delta q||_W<=B_delta,
    B_delta=max(1,E_d sqrt(V_0(delta))),
                       uniformly over ||q||inf<=1.   (3.4)

This is a regularity proof, not a procedure that samples or queries
an unknown `q` to estimate its norm. No field is executed to supply
a free datum to the deterministic solver.

## 4. Weighted Wiener smoothing, with the required overlap

For `b>=0` define

    ||u||_(W_b)=sum_nu exp(b|nu|^theta)|uhat(nu)|,
    theta=min(1,alpha),       kappa_F=c(2pi)^alpha.

Since `0<theta<=1`, the triangle and concavity inequalities give
`|nu+mu|^theta<=|nu|^theta+|mu|^theta`. The weighted convolution
inequality proves that every `W_b` is a Banach algebra. This is
the precise reason for using `theta`, rather than `alpha` when
`alpha>1`.

Choose `a=kappa_F/2`. For `t>=s0>=0`, at every nonzero integer
frequency `|nu|>=1`,

    exp(a t|nu|^theta) exp(-kappa_F(t-s0)|nu|^alpha)
                         <=exp(a s0|nu|^theta).      (4.1)

The zero frequency also satisfies the inequality. Hence the heat
map contracts from `W_(a s0)` into `W_(at)`.

If `||u0||_W<=B0`, `B0>=1`, weighted mild Picard iteration on

    sup_(0<=t<=h)||u(t)||_(W_(at))<=2B0

is invariant and contractive whenever

    h[2B0+(2B0)^D]<=B0/2,
    h[1+D(2B0)^(D-1)]<=1/2.                          (4.2)

Indeed (4.1), the algebra inequality, and integration along real
time bound the nonlinear map and its difference by exactly these
two expressions. Use curves continuous into the unweighted `W`
with finite displayed weighted supremum norm. This is complete:
a Cauchy sequence also converges uniformly in `W`, and weighted
norm convergence follows at every time. The mild map is continuous
into `W`; for each fixed output time its integrand is strongly
measurable in the separable weighted sequence space, by coordinate
measurability, and has the integrable bound above. Its Bochner
integral therefore exists with that bound. Picard contraction in
this space gives the fixed point. Embedding into `C(X)` and mild
uniqueness identify it with the actual PDE.

Now consider the known input of (1.4). The Gevrey norm `G_rho`
is a Banach-algebra norm: the normalized product rule has
coefficient `1/binom(mu,nu)<=1`. Real fractional heat commutes
with derivatives and contracts their sup norms. Dominated summation
gives strong continuity in that norm. Define a positive fixed
`h0<=1` by, for example,

    h0=min(1, B/[2(2B+(2B)^D)],
                    1/[2(1+D(2B)^(D-1))]).

Gevrey mild Picard gives

    ||S_tq0||_(G_(rho0/R))<=2B,       0<=t<=h0.       (4.3)

Integrate by parts in a coordinate of largest frequency. The
derivative bound `2B (R/rho0)^j(j!)^2`, with an integer
`j` proportional to `sqrt(|nu|/R)`, gives an exponential in
`-sqrt(|nu|/R)`. Summing integer shells and absorbing the
polynomial shell factor into half that exponent yields fixed
positive constants `C0,b0` with

    sum_(|nu|inf>H)|uhat(t,nu)|
       <=C0 R^d exp(-b0 sqrt(H/R)),       0<=t<=h0.   (4.4)

The bound also covers small `H/R` after increasing `C0`. No
derivatives of an unknown input are acquired in this argument.

Choose

    delta=h0/4,
    h1=min(h0/4,
            B_delta/[2(2B_delta+(2B_delta)^D)],
            1/[2(1+D(2B_delta)^(D-1))]),
    t_star=delta+h1<=h0/2,       b1=a h1>0.           (4.5)

For any real time `t>=t_star`, restart the actual bounded PDE at
`t-t_star`. Section 3 gives Wiener norm at most `B_delta` after
the first `delta`. Apply (4.2) for the next `h1`. Thus, uniformly
over all continuous closed-unit initial profiles,

    sum_nu exp(b1|nu|^theta)|uhat(t,nu)|<=2B_delta,
                                                    t>=t_star,
    sum_(|nu|inf>H)|uhat(t,nu)|
                <=2B_delta exp(-b1 H^theta).         (4.6)

The overlap `t_star<=h0/2` is explicit. There is no time gap
between the initial Gevrey interval and the uniformly smoothed
interval, even if `B_delta` is very large and `h1` very small.
For the known input (1.4), at every real time `0<=t<=S`,

    ||(I-P_H)S_tq0||inf<=t_H,
    t_H=C0 R^d exp(-b0 sqrt(H/R))
                            +2B_delta exp(-b1 H^theta).        (4.7)

For an arbitrary closed-unit continuous input, (4.6) applies at
time one because `t_star<=1/2`. It supplies the small output
cutoff used in Section 9. When `beta<1/2`, (4.6) asserts a
stretched-exponential tail, not an analytic strip.

## 5. Cutoff-independent complex-time bound

For the deterministic time solver we need

    ||P_z||_(C(X;C)->C(X;C))<=K_sec,
        z!=0, |arg z|<=pi/4,                         (5.1)

with fixed `K_sec` independent of `|z|` and the Fourier cutoff.
The following elementary Fourier proof also makes clear that
`alpha=1` is not a gap in the argument.

### 5a. An explicit annular decomposition

Let `w=exp(i phi)`, `|phi|<=pi/4`, and consider the Euclidean
multiplier `m_w(xi)=exp(-w|xi|^alpha)`. In this section `xi` is
an ordinary Euclidean Fourier variable, not a torus index.

Choose the explicit smooth radial cutoff

    eta0(y)=1-wflat((|y|^2-1)/3),

where `wflat(t)=exp(-1/t)/(exp(-1/t)+exp(-1/(1-t)))` in
`0<t<1`, extended by zero and one. Thus `eta0=1` on the unit
ball and zero outside radius two. Put

    psi(y)=eta0(y)-eta0(2y).

This is supported in `1/2<=|y|<=2`. Telescoping gives, for
`xi!=0`,

    m_w(xi)=eta0(xi)
      +sum_(j<=0)[m_w(xi)-1]psi(2^(-j)xi)
      +sum_(j>=1)m_w(xi)psi(2^(-j)xi).              (5.2)

There are only finitely many nonzero annular terms at each
nonzero frequency. At zero the right side is one.

Set `l=ceil((d+1)/2)` and `M=2l>d`. For a smooth function `b`
supported in the radius-two ball, Fourier integration by parts
using `(1-Delta_y)^l` gives

    ||inverseFT b||_L1(R^d)
                      <=C_inv max_(|mu|<=M)||partial^mu b||inf,
    C_inv=(2pi)^(-d)4^d(1+d)^l
                [2^d+2^(2d)/(1-2^(d-2l))].          (5.3)

For the last factor, integrate `(1+|x|^2)^(-l)` over the unit
cube and the dyadic outer cubes. Scaling `b(xi)` to `b(2^-j xi)`
does not change the `L1` norm of its inverse transform.

On the fixed annulus, all derivatives of `|y|^alpha` through
order `M` have public finite bounds. Here is a finite way to
obtain them, without an optimization or differentiation oracle.
Keep terms `C y^mu |y|^(alpha-2k)`. Differentiation in coordinate
`i` replaces each term by the two terms

    C mu_i y^(mu-e_i)|y|^(alpha-2k),
    C(alpha-2k)y^(mu+e_i)|y|^(alpha-2k-2).

Omit the first term when `mu_i=0`, and discard zero coefficients.
Start with `(C,mu,k)=(1,0,0)`, apply at most `M` recursions,
and bound a term on the annulus by
`|C| 2^(|mu|+|alpha-2k|)`. Powers of two use `exp/log`.

The cutoff derivative bounds can also be obtained by a finite
recurrence. On `(0,1)`, write each derivative of `phi(t)=exp(-1/t)`
as a finite sum of terms `a_m t^-m phi(t)`. Differentiation replaces
one such coefficient by `-m a_m` at power `m+1` and `a_m` at
power `m+2`. Bound `t^-m exp(-1/t)` by `m^m` for `m>=1` and
by one for `m=0`; the resulting absolute coefficient sums are
public bounds `P_j` for `phi^(j)`. The denominator
`Dflat=phi(t)+phi(1-t)` has `Dflat>=exp(-2)` and derivative
bounds `2P_j`. With

    R_0=exp(2),
    R_j=exp(2) sum_(i=1)^j binom(j,i) 2P_i R_(j-i),

differentiate `Dflat*(1/Dflat)=1` to bound the reciprocal
derivatives by `R_j`. Product differentiation then bounds all
`wflat` derivatives through order `M`. Its endpoint derivatives
match the constant pieces by flatness. Finite quadratic
composition and the factor `2^|mu|` in `eta0(2y)` give bounds
for `eta0,psi`. These are finite sums and recurrences on public
data, consistent with T81/T84's stronger Gevrey estimates;
no derivative or supremum oracle is used.

Consequently the finite product and chain rules produce public
constants `C_eta,C_low,C_high` such that, with
`lambda_j=2^(j alpha)` and `a_*=2^(-alpha)/sqrt(2)`,

    max_(|mu|<=M)||partial^mu eta0||inf<=C_eta,
    max_(|mu|<=M)||partial^mu
       [(exp(-w lambda_j |y|^alpha)-1)psi(y)]||inf
                         <=C_low lambda_j,          j<=0,
    max_(|mu|<=M)||partial^mu
       [exp(-w lambda_j |y|^alpha)psi(y)]||inf
          <=C_high(1+lambda_j)^M exp(-a_* lambda_j), j>=1.
                                                               (5.4)

For the low zeroth derivative use the integral of the exponential
derivative and `Re w>=0`. Every positive-order term has at least
one factor `lambda_j<=1`. For high derivatives use `Re w>=1/sqrt(2)`
and `|y|>=1/2`; the number of lambda factors is at most `M`.
These observations prove (5.4) and specify finite sums for all
its constants.

The low sum is bounded by `C_low/(1-2^-alpha)`. For the high
sum use

    (1+lambda)^M exp(-a_* lambda)
       <=(4M/a_*)^M exp(-a_* lambda/2),       lambda>=1,
    2^(j alpha)>=(1+j(2^alpha-1)).

With `r_*=exp[-a_*(2^alpha-1)/2] in (0,1)`, (5.2)--(5.4)
therefore give the explicit finite majorant

    K_sec=max(1, C_inv[C_eta+C_low/(1-2^-alpha)
       +C_high(4M/a_*)^M exp(-a_*/2) r_* /(1-r_*)]).  (5.5)

The inverse-transform series converges absolutely in `L1`.
Its Fourier transform is `m_w`; uniqueness identifies the correct
complex heat kernel. In particular this is not an estimate of
the absolute Fourier series, which would diverge as time tends
to zero.

### 5b. Scaling, periodization, holomorphy, and primary check

For `z=|z|w`, changing variables by `(c|z|)^(1/alpha)` in
Euclidean space preserves the kernel's `L1` norm. Periodization
does not increase that norm, since integration of the sum of
absolute values over the torus equals the Euclidean integral.
Its torus coefficients are exactly `exp(-c z|2pi nu|^alpha)`.
This proves (5.1), including `alpha=1` and `alpha=2`.

On compact subsets of `Re z>0`, the torus Fourier series and
all its time derivatives converge absolutely and uniformly.
It is therefore holomorphic in operator norm there. At zero,
strong continuity within the closed sector follows first for
trigonometric polynomials and then for all continuous functions
by their uniform density and (5.1). On any Fourier subspace the
same operator bound holds without an extra projector norm.

As an external primary check, Zhao--Zheng, arXiv v2 (2022),
Theorem 1.1 on PDF page 2, treats complex kernels for `alpha<1`
and `alpha>1`. Scaling its estimates to `|z|=1` and using
`cos(arg z)>=1/sqrt(2)` gives integrable bounds at zero and
infinity, consistent with (5.1). That theorem omits `alpha=1`;
the direct proof above covers it. The source is not used as an
uncounted computational oracle. [Zhao--Zheng, *Uniform Complex
Time Heat Kernel Estimates without Gaussian Bounds*](https://arxiv.org/pdf/2012.08763).

No result restricted to `alpha>1` is substituted for the small-
fractional-order case. The elementary bound (5.5) can be large
as `alpha` tends to zero, which is consistent with the theorem's
fixed-parameter quantifiers.

## 6. Spatial discretization and its nonlinear stability

Let `P_H` be the rectangular Fourier projector and use the
public majorant

    Lambda_H=[4(1+log(2H+2))]^d
                      >=||P_H||_(inf->inf)>=1.

The one-dimensional Dirichlet-kernel estimate follows by
integrating its bound by the minimum of `2H+1` and a constant
over distance to the nearest integer; tensoring gives this
safe majorant. It grows as `(1+log(H+1))^d`.

Consider the exact finite-dimensional Galerkin ODE

    U'=A_H U+P_H f(U),       f(U)=U-U^D,              (6.1)

where `A_H` is the restriction of `A`. Initialize it as described
below, with error `epsilon0` relative to `P_Hq0`.
Until `||U||inf` reaches two, the real Lipschitz constant

    L2=1+D 2^(D-1)

is safe. Compare the two mild equations, use real heat
contraction, and add the true solution tail (4.7). Gronwall gives

    ||U(t)-S_tq0||inf
        <=(epsilon0+t_H) exp(L2 Lambda_H S),
                                           0<=t<=S. (6.2)

Making the right side at most `exp(-P)/4` also makes it less
than `1/4`. Actual invariance then gives `||U||inf<=5/4`,
closing the stopping argument and proving finite-ODE continuation
to `S`. There is no Galerkin maximum principle in this proof.

Choose exactly the cutoff form in (1.4):

    H=ceil(C R E^eta),       eta=ceil((2d+8)/theta).

It satisfies `eta/2>=d+4` and `eta theta>=2d+8`.
For a sufficiently large fixed `C`, the two tail exponents in
(4.7) both dominate

    P+L2 Lambda_H S+d log R+O(1).

Indeed `log(H+1)<=C'(1+log C)E`, whereas
`sqrt(H/R)>=sqrt(C) E^(d+4)` and
`H^theta>=C^theta E^(2d+8)`. Here `R>=1`; dropping `R^theta`
only weakens the second lower bound. Polynomial growth in
`log C` is dominated by `sqrt(C)` and `C^theta`, so choosing
`C` is not circular. The value of `theta>0` is fixed.

For initialization, take a power-of-two grid size `Q0>=4H`
in each coordinate, evaluate the actual known `q0` there, and
perform a tensor FFT. Keep the box of radius `H`. Absolute
Fourier summability follows from its initial Gevrey bound.
Every retained residue has distinct representatives modulo
`Q0`, so the aggregate alias error is bounded by the single
Fourier tail beyond `Q0-H`. There is no extra mode-count
factor. Equation (4.4) bounds `epsilon0`. Increasing the same
fixed cutoff constant makes (6.2) at most `exp(-P)/4`.

To compute the nonlinearity in (6.1), use a power-of-two grid
strictly larger than `2D H` per coordinate. The full product
`U^D` has support in the box of radius `D H`; hence transforming,
taking the fixed integer power, transforming back, and restricting
computes exactly `P_H(U-U^D)` without aliasing. The strict
padding condition covers every fixed odd degree, not just cubic.
Butterfly arithmetic, trigonometric twiddles, arrays, integer
powers, and padding cost `O_(d,D)(H^d log(H+1))`. No FFT is
charged as one operation. Exact conjugate symmetry preserves
real-valuedness.

## 7. A finite deterministic time algorithm

### 7a. Complex neighborhoods of the actual Galerkin trajectory

The real Galerkin trajectory is bounded by `5/4` from Section 6.
Set

    Bcx=4K_sec,       Fcx=Bcx+Bcx^D,
    Lcx=1+D Bcx^(D-1),
    rho_H=1/[16K_sec Lambda_H(1+Fcx+Lcx)].

Radial complex-time mild Picard iteration, using (5.1), proves
a bounded holomorphic solution on the forward sector of radius
`rho_H` from every real starting state on that trajectory.
The radius-`Bcx` ball is invariant: its linear term is at most
`(5/4)K_sec`, and its nonlinear increment is at most `1/16`.
Its Lipschitz factor is at most `1/16`. These are analytical
restarts; the algorithm does not request any exact restart value.

The disk crossing the negative real axis at time zero requires
a separate estimate. For `D_H=(2H+1)^d`, a direct coefficient
bound gives

    ||A_H V||inf<=M_H||V||inf,
    M_H=D_H c(4pi^2 d H^2)^beta.

Define `F4=4+4^D`, `L4=1+D 4^(D-1)`, and

    a_H=1/[16(1+M_H+Lambda_H(F4+L4))].               (7.1)

Finite-dimensional complex ODE Picard iteration on the radius-
four ball gives an actual disk of radius `a_H` about time zero.
Its map stays within that ball and has Lipschitz factor at most
`1/16`. In particular

    log(1/a_H)<=C(1+log(H+1)).

A cutoff-independent disk at zero is not asserted. The finite
generator has size at most `C H^(d+alpha)`, and its logarithm,
rather than that size itself, determines the number of startup
panels.

### 7b. Public panels and forcing interpolation

Choose

    L=ceil(C_time E^(d+4)),
    beta_L=8(1+log(L+1)),
    h=1/[1600K_sec(1+Fcx+Lcx)(1+F4+L4)
                                      Lambda_H beta_L].

Then `h<=min(1/100,rho_H/100)` and

    L4 h Lambda_H beta_L<=1/4,
    F4 h Lambda_H beta_L<=1/2.                       (7.2)

For `S=0`, return the initialized Fourier polynomial. For `S>0`,
start with a panel of length
`min(S,a_H/16,h/16)`. If it does not reach `S`, double with
panels `[t,2t]`, truncating a panel at `S` if necessary, until
either finished or the endpoint `b0` first lies in `[h,2h)`.
If `S>b0`, use `ceil((S-b0)/h)` equal positive remaining panels.
They have length at most `h`; a small last interval causes no
problem for the bounds below. All counts are finite and public.

The parameter-two Bernstein ellipse of the first panel lies
inside the initial disk. For `[1,2]` that ellipse has real part
at least `7/8`, imaginary part in absolute value at most `3/8`,
and modulus less than three. Thus each doubled startup panel,
including one truncated at `S`, fits in the forward sector
based at zero. For a later panel `[b,b+ell]`, use the sector
based at `b-h>=0`: its relative ellipse has real part at least
`h-ell/8>=7h/8`, imaginary part at most `3ell/8<=3h/8`,
and modulus below `3h`. These estimates do not require
`ell>=h/2`.

It follows that every panel has the same ellipse parameter and

    n_pan<=C[1+log(H+1)+log(L+1)+S Lambda_H beta_L]
                                           <=C E^(d+2).       (7.3)

The forcing `P_H f(U(t))` is bounded there by `C Lambda_H`.
Cauchy estimates on the Banach-valued Chebyshev coefficients
and the finite Lobatto alias identity give interpolation error
`C Lambda_H 2^-L`. The Lobatto Lebesgue bound by `beta_L`
follows from the elementary cardinal-function harmonic sum;
this is the same scalar interpolation lemma used and audited
in T94 Section 4c and T84 Section 5. No time integration oracle
is used by the algorithm.

### 7c. Nodal contraction, a fixed iteration count, and stability

On a panel of length `ell`, let `theta_i`, `0<=i<=L`, be
Lobatto nodes rescaled to `[0,1]`, and `l_j` their cardinal
polynomials. From the computed starting array `U_b`, iterate
the actual finite map

    V_i=exp(theta_i ell A_H)U_b
      +ell integral_0^(theta_i) exp((theta_i-r)ell A_H)
                             sum_j l_j(r)P_H f(V_j) dr.        (7.4)

Section 7d evaluates these integrals by finite formulas. In the
real nodal sup norm, with `||U_b||inf<=2`, the radius-four ball
is invariant and the Lipschitz factor is

    q_ell=L4 ell Lambda_H beta_L<=1/4.

The linear heat start has norm at most two. Taking exactly `L`
Picard iterations gives error at most `C 4^-L` from the unique
fixed point in that ball. A fixed iteration count is used even
if intermediate answers happen to be close.

Insert the exact Galerkin nodal values into (7.4). If the initial
panel error is `e`, the terminal error satisfies

    e_next<=e/(1-q_ell)
       +C ell Lambda_H 2^-L/(1-q_ell)+C 4^-L.

Since the panel lengths sum to `S`, the product of the first
factors is bounded by `exp(C S Lambda_H beta_L)`. Hence the
global time error is at most

    exp(C S Lambda_H beta_L)
              [C S Lambda_H 2^-L+C n_pan 4^-L].     (7.5)

For a sufficiently large fixed `C_time`, this is at most
`exp(-P)/4`. To see the noncircular choice, `Lambda_H<=C E^d`
and `beta_L<=C(1+log C_time+log E)`, whereas `L` grows linearly
in `C_time` and as `E^(d+4)`. The exponent and prefactors in
(7.5) are absorbed by that margin. Induction keeps computed
starts within `5/4+1/4<2`, closing this second bootstrap.

The stability exponent contains neither `H^alpha S` nor the
number of startup panels. Replacing it by either quantity
would fail to prove the desired paid bound; (7.5) is the actual
estimate used.

### 7d. All weights, powers, and operations are finite primitives

For a nonzero frequency the exact coefficient

    a_nu=c exp(beta log(4pi^2 |nu|^2))

uses permitted primitives and a positive logarithm argument.
The zero mode is set to zero before taking a logarithm. For a
positive panel length put `z=a_nu ell`. Expanding `l_j` in
monomials reduces (7.4) to

    I_k(z,theta)=integral_0^theta exp(-z(theta-r))r^k dr.

For `z>0`, use the exact finite recurrence

    I_0=(1-exp(-z theta))/z,
    I_k=theta^k/z-(k/z)I_(k-1),       k>=1.           (7.6)

For `z=0` use `theta^(k+1)/(k+1)`; for `theta=0` use zero.
The cardinal-polynomial denominators are nonzero because the
Lobatto nodes are distinct. Their nodes use cosine, and all
integer powers and polynomial coefficients use finite loops.

Weight construction costs `O(D_H L^3)` per panel. One Picard
step costs `O_(d,D)(D_H L^2+L D_H log(H+1))`, with the strict
`2DH` padding from Section 6 at every node. The `L` iterations,
all panels, initial known-profile evaluations, and array costs
therefore satisfy

    Work<=C n_pan D_H[L^3+L^2 log(H+1)]
                      +C D_H[log(H+1)+Wq].          (7.7)

Initialization and nonlinear padding use grid sizes within
fixed multiples of `H`; repeated doubling constructs them in
`O(log(H+1))` operations. A terminal Fourier evaluation is
`O_d(D_H)` and is included if requested.

Substituting `H<=C R E^eta`, `L<=C E^(d+4)`, and (7.3),
the largest exponent needed in (7.7) is

    eta*d+(d+2)+3(d+4)=eta*d+4d+14<a_solver.

This proves the work bound in (1.4), with room for parameter
preparation and indexing. Equations (6.2) and (7.5) give error
at most `exp(-P)/2`, within the stated `exp(-P)` budget. The
`S=0` case uses only the initialization bound.

Small-`z` cancellation in (7.6), large exact coefficients, and
complex arithmetic do not disappear; they are outside a bit
or floating-point theorem. The inherited model explicitly
counts exact operations on finite real magnitudes. No claim
about stable floating implementation is made.

## 8. The actual fixed-time derivative fields to be composed

At time one take the odd-power parent (3.1) in T95's construction.
With `r=d+1`, write `V_j=V_j(1)` from (3.2) and `B_j=sqrt(V_j)`.
For continuous known `g`, `||g||inf<1`, and `e=v-g`, the genuine
Frechet map and Taylor bound are

    E W_j=D^j S_1(g)[e,...,e],
    E||W_j||_r^2<=V_j||e||inf^(2j),
    ||S_1(g+e)-sum_(j=0)^(J-1)D^jS_1(g)[e^j]/j!||_r
                                      <=B_J||e||inf^J/J!,      (8.1)

where the Taylor assertion requires the full segment in the
open unit ball. T95/T97 establish Bochner measurability and
integrability and actual `C(X)`-Frechet differentiation, not
merely a family of pointwise derivative formulas.

For clarity, the sample on a completed clocked tree is

    W_j=h_(2a)(.-U) z,
    z=(n)_j C_I product_(b=1)^j e(U+Z_(I_b)).         (8.2)

Here `I` is a uniform ordered injection of distinct leaf labels,
`|C_I|<=1`, and the **whole** residual Gaussian vector is
independent of the extracted common Gaussian conditional on
the chronology and all scalar stable clocks. The same `U`
is used in all leaf locations. Unconditional Gaussian
independence is not asserted. Stable clocks are spatially shared,
and their positive-law primitive formula and endpoint guards
are those in T95 Section 2.

The actual output is `P_N W_j`, a finite real array. Its constant
coefficient is `z`; for one representative of each `{nu,-nu}`,
its cosine and sine coefficients are respectively

    2z exp(-4pi^2 a|nu|^2) cos(2pi nu.U),
    2z exp(-4pi^2 a|nu|^2) sin(2pi nu.U).             (8.3)

If `n<j`, it is zero without acquisition. Otherwise exactly
the selected at most `j` scalar values of `v` are needed.
Different labels can share a spatial point; repeated acquisitions
are still counted. The whole tree, its clocked Gaussian
recursion, tuple, known-leaf values, and `C_I` are prepared
before those queries.

For `K=(2N+1)^d`, the proved conditional and expected costs are

    Work(sample)<=C[(1+Gg)n+K],
    E Work(sample)<=C(1+Gg+K).                       (8.4)

These include the linear tree passes, exact stable primitives,
Gaussian arrays, finite corner evaluations for the mixed
partial, and all Fourier entries. No dense covariance sampler
or free stable distribution is introduced in this composition.

## 9. Coarse interpolation, projected means, and complete risk

### 9a. A known finite program from exactly k^d coarse values

Use the fixed tensor stencil and normalized Gevrey bump
partition from T81 Section 3 and T84 Section 2. Precisely,
integer translates of `exp(-1/(1-t^2))` on `|t|<1`, zero
elsewhere, have normalized denominator at least `exp(-4/3)`.
There are a bounded number of active translates. Tensor them
and attach the degree-`s-1` tensor stencil polynomials to the
`k`-grid, with periodic lifts.

The tensor stencils reproduce every polynomial of total degree
at most `s-1`. Comparing to the total-degree Taylor polynomial
at the evaluation point uses only derivatives through total
order `s`; it does not require higher tensor mixed derivatives.
The accepted quantitative bounds are

    ||v-g||inf<=Cint k^-s,
    ||partial^mu g||inf<=B0(C0 k)^|mu|(mu!)^2,
    ||g||inf<=3/4,       Gg<=C_(d,s),               (9.1)

provided `k>=k0>=2s` and `Cint k0^-s<=1/4`.
All records are built in `O_(d,s)(k^d)` paid operations from
exactly `k^d` values. Floor, periodic indexing, bounded-support
lookup, polynomial evaluation, and guarded bump evaluations
give the stated constant known-lookup cost. There is no new
unknown-input call when the stored `g` is evaluated later.

The derivative estimate gives a fixed Gevrey norm bound at
scale `R=k`, for a fixed sufficiently small `rho0`. Thus the
base solver in (1.4) applies with constants independent of `k`.

### 9b. Public budgets and a paid base value

From (4.6) at time one choose fixed `A_tail>=1,b_tail>0` with

    ||(I-P_N)S_1v||inf<=A_tail exp(-b_tail N^theta),
                                         for every v in V.    (9.2)

For `T>=2`, put `S=T-1`, `Lchi=25`, and define

    epsilon=exp(-S)/(16 Lchi),
    N=max(1,ceil(((S+log(32 Lchi A_tail))/b_tail)^(1/theta))),
    K=(2N+1)^d,
    Cstar=1+sum_(j=1)^m B_j Cint^j/j!
                                      +B_J Cint^J/J!,
    k=max(k0,ceil((4 E_d Cstar/epsilon)^(1/q))),
    M=k^d.                                          (9.3)

All real powers have positive bases and are evaluated by
`exp/log`; the public ceilings are allowed. Then

    N<=C(1+T)^(1/theta),       K<=C(1+T)^(d/theta),
    k^d<=C exp(gamma T).                              (9.4)

The last line follows directly from the ceiling inequality
and `epsilon^(-d/q)`. No power of `K` enters the query budget.
Equation (9.2) is at most `epsilon/2` with this `N`.

The order-zero mean is computed, not queried. Set

    D_N=sqrt(K)(1+dN^2)^(r/2),
    tau_base=epsilon/(4 E_d D_N),
    P_base=max(1,log(1/tau_base)).

Run the paid solver (1.4) from the actual known `g` for time
one and precision `P_base`, using scale `R=k`. Its cutoff can
be chosen at least `N` by increasing a fixed constant: `eta`
is greater than `1/theta`, and `E_base=O(1+T)`. For every
retained complex coefficient a sup error `tau_base` bounds its
coefficient error. Consequently

    ||P_N(U_base-S_1g)||_r<=D_N tau_base
                                      =epsilon/(4E_d).        (9.5)

The actual paid cost is `C k^d(1+T)^a_solver`. The additional
precision term `log D_N` is only `O(log(2+T))`. There is no
evolved-value or integral oracle hidden in (9.5).

### 9c. Hilbert means, Taylor remainder, and actual clipping

For each fixed `j=1,...,m`, take `M` independent complete
samples (8.3). For each fixed input, the coarse transcript and
`g` are deterministic. Hilbert centering and independence
between **copies** give

    E||M^-1 sum_(a=1)^M(P_N W_(j,a)-E P_NW_j)||_r^2
                                   <=V_j||v-g||inf^(2j)/M.    (9.6)

The cross-copy inner products vanish by centering and Fubini;
the second moments justify the operation. Frequencies inside
one copy may be correlated. Projection is an `H^r` contraction,
and (9.6) targets the projected mean, not a free full-profile
mean.

Form the real polynomial

    p_raw=P_N U_base
              +sum_(j=1)^m [1/(j!M)]sum_(a=1)^M P_N W_(j,a).

The segment from `g` to `v` has norm at most `3/4` and therefore
lies in the open unit ball. Hilbert Minkowski, (8.1), (9.1),
(9.5), and (9.6) give

    (E||p_raw-P_N S_1v||_r^2)^(1/2)
      <=epsilon/(4E_d)
        +sum_(j=1)^m B_j Cint^j k^(-js-d/2)/j!
        +B_J Cint^J k^(-Js)/J!
      <=epsilon/(4E_d)+Cstar k^-q
      <=epsilon/(2E_d).                              (9.7)

Here `Js>=s+d/2=q`. Derivatives of the time-one flow do not
impose any extra initial smoothness assumption.

Use the actual real basis `1,cos,sin`: clip its constant
coefficient to `[-1,1]` and all others to `[-2,2]`. Because
`||S_1v||inf<=1`, every target coefficient is in its corresponding
interval. The real Hilbert squared error equals

    e_0^2+(1/2)sum_(nu representatives)(1+|nu|^2)^r
                                     (e_(nu,c)^2+e_(nu,s)^2).

Coordinate interval projection decreases every summand. Thus
the clipped `p_N` still satisfies (9.7), although it can be
biased. The conversion from a complex array is
`c_(nu,c)=2 Re uhat(nu)`, `c_(nu,s)=-2 Im uhat(nu)`, matching
the positive sine coefficient in (8.3).

Sobolev embedding and the separately paid true tail (9.2)
now give the full strong bound

    (E||p_N-S_1v||inf^2)^(1/2)<=epsilon.              (9.8)

This step accounts for the omitted Fourier modes rather than
silently replacing the target by its projection.

## 10. Saturation and paid nonlinear continuation

Use the degree-dependent thresholds

    a_chi=(1+sigma_p)/2,
    b_chi=(1+a_chi)/2,
    sigma_p<a_chi<b_chi<1.

For `z>=0` define

    chi(z)=z,                                      z<=a_chi,
    chi(z)=z+(b_chi-z)
                 wflat((z-a_chi)/(b_chi-a_chi)),    a_chi<z<b_chi,
    chi(z)=b_chi,                                  z>=b_chi,

and extend oddly. Branches guard all divisions. The interior
denominator in `wflat` is at least `exp(-2)`. The function is
smooth, has range in `[-b_chi,b_chi]`, equals the identity on
the range in (2.3), and has Lipschitz constant at most 25:
its middle derivative is `1-wflat(t)+(1-t)wflat'(t)`, while
`0<=wflat'(t)<=8e<24`.

The flat exponential, reciprocal, affine rescaling, and product
estimates give public constants depending on `p` with

    sup_z|chi^(l)(z)|<=Achi Cchi^l(l!)^2.             (10.1)

These are exactly T94's degree-dependent saturation bounds,
not the cubic threshold transplanted to a different reaction.

For the clipped box polynomial,
`||partial^mu p_N||inf<=2K(2pi N)^|mu|`. The finite-jet
Faà di Bruno formula and

    sum_(mu_1+...+mu_l=mu)1/(mu_1!...mu_l!)=l^|mu|/mu!

give, for `n=|mu|>=1`,

    ||partial^mu chi(p_N)||inf
       <=Achi(2pi N)^n sum_(l=1)^n(2Cchi K)^l l! l^n
       <=Achi(C_(d,p) N K)^n(mu!)^2.                (10.2)

For the last inequality use `l!<=n!`, `l^n<=n^n<=e^n n!`,
`n<=2^n`, and `n!<=d^n mu!`. Summing at a sufficiently small
fixed Gevrey radius proves that

    qhat=chi(p_N),       ||qhat||inf<=b_chi<1,
    Rhat=N K,
    ||qhat||_(G_(rhohat/Rhat))<=Bhat,
    Wqhat<=C_d K.                                    (10.3)

The constants are uniform over every finite clipped array.
The evaluator is the actual finite Fourier sum followed by
the guarded transition, so its `K` cost is paid.

From (2.3), (9.8), and the global Lipschitz bound,

    (E||qhat-S_1v||inf^2)^(1/2)<=exp(-S)/16.

Run (1.4) from this known `qhat`, for time `S=T-1`, precision
`P_out=T+log(16)`, and scale `Rhat`. It has deterministic
conditional error at most `exp(-T)/16` on every completed
transcript. Apply (2.1) **before** taking expectations. Then
Minkowski gives

    (E||U_T-S_Tv||inf^2)^(1/2)
       <=exp(S)(E||qhat-S_1v||inf^2)^(1/2)+exp(-T)/16
       <=1/16+exp(-T)/16<=1/8.                      (10.4)

The nonlinear continuation is paid and uniformly controlled.
Its input is kept in the invariant interval by the explicit
saturation; no claim is made that its numerical Fourier
trajectory itself obeys a maximum principle.

## 11. Complete costs, termination, measurability, and short horizons

The grid and base solver cost `C k^d(1+T)^a_solver`.
The fixed `m` derivative orders cost, by (8.4), at most
`C k^d(1+K)` in expectation. For the last deterministic solve,

    Rhat<=C(1+T)^((d+1)/theta),
    Wqhat<=C(1+T)^(d/theta),
    E_out<=C(1+T).

Its cost is at most

    C(1+T)^(a_solver+d(d+2)/theta).

Together with (9.4), these prove the deliberately loose
`A_work` in (1.3). The final cutoff is at most
`C(1+T)^(eta+(d+1)/theta)`, proving the `A_array` entry bound.
Only the final array is counted as output; the base solver's
larger intermediate array is still fully charged as work.

Every unknown acquisition is either one coarse value or a
selected tuple value. Frequencies share a tuple rather than
requiring separate unknown values. Therefore, on every seed,

    Q_T<=k^d+M sum_(j=1)^m j
         =[1+J(J-1)/2]k^d.                          (11.1)

All stochastic preparation precedes a sample's acquisitions.
Even a null path whose tree preparation never terminates
cannot exceed the total query cap. Nonexplosion, finite tree
moments, and the fixed deterministic solver counts give
almost-sure halting and the stated expected work bound. There
is no algorithmic detection of the null nontermination set.

All finite operations are Borel: branch comparisons, uniform
endpoint guards, stable-clock logarithms on positive arguments,
Gaussian generation, guarded variance recursion, tuple selection,
finite Fourier entries, and the deterministic solver formulas.
At nonzero frequencies, `a_nu>0`; panel lengths are positive;
zero-frequency and zero-node divisions are separately guarded.
The `S=0` branch skips the panel construction entirely.

The output is an explicitly indexed finite real array, hence
defines a measurable `C(X)` random element. Its sup-norm loss
is measurable. For probability statements assign any fixed
array to the null nontermination set. Finite but off-promise
responses can first be clipped to `[-1/2,1/2]`; every computed
finite formula still terminates, even if its accuracy hypotheses
fail. Fixed iteration counts and final coefficient clipping
avoid unverified convergence or regularity tests.

For `0<=T<=2`, choose a fixed `k_*>=k0` with

    Cint k_*^-s<=exp(-2)/16.

Construct the same known `g` from its fixed grid, then use (1.4)
with `S=T`, fixed scale `k_*`, and precision `log(32)`. The
solver proof explicitly allows `S=0` and truncated startup
panels. Equation (2.1) gives interpolation propagation at most
`1/16`; numerical error is at most `1/32`. The deterministic
strong error is therefore at most `3/32`, with bounded work,
queries, and output size depending only on the fixed parameters.
There is no small-horizon field with a singular negative-moment
constant in this patch.

## 12. Scope, obstruction avoided, attribution, and provenance

The nonanalytic example in T95/T97 remains valid. When
`beta<1/2`, a small signed smooth series with coefficients
`exp(-k^zeta)`, `2beta<zeta<1`, has under the linear fractional
flow coefficients

    (delta/2)exp[-k^zeta-c t(2pi k)^(2beta)].

They satisfy no exponential-in-`k` bound. This forbids copying
the former analytic-tail argument for all fractional orders.
It does not contradict (4.6), which uses exponent `2beta` in
that regime. The new cutoff remains polynomial in the required
logarithmic accuracy because every `theta>0` is fixed.

The genuinely necessary replacements in this upper proof are:

1. A closed-unit order-zero field bound, then a Wiener bound,
   then weighted Wiener smoothing with an explicit overlap.
2. A fractional complex-time semigroup estimate independent
   of Fourier cutoff, including the case `alpha=1`.
3. The new cutoff exponent `eta`, the fractional eigenvalues
   in each paid scalar time weight, and strict degree-`D`
   product padding.
4. Separate true-tail error and projected Hilbert sampling
   error, followed by a paid Gevrey continuation interface.

Bounded voting/branching representations, stable subordination,
Kanter sampling, Fourier Gevrey algebras, complex semigroup
estimates, Fourier Galerkin methods, and polynomial collocation
are classical ingredients. The primary check above supports
the analytic context; it is not a claim of priority for this
composition or for any ingredient. No literature-wide novelty
search was performed.

This theorem does not assert a lower bound, exact optimal paid
work, uniformity as diffusion vanishes, a stable floating-point
implementation, a bit-cost estimate, variable diffusion,
systems, all inward polynomial long-time rates, or physical
coefficient rescaling. The normalized odd-power reaction and
the complete signed class in (1.2) are retained throughout.
Root's separate lower-bound investigation is not imported as
an assumption or result here.

The requested research skill configuration, routing, execution
rules, project instructions, and dirty workspace state were
checked. The only local mathematical source edits in this
task are this new file. T94, T95, and T97 had been read and
checked completely in this worker's prior assigned tasks;
their identical frozen hashes were reverified. For T101 I
freshly read both complete acceptance notes 04ab and 04ac,
T94's statement and upper/solver portions through Section 5,
T95's contract and Hilbert/Frechet passages, T97's statement
and locks, T84 Sections 2, 5, 6, and T81 Section 7a--7b.

External access for this task was a direct read of
`https://arxiv.org/pdf/2012.08763`, which returned v2 dated
27 September 2022; I read its title, generator normalization,
Theorem 1.1, and scaling statement. A requested screenshot
of PDF page 2 failed with a cache-miss error and supplied no
evidence. No search-engine query, Merz or Bae--Biswas read,
or claim to have checked those papers is made.

No numerical execution, symbolic experiment, random sampling,
unknown-input acquisition, PDE run, Lean build, or code change
was performed. All algorithms above are proved finite programs,
not executions reported as completed experiments. Root must
independently review this candidate before any acceptance.
