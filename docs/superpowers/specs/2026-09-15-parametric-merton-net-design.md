# Parameter-conditioned network for the Merton family (D02)

Status: approved in chat on 2026-09-15 ("对 theta 或者对 phi 去预测能开始做了").
Branch: `research/nn-architecture`. Plan: `docs/research/runs/2026-09-15-nn-backbones/02-plan.md`
Stage 3, brought forward because Stage 1 (D04) tied and stopped.

## Goal

One network for a whole family of Merton problems: input \((t, x, \theta)\),
\(\theta = (\gamma, \mu, \sigma)\), output \(u(t, x; \theta)\), with the
optimal portfolio fraction obtained from the network's own derivatives,

\[
\pi^*(t,x;\theta) = -\frac{\mu}{\sigma^2}\,\frac{u_x}{x\,u_{xx}},
\]

which for the Merton HJB in `library.merton_hjb` (zero interest rate) is
the constant \(\mu/(\gamma\sigma^2)\) — the classical Merton fraction, a
closed-form referee for the policy. Questions, in order:

1. Does conditioning on \(\theta\) reach per-instance accuracy on held-out
   \(\theta\)? Which conditioning — concatenation or FiLM — does better?
2. Are autograd derivatives of a \(u\)-trained net good enough for the
   policy (≤ 2 % relative error), and do derivative labels
   (`DxN` roots, D07) fix it if not?

## Non-goals

- The Vasicek (stochastic-rate) family — next slice, once the constant-rate
  family works.
- Any change to the sampler or corpus format beyond an optional root code
  per draw.
- Operator learning over \(\phi\) (D03) — separate spec.

## Data

Corpus family `merton` (exists: \(\gamma\in[0.3,0.8]\), \(\mu\in[0.02,0.06]\),
\(\sigma\in[0.08,0.2]\), \(T=0.1\), \(\rho=0.01\), segment \([100,200]\)),
500 train / 50 held-out instances, 500 states, \(M=1000\), seeds as
`sample_instances(..., seed=0)` / `seed=1`. Per-instance MLP baseline at
the same \(M\) on the held-out instances.

**Derivative labels.** `InstanceSpec` gains `deriv_codes: tuple[str, ...] = ()`;
each entry names a root code (`"Dx1"` → `DxN((1,))`, `"Dx2"` → `DxN((2,))`).
`Instance` gains three optional arrays, `None` when `deriv_codes` is empty:
`deriv (n_codes, N)` (one draw per code, seed `1000·seed + 100 + k`),
`deriv_stderr (n_codes, N)`, `deriv_exact (n_codes, N)`. `y`, `stderr`,
`u_exact` keep their shapes, so every existing file, test and consumer is
untouched; a derivative corpus lives under its own root (`<root>/deriv`)
because `instance_path` keys on family and seed only. Exact derivatives
come from a family hook `Family.deriv_factory_name` naming a library
function that returns `(u_x, u_xx)` callables; for Merton
(`deep.families.merton_hjb_derivatives`) by hand from the closed form:
\(u = x^{1-\gamma} g(t)\), \(u_x = (1-\gamma)x^{-\gamma} g\),
\(u_{xx} = -\gamma(1-\gamma)x^{-\gamma-1} g\).

## Model

`ConditionedNet(d, n_params, mode)` in `parabolab/deep/condnet.py`, built
on the ablation's R5A trunk (6 hidden layers × 64, gelu, no norm, scaled
input/output buffers, `fit_scalers` fits them from the pooled corpus):

- `mode="concat"`: input `[t, x, θ_scaled]` → trunk → 1.
- `mode="film"`: input `[t, x]` → trunk whose every hidden layer output
  \(h\) is replaced by \(h \odot (1+\alpha_\ell(\theta)) + \beta_\ell(\theta)\),
  with \((\alpha_\ell, \beta_\ell)\) from a 2-layer MLP on \(\theta_{scaled}\).
- \(\theta\) scaled by the family's fixed midpoint/half-range constants
  (buffers), as in `SetDenoiser`.
- Derivatives \(u_x, u_{xx}\) at \((t,x,\theta)\) by `torch.autograd`
  (`create_graph=True` so they can enter the loss).

## Training (`parabolab/deep/condtrain.py`)

`train_conditioned(net, instances, *, steps, batch_states=4096, lr=1e-3,
schedule cosine, weight_decay=0, loss_weights=(1.0, w1, w2), device, seed)`:
each step samples `batch_states` (instance, state) pairs uniformly from the
pooled corpus (all instances' finite rows), loss = MSE on scaled \(u\)
labels + \(w_1\)·MSE on scaled \(u_x\) + \(w_2\)·MSE on scaled \(u_{xx}\)
(each derivative label scaled by its own pooled std); \(w_1=w_2=0\) for the
\(u\)-only rungs. Full-batch is not possible (250 000 rows), so this is
mini-batch Adam with cosine decay.

Evaluation (`evaluate_conditioned(net, instances, device)`): per held-out
instance, grid L1 on \(u\) (the usual 101 points) and the relative policy
error \(\text{median}_x |\hat\pi^*(0,x) - \pi^*|/\pi^*\) over the interior
grid points \(x \in [110, 190]\) (the boundary is where autograd of a fitted
net is worst and the paper's grid includes it; report both).

## Rungs (single-knob, one commit each)

| Rung | Change | Question |
|---|---|---|
| C0 | per-instance R5A at \(M\) on the 50 held-out θ (baseline; from `settrain.per_instance_mlp_l1`) + its autograd policy error | what per-instance nets give |
| C1 | `concat`, \(u\) labels only | conditioning works? |
| C2 | `film`, \(u\) labels only | better conditioning? |
| C3 | best of C1/C2 + derivative labels, \(w_1=w_2=1\) (D07) | do derivative labels fix the policy? |

Kept-rung rule: lower held-out \(u\)-L1 median, then lower policy error;
report both always.

**Success / failure** (fixed before running): C1 or C2 held-out \(u\)-L1
median within 1.5× of C0's; policy relative error ≤ 2 % for the kept rung
(with or without C3). Either failing is recorded as such; a policy error
> 2 % after C3 means autograd policies from MC-trained nets are not
reliable at this budget, which is itself the finding.

## Driver

`examples/parametric_merton.py --rungs C0 C1 C2 C3 --steps 20000 --device cuda
--jobs 16 --corpus-root examples/nn_corpus --out examples/parametric_merton.csv`
(`--tiny` for tests). CSV: `rung, instance_seed, l1_u, policy_err_interior,
policy_err_full, seconds`. `if __name__ == "__main__"`. Un-ignore the CSV.

## Testing (fast)

- Corpus: `deriv_codes=("Dx1","Dx2")` instance has `deriv.shape == (2, N)`,
  `deriv_exact` matches central finite differences of the closed-form
  \(u\) to 1e-4 relative, and the MC derivative labels agree with
  `deriv_exact` within 4 stderr on every state; default `deriv_codes=()`
  keeps `test_deep_corpus.py` green and the cache round-trip bit-identical.
- `ConditionedNet`: shapes, both modes; `film` with zero-initialised
  FiLM head equals the plain trunk at init; autograd `u_x, u_xx` finite and
  match finite differences on a randomly initialised net to 1e-3.
- Training: 30 steps on a 4-instance toy corpus decreases the loss;
  evaluation returns finite metrics; the exact Merton policy of the
  closed form equals \(\mu/(\gamma\sigma^2)\) (unit test of the referee).
- Driver `--tiny` writes all four rungs' rows.

## Deliverables

Code + tests; `examples/parametric_merton.csv`; `## Results` section here
with the C0–C3 table, the kept rung, the success/failure verdict, and one
paragraph per rung; gotchas if any.

## Results

Corpus: 500 train / 50 held-out θ (γ, μ, σ uniform in the ranges), 500
states, M = 1000, one draw (≈ 5 min to generate on 16 workers); C3's
derivative corpus adds `Dx1`/`Dx2` roots for the 500 training instances
(≈ 10 min). Training: 20 000 steps × 4096 pooled (instance, state) rows,
Adam 1e-3 cosine, RTX 4060; C1 21 k params, C2/C3 71 k params. All rows
in `examples/parametric_merton.csv` (200 rows). `seconds` is per-instance
wall-clock for C0 and training time amortised over the 50 test instances
for C1–C3.

| rung | n | u-L1 median | u-L1 max | policy err interior (median) | policy err full | s/instance |
|---|---|---|---|---|---|---|
| C0 per-instance R5A, M = 1000 | 50 | 2.01e-02 | 9.04e-02 | 54.43 % | 61.63 % | 4.3 |
| C1 concat, u only | 50 | 8.69e-03 | 2.58e-02 | 5.06 % | 5.65 % | 0.7 |
| **C2 FiLM, u only** | 50 | **4.12e-03** | 1.81e-02 | **3.03 %** | 3.26 % | 1.3 |
| C3 FiLM + derivative labels (1,1,1) | 50 | 2.57e-02 | 1.18e-01 | 3.63 % | 3.69 % | 3.4 |

**Kept rung: C2.** Verdict against the fixed criteria: the accuracy
criterion **passes** by a wide margin (C2's u-L1 is 0.20× C0's, not
merely within 1.5×); the policy criterion **fails** (3.03 % > 2 %) with
or without C3.

C0 — per-instance nets at M = 1000. With 3× the label noise of the
ablation's M = 10⁴ setting (median stderr 0.052 on |u| ≈ 22), a net fitted
to one instance's 500 points reaches only 2.0e-2 and its autograd
derivatives are useless for the policy: median error 54 %, p90 97 %. A
fitted curve's second derivative is not something 500 noisy points
determine.

C1 vs C2 — conditioning works and FiLM is better. C1 (θ concatenated to
the input) beats C0 on u by 2.3×; C2 (FiLM: θ modulates every hidden
layer) by 4.9×, and beats C0 on all 50 held-out θ and C1 on 41 of 50.
Pooling 250 000 noisy points across θ lets the net average noise that no
single instance can (u-L1 4.1e-3 is 13× below the per-state stderr). The
policy from C2's autograd derivatives is at 3.0 % median (p90 8.9 %; 40 of
50 instances above 2 %): usable, not yet at the target.

C3 — derivative labels hurt, and the reason is a finding (corrected after
review: the first write-up blamed miscalibrated stderr; the corpus says
otherwise). Over the 500-instance derivative corpus (250 000 rows) the
per-state standard errors of the `DxN`-rooted labels are *calibrated*:
z = (label − exact)/stderr has RMS 1.03 (u_x) and 1.00 (u_xx), |z| p99 =
2.4 / 2.1, max 6.0 / 4.4. What breaks C3 is heteroscedasticity: the
stderr of u_x ranges from 1.2e-3 (median) to 0.12 (p99) and 0.97 (max),
and the 1 % of states with the largest stderr carry 77 % (u_x) / 73 %
(u_xx) of the total squared label error. Relative to the spread of the
true values (u_x std 6.1e-2, u_xx std 1.6e-4) the RMS label errors are
2.7e-2 and 1.8e-3 — so u_xx's labels are on average 11× noisier than the
signal they carry, u_x's about half as noisy. Scaling each derivative
term by its pooled std and weighting it 1 therefore lets a few hundred
states of near-pure noise dominate the loss; u itself degrades 6×
(2.57e-2) and the policy does not improve (3.6 %; better than C2 on
24/50). The right follow-up is the opposite of gotcha 40's lesson for
u: because the derivative stderrs *are* calibrated, 1/stderr² weighting
of the derivative terms (or dropping the top-stderr states) is justified
here — a new rung, not part of this ladder.

The label whose stderr is *not* calibrated in this corpus is u: RMS z =
4.57, |z| p99 = 19.7, max 79 — the tail-missing signature of gotchas
15/20 on the Id-rooted Merton trees at M = 1000. Pooling 250 000 such
rows still let C2 average through it (u-L1 4.1e-3); a per-instance net
cannot.

Commands that produced the table (two invocations, C3's mode chosen
after C1/C2):
`python examples/parametric_merton.py --rungs C0 C1 C2 --steps 20000 --device cuda --jobs 16`
then `python examples/parametric_merton.py --rungs C3 --c3-mode film --steps 20000 --device cuda --jobs 16`.
The `mlp_10M` baseline of the D04 experiment shares its first 1000 tree
draws per state with the M = 1000 labels (same instance seed); no
conclusion depends on their independence.

Cost: corpus ≈ 15 min; C0 3.6 min; C1/C2/C3 ≈ 0.6 / 1.1 / 2.8 min of GPU
training each.

### C4 / C5 — inverse-variance-weighted derivative labels (follow-up, plan Task 6)

Same corpus and FiLM net as C3; the derivative loss terms now carry
per-state weights \(1/\max(\text{stderr}_i, \epsilon)^2\) (normalised to
mean 1, \(\epsilon = 10^{-3}\cdot\)median), justified by the calibration
finding above. C4 uses \(u_x\) and \(u_{xx}\) labels, C5 \(u_x\) only.
Commands: `--rungs C4 C5 --c3-mode film --steps 20000 --device cuda --jobs 16`.

| rung | n | u-L1 median | u-L1 max | policy err interior (median / p90 / max) | policy err full | s/instance |
|---|---|---|---|---|---|---|
| C2 FiLM, u only | 50 | 4.12e-03 | 1.81e-02 | 3.03 % / 8.86 % / 15.1 % | 3.26 % | 1.3 |
| C3 + derivatives, unit weights | 50 | 2.57e-02 | 1.18e-01 | 3.63 % | 3.69 % | 3.4 |
| **C4 + derivatives, 1/stderr² weights** | 50 | 7.65e-03 | 3.17e-02 | **0.19 % / 0.30 % / 0.53 %** | 0.21 % | 3.5 |
| C5 + u_x only, 1/stderr² weights | 50 | 6.40e-03 | 2.19e-02 | 0.38 % / 0.64 % / 0.77 % | 0.40 % | 2.7 |

Reading. Weighting the derivative terms by their (calibrated) inverse
variance turns C3's failure into the best policy net of the study: C4's
Merton fraction is within 0.19 % of the closed form at the median and
within 0.53 % on the *worst* of 50 held-out θ (C2: 15 %), beating C2 on
all 50 instances. The price is on \(u\): 7.65e-3 vs C2's 4.12e-3 (C4 is
better on only 9/50) — the derivative terms pull capacity toward the
shape of \(u\) rather than its level, and the \(u_{xx}\) labels are still
11× noisier than their signal on average. C5 (drop \(u_{xx}\)) recovers
some \(u\) accuracy (6.40e-3) at 2× the policy error of C4 (0.38 %, still
far inside the 2 % target); C4 beats C5 on policy on 48/50.

Verdicts against the fixed criteria: C4 and C5 both satisfy *both*
(u-L1 ≤ 1.5× C0 = 3.0e-2; policy ≤ 2 %). The kept-rung rule as written
(lowest u-L1 first) still selects C2, which fails the policy criterion —
the rule did not anticipate a u/policy trade-off, and that trade-off is
the finding: **a value-function net and a policy net want different
losses.** For value estimation keep C2; for policies use C4. A rung that
serves both — larger net, or a two-headed net trained with C4's loss —
is the natural next step and is not run here.
