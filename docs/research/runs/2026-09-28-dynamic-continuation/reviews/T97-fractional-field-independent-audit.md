# T97: independent audit of the fractional derivative-field sampler

Date: 2026-09-29. Conventional mathematical audit only.

**Verdict: PASS for frozen T95 in its stated fixed-time scope and
paid exact-real model.** No material repair is required. The complete
773-line source has SHA256

    9bc1d42d582f75b96a4e562dacbc925cbd01151b2a3b4702c5dc2b0a1ab99d74

The unequal-height extraction, conditional Gaussian law, stable-clock
normalization, negative moments, genuine Frechet field construction,
cutoff-independent second moment, hard scalar-query cap, and linear
preparation all pass the independent checks below. The sharper bound
`E[a^(-q)|T]<=n^q M_q` retains its stated restriction `q>=1`.
That restriction is substantive and already sufficient for the proof.

The result is a fixed-time sampling theorem. This audit accepts no
fractional known-profile work solver, complete long-horizon upper or
lower bound, analytic regularization for every beta, finite-bit cost,
implementation, experiment, or novelty conclusion. Root review and
source/model correspondence remain separate from this verdict.

Only this new T97 file is owned by this task. Frozen sources, E4,
accepted ledgers, run state, configuration, Lean, and code are untouched.
The requested inherited research role is `gpt-6-astra/max`; the actual
serving backend and effort are not independently exposed.

## 1. Locked sources, read scope, and exact assertion

All paths in this table are relative to
`docs/research/runs/2026-09-28-dynamic-continuation/`. All seven
dependency locks match the actual files.

| Dependency named by T95 | Verified SHA256 |
| --- | --- |
| `04aa-polynomial-fields-and-linear-gaussian-preparation.md` | `433c699d951c74fa6ba19166e159069130e1340a7a319aa0334b0ba4f8a1b8a1` |
| `reviews/R20-polynomial-reaction-field-sampler-candidate.md` | `b1e42a195c67942066894d04a11c28d7ba2951a6d6730977070e424ac84542b9` |
| `reviews/R20b-continuous-domain-addendum.md` | `6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527` |
| `reviews/R21-linear-tree-common-gaussian-candidate.md` | `99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461` |
| `reviews/T91-polynomial-field-linear-gaussian-independent-audit.md` | `2f06d787fcbb631662b3be4997eb6c610e145120147a0e831d245345abde1af7` |
| `04z-all-positive-diffusivity-sharp-queries.md` | `57ef1d86ddba30ce9d54f316b0eb2dc97f407f7aeb4446a66b3103c28e0aedd4` |
| `reviews/T87-all-diffusion-sharp-query-feasibility.md` | `acd788e6ee5564778cd0663be99aab17fb61f22bdfb4b345ccade008f18feff1` |

I read T95 completely in ranges 1--280, 281--550, and 551--773,
without truncation, and checked targeted numbered passages again.
I read 04aa completely for this task. R20/R20b/R21 and the complete
T91 audit were already read and checked in this worker's preceding
T91 task; 04z and T87 were read completely in preceding T90/T94
work. Relevant R20 construction and T87 interface passages were
reopened here. Matching hashes identify those same proof inputs;
I do not claim a fresh full read of every old file in this turn.

The assertion under review fixes `d>=1`, `0<beta<=1`, `c>0`,
`tau>0`, and a known real polynomial with `f(-1)>=0`, `f(1)<=0`.
The actual equation is

    u_t=-c(-Delta)^beta u+f(u),       X=(R/Z)^d,
    (-Delta)^beta e^(2pi i nu.x)=(4pi^2|nu|^2)^beta e^(2pi i nu.x).

The base `g` and unknown `v` are continuous, `||g||inf<1`, and
`g` has a real evaluator of uniform paid cost `G` making no extra
calls to `v`. Only scalar values of `v` are acquired. The direction
`e=v-g` need not be small. A Taylor statement separately requires
the full segment `g+t e` to lie in the open unit ball.

The mathematical random field lies in `H^(d+1)`, while the actual
finite output is its explicitly indexed real Fourier projection
`P_N W_j`, of size `K=(2N+1)^d`. This distinction does not supply
an infinite-output or heat-density evaluation primitive. These
quantifiers preserve both repairs in R20b and the D43/D44 interface.

## 2. Lemma 1: normalized stable clocks are finite primitive programs

**Source:** T95 lines 85--141, equations (2.1)--(2.5).

I checked the external law rather than treating a skew-stable
parameter name as a normalization. Demni's primary text defines its
positive variable by Laplace transform `exp(-z^beta)` and gives
`S_beta^(beta/(1-beta))=a_beta(Theta)/E` in distribution, with the
explicit sine-ratio expression for `a_beta`. Expanding and taking
the indicated power gives exactly

    S_beta=sin(beta Theta)/(sin Theta)^(1/beta)
                  *[sin((1-beta)Theta)/E]^((1-beta)/beta).

The independent inputs are a uniform angle on `(0,pi)` and a
mean-one exponential. The cited factorization is a classical input;
this audit verifies its use and normalization, not a new proof of
Kanter's original theorem. [Demni, pages 1--2](https://arxiv.org/pdf/1009.4926).

The author-hosted Devroye--James text separately supplies the same
factorization, Laplace convention, and deterministic endpoint
`S_1=1`. Its stated integral distribution formula also verifies that
independent uniform and exponential draws realize the representation.
[Devroye--James, unilateral stable-law section](https://luc.devroye.org/devroye-james-stablesurvey-2013.pdf).

For a positive chronological edge length `ell`, scaling by
`(c ell)^(1/beta)` gives

    E e^(-z L)=exp(-c ell z^beta).

This is T95's exact law; there is no missing cosine scale factor.
Its logarithmic implementation has three sine evaluations, five
logarithms, one exponential, two scalar draws, and a fixed number
of arithmetic operations. The fifth logarithm includes `log(c ell)`;
the other four concern the three sines and `E`.

For `0<beta<1` and `0<Theta<pi`, all three sine arguments lie
strictly between zero and pi. Therefore every logarithm is legal
when `ell>0` and `E>0`. The resulting exact value is positive and
finite. A branch for `ell=0` returns zero, and a separate branch
for `beta=1` returns `c ell`; neither evaluates the singular limiting
formula. Replacing uniform endpoints by `1/2` and exponential zero
by one changes only null events and requires no rejection loop.
Large exact magnitudes do not change the stated operation model.

At `beta=1/2`, the elementary identity
`sin Theta=2sin(Theta/2)cos(Theta/2)` reduces the formula to
`1/[4E cos^2(Theta/2)]`. Its reciprocal mean is two. This agrees
with the independent Gamma-integral computation below. These are
algebraic checks; no random numbers were generated.

**Check: PASS.** Stable, Gamma, quantile, density, and fractional-kernel
oracles are unnecessary.

## 3. Lemma 2: CMS conversion and the shared-coordinate generator

**Source:** T95 lines 143--166 and 592--600.

The Penent--Privault CMS expression uses `alpha=2beta`, an angle
`U0 in (-pi/2,pi/2)`, and clock scale `2t^(1/beta)`. Substituting
`Theta=U0+pi/2` gives `cos U0=sin Theta` and
`cos(U0-beta(U0+pi/2))=sin((1-beta)Theta)`. Their clock is thus
`2t^(1/beta) S_beta`, with Laplace exponent `(2z)^beta`, as their
equations (1.8)--(1.10) specify. The numerical section states an
overlap range `beta>1/2`; Demni supplies the all-`(0,1)` law used
here. [Penent--Privault, CMS formula and normalization](https://arxiv.org/pdf/2106.12127).

T95 instead uses clock `L` with exponent `c z^beta` and a
conditional Gaussian displacement of covariance `2L I_d`.
Consequently, for every `xi in R^d`,

    E exp(i xi.D)=E exp(-L|xi|^2)
                              =exp(-c ell |xi|^(2beta)).

At torus frequency `2pi nu`, this is exactly the required
`exp[-c ell(4pi^2|nu|^2)^beta]`. At `beta=1`, covariance becomes
`2c ell I_d`, so the correspondence with the old Brownian convention
is `kappa=2c`. For a single leaf the returned heat width is `2L`,
and averaging its multiplier makes the same check directly.

One scalar clock must be shared by all physical coordinates of an
edge. With independent coordinate clocks the exponent would contain
`sum_k |xi_k|^(2beta)`, not `(|xi|^2)^beta`. At `xi=(1,1)` the
distinction is `2` versus `2^beta` when `beta<1`. Different edges,
however, require independent clocks and independent conditional
Gaussian arrays; shared ancestry is carried by the common edge
increments. Sampling finite endpoints suffices for this construction.

**Check: PASS.** Both the factor two and the isotropic spatial law
are correct. This is subordinate Brownian motion, not fractional
Brownian motion.

## 4. Lemma 3: the bounded branching functional is the actual flow

**Source:** T95 lines 163--210, equations (3.2)--(3.4); repaired R20.

Stable scaling and independent edge increments give the convolution
semigroup law. Gaussian mixtures are positive probability kernels,
so they preserve constants and contract `C(X)`. On trigonometric
polynomials their multipliers tend to one as time tends to zero.
Density and contraction extend strong continuity to every continuous
profile. No spatial derivative of that profile is needed.

Let `Fmax=max|F_i|` in the degree-`B` Bernstein representation and
`lambda=1+B Fmax/2`. The perturbation `|F_i|/lambda` is less than
`2/B` when nonzero. Interior nodes `2i/B-1` have at least that
distance from the boundary. Endpoint inward signs put `c_0,c_B`
inside the interval as well. Thus all parent corner values lie in
`[-1,1]`, their multi-affine cube interpolation is bounded by one,
and its diagonal is exactly `z+f(z)/lambda`.

At the first split, child subtrees are independent given the common
parental location. Since the parent rule is separately affine, taking
their expectations yields its diagonal evaluated at `F_(t-a)(q)`.
This is precisely T95 (3.4). Killed-semigroup variation of constants
then gives the mild equation for `-c(-Delta)^beta+f`.

Polynomial local Lipschitz continuity gives mild local uniqueness and
existence on `C(X)`. For comparison, add a sufficiently large linear
term to make the reaction nondecreasing on `[-1,1]`, and use the
positive killed semigroup. The constant sub/supersolutions `-1,1`
then give the invariant interval. Bounded continuation is global for
data in this interval. The branching expectation is therefore the
actual solution, not a different nonlinear field.

For the population, direct binomial expansion proves

    lambda n[(n+B-1)^k-n^k]<=lambda(B^k-1)n^k.

Stopped Gronwall bounds its moments. The first moment bounds the
probability of reaching any population threshold before `tau`,
excluding explosion. Limiting gives (3.3) for every positive integer
`k`. The exact segment count is `(Bn-1)/(B-1)<=2n-1`, because
each internal segment has exactly `B>=2` children.

**Check: PASS.** Replacing the spatial semigroup preserves this
branching/PDE argument; it does not require new reaction assumptions.

## 5. Lemma 4: the unequal-height partition inequality

**Source:** T95 lines 212--248, equations (4.1)--(4.3).

Fix any finite tree of nonnegative finite clock lengths, including
zero edges and unequal leaf path totals. Write

    C=sum_e L_e b_e b_e^t,
    H_i=sum_(e on path i)L_e,       m=min_i H_i.

An edge occupies the open height interval beginning at its ancestral
clock sum and of length `L_e`. On each root-to-leaf path these
intervals concatenate from zero to its own `H_i`. Exclude the finite
set of their endpoints. For any remaining `0<h<m`, each leaf path
contains exactly one active edge. Two active edges cannot be ancestor
and descendant. In a rooted tree, overlapping descendant label sets
would force that ancestor relation; thus the active sets are disjoint
and cover all terminal leaves.

There are at most `n` such nonempty blocks. For arbitrary signed
`z in R^n`, their sums satisfy

    sum_active (sum_(i in block)z_i)^2 >=(sum_i z_i)^2/n.

Integrate over `0<h<m`; the contributions at larger heights are
nonnegative. The result is `z^t C z >=(m/n)(sum_i z_i)^2`, including
signed test vectors. When `m=0` it reduces to the ordinary PSD
statement. Zero intervals and coincident heights alter only the
discarded finite endpoint set.

**Check: PASS.** Clock height, rather than chronological time, is
the partition coordinate; equal Gaussian path heights are unnecessary.

## 6. Lemma 5: extraction, degeneracy, maximality, and conditioning

**Source:** T95 lines 250--313, equations (5.1)--(5.5).

Condition on the complete chronological tree and every stable clock.
All clock lengths are now finite deterministic numbers. At an
internal segment, both the positive-child and zero-child branches
of the recursion satisfy

    sum alpha_v=1,       alpha_v>=0,
    alpha_v a_v=h for every child,
    sum alpha_v^2 a_v=h.

In the zero branch, the selected child has `a_v=0`, so these equalities
hold literally; no zero reciprocal is evaluated. A zero-variance
aggregate is itself the zero linear combination of the nonzero edge
Gaussians, by induction through this branch.

Disjoint child subtrees and their incoming parent edge are conditionally
independent. The induction therefore gives

    Var(A_e)=L_e+h=a_e,
    Cov(X_(e,i),A_e)=L_e+alpha_v a_v=a_e.

It also gives a convex combination of descendant leaf path sums:
the child weights sum to one, so the shared incoming edge is counted
once. At the root, `A=w^t X`, `w>=0`, `1^t w=1`, and `Cw=a1`.

For `Z^0=X-A1`, covariance subtraction yields
`Cov(A,Z^0)=0` and `Cov(Z^0)=C-a11^t`. The full joint law is
Gaussian conditional on these clocks. Its characteristic function
has no mixed block and factors, even if the covariance is singular.
Thus `A` is independent of the *whole* residual vector under this
conditional law. Scaling by `sqrt(2)` in each of `d` independent
conditional coordinate arrays gives exactly `G~N(0,2a I_d)` and
the full physical residual covariance.

There is no unconditional independence conclusion: the conditional
variance `a` and residual covariance are functions of the same random
clocks. Their mixture need not be Gaussian, or have finite second
moments. The extraction proof never averages these covariance
matrices as if unconditional covariances existed.

Testing Lemma 4 on `w` gives `a>=m/n`. If every `H_i>0`, this proves
`a>0`; covariance Cauchy--Schwarz with each leaf gives `a^2<=a H_i`,
so `a<=m`. For any proposed `C-b11^t>=0`, testing against `w`
gives `a-b>=0`, proving maximal common variance, even for singular `C`.

Finally, all entries of `C` are nonnegative. Hence

    a=w^t Cw>=sum_i H_i w_i^2
                    >=1/(sum_i H_i^(-1)).

The second inequality is Cauchy--Schwarz applied to
`sum_i(sqrt(H_i)w_i)/sqrt(H_i)=1`. Nonnegative weights justify
discarding the cross terms in the first inequality. This is the
stronger harmonic lower bound. Computing the weights at individual
nodes is enough; expanding `w` at the leaves is not required.

**Check: PASS.** None of this argument used equal path heights.

## 7. Lemma 6: negative moments and the necessary q restriction

**Source:** T95 lines 315--371, especially lines 350--353.

Condition only on the chronological tree. Each path has total
chronological length `tau`. Independence of its edge clocks makes
its conditional Laplace transform the product

    product_(e on path i) exp(-c ell_e z^beta)
                                      =exp(-c tau z^beta).

Thus every `H_i` has the same marginal law `L_tau`; the different
`H_i` are generally dependent. A finite positive-height chronological
path has at least one positive edge, whose guarded stable value is
strictly positive. Consequently all `H_i` and `a` are positive on
every finite execution under the specified guards.

For `q>0`, applying the Gamma integral to `x^(-q)` and Tonelli to
this Laplace transform gives, by the substitution `y=c tau z^beta`,

    M_q=E L_tau^(-q)
       =Gamma(q/beta)/[beta Gamma(q)](c tau)^(-q/beta).

At zero the integrand behaves like `z^(q-1)`; at infinity its
stretched-exponential factor dominates every power. The integral
is therefore finite for every `q>0`. At `beta=1` it becomes
`(c tau)^(-q)`, with no limiting singularity.

The partition bound supplies, for all `q>0`,

    a^(-q)<=n^q max_i H_i^(-q)<=n^q sum_i H_i^(-q),
    E[a^(-q)|T]<=n^(q+1) M_q.

For `q>=1`, the harmonic bound and convexity sharpen this to

    a^(-q)<=(sum_i H_i^(-1))^q
                       <=n^(q-1)sum_i H_i^(-q),
    E[a^(-q)|T]<=n^q M_q.                            (7.1)

Only common marginal laws are used when taking the expectation.
No independent-leaf step is hidden here. Stable clocks' infinite
positive means when `beta<1` play no role in these negative moments.

The qualifier `q>=1` in the source is essential. Fix `0<beta<1` and
`0<q<1`, and take a zero-root two-leaf star of height `tau`, with
independent nondegenerate stable terminal clocks `H_1,H_2`. Then
`a^(-1)=H_1^(-1)+H_2^(-1)`.
Strict concavity of `x^q` gives

    E a^(-q)>2^q M_q.

This is not a defect in T95, which makes no such stronger small-`q`
claim. If a positive chronological root is required, take independent
standard beta-stable variables `S^(0),S^(1),S^(2)` and put

    L0(t)=(ct)^(1/beta) S^(0),
    Yi(t)=[c(tau-t)]^(1/beta) S^(i),       i=1,2,
    a_t=L0(t)+[Y1(t)^(-1)+Y2(t)^(-1)]^(-1).

The path totals `L0(t)+Yi(t)` still each have law `L_tau`.
For `0<t<=tau/2`, `a_t^(-q)` is bounded by an integrable constant
times `(S^(1))^(-q)+(S^(2))^(-q)`. Dominated convergence as `t`
decreases to zero preserves the strict failure for all sufficiently
small positive `t`. A binary chronology with just this split has
positive density on such a time interval. Thus even an almost-everywhere
extension to all `q>0` would be false.

The actual proof uses only the integer `p=2d+1>=1` in (7.1).
For its elementary envelope, `p/beta>=1` and `b=ceil(p/beta)`.
On `(0,1)`, the Gamma integrand is at most one; on `(1,infinity)`
it is at most `x^(b-1)e^(-x)`. Therefore
`Gamma(p/beta)<=1+(b-1)!`, exactly as claimed. This yields `Mbar_p`
using finite factorial loops and permitted `exp/log` operations.

**Check: PASS in the stated q ranges.** No small-edge time integral
or Gamma computational primitive is introduced.

## 8. Lemma 7: all explicit Hilbert constants pass

**Source:** T95 lines 373--413, equations (7.1)--(7.2).

The embedding follows by Fourier Cauchy--Schwarz. To check the
displayed constant, the shell `|nu|inf=k` has at most
`2d(2k+1)^(d-1)<=2d 3^(d-1)k^(d-1)` points. For `r=d+1`,
its weighted reciprocal sum is bounded by the corresponding constant
times `k^(-d-3)`. Since that positive series is at most two,

    sum_nu(1+|nu|^2)^(-r)<=1+4d 3^(d-1)=E_d^2.

For `theta=8pi^2` and `0<a<=1`, the integral comparison for the
one-dimensional Gaussian sum gives

    sum_k e^(-theta a k^2)
       <=1+sqrt(pi/(theta a))<=b0 a^(-1/2).

Splitting its exponential in half, and maximizing
`x^r e^(-theta a x/2)`, proves

    |k|^(2r)e^(-theta a k^2)
       <=(2r/(theta a))^r e^(-theta a k^2/2).

Tensorization and
`(1+sum nu_k^2)^r<=(d+1)^(r-1)(1+sum |nu_k|^(2r))`
give exactly T95's

    H=(d+1)^(r-1)[b0^d+d(2r/theta)^r b1 b0^(d-1)],
    ||h_(2a)||_r^2<=H a^(-r-d/2),       0<a<=1.

For `a>=1`, Fourier monotonicity bounds the norm by its value at one.
Since `p=r+d>=r+d/2`, the valid global envelope is
`H(1+a^(-p))`. The factor `8pi^2 a` is correct: the field uses
variance `2a`, multiplier `exp(-4pi^2 a|nu|^2)`, and the Hilbert
square norm squares that multiplier.

With the chronological tree fixed, multiply by `n^(2j)` and apply
(7.1). Then average over chronology and use its integer moment at
`2j+p` to obtain

    E[n^(2j)||h_(2a)||_r^2]
       <=H(1+Mbar_p)exp[lambda tau(B^(2j+p)-1)]=V_j.

The inequality `n^(2j)<=n^(2j+p)` covers the additional constant
term, including `j=0`. No Fourier cutoff occurs. The constants are
finite functions of fixed parameters in the permitted primitive
model and need not be small or uniform in those parameters.

**Check: PASS.** The saved population power is justified, not guessed.

## 9. Lemma 8: nonlinear translation and the actual C-to-H map

**Source:** T95 lines 415--485, equations (8.1)--(8.4).

First fix the complete clocked tree. Lemma 5 makes `G` independent
of the full residual array under this conditional law. For a fixed
residual array, integrating `G` through the bounded continuous
function of all leaves gives

    E_G F(x+G+Z_1,...,x+G+Z_n)
       =int_X h_(2a)(x-u)F(u+Z_1,...,u+Z_n)du.

This follows by torus periodization and the even Gaussian density.
Every leaf argument is translated by the same `u`. Applying it to
the complete tree polynomial and then mixing clocks yields

    E[h_(2a)(.-U)P_T(q(U+Z_1),...,q(U+Z_n))]=S_tau q.

Both residual law and damping change consistently. Independence of
the eventual scalar coefficient from `U` is neither true nor needed.

For a fixed finite tree, `F_omega(q)` is a finite polynomial map
from `C(X)` to `H^r`. The corner finite-difference formula bounds
each distinct-leaf mixed derivative by one on the cube. Its actual
order-`j` chain rule is the sum over ordered distinct leaf labels,
so its operator norm is at most

    A_j(omega)=n^j||h_(2a)||_r.

The expectation of `A_j^2` is at most `V_j`. When two leaves have
the same spatial location their evaluation functionals coincide,
but their polynomial labels remain distinct. The ordered expansion
still gives the correct multiplicities.

On each finite tree shape, all finite formulas are Borel. The map
`(a,U)->h_(2a)(.-U)` is continuous into `H^r` locally on `a>0`:
a neighborhood of any positive `a` gives a summable dominating
Gaussian Fourier sequence. Countably many tree shapes, separability
of `H^r`, and extension by zero on the null nontermination set
give strong measurability for each fixed input and tuple of directions.
The square-integrable envelopes imply Bochner integrability. They
do not require a deterministic lower bound on `a` for a fixed `n`.

To check actual Frechet differentiation, define the candidate operator
`T_j(q)[e_1,...,e_j]` by the Bochner integral at these fixed directions.
It is bounded multilinear with norm at most `E A_j<=sqrt(V_j)`.
For a small perturbation `eta` staying in the open ball, finite-tree
Taylor expansion gives, in the operator norm on unit directions,

    ||D^jF_omega(q+eta)-D^jF_omega(q)||op
                                     <=A_(j+1)||eta||inf,
    ||D^jF_omega(q+eta)-D^jF_omega(q)
                    -D^(j+1)F_omega(q)[eta,.]||op
                               <=(1/2)A_(j+2)||eta||inf^2.

Integrate these inequalities at fixed directions, then take their
supremum. The resulting deterministic operators have the same
bounds with `E A_(j+1)` and `E A_(j+2)`. Induction proves actual
`C^infinity` Frechet differentiability and continuity in operator
norm. No Bochner integral in a possibly nonseparable operator space
has been presumed. This is stronger than only directional or formal
tree differentiation.

Bounded point evaluations commute with the `H^r` Bochner integral,
identifying its mean with the actual continuous PDE solution. The
integral Taylor remainder on an admissible complete segment gives
the claimed `sqrt(V_J)||e||inf^J/J!`. Arbitrary continuous directions
are legitimate derivatives at `g`; endpoint evaluation `S_tau(v)`
is invoked only under the separate segment condition.

**Check: PASS.** The same proof at each fixed larger Sobolev order
gives spatial smoothness with order-dependent bounds, not analyticity.

## 10. Lemma 9: the tuple oracle and finite real coefficients

**Source:** T95 lines 487--534, equations (9.1)--(9.3).

Condition on the tree, clocks, residuals, and uniform `U`. For
`n>=j`, uniformly choosing an ordered injection from the `(n)_j`
possibilities and multiplying by `(n)_j` reproduces exactly the
ordered sum in Lemma 8. Thus

    z=(n)_j C_I product_b e(U+Z_(I_b)),
    W_j=h_(2a)(.-U)z

has mean `D^jS_tau(g)[e,...,e]`. The factor `j!` is not divided
out in this derivative sample; it belongs only to Taylor coefficients.
For `n<j` every such derivative of the degree-at-most-`n` leaf
polynomial is zero, so returning zero is correct.

The corner formula for `C_I` needs at most `2^j` complete upward
passes after known values have been cached. All selected coordinates
are set to the chosen `+/-1` corner values in those passes. No
unknown direction value enters `C_I`; it is prepared before any
acquisition. At most `j` values of `v` are then obtained. Distinct
leaf labels can coincide spatially; charging those repetitions
separately still respects the cap.

Pathwise, `|z|<=n^j||e||inf^j`. Multiplying by the heat norm before
expectation proves the second-moment bound with `V_j`, including
every coefficient/location dependence.

The constant coefficient is `z`. For each nonzero real frequency
pair, the actual coefficients are

    2z exp(-4pi^2 a|nu|^2)cos(2pi nu.U),
    2z exp(-4pi^2 a|nu|^2)sin(2pi nu.U).

The positive sine sign follows by expanding `cos(2pi nu.(x-U))`.
The factor two agrees with converting the complex coefficient
`z exp(-4pi^2 a|nu|^2)exp(-2pi i nu.U)` to a real cosine/sine
basis. This computes the finite projection exactly with listed
primitives, without evaluating any heat or stable density.

**Check: PASS.** The only unknown-input oracle remains a scalar
initial value; modes share those same values.

## 11. Lemma 10: paid linear preparation, totality, and halting

**Source:** T95 lines 528--590, especially (10.1)--(10.2).

Use a stored segment tree. Its total child-list entries are one
less than its segment count. A depth-first chronological construction
draws one exponential lifetime per processed segment and truncates
at the remaining time; a global heap is unnecessary. Since `B>=2`,
all these counts are `O(n)`.

Each stable edge endpoint costs fixed work by Lemma 1. A postorder
pass computes `a_e` and the guarded child weights, scanning each
child list a bounded number of times. Gaussian generation, a preorder
path-sum pass, a postorder aggregate pass, and final subtraction
cost `O_d(n)` and storage `O_d(n)`. Shared coordinate clocks are
stored once per edge. Complete root paths are not separately
resummed for each leaf, and expanded leaf weights are not stored.

Initialize a leaf-index array once and perform `j` partial Fisher--Yates
swaps using a uniform draw, floor, and endpoint guard each time.
This costs `O(n+j)` and gives the exact ordered-injection law with
no rejection. Modular reductions, `n` known lookups, and `2^j`
parent passes cost `C_(B,j,d)(1+G)n`. The falling factorial and
unknown acquisitions cost `O(j)`, with fixed `j`. Finally the real
array requires `O_d(K)` enumeration, arithmetic and stored entries.

Thus every finite execution obeys the claimed

    Work<=C[(1+G)n+K].

Only the first population moment is needed to average this work:
`E n<=exp[lambda tau(B-1)]`. Very large stable endpoints do not
increase arithmetic word count in this ideal model; their infinite
mean is not infinite simulation time. This is no assertion about
bit complexity or conditioning.

Nonexplosion makes chronology finite almost surely. Every finite
positive-height tree has `a>0`, and the guards make every subsequent
operation legal and finite. This proves almost-sure halting for
every continuous input. On a null seed with infinite chronology,
no unknown value has yet been acquired, so the hard `j` cap holds
on every seed path, not merely almost surely. There is no claim
that the program detects such a null path and returns in finite time.

**Check: PASS.** Linear preparation is a finite program, and no
unpaid transform, covariance, stable-clock, or function oracle remains.

## 12. Lemma 11: Hilbert sampling risk and its precise output target

**Source:** T95 lines 535--546, equation (9.4).

The mean exists in the real Hilbert space by the second-moment
bound. For independent complete copies, Fubini and Cauchy--Schwarz
justify the mixed inner products, which have expectation zero after
centering. Expansion therefore gives exactly

    E||M^(-1)sum_b W_(j,b)-mu_j||_r^2
       =[E||W_j||_r^2-||mu_j||_r^2]/M
       <=V_j||e||inf^(2j)/M.

No independence of Fourier modes within a sample occurs in this
proof. Orthogonal projection contracts this norm, and its finite
output version is centered at `P_N mu_j`. The fixed embedding gives
a spatial supremum inside expectation for that projected error.
If one instead compares the finite array to the entire `mu_j`,
the omitted-mode bias remains to be counted. T95 does not claim
that this bias vanishes, or that it has a uniform analytic tail.
The infinite-field identity is a mathematical statement about the
specified random field, not an infinite output operation.

**Check: PASS.** The risk envelope remains an inequality, preserving
the second mandatory repair in R20b.

## 13. Lemma 12: nonanalytic regularization and long-time boundaries

**Source:** T95 lines 630--683, equations (12.1)--(12.2).

For `0<beta<1/2`, choose `2beta<eta<1`. The periodic cosine series
with coefficients `delta exp(-k^eta)` has every derivative series
absolutely convergent, because each factor `k^l` is dominated by
this stretched exponential. Choosing positive `delta` sufficiently
small imposes the stated sup and finite-order derivative bounds.
Its zero mean and nonzero first Fourier coefficient force a sign
change: a continuous nonzero function of only one sign could not
have integral zero. Dependence on one coordinate extends the example
to every dimension without introducing other derivatives.

For the zero reaction, the time-`tau` positive-frequency coefficient
is exactly

    (delta/2)exp[-k^eta-c tau(2pi k)^(2beta)].

For every `b>0`, adding `bk` in the exponent makes it tend to
positive infinity. There is therefore no exponential coefficient
bound with any positive rate. A real-analytic periodic function
has a common positive complex strip by compactness, and its Fourier
coefficients have such a bound. Hence this smooth solution is not
analytic. Also an omitted Fourier coefficient is bounded by the
sup norm of the projection tail; an `exp(-bN)` tail estimate would
contradict the coefficient at `k=N+1`.

This is an exact counterexample to copying the analytic-tail premise
for all beta. It is not a lower bound excluding polynomial-size
cutoffs: linear fractional multipliers still give a tail bounded by
a stretched exponential with polynomial shell factors, permitting
cutoffs polynomial in a logarithmic accuracy parameter for fixed
positive time. T95 properly leaves the nonlinear paid solver and
its scale/time/accuracy cost unproved.

Likewise, a positive first spectral gap by itself proves no signed-prior
separation or full long-horizon lower. The mean reaction is generally
not the reaction at the mean, and a general inward polynomial can
have different instability properties or none. The example `f=-u`
already excludes a universal positive long-time exponent for this
entire reaction class. Zero diffusivity or zero burn-in cannot even
smooth every continuous zero-reaction input into `H^r`; beta zero
and beta greater than one are outside the theorem.

**Check: PASS.** No full fractional complexity theorem is silently
accepted from this fixed-time gate.

## 14. Primary attribution and exact audit activity

The stable factorization, subordination, negative moments, and
branching ideas are classical ingredients. The independent reasoning
above checks their specific normalization and the complete field law.
No priority or award inference follows from PASS.

I inspected the primary Penent--Privault generator convention,
negative moments (1.8),(1.10), Remark 4.2, higher-spatial-derivative
discussion, and CMS formula. Remark 4.2 removes the clock-moment
integrability restriction for reactions without spatial derivatives.
Its higher-derivative obstruction concerns spatial integration by
parts and an integral near zero edge duration. T95 differentiates
the initial function and uses full path duration `tau>0`; it does
not resolve that gradient-reaction obstruction. An all-beta
non-gradient branching representation is already prior work.
[Primary fractional branching paper](https://arxiv.org/pdf/2106.12127).

The R20 polynomial voting rule and R21 inverse-variance Gaussian-tree
recursion retain their existing classical attributions, checked in
the preceding T91 audit. T95 extends their inspected mathematical
use; an internal proof does not establish external originality.

For this audit, external access was limited to direct openings of
the following three URLs and targeted text inspection:

- `https://arxiv.org/pdf/1009.4926`: Laplace definition and factorization
  on PDF pages 1--2.
- `https://arxiv.org/pdf/2106.12127`: generator and negative-moment
  passages on PDF pages 4--7; Remark 4.2 on page 20; higher derivative
  and CMS passages on pages 23--24.
- `https://luc.devroye.org/devroye-james-stablesurvey-2013.pdf`:
  title/introduction and the unilateral stable-law section on PDF page 10.

The exact PDF text-find strings were `(1.8)`, `Remark 4.2`, and
`Chambers` in Penent--Privault; `positive stable` and `Kanter` in
Devroye--James. The first Devroye--James string had no match, and the
second located the relevant text. No search-engine query was issued.
The relevant equations were read in extracted PDF text; this audit
performed no screenshot or visual-PDF claim. I did not open Kanter's
original paper or repeat T95's unsuccessful original-paper access
attempts; the accessible primary texts above are the actual inputs.

Local activity was the complete source read, targeted `rg`/`sed`
and numbered reads, all seven SHA256 checks, inspection of the
accepted 04aa interface, the displayed mathematical derivations,
and writing/rereading this one audit. The mathematical countercheck
for `q<1` is an analytic argument, not an executed experiment.

The math-auto-research skill, its defaults/general profile and
model-routing/execution instructions, and project instructions were
read in this worker's preceding tasks and remain applicable. The
one-owner-file audit does not authorize changing accepted ledgers
or implementation state. Reading a model configuration is not
evidence of a backend change or independently exposed identity.

No numerical or symbolic-algebra execution, random experiment,
unknown-input acquisition, solver run, implementation test, or Lean
invocation was performed. E4 and all frozen sources were preserved.
The source and dependency hashes are rechecked at final handoff;
the audit's own final SHA is reported separately after self-review.

The final conclusion is PASS for T95's actual fixed-time
`C(X)`-to-`H^(d+1)` derivative field, explicit finite coefficient
sampler, stated moment ranges, hard query cap and linear paid
preparation. Its long-time and prior-art limitations remain intact.
