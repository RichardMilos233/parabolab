# T61: weighted phase derivative and the signed lower bound in every fixed dimension

Date: 2026-09-28. Independent conventional theory derivation and review
of R04. This file is the sole T61 edit. No existing source, ledger,
formalization, implementation or numerical artifact was changed.

**Verdict: the weighted third-derivative obligation is proved below,
and R04's lower-bound conclusion follows for every fixed pair of
integers d,s>=1.** The proof marks one variation in L1, uses the actual
parabolic kernels to smooth it after time one, and retains that factor
in the centered-energy estimates. It does not infer a common dominating
measure from total variation or translation symmetry. The proposed
common measure on triples is unnecessary and is not asserted here.

The finite-layer concentration and exceptional-prior accounting also
pass. In particular, the proof retains the full Hamming-layer prior;
conditioning that prior on a PDE-good event would invalidate the
unchanged exchangeability argument. The resulting statement is a
worst-input expected-query lower bound, not a common-baseline result,
an all-dimension matching upper bound, a runtime theorem, or a priority
claim. Root review of this new proof remains the acceptance step.

## 1. Setting and theorem

Let X=(R/Z)^d with normalized Haar measure and heat semigroup P_t for
Delta/2. Fix 0<a0<1; a0=7/8 is permitted. Let S_t v solve

    u_t=Delta u/2+u-u^3,   u(0)=v,

for continuous real v with ||v||infinity<=a0. Set

    nu=2*pi^2-1,
    b(t)=integral_X u(t),   w(t)=u(t)-b(t),
    G(y)=y/sqrt(1-y^2),   Psi(z)=z/sqrt(1+z^2).

Use the actual phase coordinate from T56,

    A(v)=G(integral v)
         -integral_0^infinity J(t,v) dt,
    J(t,v)=exp(-t)*G'(b(t))*R(t),
    R(t)=3b(t)*integral w(t)^2+integral w(t)^3.       (1.1)

The claim proved here is that there is a finite B=B(d,a0)>0 such that
for all v in this closed ball and all continuous directions h1,h2,h3,

    |D^3 A(v)[h1,h2,h3]|
       <= B ||h1||infinity ||h2||infinity ||h3||1.   (1.2)

The derivative is the ordinary continuous-function-space Frechet
derivative on the open ball ||v||infinity<1. Thus directions may be
scaled as required to stay in that domain. Symmetry allows any one
direction to occupy the L1 position. An explicit finite recipe for B
is given in Section 5; no norm depending on derivatives of v occurs.

The domain normalization matters. The spectral gap used below is that
of the period-one torus in every coordinate. Only constants, not a
dimension-uniform estimate or a different domain geometry, are claimed.

## 2. The actual phase and its uniform PDE approximation

For completeness, the ingredients of T56 Section 3 used here follow
directly from comparison and centered energy. Write delta=1-a0^2.
Scalar comparison gives

    |u(t,x)|<=ell_a0(t)<1,
    1-b(t)^2>=delta*exp(-2t).                         (2.1)

Spatial integration gives the exact equation

    b'=b-b^3-R.                                     (2.2)

For mean-zero w, the unit-torus Poincare inequality and
(u-b)(u^3-b^3)>=0 give

    (1/2)d||w||2^2/dt<=-nu||w||2^2,
    ||w(t)||2<=a0*exp(-nu*t).                        (2.3)

Since |b|<=1 and ||w||infinity<=2,

    |R(t)|<=5a0^2*exp(-2nu*t).                       (2.4)

The identity G'(b)(b-b^3)=G(b) proves

    d[exp(-t)G(b(t))]/dt=-J(t,v).

Therefore (1.1) is an absolutely convergent actual PDE coordinate and

    |A(v)-exp(-t)G(b(t))|
       <=C0*exp(-(2nu-2)t),
    C0=5a0^2/[delta^(3/2)*(2nu-2)].                  (2.5)

It is odd, A(0)=0, and A(c)=G(c) on spatially constant inputs.
No closed equation for the initial mean is being assumed.

Here is also an explicit usable spatial remainder. Put

    theta=exp(-2*pi^2),
    rho=((1+theta)/(1-theta))^d.

The torus heat series implies ||p_1||infinity<=rho, and rho>=1. With
q=u^2+ub+b^2 in[0,3], the centered equation is

    w_t=Delta w/2+(1-q)w+integral q w.

Its local propagator is dominated by exp(t-r)P_(t-r). Over the last
unit of time, use ||p_1||2<=rho and (2.3). For T>=1 this gives

    ||w(T)||infinity<=Cw*exp(-nu*T),
    Cw=a0*exp(nu+1)*(rho+3/(nu+1)).                  (2.6)

Finally b(T)=Psi(exp(T)*exp(-T)G(b(T))) and Psi is globally
1-Lipschitz. Thus, uniformly over this whole sup ball,

    ||S_Tv-Psi(exp(T)A(v))||infinity
      <=E(T):=Cw exp(-nu*T)+C0 exp(-(2nu-3)T).       (2.7)

Both exponents decay. These estimates include A(v)=0 and inputs
arbitrarily close to that set.

## 3. One marked leaf in the actual variational kernels

For a nonempty labelled subset S of {1,2,3}, let

    U_S(t)=D^(|S|)S_t(v)[h_i:i in S],
    b_S=integral U_S,   W_S=U_S-b_S.

Take label3 as the marked direction. Define H_empty=1 and

    H_S=product_(i in S) ||h_i||infinity,       3 notin S,
    H_S=||h3||1*product_(i in S\{3}) ||h_i||infinity,
                                             3 in S.

For disjoint label groups these quantities multiply to H of their
union. This bookkeeping is essential: there is exactly one L1 factor,
not a product of two L1 factors at the same spatial point.

Let V(t,r) be the fundamental propagator with potential
c(t,x)=1-3u(t,x)^2. Since -2<=c<=1, its Feynman–Kac kernel obeys

    |V(t,r)f|(x)<=exp(t-r)*P_(t-r)|f|(x).             (3.1)

This is a bound for the actual time-dependent PDE kernel. Finite-time
Picard differentiation gives

    U_i(t)=V(t,0)h_i,
    U_ij(t)=-6 integral_0^t V(t,r)[u U_i U_j](r) dr,
    U_123(t)=integral_0^t V(t,r)[
        -6 U_1 U_2 U_3
        -6u(U_12 U_3+U_13 U_2+U_23 U_1)](r) dr.    (3.2)

Here products use disjoint derivative labels, even when two direction
functions happen to be equal. The subscripts1,2,3 in the ternary
product are single labels, not derivative orders.

Set c0=1,c1=1,c2=6,c3=57. Induction in (3.2) proves, for j=|S|<=3,

    ||U_S(t)||infinity<=c_j exp(jt) H_S,
                                  when3 notin S,   (3.3)

and the stronger pointwise marked bound

    |U_S(t,x)|<=c_j exp(jt) P_t|h3|(x)
                   *product_(i in S\{3})||h_i||infinity,
                                  when3 in S.      (3.4)

For order2 the scalar time coefficient is bounded by
6 exp(t)(exp(t)-1). In order3, the absolute forcing coefficients
are bounded by6+3*6*6=114 times exp(3r). Integration against
exp(t-r) gives57 exp(t)(exp(2t)-1). These prove the stated constants.

The marked calculation is pointwise, not an assumed weighted operator
bound: after all unmarked factors have been bounded in sup norm, every
term contains P_r|h3| exactly once, and

    P_(t-r) P_r|h3|=P_t|h3|.

In a heat-tree expansion this integrates all unmarked leaves out and
concatenates the heat kernels along the single root-to-marked-leaf
path. That path has total duration t, whatever the branching times.
No diagonal density bound on the entire tuple of leaves is needed.

Consequently, for all t>=0,

    ||U_S(t)||1<=c_j exp(jt) H_S,
    |b_S(t)|<=c_j exp(jt) H_S                       (3.5)

in the marked case, with the same scalar mean bound in the unmarked
case. At t=0 the first variation is h_i and higher variations vanish;
the L1 statements still hold. For t>=1, P_t has sup kernel bound rho.
Thus for every label group, marked or unmarked,

    ||U_S(t)||infinity<=M_j exp(jt) H_S,
    M_j=c_j*rho,   j=1,2,3.                        (3.6)

This step, performed only after time one, is why no nonintegrable
short-time factor t^(-d/2) appears in high dimensions.

## 4. Centered L2 estimates retain the L1 direction

For order zero put U_empty=u,b_empty=b,W_empty=w, M0=1 and N0=a0.
We now prove constants N_j such that, for t>=1,

    ||W_S(t)||2<=N_j exp((j-nu)t) H_S,
                                      j=|S|<=3.    (4.1)

Order zero is (2.3). Direct centering of the variational equations gives

    (W_S)_t=Delta W_S/2+(I-Pi)(c W_S)
               +b_S(c-Pi c)+(I-Pi)F_S,             (4.2)

where Pi is spatial averaging and F_S is the lower-order forcing from
(3.2); F_i=0. The homogeneous equation on mean-zero functions has
L2 propagator norm at most exp(-nu*(t-r)): its energy is bounded by
-nu||W_S||2^2 because c<=1. Also

    ||c-Pi c||2
      <=3||u^2-b^2||2<=6||w||2.                    (4.3)

The orthogonal projection I-Pi is contractive in L2. Subtract from
F_S its spatially constant expression formed from b and the b_J.
At order2 the required telescoping identity is

    u U_i U_j-b b_i b_j
       =w U_i U_j+b(W_i U_j+b_i W_j).               (4.4)

At order3 use

    U_i U_j U_l-b_i b_j b_l
       =W_i U_j U_l+b_i W_j U_l+b_i b_j W_l,
    u U_ij U_l-b b_ij b_l
       =w U_ij U_l+b(W_ij U_l+b_ij W_l).            (4.5)

Every term has a centered factor. Put that factor in L2 and all
others in the sup bounds (3.6). If the marked label occurs in the
centered factor, use its marked L2 bound. If it occurs in another
factor, use its marked sup bound. In either case disjoint labels give
exactly H_S. No factor ||h3||infinity is reintroduced.

Here are explicit scalar recursions proving the induction. Define

    C1=6a0 M1,
    N1=M1 exp(nu)+C1,
    C2=6a0 M2+6(a0 M1^2+2M1 N1),
    N2=M2 exp(nu)+C2/2,
    C3=6a0 M3+18N1 M1^2
                  +18(a0 M2 M1+N2 M1+M2 N1),
    N3=M3 exp(nu)+C3/3.                             (4.6)

Equations (4.3)–(4.5) bound the complete source in (4.2) by
C_j exp((j-nu)t)H_S. At time1, projection contraction gives
||W_S(1)||2<=M_j exp(j)H_S. Convolving the source with the
mean-zero propagator yields

    integral_1^t exp(-nu*(t-r))*exp((j-nu)r)dr
       <=exp((j-nu)t)/j.

The initial term is bounded by M_j exp(nu) exp((j-nu)t)H_S.
This proves (4.1) with (4.6). Also

    ||W_S(t)||infinity<=2M_j exp(jt)H_S              (4.7)

for j>=1, and ||w||infinity<=2 for j=0.

All estimates here are scalar spatial estimates for actual variations
in specified continuous directions. No Banach-space energy inequality
for signed measures or Radon–Nikodym densities is assumed.

## 5. Differentiating the phase and an explicit finite B

Use ordered partitions of the derivative labels among the factors in

    R=3b Pi(w*w)+Pi(w*w*w).

A derivative replaces a centered w by a centered W_S. It never
removes that factor. Every derivative term still has at least two
centered factors. On t>=1 put two in L2 using (4.1), and the optional
third in sup norm using (4.7). The mean factor uses (3.6). Hence

    |D^j R(t)[h_i:i in S]|
       <=R_j exp((j-2nu)t)H_S,    j=|S|<=3.         (5.1)

One explicit choice is

    R_j=3 sum_(a+b+c=j) [j!/(a!b!c!)] M_a N_b N_c
          +sum_(a+b+c=j) [j!/(a!b!c!)] N_a N_b (2M_c),

with M0=1,N0=a0 and (4.6) for the other constants. For j=0 this
recovers R_0=5a0^2. A marked label in the third sup factor is allowed
because (3.6) already retains its L1 norm.

For 0<=t<=1 use (3.3)–(3.5) instead: a marked W_S has L1 norm
at most2c_j exp(jt)H_S; an unmarked W_S has the same sup bound.
If the mark occurs in b_S, use its scalar bound (3.5). Bound other
factors in sup norm and integrate only the marked factor in L1.
This gives

    |D^j R(t)[h_i:i in S]|<=S_j exp(jt)H_S,
    S_j=20 sum_(a+b+c=j) [j!/(a!b!c!)] c_a c_b c_c. (5.2)

This short-time estimate uses no heat-density supremum. It is uniform
down to t=0 and remains valid for signed directions.

To make all chain-rule constants explicit, put

    g0=delta^(-3/2),  g1=3delta^(-5/2),
    g2=15delta^(-7/2), g3=105delta^(-9/2).

Direct differentiation of G and (2.1) give

    |G^(k+1)(b(t))|<=g_k exp((2k+3)t),  k=0,1,2,3.

For example G'''(y)=(3+12y^2)/(1-y^2)^(7/2) and
G''''(y)=(45y+60y^3)/(1-y^2)^(9/2). Define

    alpha0=g0,
    alpha1=g1*c1,
    alpha2=g1*c2+g2*c1^2,
    alpha3=g1*c3+3g2*c2*c1+g3*c1^3.

The finite chain rule, using the mean bounds (3.5), then proves

    |D^q[G'(b(t))][h_i:i in S]|
       <=alpha_q exp((3q+3)t)H_S,  q=|S|<=3.       (5.3)

The same assertion covers unmarked label groups. The order-zero
version has H_empty=1. Products in Leibniz's rule use disjoint
groups, so the complete third derivative of J satisfies

    |D^3 J(t,v)[h1,h2,h3]|<=H_{123}*
       { L_short exp(11t),         0<=t<=1,
         L_late exp((11-2nu)t),    t>=1 },           (5.4)

where

    L_short=sum_(q=0)^3 binom(3,q)*alpha_q*S_(3-q),
    L_late =sum_(q=0)^3 binom(3,q)*alpha_q*R_(3-q).

For the late estimate, a term differentiating G'(b) q times has
exponent (3q+3)+(3-q-2nu)-1=2q+5-2nu, at most11-2nu.
There is no missing factor from a differentiated denominator or
from a marked scalar mean. All its possible assignments are included
in (5.3) and the binomial sum.

Since 2nu=4*pi^2-2>34>11, the majorant is integrable. A valid
constant for (1.2) is therefore

    B=g2 + L_short*(exp(11)-1)/11
            + L_late*exp(11-2nu)/(2nu-11).          (5.5)

The first term bounds D^3[G(integral v)] because
|integral h_i|<=||h_i||infinity for i=1,2 and
|integral h3|<=||h3||1. This B is positive, finite and independent
of v and all three directions. Its dependence on d is through the
finite heat bound rho and subsequent scalar recursions.

Differentiation under the time integral is justified, not presumed.
On a finite interval the mild solution and variations (3.2) are
continuous in time for continuous inputs and directions. Their
products and spatial averages are jointly measurable. On each
interval [epsilon,L] with epsilon>0, the heat kernels and mild
formulas give the usual operator-norm continuous finite-time
derivatives. One can first differentiate that truncated integral,
then send epsilon down to zero using the uniform short-time
operator bounds from (5.2)–(5.3). No operator-norm continuity of
P_t at t=0 is required. The
corresponding estimates of orders j=0,1,2 have late exponents
3j+2-2nu, which also decay. Since ||h3||1<=||h3||infinity on this
normalized space, the weighted bounds imply integrable ordinary
multilinear-operator-norm bounds as well. Thus finite-cutoff phase maps
and their derivatives through order3 converge uniformly on each
closed ball strictly inside the open unit ball. The fundamental
theorem of calculus on line segments, applied successively to these
uniform limits, proves genuine C3 Frechet differentiability and the
derivative formula used in (5.4)–(5.5).

This resolves the analytic obligation directly. It asserts neither
a universal positive measure on X^3 nor a conclusion obtainable
from uniform total variation alone. There is no remaining
short-time, label-measurability, or high-dimensional singular-kernel
gate in the weighted estimate just proved.

## 6. Sensitivity of the nonlinear correction to one cell

Let F(v)=A(v)-integral v. Oddness gives D^2A(0)=0. Also DA(0)h=integral h:
the integrand correction in (1.1) starts at cubic order, or this follows
directly by differentiating at the zero solution in (3.2).
Taylor's formula for DA along the segment from0 to v therefore gives

    |DF(v)[h]|<=integral_0^1 (1-r)
                     |D^3A(rv)[v,v,h]| dr
               <=(B/2)||v||infinity^2 ||h||1.       (6.1)

Fix the original smooth interior bump psi on(0,1)^d, with
0<=psi<=1, I=integral psi>0 and
D=max(1,max_(|alpha|<=s)||partial^alpha psi||infinity).
Let a=1/(8D), take an even grid size k, and put

    K=k^d, Aamp=a*k^(-s),
    v_xi=sum_j xi_j*Aamp*psi(kx-j), xi_j in{-1,+1}.

Disjoint cell interiors give ||v_xi||infinity<=Aamp. A single sign
flip changes its L1 norm by exactly2Aamp I/K. Every point on the
joining segment has sup norm at most Aamp. As soon as Aamp<=a0,
(6.1) proves

    |F(v_xi)-F(v_flip_i xi)|
       <=B I Aamp^3/K<=Lflip:=B Aamp^3/K.           (6.2)

A swap of one positive and one negative cell costs at most2Lflip.
No spatial permutation invariance of F is needed for this bound.

## 7. Finite Hamming-layer concentration: PASS

Let K and r be even with sqrt(K)<=r<=2sqrt(K)<=K/4. Let pi_r be
uniform on sign vectors with sum r, and pi_0 uniform on the balanced
layer. Global sign reversal preserves pi_0 and changes F's sign;
therefore E_pi0 F=0.

Start with a uniform balanced sign vector and flip a uniformly chosen
subset of r/2 of its negative signs. The resulting law is pi_r:
every target positive set of size(K+r)/2 has the same number of
predecessor balanced sets, and every predecessor/added-subset choice
has the same probability. The path uses r/2 single flips, so

    |E_pir F|<=r*Lflip/2=B Aamp^3 r/(2K).           (7.1)

The negative layer has the analogous bound. The coupling concerns
the prior distribution, not the algorithm's observations.

For variance, reveal coordinates in a fixed order and use the Doob
martingale of F. Given a prefix with both next signs possible, the
remaining suffix positive counts differ by one between those two
conditions. Couple them by choosing a uniform subset of the smaller
size, then adding one uniformly selected point of its complement.
The larger subset is uniform, because each such subset has the same
number of predecessors. The two full sign vectors differ by swapping
the current coordinate with the added suffix coordinate. By (6.2)
their F values, and hence their conditional expectations, differ by
at most2Lflip.

If p is the conditional probability of the next positive sign, the
conditional variance of that martingale increment is at most
p(1-p)(2Lflip)^2<=Lflip^2. A forced next sign contributes zero.
Finite martingale orthogonality gives

    Var_pir(F)<=K Lflip^2=B^2 Aamp^6/K.              (7.2)

This is a without-replacement finite argument; no iid coin model or
unproved slice-Poincare constant is inserted.

The positive-layer mass is m=Aamp I r/K. If

    B Aamp^2/(2I)<=1/8,

then |E F|<=m/8, and Chebyshev yields

    P_pir(|F|>m/4)
       <=64 B^2 Aamp^4 K/(I^2 r^2)
       <=64 B^2 Aamp^4/I^2.                         (7.3)

The same holds on the negative layer, with |m|. A convenient stronger
condition Aamp^2<=I/(64B) makes the last bound at most1/64, hence
at most1/32, and also implies the mean condition. Because s>=1,
Aamp tends to zero as k tends to infinity in every fixed dimension.
This is the step that replaces the earlier worst-arrangement cubic
error by a controlled exceptional-prior probability.

## 8. Actual PDE separation and all-horizon thresholds

Let q=s+d/2 and use R04's choices

    R_T=(a I exp(T))^(1/q),
    k=2 floor(R_T/2), K=k^d,
    r=2 ceil(sqrt(K)/2).                            (8.1)

For R_T>=4, R_T/2<=k<=R_T. At sufficiently large T, K>=2048,
r is even, sqrt(K)<=r<=2sqrt(K)<=K/4, and each sign configuration
has both signs. Every v_xi lies in the original fixed smooth signed
class: its derivatives through order s are bounded by aD<=1/8,
its height is at most1/8, and compactly supported cell bumps give
smooth periodic extension. The higher derivatives need not have
uniform bounds. This applies to good and bad configurations alike.

For m=Aamp I r/K on the positive layer,

    1<=exp(T)m<=2^(q+1).                            (8.2)

Indeed r is between k^(d/2) and twice that value, and R_T/k lies
between1 and2. Thus on |F(v)|<=m/4,

    A(v)>=3m/4,
    Psi(exp(T)A(v))>=Psi(3/4)=3/5.

Choose T so that E(T)<=1/32 in (2.7). The actual PDE target is
then at least91/160>1/2 on the positive good set, and at most
-91/160<-1/2 on the negative good set. This uses the true nonlinear
coordinate, not an assumed scalar evolution of the initial mean.

These choices can be made for every T beyond one fixed threshold,
not merely a subsequence. For example choose an integer k_*>=4
such that k_*^d>=2048, a*k_*^(-s)<=a0, and
a^2*k_*^(-2s)<=I/(64B). Taking

    T>=q*log(2k_*)-log(aI)

ensures k>=k_*. Additionally take T>=1 and

    T>=max(0,log(64Cw))/nu,
    T>=max(0,log(64C0))/(2nu-3).

The maximum of these finitely many thresholds suffices. All depend
only on the fixed dimension, smoothness, bump and analytic ball.
There is no d<=4s restriction in them.

## 9. Full-prior testing and expected query cost: PASS

Keep the two full uniform layers with equal prior weights. Do not
condition them on |F|<=|m|/4. Their bad probabilities are at most
1/32 each. A class-uniform RMS1/4 estimator has MSE<=1/16 at every
input. Threshold its real output at zero. On every good input the
true target has magnitude>1/2 with the prescribed sign, so Markov's
inequality bounds its sign error by1/4. On bad inputs bound error
by1. The Bayes error of this sign test is consequently at most

    1/4+1/32=9/32.                                 (9.1)

This uses the original class-uniform guarantee, not a replacement
high-probability input promise.

For completeness the finite information estimate is unchanged and
can be checked directly. An exact point query reveals at most one
cell sign; giving that sign even at a zero of the bump only strengthens
the oracle. Conditioned on any distinct revealed signs, unused cells
are exchangeable. Thus adaptive choice of the next unused cell has
the ordinary without-replacement law. Pad a procedure using at most
n=floor(K/1024) queries with unused signs to n observations.

For a prefix of length l<n with j positive signs, the two next-positive
probabilities are

    p_plus =[(K+r)/2-j]/(K-l),
    p_minus=[(K-r)/2-j]/(K-l).

For K>=2048 and r<=2sqrt(K), p_minus lies in[1/4,3/4], and
|p_plus-p_minus|<=2r/K. Hence

    KL(Ber(p_plus)||Ber(p_minus))
       <=(p_plus-p_minus)^2/[p_minus(1-p_minus)]
       <=256/(3K).

All prefixes of this length have positive probabilities under both
layers. The chain rule gives transcript KL<=n*256/(3K)<=1/12.
Including the private input-independent seed does not change this
bound: conditional exchangeability holds for every seed, and the
padded signs have the same urn law. Pinsker and data processing
give total variation at most sqrt(1/24)<1/4, so every capped sign
test has Bayes error at least3/8. This argument never changes the
fixed spatial functions into independent noisy oracle responses.

Let qbar be the original estimator's expected point-query count
averaged over this finite prior and its seed. If qbar is infinite,
the lower bound is immediate. Otherwise truncate before query n+1
and return a fixed decision there. The average extra test error is
at most P(Q>n)<=qbar/n. Combining with (9.1) yields

    qbar>=n*(3/8-9/32)=3n/32>=3K/65536.             (9.2)

The last step uses n>=K/2048 for K>=2048. Almost-sure halting and
measurability are the original oracle assumptions. Only a finite
prior is coupled at each T, so its inputwise exceptional null sets
can be removed together. Biased or unbounded real outputs cause no
problem; the argument uses only their MSE and the bounded sign test.

Finally (8.1) gives

    qbar >= [3*2^(-d-16)*(aI)^(d/q)] exp(dT/q)
          = C exp(2dT/(2s+d)).                      (9.3)

The prior is independent of the algorithm. Its average lower bound
implies the same worst-input lower bound. An expensive member can
depend on T and the algorithm; no single common baseline or fixed
hard profile is supplied by this proof.

## 10. Conclusion, scope and immutable inputs

The new weighted estimate (1.2) holds on every fixed closed sup ball
strictly inside(-1,1), with an explicit finite B from (5.5). It closes
R04's outstanding analytical gate by a direct actual-kernel argument.
The finite concentration and bad-event calculation preserve the
claimed constants and establish the signed expected-query lower
exponent for every fixed d,s>=1. The earlier d<=4s cutoff is not
needed for this strengthened lower proof.

No stronger common dominating measure on triple input space is proved
or required. No corresponding higher-dimensional upper theorem is
derived here; T56/T59's upper range remains as stated in those frozen
sources. No Lean, numerical, arithmetic-work, novelty or award
conclusion follows. There is no unresolved mathematical gate inside
this conventional derivation as written; independent acceptance and
any later formal correspondence remain separate work.

Reviewed source snapshots:

| File in the dynamic-continuation run | SHA256 |
| --- | --- |
| reviews/R04-signed-all-dimension-lower-candidate.md | 2bc5129ec4b9da882d7b16543d03f0bc8f34989cc02f9b9a65c5e805c1f4ae75 |
| reviews/T56-signed-upper-feasibility.md | 0f0cd6a6fbe97d5746c42f2da94161284f4b4fb3da70b724b5992450388d5933 |
| reviews/T59-signed-upper-independent-audit.md | 47d3ce98ac19210e9bbcd318ac1de2fb9dddd5bc372bff201dc97d47572301ab |
| 04r-signed-many-bump-complexity.md | 4bdcb75b7ee62c40879a80cb84b0949f1a9e796d387775e5760cab04a33fa419 |

The exact oracle/class interface was also read in
04o-unstable-phase-query-lower-bound.md. All existing files were
read-only for T61. The hash of this new proof is reported externally
after its final write, avoiding a self-referential file hash.
