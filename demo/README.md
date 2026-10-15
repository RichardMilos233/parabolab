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
$T_2(\lambda)=\log(1+K\lambda^2)/\lambda$ for four spatially constant
polynomial examples: Allen–Cahn at terminal values `0.5` and `0.3` and
Fisher–KPP at `0.5` and `0.2`. The heatmaps sample actual coding trees on a
configurable `T`–lambda grid; the theoretical boundary never supplies the
heatmap values.

For each grid cell, the main statistic is the sample variance of the
individual tree outputs, with `ddof=1`:

\[
\widehat{\operatorname{Var}}(H)
=\frac1{N-1}\sum_{i=1}^N(H_i-\overline H)^2.
\]

This is not the variance of the sample mean (which would divide by `N`
again), and it does not subtract an exact PDE solution squared. Each
horizon uses a newly constructed PDE with that terminal time.

### Why the variance alone can look stable beyond the boundary

With flat data, every branching of an `f^(k)` particle selects the tuple
`(Dx, Dx, ...)` with probability `1/2`, and that tuple makes the whole tree
value zero (`phi' = 0`). Derivative chains also end in `f^(k) ≡ 0`. As
`lambda T` grows, almost every tree is therefore exactly zero, while the
unbiased estimator keeps `E[H] = u(0)`; the rare nonzero trees carry
correspondingly large weights (roughly `u/p` when a fraction `p` is
nonzero, so `E[H^2] ≈ u^2/p`). Beyond `T_2` the second moment is infinite,
yet a finite batch may contain no nonzero tree at all and report a small or
zero variance. The demo therefore records several diagnostics per cell.

### Reading the figures

Every panel is one PDE; the horizontal axis is the branching rate `lambda`,
the vertical axis the horizon `T`, and each cell is an independent batch of
`N` trees started at `(t, x) = (0, 0)`. Common overlays:

- **solid white/black curve, `T_2(lambda)`**: the analytic second-moment
  boundary. Below it `E[H^2] < infinity`; on and above it `E[H^2] = infinity`.
  It is computed from the moment ODE, never from the samples.
- **grey cells**: no value to show — the batch failed (overflow, node
  limit), or the statistic is undefined (all samples zero).
- **panel title**: PDE, grid, `N` per cell and the sampler used
  (`flat-data sampler (special case)` or `general sample_tree`).

| Figure | Statistic per cell | How to read it | What it is for | Limits |
|---|---|---|---|---|
| `time_lambda.png` | sample variance `s^2 = sum (H_i - mean)^2 / (N-1)` (symlog colour scale); thin lines are iso-variance contours `s^2 = 0.1, 1, 10, 100` (value written on each line, drawn from the raw per-cell values with no smoothing) | dark = small, bright = large; below `T_2` the contours are smooth and ordered (the data are smooth there), above it they break into fragments; also look for the speckle (neighbouring cells differing by orders of magnitude) | the quantity a user of the estimator actually sees; shows how large and how erratic the variance becomes | beyond `T_2` it is a finite number from a finite batch; all-zero batches show `0`, which looks *stable* although the true variance is infinite |
| `time_lambda_slices.png` | for `lambda ≈ 1, 2, 6`: the MC sample variance (dots) along `T` and the exact `Var(H)` (black) from the moment ODE `m_k' = lambda m_k + 2 m_0 m_{k+1}/lambda` (with the matching first-moment ODE for `E[H]`) | below `T_2` the dots lie on the black curve; the black curve shoots to infinity at `T_2` (red dashed), the dots continue smoothly and scatter above it | checks the sampler against exact theory and shows why the heatmaps cannot show a sharp edge at `T_2` | near `T_2` the MC variance is systematically low (observed 12–90 % of the exact value in the last `0.05` before `T_2` at `N = 10^6`): the divergence is carried by trees far rarer than `1/N` |
| `time_lambda_max_share.png` | `max_i H_i^2 / sum_i H_i^2`, the largest sample's share of the sum of squares (0 to 1) | near 0 (dark) = many samples contribute; near 1 (yellow) = one sample *is* the variance | the diagnostic matched to `T_2`: for i.i.d. samples it tends to 0 almost surely **iff** `E[H^2] < infinity`; it should be dark below the curve and stay patchy/bright above it as `N` grows | a single batch: values are random; just above `T_2` the tail is barely too heavy and the ratio decays only slowly, so the boundary looks gradual, not sharp |
| `time_lambda_batch_cv.png` | split the `N` samples into 10 consecutive batches, compute each batch's variance `v_1..v_10`, then `std(v)/mean(v)` (0 to 3) | 0 = the 10 repeated variance estimates agree; 3 = all variance sits in one batch | reproducibility: would a repeated experiment give the same variance? | governed by the **fourth** moment, which diverges earlier than the second; it can light up below `T_2` and is not a test of the `T_2` boundary |

`n_nonzero` (number of nonzero samples, in the NPZ) is not plotted; it
explains the grey all-zero cells and how much information a cell carries.

Observed in the 101 × 101 × 10^6 run (15 October 2026; one batch per
cell, so an observation, not a test): `max_share` is near zero below every
curve; 10× more samples (10^5 → 10^6) made cells 0.1–0.4 above `T_2` more
often unstable but barely changed the band just above it: close to `T_2`
the tail is only slightly too heavy, so the instability appears gradually
rather than as a sharp edge.

These are finite-sample diagnostics. Agreement with the curve is
experimental evidence consistent with the analytic boundary, not a
numerical proof of explosion; the proof is the moment calculation below.

### Samplers and parallel runs

> **Scope.** The general estimator is `parabolab.tree.sample_tree`
> (`--sampler tree`); it is unchanged and remains the reference for every
> PDE in the package. The figures of this demo are produced with the
> accelerated `--sampler flat`, which is valid **only** for semilinear PDEs
> with the raw uniform mechanism, polynomial `f` and a globally constant
> terminal condition (`phi' = 0`), root `Id` at `t = 0`. It does not apply
> to spatial terminal data, tuple proposals, fully nonlinear or
> multidimensional PDEs. Each panel title names the sampler used.

The default `--sampler flat` (`parabolab/flat_batch.py`) advances all
particles of a chunk of trees together as arrays. It uses that `H` is the
product of node factors, that Brownian positions do not enter flat data, and
that a sample can be abandoned once a factor is zero. Its `H` has the same
law as `sample_tree` (tested against `sample_tree` and against the exact
second-moment ODE), but its random stream differs, and its node counts cover
only the visited particles, so they are not comparable with `sample_tree`
counts. `--sampler tree` runs the original recursive estimator.

`--n-jobs N` distributes chunks over `N` worker processes; `--chunk-size C`
sets independently seeded chunks of at most `C` trees (flat default:
`100000`). Results depend on the seed, sampler and chunk size, not on `N`.
Neither sampler has a depth cutoff or default node budget; `--max-nodes`
optionally marks a cell invalid (grey) when any tree visits more nodes.
Arithmetic overflow or recursion failure also marks a cell invalid rather
than assigning zero variance.

This calculation applies to the raw uniform semilinear mechanism (tuple
probability `1/2`) with a caller-asserted globally flat terminal condition.
It makes no universal claim for spatial waves, custom proposals,
non-polynomial nonlinearities, or fully nonlinear PDEs. `K` uses converged
floating-point Gauss–Legendre quadrature after mapping the infinite interval
to a finite one; this numerical check is not a formal certificate. The
boundary calculation itself uses no Monte Carlo or depth truncation.

Run the default (four PDE cases, a `12 × 10` grid per case, 128 trees per
cell):

```bash
python demo/time_lambda.py
```

A large configuration (an example command, not a recorded completed
experiment):

```bash
python demo/time_lambda.py \
  --mc-lambda-points 101 --mc-T-points 101 --samples-per-cell 100000 --n-jobs 8
```

The default ranges are lambda `0.01–12` and T `0.05–1.3`. These can be changed
in the demo's sweep call if needed. Runs are reproducible from their saved
seed, sampler and chunk size. Checkpoints are written every five minutes.

Output goes to `--output-dir` (default `demo/`): `time_lambda.png` (variance,
plus one panel per case), `time_lambda_max_share.png`,
`time_lambda_batch_cv.png`, `time_lambda_slices.png` and `time_lambda_mc.npz`. Per-case checkpoints
are saved alongside them, including on a keyboard interrupt. The NPZ
contains axes, observed statistics, diagnostics, completion counts,
statuses, reasons and sampling settings. Generated NPZs and figures are
ignored by Git. To redraw saved data without sampling, use the library:

```python
from parabolab import TimeLambdaMCComparison
data = TimeLambdaMCComparison.load("demo/time_lambda_mc.npz")
data.plot("demo/time_lambda.png")
data.plot("demo/time_lambda_max_share.png", statistic="max_share")
```

The library retains `sweep_time_lambda` for theory-only plots and optional
explicit node limits in `sweep_time_lambda_mc` for callers that need them;
both node limits default to `None`. An explicit limit invalidates the whole
affected cell rather than substituting a truncated or survivor-only variance.

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
