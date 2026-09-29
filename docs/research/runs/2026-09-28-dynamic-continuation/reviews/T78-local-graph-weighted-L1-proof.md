# T78: the local graph proxy has the required weighted-L1 third derivative

Date: 2026-09-29. Conventional proof candidate, supplied for independent
research audit and full root correspondence review. The sole T78 edit is
this file. No accepted claim, frozen source, numerical record, code, or
Lean declaration is changed.

**Verdict: GO candidate for the missing local weighted-L1 derivative
lemma in R14.** The proof uses the actual heat kernel and actual
Allen--Cahn variational equations. It constructs the stable graph and
estimates its derivatives in both weighted spatial L-infinity and L1
norms. Ordinary composition then gives the desired third derivative of
the actual local proxy. In particular the L1 estimate is not inferred
from an L-infinity operator bound or from a product-measure theorem.

This is a local analytic lemma. It supplies no full-class burn-in,
long-time output estimate, hard signed prior, query lower bound,
derivative sampler, base-value algorithm, or work theorem. Those remain
separate obligations even if this candidate is accepted.

## 1. Statement with a buffered, full local input domain

Fix an integer d>=1 and kappa>0 such that

    lambda1=2 pi^2 kappa>1,    nu=lambda1-1>0.

Let X=(R/Z)^d with probability Haar measure dx. All functions and
derivatives in this proof are real. Write Pi f=integral_X f dx,
also identifying this scalar with the constant function, and Q=I-Pi.
Let P_t be the heat semigroup with generator kappa Delta/2, and let S_t
be the actual Allen--Cahn flow

    u_t=kappa Delta u/2+u-u^3,    u(0)=v.             (1.1)

Continuous initial data are interpreted as mild solutions continuous
in C(X) down to time zero and classical for positive time. Smooth
periodic data are included. All Frechet derivatives below are derivatives
on C(X), or on its closed mean-zero subspace C_0(X). Their directions
are arbitrary continuous functions in those respective spaces.

Choose any fixed 0<sigma<nu. Section 2 supplies a finite M>=2 for the
actual centered heat kernel; define

    C=M/(nu-sigma)+1/(1+sigma),
    0<R<=1,    C R^2<=1/8,    r=R/(4M).             (1.2)

Any further decrease of R is allowed. Construct Theta on

    W={w in C_0(X): ||w||inf<3r}

by Sections 3--4. Fix any finite L>=0 and put

    rho0=min(1/4, r exp(-L)/4),
    O={v in C(X): ||v||inf<2rho0},
    H(v)=Pi S_Lv-Theta(Q S_Lv),
    Atilde(v)=exp(-L)H(v).                           (1.3)

Then Q S_Lv belongs to the radius-r ball for every v in O, so (1.3)
is defined on an open neighborhood of the entire closed ball
||v||inf<=rho0. No sign, mean, spatial support, or derivative-norm
restriction is imposed on v in this local ball. In particular all
smooth members of the original signed class lying in the ball are
included, without an extra promise.

The map Atilde is odd and C-infinity on O, and

    Atilde(0)=0,    D Atilde(0)[h]=Pi h,
    D^2 Atilde(0)[h1,h2]=0.                         (1.4)

There is an explicitly displayed finite constant B such that, uniformly
for ||v||inf<=rho0 and h1,h2,h3 in C(X),

    |D^3 Atilde(v)[h1,h2,h3]|
      <=B ||h1||inf ||h2||inf ||h3||1.              (1.5)

The same estimate holds with any one of the three direction labels in
L1. All L1 norms use probability Haar measure. The constant depends on
fixed d,kappa,sigma,R,L, not on v, the directions, their support widths,
or a later horizon T. Once sigma and R have been fixed from the public
equation parameters, it is a fixed equation/L-dependent constant.
No uniformity as nu decreases to zero is asserted.

## 2. Actual heat envelopes for the changed diffusivity

For t>0 the heat kernel is the periodic wrapped Gaussian

    p_t(x)=sum_(n in Z^d) (2 pi kappa t)^(-d/2)
                         exp(-|x+n|^2/(2 kappa t)).

It is positive, has integral one, and convolution with it is P_t.
Gaussian integration against exp(-2 pi i m.x) gives its Fourier
coefficients exp(-lambda1 |m|^2 t). Thus

    p_t(x)=sum_(m in Z^d) exp(-lambda1 |m|^2 t)
                              exp(2 pi i m.x),       (2.1)

with absolute convergence for every positive t. This identifies the
diffusivity kappa in the actual kernel, rather than importing a sampler
or replacing a symbol in a kappa=1 sampling formula. Positivity and
unit mass give ||P_t||_(1->1), ||P_t||_(inf->inf)<=1. Translation
invariance gives Pi P_t=Pi; the same facts hold at t=0 with P_0=I.

Put B_t=exp(t)P_tQ and define

    q=exp(-lambda1),
    rhoH=((1+q)/(1-q))^d,    M=2 exp(lambda1) rhoH.

The signed convolution measure of B_t is

    beta_t=exp(t)(p_t(x)-1) dx  for t>0,
    beta_0=delta_0-dx.

For 0<=t<=1 its variation is at most 2 exp(t), and
2 exp(lambda1 t)<=M. For t>=1, (2.1) and |m|^2>=1 when m!=0 give

    integral_X |p_t-1| dx
      <=sum_(m!=0) exp(-lambda1 |m|^2 t)
      <=exp(-lambda1(t-1)) sum_(m!=0) exp(-lambda1 |m|^2)
      <=exp(-lambda1(t-1))(rhoH-1).                 (2.2)

For the last inequality, use n^2>=|n| for every integer n and sum
the resulting geometric series separately in each coordinate.
Both time regimes prove

    ||beta_t||TV<=M exp(-nu t),    t>=0.             (2.3)

Define a deterministic positive envelope by convolution with
|beta_t|, denoted Babs_t. For t=0 this is f -> f+Pi f on nonnegative
f. For p in {1,infinity}, Fubini and translation invariance give

    |B_t f|<=Babs_t |f|,
    ||B_t f||p<=||Babs_t |f|||p
               <=M exp(-nu t)||f||p.               (2.4)

In particular the L1 estimate is proved by integrating the absolute
kernel in the spatial output variable. It is not an inference about
arbitrary multilinear operators. If a different public M is already
being used, any M satisfying the actual variation bound (2.3) works.
The displayed M agrees with the explicit natural-gap graph choice in
R14c, but that candidate is not a premise here.

## 3. Lyapunov--Perron contraction in both spatial norms

Let E_inf consist of continuous C(X)-valued trajectories and E_1 of
continuous L1(X)-valued trajectories with respective norms

    ||F||_(sigma,p)=sup_(t>=0) exp(sigma t)||F(t)||p<infinity.

These are Banach spaces. Because X has probability mass one, E_inf
embeds continuously into E_1. Define the linear operator

    (K F)(t)=-integral_0^t B_(t-s)F(s) ds
              +integral_t^infinity exp(t-s)Pi F(s) ds. (3.1)

The forward and backward integrals converge in the respective spatial
Banach spaces. Their weighted norm bounds are

    M integral_0^t exp(-(nu-sigma)(t-s)) ds<=M/(nu-sigma),
    integral_t^infinity exp(-(1+sigma)(s-t)) ds=1/(1+sigma).

Consequently

    ||K F||_(sigma,p)<=C ||F||_(sigma,p),
                                      p=1,infinity. (3.2)

Strong heat continuity, compact-time integration and the displayed
integrable tail bounds show that K F is continuous in time. Absolute
domination follows from the positive integral operator obtained by
replacing the minus sign and B with a plus sign and Babs. Its identical
weighted bound is independent of the base profile. There is no hidden
spatial supremum inside an L1 integral.

For trajectories F1,F2,F3 one has

    ||F1 F2 F3||_(sigma,inf)
       <=product_i ||Fi||_(sigma,inf),
    ||F1 F2 F3||_(sigma,1)
       <=||F1||_(sigma,inf)||F2||_(sigma,inf)||F3||_(sigma,1). (3.3)

Indeed the product has the extra time factor exp(-2sigma t)<=1.
Permuting the three factors gives the estimate with any one in E_1.

For w in W, solve in E_inf

    U_w(t)=B_t w+K(U_w^3)(t).                       (3.4)

On the closed radius-R ball, the right side has norm at most
3Mr+C R^3<=7R/8. Since |a^3-b^3|<=3R^2|a-b| for real a,b of
absolute value at most R, its Lipschitz constant is at most

    alpha=3 C R^2<=3/8.                            (3.5)

Banach contraction gives a unique fixed point in this ball, lying
strictly inside it. In particular

    ||U_w(t)||inf<=R exp(-sigma t).                 (3.6)

The polynomial map (w,U) -> U-B_.w-K(U^3) from C_0(X) x E_inf
into E_inf is C-infinity. Its derivative in U is I-T_U, where

    T_U Z=K(3U^2 Z),
    ||T_U||_(E_inf->E_inf), ||T_U||_(E_1->E_1)<=alpha. (3.7)

The same geometric Neumann series is an inverse in either space,
with norm at most

    b0=1/(1-alpha)<=8/5.                            (3.8)

The implicit function theorem, or contraction difference quotients
followed by this inverse, proves that w -> U_w is C-infinity on W
as an E_inf-valued map. Only this C(X)-based differentiability is
asserted; the cubic is not being declared smooth on an open L1 ball.
The E_1 estimates below apply to these actual C(X) derivatives.

## 4. Equality with the actual stable flow, and parity

Taking the mean in (3.4) gives

    m(t)=Pi U_w(t)=integral_t^infinity exp(t-s)Pi U_w(s)^3 ds.

Set

    Theta(w)=Pi U_w(0),
    |Theta(w)|<=R^3/(1+3sigma).                     (4.1)

At time zero, Q U_w(0)=w, so U_w(0)=w+Theta(w). Splitting the
integral in Theta at t gives

    m(t)=exp(t)Theta(w)
           -integral_0^t exp(t-s)Pi U_w(s)^3 ds.

Adding this to the centered part of (3.4) proves exactly

    U_w(t)=exp(t)P_t(w+Theta(w))
                -integral_0^t exp(t-s)P_(t-s)U_w(s)^3 ds. (4.2)

This is the actual mild equation of (1.1), with the correct negative
cubic. Its bounded solution is unique: on any finite time interval,
subtract two bounded mild solutions and use the cubic local Lipschitz
bound and Gronwall. Thus

    U_w(t)=S_t(w+Theta(w)).                          (4.3)

The graph starting datum has norm at most R by (3.6) at t=0. The
infinite integral in (3.1) has constructed the scalar mean component;
no backwards PDE or changing external input has been inserted.

Replacing w,U by -w,-U preserves (3.4), so uniqueness gives
U_(-w)=-U_w. Hence Theta is odd and C-infinity. At w=0 the fixed
point is zero and differentiation of (3.4) gives

    D U_0[a](t)=B_t a,    D Theta(0)[a]=Pi a=0,
                                                   a in C_0(X). (4.4)

The second derivative of U at zero is zero, either by its equation
in Section 5 or by oddness. In particular D^2 Theta(0)=0.

## 5. Explicit mixed graph derivative estimates

Write U=U_w. For centered directions a_i, use

    J_i=D U_w[a_i],    J_ij=D^2 U_w[a_i,a_j],
    J_123=D^3 U_w[a1,a2,a3].

Differentiating the bounded polynomial (3.4) gives the exact equations

    J_i=B_.a_i+T_U J_i,

    J_ij=T_U J_ij+K(6U J_i J_j),

    J_123=T_U J_123
       +K(6 J_1 J_2 J_3
           +6U(J_12 J_3+J_13 J_2+J_23 J_1)).       (5.1)

The three last terms record all placements of the second derivative.
These are actual Frechet derivatives, because smoothness has already
been proved. Their infinite-time integrals and Neumann series converge
absolutely in the stated norms by (3.2), (3.3), and (3.7); a stochastic
derivative/expectation interchange is not used.

Define finite nonnegative constants

    K1=b0 M,
    K2=b0 6 C R K1^2,
    K3=b0 C(6 K1^3+18 R K1 K2).                    (5.2)

The first equation, (2.4), and (3.8) give

    ||J_i||_(sigma,p)<=K1 ||a_i||p,    p=1,infinity. (5.3)

This applies in E_1 because J_i, initially obtained in E_inf, is
already an E_1 element; the same equation and inverse hold there.
There is no new weak solution to identify. The second equation and
(3.3) give both

    ||J_ij||_(sigma,inf)<=K2 ||a_i||inf ||a_j||inf,
    ||J_ij||_(sigma,1)<=K2 ||a_i||inf ||a_j||1.     (5.4)

The reversed mixed estimate follows by symmetry. For the third
equation, bound J_12 in E_inf and J_3 in E_1; bound J_13 in E_1
and J_2 in E_inf; and bound J_23 in E_1 and J_1 in E_inf. The
direct product uses J_3 in E_1. This yields

    ||J_123||_(sigma,1)
       <=K3 ||a1||inf ||a2||inf ||a3||1.            (5.5)

The all-sup-norm version has the same constant K3.

The linear functional F -> Pi F(0) has norm at most one on E_1
and E_inf. Thus for k=1,2,3,

    |D^k Theta(w)[b1,...,bk]|
       <=Kk (product_(i<k)||bi||inf) ||bk||1,       (5.6)

uniformly on W, and also with all directions measured in sup norm.
The same holds for every permutation of the labels. This is the
required local graph estimate before finite-time composition.

## 6. Finite-time actual flow: smoothness and an L1-preserving envelope

For ||v||inf<1, the actual flow remains in [-1,1]. For completeness,
local mild existence follows by contraction for the locally Lipschitz
cubic on a short time interval. Comparison with the stationary
solutions +/-1 prevents escape from that interval and gives global
continuation. Comparison follows by subtracting bounded solutions:
their difference solves a linear equation with a bounded coefficient,
whose positivity is proved by the same shifted positive iteration
used below. Consequently no regularized or truncated flow occurs here.

On a fixed [0,L], put u(t)=S_tv. The mild equation is

    u(t)=exp(t)P_t v-integral_0^t exp(t-s)P_(t-s)u(s)^3 ds. (6.1)

This is a polynomial equation on C([0,L];C(X)). Its derivative in u
is I+V_u, with V_u z(t)=integral_0^t exp(t-s)P_(t-s)3u(s)^2 z(s) ds.
Because ||u||inf<=1, the n-fold Volterra iterate has norm at most
(3 exp(L)L)^n/n!. Hence the series for (I+V_u)^(-1) converges
absolutely, without a smallness requirement on L. The implicit
function theorem proves C-infinity dependence on v on the open unit
ball. Evaluation at time L gives C-infinity smoothness of S_L.

Here is a positive envelope for the actual first variational flow.
For 0<=s<=t<=L let E_u(t,s)f solve

    z_t=kappa Delta z/2+(1-3u(t,x)^2)z,    z(s)=f.

Writing this equation with scalar linear coefficient -2 gives the
Volterra representation with free semigroup exp(-2(t-s))P_(t-s)
and multiplier 3-3u^2>=0. Its successive iterates are nonnegative
for f>=0 and converge by the factorial bound. Thus E_u(t,s) is a
positive linear operator. Returning to coefficient +1 gives, for
f>=0,

    E_u(t,s)f=exp(t-s)P_(t-s)f
      -integral_s^t exp(t-a)P_(t-a)3u(a)^2 E_u(a,s)f da
      <=exp(t-s)P_(t-s)f.

By positivity and linearity, for signed f as well,

    |E_u(t,s)f|<=E_u(t,s)|f|
                       <=exp(t-s)P_(t-s)|f|.       (6.2)

The positive envelope on the right is independent of v and preserves
Haar mass up to the factor exp(t-s). Therefore

    ||E_u(t,s)f||p<=exp(t-s)||f||p,
                                      p=1,infinity. (6.3)

For an inhomogeneous variational equation with source F, its solution
is E_u(t,0)z(0)+integral_0^t E_u(t,s)F(s) ds. Substitution in the
Volterra equation and Fubini prove this formula; all integrands have
the finite-time absolute bounds just given. The same bounds apply to
that formula in L1 and sup norm.

In particular, differentiating the actual flow and writing
Y_i=D S_t(v)[h_i], Y_ij=D^2 S_t(v)[h_i,h_j], and Y_123=D^3 S_t(v)[h1,h2,h3],
one obtains

    Y_i(t)=E_u(t,0)h_i,

    Y_ij(t)=-6 integral_0^t E_u(t,s)(u(s)Y_i(s)Y_j(s)) ds,

    Y_123(t)=-6 integral_0^t E_u(t,s)
       [Y_1Y_2Y_3+u(Y_12Y_3+Y_13Y_2+Y_23Y_1)](s) ds. (6.4)

Every coefficient and sign comes from differentiating u-u^3.
Using (6.3), |u|<=1, and the spatial product estimate with exactly
one factor in L1 gives, for k=1,2,3,

    ||D^k S_t(v)[h1,...,hk]||1
       <=ck(t) (product_(i<k)||hi||inf) ||hk||1,     (6.5)

and the all-sup-norm version with the same constants, where

    c1(t)=exp(t),
    c2(t)=6t exp(2t),
    c3(t)=(6t+54t^2)exp(3t).                        (6.6)

For the second derivative, the integrand norm is at most
6 exp(t-s)exp(2s) times the direction product, whose integral is
at most 6t exp(2t). For the third derivative, each of the three
paired terms is at most c2(s)c1(s) times that product, with the L1
factor assigned to whichever derivative contains the last label.
Its full integrand is at most

    (6+108s)exp(t+2s)
       <=(6+108s)exp(3t)

times the product. Integrating gives c3(t). This proves (6.5) for
arbitrarily concentrated continuous directions; no Cauchy--Schwarz
or L2 intermediate bound occurs.

We will also use ||S_t v||inf<=exp(t)||v||inf on the open unit ball.
It follows by integrating DS_t along the segment theta v, 0<=theta<=1,
and using S_t0=0 and the k=1 sup estimate in (6.5).

## 7. Composition, explicit B, and derivatives at zero

For v in O, (6.5) and the definition of rho0 give

    ||Q S_Lv||inf<=2 exp(L)||v||inf<4 exp(L)rho0<=r.

This proves the domain and neighborhood assertions in Section 1.
Put W_L(v)=Q S_Lv and c_k=c_k(L). Since
||Q f||p<=2||f||p for p=1,infinity, (6.5) implies

    ||D^k W_L(v)[h1,...,hk]||1
       <=2ck (product_(i<k)||hi||inf)||hk||1,        (7.1)

with the analogous sup bound. Every W_L derivative is centered,
as required for the directions in (5.6).

The third-order chain rule has exactly the five terms

    D^3(Theta composed W_L)[h1,h2,h3]
      =D^3Theta[W_1,W_2,W_3]
       +D^2Theta[W_12,W_3]
       +D^2Theta[W_13,W_2]
       +D^2Theta[W_23,W_1]
       +DTheta[W_123],                              (7.2)

where Theta derivatives are evaluated at W_L(v) and W_I denotes
the actual derivative indexed by I at v. In each term exactly one
block contains label 3. Apply its L1 estimate in (7.1), and the sup
estimate to every other block. Symmetry allows (5.6) to put that
block in its L1 position. This proves

    |D^3(Theta composed W_L)[h1,h2,h3]|
       <=[8K3 c1^3+12K2 c2 c1+2K1 c3]
                             ||h1||inf||h2||inf||h3||1. (7.3)

Moreover |Pi D^3 S_L(v)[h1,h2,h3]| is at most the L1 norm in
(6.5). Thus one explicit constant in (1.5) is

    B=exp(-L)[c3+8K3 c1^3+12K2 c2 c1+2K1 c3].      (7.4)

All constants are finite for every fixed nu>sigma>0. Both estimates
are actually uniform on O; the stated closed ball keeps an explicit
buffer to its boundary.

The equation is odd, so uniqueness makes S_L(-v)=-S_L(v). Together
with the oddness of Theta this proves oddness of Atilde. At zero,
the first variational equation is Y_t=kappa Delta Y/2+Y, hence

    DS_L(0)h=exp(L)P_Lh.

Using DTheta(0)=0 and Pi P_L=Pi therefore gives

    D Atilde(0)h=exp(-L)Pi exp(L)P_Lh=Pi h.

For any C^2 odd map, differentiating f(-v)=-f(v) twice at v=0
gives D^2f(0)=-D^2f(0), so D^2f(0)=0. This proves (1.4) and
completes the conventional proof of the claimed local lemma.

## 8. A direct consequence useful for a later lower argument

Let F=Atilde-Pi on O. For ||v||inf<=rho0, Taylor's integral formula
applied to t -> D Atilde(tv)[h] uses (1.4) to give exactly

    DF(v)[h]=integral_0^1 (1-t)D^3 Atilde(tv)[v,v,h] dt,
    |DF(v)[h]|<=B ||v||inf^2 ||h||1/2.              (8.1)

If v and v+z belong to the closed rho0 ball, the whole segment does,
so a further integral yields

    |F(v+z)-F(v)|<=B rho0^2 ||z||1/2.               (8.2)

These estimates retain the spatial mass of a localized perturbation.
They do not supply output separation or any adaptive information
inequality, and are not a full signed lower theorem.

## 9. Proof dependencies, correspondence boundaries, and evidence

The mathematical dependency chain is explicit:

    wrapped-Gaussian heat kernel and its Fourier coefficients
      -> actual positive/absolute convolution bounds in L1 and sup norm
      -> Lyapunov--Perron contraction and actual mild-flow identity
      -> mixed graph variational estimates through order three
      -> finite-time actual variational positivity and mixed estimates
      -> ordinary chain rule for the actual Atilde.

Only elementary Banach contraction/implicit differentiation, geometric
and Volterra Neumann series, absolute Fubini estimates, and bounded
mild-solution uniqueness/comparison are used. Each analytical operator
appearing in the L1 route is explicitly constructed. No multilinear
operator-to-product-measure identification, common derivative-dominating
measure, marked-tree representation, or stochastic law is assumed.
The deterministic envelopes already prove the stated inequality, so
outer-tree moments, conditional child independence, and root-displacement
sampling are not premises of this lemma.

In particular this proof does not extend T69/T73's derivative sampler
or its cost theorem to the new kappa. Such an extension must separately
construct the actual changed heat primitive and recheck all moments and
primitive costs. Nor does a finite bound B give an algorithm for its
derivative coefficients or a free Theta, mean, evolved-profile, mass,
or phase oracle. Any later data, coefficient-construction, root-solver,
interpolation, stochastic, or arithmetic work statement must discharge
its own gates. The proof does not change the signed input class.

Sources inspected for setup and boundaries include the R14 candidate,
T65 Sections 2--5, R14b, the T76 supplied-trajectory audit, R14c Sections
1--3, T69's weighted graph and composition sections, T73's exact gate
statement, R10b's actual derivative construction, T68's scope, and
the D29--D33 ledger/checkpoint. These are context and comparisons;
the analytic lemma above is derived here. No T69 second-moment bound
or R14c unreviewed assertion fills a proof step.

Frozen source digests checked during T78:

    T65-local-stable-graph-upper-proof.md
    58e862c9cfbaf0946605d30d9c8e8a37e2570c0c0719d626683f22db60fc9f81
    R14-spectral-gap-extension-candidate.md
    5b113f637b266e558b6f530cbc29049d59ae41141b56a3926fd148d097bedff0
    R14b-local-graph-output-and-root-proof.md
    dff72bd839794df81eb36ac0744dfd5f711de6c2bcb5f8a128b2dd922ca24cf6
    R14c-natural-gap-graph-burnin-proof.md
    89a144617890314a47cbe1f7279053b9ea82c60dd670609739715a2a1ff2abbd
    T76-local-graph-output-root-independent-audit.md
    3a5a785173801120d8ff1a7aa6d8bc4ff0c54eadef54c274a8bb92febd23a58f
    T69-stable-graph-sampler-feasibility.md
    ff537ca6679fdefeefe9c08990194a09f6a2cec23460e1656876e7fdf8a37d9b
    T73-stable-graph-sampler-independent-audit.md
    f21e469f8a15fdebf2293b1cf227e5ec8f3798426f875bdbdcf1641312890df5
    R10b-finite-burnin-derivative-sampling.md
    23683587539ef2905e0679100325808ae3f6353a3782a4bb362b2d24252034f0
    T68-finite-burnin-sampler-independent-audit.md
    442b446ae523b220e34ddadcf8c23b181ce60104100fd27c7e8027524840ed9f

The initial working tree already contained unrelated modifications;
they were preserved. Project instructions, CLAUDE.md, the research
guide, relevant run state, and math-auto-research 0.2.0 defaults,
model-routing, execution guidance, and configured general profile were
read. The skill's configured research preference is gpt-6-astra/max;
this worker made no model-setting change, and its serving backend and
effort are not independently exposed by its tools. Its actual role was
mathematical research and conventional proof authorship.

No new numerical calculation, oracle acquisition, Lean invocation,
implementation test, literature/priority assertion, or auxiliary agent
was used. The proof uses no unproved research lemma, but independent
mathematical audit and full root correspondence acceptance are pending.
The final source hash is reported in the handoff rather than embedded
in this file.
