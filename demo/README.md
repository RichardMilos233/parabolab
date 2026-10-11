# Demos

The solution demos define one PDE, solve it with multiple methods or sampling
settings, print a comparison table, and save a figure. The separate rate
sweep compares sampling diagnostics across several PDE configurations.
Current research concerns recursive moment control, rate selection and tuple
probabilities `q_c(Z)`; runtime is a supporting measurement.

```bash
python demo/allen_cahn.py        # Allen-Cahn d=1 (JCP2024 Table 1 / Fig. 1)
python demo/variance_reduction.py # Allen-Cahn: baseline / selected rate / terminal q / both
python demo/rate_variance.py     # finite-depth rate diagnostics + binary Riccati control
python demo/time_lambda.py       # full-tree second-moment T-lambda boundaries
python demo/merton.py            # Merton HJB d=1 (JCP2024 eq. (4.6), Table 5)
python demo/merton_vasicek.py     # retained stochastic-rate Merton example (d=1 reduced)
python demo/dym.py               # Dym non-integrability diagnostic (JEQ Fig. 6)
```

Figures land next to the scripts.

## One PDE, several methods

The scripts use the uniform solver interface (`parabolab.solve`). Every solver implements `Solver(**budget).solve(pde, grid) -> Curve`, so comparing or toggling methods is straightforward:

```python
curves = [
    CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid),
    DeepBranching(n_states=1000, m_samples=10_000, epochs=3000, n_jobs=8).solve(pde, grid),
    DeepBSDE(epochs=3000, n_states=1000).solve(pde, grid),
    DeepGalerkin(epochs=3000, n_states=1000).solve(pde, grid),
]
compare(pde, *curves).table().plot("out.png")
```

* **Coding-tree Monte Carlo** estimates a pointwise expectation
  ($\mathbb{E}[\mathcal{H}]$), when it exists, without neural-network training.
* **Deep Branching, Deep BSDE, and Deep Galerkin** fit neural networks. Their
  budgets and existing demo configurations remain available.

## Same solver, different sampling settings

`variance_reduction.py` uses the same `curves` list and `compare` call. It
selects two rates at `(t, x) = (0, 0)`, one with uniform tuple sampling and one
with a fixed `TerminalTupleProposal`, then compares four configurations:

- baseline: rate 1 and uniform tuples;
- selected rate and uniform tuples;
- rate 1 and the terminal-data tuple proposal;
- selected rate and the same terminal-data tuple proposal.

The only solver settings added are `rate=...`, `tuple_proposal=...`, and
`label=...`. Custom tuple proposals currently require `n_jobs=1`. The demo
prints setup/tuning time, sampling time, estimation errors, and average
empirical variance over the grid; the figure uses the existing error bars.

Rate selection uses a finite-depth quadrature objective. The selected rate
is reused across the grid and is not a pointwise optimum everywhere. The tuple
proposal uses terminal data, not exact child second moments. These are
estimation algorithms to evaluate, not guaranteed improvements on every PDE.
For node counts and pointwise variance-times-work diagnostics, use
[`examples/sampling_tuning.py`](../examples/sampling_tuning.py).

## Rate sensitivity diagnostics

`rate_variance.py` compares the short-time approximation
$\lambda_{\mathrm{short}}(x)=|f(\phi(x))|/|\phi(x)|$ with a numerical selector
and full-tree Monte Carlo samples at `T=0.05`. This formula is the leading
short-horizon rule for the specified scalar semilinear root, not an exact
finite-horizon optimum. The four panels are:

- Allen–Cahn wave at `x=0` and at `x=-1`, illustrating that the starting state
  affects the rate objective;
- spatially constant Fisher–KPP with terminal value `0.5`;
- binary Riccati control with terminal value `1`, whose explicitly binary
  mechanism has a closed-form full-tree second moment.

For the first three panels, the default deterministic curve is depth-two
second-moment quadrature minus the exact PDE mean squared. This is a proxy
for full-tree variance, not a certified enclosure or the variance of the
killed-depth estimator. Its numerical minimizer is constrained to a supplied
rate interval. The binary panel instead evaluates the exact Riccati formula
and numerically locates its stationary rate.

The current plot and table labels use “optimal”, “strict convexity” and
“verification”; read them within these scopes. A plotted U-shape and Monte
Carlo agreement do not prove convexity or certify a global optimum. The
variance error bars are plug-in estimates using the sample fourth moment,
not rigorous confidence bounds. The displayed variance reduction compares
the nearest sampled rates to `1` and to the selected rate, and clips negative
reductions to zero; it is not an exact comparison at those two rates.

For actual full-tree bounds, use the separate
[certified-rate report](../docs/research/results/certified-rate-checkpoint.md)
and [profile report](../docs/research/results/profile-efficiency-checkpoint.md).
The profile method chooses one common rate for several **starting states**;
it does not change the rate within a tree. It is optional when the research
question concerns only one starting state. Python selects and checks the
rates; Lean currently verifies selected mathematical lemmas, not the entire
sampler or numerical verifier.

## Full-tree second-moment boundary

`time_lambda.py` plots the analytic boundary
$T_2(\lambda)=\log(1+K\lambda^2)/\lambda$ for five spatially constant
polynomial examples: Allen–Cahn at terminal values `0.5` and `0.3`,
Fisher–KPP at `0.5` and `0.2`, and the standard binary control mechanism at
terminal value `1`. The `--T` option draws a reference horizontal; it does
not enter the boundary calculation. Equality is excluded from the displayed
safe interval.

This calculation applies to the raw uniform semilinear mechanism (tuple
probability `1/2`) with a caller-asserted globally flat terminal condition,
or to the library's standard binary mechanism. It makes no universal claim
for spatial waves, custom proposals, non-polynomial nonlinearities, or fully
nonlinear PDEs. `K` uses converged floating-point Gauss–Legendre quadrature
after mapping the infinite interval to a finite one; this numerical check is
not a formal certificate. The demo performs no Monte Carlo or depth
truncation.

The [full derivation, reviewed 12 October 2026](../docs/research/results/lambda-horizon-checkpoint.md#flat-polynomial-derivation)
starts from the original codewise first-step recursion. It proves spatial
independence and the pathwise-zero `D_x` subtree before simplifying the moment
system. With remaining time `r`, the derivative moments satisfy
$B_k'=\lambda B_k+2B_0B_{k+1}/\lambda$ and $B_k(0)=f^{(k)}(a)^2$.
After removing the common exponential factor, the cumulative variable
$z(r)=2\int_0^r B_0(s)ds/\lambda$ gives the polynomial
$Q(z)=\sum_k f^{(k)}(a)^2z^k/k!$ and
$\int_0^{z(r)}dw/Q(w)=2(e^{\lambda r}-1)/\lambda^2$.
For degree at least two and `f(a) != 0`,
$K=\tfrac12\int_0^\infty dw/Q(w)$ is finite. The root moment is squeezed
between $a^2e^{\lambda r}+z(r)/2$ and $e^{\lambda r}(a^2+z(r)/2)$,
so it reaches the same explosion endpoint. Equilibrium data `f(a)=0` and
degree at most one instead have no finite-time boundary.
This conditional derivation is exact; the reported `K` values and interval
roots are floating-point approximations, and the plot does not compute an
optimal rate or supply a new Lean proof.

That recurrence is specific to the raw derivative-coded semilinear
mechanism. The binary panel instead follows its separate Riccati moment
equation $M'=\lambda M+M^2/\lambda$, $M(0)=1$, which gives the same boundary
form with $K=1$.

The original Merton demos remain benchmarks. Multifactor Merton is no longer
the active research roadmap. Dym is a negative control: its specified
real-extension estimator is non-integrable for every positive rate, so its
finite-sample curves and displayed errors are not convergence evidence.

## Historical example runs

These previously recorded runs illustrate the network solvers; errors and
runtimes depend on the environment, seed, and budget.

| PDE | Method | $L_1$ Error | Runtime |
|---|---|---|---|
| Allen-Cahn $d=1$ | Deep Branching | 1.89e-03 | 22 s |
| | Deep BSDE | 5.68e-03 | 50 s |
| | Deep Galerkin | 5.31e-03 | 35 s |
| Merton HJB $d=1$ | Deep Branching | 1.12e-02 | 22 s |
| Merton Vasicek $d=1$ | Deep Branching | 6.89e-04 | 6 s |

Full multi-run paper reproduction scripts are located in `examples/`.
The [research guide](../docs/research/README.md) records current claims,
implementation limits, and next steps. The
[documentation map](../docs/documentation-map.md) distinguishes current
guidance, dated results and inactive research.
