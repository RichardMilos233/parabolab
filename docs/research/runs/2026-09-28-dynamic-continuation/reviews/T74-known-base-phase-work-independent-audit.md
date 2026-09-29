# T74: independent audit of the known-base work gate

Date: 2026-09-29. Research-only mathematical audit.

**Verdict: PASS for R12 Gate A in the stated exact real elementary-operation
model.** The quantitative solver lemma in T70 can be justified with the
displayed cutoffs and a finite polynomial work overhead. I found no
unresolved mathematical obstruction in that lemma or its application to
the actual graph functional. This verdict includes the explicit local
completions and scope qualifications below; it does not merely adopt the
author's GO label.

The accepted statement uses the full D29 input class, every fixed pair of
integers `d,s>=1`, the unit torus, and the actual equation

    u_t=Delta u/2+u-u^3.

Precisely, `v` is smooth and periodic, `||v||inf<=1/2`,
`max_(|alpha|<=s)||partial^alpha v||inf<=1`, and
`min v<0<max v`. The bound is uniform over this full class.

The public interpolant is the Gevrey-2 partition/stencil formula in T70.
No Gevrey assumption is imposed on the unknown datum. Given the paid
`k^d` uniform-grid values, its construction, its fixed-tolerance mean
test, and its near-branch value `h0` require at most

    C k^d (1+T)^a

operations, with

    |h0-H(g)|<=eta,       eta=exp(-(T-L))/192,
    H(g)=Pi S_Lg-Theta(Q S_Lg).

Here `T>=T0`, `k>=k0`, and `log k<=Klog(1+T)` for a fixed public
`Klog`. Constants may depend on fixed `d,s,Klog` and the fixed accepted
analytic constants. The later known-profile lookup `g(x)` has constant
work in this model. There are no further acquisitions of the unknown
datum. The procedure is Borel and halts deterministically.

R12 explicitly permits the far branch to return its accepted scalar
comparison output without computing `h0`. T70's introductory wording
about computing `H(g)` is broader than the procedure's far-branch output.
If an `h0` is required on every transcript, execute the same graph-root
routine on the far branch as well. Its hypotheses hold there too, and
the same work bound holds. This is the first local completion, designated
**C1**; it changes neither the input class nor the asymptotic bound.

This file does not accept Gate B, promote a combined work theorem, or
change D29's existing query-theorem status. T73 and the root's subsequent
shared-model/source correspondence remain separate acceptance gates.

## 1. Evidence, independence, and immutable inputs

The entire 763-line T70 source was read. The following SHA256 values were
computed from the files, rather than copied from an author's assertion:

| Input in this run | SHA256 |
| --- | --- |
| `reviews/T70-known-base-phase-work-feasibility.md` | `46666ef19d4d66eb6196c486df726b6cc623f401fb717d925c82806bd3a905d6` |
| `reviews/T65-local-stable-graph-upper-proof.md` | `58e862c9cfbaf0946605d30d9c8e8a37e2570c0c0719d626683f22db60fc9f81` |
| `reviews/T56-signed-upper-feasibility.md` | `0f0cd6a6fbe97d5746c42f2da94161284f4b4fb3da70b724b5992450388d5933` |
| `reviews/T59-signed-upper-independent-audit.md` | `47d3ce98ac19210e9bbcd318ac1de2fb9dddd5bc372bff201dc97d47572301ab` |
| `reviews/R12-signed-work-composition-contract.md` | `390ede56727253adb0c23fb5356671f6b691b5c958ff4258d0e69ceeafd280ee` |

I inspected the run context, current checkpoint and D29/D30 claim entries,
the relevant actual-phase/interpolation passages of T56/T59, and T65's
graph definition, uniform burn-in, derivative lower bound, branch test,
and finite root reduction. T65's previously accepted analytic facts are
declared dependencies here; this is not a replacement audit of all its
all-order derivative-measure constructions. The root's preliminary T70
review was not used as independent proof evidence.

The math-auto-research skill, defaults, model-routing instructions,
general reader profile and theory-first execution instructions were read.
The requested/dispatched research role is `gpt-6-astra/max`. Backend
identity is not separately attested by the tools available inside this
worker. No model-setting change is claimed merely from reading a config.

Only this new T74 file is editable by this worker. Source inspection,
hashing and two primary-source retrievals were read-only. No numerical
experiment, solver implementation, oracle acquisition, Lean invocation,
publication or accepted-ledger edit was performed.

## 2. Coverage map and accepted cost model

Line references below refer to the frozen T70 source.

| T70 passage | Audit result |
| --- | --- |
| 27–70: class, graph, primitives | Pass with the near/far distinction C1 above. |
| 72–142: Gevrey interpolant and lookup | Pass; total-order smoothness suffices, including `s=1`. |
| 144–221: solver statement, Banach algebra, initial tails | Pass with explicit derivations below. |
| 223–257: real-solution analytic smoothing | Pass; the contour/Picard argument gives public uniform constants. |
| 259–310: projection, bootstrap, aliasing | Pass; projection losses remain and no Galerkin maximum principle is used. |
| 312–396: startup, sectors, panels, interpolation | Pass; completion C2 supplies an explicit ellipse and balanced panel choice. |
| 398–455: collocation and accumulated errors | Pass; completion C3 writes the recurrence and compatible allocations. |
| 457–531: scalar weights, work, conditioning | Pass in exact primitives; the guard-precision claim is a perturbation bound, not a bit theorem. |
| 533–586: burn-in and stored low modes | Pass; completion C4 makes the coefficient-access interface explicit. |
| 588–664: phase conditioning and graph root | Pass with absolute budgets, including exact interface zero. |
| 666–712: work, Borel rules, halting, boundaries | Pass within the declared model and fixed-parameter regime. |
| 714–763: literature/provenance | No novelty conclusion imported; selected primary-source checks are recorded in Section 14. |

One unit is charged for each arithmetic operation, comparison,
integer/index operation, floor/ceiling, stored-value access, and `exp`,
`log`, `sin`, `cos`, or positive-square-root evaluation. Each unknown
exact value acquisition also costs at least one unit. Complex arithmetic
is represented by a fixed number of real operations. Constants depending
on the fixed public parameters are allowed. No transform, quadrature,
ODE/PDE solve, arbitrary known-function evaluation, or root search is
an extra primitive.

This is a real-RAM model with the listed elementary primitives. Exact
oracle reals and exact comparisons are part of it. Finite floating
representations, elementary-function bit costs and memory-address bit
lengths are not being bounded. Gate A uses no random primitive. Gate B
must independently state its random-draw model and use this actual `g`.

## 3. The interpolant uses only the promised finite smoothness

Fix the stencil, for example the `s` consecutive scaled nodes
`0,...,s-1` in each coordinate relative to its center. It includes the
center, has tensor degree at most `s-1`, and reproduces every polynomial
of total degree at most `s-1`. The condition `k>=2s` permits consistent
periodic local lifts with distinct stencil nodes. All stencil values
are members of the same paid grid.

At a point `x`, freeze the total-degree Taylor polynomial of `v` at `x`
through degree `s-1`, using a common local torus lift. All nodes relevant
to the finitely many overlapping polynomials are at distance `O(1/k)`.
Their Taylor remainders are `O(k^-s)`, using only derivatives with total
order at most `s`. Scaled cardinal polynomials and scaled partition
weights have derivatives of order `j` bounded by `C_j k^j`. Polynomial
reproduction and the partition identity therefore give

    ||v-g||inf<=Cint k^-s,
    |partial^alpha g(x)-partial^alpha v(x)|
        <=C k^(|alpha|-s),                 |alpha|<s,
    ||partial^alpha g||inf<=C,             |alpha|=s.

For `s=1`, the Taylor polynomial is constant and the same argument
controls the first derivatives of the blended constants. Mixed
derivatives of total order greater than `s` of `v` are not invoked.

The cutoff also has a uniform quantitative all-order bound. Cauchy's
estimate for `exp(-1/z)` in a disk whose radius is a fixed small
multiple of positive `t` gives

    |(d/dt)^m exp(-1/t)|<=m! (c t)^-m exp(-c'/t).

For `m>=1`, maximizing `t^-m exp(-c'/t)` gives `(m/(e c'))^m`;
the elementary factorial bounds convert this to `A C^m(m!)^2`.
Composition with `1-t^2` retains the bound: its chain rule has only
first and second derivatives, with at most exponentially many weighted
terms. Every derivative tends to zero at the support endpoints, so
extension by zero is smooth with the same Gevrey order.

For the periodic denominator `D(t)=sum_j beta(t-j)`, the nearest
integer gives `D(t)>=beta(1/2)=exp(-4/3)`. There are at most two nonzero
terms. To verify the reciprocal bound explicitly, suppose
`||D^(l)||<=A B^l(l!)^2` and `D>=delta>0`. Differentiating `D R=1`
with `R=1/D`, and inducting on `m`, gives, after normalization by
`K C^m(m!)^2`, a bound

    (A/delta) sum_(l=1)^m (B/C)^l / binom(m,l).

Choose `K>=1/delta` and then `C` sufficiently larger than `B` that
`(A/delta)(B/C)/(1-B/C)<=1`. This closes the induction. Thus the
normalized weights are Gevrey-2 with public constants. Tensor products,
bounded overlap and fixed-degree scaled polynomials give

    ||partial^alpha g||inf<=B0(C0 k)^|alpha| (alpha!)^2.

Consequently, for `c C0<1`,

    ||g||_(G_(c/k))<=B0(1-c C0)^-d.

This constant is independent of `k` and the transcript. The statement
concerns the constructed `g`, not higher derivatives of `v`.

Taking the public `k0` large enough gives `||g||inf<=3/4` and also
the accepted branch condition `exp(L)Cint k0^-s<=r/32`. Increasing
`Cint,k0` for this chosen basis is allowed; the exponential rate is
unchanged. At a paid node all other translated bumps vanish and the
centered local polynomial reproduces that paid value.

Each node has only `O_(d,s)(1)` polynomial coefficients. A fixed matrix
converts its stencil values to scaled coefficients in constant work,
so preprocessing and storage cost `O(k^d)`. For any query location,
floor and modular indexing identify a bounded number of neighboring
records. Fixed-degree evaluation and a bounded number of cutoff
evaluations then compute `g(x)` in `O_(d,s)(1)` operations. The support
test precedes `1/(1-t^2)`, and `D` never vanishes. This proves the
actual lookup contract; it does not add an oracle for `g`.

## 4. Initial Gevrey control and a uniform spatial tail

Let `rho=c/kappa` and let the norm be T70's

    ||f||_(G_rho)=sum_alpha rho^|alpha| ||partial^alpha f||inf/(alpha!)^2.

In the multi-index product rule, the coefficient after this
normalization is `1/binom(alpha,beta)<=1`. Tonelli therefore gives
`||fg||_(G_rho)<=||f||_(G_rho)||g||_(G_rho)`. A Cauchy sequence
converges uniformly with every derivative; differentiation is closed
under these limits. This proves completeness. Real heat convolution
contracts each derivative sup norm. Strong continuity follows by
dominated convergence in the summable derivative series. These points
justify the claimed Banach-algebra mild fixed point, including at zero.

On the radius-`2B` trajectory ball, `f(u)=u-u^3` has a norm bound
`2B+(2B)^3` and Lipschitz bound `1+12B^2`. Select a fixed `h0>0`
small enough for invariance and contraction. It depends on `B`, not
`kappa`. Thus `||S_tq||_(G_rho)<=2B` on `[0,h0]`.

For a coordinate with `|n_i|=|n|inf`, integration by parts `m` times
gives

    |uhat(t,n)|<=2B (m!)^2/(2 pi rho |n|inf)^m.

Take `m=floor(c1 sqrt(|n|inf/kappa))`, with `c1` small enough that
the last ratio decreases geometrically in `m`; use the trivial bound
for the finitely many indices for which `m=0`. Summing lattice shells
and substituting `y=sqrt(j/kappa)` bounds the tail by an integral
of `C kappa^d y^(2d-1) exp(-c2 y)`. Absorbing its polynomial into
a slightly weaker exponential proves

    sum_(|n|inf>N)|uhat(t,n)|
       <=C kappa^d exp(-c3 sqrt(N/kappa)),       0<=t<=h0.

This includes `t=0`. A mere list of finite derivative bounds for an
arbitrary smooth formula would not imply the needed uniform rate.

## 5. The analytic strip is derived from the real solution

Real comparison gives `||S_tq||inf<=1` for every real time, since
the constants `+/-1` are equilibria. This fact applies to the actual
PDE and is established before considering Fourier discretization.

For real heat time `t>0`, the absolute value of the complex-shifted
Gaussian has integral `exp(|y|^2/(2t))`; periodization cannot increase
the corresponding `L1` upper bound. Consider the tube
`|Im z|_2<a sqrt(t)`. If a holomorphic profile at time `r<t` is
bounded in its tube, shift the convolution contour to
`y_r=sqrt(r/t)y`. Each coordinate contour stays inside the tube,
and periodicity cancels the vertical faces. The displacement obeys

    |y-y_r|<=a(sqrt(t)-sqrt(r))<=a sqrt(t-r).

Consequently the heat map between these tubes has norm at most
`K=exp(a^2/2)`, uniformly in `r,t`. At `r=0` the contour is real.
Choose a tube-space radius `R=2K` and fixed `h1>0` such that

    K+h1 K(R+R^3)<=R,
    h1 K(1+3R^2)<1.

The Duhamel map is then invariant and contractive on bounded
time-dependent holomorphic profiles. All integrals converge at zero
by the uniform bound. The iterates are holomorphic at each positive
time, and local uniform limits preserve holomorphy. On the real torus
uniqueness of the mild equation identifies the limit with `S_tq`.
For the smooth data used here continuity at zero causes no extra issue.

Take `h1<=h0`. Restart at the actual real profile at time `t-h1`.
Its sup norm is still at most one, so every `t>=h1` has the same
strip width `a sqrt(h1)` and bound `R`. Fourier contour shifting
inside a smaller fixed strip yields `|uhat(t,n)|<=R exp(-c|n|)`;
summing again gives `C exp(-c' N)`. In particular the constants are
independent of `kappa,t,S`.

The initial and restarted intervals cover `[0,S]`. Hence the Fourier
tail and the sup-norm projection error there are bounded by

    t_N=C kappa^d exp(-c sqrt(N/kappa))+C exp(-cN).

No initial analyticity promise, analytic continuation of the unknown
input, or maximum principle for a spectral truncation was used.

## 6. Projection loss, real bootstrap, and exact spatial algebra

Let `P_N` retain `|n_i|<=N`. In one dimension the Dirichlet kernel
is bounded by `C min(N+1,dist(x,Z)^-1)`; integrate separately on
`dist(x,Z)<1/(N+1)` and its complement. Tensor products give a
public bound

    ||P_N||_(inf->inf)<=Lambda=C_d(1+log(N+1))^d,

which can be taken at least one. All following estimates use this
upper bound, not a presumed contraction of the projection.

For `u=S_tq`, let `v_N=P_Nu` and let `u_N` solve the Galerkin ODE
from initial error `epsilon0` relative to `P_Nq`. Until `||u_N||inf`
first reaches two, both real arguments of the cubic lie in `[-2,2]`,
where a fixed Lipschitz constant, for example 11, suffices. Duhamel
for `u_N-v_N`, followed by adding `v_N-u`, gives

    D(t)<=epsilon0+t_N+11 Lambda integral_0^t D(r) dr,
    D(t)=||u_N(t)-u(t)||inf.

Thus `D(t)<=(epsilon0+t_N) exp(11 Lambda t)`. Selecting this bound
below `min(1/4,exp(-P)/4)` keeps `||u_N||inf<=5/4`, strictly inside
the bootstrap region. Its Fourier coefficients then remain bounded,
so the finite ODE cannot cease to exist before `S`.

For `E=1+P+S+log(kappa+1)` and
`N=ceil(C kappa E^(2d+8))`, one has

    log(N+1)<=C E,       Lambda<=C E^d,
    log kappa+P+Lambda S<=C E^(d+1),
    sqrt(N/kappa)>=c sqrt(C) E^(d+4).

The tail exponent dominates the required initial-error and Gronwall
budgets uniformly. Increasing a fixed public constant covers the bounded
small-parameter range. The large `Lambda` is paid, not suppressed.

For initialization by point evaluations of known `q`, choose the smallest
power-of-two grid `Q>=4N`. Absolute Fourier summability justifies the
alias identity. In the retained box the error is

    qhat_discrete(n)-qhat(n)=sum_(ell!=0) qhat(n+Q ell).

Different retained indices have different residues since `Q>2N`.
Every extra index has norm at least `Q-N`. Therefore the sum of retained
coefficient errors is bounded by the single Fourier tail beyond `Q-N`,
not that tail multiplied by the number of retained coefficients. For
perturbed nodal values, the additional coefficient `l1` error is at
most `M epsilon_grid`, `M=(2N+1)^d`. These are uniform public bounds.

For a polynomial supported in the `N` box its cube is supported in the
`3N` box. A power-of-two grid strictly exceeding `6N` separates every
frequency in that box. Inverse transform, nodal cubing, forward transform
and restriction thus give the exact projected cubic in the exact model.
A grid of `2N+1` points would not suffice.

Radix-two even/odd splitting uses a bounded number of additions and
multiplications per butterfly and `O(log Q)` stages. The tensor FFT,
including its generated `sin/cos` twiddle factors and array accesses,
therefore costs `O_d(N^d log(N+1))`. Padding has only a fixed factor
in each dimension. This counts an actual finite transform algorithm.

## 7. Complex time, the startup disk, and explicit panels — C2

For `z` with `|arg z|<=theta<pi/2`, integration of the absolute
complex Gaussian gives

    ||exp(z Delta/2)||_(inf->inf)<=(sec theta)^(d/2)=Ktheta.

It applies to complex-valued Fourier polynomials by restriction of the
full heat operator. With initial real Galerkin sup norm at most two,
take a fixed complex norm ball larger than `2Ktheta`. Its cubic
Lipschitz constant is `C_d Lambda`. Integration on radial segments
in the sector is bounded by `|z|Ktheta`, so Picard contraction yields
a fixed norm bound throughout a forward sector of radius
`rho_N=c_d/Lambda`. Uniqueness identifies the sector solution with
the real Galerkin trajectory on their common real interval. The same
argument restarts from every real time because the real bootstrap is
already proved.

These restarts are an a priori analytic proof. The algorithm does not
request or reconstruct the exact profile at a restart base; its actual
inputs are the stored approximate panel endpoints.

This is a sector, not a disk crossing the negative real axis. At zero,
use instead

    ||A_N f||inf
      <=sum_(|n_i|<=N) 2 pi^2 |n|^2 |fhat(n)|
      <=C_d N^(d+2)||f||inf=:D_N||f||inf.

Ordinary ODE Picard iteration for `A_Nu+P_N(u-u^3)` on a fixed norm
ball gives a genuine disk radius `a_N=c_d/(D_N+Lambda)`. This includes
negative times and uses the actual highest-frequency dependence.

For completeness, fix `theta=pi/4` and a Bernstein ellipse parameter
`varrho=2`. After scaling the interval `[1,2]`, that ellipse has
real part at least `7/8`, imaginary part of magnitude at most `3/8`,
and modulus below 3. It lies strictly inside this sector. For the
scaled interval `[0,1]`, its modulus is below 2.

Let `beta_p=C(1+log(p+1))>=1` be a public Lobatto Lebesgue bound,
choose

    h=c/(Lambda beta_p),
    a=min(a_N/16,h/16),

and take `c` small enough for `49h Lambda beta_p<=1/4` and
`h<=min(1/100,rho_N/100)`. The first panel `[0,a]` has its
`varrho=2` ellipse inside the initial disk. Panels `[t,2t]`, starting
at `t=a`, double the endpoint until it first reaches `[h,2h)`.
Their ellipses lie in the sector based at zero and have modulus
less than `3h<rho_N`.

Write the resulting endpoint as `b0`. For the remaining length
`Remainder=S-b0`, let `J=ceil(Remainder/h)` and take `J` equal
panels of length `ell=Remainder/J`. Since `S>=1` and `b0<2h`,
`Remainder>=h`, so `h/2<=ell<=h`. For a panel beginning at `b`,
restart the sector at real time `b-h>=0`. The relative interval is
`[h,h+ell]`; its ellipse has real part at least `7h/8`, imaginary
part at most `3h/8`, and modulus below `3h`. This proves one uniform
ellipse parameter for every panel and avoids a tiny last panel.

There are `O(1+log(h/a))` startup panels and `O(S/h)` later panels.
In particular

    n_pan<=C[1+log(N+1)+log(p+1)+S Lambda beta_p],
    log(1/ell_min)<=C[1+log(N+1)+log(p+1)].

For `p=ceil(C E^(d+4))`, `n_pan<=C E^(d+2)` and
`S Lambda beta_p<=C E^(d+2)`. All lengths and counts are public.

To check the interpolation bound itself, for nodes `cos(j pi/p)`
the cardinal formula gives, at `cos(theta)`,

    |L_j(cos(theta))|
       <=C min(1,1/(p|theta-j pi/p|)).

Use `|sin(p theta)|<=min(1,p|theta-j pi/p|)` and the factorization
of the cosine difference; endpoint cardinal weights only improve
the bound. Summing the equally spaced angles gives the harmonic
bound `beta_p`. This is a bound for the interpolation operator,
not a claim that it is contractive.

On each verified ellipse the exact Galerkin forcing
`F_N=P_N(u_N-u_N^3)` has norm at most `C_d Lambda`. Cauchy's
integral for its Banach-valued Chebyshev coefficients gives geometric
decay. At Lobatto nodes, higher Chebyshev polynomials alias to
Chebyshev polynomials of degree at most `p`, whose real-interval
norm is at most one. Summing the coefficient tail and these aliases
therefore gives

    ||F_N-I_pF_N||inf<=C_d Lambda 2^-p.

This supplies the claimed estimate directly. No uncontrolled
`N^(2p)` time-derivative bound is substituted for analyticity.

## 8. Collocation contraction and the global recurrence — C3

Consider the nodal map in T70 (6.1), in the real vector space of
Fourier polynomials with norm `max_i ||V_i||inf`. On the radius-four
ball, `|f(z)|<=68` and `|f'(z)|<=49` are valid loose bounds. Real
heat contraction, projection and time interpolation give

    Lip(T_ell)<=q_ell=49 ell Lambda beta_p<=1/4,
    ||T_ell(V)||<=2+68 ell Lambda beta_p<4

whenever the initial profile has norm at most two. Thus the fixed
point exists uniquely in this ball. The linear-heat start is in it,
and `K` Picard iterations have error at most `C 4^-K`. Choose a
public `K=ceil(Citer p)`; no residual test or nonlinear solver oracle
is involved.

Insert the exact Galerkin nodal values starting at the exact endpoint.
Their residual in this same nodal map is at most
`C ell Lambda 2^-p`. If the starting profiles differ by `e`, the
two fixed points differ by at most `e/(1-q_ell)`. Therefore the
endpoint error after a panel obeys the concrete recurrence

    e_next<=e/(1-q_ell)
             +C ell Lambda 2^-p/(1-q_ell)
             +C 4^-K+epsilon_alg.

The exact nodal values lie in the ball by the real bootstrap.
The numerical-start bootstrap closes by induction once the accumulated
error is below `1/4`. Hence this recurrence is not assuming its own
unproved stability region.

Since `-log(1-q_ell)<=C q_ell` and `sum ell=S`, the product of the
sensitivity factors is at most `exp(C S Lambda beta_p)`. Summing the
local errors gives

    e_final<=exp(C S Lambda beta_p)
      [C S Lambda 2^-p+C n_pan 4^-K+n_pan epsilon_alg].

In particular the startup costs neither `exp(C n_pan)` nor
`exp(C N^2 S)` in this bound. Heat stiffness has been integrated
exactly and appears in the initial disk and spatial arrays.

Here is one non-circular public error allocation. Put `delta=exp(-P)`
and make the spatial/initialization error at most `delta/4`, as in
Section 6. Make each of the three bracketed temporal contributions
at most `delta exp(-C S Lambda beta_p)/16`. The first two conditions
hold by increasing the fixed constants in `p` and `K`, since their
negative logarithms grow as `E^(d+4)`, while the required positive
logs are bounded by `C E^(d+2)`. Choose

    epsilon_alg<=delta exp(-C S Lambda beta_p)/(16 n_pan).

Any approximate initial nodal evaluation can be required to satisfy
`M epsilon_grid<=delta exp(-11 Lambda S)/C` with another fixed
constant. These choices are functions of public bounds alone. They
leave a strict margin both in the error target and the radius-four
ball. Exact primitive arithmetic can set all scalar errors to zero.

## 9. Scalar weights, FFT work and conditioning are accounted for

Let `lambda_n=2 pi^2 |n|^2`, `z=lambda_n ell`. Expanding `L_j`
in monomials reduces every weight to the moments

    I_m(z,theta)=integral_0^theta exp(-z(theta-r)) r^m dr.

Integration by parts gives exactly, for `z>0`,

    I_0=(1-exp(-z theta))/z,
    I_m=theta^m/z-(m/z) I_(m-1).

For `z=0`, use `theta^(m+1)/(m+1)`; for `theta=0`, use zero.
The test for `z=0` can simply use the zero Fourier index. Every
nonzero index has `lambda_n>0`, and every panel length is positive.
Thus no singular division is hidden in this formula.

Multiplying the `p` linear factors for each of the `p+1` cardinal
polynomials costs `O(p^3)`, including the denominators. For each
Fourier index, moments for all nodes and their combinations with
all cardinals cost `O(p^3)`. All weights for a panel therefore cost
`O(M p^3)`; they form `p` by `p` time matrices for each separate
Fourier mode, not a dense `M` by `M` spatial matrix.

One Picard iterate costs `O(M p^2+p M log(N+1))`: time-matrix
application and a padded cubic FFT at each node. The linear heat
factors cost `O(Mp)` exponentials and multiplications, included here.
With `O(p)` iterates, the total is

    C n_pan M[p^3+p^2 log(N+1)]
       +C M[log(N+1)+Wq].

This includes initialization evaluations, transforms, scalar weights,
array creation/access, index work and elementary evaluations. The
smallest power-of-two grids can be chosen by `O(log N)` public
doublings. Node cosines and FFT twiddles are also generated explicitly.

Substituting the bounds for `N,p,n_pan` gives, for the leading term,

    M<=C kappa^d E^(2d^2+8d),
    n_pan M p^3<=C kappa^d E^(2d^2+12d+14).

The other terms have no larger necessary exponent, apart from the
explicit factor `1+Wq`. T70's deliberately larger
`a=2d^2+20d+50` safely bounds the solver work. This proves (3.2)
as a finite operation bound, not just existence of a Fourier
approximation.

The recurrence is ill-conditioned at small `z`; fixed machine
precision would not justify it. Its exact-real use is valid without
a numerical conditioning assumption. The further perturbation claim
can also be checked without inventing a bit theorem:

1. Lobatto separation is at least `c p^-2`. Products of node
   differences and their reciprocals give coefficient magnitudes and
   sensitivities bounded by `exp(C p log(p+1))`.
2. Balanced panels give, for nonzero `z`,
   `log(1/z)<=C(1+log(N+1)+log(p+1))`; also
   `log(1+z)<=C log(N+1)`. Expanding the moment recurrence shows
   powers of `1/z` of degree at most `p+1` and factorial-sized
   coefficients. Its values and first sensitivities are bounded by
   `exp(C p[1+log(N+1)+log(p+1)])`, after enlarging constants.
   This covers the subtraction in `1-exp(-z theta)` as an absolute,
   rather than relative, error bound.
3. The weights act on bounded real Picard profiles. Small absolute
   weight errors produce at most polynomial factors of `M,p,Lambda`
   in the nodal sup error. FFT butterflies have bounded twiddle
   magnitudes and logarithmic depth; their additional amplification
   is polynomial in array size. Cubing bounded nodal values is
   Lipschitz on a fixed slightly enlarged ball. Picard contraction
   controls propagation of these per-iterate defects; Section 8
   controls propagation between panels.

Thus logarithms of every needed guard factor, operation count and
endpoint amplification are bounded by a fixed polynomial in `E`.
Choose a sufficiently large fixed `b` and absolute scalar tolerance
`exp(-E^b)`, including node/weight construction and accumulated sums.
It meets the public `epsilon_alg` and initialization allocations.
Very negative exponential arguments can be replaced by zero only
with this error included. Exact primitive evaluations avoid these
perturbations altogether.

This last argument controls a finite calculation under sufficiently
small perturbations of its scalar inputs and operations, with the
public integer choices fixed or chosen by conservative bounds and
the prescribed buffered branch rules retained. It does not encode
arbitrary oracle reals in finitely many bits, prove a
Turing-machine bound for their acquisition, or endorse monomial
recurrences at ordinary floating precision. If `q` is available only
through an approximate evaluator, `Wq` must include its actual cost
at the indicated accuracy, as the source explicitly requires.

## 10. Burn-in and the stored-coefficient interface — C4

The preceding solver applies to `g` with `kappa=k`, a fixed public
Gevrey bound and constant evaluator cost. For `S=L` and requested
log accuracy `O(1+T)`, its work is `C k^d poly(1+T)` under the
fixed `log k` restriction.

Set exactly as in T70

    xi=min(r/64,eta/[4(1+2v1)]),
    zeta=min(r/16,eta/2).

The analytic strip at `L>=1` gives a tail at most `xi/2` beyond
`n0=ceil(C(1+T))`, with fixed sufficiently large `C`. Let the first
solve return `U_L` with sup error at most `xi/(4 Lambda_(n0))`.
The requested logarithmic accuracy remains `O(1+T)`, including
`log Lambda_(n0)`. The large first cutoff is at least `n0` after
increasing a public constant. For `p=P_(n0)U_L`,

    ||p-S_Lg||inf
      <=Lambda_(n0)||U_L-S_Lg||inf+||(I-P_(n0))S_Lg||inf
      <=3xi/4<=xi.

`Pi p` is exactly the stored zero coefficient. Thus the fixed mean
test has error at most `xi<=r/64<r/32`, with no extra integration
or unknown acquisition. The same branch buffer as T65 is valid.

Uniform analytic-strip control also bounds the true coefficient
absolute sum of `S_Lg` by a public constant. Each computed low
coefficient differs from it by at most
`epsilon1=||U_L-S_Lg||inf`. Hence

    sum_(|n_i|<=n0)|phat(n)|
       <=C+(2n0+1)^d epsilon1<=C'.

The second bound is uniform: `epsilon1<=C exp(-T)` and
`(1+T)^d exp(-T)` is bounded for fixed `d`. It does not assert
boundedness of an arbitrarily inaccurate projected profile.

For `wtilde=p-Pi p` and `|c|<=r/4`, the coefficients of
`c+wtilde` have a public bounded absolute sum. Differentiating
their modes gives

    ||partial^alpha(c+wtilde)||inf
       <=C'(2 pi n0)^|alpha|,
    ||c+wtilde||_(G_(c0/n0))
       <=C' product_(i=1)^d sum_(m>=0)(2 pi c0)^m/(m!)^2.

This is a fixed bound independent of `k,T,c`. No differentiation
or norm oracle is required to compute the bound.

**C4, representation clarification.** The stored-polynomial shortcut
means an indexed Fourier array from which retained coefficients can
be read in unit work per entry, followed by zero-padding. The profile
here has degree `n0`, already stored in exactly that form, and the
next cutoff is at least `n0`; initialization costs at most the new
array size. If the generic solver lemma is applied to a polynomial
given in some other encoding, decoding/reading its required
coefficients is not free. For a higher-degree indexed array one
can read the retained coefficients directly and use the proved
tail bound for those discarded. The application in T70 needs
neither a huge scan nor arbitrary polynomial decoding.

## 11. The graph phase and its conditioning are the actual ones

Let `w=Q S_Lg`. The accepted burn-in and the just-proved sup error
give

    ||wtilde-w||inf<=2xi,
    ||wtilde||inf<=r/16+2xi<=3r/32<r/8.

Thus every `c+wtilde`, `|c|<=r/4`, has norm at most `11r/32<r`.
The stable graph constructed in T65 has
`|Theta(wtilde)|<=r/8` and
`A(Theta(wtilde)+wtilde)=0`. Its decaying actual trajectory proves
this identity; the root is not defined by an unrelated numerical
surrogate.

For clarity, the derivative lower bound follows from the accepted
actual `C^3` phase bound: oddness gives `D^2A(0)=0`, and
`DA(0)[1]=1`. Twice integrating derivatives on the segment from
zero to `c+wtilde` gives

    |DA(c+wtilde)[1]-1|<=K3 r^2/2<=1/64.

Hence `f(c)=A(c+wtilde)` is strictly increasing with derivative
at least `m0=63/64`. Its root lies in `[-r/8,r/8]`, while the
search interval is `[-r/4,r/4]`. The endpoint sign buffers are
at least `m0 r/8`.

The phase approximation uses its actual PDE-mean definition. For
data of norm at most `a0=7/8`, scalar comparison yields

    |Pi S_tau q|<=b_tau,
    b_tau=[1+(a0^-2-1)exp(-2tau)]^-1/2,
    1-b_tau^2>=(1-a0^2)exp(-2tau).

Since `G'(b)=(1-b^2)^-3/2`,

    sup_(|b|<=b_tau)|(exp(-tau)G)'(b)|
       <=C exp(2tau),       C=(1-a0^2)^-3/2.

This is the relevant conditioning factor. It is not uniform in
`tau`, and the proof does not pretend that it is.

With `epsilon_A=m0 zeta/4`, choose the public integer

    tau=max(1,ceil(log(2C0/epsilon_A)/(2nu-2))),
    nu=2 pi^2-1.

Then the accepted phase tail is at most `epsilon_A/2`. Solve
`c+wtilde` to sup error at most
`epsilon_A exp(-2tau)/(4C)`. The computed zero coefficient has
at most that error from the true mean. Clipping it to
`[-b_tau,b_tau]` is nonexpansive relative to that true mean, and
the transform then adds at most `epsilon_A/4`. An optional
absolute scalar transform error `epsilon_A/4` completes the
`epsilon_A` budget. In the exact model the latter error is zero.

Here `tau=O(1+T)` and the required solver log accuracy is also
`O(1+T)`, since it contains `2tau+log(1/epsilon_A)`. The initial
scale is `kappa=n0=O(1+T)`, and its coefficients are stored.
Each phase evaluation therefore costs `poly(1+T)` operations.

In exact elementary arithmetic `b_tau<1`, so clipping makes the
square root in `G` strictly positive. Finite-precision evaluation
would have to resolve the `exp(-2tau)` endpoint distance; this is
within the claimed polynomial guard precision but is not permission
to round an endpoint to one. No undefined endpoint evaluation is
present in the accepted exact algorithm.

## 12. Buffered bisection, zero phase, and the branch interface

At a midpoint, `fhat>epsilon_A` implies `f(c)>0`, so keeping the
lower half preserves the root. Likewise `fhat<-epsilon_A` permits
the upper half. In the remaining case, including equality,

    |f(c)|<=2epsilon_A,
    |c-Theta(wtilde)|<=2epsilon_A/m0=zeta/2.

The algorithm may immediately return this midpoint. Otherwise
after at most

    max(0,ceil(log_2(r/(4zeta))))

halvings the bracket length is at most `2zeta`, and its midpoint
has root error at most `zeta`. This is `O(1+T)` phase calls with
a fixed public maximum, irrespective of near-zero comparisons.

For the returned `chat`, set `h0=Pi p-chat`. The actual graph's
Lipschitz bound on the mean-zero ball gives

    |h0-H(g)|
       <=|Pi p-Pi S_Lg|
           +|Theta(wtilde)-Theta(w)|+|chat-Theta(wtilde)|
       <=(1+2v1)xi+zeta<=3eta/4<eta.

All three errors are absolute. Even if the two terms defining `h0`
almost cancel, their subtraction is an exact model operation and
the bound remains the sum of their absolute errors. Optional final
rounding can use the spare `eta/4`. There is no denominator involving
`H(g)`, `A(c+wtilde)` or distance from the stable interface. This
includes `H(g)=0` exactly.

The coarse test itself uses only `btilde=Pi p`. Together with
`exp(L)||v-g||inf<=r/32`, its accepted error bound implies that
`|btilde|>r/2` gives

    sign(btilde) Pi S_Lv>7r/16,
    sign(btilde) S_Lv>=3r/8.

The existing scalar comparison and sufficiently large `T0` give
the far-branch error. Conversely `|btilde|<=r/2` gives the accepted
near-branch bound along the entire segment between `g` and `v`.
Thus replacing the old expensive known-profile calculation by this
one preserves the branch interface. No phase-sign oracle is used.

C1's optional unconditional computation of `h0` is valid because
the graph-root construction uses small `Q S_Lg`, a property of the
entire accepted `7/8` ball. It does not require the evolved mean
itself to be small. Only the later phase/PDE proxy comparison uses
the near-branch condition.

## 13. Total work, totality and limits of acceptance

The data structure costs `C k^d`, and the one accurate burn-in
costs `C k^d poly(1+T)`. Projection and low-mode storage cost
`poly(1+T)` additional work. The `O(1+T)` graph-phase calls each
cost `poly(1+T)`, so their aggregate is still polynomial. Bisection,
clipping and scalar outputs have already been counted. Increasing
the finite exponent absorbs this last polynomial because `k>=1`.

For example, if `a_solver` is the safe exponent in Section 9,
the graph calls can be bounded by
`C(1+T)^(a_solver+d+1)`. The whole gate is then bounded by
`C k^d(1+T)^(a_solver+d+1)`. No identical numerical value of the
symbol `a` needs to serve both the standalone solver and the final
gate. The original T70 statement also allows this increase.

Exactly the `k^d` coarse unknown values are acquired. Known-grid
FFT evaluations and all later `g` evaluations read the saved
formula. Neither an unknown derivative nor a fine-grid value of
`v` is accessed. All accuracy parameters, truncations and loop
maxima use the horizon and public constants, not unknown norms.

The total off-promise rule is also finite. Coarse responses may
first be clamped to `[-1/2,1/2]`, without affecting promised
transcripts. A malformed smoothness transcript can invalidate the
accuracy/bootstrap estimates, but not the finite operation program.
Picard iterations are run for their fixed count and consist of
polynomial operations on finite real arrays. Their values may be
large, but each remains a finite real. No norm-success test controls
termination. Graph means are clipped to the public strict interior
comparison interval before the square root. Cardinal denominators,
partition denominators and nonzero-mode `z` denominators are public
and nonzero on every transcript. The far sign division is used
only when its argument has magnitude above `r/2`.

Finite compositions of these arithmetic/elementary maps, floors,
support tests, clipping and finite buffered branches are Borel.
All loops have public finite maxima. This proves deterministic
halting and Borel transcript rules, even though accuracy is claimed
only on the promised class.

The following stronger interpretations are rejected or remain outside
this audit:

- A corresponding work bound for every arbitrary known smooth formula
  without quantitative Gevrey control and evaluator accounting.
- A Galerkin maximum principle, an initial complex-time disk with radius
  independent of the cutoff, or exact cubic projection on an unpadded
  `2N+1` grid. None is needed by the accepted proof.
- A fixed-machine-precision or finite-bit guarantee, or practical
  efficiency. The exponents and constants can be extremely large.
- Uniformity as dimension, smoothness order or domain size varies.
- A literal unconditional `h0` output from the far-stop branch without
  C1; R12 itself only asks for `h0` on the near branch.
- Acceptance of T69's derivative sampler, its moments, hard query cap,
  random primitives or expected work. Those require T73 and root
  correspondence with this same interpolation representation.
- An accepted combined signed work theorem, a Lean certificate,
  numerical performance evidence or a novelty/priority claim.

There is no material open Gate-A lemma left by this review. The local
completions C1–C4 are supplied here in mathematical detail and do not
require stronger input assumptions, extra unknown queries or a larger
exponential rate. Frozen T70 and the other source files remain unchanged.

## 14. Bounded primary-source check and final provenance

I opened Trefethen's complete one-page *Lecture 3: Chebyshev series*
note. It states the Bernstein-ellipse geometric convergence principle
and warns about monomial conditioning. The concrete ellipse placement,
Banach-valued alias argument and growing-parameter error allocation
needed here were derived above, rather than imported as an unspecified
high-order convergence result. [Primary author note](https://people.maths.ox.ac.uk/~trefethen/outline3_2017.pdf).

I also opened the introduction of Hochbruck–Ostermann,
*Exponential integrators*, Acta Numerica 19 (2010). Its variation-of-
constants discussion and distinction between stiff and classical order
are consistent with the finite semigroup-convolution construction.
It is not used as a theorem establishing T70's growing-degree,
growing-cutoff or long-time work bound. [Primary author PDF](https://na.math.kit.edu/download/papers/acta-final.pdf).

These are bounded checks of relevant primary material, not a priority
search or independent verification of every bibliographic statement in
T70. The audit's mathematical acceptance rests on the displayed
derivations and explicitly named accepted analytic dependencies.

No code, experiment or Lean check was run. The recorded work consists
of read-only source/context inspection, SHA256 verification, the two
primary-source retrievals, independent mathematical derivation, and
writing this dedicated report. Root correspondence must bind this
report's final hash to the frozen T70 hash above and to the separately
audited Gate B before changing the combined theorem's status.
