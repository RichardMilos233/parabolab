# Stochastic-rate Merton extension

Status: approved in chat on 2026-09-07.

## Goal

Extend the coding-tree Monte Carlo and deep-branching pipeline from the
constant-rate Merton benchmark to a Merton consumption/investment problem with
a Vasicek short rate.

The work is deliberately staged:

1. derive and solve the CRRA-homogeneity-reduced problem \(F(t,y)\);
2. solve the unreduced value function \(V(t,x,y)\);
3. use the reduced solution as an independent reference for the full solver;
4. only then add correlation between stock and rate shocks.

All implementation work lives on `feature/stochastic-rate-merton`. Existing
uncommitted work in `demo/merton.py` is user-owned and must not be edited or
included in commits.

## Non-goals

- CIR or other positive short-rate models in the first implementation;
- calibration to market data or construction of a full yield curve;
- transaction costs, portfolio constraints, or partial information;
- changing the existing constant-rate Merton benchmark;
- claiming that the existing JCP2024 theorem already covers explicit
  state-dependent nonlinearities without a new derivation;
- learning only a one-dimensional slice and calling it a two-dimensional
  solution.

## Financial model

Let the short rate follow a Vasicek process

\[
dR_s=\kappa(\theta-R_s)\,ds+\eta\,dW_s^r,
\qquad \kappa,\eta>0.
\]

The bank account and risky asset satisfy

\[
\frac{dB_s}{B_s}=R_s\,ds,
\qquad
\frac{dS_s}{S_s}=(R_s+\lambda)\,ds+\sigma\,dW_s^S.
\]

Thus \(\lambda\) is a constant excess return. The investor chooses the risky
wealth fraction \(\pi_s\) and consumption rate \(c_s\):

\[
dX_s=
\left(R_sX_s+\pi_sX_s\lambda-c_s\right)ds
+\pi_sX_s\sigma\,dW_s^S.
\]

The first stage assumes

\[
d\langle W^S,W^r\rangle_s=0.
\]

For CRRA utility \(U(q)=q^{1-\gamma}/(1-\gamma)\), \(0<\gamma<1\), the objective
is

\[
V(t,x,r)=
\sup_{\pi,c}\mathbb E_{t,x,r}\left[
\int_t^T e^{-\rho(s-t)}U(c_s)\,ds
+e^{-\rho(T-t)}U(X_T)
\right].
\]

## Normalized rate coordinate

Use

\[
Y_s=\frac{R_s-\theta}{\eta},
\qquad R_s=\theta+\eta Y_s.
\]

Then

\[
dY_s=-\kappa Y_s\,ds+dW_s^r.
\]

This normalization is important for the coding-tree implementation: the rate
factor has the standard \(1/2\)-Laplacian required by the existing Brownian
sampler. It avoids a large artificial cancellation when \(\eta^2\ll1\).

## Full HJB

Write \(r(y)=\theta+\eta y\). Optimizing the independent-shock HJB over
\(\pi\) and \(c\) gives

\[
\begin{aligned}
0={}&V_t-\kappa yV_y+\frac12V_{yy}+r(y)xV_x\\
&-\frac{\lambda^2}{2\sigma^2}\frac{V_x^2}{V_{xx}}
+\frac{\gamma}{1-\gamma}V_x^{1-1/\gamma}
-\rho V,
\end{aligned}
\]

with

\[
V(T,x,y)=\frac{x^{1-\gamma}}{1-\gamma}.
\]

The feedback controls are

\[
\pi^*(t,x,y)
=-\frac{\lambda V_x}{x\sigma^2V_{xx}},
\qquad
c^*(t,x,y)=V_x^{-1/\gamma}.
\]

To use a standard two-dimensional Brownian reference operator, write the PDE
as

\[
V_t+\frac12(V_{xx}+V_{yy})+f(x,y,J V)=0,
\]

where \(f\) contains a cancelling term \(-V_{xx}/2\), as in the existing
constant-rate Merton benchmark.

## Homogeneity reduction

CRRA homogeneity implies

\[
V(t,x,y)=\frac{x^{1-\gamma}}{1-\gamma}F(t,y).
\]

Substitution into the full HJB gives

\[
\begin{aligned}
0={}&F_t-\kappa yF_y+\frac12F_{yy}\\
&+\left[
(1-\gamma)(\theta+\eta y)
+\frac{(1-\gamma)\lambda^2}{2\gamma\sigma^2}
-\rho
\right]F
+\gamma F^{-(1-\gamma)/\gamma},
\end{aligned}
\]

with

\[
F(T,y)=1.
\]

This is a one-dimensional semilinear, state-dependent PDE. It is the first
implementation target and later supplies the reference

\[
V_{\mathrm{ref}}(t,x,y)
=\frac{x^{1-\gamma}}{1-\gamma}F(t,y)
\]

for every point in the full two-dimensional domain.

## Why the current algorithm cannot accept this PDE directly

`FullyNonlinearPDEnD` currently represents

\[
u_t+\frac{\sigma_0^2}{2}\Delta u
+f(\partial^{\alpha_1}u,\ldots,\partial^{\alpha_m}u)=0.
\]

Its `f_expr` has jet symbols only. `FNu` records derivatives of \(f\) with
respect to those jet arguments, and `FullyNonlinearMechanismND` derives its
tables under the assumption that \(f\) has no explicit spatial dependence.

Both stochastic-rate equations instead contain coefficients such as
\(-\kappa y\), \(\theta+\eta y\), and \(x(\theta+\eta y)\). Simply allowing an
`x_symbol` in `f_expr` without changing the mechanism would omit explicit
spatial chain-rule terms and produce a biased estimator.

The Brownian tree sampler itself can remain the reference sampler after the
rate normalization. The principal mathematical change is the coding mechanism
for

\[
f(x,\partial^{\alpha_1}u,\ldots,\partial^{\alpha_m}u).
\]

## Architecture

### State-dependent PDE specification

Add a separate state-dependent PDE type rather than changing the behavior of
the existing classes. Its nonlinearity is a symbolic expression in both:

- spatial symbols \(x_1,\ldots,x_d\);
- jet symbols \(z_1,\ldots,z_m\).

It caches mixed derivatives

\[
\partial_x^\beta\partial_z^\nu f
\]

and lambdifies them as functions of the current state and solution jet.

### State-dependent codes and mechanism

Introduce a code carrying both multi-indices:

\[
(a\,\partial_x^\beta\partial_z^\nu f)^*.
\]

The mechanism must be derived from the chain rule for
\(f(x,J u(x))\), including:

- derivatives acting explicitly on \(x\);
- derivatives acting on jet components;
- mixed \(x\)-jet derivatives;
- the quadratic terms generated by the reference Laplacian.

The implementation must be checked symbolically against direct SymPy
differentiation at low orders before it is used in Monte Carlo tests.
State-independent expressions must reduce to the current mechanism and,
where practical, produce identical tables.

### Tree sampler

Keep `tree.py`'s existing random draw order and behavior unchanged. The new
mechanism continues to satisfy the existing `tuples`, `terminal`, and
`is_identically_zero` protocol. Terminal evaluation additionally passes the
current spatial state into mixed derivatives of \(f\).

If this cannot be achieved without changing existing random draws, add a
parallel state-dependent sampler instead of modifying the established path.

### Deep-branching domain

The current generator samples

\[
[x_{\min},x_{\max}]\times\{x_{\mathrm{mid}}\}^{d-1}.
\]

For the full stochastic-rate problem, add rectangular bounds and sample both
wealth and rate:

\[
(X_i,Y_i)\sim
\operatorname{Uniform}
([x_{\min},x_{\max}]\times[y_{\min},y_{\max}]).
\]

The existing network already accepts \(d\)-dimensional states. Evaluation
must support fixed-rate slices and a full two-dimensional error set; the
one-dimensional `Curve` facade is not used to pretend that a surface is a
curve.

## Delivery stages

### Stage A: mathematical and deterministic reference

1. Record the full and reduced derivations in executable symbolic checks.
2. First remove intermediate consumption. The reduced PDE is then linear:

   \[
   F_t-\kappa yF_y+\frac12F_{yy}+(a_0+a_1y)F=0,\qquad F(T,y)=1,
   \]

   where

   \[
   a_0=(1-\gamma)\theta
   +\frac{(1-\gamma)\lambda^2}{2\gamma\sigma^2}-\rho,
   \qquad a_1=(1-\gamma)\eta.
   \]

   Use the exact Gaussian Vasicek expectation

   \[
   F(t,y)=\exp\left(a_0\tau+a_1m_I+\frac12a_1^2s_I^2\right),
   \quad \tau=T-t,
   \]

   with

   \[
   m_I=y\frac{1-e^{-\kappa\tau}}{\kappa},
   \]

   \[
   s_I^2=\frac1{\kappa^2}\left[
   \tau-\frac{2(1-e^{-\kappa\tau})}{\kappa}
   +\frac{1-e^{-2\kappa\tau}}{2\kappa}
   \right],
   \]

   as the first exact control.
3. For the consumption equation, implement an independent method-of-lines
   reference on a truncated \(y\)-interval, using centered spatial
   differences and an implicit stiff time integrator. Enlarge the spatial
   interval and refine both grids until the reported interior values stop
   changing at the target tolerance; exclude boundary-adjacent points from
   Monte Carlo validation.
4. Verify positivity of \(F\), the terminal condition, agreement with the
   exact no-consumption control, and convergence under grid/time/domain
   refinement.

This stage establishes a trusted answer before changing the Monte Carlo
mechanism.

### Stage B: reduced coding-tree benchmark

1. Implement the one-dimensional state-dependent PDE/code mechanism.
2. Estimate \(F(t,y)\) pointwise by coding-tree Monte Carlo.
3. Compare errors against the deterministic reference in units of Monte Carlo
   standard error.
4. Sweep horizon and branching rate to identify the integrability window.

Success criterion: at every selected interior checkpoint the absolute error
is at most four reported Monte Carlo standard errors, and the aggregate mean
over three independent seeds is at most two pooled standard errors from the
deterministic reference. The deterministic discretization error must be
smaller than one quarter of the Monte Carlo standard error used in the
comparison.

### Stage C: full two-dimensional value function

1. Generalize the state-dependent mechanism to \(d=2\).
2. Solve \(V(t,x,y)\) pointwise.
3. Check the homogeneity identity against the Stage B solution throughout a
   two-dimensional test grid.
4. Recover \(\pi^*\) and \(c^*\) from derivatives and compare them with the
   controls implied by the reduced solution.

Success criterion: both value and feedback controls satisfy the homogeneity
reference within Monte Carlo uncertainty.

### Stage D: deep branching on a rectangle

1. Generalize training-state sampling to vector bounds.
2. Train on \((x,y)\) rather than on a one-dimensional segment.
3. Compare network predictions with held-out coding-tree estimates and the
   homogeneity reference.
4. Plot fixed-rate slices and a two-dimensional error surface.

Success criterion: held-out error is comparable to the noise level in the
Monte Carlo labels, and consistency plots expose any optimization failure.

### Stage E: correlated shocks

Let

\[
d\langle W^S,W^r\rangle_s=\zeta\,ds.
\]

After optimizing \(\pi\), replace the portfolio term by

\[
-\frac{(\lambda V_x+\zeta\sigma V_{xy})^2}
{2\sigma^2V_{xx}}.
\]

This stage is accepted only after the independent case is stable. It adds the
mixed derivative \(V_{xy}\) but no new state variable.

## Validation strategy

- Preserve all existing tests and exact RNG-order tests.
- Unit-test mixed symbolic derivatives of the new nonlinearity.
- Golden-test the state-independent limit against the existing mechanism.
- Test terminal values and CRRA scaling exactly.
- Compare reduced Monte Carlo values with the deterministic reference.
- Compare full values with the reduced reconstruction on held-out points.
- Test at least three independent seeds and report estimate, standard error,
  tree-size diagnostics, and maximum absolute sample.
- Treat agreement from a single seed as insufficient because coding-tree
  estimators can have rare, heavy-tailed samples.

## Main risks

1. **Mechanism correctness.** Explicit state dependence changes the chain
   rule; a superficial `f(x,z)` API change would silently bias the estimator.
2. **Integrability.** The reduced reaction contains a negative power of
   \(F\); derivatives of that nonlinearity grow factorially.
3. **Artificial diffusion cancellation.** The full equation uses
   \(+V_{xx}/2-V_{xx}/2\), which is exact but may increase variance.
4. **Training coverage.** A line sample cannot validate a two-dimensional
   solution.
5. **Vasicek rates can be negative.** This is a known model property, not a
   numerical bug; the selected rate domain and parameters must make the
   interpretation explicit.

## Decision

Proceed with the staged independent-Vasicek design. Do not implement
correlation, CIR dynamics, or a full-domain neural solver until the reduced
state-dependent coding-tree estimator has passed deterministic and
statistical validation.
