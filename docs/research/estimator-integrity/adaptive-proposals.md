# Safe adaptive branching proposals

**Mathematical status:** conventional proofs under the support, measurability, and
integrability hypotheses stated below.

**Implementation status (16 September 2026):**
[`proposals.py`](../../../parabolab/proposals.py) implements finite-table
square-root probabilities, frozen pilot tables and a terminal-data proxy.
The proxy is not the true continuation-moment oracle. A general sampler for
Theorem 6.2's unrestricted event-time law and a certified continuation-aware
proposal are not implemented. The saved Allen–Cahn certificates use fixed
uniform tuple probabilities; changing `q` requires new moment verification.
During scalar rate differentiation, `q` stays fixed while the descendant
moments still vary with `lambda`.

[`Proposal.lean`](../../../formal/EstimatorIntegrity/Proposal.lean) checks
finite-table algebra, including the square-root objective and mixture/error
bounds. Conditional expectations, full-tree unbiasedness, the pilot
concentration event and composition over a random tree remain conventional
arguments under their written hypotheses. Finite-sample agreement with a
reference is not a proof of these hypotheses or of unbiasedness.

This note separates three questions that are often conflated in adaptive
branching Monte Carlo:

1. which proposal minimizes a conditional second moment when the continuation
   contributions are known;
2. when a proposal estimated from data preserves the target mean; and
3. how pilot error degrades the oracle second moment at finite tree depth.

All proposal optimizations are importance-sampling statements. A proposal may
change the law under which a tree is generated, but every retained alternative
must carry its exact inverse proposal probability. The results do not repair a
non-integrable target functional: a positive proposal floor controls likelihood
ratios, not singular terminal factors.

## Setup

Consider one tuple decision with a finite labelled mechanism table
\(\{Z_1,\ldots,Z_m\}\). Labels are retained even when two entries have the same
ordered child tuple. Conditional on all information available before the tuple
draw, let \(Y_i\) be the unweighted continuation associated with selecting
\(Z_i\), including all randomness sampled after the selection. Define

\[
A_i:=\mathbb E\!\left[|Y_i|^2\mid\mathcal H\right]\in[0,\infty],
\tag{6.1}
\]

where \(\mathcal H\) is the pre-selection history. If \(I\) is drawn with
probabilities \(q_1,\ldots,q_m\), the tuple part of the likelihood-weighted
continuation is \(Y_I/q_I\), and hence

\[
\mathbb E\!\left[
\left|\frac{Y_I}{q_I}\right|^2
\middle|\mathcal H
\right]
=\sum_{i=1}^m q_i\frac{A_i}{q_i^2}
=\sum_{i=1}^m\frac{A_i}{q_i}.
\tag{6.2}
\]

The same calculation applies when the \(A_i\) are deterministic quantities
obtained after integrating over a branch time and branch position. Throughout
the optimizer theorems, every displayed second moment is assumed finite unless
the extended-real case is discussed explicitly.

## Theorem 6.1 (finite tuple optimizer)

Let \(m\geq1\), \(A_i>0\), \(q_i>0\), and
\(\sum_{i=1}^m q_i=1\). Then

\[
\boxed{
J(q):=\sum_{i=1}^m\frac{A_i}{q_i}
\geq
\left(\sum_{i=1}^m\sqrt{A_i}\right)^2.
}
\tag{6.3}
\]

Equality holds if and only if

\[
\boxed{
q_i=q_i^*
:=
\frac{\sqrt{A_i}}{\sum_{j=1}^m\sqrt{A_j}},
\qquad i=1,\ldots,m.
}
\tag{6.4}
\]

### Proof

Apply the finite-dimensional Cauchy--Schwarz inequality to

\[
a_i:=\sqrt{\frac{A_i}{q_i}},
\qquad
b_i:=\sqrt{q_i}.
\tag{6.5}
\]

Because \(A_i,q_i>0\), both vectors are well defined, and

\[
\begin{aligned}
\left(\sum_{i=1}^m\sqrt{A_i}\right)^2
&=
\left(\sum_{i=1}^m
\sqrt{\frac{A_i}{q_i}}\sqrt{q_i}\right)^2\\
&\leq
\left(\sum_{i=1}^m\frac{A_i}{q_i}\right)
\left(\sum_{i=1}^m q_i\right)
=J(q).
\end{aligned}
\tag{6.6}
\]

This proves (6.3). Equality in Cauchy--Schwarz holds exactly when there is a
constant \(c>0\) such that \(a_i=cb_i\) for every \(i\). In the present
notation,

\[
\sqrt{\frac{A_i}{q_i}}=c\sqrt{q_i}
\quad\Longleftrightarrow\quad
q_i=\frac{\sqrt{A_i}}{c}.
\tag{6.7}
\]

Normalization gives
\(c=\sum_j\sqrt{A_j}\), and therefore (6.4). Conversely, substituting
(6.4) into (6.7) gives equality in (6.6). Positivity of every \(A_i\)
makes the equality proposal unique. \(\square\)

### Exact zeros and proposal support

The strict positivity assumption in Theorem 6.1 is a support condition, not
an instruction to replace a small estimate by zero. Let

\[
S_+:=\{i:A_i>0\}.
\tag{6.8}
\]

If \(S_+\neq\varnothing\) and \(A_i=0\) has been proved exactly for
\(i\notin S_+\), then \(Y_i=0\) almost surely for those indices. They may be
removed by exact zero pruning, and Theorem 6.1 applies on \(S_+\). Equivalently,
on the closed simplex the optimizer assigns zero mass to the exactly zero
indices and normalizes \(\sqrt{A_i}\) over \(S_+\). If every \(A_i=0\), the
objective is zero for every supported proposal.

If a zero has not been established analytically, the corresponding labelled
branch remains live. In particular, a zero pilot count or a numerically
underflowed estimate is not a proof that \(A_i=0\). Assigning proposal
probability zero then removes part of the target mechanism and invalidates the
likelihood identity. Such an unpruned branch must retain positive probability,
for example through

\[
q_i^{(\varepsilon)}
=(1-\varepsilon)q_i+\frac{\varepsilon}{m},
\qquad 0<\varepsilon<1.
\tag{6.9}
\]

If exact zero alternatives are kept while the admissible class requires
\(q_i>0\) for every label, the square-root value is an infimum approached as
their probabilities decrease to zero; it is not attained in that open
simplex. A positive floor gives an attained, support-preserving alternative.
There is no safe silent zero-probability assignment to an unpruned live
branch.

## Theorem 6.2 (first-event leaf/branch optimizer)

Fix a remaining horizon \(\Delta=T-t>0\). Treat the first event as one
probability distribution on the disjoint union

\[
\{\mathrm{leaf}\}\;\dot\cup\;(0,\Delta).
\tag{6.10}
\]

The leaf has probability \(r_0\), while a branch at time \(s\) has
unconditional density \(r(s)\), so

\[
r_0\geq0,\qquad r(s)\geq0,\qquad
r_0+\int_0^\Delta r(s)\,ds=1.
\tag{6.11}
\]

Let \(A_0\geq0\) be the unweighted leaf second-moment contribution and let
\(A:(0,\Delta)\to[0,\infty]\) be a measurable unweighted branch
second-moment density. Set

\[
C:=\sqrt{A_0}+\int_0^\Delta\sqrt{A(s)}\,ds.
\tag{6.12}
\]

For every admissible proposal that is positive on the support of \(A_0\) and
\(A\),

\[
\boxed{
J(r_0,r)
:=
\frac{A_0}{r_0}
+
\int_0^\Delta\frac{A(s)}{r(s)}\,ds
\geq C^2.
}
\tag{6.13}
\]

Here a positive numerator divided by zero is \(+\infty\), while \(0/0\) is
set to zero only on an event whose zero contribution has been established
exactly. If \(0<C<\infty\), equality is attained by

\[
\boxed{
r_0^*=\frac{\sqrt{A_0}}{C},
\qquad
r^*(s)=\frac{\sqrt{A(s)}}{C}
\quad\text{for almost every }s\in(0,\Delta).
}
\tag{6.14}
\]

### Proof

Let

\[
\nu:=\delta_{\mathrm{leaf}}+\operatorname{Leb}|_{(0,\Delta)}
\tag{6.15}
\]

be the measure with one leaf atom and a Lebesgue branch-time component. Define
\(a(\mathrm{leaf})=A_0\), \(a(s)=A(s)\),
\(p(\mathrm{leaf})=r_0\), and \(p(s)=r(s)\). Then
\(\int p\,d\nu=1\). If \(J(r_0,r)=\infty\), the asserted inequality
already holds. Otherwise
\(\sqrt{a/p}\in L^2(\nu)\) and \(\sqrt p\in L^2(\nu)\), so the
Cauchy--Schwarz inequality in \(L^2(\nu)\) gives

\[
\begin{aligned}
C^2
&=
\left(
\int
\sqrt{\frac{a}{p}}\sqrt p\,d\nu
\right)^2\\
&\leq
\left(\int\frac{a}{p}\,d\nu\right)
\left(\int p\,d\nu\right)
=J(r_0,r).
\end{aligned}
\tag{6.16}
\]

This argument also proves that \(C=\infty\) forces
\(J(r_0,r)=\infty\). If \(0<C<\infty\), equality requires and is implied by

\[
\sqrt{\frac{a}{p}}=C\sqrt p
\quad \nu\text{-almost everywhere on }\{a>0\},
\tag{6.17}
\]

which is equivalent to \(p=\sqrt a/C\). This is precisely (6.14), and
(6.12) verifies its normalization. \(\square\)

If \(C=\infty\), (6.13) says that every admissible proposal has infinite
second-moment objective. If \(C=0\), both \(A_0\) and \(A\) vanish almost
everywhere and the objective is zero after exact pruning. When \(A_0=0\), or
when \(A\) vanishes on a set of positive measure, (6.14) lies on the boundary
of the proposal simplex. As in Theorem 6.1, exact zero events may be removed;
otherwise a positive atom/density floor is required, and the boundary value is
only an infimum in a strict full-support class.

### Why this is not exponential-rate optimization

The proposal \((r_0,r)\) in Theorem 6.2 is an unconstrained distribution for
the first event on one fixed horizon. An exponential lifetime with rate
\(\lambda>0\) produces only the one-parameter subfamily

\[
r_{0,\lambda}=e^{-\lambda\Delta},
\qquad
r_\lambda(s)=\lambda e^{-\lambda s},
\quad 0<s<\Delta.
\tag{6.18}
\]

The atom and density in (6.18) cannot be selected independently:

\[
r_{0,\lambda}+\int_0^\Delta r_\lambda(s)\,ds=1
\tag{6.19}
\]

holds because both are generated by the same \(\lambda\). Its objective is

\[
J_{\exp}(\lambda)
=A_0e^{\lambda\Delta}
+
\frac1\lambda\int_0^\Delta A(s)e^{\lambda s}\,ds.
\tag{6.20}
\]

Minimizing (6.20) is a scalar constrained optimization problem. The
square-root solution (6.14) belongs to this exponential family only when
\(\sqrt{A(s)}\) is proportional to \(e^{-\lambda s}\) and its normalization
also gives the matching leaf atom. Thus (6.14) is not a formula for an
optimal exponential rate. Changing \(\lambda\) simultaneously changes leaf
survival, the branch-time density, likelihood weights, and the expected tree
size.

## Theorem 6.3 (pilot/freeze unbiasedness)

Let \((\Omega,\mathcal F,\mathbb P)\) carry a pilot sigma-field
\(\mathcal P\). For every live pre-selection history \(h\), let

\[
\widehat q_h=(\widehat q_h(1),\ldots,\widehat q_h(m_h))
\tag{6.21}
\]

be \(\mathcal P\)-measurable and satisfy, almost surely,

\[
\sum_{i=1}^{m_h}\widehat q_h(i)=1,
\qquad
\widehat q_h(i)\geq q_{\min}>0
\quad\text{for every live }i.
\tag{6.22}
\]

The policy is jointly measurable in the pilot outcome and the displayed
history variables, and (6.22) holds on one common full-probability pilot
event. All unchanged non-tuple kernels retain their target support. Any
changed non-tuple kernel is mutually absolutely continuous on the live target
support and contributes its exact finite Radon--Nikodym factor.

The dependence on \(h\) permits code-, time-, state-, and depth-dependent
frozen policies. Evaluation trees are generated from fresh base randomness:
conditional on \(\mathcal P\), each tuple is drawn from (6.21), child
continuations use the prescribed conditionally independent kernels, and no
evaluation outcome is used to revise \(\widehat q\). Every selected tuple
contributes the factor \(1/\widehat q_h(i)\). If an event-time or Markov
proposal is also changed, its exact conditional density ratio is included as
well.

Assume that the target coding-tree representation has a finite deterministic
mean \(u\) and that the conditional integrability conditions listed after the
theorem hold. Then the evaluation functional \(\widehat H\) satisfies

\[
\boxed{
\mathbb E[\widehat H\mid\mathcal P]=u
\quad\text{almost surely},
\qquad
\mathbb E[\widehat H]=u.
}
\tag{6.23}
\]

The statement applies componentwise to real and imaginary parts for a complex
functional.

### Proof for a finite-depth tree

Fix a pilot outcome \(p\) outside a \(\mathcal P\)-null set. The frozen
policy \(\widehat q(p)\) is now deterministic. Index a finite-depth labelled
tree topology by \(\theta\), write \(\xi\) for all non-tuple marks on that
topology, and let \(\nu_\theta(d\xi)\) be their proposal-independent base
measure. The marks include branch times and shared branch positions if their
laws have not been changed. Let \(G_\theta(\xi)\) be the unweighted target
integrand, including any fixed mechanism coefficients. If
\(\mathcal B(\theta)\) is the finite set of tuple selections in the topology,
its conditional proposal probability is

\[
Q_p(\theta,\xi)
:=
\prod_{v\in\mathcal B(\theta)}
\widehat q_{h_v(p,\theta,\xi)}(i_v).
\tag{6.24}
\]

Every factor is positive by (6.22). Under the conditional proposal law, the
topology density contributes \(Q_p\), while the estimator contributes its
reciprocal:

\[
\widehat H_p(\theta,\xi)
=\frac{G_\theta(\xi)}{Q_p(\theta,\xi)}.
\tag{6.25}
\]

Absolute integrability permits the labelled topology sum and mark integrals
to be evaluated in either order. Pointwise cancellation gives

\[
\begin{aligned}
\mathbb E[\widehat H\mid\mathcal P=p]
&=
\sum_\theta
\int
Q_p(\theta,\xi)
\frac{G_\theta(\xi)}{Q_p(\theta,\xi)}
\,\nu_\theta(d\xi)\\
&=
\sum_\theta\int G_\theta(\xi)\,\nu_\theta(d\xi)
=u.
\end{aligned}
\tag{6.26}
\]

The last expression contains no pilot outcome. Equivalently, cancellation can
be performed one tuple at a time. If \(\mu_{h,i}\) is the conditional law of
the continuation after selecting \(i\), then

\[
\mathbb E\!\left[
\frac{Y_I}{\widehat q_h(I)}
\middle|\mathcal P,h
\right]
=
\sum_{i=1}^{m_h}
\widehat q_h(i)
\frac{\int y\,\mu_{h,i}(dy)}{\widehat q_h(i)}
=
\sum_{i=1}^{m_h}\int y\,\mu_{h,i}(dy).
\tag{6.27}
\]

Equation (6.27) is a conditional identity given the pilot and all
pre-selection history; iterating it over the finitely many decisions gives
(6.26).

Because the construction is measurable in \(p\), (6.26) is a version of the
conditional expectation and proves the first equality in (6.23). The tower
property, justified by unconditional integrability, then gives

\[
\mathbb E[\widehat H]
=
\mathbb E\!\left[
\mathbb E[\widehat H\mid\mathcal P]
\right]
=\mathbb E[u]
=u.
\tag{6.28}
\]

This proves the theorem when \(\widehat H\) is a fixed finite-depth target.

### Conditional integrability requirements

Full support and a lower probability floor are not moment assumptions. The
following conditions are required; none follows from \(q_{\min}>0\) alone.

1. **Finite target mean.** The target \(u\) is finite. No expression of the
   form \(+\infty-\infty\) is used to define it.
2. **Conditional absolute integrability.** For almost every pilot outcome,
   \[
   \mathbb E\!\left[|\widehat H|\mid\mathcal P\right]<\infty.
   \tag{6.29}
   \]
   For a finite-depth topology expansion, a sufficient and proposal-invariant
   formulation is
   \[
   \sum_\theta\int|G_\theta(\xi)|\,\nu_\theta(d\xi)<\infty.
   \tag{6.30}
   \]
   Indeed, the same cancellation as in (6.26) makes the conditional absolute
   expectation equal to (6.30).
3. **Integrable conditional norm.** To use the unconditional tower property,
   \[
   \mathbb E\!\left[
   \mathbb E(|\widehat H|\mid\mathcal P)
   \right]<\infty.
   \tag{6.31}
   \]
   Condition (6.30), when deterministic and finite, implies (6.31).
4. **Recursive products.** If (6.23) is proved recursively rather than by the
   topology expansion, every conditional child product being integrated must
   be absolutely integrable after conditioning on the one shared branch
   position. This licenses the conditional Fubini steps and excludes an
   undefined product expectation obtained by subtracting infinite signed
   parts.
5. **Unrestricted-tree passage.** For an unbounded-depth tree, almost-sure
   nonexplosion and measurable construction are required. In addition, the
   killed-depth functionals must converge in conditional \(L^1\):
   \[
   \mathbb E\!\left[
   |\widehat H^{[n]}-\widehat H|
   \mid\mathcal P
   \right]\longrightarrow0
   \quad\text{almost surely}.
   \tag{6.32}
   \]
   Conditional domination by \(|\widehat H|\) proves (6.32) when
   \(\widehat H^{[n]}=\widehat H
   \mathbf 1_{\{\operatorname{depth}\leq n\}}\) and (6.29) holds.
   The finite-depth target means must also converge to the represented value
   \(u\). Nonexplosion by itself gives pathwise stabilization but does not give
   the \(L^1\) passage.

These requirements expose why the Dym functional in the companion note is
outside Theorem 6.3: a proposal floor does not remove its divergent absolute
terminal integral.

For completeness, suppose now that \(\widehat H\) is the unrestricted
functional. Let \(u_n\) be the target mean of its killed-depth version
\(\widehat H^{[n]}\). The finite-depth result gives

\[
\mathbb E[\widehat H^{[n]}\mid\mathcal P]=u_n.
\tag{6.32a}
\]

By conditional Jensen's inequality and (6.32),

\[
\left|
\mathbb E[\widehat H^{[n]}-\widehat H\mid\mathcal P]
\right|
\leq
\mathbb E[
|\widehat H^{[n]}-\widehat H|
\mid\mathcal P]
\longrightarrow0
\quad\text{almost surely}.
\tag{6.32b}
\]

If \(u_n\to u\), equations (6.32a)--(6.32b) give
\(\mathbb E[\widehat H\mid\mathcal P]=u\). Condition (6.31) then licenses
the tower calculation (6.28), proving both assertions in (6.23) for the
unrestricted tree. \(\square\)

### Why fresh evaluation randomness matters

The independence requirement is more precisely a conditional-kernel
requirement. Pilot randomness determines \(\widehat q\); fresh evaluation
randomness is then sampled from the kernel indexed by that frozen value.
This makes \(\widehat q\) fixed when (6.27) is evaluated.

Adapting inside one realization is not inherently biased. A sequential
proposal may depend on the observed past and remain unbiased if it has full
conditional support and the estimator carries the complete product of
conditional Radon--Nikodym factors. Bias enters when selection uses the same
continuation outcomes but the estimator is weighted as if the proposal had
been fixed independently, or when rejected alternatives disappear from the
joint likelihood.

A two-alternative example isolates the failure. Let \(Y_1,Y_2\) be independent
Rademacher variables. The target

\[
\mathbb E[Y_1+Y_2]=0.
\tag{6.33}
\]

If one observes both values, selects \(I=\arg\max(Y_1,Y_2)\), and reports
\(2Y_I\) as though \(I\) had been uniform, then

\[
\mathbb E[2Y_I]
=2\,\mathbb E[\max(Y_1,Y_2)]
=1.
\tag{6.34}
\]

The missing factor is not a cosmetic normalization: the selection event is
part of the joint law, has used future outcome information, and has zero
conditional support for the rejected index. If instead a history-dependent
rule has positive conditional probabilities and each selected path is divided
by its actual joint conditional probability, the cancellation (6.27) is
restored. Pilot/freeze is the simpler auditable construction because it avoids
this same-sample selection law.

## Theorem 6.4 (finite-depth multiplicative oracle inequality)

Assume \(A_i>0\) and let \(q^*\) be (6.4). Suppose pilot estimates satisfy,
simultaneously for every \(i\),

\[
(1-\eta)A_i
\leq\widehat A_i
\leq(1+\eta)A_i,
\qquad 0<\eta<1.
\tag{6.35}
\]

Define

\[
\widehat q_i
:=
\frac{\sqrt{\widehat A_i}}
{\sum_j\sqrt{\widehat A_j}},
\qquad
\kappa_\eta
:=
\sqrt{\frac{1+\eta}{1-\eta}}.
\tag{6.36}
\]

Then, componentwise,

\[
\boxed{
\frac{\widehat q_i}{q_i^*}
\in
\left[
\sqrt{\frac{1-\eta}{1+\eta}},
\sqrt{\frac{1+\eta}{1-\eta}}
\right]
=
\left[\kappa_\eta^{-1},\kappa_\eta\right].
}
\tag{6.37}
\]

Consequently,

\[
\boxed{
J(\widehat q)
\leq
\kappa_\eta J(q^*).
}
\tag{6.38}
\]

For a support-preserving uniform mixture

\[
\widetilde q_i
:=
(1-\varepsilon)\widehat q_i+\frac{\varepsilon}{m},
\qquad 0\leq\varepsilon<1,
\tag{6.39}
\]

one has

\[
\boxed{
J(\widetilde q)
\leq
\frac{\kappa_\eta}{1-\varepsilon}J(q^*).
}
\tag{6.40}
\]

### Proof

Put

\[
S:=\sum_j\sqrt{A_j},
\qquad
\widehat S:=\sum_j\sqrt{\widehat A_j}.
\tag{6.41}
\]

Taking square roots in (6.35) and summing gives

\[
\sqrt{1-\eta}\,S
\leq\widehat S
\leq\sqrt{1+\eta}\,S.
\tag{6.42}
\]

For each component,

\[
\frac{\widehat q_i}{q_i^*}
=
\frac{\sqrt{\widehat A_i}}{\sqrt{A_i}}
\frac{S}{\widehat S}.
\tag{6.43}
\]

The first factor in (6.43) lies in
\([\sqrt{1-\eta},\sqrt{1+\eta}]\), while the second lies in
\([1/\sqrt{1+\eta},1/\sqrt{1-\eta}]\). Multiplying the lower endpoints and
the upper endpoints proves (6.37).

The lower ratio in (6.37) gives
\(q_i^*/\widehat q_i\leq\kappa_\eta\). Therefore

\[
\begin{aligned}
J(\widehat q)
&=
\sum_i\frac{A_i}{\widehat q_i}
=
\sum_i
\frac{q_i^*}{\widehat q_i}
\frac{A_i}{q_i^*}\\
&\leq
\kappa_\eta
\sum_i\frac{A_i}{q_i^*}
=\kappa_\eta J(q^*),
\end{aligned}
\tag{6.44}
\]

which proves (6.38). Finally,
\(\widetilde q_i\geq(1-\varepsilon)\widehat q_i\), so

\[
J(\widetilde q)
\leq
\frac1{1-\varepsilon}J(\widehat q).
\tag{6.45}
\]

Combining (6.45) with (6.38) proves (6.40). \(\square\)

The relative-error event forces every \(\widehat A_i>0\). Outside that event,
a practical proposal still needs a positive floor; otherwise a failed or
underflowed pilot estimate could destroy support. A lower oracle support bound
\(q_i^*\geq q_{\min}>0\) is useful for obtaining relative concentration in
the first place, although it is not needed in the algebra from (6.35) to
(6.40).

### Composition over a finite-depth tree

The one-decision factor in (6.40) composes multiplicatively; it does not remain
a single factor for a tree with several tuple selections. Let
\(H^{[n]}\) be a killed tree of maximum generation \(n\), let \(q^*\) be the
backward-induction oracle tuple policy, and leave all non-tuple sampling laws
fixed. At each reachable pre-selection history \(h\), define the exact
\(A_{h,i}\) using the oracle continuation policy below that history. Theorem
6.1 selects \(q_h^*\) from these values. Backward induction proves that this
policy minimizes the finite-depth second moment: the terminal generation has
no tuple decision, and at every earlier history the leaf term is independent
of \(q_h\) while the branch term has the form
\(\sum_i A_{h,i}/q_h(i)\).

Assume exact-zero alternatives have been pruned and

\[
q_h^*(i)\geq q_{\min}>0
\tag{6.46}
\]

for all reachable live histories and labels. On the simultaneous relative
pilot event, (6.37)--(6.39) imply

\[
\frac{q_h^*(i)}{\widetilde q_h(i)}
\leq
K_{\eta,\varepsilon}
:=
\frac{\kappa_\eta}{1-\varepsilon}.
\tag{6.47}
\]

Let \(B_n\) be the largest number of tuple selections on any nonzero topology
of \(H^{[n]}\). It is finite for a fixed root and finite \(n\): finite
mechanism tables and finite child tuples imply by induction that only finitely
many code-labelled topologies are reachable at each generation. If every
tuple has at most \(b\) children, one may use

\[
B_n\leq
\begin{cases}
n,&b=1,\\[2mm]
\dfrac{b^n-1}{b-1},&b>1,
\end{cases}
\tag{6.48}
\]

because tuple selections occur only at generations \(0,\ldots,n-1\).

For a fixed labelled topology \(\theta\) with \(b(\theta)\) tuple selections,
the tuple-dependent factor in its second-moment integral is

\[
\prod_{v\in\mathcal B(\theta)}\frac1{q_{h_v}(i_v)}.
\tag{6.49}
\]

This follows because the sampling law contributes one \(q\) and the squared
likelihood contributes \(q^{-2}\) at each selection. All remaining
time, position, terminal, and coefficient factors are common to the two
policies and nonnegative after taking the squared modulus. Equations
(6.47) and (6.49) therefore bound each topology contribution under
\(\widetilde q\) by
\(K_{\eta,\varepsilon}^{b(\theta)}\) times its oracle contribution. Summing
the nonnegative topology integrals yields

\[
\boxed{
\mathbb E_{\widetilde q}|H^{[n]}|^2
\leq
K_{\eta,\varepsilon}^{B_n}
\mathbb E_{q^*}|H^{[n]}|^2.
}
\tag{6.50}
\]

The exponent \(B_n\) is needed without additional structure. It records the
number of likelihood-ratio decisions that can occur, rather than only the
generation depth.

### High-probability oracle statement

Let the pilot concentration event be

\[
\mathcal E_{\eta,n}
:=
\bigcap_{(h,i)\in\mathscr I_n}
\left\{
(1-\eta)A_{h,i}
\leq\widehat A_{h,i}
\leq(1+\eta)A_{h,i}
\right\},
\tag{6.51}
\]

where \(\mathscr I_n\) contains every proposal component used by the frozen
finite-depth policy. Suppose

\[
\mathbb P_{\mathrm{pilot}}(\mathcal E_{\eta,n})\geq1-\delta.
\tag{6.52}
\]

Then Theorem 6.4 gives the finite-depth high-probability oracle inequality

\[
\boxed{
\mathbb P_{\mathrm{pilot}}\!\left(
\mathbb E_{\widetilde q}|H^{[n]}|^2
\leq
\left[
\frac1{1-\varepsilon}
\sqrt{\frac{1+\eta}{1-\eta}}
\right]^{B_n}
\mathbb E_{q^*}|H^{[n]}|^2
\right)
\geq1-\delta.
}
\tag{6.53}
\]

At a single table, the local objective has the exponent-one bound (6.40);
the full second moment also satisfies the exponent-one specialization of
(6.53). If \(\mathscr I_n\) is finite and componentwise pilot bounds fail
with probabilities at most \(\delta_{h,i}\), the union bound establishes
(6.52) with

\[
\delta\leq\sum_{(h,i)\in\mathscr I_n}\delta_{h,i}.
\tag{6.54}
\]

Finite depth does not make a continuously state-dependent history space
finite. Formula (6.54) directly covers a finite frozen policy table, such as
one indexed by code and generation. A state-dependent policy over a continuum
requires a genuinely uniform concentration event in (6.52), or a separate
finite approximation argument. No unrestricted-depth inequality follows from
(6.53): passing \(n\to\infty\) would require uniform integrability, control of
\(B_n\), and finite expected computational cost.

## Variance and computational cost

Let \(\mu=\mathbb E_qH\), which is independent of \(q\) under Theorem 6.3.
For a real estimator,

\[
\operatorname{Var}_q(H)
=\mathbb E_q[H^2]-\mu^2,
\tag{6.55}
\]

and for a complex estimator the analogous quadratic risk is
\(\mathbb E_q|H-\mu|^2=\mathbb E_q|H|^2-|\mu|^2\). Since the subtracted term
does not depend on the proposal, minimizing the second moment minimizes the
variance whenever the second moment is finite. A multiplicative bound on the
second moment is not automatically the same multiplicative bound on variance;
for example, (6.38) implies

\[
\operatorname{Var}_{\widehat q}(H)
\leq
\kappa_\eta\operatorname{Var}_{q^*}(H)
+
(\kappa_\eta-1)|\mu|^2
\tag{6.56}
\]

at a one-decision real or complex quadratic-risk problem.

There is an important topology qualification. A tuple-only proposal leaves
the lifetime law, and therefore the branch-versus-leaf probability and branch
time of each already-born particle, unchanged. With a positive floor it also
leaves the **support** of possible labelled topologies unchanged. It does not,
in general, leave their probability distribution or expected node count
unchanged. If one table contains \(Z_1=(a)\) and \(Z_2=(b,b)\), changing
\(q(Z_1)\) changes the root offspring-count distribution and consequently the
tree-size distribution. Tuple optimization preserves node-count laws only in
special homogeneous cases, such as alternatives with identical arity and
identical continuation-cost laws.

An event-time proposal has a more direct cost effect: changing
\((r_0,r)\), or changing an exponential rate \(\lambda\), changes whether and
when particles branch and therefore changes the expected number of descendants.
Both tuple and event-time comparisons should consequently record empirical
node cost unless the mechanism structure proves that tuple costs coincide.

For a measured proposal \(q\), define the work-normalized diagnostic

\[
\mathcal W(q)
:=
\widehat{\operatorname{Var}}_q(H)
\times
\widehat{\mathbb E}_q[N_{\mathrm{nodes}}].
\tag{6.57}
\]

When node cost is approximately constant and independent replications are run
under a fixed work budget, (6.57) is motivated by the heuristic variance
\(\operatorname{Var}(H)/N\) with
\(N\) approximately equal to work divided by mean nodes. It is an empirical
efficiency metric, not a theorem for unconstrained branching. The
interpretation can fail when either factor is infinite, per-node costs depend
strongly on code or state, runtime overhead dominates, tree cost has a heavy
tail, or the stopping rule couples sample count to realized costs. Reports
should therefore include the second moment, maximum observed magnitude, mean
and maximum nodes, and the separate factors in (6.57), rather than presenting
their product as a universal complexity bound.

## Claim boundary

The proved statements in this note are finite-table optimizers, a
fixed-horizon first-event optimizer, conditional pilot/freeze unbiasedness, and
a finite-depth multiplicative oracle bound on an explicit pilot concentration
event. They do not establish:

- finite moments for a singular coding-tree functional;
- optimality inside the exponential lifetime family from the unconstrained
  first-event formula;
- safety of same-realization adaptation without its joint likelihood ratio;
- a state-uniform pilot concentration rate from finite depth alone;
- an unrestricted-depth oracle inequality; or
- a proposal-independent computational complexity theorem.
