# T26 — independent audit of the critical tilted sampler

Decision: **PASS as an ideal exact-oracle construction**, with the
finite-tree completion proof supplied in Section 3. No finite expected
arithmetic/bit-cost claim follows. No code, Lean or numerical experiment
was run.

Reviewed source: 04i-critical-tilted-sampler.md, 142 lines, SHA256
2dbcdd7353f194de5abe853f7b06c6cf0a7183bead8719e3043366931931f715.
That version already incorporates the spatial-mark and higher-cost
clarifications communicated during this audit. T19 and T22 are frozen.
The new historical references in 04i were supplied and inspected by root;
this audit concerns the mathematics and does not extend that literature
search or assert priority.

## 1. The exact object and its reduction

Fix $\alpha>0$, $p>1$, and
\[
 \Phi(z)=(1-z^2)^{-\alpha},\quad
 F(z)=\int_0^z(1-y^2)^\alpha\,dy,\quad
 \tau=F(1),\quad Z=F^{-1},\quad a=1/p.
\]
The function $Z$ is continuously defined on $[0,\tau]$; its
differential equation $Z'=\Phi(Z)$ is used only for $t<\tau$.
We have $0<\tau<1$.

Let $\nu_\tau$ be the signed scalar topology-and-time measure of
nonzero completed Id trees for constant zero datum and
$f_\alpha(y)=(1+y^2)^{-\alpha}$. Put $\mu=|\nu_\tau|$.
The audited constant-profile theorem gives $\mu(\Omega)=1$.
On a tree with $n$ internal events,
\[
 N=2n\geq2.
\]
The sign $\sigma=d\nu_\tau/d\mu$ has magnitude one and is the product
of its nonzero terminal derivative signs.

Integrating the irrelevant Brownian marks is legitimate here:
conditional on a scalar tree, its terminal signs, magnitudes and
node count do not depend on those marks, and the conservative
heat-kernel factor integrates to one. Thus this particular
pushforward preserves total variation as well as signed mass.
Total variation need not commute with a general pushforward; the
constant-sign-on-each-fibre property is what makes it valid here.

For a proposal on the fully spatially marked tree, attach the
conditional heat marks along the final rescaled edges. Merely
rescaling event times while retaining the old spatial positions
would be incorrect. This issue is corrected in the reviewed source.

The sampler supports every nonzero contribution. It does not
sample every syntactically possible zero-weight gradient tree.
That is consistent with the contract $|\nu|\ll Q$. A stronger
contract demanding all zero-weight labels needs an additional
support construction rather than a change in terminology.

## 2. All subcritical recursive probabilities are valid

For $0<t<\tau$, define
\[
 M_I(t)=Z(t),\qquad M_k(t)=\Phi^{(k)}(Z(t)),\qquad
 a_k=M_k(0).
\]
These are the minimal canonical absolute masses, not just an
arbitrary solution of an infinite ODE system. Their identification
follows from the monotone terminal-jet truncation in T13: finite
polynomial chains converge to $\Phi^{(k)}(Z(t))$ inside the radius
one of the terminal-jet series. On a compact subcritical time
interval all derivatives of that power series converge uniformly
on a slightly larger compact interval of $z<1$.

The Id root has zero terminal mass. Its branch density in remaining
time $s\in(0,t)$ is $M_0(s)/Z(t)$, whose cumulative distribution is
$Z(s)/Z(t)$. Hence the inverse
\[
 s=F(UZ(t)),\qquad U\in(0,1),
\]
is correct.

For code $F_k$,
\[
 M_k(t)=a_k+\int_0^t M_0(s)M_{k+1}(s)\,ds.
\]
Consequently its terminal probability is $a_k/M_k(t)$, and
its unconditional branch-time density is
\[
 \frac{M_0(s)M_{k+1}(s)}{M_k(t)}
 =\frac{M_k'(s)}{M_k(t)}.
\]
The source's single-uniform terminal/inversion rule realizes these
probabilities exactly, with no missing survival term. Following a
branch, independently sampling $F_0$ and $F_{k+1}$ realizes the
product in the positive mild law.

Every $M_k(t)>0$ when $t>0$. For odd $k$, $a_k=0$ and terminal
selection has probability zero. For even $k$, $a_k>0$.
On a branch, $UM_k(t)>a_k$, so the inverse is strictly inside
$(0,t)$. Use uniforms in $(0,1)$; the null events at their endpoints
need no arbitrary division by a zero mass.

The inverse is well-defined because $\Phi^{(k+1)}(z)>0$ for
$0<z<1$. The possible zero derivative at $z=0$ for even $k$
does not affect the interior inverse. Equivalently, solve
$\Phi^{(k)}(y)=UM_k(t)$ for $0<y<Z(t)$ and then set $s=F(y)$.
The algorithm never requests a normalized Id law at $t=0$.

The finite-polynomial derivative formula also checks out. If
$P_k(z)=\sum_{j=0}^k b_jz^j$ with $b_j\geq0$, then
\[
 P_{k+1}(z)
 =\sum_{j=1}^k j b_j z^{j-1}
  +\sum_{j=0}^k[2(\alpha+k)-j]b_jz^{j+1}.
\]
Every displayed coefficient is nonnegative, and
$2(\alpha+k)-j\geq2\alpha+k>0$. Thus
$\Phi^{(k)}(z)=P_k(z)(1-z^2)^{-\alpha-k}$ has the stated
explicit form. This verifies a finite expression, not a
constant-cost derivative evaluation for unbounded $k$.

## 3. Completion without a circular integrability assumption

The source says that the recursive process must be identified with
the completed-tree measure. The following argument closes that step.

Construct the recursive process from the displayed probability
kernels, provisionally allowing an infinite tree. For any specified
finite completed tree, multiply its terminal probabilities and its
internal event-time densities. Each internal numerator contains the
two child masses. They cancel the denominators contributed by those
children. At the root, the remaining denominator is $M_k(t)$ for
an $F_k$ tree or $Z(t)$ for an Id tree.

The resulting density is exactly the product of terminal absolute
jets, times the original ordered event-time measure, divided by
the appropriate root canonical mass. In other words, it is the
canonical absolute density of that finite tree normalized by its
total mass. This calculation concerns only finite products and
does not presuppose completion.

The union over all finite completed tree shapes has probability
one, because its nonnegative canonical mass is exactly the root
mass used to normalize it. Tonelli and completed-tree exhaustion
justify this sum. Thus the recursive process completes almost
surely. Decreasing remaining times alone would not prove this.

For Id, write $Z(t)=\sum_{n\geq1}c_nt^n$ with $c_n\geq0$.
The now-identified law has
\[
 \mathbb E_tN
 =\frac{2\sum_{n\geq1}nc_nt^n}{Z(t)}
 =\frac{2tZ'(t)}{Z(t)}<\infty,\qquad 0<t<\tau.
\]
Differentiation is inside the convergence radius; no endpoint
derivative is being exchanged with an infinite expectation.
The clocks and children therefore have the required law, and
the finite-mean claim is not being used to assume that law.

## 4. Gamma rejection and the time-rescaling density

The function $Z$ is convex, $Z(0)=0$, $Z(\tau)=1$, and
$Z'(t)\geq1$ for $t<\tau$. Thus
\[
 t\leq Z(t)\leq t/\tau,\qquad 0\leq t\leq\tau.
\]
For $S\sim\operatorname{Gamma}(a,\text{rate }2)$, set
\[
 t(S)=\tau e^{-2S},\qquad
 A(S)=e^{2S}Z(t(S)).
\]
Then $\tau\leq A(S)\leq1$. Rejection sampling is well-defined
and has expected proposal count at most $1/\tau$.
Also $0<t(S)<\tau$ almost surely.

Let $R_t$ scale the remaining event times of a horizon-$t$
scalar tree by $\tau/t$. The correct measure identity is
\[
 \frac{d(R_t)_*|\nu_t|}{d\mu}(\omega)
 =(t/\tau)^{n(\omega)}.
\]
Indeed each of the $n$ event-time coordinates contributes one
factor $t/\tau$ when the integration variables are rescaled.
Terminal factors and the partial-order domain are otherwise
unchanged. Since $N=2n$, for $t=t(S)$ this factor is $e^{-SN}$.

Define
\[
 Z_p=\int N^{-a}\,d\mu.
\]
It is finite and strictly positive. From the nonnegative time
series, equivalently from the preceding measure identity,
\[
 Z(\tau e^{-2s})=\int e^{-sN}\,d\mu.
\]
The acceptance probability is therefore exactly
\[
 \begin{aligned}
 r_a
 &=\frac{2^a}{\Gamma(a)}
   \int_0^\infty s^{a-1}Z(\tau e^{-2s})\,ds\\
 &=2^a\int N^{-a}\,d\mu=2^aZ_p.
 \end{aligned}
\]
All interchanges are Tonelli interchanges. In particular
$r_a\in[\tau,1]$ and
$2^{-a}\tau\leq Z_p\leq2^{-a}$.

Given accepted $S=s$, the rescaled normalized subcritical tree has
density $e^{-sN}/Z(\tau e^{-2s})$ relative to $\mu$.
Combining it with the accepted gamma density gives the joint law
\[
 Q(ds,d\omega)
 =\frac{s^{a-1}e^{-sN(\omega)}}{\Gamma(a)Z_p}\,ds\,\mu(d\omega).
\]
Integrating out $s$ proves
\[
 Q_*(d\omega)=Z_p^{-1}N(\omega)^{-a}\mu(d\omega).
\]
This verifies both the factor two in the gamma rate and the
factor $2^{-a}$ needed later. There is no hidden use of $Z_p$
by the rejection sampler.

The resulting tree is finite almost surely for every $p>1$:
condition on the accepted finite $S>0$ and apply Section 3.
Its mean size can be infinite outside the moment/work regime.
Almost-sure completion and finite expected work remain separate.

## 5. The independent normalization trial

Draw one fresh independent gamma proposal $S_0$ and one fresh
uniform to form $B\sim\operatorname{Bernoulli}(A(S_0))$
conditionally on $S_0$. This is a single trial, not rejection
sampling until it succeeds. It satisfies
\[
 \mathbb EB=r_a=2^aZ_p.
\]
It is independent of the accepted tilted tree. Hence for
\[
 \widehat Z_p=2^{-a}B,\qquad
 H_{\mathrm{new}}=\widehat Z_p\,\sigma N^a,
\]
we have, first, the finite absolute expectation
\[
 \mathbb E|H_{\mathrm{new}}|
 =2^{-a}r_a\mathbb E_{Q_*}N^a
 =Z_p\frac{\mu(\Omega)}{Z_p}=1.
\]
The signed factorization is consequently legitimate and gives
\[
 \mathbb EH_{\mathrm{new}}
 =\int \sigma\,d\mu=\int d\nu_\tau.
\]
T22 independently identifies this last integral with the global
signed ODE solution $u(\tau)$.

Because $ap=1$ and $B^p=B$,
\[
 \mathbb E|H_{\mathrm{new}}|^p
 =2^{a-1}S_p,\qquad
 \mathbb E_{Q_*}N=S_p/Z_p,\qquad
 S_p=\int N^{(p-1)/p}\,d\mu.
\]
These are also valid as extended nonnegative identities when
$S_p=\infty$. The T22 cusp test therefore proves the exact
coexistence condition $1<p<1+1/\alpha$.

The normalizer is bounded, but the final output is not bounded:
nonzero trees of arbitrarily large $N$ have positive probability,
and $B=1$ has positive probability. This is consistent with the
bounded-output obstruction in T22.

Reusing the accepting Bernoulli would set it equal to one and
inflate the signed mean by the factor $1/r_a$. Fresh randomness
ensures the displayed factorization; a coupling would require
a separate conditional-unbiasedness proof.

This output is not the original-tree likelihood pointwise.
Its conditional mean given the sampled tree is, however,
\[
 \mathbb E[H_{\mathrm{new}}\mid\omega]
 =Z_p\sigma(\omega)N(\omega)^a
 =\frac{d\nu_\tau}{dQ_*}(\omega).
\]
Conditional Jensen therefore supplies another check that the
extra randomization cannot evade the fixed-tree moment/work
obstruction.

The penalty relative to the ideal known-normalizer likelihood
is explicit:
\[
 \frac{\mathbb E|H_{\mathrm{new}}|^p}
      {\mathbb E|H_*|^p}
 =r_a^{1-p}\leq\tau^{1-p}
\]
when the moments are finite. The sampled-tree law and node work
are the same. This compares $p$th moments, not variances, and does
not charge implementation costs of scalar function evaluation.
There are at most $1/\tau+1$ gamma proposals in expectation
including the independent normalizer trial.

## 6. Higher work costs and oracle limitations

Write $\gamma=1/(\alpha+1)$. For the particular proposal above,
\[
 \mathbb E_{Q_*}N^q
 =Z_p^{-1}\int N^{q-1/p}\,d\mu.
\]
For any $q>0$ this is finite exactly when
$q-1/p<\gamma$; nonpositive exponents are automatically finite.
For exponents at least $\gamma$, divergence follows by
dominating the already divergent critical fractional moment.

The optimum-existence condition for cost $N^q$ across proposals
is a different statement:
\[
 \int N^{q(p-1)/p}\,d\mu<\infty
 \quad\Longleftrightarrow\quad
 q(p-1)/p<\gamma.
\]
Its ideal likelihood tilt is $N^{-q/p}$. The reviewed source
correctly distinguishes these tests after the audit clarification.
In particular, for actual cost comparable to $N^2$ and output
moment $p=2$, the optimal criterion already fails for every
$\alpha>0$, since $1\geq\gamma$.

As a purely algebraic extension, the same gamma construction can
use $a=q/p$ instead. Its conditional tree law is then proportional
to $N^{-q/p}\mu$, and the randomized normalization gives
\[
 \mathbb E|H_{\mathrm{new}}|^p
 =2^{-q(p-1)/p}\int N^{q(p-1)/p}\,d\mu,\qquad
 \mathbb E N^q
 =\frac{\int N^{q(p-1)/p}\,d\mu}
        {\int N^{-q/p}\,d\mu}.
\]
Thus the ideal scalar-oracle construction also realizes the
retuned abstract phase. This extension does not turn a
quadratic-cost obstruction into a feasible quadratic-cost
finite-variance algorithm.

The available claim is about exact distributional sampling and
expected syntactic nodes, or about numbers of unit-cost oracle
calls in an explicitly idealized model. It requires exact gamma
and uniform draws, values of $\tau$, $F$ and $Z$, arbitrary
$\Phi^{(k)}$ values, and their indicated monotone inverses.
The latter functions are explicit, so there is no circular use
of the unknown normalizer. Their numerical evaluation is still
real work.

In particular:

* An explicit polynomial of degree $k$ is not a fixed-cost oracle
  when code orders are unbounded.
* Near the critical endpoint, $F'$ becomes small. An inverse
  residual alone gives no uniform error in the sampled clock law.
* Very large gamma draws make both the numerator and denominator
  of $A(S)$ small. Direct floating-point division can fail even
  though the exact ratio lies in $[\tau,1]$.
* Finite-bit distributions, approximate special functions and
  approximate branch comparisons need their own bias and cost
  analysis. For a computability assertion, the representation of
  the real parameters must also be specified.

No expected arithmetic bound is supplied by the finite polynomial
recurrence. If a future implementation genuinely incurs a cost
bounded below by a constant times $N^2$, the preceding obstruction
is substantive. An $O(N^2)$ upper bound alone would not prove that
its expected cost is infinite; it would merely fail to certify
finiteness.

The physical signed ODE has its own deterministic scalar inverse
$t=\int_0^{u(t)}(1+y^2)^\alpha\,dy$. This remains the appropriate
simple baseline. The audited construction realizes a precise
representation frontier in an ideal oracle model and establishes
no competitive ODE-solver claim.

## 7. Corrections to integrate before freezing 04i

The core construction needs no coefficient or sign correction.
The spatial pushforward and the distinction between the actual
and retuned $N^q$ criteria are already present in the reviewed
version.

Replace the remaining sentence that completion “must be
identified” with the finite-tree telescoping/exhaustion proof
from Section 3. State the normalized subcritical law for
$0<t<\tau$ and the derivative equation for $t<\tau$.
These are proof/domain clarifications, not a proposed new
algorithm.

After those additions, the ideal mathematical construction can
be frozen. The next formal gate can check the gamma/Laplace
normalization and the independent-Bernoulli moment calculation
under explicit distributional hypotheses. Formalizing only
arithmetic identities must not be reported as formalizing
recursive completion or effective sampling.
