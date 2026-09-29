# T68: independent audit of the fixed-burn-in derivative tuple sampler

Date: 2026-09-29. **Verdict: GO for frozen R10b in its stated
ideal-primitive model and explicit continuous-residual setting.** The
rate-two normalization,
bounded multiaffine partials, ordered-injection formula, actual Frechet
derivatives, product measures, second moment, query cap, finite expected
primitive work, and centered-root variant pass. No mathematical repair
is needed for the intended subroutine. The continuity and cost-model
clarifications below must remain attached to any downstream statement.

This is an independent audit of the 191-line final source
`reviews/R10b-finite-burnin-derivative-sampling.md`, SHA256

    23683587539ef2905e0679100325808ae3f6353a3782a4bb362b2d24252034f0

The original 187-line submission was
`reviews/R10-finite-burnin-derivative-sampling.md`, SHA256

    c8c0b8445e570a278d4ccdf8773edf44fb54b3128a57c95f568ff75b8f18032d

I read both complete versions and checked their exact diff. R10b changes
only the title/version note and the first paragraph's explicit residual
continuity and application context. R10 left that continuity implicit;
the root supplied R10b after I identified the standalone wording
ambiguity. The original signed input class is unchanged. References
below to R10's formulas and construction apply identically to R10b.

I did not contribute to R10's tuple sampler. I authored T65's separate
measure proof, but that result is neither assumed nor used to establish
any sampling, variance, differentiation, or work claim here. The
calculation below starts from R10's actual random tree and polynomial.
I read R08 for the surrounding work gates; those gates remain open
beyond this finite-time subroutine.

The sole T68 edit is this new audit. R10, R10b, T65, accepted ledgers, Lean,
code, and numerical artifacts are unchanged. No numerical experiment,
solver run, theorem-prover invocation, or implementation test was run.

## 1. Accepted scope and two precise conventions

Fix `0<=L<infinity`, an integer `j>=1`, the unit torus `X`, and a
known `g in C(X)` with `||g||infinity<=a<1`. In the intended use,
`v` belongs to the previously fixed smooth input class, so

    e=v-g in C(X),       ||e||infinity<=delta.

R10b's expression `D^j S_L(g)[e,...,e]` is the ordinary derivative
on `C(X)`, and hence has continuous directions. For merely bounded
Borel `e`, the same sampling formula remains defined and gives the
bounded-Borel extension of the derivative measure constructed below;
that is not a new Frechet-direction claim. Arbitrary nonmeasurable
residuals are not part of the theorem. This is a clarification of the
existing smooth-input context, not a restriction of that context.

The work theorem is explicitly ideal. It permits exact exponential,
Gaussian and uniform draws, elementary real arithmetic, comparisons,
indexing/modular reduction, and exact evaluation of the known `g` as
primitives. A Gaussian increment may be drawn directly with its known
time variance. It does not provide a finite-bit implementation of an
exact continuous query location or exact evaluation of an arbitrary
continuous function. In an application, `g` is the explicit formula
formed from previously paid values; its evaluation and preprocessing
costs still have to be counted. Section 7 separates these terms.

Within this model, for each root `x`, the output has

    E Z_j(x)=D^jS_L(g)[e,...,e](x),
    E |Z_j(x)|^2 <=delta^(2j) E N_L^(2j)
       <=delta^(2j) exp(2(3^(2j)-1)L),                 (1.1)

at most `j` new unknown-input acquisitions on every path, almost-sure
termination, and expected ideal work at most
`C_j(d+1)exp(4L)`. All statements concern a fixed finite `L,j`.

## 2. The bounded tree polynomial and its partial derivatives

The vertex map is

    M(a,b,c)=(a+b+c-abc)/2.

Its eight values at `{-1,1}^3` are exactly the majority sign. Because
it is affine in each coordinate separately, its value at any point
of `[-1,1]^3` is a convex combination of those corner values. Hence
`|M|<=1` on the cube.

A finite ternary genealogy is a tree, with disjoint sets of descendant
leaf labels under its three children. Inducting from the leaves proves
that the recursively evaluated `P_T(z_1,...,z_N)` is affine separately
in each leaf coordinate and lies in `[-1,1]` on the full leaf cube.
Shared spatial positions do not identify leaf labels or alter this
algebraic fact.

For distinct labels `i_1,...,i_j`, freeze all remaining coordinates
inside their cube. The coefficient of the product of the selected
coordinates, which is their mixed partial, is exactly

    partial_(i_1)...partial_(i_j)P_T(z)
      =2^(-j) sum_(epsilon in {-1,1}^j)
          (product_l epsilon_l)
          P_T(z with z_(i_l)=epsilon_l).               (2.1)

The selected mixed partial is independent of the selected coordinate
values. There are `2^j` summands, each bounded in absolute value by
one, so its absolute value is at most one. Repeated differentiation
with respect to a single leaf coordinate gives zero. This verifies
R10's bound for every order, including orders greater than the degree,
without any derivative estimate for `g`.

These are exact identities in a finite polynomial. They are not
finite differences with a small step and carry no discretization bias.
The use of corner values `+/-1` is legitimate although the base profile
is strictly inside the cube: `P_T` is a globally defined polynomial,
and the cube bound holds at its boundary too.

## 3. Nonexplosion, finite moments, and the exact expected tree size

Each existing particle splits into three at rate two. Thus the leaf
population starts at one and has jumps `n -> n+2` at total rate `2n`.
Before the first time `tau_K` it reaches or exceeds `K`, this is a
bounded-rate process. Its stopped population is at most `K+1`, so
Dynkin's formula is legitimate without presupposing nonexplosion.

For every integer `m>=1`,

    A(n^m)=2n((n+2)^m-n^m)
      =2 sum_(r=1)^m binom(m,r)2^r n^(m-r+1)
      <=2(3^m-1)n^m,       n>=1.                      (3.1)

The inequality uses `m-r+1<=m`; the coefficient sum is
`sum_(r=1)^m binom(m,r)2^r=3^m-1`. For the stopped process,
the generator contribution is multiplied by `1_(s<tau_K)`.
Consequently

    E N_(t wedge tau_K)^m
      <=1+2(3^m-1) integral_0^t E N_(s wedge tau_K)^m ds
      <=exp(2(3^m-1)t).                               (3.2)

For `m=1`, reaching `K` by time `t` implies
`N_(t wedge tau_K)>=K`, giving

    P(tau_K<=t)<=exp(4t)/K.

Letting `K` tend to infinity excludes a finite-time explosion.
Fatou, or monotone convergence along the stopped increasing counts,
gives all the finite moments asserted in R10.

For the first moment the generator is exactly `A n=4n`. Removing
stopping in its integral identity is justified by monotone convergence
and the finite first-moment bound. Thus

    E N_t=1+4 integral_0^t E N_s ds=exp(4t).            (3.3)

If `B` is the number of branching vertices, then `N=2B+1`. Each
branch replaces one leaf by three children, so the total number of
nodes, including leaves, is

    3B+1=(3N-1)/2.                                    (3.4)

All these statements are independent of `g`, `e`, and the spatial
root. Generation to a fixed horizon is almost surely a finite tree.
No depth or size truncation is part of the estimator.

## 4. The rate-two tree gives the stated Allen--Cahn flow

Start a particle at `x`. For each node, sample its rate-two clock;
its spatial endpoint is a Brownian increment with covariance equal to
the smaller of the remaining horizon and its lifetime, wrapped modulo
one. If it branches, all three children start at this same endpoint,
with independent subsequent clocks and increments. A sampled continuous
Brownian path is unnecessary because there is no path-dependent weight.

Let `u(t,x)` be the expectation of the root polynomial with terminal
values `g(X_i)`. It is bounded by one by Section 2. Conditional on the
first branching time and position, the three descendant subtrees are
independent, with the same conditional mean. Multiaffinity therefore
gives the exact renewal equation

    u(t)=exp(-2t)P_tg
       +integral_0^t 2exp(-2r)P_r[
                         (3u(t-r)-u(t-r)^3)/2] dr.     (4.1)

This is the mild equation with linear generator `Delta/2-2` and
source `3u-u^3`, hence with total reaction

    -2u+(3u-u^3)=u-u^3.

Equivalently `2(M(u,u,u)-u)=u-u^3`. The spatial generator is
`Delta/2` because each increment has covariance `r I`, not `2r I`.
These factors are checked directly, rather than taken from literature
with a different diffusion or vote normalization.

The bounded renewal solution is the bounded mild Allen--Cahn solution:
the reaction is Lipschitz on the bounded range, so subtracting two
bounded mild solutions and applying Gronwall gives uniqueness. Initial
continuity and boundedness follow either from (4.1), or by coupling the
finite marked tree and using the continuity of `g`. Thus

    u(L,x)=S_Lg(x)=E P_T(g(X_1),...,g(X_N)).             (4.2)

Terminal leaf positions are correlated through their common ancestry.
Only conditional independence of the child subtrees after a branching
event was used. Replacing their common starting position by independent
positions would be a different and incorrect construction.

## 5. Ordered labels, actual product measures, and C-infinity exchange

For a fixed finite marked tree define

    F_T(g)(x)=P_T(g(X_1),...,g(X_N)).

Its `j`th derivative in labelled directions `h_1,...,h_j` is

    A_(T,j)(g)[h_1,...,h_j](x)
      =sum_(i_1,...,i_j distinct)
          C_(i_1,...,i_j)(g,X)
              product_(ell=1)^j h_ell(X_(i_ell)),       (5.1)

where `C_I` is the selected leaf mixed partial in (2.1). The derivative
chain rule gives ordered injections of direction labels into distinct
leaf coordinates. Consequently there are `(N)_j` terms, with the
falling factorial understood as zero when `N<j`.

There is no missing or extra `j!`. For equal directions, each unordered
set of `j` leaves appears `j!` times in (5.1), exactly as required by
the ordinary `j`th derivative. A later Taylor coefficient would divide
this derivative by `j!`; R10 estimates the derivative itself.

The corresponding finite signed atomic measure is

    mu_(T,j)(g,x)
      =sum_(I ordered injection) C_I(g,X)
                        delta_(X_(i_1),...,X_(i_j)).   (5.2)

By Section 2 its total variation is at most `(N)_j`. Spatial atom
collisions may reduce the variation and cause no problem. Labelling
leaves by a fixed traversal order, clocks, marked increments, leaf
positions, coefficients, and each Borel-set evaluation of (5.2) are
measurable functions of the seed on the set of finite trees. Define
the measure to be zero on the null nontermination set.

For every Borel set `A subset X^j`, define

    mu_j(g,x;A)=E mu_(T,j)(g,x;A).

The integrable envelope `(N)_j<=N^j` allows dominated convergence on
disjoint unions. Hence this is a countably additive signed Borel
measure, and

    ||mu_j(g,x)||TV<=E(N)_j<=E N^j.                    (5.3)

For example, the variation inequality follows by bounding the sum over
each finite Borel partition by `E||mu_(T,j)||TV` and then taking the
partition supremum. There is no implicit Bochner integral of Dirac
measures in the total-variation norm and no generic multilinear
representation theorem in this step.

Here is the full rootwise and Banach-space differentiation justification.
Use one common marked-tree seed for every root and translate every
endpoint: `X_i(x)=x+Y_i modulo X`. For a fixed finite tree, (5.1) is
continuous in `x` when `g,h_ell` are continuous. Its absolute value is
at most `N^j product_l ||h_l||`, an integrable envelope independent
of `x`. Dominated convergence therefore makes

    A_j(g)=E A_(T,j)(g)

a bounded `j`-linear map into `C(X)`, with norm at most `E N^j`.
The same coupling also gives Borel dependence on the root for the
setwise measures in (5.3).

If `g,g'` are in the open unit ball, their joining segment stays in
the cube. One extra derivative label in (5.1) and the fundamental
theorem give

    ||A_j(g')-A_j(g)||op
       <=E N^(j+1) ||g'-g||infinity.                   (5.4)

This estimate is uniform in the root. More explicitly, for a small
increment `h` whose segment remains inside the ball, the tree-level
Taylor remainder for the `j`th derivative is bounded by

    (1/2) N^(j+2) ||h||infinity^2

in `j`-linear operator norm. Averaging yields

    ||A_j(g+h)-A_j(g)-A_(j+1)(g)[.,...,.,h]||op
       <=(1/2) E N^(j+2) ||h||infinity^2.              (5.5)

All these moments are finite by Section 3. Starting with
`A_0(g)=E F_T(g)=S_Lg`, induction using (5.5) proves that `S_L` is
`C^infinity` on the open unit ball and `D^j S_L(g)=A_j(g)`.
Equation (5.4) supplies operator continuity. Thus (5.1)--(5.3)
represent the actual derivatives into `C(X)`, not merely formal
termwise derivatives at a single root.

No smoothness of an infinite-time coordinate, invariant manifold, or
local stable graph is implied by this finite-`L` proof.

## 6. Unbiased tuple sampling, its second moment, and all data calls

When `N>=j`, sample an ordered injection `I` uniformly among its
`(N)_j` possible values. Conditional on the complete marked tree,
R10's return is

    Z_j=(N)_j C_I product_(ell=1)^j e(X_(I_ell)).        (6.1)

Its conditional mean is exactly the sum (5.1) with all directions
equal to `e`. When `N<j`, that sum vanishes and returning zero is
correct. Integrating over the tree and using Section 5 proves the
mean in (1.1).

The pathwise bound

    |Z_j|<=(N)_j delta^j<=N^j delta^j

gives

    E |Z_j|^2 <=delta^(2j) E (N)_j^2
                <=delta^(2j) E N^(2j).                (6.2)

The last moment is bounded by (3.2) with `m=2j`, giving precisely
R10's exponent `2(3^(2j)-1)L`. The falling-factorial moment could
give a sharper bound, but no sharper one is needed or claimed.

The only new unknown values in (6.1) are
`v(X_(I_1)),...,v(X_(I_j))`. The values of `g` are known formula
evaluations. Two distinct selected leaves can land at the same point;
both acquisitions are still charged. No residual value controls the
tree law, tuple law, or mixed-partial coefficient. Thus the data cap
is at most `j` on every completed run.

Generate the entire tree, choose the tuple, and compute the coefficient
before requesting these values. On a seed for which tree generation
or a discrete rejection sampler fails to finish, no subsequent data
acquisition occurs. The deterministic data cap therefore holds on
all seeds; termination itself is almost sure. If `g` was built from
earlier charged data, this argument applies conditional on that
transcript with fresh independent sampler randomness. It does not
erase or exempt the earlier coarse-data queries.

At `L=0` the tree has one leaf at the root. The sampler gives `e(x)`
for `j=1` and zero for `j>=2`, as required by the derivatives of
`S_0=I`. This endpoint requires no separate limiting assertion.

## 7. Concrete coefficient computation and the exact work boundary

The selected coefficient can be obtained as follows, using no PDE or
derivative oracle.

1. Cache `g(X_i)` for the `N` leaves.
2. For each of the `2^j` sign assignments in (2.1), replace the selected
   coordinates by those signs and propagate `M` upward through the
   already generated finite tree.
3. Sum the signed root values and divide by `2^j`.

There are at most `2^j` full passes, each linear in the number of
nodes. The fixed-order signs and their products can also be computed
within `C_j N` scalar operations. No tensor with `N^j` entries is
materialized. All unselected terminal values are cached; the selected
cached `g` values can subsequently be used in the residual factors.
Cancellation in (2.1) is exact in the ideal arithmetic model. A
floating-point error analysis is not supplied by this fact.

The genealogy has `(3N-1)/2` nodes. Each needs at most one clock and
one Brownian endpoint increment, the latter requiring `d` scalar
Gaussian primitives and coordinate operations. Generation, storage,
and the position bookkeeping therefore take at most `C(d+1)N`
ideal operations. The tree data also provide an array of its leaves.
The first `j` steps of a Fisher--Yates shuffle select a uniform ordered
injection; initializing the leaf array costs `O(N)`, and the selection
itself costs `O(j)` ideal integer-uniform primitives and swaps.

If those integer draws instead use fair-bit rejection, drawing from
a range of size `n` needs a number of trials with mean at most two,
each using `ceil(log2 n)` bits. A partial shuffle therefore uses at
most `Cj(1+log(N+1))` expected bits conditional on `N`. This is
integrable, for example because

    E log(N+1)<=log(1+E N)=log(1+exp(4L)).

Use the partial shuffle for this particular bit-count assertion;
the ideal-unit-cost linear-work alternative of a full shuffle does
not itself have the same `j log N` random-bit count. The source
correctly identifies the partial integer-selection method separately.
This discrete-bit observation does not simulate an exact Gaussian or
an exact continuously uniform root using finitely many bits.

With one known `g` evaluation counted as one primitive, all operation
counts above, including at most `j` data-call instructions and scalar
products, are bounded by `C_j(d+1)N`. Equation (3.3) then gives

    E Work_ideal <=C_j(d+1)exp(4L).                    (7.1)

This is an expectation, not a deterministic bound on tree size or
arithmetic work. For fixed `j`, the purely ideal constant can be
chosen independent of `L`; its dependence on `j` includes `2^j`.

For actual known-formula evaluation, the more informative accounting is

    Work <=C_j(d+1)N + sum_(i=1)^N Cost_g(X_i),         (7.2)

up to a changed fixed-order constant. If a public uniform bound
`Cost_g<=G` is available, this becomes
`E Work<=C_j(d+1+G)exp(4L)`. The cost of constructing the known
formula or its spatial lookup structure is additional caller-side
preprocessing. If `g` is a paid local interpolant, lookup, partition
evaluation, polynomial evaluation, access to its stored coarse values,
and any horizon dependence of those operations must all be retained.
R10 does not prove such costs uniformly constant merely by calling
`g` known. Conversely, those known-profile operations acquire no new
information about `v` when they use only its saved coarse transcript.

Measurability follows from a countable product seed, a fixed node/leaf
ordering, and finite arithmetic on the event that the tree is finite.
Every finite-shape event is Borel in its clock coordinates; endpoint
positions and tuple choices are Borel functions of the marks. With
continuous `g,v`, their evaluations are measurable. The null
nontermination event can be assigned output zero for the expectation.
Thus the stated continuous-seed ideal sampler is an admissible
measurable finite-query procedure with almost-sure halting. It is not
an executable finite-bit specification at exact random coordinates.

## 8. Mean and centered derivatives

Let `U` be uniform on the torus, independent of the other randomness.
Applying the same sampler at root `U` gives

    E Z_j(U)=integral_X D^jS_L(g)[e^j](y) d lambda(y)
            =D^j(Pi S_L)(g)[e^j].

The exchange with the spatial integral is justified by the uniform
moment envelope in (6.2), or by the continuous bounded derivative
from Section 5. Sampling `U` adds only `O(d)` ideal uniform primitives
and no unknown-input values before the residual tuple is acquired.

For the centered derivative at `x`, use one fair coin and one tree:

    Zcenter=2Z_j(x) on heads,
    Zcenter=-2Z_j(U) on tails.

Then

    E Zcenter=D^j(Q S_L)(g)[e^j](x),
    E |Zcenter|^2
      =2 E|Z_j(x)|^2+2 E|Z_j(U)|^2
      <=4delta^(2j) E N^(2j).                         (8.1)

The two alternatives are not both sampled on one run, so the cap is
still `j`, not `2j`. The same ideal expected-work order holds. This
construction proves the displayed finite bound only. A small actual
centered field or mean does not make its coin-mixture variance small.

## 9. What this audit does and does not resolve

R10 provides a concrete derivative-sampling primitive for `S_L`,
`Pi S_L`, and `Q S_L`, at fixed finite `L`. It avoids enumerating
the finite-time derivative coefficient tensor while simultaneously
proving an actual second-moment bound, a hard unknown-query cap, and
an expected ideal arithmetic-work bound. That specific part of R08's
derivative-work question is resolved conventionally by this proof.

The following limitations remain and are part of the accepted scope:

* It does not sample a derivative of `Theta`, the local stable graph,
  `H_L`, or the infinite-time phase. Composing or recursively sampling
  any such functional still needs its own joint signed-weight,
  variance, termination, and work proof. T65's measure existence does
  not supply that result.
* It does not evaluate the base phase or graph value to error
  `O(exp(-T))` at near-query-order arithmetic cost. The base-value
  obligation in R08 remains independent of this tuple sampler.
* A naive direct use with `L=T` retains expected population
  `exp(4T)`. For increasing derivative order or burn-in time, the
  factors `2^j`, `exp(4L)`, and the second-moment exponent
  `2(3^(2j)-1)L` must remain visible.
* The centered coin construction has (8.1), not a variance estimate
  proportional to the deterministic centered-flow contraction. A
  later stable-graph recursion cannot substitute the latter for the
  former.
* Coarse preprocessing and known-profile evaluation work remain real
  costs. Exact continuous randomness, integer/scalar word sizes,
  arithmetic cancellation, rounding, and random-bit generation need
  separate machine-level analysis.
* No all-dimension efficient-work theorem, practical speedup,
  stable-graph sampler, new voting representation, publication
  priority, or numerical/formal verification follows from this audit.

There is no conflict with the already proved query upper bound: that
theorem permits large finite auxiliary computation. R10 addresses a
particular possible replacement for one such computation; it does not
upgrade the whole theorem to a matching work bound.

## 10. Primary attribution and review provenance

I opened the primary AHR text and checked its majority-model discussion
in Section 3.1, its diffusion convention, and the recursive propagation
context in Section 3.4. AHR attributes the Allen--Cahn majority model
to Etheridge, Freeman, and Penington. Its diffusion normalization differs
from this project, which is why Section 4 above independently derives
the rate and generator. [AHR primary text](https://arxiv.org/html/2209.03435).

I also opened the EFP abstract, which describes the Allen--Cahn and
branching-process setting. No derivative-sampler theorem is attributed
to that abstract. The general recursive-propagation claims in AHR are
not imported to justify integrability here; the bounded leaf-cube
polynomial supplies it directly. [EFP primary abstract](https://arxiv.org/abs/1607.07563).

This was a bounded attribution check, not a search for worldwide novelty
of derivative tuple sampling. The source review, all calculations, and
the rootwise derivative/measure justifications are independent of T65's
earlier proof. The audit is conventional mathematics only.

Research-role metadata: T68 was assigned the skill's `gpt-6-astra`/`max`
research routing. This worker made no model-setting change; the actual
backend and reasoning setting are not independently exposed by its
tools. Performed: full R10, R10b and R08 reading, primary-source inspection,
source-hash and version-diff verification, the derivation above, and this
sole audit-file write. The final file hash is reported in the handoff,
not self-embedded.
