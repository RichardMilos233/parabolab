# T40 — exact point-query lower bound near the unstable Allen–Cahn phase

Status: bounded theory/feasibility task complete, 2026-09-28. The
conventional proof below closes a representation-independent lower bound
in the stated exact-value oracle model. It awaits the separately assigned
independent mathematical audit before acceptance or a Lean gate. No
implementation, Lean, experiment, data, or other research file was changed.
The primary search used 16 purposeful queries, within the limit of 20.
No publication-priority or optimal-exponent claim is made.

Read inputs: D10 in `04c-general-obstruction.md`, SHA-256
`5417a77bf2e64e4de9b14a4be14cded9f46671c0ee5b393c1713eddca285e381`,
and D19 in `04l-two-barrier-voting.md`, SHA-256
`87bc9b8424fc1ea04397adeeb38aa99843d9ade97b81e13c8857b31919706d42`.
The root's concurrently derived `04o-unstable-phase-query-lower-bound.md`
was subsequently read without editing. Its constants differ, but its
argument agrees with the independent construction below. T41 owns its
independent mathematical audit.

## 1. Decision

**Go for independent review of the exact point-query theorem.** A
single unknown localized bump already suffices; a random mean-field
microcell approximation is unnecessary. Positive heat spreading followed
by exact scalar comparison controls the nonlinear evolution. A common
small sine background makes the baseline and every hard input genuinely
sign-changing.

For every fixed spatial dimension `d≥1` and finite integer smoothness
order `s≥1`, there are constants `C>0` and `T0` such that uniform absolute
RMS error at most `1/4` on one fixed class of smooth sign-changing data
requires

\[
 \sup_v\mathbb E Q_T(v)\ \ge\ C\exp\!\left(\frac{d}{s+d}T\right),
 \qquad T\ge T_0.
\]

Here `Q` counts **exact deterministic initial-data evaluations**. The
bound allows adaptive randomized algorithms, input-dependent stopping,
arbitrary postprocessing, and biased estimates. It is not confined to a
branching representation and uses no Bernoulli input oracle.

This is a worst-case-in-input statement at each horizon. The sign-changing
baseline on which large expected cost is proved depends on `T`. It does
not assert increasing difficulty of one fixed known profile. Classical
fooling functions already supply the information argument; the bounded
literature search did not locate the exact Allen–Cahn horizon-transfer
statement proved here, and does not establish novelty.

## 2. Fixed class, PDE, information, and error criterion

Work on the unit flat torus `T^d=R^d/Z^d`, with normalized Lebesgue volume
one, and fix a query point `x*`. Let `S_t v` solve

\[
 \partial_tu=\tfrac12\Delta u+u-u^3,\qquad u(0,\cdot)=v.
\]

Define

\[
 \|v\|_{C^s,\max}
 :=\max_{|\alpha|\le s}\|\partial^\alpha v\|_\infty,
 \qquad
 \mathcal F_{d,s}
 :=\{v\in C^\infty(\mathbb T^d):
       \|v\|_{C^s,\max}\le\tfrac14,
       \min v<0<\max v\}.
\]

The class does not depend on `T`. In particular its range is contained in
`[−1/4,1/4]`. Only derivatives through the fixed finite order `s` have a
uniform bound; this is not an analytic class or a class with uniform
bounds on every derivative. Smooth global solutions exist by the usual
local semilinear theory and the invariant interval `[−1,1]`.

An algorithm knows the PDE, `d,s,T,x*` and this class. Its only access to
the unknown input is to choose a point `x` and receive the exact real
number `v(x)`. Query locations, stopping, and returned real value may be
measurable functions of the preceding transcript and private randomness.
The algorithm may depend on `T`. All arithmetic and random-number
generation can be free: the lower bound charges only data queries.

The oracle does not reveal the input's formula, source, bump location,
integral, Fourier coefficients, derivative values, or evolved solution.
There is no preprocessing that has already read the unknown function.
The same proof applies to unit-periodic inputs on `R^d`: arbitrary
queries there reduce modulo the period.

Write the output and query count as `H_T(v)` and `Q_T(v)`. Assume a.s.
termination on the class and require

\[
 \sup_{v\in\mathcal F_{d,s}}
 \mathbb E\left|H_T(v)-S_Tv(x_*)\right|^2\le\varepsilon^2.
 \tag{E}
\]

Infinite expected query count already satisfies a lower bound. The
nontrivial proof therefore assumes finite expected count on its baseline.
All inputs are coupled with a common random tape; this is the standard
realization of private-randomness adaptive algorithms. Measurability of
queries, stopping events, and output is part of the algorithm contract.

## 3. Explicit hard family in that fixed class

These are T40's constants, chosen independently of the root's 04o
constants. Fix a nonzero function

\[
 \phi\in C_c^\infty((1/4,3/4)^d),\qquad 0\le\phi\le1,
 \qquad I:=\int\phi>0.
\]

Put

\[
 D:=\max_{|\alpha|\le s}\|\partial^\alpha\phi\|_\infty,
 \quad D_{\sin}:=(2\pi)^s,
 \quad \eta:=\frac1{4(D+I D_{\sin}+1)},
 \quad q:=\eta I,
 \quad r:=s+d.
\]

For the generator `Delta/2`, the time-one periodized Gaussian kernel
obeys

\[
 p_1(x,y)\ge\kappa_d:=(2\pi)^{-d/2}e^{-d/8}>0.
 \tag{K}
\]

Indeed, choose an integer translate of `x−y` with every coordinate in
`[−1/2,1/2]`. Its single Gaussian term supplies this lower bound; the
remaining terms are nonnegative. Set

\[
 B:=e/\kappa_d,
 \qquad \delta:=\frac1{8\,2^rB},
 \qquad T_0:=\max\{1,\log(B4^r/q)\}.
\]

For `T≥T0`, define

\[
 R_T=(q e^T/B)^{1/r},\qquad
 k=\lfloor R_T\rfloor\ge4,\qquad K=k^d,\qquad
 \mu=qk^{-r}.
\]

Partition the torus into `K` half-open cubes `C_j` of side `1/k`. In
cube `j∈{0,…,k−1}^d`, let

\[
 b_j(x)=\eta k^{-s}\phi(kx-j),\qquad
 g_T(x)=\delta\mu\sin(2\pi x_1),\qquad
 v_{j,+}=g_T+b_j,\quad v_{j,-}=g_T-b_j.
 \tag{F}
\]

Each bump is extended by zero outside its cube; compact support in the
cube's interior makes the extension smooth and periodic. Its integral
is exactly `mu`. The floor bounds `R_T/2≤k≤R_T` imply

\[
 B\le\mu e^T\le2^rB,
 \qquad
 K\ge2^{-d}(q/B)^{d/r}e^{dT/r}.
 \tag{M}
\]

Every derivative of `b_j` through order `s` is bounded by `eta D`, since
its scaling factor is `k^{|alpha|−s}≤1`. Also

\[
 \|g_T\|_{C^s,\max}
 \le\delta\mu D_{\sin}
 \le\eta I D_{\sin},
 \qquad
 \|v_{j,\pm}\|_{C^s,\max}
 \le\eta(D+I D_{\sin})<1/4.
\]

Because `k≥4`, the complement of each entire cube contains points where
`sin(2 pi x_1)` is strictly positive and strictly negative. On that
complement, both inputs equal `g_T`. Thus `g_T` and every `v_{j,±}`
belong to the genuinely sign-changing class `F_{d,s}`. Their sup norms
tend to zero as `T→∞`, since `s≥1` and `k→∞`. The relevant smoothness
budget remains fixed throughout.

## 4. Exact nonlinear separation at time T

For a nonnegative bump, comparison gives `0≤S_t b_j≤1`. Its reaction
`u−u^3` is nonnegative on this interval, so the mild equation and (K)
give the pointwise estimate

\[
 S_1 b_j(x)\ge P_1b_j(x)\ge\kappa_d\mu.
 \tag{P}
\]

Let `c=kappa_d mu`. It lies in `(0,1)`. Comparing after time one with
the spatially constant Allen–Cahn solution gives

\[
 S_Tb_j(x)\ge\ell_c(T-1),\qquad
 \ell_c(t)=\frac{c e^t}{\sqrt{1+c^2(e^{2t}-1)}}.
\]

By (M), `z=c exp(T−1)≥1`. Hence

\[
 \ell_c(T-1)
 =\frac{z}{\sqrt{1+z^2-c^2}}
 \ge\frac{z}{\sqrt{1+z^2}}
 \ge\frac1{\sqrt2}.
 \tag{A}
\]

This uses the full cubic flow. It does not propagate a linear
approximation until the output becomes order one, and it does not
assume that the spatial mean satisfies a closed scalar equation.

For any two solutions `u,w` in the invariant interval, their difference
solves

\[
 \partial_t(u-w)
 =\tfrac12\Delta(u-w)
   +[1-(u^2+uw+w^2)](u-w).
\]

The bracket is at most one because
`u^2+uw+w^2=(u+w/2)^2+3w^2/4≥0`. The maximum principle, applied to
`exp(−t)(u−w)` and its negative, yields

\[
 \|S_t v-S_t\widetilde v\|_\infty
 \le e^t\|v-\widetilde v\|_\infty.
 \tag{L}
\]

This is an upper-potential estimate, not the false assertion
`|f'|≤1` on `[−1,1]`. Oddness gives `S_t(−b_j)=−S_t b_j`. Finally,
the common background satisfies

\[
 e^T\|g_T\|_\infty\le\delta 2^rB=1/8.
\]

Combining (A) and (L), at every query point and for every `j`,

\[
 a_j:=S_Tv_{j,+}(x_*)\ge1/\sqrt2-1/8>1/2,
 \qquad
 c_j:=S_Tv_{j,-}(x_*)\le-1/\sqrt2+1/8<-1/2.
 \tag{G}
\]

The targets are therefore separated by more than one even though all
initial profiles approach zero uniformly.

## 5. Adaptive query proof, including random stopping

Fix the random tape and run the algorithm on the baseline `g_T`. Let
`J` be the set of distinct cubes visited before this run stops. Since
the half-open cubes partition the torus,

\[
 |J|\le\min\{K,Q_T(g_T)\}.
\]

For `j∉J`, every baseline query receives the same response under
`g_T`, `v_{j,+}`, and `v_{j,-}`. Induction over the finite baseline
query sequence shows that the adaptive locations, stopping decision,
and final returned value coincide on those three inputs. Querying on a
cube boundary causes no difficulty: the cubes have unique membership
and the bumps vanish near boundaries. Visiting a cube where the bump
vanishes can only overcount the possible information gained.

For arbitrary real `y,a,c`,

\[
 \frac{(y-a)^2+(y-c)^2}{2}
 =\left(y-\frac{a+c}{2}\right)^2+\frac{(a-c)^2}{4}.
\]

Consequently, on the no-visit event `j∉J`, (G) gives an average paired
squared loss at least `1/4`, regardless of bias or the size of the
returned value. Discarding the nonnegative losses on visit events and
then averaging over `j` and the random tape gives

\[
 \begin{aligned}
 &\frac1{2K}\sum_{j=1}^K
   \mathbb E\bigl[
    |H_T(v_{j,+})-a_j|^2+|H_T(v_{j,-})-c_j|^2
   \bigr]\\
 &\hspace{1cm}\ge\frac1{4K}\sum_{j=1}^K\mathbb P(j\notin J)
 =\frac14\left(1-\frac{\mathbb E|J|}{K}\right)
 \ge\frac14\left(1-\frac{\mathbb E Q_T(g_T)}K\right).
 \end{aligned}
 \tag{I}
\]

Only a finite sum and nonnegative integration are used. There is no
independence assumption between output, stopping, and discovered data,
and no likelihood differentiation or optional-stopping identity.
If the baseline's expected count is infinite, the lower bound is
already true; otherwise a.s. finite halting justifies the transcript
induction outside a null set.

Condition (E), applied to the `2K` hard inputs, bounds the left side
by `epsilon^2`. Therefore, for every `0<epsilon<1/2`,

\[
 \boxed{\quad
 \mathbb E Q_T(g_T)\ge(1-4\varepsilon^2)K
 \ge(1-4\varepsilon^2)2^{-d}(q/B)^{d/(s+d)}
          e^{dT/(s+d)}.
 \quad}
\]

In particular, for absolute RMS at most `1/4`, the coefficient is at
least `(3/4) 2^{−d}(q/B)^{d/(s+d)}`. This proves the stated
representation-independent lower bound. It is a lower bound on initial
data queries, not an identification of the optimal rate or constants.

## 6. Falsification checks and limits

| Potential failure | Resolution or actual limit |
|---|---|
| Exact values reveal a real parameter in one query | The unknown cell and sign are absent from every response outside that cell; exact precision cannot reveal them there. |
| T-dependent smoothness budget | `F_{d,s}` is fixed; only the chosen members and derivatives above order `s` vary. |
| Hard inputs are merely one-signed | The common sine has both signs outside every cell, including on the baseline. |
| Nonlinear mean correction invalidates linear growth | No mean closure or linearized approximation is used; (P), exact scalar comparison, and (L) prove the gap. |
| Adaptive points or stopping evade a fixed-grid argument | The grid is a family of disjoint hiding regions, not a restriction on the algorithm's points. The proof follows its full baseline transcript. |
| Rare expensive branches or unbounded returns evade expected cost | Inequality (I) uses expected baseline query count directly and holds for every real output. |
| Unlimited symbolic information about v | Excluded by the stated oracle contract; this proof makes no such lower bound. |
| Every fixed datum becomes harder as T grows | Not proved; the sign-changing baseline here depends on T. |
| Uniformity in spatial dimension or infinitely many derivative bounds | Not claimed; `d,s` are fixed and constants depend on them. |
| Relative defect error | Not the criterion; the result concerns absolute error for the signed solution value. |

The one-query constant-profile counterexample remains decisive against
silently importing a coin-oracle Fisher-information bound: a deterministic
value query to a constant function returns its unknown parameter exactly.
No statement such as `Var(H) E N≥exp(2T)` is asserted for this oracle.
The present spatial information bound remains valid precisely because
unqueried regions agree identically with a common baseline.

D10 concerns likelihood estimators on one specified derivative-code tree
measure; the theorem above has no such restriction. D19 concerns a fixed
strict phase interval, and the burn-in extension uses fixed positive mass
certificates. This hard family instead has vanishing mass and both signs.
There is no contradiction with their uniform-in-time work bounds, nor any
claim about the cost of the fixed known cosine profile in the completed
experiment.

## 7. Primary-literature overlap

[Kunsch and Rudolf, *Optimal confidence for Monte Carlo integration of
smooth functions*](https://arxiv.org/pdf/1809.09890), Section **2.1**, uses
function-value information, permits adaptive locations in its lower
bounds, and discusses random input-dependent cardinality. **Lemmas
2.1–2.2** use disjoint supports and unknown signs. Section **2.2**, proof
of **Theorem 2.3**, scales bumps to preserve smoothness norms; **Theorem
3.6** identifies optimal integration rates. This is direct prior for the
information argument and bump construction, not an Allen–Cahn horizon
theorem. The single-bump construction here does not claim the stronger
minimax exponent suggested by many-bump integration results; transferring
those cancellations through nonlinear evolution would need further proof.

[Kwas, *Complexity of multivariate Feynman–Kac path integration in
randomized and quantum settings*](https://arxiv.org/pdf/quant-ph/0410134),
Section **3.2**, equation **(4)**, uses exact function values, random
query cardinality measured in expectation, and worst-case RMS error.
Section **8.1** reduces PDE evaluation to Gaussian weighted integration
by setting the potential to zero. Section **9** obtains smooth-input
lower bounds from supported functions. These are direct precedents for
representation-independent information lower bounds on parabolic
evaluation. The inspected reduction concerns a linear PDE at a fixed
target time; it does not state the nonlinear unstable-phase transfer
above.

[Petras and Ritter, *On the Complexity of Parabolic Initial Value
Problems with Variable
Drift*](https://drops.dagstuhl.de/storage/16dagstuhl-seminar-proceedings/dsp-vol04401/DagSemProc.04401.10/DagSemProc.04401.10.pdf),
Section **4.1**, **Theorem 2**, records classical signed-bump integration
bounds. Section **4.3**, **Theorem 4** and **Corollary 2**, transfers
randomized lower bounds to parabolic solution evaluation while explicitly
controlling higher-order terms. This is particularly relevant precedent
for the need to control nonlinear dependence on unknown input rather
than infer a lower bound from a large derivative alone. Its unknown
inputs are equation coefficients, with the initial condition fixed; it
does not give the present fixed-reaction, unknown-initial-profile,
large-horizon result in the inspected statements.

The closest known-method description is therefore **a classical
disjoint-support query lower bound transferred through positive heat
spreading and an unstable nonlinear flow**. No new lower-bound principle
is claimed. The 16-query search did not locate the exact combination;
priority remains unestablished, and older or differently indexed work
may contain it. The conventional proof does not depend on that search
being exhaustive.

## 8. Fixed possible formal targets after independent review

The proof obligations above are closed conventionally. If the independent
audit passes, the useful finite formal target is the actual information
inequality, not a theorem that assumes exponential query growth:

1. For a finite index set of size `K`, measurable no-visit events, a
   common output on each paired event, target separation at least one,
   and pointwise coverage `number visited≤Q`, prove (I) and derive
   `E Q≥K(1−4 epsilon^2)`. A bounded-output formulation loses no
   algorithms: clipping to `[−1,1]` cannot increase error for these PDE
   targets or query cost. The adaptive-transcript implication must then
   be stated separately from this finite measure inequality.
2. Prove the scalar Allen–Cahn amplification implication used in (A),
   together with the background-perturbation arithmetic giving (G).
   This is only the finite scalar analytic component. Heat-kernel
   positivity, comparison, PDE existence, and the maximum-principle
   stability estimate remain explicit conventional bridges unless
   separately formalized.
3. The floor estimate in (M) transfers the finite family size to the
   exponential horizon bound. It is supporting arithmetic, not a
   substitute for the information or PDE arguments.

The recommendation is to review and formalize this fixed theorem before
any experiment. Numerical examples cannot establish a worst-case oracle
lower bound, and no extra sampler experiment is needed for this decision.

## 9. Bounded search log

The following 16 queries were used; primary-paper opens and in-document
searches followed. Secondary aggregators and search snippets were used
only to locate primary sources, not to support theorem claims.

1. `randomized complexity nonlinear initial value parabolic equations point evaluations lower bounds`
2. `information based complexity semilinear parabolic equations randomized lower bound`
3. `randomized integration smooth functions lower bound Bakhvalov disjoint bumps`
4. `Allen Cahn unstable equilibrium solution map exponential amplification lower bound`
5. `"Optimal confidence for Monte Carlo integration of smooth functions" arxiv`
6. `"complexity" "parabolic initial value problems" "randomized"`
7. `"semilinear" "information-based complexity" lower`
8. `"nonlinear semigroup" "complexity" approximation lower bound`
9. `"randomized complexity" "Feynman-Kac"`
10. `"Allen Cahn" "lower bound" "queries"`
11. `"parabolic" "complexity" "initial condition" "lower"`
12. `"initial value problems" "long time" "information-based"`
13. `"Complexity of multivariate Feynman-Kac path integration" arxiv`
14. `"Allen-Cahn" "information-based complexity"`
15. `"semilinear" "point evaluations" "lower bound" complexity`
16. `"parabolic" "randomized" "exponential" "time horizon" complexity`
