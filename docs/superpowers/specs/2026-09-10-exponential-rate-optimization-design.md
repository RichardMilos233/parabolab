# Branching clock exponential rate optimization design

> **Archived design — status reviewed 16 September 2026.**
> This specification preceded the implemented scalar-rate theory and optimizer.
> Later work corrected the binary-estimator comparison and added full-tree
> certificates. The scoped [theory note](../../research/estimator-integrity/exponential-rate-optimization.md),
> [binary audit](../../research/results/binary-benchmark-audit.md), and
> [proof registry](../../research/proof-registry.md) supersede its original
> mathematical and formalization targets as statements of current evidence.
> Navigation: [archive index](../README.md), [current research](../../research/README.md),
> [documentation map](../../documentation-map.md).

Original approval date: 2026-09-10.

## Goal

Investigate the mathematical existence, convexity, asymptotic scaling, and numerical determination of the "sweet spot" branching clock rate $\lambda > 0$ in branching Monte Carlo estimators for nonlinear parabolic partial differential equations.

The research separates two fundamental settings:
1. **The local single-event horizon objective $J_{\exp}(\lambda)$**, which treats continuation variance as a fixed density and admits a strictly convex, unique global minimizer;
2. **The full recursive coding-tree second moment $V(t, x; \lambda)$**, whose topology expansion supports convexity under the stated disintegration assumptions. A unique interior minimum additionally requires properness and positive leaf and branching contributions; finite variance alone is not enough. The specified Harry Dym estimator instead has $V \equiv +\infty$ for all $\lambda > 0$ and possesses no finite variance-minimizing rate.

## Terminology and classification policy

Every theoretical statement is classified under the project's standard evidence ledger:
- **Proved theorem:** Complete mathematical proof with no unproved assumptions;
- **Lean-formalized theorem:** Mechanically verified in Lean 4 without `sorry`, `admit`, or non-standard axioms;
- **Analytic control / oracle:** Closed-form benchmark against a solvable Riccati ODE system;
- **Deterministic numerical result:** High-order Gauss--Legendre / Gauss--Hermite quadrature;
- **Empirical Monte Carlo result:** Finite-sample simulation with documented seeds, sample counts, and standard errors.

## Mathematical specification

### 1. The local single-event objective

For horizon $\Delta = T - t > 0$, leaf second-moment contribution $A_0 > 0$, and continuation second-moment density $A \in L^1(0, \Delta)$ satisfying $A(s) \ge 0$ a.e. and $B := \int_0^\Delta A(s) \, ds > 0$:

\[
J_{\exp}(\lambda) = A_0 e^{\lambda \Delta} + \frac{1}{\lambda} \int_0^\Delta A(s) e^{\lambda s} \, ds, \qquad \lambda \in (0, \infty).
\]

#### First and second derivatives

Let $I_k(\lambda) := \int_0^\Delta s^k A(s) e^{\lambda s} \, ds$ for $k \in \{0, 1, 2\}$. Then:

\[
J_{\exp}'(\lambda) = A_0 \Delta e^{\lambda \Delta} + \frac{1}{\lambda^2} \int_0^\Delta A(s) e^{\lambda s} (\lambda s - 1) \, ds,
\]
\[
J_{\exp}''(\lambda) = A_0 \Delta^2 e^{\lambda \Delta} + \frac{1}{\lambda^3} \int_0^\Delta A(s) e^{\lambda s} \left[(\lambda s - 1)^2 + 1\right] ds.
\]

#### Properties
1. **Strict convexity:** Since $A_0 > 0$, $\Delta > 0$, and the kernel $[(\lambda s - 1)^2 + 1] \ge 1 > 0$, $J_{\exp}''(\lambda) > 0$ for all $\lambda > 0$.
2. **Boundary asymptotics:**
   - As $\lambda \downarrow 0$: $J_{\exp}(\lambda) = \frac{B}{\lambda} + O(1) \to +\infty$, and $J_{\exp}'(\lambda) = -\frac{B}{\lambda^2} + O(1) \to -\infty$.
   - As $\lambda \to +\infty$: $J_{\exp}(\lambda) \ge A_0 e^{\lambda \Delta} \to +\infty$, and $J_{\exp}'(\lambda) \to +\infty$.
3. **Existence and uniqueness of optimum:** By the Intermediate Value Theorem and strict monotonicity of $J_{\exp}'$, there exists a unique $\lambda^* \in (0, \infty)$ satisfying $J_{\exp}'(\lambda^*) = 0$.

### 2. Full recursive coding-tree second moment

For an unrestricted or finite-depth coding tree, each completed tree topology $\theta$ with $B_\theta$ branch nodes and total particle-duration $L_\theta$ contributes a weight:

\[
h_{B, L}(\lambda) = \lambda^{-B} e^{\lambda L}.
\]

Its derivatives satisfy:
\[
h_{B, L}'(\lambda) = h_{B, L}(\lambda) \left( L - \frac{B}{\lambda} \right),
\]
\[
h_{B, L}''(\lambda) = h_{B, L}(\lambda) \left[ \left( L - \frac{B}{\lambda} \right)^2 + \frac{B}{\lambda^2} \right] > 0 \quad \text{for } L > 0.
\]

Consequently:
- Each finite-depth moment $V_{c, K}(t, x; \lambda)$ is strictly convex in $\lambda$ whenever a non-trivial branch topology is live;
- The unrestricted moment $V_c(t, x; \lambda) = \sup_K V_{c, K}(t, x; \lambda)$ is lower-semicontinuous, convex, and strictly convex on its domain of finiteness;
- Under properness, a positive root-survival coefficient, and a positive branching-topology contribution, $V_c(\lambda) \to \infty$ as $\lambda \downarrow 0$ and $\lambda \to \infty$, giving a unique global interior minimum. These are explicit hypotheses in the final theory note's Corollary 7.3.
- For non-integrable problems like the Harry Dym equation, $V_c(\lambda) \equiv +\infty$ for all $\lambda > 0$.

### 3. Short-horizon scaling ($T \downarrow 0$) vs. the JCP heuristic

Under positive leading coefficients and the uniform expansion and domination
hypotheses of the final theory note's Theorem 7.4, the short-time limit is:
\[
\lambda^*(T) \longrightarrow \sqrt{\frac{B_c(x)}{G_c(x)}} = \frac{|f(J\phi(x))|}{|\phi(x)|} = O(1).
\]
In contrast, the heuristic $\lambda_{\text{JCP}}(T) = -\frac{\ln(0.95)}{T} = O(1/T)$ keeps the root branching probability at $5\%$. This probability alone does not give a universal expected-tree-size bound. Under the displayed short-time hypotheses, the local leading **second-moment** ratio approaches $1/0.95$; this is not a multiplicative ratio of centered variances. See the final theory note for the additive variance interpretation.

### 4. Analytic Riccati control

For the semilinear equation $u_t + \frac{1}{2}u_{xx} + u^2 = 0$ with $\phi \equiv 1$, the exact second moment of the one-type `Id -> (Id, Id)` binary tree is obtained by solving $Y'(r) = \frac{e^{\lambda r}}{\lambda} Y(r)^2$ with $Y(0) = 1$:
\[
V(T; \lambda) = \frac{\lambda^2 e^{\lambda T}}{\lambda^2 + 1 - e^{\lambda T}} \quad \text{for } \lambda^2 > e^{\lambda T} - 1.
\]
The unique variance-minimizing rate satisfies:
\[
2(e^{\lambda T} - 1) = T \lambda (\lambda^2 + 1), \qquad \lambda^*(T) = 1 + \frac{T}{2} + \frac{7T^2}{24} + O(T^3).
\]
This is an analytic oracle for that one-type estimator. It is not the moment
of the derivative-coded mechanism merely because both represent the same
PDE. A finite-depth optimizer also targets its truncated moment, so matching
the full-tree oracle to machine precision is not a general acceptance
criterion. The later binary audit records both distinctions.

## Original Lean 4 targets and actual coverage

The following were **proposed targets**, not a list of completed theorems in
`formal/EstimatorIntegrity/ExponentialRate.lean`:
- Definition of kernel $w(\lambda, s) = \frac{e^{\lambda s}}{\lambda}$;
- Formulas for first and second derivatives of $w(\lambda, s)$ and $h_{B, L}(\lambda) = \lambda^{-B} e^{\lambda L}$;
- Direct algebraic proof of positivity: $[(\lambda s - 1)^2 + 1] > 0$ and $[(L - B/\lambda)^2 + B/\lambda^2] > 0$;
- Continuity and differentiability of $J_{\exp}(\lambda)$ on $(0, \infty)$ for continuous positive integrand $A(s)$;
- Proof of strict convexity via positive second derivative;
- Existence and uniqueness of the minimizer $\lambda^*$ on $(0, \infty)$.

As reviewed on 16 September 2026, that module proves positivity of the
displayed algebraic factors and the AM–GM optimization of $a\lambda+b/\lambda$,
including its equality condition. It does not formalize the integrated
objective's derivative interchange or its complete minimizer theorem. Later
certificate modules add separate finite algebraic and convex-enclosure
lemmas; consult the proof registry for exact names and omitted bridges.

Deliberately outside Lean scope:
- Full continuous-time measure disintegration of random tree topologies;
- Brownian path integrals and non-explosion boundary estimates.

## Numerical architecture

1. **`parabolab/rate_optimization.py`**:
   - Computes deterministic derivatives $(V, \partial_\lambda V, \partial^2_\lambda V)$ via Gauss--Legendre and Gauss--Hermite quadrature;
   - Implements safeguarded bisection and Newton-Raphson root-finding on $\partial_\lambda V(\lambda) = 0$;
   - Provides analytical Riccati oracle for $u^2$.
2. **`tests/test_rate_optimization.py`**:
   - Validates numerical derivatives against centered finite differences;
   - Tests bisection against the Riccati oracle ($< 10^{-8}$ relative error);
   - Validates that finite-depth quadrature matches Monte Carlo empirical second moments;
   - Tests detection of non-convergent/divergent models.
3. **`examples/exponential_rate_sweet_spot.py`**:
   - Generates U-curves across $\lambda \in [0.1, 5.0]$ for the binary control and Allen--Cahn ($d=1$);
   - Evaluates short-horizon scaling of $\lambda^*(T)$ vs. $\lambda_{\text{JCP}}(T)$ and package default $\lambda = 1.0$;
   - Runs Dym rate sweeps demonstrating failure to stabilize with increasing $N$.

## Original ownership and execution protocol (historical)

- **GPT 5.6 Sol Max (Subagents):**
  - Mathematical proof documentation (`docs/research/estimator-integrity/exponential-rate-optimization.md`);
  - Lean 4 formalization (`formal/EstimatorIntegrity/ExponentialRate.lean`).
- **Gemini / Execution Agent:**
  - Python solver and optimizer (`parabolab/rate_optimization.py`);
  - Test suite (`tests/test_rate_optimization.py`);
  - Experiment script and figures (`examples/exponential_rate_sweet_spot.py`);
  - Documentation integration and audit updates.
