# T31 — limiting-clock rejection and scaled-defect audit

**Verdict: pass for the exact ideal rejection sampler and all stated
constants.** The finite-horizon conditional clock law is correct, rejection
trials have the claimed uniform expected total, the rearranged inverse has
the stated domain, and the scaled coefficient substitution has the claimed
one-sided error bounds. This is the same ideal tree law as the audited
two-barrier Allen–Cahn construction.

The formulas are not an exact finite-bit implementation or a complete
floating-point bias certificate. In particular, the current bounded-measurable
data class admits a concrete obstruction to any blanket guarantee for
finite-bit spatial queries. That limitation does not affect the ideal theorem.

Audited source:
[04m-horizon-free-clock-proposal.md](../04m-horizon-free-clock-proposal.md),
91 lines, SHA-256
1f159f13b6f380915d4e3c3aa83e028dccf1e7bf5298ae963cc00006ed32cca7.
Context: [04l-two-barrier-voting.md](../04l-two-barrier-voting.md),
SHA-256 74e9dcfa4788a5830e303fc77f32d4d1f07da4dcf267c5664b63e8eb0f6e12f1,
and [T30](T30-two-barrier-voting-audit.md).
No source file, frozen review, implementation, Lean file, or numerical result
was changed or produced. This is a mathematical audit, with bounded
recommendations for a later numerical contract.

## 1. Assumptions and the limiting proposal

This explicit specialization assumes

$$
f(u)=u-u^3,\qquad 0<m<M<1,\qquad m\leq v\leq M,
$$

and a finite nonnegative remaining time $T$. Put

$$
A=m^{-2}-1,\quad B=M^{-2}-1,\quad z_0=m/M,\quad
z(t)=\sqrt{\frac{1+B e^{-2t}}{1+A e^{-2t}}},\quad
R(z)=\frac{z^2}{1+z}.
$$

Then $A>B>0$, $z_0\leq z(t)<1$, and $z(t)\uparrow1$. The previously
audited relation is

$$
\lambda(t)=\frac{d}{dt}\log R(z(t)),\qquad
\Lambda(t)=\log\frac{R(z(t))}{R(z_0)},\qquad
\Lambda_\infty=\log\frac{1}{2R(z_0)}<\infty.
$$

The proposal space is a separate leaf symbol together with event times
$s\in(0,\infty)$. Define the proposal probability measure $\Pi$ by

$$
\Pi(\{\mathrm{leaf}\})=e^{-\Lambda_\infty}=2R(z_0),\qquad
\Pi(ds)=\lambda(s)e^{-(\Lambda_\infty-\Lambda(s))}\,ds.
$$

It is normalized because the integral of the density is
$1-e^{-\Lambda_\infty}$. In particular the leaf atom is indispensable:
there is no event density alone with unit mass.
Its cumulative probability including the leaf is

$$
\Pi(\{\mathrm{leaf}\}\cup(0,s])
=e^{-(\Lambda_\infty-\Lambda(s))}
=2R(z(s)).
$$

No Brownian motion over an infinite physical edge is part of this auxiliary
law.

## 2. Exact conditioning and finite-horizon clock law

At remaining time $T$, accept the set
$E_T=\{\mathrm{leaf}\}\cup(0,T)$, and independently repeat proposals until
one is accepted. Its probability is

$$
\alpha(T)=\Pi(E_T)
=e^{-(\Lambda_\infty-\Lambda(T))}
=2R(z(T))\geq 2R(z_0)=:\alpha_0>0.
$$

The usual geometric-series calculation gives, for every measurable accepted
set $D$,

$$
\mathbb P(\text{accepted proposal}\in D)
=\sum_{k\geq1}(1-\alpha(T))^{k-1}\Pi(D\cap E_T)
=\frac{\Pi(D\cap E_T)}{\alpha(T)}.
$$

Consequently the accepted leaf probability and event density are exactly

$$
\mathbb P_T(\mathrm{leaf})=e^{-\Lambda(T)},\qquad
\mathbb P_T(ds)
=\lambda(s)e^{-(\Lambda(T)-\Lambda(s))}\,ds,\quad 0<s<T.
$$

These are the finite-horizon first-event law used in 04l. At $T=0$, only
the leaf is accepted; its conditional probability is one. At a finite
positive $T$, $s=T$ is a null event in the ideal continuous proposal, so the
strict acceptance convention is harmless. It is not a null-event argument
for an already discretized random source.

The accepted event's remaining time, mixture parameter, Brownian edge, and
independent children are consequently distributed exactly as before.
Rejected proposals create neither children nor spatial increments. No
likelihood reweighting of the completed return is needed.

## 3. Proposal counts on the random tree

For a node at time $T$, the number $K_T$ of proposals until acceptance is
geometric on $\{1,2,\ldots\}$:

$$
\mathbb E K_T=\alpha(T)^{-1}\leq\alpha_0^{-1}.
$$

Multiplication by the expected random node count requires a conditional
argument, not an assumption that node counts and proposal counts are
independent.

Index potential vertices by finite words in $\{1,2,3\}$, with an unused
third child absent at a binary event. For a potential vertex $v$, let
$I_v$ indicate that it is visited and let $T_v$ be its remaining time.
Its activation and time are determined by the ancestral history. Give each
vertex a fresh independent proposal stream. Conditional on that history,

$$
\mathbb E[I_v K_{T_v}\mid\text{ancestral history}]
=\frac{I_v}{\alpha(T_v)}
\leq\frac{I_v}{\alpha_0}.
$$

All summands are nonnegative. Tonelli, or first summing through a finite
generation and then taking a monotone limit, proves

$$
\mathbb E\!\left[\sum_{\text{visited }v}K_{T_v}\right]
\leq \alpha_0^{-1}\mathbb E N_{\rm all}.
$$

The accepted tree has the previously audited law and finite node expectation.
Each local rejection loop completes almost surely, and the displayed
finite total expectation also proves completion of the augmented algorithm.
There is no hidden factor from repeated work in rejected subtrees, since
none are generated. This counts uniform proposals; it does not charge their
real-arithmetic evaluation cost.

For $m=1/2$, $M=3/4$, $z_0=2/3$, so

$$
\alpha_0=\frac{8}{15},\qquad
\sup_T\mathbb E K_T=\frac{15}{8},\qquad
\mathbb E N_{\rm all}
\leq\frac{25\sqrt6}{16}-1.
$$

Thus the total proposal bound is exactly

$$
\mathbb E N_{\rm proposals}
\leq\frac{15}{8}\left(\frac{25\sqrt6}{16}-1\right).
$$

The node expression is an upper bound from $N_{\rm all}\leq2L-1$, not the
exact mean node count of the mixed-arity process. The new rejection procedure
preserves that node law; it adds clock proposals rather than improving the
mathematical node count.

## 4. Uniform inverse, rearranged numerator, and domain

Draw an ideal $U\in(0,1)$. If $U\leq2R(z_0)$, propose a leaf. Otherwise put

$$
y=U/2,\qquad
\zeta=\frac{y+\sqrt{y^2+4y}}2.
$$

The function $R$ is strictly increasing on $(0,1)$, and the positive
quadratic root solves $\zeta^2=y(1+\zeta)$, or $R(\zeta)=y$.
The event branch therefore has
$z_0<\zeta<1$. By the cumulative formula in section 1 this is exactly the
inverse of the limiting proposal, provided $\zeta$ is converted to its
physical event time.

The source identity is correct:

$$
(1-\zeta)(1+\zeta-y)
=1-\zeta^2-y+y\zeta
=1-2y=1-U.
$$

Multiplying by $1+\zeta$ gives

$$
d=\frac{(1-U)(1+\zeta)}{1+\zeta-y}=1-\zeta^2.
$$

All factors in the fraction's denominator are in a safe mathematical domain:
$y<1/2$ and $\zeta>0$ imply $1+\zeta-y>1/2$.
Inverting
$\zeta^2=(1+Bq)/(1+Aq)$ then gives

$$
q_{\rm event}
=\frac{d}{A-B-Ad}
=\frac{1-\zeta^2}{A\zeta^2-B}.
$$

The denominator is bounded below as claimed:

$$
A\zeta^2-B>A z_0^2-B=1-z_0^2>0.
$$

Also $0<d<1-z_0^2$, and

$$
A\zeta^2-B-(1-\zeta^2)
=(A+1)\zeta^2-(B+1)>0
$$

because $\zeta>m/M$. Hence $0<q_{\rm event}<1$ and
$s=-\tfrac12\log q_{\rm event}$ is finite and positive.
As $U$ increases from the leaf threshold to one, $s$ increases from zero
to infinity. After rejection enforces $s<T$, the accepted Brownian edge
variance $T-s$ is strictly positive; a leaf uses variance $T$.

The mixture formula is unchanged and valid:

$$
p(\zeta)=\frac{3(1+\zeta)}{2(2+\zeta)}.
$$

For the fixed phase it lies strictly between $15/16$ and one at an event.
The constants $A=3$, $B=7/9$, $A-B=20/9$, and
$A\zeta^2-B>5/9$ also check out.

The rearrangement avoids evaluating $1-\zeta^2$ by subtracting two close
numbers. It does not make every operation well-conditioned uniformly over
all phase parameters or random inputs. The denominator may become small
when $m/M$ approaches one, and the input inverse has increasing sensitivity
as $U$ approaches one. For the fixed phase,

$$
q_{\rm event}\sim \frac35(1-U),\qquad
s\sim-\frac12\log\!\left(\frac35(1-U)\right)
\quad(U\uparrow1).
$$

Finite precision that rounds $U$ to one still produces a zero logarithm
argument. Near the leaf threshold, $q_{\rm event}$ is close to one, so
computing a very small positive event time has its own rounding issue.
The exact positivity proof is not permission to silently clip an out-of-domain
floating result without accounting for the law change.

## 5. Scaled defect and the coefficient-only limit error

For $c\in(0,1)$, let $A_c=c^{-2}-1$ and $q=e^{-2T}>0$. The scalar solution
is $\ell_c(T)=(1+A_cq)^{-1/2}$. Rationalizing its positive defect yields

$$
R_c(T):=e^{2T}(1-\ell_c(T))
=\frac{A_c}{\sqrt{1+A_cq}\,[1+\sqrt{1+A_cq}]}.
$$

Thus, for exactly the same bounded tree return $Z$ as before,

$$
W=R_M(T)Z+R_m(T)(1-Z),\qquad
\mathbb E W=e^{2T}(1-u(T,x)).
$$

The convex-combination form avoids subtracting the PDE value from one.
The function $R_c(T)$ increases from $1-c$ to $A_c/2$ as $T$ increases.
Since $m<M$ implies $R_m(T)>R_M(T)$, for the fixed phase

$$
\frac14\leq W\leq\frac32.
$$

The lower bound is attained by the upper constant datum at time zero; the
upper bound is a valid closed bound even though the scalar lower-barrier
coefficient approaches $3/2$ only as $T\to\infty$.

To check the proposed limit substitution, write
$F_A(q)=A/(x+\sqrt x)$ with $x=1+Aq\geq1$. Then

$$
-F_A'(q)
=\frac{A^2(1+1/(2\sqrt x))}{(x+\sqrt x)^2}
\leq\frac{3A^2}{8}.
$$

Integration from zero to $q$ gives exactly

$$
0\leq A_c/2-R_c(T)\leq\frac{3A_c^2q}{8}.
$$

Couple the original and substituted output using the same exact $Z$ at the
same finite horizon, and put
$W_0=(A_M/2)Z+(A_m/2)(1-Z)$. Then

$$
0\leq W_0-W
\leq\max\left(\frac{3A_M^2q}{8},\frac{3A_m^2q}{8}\right)
=\frac{27q}{8}.
$$

The mean bias is one-sided, and since $\mathbb EW\geq1/4$,

$$
0\leq\frac{\mathbb EW_0-\mathbb EW}{\mathbb EW}
\leq\frac{27q}{2}.
$$

This proof is specific to replacing the two root coefficients by their
$q=0$ limits while leaving the tree return unchanged. The rejection clock
indeed avoids using the root quantity $e^{-2T}$ or $z(T)$, so that coupling
is available. It does not replace $q_{\rm event}$ by zero at a proposed
event; that would change event times and the tree.

If an underflow policy is triggered only when the true $q\leq\eta$ for a
specified positive threshold, these bounds become the deterministic
absolute and relative certificates $27\eta/8$ and $27\eta/2$ for this
substitution alone. A floating exponent routine must supply the premise;
underflow modes and subnormal handling cannot be inferred from the identity.

If the physical multiplier is itself replaced by zero, returning
$\widehat q\,W_0=0$ for a positive physical defect has relative error one.
The small coefficient-substitution bound does not apply to that output.
Reporting the scaled mean, or a logarithmic representation retaining
$-2T$, avoids this separate underflow. Taking the logarithm of a sample mean
is a plug-in estimate; unbiasedness of $W$ does not imply an unbiased
log-defect estimator.

## 6. A concrete finite-bit limitation for measurable data

Suppose a floating implementation queries the initial profile only at points
in a countable set $S$ of representable coordinates. On the flat torus take

$$
v(x)=
\begin{cases}
M,&x\in S,\\
m,&x\notin S.
\end{cases}
$$

This is bounded and measurable and satisfies the ideal theorem's data
hypothesis. Every exact positive-time Brownian marginal has a density and
avoids $S$ almost surely. Conditional on the ideal clock tree, each leaf
has total physical Brownian elapsed time $T>0$ along its lineage, and the
finite collection of leaves therefore all evaluate to $m$ almost surely.
The ideal normalized leaf values are zero, the OR/majority votes preserve
zero, and $W=R_m(T)$ almost surely. Equivalently $v=m$ almost everywhere,
so the ideal positive-time PDE solution is $\ell_m(T)$.

Every finite-bit query of this same datum returns $M$. The floating leaf
values are then one, the votes preserve one, and the corresponding output
is the upper-barrier coefficient $R_M(T)$, even with perfectly evaluated
clock identities and root coefficients. The discrepancy is substantive.
Taking the union of representable coordinate sets over a sequence of finite
precisions still gives a countable $S$, so increasing precision alone does
not repair this example for the full measurable-data class.

This example is not a defect in rejection sampling. It shows that exact
transition/data oracles or additional regularity and numerical contracts on
the chosen profile are necessary for a full floating-bias claim. Clock
distribution checks alone cannot supply them.

## 7. Bounded recommendations for a later numerical contract

These are recommended requirements, not an executed or separately frozen
experiment protocol.

- Keep the first floating study at the fixed phase $[1/2,3/4]$, specify the
  uniform-bit convention, precision, exponent/underflow mode, inverse
  evaluations, and handling of $s<T$ and $T-s$. State explicitly that it
  approximates the ideal law. Report any guards or clipping as algorithmic
  changes rather than treating them as consequences of the exact proof.
- Use a fixed smooth initial-profile oracle. The root's proposed
  $v(x)=5/8+(1/8)\cos x$ on the $2\pi$ torus has the exact range
  $[1/2,3/4]$ and Lipschitz bound $1/8$. Constant profiles at both endpoints
  also provide exact barrier checks. The counterexample in section 6 means
  these tests must not be described as validating all bounded measurable
  data.
- Separate deterministic algebra/domain checks from statistical PDE checks.
  The deterministic identities are $R(\zeta)=U/2$,
  $d=1-\zeta^2$, the inverse ratio for $q_{\rm event}$, and the reconstructed
  $z(s)=\zeta$. Their near-endpoint comparison needs a higher-precision
  reference and absolute as well as relative errors. Include inputs near the
  leaf threshold and near one; a value that rounds to one in the working
  precision is an expected domain limitation, not an exact event sample.
  No evaluation of $z(T)$ is needed in the production rejection procedure;
  its high-precision value can still be used for validation of the conditional
  leaf probability and clock cumulative distribution.
- Compare the scaled mean directly with an independent deterministic scaled
  reference, not a reference obtained by subtracting a computed $u$ from one.
  If $D(T,x)=e^{2T}(1-u(T,x))$, its exact equation is
  $D_t=\tfrac12 D_{xx}+3e^{-2T}D^2-e^{-4T}D^3$ and
  $D(0,x)=1-v(x)$. Reference discretization error and Monte Carlo uncertainty
  require separate reported budgets. The exact output range and the proved
  node/proposal expectations provide diagnostics, not guarantees that a
  finite sample average of counts must lie below its expectation bound.
- If coefficient limiting is used, fix its trigger $\eta$ in advance and
  report the two explicit substitution budgets $27\eta/8$ and $27\eta/2$.
  Keep this term separate from uniform discretization, comparison decisions,
  square-root/log errors, mixture/vote arithmetic, Gaussian sampling,
  profile evaluation, and reference error. Do not describe the one term as
  a certificate for total numerical bias.

No full rounding theorem, exact finite-bit sampler, or horizon-uniform bit
complexity follows from this audit. The exact ideal rejection construction
does pass and is ready to be integrated with the already reviewed
two-barrier theorem, subject to the separate formal/numerical gates set by
the root task.
