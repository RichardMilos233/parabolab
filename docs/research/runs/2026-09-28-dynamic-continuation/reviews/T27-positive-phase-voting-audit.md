# T27: positive-phase voting theory and primary-literature audit

Date: 2026-09-28. Scope: independent review of `04j-positive-phase-voting.md`;
no implementation, numerical experiment, Lean edit, or review of the broader
`04k` candidate. Reviewed source SHA-256:
`b7ded6be58eb0b0410f0ad445376c8eb2164eb7c8ea5bda2e5d1e28c46af2ee3`.
The math-auto-research skill, defaults, model-routing and execution guidance
were read. Role: mathematical reviewer; actual service model/effort is not
independently exposed here, so parent dispatch metadata remains authoritative.

## Verdict

**The stated ideal sampler is mathematically valid for every finite horizon,
with uniformly bounded expected full-tree node count and relative RMS defect
error, under the strict phase bounds `0 < m <= v <= M < 1`.** No sign, clock,
dimension, or integrability counterexample was found. The proof details below
close the draft's completion and measurable-mild-correspondence sketches
without assuming the desired representation in advance.

The published variance constant is valid but unnecessarily weak. It improves
from `K_range^2/4` to `K_range - 1`. The pure ternary construction is also not
the cheapest elementary voting representation: a binary/ternary mixture has
the same mean and range, and a smaller uniform node bound. An ODE-barrier
estimate already meets some relative-error targets without querying the
spatial oracle. These comparisons limit efficiency claims; they do not refute
the all-horizon existence result.

This is a conventional mathematical verdict, not Lean or floating-point
certification. The bounded literature search found the generic voting,
normalization, and decaying-branching ingredients in primary predecessors.
The exact Allen–Cahn combination below was not located in the inspected
sources. Priority for that combination remains unconfirmed.

## 1. Exact statement and mild-data convention

Let `L = Delta/2` on `R^d`, or the generator of Brownian motion on a fixed flat
torus, with any finite integer `d >= 1`. Let `v` be bounded measurable with
pointwise bounds `0 < m <= v(x) <= M < 1`. Write `P_t` for its Markov heat
semigroup. The solution meant here is the unique bounded mild solution

```
u(t) = P_t v + integral_0^t P_(t-s) [u(s)-u(s)^3] ds.
```

Existence, comparison, and uniqueness follow by using a globally Lipschitz
extension of `f(a)=a-a^3` from `[0,1]`, semigroup iteration, and the invariant
constant barriers `0,1`. Order comparison on `[0,1]` can equivalently use the
increasing nonlinearity `f(a)+2a=3a-a^3` and the killed semigroup. Comparing
against the scalar solutions gives

```
ell_m(t) <= u(t,x) <= ell_M(t),
ell_b(t) = [1+(b^(-2)-1) exp(-2t)]^(-1/2).
```

No spatial derivative of `v` is required. Borel measurability is a convenient
probabilistic convention. Lebesgue-measurable data give the same positive-time
expectations after choosing a Borel representative: conditional on a finite
tree, each leaf endpoint has a heat-kernel distribution. At time zero the
chosen pointwise oracle is returned. For merely measurable data, do not
assert continuity in supremum norm at zero or convergence to the assigned
`v(x)` at every point; the usual semigroup trace is sufficient.

All uniform statements below range over **finite** `T >= 0`. They do not
define a Brownian endpoint or a relative error at `T = infinity`.

## 2. Algebra, signs, and bounded vertices

Put `ell=ell_m`, `r=1-ell` and `u=ell+r w`. Since `r'=-f(ell)`, the transformed
reaction is

```
[f(ell+r w) - (1-w) f(ell)]/r
 = r(1+2ell)w - 3ell r w^2 - r^2 w^3
 = r w(1-w)[1+2ell+r w].
```

Thus the transformed drift is nonnegative on `[0,1]`, vanishes at its
endpoints, and agrees with the draft. With

```
lambda = r(2+ell),
b = (0, (1+ell)/(2+ell), 1, 1),
B_ell(w) = 3 b1 w(1-w)^2 + 3 w^2(1-w) + w^3,
```

direct expansion gives

```
lambda(B_ell(w)-w)
 = r(1+2ell)w - 3ell r w^2 - r^2 w^3.
```

All Bernstein coefficients are in `[0,1]`. The eight products in the
multiaffine vertex `F_ell(z1,z2,z3)` are nonnegative and sum to one when each
`zi` is in `[0,1]`; consequently its return lies in `[0,1]`. Given the event
time and location, the child returns use independent descendant marks.
Multiaffinity, rather than any assertion that child values are Bernoulli,
then gives `E F_ell(Z1,Z2,Z3) = B_ell(E Z1)`.

For comparison, among pure ternary Bernstein representations of this same
reaction, the chosen rate is minimal: at any rate `beta`, the second
Bernstein coefficient of `w+F_reaction(w)/beta` is
`2/3 + r(2+ell)/(3 beta)`. Its being at most one requires
`beta >= r(2+ell)`. This does not imply minimum work over other offspring laws.

## 3. Time direction, hazard, and inverse

The root is at PDE time `T`; a particle advances for elapsed Brownian time
`T-s` to an event at remaining PDE time `s`. Its hazard there is `lambda(s)`,
and all three children start with remaining time `s`. This convention yields
the first-event equation

```
z(T,x) = exp(-Lambda(T)) P_T w0(x)
       + integral_0^T exp(-(Lambda(T)-Lambda(s))) lambda(s)
           P_(T-s)[B_ell(s)(z(s))](x) ds,
w0 = (v-m)/(1-m),   Lambda(t) = integral_0^t lambda(s) ds.
```

This is the killed-semigroup mild form of
`z_t = Lz + lambda(t)(B_ell(t)(z)-z)`. A forward-elapsed-time rate `lambda(t)`
without reversing its argument would describe a different tree/PDE.

Using `ell'=ell(1-ell)(1+ell)` gives

```
Lambda(T) = [2 log a - log(1+a)]_(a=m)^(a=ell(T)),
Lambda(infinity) = log((1+m)/(2m^2)).
```

Let `R(a)=a^2/(1+a)`. Then

```
P(no event while going from T down to s)
 = exp(-(Lambda(T)-Lambda(s))) = R(ell(s))/R(ell(T)).
```

For `U` uniform on `(0,1)`, if `U R(ell(T)) <= R(m)`, return a time-zero
leaf. Otherwise set `y=U R(ell(T))`. Since `R` is strictly increasing on
`(0,1)` and `R(m)<y<R(ell(T))<1/2`,

```
a = (y+sqrt(y^2+4y))/2,
s = (1/2) log((1-m^2)a^2 / (m^2(1-a^2)))
```

satisfy `a^2=y(1+a)`, `m<a<ell(T)` and `0<s<T`. This checks both inverse
steps and the Brownian edge variance `T-s`. Endpoint conventions for equality
or `U=0,1` have no probabilistic effect, but an implementation should specify
them. The formulas are exact-real identities, not stable floating formulas.

## 4. Completion and expected work without circularity

Construct independent clock and Brownian marks on the countable labelled
ternary tree. Let `N_D(T)` count nodes reached through generation `D`, stopping
artificially there, and put `n_D(T)=E N_D(T)`. This random count is finite before
any assertion about the full tree. Write

```
k(T,s) = exp(-(Lambda(T)-Lambda(s))) lambda(s).
```

The finite recursion, including the root in either case, is

```
n_0(T)=1,
n_(D+1)(T)=1+3 integral_0^T k(T,s) n_D(s) ds.
```

The explicit function

```
n(T) = (3 exp(2 Lambda(T))-1)/2
```

solves this integral equation with `n_D` replaced by `n`; equivalently,
`n(0)=1` and `n'=lambda+2 lambda n`. Positivity of `k` proves inductively
`n_D<=n`. Since the counts increase with `D`, monotone convergence gives

```
E N_infinity(T) <= n(T) <= K_m < infinity,
K_m = [3((1+m)/(2m^2))^2-1]/2.
```

Therefore `N_infinity(T)` is finite almost surely and the recursion completes.
Only now take the limit in the count recursion. It solves the same linear
integral equation; uniqueness yields `E N_infinity(T)=n(T)`. A completed
ternary tree has `N=1+3I` nodes and `L=1+2I` leaves, so
`N=(3L-1)/2` and `E L=exp(2 Lambda(T))` follow as well. In particular `K_(1/2)=13`.
No solution expectation, unproved integrability, or infinite-tree return was
used to obtain completion.

Now the bounded vertex rule defines an integrable completed return `Z_w`.
Its expectation satisfies the first-event equation in Section 3. The maps
`B_ell` are uniformly Lipschitz on `[0,1]` (the bound `3` suffices), so semigroup
contraction and Gronwall give uniqueness among bounded `[0,1]`-valued mild
solutions on every finite interval. Transforming back identifies

```
E[ell(T)+r(T)Z_w] = u(T,x),
E[r(T)(1-Z_w)] = 1-u(T,x).
```

## 5. Relative defect bound and a strict improvement

Set `a_b=b^(-2)-1` and `K=K_range=a_m/a_M>=1`. The stable defect formula is

```
r_b(t) = a_b exp(-2t) /
  [sqrt(1+a_b exp(-2t)) (1+sqrt(1+a_b exp(-2t)))].
```

Its denominator is increasing in `a_b`, hence `r_m/r_M<=K`. This constant
cannot be improved using just the uniform ratio: the ratio tends to `K` as
`t` tends to infinity. If `D=1-u(T,x)` and `H=r_m(T)(1-Z_w)`, comparison gives
`0<r_M(T)<=D<=r_m(T)` and `0<=H<=r_m(T)`.

The draft's `Var(H)/D^2 <= K^2/4` follows from the range bound. More sharply,
`H^2<=r_m H` gives

```
Var(H) <= r_m D - D^2,
Var(H)/D^2 <= r_m/D - 1 <= K-1.
```

This always improves the stated bound since
`K^2/4-(K-1)=(K-2)^2/4>=0`. For `rho>0`,

```
n_roots = max(1, ceil((K-1)/rho^2))
```

independent roots therefore give relative RMS at most `rho`, with expected
total nodes at most `K_m n_roots`, uniformly over finite `T`, `x`, and `d`.
For `m=M`, the data are known constant and the exact scalar ODE solution can
be returned without sampling. This corner case also correctly has zero
variance under the improved inequality.

## 6. Falsification attempts and stronger comparisons

The following are analytical checks, not executed numerical experiments.

- At `T=0`, the tree has one leaf and returns `v(x)`, so there is no initial
  normalization error. At `v=m`, every normalized leaf and ancestor is zero,
  giving the exact lower scalar solution. For any constant `v=b` in `[m,M]`,
  bounded mild uniqueness identifies the mean with `ell_b(T)`.
- As `m` tends to zero, the integrated hazard diverges and `K_m` grows like
  `3/(8m^4)`. Nothing here extends uniformly to `m=0`, interfaces, or arbitrary
  sign-changing data. As `M` tends to one, the relative-defect constant
  diverges. These are visible restrictions, not hidden counterexamples.
- The root oracle and Brownian endpoints work in arbitrary finite dimension,
  but a Gaussian endpoint costs `O(d)` scalar draws, and the cost of evaluating
  `v` is unspecified. Precision sufficient to resolve a defect of order
  `exp(-2T)` is outside the node-count theorem. Returning `1-H_u` in ordinary
  floating arithmetic can lose the entire defect; using the direct defect
  output is logically part of a future arithmetic contract.

**Cheaper mixed voting rule.** Define

```
p_ell = 3(1+ell)/(2(2+ell)),
OR2(w) = 2w-w^2,
MAJ3(w) = 3w^2-2w^3.
```

Then `3/4<=p_ell<1` and

```
B_ell(w) = p_ell OR2(w) + (1-p_ell) MAJ3(w).
```

At the same clock, select two-child OR with probability `p_ell`, or
three-child majority with probability `1-p_ell`. Their bounded multiaffine
returns are respectively `z1+z2-z1 z2` and
`z1 z2+z1 z3+z2 z3-2 z1 z2 z3`. They preserve the mean PDE and `[0,1]` range.
This changes the estimator law; equality of its variance with the ternary
estimator is not claimed.

The mean population growth rate is now

```
g(t)=lambda(t)(2-p_ell(t)) = r(t)(5+ell(t))/2,
A(T)=integral_0^T g(t)dt
    = [(5/2)log a - 2log(1+a)]_m^ell(T),
exp(A(infinity)) = (1+m)^2/(4m^(5/2)).
```

For a completed tree with every internal node having at least two children,
`N<=2L-1`. The same finite-generation argument justifies completion and
`E L=exp(A(T))`. Consequently the mixed rule has the bound

```
E N <= 2exp(A(T))-1 <= (1+m)^2/(2m^(5/2))-1.
```

At `m=1/2` the last number is `9sqrt(2)/2-1`, about `5.364`, compared with `13`.
Together with the same universal `K-1` variance bound, this is a stronger
certified work upper bound. The specific decomposition and cost calculation
are audit derivations, not a claim that this exact formula was found in a
published source. Mixed offspring voting itself has an explicit predecessor
in O'Dowd's Section 4.5, cited below.

**Zero-query ODE baseline.** Given only `D in [a,b]=[r_M(T),r_m(T)]`, the harmonic
center `D_hat=2ab/(a+b)` satisfies

```
sup_(D in [a,b]) |D_hat-D|/D = (b-a)/(b+a)
                           <= (K-1)/(K+1).
```

Equality of the endpoint relative errors proves this minimax formula. Any
empirical accuracy regime already covered by this bound has a deterministic
competitor requiring no spatial calls. A meaningful sampler demonstration
should beat this baseline's actual finite-`T` error guarantee. Returning the
equilibrium itself has relative defect error one and remains an inadequate
baseline for a small relative target.

## 7. Bounded primary-literature audit

The search used 30 query strings, followed by targeted primary-source reads,
on 2026-09-28 and ended after the sources below. The
statements about overlap concern the inspected material; they are not an
exhaustive bibliographic priority judgment.

| Primary source | Established overlap and limitation |
| --- | --- |
| [An, Henderson and Ryzhik, *Voting models and semilinear parabolic equations* (2022 preprint)](https://arxiv.org/html/2209.03435) | Sections 3.2–3.3, Theorems 3.2–3.3 and equations 3.28–3.31 give polynomial Bernstein voting and a sufficient branching rate. Section 3.4 treats deterministic recursive propagation. These cover the algebraic voting ingredient, with constant rate and continuous initial data in the stated theorems. The inspected text does not state the positive scalar-barrier rescaling, finite integrated hazard, or uniform relative-defect/work combination. |
| [Zack O'Dowd, *Branching Brownian motion and partial differential equations* (Oxford thesis, 2019)](https://www.stats.ox.ac.uk/~etheridg/odowd.pdf) | Chapter 4 gives voting measures and generalized voting; Corollary 4.4.6 covers inward-pointing polynomial endpoint signs. Section 4.5 and Proposition 4.5.2 explicitly permit arbitrary offspring distributions, including mixtures. Lemma 3.1.8 gives the classical mean population formula. The text uses fixed branching rates; no exact barrier-rescaled uniform-work relative-defect result was located. |
| [Etheridge, Freeman and Penington, *Branching Brownian motion, mean curvature flow and the motion of hybrid zones* (2016 preprint; 2017 publication)](https://arxiv.org/abs/1607.07563) | Primary predecessor for Allen–Cahn ternary majority voting. The abstract and its precise role in the AHR construction were inspected. This is prior art for the untransformed voting representation, not evidence that the present complexity statement is new. The full EFP technical text was not audited here. |
| [Engländer and Winter, *Law of Large Numbers for a Class of Superdiffusions* (2005 preprint; 2006 publication)](https://arxiv.org/pdf/math/0504377) | Section 2.1 and Appendix B, Lemma 3, use a space-time transform `H(x,t)=exp(-lambda_c t)h(x)` producing zero linear growth and branching coefficient `alpha h exp(-lambda_c t)`. The proof explicitly exploits exponentially decaying branching. Thus normalization producing an integrable branching coefficient is established prior art. The process and objective are superdiffusion laws of large numbers, not an unbiased bounded Allen–Cahn voting query with the stated node and relative-defect bounds. |
| [Ossiander, *A probabilistic representation of solutions of the incompressible Navier–Stokes equations in R3* (2004 preprint)](https://arxiv.org/pdf/math/0412034) | Sections 3–5 use majorizing kernels, normalized functionals, h-Brownian motion and terminating cascades to obtain small-data all-time representations. This excludes a broad claim to have invented normalization or all-horizon bounded stochastic representations. Its equation, hypotheses and tree differ from the present construction. |
| [Henry-Labordère, Oudjane, Tan, Touzi and Warin, *Branching diffusion representation of semilinear PDEs and Monte Carlo approximation*](https://arxiv.org/html/1603.01727) | Allows time/space polynomial coefficients and age-dependent lifetimes; it provides Monte Carlo representations and moment criteria, with explicit small-maturity/small-nonlinearity restrictions in Assumption 3.10 and Theorem 3.12. General nonconstant coefficients/lifetimes are therefore not new. It does not, in the inspected statements, supply the present uniform relative-defect result. |
| [Agarwal and Claisse, *Branching diffusion representation of semi-linear elliptic PDEs and estimation using Monte Carlo method*](https://eprints.gla.ac.uk/210343/7/210343.pdf) | Proposition 3.4 bounds estimator moments using supersolutions; the following discussion uses dominating branching processes. Supersolution-based moment certification and finite-depth limiting arguments are known methods. This is an elliptic bounded-domain result, not the exact time-uniform positive-phase theorem. |
| [Hwang et al., *Unconditionally stable Monte Carlo simulation for solving the multi-dimensional Allen–Cahn equation* (2023)](https://aimspress.com/article/doi/10.3934/era.2023261) | Uses operator splitting, Monte Carlo diffusion and a local analytic nonlinear step on a virtual grid. It is a relevant existing numerical comparator for stability and long-time computation. Its discretized algorithm is not the same unbiased point-query estimator, and the inspected results do not establish uniform relative defect work. |

Search families included exact and combined phrases for Allen–Cahn voting,
time-dependent/time-inhomogeneous branching, ODE/lower barriers, normalization,
supersolutions, uniform-in-time Monte Carlo, relative error, equilibrium and
long-time variance. Exact-title and citation follow-ups retrieved the primary
papers above. Searches also returned unrelated physics and social-voting
material, which was not used as evidence. A repository metadata result for a
recent *Vote-BranchNet* dissertation was seen, but its full text was not
retrieved; no overlap or non-overlap claim rests on that lead.

**Positioning allowed by this search:** an explicit synthesis for the strict
positive phase of Allen–Cahn, with proved constants for finite-horizon exact
sampling, is mathematically defensible. **Positioning not established:** a
new generic voting method, a new principle of normalization producing
decaying branching, the first all-horizon branching representation, global
priority for the exact theorem, optimal work, or a demonstrated practical
advantage. Citation chasing in superprocess transforms, perfect simulation
and numerical voting literature remains incomplete.

## 8. Fixed possible Lean targets after this review

These are approved mathematical statements for a possible later handoff,
not declarations claimed to have been built. Keep the original pure ternary
sampler as the target unless root explicitly selects the mixed alternative.

1. **Transformation and Bernstein identities.** For real `ell,w`, prove the
   denominator-cleared cubic transformation in Section 2. Under `0<=ell<=1`,
   prove the Bernstein expansion, coefficient and multiaffine range bounds
   (so the denominator `2+ell` is positive). These directly check the signs
   and the pathwise invariant.
2. **Clock algebra.** For `0<a<1`, prove `R(a)=a^2/(1+a)` is increasing, the
   positive quadratic inverse for `0<y<1/2`, and
   `(2/a-1/(1+a))*a*(1-a)*(1+a)=(1-a)*(2+a)`. If only the last algebraic
   identity is encoded, the logarithmic integral, ODE, and clock distribution
   remain outside formal coverage.
3. **Finite-tree work facts.** For a finite full ternary tree, prove
   `N=1+3I`, `L=1+2I`, hence `N=(3L-1)/2`. Prove the nonnegative-kernel
   finite-iteration domination `n_D<=n` with the actual recurrence from
   Section 4 if the relevant integration infrastructure is included. A
   formal real-number recurrence alone is not a proof that its terms equal
   stochastic node-count expectations.
4. **Defect ratio and moment algebra.** Prove the actual square-root defect
   ratio for `0<m<=M<1`, finite `t>=0`, and then: if `mu>0`, `s2<=r*mu`,
   `0<q<=mu`, `r<=K*q`, `K>=1`, then
   `s2-mu^2 <= (K-1)*mu^2`. The latter is the deterministic bridge; a full
   variance theorem additionally requires `mu=E H`, `s2=E H^2`, boundedness,
   and unbiasedness.
5. **Optional comparison targets.** Prove the exact binary/ternary polynomial
   decomposition and its probability bounds, the finite-tree inequality
   `N<=2L-1`, and the harmonic-center relative-error bound for `0<a<=b`.
   These validate comparisons without silently replacing the sampled law.

PDE mild existence/comparison/uniqueness, stochastic construction,
conditional independence, monotone convergence, unbiasedness, sample-mean
RMS, and all real-arithmetic/oracle-to-bit-cost bridges must be listed
separately if they are not formalized. A successful finite algebra build
must not be reported as full verification of the all-horizon estimator.
