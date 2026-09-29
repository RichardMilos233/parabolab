# T67: independent audit of the all-dimension signed query upper bound

Date: 2026-09-29.

**Verdict: GO for the conventional upper theorem in frozen T65.** I found
no blocking mathematical, oracle, measurability, finite-computation, or
halting gap. For every fixed pair of integers `d,s>=1`, T65 establishes
an admissible algorithm on the full stated signed class with uniform
absolute RMS at most `7/64<1/4` and deterministic exact-initial-value
query cap `C exp(2dT/(2s+d))`, for all sufficiently large public `T`.
No additional assumption or weakening of that target is needed.

This is an independent conventional mathematical audit. I did not
contribute to R07 or T65, and did not use a root self-review as acceptance
evidence. Reading the already accepted T56/T59 dependency does not
replace the checks of T65's new all-order construction below. The only
file written by this task is this new T67 review. All frozen proofs,
accepted ledgers, code, formal files, experiment data, and canvases are
preserved.

The separately accepted D28 lower bound is not a dependency of this
upper proof. This audit does not synthesize a matching theorem or edit
the accepted ledger. It supplies no runtime bound, dimension-uniform
constant, large-domain extension, Lean certificate, numerical result,
or novelty conclusion.

## 1. Exact evidence and theorem being accepted

I read all 1003 lines of `T65-local-stable-graph-upper-proof.md`, all of
R07, the complete 717-line T56 and 544-line T59, accepted D27/04t, and
the exact query-model statement in 04o. I also inspected the project
research guide, run context and latest checkpoint, and relevant accepted
claim-ledger entries. The frozen hashes checked for this audit are:

    reviews/T65-local-stable-graph-upper-proof.md
    58e862c9cfbaf0946605d30d9c8e8a37e2570c0c0719d626683f22db60fc9f81

    reviews/R07-local-stable-graph-upper-candidate.md
    adbe2c455bc36b22b5414b6090930e2f0e92711a85029643ca517d6676d52071

    reviews/T56-signed-upper-feasibility.md
    0f0cd6a6fbe97d5746c42f2da94161284f4b4fb3da70b724b5992450388d5933

    reviews/T59-signed-upper-independent-audit.md
    47d3ce98ac19210e9bbcd318ac1de2fb9dddd5bc372bff201dc97d47572301ab

    04t-matching-signed-query-complexity.md
    260ae16cb5104bfdc56eadc8a7829410c1a4b73c81703b038665427313d8eca9

    04o-unstable-phase-query-lower-bound.md
    67d6463087775a857a2ffc035fa6ef7fa31db47b4c99b496ecdcc9e8f87fd765

The equation, domain and promised inputs are exactly

    X=(R/Z)^d with normalized Haar measure,
    u_t=Delta u/2+u-u^3,   u(0)=v,
    v in C^infinity(X), ||v||infinity<=1/2,
    max_(|alpha|<=s)||partial^alpha v||infinity<=1,
    min v<0<max v.

The target is the actual value `S_Tv(x*)` at one fixed point. The
algorithm obtains unknown-input information exclusively through charged
exact values `v(y)`. Repeated acquisitions and preprocessing acquisitions
count. The algorithm may be biased, use transcript-dependent rules and
private randomness, and process exact real responses by Borel rules;
it must halt almost surely on every promised input. No unknown formula,
mean, derivative, phase, or evolved-value oracle is supplied.

T65 proves an upper theorem under this model, with finite constants
depending on fixed `d,s`. The enlarged `7/8` ball is an auxiliary
domain, not a new promise on the signed input. The upper construction
in fact handles more inputs, but does not exclude any member of the
displayed class. The argument never imposes a distance from the stable
interface.

The accepted T56/T59 inputs used by T65 are the actual `C^3` phase `A`,
its uniform ordinary third derivative bound, the phase and spatial
remainder estimates, paid smooth interpolation, and finite evaluation
of `A` on known smooth formulas. These analytic facts hold in every
fixed dimension; D27's restriction `d<=4s` entered the quadratic
algorithm's Taylor balance. T65 does not assume higher derivatives of
the global phase or reuse T61's marked-direction derivative estimate.

## 2. Stable heat kernel, trajectory contraction and graph

The explicit signed kernel

    B_t(x,dy)=exp(t)(P_t(x,dy)-lambda(dy))

has the asserted total-variation bound, including `t=0`. For `t<=1`,
`||B_t||TV<=2 exp(t)` and the proposed `M` dominate it after multiplication
by `exp(nu*t)`. For `t>=1`, factor `exp(-2*pi^2*(t-1))` from the
nonconstant heat Fourier modes and use `n^2>=|n|` in each coordinate.
This gives `exp(2*pi^2)(rho-1) exp(-nu*t)`, below the proposed
`M exp(-nu*t)`. This is a bound on the kernel itself, not an assumed
multilinear representation theorem.

The linear map `L` on `E_sigma` has forward and backward norm bounds

    M/(nu-sigma),          1/(1+sigma),

respectively. Its time integrals are continuous `C(X)` trajectories:
strong continuity handles the forward heat integral, and dominated
convergence on compact time intervals plus the integrable tail handles
the backward integral. The product of three trajectories has
`E_sigma` norm at most the product of their norms.

For `||Qz||<3r`, use `B_tz=B_t(Qz)`. The fixed-point map has norm at most

    3Mr+Cstar R^3 <= 3R/4+R/8=7R/8

on the radius-`R` ball, and contraction constant
`kappa=3 Cstar R^2<=3/8`. All restrictions on `R` can be achieved by
decreasing one positive public number, with `r=R/(4M)`; none is a
contradictory lower bound on `R`.

The backward mean term has the correct positive sign. Writing
`b(t)=Pi U(t)` gives

    b(t)=integral_t^infinity exp(t-rho) Pi(U(rho)^3) d rho,
    b'=b-Pi U^3,
    b(0)=Theta(w).

Combining this identity with the centered forward equation recovers
the full mild PDE starting from `w+Theta(w)`. Uniqueness therefore
identifies the constructed trajectory with the actual solution. Also

    |Theta(w)|<=R^3/(1+3sigma)<=r/8.

Even for `||w||<3r`, the initial graph datum has norm below
`25r/8<25/64<7/8`, so using the accepted phase there is justified.
The trajectory decays in `E_sigma`, and its phase is zero.

Ordinary `C^infinity` dependence on `z` follows from the implicit
equation on `C(X) x E_sigma`: the derivative in the trajectory variable
is `I-L(3U^2 .)`, whose inverse is bounded by `(1-kappa)^(-1)`.
The solution is strictly inside the radius-`R` ball. This establishes
ordinary differentiability before, and independently of, constructing
the derivative measures.

## 3. The signed-kernel Banach space is valid

For each fixed `j`, T65 uses actual finite signed Borel measures on
`X^j`, indexed by every `(t,x)`, with norm

    sup_t exp(sigma*t) sup_x ||K(t,x;.)||TV.

There are no rootwise almost-everywhere versions or exceptional sets
that could depend on a leaf tuple. A norm-Cauchy sequence has a TV limit
at each root and time. The weighted uniform Cauchy bound passes to that
limit, proving convergence in the displayed norm. For every Borel set,
its evaluation is a pointwise limit of Borel functions. Hence the limit
is a kernel and this space is complete.

The countable-algebra argument for variation measurability is correct.
Fix a Borel leaf set `A` and a countable algebra generating the Borel
sigma-algebra of `X^j`. For each individual root measure, approximate
its Hahn partition in the finite measure `|K|` by algebra sets. This
proves that variation on `A` is the supremum over finite algebra
partitions of the sums of absolute evaluations on `A` intersected with
the partition cells. There are only countably many such partitions,
and every evaluation in this supremum is Borel in `(t,x)`. Thus
`|K|(A)` is Borel. The identities

    K^+=(|K|+K)/2,         K^-=(|K|-K)/2

give Borel Jordan kernels as well. The approximating algebra sets may
depend on the individual root measure; the countable supremum formula
does not require a measurable choice of those sets.

For tensor products, rectangle evaluations are Borel. Positive kernels
extend this property to all Borel product sets by a monotone-class
argument, and finite Jordan expansion handles signs. Tensoring disjoint
leaf labels and then permuting them therefore constructs actual kernels,
with TV bounded by the product of the factor TVs. When each factor
has weight `sigma`, the extra decay `exp(-(p-1)sigma*t)` for a product
of `p` factors can be discarded. Continuous trajectory multipliers
are covered by the same bound.

For spatial composition, the setwise measure

    A -> integral K(rho,y;A) D(t,rho,x;dy)

is countably additive whenever `integral ||K(rho,y)||TV |D|(dy)` is
finite. Domination by this variation envelope justifies convergence
on disjoint unions and pairing with bounded leaf test functions.
Jordan decomposition and the usual simple-function construction prove
measurability with the parameters. Applying the same reasoning to
time integration supplies T65's `L` on kernels.

The heat kernel is jointly Borel at positive lag from its explicit
density, and at lag zero its set evaluations are `1_A(x)`. Thus the
lag-zero Dirac term does not create a measurability gap. The forward
and backward variation envelopes give exactly the two constants in
`Cstar`, with TV taken before the root supremum.

There is a useful distinction here: truncating the backward integral
at one fixed absolute time need not converge uniformly in the weighted
norm over all later root times. T65 only uses the absolutely convergent
setwise integral at each root to define a bounded operator on the
kernel space. Its Neumann series then converges in that Banach norm.
The proof does not require the false uniform absolute-time-truncation
claim.

No Bochner measurability of `x -> delta_x` in the TV norm is needed or
asserted. No disintegration or jointly chosen Hahn decomposition is
needed either: the construction starts with explicit kernels and
performs the forward integrations just described.

## 4. Identification with every finite actual graph derivative

The ordered three-block formula retains every input label. Exactly
three partitions place all `j` labels in one block, giving
`3u^2 U_[j]`. All other blocks have lower order; at `j=1` the proper
source is zero. At orders two and three the proper-source coefficient
counts are, respectively,

    6u U_1 U_1,
    6 U_1 U_1 U_1 + 18u U_2 U_1

when equal directions are substituted, consistent with the cubic.

The first source is the explicit signed kernel `B`. Every later source
is a finite sum of tensors of already constructed lower-order kernels,
multiplied by zero-order trajectories when needed. The feedback map
`K -> L(3u^2 K)` has norm at most the same `kappa<1` at every order.
Consequently the Neumann construction converges in weighted TV to
actual countably additive measures, with precisely the recurrence
`v_j` in T65 (4.4). The coefficient `j!/(a!b!c!)` counts the ordered
partitions of the distinct derivative labels. There is no missing
factorial or order-dependent contraction constant.

To identify this measure construction, pair its order-`j` equation
against an arbitrary product of continuous directions. Tensor products
produce the required products of lower variations. The variation
envelopes justify all spatial, time and series interchanges. Inductively
the paired source is in `E_sigma`; its Neumann sum converges there.
The resulting trajectory solves exactly the differentiated fixed-point
equation. That equation has the unique bounded resolvent solution, so
it is the ordinary Fréchet derivative already supplied by the implicit
argument.

Integrating the root at time zero against Haar measure gives the
scalar measure representing `D^j F(z)`, with TV at most `v_j`. This
establishes T65 (4.6) for every prescribed finite `j`. It does not infer
a product measure from a generic bounded multilinear form.

All derivatives live in the same weighted trajectory space. Products
improve decay instead of introducing unstable `exp(jt)` factors in
this infinite-time construction. Accordingly no requirement such as
`j sigma<nu` or `3j+2<2nu` appears. The constants can grow rapidly with
`j`; only finiteness at the fixed chosen order is required.

## 5. Finite-time flow and composition measures

For an input in the strict unit ball, comparison preserves that ball
over `[0,L]`, so the first-variation potential `1-3u^2` has absolute
value at most two. The heat Volterra series is bounded term by term
by `(2L)^n/n!`, and therefore converges uniformly in rootwise TV to
an actual kernel. At higher order the same resolvent acts on the
proper lower-order cubic source. Its source integral has bound
`L exp(2L)`, proving the finite recurrence (5.1). The same pairing
argument identifies these kernels with the actual finite-time flow
derivatives. Local Picard differentiation followed by continuation
of the bounded solution suffices for ordinary `C^infinity` regularity.

The burn-in `L` is fixed independently of the target horizon and can
make `||Q S_Lq||<=r/16` simultaneously for every `||q||<=7/8`.
It follows that

    H(q)=Pi S_Lq-Theta(Q S_Lq)

is defined and smooth on an open set containing that entire closed
ball, even when the evolved mean is close to an equilibrium. The
large mean is irrelevant to the graph's centered argument. Smallness
of the mean is required only for the later multiplicative comparison.

For each chain-rule set partition, the product of flow kernels is a
Borel kernel in the intermediate root tuple: pull each kernel back
by the corresponding root projection, tensor, and permute the leaves.
Its variation is bounded by the product of the relevant `a_j^flow`.
Integrating it against the finite signed outer measure `tau_p` produces
a genuine finite measure, with TV at most

    v_p product_(blocks B) a_(|B|)^flow.

This verifies (5.5) directly. No disintegration of a generic multilinear
operator is being assumed. Summing the finitely many partitions and
the mean term yields (5.6) with the stated `B_j`. These bounds hold
uniformly on T65's open domain `D` and in particular throughout the
`7/8` ball. No Borel dependence of `q -> tau_j(q)` is required by this
argument or by the algorithm: for fixed `q` the measures prove bounds;
the algorithm computes scalar coefficients by a separate finite recipe.

## 6. The phase multiplier and paid branch test

Oddness gives `D^2A(0)=0`. Also `DA(0)=Pi`, either by the accepted
derivative convergence applied to `exp(-t)G(Pi S_tq)` at zero or by
the accepted phase formula. Twice applying the fundamental theorem
therefore gives

    |DA(p)[1]-1| <= K3 ||p||^2/2 <= 1/64

on the radius-`r` ball. The graph datum has phase zero, so integration
in the constant direction gives

    A(b+w)=c(b-Theta(w)),       63/64<=c<=65/64,

whenever the indicated segment stays in that ball. This includes
`b=Theta(w)` without a sign test.

For `c` in this interval,

    |partial_c Psi(cz)|
      = |z|/(1+c^2 z^2)^(3/2) <= 1/[2(1-1/64)].

The elementary bound uses `y/(1+y^2)^(3/2)<=1/2`; it follows from
`(1+y^2)^(3/2)>=1+y^2>=2y`. Integrating from one to `c` proves the
uniform output error at most `1/64`, regardless of the magnitude of
`z`. This multiplicative control is what permits arbitrarily small
nonzero distances from the interface.

The exact semigroup phase identity follows by shifting the limit:
`A(S_Lv)=exp(L)A(v)`. In its actual use both `v` and `S_Lv` lie in
the accepted phase domain. The argument does not evaluate the phase
of a far-branch evolved profile outside the `7/8` ball.

The only branch information is the paid coarse interpolant and its
known-profile finite solve. The combined error between `btilde` and
`Pi S_Lv` is at most `r/16`. Thus the far branch `|btilde|>r/2`
implies a signed mean greater than `7r/16`, and the spatial bound
implies pointwise signed values greater than `3r/8`. Scalar comparison
with `a=3r/8` gives the claimed error at most `1/16` for the specified
public large-time threshold.

On the near branch, every interpolating initial profile `q_theta`
has evolved mean at most `9r/16` in magnitude and centered norm at
most `r/16`. Hence `||S_Lq_theta||<=5r/8`. For `v`, the associated
stable graph datum has norm at most `3r/16`. Their constant-direction
joining segment lies in the radius-`r` ball, which verifies every
hypothesis of the multiplier estimate. Threshold equality is assigned
to this safe near branch. No exact unknown mean or phase is used.

## 7. Known-profile evaluation is finite and uses no extra input values

The explicit Euler/central-difference scheme is monotone on `[-1,1]`
under the stated CFL condition. Its diagonal derivative is at least

    1-h_t*(d/h_x^2+2)>=0,

its off-diagonal derivatives are nonnegative, and its row sum is at
most `1+h_t`. The constant endpoint arrays are fixed. Consequently
the scheme preserves the interval and has the claimed stability.
An integer number of steps ending at `L` removes an endpoint-step
issue.

Spatial derivatives of the actual known-profile solution through order
four have finite public recursive bounds: the highest derivative has
potential `1-3u^2<=1`, and the remaining differentiated cubic terms
involve strictly lower positive derivative orders. The corresponding
maximum-principle recursion supplies the consistency constants. Time
order two requires no extra unknown-input regularity because

    u_tt=Delta^2 u/4+f'(u)Delta u
           +f''(u)|gradient u|^2/2+f'(u)f(u),
    f(u)=u-u^3.

The required initial derivatives belong to the known formula being
solved, not to the unknown `v`. Bounds can be chosen uniformly from
the finite partition sizes, scales and bounded formula coefficients.
The global mesh error, value-evaluation errors and any rounding errors
are therefore controlled by fixed finite mesh choices. Clipping after
updates is nonexpansive relative to the true interval-valued data.

A translated smooth positive partition on the uniform final grid can
be normalized to sum to one. Translation symmetry then makes every
weight integral exactly `1/Ngrid`. The smooth blend `p` consequently
has a known formula, exact arithmetic mean `Pi p`, and sup-norm error
at most `xi` after adding the public Lipschitz interpolation error.
This also implements the coarse mean test.

For graph evaluation, exact subtraction of that known mean yields
`wtilde=p-Pi p` with zero mean and

    ||wtilde-Q S_Lq||<=2xi,
    ||wtilde||<=3r/32       when xi<=r/64.

The scalar function `f(c)=A(c+wtilde)` on `[-r/4,r/4]` has its
root `Theta(wtilde)` in `[-r/8,r/8]` and derivative at least `63/64`.
All these profiles are within the radius-`r` ball. With phase evaluation
error `epsA=(63/64)zeta/4`, either the approximate sign safely selects
a half interval containing the root, or the uncertain-sign return has
root error at most `zeta/2`. After a fixed number of halvings the
interval width is at most `2zeta`, so its midpoint has error at most
`zeta`. No exact-zero decision or indefinite accuracy refinement occurs.

Each phase evaluation uses only the accepted known-profile procedure:
a public phase-tail time, a finite mesh solve on `c+wtilde`, and an
approximation of the transformed mean. Clipping the computed mean to
its scalar comparison interval controls the derivative of `exp(-tau)G`
by a public multiple of `exp(2tau)`. Arbitrarily small positive
`epsA` therefore needs a finite, possibly enormous, calculation.

The graph's Lipschitz bound gives the complete outer error

    |(Pi p-chat)-H(q)| <= (1+2v1)xi+zeta < epsilon

with T65's choices. Its strict slack is at least the difference between
`epsilon` and `3epsilon/4`. The nested initial profiles are all known
finite combinations of paid coarse values and public functions. At no
level does a mesh solver or root iteration acquire an additional `v(y)`.

## 8. Arbitrary-order Taylor coefficients and repeated directions

The chosen `J=ceil(1+d/(2s))` is finite, at least two, and satisfies
`Js>=s+d/2`. The Taylor expansion stops at `m=J-1`, with remainder
`B_J delta^J/J!` on the segment from `g` to `v`.

For a positive partition, the formal residual interpolant `Pe` has
norm at most `delta`. Its error is controlled using only the public
residual Lipschitz bound, including when `s=1`. The actual derivative
measure gives the ordered coefficient bound

    sum_I |D^jH(g)[theta_(i_1),...,theta_(i_j)]| <= B_j,

because the corresponding nonnegative products of partition weights
sum to one on `X^j`. Multilinear telescoping gives the action error
`j B_j delta^(j-1) epsilonP<=eta/2`. This calculation would not follow
from an arbitrary bounded multilinear operator alone.

The mixed forward-difference formula correctly treats the occurrences
of repeated indices as distinct labels. Repeating a direction does
not identify the kernel's leaf coordinates or remove any subset term.
The iterated fundamental theorem over `[0,1]^j` gives the exact
averaged derivative formula in T65. Subtracting the value at `g` and
using `B_(j+1)` bounds the error by

    h B_(j+1) integral_[0,1]^j sum_l t_l dt
       = (j/2) B_(j+1) h.

Therefore derivatives only through order `J` are needed. For the
specified increment and tolerances, the summed errors over `N^j`
ordered tuples are bounded by

    finite differences:    eta/8,
    scalar H evaluations: eta/8,
    rational rounding:    eta/8.

Their sum `3eta/8` is below `eta/2`. Since `delta<=1`, its action
on the residual products is below `eta/2`; combined with partition
error this proves (9.2). The coefficient weight bound `B_j+1` follows
from `eta<=1`. All Taylor factors `1/j!` remain in the estimator.

Every finite-difference profile has norm at most `13/16` on a promised
run. Off promise, clipping coarse responses and saturating the raw
interpolant to `[-13/16,13/16]` leaves enough room for perturbations
of norm at most `1/16`, yielding the closed `7/8` ball. That saturation
is the identity on all promised interpolants. No unknown norm test is
required to establish the evaluation domain.

## 9. Risk, every charged query, and the all-dimension rate

For each fixed input, the coarse transcript is deterministic. Conditional
on it, the rational coefficients and sampling laws are fixed. A sample
of order `j` has expectation equal to the desired finite weighted sum
and absolute value at most `(B_j+1)delta^j`. Independent samples within
an average therefore give standard deviation at most
`(B_j+1)delta^j/sqrt(Mquery)`. Independence across different orders is
unnecessary for the Minkowski bound.

The deterministic coefficient error is at most
`eta*(1+sum_(j=1)^m 1/j!)<3eta`. Adding the Taylor remainder proves
T65 (10.2), including every factorial. The random errors have powers
`k^(-js-d/2)`, all bounded by the leading `k^(-s-d/2)`. The remainder
is bounded by that same power since `Js>=s+d/2`. Equality is allowed;
no strict inequality or unmentioned asymptotic slack is needed.

With the exact choices of `k` and `eta` in (10.3), scaling the proxy
error by `exp(T-L)` gives

    Bstar k^(-qrate) exp(T-L) <= 1/32,
    3eta exp(T-L) = 1/64,
    exp(T-L) RMS(Hhat-H(v)) <= 3/64.

The global 1-Lipschitz property of `Psi`, the local phase multiplier
and the accepted PDE profile remainder then give near-branch RMS

    3/64 + 1/64 + 1/32 = 6/64.

Final scalar approximation adds at most `1/64`, giving `7/64<1/4`.
Clipping to `[-1,1]` cannot increase error against the actual PDE
target. The far branch has deterministic error at most `1/16`.
Each promised input belongs to one deterministic branch, so these
are uniform bounds, including all interface inputs.

Exactly `k^d` coarse values are charged. For order `j`, at most
`Mquery=k^d` tuples are selected, each acquiring `j` values, with
repeats counted. Zero-weight orders need no calls. Thus every run has

    Q <= [1+sum_(j=1)^(J-1) j] k^d
       = [1+J(J-1)/2] k^d.

No fine residual grid is acquired during coefficient construction.
All other evaluations are of already known formulas and reveal no new
input information. The exact ceiling and fixed thresholds imply
`k^d<=C' exp(dT/(s+d/2))`. This proves the asserted deterministic cap
for every fixed `d,s>=1`. The proof's constants may be very large;
their growth does not impose a finite upper bound on the allowed `d`.

## 10. Borel rules and almost-sure finite halting

The order of public parameter choices in T65 Section 11 is consistent.
There is no circular selection using an unknown solution norm. The
coarse coefficients are bounded, every public partition is finite,
and all known-profile derivative bounds and finite mesh sizes can be
fixed from these quantities and the prescribed tolerances. All root
loops have public finite maximum lengths.

Fixed smooth formula evaluation, finite arithmetic, clipping,
saturation, comparisons and fixed-precision rational rounding are
Borel transcript operations. Bisection's uncertain-sign branch deals
with equality without requesting an infinite real-number precision
test. The permitted model already treats oracle responses as exact
reals with Borel scalar processing; no finite-bit encoding claim for
arbitrary real responses is being inserted.

Rational coefficients give a finite distribution with integer weights
after multiplying by a common denominator. Uniform-integer rejection
from the smallest covering power of two has acceptance probability at
least `1/2`. Using fresh independent fair bits gives the required
independent draws. A fixed finite number of such draws terminates
almost surely for each input. Infinite rejection paths acquire no new
values while stuck, so even those paths cannot breach the data-query
cap. Zero total weights are skipped by an exact rational test.

The final scalar approximation is also finite. For example,
`|H(g)|<=1+r/8` and the bounded correction samples give a public finite
bound on `|exp(T-L)Hhat|` at each horizon. A fixed approximation of
`Psi` on that bounded interval to `1/64` is sufficient. Its arithmetic
does not call the unknown input. These observations establish the
stated measurable, almost-surely halting algorithm, rather than merely
an ideal measure-sampling estimator.

## 11. Primary-source check and scope of the verdict

I made one bounded search for signed-kernel variation/Jordan
measurability and inspected the finite-measure preliminaries and
countable-algebra approximation in Section 3.1 of Lovasz,
[Flows on measurable spaces](https://link.springer.com/article/10.1007/s00039-021-00561-9).
That primary source records the TV Banach space and uses approximation
in a finite measure by a countable generating algebra. It is background
confirmation; the kernel, derivative and algorithm arguments in this
audit were checked directly above. No disintegration theorem from
that paper is imported. This was not a priority or novelty search.

The proof avoids all the identified failure modes: generic multilinear
forms are not declared to be product measures; Dirac kernels are not
treated as TV-Bochner-continuous; higher global-phase smoothness is not
assumed; exact unknown phase or mean information is not used; and
fine residual nodes are queried only when sampled and fully charged.
No mathematical repair remains before conventional acceptance of
T65's stated upper theorem.

This verdict is limited to the normalized unit torus with the stated
diffusion and reaction, fixed finite `d,s`, fixed absolute target
accuracy, and the exact point-query model. It neither bounds auxiliary
arithmetic work nor validates a practical implementation. It implies
no theorem on arbitrary domains or weaker diffusion, no uniform
constant as dimension increases, no unbiasedness, and no new formal,
numerical or publication-priority claim.

Research-role metadata: T67 was assigned the skill's requested
`gpt-6-astra`/`max` mathematical-review routing. This worker made no
model-setting change; actual backend and effort are not independently
exposed by its tool telemetry. The math-auto-research skill, defaults,
model routing, general profile and execution guidance were read.
Work performed: read-only source inspection, hash checks, one bounded
primary-source search/inspection, independent mathematical checking,
and this single new review-file write. No subagent, code, numerical
experiment, Lean invocation, canvas, or ledger update was used.
The final file hash is reported in the handoff instead of self-embedded.
