# An explicit heat-transform sampler for the quadratic code system

Status: conventional theory audited in T17; no implementation, numerical
experiment, or Lean result is claimed here. The supersolutions are those of
04e, independently checked in T15. This note proves the sampler and its cost,
and fixes a small formalization target before coding.

The ideal sampler is unbiased, has a deterministic output bound, and visits
at most 112 nodes in expectation, uniformly in the horizon. This concerns
the specified transformed and exactly reduced quadratic code system. It is
not the law of the original fixed-rate estimator. A simpler scalar binary
representation has substantially stronger bounds for this particular PDE;
Section 10 makes that comparison explicit.

## 1. The theorem and its input contract

Let \(d\) be an integer with \(d\geq5\), let \(0<\epsilon\leq1/32\), and
let \(v\in C^1(\mathbb R^d)\) satisfy, for every \(x\) and coordinate \(i\),

\[
 0\leq v(x)\leq\epsilon e^{-|x|^2/2},
 \qquad
 |\partial_i v(x)|\leq2\epsilon e^{-|x|^2/2}.
 \tag{1}
\]

The derivatives in (1) are continuous. These bounds imply that \(v\) and
its first derivatives are bounded and uniformly continuous. No radial
symmetry or second derivative of the datum is required. The example
\(v(x)=\epsilon e^{-|x|^2}\) belongs to this class.

Let \(u\) be the unique bounded nonnegative mild solution of

\[
 u_t=\tfrac12\Delta u-u^2,\qquad u(0,x)=v(x).
 \tag{2}
\]

For every finite \(T\geq0\) and \(x\in\mathbb R^d\), the algorithm below
defines an ideal real-valued estimator \(\widehat H_I(T,x)\) such that

\[
\begin{split}
 \mathbb E\widehat H_I(T,x)&=u(T,x),\\
 |\widehat H_I(T,x)|
 &\leq (\epsilon+C\epsilon^2T)G(T,x)\leq\epsilon
       \quad\hbox{almost surely},\\
 \mathbb E N_{\rm all}(T,x)&\leq112.
\end{split}
\tag{3}
\]

Here \(N_{\rm all}\) includes constant-code leaves, and the constants and
the kernel \(G\) are defined below. In particular, the tree is finite almost
surely, and for every real \(p>0\),

\[
 \mathbb E|\widehat H_I(T,x)|^p
 \leq [(\epsilon+C\epsilon^2T)G(T,x)]^p\leq\epsilon^p.
 \tag{4}
\]

The node bound is uniform over all allowed \(T,x,d,\epsilon,v\).
Arithmetic cost, bit precision and the cost of evaluating an arbitrary
input function are different quantities. The theorem uses exact real
uniform and Gaussian draws, exact terminal-value/first-derivative oracles,
and the unique real roots of explicit scalar monotone functions. Mere
membership in \(C^1\) is not a computability assumption on how \(v\) is
presented. If \(\epsilon=0\), (1) forces \(v=0\); the root returns zero
directly and all divisions below are bypassed.

## 2. Signed codes, closure and envelopes

Use the codes \(I,A,B,D_1,\ldots,D_d,F_2\), where the physical fields are
\[
 U=u,\quad A=-u^2,\quad B=-2u,\quad D_i=\partial_i u,\quad F_2=-2.
 \tag{5}
\]
The nonzero signed mechanisms are

| Parent | Ordered children | Scalar coefficient |
|---|---|---:|
| \(I\) | \(A\) | \(+1\) |
| \(A\) | \(A,B\) | \(+1\) |
| \(A\) | \(D_i,D_i,F_2\), for each \(i\) | \(-1/2\) |
| \(B\) | \(A,F_2\) | \(+1\) |
| \(D_i\) | \(B,D_i\) | \(+1\) |

The terminal values at time zero are \(v,-v^2,-2v,\partial_i v,-2\).
Every higher reaction code has zero completed-tree contribution. Integrate
the constant \(F_2\) code exactly, so its normalized return value is \(-1\)
under the envelope \(h_{F_2}=2\).

Set
\[
\begin{gathered}
 G(t,x)=(1+t)^{-d/2}\exp\{-|x|^2/[2(1+t)]\},\qquad
 w(t)=(1+t)^{-d/2},\\
 I_0(t)=\int_0^t w(s)\,ds,\qquad
 I_1(t)=\int_0^t s w(s)\,ds,\\
 I_0(\infty)=\frac2{d-2},\qquad
 I_1(\infty)=\frac4{(d-2)(d-4)},\qquad
 C=2+16dI_0(\infty),\\
 b(t)=2\epsilon+2C\epsilon^2t,\qquad
 J(t)=2\epsilon I_0(t)+2C\epsilon^2 I_1(t),\\
 J_\infty=2\epsilon I_0(\infty)+2C\epsilon^2 I_1(\infty),\\
 \delta(t)=2\epsilon e^{J(t)},\qquad
 a(t)=\epsilon^2+C\epsilon^2J(t)
       +4d\epsilon^2e^{2J_\infty}I_0(t).
\end{gathered}
\tag{6}
\]
The nonconstant envelopes \(h_c=m_cG\) use
\[
 m_I=b/2,\qquad m_A=a,\qquad m_B=b,\qquad m_{D_i}=\delta.
 \tag{7}
\]

The identities \((\partial_t-\Delta/2)G=0\) and \(G^2\leq wG\) are
direct. For completeness, the quantitative inequalities needed here are
\[
 C\leq166/3,\qquad J_\infty\leq107/576<1/4,\qquad
 a(t)\leq3C\epsilon^2/4<C\epsilon^2.
 \tag{8}
\]
Indeed \(I_0(\infty)\leq2/3\), \(I_1(\infty)\leq4/3\), and
\[
 J_\infty\leq1/24+83/576.
\]
Since \(e^{1/2}<2\) and \(C=2+16dI_0(\infty)\),
\[
 \frac{a(t)}{\epsilon^2}
 \leq1+C/4+8dI_0(\infty)=3C/4.
 \tag{9}
\]
All four amplitudes are strictly positive and increasing, and
\[
 a'\geq w(ab+d\delta^2),\qquad b'=2C\epsilon^2\geq2a,
 \qquad\delta'=wb\delta,\qquad m_I'=C\epsilon^2\geq a.
 \tag{10}
\]
For example,
\[
 a'=C\epsilon^2bw+4d\epsilon^2e^{2J_\infty}w
 \geq w(ab+d\delta^2).
\]
The terminal values are dominated by the corresponding \(h_c(0,\cdot)\).
In the \(A\) row use \(v^2\leq\epsilon^2G(0,\cdot)^2
\leq\epsilon^2G(0,\cdot)\).

Equations (10) say exactly that the total absolute mechanism rate is
bounded by \((\partial_t-\Delta/2)h_c=m_c'G\).
They do not require knowing the solution \(u\).

## 3. The heat transform, with the time direction fixed

Write \(p_t(x,y)\) for the heat kernel with generator \(L=\Delta/2\).
At a node with remaining time \(T\) and position \(x\), define, for
\(0\leq s<T\),
\[
 K_{T,s}(x,dy)=p_{T-s}(x,y)\frac{G(s,y)}{G(T,x)}\,dy.
 \tag{11}
\]
This is a probability kernel because \(P_{T-s}G(s,\cdot)=G(T,\cdot)\).
The kernels compose in decreasing remaining time, by the heat semigroup
identity and cancellation of the intermediate \(G\) factor.

Completing the square in (11) gives the exact edge draw
\[
 Y=\frac{1+s}{1+T}x+
 \sqrt{\frac{(1+s)(T-s)}{1+T}}\,Z,\qquad Z\sim N(0,I_d).
 \tag{12}
\]
For \(s=T\), use the degenerate kernel \(Y=x\). In elapsed time
\(\tau=T-s\), this is the diffusion
\[
 dX_\tau=-\frac{X_\tau}{1+T-\tau}\,d\tau+dW_\tau,
 \qquad 0\leq\tau\leq T.
 \tag{13}
\]
It is Brownian motion conditioned to be at zero at the fictitious elapsed
time \(T+1\), observed only up to time \(T\). There is no singular endpoint
on the simulated interval, and no diffusion time mesh.

One can verify the likelihood directly through (11), without invoking an
unproved Girsanov exponential-martingale condition. Equivalently, on each
finite interval the density relative to Brownian motion is
\(G(T-\tau,X_\tau)/G(T,x)\), a positive martingale of mean one.
Its stochastic logarithm has integrand \(\nabla\log G(T-\tau,X_\tau)\);
the resulting drift is the negative sign in (13).

For a field \(z_c=h_cq_c\), the normalized differential equation is
\[
 \partial_tq_c=(L+\nabla\log G\cdot\nabla)q_c-\kappa_cq_c
 +\sum_{\ell}\gamma_\ell
        \frac{\prod_{j\in\ell}h_j}{h_c}\prod_{j\in\ell}q_j,
 \qquad \kappa_c=\frac{m_c'}{m_c}.
 \tag{14}
\]
This calculation explains both the heat transform and the clock. Spatial
normalization alone would miss the killing term \(-\kappa_cq_c\).

## 4. The complete ideal sampling rule

The normalized recursive return value is denoted \(Z_c(T,x)\).
Fresh randomness is used at every child, conditionally independently given
the parent event. In particular, the two copies of \(D_i\) in a gradient
branch are independent simulations; squaring one simulation changes the
expectation and is incorrect.

For \(F_2\), return \(-1\) immediately. For an identically zero higher
reaction code, return zero immediately. At any nonconstant code:

1. If \(T=0\), return its signed terminal value divided by \(h_c(0,x)\).
2. Otherwise draw \(U\) uniformly in \((0,1)\).
3. If \(U m_c(T)\leq m_c(0)\), draw \(Y\) from \(K_{T,0}(x,\cdot)\) and
   return the signed terminal value at \(Y\), divided by \(h_c(0,Y)\).
4. Otherwise let \(s\in(0,T)\) be the unique solution of
   \(m_c(s)=U m_c(T)\), and draw \(Y\) from \(K_{T,s}(x,\cdot)\).
5. At \((s,Y)\), choose a mechanism \(\ell\) with probability
\[
 p_{c,\ell}(s,Y)=
 \frac{|\gamma_\ell|\prod_{j\in\ell}h_j(s,Y)}
      {\kappa_c(s)h_c(s,Y)}.
 \tag{15}
\]
   The remaining probability is a new slack outcome whose return is zero.
   On a retained mechanism, return
\[
 \operatorname{sgn}(\gamma_\ell)
       \prod_{j\in\ell}Z_j(s,Y).
 \tag{16}
\]

The final unnormalized root output is
\(\widehat H_I(T,x)=h_I(T,x)Z_I(T,x)\). All products in this algorithm are
products of normalized values. Multiplying by child envelopes again in
(16) would count the likelihood normalization twice.

The explicit probabilities are:

| Parent and mechanism | Conditional event probability |
|---|---:|
| \(I\to A\) | \(a/(C\epsilon^2)\) |
| \(B\to(A,F_2)\) | \(a/(C\epsilon^2)\) |
| \(A\to(A,B)\) | \(bG/\kappa_A=abG/a'\) |
| \(A\to(D_i,D_i,F_2)\), each \(i\) | \(\delta^2G/(a\kappa_A)=\delta^2G/a'\) |
| \(D_i\to(B,D_i)\) | \(bG/\kappa_D=G/w\) |

Every entry is evaluated at \((s,Y)\). The first two are at most \(3/4\).
For the \(A\) row the sum is
\[
 \frac{(ab+d\delta^2)G}{a'}\leq\frac Gw\leq1.
 \tag{17}
\]
The derivative row is also at most one. Therefore the slack probability
is nonnegative. If a gradient event is selected, its coordinate may be
chosen uniformly from \(1,\ldots,d\), since all \(d\) label probabilities
are identical. The coefficient \(-1/2\) in that event has negative sign;
its factor \(1/2\) has already cancelled \(h_{F_2}=2\). The return
\(-Z_{D_i}^{(1)}Z_{D_i}^{(2)}Z_{F_2}\) is positive times the product of
the two derivative returns because \(Z_{F_2}=-1\).

The clock survival from remaining time \(T\) down to \(s\) is
\[
 \exp\left\{-\int_s^T\kappa_c(r)\,dr\right\}
 =\frac{m_c(s)}{m_c(T)}.
 \tag{18}
\]
Consequently the no-event mass is \(m_c(0)/m_c(T)\), and the event-time
density with respect to increasing \(ds\) on \((0,T)\) is
\[
 \frac{m_c'(s)}{m_c(T)}\,ds.
 \tag{19}
\]
There is no missing survival factor in the inverse rule.

## 5. Completion and expected work, proved before using infinite trees

Count only nonconstant nodes first. Let \(N_c^{(n)}(T,x)\) count nodes
through generation \(n\), including the root at generation zero and
discarding deeper descendants. The tree has at most two nonconstant
children per node, so each \(N_c^{(n)}\) is bounded by \(2^{n+1}-1\)
without any completion assumption.

Let \(M_c^{(n)}\) be the supremum of its expectation over \(T,x\), and
let \(M_D^{(n)}\) also take the maximum over coordinates. These suprema
are finite for each \(n\). The following unconditional branch-probability
bounds are uniform in the state.

* The successful \(I\) and \(B\) branches have probability at most \(3/4\):
  this bound holds conditionally at every clock event.
* A \(D_i\) node branches only if its clock rings, whose probability is
  \(1-e^{-J(T)}\leq J(T)\leq1/4\).
* The probability of an \(A\) reaction branch is at most \(1/4\). Indeed,
  combining (19) with its event probability gives
\[
\begin{split}
 \mathbb P_{T,x}(A\hbox{ reaction})
 &=\int_0^T\frac{a(s)}{a(T)}b(s)
                  \mathbb E_{K_{T,s}(x,\cdot)}G(s,Y)\,ds\\
 &\leq\int_0^T b(s)w(s)\,ds=J(T)\leq1/4.
\end{split}
\tag{20}
\]
  This uses that \(a\) increases. A bound on the conditional reaction
  label alone would not establish (20).
* The total probability of an \(A\) gradient branch is at most one.

Condition on the first event, use the uniform bounds on descendant
expectations, and obtain
\[
\begin{aligned}
 M_A^{(n+1)}
 &\leq1+\tfrac14(M_A^{(n)}+M_B^{(n)})+2M_D^{(n)},\\
 M_B^{(n+1)}&\leq1+\tfrac34M_A^{(n)},\\
 M_D^{(n+1)}&\leq1+\tfrac14(M_B^{(n)}+M_D^{(n)}),\\
 M_I^{(n+1)}&\leq1+\tfrac34M_A^{(n)}.
\end{aligned}
\tag{21}
\]

The finite invariant vector, in the order \(A,B,D,I\), is
\[
 K=(220/3,\ 56,\ 20,\ 56).
 \tag{22}
\]
Every coordinate of \(M^{(0)}=(1,1,1,1)\) is at most \(K\).
The right sides of (21), with \(K\) substituted, equal respectively
\[
 1+\tfrac14(220/3+56)+40=220/3,\quad
 1+\tfrac34(220/3)=56,\quad
 1+\tfrac14(56+20)=20,\quad56.
 \tag{23}
\]
Their coefficients are nonnegative. Induction therefore proves
\(M_c^{(n)}\leq K_c\) at every finite depth.

Now \(N_c^{(n)}\) increases to the full nonconstant node count \(N_c\),
possibly infinite. Monotone convergence gives \(\mathbb E N_c\leq K_c\).
A nonnegative integer-valued count with finite expectation is finite
almost surely. This proves completion, including exclusion of infinitely
many births accumulating before time zero.

Only \(B\) branches and \(A\) gradient branches create an \(F_2\) leaf,
and each creates at most one. Consequently, pathwise,
\[
 N_{\rm all}\leq2N_{\rm nonconstant},
 \qquad \mathbb E N_{{\rm all},I}\leq2\cdot56=112.
 \tag{24}
\]
Evaluating all requested children gives this bound; an exact zero
short-circuit can only reduce work. The count bound concerns mean work,
not a deterministic maximum, a tail guarantee, or all moments of work.

## 6. Output bounds and the likelihood identity

The normalized terminal values have magnitude at most one. The constant
code returns \(-1\), slack returns zero, and every internal multiplier in
(16) has magnitude one. A finite product induction therefore gives
\[
 |Z_c(T,x)|\leq1
 \tag{25}
\]
on every finite sampled tree. Section 5 has proved that these are the
only trees encountered almost surely.

For a check of the target law, put \(q_c=\mathbb E Z_c\) and
\(z_c=h_cq_c\). The no-event contribution, after multiplication by
\(h_c(T,x)\), is exactly
\[
 h_c(T,x)\frac{m_c(0)}{m_c(T)}
 \int K_{T,0}(x,dy)\frac{g_c(y)}{h_c(0,y)}
 =P_Tg_c(x).
 \tag{26}
\]
Here \(g_c\) is the signed terminal code. For a branch \(\ell\), the
product of event density, transformed spatial density, label probability
and root envelope is
\[
\begin{split}
 &h_c(T,x)\frac{m_c'(s)}{m_c(T)}
  p_{T-s}(x,y)\frac{G(s,y)}{G(T,x)}
  \frac{|\gamma_\ell|\prod_{j\in\ell}h_j(s,y)}
       {\kappa_c(s)h_c(s,y)}\\
 &\hspace{25mm}=
 p_{T-s}(x,y)|\gamma_\ell|\prod_{j\in\ell}h_j(s,y).
\end{split}
\tag{27}
\]
Thus independent child means and the sign in (16) yield the exact signed
mild system
\[
\begin{aligned}
 z_I&=P_tv+\int_0^tP_{t-s}z_A(s)\,ds,\\
 z_A&=-P_t(v^2)+\int_0^tP_{t-s}
                       \left(z_Az_B+\sum_i z_{D_i}^2\right)(s)\,ds,\\
 z_B&=-2P_tv-2\int_0^tP_{t-s}z_A(s)\,ds,\\
 z_{D_i}&=P_t(\partial_i v)+\int_0^tP_{t-s}(z_Bz_{D_i})(s)\,ds,\\
 z_{F_2}&=-2.
\end{aligned}
\tag{28}
\]
The squares in this mean equation come from products of independent
copies. They are not second moments of a child estimator.

All quantities in (26)--(28) are integrable on finite time intervals,
by (25) and the envelopes. Alternatively, stop the estimator at generation
\(n\), returning zero on cut edges. These bounded normalized estimators
eventually agree with the full output on every finite tree; dominated
convergence gives the same identities.

This also identifies the canonical signed sum, not only a solution of
the same equations. For each finite allowed nonconstant depth, expand
the stopped expectation by its first event. Iterating (26)--(27) cancels
every proposal density and leaves exactly the signed heat-kernel
integral for each retained completed tree. Applying the same calculation
to its absolute value gives the sum of the absolute canonical
contributions at that depth. These finite-depth absolute sums are at
most \(h_c(T,x)\), and increase as the allowed depth increases.
Monotone convergence therefore proves absolute summability of the
reduced completed-tree expansion; dominated convergence of the bounded
sampled returns identifies its signed sum with \(\mathbb E\widehat H_c\).
Section 8 explains why the reduced signed and absolute sums equal the
corresponding original completed-tree sums after exact integration of
the constant leaves. In particular,
\[
 \mathbb E|\widehat H_c(T,x)|=W_c(T,x),
 \tag{28a}
\]
where \(W_c\) is the canonical absolute mass of 04e. This is an equality
of integrals, not equality of the two random outputs or their proposal laws.

The uniform second inequality in (3) also needs checking. Put
\(\alpha=C\epsilon\). Then
\(\alpha\leq83/48<5/2\leq d/2\), and
\[
 \frac{d}{dt}\big[(1+\alpha t)(1+t)^{-d/2}\big]
 =(1+t)^{-d/2-1}
   \big[\alpha-d/2+\alpha(1-d/2)t\big]\leq0.
 \tag{29}
\]
Since the spatial exponential is at most one, \(h_I(t,x)\leq\epsilon\).
Equations (25) and (29) prove every bound in (4).

## 7. Identification with the absorption PDE for \(C^1\) data

For bounded nonnegative initial data, standard heat-semigroup local
existence and comparison give
\[
 0\leq u(t,x)\leq P_tv(x)\leq\epsilon G(t,x)\leq\epsilon.
 \tag{30}
\]
The uniform bound prevents finite-time loss of the mild solution.
With the \(C^1\) datum (1), differentiate the local mild construction:
\(D_i=\partial_i u\) solves
\[
 (D_i)_t=LD_i-2uD_i,\qquad D_i(0)=\partial_i v.
 \tag{31}
\]
For instance the linear Feynman--Kac formula, or its positive and negative
comparison inequalities, gives
\[
 |D_i(t,x)|\leq P_t|\partial_i v|(x)\leq2\epsilon G(t,x).
 \tag{32}
\]
The solution is smooth at positive times. On \(t>0\), the chain rule gives
\[
 (\partial_t-L)(-u^2)=2u^3+|\nabla u|^2,\qquad
 (\partial_t-L)(-2u)=2u^2.
 \tag{33}
\]
Hence the physical family (5) solves (28). To include time zero without
assuming \(C^2\) data, first integrate from a positive time \(\eta\).
The \(C^1\) continuity at zero and bounds (30)--(32) allow
\(\eta\downarrow0\) in the mild identities by dominated convergence.

Both (28) from the sampler and (5) from the PDE are bounded on every
finite interval. On a common bounded range, the finite polynomial vector
field in (28) is Lipschitz in the coordinatewise supremum norm. The
heat semigroup is a contraction in that norm, so the difference of two
bounded mild solutions is at most a finite Lipschitz constant times its
time integral. Gronwall's inequality gives uniqueness. This proves
\(z_I=u\), rather than inferring unbiasedness from an absolute-moment
bound alone.

## 8. What is preserved, and what has changed

On every retained nonzero mechanism the proposal density in (27) is
strictly positive at finite \(T,s,x,y\). No contributing event-time or
spatial region has been discarded. The new slack outcome contributes
exactly zero, and has been included in the normalized mild equation.

Higher quadratic reaction codes are removed only because their
completed-tree terminal contribution is identically zero. The \(F_2\)
code is handled by exact integration of the constant field \(-2\).
Under a fully expanded positive-rate proposal, an \(F_2\) event produces
a zero higher-code factor, and the surviving no-event histories integrate
to \(-2\). Collapsing that calculation is exact at the level of (28).

More explicitly, a finite tree rooted at any \(F_k\), \(k\geq3\), has a
distinguished descendant chain whose reaction-code index strictly
increases until a terminal \(F_j\) leaf, \(j\geq3\), contributes zero.
Thus every such finite completed tree has zero weight, including every
tree in which an \(F_2\) node branches. In every nonzero original
completed tree, an \(F_2\) node is consequently a no-event terminal leaf.
Integrating its remaining heat endpoint gives the same constant \(-2\),
or magnitude \(2\) in the absolute sum, because the heat kernel has
mass one. Removing these endpoint variables and the identically zero
trees leaves precisely the reduced expansion used in Section 6.

The safe description is therefore an exact heat-transformed importance
sampler for the quadratic code closure with analytically integrated
constant codes and omitted identically zero contributions. It is not a
claim that its output distribution, moments, or random work equal those
of the original fixed-rate tree. A theorem requiring positive probability
for every syntactic label of the fully expanded tree cannot be invoked
without explaining this reduction. Equation (27) supplies the required
direct correctness proof.
In particular, this is not full-support raw completed-tree sampling of
every syntactically possible zero subtree.

## 9. Scalar inverses and the boundary of implementability

The \(I\) and \(B\) amplitudes are affine, so a retained event has
\[
 s=\frac{U b(T)-2\epsilon}{2C\epsilon^2}.
 \tag{34}
\]
For a \(D_i\) event solve
\[
 J(s)=J(T)+\log U.
 \tag{35}
\]
For an \(A\) event solve \(a(s)=Ua(T)\). These are strictly monotone
scalar equations with a unique root in \((0,T)\).

With \(q=(1+s)^{-1/2}\), the only integrals in the coefficients are
\[
 I_0(s)=\frac{1-q^{d-2}}{d/2-1},\qquad
 I_1(s)=\frac{1-q^{d-4}}{d/2-2}-I_0(s).
 \tag{36}
\]
Thus \(J\) and \(a\) are explicit monotone combinations of powers on
\([(1+T)^{-1/2},1]\); neither needs a PDE solution oracle. Equation (12)
needs one Gaussian vector per sampled edge. An aggregate gradient label
and a uniform coordinate avoid constructing a length-\(d\) probability
table.

In a real-arithmetic model with fixed-cost elementary functions, scalar
inverses and terminal queries, the expected vector work is \(O(d)\)
uniformly in \(T\). For an actual implementation, denote the inverse
clock cost by \(L\) and the terminal oracle cost by \(Q_v\); a node count
alone does not bound \(L\) or \(Q_v\). The following issues are outside
the theorem and must be resolved in the numerical contract:

* Cancellation in (36) near \(s=0\), and near saturation of \(J,a,\delta\)
  at very large \(T\), needs stable formulas and bracketed inverses.
* A small residual in a flat monotone function does not by itself give a
  small error in the event time, branch law or expected estimator.
* Direct division by a tiny \(G(0,Y)\), evaluation of \(G\) at extreme
  coordinates, and very large \(T\) need scaled or logarithmic formulas.
  Underflow is not a proof that a label or terminal value is exactly zero.
* Finite-bit uniforms, approximate Gaussian draws, approximate \(v\) and
  derivative evaluations, and root tolerances introduce distinct errors.
  Exact ideal unbiasedness does not certify an ordinary floating program.

No uniform bound on bit operations at arbitrarily large \(T\), and no
validated inverse-clock error bound, has been established in this note.

## 10. Stronger baselines for this PDE

### 10.1 A scalar binary heat-transform sampler

The absorption equation itself has the familiar scalar binary mechanism
\(I\to(I,I)\) with coefficient \(-1\). It does not require derivative
codes. Applying the same normalization principle directly is much cheaper
in the bounds, as the following conventional calculation shows.

Let
\[
 \eta=\epsilon I_0(\infty),\qquad
 m_*(t)=\frac{\epsilon}{1-\epsilon I_0(t)},\qquad
 h_*(t,x)=m_*(t)G(t,x).
 \tag{37}
\]
For \(d\geq5\), \(\eta\leq1/48\). We have
\(m_*'=m_*^2w\), so the clock is
\(\kappa_*=m_*w\), and its conditional successful binary probability is
\[
 \frac{h_*}{\kappa_*}=\frac Gw\leq1.
 \tag{38}
\]
At a successful branch return minus the product of two independent
normalized children; use \(v/(\epsilon G(0,\cdot))\) at a leaf and zero
on slack. The same likelihood calculation proves unbiasedness.

The probability that the clock even rings is
\[
 1-\frac{m_*(0)}{m_*(T)}=\epsilon I_0(T)\leq\eta.
 \tag{39}
\]
Finite-depth counts satisfy \(M_{n+1}\leq1+2\eta M_n\), \(M_0=1\).
Induction and monotone convergence give
\[
 \mathbb E N_*\leq\frac1{1-2\eta}\leq\frac{24}{23},
 \qquad
 |\widehat H_*|\leq h_*
 \leq\frac{48}{47}\epsilon G.
 \tag{40}
\]
There are no constant-code nodes. Its clock inverse can also be written
using \(I_0(s)\) and a single power:
\[
 I_0(s)=\frac{1-[1-\epsilon I_0(T)]/U}{\epsilon}
 \quad\hbox{on the event branch}.
 \tag{41}
\]
The same construction works for \(d\geq3\) whenever
\(\epsilon I_0(\infty)<1/2\), without the derivative assumption in (1),
provided the nonnegative datum is bounded by \(\epsilon G(0,\cdot)\).
It is a different representation from the derivative-coded expansion.

Thus the 112-node theorem is useful as a constructive consequence of the
all-code supersolution, but it establishes no efficiency advantage over
the standard scalar representation for (2). Bounds (40) versus (3) are
theoretical comparisons, not measured runtime ratios.

### 10.2 Heat flow and the zero estimator

The deterministic heat flow \(P_Tv\) has an explicit absorption bias bound.
Using (30) in Duhamel's formula and \(G^2\leq wG\) gives
\[
 0\leq P_Tv(x)-u(T,x)
 \leq\epsilon^2 I_0(T)G(T,x).
 \tag{42}
\]
For the Gaussian example,
\[
 P_Tv(x)=\epsilon(1+2T)^{-d/2}
                 e^{-|x|^2/(1+2T)}
 \tag{43}
\]
is closed form. The zero estimator already has absolute error at most
\(\epsilon G(T,x)\leq\epsilon(1+T)^{-d/2}\).
Any experiment claiming practical long-horizon improvement must include
these inexpensive biased baselines at the requested accuracy, alongside
the unbiased scalar sampler and a suitable deterministic reference.

For \(N\) independent root samples from (3), the ideal mean-square error
is at most \(h_I(T,x)^2/N\) and expected total nodes are at most \(112N\).
This is an absolute-error guarantee. It supplies neither a uniform
relative-error bound nor dimension-free arithmetic complexity. For the
Gaussian example the root envelope and the mean have different
long-time scalings, and even Gaussian envelope ratios can deteriorate
with \(d\). Output moments do not by themselves establish practical gain.

## 11. Bounded primary-literature check and novelty limit

The mechanism of transforming branching laws is established literature.
The following are the directly inspected primary sources relevant to this
bounded audit:

* Ossiander, “A probabilistic representation of solutions of the
  incompressible Navier–Stokes equations in \(\mathbb R^3\)” (2004
  preprint), uses majorizing kernels and an \(h\)-transformed Brownian
  motion. Section 4, equation (18), is the kernel
  \(h(y)K(x-y,2\nu t)/h(x)\); Theorem 4.2 gives a global small-data
  representation \(u=h\mathbb E\Upsilon\), and Proposition 4.2 bounds
  \(|\Upsilon|\). Its dominating 0/2 Galton–Watson tree permits a
  strict offspring probability \(p<1/2\), which also gives expected
  total nodes at most \(1/(1-2p)\). The last mean-cost deduction is our
  consequence of that domination, not an attributed complexity theorem.
  [Author preprint](https://arxiv.org/abs/math/0412034).
  T19 independently checked these primary theorem details.
* Ikeda, Nagasawa and Watanabe, “Transformation of Branching Markov
  Processes” (1966), establishes the historical transformation setting.
  [Publisher record](https://www.jstage.jst.go.jp/article/pjab1945/42/7/42_7_719/_article).
* Beznea, Boeangiu and Lupaşcu-Stamate, “h-transform of Doob and nonlocal
  branching processes” (2020), studies preservation of the branching
  property and the associated nonlinear evolution equation.
  [Publisher abstract](https://link.springer.com/article/10.1007/s13324-020-00390-3).
  Only the accessible abstract and bibliographic record were inspected;
  no theorem-level equivalence with this sampler is asserted.
* Agarwal and Claisse, “Branching diffusion representation of semi-linear
  elliptic PDEs and estimation using Monte Carlo method” (2020),
  Proposition 3.4, uses nonnegative supersolutions to bound moments of
  branching estimators. The setting is elliptic on bounded domains.
  [Author accepted manuscript](https://eprints.gla.ac.uk/210343/7/210343.pdf).
* Henry-Labordère, Oudjane, Tan, Touzi and Warin, “Branching diffusion
  representation of semilinear PDEs and Monte Carlo approximation,”
  develops weighted, marked branching representations for polynomial
  nonlinearities. [Author preprint](https://arxiv.org/abs/1603.01727).
* Nguwi, Penent and Privault, “A fully nonlinear Feynman–Kac formula with
  derivatives of arbitrary orders,” supplies the stochastic coding-tree
  context of the present project.
  [Author preprint](https://arxiv.org/abs/2201.03882).

The explicit amplitudes, exact Gaussian edge kernel and numerical
invariant vector form a verifiable construction for this code family.
This bounded search does not establish priority for that exact
combination. Doob transforms, envelope normalization, supersolution
moment control and subcritical branching work arguments are not new
principles. The simpler scalar baseline further prevents presenting
this construction as a general PDE-solver breakthrough.

## 12. Fixed minimal Lean targets before implementation

These are proposed formal targets, not declarations that have been built.
Their statements should remain fixed when handed to a coding worker.
They deliberately do not claim the heat-kernel, probability or PDE
bridges have been formalized.

**LT17.1 — bounded finite products.** For every finite list of real numbers
\(z_1,\ldots,z_k\) with \(|z_j|\leq1\), and every real scalar
\(\sigma\) with \(|\sigma|\leq1\),
\[
 \left|\sigma\prod_{j=1}^kz_j\right|\leq1.
 \tag{44}
\]
The empty product is one. A finite-tree induction combines this lemma
with normalized terminal bounds and zero slack to prove (25). Leaf
normalization may be a separate algebraic lemma:
\(h>0,\ |g|\leq h\Rightarrow |g/h|\leq1\).

**LT17.2 — the finite multitype work recurrence.** For real sequences
\(A_n,B_n,D_n,I_n\), \(n\in\mathbb N\), assume that their initial values
are nonnegative and at most one, all sequence entries are nonnegative,
and for every \(n\) the four inequalities (21) hold with these sequences.
Prove, for every \(n\),
\[
 A_n\leq220/3,\quad B_n\leq56,\quad D_n\leq20,\quad I_n\leq56.
 \tag{45}
\]
The proof is simultaneous induction using (23). If another real sequence
\(R_n\) satisfies \(R_n\leq2I_n\), conclude \(R_n\leq112\).
No hypothesis asserting finite untruncated expected work is permitted.

**LT17.3 — optional scalar-baseline recurrence.** If
\(0\leq\eta\leq1/48\), \(M_0\leq1\), and
\(M_{n+1}\leq1+2\eta M_n\), with nonnegative real entries, prove
\(M_n\leq24/23\). This checks the baseline arithmetic without certifying
its stochastic realization.

The minimal gate is LT17.1 and LT17.2, with fresh successful builds,
named declarations, and transitive axiom reports. The normalization
kernel (11), exact law (18)--(19), branch identity (27), conditional
independence, monotone convergence to a finite tree, PDE uniqueness, and
floating-clock error analysis remain explicitly outside these finite
Lean targets. A green build of (44)--(45) must not be reported as an
end-to-end formal certificate for (3).
