# T22 — independent audit of the critical moment/work frontier

Decision: **PASS for the conventional mathematical theorem**, with the
endpoint-domain clarification below. There is no implementation or
publication-priority conclusion.

Source reviewed: 04h-critical-moment-work.md, 142 lines, SHA256
b2ae865b8a8c8b4e2861b5fb251ad712fe2ddc69cc4d647cbfb9441eb5174da5.
The proof agrees with the independently derived proposition in the
frozen T19 review. T13 supplies the finite-tree/constant-majorant
endpoint result. This audit writes only this review.

## 1. Exact theorem that passes

For the original derivative-coded completed-tree measure at constant
zero datum and
\[
 f_\alpha(y)=(1+y^2)^{-\alpha},\qquad \alpha>0,
\]
let
\[
 \tau_\alpha=\int_0^1(1-z^2)^\alpha\,dz.
\]
At $t=\tau_\alpha$, canonical Id total variation is one. For any real
$p>1$, an arbitrary global tree proposal supporting that measure and
returning its exact single-tree likelihood can have both
\[
 \mathbb E|H|^p<\infty,\qquad \mathbb E N<\infty
\]
if and only if
\[
 1<p<1+\frac1\alpha.
\]
Here $N$ is the full syntactic node count for that fixed tree
representation. The existence direction concerns a probability law
whose global normalizer and conditionals are available in principle;
the theorem does not yet construct a local sampling algorithm.

For $p=2$, the sharp condition is $0<\alpha<1$. The equality
$p=1+1/\alpha$ is excluded by a logarithmic divergence. This strict
boundary is essential.

## 2. The measure and optimization argument

Write $\mu=|\nu|$ and assume $\nu\ne0$, $\mu(\Omega)<\infty$,
and $1\leq N<\infty$ $\mu$-almost everywhere. These premises hold on
the canonical space of completed finite trees here. An admissible
proposal is a probability $Q$ with $\mu\ll Q$ and output
$H=d\nu/dQ$.

Because $d\mu=|H|\,dQ$, Hölder with conjugate exponents
$p$ and $p/(p-1)$ gives
\[
 S_p:=\int N^{(p-1)/p}\,d\mu
 =\mathbb E_Q[|H|N^{(p-1)/p}]
 \leq(\mathbb E_Q|H|^p)^{1/p}
      (\mathbb E_QN)^{(p-1)/p}.
\]
This covers every full joint likelihood proposal, including adaptive
choices, provided the final joint Radon–Nikodym contract holds.
There is no need for the proposal's children to be independent in
this argument.

If $S_p<\infty$, define
\[
 Z_p=\int N^{-1/p}\,d\mu,\qquad
 Q_*(d\omega)=Z_p^{-1}N(\omega)^{-1/p}\mu(d\omega).
\]
The assumptions imply $0<Z_p<\infty$. Since $|\sigma|=1$
$\mu$-almost everywhere for $\sigma=d\nu/d\mu$,
\[
 H_*=\sigma Z_pN^{1/p},\qquad
 \mathbb E_{Q_*}N=S_p/Z_p,\qquad
 \mathbb E_{Q_*}|H_*|^p=Z_p^{p-1}S_p.
\]
Thus the displayed inequality is attained as a product of $p$th
absolute moment and mean cost. This does not assert that the same
law minimizes variance times mean cost.

The zero measure is a harmless separate case: output zero under any
finite-mean-cost completing proposal. It must be excluded only when
dividing by $Z_p$.

### Full syntactic support can be restored here

In a general abstract tree model, the mixture argument should be
conditional on existence of a full-support reference law $Q_0$ with
finite mean cost. The original coding mechanism does supply one.
Use independent rate-one exponential lifetimes and positive
probabilities for every available label, with the original heat
transitions. Offspring count is at most three. For a finite horizon
$t$, the expected living population is at most $e^{2t}$, and the
expected total number of vertices is bounded by
\[
 1+3\int_0^t e^{2s}\,ds
 =1+\frac32(e^{2t}-1)<\infty.
\]
This also gives almost-sure finite completion. Positive label
probabilities and positive heat/event-time densities provide the
needed support, even though terminal weights may be zero or very
large.

For $Q_\theta=(1-\theta)Q_*+\theta Q_0$, $0<\theta<1$,
\[
 \mathbb E_{Q_\theta}|H_\theta|^p
 \leq(1-\theta)^{1-p}\mathbb E_{Q_*}|H_*|^p,
\]
while mean cost is the finite corresponding mixture. Extra support
therefore changes neither side of the existence criterion in this
specific code family.

## 3. Terminal jets, endpoint mass and the precise ODE domain

The Taylor coefficients at zero are
\[
 f_\alpha^{(2k)}(0)
 =(-1)^k(2k)!\frac{(\alpha)_k}{k!},\qquad
 f_\alpha^{(2k+1)}(0)=0,
\]
where $(\alpha)_k>0$ is the rising factorial. Therefore
\[
 \sum_{j\geq0}\frac{|f_\alpha^{(j)}(0)|}{j!}z^j
 =\sum_{k\geq0}\frac{(\alpha)_k}{k!}z^{2k}
 =(1-z^2)^{-\alpha},\qquad 0\leq z<1.
\]
The radius is one, and the audited constant-profile theorem gives
$W_I(\tau_\alpha)=1$. Substitution $r=z^2$ also confirms
\[
 \tau_\alpha
 =\frac12 B(1/2,\alpha+1)
 =\frac{\sqrt\pi\,\Gamma(\alpha+1)}
        {2\Gamma(\alpha+3/2)}.
\]

The draft should explicitly write
\[
 Z_\alpha'=(1-Z_\alpha^2)^{-\alpha}
 \quad\text{for }0\leq t<\tau_\alpha,
 \qquad Z_\alpha(\tau_\alpha):=1
\]
by continuous extension. The derivative is not finite at the
endpoint. Only $W_I=Z_\alpha$ and its continuous extension are
asserted on the closed interval. This removes the one potentially
misleading domain reading of the displayed formulas.

No finiteness of all reaction-code moments at the endpoint is used.
For example the absolute $F_0$ majorant tends to infinity there.
The finite Id moment is consistent with that divergence because Id
integrates the reaction contribution in time.

## 4. Node count, time degree and total variation

On every nonzero completed Id tree, the zero terminal datum forces a
unary root event $I\to F_0$. A spatial-derivative subtree always has
a zero spatial-derivative leaf. Thus any gradient event has zero
completed-tree weight and is absent from the support of $\mu$.

Every other internal vertex in a nonzero tree has two children.
If the number of internal vertices is $n$, the number of edges is
$1+2(n-1)=2n-1$, hence the full node count is exactly $2n$.
Equivalently, there are $n$ leaves. This count includes terminal
reaction-code leaves, not only event vertices.

For a fixed such tree, all terminal factors are constants, all
Brownian transition integrals are one, and its event-time domain
scales by $t^n$. The heat motion must be conservative, as it is on
the flat torus and on $\mathbb R^d$ in the project setting. A killed
boundary problem would require a different argument.

Grouping by $n$ gives a nonnegative series
\[
 Z_\alpha(t)=\sum_{n\geq1}c_nt^n,\qquad
 \sum_{n\geq1}c_n\tau_\alpha^n=1.
\]
For a fixed $n$, only finitely many reaction-code orders and tree
shapes contribute; the terminal derivatives used are finite.
These are absolute weights before cancellation between differently
signed trees. Thus
\[
 S_p=2^\beta\sum_{n\geq1}n^\beta c_n\tau_\alpha^n,
 \qquad\beta=(p-1)/p.
\]
This bridge is exact. It does not differentiate an infinite endpoint
expectation or identify total variation after signed summation.

Removing zero-weight trees has no effect on this obstruction.
Counting only internal vertices or leaves on a nonzero tree also
gives a cost comparable to $n$. Analytic resummation, factor reuse,
or a different representation can change the cost or signed
measure and is not covered by the conclusion.

## 5. Fractional-moment test and strict boundary

Put $\delta=1-Z_\alpha(t)$. Directly,
\[
 \tau_\alpha-t
 =\int_0^\delta [r(2-r)]^\alpha\,dr.
\]
For $0\leq r\leq1$, $r\leq r(2-r)\leq2r$, so
\[
 \frac{\delta^{\alpha+1}}{\alpha+1}
 \leq\tau_\alpha-t
 \leq\frac{2^\alpha\delta^{\alpha+1}}{\alpha+1}.
\]
Hence, with $\gamma=1/(\alpha+1)$, there are finite positive
constants bounding
$1-Z_\alpha(\tau_\alpha e^{-s})$ above and below by $s^\gamma$
for $0<s\leq1$.

For $0<\beta<1$, substitution and integration by parts prove
\[
 n^\beta=\frac{\beta}{\Gamma(1-\beta)}
          \int_0^\infty(1-e^{-ns})s^{-1-\beta}\,ds.
\]
The boundary terms vanish because $\beta\in(0,1)$.
Tonelli is applicable to the nonnegative series, giving
\[
 \sum_{n\geq1}n^\beta c_n\tau_\alpha^n
 =\frac{\beta}{\Gamma(1-\beta)}
   \int_0^\infty
       [1-Z_\alpha(\tau_\alpha e^{-s})]s^{-1-\beta}\,ds.
\]
For $s\geq1$, the bracket is at most one, so the tail is finite.
For $s\downarrow0$, the integrand is comparable to
$s^{\gamma-\beta-1}$. Its integral is finite exactly for
$\gamma>\beta$, and equality gives a logarithmic divergence.
Since $\alpha>0$ and $p>1$,
\[
 \frac{p-1}{p}<\frac1{\alpha+1}
 \quad\Longleftrightarrow\quad
 \alpha(p-1)<1
 \quad\Longleftrightarrow\quad
 p<1+\frac1\alpha.
\]
Every endpoint inequality in the draft has the correct direction.
No coefficient asymptotic or Tauberian result is being hidden.

## 6. Signed ODE correspondence can also be closed

The moment/work theorem itself concerns $\nu$ and does not need
its integral to be the physical solution. If the synthesis describes
the likelihood estimator as an estimator of $u(\tau_\alpha)$, the
following short argument supplies that additional identification.

The signed physical ODE has a unique global solution because
$f_\alpha$ is smooth and $0<f_\alpha\leq1$ on the real line.
Near zero it is real analytic. Its formal derivative family
$S_k=f_\alpha^{(k)}(u)$ satisfies
\[
 S_k'=S_0S_{k+1},\quad
 S_k(0)=f_\alpha^{(k)}(0),\quad
 u'=S_0,\quad u(0)=0.
\]
The coefficient of degree $m+1$ on the left is determined by
coefficients of degree at most $m$ on the right. Induction in degree
therefore uniquely determines these formal coefficients, even though
the code family is infinite. The finite-tree coefficient recursion is
the same one.

The absolute majorant series converges for $|t|<\tau_\alpha$, so the
signed Id series is analytic there and agrees with the physical
analytic ODE solution near zero. It agrees throughout
$[0,\tau_\alpha)$ by analytic continuation, or by the local ODE
identity and uniqueness. No boundedness of an infinite derivative
family in an unweighted sequence norm is required.

At the endpoint, the absolute coefficient sum is one. Dominated
convergence for the signed coefficient series gives
\[
 \int d\nu_{\tau_\alpha}
 =\lim_{t\uparrow\tau_\alpha}\int d\nu_t
 =\lim_{t\uparrow\tau_\alpha}u(t)
 =u(\tau_\alpha).
\]
The first limit can equivalently be taken tree by tree after scaling
the time simplexes to a common unit-time tree space. This avoids
assuming any reaction-code integrability at $\tau_\alpha$.

Thus the impossibility result is meaningful even for a globally
well-behaved signed ODE. It is an obstruction to this fixed
likelihood representation and cost, not to the ODE solution.

## 7. Immediate corollaries and the formalization boundary

For every $\alpha>0$, a bounded output and finite mean full-tree
work cannot coexist at the critical endpoint: a bounded output
would have every finite $p$th moment, contradicting the theorem
for $p\geq1+1/\alpha$.

In particular, when $0<\alpha<1$, abstract finite-variance/finite-work
proposals exist, but they cannot also have a deterministic finite
output bound. The normalized absolute law $Q=\mu$ gives the bounded
output $H=\sigma$ here, yet has infinite mean node count.
Indeed,
\[
 \mathbb E_\mu N
 =2\sum_{n\geq1}n c_n\tau_\alpha^n
 =\infty,
\]
because $Z_\alpha'(t)$ diverges as $t\uparrow\tau_\alpha$ and
the derivative series has nonnegative coefficients.

The smallest useful subsequent Lean gate is the exact exponent
equivalence under $\alpha>0,p>1$. A stronger honest gate would
formalize the Hölder inequality and the explicitly defined optimal
law under all measure/cost hypotheses. Proving only the exponent
algebra does not formalize the tree measure, $N=2n$, endpoint
series passage, or the signed ODE correspondence.

The parent can freeze the conventional theorem after adding the
subcritical-time domain for the majorant differential equation.
Any later constructive sampler must separately establish its
joint law, normalizer treatment, completion, expected work and
arithmetic/oracle contract. Those claims are not consequences of
probability-law existence alone.
