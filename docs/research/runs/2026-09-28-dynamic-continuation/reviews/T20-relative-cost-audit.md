# T20 audit: relative-accuracy separation of quadratic representations

Verdict: **the conventional separation in 04g passes**. There is no
remaining mathematical blocker under its deterministic root-count,
independent unbiased sample-mean contract. The T17 exact reduction
preserves canonical absolute mass, which is the essential hypothesis.
The scalar comparison should use the Gaussian envelope matched to the
datum: its relative-variance and expected-node bounds are uniform in
\(T,x,d\), not merely in \(T\) at fixed \(d\).

The weaker broad-Gaussian comparison initially written in 04g is valid,
but its factor \(2^d\) is avoidable for the scalar baseline. The matched
comparison below is the recommended replacement. The derivative-code
upper bound still has a \(d\)-dependent constant. Root owns 04g; this
audit edits only this review.

No numerical experiment, code, Lean declaration or finite-bit
complexity certificate is asserted. The broad importance-sampling
variance inequality is classical; novelty of this code-specific
asymptotic comparison has not been established.

## 1. Precisely accepted scope

Fix an integer \(d\geq5\), \(0<\epsilon\leq1/32\), and
\[
 v(x)=\epsilon e^{-|x|^2},\qquad
 u_t=\tfrac12\Delta u-u^2,\quad u(0)=v.
 \tag{1}
\]
The derivative-code lower bound is evaluated at \(x=0\). Let \(W_I\)
be the canonical absolute mass of the original derivative-coded
expansion, in the finite-completed-tree convention of 04e/T15.

For any exactly weighted, genuinely supported and almost-surely
completing proposal that retains that signed completed-tree
representation, its root output \(H\) satisfies
\[
 \mathbb EH=u,\qquad \mathbb E|H|=W_I.
 \tag{2}
\]
The same identities hold for the T17 transformed estimator, even
though it integrates constant-code endpoints and omits zero trees;
Section 3 checks this independently of mere signed unbiasedness.

The estimator being compared is the equally weighted average of
\(N\geq1\) independent identically distributed roots, with deterministic
\(N\) chosen for the known query and target relative RMS \(\rho>0\).
The proposal may depend on the horizon. The lower bound does not
address biased solvers, control variates, cancellation before sampling,
correlated or coupled roots, random stopping policies, self-normalized
averages, continuation, or a different signed representation.

## 2. Canonical mass and the relative-variance lower bound

The nonnegative \(A\)-equation in 04e gives
\[
 A(s,\cdot)\geq P_s(v^2).
\]
Tonelli and the heat semigroup then give, for every \(T\geq0\),
\[
\begin{split}
 W_I(T,x)
 &=P_Tv(x)+\int_0^T P_{T-s}A(s,\cdot)(x)\,ds\\
 &\geq P_Tv(x)+T P_T(v^2)(x).
\end{split}
\tag{3}
\]
The terminal \(A\)-leaf under one \(I\to A\) event already supplies
the second term, so the argument does not need an asymptotic expansion
or a limiting PDE comparison.

The nonnegative absorption solution has
\(0<u(T,x)\leq P_Tv(x)\). Positivity follows, for example, from the
linear Feynman–Kac formula proved below. At the origin,
\[
 P_Tv(0)=\epsilon(1+2T)^{-d/2},\qquad
 P_T(v^2)(0)=\epsilon^2(1+4T)^{-d/2}.
 \tag{4}
\]
Consequently
\[
\begin{split}
 \frac{W_I(T,0)}{u(T,0)}
 &\geq1+\epsilon T
       \left(\frac{1+2T}{1+4T}\right)^{d/2}\\
 &\geq1+kT,\qquad k=\epsilon\,2^{-d/2}>0.
\end{split}
\tag{5}
\]
The second inequality uses \((1+2T)/(1+4T)\geq1/2\) and a positive
power, and is valid also at \(T=0\).

If \(H\) has finite second moment, Cauchy–Schwarz and (2) imply
\[
 \frac{\operatorname{Var}H}{u(T,0)^2}
 =\frac{\mathbb EH^2}{u(T,0)^2}-1
 \geq\left(\frac{W_I(T,0)}{u(T,0)}\right)^2-1
 \geq(1+kT)^2-1.
 \tag{6}
\]
This is the classical unavoidable variance from a signed integrand's
absolute mass; changing the sampling law cannot change that mass.
The standard importance-sampling formulation and the optimal
absolute-integrand proposal are discussed in
[Owen, Chapter 9, Section 9.1](https://artowen.su.domains/mc/Ch-var-is.pdf).
No novelty is assigned to Cauchy–Schwarz or that proposal principle.

Independence and exact centering therefore give
\[
 \frac{\mathbb E(\overline H_N-u(T,0))^2}{u(T,0)^2}
 \geq\frac{(1+kT)^2-1}{N}.
 \tag{7}
\]
If \(\mathbb EH^2=\infty\), the average also has infinite second
centered moment: condition on the first root and apply conditional
Jensen to the square of the centered sum. The other roots have
integrable centered means zero, so this lower-bounds the sum's second
moment by the first root's infinite centered second moment. Thus no
undefined infinity-minus-infinity covariance argument is needed.

Relative RMS at most \(\rho\) consequently requires
\[
 N\geq\frac{(1+kT)^2-1}{\rho^2}
 \geq\frac{k^2T^2}{\rho^2}.
 \tag{8}
\]
This is \(\Omega(T^2)\) for fixed \(d,\epsilon,\rho\). Its constant
\(k^2=\epsilon^2 2^{-d}\) is not uniform away from zero as \(d\)
increases or \(\epsilon\) decreases. The theorem is not a universal
lower bound for solving the absorption PDE.

## 3. Why the T17 reduction preserves absolute mass

At each finite allowed nonconstant depth, T17's root likelihood
cancellation can be applied after taking the absolute value. The
normalized branch products use independent children, and the
probabilities contain the absolute scalar mechanism coefficients.
This yields exactly the corresponding nonnegative canonical tree sum.
The finite-depth sums increase and are bounded by T17's envelope.
Their limit therefore equals the absolute canonical mass of the
reduced expansion.

The reduction to that expansion preserves absolute mass as well:

* For \(F_j\), \(j\geq3\), every finite tree has an increasing
  reaction-index descendant chain ending in a terminal code that is
  identically zero. Its whole contribution is zero.
* A branched \(F_2\) node contains such an \(F_j\) descendant, so it
  also contributes zero. Every nonzero \(F_2\) history is consequently
  the no-event constant leaf.
* That leaf has signed value \(-2\), independent of its Brownian
  endpoint. Its heat-kernel integral is \(-2\), and its absolute
  integral is \(2\). Collapsing it merges no opposite-sign contributions.

Therefore reduced and original canonical absolute sums agree.
T17 has already proved almost-sure completion; its bounded
depth-truncated outputs converge to the actual output. Dominated
convergence of their absolute values gives
\[
 \mathbb E|\widehat H_I(T,x)|=W_I(T,x).
 \tag{9}
\]
This is the required bridge for (6); agreement of signed means alone
would not prove it. More aggressive integration that cancels opposite
signs can change absolute mass and is outside this lower bound.

## 4. Matching \(O(T^2)\) upper bound for the T17 code sampler

Use the heat envelope matched to the Gaussian datum for the PDE
comparison:
\[
\begin{gathered}
 G_v(t,x)=(1+2t)^{-d/2}
              e^{-|x|^2/(1+2t)},\qquad
 w_v(t)=(1+2t)^{-d/2},\\
 I_v(t)=\int_0^t w_v(s)\,ds,\qquad
 I_v(\infty)=\frac1{d-2},\qquad
 \eta_v=\frac{\epsilon}{d-2}\leq\frac1{96}.
\end{gathered}
\tag{10}
\]
The exact heat flow is \(P_tv=\epsilon G_v(t,\cdot)\), and
\[
 0\leq u(t,x)\leq\epsilon G_v(t,x)\leq\epsilon w_v(t).
 \tag{11}
\]
View the fixed solution \(u\) as the bounded nonnegative coefficient in
the linear equation \(u_t=Lu-u(t,x)u\). Feynman–Kac gives
\[
 u(T,x)=\mathbb E_x\left[
 v(B_T)\exp\left\{-\int_0^T u(T-r,B_r)\,dr\right\}\right].
 \tag{12}
\]
The integrated coefficient is between zero and
\(\epsilon I_v(T)\leq\eta_v\). Hence
\[
 e^{-\epsilon I_v(T)}P_Tv(x)
 \leq u(T,x)\leq P_Tv(x),
 \quad\hbox{and in particular}\quad
 u(T,x)\geq e^{-\eta_v}P_Tv(x)>0.
 \tag{13}
\]
The comparison uses the unknown solution only as a proof witness;
neither sampler queries it.

The actual T17 derivative-code sampler retains the broader envelope
\[
 h_I(T,x)=(\epsilon+C\epsilon^2T)G(T,x).
 \tag{14}
\]
At \(x=0\),
\[
 \frac{G(T,0)}{G_v(T,0)}
 =\left(\frac{1+2T}{1+T}\right)^{d/2}\leq2^{d/2}.
 \tag{15}
\]
Thus (13), (14), and the deterministic T17 output bound give
\[
 \frac{\mathbb E\widehat H_I(T,0)^2}{u(T,0)^2}
 \leq e^{2\eta_v}2^d(1+C\epsilon T)^2.
 \tag{16}
\]
One may subtract one on the right to bound relative variance, but it
is harmless to use the displayed second-moment upper bound.
For instance
\[
 N_T=\left\lceil
 \frac{e^{2\eta_v}2^d(1+C\epsilon T)^2}{\rho^2}
 \right\rceil
 \tag{17}
\]
guarantees relative RMS at most \(\rho\).
The original 04g choice with the larger broad-envelope
\(\eta=\epsilon I_0(\infty)\) also works; (17) is a minor improvement.

Every root costs at least one counted node and at most 112 nodes in
expectation. Equations (8) and (17) prove that the required number of
roots and the achievable expected total visited nodes for the T17
sample mean are \(\Theta(T^2)\) at fixed \(d,\epsilon,\rho\).
This is a sharp horizon exponent for this estimator architecture,
not a finite-bit runtime result or a dimension-uniform lower bound.

## 5. The matched scalar binary comparator

Normalize the ordinary scalar mechanism \(I\to(I,I)\), with scalar
coefficient \(-1\), by
\[
 m_v(t)=\frac{\epsilon}{1-\epsilon I_v(t)},\qquad
 h_v(t,x)=m_v(t)G_v(t,x),\qquad
 \kappa_v(t)=m_v(t)w_v(t).
 \tag{18}
\]
Since \(m_v'=m_v^2w_v\), its absolute reaction envelope satisfies
\((\partial_t-L)h_v=m_v^2w_vG_v\geq h_v^2\).
The no-event normalized terminal return is exactly one, because
\(v=\epsilon G_v(0,\cdot)\).

The transformed edge kernel is
\[
 K^v_{T,s}(x,dy)
 =p_{T-s}(x,y)\frac{G_v(s,y)}{G_v(T,x)}\,dy.
 \tag{19}
\]
It is the Gaussian
\[
 Y=\frac{1+2s}{1+2T}x+
     \sqrt{\frac{(1+2s)(T-s)}{1+2T}}\,Z,
 \qquad Z\sim N(0,I_d).
 \tag{20}
\]
The elapsed-time drift is
\(-2X_\tau/[1+2(T-\tau)]\): equivalently, a Brownian bridge pinned
at zero at elapsed time \(T+1/2\). This verifies both the parent
proposal's mean and covariance; no extra factor two belongs in
the covariance.

Use the clock survival \(m_v(s)/m_v(T)\), and, at an event, branch
into two independent children with conditional probability
\[
 \frac{h_v}{\kappa_v}=\frac{G_v}{w_v};
 \tag{21}
\]
return zero on the remaining probability, and minus the product
of the child returns on success. The inverse clock is explicit:
\[
\begin{gathered}
 I_v(s)=\frac{1-[1-\epsilon I_v(T)]/U}{\epsilon},\\
 I_v(s)=\frac{1-(1+2s)^{\,1-d/2}}{d-2},\qquad
 s=\frac{[1-(d-2)I_v(s)]^{-2/(d-2)}-1}{2},
\end{gathered}
\tag{22}
\]
on the event branch. As before these are ideal real formulas, not
a floating-point error certificate.

The total clock-event probability is
\[
 1-\frac{m_v(0)}{m_v(T)}
 =\epsilon I_v(T)\leq\eta_v\leq1/96.
 \tag{23}
\]
Finite-depth node counts obey \(M_{n+1}\leq1+2\eta_vM_n\), \(M_0=1\).
Induction, followed by monotone convergence, gives completion and
\[
 \mathbb E N_v\leq\frac1{1-2\eta_v}\leq\frac{48}{47}.
 \tag{24}
\]
The same exact finite-tree likelihood proof as T17 yields unbiasedness
and \(|\widehat H_v|\leq h_v\). Combining this with (13) gives
\[
 \frac{\mathbb E\widehat H_v(T,x)^2}{u(T,x)^2}
 \leq
 \frac{\exp(2\epsilon I_v(T))}
      {[1-\epsilon I_v(T)]^2}
 \leq
 \frac{e^{2\eta_v}}{(1-\eta_v)^2}.
 \tag{25}
\]
Every bound here holds for all finite \(T\geq0\), all \(x\), and
all allowed \(d,\epsilon\). The artificial factor \(2^d\) from
the broad scalar envelope has disappeared.

For a concrete nonoptimized universal variance bound, use
\(e^a\leq(1-a)^{-1}\) for \(0\leq a<1\). Then
\[
\begin{split}
 \frac{\operatorname{Var}\widehat H_v}{u^2}
 &\leq\frac{e^{1/48}}{(95/96)^2}-1\\
 &\leq\frac{48}{47}\left(\frac{96}{95}\right)^2-1
 =\frac{18193}{424175}<\frac1{20}.
\end{split}
\tag{26}
\]
Consequently
\[
 N_\rho=\left\lceil\frac1{20\rho^2}\right\rceil
 \tag{27}
\]
independent matched scalar roots suffice for relative RMS at most
\(\rho\) at every allowed \(T,x,d,\epsilon\), with expected total
nodes at most \(48N_\rho/47\). The sharper variance constant in
(25) may be used instead. The dimension still enters Gaussian
generation and vector arithmetic; these are node and sample-count
guarantees in the same ideal model.

## 6. The biased heat-flow baseline is still material

Equation (13) immediately gives a relative-error certificate for
returning the exact heat flow:
\[
 0\leq\frac{P_Tv(x)-u(T,x)}{u(T,x)}
 \leq e^{\epsilon I_v(T)}-1
 \leq e^{\eta_v}-1
 \leq\frac{\eta_v}{1-\eta_v}
 \leq\frac1{95}.
 \tag{28}
\]
Thus a relative tolerance at least \(1/95\) is already guaranteed
without Monte Carlo over the entire parameter range. For a specified
\(d,\epsilon,T\), the sharper threshold \(e^{\epsilon I_v(T)}-1\)
can be substantially smaller. This is a biased method and therefore
outside (8); that exclusion is substantive.

A later numerical study should use an accuracy regime below this
certificate and preserve the matched scalar comparison. It would
illustrate the theory; no finite collection of plots could prove
the \(\Omega(T^2)\) lower bound.

## 7. Recommended changes to the root-owned note

1. Keep the original-code lower bound and iid scope as written.
   Replace the request for T17 confirmation with the established
   mass-preservation identity (9), also recorded as 04f equation (28a).
2. Use \(G_v,w_v,I_v,\eta_v\) for the scalar baseline. Replace its
   \(24/23\) node bound by \(48/47\), remove its \(2^d\) relative
   factor, and state uniformity in \(T,x,d,\epsilon\) over the
   explicit allowed range. Keep the ideal arithmetic qualification.
3. The derivative-code upper bound may replace \(e^{2\eta}\) by
   \(e^{2\eta_v}\), while retaining \(2^d\) and the fixed-\(d\)
   asymptotic comparison.
4. State that expected total counted-node work is bounded between
   \(N\) and \(112N\) for the T17 sample mean, so the \(\Theta(T^2)\)
   statement has an explicit cost object.
5. Include the relative heat-flow certificate (28). The convenient
   rational bound (26) is optional; it is an algebraic simplification,
   not new numerical evidence.

A later finite Lean target can encode the Cauchy–Schwarz consequence
from real inequalities \(u>0\), \(a\geq(1+kT)u\), and \(m_2\geq a^2\),
and the rational recurrence/bound arithmetic. It will not itself
certify (2), the heat semigroup, Feynman–Kac, independence, asymptotic
node complexity, or floating implementation.
