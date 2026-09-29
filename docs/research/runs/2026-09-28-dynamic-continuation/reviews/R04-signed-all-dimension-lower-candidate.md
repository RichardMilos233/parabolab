# R04: a candidate route to removing the signed lower-bound dimension cutoff

Status: new root theory candidate, not accepted or independently checked.
This does not modify D25 or frozen T56. It depends on a strengthening of
T56's derivative-measure estimates that must be proved, not silently
inferred from a total-variation norm. No Lean/code/numerical work is
requested by this draft. The larger-dimensional matching upper is not
claimed even if this lower route passes.

## 1. Proposed strengthening and why the existing proof is insufficient

Let A(v) be T56's actual nonlinear phase coordinate, defined on a fixed
sup-norm ball strictly inside(-1,1). The required stronger lemma is a
single finite positive measure mu3 on(T^d)^3, independent of v, such that

    |sigma3(v)| <= mu3,

for every v in that ball, where sigma3(v) represents D^3 A(v). Require
mu3 to be invariant under simultaneous translation of all three input
positions. Its third marginal is then B3 times normalized Haar measure,
where B3=mu3((T^d)^3)<infinity. In particular,

    |D^3 A(v)[h1,h2,h3]|
       <=B3 ||h1||infinity ||h2||infinity ||h3||1.        (1.1)

The existing uniform bound ||sigma3(v)||TV<=K3 alone does NOT imply this
common domination or(1.1). This is the precise new analytical obligation.
A proof can instead directly establish(1.1) with a v-independent B3;
common translation-invariant domination is a sufficient route.

A candidate construction follows the actual envelopes in T56 rather
than an arbitrary functional representation. At t=1, each unweighted
uniform-root heat-tree law is translation invariant. Common-Gaussian
shift domination bounds its root-dependent density uniformly. Choose
finite positive translation-invariant measures rho_j for j=1,2,3 from
these unweighted laws. The weighted PDE kernels are dominated by these
measures after their coefficient bounds are removed.

For t>=1 the mixed sup/L2 inductions can potentially be retained
pointwise in the input labels instead of integrated only at the end.
Enlarge the envelopes recursively:

    bar_rho1 = a finite multiple of rho1,
    bar_rho2 = a finite multiple of rho2+rho1 tensor rho1,
    bar_rho3 = a finite multiple of
       rho3 + sum_(label permutations)(bar_rho2 tensor rho1)
            + rho1 tensor rho1 tensor rho1.

All are finite and invariant under simultaneous translations. The
Duhamel and centered-energy inequalities use scalar bounds independent
of v and products with disjoint derivative labels. If carried out
pointwise under a common dominating measure, they give density bounds
M_j(t,Y)<=C exp(jt) dbar_rho_j and
N_j(t,Y)<=C exp((j-nu)t) dbar_rho_j, in the appropriate Radon–Nikodym
sense. The two-centered-factor estimates then dominate the third
phase-integrand derivative by a finite invariant measure times
exp((11-2nu)t), which is integrable on the unit torus.

On0<t<=1, bound the finite-time variational tree weights before
integrating spatial roots. Centering only adds independent spatially
averaged roots; after replacing the undifferentiated u,w coefficients
by uniform scalar bounds, each resulting positive envelope is invariant
under translating every initial leaf. The total masses are uniformly
bounded in this time interval. Time integration produces a finite
invariant envelope, including possible diagonal singularities. The
initial term G(integral v) contributes a bounded multiple of product
Haar measure. Their sum would be mu3.

This paragraph is an explicit proposed proof plan, not a completed
measure-valued argument. A reviewer must check common dominating measures,
pointwise-label energy inequalities, measurability in time, label
symmetrization, and the short-time envelopes. The route must be rejected
or repaired if any step only controls a multilinear operator norm.

## 2. Consequence for a single hidden-cell sign change

Assume(1.1) has been proved. Put F(v)=A(v)-integral v. At zero,
DA(0)[h]=integral h and D^2 A(0)=0; the latter follows from oddness and
C3 regularity. Taylor's formula for DA along the line from0 to v gives

    |DF(v)[h]| <=(B3/2)||v||infinity^2 ||h||1.             (2.1)

Use D25's disjoint smooth bumps with K=k^d cells,

    v_xi=sum_j xi_j a k^(-s)psi(kx-j),
    xi_j in{-1,+1}, I=integral psi>0,
    Aamp=a k^(-s), 0<=psi<=1.

All profiles, and every straight segment joining a single sign flip,
have sup norm at most Aamp. Flipping one sign changes the L1 norm of
the datum by2Aamp I/K. Hence(2.1) yields

    |F(v_xi)-F(v_flip_i xi)| <=B3 I Aamp^3/K
                             <=B3 Aamp^3/K=:Lflip.       (2.2)

For simplicity the later bounds retain the weaker last constant I<=1.
Swapping one positive and one negative sign costs at most2Lflip.
This estimates the nonlinear correction itself, not the whole phase
coordinate whose first-order sensitivity is the mass.

## 3. Mean and variance under an exact Hamming layer

Take even K and even r with sqrt(K)<=r<=2sqrt(K), as in D25. Let pi_r
be uniform on sign configurations whose sum is r; pi_0 is the balanced
layer. Oddness of F and sign-reversal symmetry give E_pi0 F=0.

To sample pi_r, start with a uniform balanced configuration and flip a
uniform subset of r/2 negative signs. The resulting law is permutation
invariant on the r layer, hence uniform. Repeated use of(2.2) gives

    |E_pir F| <=(r/2)Lflip <=B3 Aamp^3 r/(2K).            (3.1)

The minus layer is analogous. This is a coupling statement about the
prior, not an assumption that the algorithm observes independent signs.

For variance, reveal the signs in a fixed order. At each prefix, couple
the two possible next-sign conditions by swapping that sign with one
uniformly chosen opposite sign in the unrevealed suffix. The suffix laws
are uniform with the required counts: a uniform subset plus one uniformly
chosen complement point remains uniform among subsets of the larger size.
The two complete configurations differ by a swap, so their conditional
expectations of F differ by at most2Lflip.

If p is the conditional probability of the next positive sign, the
conditional variance of the Doob increment is therefore at most
p(1-p)(2Lflip)^2<=Lflip^2. Degenerate next signs contribute zero.
Orthogonality of the finite martingale increments yields

    Var_pir(F)<=K Lflip^2 <=B3^2 Aamp^6/K.                (3.2)

This is an explicit finite argument; it does not quote an unspecified
slice Poincare constant or replace without-replacement samples by iid ones.

The true mass on the positive layer is m=Aamp I r/K. If Aamp is sufficiently
small that B3 Aamp^2/(2I)<=1/8, then(3.1) gives |E F|<=m/8. Chebyshev
and(3.2) imply

    P_pir(|F|>m/4)
       <=64 B3^2 Aamp^4 K/(I^2 r^2)
       <=64 B3^2 Aamp^4/I^2.                             (3.3)

This tends to zero as k tends to infinity for EVERY fixed d>=1,s>=1,
since Aamp=a k^(-s). In particular the exceptional probability can be
at most1/32 at both layers. No condition d<=4s appears in this step.

## 4. PDE separation with an explicitly charged bad-prior event

Keep D25's horizon-dependent even grid, with q=s+d/2,

    k=2 floor((a I exp(T))^(1/q)/2), K=k^d,
    r=2 ceil(sqrt(K)/2).

For all sufficiently large T, K>=2048 and
1<=exp(T)|m|<=2^(q+1), as in T50. On the positive-layer good event
|F|<=m/4, the phase A(v)=m+F is at least3m/4. Thus

    Psi(exp(T)A(v)) >=Psi(3/4)=3/5.

The uniform coordinate-to-PDE error from T56 Section3 tends to zero
independently of the particular sign arrangement. Choose T large enough
that it is at most1/32. Then the actual PDE target exceeds1/2 on the good
positive-layer event, and is below-1/2 on its negative counterpart.

This is deliberately weaker than requiring separation for EVERY sign
arrangement. The exceptional prior probability is retained below; it may
not be dropped from the testing argument. Every configuration, good or
bad, still belongs to the fixed genuinely sign-changing C^s class.

A class-uniform RMS1/4 estimator gives a sign test with error at most1/4
on each good input, by its actual MSE bound and the target gap1/2.
On bad inputs use the trivial error bound1. Consequently its Bayes sign
error under the two equal layer priors is at most

    1/4+1/32=9/32.                                      (4.1)

No high-probability premise about the unknown input replaces the original
class-uniform estimator guarantee. The hard prior is used only inside a
valid worst-input lower-bound argument.

## 5. Expected query lower bound and proposed all-dimension conclusion

D25's finite-urn information estimate is unchanged: with at most
n=floor(K/1024) sign queries, Bayes error is at least3/8. Full-cell signs
remain a stronger oracle than exact initial point values. Let qbar be
the prior-average expected point-query cost of the original estimator.
If it is infinite the lower bound is immediate. Otherwise truncate before
query n+1. Markov's inequality increases test error by at most qbar/n.
Combining with(4.1) gives

    qbar>=n*(3/8-9/32)=3n/32>=3K/65536, K>=2048.         (5.1)

The floor comparison for k therefore proposes

    qbar >=C exp(2dT/(2s+d))

for every fixed d,s>=1 and all sufficiently large T. The finite prior is
independent of the algorithm; some expensive member may depend on both
T and the algorithm. This is not a common-baseline or fixed-profile
query lower bound. It would extend D25's lower range, not establish an
all-dimension matching upper bound or practical computational complexity.

## Outstanding gate

Sections2–5 are conditional on the stronger PDE derivative estimate(1.1).
The proof outline in Section1 must be expanded and independently checked.
The finite Hamming-layer mean/variance coupling and exceptional-event
accounting also need an independent review. Until then D25 keeps its
accepted d<=4s scope. Do not put an all-dimension claim into the ledger,
canvas, formal contract or numerical protocol.
