# D29: matching signed query complexity in every fixed dimension

Status: conventional theorem accepted after frozen T65, independent T67,
and root correspondence. This combines the new upper bound with the
separately accepted D28 lower bound. The earlier D27 and D28 artifacts are
preserved with their historical scope. No arithmetic-work theorem follows.

## Exact theorem and oracle model

Fix integers `d,s>=1`, one point `x*` of the normalized unit torus
`X=(R/Z)^d`, and the Allen--Cahn flow

    u_t = Delta u/2 + u - u^3,       u(0)=v.

Use exactly the fixed genuinely signed class

    V = {v in C^infinity(X;R): ||v||infinity<=1/2,
         max_(|alpha|<=s)||partial^alpha v||infinity<=1,
         min v<0<max v}.

An algorithm observes only charged exact initial values `v(y)`. Every
acquisition, including repeated and preprocessing acquisitions, counts.
Rules are Borel, private randomness is input independent, and the
algorithm halts almost surely on every promised input. Bias, adaptivity,
random stopping and unbounded real outputs are permitted. No initial
formula, mean, phase, derivative or evolved-value oracle is supplied.

Let `N(T)` be the infimum of `sup_(v in V) E Q_T(v)` over these algorithms
with `sup_(v in V) E|H_T(v)-S_Tv(x*)|^2<=1/16`. There are positive finite
constants `c,C,T0`, depending on the fixed public parameters, such that
for every real `T>=T0`,

    c exp(2dT/(2s+d)) <= N(T) <= C exp(2dT/(2s+d)).

The upper algorithm has a deterministic query cap and RMS at most
`7/64<1/4`. The lower holds even for a finite prior chosen before the
algorithm, hence also in the worst-input expectation. Its expensive
input may depend on both `T` and the algorithm. This is not a lower
bound at a single common input or on every fixed trajectory.

## Why the old dimension cutoff disappears

The paid coarse interpolant `g` uses `k^d` values and has residual
`e=v-g`, `||e||infinity<=Cint k^(-s)`. Monte Carlo correction of a
bounded linear functional of this residual has leading scale
`k^(-s-d/2)` when it uses `k^d` samples. Long-time instability demands
that the relevant phase error be of order `exp(-T)`.

D27 used the global phase `A`, its first two Taylor terms and a cubic
remainder. The balance `3s>=s+d/2` imposed `d<=4s`. T65 replaces that
specific expansion by an arbitrarily high, but fixed, order expansion
of a smooth local stable-interface coordinate. It does not assert
arbitrary smoothness of the global phase.

Write `Pi` for spatial average, `Q=I-Pi`, and `nu=2*pi^2-1`. The explicit
signed stable heat kernel `B_t=exp(t)(P_t-lambda)` has
`||B_t||TV<=M exp(-nu*t)`. In a weighted trajectory space, the equation

    U(t)=B_t w - integral_0^t B_(t-r) U(r)^3 dr
                   + integral_t^infinity exp(t-r) Pi(U(r)^3) dr

is a contraction on a sufficiently small public ball. Its mean at
time zero defines `Theta(w)`. The actual solution starting from
`w+Theta(w)` decays and has zero phase. All finite derivatives of this
graph are constructed as actual signed product measures: tensor the
lower variations and solve the same contraction resolvent at each
order. Products improve time decay, so no order-dependent spectral
restriction is introduced. Countable additivity, kernel measurability
and weighted total-variation convergence are proved explicitly.

Choose a fixed burn-in `L`, independent of `T`, so the centered part
of every profile in the auxiliary `7/8` ball enters this small ball.
Then

    H(q)=Pi S_Lq-Theta(Q S_Lq)

has derivatives of every prescribed finite order, represented by
bounded-TV product measures. Near the stable interface,

    A(S_Lv)=c(v) H(v),       63/64<=c(v)<=65/64.

Because `Psi(z)=z/sqrt(1+z^2)` is insensitive to this small multiplicative
error uniformly in `z`, using `Psi(exp(T-L)H(v))` incurs at most `1/64`
of profile error. A paid coarse mean test handles profiles away from
the interface by scalar comparison and returns the appropriate sign.
No exact unknown phase or distance from the interface is assumed.

## A finite algorithm, not a free derivative oracle

Set

    qrate=s+d/2,       J=ceil(1+d/(2s)),       m=J-1.

Then `Js>=qrate`. Expand `H` around `g` through order `m`. A positive
finite partition and the derivative measures bound each ordered
coefficient table in l1. Mixed forward differences, including repeated
indices, approximate those coefficients using only known profiles.
Each known `H` value is computed by a finite PDE mesh solve and a
finite, error-aware scalar root search for the stable graph. All
mesh values are evaluations of already known formulas; they are not
new acquisitions from the unknown input.

Rational coefficient rounding supplies an explicit finite tuple law.
For each order `j`, sample at most `k^d` tuples and acquire exactly the
`j` required residual values per tuple. The sample magnitude is bounded
by `(B_j+1)||e||infinity^j`. Thus, with the Taylor factorials included,

    RMS(Hhat-H(v)) <= Bstar k^(-qrate)+3 eta,

where `Bstar` is finite for the fixed `d,s`. Choose

    k=max(k0,ceil((32 Bstar exp(T-L))^(1/qrate))),
    eta=exp(-(T-L))/192.

The scaled error is at most `3/64`. Adding the local multiplier error
`1/64`, the actual PDE profile remainder `1/32`, and final scalar
approximation `1/64` gives RMS at most `7/64`. The far branch has
deterministic error at most `1/16`. The total query cap on every path is

    Q <= [1+J(J-1)/2] k^d.

Every internal mesh and root loop has a finite public bound. Rational
tuple sampling uses almost-surely terminating integer rejection; it
does not acquire unknown values while rejecting. Saturation defines
Borel off-promise rules without changing promised inputs. The proof
therefore gives an admissible finite-query algorithm.

## Evidence and limits

- Upper proof: `reviews/T65-local-stable-graph-upper-proof.md`, SHA256
  `58e862c9cfbaf0946605d30d9c8e8a37e2570c0c0719d626683f22db60fc9f81`.
- Independent upper audit: `reviews/T67-all-dimension-upper-independent-audit.md`,
  SHA256 `f7fc4f5e96782354e7aefb5d4e27b5e8ae086f285aab0625041cb96eae7fea26`.
- Lower synthesis: `04u-all-dimension-signed-query-lower-bound.md`, SHA256
  `6587b4ba1b30a904bb6b336d8ca22917baad12f7db26627ca313aef632d94117`,
  with the separately frozen T61/T64 author and audit proofs.

All fixed integers `d,s>=1` are now covered, including the old boundary
and every `d>4s`. Constants are not uniform as dimension grows. The
domain remains the normalized unit torus with the stated diffusion;
larger domains or weaker diffusion can introduce additional unstable
modes and are not covered by changing `d` in this theorem.

The finite coefficient tables and nested known-profile solves may be
enormously expensive. Matching arithmetic work, bit complexity,
variable-accuracy complexity and practical speed are unresolved.
R08 records these separate gates; the fixed-time R10b derivative sampler
addresses only a subroutine. T62 formalizes actual Bernoulli information
ingredients, not this upper theorem or the whole lower theorem. E4
tests a separate nonnegative algorithm against a scalar surrogate;
it is not numerical evidence for D29. Publication originality and
significance require further scrutiny. No prize conclusion is made.
