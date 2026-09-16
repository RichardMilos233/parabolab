# First research milestone: a financial coding-tree moment theorem

> **Historical milestone; application inactive — reviewed 16 September 2026.**
> The multidimensional Merton application decision was superseded on
> 12 September. The mathematical analysis and check artifacts are retained;
> the “Proceed” recommendation and two-week/week-eight schedule below are
> historical and create no current tasks or deadlines. The active scope is
> [branching-PDE algorithms, scalar lambda, q, and mathematical guarantees](README.md).
> See also the [documentation map](../documentation-map.md).
> Implementation snapshots, dirty-file notes, registry corrections, test
> counts, and literature-version assessments describe the original audit,
> not the current checkout. This status review did not rerun the old checks
> or repeat the literature search.

Date: 12 September 2026. Programme: **Reliable branching Monte Carlo for nonlinear portfolio control: moment bounds, adaptive sampling, and policy accuracy.**

## Original decision and evidence boundary (application decision superseded)

**Proceed, with the theorem restricted to affine opportunity factors and a quadratic log-value driver.** The main analytical obstruction can be resolved for this class: high spatial derivative codes vanish **pathwise**, leaving a finite graded system. Below is an explicit second-moment majorant over the entire factor space, not a conditional assertion that a supersolution would suffice. A rational two-factor financial instance has a certified interval $0\le T-t\le 1/100$. The bound is conservative; it does not certify the assessment's $T=0.4$ experiment.

There is also a substantive obstruction to a seemingly modest extension: a quadratic, rather than affine, risk premium creates an unrestricted estimator with infinite absolute first moment at every positive horizon. Section 6 proves this through two actual mechanism alternatives. Smooth polynomial data and finite individual Gaussian polynomial moments do not prevent the failure.

These are **ordinary mathematical proofs developed and independently reviewed in this milestone**, with bounded symbolic checks of the mechanism. They are not new Lean-checked stochastic theorems. Publication priority remains unestablished. The new candidate contribution is the exact code reduction and quantitative certificate for this particular estimator on unbounded states; the scalar ODE comparison technique is established prior work.

Mathematical development/review used GPT-6 Astra Max subagents; bounded implementation and numerical/symbolic execution used GPT-5.6 Sol High. Both requested combinations were accepted. Existing dirty files (`demo/README.md`, `parabolab/solve.py`, `tests/test_solve.py`, `demo/dym.py`) are outside this change. No reproduction campaign, solver rewrite, dependency installation, or work in wavelab is part of this milestone.

## 1. Results and obligations at the 12 September audit

Audited inputs: [assessment](../../../research/quant_fyp_assessment_2026-09-12/assessment.md) in the sibling FYP research directory, its verification inventory and log-factor results, [proof registry](proof-registry.md), and the underlying notes linked below. The assessment files live outside this repository and must accompany it to rerun their imported checks. The registry's word “authoritative” is not an evidentiary premise. Its last-reviewed hash and some implementation pointers are stale.

| Area | Audited status | What must not be inferred / remaining work |
|---|---|---|
| Moment identities, PR-MOM-1–3 | The [moment note](estimator-integrity/notation-and-moment-theorem.md) correctly uses killed-depth indicators, conditional independence at one shared position, Tonelli and monotone convergence. The unrestricted identification assumes nonexplosion. | Its prefixed-point criterion does not construct a financial bound. Finite-depth approximations are lower approximations to absolute moments, not upper certificates. |
| Dym, PR-DYM-1–3 | The [five-particle argument](estimator-integrity/dym-nonintegrability.md) isolates $1/x$ under a strictly positive Gaussian density, restricts the other singular leaf away from zero, and splits signs. This is an ordinary non-$L^1$ proof for the specified real extension. | It violates the source paper's smoothness hypotheses and does not contradict that theorem. The older CLAUDE explanation attributing failure primarily to deep derivative growth is superseded by this shallow obstruction. |
| Proposals, PR-PROP-1–4 | [Finite optimizers and likelihood cancellation](estimator-integrity/adaptive-proposals.md) are valid under their stated support and integrability assumptions; the finite-depth multiplier retains its simultaneous pilot-error event and decision-count bound. | A probability floor is not a moment bound. The finite-depth likelihood argument targets the finite-depth mean; the unrestricted result additionally requires its stated $L^1$ passage. No generic empirical concentration theorem or full-tree adaptive performance guarantee is supplied. |
| Clocks, PR-RATE-1–4 | [Local convexity, topology kernels and binary Riccati oracle](estimator-integrity/exponential-rate-optimization.md) are useful completed results. The actual note numbers are Theorems 7.1, 7.2, 7.4 and 7.5, not the master table's 1.1–4.1. | The full-recursive short-time law needs uniform expansions and domination. Its nonzero terminal-leaf premise fails for log-value terminal data $u(T)=0$. |
| Financial derivation, PR-MM-1–4 | [Hamiltonian optimization, CRRA substitution, no-fixed-linear-index test, and Riccati coefficient matching](multifactor-merton-proofs.md) are sound algebra/PDE results under the displayed hypotheses. | They do not establish control admissibility, a verification theorem, or unrestricted tree integrability. “No fixed linear index” does not imply nonseparability, no closed form, or high-dimensional hardness. |
| Mechanism, PR-MM-5–7 | The wealth-domain obstruction is valid. The explicit-state/full-covariance source identity follows from the displayed second-order chain rule, including the mixed covariance term. | MM-7 remains conditional for the general class. The theorem below discharges its moment and uniqueness issues only in the finite graded specialization. |
| Implementation at that audit | `StateDependentPDEnD` and `StateDependentMechanismND` exist in `parabolab/state_dependent.py`; drift-as-source and exact support pruning already work. Positive-definite constant covariance can be whitened. | Native full covariance is not implemented. `finite_depth_moment_1d` and `finite_depth_moment_derivatives_1d` are one-dimensional and are not certified quadrature. The registry's `iterate_moments` and `optimal_tuple_proposal` names did not match the audited API (`sqrt_optimal_probabilities` is the latter). |
| Existing verification | The assessment records 17 targeted moment/proposal/rate tests, 6 state-dependent tests, and a successful existing Lean build. Its log-factor checks support algebra, coordinate mapping and ODE consistency. | Those are historical targeted runs, not a fresh full-suite run in this milestone. ODE-method agreement and residuals are not validated numerical error bounds or moment proofs. |
| Lean boundary | `FiniteTree.lean` defines a finite algebraic operator; `MomentIteration.lean` proves order/iteration properties; Dym, proposal and rate files formalize selected substatements. | Brownian construction, spatial/time integration, random-tree exhaustion, the financial model and this milestone's proofs are not formalized there. A build verifies the statements written, not these omitted obligations. |

The named `lean-proof` skill supplies the hardest-case-first and one-tactic-at-a-time discipline for any later formalization. `lean4-setup` concerns building a Lean compiler repository; this is an already functioning Lake/mathlib project, so compiler rebuilding is inapplicable. No new Lean implementation was delegated before settling the mathematical statement, and no infrastructure was rebuilt.

## 2. Closest primary sources and the exact gap

| Primary source | Applicable result and hypothesis boundary |
|---|---|
| [Nguwi–Penent–Privault, JEQ2023](https://doi.org/10.1007/s00028-023-00873-3), Assumption A, Theorem 1, Proposition 4.2 | The arbitrary-jet representation assumes smoothness, appropriate Gaussian-weighted integrability, all-code absolute integrability and coupled mild-system uniqueness. Its sufficient terminal-code criterion uses a uniform $K<1$, $K\le\bar F(T)$, a decreasing lifetime density, and $\rho(T)\ge1/\inf q_c$. Here the terminal source code is an unbounded quadratic (h(z)), so even its zeroth-code supremum fails. Explicit factor dependence also needs the extended mechanism. The [author preprint](https://personal.ntu.edu.sg/nprivault/papers/fully_nonlinear_feynman-kac.pdf) numbers the corresponding results Theorem 4.2 and Proposition 4.3. |
| [Nguwi–Penent–Privault, JCP2024](https://doi.org/10.1016/j.jcp.2023.112712), §2 and Appendix A ([preprint](https://arxiv.org/abs/2203.03234)) | Multidimensional code algebra and neural regression do not remove integrability or coupled-system uniqueness assumptions. Its existing Merton experiment already precludes novelty based solely on applying branching to portfolio control. |
| [Huang–Privault, stability, v2](https://arxiv.org/html/2502.17853v2) | Latest arXiv version located: v2, 9 March 2026 ([version record](https://arxiv.org/abs/2502.17853)). It studies $u_t+\frac12\Delta u+f(u)=0$, with normalized derivatives, a different binary mechanism, and special probabilities. Propositions 2.5–2.6 bound all terminal derivatives and derivatives of $f^{(j)}(\phi)$ in global sup norm, using specified factorial/exponential growth and clock conditions. Theorem 2.8 also needs a classical solution in its code-growth class. Theorem 2.10 retains the consistency condition $u_f=f(u_{\mathrm{Id}})$; Proposition 8.4 provides sufficient enlarged-system/uniform-integrability conditions. These are substantial stability and uniqueness results, but do not directly certify our explicit-state quadratic-gradient driver or unbounded $h$. Replacing our tree by theirs would change the estimator, not just its proposal. |
| [Henry-Labordère–Oudjane–Tan–Touzi–Warin, 2019](https://arxiv.org/pdf/1603.01727), §3.2, Theorem 3.12, §4 | Polynomial drivers involving gradients, branching moment bounds from a scalar ODE, and extensions to PDE systems are established. Their Malliavin-weight estimator differs from this coding tree; the stated bounded coefficient/drift conditions do not directly cover the unbounded affine drift and quadratic potential here. Moving drift into an OU reference would require a different mechanism and derivative-commutator analysis. |
| [Liu, Portfolio Selection in Stochastic Environments](https://rady.ucsd.edu/_files/faculty-research/liu/portfolio.pdf), and [Zariphopoulou, 2001](https://doi.org/10.1007/PL00000040) | Quadratic-factor portfolio solutions, Riccati reductions and power/exponential transformations have established antecedents. They supply benchmarks and context, not a new branching moment certificate. |

**Remaining gap addressed here:** establish an actual whole-space bound for every reached code of the existing financial sampler, then identify its mean without assuming uniqueness of an arbitrary infinite system. The potentially new part is the pathwise high-code extinction, finite graded quotient, and quantitative consequence for this named estimator. Neither a general ODE-majorant invention nor a priority claim is justified by this bounded literature search. The obstruction in Section 6 also needs a targeted priority check before being described as new.

## 3. Financial formulation audit

Use wealth $X>0$, factors $Y\in\mathbb R^2$, terminal utility $U(X_T)=X_T^a/a$, $a=1-\gamma$, initially $0<\gamma<1$, and no intermediate consumption. Here $\pi$ denotes risky-asset wealth fractions and the objective is

$$
V(t,x,y)=\sup_{\pi}\mathbb E[e^{-\delta(T-t)}U(X_T)\mid X_t=x,Y_t=y].
$$

The admissible class must preserve positive wealth under

$$
dX_s=X_s[r(Y_s)+\pi_s^\top\lambda(Y_s)]ds+X_s\pi_s^\top S\,dW_s,
\qquad dY_s=b(Y_s)ds+D\,dW_s.
$$

Let return and factor shocks have these common Brownian loadings $S,D$:

$$
\Sigma=SS^\top\succ0,\quad A=DD^\top\succ0,\quad C=SD^\top,
\qquad\begin{pmatrix}\Sigma&C\\C^\top&A\end{pmatrix}\succeq0.
$$

For a specified scalar correlation, $C_{ij}=\sigma_i\sigma_{Y_j}\rho_{ij}$; correlation alone is not covariance. Joint loadings, or a Schur-complement check, are required. The reference Brownian motion used by the tree need not be the physical factor dynamics: its omitted drift remains in the source.

With $R=\Sigma^{-1}$, $V=x^aF/a$, the optimized terminal-wealth HJB reduces algebraically to

$$
 F_t+b\cdot\nabla F+\tfrac12 A:D^2F+(ar-\delta)F
 +\frac{a}{2\gamma F}(\lambda F+C\nabla F)^\top R(\lambda F+C\nabla F)=0,
 \qquad F(T)=1.
$$

The notation $\lambda(y)$ denotes the **financial excess-return vector**; $\ell>0$ below denotes a **tree clock rate**. They are different quantities. For $F>0$, put $g=\log F$. Substituting $D^2F/F=D^2g+\nabla g\nabla g^\top$ gives

$$
g_t+\tfrac12A:D^2g+\widetilde b\cdot\nabla g
+\tfrac12\nabla g^\top M\nabla g+h=0,\qquad g(T)=0,
$$
$$
\widetilde b=b+\frac a\gamma C^\top R\lambda,
\quad M=A+\frac a\gamma C^\top RC,
\quad h=ar-\delta+\frac a{2\gamma}\lambda^\top R\lambda.
$$

Whiten using **a square invertible** $B$ with $A=BB^\top$, $y=Bz$, $u(t,z)=g(t,Bz)$. Then

$$
\nabla_y g=B^{-\top}\nabla_z u,\quad A:D_y^2g=\Delta_z u,
\quad d(z)=B^{-1}\widetilde b(Bz),\quad N=B^{-1}MB^{-\top}.
$$

All physical coefficient functions must be evaluated at (Bz). The assessment script previously corrected exactly this coordinate error. Its general rectangular joint shock loading is not this square whitening matrix. The policy and error map are

$$
\pi^*(t,Bz)=\frac1\gamma R[\lambda(Bz)+CB^{-\top}\nabla u(t,z)],
\quad
\|\widehat\pi-\pi^*\|\le\frac{\|RCB^{-\top}\|_{\rm op}}\gamma
\|\widehat d-\nabla u\|.
$$

This condition number issue matters even when whitening is algebraically valid. Exponentiating a noisy $u$ estimate is a plug-in estimate of $F$, not an unbiased one.

For affine $b=k-Ky$, $\lambda=l+Ly$, $r=r_0+r_1^\top y$, the whitened equation has precisely

$$
u_t+\tfrac12\Delta u+f(z,\nabla u)=0,\qquad
f(z,p)=(d_0+D_0z)\cdot p+\tfrac12p^\top Np
+h_0+h_1^\top z+\tfrac12z^\top Qz.\tag{1}
$$

The Riccati benchmark is $g(T-\tau,y)=\alpha+\beta^\top y+\frac12y^\top Py$. Equivalently, in whitened coordinates with the same polynomial convention,

$$
P'=D_0^\top P+PD_0+PNP+Q,
\quad \beta'=Pd_0+D_0^\top\beta+PN\beta+h_1,
$$
$$
\alpha'=\tfrac12\operatorname{tr}P+d_0^\top\beta
+\tfrac12\beta^\top N\beta+h_0,
\qquad(P,\beta,\alpha)(0)=0.\tag{2}
$$

This matches the physical-coordinate system in MM-4 after transformation. ODE existence and coefficient matching provide a classical PDE solution on the ODE's existence interval. They do not themselves establish a control verification theorem.

The precise additional control obligations are positive-wealth admissibility of the feedback, the chosen admissible-control class, sufficient integrability/localization to pass the discounted Itô identity to expectations, and terminal transversality. Completing the square gives the local Hamiltonian gap

$$
\mathcal H(\pi^*)-\mathcal H(\pi)
=\frac\gamma2 x^aF(\pi-\pi^*)^\top\Sigma(\pi-\pi^*).
$$

Only after those control obligations are proved does its time integral yield an expected terminal-utility loss. Pointwise policy confidence is not a pathwise or realized-profit guarantee. For one asset and two full-rank factors, $C\ne0$, $a\ne0$, the rank-one matrix $M-A$ cannot equal $(\kappa-1)A$; hence a scalar $e^{\kappa g}$ cannot cancel the quadratic term for all gradients. This does not exclude Riccati or other reductions.

## 4. Candidate theorem, now with an ordinary proof

### The estimator and its finite constants

Call the exact-arithmetic estimator for (1) the **quadratic-log factor coding-tree estimator**. It uses the existing `StateDependentMechanismND`, `sigma2=1`, terminal zero, derivative map `((0,0),(1,0),(0,1))` (the value jet is unused), exact polynomial-support reduction, uniform sampling over the resulting **labelled** tuples, and a common exponential clock $\ell$. There is no depth cap, filtering, state truncation, or extra pruning of high derivatives. All children share the parent's position and have independent future randomness. The theorem concerns the mathematical law specified by these conventions; finite-precision overflow and runtime interruptions are separate implementation issues.

Write $D^\mu$ for spatial derivative codes, identifying $D^0$ with Id. Normalize a source code to

$$
G_{\beta,\nu}=(\partial_z^\beta\partial_p^\nu f)^*.
$$

Its incoming scalar multiplier is kept explicitly, not discarded. The potentially nonzero normalized types are the six $D^\mu$ with $|\mu|\le2$, and the fifteen $G_{\beta,\nu}$ with $|\beta|+|\nu|\le2$, excluding identically zero source polynomials. Thus there are at most 21 types. A derivative in the unused value jet is identically zero. Assign

$$
r(D^\mu)=2-|\mu|,\qquad r(G_{\beta,\nu})=2-|\beta|-|\nu|.\tag{3}
$$

For each normalized parent $c$, retain its original table size $m_c$, probabilities $q_{c,j}=1/m_c$, and duplicate labelled occurrences. Extract all scalar child multipliers as an external product $a_{c,j}$. A tuple with an identically zero source, zero scalar, or high derivative has zero contribution to the constants, but **its probability is not redistributed**. Let $g_c(z)$ be the normalized terminal polynomial, and let $L_c$ be the sum of the absolute values of its standard-monomial coefficients. Define

$$
A_0=\max\{1,\max_c L_c^2\},\quad
\mathcal B=\max_c\sum_{j\text{ nonzero}}\frac{|a_{c,j}|^2}{q_{c,j}},
\quad K=\mathcal B/\ell,\quad c_0=\ell+4.\tag{4}
$$

These are finite, directly checkable constants. For the source convention (1), uniformly over its real polynomial coefficients,

| Parent family | Largest original table size | Nonzero sum of squared outside coefficients | Bound for row contribution to $\mathcal B$ |
|---|---:|---:|---:|
| Id | 1 | 1 | 1 |
| First spatial derivative | 3 | 3 | 9 |
| Second spatial derivative | 11 | 9 (two high-derivative alternatives are zero) | 99 |
| Undifferentiated $G$ | 20 | $25/2$ | 250 |
| First partial derivative of $G$ | 6 | 6 | 36 |
| Second partial derivative of $G$ | zero fallback | 0 | 0 |

The undifferentiated row has six coefficient-one chain terms, two coefficient-(-1/2) pure spatial terms, four coefficient-(-1) mixed terms, and eight coefficient-(-1/2) jet-Hessian terms. Actual zeros can only reduce both table size and squared-coefficient sum. Source polynomial coefficients reside inside normalized terminal/source functions; they are not silently added a second time to $a_{c,j}$. In particular, $\mathcal B\le250$.

### Theorem M1 (whole-space second-moment certificate)

For estimator (1)–(4), define, when $K>0$,

$$
\tau_* =\frac1{2c_0}\log\left(1+\frac{c_0}{K A_0^2}\right),
\quad
b(\tau)=\frac{A_0e^{c_0\tau}}
 {\sqrt{1-\frac{K A_0^2}{c_0}(e^{2c_0\tau}-1)}}.\tag{5}
$$

If $K=0$, set $\tau_*=\infty$, $b(\tau)=A_0e^{c_0\tau}$. For every $0\le\tau<\tau_*$, every $z\in\mathbb R^2$, and each normalized surviving type,

$$
\boxed{\mathbb E|H_{T-\tau,z,c}|^2\le
b(\tau)(1+|z|^2)^{r(c)}.}\tag{6}
$$

For incoming scalar $s$, multiply the right side by $|s|^2$. All $D^\mu$ of order at least three and all zero source/scalar codes have zero functionals almost surely. The unrestricted tree is nonexplosive; its expected particle count is at most $(3e^{2\ell\tau}-1)/2$. Its means are the Riccati code fields in (2), including $\mathbb EH_{\rm Id}=u$ and $\mathbb EH_{D_i}=\partial_i u$, on this interval. This is identification within the finite polynomial code system, not unrestricted uniqueness of every possible unbounded PDE solution, and not stochastic-control verification.

### Proof

**1. Nonexplosion before using pathwise zero arguments.** Every nonzero source derivative has jet order at most two. A term in $D^\mu f(z,\nabla u)$ therefore contains at most two derivative factors and one source factor, irrespective of $|\mu|$. A source-code row differentiates $f$ only once in space in its chain part, so it also has at most three children. Zero fallback rows have one child. A common finite clock is consequently dominated by a process in which every particle splits into three at rate $\ell$. Its active population has mean $e^{2\ell\tau}$; integrating the birth intensity $3\ell e^{2\ell s}$ bounds total born particles by $(3e^{2\ell\tau}-1)/2$, hence proves nonexplosion. This bounds node count, not symbolic table-construction cost.

**2. High-code extinction is pathwise.** For $|\mu|\ge3$, differentiating the quadratic potential gives zero. Differentiating an affine coefficient times $\partial_i u$ leaves a derivative of $u$ of order $|\mu|+1$ or $|\mu|$. Differentiating $\partial_i u\partial_j u$ distributes a total derivative order $|\mu|+2\ge5$ between two children, so at least one has order at least three. Every nonzero tuple therefore carries another high derivative. Following such a child in a finite realized tree must reach a terminal high derivative of zero data. Its zero propagates to the root product. This does not use the Riccati solution or cancellation of expectations.

Scalar normalization is also pathwise under coupling: the current tables and their uniform probabilities depend on $(\beta,\nu)$, not the incoming scalar. Each ordinary source tuple scales exactly one child. A constant-source row instead returns the fixed zero-scalar fallback; that branch vanishes in both coupled evaluations. Following the scalar lineage to a leaf, or to such a zero branch, yields $H_{sG}=sH_G$, including $s=0$. The current zero predicate need not prune scalar-zero codes immediately for this proof to hold.

**3. Grade closure includes every remaining code.** Chain/product differentiation reduces the grade in (3) by one per spatial derivative. Surviving $D^\mu$ tuples therefore have child-grade sum $2-|\mu|$. In a $G$ row, the chain term combines a source of grade $r-1$ with the expansion of $D_i f$, which has grade one. Each direct spatial, mixed, or jet-Hessian correction has total grade $r-2$. Thus every surviving tuple satisfies

$$
0\le\sum_j r(c_j)\le r(c),\qquad 1\le\#\{c_j\}\le3.\tag{7}
$$

No claim that terminal-zero Hessian or gradient codes are zero is made: they have nonzero source branches. Constant source codes are also retained; they return their terminal constant on survival and zero on branching.

**4. Whole-space weights.** Put $w_r(z)=(1+|z|^2)^r$. A monomial of degree at most $r$ is bounded in magnitude by $(1+|z|^2)^{r/2}$, so $|g_c|^2\le L_c^2 w_{r(c)}$. Equation (7) gives $\prod_j w_{r(c_j)}\le w_{r(c)}$. In dimension two,

$$
\tfrac12\Delta w_0=0,\quad \tfrac12\Delta w_1=2,\quad
\tfrac12\Delta w_2=4+8|z|^2\le4w_2.
$$

Gaussian polynomial moments and the semigroup differential inequality give $P_s w_r\le e^{4s}w_r$ for all three grades. There is no bounded-domain step.

**5. Construct the prefixed point.** The exact second-moment recursion, in remaining time, is

$$
(\Phi_2 V)_c(\tau,z)=e^{\ell\tau}P_\tau|g_c|^2(z)
+\sum_j\frac{|a_{c,j}|^2}{\ell q_{c,j}}
\int_0^\tau e^{\ell s}P_s\!\left[\prod_i V_{c_{j,i}}(\tau-s,\cdot)\right](z)\,ds.\tag{8}
$$

Set $W_c(\tau,z)=b(\tau)w_{r(c)}(z)$. Equation (5) solves

$$
b'=c_0b+Kb^3,\qquad b(0)=A_0\ge1,
$$

so $b\ge1$. For arity one through three, $b^k\le b^3$. Substituting the explicit weight estimates into (8) gives

$$
(\Phi_2W)_c\le w_{r(c)}\left[A_0e^{c_0\tau}
+K\int_0^\tau e^{c_0s}b(\tau-s)^3\,ds\right]=W_c.
$$

Apply this to each finite killed-depth moment, starting at zero. Induction bounds all iterates by $W$. Nonexplosion and monotone convergence identify their limit with the unrestricted second moment. This proves (6); Cauchy–Schwarz supplies $L^1$. The formula (5), not an assumed finite unknown function, establishes a positive interval.

**6. Mean identification closes the remaining uniqueness issue.** After eliminating pathwise-zero types, every killed-depth mean is a polynomial of degree at most (r(c)): its initial data, products and heat transitions preserve this finite graded family. For each type, evaluate on a fixed unisolvent finite set for polynomials of that degree. The $L^1$ killed-depth convergence just proved implies convergence at these points, and hence convergence of all polynomial coefficients. Thus the full means also belong to this polynomial family.

The bound (6) makes their coefficients locally bounded in time, by the same finite interpolation. Passing to the first-event mean identity is legitimate by absolute integrability (or dominated killed-depth convergence). The finite coefficient vector satisfies

$$
\partial_\tau m_c=\tfrac12\Delta m_c+\sum_j a_{c,j}\prod_i m_{c_{j,i}},
\qquad m_c(0)=g_c,
$$

a finite-dimensional polynomial ODE. Its mild form gives continuity, and its polynomial vector field is locally Lipschitz. The Riccati code fields solve this same initial-value problem, so local ODE uniqueness identifies them. This holds first on their common existence interval. If the Riccati coefficients were to blow up before any fixed $h<\tau_*$, the already bounded Id, gradient and Hessian mean coefficients would bound $(\alpha,\beta,P)$ up to that time, contradicting the ODE continuation criterion. Identification therefore extends throughout $\tau<\tau_*$. No infinite-system uniqueness hypothesis is left hidden. $\square$

### A named rational financial instance

Take one asset, two OU factors, and

$$
\gamma=\tfrac12,\quad\Sigma=1,\quad A=I_2,\quad C=(\tfrac12,\tfrac14),
\quad b(y)=-y,\quad r(y)=y_1/10,\quad\lambda(y)=y_2/10,\quad\delta=0.
\tag{9}
$$

The covariance is physical: take factor Brownian motions $W^1,W^2$, and the asset return shock $\frac12dW^1+\frac14dW^2+\frac{\sqrt{11}}4dW^3$. The factor Schur complement has eigenvalues $1,11/16>0$. No whitening is needed in this exact example. The source is

$$
 f(y,p)=(-y_1+y_2/20)p_1-\frac{39}{40}y_2p_2
+\frac12p^\top\begin{pmatrix}5/4&1/8\\1/8&17/16\end{pmatrix}p
+\frac{y_1}{20}+\frac{y_2^2}{200}.\tag{10}
$$

Here $A_0=25/16$, from the largest normalized terminal coefficient norm $5/4$. Choose the existing uniform sampler with **clock rate $\ell=32$**. The safe generic bound $\mathcal B\le250$ gives $K=125/16$, $c_0=36$. All normalized code moments satisfy the particularly simple certificate

$$
\boxed{\mathbb E|H_c|^2\le6(1+|y|^2)^{r(c)},
\qquad 0\le T-t\le1/100,\quad y\in\mathbb R^2.}\tag{11}
$$

This interval can be certified using rational inequalities alone. For $\tau\le1/100$,

$$
e^{36\tau}\le(1-36/100)^{-1}=25/16,
\quad e^{72\tau}-1\le(25/16)^2-1=369/256.
$$

Thus the denominator squared in (5) is at least

$$
1-\frac{78125}{147456}\frac{369}{256}>1/5,
$$

while its numerator is at most $(25/16)^2<5/2$. Therefore $b^2<125/4<36$, proving (11). This uses $e^x\le(1-x)^{-1}$ for $0\le x<1$, directly from the power series, and is independent of floating-point ODE output.

The short-rate and excess-return loadings are nonparallel, so this example fails the fixed-linear-index reduction test. It still has a Riccati solution, and portions may be separable; it is a validation model, not evidence of computational superiority over analytic finance. Its feedback is $\pi^*=y_2/5+u_{y_1}+u_{y_2}/2$. Equation (11) supports pointwise gradient and policy inference on this small interval, but its constants can make confidence bounds loose. Economically useful horizons and precision are still development targets.

## 5. Attempts that failed, and why

| Attempt | Outcome |
|---|---|
| Transfer the source papers' uniform terminal bounds | Fails immediately: $G_{0,0}(T,z)=h(z)$ is unbounded. Scaling code labels cannot turn a nonconstant polynomial into a bounded function. |
| Use positivity of $F$, smoothness, or a stable Riccati solution as a tree certificate | Invalid implication. These describe the PDE solution, not absolute products under the tree law. Section 6 gives a concrete smooth-data obstruction. |
| Drop high derivatives because the Riccati solution is quadratic | Circular until pathwise extinction is proved. Step 2 is the required repair. Dropping those labels and renormalizing their probability would also change the estimator being certified. |
| Use the same polynomial or Gaussian weight for all codes | Positive product branches increase its spatial power/exponent. A single grade-blind bound does not close. The code-specific degree assignment is essential. |
| Infer an upper bound from several small Picard iterates or finite sample variances | Those moment iterates are lower approximations. Neither finite simulations nor cutoff stability certify the omitted tail. None was used as an upper certificate. |
| Reuse the old short-time optimal clock law | The log-value leaf is zero. Even the frozen objective $J(\ell)=A(e^{\ell\tau}-1)/\ell^2$ has minimizer $\ell\tau\approx1.59362426$, not an (O(1)) rate. This does not establish an optimum for the full financial tree. |
| Extend the finite graded proof to any smooth nonquadratic premium | False as a blanket expectation claim. The next section proves absolute-moment divergence for a quadratic premium. A small coefficient does not repair its unbounded-state tail. |

The scalar majorant deliberately sacrifices code-specific constants, zero terminal data for Id/gradients, and lower arities. It proves existence of a regime, not an efficient sampling method or an optimal clock. A finite vector of polynomial-weight bounds is the next refinement. Its numerical ODE solution alone would still need an analytic enclosure or validated residual inequality to become an upper certificate.

## 6. A verified obstruction: quadratic risk premium

Keep (9) but replace the financial premium by $\lambda(y)=y_2^2/10$. This is an analytical stress case, not an extra application programme. Its source has

$$
h(y)=y_1/20+y_2^4/200,\quad
\widetilde b(y)=(-y_1+y_2^2/20,-y_2+y_2^2/40),\quad N_{22}=17/16.
$$

Use any common finite positive exponential clock, with the original uniform full-support, exact-zero-reduced tables and no depth cap or filtering. Write $D=D^{(0,2)}$, and

$$
A_c(\tau,y)=\mathbb E|H_{T-\tau,y,c}|\in[0,\infty].
$$

Two labelled alternatives in the actual $D$ table are

$$
(G_{y_2y_2}),\qquad (G_{p_2p_2},D,D).\tag{12}
$$

The terminal factors of these two source codes are $3y_2^2/50$ and $17/16$. The latter is a constant source code: its branches have zero functional, and its absolute first moment equals $17/16$. All trees remain nonexplosive because jet degree is at most two and offspring count at most three, even though higher spatial derivatives now survive.

**Claim M1-O:** for every $\tau>0$ and finite $y$, the $D^{(0,2)}$, $D^{(0,1)}$, and Id root functionals have infinite absolute first moment. In particular none has a finite second moment.

**Proof.** First-order absolute moments have an exact nonnegative heat-convolution recursion: $q$ and the lifetime density cancel. Restricting to the first alternative in (12) and a surviving child yields

$$
A_D(\varepsilon,y)\ge\frac3{50}\varepsilon P_\varepsilon[y_2^2](y).\tag{13}
$$

The full nonnegative recursion can be restarted at any remaining time $\varepsilon$. This follows by splitting its time integral and applying the semigroup property and Tonelli, including extended values. The second alternative in (12) then gives, with $c=17/16$,

$$
A_D(\varepsilon+u)\ge P_uA_D(\varepsilon)
+c\int_0^u P_{u-s}[A_D(\varepsilon+s)^2]\,ds.\tag{14}
$$

Suppose $A_D(\varepsilon+\delta,R)<\infty$. For $0\le u\le\delta$, define

$$
F(u)=P_{\delta-u}A_D(\varepsilon+u)(R),
\quad A=P_\delta A_D(\varepsilon)(R).
$$

The restarted recursion bounds $F(u)\le A_D(\varepsilon+\delta,R)$. Applying $P_{\delta-u}$ to (14), and Jensen's inequality to each probability kernel, gives

$$
F(u)\ge A+c\int_0^uF(s)^2ds,
\qquad A\ge\frac3{50}\varepsilon(R_2^2+\varepsilon+\delta)>0.\tag{15}
$$

For completeness set $G(u)=A+c\int_0^uF(s)^2ds$. Then $F\ge G\ge A>0$, $G'\ge cG^2$ almost everywhere, and $(1/G)'\le-c$. A bounded $F$ on $[0,\delta]$ consequently requires $c\delta A<1$. Equation (15) violates this for all sufficiently large $|R_2|$. Thus $A_D(\varepsilon+\delta,R)=\infty$ on a nonempty open set of factor states.

For any desired horizon $h>0$, take $\varepsilon=\delta=h/3$. Restart for the final $h/3$:

$$
A_D(h,y)\ge P_{h/3}A_D(2h/3,\cdot)(y)=\infty
$$

because the Gaussian density is strictly positive on that open set from every $y$. This proves the Hessian assertion.

The $D^{(0,1)}$ table contains $(G_{p_2},D)$, and the $G_{0,0}$ table contains $(G_{p_2},G_{p_2},D)$. The terminal polynomial of $G_{p_2}$ is $-y_2+y_2^2/40$; its Gaussian absolute moment is strictly positive at every state for positive remaining time. The corresponding product moment terms therefore force $A_{D^{(0,1)}}=A_{G_{0,0}}=\infty$, and Id's singleton source branch forces $A_{\rm Id}=\infty$. No subtraction of signed infinities or inference from simulation is used. $\square$

This claim concerns the unrestricted estimator and positive horizons. At every fixed depth all absolute moments are finite: there are finitely many possible nodes and codes, bounded clock likelihoods on a fixed horizon, and polynomial terminal factors under Gaussian transitions. The infinite-depth limit nevertheless has infinite absolute first moment. This is an unbounded-state/infinite-depth obstruction, distinct from Dym's finite-topology singularity. No fixed positive clock rate repairs it, since the first absolute-moment recursion cancels that rate. The argument would also rule out finite polynomial majorants, but proves the stronger failure of $L^1$ itself. It does not prove that both signed parts diverge, identify an expectation by cancellation, or assert that the control value for this $0<\gamma<1$ stress case is finite. It also does not rule out every bounded smooth perturbation.

A useful distinction is available within the same model: at $\gamma=2$, $a=-1$, the corresponding constants become $h=-y_1/10-y_2^4/400$, $h_{22}=-3y_2^2/100$, $N_{22}=31/32>0$. Taking absolute values repeats the proof. For any admissible-control class preserving positive wealth and containing the zero-risky-position policy, the terminal-utility supremum is a finite real number: $U(w)=-1/w\le0$, while the zero-risky-position policy has a finite negative expected utility, since the integral of the Gaussian OU short rate has all finite exponential moments. Thus the supremum lies between a finite negative number and zero. This elementary bound does **not** establish strict positivity of a factor $F$, a smooth log-value solution, or a full control verification theorem. The estimator obstruction does not require those additional claims.

## 7. Bounded verification and reproducibility

Companion files: [check script](milestone-1-checks.py), [machine-readable results](milestone-1-checks.json), and [text results](milestone-1-checks.txt). Run from the repository root:

```sh
conda run --no-capture-output -n parabolab python docs/research/milestone-1-checks.py
```

The script reuses the assessment's deterministic functions without calling its main function, so it does not overwrite the assessment outputs. It records the imported script's SHA-256 and the complete labelled graphs. The environment is `/opt/miniconda3/envs/parabolab/bin/python`: Python 3.11.15, NumPy 2.4.6, SymPy 1.14.0, SciPy 1.17.1. No seeds apply: all checks are deterministic, and there was no Monte Carlo run or dependency installation.

| Bounded check | Result | Evidentiary meaning |
|---|---|---|
| Generic quadratic graph | 21 normalized types; 94 original reduced labels; 78 nonzero retained labels; largest row 20; maximum arity 3; exact $\mathcal B=250$ | Finite coefficient/table check; the large arbitrary generic coefficients are for support coverage, not financial calibration. |
| Rational financial graph (10) | 18 types (6 derivative/Id, 12 source); 81 original reduced labels; 68 retained; largest row 18; exact $\mathcal B=405/2$, $K=405/64$ at clock 32; $A_0=25/16$ | Confirms that (11) is conservative for the actual mechanism. Its sharper scalar denominator vanishes at approximately 0.016708653; this decimal is not the rational interval certificate. |
| Higher derivatives | 15 multiindices of orders 3–5; 28,224 expansion terms; zero invariant violations | Finite symbolic corroboration. The proof for every order is Section 4, not extrapolation from these counts. |
| Nonquadratic stress, both $\gamma=1/2$ and $\gamma=2$ | Required forcing, feedback, propagation and constant-zero-branch labels found exactly; terminal polynomials and constants match Section 6 | Confirms the code/table correspondence of the ordinary obstruction proof. |
| Existing log-factor audit | Symbolic PDE transform and Hamiltonian gap zero; joint covariance minimum eigenvalue about 0.00808216 | Algebra and covariance checks for the assessment's synthetic model. |
| Existing Riccati/coordinate checks | DOP853–Radau difference $4.40\times10^{-14}$; log/direct residuals $2.08\times10^{-17}$, $4.16\times10^{-17}$; whitened/API source differences $1.73\times10^{-18}$, $4.86\times10^{-16}$ | Reproduces existing deterministic checks. These decimals do not validate stochastic moments or an exact ODE error bound. |
| Assessment's whitened moment constants | Floating $A_0\approx2.7605944$, $\mathcal B=250$, scalar threshold about 0.00656817 at clock 32 | A diagnostic showing the bound's conservatism. The floating source coefficients have no interval enclosure; this does not certify its 0.4 horizon. |
| Lean resolution, read only | The commands below resolve root stable to 4.33.1 and the formal project to 4.33.0 | The assessment's apparent mismatch was a working-directory/default distinction. No compiler rebuild, toolchain installation or version change is required. |

The version inventory runs `lean --version`, `lake --version` and `elan show` from both the repository root and its formal directory; commands, working directories and actual outputs are retained in the JSON. It checks the formal 4.33.0 pin.

Execution limitation: an initial run was interrupted after approximately 120 seconds because the check script searched incrementally for a very large rational horizon denominator in the deliberately large-coefficient generic fixture. Replacing that search by the direct bound $n>2c_0+2KA_0^2$ removed the script overhead. It was not a model instability or an expensive Monte Carlo experiment. The final scientific checks completed in 2.217 seconds (about 4.5 seconds including conda launch); subsequent reruns will record their own elapsed time.

The rational inequality in (11) supplies the actual upper certificate. Floating-point coefficient norms, ODE-method agreement, and finite-depth moment approximations do not. The generated report also contains a cruder automated rational horizon; use its explicitly named `conservative_T_1_over_100_certificate` for (11). The obstruction uses exact row membership plus the ordinary Tonelli/Jensen proof, not a numerically exploding Picard sequence.

## 8. Historical two-week work plan and week-eight gate (inactive)

The application was dropped after this plan was written. The dates and
targets below are preserved to explain the original decision criteria;
they are not current deadlines or outstanding work. The retained theorem
and obstruction can be cited within their stated scope without restarting
the financial programme.

Theorem M1 and obstruction M1-O provide one focused research story: characterize when the selected portfolio estimator is a legitimate expectation, improve sampling inside that supported regime, and measure the resulting policy error. They do not justify adding further financial domains.

| Time | Concrete work and deliverable | Success / stopping rule |
|---|---|---|
| Days 1–3 | Have the supervisor review the exact code-extinction proof, scalar normalization, finite-ODE identification and obstruction; compare their scope with the cited stability and polynomial-system papers. Produce a corrected claim/priority checklist. | If the theorem is already a direct published corollary for this estimator, frame the work as a quantitative specialization and seek a sharper useful bound, rather than relabeling it new. |
| Days 4–7 | Replace the common scalar envelope with a small code-specific polynomial-weight system, exploiting zero root leaves and actual coefficient/probability tables. Enclose one solution analytically or by validated residual bounds. Separately write the admissible-control and verification conditions for the affine benchmark. | Produce a rigorously improved horizon or a quantified explanation of conservatism. A small computed lower moment is not a pass. No broad solver change is needed. |
| Days 8–10 | Reuse the financial check fixture to sample Id and the two gradient roots with the existing API in a small, timed, predeclared budget. Compare physical-coordinate policies with the Riccati reference. Preserve separate pilot/evaluation seeds and report interruptions. | Check implementation correspondence, not moment existence. Obtain approval before any expensive batch or dependency change; begin with only inexpensive smoke checks. |
| Days 11–14 | Compare a competent fixed clock with one frozen tuple proposal on the certified regime, counting setup and pilot work. Draft pointwise policy bands from the proven moments and list the remaining control-verification obligations. | Deliver one cost/accuracy comparison with uncertainty, one usable certificate or an explicit limitation, and a two-page supervisory decision memo. Do not add another adaptive mechanism if pilot cost erases the gain. |

**Week-eight decision gate: 7 November 2026.** Continue the full six-month plan only if there is $i$ an independently scrutinized theorem with a credible literature boundary; (ii) a quantitatively usable affine two-factor regime, or a justified explanation of why the initial bound must remain small; (iii) tested gradient-to-policy correspondence and explicit control-verification status; and (iv) a financially informative application plan with an honest comparator.

An aspirational quantitative target is a certified horizon of at least 0.05 in the fixed declared time units, together with policy uncertainty small enough to resolve a predeclared allocation difference. This is a decision criterion, not a proved promise. If only the crude (0.01) existence certificate remains, assess whether its boundary theorem and negative result are sufficient for a strong numerical-probability FYP. Narrow to those supported results if necessary; do not spend the remaining months assuming a nonquadratic tree has an expectation.

The financial application stays terminal-wealth portfolio control. The Riccati model is the exact control and cannot support a speed claim against the Riccati ODE. A single nonquadratic application may be admitted later only after checking its specific estimator's integrability or using an explicitly justified different approximation/representation. A deterministic two-dimensional reference and policy-loss analysis would then be necessary. No XVA, market-making, neural-surrogate, wavelab, or general solver development is implied.

For the final FYP, the strongest defensible claim is about reliable numerical decisions: a theorem describing supported and unsupported estimators, a transparent sampling comparison, and quantified allocation error. It is useful evidence for quant research or trading interviews without being presented as a calibrated market model or an alpha strategy.
