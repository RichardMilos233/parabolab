# T84: independent audit of the all-positive-diffusivity work upper bound

Date: 2026-09-29. Conventional mathematical review only.

**Verdict: PASS for frozen T81 in its stated ideal operation model.**
For every fixed `kappa>0` and fixed integers `d,s>=1`, the construction
has the claimed uniform RMS bound and expected-work exponential rate on
the entire stated signed class. The proof includes the critical value
`2*pi^2*kappa=1` and the regime below it. I found no material repair
necessary. The detailed checks below independently justify the inherited
solver adaptation, the new saturation interface, the unconditional risk
bound, and the all-seed acquisition cap.

Section 10a also verifies a stronger corollary already implicit in the
frozen construction: it may return the whole indexed Fourier profile,
with the same RMS tolerance in spatial sup norm and the same work rate.

The audited source is the complete 857-line
`reviews/T81-fixed-burnin-all-diffusion-upper-proof.md`, SHA256

    d9b249ed669897df319ca712fc4ad26625fc97e1a9b32b79eacaf497b290bae5

This review does not accept a lower bound for the enlarged diffusion
scope, exact query order without a polynomial factor, a finite-bit
algorithm, practical efficiency, numerical evidence, a full Lean
theorem, or novelty. T82/T83 are separate work. Root source/model
correspondence remains necessary before changing an accepted ledger.
Only this new T84 file was written by this reviewer.

## 1. Exact statement, dependencies, and scope of inspection

The equation, torus, and unknown-data class are

    u_t=(kappa/2) Delta u+u-u^3,       X=R^d/Z^d,
    V={v in C^infinity(X): ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

Only exact initial point values of `v` are supplied. For fixed `x*`,
T81 constructs Borel almost-surely halting algorithms such that, for
every real `T>=2`,

    sup_(v in V) ||Y_T(v)-S_T^kappa v(x*)||L2 <=1/8,
    sup_(v in V) E Work_T(v)<=C exp(gamma T)(1+T)^A,
    gamma=d/(s+d/2)=2d/(2s+d).

The deterministic acquisition cap is T81 (9.2), including null seeds
on which a preparation fails to terminate. Constants can depend on
fixed `d,s,kappa`; there is no uniformity as `kappa` tends to zero.
Section 13 below checks the optional bounded-time completion.

The operation model matches 04w/D33: every acquisition, scalar
arithmetic operation, comparison, floor/ceiling, integer/index/modular
operation, stored-value access, and listed elementary function is
charged. The elementary functions are `exp,log,sin,cos` and positive
square root. Exact uniform, exponential-clock and Gaussian draws with
known parameters are charged random primitives. Complex arithmetic
uses a fixed number of real operations. Fixed public constants,
unbounded exact real magnitudes, and ideal integer/address words are
part of this model. A transform, derivative, evolved-value evaluator,
integration routine, or arbitrary known-function evaluator is not an
additional primitive.

The following hashes were computed from the actual source files.

| Source in this run | SHA256 |
| --- | --- |
| `reviews/T81-fixed-burnin-all-diffusion-upper-proof.md` | `d9b249ed669897df319ca712fc4ad26625fc97e1a9b32b79eacaf497b290bae5` |
| `reviews/T70-known-base-phase-work-feasibility.md` | `46666ef19d4d66eb6196c486df726b6cc623f401fb717d925c82806bd3a905d6` |
| `reviews/T74-known-base-phase-work-independent-audit.md` | `0cc8fea39eeee5f1f43f21fa3d29a52525f26fed767ff0e7b1677c1fc8d2dd1c` |
| `reviews/R10b-finite-burnin-derivative-sampling.md` | `23683587539ef2905e0679100325808ae3f6353a3782a4bb362b2d24252034f0` |
| `reviews/T68-finite-burnin-sampler-independent-audit.md` | `442b446ae523b220e34ddadcf8c23b181ce60104100fd27c7e8027524840ed9f` |
| `04w-signed-ideal-work-exponential-rate.md` | `7eb75d72f0185a75f5823e9fb5175b9033e92a408d89ea268653c4d798f96a79` |

I read all six files, including the essential solver proof in T70
Sections 2--7 and T74 Sections 3--9, the explicit C2/C3 panels and
recurrence, and the C4 indexed-array/totality explanations. The older
graph-specific parts were read for dependency separation; no stable
graph or phase result from them is a premise here. R10b/T68's actual
tree, differentiation, moments, and work arguments were checked rather
than accepted from their verdict labels.

I also inspected the supplied repository instructions, repository and
research README passages, run context and current checkpoint, and
D29--D36 claim passages. In particular, 04w/D33 remains at `kappa=1`,
whereas D36 has the natural-gap lower-bound scope. Neither statement
is silently expanded by this audit. I read the math-auto-research
skill, defaults, general profile, routing, and execution instructions.
No inaccessible earlier session is claimed to have been inspected.

## 2. Paid interpolation: finite smoothness and actual lookup work

T81 uses the explicit T70/T74 interpolant, which is an allowed choice
of the known approximation formula. It adds no regularity assumption
to `v`.

For `beta(t)=exp(-1/(1-t^2))` inside `(-1,1)`, extended by zero,
the Cauchy estimate for `exp(-1/z)` on a disk of radius proportional
to a positive real argument gives derivative bounds of order
`A C^r(r!)^2`. Composition with the fixed quadratic preserves this
Gevrey order; all endpoint derivatives vanish. Its normalized
integer-translate denominator is at least

    beta(1/2)=exp(-4/3).

There are at most two nonzero translates in one coordinate. A
reciprocal derivative induction, using the normalized coefficients
`1/binom(r,l)`, gives the same Gevrey order for the reciprocal of
this positive denominator. Tensor products produce a smooth periodic
partition with a fixed overlap count.

Each fixed tensor stencil of degree `s-1` reproduces every polynomial
of total degree at most `s-1`. At a point `x`, compare every relevant
stencil to the total-degree Taylor polynomial of `v` about `x`, in
consistent local torus lifts. All relevant nodes are at distance
`O_(d,s)(1/k)`, so their Taylor remainders are `O(k^-s)` using only
the promised total-order derivatives through `s`. Fixed scaled
cardinal bounds and the partition identity then give

    ||v-g||inf<=Cint k^-s.

This argument works when `s=1` and does not require tensor mixed
derivatives of total order larger than `s`. Bounded stencil
coefficients, fixed degree, and the scaled Gevrey weights also give

    ||partial^alpha g||inf
       <=B0(C0 k)^|alpha|(alpha!)^2.

For a fixed sufficiently small `c>0`, summing these bounds proves a
uniform `G_(c/k)` norm bound. Increasing `k0>=2s` makes
`Cint k0^-s<=1/4`, so `||g||inf<=3/4` on every promised transcript.
Both `g` and `e=v-g` are continuous, as required by R10b's genuine
`C(X)` derivative statement.

There are `O_(d,s)(1)` stored coefficients per grid node. Fixed
stencil matrices construct them in `O(k^d)` operations from exactly
`k^d` paid values. Floors and periodic indices locate only a fixed
number of local records at any later point. Their polynomials and
bumps use a fixed number of the listed primitives. Support tests
precede the bump divisions, and the translate denominator never
vanishes. Thus `Gg<=C_(d,s)` is an actual program-cost bound. Reusing
saved values pays arithmetic and memory accesses without acquiring
new information about `v`.

## 3. Actual PDE smoothing for fixed positive diffusivity

The norm

    ||f||_(G_rho)=sum_alpha rho^|alpha|
                               ||partial^alpha f||inf/(alpha!)^2

is a Banach-algebra norm. The multi-index product coefficient after
normalization is `1/binom(alpha,beta)<=1`; summing proves the product
bound. Uniform convergence of derivatives proves completeness. Real
heat convolution for `kappa>0` contracts every derivative sup norm,
and dominated convergence in the derivative sum gives strong
continuity. Hence the cubic mild map on a fixed radius-`2B` ball
gives a time `h0>0`, independent of `R`, with

    ||S_t^kappa q||_(G_(c/R))<=2B,       0<=t<=h0.

Integration by parts in a coordinate of maximum Fourier frequency
and the choice `r` proportional to `sqrt(|n|inf/R)` imply a
coefficient bound `C exp(-c1 sqrt(|n|inf/R))`. Summing shells, with
the substitution `y=sqrt(j/R)`, gives

    sum_(|n|inf>H)|uhat(t,n)|
       <=C R^d exp(-c2 sqrt(H/R)),       0<=t<=h0.

The late-time analytic bound is derived from the actual real PDE.
Comparison with the equilibria `+/-1` first gives `||u(t)||inf<=1`.
For the periodized heat kernel at time `t>0`, an imaginary shift by
`y` has kernel `L1` bound

    exp(|y|^2/(2 kappa t)).

In the tube `|Im z|_2<a sqrt(kappa t)`, shifting the convolution
contour at time `r` to `y_r=sqrt(r/t)y` leaves displacement at most
`a sqrt(kappa(t-r))`. Thus the heat map between these tubes has norm
at most `Kheat=exp(a^2/2)`. Periodicity cancels the contour faces;
successive coordinate shifts stay inside the tube. At `r=0` the
contour is real.

Take a fixed radius `Rball=2Kheat` and `h1>0` so small that

    Kheat+h1 Kheat(Rball+Rball^3)<=Rball,
    h1 Kheat(1+3Rball^2)<1,
    h1<=min(h0,1).

These explicit inequalities make the complex-space mild map invariant
and contractive. Its iterates and limit are holomorphic at positive
times; the uniform bounds justify the Duhamel integrals at zero.
Real mild uniqueness identifies the real restriction with the actual
solution. Restarting from `u(t-h1)`, which is still bounded by one,
gives the same positive strip width `a sqrt(kappa h1)` for every
`t>=h1`. A smaller fixed strip and Fourier contour shifting yield

    sum_(|n|inf>H)|uhat(t,n)|<=C_kappa exp(-c_kappa H).

Together these are exactly the two uniform tails needed on `[0,S]`.
The strip is allowed to shrink as `kappa` decreases. The proof uses
neither a spectral gap nor convergence to a constant. In particular
it remains valid when additional linearized modes grow.

## 4. Galerkin bootstrap, initialization, and exact spatial operations

The rectangular Fourier projector has

    ||P_H||_(inf->inf)<=Lambda_H=C_d(1+log(H+1))^d,

by the one-dimensional Dirichlet-kernel `L1` bound and tensorization.
It is not assumed to be a contraction. Let `U` solve the Galerkin
ODE with initialization error `epsilon0` relative to `P_Hq`. Until
`||U||inf` reaches two, the real cubic has Lipschitz constant at most
11 on the relevant interval. Comparing `U` to `P_Hu`, adding the
true projection tail, and using real heat contraction gives

    D(t)<=epsilon0+t_H+11 Lambda_H integral_0^t D(r) dr,
    D(t)=||U(t)-u(t)||inf.

Thus `D(t)<=(epsilon0+t_H)exp(11 Lambda_H t)`. Making this at most
`min(1/4,exp(-P)/4)` keeps `||U||inf<=5/4`. The real bootstrap
closes, and bounded finite-dimensional coefficients prevent finite
ODE blowup on the requested interval.

For `E=1+P+S+log(R+1)` and

    H=ceil(C_kappa R E^(2d+8)),

one has `log(H+1)<=C_kappa E`, `Lambda_H<=C_kappa E^d`, and
`sqrt(H/R)` of order `sqrt(C_kappa) E^(d+4)`. This dominates
`log R+P+11 Lambda_H S` after increasing the fixed constant. The
analytic tail is absorbed as well. Constants appearing inside
`log H` grow only logarithmically with that chosen cutoff constant,
so this choice is not circular.

Initialization uses actual known-profile evaluations on a power-of-two
grid `Q>=4H`, followed by its tensor FFT. For retained `n`, the alias
error is `sum_(ell!=0) qhat(n+Q ell)`. Retained frequencies have
distinct residues; every extra frequency has norm at least `Q-H`.
Hence their aggregate coefficient `l1` error is bounded by a single
Fourier tail, with no extra factor counting retained modes. The
early Gevrey estimate covers this error at time zero.

A polynomial in the `H` box has cubic support in the `3H` box. A
power-of-two grid strictly larger than `6H` represents that cubic
without aliasing. Forward/inverse transforms, pointwise cubing, and
restriction therefore compute the actual projected cubic in exact
arithmetic. Radix-two butterflies, generated trigonometric twiddles,
padding, and all array operations cost `O_d(H^d log(H+1))`. The
cutoff is also a public finite integer. These are concrete operations,
not a supplied transform or PDE oracle.

Real initial grid values give conjugate-symmetric Fourier arrays.
Real scalar heat factors, cubic evaluation, and the real time weights
preserve that symmetry. Thus all real-time polynomials used in the
real bootstraps and the returned profile are genuinely real valued.

## 5. Time analyticity and collocation: both bootstraps pass

For a complex time in a fixed forward sector, integration of the
absolute complex Gaussian gives

    ||exp(z kappa Delta/2)||_(inf->inf)
       <=(sec(arg z))^(d/2).

The positive factor `kappa` cancels from this bound. On a fixed complex
norm ball containing the bounded real Galerkin starts, the nonlinear
Lipschitz constant is `C_d Lambda_H`. Radial mild Picard iteration
therefore gives a bounded holomorphic sector of radius
`rho_H=c_d/Lambda_H`, restarted from each real time. These restarts
are analytic estimates on the exact trajectory; the algorithm never
acquires its exact values at restart bases.

At zero, a separate disk is necessary. For a Fourier polynomial,

    ||(kappa/2)Delta f||inf
       <=sum_(|n|inf<=H) 2*pi^2*kappa*|n|^2 |fhat(n)|
       <=C_d kappa H^(d+2)||f||inf.

Finite-dimensional complex ODE contraction then gives the genuine
disk of radius `a_H=c_d/(C_d kappa H^(d+2)+Lambda_H)`. Its logarithmic
reciprocal is `O_kappa(1+log(H+1))`. An initial disk independent of
the highest frequency is neither assumed nor needed.

Here is the concrete T74 C2 panel construction with this `a_H`.
Take sector angle `pi/4`, ellipse parameter two,
`p=ceil(C_kappa E^(d+4))`, `beta_p=C(1+log(p+1))>=1`, and

    h=c/(Lambda_H beta_p),
    a=min(a_H/16,h/16).

Choose `c` so `h<=min(1/100,rho_H/100)` and
`49h Lambda_H beta_p<=1/4`. The ellipse of `[0,a]` lies inside
the initial disk. The parameter-two ellipse of `[1,2]` has real
part at least `7/8`, imaginary part at most `3/8`, and modulus below
3; it lies strictly within the sector. Thus doubling panels `[t,2t]`
fit until their final endpoint `b0` first lies in `[h,2h)`.

For the remainder, use
`Jpan=ceil((S-b0)/h)` equal panels. Since `S>=1` and `h<=1/100`,
their lengths lie in `[h/2,h]`. For a panel beginning at `b`, base
the sector at `b-h>=0`; its relative ellipse lies within the same
scaled bounds. This proves a uniform ellipse parameter on all
panels and yields

    n_pan<=C_kappa[1+log(H+1)+log(p+1)+S Lambda_H beta_p]
         <=C_kappa E^(d+2).

All lengths are positive and public. The ordinary doubling procedure
and balanced remainder give finite loop maxima; there is no tiny
uncontrolled terminal panel.

On those ellipses, the projected forcing has norm `C_d Lambda_H`.
Cauchy's estimate for Banach-valued Chebyshev coefficients, followed
by the Lobatto aliases of higher Chebyshev modes, gives forcing
interpolation error `C_d Lambda_H 2^-p`. The Lobatto Lebesgue bound
`beta_p` follows from the cardinal bounds and their harmonic sum.

On a panel of length `ell`, the semigroup-convolution nodal map is

    V_i=exp(theta_i ell A_H)U_b
      +integral_0^(theta_i ell) exp((theta_i ell-r)A_H)
          sum_j L_j(r/ell)P_H(V_j-V_j^3) dr.

On the real radius-four nodal ball and with `||U_b||inf<=2`, it has
Lipschitz constant `q_ell=49ell Lambda_H beta_p<=1/4` and image norm
at most `2+68ell Lambda_H beta_p<4`. Fixed point existence and a
fixed public `Kiter=ceil(Citer p)` Picard count are therefore proved.
The iteration error is at most `C4^-Kiter`.

Insert the exact Galerkin nodal values. If the starting error is `e`,
the endpoint error after the panel obeys

    e_next<=e/(1-q_ell)
      +C ell Lambda_H 2^-p/(1-q_ell)+C4^-Kiter.

The product of the first factors is at most
`exp(C sum ell Lambda_H beta_p)=exp(C S Lambda_H beta_p)`.
Consequently the global time error is bounded by

    exp(C S Lambda_H beta_p)
      [C S Lambda_H 2^-p+C n_pan 4^-Kiter].

Because `S Lambda_H beta_p<=C_kappa E^(d+2)`, the displayed choices
of `p,Kiter` make this at most `min(1/4,exp(-P)/4)`. Induction then
keeps numerical starts within the assumed radius two, closing the
second bootstrap. Exact arithmetic sets scalar perturbation error
to zero. Neither stiffness `exp(C kappa H^2 S)` nor an exponential
in the number of startup panels is hidden in this stability estimate.

## 6. Every time weight and solver operation is counted

For mode `n`, the eigenvalue is

    lambda_n=2*pi^2*kappa*|n|^2,
    z=lambda_n ell.

The actual nodal weight is `ell` times a linear combination of

    I_m(z,theta)=integral_0^theta exp(-z(theta-r))r^m dr.

Integration by parts gives T81's exact recurrence

    I_0=(1-exp(-z theta))/z,
    I_m=theta^m/z-(m/z)I_(m-1),       m>=1.

For every nonzero frequency, `z>0` since both `kappa` and `ell`
are positive. The zero mode uses `theta^(m+1)/(m+1)`, and the
node `theta=0` uses zero. The Lobatto nodes are distinct, so the
cardinal-polynomial denominators are nonzero. Generating nodes,
cardinal monomial coefficients, integer powers, and all moments uses
only the stated primitives and finite loops.

Put `D=(2H+1)^d`. Scalar-weight construction costs `O(Dp^3)` per
panel. Each Picard step costs `O(Dp^2+pD log(H+1))`, including one
dealiased cubic per time node. Including all panels, iterations,
initial evaluations, storage, and the terminal point evaluation gives

    C n_pan D[p^3+p^2 log(H+1)]
      +C D[log(H+1)+Wq].

The leading exponent after substitution is at most
`2d^2+12d+14` in `E`, whereas T81 permits
`a0=2d^2+20d+50`. Thus the claimed
`C R^d E^a0(1+Wq)` bound has ample room for the other operations.
The cutoff constant may depend on fixed `kappa,B,c,d`, as allowed.

Small-`z` cancellation makes these recurrences unsuitable for an
unqualified floating-point claim. It does not invalidate their exact
real operation count. This audit uses the exact model; it does not
need T70's additional guard-digit discussion to infer a bit theorem.

## 7. Fixed-time Fourier data and the genuine derivative sampler

Scalar comparison from `||v||inf<=1/2` gives

    ||S_1^kappa v||inf<=(1+3exp(-2))^-1/2<7/8.

The last inequality is equivalent to `exp(2)<49/5`, which follows
from `exp(1)<3`. Section 3's positive strip at time one gives a
uniform tail `A_kappa exp(-b_kappa N)`, independent of the unknown
datum. No initial analyticity is required for this time-one bound.

The representative convention for pairs `{n,-n}` gives one constant
and two real basis elements per nonzero pair, hence exactly
`K=(2N+1)^d` real coefficients. With the convention
`uhat(n)=integral u(x)exp(-2*pi*i*n.x)dx`, the real coefficients are

    c0=uhat(0),       c_(n,c)=2 Re uhat(n),
    c_(n,s)=-2 Im uhat(n).

Equivalently their functionals integrate against `1`, `2cos`, and
`2sin`. The factor two and the sine sign are correct. The coefficient
functional norms are at most two; `[-1,1]` and `[-2,2]` contain the
respective true target coefficients. Indexed array extraction pays
`O(K)` reads and arithmetic, without another integration oracle.

For the sampler, each rate-two ternary vertex propagates
`M(a,b,c)=(a+b+c-abc)/2`; its corner values are the majority signs.
A finite tree polynomial is multiaffine, since child leaf labels are
disjoint, and bounded by one throughout the leaf cube. The mixed
partial in `j` distinct labels is its signed `2^j`-corner average,
so its absolute value is at most one. Repeated-label partials vanish.

Brownian endpoints of covariance `kappa times edge_length` have
generator `kappa Delta/2`. The children share the branch endpoint
and use independent subsequent randomness. Their conditional means
therefore give exactly

    2(M(u,u,u)-u)=u-u^3.

The bounded renewal solution is the actual bounded mild solution by
uniqueness. This verifies the physical normalization directly.

The population generator on powers is

    A(n^r)=2n[(n+2)^r-n^r]<=2(3^r-1)n^r.

Stopping at a large population threshold and applying Gronwall gives
the moment bounds before assuming nonexplosion. The first-moment
bound makes the probability of reaching that threshold tend to zero.
Removing stopping then yields

    E N_1^r<=exp(2(3^r-1)),       E N_1=exp(4).

These population statements do not involve `kappa`.

The actual `j`th derivative is the sum over ordered injections of
direction labels into distinct leaves. Equal directions therefore
include exactly the usual `j!` multiplicity; Taylor division by
`j!` occurs later. The derivative sum has norm bounded by `N_1^j`.
One further derivative gives operator continuity with envelope
`N_1^(j+1)`, and the derivative remainder has envelope
`N_1^(j+2)||h||inf^2/2`. All are integrable. Coupling roots by
translation and dominated convergence put the expectations in
`C(X)`. Inducting on derivative order identifies genuine Frechet
derivatives of the actual flow on its open unit ball.

For a uniform root `U`, a complete marked tree, and a uniform ordered
injection `I`, the scalar residual tuple is

    Z_j=(N_1)_j C_I product_a[v(X_(I_a))-g(X_(I_a))].

It is zero if `N_1<j`. Multiplying the same sample by each
`psi_l(U)` gives the simultaneous Fourier outputs. Conditional
averaging over `I`, then the tree and root, gives the actual
`D^jF_l(g)[e^j]`. Their marginal bounds are

    E|Z_(j,l)|^2<=V_j delta^(2j),
    V_j=4exp(2(3^(2j)-1)),
    ||D^jF_l(q)||op<=B_j=2exp(2(3^j-1)).

The bounded weights justify root integration and differentiation.
Every `j` is fixed as the horizon varies.

There are `(3N_1-1)/2` tree nodes. Clocks, Gaussian increments,
positions, leaf storage, partial Fisher--Yates selection, known `g`
values, and `2^j` coefficient passes cost
`C_j(d+1+Gg)N_1`. A uniform draw and floor choose each integer;
assigning an endpoint draw to a valid last index preserves totality
without changing the distribution. Forming all weights and updating
all coefficient accumulators costs an additional `O_d(K)`. Thus
the expected vector-sample work is `C_(j,d,s)(1+K)`.

All tree, tuple, and mixed-coefficient preparation occurs before the
at-most-`j` original-value acquisitions. Repeated locations remain
charged. Sharing the sample across modes does not acquire more data.

## 8. Public parameters and coefficient risk, without mode independence

T81 chooses

    S=T-1,       Lchi=25,       epsilon=exp(-S)/(16Lchi),
    N=max(1,ceil((S+log(32Lchi A_kappa))/b_kappa)),
    K=(2N+1)^d,       qrate=s+d/2,
    J=ceil(1+d/(2s)),       m=J-1.

These are valid for every real `T>=2`; in particular `J>=2` and
`Js>=qrate`. The chosen `N` makes the actual tail at most
`epsilon/2`. With the displayed positive fixed `Cstar`, set

    eta=epsilon/(4K),
    k=max(k0,ceil((4 Cstar K/epsilon)^(1/qrate))),
    M=k^d.

Positive powers can be formed with `exp` and `log`, followed by the
charged ceiling. All sample counts and loop bounds are public finite
integers. Also `N=O_kappa(1+T)` and `log k=O_(d,s,kappa)(1+T)`.

For the base call use the actual paid `g`, `R=k`, time one and
`Pbase=log(2/eta)>1`. The known-profile lemma applies with fixed
Gevrey norm and evaluator cost. Its sup error is at most `eta/2`,
so every extracted real coefficient has error at most `eta`.
Taking its cutoff at least `N` preserves the work estimate
`C k^d(1+T)^a0`. No new original datum is queried in this solve.

For each order, the `M` independent vector samples have marginal
variance at most `V_j delta^(2j)/M` after averaging. Independence
between Fourier modes is neither true nor used. Taylor's integral
remainder on the segment from `g` to `v`, which lies in the open
unit ball, is at most `B_J delta^J/J!`. Consequently, for every
coefficient, Minkowski gives

    ||c_l^raw-F_l(v)||L2
      <=eta+sum_(j=1)^m sqrt(V_j)Cint^j k^(-js-d/2)/j!
             +B_J Cint^J k^(-Js)/J!
      <=eta+Cstar k^(-qrate)<=epsilon/(2K).

The ceiling for `J` is precisely sufficient for the remainder to
have this order; no unknown higher derivative is acquired. Interval
projection onto the indicated coefficient intervals is nonexpansive
relative to the true coefficients, so this same estimate holds
after clipping. The new bias from clipping is harmless for this
absolute `L2` bound.

For the finite reconstruction `p=sum_l c_l b_l`, one has pathwise
`||p-P_N S_1^kappa v||inf<=sum_l|c_l-F_l(v)|`. The triangle
inequality in scalar `L2` and the actual tail therefore give

    || ||p-S_1^kappa v||inf ||L2<=epsilon.

This is a bound on the spatial supremum inside `L2`; it does not
replace that quantity by a supremum of pointwise RMS errors.

## 9. Explicit saturation and its uniform all-array Gevrey bound

Let `a=7/8`, `b=15/16`. For `0<t<1`, put

    phi(t)=exp(-1/t),
    w(t)=phi(t)/(phi(t)+phi(1-t)).

Extend `w` by zero and one outside the interval. The denominator is
at least `exp(-2)`, since one of `t,1-t` is at least `1/2`.
The branch tests avoid endpoint divisions. The source's `chi` is
the identity through `a`, then `z+(b-z)w((z-a)/(b-a))`, then the
constant `b`, with odd extension.

Flatness of `w` at zero and of `1-w` at one matches every derivative
of these pieces. The odd extension has no singularity at zero,
where `chi` is already the identity on an open neighborhood. It
maps all reals into `[-b,b]` and equals the identity on `[-a,a]`.

For `0<t<1`, direct differentiation gives

    0<=phi(t)<=exp(-1),       0<=phi'(t)<=4exp(-2),
    w'(t)=[phi'(t)phi(1-t)+phi(t)phi'(1-t)]
                     /(phi(t)+phi(1-t))^2,
    0<=w'(t)<=8exp(1)<24.

On the transition interval,
`chi'(z)=1-w(t)+(1-t)w'(t)`, so `0<=chi'<=25`. On the other
pieces its derivative is zero or one. Hence the stated global
Lipschitz constant `Lchi=25` is valid.

The Cauchy estimate on a disk of radius `c t` about `t>0` gives
`r!(ct)^-r exp(-c'/t)` for `phi^(r)(t)`. Maximizing in `t`
bounds this by `A C^r(r!)^2`. Its derivatives vanish at zero;
the reflected term has the corresponding property at one. Products
preserve this bound. For a denominator with lower bound `delta>0`
and derivative bounds `A B^l(l!)^2`, differentiating `D R=1`
and normalizing an induction for `R=1/D` gives

    (A/delta) sum_(l=1)^r (B/C)^l/binom(r,l).

Taking `C` large makes this at most one. This verifies the
reciprocal estimate rather than merely invoking smoothness. Fixed
affine rescaling, multiplication by the linear transition factor,
the matching constant/identity pieces, and reflection then prove

    sup_z|chi^(r)(z)|<=Achi Cchi^r(r!)^2,       r>=0,

with fixed public constants. Evaluation of `chi` itself is a fixed
finite elementary program; this derivative proof adds no evaluator
or integral primitive.

Now every clipped array, regardless of its probability or the size
of its pre-clipping values, satisfies

    ||partial^alpha p||inf<=2K(2*pi*N)^|alpha|.

For `n=|alpha|>=1`, the ordered finite-jet chain rule gives

    partial^alpha(chi(p))
      =alpha! sum_(r=1)^n chi^(r)(p)/r!
         sum_(beta_1+...+beta_r=alpha, |beta_i|>=1)
                    product_i partial^beta_i p/beta_i!.

Allowing zero multi-indices in the nonnegative inner estimate gives
the multinomial identity `r^n/alpha!`. Hence

    ||partial^alpha(chi(p))||inf
      <=Achi(2*pi*N)^n sum_(r=1)^n (2Cchi K)^r r! r^n.

Since `2Cchi K>=1`, bound the sum by
`n(2Cchi K)^n n! n^n`. Using

    n<=2^n,       n^n<=exp(n)n!,       n!<=d^n alpha!,

gives exactly

    ||partial^alpha qhat||inf
      <=Achi[8*pi*exp(1)*Cchi*d^2*N*K]^n(alpha!)^2,
    qhat=chi(p).

Thus T81's specific sufficient constant in (7.4) is valid. With
`Rhat=NK` and `chat` at most the reciprocal of twice the bracket's
fixed constant, summing all multi-indices gives

    ||qhat||_(G_(chat/Rhat))<=Achi 2^d,
    ||qhat||inf<=15/16.

Both are uniform over all clipped coefficient arrays. Evaluating
their trigonometric polynomial and then `chi` costs `O_d(K)`
operations, including all coefficient accesses. No norm test is
needed. The inverse Gevrey scale is polynomial in `T`, not a random
regularity parameter depending on a favorable sample event.

## 10. Actual-flow comparison and complete error allocation

The exact time-one target lies in the identity interval of `chi`.
The preceding `L2` estimate and the global Lipschitz bound yield

    || ||qhat-S_1^kappa v||inf ||L2<=Lchi epsilon=exp(-S)/16.

For two real solutions, their difference has coefficient

    1-(u^2+uw+w^2)<=1

in its linear parabolic equation. Applying the maximum principle to
the exponentially rescaled difference gives

    ||S_t^kappa f-S_t^kappa h||inf<=exp(t)||f-h||inf.

The profiles in this application are bounded by one; their global
solutions and comparison are available. This uses the one-sided
rate one, and does not substitute the absolute reaction Lipschitz
constant on a bounded interval.

Consequently the exact continued value from `qhat` has RMS error
at most `1/16` from the actual `S_T^kappa v(x*)`. The final known-
profile call uses time `S=T-1>=1`, the uniform interface from
Section 9, and `Pout=T+log(16)>1`. It has deterministic conditional
sup error at most `exp(-T)/16` on every completed coefficient array.
Thus

    ||Y_T-S_T^kappa v(x*)||L2
      <=1/16+exp(-T)/16<=1/8.

Optional output projection onto `[-1,1]` can only improve this error.
The first term includes the Fourier tail, known-base numerical bias,
all marginal sampling errors, the finite Taylor remainder, and
saturation. The second term pays the actual final evolution error.
There is no omitted phase approximation, branch classification,
event-complement loss, or favorable-input assumption.

## 10a. Whole-profile output at each prescribed horizon

At the root's request, I independently checked the stronger output
interpretation before freezing this review. It follows from the
displayed inequalities without changing the T81 source or algorithm
parameters. Return its indexed real Fourier array `U_out`, and omit
the optional scalar output projection.

On every completed sample path, the deterministic final solver gives

    ||U_out-S_S^kappa qhat||inf<=exp(-T)/16.

The preceding comparison also holds in spatial sup norm. Applying
Minkowski to those same two terms therefore proves

    sup_(v in V) (E||U_out-S_T^kappa v||inf^2)^(1/2)
       <=1/16+exp(-T)/16<=1/8,       T>=2.

This controls the spatial supremum before taking the expectation.
It is stronger than a separate pointwise RMS guarantee at every
point. The array coefficients are Borel functions of the transcript,
and its finite-dimensional embedding into `C(X)` is continuous, so
the sup-norm random variable is measurable. The zero-array extension
on null nontermination seeds gives the same interpretation as the
scalar output.

The final cutoff can be chosen as

    H_out=ceil(C_kappa Rhat Eout^(2d+8))
         <=C(1+T)^(3d+9).

Consequently the stored array has at most
`C(1+T)^(3d^2+9d)` entries, and its value at any specified point is
computable in `O_d((2H_out+1)^d)` charged operations. Its construction,
storage, and one such evaluation were already included in T81's
work accounting. Returning the array instead of the final scalar
does not increase that bound and acquires no additional unknown
values. No clipped function is being claimed to remain a Fourier
polynomial; the returned object is the unsaturated solver output
array itself. The saturation was applied to its input `qhat`.

This is a fixed-horizon assertion for the algorithm chosen at each
prescribed `T`. It does not assert a bound on the expectation of a
supremum over all horizons, almost-sure uniform-in-time error, or a
single pathwise event controlling an infinite family of algorithms.
The deterministic bounded-horizon patch in Section 13 also returns
a Fourier polynomial and has the same spatial sup error `3/32`.

A separately proved exact-value point-query lower bound transfers
to this stronger profile approximation problem: evaluating a returned
finite array at `x*` adds no original-data acquisitions, and point
error is bounded by sup-norm error. Such a query lower bound also
lower-bounds profile work because each acquisition is charged.
This transfer does not accept or prove any missing all-diffusivity
lower bound; T82/T83 remain separate evidence.

## 11. Work bound and all-seed query cap

Paid interpolation and the accurate base solve cost
`C k^d(1+T)^a0`. There are `M=k^d` samples for each of the fixed
orders `1,...,m`; their expected total work is `C k^d(1+K)`.
Frequency enumeration, allocation, coefficient extraction and clipping
are also counted and are absorbed by these bounds.

For every completed array, the continuation profile has

    Rhat=NK<=C(1+T)^(d+1),
    Wqhat<=C(1+T)^d,       Eout<=C(1+T).

Its deterministic conditional work is therefore at most
`C(1+T)^(a0+d^2+2d)`. This includes the actual `O(K)` cost of every
profile evaluation on the final initialization grid; treating the
saturation as a unit-cost function oracle would be incorrect.
Combining the terms gives T81 (9.1).

The only original-data acquisitions are the grid and the residual
tuples, so on every seed path

    Q_T<=k^d+sum_(j=1)^m jM
       =[1+J(J-1)/2]k^d.

On a null nonterminating preparation path, that sample has made no
acquisitions; any earlier completed samples remain within the same
public count. Repeated spatial points are included. Vector sharing
does not multiply this cap by the number of Fourier coefficients.

Finally,

    k^d<=C exp(gamma T)K^(d/qrate)
       <=C exp(gamma T)(1+T)^(d^2/qrate).

This proves the expected-work upper bound with, for example,

    A=a0+d^2+2d+ceil(d^2/qrate)+2.

The query cap retains its polynomial overhead. This proof gives no
exact `Theta(exp(gamma T))` query statement for all `kappa>0` and
does not by itself give any lower bound.

## 12. Borel rules, endpoints, and off-promise totality

Every deterministic solver count depends on public parameters alone.
FFT construction, polynomial arithmetic, floors, guarded bumps,
clipping, and saturation are Borel finite operations. Cardinal
denominators are nonzero, nonzero-mode `z` is positive, and all bump
or saturation divisions occur inside guarded positive-denominator
branches. Zero-frequency and zero-node convolution weights are
specified separately. A zero-length Gaussian edge is assigned the
zero vector, so no positive-square-root primitive is called on zero.

The random seed can be a countable product of the stated primitives.
With a fixed traversal and labeling order, finite-tree events,
positions, selected tuples and original query points are Borel.
Continuous promised `v,g` make the evaluations measurable. Each
tree has finite expected work and halts almost surely; only finitely
many trees are requested at fixed `T`. This proves almost-sure
halting and the asserted expectation, without a tree truncation.

The set of finite completion histories is a countable Borel union.
Extending the output by zero on the null nontermination set gives
a Borel random variable. This mathematical extension does not claim
that a finite program can detect that null set.

For arbitrary finite off-promise responses, optional projection onto
`[-1/2,1/2]` leaves all promised transcripts unchanged. Even if the
resulting coarse interpolant fails the accuracy or norm hypotheses,
its lookup remains a finite guarded formula. Every fixed-count
Galerkin/collocation operation remains algebra on finite real arrays;
large values do not cause a real-arithmetic overflow. The stochastic
genealogy law is input independent, and every preparation on a finite
tree contains only finitely many such operations. Halting is not
controlled by an unverified norm or convergence test. Coefficient
projection then gives the uniform continuation interface for every
completed transcript, whether or not the original data were promised.

The ideal word sizes, exact continuous random locations, and unbounded
finite real magnitudes are essential parts of this argument's model.
They are not a hidden finite-bit implementation claim.

## 13. Bounded horizons and acceptance boundaries

Choose the bounded-time grid `k_b>=k0` large enough that
`exp(2)Cint k_b^-s<=1/32`. Actual comparison controls its flow
error by `1/32` uniformly on `[0,2]`. The early Gevrey and later
analytic tail argument includes time zero, so a fixed spatial cutoff
and fixed initialization grid make the Galerkin error at most
`1/32` throughout that interval.

This is a fixed-dimensional polynomial ODE with bounded real
trajectories. On a fixed neighborhood, its vector field, derivative,
and trajectory second derivative have public bounds. For step
`T/n_b`, the Euler local defect is `C(T/n_b)^2`; a finite Gronwall
recurrence gives global error `C/n_b`. Choosing one sufficiently
large fixed integer `n_b` makes the error at most `1/32` and keeps
the iterates in that neighborhood. At `T=0` the same public number
of zero-length updates is harmless. The exact projected cubics use
the same finite transforms.

The resulting deterministic error is `3/32`, with fixed work and
fixed acquisition count. This establishes T81's stated all-time
`1/4` completion; in fact `3/32<1/8`, so the patch is also consistent
with a uniform all-time `1/8` upper if that stronger wording is later
desired. No short-time use of an `S>=1` panel lemma is hidden here.

All substantive gates pass without a change of class, a stable graph,
a phase functional, a spectral-gap condition, or unknown higher-order
regularity. The proof supplies a conventional ideal-work upper bound.
Independent lower-bound acceptance, root correspondence, implementation,
numerical checking, formalization, finite precision and priority remain
separate questions. None is supplied by this audit's PASS.

## 14. Primary checks and final provenance

I opened the primary An--Henderson--Ryzhik text, checked its diffusion
convention and Section 3.1's ternary-majority renewal construction.
It attributes that Allen--Cahn voting representation to Etheridge,
Freeman and Penington. Its normalization differs from this project's;
Section 7 above checks the present rate and generator directly.
[Primary AHR text](https://arxiv.org/html/2209.03435).

I also read Trefethen's complete one-page *Lecture 3: Chebyshev series*
note, including its Bernstein-ellipse convergence principle and its
warning about monomial conditioning. The growing-cutoff PDE solver,
its panel geometry, and its work bound were independently checked
above; the note alone is not a complexity theorem for this algorithm.
[Primary author note](https://people.maths.ox.ac.uk/~trefethen/outline3_2017.pdf).

These were bounded attribution/approximation checks, not a priority
search. No unexamined literature result was used to replace a material
proof obligation. T69, T65, T82 and T83 were not independently audited
here, and no result from their graph or lower-bound constructions is
needed for this upper-bound verdict.

The research role was requested as `gpt-6-astra/max`; the actual backend
identity and effort are not independently attested by this worker's
available tools. Reading the routing configuration does not itself
establish a model switch.

Performed tools: read-only repository/context/skill inspection, line
counts, SHA256 source checks, the two primary-source retrievals,
independent conventional derivations, and writing this dedicated audit.
Some initially combined read outputs were truncated by the tool output
budget; the omitted relevant passages were subsequently retrieved in
separate reads. No conclusion is based on unseen truncated text.
No sampler/PDE run, numerical experiment, unknown-input acquisition,
implementation test, Lean invocation, canvas update, accepted-ledger
edit, publication or model-setting change was performed. The final
audit hash is supplied in the handoff; it is not self-embedded here.
