# R14c: stable graph, uniform burn-in, and local/far output at a natural gap

Date: 2026-09-29. Root-authored conventional proof candidate. Independent
audit pending. This is a bounded continuation of R14 and the accepted
R14b/T76 local lemmas. It proves no new query/work theorem by itself.
The accepted D29/D33 statements and frozen sources are unchanged.

## 1. Fixed equation and exact target

Let X be the normalized unit d-torus, d>=1 fixed, and consider the actual
real Allen--Cahn flow

    u_t=(kappa/2) Delta u+u-u^3,   kappa>0,
    lambda=2 pi^2 kappa>1,  nu=lambda-1>0.

Write P_t for this heat semigroup, Pi for Haar averaging, Q=I-Pi,
and choose once and for all 0<sigma<nu. All constants below may depend
on fixed d,kappa,sigma. None is uniform as nu approaches zero.
Solutions from continuous data are continuous in C(X) to time zero and
classical for positive time. The invariant interval [-1,1], uniqueness,
comparison and the usual mild equation are the actual PDE properties
used. They follow from the locally Lipschitz cubic and parabolic
comparison; the invariant interval prevents finite-time escape.

The target is to construct a local decaying stable graph and a single
finite burn-in L working for every ||q||inf<=7/8. An explicit paid
coarse mean test then separates a local sigmoid approximation from a
far branch converging uniformly to one of the two constant equilibria.
No global asymptotic phase A is used. No original-time data oracle,
numerical PDE evaluator or derivative sampler is supplied here.

## 2. An explicit centered heat bound

Let

    rho=((1+exp(-lambda))/(1-exp(-lambda)))^d,
    M=2 rho exp(lambda),  B_t=exp(t) P_t Q.

The signed kernel of B_t is exp(t)(P_t(x,dy)-dy), including at t=0.
For 0<=t<=1 its variation is at most 2 exp(t), which is at most
M exp(-nu t) since 2 exp(lambda t)<=M. For t>=1, Fourier expansion
and |n|^2>=|n|_1 for integer n give

    integral |p_t-1| <= sum_(n!=0) exp(-lambda |n|^2 t)
      <= exp(-lambda(t-1)) sum_(n!=0) exp(-lambda |n|^2)
      <= (rho-1) exp(-lambda(t-1)).

Thus at every t>=0 the actual kernel satisfies

    sup_x ||B_t(x,.)||TV <= M exp(-nu t).             (2.1)

The Fourier series is absolutely convergent for positive t. The short
time argument does not use a heat density at t=0.

## 3. Stable graph and compatible radii

Use the Banach space E_sigma of continuous C(X)-valued trajectories
with norm sup_t exp(sigma t)||U(t)||inf. Define

    (K F)(t)=-integral_0^t B_(t-a) F(a) da
             +integral_t^infinity exp(t-a) Pi F(a) da,
    C=M/(nu-sigma)+1/(1+sigma).

Both Bochner integrals converge in C(X), and (2.1) gives ||K||<=C.
For the forward term use exp(-(nu-sigma)(t-a)); for the backward
term use exp(-(1+sigma)(a-t)). Strong heat continuity and these
integrable majorants give continuity in t. Pointwise multiplication
maps E_sigma^3 to E_sigma continuously with trilinear norm at most one.

Choose a fixed sufficiently small R>0. Set

    r=R/(4M), B=R^3/(1+3sigma),
    E=3R(1+R)/sigma+3R^2/(2sigma), D=2 exp(E) B.

Require all of

    R<=1, r<=1/8, C R^2<=1/8, B<=r/8,
    D<=r/16,
    R+exp(E)-1+(1-r^2)^(-1/2)-1 <= 1/32.            (3.1)

These conditions are compatible: C,M,sigma are fixed positive
constants, B/r and D/r tend to zero quadratically in R, and the final
left side tends to zero. Choosing a smaller positive rational R is
permitted. Every condition can be checked from the displayed fixed
constants; no unknown initial profile enters this choice.

For mean-zero w with ||w||inf<3r, solve

    U_w(t)=B_t w+K(U_w^3)(t).                        (3.2)

On the closed radius-R ball, the right side has norm at most
3Mr+C R^3<=7R/8. Its Lipschitz constant is at most 3 C R^2<=3/8.
Banach contraction gives a unique U_w in that ball, actually of norm
at most 7R/8. Define

    Theta(w)=Pi U_w(0)=integral_0^infinity exp(-a)Pi U_w(a)^3 da.

Then |Theta(w)|<=B<=r/8, U_w(0)=w+Theta(w), and the centered
forward equation and scalar mean equation in (3.2) combine into the
actual mild PDE equation. Its initial norm is below 3r+r/8<1.
Uniqueness identifies U_w with S_t(w+Theta(w)). In particular

    ||S_t(w+Theta(w))||inf <= R exp(-sigma t).       (3.3)

There is no backwards parabolic solve: the backwards integral occurs
only in the scalar mean component of this fixed-point construction.

The same contraction is equivariant under sign reversal and spatial
translation; uniqueness makes Theta odd and translation invariant.
It is C-infinity as a map on the open mean-zero ball. Indeed the
derivative with respect to U of U-Bw-K(U^3) is I-K(3U^2 .), with
uniform inverse norm at most 8/5 by its Neumann series. Bounded
polynomial differentiation and the implicit theorem give all finite
derivatives, uniformly on the displayed solution ball. Differentiating
at zero gives DU_0[h](t)=B_t h and DTheta(0)=0; oddness gives
D^2Theta(0)=0. These statements concern ordinary operator derivatives,
not yet product-measure representations or weighted-L1 estimates.

## 4. Uniform centered decay without a large-gap phase theorem

Take any ||q||inf<=a0=7/8, and let u=S_tq and m=Pi u. Its centered
L2 energy obeys, for t>0,

    d/dt ||u-m||2^2
      =-kappa ||grad u||2^2+2||u-m||2^2
         -2 integral (u-m)(u^3-m^3)
      <=-2nu ||u-m||2^2.                            (4.1)

The last integral is nonnegative because the cube is increasing;
Poincare on the unit torus supplies ||grad u||2^2>=4pi^2||u-m||2^2.
The initial variance is at most ||q||2^2<=a0^2. Continuity to time
zero and Gronwall yield ||Q S_tq||2<=a0 exp(-nu t).

To upgrade to sup norm at t>=1, put a=t-1 and compare S_h(S_aq)
with the spatially constant solution b(h) from b(0)=Pi S_aq.
Their difference d(h) solves a linear equation with potential

    c(h,x)=1-(u(h,x)^2+u(h,x)b(h)+b(h)^2)<=1.

Both solutions remain in [-1,1]. The positive function
psi(h)=exp(h)P_h|Q S_aq| is a supersolution for that same linear
equation, and -psi is a subsolution. Thus at h=1,

    ||S_tq-b(1)||inf <= e ||p_1||2 ||Q S_aq||2.

Subtracting its mean costs at most a factor two. Parseval gives
||p_1||2^2=sum_n exp(-2lambda|n|^2)<=rho, so ||p_1||2<=rho.
Consequently, uniformly over the entire indicated input ball,

    ||Q S_tq||inf <= 2e rho a0 exp(-nu(t-1))
      <= Cw exp(-nu t),   Cw=2e rho exp(nu), t>=1.   (4.2)

This proof does not claim that Q obeys a positive semigroup or that a
spectral discretization has a maximum principle. Only the actual
linear difference equation is compared to heat evolution.

Choose a single integer L>=1 such that

    Cw exp(-nu L)<=r/64.                            (4.3)

Then every q in the full 7/8 sup-norm ball satisfies ||Q S_Lq||<=r/64,
strictly within the graph domain. L depends only on fixed PDE and
radius parameters and may be very large for a small spectral gap.

## 5. The global-in-input proxy and a buffered branch test

For every ||q||inf<=7/8 define the actual scalar

    H(q)=Pi S_Lq-Theta(Q S_Lq).

It is C-infinity on an open neighborhood of the closed 3/4 ball.
For example take the open 7/8 ball, on which (4.3) holds, and use
the actual finite-time smooth flow and the graph's open domain.
All fixed-order operator derivatives have uniform finite bounds
there: finite-time flow derivatives satisfy the linear variational
equation with potential 1-3u^2<=1 and lower-order product forcings;
induction and Gronwall bound them for the fixed time L. Combining
these bounds with the graph's uniformly invertible derivative
equation gives the assertion. No compactness of a C(X) ball is used.

H is odd. At zero, DS_L(0)=exp(L)P_L, so

    Atilde=exp(-L)H, D Atilde(0)=Pi, D^2 Atilde(0)=0.

The required weighted-L1 third derivative is an additional obligation;
ordinary smoothness here does not imply it.

For a possible algorithmic application, let the unknown ||v||inf<=1/2
have a known paid approximation g with ||g||inf<=3/4 and
||v-g||inf<=delta, where exp(L)delta<=r/32. Suppose a separately
certified finite computation supplies mhat with

    |mhat-Pi S_Lg|<=r/32.

These are explicit promises, not newly supplied algorithms. The actual
PDE difference comparison gives ||S_Lv-S_Lg||inf<=exp(L)delta.

If |mhat|<=r/2, then with b=Pi S_Lv and w=Q S_Lv,

    |b|<=9r/16, ||w||inf<=r/64,
    |h|=|b-Theta(w)|<=11r/16<r.

The R14b/T76 local theorem applies to this actual w+b=S_Lv and its
constructed stable trajectory (3.3). Conditions (3.1) give for every
t>=0 and every spatial point

    |S_(L+t)v(x)-Psi(exp(t)H(v))|<=1/32,
    Psi(z)=z/sqrt(1+z^2).                           (5.1)

This includes H(v)=0 and shifts arbitrarily close to zero. No phase
multiplier or lower bound on the distance to the graph is needed.

If |mhat|>r/2, then sign(mhat)*Pi S_Lv>7r/16 and (4.3) yields

    sign(mhat)*S_Lv(x)>27r/64>=r/4.

Comparison and oddness therefore bound the signed future solution
between phi_t(r/4) and 1, where

    phi_t(a)=a exp(t)/sqrt(1+a^2(exp(2t)-1)).

Since phi_t(r/4) increases to one, a fixed t_far exists with
1-phi_t(r/4)<=1/16 for all t>=t_far. Returning sign(mhat) then has
absolute error at most 1/16 for T>=L+t_far. The sign is correct for
every allowed coarse mean error and residual, not only on average.

## 6. Conditional graph evaluation interface and remaining obligations

For any explicitly supplied mean-zero wtilde with ||wtilde||<=r/8,
the graph above gives |Theta(wtilde)|<=r/8 and the same decaying
trajectory. All T76 root conditions now follow from (3.1). Thus
buffered bisection of Pi S_tau(wtilde+c), c in [-r/4,r/4], computes
Theta(wtilde) to zeta<r if each mean evaluation has deterministic
error <=exp(-2tau)zeta/8. The public choice
tau=max(1,ceil(log(1/zeta))) and at most ceil(log_2(r/zeta)) midpoint
evaluations suffice. This remains an evaluator interface, not a
cost-free PDE-value oracle or a work bound.

This candidate supplies actual graph existence, uniform entry of the
centered component, explicit compatible radii and both output branches
for every fixed lambda>1. It still requires independent audit. Even
after such an audit, the following gates remain separate:

- Uniform weighted-L1 D^3 Atilde and the full signed lower-prior
  separation/information correspondence.
- Actual all-order derivative measures and samplers, with both
  variance and operation counts rechecked at diffusivity kappa.
- A known-profile high-precision solver and paid interpolation
  interface in the same ideal work model for the changed equation.
- The complete upper risk/query/work composition, full Lean and
  numerical validation, and any novelty or significance assessment.

The critical lambda=1 and several-unstable-mode lambda<1 cases are
excluded. No uniform limit toward the critical gap, arbitrary-domain
extension, fixed-bit guarantee, practical speedup or prize claim follows.
