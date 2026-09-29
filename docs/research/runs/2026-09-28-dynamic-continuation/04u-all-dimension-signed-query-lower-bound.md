# D28: signed query lower bound in every fixed dimension

Status: conventionally proved in frozen T61, independently accepted in T64,
and accepted by root after reading both complete files. This removes the
dimension restriction from the lower bound of D25. The matching upper of
D27 still has its original restriction `d<=4s`.

## Exact statement

Fix integers `d,s>=1` and a target point `x*` on the normalized period-one
torus. Let `S_T` be the flow of

    u_t = Delta u/2 + u - u^3.

The fixed input class is

    V = {v smooth periodic real:
         ||v||infinity<=1/2,
         max_(|alpha|<=s)||partial^alpha v||infinity<=1,
         min v<0<max v}.

There are constants `C>0,T0<infinity` depending only on the fixed public
parameters such that, for every real `T>=T0`, every admissible randomized
algorithm satisfying

    sup_(v in V) E|H_T(v)-S_Tv(x*)|^2 <= 1/16

must satisfy

    sup_(v in V) E Q_T(v) >= C exp(2dT/(2s+d)).

Indeed, a finite prior on `V`, chosen from the public parameters and `T`
before the algorithm is chosen, has at least that prior-average expected
cost. An expensive member can depend on both `T` and the algorithm. This
is not a common expensive baseline and not one fixed hard profile for all
horizons.

The oracle supplies only exact initial point values. Every acquisition is
charged. Algorithms may be biased, have unbounded real outputs, choose
points and stopping times adaptively, and use input-independent randomness.
Rules are measurable and halt almost surely on each promised input. No
formula, mass, derivative, phase, evolved-value or input-dependent metadata
oracle is available. Arithmetic cost is not the quantity bounded here.

## The new analytic estimate

Write `b(t)=integral S_t v`, `w(t)=S_t v-b(t)` and `nu=2*pi^2-1`.
On any fixed sup ball of radius `a0<1`, the actual phase is

    A(v)=lim_(t->infinity) exp(-t) G(b(t)),
    G(y)=y/sqrt(1-y^2).

The exact mean equation is

    b'=b-b^3-R,
    R=3b integral w^2+integral w^3.

The centered energy and one-unit heat smoothing give

    ||S_Tv-Psi(exp(T)A(v))||infinity
        <= Cw exp(-nu*T)+C0 exp(-(2nu-3)*T),
    Psi(z)=z/sqrt(1+z^2).

T61 proves the stronger, spatially weighted derivative estimate

    |D^3 A(v)[h1,h2,h3]|
       <= B ||h1||infinity ||h2||infinity ||h3||1.

The finite constant `B` depends on the fixed dimension and sup ball, not
on derivatives of `v` or concentration of the marked direction `h3`.
The proof follows one marked direction through the actual parabolic
variations. Before time one, heat composition retains `P_t|h3|` and its
integral, with constants `1,6,57` through order three. After time one,
heat smoothing and centered energy retain the same `L1` norm. The third
phase-integrand derivative is bounded by a constant times
`exp((11-2nu)t)` at late times, which is integrable.

All exchanges with the infinite-time phase integral are justified by
uniform integrable bounds on derivatives. A common measure dominating
every third derivative is neither used nor proved. The proof avoids the
short-time density estimate that would introduce a dimension-dependent
singularity.

## Why the lower bound no longer needs d<=4s

Set `F(v)=A(v)-integral v`. Oddness and the linearized mean equation give
`DA(0)h=integral h` and `D^2 A(0)=0`. Therefore

    |DF(v)[h]| <= (B/2)||v||infinity^2 ||h||1.

Take `K=k^d` disjoint smooth cell bumps, each of amplitude
`a_k=a*k^(-s)`, and assign signs. A single sign flip changes `F` by at
most `Lflip=B*a_k^3/K` after the fixed bump integral is bounded by one.
A swap costs at most twice this amount.

For the uniform Hamming layer with sign sum `r`, a coupling to the
balanced layer and a fixed-order reveal martingale yield

    |E F| <= r*Lflip/2,
    Var F <= K*Lflip^2 = B^2*a_k^6/K.

These use full layers. They do not assume spatial permutation symmetry
of the PDE or replace the layer by independent signs. The two conditional
suffixes in a reveal step are coupled by one swap.

With `r` of order `sqrt(K)`, the exact layer mass has magnitude
`m=a_k*I*r/K`, where `I>0` is the fixed bump integral. Thus the standard
deviation of the nonlinear correction, relative to the mass, is of order
`a_k^2`. It vanishes for every fixed `d,s>=1`. This replaces the previous
worst-arrangement bound, which required `d<=4s`.

For `a_k^2<=I/(64B)`, both layers have

    P(|F|>m/4) <= 1/64 <= 1/32.

Choose `q=s+d/2`,

    R_T=(a*I*exp(T))^(1/q),
    k=2 floor(R_T/2),
    r=2 ceil(sqrt(K)/2).

Then `exp(T)m>=1`. On the good part of either layer, the actual PDE
target has the prescribed sign and magnitude at least
`Psi(3/4)-1/32=91/160>1/2` for sufficiently large `T`. The fixed amplitude
and bump derivative bounds place every configuration, including the bad
ones, in the original input class. The explicit thresholds in T61 work
for every sufficiently large real horizon, not only a subsequence.

## Information and expected cost

Keep the full uniform layer priors with equal weights. A uniform MSE
bound `1/16` implies sign-test Bayes error at most `1/4+1/32=9/32`.
The exceptional PDE-bad probability is paid explicitly; conditioning it
away would destroy the urn argument and is not permitted.

Giving the full cell sign at each new queried cell only strengthens the
oracle. For a test capped at `n=floor(K/1024)`, pad distinct revealed cells
to `n`. Conditional on the private seed and preceding reveals, the next
unused sign has the actual without-replacement law. For both hypotheses,
all relevant prefixes have positive probability. Each conditional
Bernoulli KL is at most `256/(3K)`, so the full capped KL is at most
`1/12`. Pinsker and data processing give Bayes error at least `3/8`.

If `qbar` is the full-prior expected original query count, truncation
changes the decision with probability at most `qbar/n`. Hence

    3/8 <= 9/32+qbar/n,
    qbar >= 3n/32 >= 3K/65536.

Since `k>=R_T/2`, one may take

    C=3*2^(-d-16)*(a*I)^(d/q).

This argument includes adaptive stopping, rare expensive runs and biased
outputs. Almost-sure halting null sets can be united over the finite prior.

## Evidence and remaining scope

- Author proof: `reviews/T61-all-dimension-lower-proof.md`, 614 lines,
  SHA256 `404a237be72991ac60efb97c48b5ba2347384b0a30ffe3a98219a74d1604d691`.
- Independent audit: `reviews/T64-all-dimension-lower-independent-audit.md`,
  SHA256 `07723a9f4fa3a6725b51431e773bc85a4ff8800ea5ac751cb66dd4b7eb24b8dc`.
- Earlier exact oracle model: `04o-unstable-phase-query-lower-bound.md`.
- Earlier lower and matching restricted-range upper: `04r` and `04t`.

This is a conventional mathematical theorem. The full phase/PDE,
Hamming-layer concentration and adaptive KL argument are not in Lean.
T62 addresses only the first actual Bernoulli-measure information gate.
No numerical validation of D28, all-dimensional matching upper, practical
work bound, larger-domain extension or novelty conclusion follows.
The local stable-graph upper route R07/T65 is a separate ongoing task.
