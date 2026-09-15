# General training corpus and set-to-field denoiser (Stage 0 + D04 go/no-go)

Status: approved in chat on 2026-09-15 ("可以开始做了"). Branch:
`research/nn-architecture` (continues the ablation branch; the ablation's
single-PDE datasets are the one-instance special case of the corpus).
Research plan this implements:
`docs/research/runs/2026-09-15-nn-backbones/02-plan.md`, Stage 0 and the
Stage 1 go/no-go.

## Goal

Make the trained network **general across problems** instead of one
network per PDE instance. Concretely:

1. **Stage 0 — corpus.** A generator that produces many PDE *instances*
   (same nonlinearity family, different parameters) with the sampler's
   noisy point estimates, so that a single model can be trained on all of
   them at once. Each instance carries its identity (the parameters) so a
   model can tell instances apart.
2. **D04 go/no-go.** A set-to-field denoiser: a transformer that reads an
   instance's *set* of noisy estimates and answers queries \(u(t,x)\),
   trained across instances with Noise2Noise targets. Decide in one
   experiment whether attention over the set learns anything a
   per-instance MLP does not.

The φ-family (terminal-condition) interface of D03 and the box sampler
for \(d>1\) are **not** in this spec; they get their own once D04's
answer is known.

## Non-goals

- Changing the sampler, mechanism, rate or outlier filter.
- Beating the paper on its own benchmarks (done on this branch already).
- A large pretraining corpus (Stage 4); this spec's corpora are ≤ 1000
  instances.
- Using `stderr` as loss weights (rejected in the ablation, R7).

## Families (Stage 0)

An **instance** = (family, params, seed). Two families now, both with
closed-form solutions so the go/no-go has an exact referee:

| Family key | Factory | Params \(\theta\) | Ranges (uniform) | Segment | Exact |
|---|---|---|---|---|---|
| `ac1` | `library.allen_cahn_nd(d=1, T, shift)` — **new `shift` argument**, default 0: \(u = -\tfrac12 - \tfrac12\tanh(\tfrac34(T-t) - (\tfrac{x}{2} - \text{shift}))\), i.e. the wave translated; \(\phi\) written in the logistic form with the same shift | \((T, \text{shift})\) | \(T \in [0.1, 0.5]\), shift \(\in [-3, 3]\) | \([-8, 8]\) | yes |
| `merton` | `library.merton_hjb(T, mu, sigma, gamma, rho)` (all existing arguments) | \((\gamma, \mu, \sigma)\); \(T=0.1, \rho=0.01\) fixed | \(\gamma \in [0.3, 0.8]\), \(\mu \in [0.02, 0.06]\), \(\sigma \in [0.08, 0.2]\) | \([100, 200]\) | yes |

Per instance: \(N\) states \(X_i\) uniform on the 10 %-overtrained segment,
\(\tau \equiv 0\) (the paper's protocol, kept for comparability), \(M\)
trees per state, jcp rate. **Two independent draws** at the *same*
states: draw 0 is the model input, draw 1 is the Noise2Noise target.
Exact \(u\) at the states and on the 101-point grid is stored for
evaluation (never as training input).

## Architecture

### 1. `parabolab/deep/generator.py` — one backwards-compatible hook

`generate_training_data(..., states: Optional[tuple[np.ndarray, np.ndarray]] = None)`.
When given `(ts, xs)`, the state draw is skipped and those states are
used; the tree seeds still derive from `seed`. Default path unchanged
(regression-guarded by the existing tests and `test_default_training_is_unchanged`).

### 2. `parabolab/library.py` — `allen_cahn_nd(d, T=0.5, shift=0.0)`

`shift=0.0` reproduces the current function exactly (name string
unchanged when shift is 0, so nothing downstream changes).

### 3. `parabolab/deep/corpus.py` — instances and corpora

- `FAMILIES: dict[str, Family]` with `Family(key, param_names, ranges,
  x_lo, x_hi, make_factory(params) -> functools.partial)`.
- `InstanceSpec(family, params: tuple[float, ...], n_states, m_samples,
  seed, n_draws=2)` frozen dataclass, `to_json()`.
- `sample_instances(family, n, seed) -> list[InstanceSpec]` (params
  uniform in the family's ranges, deterministic in `seed`).
- `Instance` dataclass: `spec`, `t (N,)`, `x (N,d)`, `y (n_draws, N)`,
  `stderr (n_draws, N)`, `u_exact (N,)`, `grid (101,)`, `u_grid (101,)`.
- `generate_instance(spec, executor=None) -> Instance`: draws states with
  `rng(seed)`, calls `generate_training_data` once per draw with
  `states=` and `seed = 1000*seed + draw`, evaluates the exact solution.
- `load_or_generate_corpus(family, specs, root, n_jobs) -> list[Instance]`:
  one `.npz` per instance under `<root>/<family>/<seed>.npz` with the
  spec as metadata (same refusal-on-mismatch and corrupt-file behaviour
  as `datasets.py`); shares one `ProcessPoolExecutor` across instances
  (gotcha 22).
- `Corpus` = list of `Instance` plus `collate(instances, n_context,
  n_query, rng) -> batch tensors` for training (see §5).

### 4. `parabolab/deep/setnet.py` — the set-to-field denoiser

`SetDenoiser(d, n_params, d_model=128, n_heads=4, n_layers=4, dropout=0.0)`:

- **Per-instance scaling inside the model** (the ablation's decisive
  lesson): from the context set compute \(\mu_y, s_y\) (mean/std of the
  context `y`) and \(\mu_x, s_x\) (per coordinate of \((t,x)\)); tokens
  use \(((t,x)-\mu_x)/s_x\), \((y-\mu_y)/s_y\), \(\text{stderr}/s_y\);
  the output is un-scaled with \(\mu_y, s_y\). Params \(\theta\) are
  standardised with fixed constants from the family ranges and
  broadcast into every token.
- Context encoder: `Linear(d+1+2+n_params → d_model)` → gelu →
  `nn.TransformerEncoder` (`n_layers`, `n_heads`, feed-forward `4·d_model`,
  pre-norm, batch_first).
- Query decoder: `Linear(d+1+n_params → d_model)` → gelu → one
  `nn.MultiheadAttention` (query attends to encoded context) → residual →
  MLP(`d_model → d_model → 1`).
- Forward signature: `net(ctx_tx (B,N,d+1), ctx_y (B,N), ctx_se (B,N),
  params (B,n_params), q_tx (B,Q,d+1)) -> (B,Q)`.
- ≈ 0.8 M parameters at the defaults; fits comfortably on the 8 GB GPU
  with \(B=16\), \(N=500\), \(Q=101\).

### 5. `parabolab/deep/settrain.py` — training and evaluation

- `train_set_denoiser(net, corpus, *, epochs, lr=3e-4, batch_instances=16,
  n_context=500, n_query=128, target="n2n"|"exact", device, seed,
  log_every) -> SetTrainResult`.
  Each step samples `batch_instances` instances; context = draw-0 rows at
  `n_context` random states; queries = `n_query` random states of the
  same instance with target draw-1 `y` (`"n2n"`) or `u_exact`
  (`"exact"`). AdamW, cosine schedule, grad-clip 1.0 (a transformer, not
  the ablation MLP — its optimiser choices do not carry over; recorded as
  such). Loss = MSE in the *scaled* output space.
- `evaluate_set_denoiser(net, instances, *, n_context, device) ->
  np.ndarray of L1` on each instance's 101-point grid vs `u_grid`,
  context = all draw-0 rows of the instance (capped at `n_context`).
- Baselines (same held-out instances, same grid):
  (a) `per_instance_mlp_l1(instance, draw, m_scale, …)` — the ablation's
  R5a net (`NetConfig(neurons=64, activation="gelu", norm="none",
  scale_input=True, scale_output=True)`, `TrainConfig()` defaults)
  trained on the instance's draw-0 `y`; a second variant on labels
  generated at \(10M\) (a separate `.npz` with `m_samples=10·M`);
  (b) `kernel_smoother_l1(instance)` — Nadaraya–Watson with a Gaussian
  kernel, bandwidth by leave-one-out on the context (the "is attention
  more than smoothing" control).

### 6. `examples/set_denoiser_gonogo.py` — the experiment

```
python examples/set_denoiser_gonogo.py --family ac1 --n-train 500 --n-test 50 \
    --n-states 500 --m-samples 1000 --epochs 20000 --device cuda \
    --corpus-root examples/nn_corpus --out examples/set_denoiser_gonogo.csv
```

Steps: generate/load the corpus (train + test instances, and the test
instances again at \(10M\)); train D04 with `n2n` targets and, as an
upper bound, with `exact` targets; evaluate on the 50 held-out instances;
run baselines (a) at \(M\) and \(10M\), (b); write one CSV row per
(method, instance) with L1 and cost; print the summary table (median,
max L1 per method). `if __name__ == "__main__"` guard.

**Go/no-go rule (written before running):** D04-n2n's median held-out L1
must be **below** baseline (a)-at-\(M\). Pass → Stage 1 full protocol
(Family B, budget curves, \(d=5\)). Fail → D04 stops; the plan falls back
to D03/D02.

## Compute and data budget

Family `ac1`, 550 instances × 500 states × 1000 trees × 2 draws
≈ 5.5·10⁸ trees ≈ 15 min on 16 workers; the \(10M\) test set adds
50 × 500 × 10⁴ ≈ 2.5·10⁸ ≈ 7 min. Corpus on disk ≈ 550 × 20 kB. Training
20 000 steps × 16 instances × 500 tokens on the 4060: minutes. CUDA torch
wheel required (one-line env change; gotcha 36 unaffected because numpy
stays the pip build).

## Error handling

- Instance generation failures (non-finite `y` at a state) are kept as
  NaN rows; `collate` masks them out of context and query sets; an
  instance with < 50 finite rows is excluded and logged.
- `load_or_generate_corpus` refuses a spec mismatch (ValueError) and
  regenerates unreadable files, as `datasets.py`.
- Training divergence (non-finite loss) aborts with the step number;
  evaluation records `inf` L1 for a net with non-finite outputs.

## Testing (`tests/test_deep_corpus.py`, `tests/test_deep_setnet.py`; fast, tiny sizes)

- `allen_cahn_nd(shift=0)` byte-identical name and `exact_solution` to the
  old call; `shift≠0` satisfies \(u(T,x) = \phi(x)\) and the translation
  identity \(u_{\text{shift}}(t, x) = u_0(t, x - 2\,\text{shift})\).
- `generate_training_data(states=…)` reproduces the default draw's
  `y` when given the states the default path would have drawn with the
  same seed; different `seed` with the same states gives different `y`,
  same `x`.
- `sample_instances` deterministic; params inside ranges; `InstanceSpec`
  JSON round-trip; corpus `.npz` round-trip bit-identical; mismatch
  refused.
- `SetDenoiser`: output shape `(B,Q)`; finite; **permutation invariance**
  of the context (shuffling context rows changes the output by < 1e-5);
  **scale equivariance**: multiplying context `y` and `stderr` by 7 and
  adding 3 multiplies the output by 7 and adds 3 (up to 1e-4).
- `train_set_denoiser` on a 4-instance toy corpus for 30 steps: loss
  finite and decreasing; `evaluate_set_denoiser` returns one finite L1
  per instance; `kernel_smoother_l1` on a noiseless instance is < 1e-3.
- `collate` masks NaN rows.
- Driver smoke test via `--tiny` (4 train, 2 test instances, 8 states,
  4 trees, 5 epochs) writes the CSV with all five method rows.

## Deliverables

1. Code units 1–6 with tests; the CUDA wheel installed and a
   `device="cuda"` smoke test.
2. `examples/set_denoiser_gonogo.csv` and a `## Results` section appended
   to this spec with the summary table and the go/no-go verdict.
3. CLAUDE.md gotchas for anything non-obvious (e.g. N2N vs exact-target
   gap, attention vs smoother).
