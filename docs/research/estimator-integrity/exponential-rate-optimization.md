# Exponential branching-clock rate optimization

**Mathematical status:** proved theorem for the local objective and the
finite-topology kernels; proved conditional theorem for the unrestricted
moment under the stated topology-disintegration and properness hypotheses;
analytic control for the binary Riccati model.

**Implementation status (16 September 2026):**
[`rate_optimization.py`](../../../parabolab/rate_optimization.py) propagates
first and second rate derivatives through the finite-depth child recursion
with the tuple proposal held fixed. The local frozen-continuation objective
below is not substituted for those recursive derivatives. Separate exact
rational verifiers now bound full-tree objective excess for the saved flat,
wave-root and five-point profile Allen–Cahn benchmarks; see the
[certificate checkpoint](../results/certified-rate-checkpoint.md) and
[profile checkpoint](../results/profile-efficiency-checkpoint.md). The
[mean-identification theorem](allen-cahn-mean-identification.md) justifies
their variance interpretation. These are benchmark-specific certificates,
not a general error guarantee for finite-depth quadrature or a universal
optimal-rate formula. Lean covers the explicitly listed algebraic and
order substatements in the [proof registry](../proof-registry.md).

This note studies the rate \(\lambda>0\) of the exponential lifetime law

\[
\rho_\lambda(s)=\lambda e^{-\lambda s},
\qquad
\bar F_\lambda(s)=e^{-\lambda s}.
\tag{7.1}
\]

The underlying coding-tree model, killed-depth convention, and exact
extended-valued moment identity are those of
[the common notation and moment theorem](notation-and-moment-theorem.md).
The distinction between an unrestricted first-event proposal and the
one-parameter exponential family is explained in
[the adaptive-proposal note](adaptive-proposals.md#why-this-is-not-exponential-rate-optimization).

All results below concern the second moment. Exact likelihood ratios make the
represented mean independent of \(\lambda\), whenever that mean exists.
Consequently minimizing a finite second moment also minimizes the variance.
This does not mean that a multiplicative ratio of second moments is the same
ratio of centered variances.

## The local single-event objective

Fix a remaining horizon

\[
\Delta:=T-t>0.
\tag{7.2}
\]

Let \(A_0>0\), let \(A\in L^1(0,\Delta)\) satisfy \(A(s)\geq0\) almost
everywhere, and assume

\[
B:=\int_0^\Delta A(s)\,ds>0.
\tag{7.3}
\]

Here \(A_0\) is the rate-independent leaf second-moment contribution and
\(A(s)\) is the rate-independent continuation contribution conditional on a
first branch at time \(s\). Restricting the first-event law to (7.1) gives

\[
\boxed{
J_{\exp}(\lambda)
=A_0e^{\lambda\Delta}
+\frac1\lambda\int_0^\Delta A(s)e^{\lambda s}\,ds,
\qquad \lambda>0.
}
\tag{7.4}
\]

This is a local, frozen-continuation objective. In a recursive tree the child
moments also depend on \(\lambda\); the full-tree argument later in this note
does not freeze them.

### Where the local coefficients come from

Let \(g_c=c(u)(T,\cdot)\) be the terminal factor for root code \(c\), and
let \(P_s\) be the reference diffusion semigroup. The leaf coefficient is

\[
A_{0,c}=P_\Delta|g_c|^2(x).
\]

In particular, \(A_{0,\mathrm{Id}}=P_\Delta(\phi^2)(x)\) for real terminal
data. It is determined by terminal data and the diffusion law, independently
of the clock rate. It is not \((P_\Delta\phi(x))^2\). Analytic integration,
deterministic quadrature, or diffusion-only sampling can evaluate it without
generating a branching tree.

For fixed positive code-only tuple probabilities, write
\(V_{z,\lambda}(r,y)=\mathbb E_\lambda|H_{r,y,z}|^2\). The full-tree
continuation coefficient is

\[
A_{c,\lambda}(s)=
\sum_{\ell\in L_c}\frac{1}{q_c(Z_{c,\ell})}
P_s\!\left[
\prod_{z\in Z_{c,\ell}}V_{z,\lambda}(t+s,\cdot)
\right](x).
\]

The sum is over labelled alternatives, and the product is evaluated at the
one shared branch position before taking \(P_s\). For the identity code,
whose single child is \(f^*\), this reduces to
\(A_{\mathrm{Id},\lambda}(s)=P_s[V_{f^*,\lambda}(t+s,\cdot)](x)\).
History-dependent proposals use the corresponding conditional-moment
expression at their actual decision state.

Thus removing the root likelihood factor leaves the descendants' clock
weights intact. In (7.4) the descendants' sampling rules are fixed, making
\(A(s)\) independent of the **root** rate. If one rate is changed everywhere,
the full objective instead contains \(A_{c,\lambda}(s)\), and its derivatives
include the dependence of every child moment on \(\lambda\). Formula (7.5)
alone does not differentiate that full objective.

There is no need to simulate random trees to compute these moments: the
[moment recursion](notation-and-moment-theorem.md)
is a deterministic integral system. A closed system can sometimes be solved
symbolically with \(\lambda\) left as a parameter, as in the binary Riccati
control below. In general, one evaluates a moment approximation for each
candidate rate and then updates that rate. The repository's
[moment evaluator](../../../parabolab/moments.py) and
[recursive derivative evaluator](../../../parabolab/rate_optimization.py)
use finite-depth 1D quadrature. Avoiding random tree simulation does not remove
the cost of these integrals or certify the omitted-depth and quadrature
errors. The local square-root tuple oracle has the same practical issue:
its continuation moments are generally unknown and must be computed or
approximated.

## Theorem 7.1 (strict convexity and unique local rate)

Under (7.2)--(7.3), \(J_{\exp}\) is twice continuously differentiable on
\((0,\infty)\), with

\[
\boxed{
J_{\exp}'(\lambda)
=A_0\Delta e^{\lambda\Delta}
+\frac1{\lambda^2}
\int_0^\Delta
A(s)e^{\lambda s}(\lambda s-1)\,ds
}
\tag{7.5}
\]

and

\[
\boxed{
J_{\exp}''(\lambda)
=A_0\Delta^2e^{\lambda\Delta}
+\frac1{\lambda^3}
\int_0^\Delta
A(s)e^{\lambda s}
\left[(\lambda s-1)^2+1\right]\,ds.
}
\tag{7.6}
\]

In particular,

\[
J_{\exp}''(\lambda)>0
\qquad\text{for every }\lambda>0.
\tag{7.7}
\]

Moreover,

\[
\begin{array}{lll}
\lambda\downarrow0:
&J_{\exp}(\lambda)\longrightarrow+\infty,
&J_{\exp}'(\lambda)\longrightarrow-\infty,\\[1mm]
\lambda\to+\infty:
&J_{\exp}(\lambda)\longrightarrow+\infty,
&J_{\exp}'(\lambda)\longrightarrow+\infty.
\end{array}
\tag{7.8}
\]

Therefore there is a unique
\(\lambda^*\in(0,\infty)\) satisfying
\(J_{\exp}'(\lambda^*)=0\), and this point is the unique global minimizer of
\(J_{\exp}\).

### Proof

For \(k=0,1,2\), put

\[
I_k(\lambda)
:=\int_0^\Delta s^kA(s)e^{\lambda s}\,ds.
\tag{7.9}
\]

On every compact \(\lambda\)-interval in \((0,\infty)\), the integrands and
their first two \(\lambda\)-derivatives are bounded by a constant times
\(A(s)\), because \(0\leq s\leq\Delta\). Dominated differentiation therefore
gives \(I_k'=I_{k+1}\) for \(k=0,1\). Differentiating (7.4) once yields

\[
\begin{aligned}
J_{\exp}'(\lambda)
&=A_0\Delta e^{\lambda\Delta}
-\frac{I_0(\lambda)}{\lambda^2}
+\frac{I_1(\lambda)}{\lambda}\\
&=A_0\Delta e^{\lambda\Delta}
+\frac1{\lambda^2}
\int_0^\Delta
A(s)e^{\lambda s}(\lambda s-1)\,ds,
\end{aligned}
\]

which is (7.5). A second differentiation gives

\[
\begin{aligned}
J_{\exp}''(\lambda)
&=A_0\Delta^2e^{\lambda\Delta}
+\frac{I_2(\lambda)}{\lambda}
-\frac{2I_1(\lambda)}{\lambda^2}
+\frac{2I_0(\lambda)}{\lambda^3}\\
&=A_0\Delta^2e^{\lambda\Delta}
+\frac1{\lambda^3}
\int_0^\Delta A(s)e^{\lambda s}
\bigl(\lambda^2s^2-2\lambda s+2\bigr)\,ds.
\end{aligned}
\]

Since

\[
\lambda^2s^2-2\lambda s+2
=(\lambda s-1)^2+1\geq1,
\tag{7.10}
\]

(7.6) follows. Its first term is strictly positive because
\(A_0,\Delta,\lambda>0\), and its integral term is nonnegative. This proves
(7.7).

For the lower boundary, boundedness of \(s\) and \(A\in L^1\) permit the
Taylor expansions under the integral:

\[
I_0(\lambda)=B+O(\lambda),
\qquad
\int_0^\Delta
A(s)e^{\lambda s}(\lambda s-1)\,ds
=-B+O(\lambda^2).
\tag{7.11}
\]

Consequently

\[
J_{\exp}(\lambda)=\frac B\lambda+O(1),
\qquad
J_{\exp}'(\lambda)=-\frac B{\lambda^2}+O(1),
\qquad \lambda\downarrow0.
\tag{7.12}
\]

Both lower-boundary assertions in (7.8) follow from \(B>0\).

At the upper boundary,

\[
J_{\exp}(\lambda)\geq A_0e^{\lambda\Delta}\longrightarrow+\infty.
\tag{7.13}
\]

For all sufficiently large \(\lambda\), the integrand in (7.5) can be
negative only on \(0<s<1/\lambda\). Its negative part has magnitude at most

\[
\frac1{\lambda^2}
\int_0^{1/\lambda}A(s)e^{\lambda s}\,ds
\leq \frac{eB}{\lambda^2}.
\tag{7.14}
\]

Thus

\[
J_{\exp}'(\lambda)
\geq
A_0\Delta e^{\lambda\Delta}-\frac{eB}{\lambda^2}
\longrightarrow+\infty.
\tag{7.15}
\]

The derivative is continuous, so (7.8) and the Intermediate Value Theorem
give at least one zero. Equation (7.7) makes \(J_{\exp}'\) strictly
increasing, so that zero is unique. A differentiable strictly convex
function decreases before its unique critical point and increases after it;
the critical point is therefore the unique global minimizer. \(\square\)

## Completed-tree topology kernels

Consider a completed finite coding-tree topology \(\theta\). Let
\(\mathcal B(\theta)\) be its branch nodes and
\(\mathcal L(\theta)\) its terminal leaves. For \(v\in\mathcal B(\theta)\),
write \(s_v>0\) for the realized lifetime before branching. For
\(\ell\in\mathcal L(\theta)\), write \(r_\ell>0\) for the leaf's remaining
horizon at birth. Define

\[
B_\theta:=|\mathcal B(\theta)|,
\qquad
L_\theta
:=\sum_{v\in\mathcal B(\theta)}s_v
+\sum_{\ell\in\mathcal L(\theta)}r_\ell.
\tag{7.16}
\]

The quantity \(L_\theta\) is the total particle-duration: it sums the amount
of physical time lived by every particle. A tree started with positive
remaining horizon has \(L_\theta>0\).

At a branch node, the sampling law contributes
\(q_v\rho_\lambda(s_v)\), while the squared likelihood contributes
\((q_v\rho_\lambda(s_v))^{-2}\). Their product is

\[
q_v^{-1}\rho_\lambda(s_v)^{-1}
=q_v^{-1}\lambda^{-1}e^{\lambda s_v}.
\tag{7.17}
\]

At a terminal leaf, the survival probability and squared terminal
likelihood combine to

\[
\bar F_\lambda(r_\ell)
\bar F_\lambda(r_\ell)^{-2}
=e^{\lambda r_\ell}.
\tag{7.18}
\]

All tuple probabilities, mechanism coefficients, Markov transition factors,
and squared terminal evaluations are independent of \(\lambda\). Multiplying
(7.17)--(7.18) over the topology isolates the complete rate dependence:

\[
\boxed{
h_{B,L}(\lambda):=\lambda^{-B}e^{\lambda L},
\qquad
B=B_\theta,\quad L=L_\theta.
}
\tag{7.19}
\]

Its logarithmic derivative is

\[
\frac{h_{B,L}'(\lambda)}{h_{B,L}(\lambda)}
=L-\frac B\lambda.
\tag{7.20}
\]

Differentiating once more gives

\[
\boxed{
h_{B,L}''(\lambda)
=h_{B,L}(\lambda)
\left[
\left(L-\frac B\lambda\right)^2
+\frac B{\lambda^2}
\right]>0,
\qquad \lambda>0,\ L>0.
}
\tag{7.21}
\]

The strict inequality includes \(B=0\): in that case the bracket is \(L^2\).

## Theorem 7.2 (finite-depth and unrestricted convexity)

For a fixed root \((t,x,c)\), let

\[
V_{c,K}(t,x;\lambda)
:=\mathbb E_\lambda
\left[|H_{t,x,c}^{[K]}|^2\right]
\in[0,\infty]
\tag{7.22}
\]

be a killed finite-depth second moment, and let

\[
V_c(t,x;\lambda)
:=\mathbb E_\lambda|H_{t,x,c}|^2
=\sup_K V_{c,K}(t,x;\lambda).
\tag{7.23}
\]

Assume the model hypotheses of the common moment theorem and the
finite-topology disintegration described below.

1. Every \(V_{c,K}(t,x;\cdot)\) is an extended-valued lower-semicontinuous
   convex function on \((0,\infty)\).
2. If at least one completed topology retained at depth \(K\) has a
   strictly positive second-moment contribution, then
   \(V_{c,K}(t,x;\cdot)\) is strictly convex on every interval on which it
   is finite. In particular, a live non-trivial branch topology is
   sufficient.
3. The unrestricted moment \(V_c(t,x;\cdot)\) is lower-semicontinuous and
   convex on \((0,\infty)\), and hence convex on its effective domain
   \[
   \mathcal D_c(t,x)
   :=\{\lambda>0:V_c(t,x;\lambda)<\infty\}.
   \tag{7.24}
   \]
4. If the unrestricted topology expansion contains a fixed topology with
   positive contribution, then \(V_c(t,x;\cdot)\) is strictly convex
   between any two distinct points of \(\mathcal D_c(t,x)\).

### Proof

For each labelled completed topology \(\theta\), collect all branch times,
branch positions, and terminal positions into a mark \(\xi\in\Xi_\theta\).
There is a rate-independent measure \(\nu_\theta(d\xi)\) and a nonnegative,
rate-independent measurable factor \(W_\theta(\xi)\) containing all tuple,
mechanism, Markov, and terminal terms. Equations (7.17)--(7.19) give

\[
V_{c,K}(t,x;\lambda)
=
\sum_{\theta\in\Theta_K}
\int_{\Xi_\theta}
W_\theta(\xi)
h_{B_\theta,L_\theta(\xi)}(\lambda)
\,\nu_\theta(d\xi).
\tag{7.25}
\]

The sum is over labelled occurrences: repeated mechanism tuples remain
distinct topologies. At fixed depth, finite mechanism tables and finite
child tuples make \(\Theta_K\) finite. Tonelli's theorem licenses (7.25) in
\([0,\infty]\).

Equation (7.21) says each kernel in (7.25) is strictly convex. Multiplication
by \(W_\theta\geq0\), integration, and summation preserve the non-strict
convexity inequality. If some topology has

\[
\nu_\theta\{\xi:W_\theta(\xi)>0\}>0,
\tag{7.26}
\]

then the pointwise strict kernel inequality integrates to a strict
inequality whenever the endpoint values are finite. This proves the first
two convexity assertions.

For lower semicontinuity, if \(\lambda_n\to\lambda>0\), continuity and
nonnegativity of \(h_{B,L}\), followed by Fatou's lemma, give

\[
\int W_\theta h_{B_\theta,L_\theta}(\lambda)\,d\nu_\theta
\leq
\liminf_{n\to\infty}
\int W_\theta h_{B_\theta,L_\theta}(\lambda_n)\,d\nu_\theta.
\tag{7.27}
\]

Finite sums preserve this inequality, so each \(V_{c,K}\) is lower
semicontinuous.

The killed-depth identity from the common moment theorem gives the supremum
in (7.23). A pointwise supremum of convex functions is convex:
for \(\lambda_0,\lambda_1>0\) and \(a\in(0,1)\),

\[
\begin{aligned}
V_c(a\lambda_0+(1-a)\lambda_1)
&=\sup_KV_{c,K}(a\lambda_0+(1-a)\lambda_1)\\
&\leq
\sup_K\bigl[
aV_{c,K}(\lambda_0)+(1-a)V_{c,K}(\lambda_1)
\bigr]\\
&\leq
aV_c(\lambda_0)+(1-a)V_c(\lambda_1).
\end{aligned}
\tag{7.28}
\]

A supremum of lower-semicontinuous functions is lower-semicontinuous, which
proves assertion 3.

Finally, the unrestricted topology space is the countable union of the
finite labelled topology spaces. Nonexplosion ensures that every realized
tree belongs to that union. Tonelli therefore gives the unrestricted
analogue of (7.25). If one term satisfies (7.26), that term has a strict
convexity inequality and all other terms have non-strict inequalities.
Their nonnegative sum is strict whenever both endpoint moments are finite.
This proves assertion 4. \(\square\)

## Corollary 7.3 (when a full-tree sweet spot exists)

Suppose, in addition to Theorem 7.2, that:

1. \(V_c(t,x;\lambda_0)<\infty\) for at least one \(\lambda_0>0\);
2. the root-survival coefficient is positive,
   \[
   P_\Delta|g_c|^2(x)>0;
   \tag{7.29}
   \]
3. at least one branched topology \(\theta_b\), with
   \(B_{\theta_b}\geq1\), has positive contribution.

Then the extended-valued function \(V_c(t,x;\cdot)\) has a unique global
minimizer \(\lambda^*\in(0,\infty)\).

### Proof

The root-survival topology has \(B=0\), \(L=\Delta\), and gives the lower
bound

\[
V_c(t,x;\lambda)
\geq
e^{\lambda\Delta}P_\Delta|g_c|^2(x)
\longrightarrow+\infty
\qquad(\lambda\to+\infty).
\tag{7.30}
\]

Write

\[
C_b:=\int_{\Xi_{\theta_b}}W_{\theta_b}(\xi)\,
\nu_{\theta_b}(d\xi).
\tag{7.31}
\]

Positive contribution gives \(C_b>0\). Properness at \(\lambda_0\) and
\(h_{B,L}(\lambda_0)\geq\lambda_0^{-B}\) imply \(C_b<\infty\). Since
\(e^{\lambda L}\geq1\),

\[
V_c(t,x;\lambda)
\geq C_b\lambda^{-B_{\theta_b}}
\longrightarrow+\infty
\qquad(\lambda\downarrow0).
\tag{7.32}
\]

Thus \(V_c\) is proper, lower semicontinuous, and coercive at both ends of
\((0,\infty)\). A nonempty sublevel set below
\(V_c(t,x;\lambda_0)+1\) is contained in a compact subinterval of
\((0,\infty)\); lower semicontinuity gives attainment there. The positive
topology and Theorem 7.2(4) give strict convexity on the effective domain,
so the minimizer is unique. \(\square\)

This corollary applies to an \(L^2\)-integrable binary \(u^2\) estimator and
to an \(L^2\)-integrable Allen--Cahn estimator on every horizon where their
full moments are proper and the displayed nondegeneracy conditions hold.
The common moment theorem is the required integrability gate: empirical
stability by itself is not a proof that condition 1 holds.

For the saved flat and traveling-wave Allen–Cahn examples at `T=1/20`,
the [six-code moment certificates](../results/certified-rate-checkpoint.md)
now supply finite incumbents. This closes that hypothesis for these stated
examples; it does not establish finiteness for arbitrary horizons or proposals.

The Harry Dym example lies on the other side of that gate. The
[Dym non-integrability theorem](dym-nonintegrability.md#theorem-41-infinite-absolute-first-moment)
proves, for every \(\lambda>0\), every positive horizon, and every
nondegenerate parameter \(\alpha\), that

\[
\mathbb E_\lambda|H_{t,x,\mathrm{Id}}|=\infty.
\tag{7.33}
\]

If its second moment were finite, Cauchy--Schwarz would imply
\(\mathbb E_\lambda|H|<\infty\), contradicting (7.33). Hence

\[
\boxed{
V_{\mathrm{Id}}(t,x;\lambda)
=\mathbb E_\lambda|H_{t,x,\mathrm{Id}}|^2
=+\infty
\quad\text{for every }\lambda>0.
}
\tag{7.34}
\]

The Dym estimator therefore has no finite variance sweet spot. Changing the
exponential rate can hide or expose rare singular samples at finite budget,
but cannot restore \(L^2\) integrability.

## Short-horizon scaling

The short-horizon limit needs notation that separates an instantaneous
branch coefficient from the integrated quantity \(B\) in (7.3). For a code
\(c\), let

\[
G_c(x):=|g_c(x)|^2
\tag{7.35}
\]

and, under the coefficient-encoded convention of the common moment theorem,
let

\[
B_c(x)
:=
\sum_{\ell\in L_c}
q_c(\ell)^{-1}
\prod_{z\in Z_{c,\ell}}|g_z(x)|^2.
\tag{7.36}
\]

Thus \(B_c(x)\) is the terminal-time branch density, whereas the earlier
quantity satisfies
\(\int_0^T A_T(s)\,ds=TB_c(x)+O(T^2)\) under the regularity below.

For the identity code, the mechanism table is the singleton
\(\mathcal M(\mathrm{Id})=\{(f^*,)\}\), with proposal probability one.
Since

\[
g_{\mathrm{Id}}(x)=\phi(x),
\qquad
g_{f^*}(x)=f(J\phi(x)),
\tag{7.37}
\]

equations (7.35)--(7.36) specialize to

\[
G_{\mathrm{Id}}(x)=|\phi(x)|^2,
\qquad
B_{\mathrm{Id}}(x)=|f(J\phi(x))|^2.
\tag{7.38}
\]

## Theorem 7.4 (the optimal rate is \(O(1)\) as \(T\downarrow0\))

Consider a family of local objectives at \(t=0\),

\[
J_T(\lambda)
=A_{0,T}e^{\lambda T}
+\frac1\lambda\int_0^T A_T(s)e^{\lambda s}\,ds.
\tag{7.39}
\]

Assume \(G_c(x)>0\), \(B_c(x)>0\), and, as \(T\downarrow0\),

\[
A_{0,T}=G_c(x)+O(T),
\qquad
\sup_{0\leq s\leq T}
|A_T(s)-B_c(x)|=O(T).
\tag{7.40}
\]

Then the unique minimizer \(\lambda^*(T)\) satisfies

\[
\boxed{
\lambda^*(T)
\longrightarrow
\sqrt{\frac{B_c(x)}{G_c(x)}}.
}
\tag{7.41}
\]

For the identity root at a point where both terms in (7.38) are nonzero,

\[
\boxed{
\lambda^*(T)
\longrightarrow
\frac{|f(J\phi(x))|}{|\phi(x)|}
=O(1).
}
\tag{7.42}
\]

The same leading law holds for the full recursive moment when, uniformly for
\(\lambda\) in compact subsets of \((0,\infty)\), its value and
\(\lambda\)-derivative have the expansions (7.45) and (7.44). Sufficient
conditions are uniform convergence of child moments and their
\(\lambda\)-derivatives to the terminal values, together with a uniform
short-horizon integrable majorant. Finiteness at each fixed \(T\) alone does
not supply this uniform passage.

### Proof

Fix a compact interval of positive \(\lambda\)-values. Uniformly on that
interval, (7.40) gives

\[
\begin{aligned}
A_{0,T}T e^{\lambda T}
&=TG_c(x)+O(T^2),\\
\int_0^T
A_T(s)e^{\lambda s}(\lambda s-1)\,ds
&=-TB_c(x)+O(T^2).
\end{aligned}
\tag{7.43}
\]

Substitution into the exact derivative (7.5) yields

\[
\boxed{
J_T'(\lambda)
=T\left(
G_c(x)-\frac{B_c(x)}{\lambda^2}
\right)+O(T^2),
}
\tag{7.44}
\]

uniformly on compact positive \(\lambda\)-intervals. Equivalently,

\[
J_T(\lambda)
=A_{0,T}
+T\left(
G_c(x)\lambda+\frac{B_c(x)}{\lambda}
\right)+O(T^2).
\tag{7.45}
\]

Let \(\lambda_0=\sqrt{B_c/G_c}\), and choose arbitrary
\(0<\lambda_-<\lambda_0<\lambda_+\). The leading coefficient in (7.44) is
negative at \(\lambda_-\) and positive at \(\lambda_+\). For all
sufficiently small \(T\),

\[
J_T'(\lambda_-)<0<J_T'(\lambda_+).
\tag{7.46}
\]

Theorem 7.1 makes \(J_T'\) strictly increasing, so its unique zero lies in
\((\lambda_-,\lambda_+)\). Letting both brackets approach \(\lambda_0\)
proves (7.41). Equation (7.42) follows from (7.38). \(\square\)

For example, the binary control with \(\phi=1\) and \(f(u)=u^2\) has limiting
rate \(1\). For Allen--Cahn, \(f(u)=u-u^3\), so at a nonzero terminal value

\[
\frac{|f(\phi)|}{|\phi|}=|1-\phi^2|.
\tag{7.47}
\]

At \(\phi=\pm1/2\), this gives the limiting rate \(3/4\).

### Comparison with the JCP heuristic

Put

\[
c:=-\log(0.95)=0.051293\ldots,
\qquad
\lambda_{\mathrm{JCP}}(T):=\frac cT.
\tag{7.48}
\]

Then \(\lambda_{\mathrm{JCP}}(T)=O(T^{-1})\), in contrast with (7.41).
Substitution into (7.39)--(7.40) gives

\[
\begin{aligned}
J_T(\lambda_{\mathrm{JCP}})
&=G_c(x)e^c+O(T),\\
\frac1{\lambda_{\mathrm{JCP}}}
\int_0^T A_T(s)e^{\lambda_{\mathrm{JCP}}s}\,ds
&=
B_c(x)T^2\frac{e^c-1}{c^2}+O(T^3).
\end{aligned}
\tag{7.49}
\]

By contrast, (7.45) and (7.41) imply

\[
J_T(\lambda^*(T))=G_c(x)+O(T).
\tag{7.50}
\]

Therefore

\[
\boxed{
\frac{J_T(\lambda_{\mathrm{JCP}})}
{J_T(\lambda^*(T))}
\longrightarrow
e^c
=\frac1{0.95}
=1.052631\ldots .
}
\tag{7.51}
\]

Thus the JCP scaling pays an asymptotic \(5.26\%\) multiplicative penalty in
the leading second-moment objective. Because the represented mean is
rate-independent, the corresponding excess second moment is also an
additive variance penalty. The factor in (7.51) should not be reported as a
\(1.0526\)-fold ratio of centered variances: the optimal centered variance
typically tends to zero as \(T\downarrow0\).

There is also a direction-of-effect audit. Under the optimizer,

\[
\mathbb P_{\lambda^*(T)}(\tau<T)
=1-e^{-\lambda^*(T)T}
=\lambda_0T+O(T^2)
\longrightarrow0,
\tag{7.52}
\]

whereas

\[
\mathbb P_{\lambda_{\mathrm{JCP}}(T)}(\tau<T)
=1-e^{-c}=0.05.
\tag{7.53}
\]

Consequently the \(O(T^{-1})\) heuristic does **not** over-suppress
branching relative to the short-horizon optimum; it over-samples first
branches by keeping their probability at \(5\%\) instead of letting it
vanish at rate \(O(T)\). Its motivation is to suppress tree growth at a
fixed horizon, but the literal asymptotic comparison has the direction
shown in (7.52)--(7.53).

## Exact binary Riccati control

The oracle in this section belongs to the explicit `Id → (Id,Id)` mechanism.
It is not the second moment of the default derivative-coded tree for the
same PDE. The [binary audit](../results/binary-benchmark-audit.md) corrects
the old mismatched numerical comparison; the original CSV and figure are
historical diagnostics, not oracle validation. The current binary driver
uses matching mechanisms. Its numerical stationary rates are not rigorous
interval enclosures of the exact minimizing rate.

Consider the standard binary branching representation of

\[
u_t+\frac12u_{xx}+u^2=0,
\qquad
u(T,x)=1.
\tag{7.54}
\]

Spatial motion is immaterial because the terminal condition is constant.
Write \(V(r;\lambda)\) for the second moment with remaining horizon \(r\).
First-event conditioning gives the nonnegative minimal solution

\[
V(r;\lambda)
=e^{\lambda r}
+\frac1\lambda\int_0^r
e^{\lambda s}V(r-s;\lambda)^2\,ds.
\tag{7.55}
\]

Define

\[
Y(r):=e^{-\lambda r}V(r;\lambda).
\tag{7.56}
\]

After changing variables \(q=r-s\), equation (7.55) becomes

\[
Y(r)
=1+\frac1\lambda\int_0^r e^{\lambda q}Y(q)^2\,dq.
\tag{7.57}
\]

Hence \(Y\) solves the Riccati equation

\[
\boxed{
Y'(r)=\frac{e^{\lambda r}}{\lambda}Y(r)^2,
\qquad
Y(0)=1.
}
\tag{7.58}
\]

## Theorem 7.5 (closed second moment and optimality equation)

Before its Riccati explosion time,

\[
\boxed{
V(T;\lambda)
=
\frac{\lambda^2e^{\lambda T}}
{\lambda^2+1-e^{\lambda T}}.
}
\tag{7.59}
\]

The second moment is finite precisely when

\[
\lambda^2+1-e^{\lambda T}>0.
\tag{7.60}
\]

Its unique minimizing rate in this effective domain satisfies

\[
\boxed{
2(e^{\lambda T}-1)
=T\lambda(\lambda^2+1).
}
\tag{7.61}
\]

As \(T\downarrow0\), that solution has the expansion

\[
\boxed{
\lambda^*(T)
=1+\frac T2+\frac{7T^2}{24}+O(T^3).
}
\tag{7.62}
\]

### Proof

Separating variables in (7.58) gives

\[
\frac1{Y(r)}
=1-\frac1\lambda\int_0^r e^{\lambda q}\,dq
=1-\frac{e^{\lambda r}-1}{\lambda^2}.
\tag{7.63}
\]

Multiplying \(Y(T)\) by \(e^{\lambda T}\) proves (7.59). If the denominator
in (7.59) vanishes at or before \(T\), the nonnegative Riccati solution
explodes and the minimal second moment is \(+\infty\); the algebraic
continuation of (7.59) beyond that pole is not a moment. This proves
(7.60).

Let

\[
D(\lambda,T):=\lambda^2+1-e^{\lambda T}.
\tag{7.64}
\]

On \(D>0\), direct differentiation of (7.59) yields

\[
\frac{\partial V}{\partial\lambda}(T;\lambda)
=
\frac{\lambda e^{\lambda T}}{D(\lambda,T)^2}
\left[
T\lambda(\lambda^2+1)
-2(e^{\lambda T}-1)
\right].
\tag{7.65}
\]

The prefactor is strictly positive, so stationarity is equivalent to
(7.61). The topology theorem gives strict convexity, while the moment
diverges at the boundaries of its nonempty effective domain. Thus the
stationary point in that domain is its unique minimizer.

To expand the root, divide (7.61) by \(T\lambda>0\) and continuously extend
the resulting equation to \(T=0\):

\[
F(T,\lambda)
:=
\frac{2(e^{\lambda T}-1)}{T\lambda}
-(\lambda^2+1)=0,
\qquad
F(0,\lambda)=1-\lambda^2.
\tag{7.66}
\]

Since

\[
F(0,1)=0,
\qquad
\partial_\lambda F(0,1)=-2\ne0,
\tag{7.67}
\]

the implicit function theorem gives a unique analytic root near
\((T,\lambda)=(0,1)\). Substitute

\[
\lambda(T)=1+aT+bT^2+O(T^3)
\tag{7.68}
\]

into (7.61). The coefficients of \(T^2\) and \(T^3\), respectively, give

\[
2a+1=4a,
\qquad
2b+2a+\frac13=4b+3a^2.
\tag{7.69}
\]

Therefore

\[
a=\frac12,
\qquad
b=\frac7{24},
\tag{7.70}
\]

which proves (7.62). Its leading value \(1\) agrees with (7.42), since
\(\phi=1\) and \(f(\phi)=1\). \(\square\)

## Assumption and claim audit

1. The local theorem treats \(A_0\) and \(A(s)\) as fixed while optimizing
   \(\lambda\). It is not a proof that recursively computed child moments
   are rate-independent.
2. The topology proof avoids differentiating an unrestricted expectation.
   Convexity follows pointwise from the exact rate kernel and then from
   Tonelli, Fatou, and monotone depth exhaustion.
3. Strict convexity alone does not prove finite variance. Properness of the
   exact second moment is an explicit hypothesis in Corollary 7.3.
4. The short-horizon law requires \(G_c(x),B_c(x)>0\) and the uniform
   terminal expansion (7.40). At zeros of \(\phi\) or \(f(J\phi)\), a
   different scaling may occur.
5. Equation (7.59) is valid only before Riccati explosion. A negative
   denominator is not a negative second moment; it indicates
   \(V(T;\lambda)=+\infty\).
6. The Dym conclusion is stronger than failure of \(L^2\): the existing
   five-particle topology already makes the absolute first moment infinite
   for every positive exponential rate.
7. The factor \(e^{0.051293\ldots}=1/0.95\) is a second-moment inflation
   factor. It gives an additive variance excess because the mean is fixed,
   not a universal multiplicative ratio of centered variances.
