# T59 — independent audit of the signed-class query upper bound

**Verdict: GO for the conventional theorem in T56's stated scope.** I found
no blocking analytic, oracle, measurability, or endpoint gap. The proof
establishes a randomized exact-initial-value-query upper bound with
deterministic query cap `C exp(2dT/(2s+d))` and uniform absolute RMS below
`1/4`, for fixed integers `s>=1`, `1<=d<=4s`, on precisely the signed class
of accepted D25. Combining this upper bound with accepted D25 gives the
matching asymptotic minimax **query** rate in that range. It gives no matching
arithmetic-work bound.

This is an independent mathematical review, not a Lean certificate, executed
algorithm, numerical check, or novelty assessment. The frozen author source
was not edited. This worker owns only this new audit file. No accepted
ledger or downstream implementation authorization is changed by the file.

## Evidence, independence, and exact scope

The complete 717-line source reviewed was
`reviews/T56-signed-upper-feasibility.md`, SHA256
`0f0cd6a6fbe97d5746c42f2da94161284f4b4fb3da70b724b5992450388d5933`.
I read `04r-signed-many-bump-complexity.md` for the accepted D25 statement
and `04o-unstable-phase-query-lower-bound.md` for the exact oracle interface.
I checked the relevant centered-energy/smoothing passage of T50 and the
current run context and claim ledger. I did not use the root's preliminary
correspondence review as proof evidence.

During the review the root supplied the additional direct counterexample
`reviews/R03-signed-mass-counterexample-direct.md`, SHA256
`eecc30c81c4adea40dd3ca4e62d29c58c81097257c4832175794627eff840fef`.
I independently checked that complete argument as well; it passes and does
not need T56's differentiability theorem. Its verification appears below.

The precise upper theorem fixes the unit torus, the equation
`u_t=Delta u/2+u-u^3`, a target point, and the class

    v in C^infinity(T^d), ||v||infinity<=1/2,
    max_(|alpha|<=s) ||partial^alpha v||infinity<=1,
    min v<0<max v.

There exist public finite constants `C,T0` such that for every `T>=T0`
there is an admissible algorithm with the stated risk and cap. Its only
unknown-input information is exact `v(x)` at charged points. The algorithm
may depend on the horizon and public problem parameters. The analytic ball
`||v||infinity<=7/8` is a larger domain on which to prove derivative bounds;
it does not replace or shrink the promised class. The upper proof actually
works on the corresponding nonsigned smooth class too, which is permissible.

The quantifiers match D25's worst-case expected query lower bound. They do
not turn that lower bound into a common-baseline or fixed-profile claim.
Deterministic query cap implies the required expected-query upper bound.
All constants may depend badly on fixed `d,s`; dimension and smoothness are
not uniform complexity parameters here.

## 1. The scalar coordinate uses the actual PDE mean

Write `b=integral u`, `w=u-b`, `nu=2*pi^2-1`, and `a0=7/8`. Direct spatial
integration and expansion of the cube give exactly

    b'=b-b^3-R,    R=3b integral w^2+integral w^3.

The centered energy computation is

    (1/2)d||w||2^2/dt
      =-(1/2)||gradient w||2^2+||w||2^2
          -integral (u-b)(u^3-b^3)
      <=-nu||w||2^2.

The last integrand is nonnegative pointwise. Normalized volume and the
unit-torus Poincare constant `4*pi^2` therefore give
`||w(t)||2<=a0 exp(-nu*t)`. Since `|b|<=1` and `||w||infinity<=2`, this gives
`|R|<=5a0^2 exp(-2nu*t)` without assuming a closed mean equation.

Scalar comparison gives `|u|<=ell_a0(t)<1`. The exact scalar formula gives

    1-ell_a0(t)^2
      =(1-a0^2)/(1-a0^2+a0^2 exp(2t))
      >=(1-a0^2)exp(-2t).

For `G(z)=z/sqrt(1-z^2)`, `G'(z)=(1-z^2)^(-3/2)` and
`G'(z)(z-z^3)=G(z)`. Consequently the displayed derivative of
`A_t=exp(-t)G(b(t))` is exact. Its integrand is bounded by
`5a0^2(1-a0^2)^(-3/2) exp((2-2nu)t)`. The coordinate, uniform exponential
tail, and constant-data identity in T56 (3.5)--(3.6) follow. The assertion
`|A_t|<=G(a0)` also holds: scalar comparison and
`exp(-t)G(ell_a0(t))=G(a0)` prove it directly.

For the spatial remainder, put `q=u^2+ub+b^2`. Then `0<=q<=3` and

    w_t=Delta w/2+(1-q)w+integral q w.

The local propagator has kernel dominated by `exp(t-r)p_(t-r)`.
Over the last unit of time, its homogeneous term is bounded by
`e||p_1||2||w(T-1)||2`, and the scalar forcing term by
`3 integral_(T-1)^T exp(T-r)||w(r)||2 dr`. These prove T56 (3.7) with a
finite constant for every fixed dimension. No input derivative bound is
needed for this smoothing step.

Finally `b(T)=Psi(exp(T)A_T)` is an identity and `Psi` is globally
1-Lipschitz. This gives the stated uniform error

    ||S_Tv-Psi(exp(T)A(v))||infinity
      <=Cw exp(-nu*T)+C0 exp(-(2nu-3)T).

In particular, this estimate includes the separating set `A(v)=0` and
profiles arbitrarily close to it. There is no fixed-distance-from-interface
assumption or replacement of the nonlinear mean by the scalar flow from
the initial mean.

## 2. Actual derivative measures and the Gaussian domination

Finite-time differentiability on the open sup-norm ball follows from the
heat-semigroup mild equation and local Picard differentiation of the
polynomial nonlinearity. The bounded solution permits continuation over
each fixed finite interval. The first three differentiated equations in
T56 (4.2) have the correct coefficients, including the three separately
labelled terms `-6u U_2[h_i,h_j]U_1[h_k]` at order three.

The positive kernel of `Delta/2+(1-3u^2)` and Duhamel's formula construct
the measures directly. At order two the tree has one binary vertex with
factor `-6u`. At order three there is one ternary term with factor `-6`,
and three binary--binary trees with factors of magnitude at most `36`.
Leaves carry disjoint input labels before multiplication. Thus these are
measures on the full product of leaf positions, not a claimed consequence
of a generic multilinear operator representation theorem.

For a fixed unweighted tree of duration one and `j` leaves, the covariance
identity in T56 (4.3) is valid for arbitrary signed real coefficients `c_i`.
At any intermediate time the leaf groups partition the labels into at
most `j` groups, so

    sum_groups (sum_(i in group) c_i)^2 >= (sum_i c_i)^2/j.

Integrating over a full unit interval proves the positive semidefinite
inequality `Sigma >= (1/j)11^T`. In each spatial coordinate one may
therefore represent the leaves by a common independent Gaussian shift of
variance `1/j`, plus a residual centered Gaussian vector with covariance
`Sigma-(1/j)11^T`.

Here is the measure domination explicitly. Conditional on the residual
Gaussian vector `V`, the leaf vector with root `x` is
`V+1*(x+Z)`, modulo the torus. For any nonnegative Borel test function `F`,

    E F(V+1*(x+Z))
      <=||p_(1/j)||infinity * integral_Td E F(V+1*z) dz.

The rightmost integral is exactly the leaf law with a uniform root, since
adding any independent shift to a uniform common root preserves that law.
This proves the domination uniformly in `x`. It is still valid when the
residual covariance is singular. No density in all leaf coordinates is
needed at this stage.

The total edge length is at most `j`, so all Feynman--Kac weights cost at
most `exp(j)`. Applying the domination before taking any spatial supremum
gives the mixed-norm bounds. The time simplex of each binary--binary term
has volume `1/2`, so the third coefficient is indeed
`6+3*36/2=60`. The bounds

    M_1(1)<=e||p_1||infinity,
    M_2(1)<=6e^2||p_(1/2)||infinity,
    M_3(1)<=60e^3||p_(1/3)||infinity

are valid, with `M_j=integral_Y ||U_j(.,Y)||infinity`. Weighted trees are
dominated by these unweighted positive measures; the root-dependent
weights do not invalidate the common domination.

For positive branch times, the leaf edges give Lebesgue densities. The
time-boundary configurations with zero leaf edges have zero time measure.
Possible singularities of the integrated densities on leaf diagonals are
harmless: the common positive dominating measure has finite mass. Equally,
one may first formulate the argument using that dominating measure. It
does not swap `sup_x` with an arbitrary integral or require a bounded
pointwise density on the leaf product.

For `t>=1`, the homogeneous propagator costs `exp(t-r)` in spatial sup
norm, while disjoint leaf labels give the product bounds
`6M_1^2` and `6M_1^3+18M_2M_1`. Induction yields `M_j(t)<=C_j exp(jt)`.
These constants are constructive. For example, if `m_j` are the displayed
time-one upper bounds, one can take

    C_1=m_1,
    C_2=m_2+6C_1^2,
    C_3=m_3+3C_1^3+9C_2C_1.

These deliberately loose constants suffice. The heat-kernel bound in T56
follows from `n^2>=|n|` in its Fourier series and is a finite public bound.

## 3. Centering, spatial energy, and the two decay factors

For each leaf tuple let `B_j=integral_x U_j` and `W_j=U_j-B_j`. Direct
centering gives

    (W_j)_t=Delta W_j/2+(I-Pi)(a W_j)
                +B_j(a-Pi a)+(I-Pi)F_j,
    a=1-3u^2.

The homogeneous equation preserves mean zero. Its `L2` energy form is
bounded by `-nu||W_j||2^2` because `a<=1`. The orthogonal projection
`I-Pi` is contractive in `L2`. Also

    ||a-Pi a||2
      =3||u^2-Pi(u^2)||2
      <=3||u^2-b^2||2<=6||w||2.

The subtraction of `b B_1 B_1` at second order is legitimate because it is
spatially constant and hence disappears under `I-Pi`. The stated expansion
gives `N_0 M_1^2+2M_1N_1`. At third order the ternary forcing is bounded by
`3N_1M_1^2` after subtraction of `B_1B_1B_1`; each binary forcing is bounded
by

    N_0 M_2M_1+N_2M_1+M_2N_1.

Together with the factor `B_j(a-Pi a)`, these have rate
`exp((j-nu)t)` once the lower orders have been bounded. Convolving against
`exp(-nu(t-r))` costs the finite factor `1/j`, not a growing time factor.
The initial norm is `N_j(1)<=2M_j(1)`. This proves (4.8).

For precision, this can be performed for almost every leaf tuple using
the scalar spatial energy estimate and then Tonelli/Minkowski. At time
one the kernels already lie in the required integrated spatial sup space.
Their subsequent mild equations therefore provide appropriate versions
for the tuplewise estimates. There is no energy inequality being assumed
for a Banach space of signed measures.

Every product-rule term in a derivative of
`R=3b integral w^2+integral w^3` retains at least two centered factors.
A derivative replaces a `w` by a `W_i`; it does not remove the factor.
Put two such factors in spatial `L2`, use Cauchy--Schwarz, and put any third
factor in spatial sup norm. Integrating the disjoint groups of leaf labels
factors the resulting bounds. Hence the actual product measure satisfies

    ||D^jR(t)||TV<=C_j exp((j-2nu)t),  j=0,1,2,3.

At short times, the pointwise-in-root total variations of the tree measures
are bounded. Their tensor products and integration in the root position
give bounded total variation for these derivatives of `R` as well. No
short-time mixed spatial sup estimate is required.

For `G`, differentiation shows
`|G^(k+1)(b)|<=C_k(1-b^2)^(-(2k+3)/2)`. A term of order `q` in
`D^q(G'(b))` has `k<=q` mean-derivative factors of total order `q`, and is
therefore bounded in product-measure total variation by
`C exp((2k+3+q)t)<=C exp((3q+3)t)`. Multiplying by an order `j-q`
derivative of `R` and by `exp(-t)` yields exponent

    j+2q+2-2nu <= 3j+2-2nu.

The worst case is `j=3`, requiring only `2nu>11`. On this torus
`2nu=4*pi^2-2>34`, already using just `pi>3`. All four time integrals
converge uniformly, with the advertised derivative tail rates.

For positive times the kernels can be integrated as their jointly
measurable leaf densities; the preceding bounds give convergence in
`L1`, hence in total variation. The initial term is a product-Lebesgue
measure. Uniform operator-norm convergence follows from the stronger
measure bound. Apply the finite-time derivative convergence on an open
ball slightly larger than the displayed closed ball to obtain genuine
continuous Frechet derivatives through order three. This justifies both
the Taylor formula and the actual measures in (4.1), including at `A=0`.

## 4. Interpolation requires only total-order smoothness

The coarse-grid construction in Section 5 is valid with the stated
`C^s,max` norm. Tensor Lagrange polynomials of coordinate degree at most
`s-1` reproduce every polynomial of total degree at most `s-1`; one need
not assume all mixed derivatives through coordinate order `s`.

To check a derivative of order `r<=s`, freeze the Taylor polynomial of
`v` at the evaluation point, in a local torus lift. Each relevant stencil
node lies at distance `O(1/k)`, and its remainder is `O(k^-s)` by the
total-order Taylor theorem. Derivatives of the fixed scaled interpolation
weights cost at most `O(k^r)`. Polynomial reproduction then gives the
derivative error `O(k^(r-s))` for `r<s`, and a bound for the derivative of
`g` when `r=s`. Local lifts also handle stencils crossing the torus seam.
Taking `k` beyond a public fixed threshold makes the stencil nodes distinct.

This verifies both estimates in (5.1) from exactly `k^d` values. It also
gives a public residual Lipschitz bound for `s=1`; no extra smoothness is
quietly required at that endpoint. Higher derivatives of `g` may grow
with `k`, but are computably bounded because its formula is a finite
combination of fixed smooth weights and the bounded coarse coefficients.

For large enough `k`, `||g||infinity<=3/4`, and the segment from `g` to `v`
lies in the analytic ball. The third-order Taylor remainder is consequently
at most `K3 delta^3/6` with `delta=Cint k^-s`.

## 5. Finite coefficients do not conceal an extra oracle

For a fixed public fine positive partition of unity, define
`Pr=sum r(z_i)theta_i`. Positivity gives `||Pr||infinity<=delta`, and
the public residual Lipschitz bound controls `||Pr-r||infinity` by the
support diameter. The actual derivative-measure bounds imply

    sum_i |DA(g)[theta_i]|<=K1,
    sum_ij |D^2A(g)[theta_i,theta_j]|<=K2,

because the corresponding sums of positive partition products equal one.
The linear and quadratic errors are at most `K1||Pr-r||infinity` and
`2K2 delta||Pr-r||infinity`. These estimates are uniform over all residuals
consistent with the public bounds, so selecting the fine partition needs
no values on that fine residual grid.

The finite-difference errors are also correct. The first forward difference
has error at most `K2 h/2`. For the mixed second difference, Taylor's
cubic remainders have total norm at most

    (K3 h^3/6)*(2^3+1+1)=(5/3)K3 h^3.

After dividing by `h^2`, this is the claimed `(5/3)K3 h`. The calculation
also covers the repeated-index case `i=j`. The `J+J^2` coefficient errors
can be made small in sum by selecting a public sufficiently small `h`,
then choosing scalar-evaluation error `O(eta h^2/J^2)` and coefficient
rounding precision. With `h<=1/32`, all profiles used in these differences
lie in the proved ball. No derivative or phase oracle is invoked.

The use of a common scalar approximation for `A(g)` in several differences
does not cause a sampling problem: the coefficient errors here are bounded
deterministically. Allocating errors in their sum proves the five claims
in (6.2). Since `delta<=1/4`, an allocated coefficient `l1` error also
controls its action on any allowed residual or residual pair.

Each scalar `A(q)` in those finite differences has explicitly known datum
`q=g+h theta_i+h theta_j` or a simpler member of this list. Its tail is
controlled by the already proved uniform coordinate estimate. Its finite
time mean is computed by an ordinary deterministic mesh solver applied to
that **known** formula. Values of `q` at its fine PDE mesh are calculated
from saved coarse values of `v` and public functions. They do not call `v`.

The distinction matters even if the number of scalar solves and mesh
points is enormous. Reading or calculating a function of the finite
transcript creates no additional input information in the accepted oracle
model. Querying `v` at all those mesh points would be a different procedure;
that is not the construction in T56.

## 6. Finite PDE computation, public bounds, and halting

The Euler update in Section 6c is monotone on `[-1,1]` under its stated CFL
condition. Its diagonal derivative is

    1-h_t*d/h_x^2+h_t*(1-3U_j^2)
      >=1-h_t*(d/h_x^2+2)>=0,

and its off-diagonal derivatives are nonnegative. Its Jacobian row sum is
`1+h_t*(1-3U_j^2)<=1+h_t`. The endpoint constant arrays are fixed, so the
update preserves the interval and has the claimed sup-norm stability bound.
This proves the stated consistency-to-global-error estimate by the usual
finite telescoping recurrence; no stability of an uncertified solver is
being presumed.

The public derivative bounds used in consistency can be obtained without
solving a norm-selection problem. If `D_r(t)` bounds spatial derivatives
of order `r`, differentiate the polynomial PDE. The term containing the
order-`r` derivative is `(1-3u^2)partial^alpha u`; the remaining terms are
finite products of strictly lower positive derivative orders. The maximum
principle yields recursively, for `r=1,2,3,4`, a bound of the form

    D_r(t)<=e^t D_r(0)+integral_0^t e^(t-rho)
                         P_r(D_1(rho),...,D_(r-1)(rho)) d rho,

with a public polynomial having nonnegative coefficients. All initial
bounds come from the finite known interpolation/partition formula and the
public bounds on its coefficients. Time derivatives need no additional
unknown regularity: with `f(u)=u-u^3`,

    u_tt=(1/4)Delta^2 u+f'(u)Delta u
                       +(1/2)f''(u)|gradient u|^2+f'(u)f(u).

Thus spatial bounds through order four control `u_tt`. A grid quadrature
error for the mean is bounded using these same spatial bounds. All mesh
and time-step sizes can therefore be chosen from public bounds in advance.
Choosing an integer number of time steps removes any final-step issue.

Clipping the computed mean to the known scalar comparison interval is
nonexpansive relative to the actual mean. On that interval the derivative
of `exp(-tau)G` is at most
`(1-a0^2)^(-3/2)exp(2tau)`. Consequently sufficiently small finite mesh,
time-step, and evaluation errors achieve the required scalar precision.
Under the exact-real arithmetic model the polynomial mesh operations may
be exact. If implemented with rounding, rounding/projection within
`[-1,1]` after an update is a nonexpansive way to keep the same stability
argument; its allocated error is another additive local defect. This is
a permissible realization of the source's rounding allowance, not an
extra assumption about the unknown input.

There is no uniformly bounded arithmetic-work claim, and none is needed:
for each fixed public horizon the numbers of mesh points, time steps,
partitions, and coefficient operations are finite. The smooth cutoffs and
partitions can be fixed public computable functions with explicit finite
derivative bounds. The optional transcript clipping and smooth saturation
make the procedure total off promise while leaving every promised run
unchanged. The stated range `13/16`, plus `2h<=1/16`, is indeed contained
in the analytic ball `7/8`.

Finite arithmetic and fixed smooth-function evaluations, clipping, and
fixed-precision rational rounding give Borel transcript maps. The query
model already permits such scalar processing of exact returned values;
this proof is not making a finite-bit oracle claim about arbitrary real
input values. The random seed may be a sequence of independent fair bits.
After rational rounding, multiply each distribution's weights by a common
denominator to obtain nonnegative integer weights. A uniform integer in
the required range can be obtained by rejection from the smallest covering
power of two, with success probability at least `1/2` on every attempt.
Zero total weights are skipped. There are only finitely many such draws,
so the procedure halts almost surely for each input. The zero-measure
infinite-rejection paths do not exceed the data-query cap either.

## 7. Risk, exact query accounting, and the critical dimension

Conditional on the coarse transcript, all coefficient rules and discrete
sampling distributions are fixed. For each deterministic input this
conditioning creates no hidden dependence in the new independent samples.
The random variables in Section 7 have the stated finite-sum expectations
and bounds

    |Z1|<=(K1+1)delta,
    |Z2|<=(K2+1)delta^2.

Their sample-mean standard deviations follow immediately. The bias from
`c0`, the linear coefficient approximation, and half of the quadratic
coefficient approximation is at most `(1+1+1/2)eta`. Combining this with
the Taylor remainder proves (7.2). Unbiasedness for `A(v)` or for the PDE
target is neither asserted nor needed.

Exactly `k^d` initial coarse values suffice. The linear correction uses at
most `M=k^d` further calls and the quadratic correction at most `2M`.
Repeated points may be charged again, as the source does. All residual
queries are in those two counts. No coefficient computation or PDE solve
requests any additional unknown-data value. Hence every run has at most
`4k^d` charged calls.

Let `q=s+d/2`. The three errors scale as

    k^(-s-d/2),    k^(-2s-d/2),    k^(-3s).

The condition `d<=4s` is exactly `q<=3s`; equality is allowed. At
`d=4s` the cubic term has the same order as the leading random term and
is absorbed by the finite prefactor in the chosen mesh. It does not need
to be asymptotically smaller. No strict dimensional inequality is used.

For the cost claim, instantiate the source's permitted choice by

    k=max(k0,ceil((16B exp(T))^(1/q))),
    eta=exp(-T)/64.

Then the first three terms of (7.2) total at most `exp(-T)/16`, and the
coefficient term is `5 exp(-T)/128`. Thus the phase RMS is at most
`13 exp(-T)/128<exp(-T)/8`. After the deterministic profile approximation
is at most `1/16`, the target RMS is at most `21/128<3/16`. Optional final
rounding by `1/64` still gives at most `23/128<1/4`. This leaves positive
room and verifies the numerical constants without a simulation.

The exact chosen ceiling gives `k^d<=C exp(dT/q)` at sufficiently large
`T`. Thus the asserted query cap follows. Allowing an arbitrarily excessive
`k` is unnecessary; the displayed equality is an explicit valid instance
of (7.3). The bounded-horizon extension also follows from fixed interpolation
and known-surrogate finite-time stability, as stated in T56.

## 8. The true mass-only counterexample passes separately

T56's coefficient in (2.2) is correct. R03 supplies a particularly direct
way to verify it without any functional derivative-measure theorem.
For a fixed mean-zero `phi`, let `B=||phi||infinity`, `D=||phi||2`, and
`v_epsilon=epsilon phi` within the `a0` ball. Actual PDE comparison and
centered energy retain the factors of epsilon:

    |u_epsilon|, |b_epsilon|<=epsilon B exp(t),
    ||w_epsilon||infinity<=2epsilon B exp(t),
    ||w_epsilon||2<=epsilon D exp(-nu*t).

They imply

    |R_epsilon|<=5epsilon^3 B D^2 exp((1-2nu)t),
    |exp(-t)G'(b_epsilon)R_epsilon/epsilon^3|
      <=5BD^2(1-a0^2)^(-3/2)exp((3-2nu)t).

This majorant is independent of epsilon and integrable. The finite-time
Duhamel remainder is bounded by
`epsilon^3 B^3 exp(t)(exp(2t)-1)/2`, which follows by integrating the cubic
bound against the linear propagator. Hence `u_epsilon/epsilon` and
`w_epsilon/epsilon` converge on each bounded time interval to `exp(t)P_t phi`,
while `b_epsilon/epsilon` tends to zero. Dominated convergence yields

    lim_(epsilon->0+) A(epsilon phi)/epsilon^3
      =-integral_0^infinity exp(2t) integral(P_t phi)^3 dt.

For `phi=cos(2*pi*x_1)+c cos(4*pi*x_1)`, the heat rates are `2*pi^2` and
`8*pi^2`. The only nonzero cubic cross average is
`integral cos(2*pi*x_1)^2 cos(4*pi*x_1)=1/4`. Therefore

    integral(P_t phi)^3=(3c/4)exp(-12*pi^2*t),
    lim A(epsilon phi)/epsilon^3=-3c/[4(12*pi^2-2)].

There is no missing factor of `3!`: this is the cubic Taylor coefficient,
or equivalently `D^3A(0)[phi,phi,phi]/6` where that derivative is used.
The same elementary calculation gives the initial mean derivative
`-3c epsilon^3/4`.

For any fixed nonzero `c` and sufficiently small fixed positive epsilon,
the two opposite profiles have nonzero opposite coordinates, equal mass
zero, both strict signs, and all the required finite-order derivative
bounds. Their actual solution values converge uniformly to opposite
equilibria. A mass-only rule therefore has the same output law on both,
while the target separation tends to two. The pointwise two-target
squared-loss identity gives

    liminf_(T->infinity) max(RMS_plus(T),RMS_minus(T))>=1.

This proves a fixed-profile failure of mass-only information, not a lower
bound against algorithms retaining spatial point values. It supplies no
additional fixed-profile quantifier for D25. R03 is accepted by this audit
on its own stated conventional scope, independently of Sections 2--7 above.

## 9. Primary-source scope and downstream boundary

I opened the cited primary papers and checked the relevant control-variate
and smoothness discussion. Kunsch--Rudolf's Section 3.2 and Theorems 3.5--3.6
give direct precedent for sample-based approximation followed by Monte
Carlo of the residual and the classical smooth-integration exponent.
Their result does not provide this PDE coordinate or its derivative
measures. [Primary paper](https://arxiv.org/pdf/1809.09890).

Kostianko--Zelik's introduction explicitly distinguishes exponential
tracking from stronger smoothness properties of invariant-manifold
reductions. The audit imports no generic inertial-manifold conclusion to
fill T56's kernel argument. [Primary paper](https://arxiv.org/pdf/2102.03473).

These were bounded source checks, not an independent comprehensive
priority search. All high-risk bridges for the upper theorem were checked
above from the actual displayed PDE and construction.

The next scientific stage may treat the stated upper theorem as
conventionally passed. Any formal target or executable implementation must
preserve the exact query oracle, the actual signed-coordinate correction,
the product-measure estimates, and the distinction between finite auxiliary
computation and charged input calls. This audit itself supplies no Lean
coverage, sampled risk evidence, runtime evidence, all-dimension result,
or publication-priority claim.

Research-role metadata: T59 is a separate mathematical-review worker. It
made no model-setting change; the actual backend and reasoning setting are
not independently exposed in this context. Read-only source inspection,
hash verification, and primary-paper retrieval were performed. No numerical
experiment, theorem-prover invocation, solver implementation, or edit to a
frozen source was performed.
