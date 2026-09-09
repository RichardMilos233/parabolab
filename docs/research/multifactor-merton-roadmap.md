# Multifactor Merton Research and Literature Roadmap

**Status:** approved research roadmap for the `parabolab` multidimensional benchmark programme.
**Last-reviewed commit:** `ce2949330fcff1a3faf56c8a0ff36628586b242d`
**Companion documents:**
- Primary proofs: `docs/research/multifactor-merton-proofs.md`
- Authoritative claim registry: `docs/research/proof-registry.md`
- Design specification: `docs/superpowers/specs/2026-09-09-multifactor-merton-proof-record-design.md`

---

## 1. Recovered Research Discussion and Context

The project previously implemented a single-factor prototype: Merton portfolio choice under an independent Vasicek short rate (`parabolab/library.py::merton_vasicek` and `merton_vasicek_reduced`). While effective as a code test, research review identified three critical mathematical limitations:

1. **Dimensional collapse under CRRA utility:** The unreduced model has two state variables $(x, r)$, but power-utility scaling $V(t, x, r) = \frac{x^{1-\gamma}}{1-\gamma} F(t, r)$ removes wealth entirely. The factor PDE governing $F(t, r)$ has only **one spatial dimension** ($m = 1$). It is not genuinely multidimensional.
2. **Artificial wealth diffusion and domain violation:** Unreduced coding trees that assign a non-degenerate Brownian motion to wealth $X_t$ inevitably reach negative values ($X_T \le 0$) with strictly positive probability at every horizon $T > 0$ (`PR-MM-5`). For fractional CRRA risk aversion, $x^{1-\gamma}$ is not real-valued on negative numbers. Replacing $x^{1-\gamma}$ with $|x|^{1-\gamma}$ alters the PDE and changes the economic problem.
3. **Decoupling controls from state dimension:** Having $n$ risky assets introduces an $n$-dimensional control vector $\pi \in \mathbb R^n$, but without stochastic opportunity factors, wealth remains the sole state and the HJB collapses to an ODE (`PR-MM-2.1`). High-dimensional portfolio choice requires high-dimensional **opportunity states** $Y \in \mathbb R^m$.

This roadmap establishes the literature-backed mathematical path to an irreducible, genuinely multidimensional Merton benchmark with closed-form ground truth.

---

## 2. High-Dimensional Controls vs High-Dimensional PDE States

In financial engineering and stochastic optimal control, there is a sharp mathematical distinction between high-dimensional controls and high-dimensional PDE states:

- **Vector Controls with Scalar PDE States:** Consider $n$ risky assets with constant return vector $\mu \in \mathbb R^n$, constant risk-free rate $r$, and constant covariance matrix $\Sigma \in \mathbb R^{n \times n}$. The portfolio control $\pi \in \mathbb R^n$ is an $n$-dimensional vector. However, after substituting the optimal policy:
  $$\pi^* = \frac{1}{\gamma} \Sigma^{-1}(\mu - r \mathbf 1),$$
  the portfolio terms enter the HJB equation exclusively through the scalar squared Sharpe ratio:
  $$\theta^2 = (\mu - r \mathbf 1)^\top \Sigma^{-1} (\mu - r \mathbf 1).$$
  Wealth $x$ is the sole spatial variable. After CRRA scaling $V(t, x) = \frac{x^{1-\gamma}}{1-\gamma} F(t)$, $F(t)$ satisfies an ordinary differential equation in time $t$. **No multidimensional PDE exists.**
- **Genuinely Multidimensional PDE States:** A multidimensional PDE arises only when market investment opportunities vary stochastically over time, driven by $m$ irreducible state variables $Y_t \in \mathbb R^m$. Examples include:
  - Stochastic interest rates / term-structure factors;
  - Time-varying expected returns / risk premia predictors;
  - Stochastic volatility factors;
  - Macroeconomic growth / inflation states;
  - Investor belief states in partial-information filtering.

Under CRRA utility, wealth $x$ is eliminated, leaving an irreducible $m$-dimensional PDE for the factor value $F(t, Y)$. For the coding tree, $m$ is the actual dimension of the underlying Markov process and the jet multi-indices.

---

## 3. Primary-Source Literature Map

The mathematical framework synthesizes several classical and modern literatures. Each area is anchored by primary sources:

### A. Continuous-Time Portfolio Choice and CRRA Reduction
- **Merton, R. C. (1969).** *Lifetime Portfolio Selection under Uncertainty: The Continuous-Time Case.* Review of Economics and Statistics, 51(3), 247–257. [DOI 10.2307/1926560](https://doi.org/10.2307/1926560).
- **Merton, R. C. (1971).** *Optimum Consumption and Portfolio Rules in a Continuous-Time Model.* Journal of Economic Theory, 3(4), 373–413. [DOI 10.1016/0022-0531(71)90038-X](https://doi.org/10.1016/0022-0531(71)90038-X).
  - *Contribution:* Formulated the dynamic programming HJB equation, derived the concavity-preserving Hamiltonian maximization, and introduced power-utility wealth scaling.

### B. Predictable Returns and Intertemporal Hedging
- **Kim, T. S., and Omberg, E. (1996).** *Dynamic Nonmyopic Portfolio Behavior.* Review of Financial Studies, 9(1), 141–161. [DOI 10.1093/rfs/9.1.141](https://doi.org/10.1093/rfs/9.1.141).
  - *Contribution:* Analytical solution for an Ornstein-Uhlenbeck return-predicting factor using Riccati ODE systems; identified the intertemporal hedging demand.

### C. Quadratic and Affine Multifactor Models
- **Liu, J. (2007).** *Portfolio Selection in Stochastic Environments.* Review of Financial Studies, 20(1), 1–39. [DOI 10.1093/rfs/hhl001](https://doi.org/10.1093/rfs/hhl001).
  - *Contribution:* Unified treatment of multidimensional affine and quadratic term structure and excess-return factors; derived general matrix Riccati systems for exponential-affine/quadratic value functions.

### D. Stochastic Interest Rates and Vasicek Term Structures
- **Vasicek, O. (1977).** *An Equilibrium Characterization of the Term Structure.* Journal of Financial Economics, 5(2), 177–188. [DOI 10.1016/0304-405X(77)90016-2](https://doi.org/10.1016/0304-405X(77)90016-2).
- **Chang, H.-S., and Chang, S.-L. (2014).** *Optimal Consumption and Investment with Vasicek Interest Rate and Inflation.* Journal of Systems Science and Complexity, 27(6), 1165–1182. [DOI 10.1007/s11424-014-1165-6](https://doi.org/10.1007/s11424-014-1165-6).
  - *Contribution:* Solutions for portfolio allocation with Vasicek interest rates and correlation between asset shocks and rate shocks.

### E. Partial Information and Stochastic Filtering
- **Lakner, P. (1998).** *Approximation of Optimal Portfolio Policies with Partial Information.* Stochastic Processes and their Applications, 76(2), 283–297. [DOI 10.1016/S0304-4149(98)00032-5](https://doi.org/10.1016/S0304-4149(98)00032-5).
  - *Contribution:* Gaussian Kalman-Bucy filter where the estimated drift becomes an evolving opportunity state.

### F. Coding Trees and Deep Branching Solvers
- **Nguwi, J. Y., Penent, G., and Privault, N. (2023).** *A fully nonlinear Feynman–Kac formula with derivatives of arbitrary orders.* Journal of Evolution Equations, 23, 22. [DOI 10.1007/s00028-023-00873-3](https://doi.org/10.1007/s00028-023-00873-3).
  - *Contribution:* Coding trees for arbitrary-order derivative PDEs in 1D; Faà di Bruno mechanism expansion.
- **Nguwi, J. Y., Penent, G., and Privault, N. (2024).** *A deep branching solver for fully nonlinear partial differential equations.* Journal of Computational Physics, 499, 112712. [DOI 10.1016/j.jcp.2023.112712](https://doi.org/10.1016/j.jcp.2023.112712).
  - *Contribution:* Multidimensional coding trees with isotropic diffusion $\sigma^2 I$; deep neural network training on tree targets.
- **Henry-Labordère, P., Oudjane, N., Tan, X., Touzi, N., and Warin, X. (2019).** *Branching diffusion representation of semilinear PDEs and Monte Carlo approximation.* Ann. Inst. H. Poincaré Probab. Statist., 55(1), 184–210. [DOI 10.1214/17-AIHP880](https://doi.org/10.1214/17-AIHP880).
  - *Contribution:* State-dependent branching diffusions with gradient marks for semilinear problems.

---

## 4. General Factor-Model HJB and CRRA Reduction

Let $Y_s \in \mathbb R^m$ be an observable vector of opportunity factors:
$$dY_s = b(Y_s)\,ds + \beta\,dW_s^Y, \qquad A := \beta\beta^\top \succeq 0.$$
There are $n$ risky assets with excess returns $\lambda(Y_s) \in \mathbb R^n$ and covariance $\Sigma \succ 0$. The cross-covariance between asset return shocks and factor shocks is $C \in \mathbb R^{n \times m}$:
$$d\langle W^S, W^Y \rangle_s = \sigma^{-1} C\,ds, \qquad \sigma\sigma^\top = \Sigma.$$
Wealth $X_s$ follows:
$$dX_s = [r(Y_s) X_s + X_s \pi_s^\top \lambda(Y_s) - c_s]\,ds + X_s \pi_s^\top \sigma\,dW_s^S.$$
For CRRA risk aversion $0 < \gamma < 1$, $a = 1 - \gamma$, and utility $U(c) = c^a / a$ with discount rate $\delta$:

### Value Function and Controls
The full HJB equation for $V(t, x, y)$ (`PR-MM-1`) reduces via $V(t, x, y) = \frac{x^a}{a} F(t, y)$ (`PR-MM-2`) to:
$$\boxed{
F_t + b(y)\cdot\nabla F + \frac12 A:D^2 F + (ar(y) - \delta) F + \frac{a}{2\gamma F} (\lambda(y) F + C\nabla F)^\top \Sigma^{-1} (\lambda(y) F + C\nabla F) + \gamma F^{-a/\gamma} = 0
}$$
with terminal condition $F(T, y) = 1$. The optimal feedback controls are:
$$\pi^*(t, y) = \frac{1}{\gamma} \Sigma^{-1} \left(\lambda(y) + C\nabla \log F(t, y)\right), \qquad \frac{c^*(t, x, y)}{x} = F(t, y)^{-1/\gamma}.$$
The term $C\nabla \log F$ is the **intertemporal hedging demand** arising from correlation between asset returns and opportunity shifts. When $C = 0$, the portfolio reduces to the myopic allocation $\frac{1}{\gamma} \Sigma^{-1} \lambda(y)$.

---

## 5. Recommended Two-Factor Benchmark

To ensure the benchmark is genuinely multidimensional, we specify a two-factor Ornstein-Uhlenbeck system ($m = 2$) with economically distinct roles:

1. $Y_{1,t} = r_t$: a stochastic short-rate factor (Vasicek type).
2. $Y_{2,t} = \mu_t$: a predictable expected-excess-return factor (Kim-Omberg type).

### Model Dynamics
Let $Y_t = (r_t, \mu_t)^\top \in \mathbb R^2$ satisfy:
$$dY_t = K(\bar y - Y_t)\,dt + B\,dW_t^Y,$$
$$K = \begin{pmatrix} \kappa_r & 0 \\ 0 & \kappa_\mu \end{pmatrix}, \qquad \bar y = \begin{pmatrix} \bar r \\ \bar \mu \end{pmatrix}, \qquad B = \begin{pmatrix} \sigma_r & 0 \\ \rho_{r\mu}\sigma_\mu & \sqrt{1-\rho_{r\mu}^2}\sigma_\mu \end{pmatrix}.$$
The factor covariance is $A = BB^\top = \begin{pmatrix} \sigma_r^2 & \rho_{r\mu}\sigma_r\sigma_\mu \\ \rho_{r\mu}\sigma_r\sigma_\mu & \sigma_\mu^2 \end{pmatrix} \succ 0$.

There is one representative stock index ($n = 1$) with variance $\sigma_S^2 > 0$:
- Short rate: $r(y) = y_1 \implies r_0 = 0, r_1 = (1, 0)^\top$.
- Excess return: $\lambda(y) = y_2 \implies \ell = 0, L = (0, 1)$.
- Cross-correlation: $C = (\rho_{Sr}\sigma_S, \rho_{S\mu}\sigma_S) \in \mathbb R^{1 \times 2}$.

### Genuine 2D Irreducibility Verification
We verify `PR-MM-3` (short-time obstruction to one-index reduction):
- $r_1 = (1, 0)^\top$ and $\ell_1 = L^\top = (0, 1)^\top$.
- Clearly, $r_1 \notin \operatorname{span}\{\ell_1\}$ because $(1, 0)^\top$ is orthogonal to $(0, 1)^\top$.
- Furthermore, $L^\top \Sigma^{-1} L = \frac{1}{\sigma_S^2} \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix}$ has non-collinear interaction with $r_1$.

By Theorem MM-3, the factor value function $F(t, y_1, y_2)$ **cannot collapse** to a function of a single linear index $v^\top y$ on any short-time interval. The benchmark is irreducible.

---

## 6. Exact Matrix-Riccati Validation System

For the no-consumption problem ($c \equiv 0$, terminal wealth utility), Theorem MM-4 (`PR-MM-4`) provides an exact, semi-analytic ground truth:
$$F(T-\tau, y) = \exp\left(\alpha(\tau) + \beta(\tau)^\top y + \frac12 y^\top P(\tau) y\right),$$
where $P(\tau) \in \mathbb R^{2 \times 2}$ is symmetric, $\beta(\tau) \in \mathbb R^2$, and $\alpha(\tau) \in \mathbb R$.

### The Coupled Matrix Riccati ODE System
Let $R = \Sigma^{-1} = 1/\sigma_S^2$, $k = K\bar y$, $h = C\beta$, and $H = L + CP$. Backward in time ($\tau = T - t$):
$$\boxed{
\begin{aligned}
P' &= -(K^\top P + PK) + PAP + \frac{a}{\gamma} H^\top R H, && P(0) = 0_{2\times 2},\\[1mm]
\beta' &= Pk - K^\top \beta + PA\beta + a r_1 + \frac{a}{\gamma} H^\top R h, && \beta(0) = 0_{2\times 1},\\[1mm]
\alpha' &= k^\top \beta + \frac12 \operatorname{tr}(AP) + \frac12 \beta^\top A \beta - \delta + \frac{a}{2\gamma} h^\top R h, && \alpha(0) = 0.
\end{aligned}
}$$

### Ground-Truth Delivery
Integrating this 6-dimensional ODE system (3 independent elements in $P$, 2 in $\beta$, 1 in $\alpha$) using standard high-precision solvers (e.g. `scipy.integrate.solve_ivp` with Runge-Kutta 4/5) provides:
1. Exact value function $F(t, y)$;
2. Exact spatial gradient $\nabla F(t, y) = F(t, y)(\beta(t) + P(t)y)$;
3. Exact Hessian $D^2 F(t, y) = F(t, y)[P(t) + (\beta + Py)(\beta + Py)^\top]$;
4. Exact optimal portfolio policy $\pi^*(t, y) = \frac{1}{\gamma\sigma_S^2}(y_2 + C(\beta(t) + P(t)y))$.

This provides deterministic ground truth with error $< 10^{-10}$, completely eliminating Monte Carlo uncertainty from validation.

---

## 7. Coding-Tree Proof Obligations

To represent the factor PDE by a continuous-time coding tree, the full-covariance mechanism of Theorem MM-6 (`PR-MM-6`) must be implemented and Theorem MM-7 (`PR-MM-7`) discharged:

### Mechanism Equations
The PDE is written in Duhamel form:
$$\partial_t F + \frac12 A : D^2 F + f(y, F, \nabla F) = 0,$$
where $f(y, F, \nabla F) = (k - Ky)\cdot\nabla F + (a y_1 - \delta) F + \frac{a}{2\gamma\sigma_S^2 F} (y_2 F + C\nabla F)^2$.

The jet multi-indices are:
- $z_0 \leftrightarrow F$ (order 0);
- $z_1 \leftrightarrow \partial_{y_1} F$ (order $e_1$);
- $z_2 \leftrightarrow \partial_{y_2} F$ (order $e_2$).

### Open Analytical Obligations
To promote Theorem MM-7 from a **conditional theorem** to a **proved representation**, research must discharge:
1. **$L^1$ Integrability:** Prove that the tree functional $H_{t, y, \mathrm{Id}}$ has finite absolute first moment for the non-polynomial rational term $(y_2 F + C\nabla F)^2 / F$.
2. **Positivity / Support Separation:** Ensure that child trajectories and terminal evaluations of $F$ remain strictly positive ($F > 0$) almost surely, preventing division by zero.
3. **Mild-System Uniqueness:** Establish that the code-indexed Duhamel system has a unique solution agreeing with the classical Riccati solution in an appropriate Sobolev or weighted continuous space.
4. **Non-Explosion:** Prove that the branching process with $m = 2$ and quadratic source terms has almost-sure finite node count on the horizon $[0, T]$.

---

## 8. Estimator Integrity and Proposal Requirements

Before generating Monte Carlo numbers or reporting standard errors:

1. **Finite Second-Moment Certification:** Standard Gaussian confidence intervals $\bar H \pm 1.96 \frac{s}{\sqrt N}$ require $H \in L^2$. Without certifying $V_{\mathrm{Id}}^{(2)}(t, y) < \infty$ via `PR-MOM-3`, empirical sample variances can systematically underestimate error (as in JCP Table 5 and Dym).
2. **Pilot-Frozen Adaptive Proposals:** Uniform proposals on the 2D mechanism distribute weight inefficiently to rare derivative codes. Optimal allocation requires:
   - Sampling an independent pilot batch ($\mathcal P$-measurable);
   - Freezing $q^*(Z) \propto \sqrt{\widehat A_Z}$ with a positive floor $\varepsilon \ge 0.05$ (`PR-PROP-1`, `PR-PROP-4`);
   - Evaluating on fresh seeds without within-sample re-adaptation (`PR-PROP-3`).
3. **Work-Normalized Metric:** Always report variance multiplied by mean node count $\mathcal W(q) = \widehat{\operatorname{Var}}(H) \times \widehat{\mathbb E}[N_{\text{nodes}}]$, ensuring that variance reduction is not achieved by exploding tree depth.

---

## 8.1 Comparison and Justification of Research Routes

To select the mathematically sound and numerically tractable formulation for the benchmark, we compare four candidate modeling routes against six criteria:

| Evaluation Criterion | Route 1: Unreduced Tree with Wealth Diffusion ($A_{xx} > 0$) | Route 2: Unreduced Singular Tree ($A_{xx} = 0$) | Route 3: Separately Derived Log-Wealth Tree | Route 4: CRRA-Reduced Factor-Only Tree (Selected) |
|---|---|---|---|---|
| **Domain Integrity** | **Defective:** $\mathbb P(X_T^{\text{ref}} \le 0) > 0$; fractional power $x^{1-\gamma}$ undefined (`PR-MM-5`). | **Sound:** Wealth coordinate has zero diffusion; stays $x > 0$ deterministically. | **Sound:** State is $\log x \in \mathbb R$; no positivity barrier. | **Sound:** Wealth completely eliminated; factors $(r, \mu) \in \mathbb R^2$ unbounded. |
| **PDE Spatial Dimension** | $m + 1 = 3$ variables $(x, r, \mu)$. | $m + 1 = 3$ variables $(x, r, \mu)$ with degenerate diffusion. | $m + 1 = 3$ variables $(\log x, r, \mu)$. | **Irreducible $m = 2$** variables $(r, \mu)$. |
| **Exact Ground Truth** | Semi-exact (requires scaling reconstruction). | Semi-exact. | Semi-exact. | **Exact Matrix Riccati:** Closed-form ODE for $F, \nabla F, D^2 F, \pi^*$ (`PR-MM-4`). |
| **Coding Mechanism Complexity** | High: Cross-derivatives between wealth and factor jets. | High: Degenerate covariance row requires singular Markov transition kernel. | Extreme: Transformation generates complex chain-rule jet interactions. | **Minimal / Canonical:** Follows direct full-covariance mechanism (`PR-MM-6`). |
| **Computational Efficiency** | Wasteful: Samples wealth dimension that is analytically redundant. | Moderate: Non-diffusive dimension still tracked in branch nodes. | Low: Complex jet trees increase branching factor. | **High:** Tree evaluates only irreducible opportunity factors. |
| **Risk of Overclaiming** | High: Mistaking smoke-test survival for mathematical validity. | Moderate. | Moderate. | **Zero:** Exact mathematical reduction cleanly bounded by classical theory. |

### Justification of Route 4 (Selected Route)
1. **Mathematical Cleanliness:** Route 4 completely bypasses the negative-wealth obstruction proved in Theorem MM-5 (`PR-MM-5`). It requires no artificial domain boundaries, stopping times, or ad hoc utility modifications like $|x|^a$.
2. **True Dimensional Irreducibility:** Route 4 works on the genuinely multidimensional factor space $\mathbb R^2$. The unreduced routes 1–3 create an illusion of higher dimension by retaining wealth, but wealth homogeneity makes that extra coordinate mathematically redundant.
3. **Deterministic Validation:** Route 4 directly connects to the exact matrix-Riccati benchmark (`PR-MM-4`), providing machine-precision ground truth ($< 10^{-10}$) for both the factor value $F$ and the optimal feedback policy $\pi^*$.
4. **Implementation Track:** The full-covariance state-dependent mechanism (`PR-MM-6`) operates naturally on $\mathbb R^2$, focusing computational resources on the genuine source of financial complexity: the correlation between asset shocks and factor shocks.

---

## 9. Dependency-Ordered Implementation and Research Roadmap

```
                    ┌───────────────────────────────────────────────┐
                    │ Phase 0: Master Proof Registry & Audit        │
                    │ (docs/research/proof-registry.md)             │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Phase 1: 2-Factor Matrix-Riccati ODE Solver   │
                    │ Exact ground truth for values, gradients,     │
                    │ Hessians, and policies (Theorem MM-4)         │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Phase 2: Full-Covariance Mechanism Generator  │
                    │ Arbitrary-covariance A:D^2u & direct spatial  │
                    │ multi-indices (Theorem MM-6)                  │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Phase 3: Two-Factor Tree Sampler & Validation │
                    │ Pointwise value & gradient cross-check        │
                    │ against Riccati ground truth (N = 1e5..1e6)   │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Phase 4: Moment Iteration & Proposal Tuning   │
                    │ Certify L^2 window; pilot-frozen square-root  │
                    │ tuple proposal (Theorems 2.3 & 6.1)           │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Phase 5: Deep Branching 2D Surface Solver     │
                    │ Train ResNet on 2D factor box [r_lo, r_hi]    │
                    │ x [mu_lo, mu_hi]; test L1/L2 vs Riccati       │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────┐
                    │ Phase 6: Factor-Dimension Scaling (m=1..20)   │
                    │ Multi-factor yield curve & predictor models;  │
                    │ Tree size, conditioning, runtime benchmark    │
                    └───────────────────────────────────────────────┘
```

### Detailed Phase Specifications

#### Phase 1: Two-Factor Matrix-Riccati Ground Truth (Milestone 1)
- **File:** `parabolab/riccati.py`
- **Deliverables:**
  - `solve_merton_riccati(K, y_bar, A, C, sigma_S, gamma, delta, T)` returning callable interpolants for $(P, \beta, \alpha)$.
  - Analytical value $F(t, y)$, gradient $\nabla F(t, y)$, and optimal policy $\pi^*(t, y)$.
- **Verification:**
  - Unit tests verifying ODE residual $\|P' - \text{RHS}\|_\infty < 10^{-12}$.
  - Degenerate check: when $m = 1$ and $y_2 \equiv \text{const}$, matches `merton_vasicek_reduced`.

#### Phase 2: Full-Covariance State-Dependent Mechanism (Milestone 2)
- **File:** `parabolab/mechanism.py`
- **Deliverables:**
  - `FullyNonlinearMechanismND` generalized to accept full symmetric matrix $A \succeq 0$.
  - Implement tuple blocks (7.6)–(7.9) from `PR-MM-6`.
  - Exact zero pruning using polynomial degree and support bounds.
- **Verification:**
  - Symbolic test verifying match against SymPy Duhamel source expansion.
  - Golden test matching isotropic tables when $A = \sigma^2 I$.

#### Phase 3: Two-Factor Tree Sampler & Pointwise Validation (Milestone 3)
- **File:** `examples/merton_two_factor_tree.py`
- **Deliverables:**
  - Pointwise Monte Carlo estimation of $F(0, y)$ and $\partial_{y_k} F(0, y)$ at grid points $(y_1, y_2) \in [-0.05, 0.15] \times [-0.2, 0.4]$.
  - Cross-check against Riccati ground truth across sample budgets $N = 10^4, 10^5, 10^6$.
- **Verification:**
  - Z-score test $|(\bar H - F_{\text{exact}})| / (\text{stderr}) < 2.5$.
  - No domain errors ($F > 0$ holds along all paths).

#### Phase 4: Moment Certification and Adaptive Proposals (Milestone 4)
- **File:** `examples/merton_two_factor_proposals.py`
- **Deliverables:**
  - Moment iteration testing for $L^1$ and $L^2$ boundaries over $T \in [0.01, 0.5]$.
  - Independent pilot run ($N_{\text{pilot}} = 10^4$), frozen square-root proposal with 5% floor.
  - Evaluation on 5 fresh seeds ($N_{\text{eval}} = 10^5$).
- **Verification:**
  - Exact unbiasedness preserved ($|\text{mean} - \text{exact}| < 2 \times \text{stderr}$).
  - Reduction in work-normalized variance $\mathcal W(q)$.

#### Phase 5: Deep Branching 2D Surface Solver (Milestone 5)
- **File:** `examples/merton_two_factor_deep.py`
- **Deliverables:**
  - Generate training dataset of $N = 1000$ points uniformly distributed on a rectangular domain $[r_{\min}, r_{\max}] \times [\mu_{\min}, \mu_{\max}]$ (Remark 3.1 vi).
  - Train 5-layer residual network (20 hidden units, tanh, batchnorm) under full-batch Adam.
  - Evaluate $L^1$ and $L^2$ relative errors on a $101 \times 101$ tensor evaluation grid against Riccati ground truth.
- **Verification:**
  - Relative $L^1$ error $< 1.5 \times 10^{-2}$.
  - Consistency plot comparing network predictions against unbiased tree targets.

#### Phase 6: Factor-Dimension Scaling Study (Milestone 6)
- **File:** `examples/merton_dimension_scaling.py`
- **Deliverables:**
  - Dimension sweep $m \in \{1, 2, 5, 10, 20\}$ with correlated factor blocks.
  - Measure mechanism table size $|\mathcal M(c)|$, tree sample generation time, and memory scaling.
- **Verification:**
  - Empirical verification of Faà di Bruno pruning efficiency for sparse financial interaction graphs.

---

## 10. Safe and Unsafe Novelty Language

To preserve academic integrity and avoid overclaiming, all documentation, comments, and papers must adhere to the following language standards:

| Topic | Unsafe Language (Forbidden) | Safe Language (Approved) |
|---|---|---|
| **Multifactor Merton** | "We introduce the first multidimensional Merton model." | "We formulate a CRRA-reduced two-factor Merton benchmark with matrix-Riccati ground truth, providing an exact multidimensional validation for coding trees." |
| **CRRA Reduction** | "Our novel state reduction removes wealth." | "We apply the classical CRRA scaling property (Merton 1971) to eliminate wealth and obtain an irreducible factor PDE." |
| **Full-Covariance Mechanism** | "We discovered the universal Feynman-Kac formula for general PDEs." | "We extend the isotropic coding-tree mechanism of Nguwi et al. (2023, 2024) to constant, possibly singular full-covariance matrices." |
| **Lean Formalization** | "The entire coding-tree theory is verified in Lean 4." | "We formalize the core finite-algebraic moment step, Picard monotonicity, and proposal inequalities in Lean 4; probability spaces, continuous-time martingales, and infinite-tree limits remain paper obligations." |
| **Adaptive Proposals** | "We invented optimal importance sampling for branching trees." | "We specialize the classical square-root allocation to branching tuple tables and prove finite-depth oracle bounds with pilot-frozen unbiasedness." |
| **Dym Integrability** | "The Dym equation cannot be solved by Monte Carlo." | "We prove that the specific JEQ Fig 6 full-support coding-tree estimator has infinite absolute first moment, explaining why small-sample Monte Carlo exhibits severe instability." |
| **Literature Priority** | "This is the first time this result has ever appeared." | "A scoped search of the branching and financial control literature did not locate a prior work combining these specific features." |
