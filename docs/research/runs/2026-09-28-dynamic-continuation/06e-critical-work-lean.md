# Lean gate for the critical moment--work inequality

Status: **passed** with Lean 4.33.0. The checked standalone module is
`formal/EstimatorIntegrity/CriticalMomentWork.lean`. It contains no `sorry`,
`admit`, or custom axiom declaration, and no existing module or entrypoint was
edited for this gate.

## Abstract `L²` moment--work bound

`criticalMomentWork_integrable_and_sq_le` is stated for an arbitrary type
`Omega` with a measurable space, an arbitrary measure `mu`, and real-valued
functions `H,N`. It assumes exactly

```text
0 <= N(omega)                    for every omega,
MemLp H 2 mu,
Integrable N mu.
```

Lean proves both

```text
Integrable (fun omega => |H(omega)| * sqrt(N(omega))) mu
```

and

```text
(integral |H|*sqrt(N) dmu)^2
  <= (integral H^2 dmu) * (integral N dmu).
```

The proof first obtains measurability of `sqrt ∘ N`. Pointwise
nonnegativity gives `(sqrt N)^2=N`, so integrability of `N` yields
`MemLp (sqrt ∘ N) 2 mu`. The `L²` product theorem proves the first
conclusion. Mathlib's nonnegative Holder inequality with conjugate exponents
`2,2` proves the unsquared estimate; nonnegativity, square monotonicity, and
the square-root identities give the displayed product bound. No finite-measure
assumption or almost-everywhere weakening was introduced.

## Critical exponent algebra

For real `alpha,p` with `0<alpha` and `1<p`, Lean proves

```text
(p-1)/p < 1/(alpha+1)  <->  p < 1 + 1/alpha
```

in `criticalExponent_lt_iff`. The proof records positivity of both
denominators and cross-multiplies explicitly. The companion theorem
`criticalExponent_eq_iff` proves the exact equality boundary

```text
(p-1)/p = 1/(alpha+1)  <->  p = 1 + 1/alpha.
```

Finally, `criticalExponent_alpha_one_p_two` checks the requested endpoint
identity at `alpha=1,p=2`:

```text
(2-1)/2 = 1/(1+1).
```

## Verification records

The fresh standalone build command

```text
~/.elan/bin/lake build EstimatorIntegrity.CriticalMomentWork
```

completed successfully with all 3396 jobs built. Its output is saved in
`lean/critical-moment-work/build.log`.

`lean/critical-moment-work/CriticalMomentWorkAxioms.lean` runs
`#print axioms` for all four declarations. The saved output in
`lean/critical-moment-work/axioms.log` reports only Mathlib's standard
foundational axioms `propext`, `Classical.choice`, and `Quot.sound` for each
theorem. Resolved development diagnostics are saved in
`lean/critical-moment-work/development.log`.

## Formalization boundary

The analytic theorem is an abstract real-measure inequality. It does not
formalize the canonical completed-tree measure, the Radon--Nikodym identity
`d|nu|=|H| dQ`, full syntactic node counts, adaptive proposal laws, the
optimal tilted proposal, or support-restoring mixtures.

The module also does not formalize the critical ODE family, terminal jets,
endpoint total variation, the equality between time degree and full node
count, the endpoint cusp, the fractional-moment integral test, logarithmic
divergence at equality, or signed ODE correspondence. Those reviewed results
are the conventional arguments that supply the abstract functions and
integrals used here.

Consequently this gate certifies the real variance--work Cauchy--Schwarz
inequality and the exact finite exponent bridge. It makes no claim about a
canonical tree sampler, general Holder exponents, constructive sampling,
endpoint divergence, optimal proposals, or the complete frontier theorem.
