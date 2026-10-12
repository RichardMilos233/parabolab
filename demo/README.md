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

## Time–rate boundary and Monte Carlo variance heatmap

`time_lambda.py` overlays the analytic boundary
$T_2(\lambda)=\log(1+K\lambda^2)/\lambda$ for five spatially constant
polynomial examples: Allen–Cahn at terminal values `0.5` and `0.3`,
Fisher–KPP at `0.5` and `0.2`, and the standard binary control mechanism at
terminal value `1`. The `--T` option draws a reference horizontal; it does
not enter the boundary calculation. In the theory-only view, equality is
excluded from the displayed safe interval. The heatmap samples actual coding trees on a configurable
`T`–lambda grid and displays their empirical variance; the theoretical
boundary never supplies the heatmap values.

For each grid cell, the statistic is the sample variance of the individual
tree outputs, with `ddof=1`:

\[
\widehat{\operatorname{Var}}(H)
=\frac1{N-1}\sum_{i=1}^N(H_i-\overline H)^2.
\]

This is not the variance of the sample mean (which would divide by `N`
again), and it does not subtract an exact PDE solution squared. Each
horizon uses a newly constructed PDE with that terminal time. Grid density,
samples per cell and random seed are separate controls, so small local runs
and larger overnight or SSH runs use the same experiment.

The color scale shows measured variance across orders of magnitude. A
completed batch with zero sample variance is displayed at the low end,
not treated as missing. Finite samples can miss rare large trees even where
the theoretical second moment is infinite. A smooth interior or a sudden
increase near the curve is an experimental observation to inspect, not a
pattern imposed by the plot or a finite-sample certificate of explosion.

Sampling uses the original full-tree estimator without a depth cutoff.
Optional node budgets stop excessive work by marking the whole affected
cell incomplete; a stopped tree is not replaced by zero, and surviving
samples are not reported as an ordinary complete-batch variance. Budget
failures, numerical overflow and unfinished cells remain distinguishable
in saved data and are separate from the variance colors.

This calculation applies to the raw uniform semilinear mechanism (tuple
probability `1/2`) with a caller-asserted globally flat terminal condition,
or to the library's standard binary mechanism. It makes no universal claim
for spatial waves, custom proposals, non-polynomial nonlinearities, or fully
nonlinear PDEs. `K` uses converged floating-point Gauss–Legendre quadrature
after mapping the infinite interval to a finite one; this numerical check is
not a formal certificate. The boundary calculation itself uses no Monte
Carlo or depth truncation; the accompanying heatmap is a separate MC
diagnostic. Saving its axes, statistics, completion status and sampling
settings allows figures to be redrawn without resampling.

Run the lightweight default (five PDE cases, a `12 × 10` grid per case,
128 trees per cell):

```bash
python demo/time_lambda.py
```

Increase grid resolution and samples independently when more compute is
available. This larger configuration is an example command, not a recorded
completed experiment:

```bash
python demo/time_lambda.py \
  --mc-lambda-points 40 --mc-T-points 30 --samples-per-cell 10000 \
  --lambda-min 0.01 --lambda-max 12 --T-min 0.05 --T-max 1.3 \
  --seed 20261012 --max-nodes 100000 --max-cell-nodes 0 \
  --mc-data demo/time_lambda_mc_large.npz --output demo/time_lambda_mc_large.png
```

`--max-nodes` is the per-tree work guard and `--max-cell-nodes` the aggregate
guard for each grid cell; either accepts `0` to disable that guard. The
defaults are 5,000 and 100,000 nodes respectively. If many cells are marked
incomplete, inspect their saved reasons before increasing budgets. Increasing
the sample count can also require increasing the cell budget. These guards
do not change the theoretical boundary.

The default data file is `demo/time_lambda_mc.npz`. Per-case checkpoints
are saved alongside it, including on a keyboard interrupt. The saved arrays
contain the two axes, variance, mean, second moment, completed sample counts,
node counts, status and reason; node counts include attempted nodes in trees
that hit a node guard, but exclude the unfinished tree when arithmetic or
recursion fails. JSON metadata within the NPZ stores the seed,
requested samples and budgets. Generated demo NPZs and figures are ignored
by Git. Redraw saved data, or select the previous theory-only view:

```bash
python demo/time_lambda.py --load-mc demo/time_lambda_mc.npz
python demo/time_lambda.py --no-mc --output demo/time_lambda_theory.png
```

Loading saved data performs no sampling. Changing the seed gives an independent
repeat with which to inspect the stability of the observed colors; increasing
samples alone does not certify the true variance near an infinite-moment
boundary.

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
