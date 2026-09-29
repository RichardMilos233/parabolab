# T102: fractional odd-power long-horizon lower feasibility

Date: 2026-09-29. Conventional proof candidate for independent review.
Requested research configuration: gpt-6-astra/max. This worker cannot
independently attest its backend model or reasoning effort.

**Verdict: feasible.** For every fixed fractional exponent in (0,1],
positive diffusion coefficient, and normalized odd-power reaction below,
the original complete signed smooth class has the same exponential
point-query lower bound as D45. The proof covers the strong profile loss
and arbitrary measurable biased, adaptive, privately randomized, almost
surely stopped algorithms.

This is a lower-bound candidate only. It neither uses the active T101
upper-bound work nor establishes a matching fractional complexity theorem.
Its only output is this review file. No new numerical, symbolic, Lean,
unknown-input, or sampler execution accompanies it.

## 1. Exact statement and information model

Fix integers d,s,p>=1, constants 0<beta<=1 and c>0, and put

    X=(R/Z)^d,        D=2p+1,
    q=s+d/2,         gamma=d/q=2d/(2s+d).

Volume on X is normalized to one. The fractional Laplacian convention is

    (-Delta)^beta exp(2*pi*i*nu.x)
       =(4*pi^2*|nu|^2)^beta exp(2*pi*i*nu.x).

Let S_t be the actual bounded mild flow of

    u_t=-c(-Delta)^beta u+f(u),       f(u)=u-u^D.          (1.1)

Keep exactly the signed class of D45:

    V={v smooth periodic real: ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.                                  (1.2)

There is no common bound on derivatives above s, analytic radius, mean
margin, basin information, or number of unstable spatial modes.

The only acquired information about v is an exact scalar v(x). Every
acquisition counts, including preprocessing, repeated points, zero-valued
answers, and previously visited cells. Selection rules and outputs are
measurable. A private random seed has an arbitrary measurable probability
space and is independent of the input. Algorithms may be biased, adaptive,
and almost surely stopped separately for each promised input. Auxiliary
computation is free for the query lower bound.

At a prescribed point x*, suppose an algorithm returns a real Z_T with

    sup_(v in V) E|Z_T-S_Tv(x*)|^2 <=1/16.                (1.3)

For a profile algorithm use a finite explicitly indexed real Fourier
polynomial U_T and require the stronger loss

    sup_(v in V) E||U_T-S_Tv||inf^2 <=1/16.               (1.4)

The supremum over space is inside the expectation. Let N_v be the total
number of initial-value acquisitions on input v.

The conclusion proved below is: there are explicit finite T0 and
C_lower>0, depending only on the fixed parameters and a fixed public
bump, such that for every real T>=T0, every algorithm satisfying (1.3)
or (1.4) has

    sup_(v in V) E N_v >= C_lower exp(gamma T).           (1.5)

The conclusion passes to the infimum over algorithms. It also gives
the same lower bound for any paid-work model charging at least one unit
per acquisition. No upper bound, exact total-work Theta assertion,
finite-bit claim, or uniformity as beta or c tends to zero is made.

## 2. Frozen direct inputs and proof boundary

All six direct locks below were checked with SHA256. The two accepted
checkpoints and the complete underlying proof/audit texts are the
mathematical inputs; this does not rely merely on their PASS labels.

| Input in the same run | SHA256 |
| --- | --- |
| 04ac-fractional-fixed-time-fields.md | 3330cccbe4fd4f666569b1f94401a7d8308d3a2ec5302f02616fd188c253ae3d |
| reviews/T95-fractional-diffusion-field-feasibility.md | 9bc1d42d582f75b96a4e562dacbc925cbd01151b2a3b4702c5dc2b0a1ab99d74 |
| reviews/T97-fractional-field-independent-audit.md | 9e38a6d166806997d9c42ab8653615edad0a47b0fc1fa81dc9e31e980f5dec90 |
| 04ab-odd-power-long-horizon-complexity.md | a8bd72ec33c69aae4d50126c72f6fd75ac4e1625cb08cfcef6a1b310918d18c0 |
| reviews/T94-odd-power-long-horizon-feasibility.md | 2600c29a2823aefd9a69578de113bc511179d97bdfbea7eb3a6861ac28b7e1d9 |
| reviews/T96-odd-power-long-horizon-independent-audit.md | b8f5f32be92c820bd8b955c5969406a49fa21e12a1b38c86d17bb7467ba1eda4 |

D47 supplies the actual fractional semigroup and fixed-time derivative
field, with its clock-conditioned whole-vector Gaussian decomposition.
Section 4 below checks its higher-Sobolev specialization explicitly.
D45 supplies the prior strategy to be rederived, not a fractional lower
bound. The mixed-L1 constants, complete-slice concentration, actual
fractional PDE separation, finite thresholds, and stopped information
argument are proved below.

The accepted subordination input includes the normalized positive stable
law and its classical sampling identity as audited in T95/T97. This proof
does not assert a new stable-law identity or reverify published sources
beyond those locked inputs. It adds no literature or novelty verdict.
No unresolved formal claim, pending candidate, or upper solver is used.

## 3. Positive fractional semigroup and an explicit kernel bound

Write P_t=exp(-ct(-Delta)^beta). D47 constructs it by a single positive
clock L_t shared across all d coordinates, followed conditionally by a
Gaussian with covariance 2L_t I_d. The clock satisfies

    E exp(-z L_t)=exp(-ct z^beta),       z>=0.             (3.1)

At beta=1 it is the deterministic value ct. For 0<beta<1 it is
(ct)^(1/beta) times the normalized positive beta-stable variable. This
gives exactly the isotropic Fourier multiplier in (1.1). Independent
coordinate clocks would give a different generator and are not used.

Thus P_t is a positive, constant-preserving, Haar-mass-preserving
convolution semigroup, strongly continuous on C(X). Positivity and
Fubini give the contractions

    ||P_t h||inf<=||h||inf,       ||P_t h||1<=||h||1.      (3.2)

Its Fourier multipliers are real and nonnegative, so it is also a
self-adjoint contraction on L2.

For every a>0 and t>0, the Gamma integral and nonnegative Tonelli give

    E L_t^(-a)
      =1/Gamma(a) integral_0^infinity z^(a-1)
                                     exp(-ct z^beta) dz
      =Gamma(a/beta)/[beta Gamma(a)] (ct)^(-a/beta).      (3.3)

Only integer negative moments are needed for our constants. For an
integer h>=1 define

    b_h=ceil(h/beta),
    Mbar_h(t)=[1+(b_h-1)!]/[beta (h-1)!]*(ct)^(-h/beta)   (beta<1),
    Mbar_h(t)=(ct)^(-h)                                 (beta=1).

Indeed h/beta>=1. Splitting the Gamma integral at one bounds the first
part by one and the second by Gamma(b_h), proving

    E L_t^(-h)<=Mbar_h(t).                               (3.4)

These constants involve only fixed factorials and elementary real
operations. No Gamma or stable-density evaluation oracle is required.

Let h_(2l) be the torus Gaussian density of coordinate variance 2l.
The decreasing one-dimensional Gaussian integral bounds its Fourier sum:

    ||h_(2l)||inf
      <=[sum_(k in Z) exp(-4*pi^2*l*k^2)]^d
      <=[1+(4*pi*l)^(-1/2)]^d
      <=b_heat^d(1+l^(-d)),
    b_heat=1+(4*pi)^(-1/2).                              (3.5)

For l<=1 use l^(-d/2)<=l^(-d); for l>=1 use the bound at one.
Set

    rho=b_heat^d[1+Mbar_d(1/2)].                         (3.6)

The subordinated kernel p_t=E h_(2L_t) is positive with mass one and,
for every t>=1/2,

    ||p_t||inf<=rho,       ||p_t||2<=rho.                 (3.7)

The first inequality follows by (3.4)-(3.5) and monotonicity in t.
The second follows from normalized volume. Absolute Fourier summability
also follows from the same expected positive sum, so this kernel is a
continuous function representing P_t. In particular,

    ||P_t h||inf<=rho||h||1,
    ||P_t h||inf<=rho||h||2,       t>=1/2.                (3.8)

All these bounds hold for each fixed beta>0. There is no integral of a
short-edge spatial derivative weight.

The mild fixed point for (1.1) is globally bounded on [-1,1].
For example, add D-1 to the reaction derivative on that interval,
use the positive shifted-semigroup Picard iteration, and compare with
the constant equilibria -1 and 1. Local uniqueness then gives bounded
continuation. This is the actual PDE flow.

On this interval, 1-D<=f'<=1. A secant potential between two solutions
has the same bounds. Its positive evolution family is dominated by
exp(t-r)P_(t-r), by the shifted iteration or positive comparison.
Consequently

    |S_t v-S_t w|<=e^t P_t|v-w|,                        (3.9)
    ||S_t v-S_t w||a<=e^t||v-w||a,       a=1,infinity.

For a linearized evolution E_u(t,r), the same pointwise domination
and both norm bounds hold. Oddness and uniqueness give S_t(-v)=-S_t(v).

The scalar comparison solution for z'=z-z^(2p+1) is

    phi_t(a)=a e^t/[1+a^(2p)(e^(2pt)-1)]^(1/(2p)).       (3.10)

It stays in [-1,1] from that interval. From any initial sup norm
strictly below one it gives a strict bound below one at every finite
time. This places all states used below inside D47's open input ball.

## 4. Time-one spatial gradient from the actual D47 field

The formal estimate integral_0^1 t^(-1/(2beta))dt diverges for
beta<=1/2. Copying a direct short-time gradient Duhamel bound would
therefore not justify this proof in that range. Instead we use one
additional Sobolev order in the already accepted fixed-time field.

Here are all constants and the precise specialization. For the
polynomial f in (1.1), choose exactly the T95 bounded parent construction

    B=D,
    f(2t-1)=sum_(i=0)^B F_i binom(B,i)t^i(1-t)^(B-i),
    nu_br=1+(B/2)max_i |F_i|.                            (4.1)

The coefficients F_i are the finite Bernstein coefficients of this
fixed polynomial. They can equivalently be found from its monomial
coefficients a_l by
F_i=sum_(l<=i) a_l binom(i,l)/binom(B,l).
The parent has corner values

    c_i=2i/B-1+F_i/nu_br.

Here F_0=F_B=0. Interior base values have distance at least 2/B from
the endpoints, while |F_i|/nu_br<2/B. Thus the multiaffine cube
interpolant M has |M|<=1 and
nu_br[M(z,...,z)-z]=f(z).

Use the actual rate-nu_br, B-ary chronology and the common-coordinate
stable clocks of D47. Bounded first-branch expectation is the actual
S_t by the mild uniqueness above. If n is the population at time one,

    E n^k <=exp[nu_br(B^k-1)],       integer k>=1.        (4.2)

This follows from the stopped birth generator first; its first moment
excludes explosion before higher moments are passed to the limit.

Condition on the entire chronology and all edge clocks. The actual
leaf Gaussian covariance is
C=sum_e L_e b_e b_e^t. D47's guarded recursion produces a common
conditional Gaussian variance a and the complete residual vector,
not independent residual coordinates. If H_i is the total clock
along the i-th full root-to-leaf path, its verified harmonic bound is

    a>0 almost surely,
    a>=1/[sum_(i=1)^n H_i^(-1)].                         (4.3)

Every H_i, conditional on the chronology, has the marginal law L_1.
The H_i are generally dependent. Convexity therefore gives, for an
integer P>=1 without requiring path independence,

    E[a^(-P)|chronology]
       <=n^(P-1) sum_i E[H_i^(-P)|chronology]
       <=n^P Mbar_P(1).                                 (4.4)

No version of the sharper bound for 0<P<1 is used.

For any fixed integer r>=d+1 use

    ||w||_r^2=sum_(nu in Z^d)(1+|nu|^2)^r |what(nu)|^2,
    theta=8*pi^2,
    b0=1+sqrt(pi/theta),       b1=1+sqrt(2*pi/theta),
    H_r=(d+1)^(r-1)
          [b0^d+d*(2r/theta)^r*b1*b0^(d-1)],
    P=r+d.

The same Gaussian sum proof as T95, now at this r, gives

    ||h_(2a)||_r^2
       <=H_r a^(-r-d/2)       (0<a<=1),
    ||h_(2a)||_r^2<=H_r(1+a^(-P))       (a>0).            (4.5)

Indeed use the one-dimensional Gaussian sums at theta and theta/2,
bound |k|^(2r) exp(-theta*a*k^2) by
(2r/(theta*a))^r exp(-theta*a*k^2/2), and apply
(1+sum_i nu_i^2)^r<=(d+1)^(r-1)(1+sum_i |nu_i|^(2r)).
For a>=1 use Fourier monotonicity. With

    V_(j,r)=H_r[1+Mbar_P(1)]
                       exp[nu_br(B^(2j+P)-1)],       j>=0,
    Bfield_(j,r)=sqrt(V_(j,r)),                          (4.6)

equations (4.2), (4.4), and (4.5) give

    E[n^(2j)||h_(2a)||_r^2]<=V_(j,r).                    (4.7)

For clarity, the field underlying this conclusion is exactly D47's

    F_omega(g)=h_(2a)(.-U)
                   P_tree(g(U+Z_1),...,g(U+Z_n)),

where U is independent uniform and Z is the complete physical
clock-conditioned Gaussian residual array. Conditional common-Gaussian
integration through the complete nonlinear polynomial identifies
E F_omega(g)=S_1g. A mixed partial in distinct leaves is bounded by
one; repeated-leaf partials vanish. Thus the order-j derivative has
envelope n^j||h_(2a)||_r times the product of the direction sup norms.

Strong measurability follows as in T95 from countably many finite
tree shapes and continuity of (a,U)->h_(2a)(.-U) in H^r on a>0.
Finite-tree derivative variations and Taylor remainders have respective
integrable envelopes with powers n^(j+1) and n^(j+2), by (4.7).
Integrating those finite-polynomial identities at fixed directions
proves actual Frechet differentiation, with

    ||D^j S_1(g)||_(C^j -> H^r)<=Bfield_(j,r),
    ||g||inf<1.                                        (4.8)

Here C^j denotes j copies of the continuous-function Banach space,
not spatial C^j regularity. This is uniform on the open unit ball.
The argument does not presuppose a spatial analytic radius. It is a
mathematical map estimate; the sampler's paid-evaluator condition is
only relevant when that sampler is executed, which it is not here.

Let

    E_d=sqrt(1+4d*3^(d-1)),
    r_star=d+2,       P_star=2d+2,
    G=2*pi*sqrt(d)*E_d*Bfield_(1,d+2).                   (4.9)

The Fourier shell estimate gives ||w||inf<=E_d||w||_(d+1).
Moreover ||partial_i w||_(d+1)<=2*pi||w||_(d+2).
For ||v||inf<1 the entire segment tv is in the open ball and S_1(0)=0.
The Banach-space fundamental theorem of calculus gives

    S_1(v)=integral_0^1 D S_1(tv)[v]dt,
    ||S_1v||_(d+2)<=Bfield_(1,d+2)||v||inf,
    ||grad S_1v||inf<=G||v||inf.                         (4.10)

The gradient norm is Euclidean. This proves precisely the small-amplitude
gradient bound needed for the finite spatial net. The constants may be
very large, but are finite for every fixed beta>0 and c>0.

## 5. Mixed-L1 mean correction, with the degree-dependent constant

All products and integrals in this section are on X. Set

    C2=D(D-1),       C3=D(D-1)(D-2),
    B_D=e^2[C3+(3/2)C2^2].                              (5.1)

The actual solution map has the usual finite-time C-infinity
variations on a neighborhood of any strictly bounded initial point,
from the polynomial mild equation and Volterra iteration. Alternatively
D47 identifies these derivatives into each fixed positive-time H^r.
Differentiating the mild equation gives the following norm estimates.

A first variation is E_u(t,0)h. If a direction h is marked for its L1
norm and every other direction is measured in sup norm, (3.9) gives

    ||Y_h(t)||1<=e^t||h||1,
    ||Y_v(t)||inf<=e^t||v||inf.

The second variation has source f''(u)Y_1Y_2. Its sup bound is

    C2*t*e^(2t)||v_1||inf||v_2||inf,

and its mixed bound, with one marked direction, is

    C2*t*e^(2t)||v||inf||h||1.                           (5.2)

This follows by integrating exp(t-r) times the source norm and
using integral_0^t exp(t+r)dr<=t exp(2t).

The third variation has one f'''Y_1Y_2Y_3 term and three terms of the
form f''Y_iY_(j,k). In each product place the unique marked h in L1,
wherever it occurs, and all remaining factors in sup norm. Its mixed
bound is

    ||D^3 S_t(v)[v_1,v_2,h]||1
      <=[C3*t+(3/2)C2^2*t^2]e^(3t)
                       ||v_1||inf||v_2||inf||h||1.      (5.3)

The coefficient follows by integrating C3+3C2^2 r over [0,t]
after bounding exp(t+2r) by exp(3t). This argument only uses the
positive L1/sup evolution domination, so it is unchanged by the
fractional diffusion.

Write Pi w=integral_X w and define

    A_1(v)=e^(-1) Pi S_1(v),       F(v)=A_1(v)-Pi v.

At zero, D S_1(0)=e P_1, so D F(0)=0 because P_1 preserves mass.
Oddness gives F(-v)=-F(v) and D^2 F(0)=0. By (5.3),

    |D^3 A_1(v)[v_1,v_2,h]|
        <=B_D||v_1||inf||v_2||inf||h||1.                 (5.4)

Apply Taylor's integral formula to D F on the segment from zero to v:

    |D F(v)[h]|<=(B_D/2)||v||inf^2||h||1.              (5.5)

Only strictly interior unit-ball segments will be used. In particular
no cubic constant is substituted for the degree-dependent B_D.

## 6. The complete two-slice prior is fixed before the algorithm

Fix once and for all a public nonzero bump

    psi in C_c^infinity((0,1)^d),       0<=psi<=1,
    I=integral psi>0,
    D_psi=max(1,max_(|alpha|<=s)||partial^alpha psi||inf),
    a_bump=1/(8D_psi).

For example a tensor product of smooth flat bumps supported in
[1/4,3/4] gives such a choice. In particular I<=1 and a_bump<=1/8.
These are fixed mathematical constants, not unknown input information.

Given a horizon T sufficiently large for the thresholds below, put

    R_T=(a_bump I e^T)^(1/q),
    k=2 floor(R_T/2),       K=k^d,
    A=a_bump k^(-s),        ell=2 ceil(sqrt(K)/2),
    m=A I ell/K.                                         (6.1)

Partition the torus into the K half-open grid cubes C_i of side 1/k.
In cube i put the rescaled bump psi_i(x)=psi(kx-i), extended by zero.
The flat supports make all these extensions smooth and disjoint.

For each sign vector xi in {-1,1}^K define

    v_xi(x)=A sum_i xi_i psi_i(x).                        (6.2)

All derivatives of order at most s are bounded by 1/8, because
A k^|alpha| D_psi<=1/8, and the sup norm is at most 1/8.
For K>=2048 the two sign slices

    Omega_+={xi:sum_i xi_i=ell},
    Omega_-={xi:sum_i xi_i=-ell}                         (6.3)

are nonempty and contain both signs. Every input in either slice is
therefore in exactly V. Its mean is respectively +m or -m.

The prior first chooses the slice sign with probability 1/2 and then
chooses uniformly from the ENTIRE selected slice. It depends only on T
and public fixed parameters, not on the algorithm or seed. In particular
it will never be conditioned on a favorable PDE event.

For R_T>=4 and K>=2048,

    R_T/2<=k<=R_T,
    sqrt(K)<=ell<=2sqrt(K)<=K/4,
    1<=e^T m<=2^(q+1),
    A/sqrt(K)<=2^q I^(-1)e^(-T),
    log K<=gamma T.                                     (6.4)

For example m=(a_bump I) k^(-q)[ell/sqrt(K)], which proves
the middle two estimates. The last uses a_bump I<=1.
Parity is exact: k and K are even, and ell is even.

Analytical observables below are also defined on the complete sign
cube, including its constant-sign vectors. Such vectors are used only
to prove symmetry and bounded differences of the PDE observables.
The algorithm is required to work only on its promised class V.

## 7. A finite-slice concentration lemma, proved on the full prior

Let H be a real function on {-1,1}^K, odd under simultaneous sign
reversal, and suppose changing one sign changes H by at most L.

Start with a uniform balanced vector, whose H expectation is zero by
oddness. Choose uniformly ell/2 of its negative coordinates and flip
them. The result is uniform on Omega_+: coordinate permutation symmetry
makes every vector of that slice equally likely. At most ell/2 flips
were made, hence

    |E_(Omega_+) H|<=ell L/2,
    |E_(Omega_-) H|<=ell L/2.                            (7.1)

This requires no invariance of H under spatial permutations.

Reveal the K coordinates in any fixed order within either full slice.
If both possible next signs are feasible, uniformly couple their
completions by swapping that next coordinate with one opposite sign
among the remaining coordinates. The two full vectors differ in at
most two signs. Thus the conditional expectations after the two
possible next values differ by at most 2L. Forced signs give zero
martingale increments.

Each Doob increment has conditional range of length at most 2L, hence
conditional variance at most L^2 and, by the elementary bounded-variable
exponential estimate, conditional moment generating function at most
exp(theta^2 L^2/2). Martingale orthogonality and iteration yield

    Var_(Omega_+/-) H<=K L^2,
    P_(Omega_+/-)(|H-EH|>z)
        <=2exp[-z^2/(2K L^2)].                          (7.2)

For completeness, the exponential estimate for a centered variable in
an interval of length b is exp(theta^2 b^2/8): convexity reduces the
exponential to the two endpoints, and the logarithm of that two-point
moment generating function has second derivative at most b^2/4.
Integrate twice from zero. Exponential Markov inequality and optimization
then prove the tail estimate in (7.2). No product-sign independence
has been introduced.

## 8. Actual time-one mean and profile concentration

A single sign flip in (6.2) has L1 size 2A I/K. Every intermediate
coefficient vector has sup norm at most A. Equation (5.5) therefore gives

    |F(v_xi)-F(v_xi')|
       <=B_D A^3 I/K<=B_D A^3/K.

The function xi->F(v_xi) is odd on the complete cube. With the convenient
larger flip constant L_F=B_D A^3/K, (7.1)-(7.2) give, on each full slice,

    |E F|<=B_D A^3 ell/(2K),
    Var F<=B_D^2 A^6/K.                                  (8.1)

If

    A^2<=I/(64 B_D),                                    (8.2)

then |E F|<=m/128. If |F|>m/4 its centered deviation exceeds m/8.
Since ell^2>=K, Chebyshev gives

    P(|F|>m/4)
      <=64 B_D^2 A^4/I^2<=1/64.                        (8.3)

On the positive slice's mean-good event, the actual time-one mean is

    b_1=Pi S_1(v_xi)=e(m+F(v_xi))>=3e m/4.              (8.4)

The negative counterpart follows by oddness.

For the whole profile, fix x. Equations (3.8)-(3.9) imply the one-flip
bound

    |S_1(v_xi)(x)-S_1(v_xi')(x)|
       <=2e rho A I/K<=C_cell A/K,
    C_cell=2e rho.                                      (8.5)

The pointwise observable is odd on the full cube. Its slice expectation
has magnitude at most C_cell A/sqrt(K), by (7.1) and (6.4).

Use the deterministic torus grid with

    N_K=ceil(sqrt(d) G sqrt(K)),       M_K=N_K^d,
    C_net=(1+sqrt(d)G)^d.

Then M_K<=C_net K^(d/2). Every point is within Euclidean distance
sqrt(d)/(2N_K) of a grid point. By (4.10), interpolation from that
point contributes at most A/(2sqrt(K)).

At any grid point the choice

    z_K=C_cell A/sqrt(K) * sqrt(2 log(128 M_K))

makes the tail in (7.2) at most 1/(64 M_K). A union bound over all
M_K grid points therefore proves, with probability at least 63/64
on EACH full slice,

    ||S_1(v_xi)||inf
       <=A/sqrt(K)
          [C_cell+1/2+C_cell sqrt(2 log(128 M_K))].       (8.6)

There is no random grid or maximum-over-space expectation shortcut.
Define the fixed constants

    b_net=log(128 C_net)/log 2+d/2,
    H_net=(C_cell+1/2)/sqrt(log 2)+C_cell sqrt(2 b_net),
    C0=(2^q H_net/I) sqrt(gamma).                        (8.7)

For K>=2, log(128 M_K)<=b_net log K. Thus (6.4) and (8.6) give

    ||S_1(v_xi)||inf<=C0 e^(-T) sqrt(T).                 (8.8)

In particular, writing w_1=(Id-Pi)S_1(v_xi), normalized volume and
orthogonal projection imply

    W_1:=||w_1||2<=||S_1(v_xi)||2
                         <=C0 e^(-T) sqrt(T).           (8.9)

There is no unnecessary factor two in (8.9).

Combining (8.3) and (8.8), the actual time-one mean and profile
properties hold together with probability at least 31/32 on EACH
original slice. Denote this analytical event by Good. The prior and
every later information calculation remain the complete uniform slices.

## 9. Fractional centered energy and scalar-mean error

The lower-bound inputs are smooth. The actual flow is sufficiently
regular for the energy calculation at every time at least one. One
direct justification from the accepted fixed-time result is to repeat
(4.5)-(4.8) at any fixed higher r and time 1/2. Restarting at a state
of sup norm below one gives uniform high-Sobolev bounds for times
at least 1/2. The mild Fourier coefficients satisfy their scalar
differential equations. Taking r sufficiently large makes the
fractional energy sums and their differentiated pairings summable.
More explicitly, write the energy identity for finitely many Fourier
modes, integrate it over a finite time interval, and pass to the limit.
The high-Sobolev bound controls the energy tails uniformly in time.
For r>d/2, weighted Fourier convolution and the summability of the
inverse weight give the H^r product bound, so the polynomial reaction
has the same high-Sobolev regularity and its pairings also converge.
This gives the integrated identity and hence its almost-everywhere
differential form, which suffices for Gronwall. It justifies the
identities below for the actual solution without spatial analyticity.

For a fixed good input, shift the time origin by one and put

    u(t)=S_(1+t)(v_xi),       b(t)=Pi u(t),
    w(t)=u(t)-b(t),          b(0)=b_1,
    lambda=c(4*pi^2)^beta>0.                             (9.1)

The constant lambda is the first nonzero spectral decay rate, not the
branching rate. Mass preservation gives

    b'=b-Pi(u^D).

Since z->z^D is increasing on all real numbers,

    integral w(u^D-b^D)>=0.

The zero-mean fractional Poincare inequality follows directly from
the Fourier multipliers:

    c||(-Delta)^(beta/2)w||2^2>=lambda||w||2^2.

Consequently the exact centered energy identity and its estimate are

    (1/2)d/dt ||w||2^2
       =-c||(-Delta)^(beta/2)w||2^2
                    +||w||2^2-integral w(u^D-b^D)
       <=(1-lambda)||w||2^2,

    ||w(t)||2<=e^((1-lambda)t) W_1.                     (9.2)

For lambda<1 this allows growth; the proof does not assume all
nonconstant linear modes are stable.

Set

    C_R=D(D-1)/2,
    R(t)=Pi(u(t)^D)-b(t)^D.

Taylor expansion of z^D about b(t), with |u|,|b|<=1 and Pi w=0,
gives the exact bound

    |R(t)|<=C_R||w(t)||2^2.                              (9.3)

Let z(t)=phi_t(b_1). Then b'=f(b)-R and z'=f(z).
The one-sided bound f'<=1, or its scalar secant variation formula,
gives

    |b(t)-z(t)|
       <=C_R e^t W_1^2 J_lambda(t),
    J_lambda(t)=integral_0^t exp((1-2lambda)r)dr.         (9.4)

The integral is t at lambda=1/2 and otherwise
[exp((1-2lambda)t)-1]/(1-2lambda). No denominator singularity is
used in a bound. With mu=min(1,2lambda), (8.9) gives at t=T-1,

    |b(T-1)-phi_(T-1)(b_1)|
       <=C_R C0^2 T^2 exp(-mu T).                       (9.5)

Indeed J_lambda(T-1)<=T exp((1-2lambda)_+ T), while
e^(T-1)W_1^2<=C0^2 T exp(-T). This proves decay for every positive
lambda, including the resonant value 1/2.

## 10. Final-unit spatial error and finite threshold

Let t>=1 and compare the actual u(t)=S_1u(t-1) with the constant
phi_1(b(t-1)). Equations (3.8)-(3.9) give

    ||u(t)-phi_1(b(t-1))||inf
       <=e rho||w(t-1)||2.

The distance from the mean b(t) to the same constant is bounded by
the same supremum. Thus

    ||w(t)||inf<=2e rho||w(t-1)||2.                       (10.1)

For T>=2, (9.2) and (8.9) give

    ||w(T-1)||inf<=C_w sqrt(T) exp(-lambda T),
    C_w=2e rho C0 exp(2(lambda-1)).                      (10.2)

This uses the kernel over a full final unit of chronological time.
It does not integrate a singular short-edge derivative.

Here is one explicit finite threshold containing every earlier condition:

    k_star=ceil(max(4,2048^(1/d),
                      (64 B_D a_bump^2/I)^(1/(2s)))),
    T_grid=q log(2k_star)-log(a_bump I),
    mu=min(1,2lambda),
    T_mean=(2/mu)max(0,log(512 C_R C0^2/mu^2)),
    T_space=(2/lambda)max(0,log(64 C_w/sqrt(lambda))),
    T0=max(2,T_grid,T_mean,T_space).                    (10.3)

All logarithms have positive arguments. For T>=T_grid,
R_T>=2k_star, hence k>=k_star, K>=2048, R_T>=4, and (8.2) holds.
This controls all real horizons, including the jumps in the even k.

For T>=0,

    T^2 exp(-mu T)<=8mu^(-2)exp(-mu T/2),
    sqrt(T) exp(-lambda T)<=lambda^(-1/2)exp(-lambda T/2).

The first follows from the quadratic term of exp(mu T/2);
the second from exp(lambda T)>=lambda T. Therefore at T>=T0,

    |b(T-1)-phi_(T-1)(b_1)|<=1/64,
    ||w(T-1)||inf<=1/64.                                (10.4)

If a logarithm in (10.3) is nonpositive, the corresponding prefactor
already meets the desired bound at zero, which explains its maximum
with zero. Every constant is finite for all fixed allowed parameters.
No comparison between lambda and one is needed.

## 11. Uniform target separation on the unconditioned good events

On the positive slice's good event, (8.4) and (6.4) imply

    e^(T-1)b_1>=3/4.

For a>=0, the scalar formula (3.10) gives, with y=e^t a,

    phi_t(a)>=Psi_p(y),
    Psi_p(y)=y/(1+y^(2p))^(1/(2p)).

The function Psi_p is increasing. For integer p>=1,
(1+y^2)^p>=1+y^(2p); hence

    Psi_p(3/4)>=Psi_1(3/4)=3/5.                         (11.1)

Combining this with (10.4) yields for every x in X,

    S_T(v_xi)(x)>=3/5-1/64-1/64=91/160>1/2            (Omega_+, Good),
    S_T(v_xi)(x)<=-91/160<-1/2                        (Omega_-, Good). (11.2)

The second statement follows by oddness. On each COMPLETE uniform
slice the appropriate Good event has probability at least 31/32.

This concerns the actual nonlinear fractional PDE at the prescribed
horizon, rather than just its mean, linearization, or scalar comparison
trajectory. The probability estimates in Sections 7-8 establish a
high-probability property of the original prior; they do not replace
that prior with a conditional law.

## 12. Reduction from scalar acquisitions to a stronger sign oracle

Fix any algorithm satisfying the point risk (1.3), at this T.
Classify its output as positive when Z_T>=0 and negative otherwise.
On each fixed good prior input, a wrong label entails point error at
least 1/2 by (11.2). The mean-square guarantee therefore bounds its
wrong-label probability over the private seed by 1/4. On bad prior
inputs bound it by one. On the original equal mixture of full slices,

    BayesError_original<=1/4+1/32=9/32.                 (12.1)

This uses only mean-square risk, not unbiasedness or a tail promise.
The sharper fraction is unnecessary.

Now give the algorithm a stronger oracle: at every query x reveal
the sign xi_i of the unique half-open grid cube containing x.
The actual scalar value is then exactly
A xi_i psi(kx-i), with periodic coordinates understood. A support gap,
boundary, or zero value creates no difficulty: the simulator can still
supply the actual scalar answer, and the extra sign only makes the
stronger oracle more informative. Every original acquisition is
charged even if the cell has been seen before.

Conditioned on any previous distinct revealed cell signs, all as-yet
unseen labels are exchangeable under each full slice. If j distinct
cells were revealed and z of their signs are positive, then at any
new cell the next positive-sign probabilities are

    p_+(j,z)=[(K+ell)/2-z]/(K-j),
    p_-(j,z)=[(K-ell)/2-z]/(K-j).                         (12.2)

These formulas do not depend on which unseen label is selected.
This is exactly the exchangeability that would be lost by conditioning
the prior on Good.

Take

    n_cap=floor(K/1024).

Consider any process that uses at most n_cap original acquisitions.
Whenever it halts or aborts, pad its distinct sign reveals with unused
labels, chosen for example in increasing order, until there are exactly
n_cap distinct reveals. The decision ignores padding. Repeated queries
are reconstructed from the earlier signs and count toward the original
cap, so they never create additional letters in this padded word.

Every binary prefix up to this length is feasible under both slices:
each slice has at least (K-ell)/2>=3K/8 signs of either needed type,
whereas n_cap<=K/1024. Thus (12.2) is always defined with probabilities
strictly between zero and one.

## 13. Finite-word KL bound, including arbitrary private seeds

First fix a deterministic seed and consider any such padded adaptive
selection rule. Its next previously unseen sign always has the law
(12.2). Hence the law W_+ or W_- of the length-n_cap sign word is the
same fixed finite urn law for every selection rule and fixed seed.

For 0<=j<n_cap, using j<=K/8 and ell<=K/4 gives

    1/4<=p_-(j,z)<=4/7,
    p_+(j,z)-p_-(j,z)=ell/(K-j)<=2ell/K.                  (13.1)

For Bernoulli parameters a,b in (0,1), log x<=x-1 implies

    KL(Ber(a)||Ber(b))<=(a-b)^2/[b(1-b)].

On the interval in (13.1), b(1-b)>=3/16. Consequently each one-step
conditional divergence is at most

    64 ell^2/(3K^2)<=256/(3K).                          (13.2)

The chain rule here is just expansion of the two finite positive
word probabilities into their conditional factors. It gives

    KL(W_+||W_-)<=n_cap*256/(3K)<=1/12.                  (13.3)

The finite Pinsker estimate follows directly as well: group the finite
atoms into the set where W_+ exceeds W_- and its complement, apply
the log-sum inequality, and use
d^2/da^2 KL(Ber(a)||Ber(b))=1/[a(1-a)]>=4.
This proves KL>=2TV^2. Thus

    TV(W_+,W_-)<=sqrt(1/24)<1/4.                        (13.4)

Under equal priors, any measurable decision based on this word has
error at least (1-TV)/2>=3/8.

The arbitrary seed causes no hidden regular-conditional-probability
assumption. Let its law be R on its given measurable space. The prior
contains finitely many actual promised inputs. For each input the
algorithm halts outside a seed null set; remove the finite union of
these null sets. The resulting seed set has full R measure and the
original algorithm halts on every prior input for each such seed.

For a fixed seed in this set, the next fresh-label choice, repeated
queries, locations, original scalar answers, stopping decision, and
padding are deterministic functions of the finite revealed signs.
Every possible capped prefix extends to a promised prior input, so
this simulation is well defined. The word law is the same W_+ or W_-
just computed, independently of that fixed seed. Since the input prior
is finite, finite summation and measurability identify the joint laws
of the seed and padded word as

    R times W_+,       R times W_-.

This assertion is a direct finite calculation for each fixed seed;
it does not disintegrate an arbitrary measurable seed space. Changing
the process on the removed null set has no effect. Total variation
of these product laws equals TV(W_+,W_-): the inequality follows by
finite summation and the reverse inequality by a word-only event.

The capped decision is a measurable function of this seed-word pair,
so (13.4) still yields

    BayesError_capped>=3/8.                              (13.5)

The argument permits arbitrary measurable internal computation and
seed distribution. Nothing restricts the algorithm to finite-support
randomness or deterministic query locations.

## 14. Almost-sure stopping and expected-query lower bound

Let q_bar be the average, under the original complete prior, of the
algorithm's expected number of acquisitions. If it is infinite, the
worst-input lower bound is already true because the prior is finite.

Otherwise simulate the original algorithm but stop it immediately
before it would make acquisition n_cap+1. At this cap output an
arbitrary fixed label. If the original algorithm halts without
attempting that acquisition, use its original decision. Follow with
the harmless distinct-label padding of Section 12.

The capped and original labels can differ only on {N>n_cap}.
By Markov's inequality under the full prior and seed law,

    P(N>n_cap)<=q_bar/n_cap.

Combining (12.1) and (13.5),

    3/8<=9/32+q_bar/n_cap,
    q_bar>=3 n_cap/32>=3K/65536,                         (14.1)

where K>=2048 gives floor(K/1024)>=K/2048. This truncation uses the
total original query count, including repeated and zero answers.
Almost-sure stopping, rather than a deterministic query cap, is enough.

The prior average is no larger than the worst-input expected count.
By (6.4),

    K>=2^(-d)(a_bump I)^gamma exp(gamma T).

One explicit lower constant is therefore

    C_lower=3*2^(-d-16)(a_bump I)^gamma>0.                (14.2)

Equations (14.1)-(14.2) prove (1.5) for every real T>=T0.
The constant displayed in (14.2) need not depend on beta,c,p;
the threshold T0 does depend on them, potentially very strongly.

For a profile output satisfying (1.4), evaluate its finite Fourier
polynomial at x*. This costs no initial-value acquisitions and is a
measurable scalar estimator with point risk at most the profile risk.
The point lower bound therefore proves the strong-profile lower bound.
No assumption that pointwise and profile Monte Carlo risks coincide is
used. In a paid-work model, charging each query immediately gives the
same exponential lower bound, with no claim about its sharp prefactor.

## 15. Checks, limitations, and research provenance

The proof closes the proposed lower route with these precise bridges:

- The actual isotropic fractional semigroup is positive and mass
  preserving, has the required L1/sup comparison, and has a finite
  bounded kernel over a full final unit. Its bound uses full-time
  stable inverse moments, not independently sampled coordinate clocks.
- D47's complete nonlinear field at r=d+2 and integer moment exponent
  P=2d+2 gives a uniform input-derivative bound. Integrating D S_1(tv)[v]
  gives a spatial gradient bound proportional to ||v||inf. No spatial
  analytic radius is asserted, including when beta<1/2.
- The mixed-L1 degree-dependent B_D, original uniform slices, spatial
  net concentration, and actual fractional energy give simultaneous
  mean and spatial errors at most 1/64 beyond the explicit finite T0.
  The resulting all-space target separation is exactly 91/160.
- The finite-word calculation, arbitrary-seed product law, padding,
  and truncation prove the lower bound for biased adaptive procedures
  with inputwise almost-sure halting and worst-input expected cost.

The constants have been displayed rather than optimized. Their
dependence becomes poor near beta=0 or c=0 and as the fixed degree
or dimension increases. The theorem is for the normalized reaction
and original class/tolerance; no unscaled physical-coefficient transfer
is asserted. It concerns a selected horizon, not simultaneous accuracy
at all horizons. The promised input class has not been narrowed.

At beta=1 the generator becomes c Delta, agreeing with D45 after
kappa=2c; our larger intermediate constants remain valid. Positivity
of c is essential for the conclusion stated uniformly at large T.
If c=0, one exact query v(x*) and the scalar formula (3.10) return the
exact point target at any horizon, contradicting an exponential point
lower bound. This excluded boundary case also explains why T0 cannot
be claimed uniform down to zero diffusion.

The classical components are subordination, positive-semigroup
comparison, mixed variation estimates, finite-slice concentration,
fractional spectral energy, and elementary information inequalities.
The new artifact is their audited candidate composition for this
specific lower-bound question; it does not establish publication
priority or significance.

Status: complete conventional lower-proof candidate, pending independent
review and root acceptance. Existing Lean statements are not premises
certifying the full PDE composition. This task ran only file reads,
working-tree inspection, SHA256 checks, and review-file edits. It ran
no research code, experiments, numerical or symbolic evaluations,
input acquisitions, sampler realizations, Lean commands, or T101 work.
The accepted frozen sources, root ledgers, and all implementation files
were left unchanged by this worker.
