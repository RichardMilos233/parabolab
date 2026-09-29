# T19 — bounded literature audit and a fixed-tree work obstruction

Status: bounded primary-source review complete; conventional derived
proposition included below. No implementation, experiment, Lean theorem,
or publication-priority claim is made. T13 and T15 are unchanged.

The reviewed construction is 04f-heat-transform-sampler.md, read on
2026-09-28, together with the frozen T13/T15 conclusions and the constant
profile result in 04d-sharp-constant-horizon.md. This review addresses
novelty and the next theoretical question; T17 owns the sampler proof.

## 1. Decision

The general combination of a majorizing function, an $h$-transformed
motion, killing, a bounded branching functional, and uniformly finite
expected cascade size is established methodology. It is not a defensible
general novelty claim for 04f.

The defensible result is narrower: an explicit certificate for the
specified original quadratic derivative-code closure, after the exact
constant/zero-code reductions stated in 04f, on its specified Gaussian
envelope class. The result joins the already checked absolute-moment
bound to an ideal unbiased sampler with explicit output and node-count
bounds. This bounded search does not establish priority for that exact
certificate.

For solving $u_t=\Delta u/2-u^2$ itself, the scalar binary representation
in 04f is a substantially stronger baseline. There is no established
practical advantage for the derivative-code sampler. Further numerical
demonstrations of the latter are not a useful next research gate.

The most useful new distinction from this review is mathematical:
finite first absolute tree mass does not imply that any importance
proposal for those same tree terms can simultaneously have finite
variance and finite expected syntactic node count. Section 5 gives a
complete elementary obstruction, including the finite-mass critical
endpoint from 04d.

## 2. The decisive accessible primary precedent

The closest inspected source is Mina Ossiander,
[A probabilistic representation of solutions of the incompressible
Navier–Stokes equations in R3](https://arxiv.org/pdf/math/0412034).
Section 4, equation (18), constructs an $h$-Brownian transition kernel
$h(y)K(x-y,2\nu t)/h(x)$, with missing mass sent to a trap. Theorem 4.2
gives an all-time small-data representation $u=h\,\mathbb E\Upsilon$;
Proposition 4.2 proves an almost-sure bound on $\Upsilon$. Its proof
uses a horizon-independent binary Galton–Watson tree with offspring
probabilities $p$ and $1-p$, where $0<p\leq1/2$.

For the allowed strict choice $p<1/2$, the elementary consequence is
\[
 \mathbb E N_{\mathrm{dom}}
 =\sum_{n\geq0}(2p)^n=\frac1{1-2p}.
\]
The finite-horizon tree is a subtree of this dominating tree. This
expected-node bound is an inference made here, not a complexity theorem
quoted from the paper. The endpoint $p=1/2$ only gives almost-sure
extinction and does not give a finite expected total size.

The PDE, kernels and branching rules differ from 04f. Nevertheless,
the method-level match is close enough to rule out claiming that the
general package above is new.

## 3. Other inspected sources and the access boundary

These sources delimit the claim; they are not a claim to an exhaustive
literature survey.

* Blömker, Romito and Tribe,
  [A probabilistic representation for the solutions to some non-linear
  PDEs using pruned branching trees](https://www.numdam.org/article/AIHPB_2007__43_2_175_0.pdf),
  Section 3 and Theorem 4.1, construct branching representations and
  identify the smallest positive comparison solution with a tree
  expectation. Equality with the absolute expectation holds for
  norm-multiplicative branching maps. Section 3 also discusses changing
  branching probabilities to arrange extinction. This is direct prior
  for positive comparison systems and for keeping completion separate
  from integrability. It does not by itself give 04f's explicit
  Gaussian certificate.

* Henry-Labordère, Oudjane, Tan, Touzi and Warin,
  [Branching diffusion representation of semilinear PDEs and Monte
  Carlo approximation](https://arxiv.org/pdf/1603.01727),
  provides marked branching for polynomial nonlinearities in $(u,Du)$.
  Proposition 5.1 gives an expected-particle-count renewal formula.
  Its numerical sections use resampling/importance methods. This
  establishes relevant representation and work-analysis precedent;
  it does not establish the present horizon-independent bounds.

* López-Mimbela and Wakolbinger,
  [A probabilistic proof of non-explosion of a non-linear PDE
  system](https://www.cimat.mx/BiblioAdmin/RTAdmin/reportes/enlinea/I-99-19.pdf),
  Theorem 1.1, proves global boundedness for sufficiently small
  localized data under semigroup decay, using a tree expansion.
  Both reaction components are $uv$. This is a close
  small-data/decay/tree precedent, but not the reduced system with
  a linear second reaction in 04e.

* Beznea, Boeangiu and Lupaşcu-Stamate,
  [h-transform of Doob and nonlocal branching
  processes](https://link.springer.com/article/10.1007/s13324-020-00390-3),
  has an accessible publisher abstract explicitly concerning
  preservation of branching under an $h$-transform and nonlinear
  evolution representations. Full theorem-level equivalence was not
  checked because the full article was not accessible here.

* Beznea, Ignat and Rossi,
  [From Gaussian estimates for nonlinear evolution equations to the
  long time behavior of branching processes](https://arxiv.org/pdf/1703.02807),
  Theorems 1.1–1.2 and Proposition 3.1, connect Gaussian estimates and
  long-time asymptotics to a branching process for a different
  generating-function reaction. The stated offspring mean is greater
  than one. Those results should not be cited as a uniform expected
  computation bound for 04f.

Bhattacharya and coauthors' majorizing-kernel paper was identified in
[its author's institutional publication
record](https://experts.arizona.edu/en/publications/majorizing-kernels-and-stochastic-cascades-with-applications-to-i/).
The publisher PDF was not retrieved in this run. No theorem-level
assertion here depends on a secondary transcription of that paper.
The full Ossiander preprint already supplies the decisive precedent,
so further multiplication of similar references was stopped.

### Closest mixed-system prior for the critical dimension

The accessible primary abstract of Escobedo and Levine,
[Critical blowup and global existence numbers for a weakly coupled
system of reaction-diffusion
equations](https://link.springer.com/article/10.1007/BF00375126),
allows nonnegative powers and considers
\[
 u_t=\Delta u+u^{p_1}v^{q_1},\qquad
 v_t=\Delta v+u^{p_2}v^{q_2},
 \qquad 0<p_1+q_1\leq p_2+q_2.
\]
The reduced 04e system becomes, on setting $u=B_*$ and $v=2A_*$,
\[
 u_t=Lu+v,\qquad v_t=Lv+uv,\qquad L=\Delta/2.
\]
A spatial rescaling changes $L$ to $\Delta$, so the exponent tuple is
exactly $(0,1,1,1)$, with sums $1\leq2$. This exact system match is
verified. The abstract specifically warns that $p_1<1$ has more
complicated behavior; it does not state the applicable borderline
theorem. The full 1995 article and its earlier announcement were not
obtained from an accessible primary source in this bounded search.
Thus attribution of the precise $d=4$ theorem remains unverified.

The T15 direct proof closes the mathematics independently. It does not
justify a novelty claim for a general mixed-system critical dimension.
Neither the different $uv/uv$ theorem above nor a theorem requiring
all four exponents to be at least one can be silently substituted.

## 4. What the baselines actually establish

For the 04f data class, write
\[
 G(t,x)=(1+t)^{-d/2}e^{-|x|^2/[2(1+t)]},\quad
 w(t)=(1+t)^{-d/2},\quad
 I_0(t)=\int_0^t w(s)\,ds.
\]
The scalar binary representation uses
\[
 m_*(t)=\frac{\epsilon}{1-\epsilon I_0(t)},\qquad
 h_*=m_*G,\qquad \kappa_*=m_*w.
\]
Since $m_*'=m_*^2w$, its successful-branch probability conditional
on a clock event is $G/w\leq1$. Its unconditional event probability
is at most $\eta=\epsilon I_0(\infty)$. These identities give,
by finite-depth induction,
\[
 \mathbb E N_*\leq\frac1{1-2\eta},\qquad
 |\widehat H_*|\leq\frac{\epsilon G}{1-\eta}.
\]
For $d\geq5$ and $\epsilon\leq1/32$, $\eta\leq1/48$, hence
\[
 \mathbb E N_*\leq24/23,\qquad
 |\widehat H_*|\leq48\epsilon G/47.
\]
These bounds need no derivative oracle. The construction already works
in integer dimensions $d\geq3$ for sufficiently small $\epsilon$.

The derivative-code result gives $\mathbb E N_{\mathrm{all}}\leq112$
and $|\widehat H_I|\leq(\epsilon+C\epsilon^2t)G\leq\epsilon$.
These are valid certificates with a different mechanism and oracle
contract. Comparing upper bounds does not prove a runtime ratio or
strict ordering of actual variances. It is enough to reject an asserted
efficiency advantage without further evidence.

For the Gaussian datum, the heat-flow baseline is explicit and has
absorption bias at most $\epsilon^2I_0(t)G$. The zero estimator has
absolute error at most $\epsilon G$. Any eventual efficiency question
must fix the requested error, relative versus absolute accuracy,
admissible bias, input-oracle costs, and arithmetic model. Node count
alone does not certify floating-point runtime or exact unbiasedness of
an implementation.

The status of the main assertions is therefore:

| Assertion | Audit status |
|---|---|
| $h$-transformed, killed, bounded cascades with small-data global representations | Established prior methodology |
| Uniform expected cascade size under strict subcritical domination | Elementary established consequence |
| Explicit 04f certificate for its derivative-code closure and data class | Checked local contribution; priority not established |
| New general PDE-solving method, or practical advantage on this quadratic example | Unsupported |
| Exact Escobedo–Levine theorem yielding the reduced-system $d=4$ specialization | System match verified; theorem specialization unverified |
| Finite first absolute mass implies a finite-variance, finite-mean-work proposal | False; next section gives a counterexample |

## 5. Derived proposition: the cost-weighted absolute tree measure

This is an elementary measure-theoretic observation, included with proof.
It is not presented as a new importance-sampling principle.

### Fixed representation and oracle contract

Fix a finite horizon and root. Let $\Omega$ be the measurable space of
completed finite trees with their marks, event times and spatial
locations. Let $\nu$ be the canonical signed tree measure after
likelihood cancellation, and suppose
\[
 0<W:=|\nu|(\Omega)<\infty.
\]
Here $|\nu|$ is total variation before summing differently signed
trees. Let $N:\Omega\to[1,\infty)$ be a measurable cost, finite
$|\nu|$-almost everywhere. For the application below it is the total
number of vertices of that fixed syntactic tree, including the root
and all terminal leaves.

An admissible proposal is a probability measure $Q$ with $|\nu|\ll Q$,
and its single-tree likelihood estimator is
\[
 H=\frac{d\nu}{dQ}.
\]
Auxiliary proposal randomness can be included in $\Omega$ and its
likelihood contract. Recombining different trees, analytic summation,
changing representation, or using a control variate is outside this
fixed-integrand assertion.

Define the cost-weighted absolute mass
\[
 S=\int_\Omega\sqrt N\,d|\nu|\in(0,\infty].
\]

**Proposition.** Every admissible $Q$ satisfies
\[
 \bigl(\mathbb E_Q H^2\bigr)\bigl(\mathbb E_Q N\bigr)\geq S^2.
 \tag{CW}
\]
In particular, $S=\infty$ rules out simultaneous finite second moment
and finite expected cost. Conversely, if $S<\infty$, an ideal global
proposal with both quantities finite exists, and equality in (CW) is
attained.

**Proof.** Total variation of a Radon–Nikodym density gives
$d|\nu|=|H|\,dQ$. Therefore
\[
 S=\mathbb E_Q[|H|\sqrt N]
 \leq(\mathbb E_QH^2)^{1/2}(\mathbb E_QN)^{1/2}.
\]
The assertion with an infinite integral follows by truncation, or by
the contrapositive of Cauchy–Schwarz with both moments finite.

If $S<\infty$, set
\[
 Z_N=\int_\Omega N^{-1/2}\,d|\nu|,\qquad
 dQ_*=\frac{N^{-1/2}}{Z_N}\,d|\nu|.
\]
The assumptions imply $0<Z_N\leq W<\infty$. Writing
$\sigma=d\nu/d|\nu|$, with $|\sigma|=1$ almost everywhere, gives
\[
 H_*=\sigma Z_N\sqrt N,\qquad
 \mathbb E_{Q_*}N=\frac S{Z_N},\qquad
 \mathbb E_{Q_*}H_*^2=Z_NS.
\]
Both moments are finite and their product is $S^2$.

If the proposal contract additionally demands support on syntactic
trees of zero $\nu$-weight, $Q_*$ need not have that extra support.
Provided an admissible full-support reference proposal $Q_0$ with
finite mean cost exists, the mixture
$Q_\theta=(1-\theta)Q_*+\theta Q_0$, $0<\theta<1$, has that support,
finite mean cost, and
\[
 \mathbb E_{Q_\theta}H_\theta^2
 \leq\frac1{1-\theta}\mathbb E_{Q_*}H_*^2<\infty.
\]
This establishes existence with the extra support condition, although
the equality optimum may be lost. $\square$

The optimality above concerns the product of second moment and mean
cost. It is not a claimed optimum of variance times cost, which
subtracts the mean squared. At a fixed finite mean, finiteness of
variance is equivalent to finiteness of second moment, so the
impossibility consequence applies to both.

$Q_*$ is a probability-law existence result, not an implementable
algorithm. Its normalization and conditionals require global
cost-weighted absolute tree information. Their computation could be
as difficult as the original problem.

### A finite-$L^1$ critical endpoint with no simultaneous $L^2$/work bound

Take the original derivative-coded constant-profile example
\[
 f(y)=\frac1{1+y^2},\qquad r=0,\qquad \tau=\frac23.
\]
The terminal absolute jet generating function is
$\Phi(z)=(1-z^2)^{-1}$. The audited result in 04d gives
\[
 W_I(t)=Z(t),\qquad
 t=Z(t)-\frac{Z(t)^3}{3},\quad 0\leq t<\tau,\qquad
 Z(\tau)=1.
\]
The symbol $Z$ in this subsection denotes this scalar majorant,
not a normalized random return and not the normalizer $Z_N$ above.

Group nonzero completed tree terms by their number $n$ of internal
vertices. Integrating the time simplexes and the irrelevant spatial
coordinates gives nonnegative coefficients $c_n$ such that
\[
 Z(t)=\sum_{n\geq1}c_nt^n,\qquad
 \sum_{n\geq1}c_n\tau^n=1.
 \tag{S}
\]
The coefficient is a total absolute weight at that size, before any
signed cancellation. Identity (S) follows from the finite-tree
power-series construction and monotone endpoint passage in 04d.

The node count must be fixed explicitly. A nonzero Id tree cannot
terminate at its root because $r=0$. Its root has one child $F_0$.
Every nonzero internal reaction-code vertex uses the binary mechanism
$F_k\to(F_0,F_{k+1})$. All spatial-derivative terminal values are
zero, so every tree containing a gradient mechanism has zero weight.
If there are $n$ internal vertices in total, the reaction subtree has
$n-1$ binary internal vertices and $n$ leaves. Including the Id root,
\[
 N=1+(n-1)+n=2n
 \quad\text{on every nonzero tree.}
 \tag{N}
\]
Consequently the proposition's cost-weighted mass at $\tau$ is
\[
 S=\sqrt2\sum_{n\geq1}\sqrt n\,c_n\tau^n.
 \tag{M}
\]

For every integer $n\geq1$,
\[
 \sqrt n=\frac1{2\sqrt\pi}
 \int_0^\infty(1-e^{-ns})s^{-3/2}\,ds.
 \tag{F}
\]
Indeed, substitute $r=ns$ and integrate by parts to obtain
$\int_0^\infty(1-e^{-r})r^{-3/2}\,dr
=2\int_0^\infty e^{-r}r^{-1/2}\,dr=2\sqrt\pi$.
All summands are nonnegative, so Tonelli and (S) give
\[
 \sum_{n\geq1}\sqrt n\,c_n\tau^n
 =\frac1{2\sqrt\pi}\int_0^\infty
       [Z(\tau)-Z(\tau e^{-s})]s^{-3/2}\,ds.
 \tag{FM}
\]
No estimate on individual coefficients and no Tauberian theorem is
used.

Let $z=Z(t)\in[0,1]$. The exact cubic identity factors as
\[
 \tau-t=\frac{(1-z)^2(2+z)}3.
\]
Since $2+z\leq3$,
\[
 1-Z(t)\geq\sqrt{\tau-t}.
\]
For $0<s\leq1$, $1-e^{-s}\geq s/2$, and hence
\[
 Z(\tau)-Z(\tau e^{-s})
 \geq\sqrt{\tau(1-e^{-s})}
 \geq\sqrt{\tau/2}\,\sqrt s.
\]
The integral in (FM) therefore dominates a positive constant times
$\int_0^1s^{-1}\,ds=\infty$. Equations (M) and (CW) prove:

> At $t=2/3$, the canonical first absolute Id moment is one, but no
> supported likelihood proposal for the same completed-tree measure
> has both finite second moment and finite expected full syntactic
> node count.

This also rules out both properties at any earlier time only if the
corresponding cost-weighted mass is infinite there; the argument above
claims the critical endpoint specifically. The signed physical ODE,
$u+u^3/3=t$, is global and does not blow up at this endpoint.

The scope of cost is material. Removing zero-weight gradient trees
does not remove the obstruction: they contribute nothing to $S$,
and the nonzero trees still satisfy (N). On those trees, counting
reaction internal vertices, leaves, or root-to-leaf expansion work
remains comparable to $n$ and gives the same divergence. The theorem
does not cover a method that analytically resums whole subtrees,
reuses repeated factors instead of visiting all syntactic vertices,
or changes the tree representation. Calling such a different cost
“node count” would change the proposition's premise.

### Short extension: an exact output-moment/work threshold

The same argument gives a continuous family of critical-endpoint
thresholds. Fix $\alpha>0$ and
\[
 f_\alpha(y)=(1+y^2)^{-\alpha},\qquad r=0.
\]
The even Taylor coefficients alternate in sign and have positive
absolute values. Thus
\[
 \Phi_\alpha(z)=(1-z^2)^{-\alpha},\qquad
 \tau_\alpha=\int_0^1(1-z^2)^\alpha\,dz,\qquad
 W_I(\tau_\alpha)=1.
\]
The nonzero-tree count remains $N=2n$. Write $Z_\alpha(t)=W_I(t)$
for $t\leq\tau_\alpha$. For
$\delta=1-Z_\alpha(t)\in[0,1]$,
\[
 \tau_\alpha-t
 =\int_0^\delta [r(2-r)]^\alpha\,dr.
\]
Since $r\leq r(2-r)\leq2r$ on $[0,1]$,
\[
 \frac{\delta^{\alpha+1}}{\alpha+1}
 \leq\tau_\alpha-t
 \leq\frac{2^\alpha\delta^{\alpha+1}}{\alpha+1}.
 \tag{Cusp}
\]
Consequently $1-Z_\alpha(\tau_\alpha e^{-s})$ is bounded above
and below by positive multiples of $s^\gamma$ for $0<s\leq1$,
where $\gamma=1/(\alpha+1)$.

For any real $p>1$, put $\beta=(p-1)/p$ and
$S_p=\int N^\beta\,d|\nu|$. Hölder gives
\[
 \bigl(\mathbb E_Q|H|^p\bigr)
       \bigl(\mathbb E_QN\bigr)^{p-1}\geq S_p^p.
 \tag{Hp}
\]
If $S_p<\infty$, let
\[
 Z_p=\int N^{-1/p}\,d|\nu|,\qquad
 dQ_p=Z_p^{-1}N^{-1/p}\,d|\nu|.
\]
Then $\mathbb E_{Q_p}N=S_p/Z_p$ and
$\mathbb E_{Q_p}|H_p|^p=Z_p^{p-1}S_p$, so both moments are
finite and equality holds in (Hp). The same reference-law mixture
restores any additional zero-weight support requirement; its
$p$th-moment bound incurs at most a factor $(1-\theta)^{1-p}$.

The fractional identity, proved by the same substitution and
integration by parts as (F), is
\[
 n^\beta=\frac{\beta}{\Gamma(1-\beta)}
 \int_0^\infty(1-e^{-ns})s^{-1-\beta}\,ds.
\]
Apply Tonelli to the positive time-power series for $Z_\alpha$.
The integral over $s\geq1$ is finite because its difference term is
at most one. By (Cusp), its integral near zero is finite exactly
when $\int_0^1s^{\gamma-\beta-1}\,ds$ is finite. Therefore
\[
 S_p<\infty
 \quad\Longleftrightarrow\quad
 \gamma>\beta
 \quad\Longleftrightarrow\quad
 1<p<1+\frac1\alpha.
 \tag{Threshold}
\]
Equality at the upper threshold gives logarithmic divergence.
In particular, simultaneous finite variance and finite mean syntactic
work is possible at the level of an ideal global probability law
exactly when $0<\alpha<1$. It is impossible when $\alpha\geq1$,
despite $W_I(\tau_\alpha)=1$ throughout the family.

This is a conventional extension of the displayed proofs. Existence
of $Q_p$ does not prove that its conditionals can be computed or
sampled from the allowed local oracles. Full syntactic work and the
fixed completed-tree likelihood measure remain essential premises.

## 6. At most two substantive next questions

### Question 1 — classify the loss caused by the derivative coding

For the fixed family $f(u)=-u^p$, integer $p\geq2$, and small positive
Gaussian initial profiles on $\mathbb R^d$, determine the sharp
dimension/data criterion for all-horizon absolute integrability of
the original derivative-coded Id tree. Compare it with the scalar
$p$-ary representation, not merely with a poorly chosen raw proposal.

The strong baseline is already explicit. Its scalar envelope amplitude
satisfies
\[
 m'=m^p w^{p-1},\qquad
 m(0)=\epsilon,
\]
so it is global for sufficiently small $\epsilon$ whenever
$d(p-1)>2$. Its total event probability can then be made less than
$1/p$, giving a horizon-independent expected-size bound by a
$p$-ary Galton–Watson comparison.

For the derivative hierarchy, the reaction-only subsystem is
\[
 (\partial_t-L)A_k=A_0A_{k+1},\quad 0\leq k<p,
 \qquad A_p=p!.
\]
Its homogeneous scaling weights are
$\alpha_k=(p-k)/(p-1)$. The candidate threshold suggested by the
largest weight is $d=2p/(p-1)$; for $p=2$ the T15 proof establishes
the corresponding $d=4$ boundary. For $p>2$ this is a conjectural
guide, not a proved criterion. The gradient mechanisms, critical
dimensions and propagation to Id all still need proof. The mixed
system literature must be checked before any priority claim.

This question studies a structural limitation of the representation.
It does not seek a faster solver for scalar polynomial absorption,
where the simpler baseline already has the advantage.

### Question 2 — characterize attainable variance/work tradeoffs

For a fixed signed completed-tree measure, the proposition gives an
exact existence criterion for a global proposal with finite variance
and finite mean cost:
\[
 \int\sqrt N\,d|\nu|<\infty.
\]
The nontrivial next question is whether, and with what overhead, that
criterion can be realized by locally sampled branching controls using
only specified terminal-value/jet oracles and computable envelopes,
without access to the full solution or the global tree normalizer.

The benchmark must be the ideal law $Q_*$ from Section 5, with
standard Cauchy–Schwarz optimality acknowledged. A useful result would
give a verifiable class in which local controls attain a uniform
constant factor of its second-moment/work product, or prove that no
such factor is possible under a precise local-control restriction.
It must charge envelope construction and any preprocessing instead
of treating a solution-dependent control as free.

The rational critical endpoint is a fixed negative test: no local
control can overcome its infinite cost-weighted absolute mass while
preserving that tree measure and syntactic work. Below the endpoint,
or for other analytic terminal-jet majorants with finite boundary
mass, the sharp cost-weighted criterion and constructive attainability
remain meaningful targets. Neither a scalar representation for a
different measure nor a finite-sample success can settle this
fixed-representation question.

## 7. Required wording in the parent synthesis

Attribute the general transform/majorant/subcritical-tree method to
the existing literature, with Ossiander as the closest fully inspected
source. Describe the 112-node result as an explicit ideal certificate
for the specified derivative-code closure. Put the scalar binary and
heat-flow baselines alongside it. Do not infer runtime superiority
from upper bounds, or general PDE novelty from the $d=4$ application.

Keep four separate claims: first absolute tree mass, second moment,
expected syntactic work, and signed PDE correspondence. The endpoint
proposition makes their separation necessary even for constant data.
Its proof is conventional and complete under the displayed
fixed-measure/cost contract; its publication novelty and practical
local-control implications remain unestablished.
