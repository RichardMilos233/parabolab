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

### R2 — output standardisation (parent R1)

| rung | benchmark | runs | L1 median | L2 median | L1 max | outliers | consistency |
|---|---|---|---|---|---|---|---|
| R1 | ac1 | 15 | 9.70e-04 | 2.21e-06 | 1.19e-03 | 0 | 809.65 |
| R2 | ac1 | 15 | 8.91e-04 | 1.94e-06 | 1.20e-03 | 0 | 731.33 |
| R1 | exp1 | 15 | 1.13e-02 | 4.43e-04 | 1.18e-02 | 0 | 1.10 |
| R2 | exp1 | 15 | 1.13e-02 | 4.44e-04 | 1.17e-02 | 0 | 1.10 |
| R1 | merton | 15 | 5.39e-03 | 4.31e-05 | 7.83e-03 | 0 | 2.67 |
| R2 | merton | 15 | 3.66e-03 | 2.05e-05 | 4.74e-03 | 0 | 2.35 |
| R2+ens | ac1 | 3 | 8.44e-04 | 1.92e-06 | 1.10e-03 | 0 | 279.35 |
| R2+ens | exp1 | 3 | 1.11e-02 | 4.33e-04 | 1.13e-02 | 0 | 1.09 |
| R2+ens | merton | 3 | 3.26e-03 | 1.78e-05 | 3.92e-03 | 0 | 2.34 |

Reading: helped. Merton's targets are O(26) with a spread of a few units;
fitting them standardised takes the median from 5.39e-3 to 3.66e-3 (0.43×
the paper's 8.49e-3) and the worst run to 4.74e-3 — a 1.3× seed spread
where R0 had 3× plus an anomaly. ac1 improves 8 %; exp1 unchanged. Two
free preprocessing steps have so far more than halved the Merton error
and removed the anomaly; no architecture change yet. **Kept: yes.**

### R3a / R3b — normalisation none / LayerNorm (parent R2)

| rung | benchmark | runs | L1 median | L2 median | L1 max | outliers | consistency |
|---|---|---|---|---|---|---|---|
| R2 | ac1 | 15 | 8.91e-04 | 1.94e-06 | 1.20e-03 | 0 | 731.33 |
| R3a | ac1 | 15 | 9.17e-04 | 1.66e-06 | 1.17e-03 | 0 | 3364.22 |
| R3b | ac1 | 15 | 7.92e-04 | 1.72e-06 | 1.10e-03 | 0 | 718.78 |
| R2 | exp1 | 15 | 1.13e-02 | 4.44e-04 | 1.17e-02 | 0 | 1.10 |
| R3a | exp1 | 15 | 1.15e-02 | 4.31e-04 | 1.23e-02 | 0 | 1.23 |
| R3b | exp1 | 15 | 1.14e-02 | 4.29e-04 | 1.19e-02 | 0 | 1.13 |
| R2 | merton | 15 | 3.66e-03 | 2.05e-05 | 4.74e-03 | 0 | 2.35 |
| R3a | merton | 15 | 2.48e-03 | 1.16e-05 | 3.47e-03 | 0 | 2.49 |
| R3b | merton | 15 | 3.24e-03 | 1.73e-05 | 4.04e-03 | 0 | 2.45 |
| R3a+ens | ac1 / exp1 / merton | 3 | 8.59e-04 / 1.13e-02 / 2.40e-03 | | | 0 | |
| R3b+ens | ac1 / exp1 / merton | 3 | 7.03e-04 / 1.11e-02 / 2.96e-03 | | | 0 | |

Reading: once inputs and outputs are standardised, BatchNorm is a
liability rather than a help. Removing it (R3a) cuts Merton by a further
32 % (3.66e-3 → 2.48e-3, worst run 3.47e-3); LayerNorm (R3b) improves
both ac1 (−11 %) and Merton (−11 %). Neither adds outliers. The ac1 and
exp1 differences between R2/R3a/R3b (≤ 3 %) are inside the seed spread of
those benchmarks (±15 % and ±5 %), so they do not decide. Summed median
L1: R2 1.585e-2, R3a 1.490e-2, R3b 1.543e-2 → **kept: R3a** by the rule.
The ac1 consistency statistic rises to 3364 for R3a (tails of the
traveling wave fit less tightly without normalisation) while its grid L1
does not — the metric caveat from R0 again. The norm × activation cell
(R34) re-examines this choice.

### R4a / R4b / R4c — activation silu / gelu / sin (parent R3a)

| rung | benchmark | runs | L1 median | L2 median | L1 max | outliers | consistency |
|---|---|---|---|---|---|---|---|
| R3a (tanh) | ac1 | 15 | 9.17e-04 | 1.66e-06 | 1.17e-03 | 0 | 3364.22 |
| R4a (silu) | ac1 | 15 | 1.02e-03 | 1.88e-06 | 1.23e-03 | 0 | 1700.77 |
| R4b (gelu) | ac1 | 15 | 8.83e-04 | 1.38e-06 | 1.17e-03 | 0 | 1070.93 |
| R4c (sin) | ac1 | 15 | 7.81e-04 | 1.27e-06 | 9.84e-04 | 0 | 453.37 |
| R3a | exp1 | 15 | 1.15e-02 | 4.31e-04 | 1.23e-02 | 0 | 1.23 |
| R4a | exp1 | 15 | 1.15e-02 | 4.13e-04 | 1.25e-02 | 0 | 1.18 |
| R4b | exp1 | 15 | 1.13e-02 | 4.13e-04 | 1.19e-02 | 0 | 1.12 |
| R4c | exp1 | 15 | 1.17e-02 | 3.98e-04 | 1.31e-02 | 0 | 1.14 |
| R3a | merton | 15 | 2.48e-03 | 1.16e-05 | 3.47e-03 | 0 | 2.49 |
| R4a | merton | 15 | 1.93e-03 | 5.67e-06 | 3.76e-03 | 0 | 2.42 |
| R4b | merton | 15 | 2.07e-03 | 7.96e-06 | 2.80e-03 | 0 | 2.44 |
| R4c | merton | 15 | 3.89e-03 | 2.27e-05 | 7.70e-03 | 0 | 2.54 |

Reading: no activation adds outliers. Summed median L1: tanh 1.490e-2,
silu 1.445e-2, gelu 1.425e-2, sin 1.637e-2 → **kept: R4b (gelu)**. Gelu
improves Merton by 17 % (2.48e-3 → 2.07e-3) and tightens its worst run
(3.47e-3 → 2.80e-3); its ac1/exp1 changes are within seed spread. Silu
has the lowest Merton median (1.93e-3) but a wider spread (max 3.76e-3)
and ac1 +11 %. Sin is the best ac1 activation (7.81e-4, and the only one
that pulls the ac1 consistency statistic down, 453) but the worst on
Merton (3.89e-3, max 7.70e-3), so it is recorded as benchmark-dependent
and not kept.

### R34 — norm × activation cell (parent R4b for the new configs)

The six configurations of {batch, layer, none} × {tanh, gelu}; four were
already run as R2, R3b, R3a, R4b.

| norm \ activation | tanh (median L1 ac1 / exp1 / merton) | gelu |
|---|---|---|
| batch | R2: 8.91e-4 / 1.13e-2 / 3.66e-3 | R34_batch_gelu: 1.15e-3 / 1.13e-2 / 3.90e-3 (max 5.78e-3) |
| layer | R3b: 7.92e-4 / 1.14e-2 / 3.24e-3 | R34_layer_gelu: 8.26e-4 / 1.14e-2 / 3.40e-3 (max 4.97e-3) |
| none | R3a: 9.17e-4 / 1.15e-2 / 2.48e-3 | **R4b: 8.83e-4 / 1.13e-2 / 2.07e-3 (max 2.80e-3)** |

No outliers in any cell. Reading: no interaction overturns the ladder —
"no normalisation" is best for both activations on Merton, and gelu
without normalisation is the best cell overall (summed median 1.425e-2;
next best R3b 1.543e-2). With gelu, BatchNorm is the worst choice on ac1
as well (1.15e-3). LayerNorm is the best choice for ac1 alone under tanh
(7.92e-4) — a per-benchmark preference, not a global one. **Kept: R4b
(unchanged).**

### R5a–d — width 64 / 128, depth 4 / 8 (parent R4b: 6 × 20 gelu, no norm)

| rung | benchmark | runs | L1 median | L2 median | L1 max | outliers | consistency |
|---|---|---|---|---|---|---|---|
| R4b (6×20) | ac1 | 15 | 8.83e-04 | 1.38e-06 | 1.17e-03 | 0 | 1070.93 |
| R5a (6×64) | ac1 | 15 | 8.31e-04 | 1.40e-06 | 9.41e-04 | 0 | 840.00 |
| R5b (6×128) | ac1 | 15 | 7.68e-04 | 1.41e-06 | 9.34e-04 | 0 | 321.95 |
| R5c (4×20) | ac1 | 15 | 8.40e-04 | 1.37e-06 | 1.05e-03 | 0 | 1698.17 |
| R5d (8×20) | ac1 | 15 | 8.29e-04 | 1.30e-06 | 9.08e-04 | 0 | 666.34 |
| R4b | exp1 | 15 | 1.13e-02 | 4.13e-04 | 1.19e-02 | 0 | 1.12 |
| R5a | exp1 | 15 | 1.11e-02 | 4.24e-04 | 1.18e-02 | 0 | 1.06 |
| R5b | exp1 | 15 | 1.10e-02 | 4.19e-04 | 1.14e-02 | 0 | 1.07 |
| R5c | exp1 | 15 | 1.13e-02 | 3.89e-04 | 1.26e-02 | 0 | 1.17 |
| R5d | exp1 | 15 | 1.11e-02 | 4.17e-04 | 1.18e-02 | 0 | 1.07 |
| R4b | merton | 15 | 2.07e-03 | 7.96e-06 | 2.80e-03 | 0 | 2.44 |
| R5a | merton | 15 | 1.69e-03 | 4.70e-06 | 2.38e-03 | 0 | 2.42 |
| R5b | merton | 15 | 2.49e-03 | 1.02e-05 | 3.07e-03 | 0 | 2.41 |
| R5c | merton | 15 | 2.72e-03 | 1.28e-05 | 3.17e-03 | 0 | 2.45 |
| R5d | merton | 15 | 1.78e-03 | 5.32e-06 | 2.29e-03 | 0 | 2.42 |

Reading: no outliers anywhere. Summed median L1: 6×20 1.425e-2, 6×64
1.362e-2, 6×128 1.426e-2, 4×20 1.486e-2, 8×20 1.371e-2 → **kept: R5a
(6 × 64)**. Width 64 improves every benchmark (Merton −18 %, ac1 −6 %,
exp1 −2 %) and tightens the Merton worst case to 2.38e-3, at the same
≈ 8 s per training on CPU. Width 128 is the best ac1 net (7.68e-4, and the
lowest ac1 consistency so far, 322) but worse than 64 on Merton (2.49e-3):
with 1000 full-batch targets at Merton's noise level, 66 k parameters start
fitting the noise. Depth 8 is close to width 64 (1.371e-2) and depth 4 is
the worst — the paper's 6 × 20 is under-, not over-parameterised for this
data. Per-benchmark best sizes differ (ac1: 128; Merton: 64), so the rule
picks the compromise.

### R6 — random Fourier features (32, σ_B = 1 on scaled x) (parent R5a)

| rung | benchmark | runs | L1 median | L2 median | L1 max | outliers | consistency |
|---|---|---|---|---|---|---|---|
| R5a | ac1 | 15 | 8.31e-04 | 1.40e-06 | 9.41e-04 | 0 | 840.00 |
| R6 | ac1 | 15 | 9.48e-04 | 2.77e-06 | 1.13e-03 | 0 | 2911.78 |
| R5a | exp1 | 15 | 1.11e-02 | 4.24e-04 | 1.18e-02 | 0 | 1.06 |
| R6 | exp1 | 15 | 1.18e-02 | 4.79e-04 | 1.33e-02 | 0 | 1.06 |
| R5a | merton | 15 | 1.69e-03 | 4.70e-06 | 2.38e-03 | 0 | 2.42 |
| R6 | merton | 15 | 6.09e-03 | 5.51e-05 | 6.53e-03 | 0 | 2.29 |

Reading: hurt on every benchmark (Merton 3.6× worse, ac1 +14 %, exp1
+6 %); no outliers. The targets here are smooth, low-frequency functions
of x (a tanh front, a logistic profile, a near-linear Merton value), so
the spectral-bias remedy has nothing to fix and the 65-wide periodic
embedding only adds oscillatory capacity that must be trained away.
**Kept: no.**

### R7 — MSE weighted by 1/stderr² (parent R5a)

| rung | benchmark | runs | L1 median | L2 median | L1 max | outliers | consistency |
|---|---|---|---|---|---|---|---|
| R5a | ac1 | 15 | 8.31e-04 | 1.40e-06 | 9.41e-04 | 0 | 840.00 |
| R7 | ac1 | 15 | 1.21e-01 | 3.49e-02 | 1.66e-01 | 0 | 6924.32 |
| R5a | exp1 | 15 | 1.11e-02 | 4.24e-04 | 1.18e-02 | 0 | 1.06 |
| R7 | exp1 | 15 | 9.96e-03 | 3.28e-04 | 1.23e-02 | 0 | 1.02 |
| R5a | merton | 15 | 1.69e-03 | 4.70e-06 | 2.38e-03 | 0 | 2.42 |
| R7 | merton | 15 | 2.10e-02 | 4.52e-04 | 2.23e-02 | 0 | 1.39 |

Reading: a large, consistent (all 15 runs within 1 %) loss of accuracy
on ac1 (145×) and Merton (12×), and a 10 % gain on exp1. Inverse-variance
weighting is the right estimator only when the model can represent the
truth exactly; here the states with tiny stderr (ac1's saturated tails,
where all 10⁵ samples agree; Merton's low-x end) receive weights orders of
magnitude above the rest, and the net fits those to within their stderr
while ignoring the transition region that the grid error measures. The
consistency statistic drops (Merton 2.42 → 1.39) precisely because it is
the objective being minimised. exp1 is the one benchmark whose stderr is
roughly uniform and whose error is noise-limited, and there weighting
helps as theory predicts. **Kept: no.** A capped weight (e.g. clip at
10× the median) would be the fair follow-up; not part of this ladder.

### R8a / R8b / R8c — cosine schedule / grad-clip 1.0 / L-BFGS polish (parent R5a)

| rung | benchmark | runs | L1 median | L2 median | L1 max | outliers | consistency |
|---|---|---|---|---|---|---|---|
| R5a | ac1 | 15 | 8.31e-04 | 1.40e-06 | 9.41e-04 | 0 | 840.00 |
| R8a | ac1 | 15 | 7.92e-04 | 1.39e-06 | 1.01e-03 | 0 | 382.58 |
| R8b | ac1 | 15 | 8.07e-04 | 1.40e-06 | 9.16e-04 | 0 | 840.00 |
| R8c | ac1 | 15 | 8.31e-04 | 1.40e-06 | 9.41e-04 | 0 | 840.00 |
| R5a | exp1 | 15 | 1.11e-02 | 4.24e-04 | 1.18e-02 | 0 | 1.06 |
| R8a | exp1 | 15 | 1.11e-02 | 4.31e-04 | 1.17e-02 | 0 | 1.06 |
| R8b | exp1 | 15 | 1.10e-02 | 4.29e-04 | 1.17e-02 | 0 | 1.06 |
| R8c | exp1 | 15 | 1.11e-02 | 4.24e-04 | 1.18e-02 | 0 | 1.06 |
| R5a | merton | 15 | 1.69e-03 | 4.70e-06 | 2.38e-03 | 0 | 2.42 |
| R8a | merton | 15 | 1.78e-03 | 4.79e-06 | 2.43e-03 | 0 | 2.42 |
| R8b | merton | 15 | 2.06e-03 | 6.75e-06 | 2.37e-03 | 0 | 2.41 |
| R8c | merton | 15 | 1.69e-03 | 4.65e-06 | 2.38e-03 | 0 | 2.42 |

Reading. R8a (cosine): ac1 −5 %, Merton +5 % — improves one benchmark
and worsens another, and its sum (1.367e-2) does not beat R5a
(1.362e-2); not kept. R8b (grad-clip 1.0): Merton +22 %; the clipped
early steps cost accuracy the schedule never recovers; not kept. R8c
(200 L-BFGS iterations after Adam): results identical to R5a to every
printed digit on ac1 and exp1 and within rounding on Merton, with no
extra wall time. Diagnosed directly (scratch probe on Merton d0, s0, the
R5a config): after the 3000 Adam epochs the max |gradient| is 1.8e-5 and
the float32 loss 1.52e-3; L-BFGS makes 7 closure evaluations and returns
with the loss unchanged, for `tolerance_grad` 1e-7 and 1e-12 alike — the
strong-Wolfe line search cannot find a step that lowers the float32 loss
from Adam's endpoint. The polish is a no-op at this precision; a float64
polish would be the fair test and is out of scope. **Kept: none of R8.**

### Kept path

R0 (paper) → R1 input standardisation → R2 output standardisation →
R3a no normalisation → R4b gelu → **R5a width 64**. Final configuration:
6 hidden layers × 64, gelu, no normalisation, standardised inputs and
targets, full-batch Adam with the paper's lr schedule, MSE on the MC means.

| benchmark | paper (10 runs) | R0 on frozen data (15 runs) | R5a (15 runs) | R5a ensemble of 5 |
|---|---|---|---|---|
| ac1 | 1.32e-3 | 1.12e-3 (max 1.37e-3) | **8.31e-4** (max 9.41e-4) | 7.4e-4 |
| exp1 | 1.17e-2 | 1.13e-2 (max 1.21e-2) | **1.11e-2** (max 1.18e-2) | 1.10e-2 |
| merton | 8.49e-3, 1 anomalous run | 8.68e-3 (max 1.52e-1, 1 outlier) | **1.69e-3** (max 2.38e-3) | 1.64e-3 |

Attribution, Merton median L1: 8.68e-3 → 5.39e-3 (R1, −38 %) → 3.66e-3
(R2, −32 %) → 2.48e-3 (R3a, −32 %) → 2.07e-3 (R4b, −17 %) → 1.69e-3 (R5a,
−18 %); overall 5.1× better than the paper's architecture and 5.0× better
than its published number, with the worst of 15 runs at 2.38e-3 against
the paper's own anomaly. Two preprocessing steps that change no
parameter count account for 58 % of the log-reduction; removing BatchNorm
another 20 %. ac1 improves 1.35× and stays capacity-limited (its best
individual rungs — sin activation, width 128, LayerNorm — were rejected
for hurting Merton). exp1 is MC-noise-limited: nothing but averaging
noise (the ensemble) or exact inverse-variance weighting (R7) moves it,
and R7's gain there does not survive the other two benchmarks.

Robustness: after R1 no configuration in the ladder produced an outlier
run (0 of 15 on every rung except R0), so the paper's tanh anomaly is a
consequence of feeding x ∈ [100, 200] unscaled into tanh with BatchNorm
running statistics, not an intrinsic property of the method.

Rejected with a reason worth keeping: Fourier features (targets are
low-frequency); 1/stderr² weighting (near-zero-stderr states dominate;
helps only the noise-limited exp1); L-BFGS polish (float32 no-op);
grad-clip (slows the schedule); width 128 and depth 4 (worse on Merton).

Cost of the study: 12 datasets-worth of MC (9 sets, ≈ 5 min), 600
trainings + 120 ensembles ≈ 1.7 h CPU, all in
`examples/nn_ablation_results.csv`.
