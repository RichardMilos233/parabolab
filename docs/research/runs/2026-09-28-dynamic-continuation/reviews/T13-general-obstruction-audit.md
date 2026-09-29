# T13 — adversarial audit of the general absolute-moment obstruction

Date: 28 September 2026. Scope: D10 in `04c-general-obstruction.md` and
`reviews/T10-polynomial-obstruction.md`, with `04-theory.md` as context.
The parent subsequently requested a bounded review of
`04d-sharp-constant-horizon.md`; that review is included below. This task owns
only this file. No numerical experiment, code change, test run, or Lean build
was performed. The research role follows the math-auto-research execution
profile; independent serving-model/effort telemetry is unavailable.

## Verdict and corrections

**PASS for the finite-derivative obstruction and the analytic all-horizon
classification, under the precise sampling contract below.** I found no
counterexample to their stated mathematical conclusions. The exact
constant-profile horizon in `04d` also passes as a conventional theorem,
including its finite value at a finite-radius critical time.

The following points should be made explicit when these statements are
promoted into a theorem or report:

1. A finite-depth restriction means the original output multiplied by the
   indicator that its *completed* tree has depth at most $N$. It does not
   mean replacing unfinished descendants at depth $N$ by terminal data.
2. For adaptive proposals, exact weights must mean cancellation of the
   **full joint likelihood on completed trees**, equivalently the
   Radon–Nikodym contract in Section 1. Reciprocals of marginal clock laws
   are insufficient when the actual sampling law is conditional.
3. The infinite moment fields are nonnegative tree sums. Restarting their
   mild equations uses Tonelli and the semigroup identity; it must not be
   obtained by subtracting two expressions that may both be infinite.
4. The stronger smooth classification in Section 4 is valid and should
   replace any suggestion that analyticity is needed for a classification
   **in terms of terminal jets**. Analyticity is needed for the stated
   classification in terms of the reaction on the whole connected interval.
5. In `04d`, replace “Past that time the minimal extended tree sum is
   infinite” by “At and after a finite explosion time, the **Id tree sum**
   is infinite.” A highest retained field remains $V_n=a_n$, so divergence
   of every code field would be false.
6. Keep all claims about absolute tree mass separate from correspondence to
   the original nonlinear PDE. The flat-jet example demonstrates an actual
   failure of that implication, rather than merely an unverified technical
   assumption.

These are contract and scope corrections, not a refutation of D10. The
probabilistic construction, heat positivity and infinite-tree limit are
conventional arguments here; no end-to-end formal verification is supplied.

## 1. What proposal independence must mean

Fix $t,x,c$. Let $\mathcal T_{t,x,c}$ be the disjoint union of all
finite, labelled, completed tree topologies with their internal times and
Brownian marks. On a fixed topology, the canonical measure is the product
of Lebesgue measures for internal branching times, restricted by ancestor
ordering, and the canonical Brownian transition kernels. Leaves reach the
requested terminal time. Summing over the discrete topologies defines a
sigma-finite measure $\mu_{t,x,c}$.

Write $a(\theta)$ for the product of the scalar mechanism coefficients
and terminal code values of a completed tree $\theta$. Define the
nonnegative canonical tree mass by

\[
  \nu_{t,x,c}(d\theta)=|a(\theta)|\,\mu_{t,x,c}(d\theta).
\]

Each finite-depth part has finite canonical mass. Bounded arity gives only
finitely many topologies at that depth; only finitely many derivative
orders occur; those terminal derivatives are bounded on the compact range
of $v$; and each bounded time domain has finite volume.

For a completing proposal $Q$, the needed assertion is

\[
 |H(\theta)|\,Q(d\theta)=\nu_{t,x,c}(d\theta).
 \tag{1}
\]

For the usual density construction, this says $H=a/q$, where $q$ is
the actual joint sampling density relative to the canonical measure, with

\[
 q>0\quad\mu\text{-almost everywhere on }\{|a|>0\}.
\]

The measure identity (1) is the clearest formulation if the sampling
procedure uses extra randomization or changes its exploration order.
It includes all internal conditional clock densities, conditional tuple
probabilities and leaf survival probabilities. If proposals also change
the diffusion law, the corresponding likelihood correction would be
needed; changing that law is not covered merely by clock/tuple weights.

Under this contract, clock and tuple proposals may depend on any revealed
history. The proposal children need not be independent. One first cancels
the full likelihood, obtaining $\mu$, and only then uses independence
of the canonical Brownian child evolutions conditional on their common
birth position. This resolves the adaptive-sampling issue without a false
factorization of proposal expectations.

Let $E_N$ be the event that the completed tree has depth at most $N$.
Then

\[
 \mathbb E_Q[|H|\mathbf1_{E_N}]=\nu(E_N),\qquad
 \mathbb E_Q|H|=\lim_{N\to\infty}\nu(E_N).
 \tag{2}
\]

The second identity follows from almost-sure finite completion and monotone
convergence. Its two sides may be infinite. No exchange of a signed sum
with expectation is being made. A cutoff estimator that assigns artificial
terminal values to unfinished branches is a different random variable and
does not establish (2).

The scope excludes cancellations between different completed signed trees,
conditional expectations that integrate several signed alternatives inside
one sample, changed branch combiners, control variates, and continuation
with a changed terminal profile. Topological support alone also does not
give (1). These exclusions are material: without a fixed single-tree
functional and its exact likelihood ratio, the universal-proposal claim
would be false or undefined.

## 2. Canonical equations and restart

For $L=\tfrac12\Delta$, the reachable normalized labels and rules are

\[
\begin{aligned}
 I&\longrightarrow (F_0),\\
 D_i&\longrightarrow(F_1,D_i),\\
 F_k&\longrightarrow(F_0,F_{k+1})
       \quad\text{or}\quad(D_i,D_i,-\tfrac12 F_{k+2}).
\end{aligned}
\]

Their terminal values are $v,\partial_i v,f^{(k)}(v)$. Scalar code
multipliers propagate down exactly one derivative-code child, so absolute
normalization produces the coefficient $1/2$ in the gradient term.
Distinct code tags retain their prescribed mechanisms even when their
underlying functions happen to agree.

Write $g_I=|v|$, $g_{D_i}=|\partial_i v|$, and
$g_k=|f^{(k)}(v)|$. Decomposing finite trees at their root and applying
Tonelli to their nonnegative limits gives

\[
\begin{aligned}
 W_I(t)&=P_tg_I+\int_0^tP_{t-s}W_0(s)\,ds,\\
 W_{D_i}(t)&=P_tg_{D_i}
       +\int_0^tP_{t-s}(W_1W_{D_i})(s)\,ds,\\
 W_k(t)&=P_tg_k+\int_0^tP_{t-s}
       \left(W_0W_{k+1}+\tfrac12\sum_iW_{D_i}^2W_{k+2}\right)(s)\,ds.
\end{aligned}
\tag{3}
\]

These are identities of extended nonnegative integrals. A branch with a
finite-tree zero factor contributes zero termwise; it is never evaluated
by an undefined real-arithmetic product $0\cdot\infty$.

For a generic equation $W(t)=P_tg+\int_0^tP_{t-r}N(r)dr$, split the
integral at $t_0$, use the semigroup law and Tonelli, and obtain

\[
 W(t_0+s)=P_sW(t_0)
        +\int_0^sP_{s-r}N(t_0+r)\,dr.
 \tag{4}
\]

This is valid even when $W(t_0)$ is infinite. It supplies the restart used
in T10 without differentiating an infinite field or subtracting infinities.
The equations depend on finite-tree combinatorics and the heat kernel,
not on existence of a solution of the signed semilinear PDE.

## 3. The lower chain, explosion bound and Id propagation

Suppose $f(v)\not\equiv0$ and $f^{(p)}(v)\not\equiv0$ for one finite
$p\ge2$. On a compact connected flat torus, strictly positive heat
kernels send each continuous nonnegative nonzero function to a continuous
strictly positive function. Therefore, for every $t_0>0$,

\[
 \eta_0=\min_xP_{t_0}g_0(x)>0,
 \qquad \eta_p=\min_xP_{t_0}g_p(x)>0.
\]

Both minima are finite. Compactness is used for their uniform positivity;
connectedness prevents isolated components with no seed. This step is
valid even when $f(v)$ and $f^{(p)}(v)$ never have overlapping nonzero
sets before heat smoothing.

The terminal part of (3) and $P_s1=1$ yield
$W_p(t_0+s,x)\ge\eta_p$. Equation (4), after dropping other nonnegative
terms, dominates the constant finite chain

\[
 A_k'=A_0A_{k+1}\quad(0\le k<p),\qquad A_p=\eta_p,
 \quad A_0(0)=\eta_0,\quad A_k(0)=0\ (1\le k<p).
\]

One can compare its nonnegative Picard iterates with (4), starting with the
stated initial constants. Every iterate is bounded above by the actual
extended fields. Before explosion, finite-dimensional local uniqueness and
monotone Picard convergence identify their limit with the finite ODE
solution. There is no need for a uniqueness theorem for the infinite
hierarchy, nor for a bound uniform over all derivatives of $f$.

With $Z'=A_0$, $Z(0)=0$, successive integrations give

\[
 A_k=\frac{\eta_p}{(p-k)!}Z^{p-k}\quad(1\le k\le p),
 \qquad A_0=\eta_0+\frac{\eta_p}{p!}Z^p.
\]

The separation time is

\[
 \tau_* =\int_0^\infty\frac{dz}{\eta_0+(\eta_p/p!)z^p}
 \le \frac{p}{p-1}\eta_0^{-(p-1)/p}
             (p!/\eta_p)^{1/p}=:B_p<\infty.
\]

Splitting at $R_0=(\eta_0p!/\eta_p)^{1/p}$ proves the displayed bound.
The solution has $Z(s)\to\infty$ as $s\uparrow\tau_*$. It is this
integrated divergence, rather than just $A_0(s)\to\infty$, that is
needed for the root.

Indeed, for any $T\ge t_0+B_p$, any $s<\tau_*$, and any $x$, (3)
and preservation of constants imply

\[
 W_I(T,x)\ge
   \int_{t_0}^{t_0+s}P_{T-r}W_0(r)(x)\,dr
   \ge\int_0^sA_0(r)\,dr=Z(s).
\]

Letting $s\uparrow\tau_*$ proves the claimed infinite first absolute
Id moment, uniformly in $x$, for all the stated later horizons. This
also proves infinite second moments. It says nothing about the earliest
failure time, tree noncompletion, or blowup of the signed PDE.

**Audit result:** the finite lower chain, explicit constant, restart,
comparison, and propagation to the Id root all pass.

## 4. A full smooth classification from terminal jets

The sufficient obstruction already gives necessity in the following
stronger characterization. Under the same fixed-tree proposal contract,
for smooth $f$ on a neighborhood of the compact range of smooth $v$,

\[
\boxed{
 \bigl[W_I(t,x)<\infty\text{ for every finite }t\ge0\text{ and every }x\bigr]
 \iff
 \bigl[f(v)\equiv0\bigr]
 \quad\text{or}\quad
 \bigl[f^{(p)}(v)\equiv0\text{ for every }p\ge2\bigr].
}
\tag{5}
\]

The expectation is the same for every supported completing proposal, so
the left side can equivalently quantify over one or all such proposal
families. The class is nonempty: a fixed positive exponential clock and
positive probabilities on the finitely many raw tuples have bounded
offspring arity and finite trees almost surely at each finite horizon.

### Sufficiency when all higher terminal jets vanish

Start at a code $F_k$, $k\ge2$. At each internal vertex, choose its
higher-derivative child: $F_{k+1}$ in a reaction tuple or $F_{k+2}$ in
a gradient tuple. In a finite tree this path reaches a terminal
higher-derivative code, whose value is zero. Thus every such finite tree
has zero weight. This proves $W_k=0$ for all $k\ge2$ without an
infinite-system uniqueness claim.

Because the continuous image $v(X)$ is an interval, there are two cases.
If $v$ is nonconstant, $f''=0$ on that interval implies
$f(y)=a+by$ there; in particular $f'(v)=b$ is constant. If $v\equiv r$,
put $b=f'(r)$ and $a=f(r)-br$. In either case (3) reduces to

\[
 W_1=|b|,\qquad W_0(t)=e^{|b|t}P_t|f(v)|,
\]

and hence

\[
 W_I(t)=P_t|v|+L_b(t)P_t|f(v)|,
 \qquad
 L_b(t)=
 \begin{cases}
 (e^{|b|t}-1)/|b|,&b\ne0,\\
 t,&b=0.
 \end{cases}
\tag{6}
\]

This is finite at every finite horizon. Neither global affinity of $f$
nor analyticity was used.

### Sufficiency when the terminal reaction vanishes

If $v\equiv r$ and $f(r)=0$, every derivative-code subtree $D_i$
has a zero $D_i$ leaf. A finite $F_0$ tree either follows an $F_0$
child at every reaction vertex to an $F_0$ leaf, or encounters a gradient
tuple with such a zero derivative subtree. Its weight is zero. Therefore
$W_I(t,x)=|r|$ for every $t$.

If $v$ is nonconstant and $f(v)\equiv0$, its range is a nondegenerate
closed interval $[m,M]$ on which $f=0$. All derivatives vanish on its
interior and, by continuity, at its endpoints. Thus all terminal reaction
jets vanish, and (6) gives $W_I=P_t|v|$. In particular, a nonconstant
profile taking values in a smooth zero plateau is an additional smooth
exception to a claim based only on global non-affinity of $f$.

### Necessity and useful restatements

If both alternatives in (5) fail, then $f(v)\not\equiv0$, and at least
one finite $p\ge2$ satisfies $f^{(p)}(v)\not\equiv0$. Section 3 then
forces failure at a finite horizon. This proves necessity and completes
the characterization.

For **nonconstant $v$**, (5) is equivalent simply to

\[
 f\text{ is affine on }v(X)=[\min v,\max v].
\]

For **constant $v\equiv r$**, (5) is equivalent to

\[
 f(r)=0\quad\text{or}\quad f^{(p)}(r)=0\text{ for every }p\ge2.
\]

The latter is an affine *formal Taylor jet*, not a claim that $f$ agrees
with an affine function near $r$. This distinction is precisely where
arbitrary smooth functions can defeat PDE correspondence.

## 5. Analytic corollary and converse edge cases

Let $f$ be real analytic on a connected open interval $J$ containing
the range of $v$. If $v$ is nonconstant and $f$ is non-affine on
$J$, neither $f$ nor $f''$ can vanish on the whole range interval.
Otherwise the analytic identity theorem would make $f$ zero or affine
on $J$. Thus $p=2$ is enough in Section 3.

If $v\equiv r$, $f(r)\ne0$, and all derivatives of order at least two
vanished at $r$, analyticity would make $f$ affine near $r$, then on
all of $J$. A non-affine analytic reaction therefore has some finite
nonzero higher derivative at every non-root terminal constant.

Consequently the all-horizon analytic equivalence in `04c` is correct:

\[
 W_I(t,x)<\infty\text{ for all finite }t,x
 \iff f\text{ is affine on }J
          \text{ or }v\text{ is a constant reaction root}.
\]

The following edge cases are included:

- The zero reaction and every constant reaction are affine; (6) includes
  $b=0$ without division by zero.
- If a non-affine analytic $f$ has several roots, a continuous
  nonconstant $v$ cannot range only among those roots on a connected
  torus. A nondegenerate root interval would instead force $f\equiv0$.
- A constant root may be nonzero. Its absolute Id moment is $|r|$,
  not zero.
- Vanishing $f''(r)$ at a non-root constant does not rescue integrability;
  a later finite nonzero derivative supplies the lower chain.
- Behavior of a merely smooth $f$ outside $v(X)$ does not determine
  the canonical tree mass. Analytic continuation is what links that mass
  to affinity on all of $J$.
- No positive local interval of integrability is asserted for arbitrary
  infinite terminal jets. The exact constant-profile result below shows
  how radius zero can give failure at every positive time.

## 6. PDE correspondence is a separate statement

The flat example in T10 is decisive. For

\[
 f(y)=1+e^{-1/y^2}\ (y\ne0),\quad f(0)=1,\quad v\equiv0,
\]

every higher terminal reaction jet is zero. The canonical signed and
absolute Id expectations equal $t$. The true spatially constant solution
satisfies $u'=f(u)$, $u(0)=0$, and is strictly larger than $t$ for every
$t>0$. Smoothness and even all-horizon absolute integrability therefore
do not establish correspondence. The ordinary scalar ODE is well posed;
the defect is in identifying the infinite code hierarchy with its physical
solution without a suitable uniqueness/growth class.

The original fully nonlinear paper uses equation (2.7) for the mechanism,
Definition 4.1 for the weighted functional, and Theorem 4.2 for the
representation. That theorem requires absolute integrability for every
code and separately uniqueness of the code system. These are stronger
requirements than the single Id moment conclusion at one horizon.
The torus result is a deduction from the mechanism and heat semigroup,
not a theorem being attributed to the paper.
[Nguwi–Penent–Privault, arXiv v3](https://arxiv.org/html/2201.03882).

No global existence or uniqueness result for an arbitrary semilinear PDE
has been proved in D10. Conversely, a globally existing signed solution
does not prevent raw absolute-moment failure: both the sine example and
the rational example in Section 7 exhibit this separation.

## 7. Bounded review of the exact constant-profile horizon

For $v\equiv r$, set $a_k=|f^{(k)}(r)|$ and

\[
 \Phi(z)=\sum_{k\ge0}\frac{a_k}{k!}z^k,
 \qquad R\in[0,\infty]
\]

for the nonnegative convergence radius. First separate $a_0=0$, for
which the finite-tree zero argument gives $W_I=|r|$ at every time.
Assume below that $a_0>0$.

**The theorem in `04d` is correct:** with

\[
 \tau=\int_0^R\frac{dz}{\Phi(z)},
\]

and with the radius-zero integral interpreted as zero,

\[
\begin{aligned}
 W_I(t)&=|r|+Z(t),
 &\int_0^{Z(t)}\frac{dz}{\Phi(z)}&=t
 &&(0\le t<\tau),\\
 W_I(\tau)&=|r|+R
 &&&& (\tau<\infty),\\
 W_I(t)&=\infty
 &&&& (t>\tau).
\end{aligned}
\tag{7}
\]

Here $R=\infty$ makes the critical value infinite. When $R<\infty$,
the Id moment is finite at the endpoint even if reaction moments there
are infinite.

The steps that could have failed are resolved as follows.

**Terminal-jet truncation really is monotone.** Set $a_k^{[n]}=a_k$ for
$k\le n$ and zero otherwise. For each completed tree its absolute
terminal product increases with $n$, eventually becoming the original
product. A code with index above $n$ has a derivative-descendant path to
a zero leaf. Gradient trees are zero for constant data. Thus the truncated
system is the finite chain in `04d`, not an uncontrolled truncation of an
infinite ODE solution.

**The finite reduction has the claimed normalization.** For
$\Phi_n(z)=\sum_{k=0}^na_kz^k/k!$, the finite solution before explosion is

\[
 Z_n'=\Phi_n(Z_n),\qquad
 V_k=\Phi_n^{(k)}(Z_n),\qquad W_{I,n}=|r|+Z_n.
\]

Initial values are exactly $V_k(0)=a_k$, and differentiation gives
$V_k'=V_0V_{k+1}$. Finite Picard iteration identifies these fields with
the truncated nonnegative tree sums. When a superlinear coefficient is
present, $Z_n\to\infty$ at its finite separation time, so the **Id**
tree mass is infinite at and after that time. The top retained field
$V_n=a_n$ need not diverge.

**The separation times converge to the claimed integral.** Once
$\Phi_{n_0}$ has a positive coefficient of degree at least two,
$1/\Phi_{n_0}$ is integrable on $[0,\infty)$. For $n\ge n_0$,

\[
 0\le1/\Phi_n\le1/\Phi_{n_0},
\]

and the pointwise limit away from the possible single boundary point is
$1/\Phi$ on $z<R$ and zero on $z>R$. Dominated convergence gives
$\tau_n\downarrow\tau$, including $R=0$. If there is no superlinear
coefficient, the affine solution is global and no dominating reciprocal
argument is needed.

**The subcritical inverse is identified without infinite uniqueness.**
For $z<R$, let
$F_n(z)=\int_0^z1/\Phi_n$ and $F(z)=\int_0^z1/\Phi$.
Then $F_n(z)\downarrow F(z)$. For $t<\tau$, choose $z$ on either
side of the unique $Z$ with $F(Z)=t$. The inequalities
$F_n(z)>t$ or eventually $F_n(z)<t$ squeeze
$Z_n(t)\uparrow Z(t)$. Treewise monotone convergence therefore gives
the first line of (7). For $t>\tau$, some finite $\tau_n<t$, proving
infinite Id mass there.

**The endpoint argument is essential and valid.** A nonzero fixed
constant-profile tree with $m$ internal vertices has canonical mass
$c_\theta t^m$, $c_\theta\ge0$. Rescale its ancestor-ordered time
domain from $[0,t]$ to $[0,1]$; there are $m$ time integrations and
all Brownian integrals are one. There are only finitely many nonzero
shapes and labels at each $m$. Hence

\[
 W_I(t)-|r|=\sum_{m\ge1}b_mt^m,\qquad b_m\ge0.
\]

For $0<\tau<\infty$, monotone convergence as $t\uparrow\tau$ gives
the value of this series at $\tau$, not only a left limit of a
separately defined function. That value is $R$. The case $\tau=0$
is handled directly by the original terminal value. This validates the
second line of (7) even when $W_0(\tau)=\infty$.

### Examples checked algebraically

- For $f(y)=\sin y$, $r=\pi/2$, $\Phi(z)=\cosh z$, $R=\infty$,
  $\tau=\pi/2$, and $Z=\log(\sec t+\tan t)$. The Id mass diverges at
  the endpoint. This agrees with the $A'=AB, B'=A^2$ calculation in T10.
- For $f(y)=1/(1+y^2)$, $r=0$, the even jets have absolute values
  $(2j)!$ and the odd jets vanish. Thus
  $\Phi(z)=(1-z^2)^{-1}$, $R=1$, and
  $\tau=\int_0^1(1-z^2)dz=2/3$. Consequently $W_I(2/3)=1$, while
  $W_I(t)=\infty$ for $t>2/3$. The signed ODE satisfies
  $u+u^3/3=t$ and is global. This is a counterexample to a universal
  claim that the critical Id moment must itself be infinite.
- The flat example has $\Phi=1$ and $\tau=\infty$, in agreement
  with the smooth classification and its failure of PDE correspondence.

These are exact algebraic checks, not numerical evidence. The endpoint
phenomenon does not contradict D10: its stated bound is a sufficient later
failure horizon, not a sharp identification of the critical time.

## 8. Source correspondence, remaining boundaries and disposition

The zero-spatial-index reaction tuple in the binary mechanism of Huang
and Privault is the same coefficient-one pair $F_0,F_{j+1}$. It also
retains $I\to F_0$. Discarding its other nonnegative absolute terms
therefore gives the same lower chain on the periodic version of that
representation, under the corresponding likelihood contract. This is a
direct structural inference, not a claim that their theorem states D10.
[Huang–Privault, Definition 2.2](https://arxiv.org/html/2502.17853v2).

Penent and Privault already give the scalar derivative chain in Section 2,
the weighted functional and integrability discussion in Section 4, and
the correspondence to Butcher trees in Section 6. They also discuss
patching. These ingredients cannot be claimed novel here.
[Penent–Privault, arXiv v2](https://arxiv.org/pdf/2201.05998).

One source caution matters: the proof of its Theorem 4.2 invokes uniqueness
in $\ell^\infty$. A use of that argument must put the actual physical
code family in the asserted uniqueness class. The flat-jet example shows
why bounds on the estimator alone cannot establish this identification
for arbitrary smooth $f$. Neither D10 nor the proof of (7) relies on
that inference. They construct minimal positive tree masses directly.

This was a bounded source comparison, not a comprehensive novelty search.
Publication priority of the terminal-jet classification or the sharp
constant-profile endpoint statement remains unestablished.

The audited results rely on standard but unformalized inputs: measurable
finite-tree constructions, the joint likelihood identity, monotone
convergence and Tonelli, heat-kernel positivity and continuity, finite
polynomial ODE theory, and the real-analytic identity theorem. Their
quantifiers and uses are now explicit. No claim is made for arbitrary
fully nonlinear spatial-jet reactions, noncompact space, regrouped tree
representations, finite variance in the integrable cases, or global PDE
existence.

**Disposition:** retain D10; incorporate the precise finite-depth and
likelihood contract; promote (5) as a conventional smooth strengthening;
and mark `04d` conventionally reviewed after the Id-only wording correction.
Lean coverage remains whatever its checked declarations actually encode;
this audit supplies no new formal coverage.

## Audited input fingerprints

These SHA-256 values identify the versions read before parent integration.
Later editorial integration may legitimately change them.

```text
48bca0fa2bde2e4a7a2b07e1123b9235168420a88417aef069e18e975f59df5b  04c-general-obstruction.md
68f815906ca934e2b90e94b44c107272c81a69e163d44d17aebcb325dbbad7c7  04d-sharp-constant-horizon.md
d7e39ca18dc5776097ee89b3bed2119be14e32877871d12e1df7172558677b11  reviews/T10-polynomial-obstruction.md
```
