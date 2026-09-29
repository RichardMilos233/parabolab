# T103: independent audit of the fractional long-horizon lower bound

Date: 2026-09-29. **Verdict: PASS. Required mathematical repairs: none.**

Frozen T102 proves its stated lower bound for fixed integers d,s,p>=1
and fixed reals 0<beta<=1 and c>0, on the original full signed smooth class,
at RMS tolerance 1/4. The proof covers the point loss and the strong
profile loss, and permits biased, adaptive, privately randomized
algorithms with inputwise almost-sure stopping and worst-input expected
query cost. It does not establish a fractional upper bound.

The conclusions below are conventional mathematical checks. No theorem
is accepted merely because an earlier file has a PASS label. No Lean,
implementation, numerical experiment, symbolic evaluation, sampler draw
or unknown-input acquisition was run in this audit.

## 1. Frozen target, direct locks and read scope

The target is the complete 962-line file
`reviews/T102-fractional-long-horizon-lower-feasibility.md`, SHA256

    04d04c669deb6e1e162b4d737766607b0dd35f39c786448a0556a93025541a7d

All paths below are relative to
`docs/research/runs/2026-09-28-dynamic-continuation`. Each direct source
lock matches the actual file:

| Direct source | Verified SHA256 |
| --- | --- |
| `04ac-fractional-fixed-time-fields.md` | `3330cccbe4fd4f666569b1f94401a7d8308d3a2ec5302f02616fd188c253ae3d` |
| `reviews/T95-fractional-diffusion-field-feasibility.md` | `9bc1d42d582f75b96a4e562dacbc925cbd01151b2a3b4702c5dc2b0a1ab99d74` |
| `reviews/T97-fractional-field-independent-audit.md` | `9e38a6d166806997d9c42ab8653615edad0a47b0fc1fa81dc9e31e980f5dec90` |
| `04ab-odd-power-long-horizon-complexity.md` | `a8bd72ec33c69aae4d50126c72f6fd75ac4e1625cb08cfcef6a1b310918d18c0` |
| `reviews/T94-odd-power-long-horizon-feasibility.md` | `2600c29a2823aefd9a69578de113bc511179d97bdfbea7eb3a6861ac28b7e1d9` |
| `reviews/T96-odd-power-long-horizon-independent-audit.md` | `b8f5f32be92c820bd8b955c5969406a49fa21e12a1b38c86d17bb7467ba1eda4` |

Repository HEAD at inspection was
`65dca46e42db1c80cdf9ddd8eed6a415148c37f3`. The inherited working tree
contains other ongoing work, so these content hashes, rather than HEAD
alone, identify the inspected documents.

T102 was read completely in ranges 1-260, 261-520, 521-780 and 781-962.
Both accepted checkpoints were read completely. T97's complete content
was read; a truncated combined output was repaired by explicit reads of
lines 1-305 and 300-345. This worker authored and read the locked T95 in
its earlier bounded assignment; its lines 315-485 were reopened here,
and the clock, Gaussian, moment and map arguments are checked below.

For the classical-diffusion comparison sources, this task read T94
lines 1-210, 760-1150 and 1192-1266, and T96 lines 1-105, 601-842 and
878-944. These contain their exact model, actual-flow interface, complete
lower composition, stopping argument and provenance. I do not claim a
fresh audit of their unrelated upper solver. T101 was neither opened
nor used.

The requested research configuration is gpt-6-astra/max. The actual
serving backend is not exposed. The math-auto-research skill and project
instructions were read in the preceding work and remain applicable.
Ownership here is only this T103 file; no earlier source was repaired
or changed.

## 2. Exact problem and quantifiers

**Source correspondence: T102 lines 19-104.**

Let X=(R/Z)^d with normalized Haar volume. Write D=2p+1, and use

    u_t=-c(-Delta)^beta u+u-u^D,
    (-Delta)^beta exp(2*pi*i*nu.x)
       =(4*pi^2*|nu|^2)^beta exp(2*pi*i*nu.x).

The promised input class is exactly

    V={v smooth, periodic and real:
       ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

There is no uniform control above derivative order s, and no mean
margin, basin information, analytic radius or stable-mode assumption.
The lower prior will be a finite subset of V, as is legitimate for a
worst-case lower bound; it does not replace the theorem's input class.

An acquisition supplies one exact scalar v(x). Preprocessing, repeated
points, repeat visits to a cell, and zero answers are counted. Adaptive
locations, stopping and output are measurable functions of the private
seed and observed information. The seed is input-independent and may
live on an arbitrary measurable probability space. No unbiasedness or
deterministic query cap is assumed.

Put

    q=s+d/2,       gamma=d/q=2d/(2s+d).

For point risk at a prescribed x*, the assumed bound is

    sup_(v in V) E|Z_T-S_Tv(x*)|^2<=1/16.

For a finite explicitly indexed real Fourier output, the stronger loss is

    sup_(v in V) E||U_T-S_Tv||inf^2<=1/16.

The spatial supremum is inside the expectation. The result is a lower
bound on sup_v E N_v at each prescribed real horizon T>=T0. It is not
a simultaneous-in-time guarantee, a fractional upper theorem or an
exact paid-work Theta assertion.

**Check: PASS.** The class, tolerance and algorithm quantifiers have
not been weakened relative to the requested lower problem.

## 3. Integer clock moments give the required bounded kernel

**Source correspondence: T102 lines 105-203; T95 Sections 3 and 6;
T97 Lemmas 2, 3 and 6.**

The locked subordination input uses one positive scalar clock L_t
shared across all d coordinates, with

    E exp(-z L_t)=exp(-ct z^beta).

Conditional Gaussian covariance is 2L_t I_d. Hence its characteristic
function at frequency 2*pi*nu is

    E exp(-4*pi^2*L_t*|nu|^2)
       =exp[-ct(4*pi^2*|nu|^2)^beta].

This verifies the coefficient c, factor two and isotropic generator.
At beta=1, L_t=ct deterministically, giving c Delta and the classical
convention kappa=2c. Independent coordinate clocks would give a
different multiplier and cannot be substituted.

The Gaussian mixture is a positive probability convolution kernel.
It preserves constants and Haar mass and contracts both L1 and Linf.
Its multipliers multiply in time, giving the convolution semigroup law,
and their real values give self-adjoint L2 contraction. Convergence
of multipliers to one first gives strong continuity on trigonometric
polynomials; their uniform density and contraction extend it to C(X).
This establishes the positive strongly continuous semigroup P_t used
in the actual mild equation.

For a>0, the Gamma integral and Tonelli give

    E L_t^(-a)
      =1/Gamma(a) integral_0^infinity z^(a-1)exp(-ct z^beta) dz
      =Gamma(a/beta)/[beta Gamma(a)] (ct)^(-a/beta).

The substitution is y=ct z^beta. Both endpoints are integrable.
For an integer h>=1, let b_h=ceil(h/beta). Since h/beta>=1,

    integral_0^1 x^(h/beta-1)e^(-x) dx<=1,
    integral_1^infinity x^(h/beta-1)e^(-x) dx
        <=Gamma(b_h)=(b_h-1)!.

Therefore the proposed Mbar_h(t) is valid:

    Mbar_h(t)
      =[1+(b_h-1)!]/[beta(h-1)!] (ct)^(-h/beta),  beta<1;
    Mbar_h(t)=(ct)^(-h),                        beta=1.

These are finite constants for every fixed allowed parameter. No
noninteger negative-moment convexity inequality is used.

For a Gaussian clock value l>0, decreasing-integral comparison gives

    sum_(k in Z) exp(-4*pi^2*l*k^2)
        <=1+2 integral_0^infinity exp(-4*pi^2*l*x^2) dx
        =1+(4*pi*l)^(-1/2).

Tensorization bounds ||h_(2l)||inf by its d-th power. For l<=1 it
is at most b_heat^d*l^(-d/2)<=b_heat^d*l^(-d); for l>=1 it is
at most b_heat^d, where b_heat=1+(4*pi)^(-1/2). Thus

    ||h_(2l)||inf<=b_heat^d(1+l^(-d)).

Taking the expected positive Fourier sum justifies absolute Fourier
summability and a continuous density for p_t. With

    rho=b_heat^d[1+Mbar_d(1/2)],

one obtains, for every t>=1/2,

    ||p_t||inf<=rho,       ||p_t||2<=rho,
    ||P_t h||inf<=rho||h||1,
    ||P_t h||inf<=rho||h||2.

The L2 density bound is loose but valid on volume one. Monotonicity
of Mbar_d(t) supplies the whole range t>=1/2. The clock moments concern
a fixed positive full time, with no integral over arbitrarily short
edge durations.

The polynomial reaction has 1-D<=f'<=1 on [-1,1].
Local polynomial mild iteration on C(X), positive comparison with
the equilibria +/-1, and bounded continuation give the actual global
flow from that interval. A more explicit domination argument is to
shift a secant or linearized potential by D-1. The shifted potential
is in [0,D]; positive Volterra iteration is bounded term by term by
the constant-potential series. Including the killed semigroup gives

    |E_u(t,r)h|<=e^(t-r)P_(t-r)|h|,
    |S_t v-S_t w|<=e^t P_t|v-w|.

This yields both L1 and Linf bounds with growth e^t. It uses the
one-sided upper derivative 1, not the false bound |f'|<=1.

The scalar solution is

    phi_t(a)=a e^t/[1+a^(2p)(e^(2pt)-1)]^(1/(2p)).

Comparison from any sup norm below one keeps the actual finite-time
state strictly below one. Oddness follows from the odd reaction,
the real linear semigroup and uniqueness.

**Check: PASS.** Invariance, positivity and both smoothing norms hold
for the actual fractional flow for every fixed beta>0,c>0.

## 4. The higher-Sobolev D47 specialization is an actual map estimate

**Source correspondence: T102 lines 204-335; T95 lines 315-485;
T97 Lemmas 4-8.**

The source does not merely relabel H^(d+1) as H^(d+2). Its field proof
works at any fixed integer r>=d+1, and the constants can be checked.

First take B=D and the Bernstein coefficients F_i of f(2t-1), with

    nu_br=1+(B/2)max_i|F_i|.

If a_l are the monomial coefficients of that shifted polynomial, then

    F_i=sum_(l<=i) a_l binom(i,l)/binom(B,l).

Indeed, the binomial identity for t^l in degree B follows from
binom(B,i)binom(i,l)/binom(B,l)=binom(B-l,i-l).
The endpoint coefficients vanish because f(-1)=f(1)=0.
Every interior corner 2i/B-1 has distance at least 2/B from the
endpoints, and |F_i|/nu_br<2/B. The corners
c_i=2i/B-1+F_i/nu_br consequently lie in [-1,1]. Their multiaffine
cube interpolant is bounded by one, and the Bernstein identity gives
M(z,...,z)=z+f(z)/nu_br, as required.

The first-split equation with this parent is the mild equation of
the actual flow. At a split, separately affine dependence and
independent child subtrees permit taking the expectation of each
child before evaluating the parent. Mild uniqueness then identifies
the branching expectation. This parent need not use T94's alternative
rate D-1; T102 consistently uses its own displayed nu_br.

For each integer k>=1, binomial expansion gives

    n[(n+B-1)^k-n^k]<=(B^k-1)n^k.

Apply the birth generator to stopped populations and use Gronwall.
The k=1 estimate bounds the probability of crossing arbitrarily
large population levels, proving nonexplosion first. Passing to the
limit then gives

    E n^k<=exp[nu_br(B^k-1)]

at time one. Higher moments are not assumed before nonexplosion.

Conditional on the complete chronology and clocks, set

    C=sum_e L_e b_e b_e^t,       H_i=sum_(e on path i)L_e.

The inverse-variance tree recursion yields a convex leaf vector w with

    sum_i w_i=1,       Cw=a*1,       a=w^t Cw.

For the unscaled conditional Gaussian path sums, its aggregate A
satisfies Var(A)=Cov(A,X_i)=a. Thus X-A*1 is independent of A under
the complete conditional Gaussian law. Scaling by sqrt(2) gives
the physical residuals and the common covariance 2a I_d. This
assertion is conditional on clocks; no unconditional finite covariance
or Gaussian independence is inferred for their heavy-tailed mixture.

Every matrix entry C_ij is nonnegative. Hence

    a>=sum_i H_i w_i^2
      >=1/(sum_i H_i^(-1))>0,

where the second inequality is weighted Cauchy--Schwarz and positivity
uses the positive full path clocks. Given the chronology, each path
has total chronological length one. Independent edge-clock Laplace
transforms therefore give the marginal law H_i=L_1 in distribution,
without asserting independence between different leaves.

For integer P>=1, convexity gives

    a^(-P)<=(sum_i H_i^(-1))^P
             <=n^(P-1)sum_i H_i^(-P),
    E[a^(-P)|chronology]<=n^P Mbar_P(1).

All powers used below satisfy P>=1. Stable clocks' possibly infinite
positive means are irrelevant to this conditional negative-moment
calculation.

For theta=8*pi^2, the Gaussian field has

    ||h_(2a)||_r^2
      =sum_nu(1+|nu|^2)^r exp(-theta*a*|nu|^2).

The scalar Gaussian sums at theta and theta/2 are bounded respectively
by b0*a^(-1/2) and b1*a^(-1/2) on 0<a<=1, where

    b0=1+sqrt(pi/theta),       b1=1+sqrt(2*pi/theta).

Also

    |k|^(2r)exp(-theta*a*k^2)
      <=(2r/(theta*a))^r exp(-theta*a*k^2/2).

This follows by maximizing x^r exp(-theta*a*x/2), and even discards
the improving factor e^(-r). Combining it with

    (1+sum_i nu_i^2)^r
       <=(d+1)^(r-1)(1+sum_i |nu_i|^(2r))

gives the exact constant

    H_r=(d+1)^(r-1)
           [b0^d+d*(2r/theta)^r*b1*b0^(d-1)]

and the bounds

    ||h_(2a)||_r^2<=H_r*a^(-r-d/2),      0<a<=1.
    ||h_(2a)||_r^2<=H_r*(1+a^(-P)),     P=r+d, a>0.

The second line uses P>=r+d/2 and monotonicity for a>=1. Multiplying
by n^(2j), conditioning and then using the population moment gives

    E[n^(2j)||h_(2a)||_r^2]
      <=H_r[1+Mbar_P(1)] exp[nu_br(B^(2j+P)-1)]
      =V_(j,r),                         j>=0.

The complete nonlinear field is

    F_omega(g)=h_(2a)(.-U)
                  P_tree(g(U+Z_1),...,g(U+Z_n)).

Integrating the common Gaussian through all its translated leaf
arguments gives E F_omega(g)=S_1g. This is not obtained by damping
the original leaf positions without changing their joint law.

Every distinct-leaf mixed partial of the bounded multiaffine tree
polynomial is bounded by one by its signed corner formula. Its
order-j map derivative consequently has envelope
n^j||h_(2a)||_r times the product of direction sup norms.
On each finite shape the field is Borel; (a,U)->h_(2a)(.-U) is
continuous in H^r locally on a>0. Countably many shapes and the
separability of H^r give strong measurability.

The moment estimate also controls the derivative variation and its
first-order remainder, with envelopes n^(j+1)||h||_r and
(1/2)n^(j+2)||h||_r. Integrate at fixed tuples of directions, then
take the operator supremum. This proves actual Frechet derivatives
and their operator-norm continuity, without an operator-space Bochner
measurability assumption. The resulting bound is

    ||D^j S_1(g)||_(C(X)^j -> H^r)<=sqrt(V_(j,r)).

It is uniform on ||g||inf<1. A paid evaluator for g is relevant to
executing a sampler, not to this mathematical map identity on C(X).
No such evaluator or sampler is executed in the lower proof.

**Check: PASS.** The use of r=d+2 and P=2d+2 is justified by the
same actual field with its explicitly increased moment order.

## 5. Gradient proportional to amplitude, and enough energy regularity

**Source correspondence: T102 lines 313-335 and 583-604.**

The shell |nu|inf=k contains at most
2d(2k+1)^(d-1)<=2d*3^(d-1)k^(d-1) lattice points.
Its contribution to sum_nu(1+|nu|^2)^(-d-1) is bounded by that
constant times k^(-d-3), whose positive series is at most two.
Fourier Cauchy--Schwarz therefore proves

    ||w||inf<=E_d||w||_(d+1),
    E_d=sqrt(1+4d*3^(d-1)).

Furthermore ||partial_i w||_(d+1)<=2*pi||w||_(d+2). The Euclidean
gradient norm introduces sqrt(d). Since S_1(0)=0, the Banach-space
fundamental theorem along t v, 0<=t<=1, gives

    S_1v=integral_0^1 D S_1(tv)[v] dt,
    ||grad S_1v||inf<=G||v||inf,
    G=2*pi*sqrt(d)*E_d*sqrt(V_(1,d+2)).

The entire segment stays inside the open unit ball. The estimate
requires no spatial derivative of v and no initial analytic radius.
In particular, the nonintegrability of t^(-1/(2beta)) near zero
when beta<=1/2 does not affect this argument.

The same field proof at time 1/2 and at any fixed larger r gives
a uniform H^r bound for S_(1/2)g on ||g||inf<1. Restarting from
S_(t-1/2)v proves these bounds for all t>=1/2. The strict invariant
bound places each finite-time restart in the open ball. The map
also is Lipschitz from C to each fixed H^r on admissible segments,
so time continuity in C supplies the corresponding positive-time
H^r continuity.

This gives a direct justification of the later energy identity.
Each actual mild Fourier coefficient satisfies its scalar ODE.
Write the energy identity for finitely many modes and integrate
over a finite interval starting at time one. Taking r>beta makes
the fractional energy tails uniformly vanish; choosing still larger
r controls all required differentiated expressions. The reaction
pairing also converges: H^r is an algebra for r>d/2, by weighted
Fourier convolution and summability of the inverse squared weight.
Alternatively, the uniform high-Sobolev tail of u and bounded L2
reaction already control the integrated energy pairing.

Passing to the limit gives the integrated identity and its
almost-everywhere derivative. No spatial analyticity or formal
termwise differentiation of an uncontrolled series is required.

**Check: PASS.** Both the net's gradient estimate and the actual
fractional energy calculation have sufficient conventional regularity.

## 6. Marked-L1 variations give exactly the stated B_D

**Source correspondence: T102 lines 336-396; T94 Section 6;
T96 Section 10.**

Derivatives of the finite-time actual mild flow in continuous
directions exist by local polynomial Picard differentiation and
restart. The Volterra inverse also has the usual convergent
simplex series with factorial denominators. The base trajectory
stays bounded in [-1,1].

Put C2=D(D-1), C3=D(D-1)(D-2). These bound |f''| and |f'''|
on the invariant interval. A first variation Y_h=E_u(t,0)h obeys
the L1 or Linf estimate e^t||h|| in its marked norm. For second
variations,

    Y_ij(t)=integral_0^t E_u(t,r)[f''(u)Y_i(r)Y_j(r)] dr.

Give one direction the L1 norm and all others the sup norm.
Holder's L1-times-Linf product estimate and positive propagation
give both the pure sup and mixed bound

    C2 integral_0^t exp(t-r)exp(2r) dr
      <=C2*t*exp(2t)

times the corresponding direction norms.

The third variation has exactly the sources

    f'''(u)Y_1Y_2Y_3
      +f''(u)(Y_12Y_3+Y_13Y_2+Y_23Y_1).

There is one direct third-order term and three second-first terms,
not an additional factorial. The marked direction occurs in exactly
one factor of every product. Their norm coefficients before
propagation are bounded by C3*exp(3r) and
3*C2^2*r*exp(3r). Hence

    ||D^3S_t(v)[h_1,h_2,h_3]||1
       <=[C3*t+(3/2)C2^2*t^2]exp(3t)
          ||h_1||inf||h_2||inf||h_3||1.

This is a bound on C(X) variations using an L1 norm for one direction;
it does not presume an unproved nonlinear flow on an open L1 ball.

Let A_1(v)=exp(-1)Pi S_1v and F(v)=A_1(v)-Pi v.
At zero D S_1(0)=e P_1. Mass preservation gives DF(0)=0.
Oddness gives D^2F(0)=0. Multiplying the preceding time-one estimate
by exp(-1) gives

    |D^3 A_1(v)[h_1,h_2,h_3]|
      <=B_D ||h_1||inf||h_2||inf||h_3||1,
    B_D=e^2[C3+(3/2)C2^2].

Taylor's integral formula for t->DF(tv)[h] then yields

    DF(v)[h]=integral_0^1(1-t)D^3A_1(tv)[v,v,h] dt,
    |DF(v)[h]|<=(B_D/2)||v||inf^2||h||1.

At D=3 the constant is 60e^2, but the proof retains its displayed
D dependence. Positivity and mass contraction, rather than
short-time kernel derivatives, are the only diffusion properties
used in this calculation.

**Check: PASS.** The actual mean correction has the required cubic
small-amplitude mixed bound for every fixed odd degree.

## 7. Every member of the complete two-slice prior is admissible

**Source correspondence: T102 lines 397-456.**

Fix the public compactly supported smooth nonnegative bump psi,
with I=integral psi>0, psi<=1, D_psi>=1 the stated derivative bound,
and a_bump=1/(8D_psi). Thus a_bump<=1/8 and I<=1.

For the source's even grid k and K=k^d, the rescaled disjoint bumps
are smooth across cell and torus boundaries. At every |alpha|<=s,

    ||partial^alpha v_xi||inf
      <=a_bump*k^(|alpha|-s)*D_psi<=1/8.

The sup norm also is at most 1/8. On either slice
sum_i xi_i=+/-ell, ell<=K/4 ensures that both signs occur.
Since psi is nonzero and nonnegative, every such profile has a
strictly positive and strictly negative value. Thus every complete
slice member, including the later PDE-bad members, belongs to V.

The exact scale definitions are

    R_T=(a_bump I exp(T))^(1/q),
    k=2 floor(R_T/2),     K=k^d,
    A=a_bump*k^(-s),      ell=2 ceil(sqrt(K)/2),
    m=A I ell/K.

For R_T>=4, R_T/2<=k<=R_T. For K>=2048,

    sqrt(K)<=ell<=2sqrt(K)<=K/4.

Even k gives even K; ell also is even. Thus both required slice
cardinalities (K+/-ell)/2 are integers strictly between zero and K.

The identity

    exp(T)m=(R_T/k)^q * ell/sqrt(K)

proves 1<=exp(T)m<=2^(q+1). Also

    A/sqrt(K)=a_bump*k^(-q)
          <=2^q I^(-1)exp(-T),
    log K<=d log R_T<=gamma T,

since a_bump I<=1. These estimates hold between the jumps of k,
not merely on a selected subsequence of horizons.

The prior is the equal mixture of the two complete uniform slices.
It depends on T and public constants, not on the algorithm or seed.
The PDE observables can be defined on the whole sign cube to prove
Lipschitz and oddness properties. This does not require the algorithm
to work on the all-positive or all-negative vectors outside V.

**Check: PASS.** No mean-margin promise, good-event restriction or
algorithm-dependent hard family has been introduced.

## 8. Complete-slice concentration does not need independent signs

**Source correspondence: T102 lines 457-497.**

Let H be odd under global sign reversal, and let each one-sign flip
change it by at most L. The applications have L>0; if L=0 the
concentration conclusion is trivial.

A uniform balanced sign vector has E H=0. Flip a uniformly chosen
ell/2 subset of its negative entries. For any target positive set
of size (K+ell)/2, the number of possible balanced precursor positive
sets is the same. Hence the output is exactly uniform on Omega_+.
Its H value differs from the balanced one by at most ell L/2.
The same argument or sign reversal treats Omega_-.

For concentration within either fixed slice, expose coordinates in
a fixed order. At a prefix where both next signs are possible,
suppose the negative-next completion has r positive signs among
the remaining positions. Sample their uniform r-subset, choose
uniformly one of its members, and move that positive sign to the
next coordinate. The remaining (r-1)-subset is uniform for the
positive-next completion. The two full vectors differ in two signs.

Thus the two possible conditional expectations differ by at most
2L. A centered Doob increment has range length at most 2L, variance
at most L^2 and exponential moment at most exp(theta^2 L^2/2).
Forced signs contribute zero. The bounded-variable exponential
estimate follows by reduction to interval endpoints and the bound
b^2/4 on the second derivative of the two-point log moment
generating function for an interval of length b.

Martingale orthogonality gives variance at most K L^2. Iterating
the exponential estimate and optimizing the Chernoff parameter
gives the two-sided tail

    P(|H-EH|>z)<=2 exp[-z^2/(2K L^2)].

The mean bound is |EH|<=ell L/2. H need not be invariant under
coordinate permutations; only the input law and the coupling are.
No replacement of a fixed slice by product Bernoulli signs occurs.

**Check: PASS.** Both the mean bias and concentration estimates
hold under each original complete slice.

## 9. The actual time-one mean and spatial net estimates close

**Source correspondence: T102 lines 498-582.**

A one-cell sign flip changes the input in L1 by 2A I/K.
The entire interpolation segment has sup norm at most A. Applying
the derivative bound from section 6 gives

    |F(v_xi)-F(v_xi')|<=B_D A^3 I/K<=L_F,
    L_F=B_D A^3/K.

F is odd on the complete cube. The slice lemma gives

    |EF|<=B_D A^3 ell/(2K),
    Var(F)<=B_D^2 A^6/K.

Since m=A I ell/K, the condition A^2<=I/(64 B_D) implies
|EF|<=m/128. On |F|>m/4 the centered deviation exceeds m/8.
Therefore

    P(|F|>m/4)
      <=64 B_D^2 A^4 K/(I^2 ell^2)
      <=64 B_D^2 A^4/I^2<=1/64.

On the positive slice's complementary event,

    b_1=Pi S_1v=e(m+F(v))>=3e m/4.

The negative slice has the sign-reversed conclusion.

For a fixed spatial point x, domination and the kernel bound give
the one-cell difference at most 2e rho A I/K<=C_cell A/K, where
C_cell=2e rho. This point observable is odd. Its slice expectation
has magnitude at most C_cell A/sqrt(K).

The source's deterministic grid has

    N_K=ceil(sqrt(d)G sqrt(K)),      M_K=N_K^d,
    C_net=(1+sqrt(d)G)^d,
    M_K<=C_net K^(d/2).

Every point has torus distance at most sqrt(d)/(2N_K) from a grid
point. The actual gradient bound G A consequently makes the
interpolation error at most A/(2sqrt(K)). This is why a uniform
small-amplitude gradient estimate was needed.

At a grid point choose

    z_K=C_cell A K^(-1/2)*sqrt(2 log(128 M_K)).

Its tail probability is at most 1/(64 M_K). The finite union bound,
the expectation bound and the interpolation estimate give

    ||S_1v||inf
      <=A/sqrt(K)
           [C_cell+1/2+C_cell sqrt(2 log(128 M_K))]

with probability at least 63/64 under each complete slice.
There is no interchange of a spatial supremum and expectation.

Since K>=2, define

    b_net=log(128 C_net)/log 2+d/2,
    H_net=(C_cell+1/2)/sqrt(log 2)+C_cell sqrt(2b_net).

Then log(128 M_K)<=b_net log K. The bounds from section 7 give

    ||S_1v||inf<=C0 exp(-T)sqrt(T),
    C0=(2^q H_net/I)sqrt(gamma).

Mean subtraction is an orthogonal L2 projection on normalized
volume, so its centered norm obeys the same envelope:

    W_1=||(Id-Pi)S_1v||2<=C0 exp(-T)sqrt(T).

No factor two is needed at this step. The mean-bad and profile-bad
probabilities sum to at most 1/32 on each slice. Their favorable
intersection is Good, of probability at least 31/32. No independence
between those two events is assumed and no prior is conditioned
on their intersection.

**Check: PASS.** The required actual mean and whole-profile events
have the advertised constants under the unchanged prior.

## 10. Fractional dissipation controls all positive spectral gaps

**Source correspondence: T102 lines 583-663.**

For a good input write u(t)=S_(1+t)v, b(t)=Pi u(t), w=u-b,
and lambda=c(4*pi^2)^beta. The actual mean satisfies

    b'=b-Pi(u^D).

Since D is odd, (u-b)(u^D-b^D)>=0 pointwise. The zero-mean Fourier
support of w gives

    c||(-Delta)^(beta/2)w||2^2>=lambda||w||2^2.

Using the justified integrated energy identity,

    (1/2)d/dt||w||2^2
       =-c||(-Delta)^(beta/2)w||2^2
                    +||w||2^2-integral w(u^D-b^D)
       <=(1-lambda)||w||2^2.

Consequently ||w(t)||2<=exp((1-lambda)t)W_1.
This allows growth when lambda<1. The argument does not assume
a unique unstable constant mode or a stable nonconstant spectrum.

For R(t)=Pi(u^D)-b^D, scalar Taylor expansion about b yields

    |R(t)|<=C_R||w(t)||2^2,       C_R=D(D-1)/2.

The linear term integrates to zero. Both b and u(x), and their
intervening segment, lie in [-1,1], so this bound includes every
higher power without requiring small pointwise w.

Let z(t)=phi_t(b_1). The difference b-z solves a scalar forced
equation with secant coefficient at most one and forcing -R.
It follows that

    |b(t)-z(t)|<=C_R exp(t)W_1^2 J_lambda(t),
    J_lambda(t)=integral_0^t exp((1-2lambda)r) dr.

This integral equals t at lambda=1/2. At t=T-1,

    exp(t)W_1^2<=C0^2 T exp(-T-1),
    J_lambda(T-1)<=T exp((1-2lambda)_+ T).

Hence, for mu=min(1,2lambda)>0,

    |b(T-1)-phi_(T-1)(b_1)|
      <=C_R C0^2 T^2 exp(-mu T).

The estimate decays for every positive lambda even in the regime
where the centered linear estimate itself permits growth.

**Check: PASS.** This is actual nonlinear fractional PDE separation
control, rather than a linearized or mean-only assumption.

## 11. Final-unit smoothing and every displayed T0 constant

**Source correspondence: T102 lines 664-744.**

For t>=1 compare u(t)=S_1u(t-1) to the constant
phi_1(b(t-1)). Positive domination and P_1:L2->Linf give

    ||u(t)-phi_1(b(t-1))||inf<=e rho||w(t-1)||2.

The actual mean differs from that same constant by at most this
supremum. Thus

    ||w(t)||inf<=2e rho||w(t-1)||2.

Substitution at t=T-1 gives exactly

    ||w(T-1)||inf<=C_w sqrt(T)exp(-lambda T),
    C_w=2e rho C0 exp(2(lambda-1)).

The shift by two in the centered L2 evolution is correct:
w(t-1) here is w(T-2), whose initial norm is W_1.
T>=2 supplies the final full smoothing unit.

The following constants from T102 suffice without alteration:

    k_star=ceil(max(4,2048^(1/d),
                       (64 B_D a_bump^2/I)^(1/(2s)))),
    T_grid=q log(2k_star)-log(a_bump I),
    T_mean=(2/mu)max(0,log(512 C_R C0^2/mu^2)),
    T_space=(2/lambda)max(0,log(64 C_w/sqrt(lambda))),
    T0=max(2,T_grid,T_mean,T_space).

At T>=T_grid, R_T>=2k_star and k>=R_T/2>=k_star.
This enforces R_T>=4, K>=2048 and A^2<=I/(64B_D),
including at every grid jump and between jumps.

For T>=0, the elementary exponential bounds are

    T^2 exp(-mu T)<=8mu^(-2)exp(-mu T/2),
    sqrt(T)exp(-lambda T)<=lambda^(-1/2)exp(-lambda T/2).

The first follows from exp(mu T/2)>=(mu T/2)^2/2.
The second follows by taking square roots of exp(lambda T)>=lambda T.
Thus the prefactors that need suppressing to 1/64 are precisely
512 C_R C0^2/mu^2 and 64 C_w/sqrt(lambda).
If either is at most one, its max-with-zero threshold correctly
requires no additional time. All logarithm arguments are positive
and all constants are finite at fixed parameters.

Consequently both the scalar-mean error and the final spatial
error are at most 1/64 at every real T>=T0.

On a good positive-slice input, exp(T-1)b_1>=3/4.
Writing y=exp(t)a in the exact scalar solution gives

    phi_t(a)>=Psi_p(y),
    Psi_p(y)=y/(1+y^(2p))^(1/(2p)),        a>=0.

Psi_p is increasing: its derivative is
(1+y^(2p))^(-1-1/(2p)). The binomial inequality
(1+y^2)^p>=1+y^(2p) implies Psi_p(y)>=Psi_1(y).
Therefore phi_(T-1)(b_1)>=Psi_1(3/4)=3/5, and

    S_Tv(x)>=3/5-1/64-1/64=91/160>1/2

at every x on a good positive input. Oddness gives the negative
bound on a good negative input. Good remains only an analytical
event of mass at least 31/32 within each complete slice.

**Check: PASS.** No exponent, time shift, resonance, integer-grid
or threshold repair is needed.

## 12. Stronger sign oracle and adaptive word law

**Source correspondence: T102 lines 745-815.**

Threshold a point estimator at zero. On every fixed good input,
a wrong sign implies point error at least 1/2. Its mean-square
risk bound therefore gives private-seed sign error at most 1/4.
Bad inputs have prior mass at most 1/32. The original full-prior
Bayes error is consequently at most the valid loose bound 9/32.
No unbiasedness or bounded-output assumption is involved.

A query x lies in a unique half-open grid cell i. Revealing xi_i
is a stronger oracle, because the original value is the known
quantity A xi_i psi(kx-i). This remains true on support gaps and
cell boundaries, where the scalar answer is zero. Repeated queries
are reconstructed from previous signs while retaining their full
original acquisition cost.

After j distinct labels have been revealed, with z positive signs,
unseen labels have the uniform remaining-count law under the
respective full slices:

    p_+(j,z)=((K+ell)/2-z)/(K-j),
    p_-(j,z)=((K-ell)/2-z)/(K-j).

For a fixed seed, the chosen new label is a function of its past
transcript. Conditioning on that transcript therefore imposes only
the already revealed assignments; its indices and locations do not
reveal an additional unknown coordinate. This proves the transition
formula for adaptive labels as well as fixed labels.

Set n_cap=floor(K/1024). A process capped at n_cap original
acquisitions has at most n_cap distinct reveals. After it stops,
pad with unused labels, for example in increasing order, until
there are exactly n_cap distinct revealed signs. The decision
ignores padding. This grants additional information and does not
undercharge the original algorithm.

Every prefix of length at most n_cap is feasible under both slices,
because each sign count is at least (K-ell)/2>=3K/8>n_cap.
Consequently all word probabilities used below are positive. For
each fixed seed the padded word has the same finite urn law W_+
or W_-, independently of which adaptive labels were selected.

**Check: PASS.** Repeated/zero answers, real query locations,
stopping-dependent indices and padding preserve the stated word law.
The argument would generally fail after conditioning the prior on
Good, which the source never does.

## 13. KL, arbitrary measurable seed spaces and finite-prior null sets

**Source correspondence: T102 lines 796-865.**

For j<n_cap, use j<=K/8, 0<=z<=j and ell<=K/4. The numerator of
p_- is at least K/4 and its denominator is at most K, giving p_->=1/4.
Its numerator is at most K/2 and denominator at least 7K/8, giving
p_-<=4/7. Also

    p_+-p_-=ell/(K-j)<=2ell/K,
    p_-(1-p_-)>=3/16.

For a,b in (0,1), applying log x<=x-1 to the two Bernoulli terms gives

    KL(Ber(a)||Ber(b))<=(a-b)^2/[b(1-b)].

Each transition thus has KL at most

    64 ell^2/(3K^2)<=256/(3K),

using ell^2<=4K. Expanding the finite positive word probabilities
into their conditional factors proves the chain rule directly.
Hence

    KL(W_+||W_-)<=n_cap*256/(3K)<=1/12.

For completeness, let A be the finite set of words on which W_+
exceeds W_-. Grouping its atoms and complement by the log-sum
inequality bounds the word KL below by the corresponding binary KL.
For fixed second parameter b, binary KL has value and first derivative
zero at a=b and second derivative 1/[a(1-a)]>=4. Thus

    KL(W_+||W_-)>=2 TV(W_+,W_-)^2,
    TV(W_+,W_-)<=sqrt(1/24)<1/4.

With equal priors every word-based test has error at least 3/8.

Now let the private seed law be R on its arbitrary measurable space.
At this fixed horizon the prior contains finitely many actual promised
inputs. For each, almost-sure halting supplies a measurable seed null
set. Removing their finite union leaves one full-measure seed set
on which the original algorithm halts for every prior input.

For such a fixed seed, every capped sign prefix extends to a promised
input. The simulation therefore cannot encounter an undefined
nonhalting branch before its next query/decision on a feasible prefix.
Query locations, repeated answers, stopping, the capped decision and
padding are determined by the seed and revealed word. Indices do not
have to be supplied as extra independent data; they are reconstructed
from that same pair.

The finite-prior calculation with the seed held fixed gives the
same W_+ or W_- for every seed in this full-measure set. Direct finite
summation over the prior inputs then identifies the joint laws as

    R times W_+,       R times W_-.

No regular conditional distribution on the arbitrary seed space is
needed. On the discarded null set one may define any fixed procedure.

For any measurable seed-word event, sum over its finitely many word
sections. Its probability difference is at most TV(W_+,W_-).
A word-only event attains equality, so the two product laws have
exactly that total variation. The capped output is a measurable
function of the pair, and therefore

    BayesError_capped>=3/8.

This does not restrict the seed to finitely many coins, assume
input-uniform almost-sure stopping over the whole infinite class,
or disintegrate a possibly pathological seed space. Finiteness of
the chosen prior is the sufficient uniformization step.

**Check: PASS.** The strong seed and adaptive-transcript quantifiers
survive the information comparison.

## 14. Truncation proves the expected-query lower and exact constant

**Source correspondence: T102 lines 866-912.**

Let q_bar be the original expected acquisition count averaged over
the unchanged finite prior. If it is infinite, at least one prior
input has infinite expected count and the lower conclusion is immediate.

Otherwise stop the original algorithm just before acquisition
n_cap+1 would occur, and use an arbitrary fixed label on that event.
If it halts without that attempted acquisition, retain its original
decision. Padding then supplies the capped sign word of section 12.

The original and capped decisions differ only on {N>n_cap}.
Under the full prior and seed law, Markov gives

    P(N>n_cap)<=q_bar/n_cap.

Combining both Bayes error bounds yields

    3/8<=9/32+q_bar/n_cap,
    q_bar>=3 n_cap/32.

Since K>=2048, floor(K/1024)>=K/2048. Therefore

    q_bar>=3K/65536.

The integer k lower bound gives

    K>=2^(-d)(a_bump I)^gamma exp(gamma T).

Thus the source's explicit constant is correct:

    C_lower=3*2^(-d-16)(a_bump I)^gamma>0,
    sup_(v in V) E N_v>=C_lower exp(gamma T),   T>=T0.

The supremum dominates the finite-prior average. Rare expensive
runs, repeated acquisitions and variable stopping are already
included in q_bar; a deterministic acquisition cap was never imposed
on the original estimator.

A finite real Fourier output satisfying the strong profile loss can
be evaluated at the prescribed x* without any new initial-value
acquisition. Its scalar risk is at most its profile risk. This
transfers the point lower bound to the stated strong-profile problem.
Charging at least one unit of work per query also transfers this
lower bound to paid work, without giving an upper or a bit-cost theorem.

**Check: PASS.** Both the exponential power and
3*2^(-d-16)(a_bump I)^gamma are correct in the stated range.

## 15. Failed attacks, source issues and boundaries of this PASS

The following possible failures were examined explicitly:

| Attempted objection or shortcut | Audit result |
| --- | --- |
| The short-time fractional gradient kernel is not integrable for beta<=1/2. | Correct obstruction to the naive Duhamel proof, but T102 uses the actual higher-Sobolev field and the Banach-space fundamental theorem instead. |
| Does the displayed H^(d+1) checkpoint alone justify substituting r=d+2? | Its label alone does not. T102 rederives the field estimate at r=d+2 and P=2d+2. This extra order conveniently reuses E_d; H^(d+1) can itself control a gradient via another Sobolev constant, so an objection that it can never do so would be too strong. |
| Infinite positive stable-clock means make the covariance calculation invalid. | The Gaussian covariance calculation is conditional on all finite clocks; only full-time negative moments are averaged. |
| Did the sharper inverse-clock moment inequality assume independent leaves or extend convexity below exponent one? | Neither occurs. All exponents are integers at least one and common marginal laws suffice. |
| A paid known evaluator might be required for every abstract state used by the lower proof. | The C-to-H map estimate is mathematical and holds for all continuous bases; no sampler execution or computational state evaluator is used. |
| Pointwise concentration might have been mistaken for a whole-profile event. | The fixed deterministic spatial net, explicit gradient bound and union bound close the supremum estimate. |
| The prior might exclude exceptional PDE inputs or condition on Good. | It contains both entire slices. Bad mass is added to the testing error; no information calculation uses a conditioned prior. |
| Small positive diffusion permits growing nonconstant modes. | The energy bound allows that growth; the time-one exp(-T)sqrt(T) scale makes both final errors decay for every fixed lambda>0. |
| The mean might be evolved by a scalar ODE without accounting for nonlinear spatial terms. | The exact remainder R=Pi(u^D)-b^D is bounded and propagated explicitly. |
| The resonance lambda=1/2 might invalidate a denominator. | J_lambda is kept as an integral and equals t at resonance. |
| Grid rounding or a negative threshold logarithm might leave horizons uncovered. | The even-grid inequalities hold for every real T>=T0, and each max-with-zero logarithm has the correct prefactor interpretation. |
| Adaptive real query locations might encode additional unseen signs. | Given the fixed seed and past revealed signs, locations and indices are deterministic transcript functions; the remaining labels retain their urn law. |
| Inputwise null stopping sets might require a uniform null set over all V. | Only the finite prior is needed, so its finite union is null. |
| An arbitrary measurable seed space might require regular conditional probabilities. | The seed-word product law is proved by direct finite summation, avoiding disintegration. |
| Repeat and zero-valued queries might disappear from the lower cost. | Truncation counts all original acquisitions before any distinct-label padding. |
| Rare very long runs might defeat a bounded-word lower. | Markov truncation compares their full expected count to the capped testing error. |

No material source defect or counterexample to the stated theorem was
found. The Gamma factor, heat variance convention, mixed-L1 constant,
net constant, T0 factors, target 91/160 and final lower constant all
pass. The public constants may be extremely large; they are not
claimed moderate or uniform.

Several excluded extensions are genuinely false or unproved:

- At c=0 a single exact query v(x*) and the scalar flow formula return
  the exact point target at every horizon. An exponential point lower
  cannot extend to zero diffusion, and no uniform threshold down to
  that boundary is asserted.
- This proof uses f'(0)=1 and monotonicity of the normalized odd power.
  It is not a theorem for arbitrary inward reactions or unscaled
  physical coefficients with the same input class and tolerance.
- Integer p,d,s>=1 and 0<beta<=1 are retained. No other parameter
  range, degree-uniform result or uniform beta-down-to-zero theorem
  follows.
- Higher finite Sobolev regularity does not establish a spatial
  analytic radius. No nonlinear fractional known-profile solver,
  upper algorithm or finite-bit numerical accuracy follows here.
- The hard prior depends on the chosen horizon. The theorem concerns
  a selected horizon, not simultaneous accuracy at all times.

This audit adds no literature or priority claim. The normalized
stable-law input is the already locked T95/T97 input; no new
factorization theorem or external source was needed. The semigroup,
field, variation, slice, energy and information arguments required
for this composition have been checked above.

Only source reads, bounded working-tree inspection, SHA256 checks,
and writing/rereading this owner file were performed. The six direct
locks and T102 were rechecked at handoff. No root ledger, protocol,
old evidence, Lean file, code or numerical artifact was edited.
Unknown-input acquisitions: **zero**.

The final verdict is **PASS for T102's complete fractional odd-power
long-horizon lower theorem in its exact stated model**. Root
correspondence and promotion remain separate. No fractional upper
result or full formalization is accepted by this verdict.
