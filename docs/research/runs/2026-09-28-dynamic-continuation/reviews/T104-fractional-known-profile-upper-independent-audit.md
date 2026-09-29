# T104: independent fractional paid-solver and long-horizon upper audit

Date: 2026-09-29. Independent conventional mathematical audit.
Requested research routing: gpt-6-astra/max. Actual serving model and
reasoning-effort telemetry are not exposed to this worker.

**Verdict: PASS. No mathematical repair to the frozen upper theorem is
required.** The actual fractional known-profile solver, the same-class
strong-risk composition, the hard query cap, and the stated paid-work
exponents follow in the declared exact-real model.

This verdict concerns an upper bound only. It does not use T102 or any
other lower-bound candidate, and does not establish a matching theorem,
finite-bit stability, practical performance, or novelty.

## 1. Frozen target, locks, and inspection scope

The complete target read for this audit is

    reviews/T101-fractional-known-profile-upper-feasibility.md
    1163 lines
    SHA256 e16885dc66d636cc628c46f26718a80a618ed3658d399e007bdeef8cba8e6fd2.

All seven source locks in its table were independently checked:

| Direct source, relative to the current run | SHA256 |
| --- | --- |
| 04ab-odd-power-long-horizon-complexity.md | a8bd72ec33c69aae4d50126c72f6fd75ac4e1625cb08cfcef6a1b310918d18c0 |
| 04ac-fractional-fixed-time-fields.md | 3330cccbe4fd4f666569b1f94401a7d8308d3a2ec5302f02616fd188c253ae3d |
| reviews/T94-odd-power-long-horizon-feasibility.md | 2600c29a2823aefd9a69578de113bc511179d97bdfbea7eb3a6861ac28b7e1d9 |
| reviews/T95-fractional-diffusion-field-feasibility.md | 9bc1d42d582f75b96a4e562dacbc925cbd01151b2a3b4702c5dc2b0a1ab99d74 |
| reviews/T97-fractional-field-independent-audit.md | 9e38a6d166806997d9c42ab8653615edad0a47b0fc1fa81dc9e31e980f5dec90 |
| reviews/T81-fixed-burnin-all-diffusion-upper-proof.md | d9b249ed669897df319ca712fc4ad26625fc97e1a9b32b79eacaf497b290bae5 |
| reviews/T84-all-diffusion-upper-independent-audit.md | 39cd98fcf957badbe382123bd1960eac7fb99441114c9433bd9ee0ff2d256d7d |

The original T94, T95, and T97 were read completely in this worker's
earlier bounded assignments; their identical locks were reverified.
For T104, the relevant original T94 solver passages, T95 clock/moment/
field passages, T81 Section 3 and Sections 7a-7b, and T84 Sections 2,
4-6, and 9 were freshly inspected. Both acceptance notes were also
read. Their acceptance labels do not replace the derivations below.

The complete contextual note R24 was read:

    reviews/R24-fractional-solver-kernel-prior-work.md
    SHA256 d84034638778dc93d3a2819632bda21342ecd8ecd6d22d9c4c1b18cf1989ac47.

R24 is a scoped literature/proof-routing note, not an additional
solver premise. This audit does not claim to have independently
reopened or verified the complete external papers described there.
The complex-time argument is checked directly below, including the
case alpha=1.

Only this T104 review is edited. T101, T102, the frozen sources,
root state and ledgers, Lean files, numerical code, and configuration
are not edited.

## 2. Exact theorem being passed

Fix integers d,s,p>=1, constants c>0 and 0<beta<=1, and set

    D=2p+1,       alpha=2beta,       theta=min(1,alpha),
    eta=ceil((2d+8)/theta),
    a_solver=eta*d+5d+20,
    A_work=a_solver+ceil(d(d+2)/theta)+2,
    A_array=eta*d+ceil(d(d+1)/theta).

The generator is isotropic:

    A exp(2*pi*i*nu.x)=-c(4*pi^2|nu|^2)^beta exp(2*pi*i*nu.x).

The unknown initial data are exactly

    V={v smooth real periodic: ||v||inf<=1/2,
       max_(|mu|<=s)||partial^mu v||inf<=1,
       min v<0<max v}.

Only exact scalar v(x) is acquired. Repeated points and preprocessing
count. The strong profile norm has the spatial supremum inside the
expectation.

The known-profile claim is: if the actual evaluable q0 is real,
||q0||inf<=1, and

    ||q0||_(G_(rho0/R))<=B,       R>=1,
    ||q||_(G_rho)=sum_mu rho^|mu| ||partial^mu q||inf/(mu!)^2,

with fixed B>=1,rho0>0 and lookup cost Wq, then for S>=0,P>=1
a finite deterministic program has error at most exp(-P), box cutoff

    H=ceil(C R E^eta),       E=1+P+S+log(R+1),

and paid work at most C R^d E^a_solver(1+Wq). Its input Fourier
coefficients and evolved values are computed, not provided.

The long-horizon conclusion for T>=2 is an actual finite real Fourier
output with strong profile RMS at most 1/8, all-seed query cap

    [1+J(J-1)/2] k^d,
    J=ceil(1+d/(2s)),       k^d<=C exp(2dT/(2s+d)),

expected paid work at most C exp(2dT/(2s+d))(1+T)^A_work, and at most
C(1+T)^A_array final real entries. The bounded-horizon patch has
deterministic error at most 3/32.

All constants can depend on fixed d,s,p,c,beta and the declared
known-profile parameters. The model charges arithmetic, exp/log,
sin/cos, positive square roots, indexing/storage, finite integer
operations, scalar random primitives, and unknown acquisitions.
It permits fixed public constants and ideal address words. This is
an exact-operation result; cancellation and coefficient magnitudes
are not a finite-precision claim.

## 3. Actual flow and the closed-unit smoothing transfer

The positive fractional Markov semigroup in T95 has multiplier
exp(-ct(4*pi^2|nu|^2)^beta). One scalar stable clock is shared across
the spatial coordinates on each edge. Coordinatewise independent
clocks would give a different generator.

The reaction derivative satisfies

    1-D<=f'(z)<=1       on [-1,1],       f(z)=z-z^D.

Shift the polynomial reaction by D-1 in the local mild iteration.
Its shifted derivative is nonnegative on the invariant interval.
Positivity and the constant equilibria +/-1 give global bounded
continuation. For two bounded real solutions the secant potential
has the same bounds. The shifted positive Volterra series is bounded
by exp(t)P_t, proving

    |S_t v-S_t w|<=exp(t)P_t|v-w|,
    ||S_t v-S_t w||inf<=exp(t)||v-w||inf.             (3.1)

The scalar flow is

    phi_t(z)=z exp(t)/
                  [1+z^(2p)(exp(2pt)-1)]^(1/(2p)).

Consequently ||S_1v||inf<=sigma_p<1 with exactly the value in T101.
Its dependence on p is essential for the later saturation interface.

I checked the specialization of the actual field law, not just its
moment statement. The parent

    M(y)=(sum_i y_i-product_i y_i)/(D-1)

is bounded by one on the full cube: at constant-sign corners its
numerator is +/- (D-1); at other corners the same interval contains
the numerator. Multiaffine interpolation gives the bound everywhere.
Rate D-1 then gives (D-1)[M(z,...,z)-z]=z-z^D.
The first-split equation and bounded mild uniqueness identify the
tree expectation with the actual S_t.

For r=d+1 and ell0=r+d=2d+1, the T95 Gaussian Fourier bound is

    ||h_(2a)||_r^2<=H_r(1+a^(-ell0)).

Condition on the complete chronology and all clocks. Its common
variance and complete residual array are the ones prepared by the
guarded recursion. For full path clocks H_i,

    a>=1/(sum_i H_i^(-1)),
    E[a^(-ell0)|chronology]<=n^ell0 Mbar_ell0(delta).

The latter uses convexity at an integer power at least one and the
common marginal law of each full H_i. It does not assume independent
leaf path totals. The stopped birth moment gives

    E n^k<=exp[(D-1)delta(D^k-1)].

These facts give exactly T101's V_j(delta), with no cutoff dependence.

For the order-zero field and any closed-unit continuous q,

    F_omega(q)=h_(2a)(.-U)P_tree(q(U+Z_1),...,q(U+Z_n)),

the pointwise leaf bound still holds at +/-1. Strong measurability,
the common-Gaussian identity through the complete nonlinear
polynomial, and the j=0 integrable envelope therefore give

    S_delta q=E F_omega(q) in H^r,
    ||S_delta q||_r<=sqrt(V_0(delta)).                (3.2)

This step takes no derivative at a boundary point. It is the precise
reason the closed-unit transfer is valid. Fourier Cauchy--Schwarz,
with E_d^2=1+4d 3^(d-1), now gives

    ||S_delta q||_W<=B_delta
       :=max(1,E_d sqrt(V_0(delta))).                 (3.3)

No field sample is executed to supply a norm or a known value to the
deterministic solver. Its role here is an analytical regularity proof.

## 4. Weighted Wiener algebra and complete early/late coverage

With kappa_F=c(2*pi)^alpha, use

    ||u||_(W_b)=sum_nu exp(b|nu|^theta)|uhat(nu)|.

For 0<theta<=1,

    |nu+mu|^theta<=|nu|^theta+|mu|^theta,

so weighted convolution proves the algebra inequality with constant
one. For a=kappa_F/2 and t>=s0, the heat multiplier satisfies

    exp(a(t-s0)|nu|^theta-kappa_F(t-s0)|nu|^alpha)<=1.

At nonzero lattice frequencies this uses |nu|>=1 and alpha>=theta;
at zero the multiplier is one. Thus the growing-weight heat map
used in T101 is a contraction.

On the ball sup_(0<=t<=h)||u(t)||_(W_(at))<=2B0, the nonlinear
increment and its Lipschitz factor are at most

    h[2B0+(2B0)^D],
    h[1+D(2B0)^(D-1)].

The two inequalities in T101 (4.2) make the map invariant and
contractive. The stated curve space is complete: convergence in
its norm implies uniform W convergence, and the weighted estimates
pass by coordinate limits and summation. At each fixed output time
the integrand is strongly measurable in the separable weighted
sequence space and has a uniform integrable bound. The mild integral
exists there. Its unweighted W continuity follows from the strongly
continuous heat map and continuous polynomial reaction. Actual PDE
uniqueness then identifies this weighted solution.

Independently, the Gevrey norm is an algebra because its normalized
Leibniz coefficient is 1/binom(mu,nu)<=1. Real heat commutes with
derivatives, contracts each derivative sup norm, and is strongly
continuous in the summed norm by domination. The displayed h0 in
T101 therefore gives ||S_tq0||G<=2B on [0,h0], independently of R.

Here is a constructive early-tail derivation. With n=|nu|inf>=1,
integrate by parts j times in a coordinate attaining n:

    |uhat(t,nu)|<=2B [R/(2*pi*rho0*n)]^j (j!)^2.

Set y=sqrt(2*pi*rho0*n/R). For y>=4 take j=floor(y/2).
Then j>=y/4 and (j/y)^2<=1/4. Using j!<=j^j gives a bound
2B exp[-(log 2)y/2]. For y<4, the order-zero bound enlarges
this to the common estimate

    |uhat(t,nu)|<=8B exp[-b sqrt(n/R)],
    b=(log 2)sqrt(2*pi*rho0)/2.                       (4.1)

The n-th box shell contains at most 2d 3^(d-1)n^(d-1) points.
Split the exponential in half and bound the remaining sum by
C R^d. For an explicit finite constant, group n into intervals
R j^2<=n<R(j+1)^2. Since R>=1, the resulting majorant is

    R^d sum_(j>=0)(2j+3)(j+1)^(2d-2)exp(-b j/2).

This polynomial-geometric sum is a finite rational expression in
exp(-b/2): generate its powers by repeated r d/dr applied to
1/(1-r). Thus it needs no integration or infinite-sum primitive.
We obtain the claimed C0 R^d exp(-b0 sqrt(H/R)) with fixed
computable constants, including small H/R.

Now set delta=h0/4, take h1 exactly as in T101 (4.5), and put
t_star=delta+h1. The inequalities give

    0<h1<=h0/4,       t_star<=h0/2.

At any t>=t_star, restart from the actual closed-unit state at
t-t_star. Equation (3.3) supplies W norm B_delta after delta.
The growing-weight argument supplies W_(a h1) norm at most
2B_delta after the remaining h1. Therefore

    sum_nu exp(b1|nu|^theta)|uhat(t,nu)|<=2B_delta,
    b1=a h1>0,       t>=t_star.                       (4.2)

This proves the late tail 2B_delta exp(-b1 H^theta).
The intervals [0,h0] and [t_star,infinity) overlap; there is no
uncontrolled transition interval. The sum of the early and late
tail bounds consequently controls the actual PDE at every time
used by the solver.

At time one (4.2) also holds for every closed-unit continuous input,
regardless of any initial Gevrey bound. When beta<1/2 its exponent
is 2beta, not one. The proof never asserts a spatial analytic strip
in that regime.

## 5. Direct complex-time L1 bound and computable constants

The new complex-time proof is valid for every alpha in (0,2],
including alpha=1. I checked its decomposition and every summability
and normalization step.

Use the Fourier convention

    inverseFT b(x)=(2*pi)^(-d) integral exp(i x.xi)b(xi) dxi.

For eta0 and psi=eta0-eta0(2.) from T101, one has, at xi!=0,

    sum_(j<=0)psi(2^-j xi)=eta0(xi),
    sum_(j>=1)psi(2^-j xi)=1-eta0(xi).

Thus the low-annulus subtraction of one gives exactly the symbol
m_w(xi)=exp(-w|xi|^alpha), rather than adding a delta mass.
At xi=0 the eta0 term gives one. Each fixed nonzero frequency
belongs to only finitely many annuli.

Let l=ceil((d+1)/2), M=2l>d. If b is supported in the radius-two
ball, integration by parts gives

    |inverseFT b(x)|
      <=(2*pi)^(-d) 4^d(1+d)^l
         max_(|mu|<=M)||partial^mu b||inf (1+|x|^2)^(-l).

The support volume is at most 4^d. The coefficient sum of
(1-Delta)^l is (1+d)^l. Integrating over the central cube and
dyadic outer cubes gives exactly the safe C_inv displayed by
T101:

    (2*pi)^(-d)4^d(1+d)^l
                [2^d+2^(2d)/(1-2^(d-2l))].           (5.1)

The last denominator is positive. Rescaling an annular symbol
does not change the inverse transform's L1 norm.

All derivatives used here have constructive finite bounds. On
1/2<=|y|<=2, differentiating a term
C y^mu |y|^(alpha-2k) gives exactly the two terms listed by T101.
Its bound |C|2^(|mu|+|alpha-2k|) is valid for either sign of the
radial exponent. Finite multi-index enumeration through order M
produces the required majorants.

For the cutoff, the recurrence for derivatives of exp(-1/t) is
correct: a term a_m t^-m exp(-1/t) differentiates to coefficients
-m a_m at power m+1 and a_m at power m+2. The bounds m^m for
t^-m exp(-1/t), and one for m=0, are sufficient. The denominator
phi(t)+phi(1-t) is at least exp(-2). Differentiating its reciprocal
gives exactly T101's R_j recurrence. Flat endpoint matching and
finite quadratic composition then bound eta0 and psi.

For lambda_j=2^(j alpha), the fixed-annulus low derivative bound
is C_low lambda_j. For order zero this follows from

    exp(-w lambda r)-1=-w r integral_0^lambda exp(-w t r)dt,

whose absolute value is at most lambda r since Re w>=0.
For positive derivative order every chain-rule term has at least
one lambda factor; lambda^k<=lambda when lambda<=1.
Product differentiation with psi preserves this bound.

For j>=1, every derivative has at most M lambda factors and

    |exp(-w lambda_j |y|^alpha)|
           <=exp(-a_* lambda_j),
    a_*=2^(-alpha)/sqrt(2)>0.

This proves the stated C_high(1+lambda_j)^M exp(-a_*lambda_j).
C_eta,C_low,C_high are finite chain/product-rule sums, constructible
by enumeration from the preceding bounds. They are not suprema
supplied by an oracle.

The low series sums to at most C_low/(1-2^-alpha).
For lambda>=1,

    (1+lambda)^M exp(-a_*lambda)
       <=(4M/a_*)^M exp(-a_*lambda/2).

Indeed use 1+lambda<=2lambda and maximize
lambda^M exp(-a_*lambda/2); dropping its exp(-M) only enlarges
the bound. Also 2^(j alpha)>=(1+j(2^alpha-1)).
With r_*=exp[-a_*(2^alpha-1)/2], the high series is therefore
bounded by the geometric expression in T101 (5.5). All its
denominators are positive for alpha>0.

The inverse-transform series converges absolutely in L1. Its Fourier
transform equals m_w at every frequency, identifying the actual
kernel. Restoring |z| and c uses the positive real spatial dilation
(c|z|)^(1/alpha), which preserves L1 norm. Periodization cannot
increase it. The torus coefficients are

    exp(-cz|2*pi*nu|^alpha),

exactly those of exp(zA). Hence the explicit K_sec satisfies

    ||exp(zA)||_(C->C)<=K_sec,
    z!=0,       |arg z|<=pi/4.                        (5.2)

This is not an absolute torus Fourier-sum estimate near zero.
The latter would be inappropriate for this cutoff-independent bound.

On compact subsets of Re z>0, the torus Fourier series and its time
derivatives converge in operator norm. At zero, density of
trigonometric polynomials and (5.2) prove strong continuity in the
closed cone. Restriction to a Fourier subspace keeps the same bound;
there is no additional projector factor in the linear heat map.

R24's primary-source discussion is consistent context only. The
direct argument just verified supplies the entire cone bound,
including alpha=1, without importing a theorem that omits that case.

## 6. Cutoff selection, initialization, and the real Galerkin bootstrap

The Dirichlet-kernel bound is sufficient also on complex C(X).
In one dimension, for distance t<=1/2 to the nearest integer,

    |D_H(t)|<=min(2H+1,1/(2t)).

Its integral is at most 1+log(2H+1). Tensoring proves the larger
majorant Lambda_H=[4(1+log(2H+2))]^d used by T101.

Let U solve the exact finite Galerkin ODE from the computed initial
array and u be the actual PDE. Until ||U||inf reaches two,

    D(t):=||U(t)-u(t)||inf
      <=epsilon0+t_H+L2 Lambda_H integral_0^t D(r)dr,
    L2=1+D 2^(D-1).

This follows by comparing U to P_Hu and then adding the true
projection tail. No positivity of P_H is used. Gronwall gives
T101 (6.2). Once its right side is at most exp(-P)/4<=1/4,
||U||inf<=5/4. The first-exit bootstrap and bounded finite-dimensional
coefficients prove actual continuation to S.

The cutoff preserves exactly the R^d work scale. Since theta<=1,

    eta/2>=d+4,       eta theta>=2d+8.

For C>=1 and E>=1,

    H<=2C R E^eta,
    Lambda_H<=Lambda0(C) E^d,

where, for example,
Lambda0(C)=[4(2+log 6+eta+log C)]^d is a sufficient public bound.
Thus the necessary error exponent is bounded by
C_fixed(1+log C)^d E^(d+1)+d log R+P.
Both sqrt(H/R)>=sqrt(C)E^(d+4) and
H^theta>=C^theta E^(2d+8) dominate it.

This choice can be made by a finite public program. For example,
double C until both

    b0 sqrt(C)>=1+L2 Lambda0(C)+d+log^+(16 C0),
    b1 C^theta>=1+L2 Lambda0(C)+log^+(16 B_delta)

hold. The left sides outgrow every polynomial in log C, so this
loop terminates for fixed parameters. These inequalities make the
two terms of epsilon0+t_H small enough for the required bootstrap,
after the harmless prefactor allocations just displayed. No test of
the actual PDE or an unknown profile is performed.

For initialization, the actual Q0-grid FFT gives, at retained nu,

    qtilde(nu)-qhat(nu)
       =sum_(m in Z^d, m!=0) qhat(nu+Q0 m).

Different retained nu have disjoint residue classes because Q0>=4H.
Every aliased frequency has |nu+Q0m|inf>=Q0-H>H. Therefore

    sum_(|nu|inf<=H)|qtilde(nu)-qhat(nu)|
       <=sum_(|k|inf>=Q0-H)|qhat(k)|
       <=sum_(|k|inf>H)|qhat(k)|.                    (6.1)

This is the precise inclusive boundary stated in the original T84
argument. It proves the epsilon0 bound from the initial Gevrey
tail without any retained-mode factor.

The phrase “beyond Q0-H” must be read with this inclusive lattice
boundary. A strictly greater-than Q0-H tail would miss a mode
at equality; it is neither needed nor imposed by a formula in
T101. For example a sufficiently small multiple of
cos(2*pi*(Q0-H)x) in one dimension aliases into the retained H
mode while its strict tail above Q0-H is zero. Equation (6.1)
avoids that reading and leaves every source estimate unchanged.

For f(U), the full support of U^D is in the D H box.
A power-of-two grid Q>2D H represents that entire polynomial
without aliasing. Its FFT, pointwise fixed power, inverse FFT,
and restriction compute the actual P_H(U-U^D). The number of
grid points is O_(d,D)(H^d), and radix-two butterfly work,
twiddles, padding, fixed integer powers, and memory accesses
cost O_(d,D)(H^d log(H+1)). Conjugate symmetry is preserved.
The source uses the required degree-dependent strict padding.

## 7. Complex neighborhoods and all panel geometries

From any real Galerkin state of norm at most 5/4, use the
radius-Bcx ball with

    Bcx=4K_sec,
    Fcx=Bcx+Bcx^D,       Lcx=1+D Bcx^(D-1),
    rho_H=1/[16K_sec Lambda_H(1+Fcx+Lcx)].

The linear complex heat term has norm at most (5/4)K_sec.
The radial mild nonlinear increment is at most 1/16, and its
Lipschitz factor is at most 1/16. Thus the ball is invariant and
the sector fixed point is holomorphic and bounded. By uniqueness
it extends the actual finite ODE. These are analytical restarts,
not algorithmic calls for exact trajectory values.

The initial disk is checked separately. For a Fourier polynomial V,

    ||A_H V||inf
       <=sum_(|nu|inf<=H) a_nu |Vhat(nu)|
       <=M_H||V||inf,
    M_H=(2H+1)^d c(4*pi^2 dH^2)^beta.

On the radius-four disk-space ball the vector field is bounded
by 4M_H+Lambda_H F4, and has Lipschitz bound
M_H+Lambda_H L4. The displayed

    a_H=1/[16(1+M_H+Lambda_H(F4+L4))]

therefore gives an invariant disk and contraction factor at most
1/16. The image stays below 5/4+1/4<4.
In particular log(1/a_H)=O(1+log(H+1)), although M_H itself
can be polynomially large in H.

The chosen h is at most rho_H/100 and 1/100. It also satisfies

    L4 h Lambda_H beta_L<=1/4,
    F4 h Lambda_H beta_L<=1/2.

I checked the small-S and truncated panels explicitly:

- S=0 skips the time panels and returns the initialized polynomial.
- The first positive panel has length min(S,a_H/16,h/16).
  Its parameter-two ellipse lies inside the initial disk.
- A startup panel [t,t+ell], with ell<=t, has ellipse real part
  at least 7t/8, imaginary part at most 3t/8, and modulus below
  3t. It lies in the forward cone from zero. Until completion of
  startup, t<h, so its radius is below rho_H.
- A later panel [b,b+ell], ell<=h, uses the cone from the real
  time b-h>=0. Its relative ellipse has real part at least
  7h/8, imaginary part at most 3h/8, and modulus below 3h.

Thus neither a truncated startup interval nor a very short final
interval loses the uniform ellipse parameter. If the horizon ends
during startup, no later-panel construction is needed.

The number of doubling panels is O(1+log(H+1)+log(L+1)).
The later count is at most 1+S/h. Consequently

    n_pan<=C[1+log(H+1)+log(L+1)+S Lambda_H beta_L]
         <=C E^(d+2).                               (7.1)

The large generator enters only log(1/a_H). This is the step
that preserves R^d in the solver work count.

## 8. Interpolation, fixed Picard iterations, and numerical stability

The actual projected forcing is bounded by C Lambda_H on each
parameter-two ellipse. Its Banach-valued Chebyshev coefficients
are therefore bounded by C Lambda_H 2^-n. At Lobatto nodes every
higher Chebyshev mode aliases to a mode of degree at most L,
with real-interval norm at most one. Summing the omitted modes
gives interpolation error C Lambda_H 2^-L, with no dimension
factor or extra Lebesgue multiplier in this error estimate.

For completeness, the logarithmic Lebesgue estimate has a direct
finite proof. For L>=1 the even trigonometric interpolation kernel
on 2L equally spaced angular points is

    D_L^*(t)=1+2 sum_(k=1)^(L-1)cos(kt)+cos(Lt)
           =sin(Lt)cot(t/2).

At wrapped distance |t|<=pi,

    |D_L^*(t)|<=min(2L,2/|t|).

The Lobatto polynomial is the restriction of this interpolation
to even data. Grouping nodes by their distance from the evaluation
angle and summing the harmonic bound gives a Lebesgue majorant
4+4 log(L+1), hence certainly beta_L=8(1+log(L+1)).
The node values themselves are handled by continuity.

Use the source nodal map on the real radius-four ball. With
||U_b||inf<=2, the free heat term has norm at most two.
The nonlinear increment is at most F4 ell Lambda_H beta_L,
and the Lipschitz factor is

    q_ell=L4 ell Lambda_H beta_L<=1/4.

The image lies within radius 5/2. A concrete computable initial
iterate is the free heat array
V_i^(0)=exp(theta_i ell A_H)U_b, as in the inherited T94/T81
scheme. It lies in the ball. Exactly L Picard iterations therefore
have error at most C 4^-L from the unique fixed point.
No convergence test or unknown supremum is used.

Insert the exact Galerkin nodal values into this finite map.
The initial array discrepancy contributes at most e, while the
forcing interpolation defect contributes C ell Lambda_H 2^-L.
Contraction then gives

    e_next<=e/(1-q_ell)
               +C ell Lambda_H 2^-L/(1-q_ell)+C4^-L.  (8.1)

The exact Galerkin ODE starts from the computed FFT array, so
the first panel has e=0; its error relative to the actual PDE
was already charged in Section 6.

Since -log(1-q)<=4q/3 for q<=1/4 and sum ell=S,
the amplification product is at most exp(C S Lambda_H beta_L).
Summing defects proves exactly

    exp(C S Lambda_H beta_L)
       [C S Lambda_H 2^-L+C n_pan 4^-L].             (8.2)

This is not an exponential in the number of startup panels or
in H^alpha S. Each stability loss is proportional to that
panel's chronological length.

The choice L=ceil(C_time E^(d+4)) closes the argument uniformly.
After the fixed spatial cutoff constant is chosen,
Lambda_H<=C E^d and

    beta_L<=C[1+log(C_time+2)+log E].

The logarithm of the growth and defect prefactors in (8.2) is
bounded by a computable constant of at most logarithmic growth
in C_time times E^(d+2). The decay exponent is proportional to
C_time E^(d+4). Doubling the public C_time until the resulting
finite scalar domination inequality holds terminates, since
C_time outgrows log(C_time+2). This makes (8.2)<=exp(-P)/4.

The same estimate holds at every completed prefix of the panel
list. Induction therefore keeps each computed start within
5/4+1/4<2, justifying every preceding contraction estimate.
This is the second bootstrap; the first was the exact Galerkin
bootstrap. Neither invokes a numerical maximum principle.

## 9. Exact finite weights and the complete solver work

For nonzero nu, the actual fractional eigenvalue is

    a_nu=c exp(beta log(4*pi^2|nu|^2)).

The logarithm argument is positive. The zero mode is set to zero
before this expression is used. For every positive panel length,
z=a_nu ell is positive at nonzero frequency.

Expanding each Lobatto cardinal polynomial reduces its convolution
weights to I_k(z,theta). Direct integration by parts gives

    I_0=(1-exp(-z theta))/z,
    I_k=theta^k/z-(k/z)I_(k-1),       z>0.

The guards z=0 and theta=0 give the exact elementary integrals
theta^(k+1)/(k+1) and zero respectively. Node denominators
cannot vanish because the Lobatto nodes are distinct.
The S=0 branch has no panel integral.

These are exact recurrences, not numerical quadrature calls.
All nodes, monomial coefficients, integer powers, and recurrences
have finite loops in the stated primitives. Cancellation for
small z does not change this exact-operation statement.

Here is an independent operation account, with D_H=(2H+1)^d:

1. Constructing all cardinal monomial coefficients costs O(L^3).
   For each mode and output node, computing I_0,...,I_L costs O(L).
   Dotting these against all cardinal polynomials costs O(L^2).
   Across all nodes and modes this is O(D_H L^3) per panel.
2. For each Picard step, form the projected reaction at every
   time node by the padded FFT. This costs
   O_(d,D)(L D_H log(H+1)).
3. Multiplying the stored convolution weights by the nodal
   forcing arrays costs O(D_H L^2) per step. Linear heat terms
   and node-array accesses are no larger.
4. Exactly L iterations give per-panel work
   O(D_H[L^3+L^2 log(H+1)]), including the weight preparation.
5. Initial Q0-grid evaluations and FFT cost
   O(D_H[Wq+log(H+1)]). The actual q0 evaluator is charged here.
   Twiddle construction, padding, copying, indexing and storage
   initialization fit these bounds. Point evaluation of the
   final array costs O_d(D_H).

Weight storage is O(D_H L^2) and nodal storage O(D_H L).
Every stored entry is constructed and accessed within the listed
work. No free dense matrix, FFT, source evaluator, or Fourier
coefficient oracle has entered.

Combining H<=C R E^eta, L<=C E^(d+4), (7.1), and
log(H+1)<=C E, the largest term has exponent

    eta*d+(d+2)+3(d+4)=eta*d+4d+14.                  (9.1)

The other term has exponent at most eta*d+3d+11, and
initialization costs at most C R^d E^(eta*d+1)(1+Wq).
Thus a_solver=eta*d+5d+20 is safely sufficient.

The Galerkin and time errors total at most exp(-P)/2,
within the asserted exp(-P) allowance. At S=0 the initialized
polynomial's alias error plus true tail gives the same assertion.
This verifies the known-profile theorem for all its stated
parameters, including the zero-horizon guard.

## 10. Original-class interpolation and actual derivative samples

The interpolation is a constructed known representation, not an
extra assumption on v. The compact flat bump has Gevrey-2
derivative bounds. One elementary justification starts with

    phi(t)=exp(-1/t),       t>0.

On the complex disk |z-t|<=t/2,
Re(1/z)>=2/(9t). Cauchy's estimate, followed by optimization of
t^-n exp(-2/(9t)), gives a bound 9^n(n!)^2.
The flat extension is smooth. The compact bump can also be written
as a product of flat exponentials with arguments 1-t and 1+t.
Products and the reciprocal induction preserve these bounds.

Its translate denominator is at least exp(-4/3), because a nearest
integer is within 1/2. Only a fixed number of translates is active.
Tensorization gives a finite-overlap smooth partition with the
required multi-index bounds.

Each tensor stencil reproduces all polynomials of total degree
at most s-1. Compare it to the total-degree Taylor polynomial
at the evaluation point. All relevant grid nodes lie within
C_(d,s)/k, and the remainder only uses derivatives of total
order s. Fixed cardinal bounds and the partition identity give

    ||v-g||inf<=Cint k^-s.

Bounded stencil coefficients and the scaled flat weights give

    ||partial^mu g||inf<=B0(C0 k)^|mu|(mu!)^2.

For a small fixed rho0 this sums to the required Gevrey norm
at R=k. With k>=k0, the source condition makes ||g||inf<=3/4.
The construction uses exactly k^d values and O_(d,s)(k^d) paid
work. Lookup needs floors, periodic indices, a bounded number
of stored stencils, guarded bumps, and fixed arithmetic:
Gg<=C_(d,s). The argument also works for s=1.

The derivative field is the T95 actual field specialized to
the bounded parent already checked in Section 3:

    W_j=h_(2a)(.-U) z,
    z=(n)_j C_I product_b(v-g)(U+Z_(I_b)).

The entire clock-conditioned residual vector is used. It is
not replaced by independent coordinates or by residuals from
another diffusion. The common Gaussian variance is 2a, so
the Fourier damping is exp(-4*pi^2 a|nu|^2).
The real pair coefficients have the positive sine sign in
T101 (8.3), since the kernel is translated by x-U.

The full derivative is an ordered-injection sum. Uniform
tuple sampling cancels (n)_j; only the Taylor coefficient
later divides by j!. The mixed partial bound |C_I|<=1
comes from the signed cube-corner difference formula.
Its actual second moment is at most V_j||v-g||inf^(2j).

Finite-tree Taylor remainders with one and two extra labels
and the corresponding envelopes justify genuine Frechet
differentiation on the open C(X) unit ball. For the coarse
g and promised v, their whole joining segment has norm at
most 3/4. This checks the domain of the Taylor remainder;
no derivative at a closed-unit endpoint is invoked.

Complete sample preparation uses the actual guarded stable
formula, chronology, linear variance/residual passes, tuple
selection, known-leaf cache, and finitely many corner passes.
For fixed j,D,d it costs C[(1+Gg)n+K], including all K entries.
The tree's first moment gives expected cost C(1+Gg+K).
At most j unknown scalar values are acquired, after preparation,
with repetitions charged. The n<j branch acquires none.

## 11. Projected mean, true tail, clipping, and strong risk

Set q=s+d/2 and m=J-1. The time-one true tail from Section 4
allows

    N=O((1+T)^(1/theta)),       K=(2N+1)^d.

T101's precise N makes the tail at most epsilon/2, where

    S=T-1,       epsilon=exp(-S)/(16*25).

Its k choice gives Cstar k^-q<=epsilon/(4E_d), and
k^d<=C exp(dT/q). There is no K in this query calibration.

The order-zero term is paid. The known-profile solver from g
uses R=k and sup precision tau_base=epsilon/(4E_d D_N),
where

    D_N=sqrt(K)(1+dN^2)^(r/2),       r=d+1.

Each retained complex Fourier coefficient error is at most
tau_base. Summing the weighted squares proves the actual
H^r error bound D_N tau_base. The solver cutoff can contain
the N box: eta>1/theta, P_base>=S, and its fixed constant
can be enlarged. Also E_base=O(1+T), since log k=O(1+T)
and log D_N=O(log(2+T)). Its cost is therefore
C k^d(1+T)^a_solver.

For fixed v the coarse g is deterministic. Independence between
complete samples and Hilbert centering give

    E||M^-1 sum_a(P_N W_(j,a)-E P_NW_j)||_r^2
          <=V_j||v-g||inf^(2j)/M,       M=k^d.        (11.1)

This makes no independence assertion about coordinates inside
one Fourier array. Projection contracts the Hilbert norm and
the mean is the projected actual derivative.

Hilbert Minkowski, the paid base error, and the Taylor bound
now give

    RMS_H(p_raw-P_NS_1v)
       <=epsilon/(4E_d)
         +sum_(j=1)^m B_j Cint^j k^(-js-d/2)/j!
         +B_J Cint^J k^(-Js)/J!
       <=epsilon/(2E_d).                             (11.2)

The final inequality uses js+d/2>=q for j>=1 and Js>=q.
Thus it uses exactly the promised s derivatives.

Every true constant real coefficient lies in [-1,1] and every
true cosine/sine coefficient in [-2,2]. The H^r squared error
in that real basis is diagonal with nonnegative weights,
including the factor 1/2 for each pair. Coordinate clipping
decreases it pathwise. Bias introduced by clipping is harmless.

The conversions
c_cos=2 Re uhat and c_sin=-2 Im uhat match the sample signs.
Applying the Sobolev embedding to (11.2) and separately adding
the true omitted tail proves

    (E||p_N-S_1v||inf^2)^(1/2)<=epsilon.              (11.3)

The spatial supremum is inside the expectation. Neither the
tail nor the nonlinear target has been silently replaced by a
projected target.

## 12. Saturation, continuation, output, and total exponents

The degree-dependent identity interval contains the actual
time-one range:

    sigma_p<a_chi=(1+sigma_p)/2
           <b_chi=(1+a_chi)/2<1.

The flat transition's denominator is positive and its endpoint
pieces are guarded. The middle formula is a convex combination
of z and b_chi, and its derivative is
1-wflat(t)+(1-t)wflat'(t). The bounds in the original sources
give 0<=wflat'<=8e<24, hence the global Lipschitz constant 25.

The Cauchy estimate just used for flat exponentials also proves
their Gevrey-2 bounds. For a denominator bounded below by delta,
differentiate D R=1 and normalize by (n!)^2. The resulting
coefficients are 1/binom(n,j); enlarging the geometric constant
bounds their sum. Products and fixed affine rescaling preserve
the estimate. Consequently

    ||chi^(n)||inf<=Achi Cchi^n(n!)^2,

with constants depending on the fixed p. This verifies all-order
regularity of the actual elementary evaluator, rather than
merely smoothness.

For every clipped array, derivative bounds for its polynomial
and the ordered finite-jet chain rule give

    ||partial^mu chi(p_N)||inf
      <=Achi(2*pi*N)^n
                      sum_(l=1)^n(2Cchi K)^l l! l^n,
    n=|mu|.

Use l!<=n!, l^n<=n^n<=e^n n!, n<=2^n, and
n!<=d^n mu!. This proves a bound
Achi(C_(d,p)NK)^n(mu!)^2. After summing at a fixed small
radius, the continuation input therefore satisfies

    ||qhat||inf<=b_chi<1,
    ||qhat||_(G_(rhohat/Rhat))<=Bhat,
    Rhat=NK,       Wqhat<=C_d K.                     (12.1)

These are deterministic bounds for every completed clipped
array; no favorable-event regularity test is needed.
Evaluating the Fourier sum, accessing its coefficients, and
applying chi accounts for the K source-evaluation cost.

Because chi is the identity on S_1v, equation (11.3) gives
RMS(qhat-S_1v)<=exp(-S)/16. Actual real-flow comparison is
applied pathwise before expectations. The paid final solver
with P_out=T+log16 gives conditional deterministic error
at most exp(-T)/16. Minkowski then gives

    RMS_inf(U_T-S_Tv)<=1/16+exp(-T)/16<=1/8.           (12.2)

The numerical trajectories themselves need no invariant-interval
assertion; the two bootstraps already control their errors.

The complete paid count is:

    coarse/base: C k^d(1+T)^a_solver,
    fields and accumulation: C k^d(1+K),
    continuation:
      C(1+T)^(a_solver+d(d+2)/theta).

For the last line, Rhat<=C(1+T)^((d+1)/theta),
Wqhat<=C(1+T)^(d/theta), and E_out<=C(1+T).
The factor d/theta from the actual evaluator is included.

Thus T101's stated
A_work=a_solver+ceil(d(d+2)/theta)+2 is sufficient.
The final cutoff is at most C(1+T)^(eta+(d+1)/theta);
its number of real entries is bounded by the stated
A_array=eta*d+ceil(d(d+1)/theta). The exponentially larger
base array remains counted as intermediate work.

Unknown queries are exactly the coarse acquisitions and the
selected tuples. On every seed path,

    Q<=k^d+M sum_(j=1)^m j
      =[1+J(J-1)/2]k^d.

Preparing a nonterminating tree on a null seed makes no further
queries for that sample. It cannot violate the global hard cap.
Nonexplosion and finite deterministic loop counts give almost-sure
termination and finite expected work.

All finite computations and branch guards are Borel. The output
is a finite indexed real array, hence a measurable continuous
profile; assigning an arbitrary array on the null nontermination
set defines the risk without an algorithmic test of that set.
No unknown derivative, integral, Fourier, evolved-value, or
stable-distribution oracle is added.

For 0<=T<=2, the fixed interpolation grid makes its propagated
error at most 1/16. Applying the solver with precision log32
adds at most 1/32. The S=0 and truncated-panel analysis above
covers the endpoints. This proves the deterministic 3/32 patch
with bounded work and no singular small-time field use.

## 13. Verdict boundary and provenance

No substantive gap or counterexample to the frozen theorem was
found. The precise inclusive alias boundary and the concrete
free-heat Picard initialization are recorded above from the
underlying source construction; neither changes an error budget,
a parameter choice, or a claimed exponent.

The proof uses classical positive-semigroup comparison, branching
representation, stable subordination, Fourier algebras, dyadic
kernel estimates, Galerkin comparison, polynomial interpolation,
and elementary scalar convolution recurrences. The scoped R24
literature note supplies context, not a proof of the paid solver,
query theorem, or novelty.

PASS here is conventional mathematical acceptance of this upper
construction in its exact-real model. It does not imply a matching
lower bound, full Lean verification, measured speedup, floating-point
stability, or priority. T102 is not a premise anywhere in this audit.

The only operations executed for T104 were file reads, working-tree
inspection, SHA256 checks, and edits of this new review. No numerical
or symbolic experiment, random sampler realization, unknown-input
acquisition, PDE execution, Lean command, or implementation edit was
performed. Final source-lock verification accompanies the handoff.

