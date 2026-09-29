# T82: the full Hamming prior gives the signed lower bound for every fixed positive diffusivity

Date: 2026-09-29. Conventional proof candidate; independent research audit
and root correspondence review remain required before acceptance. This is
the sole T82 edit. Existing sources, ledgers, code, formal files and
numerical artifacts are unchanged by this task.

The proposed extension closes: for every fixed kappa>0 and fixed integers
d,s>=1, the same full signed input class and exact initial-value oracle
have the expected-query lower exponent 2d/(2s+d). The argument uses the
actual flow at time one, concentration of its whole spatial profile on
the unconditioned Hamming layers, and subsequent actual PDE estimates.
It requires neither lambda1=2 pi^2 kappa>1 nor a stable graph or global
phase. All constants and the all-large-horizon threshold are specified
below. This file does not claim an accepted theorem, a matching upper
bound, full formalization, numerical evidence, or novelty.

## 1. Exact claim and information model

Let X=(R/Z)^d carry normalized Haar measure. Fix integers d,s>=1,
kappa>0, and a target x* in X. Write P_t for the heat semigroup of
(kappa/2)Delta and S_t for the actual real Allen--Cahn flow

    u_t=(kappa/2)Delta u+u-u^3,   u(0)=v.

Set lambda=2 pi^2 kappa>0. This is the first positive heat eigenvalue;
it may be below, equal to, or above one. Let Pi be spatial averaging
and Q=I-Pi. The fixed input class is exactly the D28 class

    V={v smooth periodic real:
       ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.                              (1.1)

Only derivatives through the fixed total order s are uniformly bounded.
No bound on all higher derivatives or common analytic radius is assumed.

Claim. There are C>0 and T0<infinity, depending only on the fixed public
parameters and a fixed bump, such that for every real T>=T0 and every
admissible randomized estimator H_T with

    sup_(v in V) E|H_T(v)-S_Tv(x*)|^2<=1/16,

one has

    sup_(v in V) E Q_T(v)>=C exp(2dT/(2s+d)).        (1.2)

In fact an explicitly specified finite prior on V, depending on T and
the public parameters but chosen independently of the algorithm, has
average expected query count at least the right side of (1.2).

The oracle supplies only exact initial point values. Every acquisition,
including preprocessing and repeated evaluations, is charged. Query
points, stopping and output may depend measurably on the transcript and
an input-independent random seed; the algorithm halts almost surely on
each input. Biased and unbounded real outputs are allowed. No formula,
source, derivative, mass, Fourier, evolved-value, or input-dependent
metadata oracle is supplied. Arithmetic is free for this lower bound.
The analytic quantities below are proof devices, not extra observations.

The expensive member may depend on both T and the algorithm. The claim
does not select one common expensive baseline or one fixed hard profile
for every horizon.

## 2. Actual finite-time flow and a cubic mean correction

For ||v||inf<1, the actual solution exists globally and stays in [-1,1].
Indeed the cubic is locally Lipschitz on C(X), so its mild equation has
local solutions; comparison with the stationary solutions +/-1 prevents
finite-time escape. A difference of two bounded solutions satisfies a
linear parabolic equation with a bounded potential, giving comparison
and uniqueness. These are statements about the actual unmodified cubic.

For clarity, the finite-time differentiation needed here can be obtained
directly from

    S_tv=exp(t)P_t v
          -integral_0^t exp(t-r)P_(t-r)(S_rv)^3 dr.  (2.1)

On C([0,1];C(X)), the derivative in the trajectory of the left side
after moving the integral to the left is I+V_u, where V_u is a Volterra
operator with integrand 3u(r)^2 and ||u||inf<=1. Its n-fold iterate has
norm at most (3e)^n/n!. Thus the inverse Neumann series converges, and
the implicit function theorem gives C-infinity dependence on v throughout
the open unit ball. The displayed derivative bounds below are uniform
there. No infinite-time integral or graph construction is differentiated.

Let E_u(t,r) be the actual propagator with potential 1-3u(t,x)^2.
Writing its equation with free coefficient -2 leaves the nonnegative
multiplier 3-3u^2. Positive Volterra iteration therefore proves positivity.
Writing it instead with free coefficient +1 and using that positivity
proves, for arbitrary continuous signed h,

    |E_u(t,r)h|<=exp(t-r)P_(t-r)|h|.                (2.2)

The factorial Volterra bound justifies the iterations on every bounded
time interval. Heat preservation of Haar mass makes (2.2) an L1 bound
as well as a sup-norm bound. In particular

    ||S_tv||inf<=exp(t)||v||inf,   0<=t<=1,         (2.3)

by integrating DS_t along the segment from zero to v.

For disjoint derivative labels, the actual variations satisfy

    Y_i(t)=E_u(t,0)h_i,
    Y_ij(t)=-6 integral_0^t E_u(t,r)[u Y_i Y_j](r) dr,
    Y_123(t)=-6 integral_0^t E_u(t,r)
       [Y_1Y_2Y_3+u(Y_12Y_3+Y_13Y_2+Y_23Y_1)](r) dr. (2.4)

Put one specified input direction in L1 and all the others in sup norm.
In every product in (2.4), exactly one factor carries that label. From
(2.2), |u|<=1, and Holder's product inequality, induction gives

    ||D^j S_t(v)[h1,...,hj]||1
      <=c_j(t) product_(i<j)||hi||inf ||hj||1,
    c_1(t)=exp(t),
    c_2(t)=6t exp(2t),
    c_3(t)=(6t+54t^2)exp(3t),   0<=t<=1.           (2.5)

The all-sup version has the same constants. To check the third constant,
the ternary term contributes 6 exp(t+2r), and the three paired terms
together contribute 108r exp(t+2r). Their integral is at most
(6t+54t^2)exp(3t). Assigning the L1 norm to whichever factor carries
the marked label retains its original L1 direction norm in every term.
No small-time heat-density supremum is used in (2.5).

Define the finite-time scalar and its correction by

    A1(v)=exp(-1)Pi S_1v,
    F(v)=A1(v)-Pi v,
    B=60e^2.                                       (2.6)

It follows from (2.5) that

    |D^3 A1(v)[h1,h2,h3]|
       <=B||h1||inf||h2||inf||h3||1.                (2.7)

This finite B works for every kappa>0; the later heat bounds depend on
kappa. Oddness of the PDE makes A1 and F odd. At zero,
DS_1(0)=e P_1, so DA1(0)=Pi and DF(0)=0. Odd smoothness gives
D^2A1(0)=D^2F(0)=0. Taylor's formula for DF along rv therefore gives

    DF(v)[h]=integral_0^1(1-r)D^3A1(rv)[v,v,h] dr,
    |DF(v)[h]|<=(B/2)||v||inf^2||h||1.              (2.8)

The map A1 is simply a rescaled time-one mean. No phase identity or
stable-manifold property is attributed to it.

## 3. The original full-layer bump prior and its scale

Choose once and for all psi in C_c^infinity((0,1)^d) with 0<=psi<=1
and I=integral psi>0. Put

    Dpsi=max(1,max_(|alpha|<=s)||partial^alpha psi||inf),
    a=1/(8Dpsi),   q=s+d/2.

For an even positive integer k, let K=k^d, A=a k^(-s), and

    v_xi(x)=sum_j xi_j A psi(kx-j),   xi_j in {-1,+1}, (3.1)

where j ranges over the k^d half-open torus cells and each bump is
extended by zero. Compact interior support gives a smooth periodic
extension. Disjoint supports give ||v_xi||inf<=A<=1/8 and

    ||partial^alpha v_xi||inf
      <=a Dpsi k^(|alpha|-s)<=1/8,   |alpha|<=s.      (3.2)

Let ell be even with sqrt(K)<=ell<=2sqrt(K)<=K/4. Denote by pi_ell
the full uniform law on sign vectors with sum ell, and similarly define
pi_minus_ell and the balanced layer pi_0. All vectors in the two biased
layers have both signs. Since psi has positive mass, every such profile,
including all exceptional profiles below, belongs to (1.1). Their
spatial means are exactly +/-m, where

    m=A I ell/K>0.                                 (3.3)

For each public horizon T use exactly the earlier even-grid choices

    R_T=(a I exp(T))^(1/q),
    k=2 floor(R_T/2),   K=k^d,
    ell=2 ceil(sqrt(K)/2).                          (3.4)

For R_T>=4, R_T/2<=k<=R_T. Once K>=2048, ell has the preceding
parity and size bounds. The exact scale identity is

    exp(T)m=(R_T/k)^q ell/sqrt(K).

Consequently

    1<=exp(T)m<=2^(q+1),
    A/sqrt(K)=a k^(-q)<=2^q I^(-1)exp(-T),
    log K<=d T/q.                                  (3.5)

The last inequality uses k<=R_T and aI<=1/8<1. The explicit threshold
in Section 7 ensures all of these conditions at every real T>=T0.

## 4. A finite slice lemma with an explicit martingale tail

The following argument applies to any real function f on {-1,+1}^K
whose value changes by at most L>0 under one coordinate flip. A swap of
opposite signs then changes it by at most 2L. Spatial permutation
invariance is not required.

If f is odd under simultaneous sign reversal, E_pi0 f=0. Starting with
a uniform balanced vector, choose uniformly ell/2 of its negative
coordinates and flip them. The resulting positive set has size
(K+ell)/2 and is uniform: every final set has the same number of
balanced predecessors, and every predecessor/added-subset pair has
the same probability. A path of ell/2 flips therefore proves

    |E_piell f|<=ell L/2.                           (4.1)

The negative layer has the same bound by sign reversal.

For concentration under either fixed layer, reveal coordinates in a
fixed order and set M_j=E[f | first j coordinates], j=0,...,K.
Fix a possible prefix and suppose both next signs are possible. The
positive suffix set has size r if the next sign is positive and r+1
if it is negative. Couple the two laws by taking a uniform r-subset of
the suffix positions, then adding one uniformly chosen point from its
complement. The enlarged subset is uniform, because each (r+1)-subset
has exactly r+1 predecessors with equal pair probabilities. The two
full sign vectors differ by swapping the next coordinate with that
added suffix coordinate. Hence the two conditional expectations of f
differ by at most 2L. If the next sign is forced, the increment is zero.

Thus, conditionally on every prefix, M_j-M_(j-1) is centered and lies
in an interval of length at most 2L. Its conditional variance is at
most p(1-p)(2L)^2<=L^2, where p is the conditional probability of the
next positive sign. Finite martingale orthogonality gives

    Var(f)<=K L^2.                                 (4.2)

For completeness the required conditional exponential bound follows
without an independence assumption. If a centered variable Z lies in
an interval of length 2L, the second derivative of
log E exp(theta Z) is its variance under the exponentially tilted law.
That variance is at most L^2: squared distance from the interval's
midpoint is at most L^2, and variance is no larger. Integrating twice
from theta=0, where the log moment and its first derivative vanish,
proves E exp(theta Z)<=exp(theta^2 L^2/2) for every real theta.
Apply this conditionally to each martingale increment and iterate
conditional expectations. The result is

    E exp(theta(f-Ef))<=exp(K theta^2 L^2/2).

Optimizing the exponential Markov bound at theta=z/(K L^2), and
then doing the same for -f, yields

    P(|f-Ef|>z)<=2 exp(-z^2/(2K L^2)),   z>0.       (4.3)

All laws in this proof are uniform fixed-cardinality subset laws.
Neither independent signs nor conditioning on a PDE-good event occurs.

## 5. Two good events under each full layer

### 5.1 The time-one mean has the prescribed sign

The difference between two data in (3.1) separated by one sign flip has
L1 norm exactly 2A I/K. Their joining segment has sup norm at most A<1.
Equation (2.8) gives

    |F(v_xi)-F(v_flip_i xi)|<=B I A^3/K
      <=L_F:=B A^3/K.                              (5.1)

The correction as a function of xi is odd. Equations (4.1)--(4.2)
therefore imply, on each layer,

    |E F|<=B A^3 ell/(2K),
    Var(F)<=B^2 A^6/K.                             (5.2)

Assume A^2<=I/(64B). Then |E F|/m<=B A^2/(2I)<=1/128<1/8.
If |F|>m/4, then |F-EF|>m/8. Chebyshev and ell^2>=K give

    P(|F|>m/4)<=64 B^2 A^4 K/(I^2 ell^2)
      <=64 B^2 A^4/I^2<=1/64.                     (5.3)

On the positive good event, the actual time-one mean b1 satisfies

    b1=Pi S_1v=e(m+F(v))>=3e m/4.                 (5.4)

On the negative good event it satisfies b1<=-3e m/4.

### 5.2 The entire time-one profile is small

Here positive diffusivity is essential. Set the fixed constants

    rho=((1+exp(-lambda))/(1-exp(-lambda)))^d,
    Ccell=2e rho,
    Gkappa=(1+2e)sqrt(d/kappa).                     (5.5)

The Fourier heat series and n^2>=|n| for integer n show

    ||p_1||inf<=sum_(n in Z^d) exp(-lambda |n|^2)
      <=rho,   ||p_1||2<=rho.                     (5.6)

For any fixed x, let f_x(xi)=S_1v_xi(x). Integrating the first
variation bound (2.2) along a one-flip segment gives

    |f_x(xi)-f_x(flip_i xi)|
      <=e rho (2A I/K)<=Ccell A/K=:L_x.            (5.7)

Oddness and (4.1), using ell<=2sqrt(K), show uniformly in x that

    |E f_x|<=Ccell A/sqrt(K).                      (5.8)

Equation (4.3) gives the actual full-layer pointwise tail

    P(|f_x-E f_x|>z)
      <=2 exp(-K z^2/(2 Ccell^2 A^2)).              (5.9)

We next justify a deterministic spatial Lipschitz bound. Periodizing
the Gaussian kernel with covariance kappa t I_d gives

    integral_X |grad p_t(x)| dx
      <=integral_(R^d) |grad g_(kappa t)(x)| dx
      <=sqrt(d/kappa) t^(-1/2).

The last bound is E|Z|/(kappa t)<=sqrt(d/(kappa t)) for
Z~N(0,kappa t I_d). Absolute convergence permits periodization and
differentiation. Thus

    ||grad P_t h||inf<=sqrt(d/kappa)t^(-1/2)||h||inf.

Use the actual mild equation with heat semigroup P_t and source u-u^3.
For |u|<=1, |u-u^3|<=|u|, while (2.3) gives ||u(r)||inf<=e^r A.
The integrable (1-r)^(-1/2) bound then gives

    ||grad S_1v_xi||inf
      <=sqrt(d/kappa)[A+integral_0^1(1-r)^(-1/2)e^r A dr]
      <=Gkappa A.                                  (5.10)

In particular no derivative bound depending on k enters the spatial
net. One may first differentiate the mild integral away from r=1 and
pass to the limit using the displayed integrable majorant; the smooth
inputs here also give ordinary spatial derivatives at time one.

Let

    N_K=ceil(sqrt(d)Gkappa sqrt(K)),
    M_K=N_K^d,
    Cnet=(1+sqrt(d)Gkappa)^d.

Take the equally spaced N_K-point grid in each coordinate of X. Every
point has torus distance at most sqrt(d)/(2N_K) from this grid, so
(5.10) makes its profile value differ from a grid value by at most
A/(2sqrt(K)). Also

    M_K<=Cnet K^(d/2).                              (5.11)

At every grid point apply (5.9) with

    z_K=Ccell A/sqrt(K) sqrt(2 log(128 M_K)).

The bound is 1/(64 M_K) per point. The finite union bound, followed
by (5.8) and the spatial interpolation just proved, yields

    P(||S_1v||inf>
       (A/sqrt(K))[Ccell(1+sqrt(2log(128 M_K)))+1/2])
       <=1/64.                                     (5.12)

This is an unconditioned probability under each full layer, and the
same deterministic grid works for every configuration.

To simplify the subsequent constants, for K>=2 put

    beta=log(128 Cnet)/log(2)+d/2,
    H=(Ccell+1/2)/sqrt(log(2))+Ccell sqrt(2 beta),
    C0=(2^q H/I)sqrt(d/q).                          (5.13)

Equations (5.11) and log K>=log 2 imply
log(128 M_K)<=beta log K. Hence (5.12) proves, except with
probability at most 1/64,

    ||S_1v||inf<=H(A/sqrt(K))sqrt(log K)
      <=C0 exp(-T)sqrt(T).                          (5.14)

The last step is (3.5). Orthogonal projection in normalized L2 gives

    W1:=||Q S_1v||2<=||S_1v||2
       <=C0 exp(-T)sqrt(T).                         (5.15)

Let G_plus and G_minus denote the intersections of (5.3)'s good mean
event and (5.14)'s good profile event in their respective layers.
The union bound proves

    pi_ell(G_plus^c)<=1/32,
    pi_minus_ell(G_minus^c)<=1/32.                  (5.16)

The full prior is retained. These good events are used only to bound
its average testing error, never to redefine its distribution.

## 6. Actual evolution from time one at an arbitrary positive heat gap

Fix a configuration satisfying both good conditions. For t>=0 write

    u(t)=S_(1+t)v,   b(t)=Pi u(t),   w(t)=Q u(t),
    b(0)=b1,   ||w(0)||2=W1.

The actual solution remains in [-1,1]. For positive times its centered
energy identity is

    (1/2)d||w||2^2/dt
       =-(kappa/2)||grad u||2^2+||w||2^2
          -integral w(u^3-b^3)
       <=(1-lambda)||w||2^2.                       (6.1)

The last integral is nonnegative because the cube is increasing, and
unit-torus Poincare gives ||grad u||2^2>=4 pi^2||w||2^2. Therefore

    ||w(t)||2<=exp((1-lambda)t)W1.                  (6.2)

No decay assumption is made in (6.2). It is valid also when lambda<1
and its right side grows in t.

Spatial integration gives the exact scalar equation

    b'=b-b^3-R,
    R=3b Pi(w^2)+Pi(w^3),
    |R(t)|<=5||w(t)||2^2.                          (6.3)

Here |b|<=1 and ||w||inf<=2. Let z(t)=phi_t(b1), where

    phi_t(c)=c exp(t)/sqrt(1+c^2(exp(2t)-1))

is the exact solution of z'=z-z^3, z(0)=c, for c in [-1,1].
For delta=b-z the exact difference equation has coefficient

    delta'=[1-(b^2+bz+z^2)]delta-R.

Since b^2+bz+z^2>=0, the scalar integrating-factor formula gives

    |b(t)-phi_t(b1)|
      <=5 exp(t)W1^2 J_lambda(t),
    J_lambda(t)=integral_0^t exp((1-2lambda)r) dr.   (6.4)

This uses the one-sided bound on the actual difference coefficient;
it does not replace it by an incorrectly asserted absolute Lipschitz
constant one for the cubic.

At t=T-1 and T>=2, (5.15) makes the right side of (6.4)

    <=5 C0^2 T exp(-T-1) J_lambda(T-1).

Define mu=min(1,2lambda)>0. For all lambda>0,

    J_lambda(T-1)
      <=T exp(max(0,1-2lambda)T),

so the convenient uniform bound is

    |b(T-1)-phi_(T-1)(b1)|
      <=Emean(T):=5 C0^2 T^2 exp(-mu T).            (6.5)

This includes lambda=1/2, when J_lambda(t)=t. More precisely (6.4)
has order T exp(-2lambda T) for lambda<1/2, T^2 exp(-T) at
lambda=1/2, and T exp(-T) for lambda>1/2. Only the coarser bound
(6.5) is needed, and it tends to zero for every fixed lambda>0.

The target is a point value, so the centered part must also be bounded
in sup norm. For any t>=1 set a_t=t-1. Compare u(a_t+h), 0<=h<=1,
with the spatially constant scalar solution c(h)=phi_h(b(a_t)).
Their difference solves the actual linear parabolic equation with
potential

    1-[u(a_t+h,x)^2+u(a_t+h,x)c(h)+c(h)^2]<=1

and initial difference w(a_t). Both solutions lie in [-1,1]. Positivity
and comparison, as in (2.2), imply

    ||u(t)-c(1)||inf
      <=e||P_1(|w(a_t)|)||inf
      <=e rho ||w(a_t)||2.

Subtracting the spatial mean costs at most a factor two. Thus (6.2)
gives, without any sign restriction on 1-lambda,

    ||w(t)||inf<=2e rho exp((1-lambda)(t-1))W1.      (6.6)

Inserting t=T-1 and (5.15), define

    Cw=2e rho C0 exp(2(lambda-1)),
    Espace(T)=Cw sqrt(T) exp(-lambda T).

Then

    ||w(T-1)||inf<=Espace(T),   T>=2.               (6.7)

Equations (6.5) and (6.7) prove the actual pointwise approximation on
the good configurations,

    |S_Tv(x)-phi_(T-1)(b1)|
      <=Emean(T)+Espace(T),   every x in X.         (6.8)

The source of decay for small lambda is the time-one prior bound
W1=O(exp(-T)sqrt(T)); no stable graph or uniform decay of arbitrary
centered initial profiles has been assumed.

## 7. Explicit all-large-horizon thresholds and separation

Choose an integer k_*>=4 such that

    k_*^d>=2048,
    a^2 k_*^(-2s)<=I/(64B).                        (7.1)

Such an integer exists because s>=1. The fixed amplitude a<=1/8
already keeps every joining segment inside the open unit ball.
Set

    Tgrid=q log(2k_*)-log(aI),
    Tmean=(2/mu) max(0,log(2560 C0^2/mu^2)),
    Tspace=(2/lambda) max(0,log(64 Cw/sqrt(lambda))),
    T0=max(2,Tgrid,Tmean,Tspace).                   (7.2)

Every constant in (7.2) was defined from d,s,kappa and the fixed bump.
For T>=Tgrid, R_T>=2k_* and k>=R_T/2>=k_*, so all conditions in
Sections 3 and 5 hold, including (7.1). This is true between grid
jumps as well as at them.

The elementary inequalities exp(x)>=x^2/2 and exp(x)>=x for x>=0
give

    Emean(T)<=40 C0^2 mu^(-2) exp(-mu T/2),
    Espace(T)<=Cw lambda^(-1/2) exp(-lambda T/2).

Thus T>=Tmean and T>=Tspace make the two errors at most 1/64 each,
including when the displayed logarithm is negative. Equation (6.8)
then has error at most 1/32 for every T>=T0.

On G_plus, (5.4) and (3.5) give exp(T-1)b1>=3/4. For c>=0,

    phi_t(c)>=Psi(exp(t)c),   Psi(y)=y/sqrt(1+y^2),

because its denominator sqrt(1+exp(2t)c^2-c^2) is at most
sqrt(1+exp(2t)c^2). Hence

    S_Tv(x*)>=Psi(3/4)-1/32=91/160>1/2.            (7.3)

Oddness, or the corresponding negative inequalities in the same proof,
gives

    S_Tv(x*)<=-91/160<-1/2   on G_minus.            (7.4)

These are actual PDE targets. The scalar approximation starts from the
actual mean after time one, and its later forcing error was paid in
(6.4)--(6.5); it is not a scalar evolution assumption for the original
mean. Equations (5.16), (7.3) and (7.4) are the complete PDE separation
interface needed for the original information argument.

## 8. Full-prior testing, adaptive exact values, and expected cost

Keep the equal mixture of the two full uniform layers from Section 3.
On each good input, thresholding an estimator satisfying the MSE premise
at zero gives the prescribed sign with error probability at most 1/4:
a wrong sign requires absolute estimation error greater than 1/2, and
Markov bounds its probability by 4*(1/16). On a bad input use the bound
one. Since each layer has bad mass at most 1/32, the full-prior Bayes
error of this sign test is at most

    1/4+1/32=9/32.                                 (8.1)

No change of the prior was made to obtain (8.1). In particular the
PDE-good event need not preserve exchangeability.

For the information lower bound, give the algorithm the entire sign
of the half-open cell containing each queried point. This strengthens
the original oracle: its exact value is a known function of this sign
and the point, including at zeros of psi and cell boundaries. Repeated
cells add no new sign information, but every original acquisition is
still counted. For a procedure capped at

    n=floor(K/1024)

original queries, pad its distinct revealed cells to n by querying
unused cells in any fixed rule. Conditional on a fixed seed and any
revealed signs and indices, unused signs are exchangeable under either
full layer. The next adaptively selected unused cell therefore has the
ordinary without-replacement law. The original queried locations,
values, stopping and decision can all be reconstructed from the seed
and the padded sign sequence. This accounts for all their information
by data processing; no independent noisy coin oracle is substituted.

At a sign prefix of length j<n with z positive signs, the two conditional
next-positive probabilities are

    p_plus=[(K+ell)/2-z]/(K-j),
    p_minus=[(K-ell)/2-z]/(K-j).                    (8.2)

Every such prefix has positive probability under both hypotheses,
because each sign count in each layer is at least 3K/8>n. Using
j<=K/8 and ell<=K/4 gives

    p_minus>=1/4,
    p_minus<=4/7<3/4,
    |p_plus-p_minus|=ell/(K-j)<=2ell/K.

For Bernoulli laws, log x<=x-1 gives

    KL(Ber(p_plus)||Ber(p_minus))
      <=(p_plus-p_minus)^2/[p_minus(1-p_minus)]
      <=64 ell^2/(3K^2)<=256/(3K).                 (8.3)

The finite chain rule and n<=K/1024 give padded-transcript KL<=1/12.
The seed has the same input-independent distribution under both
hypotheses, so averaging conditional KL over it changes nothing.
Adaptive indices and original values are already functions of this
augmented transcript. Pinsker yields total variation at most
sqrt(1/24)<1/4. Therefore every capped sign decision has equal-prior
error at least

    (1-TV)/2>=3/8.                                 (8.4)

Let qbar be the average expected number of original queries under the
full finite prior. If qbar=infinity, the claimed bound is immediate.
Otherwise truncate the original sign decision before its (n+1)-st
query and output any fixed sign there. This changes its decision only
on {Q>n}, whose prior probability is at most qbar/n. Combining
(8.1) and (8.4) gives

    3/8<=9/32+qbar/n,
    qbar>=3n/32>=3K/65536.                         (8.5)

The final inequality uses K>=2048, so floor(K/1024)>=K/2048.
Random stopping, rare expensive runs, biased outputs, and unbounded
real outputs are all covered. The proof uses only MSE and the bounded
sign decision. For each fixed T the prior has finitely many inputs,
so their exceptional seed null sets for almost-sure halting can be
discarded simultaneously. The truncation and padding are measurable
under the stated original oracle rules.

Finally k>=R_T/2 in (3.4) gives

    qbar>=3*2^(-d-16)*(aI)^(d/q) exp(dT/q)
         =C exp(2dT/(2s+d)),
    C=3*2^(-d-16)*(aI)^(d/q)>0.                    (8.6)

The prior is fixed before the algorithm, and its average lower bound
implies the worst-input expected-query bound (1.2). Any separate cost
notion which charges at least one unit per original query inherits the
same lower bound; no matching arithmetic upper bound is asserted here.

## 9. Dependence, scope, and review status

This proof uses only actual finite-time semilinear flow estimates,
positive heat smoothing, full-layer finite martingales, centered L2
energy, scalar comparison and the unchanged exact-value information
argument. The stable graph and the global phase are not premises.
The three analytic steps specific to this extension are the spatial
tail-and-net bound (5.12), its conversion to (5.15), and the arbitrary
positive-gap propagation (6.4)--(6.8). All are derived above with
explicit constants and an all-real-horizon threshold.

Constants and especially T0 need not be uniform as kappa decreases
to zero. The heat density rho, gradient constant Gkappa and threshold
rates make this failure of uniformity visible. At kappa=0 the problem
is qualitatively different: one exact query v(x*) followed by the
scalar logistic formula computes S_Tv(x*) exactly. Thus kappa=0 is
excluded, and no uniform vanishing-diffusion lower theorem is claimed.

The candidate includes lambda=1, lambda=1/2 and the regime lambda<1
with growing nonconstant linear modes. It proves no global spatial
synchronization theorem for arbitrary inputs in that regime. The
small fluctuation used here is a high-probability property of the
specified horizon-dependent hard prior after a fixed burn-in.

No literature priority search, PDE numerical execution, random sampling,
initial-data oracle acquisition, Lean build, or new formal certificate
was performed for T82. Commands were read-only source/status/hash
inspection and writing this proof file. Existing dirty changes were
present before the task and were not modified. The mathematical status
is a completed conventional author derivation pending independent audit
and root acceptance; all broader accepted ledgers remain outside this
task's ownership.

The math-auto-research skill, defaults, routing, execution guidance and
general profile were read. The requested research dispatch is
gpt-6-astra/max, as recorded in run.json; the actual serving backend is
not independently exposed beyond that dispatch configuration. No model
setting or run-state edit was made in T82.

Frozen source snapshots inspected for the bounded handoff:

| Source in this run | SHA256 |
| --- | --- |
| reviews/T61-all-dimension-lower-proof.md | 404a237be72991ac60efb97c48b5ba2347384b0a30ffe3a98219a74d1604d691 |
| reviews/T64-all-dimension-lower-independent-audit.md | 07723a9f4fa3a6725b51431e773bc85a4ff8800ea5ac751cb66dd4b7eb24b8dc |
| reviews/T78-local-graph-weighted-L1-proof.md | e9613938316379c257fcaaf2cdc5bbbdfa19c01945a22d647a4e62d75b771a53 |
| reviews/R14c-natural-gap-graph-burnin-proof.md | 89a144617890314a47cbe1f7279053b9ea82c60dd670609739715a2a1ff2abbd |
| reviews/R14d-natural-gap-lower-composition.md | 33124c39eef1cb1e28c6e776445b0399f07b851c7c706373febb620510ccff6f |

T61 Sections 6--9 and T64 supply the previously accepted finite-prior
template; its relevant estimates are rederived here. Only T78 Section 6's
finite-time flow mechanism and R14c Section 4's last-unit comparison
mechanism are reused; their stable-graph assumptions are not imported.
The exact class and oracle interface were also read in D28/04u and 04o.
The final hash of this new file is reported externally after completion
to avoid a self-referential hash.
