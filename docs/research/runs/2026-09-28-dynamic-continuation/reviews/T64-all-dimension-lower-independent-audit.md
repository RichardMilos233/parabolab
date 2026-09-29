# T64 — independent audit of the signed lower bound in every fixed dimension

**Verdict: GO for the conventional theorem in frozen T61. No mathematical
repair is required.** The marked-direction derivative estimate is proved
by the actual parabolic propagator, including short times. The finite
Hamming-layer mean and variance bounds are valid without spatial permutation
symmetry of the phase correction. The proof retains the full prior, pays
for its PDE-bad probability, and correctly obtains a worst-input expected
exact-point-query lower bound for every fixed pair of integers `d,s>=1`.

The resulting exponent is `2d/(2s+d)`. This extends the lower range of D25;
it does not extend the upper range of T56/T59/D27. In particular, this audit
does not establish matching complexity when `d>4s`, a common expensive
baseline, hardness of a single fixed profile, an arithmetic-work theorem,
a Lean certificate, numerical evidence, or a novelty claim.

## 1. Frozen evidence and independence

The complete 614-line author proof reviewed was
`reviews/T61-all-dimension-lower-proof.md`, SHA256
`404a237be72991ac60efb97c48b5ba2347384b0a30ffe3a98219a74d1604d691`.
The complete root candidate was
`reviews/R04-signed-all-dimension-lower-candidate.md`, SHA256
`2bc5129ec4b9da882d7b16543d03f0bc8f34989cc02f9b9a65c5e805c1f4ae75`.

I also checked accepted D25 in `04r-signed-many-bump-complexity.md`, the
oracle definition in `04o-unstable-phase-query-lower-bound.md`, the original
T50 urn argument and its T53 audit, and accepted D27 in
`04t-matching-signed-query-complexity.md`. The actual phase approximation
in T56 Section 3 is accepted background, but its relevant estimates and
the new T61 derivative argument were independently recomputed here.

This reviewer previously wrote T59 but did not contribute to R04 or T61's
new marked-direction derivation. T59 remains unchanged at SHA256
`47d3ce98ac19210e9bbcd318ac1de2fb9dddd5bc372bff201dc97d47572301ab`.
The present task owns only this new T64 report. Existing sources, accepted
ledgers, formal files, code, and numerical artifacts were read-only.

R04 explicitly offers direct proof of its weighted estimate as an
alternative to its proposed common-measure construction. T61 completes
that direct alternative. This GO does **not** certify the stronger
statement that one fixed positive measure dominates every third derivative
measure. Neither uniform total variation nor translation symmetry is used
to infer such a measure.

## 2. Exact theorem and oracle scope

Fix integers `d,s>=1`, a target `x*` on the normalized period-one torus,
and

    u_t=Delta u/2+u-u^3.

The input class consists of smooth periodic real `v` with

    ||v||infinity<=1/2,
    max_(|alpha|<=s)||partial^alpha v||infinity<=1,
    min v<0<max v.

There are `C>0,T0<infinity`, depending only on the fixed public parameters
and a fixed bump, such that for every `T>=T0` and every admissible algorithm
with

    sup_v E|H_T(v)-S_Tv(x*)|^2<=1/16,

one has

    sup_v E Q_T(v)>=C exp(2dT/(2s+d)).

More precisely, a finite prior chosen from those public parameters and `T`,
independently of the algorithm, has average expected query cost at least
that amount. An expensive member may depend on both `T` and the algorithm.

The information model is exactly the accepted one: opaque exact initial
point values, measurable adaptive rules and stopping, input-independent
randomness, and almost-sure halting on each promised input. Every
initial-data acquisition is charged. Biased or unbounded real outputs are
allowed. No formula, derivative, mass, phase, evolved-value, or input
metadata oracle is given. The analytic coordinate is a proof device for
the lower bound, not information supplied to the algorithm.

All constants may depend badly on the fixed dimension and smoothness.
The unit spatial period and normalized measure matter. Only derivatives
through the fixed total order `s` are uniformly bounded; no common bound
on higher derivatives or analytic radius has entered the proof.

## 3. The actual phase and its uniform spatial approximation

Set `nu=2*pi^2-1`, fix `0<a0<1`, and use the continuous-data ball
`||v||infinity<=a0` for the analytic proof. Scalar comparison yields
`|u(t)|<=ell_a0(t)<1` and

    1-b(t)^2>=(1-a0^2)exp(-2t),    b=integral u.

The exact centered equation gives

    b'=b-b^3-R,
    R=3b integral w^2+integral w^3,    w=u-b.

Monotonicity of the cube and the unit-torus Poincare inequality give
`||w(t)||2<=a0 exp(-nu*t)`. Thus `|R|<=5a0^2 exp(-2nu*t)`.
For `G(z)=z/sqrt(1-z^2)`, the identity
`G'(b)(b-b^3)=G(b)` proves the integral definition of `A` and its uniform
tail bound, with the exact `C0` in T61 (2.5). No closed evolution for the
initial mean is substituted for this identity.

The heat-series bound

    ||p_1||infinity
      <=rho=((1+exp(-2*pi^2))/(1-exp(-2*pi^2)))^d

follows by `n^2>=|n|` in each one-dimensional series. Heat convolution
contraction gives the same bound for `||p_t||infinity` for every `t>=1`.
Normalized volume also gives `||p_1||2<=rho`.

In the centered equation with `q=u^2+ub+b^2 in [0,3]`, the local propagator
is bounded by `exp(t-r)P_(t-r)` and the scalar source has size at most
`3||w(r)||2`. Over the last time unit the homogeneous and forced terms
are bounded respectively by

    e*rho*a0 exp(-nu*(T-1)),
    [3e*a0/(nu+1)]exp(-nu*(T-1)).

This verifies `Cw=a0 exp(nu+1)(rho+3/(nu+1))`. Inverting `G` and using
the global Lipschitz constant one of `Psi` gives T61 (2.7), uniformly on
the whole sup ball and including `A=0`.

## 4. One marked direction: the actual kernel proof passes

The variational equations in (3.2) are the differentiated mild PDE, with
the correct coefficients `-6u`, `-6`, and the three order-two/order-one
pairings. Their products use disjoint derivative labels. The potential
`c=1-3u^2` lies in `[-2,1]`, so the actual positive fundamental propagator
satisfies

    |V(t,r)f|<=exp(t-r)P_(t-r)|f|.

At order one this immediately gives the marked bound
`|U_3(t,x)|<=exp(t)P_t|h3|(x)`.

At order two, bound the unmarked first variation in sup norm, retain the
marked `P_r|h3|`, and concatenate heat kernels. The scalar time factor is

    6 exp(t) integral_0^t exp(r)dr
      =6 exp(t)(exp(t)-1)<=6 exp(2t).

At order three the ternary term has coefficient `6`; the three binary
terms each contribute at most `6*6`. Their total is `114`, and the time
integral is

    114 exp(t) integral_0^t exp(2r)dr
      =57 exp(t)(exp(2t)-1)<=57 exp(3t).

In every term exactly one factor carries the marked label. After the
other factors are bounded in sup norm, heat composition gives
`P_(t-r)P_r|h3|=P_t|h3|`. The bounded variable coefficient `u` and the
Feynman--Kac weights have already been dominated before this operation.
They do not require translation invariance of the actual solution.

Consequently (3.3)--(3.4) hold with `c0=c1=1`, `c2=6`, `c3=57`. The bound
also holds for signed directions, since the comparison uses absolute
values. It is a direct marked heat-path estimate, not an inference from
an operator norm or a measure norm on a product of leaf coordinates.

Integrating the marked estimate gives the `L1` and scalar mean bounds
in (3.5), since heat flow preserves the integral of a nonnegative function.
At `t=0`, the marked first variation is `h3` and the higher variations
vanish, so these statements remain valid. In particular no short-time
`t^(-d/2)` loss is present.

Only for `t>=1` is the heat-kernel supremum used. It gives the sup bounds
with `M_j=c_j rho`, retaining `||h3||1`. This time separation is valid in
every fixed dimension. An arbitrarily concentrated continuous marked
direction does not force its sup norm back into any later estimate.

## 5. Centered energy retains the mark and the constants

With `b_S=integral U_S` and `W_S=U_S-b_S`, direct centering gives (4.2).
On mean-zero functions the homogeneous energy form is

    -(1/2)||gradient z||2^2+integral c z^2
      <=-nu||z||2^2.

The projection term drops out of this pairing, and the equation preserves
mean zero. Its `L2` propagator therefore contracts by `exp(-nu*(t-r))`.
Also, by orthogonal projection and `|u+b|<=2`,

    ||c-Pi c||2<=3||u^2-b^2||2<=6||w||2.

At second order, subtracting the spatial constant `b b_i b_j` gives
exactly the three terms in (4.4). At third order both telescoping
identities in (4.5) have the correct factors. Every term has a centered
factor. Put that factor in `L2` and the other factors in their time-one-
and-later sup bounds. If the centered factor has the mark, its inductive
`L2` estimate retains `||h3||1`; if another factor has it, that factor's
sup estimate retains `||h3||1`. Disjoint labels imply exactly one marked
norm in the resulting product.

The source constants in (4.6) check term by term:

    C1=6a0 M1,
    C2=6a0 M2+6a0 M1^2+12M1 N1,
    C3=6a0 M3+18N1 M1^2
                       +18(a0 M2 M1+N2 M1+M2 N1).

The first term in each is from `b_S(c-Pi c)`. The coefficient `18` for
the ternary forcing is three telescoping terms times `6`, while the
other `18` is three binary pairings times `6`.

At time one, normalized volume and projection contraction give
`||W_S(1)||2<=M_j exp(j)H_S`, without an extra factor two. Its homogeneous
evolution is bounded for `t>=1` by
`M_j exp(nu)exp((j-nu)t)H_S`, since `exp(j)<=exp(jt)`. The source integral
is at most `exp((j-nu)t)/j`. Thus exactly the stated choices

    N_j=M_j exp(nu)+C_j/j

prove the centered estimates. Neither a missing time-one exponential nor
a growing time factor occurs. The supplementary centered sup bound
`2M_j exp(jt)H_S` follows by subtracting the mean.

These are ordinary scalar spatial energy estimates for given continuous
directions. No pointwise-in-leaf Radon--Nikodym argument or energy estimate
for signed measures is hidden in this induction.

## 6. Differentiation of the phase and the explicit weighted constant

Every derivative of `3b Pi(w*w)+Pi(w*w*w)` still has at least two centered
factors. On `t>=1`, put two in the proved `L2` bounds and the remaining
factor, when present, in a sup bound. Cauchy--Schwarz gives the rate
`exp((j-2nu)t)H_S`. The ordered label assignments give exactly
`j!/(a!b!c!)` terms of cardinalities `(a,b,c)`, so the formula for `R_j`
in (5.1)--(5.2) is a valid upper constant. In particular its order-zero
value is `3a0^2+2a0^2=5a0^2`.

At short times the marked centered variation has `L1` norm at most
`2c_j exp(jt)H_S`; an unmarked one has that sup bound. If the mark is in a
mean derivative, use its scalar bound instead. Hence each ordered term
in `3b Pi(w*w)` costs at most `3*2*2=12` times the product of its `c`
constants, and each term in `Pi(w*w*w)` costs at most `2^3=8`.
The stated `S_j=20 sum multinomial*c_a*c_b*c_c` is therefore correct,
including at time zero. No spatial density supremum is used there.

The displayed derivatives of `G` are correct:

    G'''(y)=(3+12y^2)/(1-y^2)^(7/2),
    G''''(y)=(45y+60y^3)/(1-y^2)^(9/2).

Together with the scalar comparison gap, they give `g0,g1,g2,g3` exactly
as stated. The chain rule has one, one, two, and three types of terms
through order three. At order three they are

    G''(b)b_123,
    G'''(b)(b_12 b_3+b_13 b_2+b_23 b_1),
    G''''(b)b_1 b_2 b_3.

This verifies the coefficient `3` in `alpha3` and all the other `alpha`
constants. The all-time mean bounds use `c_j`, not `M_j`; this is valid
because they came directly from the marked `L1` estimates.

In a Leibniz term with `q` derivatives on `G'(b)`, the late exponent is
`(3q+3)+(3-q-2nu)-1=2q+5-2nu`, at most `11-2nu`. The short-time exponent
is at most `11`. Exactly one side of the product carries the mark, so
its norm factor remains `H_{123}`. The binomial sums for `L_short` and
`L_late` count all these assignments.

Since `2nu=4*pi^2-2>34>11`, integration gives precisely

    B=g2+L_short*(exp(11)-1)/11
          +L_late*exp(11-2nu)/(2nu-11).

The initial `g2` term bounds the third derivative of `G(integral v)`;
it uses `|integral h3|<=||h3||1`. The resulting `B` is positive and finite
for every fixed `d` and `a0<1`, and contains no derivatives of the datum.

The exchange of derivatives and the infinite-time integral also passes.
On truncated intervals away from time zero, finite-time mild
differentiation gives continuous multilinear derivatives. The uniform
short-time bounds control the omitted interval as its length tends to
zero. The late bounds for orders zero through three are integrable and
uniform on each closed sup ball strictly inside the open unit ball.
Replacing the one `L1` direction norm by its larger sup norm gives the
ordinary operator-norm bounds needed for uniform convergence of these
derivatives. Successive line-segment fundamental-theorem-of-calculus
identities identify the limit as a genuine `C3` Frechet functional.
Operator-norm continuity of `P_t` at `t=0` is neither needed nor asserted.
One may use a slightly larger ball to handle derivatives at the boundary
of the fixed closed `a0` ball.

The conclusion is the actual weighted estimate

    |D^3A(v)[h1,h2,h3]|
      <=B||h1||infinity||h2||infinity||h3||1.

No stronger simultaneous domination of derivative measures is required
for any subsequent step.

## 7. Cell sensitivity and full-layer concentration

Oddness of the PDE and `G` gives oddness of `A`. At zero the variational
mean is `exp(t)integral h`, so `DA(0)h=integral h`; odd `C3` regularity
gives `D^2A(0)=0`. For `F=A-integral`, Taylor's formula for `DA` therefore
gives the exact integral remainder and the bound

    |DF(v)[h]|<=integral_0^1 (1-r)|D^3A(rv)[v,v,h]|dr
              <=(B/2)||v||infinity^2||h||1.

For the disjoint bump family, a sign flip changes the datum in `L1` by
exactly `2Aamp I/K`. Its entire joining segment has sup norm at most
`Aamp`. Thus the change in `F` is at most `B I Aamp^3/K`, and the weaker
`Lflip=B Aamp^3/K` is valid since `I<=1`. A swap costs at most `2Lflip`.
The flip path may leave a particular Hamming layer; the analytic sup ball
contains that whole path, so this is harmless.

For the balanced layer, sign reversal pairs profiles with opposite `F`,
giving mean zero. Starting from a uniform balanced positive set and adding
a uniformly selected subset of `r/2` negative positions gives a uniform
positive set of size `(K+r)/2`: each final set has the same number of
balanced predecessors with equal pair probabilities. This coupling uses
`r/2` flips, proving `|E_pi_r F|<=r Lflip/2`. It does not require `F` to
be invariant under a spatial permutation of cells.

For the variance coupling, fix a revealed prefix and suppose both next
signs are possible. Let the remaining suffix have `N` positions. When the
next sign is positive its positive suffix has some size `m`; when it is
negative the size is `m+1`. Choose a uniform `m`-subset and then one
uniform complement position. The enlarged set is uniform among
`(m+1)`-subsets, by equal predecessor counts. The resulting full vectors
differ by one swap, so the two conditional means of `F` differ by at most
`2Lflip`. This also describes correctly the cases `m=0` or `m=N-1`.
If the next sign is forced, its martingale increment is zero.

The conditional increment variance is consequently at most
`p(1-p)(2Lflip)^2<=Lflip^2`. Orthogonality of the finite Doob increments
gives `Var_pi_r F<=K Lflip^2=B^2 Aamp^6/K`. All these statements concern
the full original layer. No independent-coin substitution or unspecified
slice-Poincare constant appears.

For its positive mass `m=Aamp I r/K`, the mean-to-mass ratio is at most
`B Aamp^2/(2I)`. Once this is at most `1/8`, the event `|F|>m/4` implies
`|F-EF|>m/8`. Chebyshev then gives

    P(|F|>m/4)<=64B^2 Aamp^4 K/(I^2 r^2)
                  <=64B^2 Aamp^4/I^2.

The proposed condition `Aamp^2<=I/(64B)` gives probability at most `1/64`,
stronger than the later `1/32` allowance, and implies the mean condition.
Sign reversal proves the same conclusions on the negative layer.

This is where the new argument removes the old dimension restriction:
the correction's standard deviation is `O(Aamp^3/sqrt(K))`, while the
layer mass is of order `Aamp/sqrt(K)`. Their ratio tends to zero with
`Aamp^2` for every fixed `d,s>=1`. It is unnecessary to control every
arrangement by the old worst-arrangement `exp(T)Aamp^3` bound.

## 8. All configurations and all sufficiently large horizons

With `a=1/(8D)`, `q=s+d/2`, and the choices (8.1), `R_T>=4` gives
`R_T/2<=k<=R_T`. Even `k` gives even `K`. When `K>=2048`,

    sqrt(K)<=r<=sqrt(K)+2<=2sqrt(K)<=K/4.

Both layer counts are therefore positive integers strictly below `K`.
Every profile in both layers, whether PDE-good or PDE-bad, has both strict
signs because the fixed nonnegative bump has positive mass. Compact
support inside its cell gives a smooth periodic extension. Derivatives
of total order `|alpha|<=s` have bound
`aD k^(|alpha|-s)<=1/8`, and the height is at most `1/8`. All selected
inputs lie in the original fixed class, with no promise about higher
derivatives.

The exact scale identity is

    exp(T)m=(R_T/k)^q*r/sqrt(K).

It proves the two mass bounds in (8.2). On the good positive-layer event,
`A=m+F>=3m/4`, so `Psi(exp(T)A)>=Psi(3/4)=3/5`. Subtracting the uniform
PDE error `1/32` leaves `91/160>1/2`. The negative-layer inequality has
the opposite sign. This is separation of actual PDE targets using the
actual coordinate.

An integer `k_*>=4` meeting the three threshold conditions in T61 Section 8
exists because `s>=1`. The bound
`T>=q log(2k_*)-log(aI)` implies `R_T>=2k_*` and hence `k>=k_*`.
The two additional logarithmic bounds each make their corresponding
term of `E(T)` at most `1/64`; their sum is at most `1/32`. The use of
`max(0,log(...))` also handles constants less than `1/64`.

Thus one finite threshold works for every real `T` beyond it, including
between changes of the even floor. There is no subsequence restriction
and no remaining inequality involving `d<=4s`.

## 9. Unconditioned prior, adaptive information, and expected cost

The proof keeps the two full uniform Hamming layers with equal weights.
It never conditions on the PDE-good set. On each good input the estimator's
MSE bound and target magnitude above `1/2` make the zero-threshold sign
test's error at most `1/4`. On a bad input use only the bound one.
The full-prior Bayes error is therefore at most
`1/4+1/32=9/32`. This is a valid loose bound and keeps an explicit charge
for the exceptional prior probability.

For an exact point query, disjoint supports reveal at most one cell sign.
Giving that complete sign even where the bump value is zero only makes
the oracle stronger. Half-open cells handle boundaries; repeated queries
can reuse an already revealed sign. For a capped original procedure,
simulate its answers from this stronger oracle and pad the distinct
revealed signs to `n=floor(K/1024)` using unused cells. Its locations,
stopping decision, and returned label are a common measurable function
of the seed and this padded sequence.

Conditional on a fixed seed and previously revealed signs and indices,
unused positions remain exchangeable under either full layer. The next
adaptively chosen unused position thus has the stated urn law. The
PDE-good set need not have that symmetry, which is why not conditioning
on it is essential.

For `l<n` and `j` positives revealed, the two probabilities differ by
`r/(K-l)<=2r/K`. Both hypotheses assign positive probability to every
such prefix, since their smaller sign count is at least `3K/8>n`.
Using `l<=K/8` and `r<=K/4` gives

    p_minus>=(3K/8-K/8)/K=1/4,
    p_minus<=(K/2)/(7K/8)=4/7<3/4.

The elementary Bernoulli KL bound from `log x<=x-1` then gives

    KL(Ber(p_plus)||Ber(p_minus))
      <=(p_plus-p_minus)^2/[p_minus(1-p_minus)]
      <=(64/3)r^2/K^2<=256/(3K).

The chain rule sums this to at most `1/12`. The private seed has the same
input-independent law under both hypotheses; conditioning on it does
not change the urn calculation. Adaptive indices and the original value
transcript are then covered by data processing. With natural logarithms,
Pinsker gives total variation at most `sqrt(1/24)<1/4`, so every capped
test has equal-prior error at least `3/8`.

If the full-prior average expected original point-query count `qbar` is
infinite, the claim is immediate. Otherwise stop the sign test before
original query `n+1` and choose a fixed label there. Its decision can
change only when `Q>n`, whose prior probability is at most `qbar/n`.
Therefore

    3/8<=9/32+qbar/n,
    qbar>=3n/32>=3K/65536.

The last step uses `floor(K/1024)>=K/2048` for `K>=2048`. This is a
genuine expected-cost argument; no fixed cap or independence of stopping
from answers is imposed on the original estimator. Rare expensive runs,
biased outputs, and unbounded real outputs are included.

The original measurability and almost-sure halting assumptions suffice.
At each fixed `T` the prior is finite, so exceptional null seed sets can
be removed simultaneously across its members. Truncation and padding
preserve measurable rules. No noise is introduced into the exact spatial
oracle; the only input randomness here is the finite prior used to prove
a worst-case bound.

Finally `k>=R_T/2` gives

    qbar >=3*2^(-d-16)*(aI)^(d/q) exp(dT/q)
          =C exp(2dT/(2s+d)).

The prior is fixed before choosing the algorithm. Passing from its average
to an expensive member preserves the stated quantifier order and does
not supply a common baseline or a fixed hard profile across horizons.

## 10. Review boundary and frozen deliverable

I found no unresolved mathematical gate in the marked weighted estimate,
the layer concentration, or the exceptional-prior information reduction.
The new lower theorem can be treated as conventionally passed within the
exact scope in Section 2. The stronger common-measure proposal in R04
remains unnecessary and is not certified by this verdict.

For background I revisited Kunsch--Rudolf, Section 2.1: adaptive exact
function evaluations and finite-prior reductions have explicit classical
precedents. That source is not used to fill the new PDE derivative or
layer-concentration obligations. [Primary paper](https://arxiv.org/pdf/1809.09890).
This was not a priority search.

No all-dimensional upper theorem, practical work bound, formal proof,
numerical experiment, or publication conclusion is added. T56/T59's upper
scope and every frozen source remain unchanged. This review performs only
read-only source/hash inspection, mathematical derivation, and a bounded
primary-source check; its sole write is this audit file.

Research-role metadata: T64 is a separate audit of T61's new derivation.
The reviewer made no model-setting change; backend/model settings are not
independently exposed in this context. The final hash of this report is
reported externally after its final write, avoiding a self-reference.
