# T17 audit: heat-transform quadratic-code sampler

Conventional-theory verdict: **pass with a precise representation and
arithmetic scope**. No algebraic correction to the proposed amplitudes
or the expected total-node constant 112 was needed. No sampler code,
numerical experiment, or Lean build was run in this task.

The task read the math-auto-research skill, its defaults, model-routing
and execution instructions, and the General research profile. It read
04e and the existing signed mechanism/proposal contracts. Work was
restricted to 04f and this audit; T15's 04e file was preserved. The
dispatch inherited the research role; independent service-level
model/effort telemetry is unavailable.

## 1. Blockers and claim boundaries first

There is no remaining conventional mathematical blocker to the ideal
sampler in 04f. The following stronger claims are not established:

1. **A certified floating implementation is pending.** The two nonlinear
   clocks have unique explicit scalar inverse definitions, but no
   numerical inverse error protocol, random-bit model, terminal-oracle
   error bound or extreme-horizon arithmetic guarantee has been proved.
2. **The raw random-tree law is different.** Constant \(F_2\) subtrees
   are integrated exactly and zero completed-tree contributions are
   omitted. The sampler equals the same canonical signed sum and
   absolute mass, with exact positive likelihood on every retained
   nonzero alternative; it is not a full-support proposal over every
   zero syntactic subtree.
3. **There is no practical advantage theorem for this PDE.** The standard
   scalar binary representation admits the same heat transform with
   expected nodes at most \(24/23\) and output bound
   \(48\epsilon G/47\). It needs no derivative oracle. The derivative-code
   bound 112 is a constructive result for that code family, not evidence
   that those codes should be used for a scalar quadratic reaction.
4. **Formal coverage is pending and deliberately finite.** The fixed
   Lean targets below cover bounded products and a work recurrence.
   Heat kernels, conditional independence, expected work, PDE
   identification and floating arithmetic remain conventional or pending.
5. **Novelty is unconfirmed.** Transformation of branching processes,
   supersolution moment control and normalized stochastic cascades have
   primary precedents. A bounded source search cannot support a worldwide
   novelty claim.

## 2. Statement accepted by this audit

For any integer \(d\geq5\), \(0<\epsilon\leq1/32\), and nonnegative
\(v\in C^1(\mathbb R^d)\) satisfying
\[
 v\leq\epsilon G(0,\cdot),\qquad
 |\partial_i v|\leq2\epsilon G(0,\cdot),
\]
the ideal real sampler of 04f has
\[
 \mathbb E\widehat H_I(T,x)=u(T,x),\qquad
 |\widehat H_I(T,x)|\leq h_I(T,x)\leq\epsilon,\qquad
 \mathbb E N_{{\rm all},I}(T,x)\leq112
\]
for all finite \(T\geq0\) and all \(x\), where
\(u_t=\Delta u/2-u^2\), \(u(0)=v\). Therefore all positive absolute
output moments are bounded by \(\epsilon^p\), uniformly in \(T,x\).
The expected node count is also uniform over the allowed \(d,\epsilon,v\).
This does not say that the random work has all moments or a bounded tail.

The extension from the Gaussian example to (nonnegative) \(C^1\) data
is valid. It requires exact input value and first-derivative oracles in
the ideal sampling contract; being a mathematical \(C^1\) function does
not provide an implementation of those oracles.

## 3. Adversarial checks

| Audit item | Finding and proof location in 04f |
|---|---|
| Time orientation | Correct. Remaining time decreases, and the elapsed-time drift is \(-x/(1+T-\tau)\). Sections 3–4. |
| Gaussian covariance | Correct: \((1+s)(T-s)/(1+T)\) times the identity. It is a bridge ending one unit after the sampled interval. Section 3. |
| Doob/Girsanov density | Correct by direct heat-kernel normalization; no unverified Novikov shortcut is needed. The finite-time martingale density is \(G(T-\tau,X_\tau)/G(T,x)\). Section 3. |
| Leaf survival | Exactly \(m_c(0)/m_c(T)\). The event density is \(m_c'(s)/m_c(T)\,ds\). The inverse rule contains the survival factor. Section 4. |
| Scalar signs | Correct. The gradient mechanism has coefficient \(-1/2\) and \(F_2=-2\), producing the positive gradient-square term in the signed \(A\) equation. Sections 2, 4, 6. |
| Conditional probabilities | All are nonnegative and row sums are at most one by the coefficient supersolution. The unused mass is a zero return. Section 4. |
| Duplicate derivatives | Must be independent fresh child simulations. Reusing one draw and squaring it is biased. Section 4 makes this mandatory. |
| Finite-tree support | Every retained contributing event, space point and label has positive density at finite states. Zero subtrees and constant integration are explicitly separated. Section 8. |
| Absolute boundedness | Normalized leaves, constants and finite products have magnitude at most one. Section 6. |
| All-horizon bound | \(h_I\leq\epsilon\) follows from \(C\epsilon\leq83/48<d/2\) and a direct derivative calculation. Section 6. |
| Expected work | The proposed 112 is correct. A finite-depth invariant vector is proved before the full expected count exists. Section 5. |
| Same canonical sum and absolute mass | Finite-depth likelihood cancellation, monotone convergence of absolute sums and dominated convergence of outputs provide both bridges. Sections 6 and 8. |
| Signed PDE identity | The physical finite code family solves the same bounded polynomial mild system; finite-interval sup-norm Gronwall gives uniqueness. Section 7. |
| Arbitrary \(C^1\) envelope | Valid without radial symmetry. The datum and gradient are bounded and uniformly continuous; smoothing and a positive-time limit justify the chain rule. Sections 1 and 7. |
| Dependence on \(T,d,\epsilon\) | Node and absolute output bounds are uniform in the stated range. Vector arithmetic, relative error, inverse precision and oracle cost are not dimension- or horizon-free. Sections 9–10. |

### The work calculation without circularity

Let \(A_n,B_n,D_n,I_n\) be the suprema of expected nonconstant nodes
through generation \(n\). At every finite depth these are bounded by a
binary-tree count, so no integrability assumption has been smuggled in.
The accepted inequalities are
\[
\begin{aligned}
 A_{n+1}&\leq1+\tfrac14(A_n+B_n)+2D_n,\\
 B_{n+1}&\leq1+\tfrac34A_n,\\
 D_{n+1}&\leq1+\tfrac14(B_n+D_n),\\
 I_{n+1}&\leq1+\tfrac34A_n.
\end{aligned}
\]
The potentially delicate bound is the **unconditional** \(A\)-reaction
probability:
\[
 \int_0^T\frac{a(s)}{a(T)}b(s)
       \mathbb E_{K_{T,s}}G(s,Y)\,ds
 \leq J(T)\leq1/4.
\]
Bounding the event label at a fixed point would not replace this step.

The vector \((220/3,56,20,56)\) is fixed by the affine upper recurrence
and dominates the initial vector \((1,1,1,1)\). Simultaneous induction
gives the bound at every finite depth; only then does monotone
convergence give finite expected total nonconstant counts. Each
nonconstant node introduces at most one constant leaf, so the Id total
is at most \(2\cdot56=112\). This proof also establishes almost-sure
completion and excludes accumulation of infinitely many births.

### Why the signed/PDE argument is sufficient

The terminal values are \(v,-v^2,-2v,\partial_i v,-2\).
After all proposal factors cancel, the signed mild system is
\[
\begin{aligned}
 (\partial_t-L)U&=A,\\
 (\partial_t-L)A&=AB+\sum_iD_i^2,\\
 (\partial_t-L)B&=-2A,\\
 (\partial_t-L)D_i&=BD_i,\qquad F_2=-2.
\end{aligned}
\]
The tuple \(U=u,A=-u^2,B=-2u,D_i=\partial_i u\) solves it. Nonnegative
absorption gives \(0\leq u\leq P_tv\), and the linear derivative
equation with potential \(-2u\) gives
\(|D_i|\leq P_t|\partial_i v|\). Both the sampled means and physical
fields are bounded on each finite interval, where the polynomial
vector field is Lipschitz on their common range. Mild uniqueness
therefore identifies them. For \(C^1\) data, use the smooth equation
after a positive time and pass to time zero using these bounds.
No assumption that integrability automatically implies PDE
representation is used.

### Absolute mass is preserved despite the exact code reduction

At every finite completed depth, applying the likelihood cancellation
to the absolute sampled output gives exactly the nonnegative canonical
tree sum. The sums increase and are bounded by \(h_c(T,x)\). Monotone
convergence and the bounded-output dominated limit yield
\[
 \mathbb E|\widehat H_c(T,x)|=W_c(T,x).
\]
The \(F_2\) collapse does not combine opposite-sign alternatives:
every nonzero \(F_2\) completed tree is the no-event constant leaf.
Every finite \(F_k\), \(k\geq3\), tree has an increasing reaction-index
descendant chain ending in a zero terminal, so its contribution is
identically zero. The constant leaf's Brownian endpoint integrates to
\(-2\), with absolute mass \(2\). Thus the collapsed expansion has
the same signed sum and absolute mass, though it omits entire zero
syntactic subtrees and changes the random estimator.

## 4. Cost and value assessment

The scalar binary comparison was derived during this audit:
\[
 m_*(t)=\frac{\epsilon}{1-\epsilon I_0(t)},\qquad
 h_*=m_*G,\qquad \kappa_*=m_*w.
\]
The success probability at a clock event is \(G/w\), and the clock
rings with probability at most
\(\epsilon I_0(\infty)\leq1/48\).
Finite-depth scalar counts obey \(M_{n+1}\leq1+M_n/24\), giving
\(\mathbb E N_*\leq24/23\). The output satisfies
\(|\widehat H_*|\leq48\epsilon G/47\).
This baseline is exact at the same ideal-real level and has an explicit
power-based inverse clock. It also extends to \(d\geq3\) with
\(\epsilon I_0(\infty)<1/2\) for nonnegative Gaussian-envelope data.

The heat-flow approximation has the deterministic bound
\[
 0\leq P_Tv-u(T)\leq\epsilon^2 I_0(T)G(T),
\]
and the zero approximation has error at most \(\epsilon G(T)\).
For Gaussian data, \(P_Tv\) is explicit. These bounds prevent an
absolute-error target at long horizons from being mistaken for a
difficult practical problem merely because an unmodified tree has
large work.

No measured runtime, variance comparison, superiority claim or
worldwide novelty claim follows from this audit. The useful result is
the explicit conversion of this all-code envelope into a bounded
ideal sampler with a verified finite work recurrence.

## 5. Literature checked and the closest-mechanism limit

The inspected primary sources are linked in 04f Section 11:

* Ossiander (2004 preprint), a physical-space majorizing-kernel and
  \(h\)-Brownian representation of small-data Navier–Stokes solutions.
  T19 checked equation (18), Theorem 4.2 and Proposition 4.2. Bounded
  normalized outputs and a dominating 0/2 Galton–Watson tree are close
  precedents. Strict offspring probability below \(1/2\) gives a finite
  horizon-independent expected node count by an elementary deduction.
  This is not attributed as an explicit complexity theorem in the paper.
* Ikeda, Nagasawa and Watanabe (1966), transformation of branching
  Markov processes.
* Beznea, Boeangiu and Lupaşcu-Stamate (2020), Doob transforms and
  nonlocal branching; abstract/record access only.
* Agarwal and Claisse (2020), Proposition 3.4 on supersolution bounds
  for branching estimator moments in an elliptic setting.
* Henry-Labordère, Oudjane, Tan, Touzi and Warin, weighted polynomial
  branching diffusion representation.
* Nguwi, Penent and Privault, the derivative coding-tree representation.

These sources establish close mechanisms, not theorem-level priority
for the precise constants in 04f. The general idea of bounded
normalized branching with horizon-independent expected work is
therefore not treated as new here. No absence-of-prior-art inference
is made from the present search.

## 6. Fixed handoff gate and remaining implementation work

The minimal Lean gate is exactly 04f LT17.1 and LT17.2:

1. For any finite real list with all factors of magnitude at most one
   and a prefactor of magnitude at most one, its product has magnitude
   at most one; include a terminal-ratio lemma if useful.
2. For nonnegative real sequences starting at most one and satisfying
   the four finite-depth inequalities above, prove all four rational
   invariant bounds for every natural depth. Then derive \(R_n\leq112\)
   under \(R_n\leq2I_n\).

The proof strategy and all constants are fixed; an implementation worker
must return any mismatch instead of changing these statements silently.
Build logs, named declarations and transitive axiom output are required
before describing these finite claims as formally checked. The scalar
recurrence \(M_n\leq24/23\) is an optional baseline target, LT17.3.

Only after that gate should a numerical contract specify stable
monotone-clock inversion, leaf and label evaluation without underflow,
an explicit approximation/error policy, resource limits, and baselines.
At minimum it must preserve the exact distinction between event
probabilities and unconditional branch probabilities, independent
duplicate children, and the signs of \(A,B,F_2\).

The current accepted artifact is the conventional proof, not an
implemented or end-to-end formal sampler.
