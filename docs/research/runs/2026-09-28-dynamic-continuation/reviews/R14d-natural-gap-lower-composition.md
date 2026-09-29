# R14d: conditional signed lower bound from a local graph coordinate

Date: 2026-09-29. Root-authored conditional composition, pending independent
audit. R14c and T78 are not accepted dependencies at this writing. This
note records exactly how their proposed local estimates would replace
the strong-gap global phase in D28. It does not extend an accepted claim.

## 1. Precise analytical interface

Fix integers d,s>=1, kappa>0 with lambda=2pi^2 kappa>1, and the actual
equation u_t=(kappa/2)Delta u+u-u^3 on the normalized unit d-torus.
Use the same unknown class as D28: smooth genuinely signed v with
||v||inf<=1/2 and max_(|alpha|<=s)||partial^alpha v||inf<=1. Only exact
initial point values reveal input information; every acquisition,
including preprocessing and repeats, is charged. Algorithms may be
biased, adaptive, have unbounded outputs and random stopping; they
are Borel and halt almost surely on every input.

Assume the following two analytical conclusions, with fixed constants:

1. R14c supplies L,r>0 and the actual graph proxy
   H(v)=Pi S_Lv-Theta(QS_Lv), with |Theta|<=r/8 and
   ||QS_Lv||inf<=r/64 for ||v||inf<=7/8. If ||v||inf<=r exp(-L)/4,
   then for every T>=L,

       |S_Tv(x)-Psi(exp(T-L)H(v))|<=1/32,
       Psi(z)=z/sqrt(1+z^2).                        (1.1)

   Indeed ||S_Lv||inf<=exp(L)||v||inf<=r/4, so the actual shift from
   the stable graph has magnitude <=3r/8<r. This is the direct local
   branch of R14c, without a coarse-mean algorithm or global phase A.

2. For some a_star>0, Atilde=exp(-L)H is C3 on a neighborhood of the
   closed a_star sup-norm ball, is odd, has D Atilde(0)=Pi and
   D^2 Atilde(0)=0, and satisfies the actual mixed bound

       |D^3 Atilde(v)[h1,h2,h3]|
         <=B ||h1||inf ||h2||inf ||h3||1            (1.2)

   there. Enlarge B to at least one if necessary. T78 is assigned to
   derive this statement from the actual Lyapunov--Perron graph.

The identity exp(T-L)H(v)=exp(T)Atilde(v) is exact. Constants may
depend on the fixed gap, dimension, smoothness and graph radius. The
argument does not pass to lambda=1 or claim uniform constants there.

## 2. Local influence of one cell

Let F(v)=Atilde(v)-Pi v. The fundamental theorem of calculus applied
twice along the segment from zero to v gives

    DF(v)[h]=integral_0^1(1-t)D^3 Atilde(tv)[v,v,h] dt,
    |DF(v)[h]|<=(B/2)||v||inf^2 ||h||1.             (2.1)

This is a derivative estimate in continuous directions, not a conclusion
from an abstract sup-norm operator bound.

Choose a fixed smooth interior bump psi on (0,1)^d with 0<=psi<=1
and I=integral psi>0. Set

    Dpsi=max(1,max_(|alpha|<=s)||partial^alpha psi||inf),
    a=1/(8Dpsi), k even, K=k^d, Aamp=a k^(-s),
    v_xi(x)=sum_j xi_j Aamp psi(kx-j), xi_j in {-1,+1}.

The interiors of the cells are disjoint and the bump is zero near
their boundaries. These are smooth periodic functions; all derivatives
through total order s have norm at most a Dpsi<=1/8. Whenever the
sign vector contains both signs, v_xi is in the full stated input
class. This includes all good and bad configurations below.

For Aamp<=a_star, a single cell sign flip stays within the relevant
sup ball along its joining segment and changes the L1 input norm by
2 Aamp I/K. Therefore (2.1) implies

    |F(v_xi)-F(v_flip_i xi)|<=B I Aamp^3/K
      <=Lflip:=B Aamp^3/K.                         (2.2)

A swap of two opposite cell signs has influence at most 2 Lflip.
The proof does not assume that the spatial PDE commutes with arbitrary
permutations of cells.

## 3. Keep the full Hamming-layer prior

Let ell be even with sqrt(K)<=ell<=2sqrt(K)<=K/4. Denote by pi_ell
the uniform law on sign vectors with sum ell, and pi_0 the balanced
layer. Oddness of F and sign symmetry give E_pi0 F=0. From a uniform
balanced vector, flip a uniformly chosen ell/2-subset of its negative
coordinates. The resulting vector is uniform on pi_ell: each target
positive set has the same number of predecessor positive sets, and
each predecessor/subset choice has equal probability. Thus

    |E_piell F|<=ell Lflip/2.                       (3.1)

For the variance, reveal the coordinates in a fixed order. The two
possible next-sign conditional suffix laws can be coupled by adding
one uniform coordinate to a uniform subset of the smaller prescribed
size. The two full configurations then differ by one sign swap.
Their conditional expectations differ by at most 2 Lflip. The
conditional variance of the resulting Doob martingale increment is
at most p(1-p)(2 Lflip)^2<=Lflip^2; a forced sign contributes zero.
Orthogonality of these finite increments gives

    Var_piell(F)<=K Lflip^2=B^2 Aamp^6/K.           (3.2)

The positive-layer mean input mass is m=Aamp I ell/K. If

    Aamp^2<=I/(64B),                               (3.3)

then (3.1) implies |E F|<=m/8. Chebyshev and (3.2) yield

    P_piell(|F|>m/4)<=64 B^2 Aamp^4 K/(I^2 ell^2)
      <=64 B^2 Aamp^4/I^2<=1/64.                  (3.4)

The same estimates hold for pi_minus_ell with the absolute mass m.
The prior is never conditioned on the event in (3.4). Its exceptional
members remain genuine inputs with their original probabilities.

## 4. Actual PDE separation at every sufficiently large horizon

Put qrate=s+d/2 and choose, for each public T,

    R_T=(a I exp(T))^(1/qrate),
    k=2 floor(R_T/2), K=k^d,
    ell=2 ceil(sqrt(K)/2).                         (4.1)

For all sufficiently large real T, k is even, R_T/2<=k<=R_T,
K>=2048, and sqrt(K)<=ell<=2sqrt(K)<=K/4. Both sign layers contain
strictly positive and strictly negative cell counts. Choose the fixed
threshold additionally to ensure T>=L and

    Aamp<=min(a_star,r exp(-L)/4),
    Aamp^2<=I/(64B).                               (4.2)

Every threshold is feasible because s>=1 and k tends to infinity.
These choices work for all large T, not merely a selected subsequence.
As in D28's arithmetic, (4.1) gives

    1<=exp(T)m<=2^(qrate+1).

On the positive good event |F|<=m/4, Atilde(v)>=3m/4, so
Psi(exp(T)Atilde(v))>=Psi(3/4)=3/5. Equations (1.1) and (4.2)
therefore give, at the fixed requested point x*,

    S_Tv(x*)>=3/5-1/32=91/160>1/2.                 (4.3)

The negative good set has target at most -91/160. This is actual PDE
separation obtained through the graph coordinate. No scalar evolution
of the initial mean and no asymptotic global phase are assumed.

## 5. The unchanged exact-value information argument

Keep the equal mixture of the two full layers. A class-uniform
MSE<=1/16 algorithm, thresholded at zero, has error at most 1/4 on
each good input by (4.3) and Markov. On bad inputs use the bound one.
Its Bayes sign error is at most 1/4+1/64<=9/32.

Give the algorithm the sign of the cell at every point query even
when that point lies where the bump is zero. This strengthens the
oracle; the actual value is a known function of that sign and point.
Repeated cells add no information but their original acquisition
cost remains counted. Conditional on any distinct revealed signs,
the unused cells are exchangeable under the full layer laws.

For a cap n=floor(K/1024), pad the distinct revealed cells by unused
ones to n signs. Adaptive choices of labels, including choices based
on the input-independent seed, have the same without-replacement
sign law. At a prefix of length j<n containing z positive signs,

    p_plus=[(K+ell)/2-z]/(K-j),
    p_minus=[(K-ell)/2-z]/(K-j).

Every such prefix has positive probability under both layers,
p_minus lies in [1/4,3/4], and |p_plus-p_minus|<=2ell/K. Hence

    KL(Ber(p_plus)||Ber(p_minus))<=256/(3K).

The chain rule gives padded transcript KL<=1/12, including the common
input-independent seed. The queried indices are determined by the
seed and past revealed values and add no extra information. Pinsker
and data processing imply that every capped sign decision has Bayes
error at least 3/8. These are exactly the finite information facts
independently accepted in T61/T64; changing the diffusion coefficient
has not changed the prior or exact-value observation experiment.

Let qbar be the original expected query count under this finite prior.
If it is infinite the desired lower bound is immediate. Otherwise
truncate before query n+1 and use any fixed decision there. This
increases average error by at most P(Q>n)<=qbar/n. Consequently

    qbar>=n(3/8-9/32)>=3K/65536
      >=3*2^(-d-16)*(aI)^(d/qrate) exp(dT/qrate).   (5.1)

The finite prior does not depend on the algorithm. Its average lower
bound implies a worst-input expected-query lower bound, and any cost
model with Work>=Q inherits that lower bound. The expensive input may
depend on T and the algorithm; no common fixed hard profile is claimed.

## 6. Status and precise remaining gates

Conditional on the two actual analytical interfaces in Section 1,
this yields c exp(2dT/(2s+d)) for every fixed lambda>1 and every
fixed d,s>=1, at the original uniform MSE threshold. An independent
review must check the replacement proxy, its local ball, all-horizon
thresholds, actual PDE separation and unchanged observation law.

R14c still needs its graph/burn-in audit, and T78 is still deriving
the actual mixed derivative at this writing. No new accepted lower
bound, matching upper bound, arithmetic work theorem, full Lean,
signed numerical result, critical-gap extension or novelty claim is
made here. This file contains no numerical execution or oracle calls.
