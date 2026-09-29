# T30: two-moving-barrier voting audit

Date: 2026-09-28. Independent mathematical review of
`04l-two-barrier-voting.md`, reviewed SHA-256
`905bb1e12b890e3a13ea48d7f1583f856b020c2cc2cbc7c90b8b2b6489e774ce`.
The source was not edited. Frozen T27 was preserved. This report also checks
the root's subsequent Allen–Cahn ratio-clock addendum, labelled separately
below. No Lean, implementation, numerical experiment, or new broad literature
search was performed. The applicable skill/routing instructions were already
read for T27; actual service model/effort is not independently exposed here.

## Verdict and exact scope

**Pass as an ideal mathematical representation and node-work theorem.** The
two-barrier width has the stated finite integral without a simple equilibrium
root. The transformed polynomial, sufficient Bernstein rate, noncircular
completion argument, unbiased bounded output, positive-interval relative
variance, and Allen–Cahn constants all check out. The root's later explicit
ratio clock is also correct and improves the Allen–Cahn node bound.

One terminology correction is needed: the hypotheses establish an equilibrium
**attracting from below within the prescribed basin**. They do not establish
two-sided Lyapunov stability. For example, `(b-y)^q` with even `q` is repelling
above `b`. This does not alter the candidate's basin theorem.

The assumptions remain: a real polynomial `f` of degree at most the integer
`n>=2`; finite real bounds `m<M<b`; `f(b)=0`; `f(y)>0` for `m<=y<b`; bounded
measurable `m<=v<=M`; and a finite query horizon. The claim charges ideal
visited nodes, with the specified transition, scalar-flow and clock oracles.
It does not establish finite-bit complexity or measured runtime. The generic
statement still requires a scalar-flow/clock-oracle contract; the special
Allen–Cahn clock has explicit elementary inverses.

## 1. Scalar barriers and the integrable-width mechanism

Each scalar solution `ell_c'=f(ell_c)`, `ell_c(0)=c in [m,b)`, is increasing,
stays below `b`, exists globally, and converges to `b`. Boundedness prevents
finite-time escape. Local Lipschitz uniqueness prevents finite-time contact
with the equilibrium. A limit strictly below `b` would have positive velocity
bounded away from zero and is impossible.

Let `l=ell_m`, `a=ell_M`, and

```
Delta = integral_m^M 1/f(y) dy.
```

The denominator is continuous and positive on the compact interval `[m,M]`,
so `0<Delta<infinity`. Separation of variables gives `l(Delta)=M`; autonomous
ODE uniqueness then gives `a(t)=l(t+Delta)`. In particular `h=a-l>0`.

The essential finite identity, valid for every `T>=0`, is

```
integral_0^T h(t)dt
 = integral_T^(T+Delta) l(s)ds - integral_0^Delta l(s)ds
 = J - integral_T^(T+Delta) (b-l(s))ds,
J = integral_0^Delta (b-l(s))ds.
```

There is no subtraction of two divergent improper integrals here. The
remainder is nonnegative and at most `Delta*(b-l(T))`, which tends to zero.
Consequently

```
integral_0^infinity h(t)dt = J
 = integral_m^M (b-y)/f(y)dy
 <= Delta*(b-m) < infinity.
```

The last equality uses the scalar ODE change of variables on the finite
interval `[0,Delta]`. Its upper spatial endpoint is `M<b`; no integrability
of `(b-y)/f(y)` up to `b` is asserted or needed.

An exact abstract version of this argument is valid and suitable for a
formal gate: if `l` is continuous and nondecreasing on `[0,infinity)`,
`l(t)<=b`, `l(t)->b`, and `Delta>=0`, then
`h(t)=l(t+Delta)-l(t)` is nonnegative and integrable on `[0,infinity)`, with
integral `J` above. Finite-interval telescoping, the displayed squeeze and
monotone convergence prove integrability; it is not a hypothesis. A continuous
constant extension of `l` to negative arguments is harmless provided the
integral in the theorem remains over `[0,infinity)`. This covers `Delta=0`
as well, although the sampler itself assumes the strict bracket `m<M`.

## 2. Interpolation cancellation and Bernstein coefficients

For `u=l+h w`, the scalar derivatives are `l'=f(l)` and `h'=f(a)-f(l)`. Thus

```
F_t(w) = [f(l+h w) - (1-w)f(l) - w f(a)]/h
       = sum_(j=2)^n f^(j)(l)/j! * h^(j-1) * (w^j-w).
```

The constant and first-order Taylor terms cancel exactly. Both endpoint
values of `F_t` vanish; no concavity or sign assumption on `f''` is needed.

For completeness, the degree-`n` Bernstein coefficient of `w^q(1-w)` is

```
c_(q,k) = [binom(k,q)/binom(n,q)] * (n-k)/(n-q),
1<=q<=n-1,
```

with `binom(k,q)=0` when `k<q`. It is nonnegative and no larger than
`k(n-k)/(n(n-1))`. For `q<=k<=n-1`, its ratio to that upper bound is

```
product_(i=1)^(q-1) (k-i)/(n-i-1) <= 1;
```

the product is empty when `q=1`. The cases `k=0,n` have coefficient zero.
Since `w^j-w = -sum_(q=1)^(j-1) w^q(1-w)`, the candidate's bound follows.

The constant

```
C = sum_(j=2)^n (j-1) sup_[m,b]|f^(j)|/j! * (b-m)^(j-2)
```

is finite and nonnegative. From `0<h<=b-m`, each interior coefficient `d_k`
of `F_t` satisfies

```
|d_k| <= C h * k(n-k)/(n(n-1)).
```

If `C>0`, take `lambda=C h` and `b_k=k/n+d_k/lambda`. The sufficient
coefficient interval is certified explicitly by

```
k/n - k(n-k)/(n(n-1)) = k(k-1)/(n(n-1)) >= 0,
1 - k/n - k(n-k)/(n(n-1))
  = (n-k)(n-k-1)/(n(n-1)) >= 0.
```

Hence `0<=b_k<=1`, `b_0=0`, `b_n=1`, and `F_t=lambda(B_t-w)`. Any certified
larger constant in place of `C` works too, so exact computation of each
supremum is not logically necessary. If `C=0`, all second and higher
derivatives vanish on a nontrivial interval; `f` is affine and `F_t=0`.
The transformed equation is then the heat equation and needs no branching.

## 3. Clock contract, completion and mild correspondence

For the general construction, define
`Lambda(t)=C integral_0^t h(s)ds`. If `C>0`, this is continuous and strictly
increasing at every finite time. For a root at remaining PDE time `T`, an
exact clock is specified by a uniform `U in (0,1)`:

```
if U <= exp(-Lambda(T)): there is no event before time zero;
otherwise choose the unique s in (0,T) satisfying
  Lambda(s) = Lambda(T)+log U.
```

The survival probability from remaining time `T` to remaining time `s` is
`exp(-(Lambda(T)-Lambda(s)))`; the Brownian edge lasts `T-s`. A generic
polynomial does not guarantee a simple elementary scalar-flow or inverse
formula. These evaluations must be supplied as exact ideal oracles, or a
later arithmetic theorem must account for their approximation. For `C=0`,
skip the inverse and return a single heat leaf.

To justify the full tree, let `q_D(T)` be the expected number of visited nodes
through generation `D`, artificially stopping there. Finite-depth counts
exist before any full-tree integrability assertion. With
`k(T,s)=exp(-(Lambda(T)-Lambda(s)))*lambda(s)`,

```
q_0(T)=1,
q_(D+1)(T)=1+n integral_0^T k(T,s) q_D(s)ds.
```

The explicit comparison function

```
q(T) = [n exp((n-1)Lambda(T))-1]/(n-1)
```

satisfies the same fixed integral equation, or `q'=lambda+(n-1)lambda*q`
with `q(0)=1`. Kernel positivity proves `q_D<=q` inductively. Monotone
convergence yields finite expected full node count and therefore an almost
surely finite tree. Taking the limit in the count equation and applying
linear uniqueness gives equality with `q(T)`. The budget from Section 1 then
gives exactly the proposed `K_work`.

At a completed vertex, the multiaffine extension of the Bernstein voting
coefficients is a convex combination and belongs to `[0,1]`. Independent
child subtrees conditional on their common time and location give
`E F_vertex(children)=B_t(E child)`. Thus the bounded expected return `z`
satisfies

```
z(T)=exp(-Lambda(T)) P_T[(v-m)/(M-m)]
   + integral_0^T k(T,s) P_(T-s)[B_s(z(s))]ds.
```

This is the transformed mild equation. Since each `B_s` is Lipschitz on
`[0,1]` with a common bound `n`, bounded mild uniqueness identifies `z=w`.
For the original equation, a globally Lipschitz extension of `f` from
`[m,b]`, positivity of the heat semigroup and scalar comparison first give
existence, uniqueness and `l<=u<=a`. Equivalently, the expected transformed
solution can be changed back and identified with that unique solution.
The argument does not use unbiasedness to prove completion.

Bounded measurable data suffice. Initial values are assigned at time zero;
there is no assertion of pointwise convergence at every discontinuity or
continuity in supremum norm. The mild affine transformation follows using
the differentiable scalar factors and variation of constants, without
spatial derivatives of the data.

Consequently

```
H_u=l(T)+h(T)Z,
H_def=b-a(T)+h(T)(1-Z)
```

are unbiased for `u(T,x)` and `b-u(T,x)`, and every return satisfies the
strict positive defect interval `[b-a(T), b-l(T)]`.

## 4. Relative variance and the nonhyperbolic baseline

Polynomial divisibility makes `g(y)=f(y)/(b-y)` continuous on `[m,b]`, with
`g(b)=-f'(b)`. Since `f` is positive immediately to the left of its zero,
the left derivative gives `f'(b)<=0`; thus `g>=0` on this interval. Its finite
maximum `G` gives

```
r_m(T)/r_M(T)
 = exp(integral_T^(T+Delta) g(l(s))ds) <= exp(G Delta)=K.
```

For a random variable `H in [A,B]`, `0<A<=B`, write `mu=E H` and
`s2=E H^2`. The pointwise inequality `(H-A)(H-B)<=0` gives
`s2<=(A+B)mu-AB`. Completing a square gives the desired sharp range result:

```
(B-A)^2 mu^2 - 4AB[(A+B)mu-AB-mu^2]
 = [(A+B)mu-2AB]^2 >= 0,

Var(H)/mu^2 <= (B-A)^2/(4AB).
```

Its maximum is attained, among all distributions with this support, by
endpoint mass `P(H=B)=A/(A+B)` and mean `2AB/(A+B)`. Thus the candidate's
optimization is correct. Applying it to `H_def`, and using that
`(R-1)^2/(4R)` increases for `R>=1`, proves the stated bound
`(K-1)^2/(4K)` and the deterministic iid root-count guarantee. No central
limit theorem is needed for the RMS assertion.

If `f'(b)=0`, then `g(l(s))->0`. The fixed-length integral over
`[T,T+Delta]` tends to zero, so `r_m/r_M->1`. Accordingly the harmonic-center
estimate has relative error bounded by `(r_m-r_M)/(r_m+r_M)->0`. This holds
for every datum in the bracket; it is a genuine no-spatial-query large-time
competitor, not merely a constant-profile check. In the simple-root case the
ratio instead tends to `exp((-f'(b))*Delta)>1`.

## 5. Explicit analytical stress test at a multiple root

Take `f(y)=(1-y)^2`, `b=1`, `m=0`, `M=1/2`. Then

```
l(t)=1-1/(1+t),   a(t)=1-1/(2+t),   Delta=1,
h(t)=1/[(1+t)(2+t)],
integral_0^infinity h=log 2,
integral_0^infinity (1-l)=infinity.
```

Here `C=1`, `F_t(w)=h(t)(w^2-w)`, and the voting map is simply the binary
AND map `B(w)=w^2`. Therefore the full expected node count is at most
`2exp(log 2)-1=3` for every finite horizon. The defect ratio is
`(t+2)/(t+1)`, while the harmonic-center relative error bound is
`1/(2t+3)`. This exact example checks both the new integrable-width mechanism
and the limitation on large-time efficiency claims. No numerical code was
used for these identities.

The candidate's general formula for `(b-y)^q`, integer `q>=2`, is also
correct. Its equilibrium residual has nonintegrable order
`t^(-1/(q-1))`; the one-equilibrium normalized reaction has scale
`r_m^(q-1)`, of order `1/t`. The two-shift width nevertheless has the finite
budget `integral_m^M (b-y)^(1-q)dy`. The distinction concerns these specified
representations, not impossibility for every one-barrier algorithm.

## 6. Allen–Cahn specialization: source and checked addendum

Under the specialization `b=1`, `f(y)=y-y^3`, `0<m<M<1`, expansion gives

```
F_t(w)=h w(1-w)[2l+a+h w],
lambda=h(l+2a),
b=(0,(l+a)/(l+2a),1,1).
```

Both signs and coefficients are correct. With
`p=3(l+a)/(2(l+2a))`, `3/4<p<1`,

```
B=p OR2+(1-p) MAJ3,
OR2(w)=2w-w^2,   MAJ3(w)=3w^2-2w^3,
lambda(2-p)=h(l+5a)/2 <= 3h.
```

The selected event has two or three independent children. It preserves the
mean and output interval, not necessarily the distribution or actual variance
of the pure ternary return. The mean leaf population is
`exp(integral lambda(2-p))`. Every completed such tree has `N<=2L-1`;
finite-depth domination justifies this expectation before using it as a work
bound. Since

```
I_h=log[M(1+m)/(m(1+M))],
```

the source's bound `E N<=2 exp(3 I_h)-1` is valid. At `m=1/2,M=3/4` it is
exactly `1115/343`. The tighter scalar defect ratio is at most `27/7`, and
the positive-interval relative variance bound is exactly `100/189`.

**Checked root addendum, not present in the reviewed source hash.** Define

```
alpha=m^(-2)-1,   beta=M^(-2)-1,
z(t)=l(t)/a(t)
    =sqrt[(1+beta exp(-2t))/(1+alpha exp(-2t))],
z0=m/M,   R(z)=z^2/(1+z).
```

Then `0<z0<=z(t)<1`, `z(t)->1`, and

```
z'=z(a^2-l^2),
d/dt log R(z(t)) = h(l+2a)=lambda(t).
```

Therefore `Lambda(T)=log(R(z(T))/R(z0))`. At a root time `T`, use a uniform
`U in (0,1)`. If `U R(z(T))<=R(z0)`, there is no event; otherwise set

```
y=U R(z(T)),
zeta=(y+sqrt(y^2+4y))/2,
s=-(1/2)log[(1-zeta^2)/(alpha*zeta^2-beta)].
```

The domain checks are explicit: `z0<zeta<z(T)<1` and

```
alpha*zeta^2-beta >= alpha*z0^2-beta = 1-z0^2 > 0.
```

The ratio inside the logarithm is strictly between `exp(-2T)` and `1`, so
`0<s<T`. It is the inverse of `z(s)=zeta`, and the Brownian variance is
`T-s`. At `T=0` there is no event. Uniform endpoint conventions affect only
null events. This eliminates a non-elementary clock oracle in the special
case, but cancellation near `z=1` or `m=M` still needs a separate numerical
arithmetic contract.

For the mixed offspring law,

```
p=3(1+z)/(2(2+z)),
d/dt [(5/2)log z - 2log(1+z)] = lambda(2-p).
```

Thus, writing `Gamma(T)=integral_0^T lambda(2-p)`,

```
exp(Gamma(infinity)) = (1+z0)^2/(4*z0^(5/2)),
E N(T) <= 2exp(Gamma(T))-1
       <= (1+z0)^2/(2*z0^(5/2))-1.
```

For `z0=2/3`, the last expression is `25sqrt(6)/16-1`, approximately
`2.8273`, strictly improving the source's coarse `1115/343`. It is an upper
bound, not the exact expected total node count. The relative variance bound
`100/189` remains valid because the root support interval is unchanged.

## 7. Scoped conservative-Markov-kernel corollary

The proof extends immediately to a jointly measurable conservative Markov
transition semigroup `P_t` on a standard Borel state space, provided an exact
independent sampling oracle for `P_t(x,dy)` and a bounded measurable data
oracle are supplied. The relevant target is the semilinear mild integral
equation with `P_t`, whether or not its generator has a differential form.

Positivity, contraction and `P_t 1=1` give scalar comparison and preserve the
affine constants. Kernel composition, Fubini, and scalar variation of
constants give the transformed mild equation. Independent edge samples give
the same renewal identity and counts. No Euclidean dimension or Brownian
path continuity is used in the node argument. Transition-oracle costs remain
uncharged. Nonconservative kernels do not satisfy the same constant-barrier
argument and are outside this corollary.

## 8. Failed attacks, limits, and prior-ingredient scope

- A multiple equilibrium root does not invalidate the width integral: the
  finite shift-window identity is sufficient even with a divergent residual
  integral. The quadratic example above exhibits this explicitly.
- Large curvature or changing concavity of `f` does not invalidate the voting
  coefficients; absolute derivative bounds enter `C`. They may make the
  sufficient cost constant very large. No optimality is claimed.
- The strict conditions `m<M<b` matter. As `M` approaches `b`, the finite
  travel-time and positive lower defect bounds can deteriorate. At `M=b`
  they cannot be invoked. At `m=M`, the proposed division by width is
  undefined; known constant data should instead use the exact scalar solution.
- Bounded arbitrary measurable input does not provide a finite-bit oracle
  complexity theorem. Nor do exact inverse identities certify stable
  floating evaluation of a very small width or defect.
- The construction changes the stochastic representation. It is not a
  likelihood proposal repairing the original derivative-code estimator.

T27's primary-source audit remains the attribution basis. General Bernstein
voting already appears in [An–Henderson–Ryzhik, Theorems 3.2–3.3](https://arxiv.org/html/2209.03435)
and [O'Dowd's thesis, Chapter 4](https://www.stats.ox.ac.uk/~etheridg/odowd.pdf);
the latter also treats mixed offspring. The normalization-to-decaying-branching
ingredient has a direct antecedent in [Engländer–Winter, Appendix B Lemma 3](https://arxiv.org/pdf/math/0504377).
[Ossiander's normalized all-time cascades](https://arxiv.org/pdf/math/0412034)
also preclude a broad first-all-horizon-representation claim. The exact
two-moving-barrier width identity plus positive-interval relative-defect and
node-work synthesis was not searched independently here. Neither T27's
bounded search nor this mathematical audit settles priority for it.

## 9. Fixed possible Lean targets

These targets have validated conventional proofs. They are not claims that
formal declarations have been built.

1. **Actual integrated-width theorem.** Formalize the abstract continuous
   monotone shift lemma in Section 1, including `IntegrableOn h [0,infinity)`
   and the exact integral `J`. Do not assume integrability of `h`, finite
   integrated hazard, or integrability of `b-l`. The proof is finite-interval
   telescoping, `0<=tail<=Delta*(b-l(T))`, and monotone convergence. The
   finite-horizon bound by `J` is a useful intermediate declaration.
2. **Scalar-flow bridge.** Record separately whether ODE global existence,
   `l(Delta)=M`, the uniqueness-based shift `a(t)=l(t+Delta)`, and
   `J=integral_m^M (b-y)/f(y)dy` are formalized. The abstract shift theorem
   proves the analytical mechanism, but alone does not instantiate it for
   the polynomial scalar ODE. Merely assuming `Lambda(T)<=budget` is a
   weaker, conditional work theorem and does not cover this new mechanism.
3. **Finite coefficient gate.** Prove the interpolation/Taylor polynomial
   identity, the degree-elevation formula and coefficient inequalities in
   Section 2, and `0<=k/n+d_k/lambda<=1` under the stated bounds. A cubic
   specialization is legitimate if explicitly labelled as such; it is not
   the full degree-`n` assertion.
4. **Finite tree and moment algebra.** Prove full `n`-ary count relations,
   the finite-depth nonnegative-kernel domination, and the completed-square
   inequality in Section 4 under real moment hypotheses. The stochastic
   identification of counts/moments, limit construction, unbiasedness and
   iid RMS remain additional bridges if omitted.
5. **Allen–Cahn identities and constants.** Prove its transformed polynomial,
   coefficient and mixed-rule identities; `z'=z(a^2-l^2)` from the two scalar
   ODE identities; the two logarithmic derivative identities; and the
   denominator/domain facts for the ratio-clock inverse. Check the rational
   constants `1115/343` and `100/189`, and the sharper radical expression
   `25sqrt(6)/16-1`. If calculus or square-root/log inverse steps are omitted,
   do not describe an algebra-only build as a checked sampling clock.
6. **Relative-error transfer and baseline.** Prove monotonicity of
   `(R-1)^2/(4R)` on `R>=1`, and the harmonic-center guarantee for positive
   intervals. The scalar logarithmic shift bound and its nonhyperbolic limit
   should be linked to the exact assumptions rather than replaced by an
   unexplained ratio constant.

PDE/kernel mild correspondence, measurability, conditional independence,
probability construction, expected-count identification and arithmetic costs
must retain their own coverage status. The validated theorem supports a
theory-to-Lean handoff; it does not bypass that gate to authorize sampler code.
