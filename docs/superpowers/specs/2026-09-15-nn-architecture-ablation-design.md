# Deep-branching network ablation study

Status: approved in chat on 2026-09-15 ("go ahead"). Branch:
`research/nn-architecture`.

## Goal

Find out which changes to the deep branching solver's network and training
protocol improve **accuracy** (L1/L2 on the paper's 101-point grid) and
**robustness** (no runs that detach from the Monte Carlo scatter, cf.
gotcha 27) on the three JCP2024 one-dimensional-slice benchmarks — and
attribute every gain to one change. The study is a ladder of single-knob
ablations from the paper's own architecture, run on Monte Carlo data that
is generated once and frozen.

Higher-dimensional fitting (training states sampled in the full
\(d\)-dimensional box) is a follow-on, not part of this spec; the harness
must not preclude it.

## Non-goals

- Changing the Monte Carlo sampler, the mechanism, the rate, or the outlier
  filter. The regression targets are the paper's.
- Beating the paper by changing the evaluation protocol: `grid_errors`
  (101 points, \(t=0\), segment \([x_{lo},x_{hi}]\)) stays the referee.
- Random/Bayesian hyperparameter search.
- Sobolev / derivative-code training (gotcha 25d) — a separate research
  direction.
- GPU work. The 4060 is available but the env ships `torch 2.13.0+cpu`; the
  budgets here (\(\le 128\)-wide nets, 1000 states, full batch) run on CPU
  in seconds to a minute per training. Switching to the CUDA wheel is a
  one-line env change documented in CLAUDE.md and is out of scope.

## Benchmarks (frozen data)

| Key | PDE factory | Segment | \(M\) (paper) | Paper L1 (SD) | Ours so far |
|---|---|---|---|---|---|
| `ac1` | `library.allen_cahn_nd(d=1, T=0.5)` | \([-8, 8]\) | 100 000 | 1.32e-3 (1.05e-4), JCP Table 1 | 1.89e-3 at \(M = 10^4\) |
| `exp1` | `library.exponential_gradient_nd(d=1, T=0.05, alpha=10.0)` | \([-4, 4]\) | 30 000 | 1.17e-2 (1.36e-3), JCP Table 3 | — |
| `merton` | `library.merton_hjb()` (T=0.1, defaults) | \([100, 200]\) | 10 000 | 8.49e-3 (7.44e-4), JCP Table 5 / Fig 7 | 1.12e-2; 1 run in 10 anomalous (gotcha 27) |

Budget: \(N = 1000\) states, \(M\) per benchmark as in the table (the
paper's own), jcp rate, \(\tau \equiv 0\), 10 % overtrain — exactly the
`--full` settings of the three `examples/jcp_table*_deep.py` scripts. Three
**data seeds** (0, 1, 2) per benchmark, generated once by
`generate_training_data` and cached as `.npz` (fields of `TrainingData`
plus the generation arguments). Nine datasets total; generation cost is
~15 s per \(10^7\) trees on 6 cores (CLAUDE.md), so ≈ 3 min for the
\(M = 10^5\) AC sets and well under a minute for the others.

R0 reproduction criterion: median L1 within 2× of the paper's value on
every benchmark (our earlier reproductions were 1.4×–1.3× above the paper,
with fewer samples). Failing this stops the ladder until explained.

## Architecture of the study code

Four small units under `parabolab/deep/`, one script, one results file.
Existing `DeepBranchNet`, `train_deep_branching`, `grid_errors`,
`generate_training_data` keep their signatures and defaults so the M4
reproductions and `tests/test_deep.py` are untouched.

### 1. `parabolab/deep/datasets.py` — frozen data

- `DatasetSpec(key, factory_name, x_lo, x_hi, n_states, m_samples, seed)`
  (frozen dataclass; `factory_name` resolves to a `library` callable so the
  spec is picklable and reproducible).
- `dataset_path(spec, root) -> Path` (`<root>/<key>_s<seed>.npz`).
- `load_or_generate(spec, root, n_jobs) -> TrainingData`: loads the `.npz`
  if present, else generates, saves, returns. Stores the spec fields as
  npz metadata and refuses to load a file whose stored spec disagrees.
- The three benchmark specs as a module-level dict `BENCHMARKS`.

### 2. `parabolab/deep/net.py` — configurable network

Extend `DeepBranchNet` **backwards-compatibly** (all new arguments default
to the current behaviour):

- `norm: {"batch", "layer", "none"}` (default `"batch"`).
- `activation` gains `"silu"`, `"gelu"`, `"sin"`.
- `fourier_features: int = 0` — if \(>0\), the spatial coordinates are
  mapped through \(B\)-fixed random Fourier features
  \([\cos(2\pi Bx), \sin(2\pi Bx)]\) with \(B \sim N(0, \sigma_B^2)\),
  `fourier_sigma: float = 1.0`, seeded from the net's torch seed; \(t\) is
  passed through unchanged.
- `input_scaler: Optional[(mean, std)]` and `output_scaler: Optional[(mean,
  std)]` — fixed (non-trainable) affine maps applied to `tx` before the first
  layer and to the output after the last. Registered as buffers so the net
  stays self-contained at evaluation time.

`forward` unchanged in structure: plain first layer, residual hidden
layers, identity output.

### 3. `parabolab/deep/solver.py` — training options

Extend `train_deep_branching` backwards-compatibly:

- `loss: {"mse", "weighted_mse"}`; weighted uses \(w_i = 1/\max(\text{stderr}_i,
  \epsilon)^2\), normalised to mean 1, with `stderr` taken from
  `TrainingData`. \(\epsilon\) = 1e-3 × median stderr.
- `schedule: {"multistep", "cosine"}` (default the paper's multistep).
- `grad_clip: Optional[float]` (default `None`).
- `lbfgs_steps: int = 0` — after the Adam epochs, this many full-batch
  L-BFGS iterations (`torch.optim.LBFGS`, strong-Wolfe line search) on the
  same loss.
- Scalers: if the net carries scalers, the trainer fits them from the
  training data before the loop (`fit_scalers(net, data)`) — the trainer,
  not the net constructor, owns this so that the net can be built before
  data is loaded.

### 4. `parabolab/deep/ablation.py` — configs, runs, metrics

- `NetConfig` / `TrainConfig` frozen dataclasses mirroring the arguments
  above, plus a `RungConfig(name, parent, net, train)` with a
  `to_dict()` for the results file.
- `run_rung(rung, dataset, train_seeds, device) -> list[RunRecord]`: one
  training per seed on the given dataset. `RunRecord` holds rung name,
  benchmark key, data seed, train seed, L1, L2, consistency statistic,
  final loss, wall time, and the `n_params`.
- Metrics per (rung, benchmark) over all data seeds × train seeds:
  - `l1_median`, `l2_median` (accuracy);
  - `l1_max` and `n_outliers` = number of runs with L1 > 3 × `l1_median`
    (robustness);
  - `consistency_median` = median over runs of
    \(\frac1N\sum_i \big((v(\tau_i,X_i) - y_i)/\text{stderr}_i\big)^2\)
    (the Fig-7 check as a number; \(\approx 1\) means the net sits inside
    the MC scatter; \(\gg 1\) is a detached net).
- `ladder()` returns the ordered list of rungs (below). A rung's `parent`
  is the kept state it builds on; "kept" is decided by the researcher from
  the table and recorded in the spec's results section, not by code.

### 5. `examples/nn_ablation.py` — driver

```
python examples/nn_ablation.py --rungs R0 R1 --benchmarks ac1 merton \
    --train-seeds 5 --data-root examples/nn_ablation_data \
    --out examples/nn_ablation_results.csv
```

Appends one row per `RunRecord` to the CSV (idempotent: skips rows already
present for the same rung/benchmark/data seed/train seed), then prints the
per-rung metric table. `--report` renders the table as Markdown for the
results section. Runs under `if __name__ == "__main__"` (gotcha 37).

## The ladder

Each rung changes exactly one thing relative to its parent. Defaults not
mentioned are the paper's (6 × 20, tanh, BN, full-batch Adam lr 0.01 with
÷10 at P/3 and 2P/3, P = 3000, MSE on means).

| Rung | Parent | Change |
|---|---|---|
| R0 | — | paper baseline on frozen data (must reproduce Tables 1/3/5 within the paper's own spread) |
| R1 | R0 | input standardisation of \((t, x)\) |
| R2 | best of R0–R1 | output standardisation |
| R3a / R3b | best so far | norm = none / layer |
| R4a / R4b / R4c | best so far | activation = silu / gelu / sin |
| R34 | best so far | factorial cell: {batch, layer, none} × {tanh, best of R4} (6 configs, minus those already run) |
| R5a / R5b / R5c | best so far | neurons = 64 / 128; hidden_layers = 4 / 8 (as separate rungs) |
| R6 | best so far | Fourier features: 32 features on the *scaled* \(x\) (applied after the input scaler, so \(x\) is O(1)), \(\sigma_B = 1\) |
| R7 | best so far | weighted MSE |
| R8a / R8b / R8c | best so far | cosine schedule / grad-clip 1.0 / Adam + 200 L-BFGS steps |
| R9 | best so far | ensemble: median of the 5 train-seed nets (evaluated, not trained) |

"Best so far" = the rung with the lowest `n_outliers`, ties broken by
`l1_median`, across the three benchmarks summed. A rung that improves one
benchmark and worsens another is recorded as such and is not kept.

Evidence per rung: 5 train seeds × 3 data seeds × 3 benchmarks = 45
trainings, ≈ 20 s each at 6 × 20 on CPU (longer for R5), so ≈ 15–30 min per
rung; the whole ladder ≈ 6–8 h CPU, run rung by rung.

## Error handling

- Missing or corrupt `.npz`: regenerate (log it); a spec mismatch is an
  error, never a silent overwrite.
- A training that produces non-finite loss or non-finite grid predictions
  is recorded with `l1 = inf` and counted as an outlier, not dropped.
- CSV writes are append-only with a header check; a partial rung can be
  resumed.

## Testing

`tests/test_deep_ablation.py`, fast (tiny nets, 20 epochs, 8 states, 4
samples):

- `DeepBranchNet` new options: shape and finiteness for every
  `norm`/`activation`; scalers are buffers and round-trip through
  `state_dict`; `fourier_features=0` is byte-identical to the current net
  (same seed ⇒ same output).
- `train_deep_branching` defaults produce the same losses as before on a
  fixed tiny dataset (regression guard); weighted loss with all-equal
  stderr equals plain MSE; L-BFGS path runs and does not increase the loss.
- `datasets.load_or_generate` writes, reloads bit-identically, and rejects a
  mismatched spec.
- `ablation`: `run_rung` on a tiny dataset returns one record per seed with
  finite metrics; the CSV append is idempotent; `n_outliers` and the
  consistency statistic computed on hand-built records match by hand.

Existing `tests/test_deep.py` and `tests/test_solve.py` must stay green.

## Deliverables

1. The four code units, the driver, the tests.
2. `examples/nn_ablation_results.csv` (checked in; ~1000 rows) and a
   results section appended to this spec: the per-rung table, the kept
   path, and a one-paragraph reading per rung stating whether the change
   helped, hurt, or did nothing, with the numbers.
3. CLAUDE.md gotchas for anything non-obvious discovered (e.g. if input
   standardisation alone removes the Merton anomaly).

## Results

All runs: `examples/nn_ablation_results.csv`; datasets in
`examples/nn_ablation_data/` (git-ignored, regenerable from `BENCHMARKS`).
Columns: L1/L2 medians over 5 training seeds × 3 data seeds, L1 max,
outlier runs (L1 > 3× median or non-finite), median consistency statistic.
`+ens` rows = median of the five seed-nets per dataset (rung R9), so 3 runs.
Machine: 32-core laptop CPU, torch 2.13 CPU; one training ≈ 9 s.

### R0 — paper baseline on frozen data

Datasets generated with the paper budgets (ac1 M = 10⁵: 50 s per set;
exp1 M = 3·10⁴: 21 s; merton M = 10⁴: 12 s, 16 workers).

| rung | benchmark | runs | L1 median | L2 median | L1 max | outliers | consistency |
|---|---|---|---|---|---|---|---|
| R0 | ac1 | 15 | 1.12e-03 | 2.72e-06 | 1.37e-03 | 0 | 1400.85 |
| R0 | exp1 | 15 | 1.13e-02 | 4.58e-04 | 1.21e-02 | 0 | 1.11 |
| R0 | merton | 15 | 8.68e-03 | 9.33e-05 | 1.52e-01 | 1 | 3.07 |
| R0+ens | ac1 | 3 | 9.99e-04 | 2.33e-06 | 1.16e-03 | 0 | 637.89 |
| R0+ens | exp1 | 3 | 1.12e-02 | 4.54e-04 | 1.16e-02 | 0 | 1.10 |
| R0+ens | merton | 3 | 7.64e-03 | 8.07e-05 | 8.41e-03 | 0 | 2.85 |

Reading. The reproduction criterion (median L1 within 2× of the paper) is
met on all three: ac1 1.12e-3 vs 1.32e-3, exp1 1.13e-2 vs 1.17e-2, merton
8.68e-3 vs 8.49e-3. The Merton anomaly of gotcha 27 reproduces on frozen
data: run (d2, s2) trains to L1 1.52e-1 with consistency 159 while the other
14 runs sit at 4.7e-3–1.5e-2 — same data as its four sibling seeds, so it
is the optimiser, not the draw. Even the non-anomalous Merton runs spread
3× across training seeds (4.7e-3 to 1.49e-2 on dataset 0), which is the
robustness target for the ladder. The median-of-5 ensemble (R9) removes the
outlier (7.64e-3, max 8.41e-3) at 5× the training cost — the floor every
later rung is compared against.

Two properties of the metrics, fixed by the data rather than by any rung:
(i) on exp1 and merton the net sits inside the MC scatter (consistency
1.1 and ≈3), so L1 is bounded below by target noise (median stderr 1.3e-2
and 3.1e-2 on |y| ≈ 1.9 and 26) and accuracy gains must come from
averaging noise, not from capacity; (ii) on ac1 the consistency statistic
is in the hundreds–thousands although L1 ≈ 1e-3: the traveling wave
saturates at ±1 for |x| ≳ 4, where all 10⁵ samples agree and stderr is
≈ 0, so a 1e-4 fitting error there is hundreds of standard errors. On ac1
the statistic therefore measures net capacity in the flat tails, not
detachment from the data; compare it across rungs, not against 1.

Plan amendment recorded during implementation: the L-BFGS polish (R8c)
runs with the net in eval mode so BatchNorm running statistics are not
updated by the line search; the weighted loss (R7) raises if no state has
a finite stderr.

### R1 — input standardisation of (t, x) (parent R0)

| rung | benchmark | runs | L1 median | L2 median | L1 max | outliers | consistency |
|---|---|---|---|---|---|---|---|
| R0 | ac1 | 15 | 1.12e-03 | 2.72e-06 | 1.37e-03 | 0 | 1400.85 |
| R1 | ac1 | 15 | 9.70e-04 | 2.21e-06 | 1.19e-03 | 0 | 809.65 |
| R0 | exp1 | 15 | 1.13e-02 | 4.58e-04 | 1.21e-02 | 0 | 1.11 |
| R1 | exp1 | 15 | 1.13e-02 | 4.43e-04 | 1.18e-02 | 0 | 1.10 |
| R0 | merton | 15 | 8.68e-03 | 9.33e-05 | 1.52e-01 | 1 | 3.07 |
| R1 | merton | 15 | 5.39e-03 | 4.31e-05 | 7.83e-03 | 0 | 2.67 |
| R1+ens | ac1 | 3 | 8.81e-04 | 1.94e-06 | 1.03e-03 | 0 | 165.70 |
| R1+ens | exp1 | 3 | 1.12e-02 | 4.39e-04 | 1.15e-02 | 0 | 1.08 |
| R1+ens | merton | 3 | 4.74e-03 | 3.32e-05 | 6.17e-03 | 0 | 2.63 |

Reading: helped, on both axes. Merton — the benchmark whose raw inputs are
x ∈ [100, 200] fed straight into tanh — drops from median 8.68e-3 to
5.39e-3 (below the paper's 8.49e-3), the worst run from 1.52e-1 to 7.83e-3,
and the seed spread from 3× to 1.7×; the anomaly does not appear in 15
runs. ac1 improves 13 % (1.12e-3 → 9.70e-4); exp1 is unchanged, as
expected at its MC-noise floor. A single R1 net now matches R0's
five-net ensemble on Merton (5.39e-3 vs 7.64e-3 median). **Kept: yes.**
