# Fixed deterministic checks for the critical moment/work frontier

Status: protocol only, not executed. Run only after T22 conventionally accepts
04h and a separate named Lean gate for the moment/work inequality or its
fixed algebraic reduction has built successfully. This preserves the user's
theory -> Lean -> code order. It does not authorize a stochastic sampler or
change the frozen dynamic experiment.

## Purpose and fixed cases

Illustrate the reviewed endpoint threshold for f_alpha=(1+y^2)^(-alpha),
constant zero datum. Use alpha in {1/2,1,2}, p=2, beta=1/2, and cutoff
delta in {1e-2,1e-4,1e-6,1e-8}. Use mpmath at 80 decimal digits, with no
outcome-dependent precision or case selection. Preserve every value, source
hash, environment version, runtime and failed check.

1. Compute tau_alpha by direct quadrature of (1-z^2)^alpha on [0,1] and
   independently by sqrt(pi)*Gamma(alpha+1)/(2*Gamma(alpha+3/2)).
   Require absolute discrepancy <1e-60.
2. For derivative orders 0 through 12 at zero, compare high-precision
   differentiation of f_alpha with zero at odd orders and
   (-1)^k*(2k)!*(alpha)_k/k! at order 2k. Require scaled discrepancy
   abs(direct-formula)/max(1,abs(formula))<1e-60.
3. For each fixed delta evaluate the positive tail
   B_alpha(delta)=integral_(1-delta)^1 (1-z^2)^alpha dz directly and with
   the incomplete beta function. Require scaled discrepancy <1e-60.
   Record B_alpha(delta)/delta^(alpha+1), alongside its proved limit
   2^alpha/(alpha+1). These finite ratios illustrate the cusp; they do not
   prove the limit or any integrability classification.
4. Define F_alpha(z)=integral_0^z(1-y^2)^alpha dy and

       J_alpha(z)=(1-z)*[-log(F_alpha(z)/tau_alpha)]^(-3/2)
                   *(1-z^2)^alpha/F_alpha(z).

   Near z=1 compute -log(F/tau) as -log1p(-B/tau) from the complementary
   beta tail, avoiding cancellation. Record the endpoint contribution

       K_alpha(delta)=sqrt(2)/(2*sqrt(pi))
                      *integral_(1/2)^(1-delta) J_alpha(z) dz.

   It is a truncated endpoint contribution to the sqrt-node absolute mass,
   not the full mass S_2. Check positivity and monotonic increase as the
   cutoff decreases. Plot all three fixed curves against log10(1/delta).
   The reviewed theorem predicts a finite limit for alpha=1/2, logarithmic
   divergence for alpha=1, and a power divergence for alpha=2. Label these
   predictions as theory, never conclusions established by four data points.
5. At z=1-delta record the scaled integrand
   J_alpha(z)*delta^((alpha+1)/2) and the analytic limiting value
   (alpha+1)^(3/2)*sqrt(tau_alpha/2^alpha). Do not use an arbitrarily chosen
   residual threshold on finite-delta asymptotic error as a theorem test.

## Artifacts and interpretation

Use new `numerics/check_critical_frontier.py`,
`numerics/critical_frontier_checks.json`, a captured execution log, and
`critical-frontier.png/.svg`. Refuse to overwrite existing final artifacts.
The JSON must separate exact-identity acceptance checks from asymptotic
diagnostics, preserve high-precision values as decimal strings, and record
which gate files/hashes were read before execution.

The figure should show the cusp ratio and the three truncated endpoint
contributions with explicit units, cutoff, alpha and source captions. No
Monte Carlo confidence interval, empirical proof of infinity, finite full
moment claim for a cutoff computation, or runtime advantage claim is allowed.
The signed scalar ODE remains globally solvable; this is a diagnostic of the
original tree representation, not a proposed competitive ODE algorithm.
