# T37 — bounded primary-literature audit of two moving barriers

Status: complete, 2026-09-28. Exactly 20 purposeful search queries were
used, followed by primary-source opens. No theorem, sampler, protocol,
experiment, data, or predecessor review was changed. This is an
application-priority audit, not a mathematical re-audit of T30 and not a
claim of exhaustive literature coverage.

Reviewed local inputs:

| Input | SHA-256 at review |
|---|---|
| `04l-two-barrier-voting.md` | `87bc9b8424fc1ea04397adeeb38aa99843d9ade97b81e13c8857b31919706d42` |
| `reviews/T30-two-barrier-voting-audit.md` | `a82b3c07afbaaaaa0fe5f94b6296fd2bda187ae0d7cf9e8c6812afa8a5111ce4` |
| `reviews/T27-positive-phase-voting-audit.md` | `b4e61c70fbebb6b1917654e11eae901073fa81f20522dacedd11595d6e663066` |

T19's heat-transform literature review was also read to avoid repeating
its rejected general novelty claim. The research skill and routing
instructions read for the predecessor audits continue to apply; this
bounded role performs primary-literature assessment only.

## 1. Verdict and closest prior result

The bounded search did **not locate a primary result containing the exact
D19 combination**: two scalar solutions approaching the same one-sided
attracting equilibrium, their integrable separation even at a degenerate
root, and a bounded voting representation whose expected *total tree
size* is uniformly bounded in the requested time horizon. **Publication
novelty is not established.**

The closest direct representation theorem is An–Henderson–Ryzhik (AHR),
Section 3.2, Theorem 3.2. The closest inspected normalization mechanism is
Engländer–Winter's space-time H-transform, Appendix B, Lemma 3, used in
Section 2 to make branching decay exponentially. Ossiander supplies an
earlier all-time bounded-cascade precedent with strict subcritical
domination. These sources prevent a general claim of a new voting,
normalization, all-horizon, or finite-mean-work methodology; their exact
locations and limits are recorded below.

AHR already covers a degenerate attracting root: see its example
`f(u)=u(1−u)^2`, Section 2.3, equation (2.22), and its polynomial voting
theorem. The possible delta concerns work, not representation alone.

## 2. The exact feature being compared

This section restates the audited D19 construction, without adding a
theorem. For a polynomial `f` with `f(b)=0` and `f>0` on `[m,b)`, where
`m<M<b`, let `l=ell_m`, `a=ell_M`, and `h=a−l`. The scalar flow gives

\[
 a(t)=l(t+\Delta),\qquad
 \Delta=\int_m^M\frac{dy}{f(y)},\qquad
 \int_0^\infty h(t)\,dt
 =\int_0^\Delta(b-l(t))\,dt
 =\int_m^M\frac{b-y}{f(y)}\,dy<\infty.
\]

Both integrals on the right concern compact intervals away from the
root. This statement does not require integrability of `b−l` over the
whole half-line or a strictly negative derivative at `b`.

For `w=(u−l)/h`, the transformed polynomial is

\[
 F_t(w)=\frac{f(l+hw)-(1-w)f(l)-wf(a)}{h}.
\]

Endpoint interpolation cancels the constant and linear contributions;
the remaining Bernstein coefficients are bounded by a constant times
`h(t)`, with the endpoint factors checked in T30. Consequently a voting
rate `lambda(t)=C h(t)` is admissible. The standard pure `n`-ary tree
formula then gives

\[
 \sup_{T\ge0}\mathbb E N(T)
 \le \frac{n\exp((n-1)C\int_0^\infty h)-1}{n-1}<\infty.
\]

The comparison target is this whole chain, including the choice of
normalization that makes the hazard integrable. Merely allowing a
time-dependent rate, assuming its integral is finite, proving a.s.
extinction, or controlling an estimator's variance is not the same
statement. The monotone-shift integral identity is elementary analytic
material; this audit offers no claim that the identity itself is new.

## 3. Primary-paper evidence and exact overlap

### 3.1 AHR: the closest polynomial voting theorem

[An, Henderson and Ryzhik, *Voting models and semilinear parabolic
equations*](https://arxiv.org/html/2209.03435), Section 3.2, Theorem 3.2,
represents polynomials vanishing at 0 and 1 by pure `N`-ary voting, for
continuous data in `[0,1]`. Equations (3.22), (3.25), and
(3.28)–(3.31) give `alpha_k=k/N+b_k[f]/beta`, with constant rate `beta`.
The paper acknowledges O'Dowd's earlier construction after Theorem 3.2.

**Overlap:** bounded polynomial voting and coefficient-based rate
selection. **Unlocated feature:** the moving barriers and uniform total
tree size. Applying this machinery to `F_t` requires the time-dependent
renewal argument and width estimate; Theorem 3.2 does not literally
state D19.

### 3.2 Engländer–Winter: normalization that makes branching integrable

[Engländer and Winter, *Law of Large Numbers for a Class of
Superdiffusions*](https://arxiv.org/pdf/math/0504377), Appendix B,
**Lemma 3(a)**, transforms coefficients to
`(L+a grad(H)/H · grad, beta+(LH+partial_t H)/H, alpha H)`.
**Lemma 3(b)** and Section 2, equation **(9)**, use
`H(x,t)=exp(−lambda_c t) phi_c(x)`, giving zero linear growth and
branching coefficient `alpha phi_c exp(−lambda_c t)`.
Section **2.3**, first proof paragraph, identifies exponentially decaying
branching. **Lemma 1** gives bounded variance; Assumption 1 requires
`lambda_c>0` and bounded `alpha phi_c`.

**Overlap:** normalization producing decaying branching and uniform
moment control. **Limit:** this superdiffusion result uses spectral
exponential decay; the inspected statements give neither moving scalar
pairs nor finite full voting-tree work at a degenerate root.

### 3.3 Ossiander: all-time bounded cascades and uniform expected work

[Ossiander, *A probabilistic representation of solutions of the
incompressible Navier–Stokes equations in R3*](https://arxiv.org/pdf/math/0412034),
Section 4, **Theorem 4.2**, gives the all-time small-data representation
`u=h E Upsilon`. **Proposition 4.2** bounds the return. Its proof,
printed pages 21–22, uses a binary Galton–Watson tree with branching
probability `p≤1/2`. For the allowed strict choice `p<1/2`, summing
generation means gives `E N_dom=1/(1−2p)`. This is the audit's inference,
not a quoted complexity theorem. The endpoint `p=1/2` gives a.s.
finiteness without finite expected total size.

**Overlap:** bounded all-time cascades with finite-mean domination.
**Limit:** this majorizing-kernel and Navier–Stokes construction does
not supply the paired-ODE width criterion.

### 3.4 Henry-Labordère and coauthors: expected tree-size analysis

[Henry-Labordère, Oudjane, Tan, Touzi and Warin, *Branching diffusion
representation of semilinear PDEs and Monte Carlo
approximation*](https://arxiv.org/html/1603.01727), **Proposition 5.1**
in Section 5.1 gives a renewal series for the expected total particle
count, `m(t)=sum_k n0^k F^{*,k}(t)`. The preceding complexity paragraph
explicitly uses all particles in the tree as computational work.
**Assumption 3.10** and **Theorem 3.12** give sufficient moment and
representation conditions, described in the paper as small maturity or
small nonlinearity restrictions.

**Overlap:** non-exponential lifetimes, polynomial branching Monte
Carlo, and full-tree work analysis are already available. **Limit:** the
inspected conditions do not construct the D19 moving interval or prove
that its scalar width makes total hazard finite uniformly in `T`.
Uniform integrability over a fixed `[0,T]` must not be relabelled as a
bound uniform over all horizons.

### 3.5 Backbone decompositions: shifts and nonlinear transforms

[Kyprianou, Pérez and Ren, *The backbone decomposition for spatially
dependent supercritical superprocesses*](https://arxiv.org/pdf/1304.2019),
Section **3.2, Lemma 3.2**, gives the extinction-conditioned shift
`u_f^*=u_{f+w}−w` and mechanism
`psi^*(x,z)=psi(x,z+w(x))−psi(x,w(x))`. Section **3.4**, equations
**(22)–(25)**, gives transformed motion and skeleton rate
`q=partial_z psi(x,w)−psi(x,w)/w`. **Theorem 4.2** identifies the
dressed backbone law with the original localized superprocess.

**Overlap:** shifting nonlinear semigroups about a solution and
constructing a transformed branching law. **Limit:** `w` here is a
stationary extinction function; the backbone describes prolific
lineages. The inspected construction does not assert a finite
horizon-independent total genealogy, much less the moving-pair width
criterion.

[Fekete, Fontbona and Kyprianou, *Skeletal stochastic differential
equations for superprocesses*](https://people.bath.ac.uk/ak257/ssdes.pdf),
**Theorem 1**, printed page 1122, constructs the coupled skeleton and
mass process. Section **5, Theorem 2**, equation **(5.7)**, contains a
time-dependent nonlinear difference involving `f^T` and `w exp(−h^T)`.
This is a closer algebraic resemblance than a purely spatial
H-transform. However, the construction retains a fixed martingale
function `w`; Section 5 uses the time-dependent functions for its
Laplace-functional proof. No paired scalar-flow integrability or
uniform Monte Carlo tree-work theorem was located in those statements.

### 3.6 A screened finite-horizon extension

[Belak, Hoffmann and Seifried, *Branching Diffusions with Jumps and
Valuation with Systemic
Counterparties*](https://www.uni-trier.de/fileadmin/fb4/prof/BWL/FIN/QFRA_Working_Papers/QFRA_20_04.pdf),
**Theorems 3.2–3.3**, extends branching Monte Carlo to mixed local and
nonlocal nonlinearities. Section 3.2, equations **(3.4)–(3.5)**, uses
a scalar majorant ODE for moment control. Theorem 3.3(ii) explicitly
imposes a sufficiently small terminal time. This search lead supplies
additional ODE-comparison precedent, but no closer result on two moving
barriers or degenerate-root uniform work.

## 4. Defensible delta and prohibited overstatement

A source-supported comparison can say:

> We apply established polynomial voting representations to an affine
> normalization by two scalar solution barriers. Their separation has
> finite total integral because the barriers are time translates of one
> monotone bounded orbit. This gives an explicit horizon-uniform
> expected-node bound for the stated scalar polynomial basin, including
> one-sided attracting equilibria with zero linearization. A bounded
> literature search did not locate this exact application; priority
> remains unresolved.

This describes the local result relative to the inspected literature.
It does not establish a new general branching framework. In particular:

| Proposed claim | Assessment |
|---|---|
| First polynomial voting representation | Contradicted by primary prior |
| First branching representation at a degenerate attracting root | Contradicted by the AHR polynomial scope and explicit example |
| First normalization producing decreasing or integrable branching | Contradicted at mechanism level by space-time H-transform work |
| First all-time bounded branching estimator with finite mean tree work | Contradicted at method level by strict subcritical cascade domination |
| Exact D19 paired-barrier width-to-work certificate appears in an inspected source | Not located |
| D19 is publication-new, optimal, or practically superior | Not established |

The node-count conclusion must retain D19's ideal initial-data,
scalar-clock and transition-oracle contract. It is not a bound on exact
bit complexity or floating-point runtime. The harmonic-center baseline
from T30 also remains material: in the nonhyperbolic case its certified
relative defect error tends to zero. The literature search does not
turn horizon-independent unbiased tree work into a demonstrated
advantage over that deterministic approximation.

## 5. Search record and coverage boundary

Exactly the following 20 queries were issued in this audit. Primary
paper opens and in-document searches were then used to test the useful
leads. Search-result snippets, aggregators and generated topic pages
were not used as theorem evidence.

1. `"branching" "PDE" "two solutions" normalization`
2. `"branching" "moving interval" semilinear`
3. `"branching" "nonhyperbolic" Monte Carlo`
4. `"branching" "integrable" "hazard" semilinear PDE`
5. `"branching diffusion" "uniform in time" dissipative`
6. `"branching" "lower and upper solutions" stochastic`
7. `superprocess "time-inhomogeneous backbone"`
8. `"branching" "normalization" "semilinear" Monte Carlo`
9. `superprocess backbone decomposition finite time time dependent branching mechanism`
10. `semilinear PDE Monte Carlo branching long time rescaling dissipative`
11. `branching voting reaction diffusion time inhomogeneous rate normalization`
12. `branching processes nonlinear PDE two solutions h transform`
13. `superprocess "two solutions" transform`
14. `"branching" "time-dependent" "voting"`
15. `"branching" "finite total" "PDE"`
16. `"dissipative" "branching" "Monte Carlo"`
17. `"semilinear" "branching" "rescaling"`
18. `"voting models" "time-dependent"`
19. `"branching" "two solutions" "superprocesses"`
20. `"branching" "uniform" "time horizon" "PDE"`

The first narrow terminology queries mostly returned unrelated
bifurcation, population, and network material. The backbone queries
yielded the two primary papers in Section 3.5; the last query yielded
the finite-horizon extension in Section 3.6. Known predecessor leads
were reopened directly to verify the precise theorem locations.

This bounded search did not exhaust older non-English branching
literature, all variants of nonlinear H-transforms, theses, unindexed
papers, or citation descendants. It did not establish priority of the
elementary shift-width identity. Nor does failure to locate the exact
combination distinguish a publishable contribution from a short
consequence of known representation machinery. The defensible present
status is a validated local application with an explicit work
certificate and unresolved priority; no located exact prior result
collapses that narrow application.
