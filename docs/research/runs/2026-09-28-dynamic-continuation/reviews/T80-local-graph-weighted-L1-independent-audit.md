# T80: independent audit of the local graph weighted-L1 derivative proof

Date: 2026-09-29. Role: independent mathematical research audit.

**Verdict: GO for the exact local analytic theorem in frozen T78.**
The actual normalized unit-torus Allen--Cahn proxy has the stated smoothness,
parity, normalization, and mixed third derivative bound on a neighborhood
of the closed local input ball. No substantive repair, additional input
promise, stochastic representation, or additional research lemma is needed.
The detailed arguments below make the Banach-space and marked-direction
steps independently inspectable.

The sole mathematical acceptance target is
`T78-local-graph-weighted-L1-proof.md`, all 565 lines, with SHA-256

    e9613938316379c257fcaaf2cdc5bbbdfa19c01945a22d647a4e62d75b771a53

Line references below refer to that frozen source. The source was read in
full and its digest was checked. This audit owns only the present file;
the source, claim ledger, run state, code, and other reviews are unchanged.

This GO does not accept R14c or R14d, extend the accepted D29/D33 scope,
or establish a full signed lower, upper, sampling, or work theorem. R14c's
graph definitions and R14d's analytic interface were read as context;
their separate arguments remain the responsibility of their own review.

## 1. Exact accepted statement and quantifiers

Fix d>=1, kappa>0, lambda1=2 pi^2 kappa>1, nu=lambda1-1, and
0<sigma<nu. The measure on X=(R/Z)^d is probability Haar measure.
Let P_t have generator kappa Delta/2 and let S_t be the actual real flow

    u_t=(kappa/2)Delta u+u-u^3.

Pi is Haar averaging, identified with a constant function where needed,
and Q=I-Pi. With the actual centered heat bound M specified in T78, put

    C=M/(nu-sigma)+1/(1+sigma),
    0<R<=1,  C R^2<=1/8,  r=R/(4M).

T78 constructs a C-infinity odd graph Theta on the open mean-zero
sup-norm ball W={||w||inf<3r}. Its graph trajectories solve the actual
PDE and satisfy ||S_t(w+Theta(w))||inf<=R exp(-sigma t).

For each fixed finite L>=0, define

    rho0=min(1/4,r exp(-L)/4),
    O={v in C(X): ||v||inf<2rho0},
    Atilde(v)=exp(-L)[Pi S_Lv-Theta(Q S_Lv)].

The accepted conclusion is that Atilde is defined and C-infinity on O,
is odd, and satisfies

    Atilde(0)=0,
    D Atilde(0)[h]=Pi h,
    D^2 Atilde(0)=0,

and, uniformly for ||v||inf<=rho0,

    |D^3 Atilde(v)[h1,h2,h3]|
      <=B ||h1||inf ||h2||inf ||h3||1

for arbitrary h1,h2,h3 in C(X), with any one label assigned the L1
norm. These are Frechet derivatives on C(X), with the graph derivatives
taken on its closed mean-zero subspace. The theorem is not an assertion
of Frechet differentiability on an open L1 ball.

The graph radius and local input radius impose no sign, mean, support,
or spatial derivative restriction. In particular the conclusion includes
every smooth signed input of the original class that lies in this local
ball. The estimate itself holds for continuous directions with arbitrarily
small support, independently of their derivative norms. Its constants
depend only on fixed d,kappa,sigma,R,L; they need not remain bounded as
nu tends to zero, and no uniformity in L is asserted.

## 2. The heat estimates are estimates for the actual kernel

T78 lines 85--140 pass independently. The wrapped Gaussian with covariance
kappa t has Fourier coefficient exp(-2 pi^2 kappa |m|^2 t), so its
frequency-one decay is exactly lambda1. Positivity, unit mass, and
translation invariance give both spatial contraction bounds and
Pi P_t=Pi. No kappa=1 sampler or changed-symbol argument is used.

For B_t=exp(t)P_tQ, the signed convolution measure is

    beta_t=exp(t)(p_t-1)dx,  t>0,
    beta_0=delta_0-dx.

With q=exp(-lambda1), rhoH=((1+q)/(1-q))^d, and
M=2 exp(lambda1)rhoH, check the two time ranges separately:

1. For 0<=t<=1, ||beta_t||TV<=2 exp(t), and
   2 exp(t)exp(nu t)=2 exp(lambda1 t)<=2 exp(lambda1)<=M.
2. For t>=1, Fourier absolute convergence and |m|^2>=1 for m!=0 give

       ||beta_t||TV
         <=exp(t)exp(-lambda1(t-1)) sum_(m!=0)exp(-lambda1|m|^2)
         <=exp(lambda1)(rhoH-1)exp(-nu t)
         <=M exp(-nu t).

The lattice bound uses n^2>=|n| coordinate by coordinate, including
the zero mode before subtracting one. It has no missing dimension factor.
The short-time argument uses a measure at t=0, where no heat density is
needed. Haar measure is nonatomic because d>=1, so |beta_0|=delta_0+dx.

The decisive L1 fact follows from convolution, not from an arbitrary
sup-norm operator estimate. Namely, with eta=|beta_t|,

    integral_X integral_X |f(x-y)| eta(dy) dx
      =eta(X)||f||1.

Tonelli and translation invariance prove this equality. The analogous
pointwise bound proves the sup-norm estimate. Thus convolution with
|beta_t| dominates B_t in absolute value and has the same displayed
upper bound M exp(-nu t) in both norms. This is a deterministic positive
envelope; a product measure for a multilinear derivative is unnecessary.

## 3. The weighted trajectory operator and its inverse are valid

T78 lines 144--213 pass. For p=1 or infinity, interpret the spatial
Banach space as L1(X) or C(X) with the sup norm, respectively. The space
E_p of continuous trajectories with norm

    ||F||_(sigma,p)=sup_(t>=0)exp(sigma t)||F(t)||p

is Banach: multiplication by exp(sigma t) identifies it with bounded
continuous trajectories in the relevant spatial Banach space. Since Haar
mass is one, the canonical inclusion E_inf -> E_1 is bounded with norm
at most one. It commutes with the operators and Bochner integrals used
here.

For

    (KF)(t)=-integral_0^t B_(t-s)F(s) ds
              +integral_t^infinity exp(t-s)Pi F(s) ds,

the forward weighted bound is

    exp(sigma t) integral_0^t M exp(-nu(t-s))||F(s)||p ds
      <=M||F||_(sigma,p) integral_0^t exp(-(nu-sigma)(t-s))ds.

The backward bound is ||F||_(sigma,p)/(1+sigma). Pi has norm at most
one in either spatial norm, including when its value is treated as a
constant function. Consequently ||K||<=C in both trajectory spaces.
Both integrals are absolutely Bochner integrable in their stated spaces.

Here are explicit continuity details for the source's compact-time/tail
argument. P_t is strongly continuous on C(X) by the approximate-identity
property of the wrapped Gaussian; density of continuous functions and
the L1 contraction extend this to L1(X). B_t is therefore strongly
continuous there as well, including B_0=Q. On any compact time interval,
the forward convolution is continuous by strong continuity, dominated
integration, and the vanishing integration interval at time zero. For
0<=t<=T and A>=T the backward tail after A is bounded by

    ||F||_(sigma,p) exp(T) exp(-(1+sigma)A)/(1+sigma).

It tends uniformly to zero as A tends to infinity. The remaining
compact integral is continuous. Thus K maps the stated continuous
trajectory space into itself. No uniform continuity on the whole half
line and no continuity of a heat density at zero is required.

The trilinear product estimate is also correct: the weighted product
has an extra factor exp(-2sigma t)<=1. It applies with all three
factors in E_inf, or with any selected factor in E_1 and the other two
in E_inf. This directly proves bounded polynomial smoothness on
E_inf; it does not make the cubic smooth on E_1.

For ||w||inf<3r and ||U||_(sigma,inf)<=R,

    ||B_.w+K(U^3)||_(sigma,inf)
      <=M||w||inf+C R^3<3R/4+R/8=7R/8,

and the contraction factor is at most alpha=3 C R^2<=3/8. The fixed
point is strictly inside the radius-R ball. This interior margin makes
the implicit-function argument legitimate at every w in the open W:
the locally produced branch remains within that ball and hence agrees
with the unique contraction solution.

At any such U, T_U Z=K(3U^2 Z) has norm at most alpha on both E_inf
and E_1. Therefore

    (I-T_U)^(-1)=sum_(n>=0)T_U^n,
    ||(I-T_U)^(-1)||<=b0=(1-alpha)^(-1)<=8/5

holds in both spaces. For an E_inf datum, the two inverse series agree
under the canonical inclusion into E_1, since every finite partial sum
agrees and the inclusion is continuous. This is the precise reason the
same inverse can estimate actual C(X)-derivatives in E_1. There is no
additional L1 differentiability or weak-solution identification premise.

## 4. The graph is a graph of actual decaying PDE trajectories

T78 lines 217--256 pass. Applying Pi to the fixed-point equation removes
the centered forward terms and gives

    m(t)=integral_t^infinity exp(t-s)Pi U(s)^3 ds.

It follows that Theta(w)=m(0), QU(0)=w, and
|Theta(w)|<=R^3/(1+3sigma). Splitting the integral defining m(0) at
t gives

    m(t)=exp(t)Theta(w)-integral_0^t exp(t-s)Pi U(s)^3 ds.

Adding the centered fixed-point identity yields

    U(t)=exp(t)P_t(w+Theta(w))
          -integral_0^t exp(t-s)P_(t-s)U(s)^3 ds.

Thus the unstable scalar component has the correct negative-cubic
forward evolution; the backward integral has only selected its initial
value. This identity is the actual mild Allen--Cahn equation. Subtracting
two bounded mild solutions on a finite interval and using the local
Lipschitz constant of the cubic proves uniqueness by Gronwall. The fixed
trajectory is therefore S_t(w+Theta(w)) for every t>=0.

Its initial norm is at most 7R/8<1, using the strict contraction margin
above. Hence the invariant-interval flow used later also covers these
initial data, even if R=1 is permitted in the stated parameters. No
separate smallness condition on |Theta|/r is needed for T78's conclusion.

Sign reversal preserves the fixed-point equation, so uniqueness gives
U_(-w)=-U_w and oddness of Theta. Differentiation at zero gives
DU_0[a]=B_.a and DTheta(0)[a]=Pi B_0a=0 for centered a. Oddness of
the C-infinity map gives D^2Theta(0)=0. All these properties concern
this constructed graph, rather than an assumed global phase coordinate.

## 5. The mixed graph constants and all marked-label placements pass

T78 lines 260--317 pass. Smoothness on C_0(X) was established before
the variational equations are used. With J_i=DU[a_i],
J_ij=D^2U[a_i,a_j], and J_123=D^3U[a1,a2,a3], differentiating the
cubic gives exactly

    (I-T_U)J_i=B_.a_i,
    (I-T_U)J_ij=K(6U J_i J_j),
    (I-T_U)J_123
      =K(6J_1J_2J_3+6U[J_12J_3+J_13J_2+J_23J_1]).

There are three second-derivative placements, each with coefficient six.
The equations hold in E_inf, hence also in E_1. The bounded polynomial
and K justify differentiation of the trajectory equation; no unbounded
time-derivative interchange is being taken on faith.

Using the inverse just checked, define

    K1=b0 M,
    K2=6b0 C R K1^2,
    K3=b0 C(6K1^3+18R K1K2).

For J_i, the E_1 estimate is K1||a_i||1 and the E_inf estimate is
K1||a_i||inf. For J_ij, put whichever label is marked into E_1;
the other J and U remain in E_inf. This gives the claimed K2 estimate
and its symmetric version. For J_123 with label 3 marked, use:

| Forcing term | Factor estimated in E_1 | Other factors |
|---|---|---|
| J_1 J_2 J_3 | J_3 | J_1,J_2 in E_inf |
| U J_12 J_3 | J_3 | U,J_12 in E_inf |
| U J_13 J_2 | J_13, with label 3 marked | U,J_2 in E_inf |
| U J_23 J_1 | J_23, with label 3 marked | U,J_1 in E_inf |

This gives 6K1^3+3(6R K2K1) before applying b0 C, exactly the
displayed K3. The same proof with all factors in E_inf gives the
all-sup bound. Every product and every feedback series converges
absolutely in the required weighted norm.

Finally, F -> Pi F(0) has norm at most one on E_1 and E_inf, so it
transfers these estimates to D^kTheta for k=1,2,3. Frechet derivative
symmetry permits the marked argument in any slot. This supplies the
mixed graph estimate without a multilinear measure representation,
spatial support restriction, or product-measure assumption.

## 6. The actual finite-time flow and its positive envelope pass

T78 lines 321--415 pass, with the following explicit reading of the
existence and comparison argument. Local mild existence follows from
contraction for the polynomial on a short interval. The difference
of two locally bounded solutions solves a linear equation with bounded
potential 1-(u^2+uv+v^2). For any bounded potential a(t,x), adding a
sufficiently large scalar A makes a+A nonnegative. Iteration around
exp(-A(t-s))P_(t-s) is positive and converges by a factorial Volterra
bound. Applying this to comparison with the constant solutions +/-1
proves invariance of [-1,1]. Uniform local existence times on this
bounded set then give global continuation for ||v||inf<1.

For a fixed [0,L], the mild equation is a bounded polynomial equation
on C([0,L];C(X)). Its derivative with respect to the trajectory is
I+V_u, where

    V_u z(t)=integral_0^t exp(t-s)P_(t-s)3u(s)^2 z(s) ds.

The n-fold time simplex has volume at most L^n/n!, so
||V_u^n||<=(3 exp(L)L)^n/n!. Consequently sum_n(-V_u)^n is an
absolutely convergent inverse. The implicit theorem gives C-infinity
dependence on v on the open unit ball, without any smallness requirement
on L. Evaluation at L is continuous. At L=0 the same conclusion is
simply S_0=I.

For the first variational propagator E_u(t,s), the potential is
1-3u^2, lying in [-2,1]. The shifted representation with free
semigroup exp(-2(t-s))P_(t-s) has nonnegative multiplier 3-3u^2.
Its convergent iteration proves positivity. Rewriting with scalar
coefficient +1 then gives, for f>=0,

    0<=E_u(t,s)f
       =exp(t-s)P_(t-s)f
          -integral_s^t exp(t-a)P_(t-a)3u(a)^2 E_u(a,s)f da
       <=exp(t-s)P_(t-s)f.

For signed f, positivity gives |E_u(t,s)f|<=E_u(t,s)|f|. Integration
in x and Haar mass preservation therefore imply

    ||E_u(t,s)f||p<=exp(t-s)||f||p,  p=1,infinity.

This bound applies directly to continuous directions and sources.
It does not claim that the signed centered semigroup QP_t is positive.
The inhomogeneous Duhamel formula follows by substitution into the
Volterra equation and Fubini; bounded coefficients and a finite time
interval make all of those integrals absolutely convergent. Joint
strong continuity of the propagator follows from its uniformly
convergent Volterra series on each fixed compact interval.

The actual derivative equations are

    Y_i(t)=E_u(t,0)h_i,
    Y_ij(t)=-6 integral_0^t E_u(t,s)[uY_iY_j](s) ds,
    Y_123(t)=-6 integral_0^t E_u(t,s)
       [Y_1Y_2Y_3+u(Y_12Y_3+Y_13Y_2+Y_23Y_1)](s) ds.

Both the cubic signs and coefficients are correct. Using one L1 block
containing the marked label, and sup norms for all other blocks, gives

    c1(t)=exp(t),
    c2(t)=6t exp(2t),
    c3(t)=(6t+54t^2)exp(3t).

Independently, the second-order integrand is at most
6 exp(t-s)exp(2s), whose integral is <=6t exp(2t). At third order
each paired term is bounded by 6s exp(3s), so the entire integrand is

    (6+108s)exp(t+2s)<=(6+108s)exp(3t).

Its integral is exactly the stated upper bound. The third label is
placed in Y_3, Y_3, Y_13, or Y_23 in the four forcing terms,
respectively. The all-sup estimates follow by the same calculation.
The estimates hold for arbitrary continuous directions and incur no
L2 norm, support-width factor, or derivative-norm factor.

Integrating DS_t(theta v)[v] for theta in [0,1] also justifies
||S_tv||inf<=exp(t)||v||inf on the open unit ball. This step uses
the actual differentiable flow, and S_t0=0, so it is not a separate
linearized approximation to the nonlinear solution.

## 7. Domain buffer, chain rule, and normalization pass

T78 lines 419--473 pass. Since 2rho0<=1/2, the whole open O lies
strictly inside the unit ball where the finite-time flow estimates hold.
For v in O,

    ||Q S_Lv||inf<=2 exp(L)||v||inf
      <4 exp(L)rho0<=r<3r.

For the closed rho0 ball the stronger bound <=r/2 holds. Thus the
full closed local input ball has an actual open neighborhood on which
the composition is defined; no boundary derivative or silent domain
restriction occurs. The graph estimates are uniform on all of W,
so no compactness of an infinite-dimensional input ball is needed.

Set W_L(v)=Q S_Lv. The operator Q has norm at most two in both L1
and sup norm, so every derivative D^kW_L for k<=3 has the relevant
mixed or all-sup constant 2c_k(L). Each such derivative is centered,
making it an admissible direction for a derivative of Theta.

The ordinary third-order chain rule contains exactly

    D^3Theta[W_1,W_2,W_3],
    D^2Theta[W_12,W_3],
    D^2Theta[W_13,W_2],
    D^2Theta[W_23,W_1],
    DTheta[W_123].

In each term a unique block contains label 3. Its mixed bound uses
||h3||1, and all remaining directions use their sup norms. The first
term therefore contributes 8K3 c1^3, the three middle terms contribute
3(4K2 c2c1)=12K2 c2c1, and the last term contributes 2K1 c3. Also
|Pi D^3S_L| is bounded by the mixed L1 estimate c3. It follows that

    B=exp(-L)[c3+8K3 c1^3+12K2 c2c1+2K1 c3]

is valid, with c_k=c_k(L). It is finite and nonnegative for every
fixed permitted parameter choice. These bounds actually hold uniformly
on O and therefore imply the stated closed-ball estimate. At L=0,
c1=1 and c2=c3=0, so B=8K3, which is the correct direct bound for
Atilde=Pi-Theta composed Q; there is no excluded zero-time case.

Uniqueness makes S_L odd. Since Theta is odd and Q linear, Atilde is
odd and Atilde(0)=0. At zero, DS_L(0)=exp(L)P_L and DTheta(0)=0;
hence

    D Atilde(0)=exp(-L)Pi exp(L)P_L=Pi.

Twice differentiating oddness at zero gives D^2Atilde(0)=0. The
normalizing exp(-L) is therefore exact, including for nonzero-mean
directions. No phase asymptotics or positive-time limit is involved.

## 8. Taylor consequence and compatibility with separate interfaces

T78 lines 475--490 also pass. Put F=Atilde-Pi and apply the one-variable
Taylor formula to q(t)=D Atilde(tv)[h]. Its first derivative at zero
is zero and its second derivative is D^3Atilde(tv)[v,v,h]. Thus

    DF(v)[h]=integral_0^1(1-t)D^3Atilde(tv)[v,v,h]dt,
    |DF(v)[h]|<=(B/2)||v||inf^2||h||1.

If v and v+z are in the closed rho0 ball, convexity keeps the entire
joining segment in the ball. Integrating the last estimate along that
segment gives |F(v+z)-F(v)|<=(B/2)rho0^2||z||1. The factor one-half
is correct. This is a local influence estimate, not output separation
or an information inequality.

R14c Sections 1--3 use exactly the same M, sigma, K, r=R/(4M),
fixed-point equation, and definition Theta=Pi U(0), with stronger
smallness conditions on R for separate output/root purposes. Choosing
the same R satisfies the weaker T78 conditions automatically. Uniqueness
of the fixed point in the same radius-R trajectory ball identifies the
graphs. This correspondence uses only the definitions and the contraction
proved above, and imports no R14c burn-in or output assertion.

For a separately reviewed composition requesting R14d's local analytic
interface, T78 supplies a_star=rho0 and the displayed B, or max(1,B)
if that interface normalizes B>=1. The identity
exp(T-L)H(v)=exp(T)Atilde(v) is merely definitional. This compatibility
does not accept any later prior, lower-bound, upper-bound, or work proof.

## 9. Completion status, evidence, and limits

There is no substantive mathematical correction to request. The explicit
continuity argument, compatibility of the two Neumann inverses, shifted
comparison construction, and marked-label accounting in this report
complete routine compressed details already justified by T78's bounds.
They preserve all constants, quantifiers, and input domains. No additional
localized assumption is introduced.

The accepted dependency chain is entirely deterministic:

    actual kappa heat convolution
      -> L1 and sup bounds for K and its feedback inverse
      -> actual smooth decaying graph and mixed graph derivatives
      -> actual finite-time positive variational flow
      -> five-term composition and normalization.

In particular this audit does not assume or supply a common derivative
dominating measure, product-measure theorem, tree sampler, unbiased
coefficient construction, changed-diffusivity primitive cost, finite
second moment, or free mean/Theta/PDE/phase oracle. It establishes neither
full-class burn-in nor long-time output separation. It does not prove a
signed prior, adaptive information inequality, query lower bound, upper
algorithm, base evaluation algorithm, arithmetic work theorem, finite-bit
bound, or extension of the old global phase theorem. Those claims require
their own object-level correspondence and independent review.

This was a conventional mathematical audit. No numerical experiment,
symbolic/numerical falsification run, PDE solve, unknown-input point query,
Lean invocation, implementation test, or literature/novelty search was
performed or claimed. A Lean source toolchain file was read for context;
that is not a build. The shell commands used for evidence were file
discovery/reading, line counting, SHA-256 provenance checks, and working-tree
inspection. The preexisting unrelated modifications were preserved.

Project instructions, CLAUDE.md, the research guide, relevant claim/run
checkpoint context, and math-auto-research 0.2.0 defaults, model-routing,
execution guidance, and configured general reader profile were inspected.
The dispatch explicitly requested the configured mathematical-research
role gpt-6-astra/max; the serving backend/effort are not independently
exposed inside this worker. No model-setting change, auxiliary agent,
or model-usage total is claimed.

Final disposition: **GO for frozen T78's local analytic lemma and its
stated Taylor consequence only.** Root correspondence acceptance and
any ledger promotion remain separate. The audit file's final digest is
reported in the handoff rather than embedded in its own contents.
