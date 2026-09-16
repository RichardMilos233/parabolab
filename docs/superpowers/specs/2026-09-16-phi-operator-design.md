# Terminal-condition operator learning on coding-tree labels (D03)

Status: approved in chat on 2026-09-16 ("继续做 A 跟 B"). Branch
`research/nn-architecture`. Research plan:
`docs/research/runs/2026-09-15-nn-backbones/02-plan.md`, Stage 2.

## Goal

Learn the map \(\phi \mapsto u(t,\cdot)\) for a fixed PDE from
coding-tree labels, so that a new terminal condition costs a forward pass
instead of a Monte Carlo run — and compare three operator backbones on
identical data, which is the "换 backbone" experiment the pointwise
interface could not host.

Questions, in order:

1. Can an operator trained on branching-MC labels reach the accuracy of a
   per-φ network (the D02 result, now over φ instead of θ)?
2. Which backbone — DeepONet, FNO-1D, or a cross-attention operator — does
   it best, and how does each scale with the number of training φ?

## Non-goals

- Fully nonlinear examples with derivative codes (tan / cosine / log): a
  third step after the two here; their reference solution would be
  high-M MC and their φ-family needs bounded higher derivatives.
- \(d > 1\), time-dependent evaluation (\(t \ne 0\) queries), Sobolev
  labels.
- Pretraining across nonlinearities (D10).

## Data: two φ-families, one PDE each

φ is a random Fourier series on the segment \([-8, 8]\), \(\omega = \pi/8\):

\[
\phi(x) = A\sum_{k=1}^{K}\big(a_k\cos(k\omega x) + b_k\sin(k\omega x)\big),
\qquad a_k, b_k \sim N\!\big(0, (1+k)^{-2}\big),\; K = 4,
\]

with \(A\) chosen per instance so that \(\max|\phi| = 0.9\) (Allen–Cahn's
stable range). The instance's identity is its 8 coefficients (plus \(A\)),
stored as `params`; the instance also stores `phi_grid` = φ on the
101-point evaluation grid (the operator input).

| Family key | PDE | \(T\) | Reference \(u(0,\cdot)\) on the grid |
|---|---|---|---|
| `heat_phi` | \(\partial_t u + \tfrac12 u_{xx} = 0\) (`f ≡ 0`) | 0.3 | closed form: each mode damped by \(e^{-k^2\omega^2 T/2}\) |
| `ac_phi` | Allen–Cahn \(f(u) = u - u^3\) | 0.3 | 1-D finite differences (explicit Euler, \(\Delta x = 0.02\), \(\Delta t = 0.4\,\Delta x^2\), zero-flux boundary on \([-12, 12]\)), validated against the traveling-wave closed form to \(< 10^{-4}\) |

`heat_phi` isolates label noise and φ-family design from any nonlinear
question (Step 1 of the research plan); `ac_phi` is the real target
(Step 2). Corpus per family: 1000 train φ (seed 0), 50 held-out φ
(seed 1), 500 states, \(M = 1000\), one draw. For the learning curve the
operators are also trained on the first 250 and 500 of the 1000.

Sampler: only φ itself is evaluated at leaves for these semilinear
problems (no derivative codes), so any φ with a sympy expression works;
the Fourier series differentiates in milliseconds if ever needed.

## Corpus changes (`parabolab/deep/corpus.py`)

- `Family` gains `param_sampler: Optional[str] = None` — `None` = uniform in
  `ranges` (current), `"fourier"` = the Gaussian-decay coefficients above
  with the amplitude normalisation; and `reference_name: Optional[str] =
  None` — a `library` function `(pde, grid) -> u_grid` used when
  `pde.exact_solution is None`.
- `Instance` gains `phi_grid: Optional[np.ndarray]` (101,), filled for
  every instance from `pde.phi_mu((0,))` (cheap; `None` only for files
  written before the field existed — loader tolerant as for `deriv`).
- `library.heat_fourier_1d(T, coeffs)`, `library.allen_cahn_fourier_1d(T,
  coeffs)` (`coeffs` = `(A, a_1..a_K, b_1..b_K)`), and
  `library.fd_reference_1d(pde, grid, *, dx=0.02, x_pad=4.0) -> u_grid`
  (explicit FD for `f_expr` a function of `u` only; raises otherwise).
- `sample_instances` uses `Family.param_sampler`.

## Backbones (`parabolab/deep/opnet.py`)

All take `phi_grid (B, 101)` and queries `q_tx (B, Q, 2)` and return
`(B, Q)`; all standardise φ by a fixed corpus-level scale (buffer) and the
output by the pooled label mean/std (buffers, fitted by the trainer as in
`condtrain`). ≈ 0.2–1 M parameters each.

1. **`DeepONet`**: branch MLP `101 → 128 → 128 → p` (gelu), trunk MLP
   `2 → 128 → 128 → p` (gelu), output \(\sum_k b_k t_k + c\); `p = 64`.
2. **`FNO1d`**: input channels `[φ(x_j), x_j/8]` on the 101-point grid →
   lift to width 32 → 4 spectral-convolution layers (16 modes, gelu) →
   project to 1 → `u` on the grid; queries answered by linear
   interpolation along the grid (differentiable). Time enters nowhere
   (all queries are at \(t = 0\) here; recorded as a limitation).
3. **`AttnOperator`**: `SetDenoiser` re-used verbatim with context tokens
   \((x_j, \phi(x_j), \text{se}=0)\), `params` = the empty vector, query
   \((0, x)\) — the GNOT/Transolver-style cross-attention operator in the
   code we already have.

Baseline: per-φ R5A `DeepBranchNet` trained on that φ's own 500 labels
(`settrain.per_instance_mlp_l1`), as C0 in D02.

## Training and evaluation (`parabolab/deep/optrain.py`)

`train_operator(net, instances, *, steps=20000, batch_instances=32,
n_query=64, lr=1e-3, device, seed)`: each step draws `batch_instances`
instances and `n_query` finite states per instance, loss = MSE in scaled
units against draw-0 labels; Adam + cosine, grad-clip 1.0.
`evaluate_operator(net, instances, device) -> L1 per instance` on the
101-grid against `u_grid`.

## Protocol and rules (fixed before running)

For each family and each `n_train ∈ {250, 500, 1000}`: train the three
backbones (seed 0) and evaluate on the 50 held-out φ; run the per-φ
baseline once per family. Report the table (backbone × n_train, median
and max L1) and the learning curve.

- **Step 1 gate (`heat_phi`)**: at least one backbone reaches median L1
  ≤ 1.5× the per-φ baseline at `n_train = 1000`; if none does, label noise
  or the φ-family is the bottleneck and Step 2 is not run until that is
  understood.
- **Step 2 verdict (`ac_phi`)**: same criterion; the "which backbone"
  answer is the learning curve, reported whatever it shows. The kept
  backbone is the one with the lowest median L1 at `n_train = 1000`,
  ties by max L1.

## Driver

`examples/phi_operator.py --family heat_phi --n-train 1000 --n-test 50
--curve 250 500 1000 --steps 20000 --device cuda --jobs 16` (+ `--tiny`).
CSV `examples/phi_operator.csv`: `family, backbone, n_train, instance_seed,
l1, seconds`. Un-ignore the CSV.

## Testing (fast)

- Fourier φ: `max|phi_grid| ≈ 0.9`; `heat_fourier_1d` exact solution equals
  the FD reference on the grid to 1e-3 (cross-validates both);
  `fd_reference_1d` on `allen_cahn_nd(d=1, T=0.3)` matches the traveling
  wave to 1e-4; `fd_reference_1d` raises for a gradient-dependent `f`.
- Corpus: a `heat_phi` instance has `phi_grid.shape == (101,)`, MC labels
  agree with the exact solution within 4 stderr on ≥ 95 % of states; old
  files without `phi_grid` still load.
- Backbones: output shapes; `FNO1d` interpolation reproduces grid values
  at grid queries exactly; `AttnOperator` is permutation-invariant in the
  φ tokens; every backbone's output scales with the output scaler.
- Trainer: 30 steps on a toy corpus lowers the loss; evaluation returns
  finite values; driver `--tiny` writes rows for all three backbones and
  the baseline.

## Deliverables

Code + tests; `examples/phi_operator.csv`; `## Results` here with the
Step 1 gate outcome, the Step 2 table and learning curves, the kept
backbone, and the per-backbone reading; gotchas if any.

## Results

Corpora: per family 1000 train / 50 held-out random Fourier φ (K = 4,
max|φ| = 0.9), 500 states, M = 1000, one draw; operators trained on the
first 250 / 500 / 1000 training φ (20 000 steps × 32 instances × 64
queries, Adam 1e-3 cosine, RTX 4060); per-φ baseline = R5A net on each
held-out φ's own 500 labels (3000 epochs). Backbone sizes: DeepONet
63 k, FNO-1D 74 k, attention operator 911 k parameters. Rows in
`examples/phi_operator.csv`. Training rows restricted to the sensor
range \([-8, 8]\) for all backbones (the FNO clamps outside its grid).
Commands: `python examples/phi_operator.py --family <heat_phi|ac_phi>
--steps 20000 --device cuda --jobs 16`.

### Step 1 — `heat_phi` (linear heat, exact reference)

Held-out MC labels: median stderr 6.0e-3 on |u| ≈ 0.3.

| backbone | n_train | L1 median | L1 max | wins vs per-φ (of 50) |
|---|---|---|---|---|
| per-φ R5A net | — | 1.26e-03 | 2.51e-03 | — |
| DeepONet | 250 / 500 / 1000 | 5.60e-03 / 2.46e-03 / 1.71e-03 | 1.88e-02 / 1.19e-02 / 7.70e-03 | 13 |
| attention operator | 250 / 500 / 1000 | 1.96e-03 / 1.29e-03 / 1.24e-03 | 6.26e-03 / 2.81e-03 / 2.90e-03 | 39 |
| **FNO-1D** | 250 / 500 / 1000 | 1.60e-03 / 1.12e-03 / **8.12e-04** | 4.18e-03 / 2.63e-03 / **2.19e-03** | **49** |

**Gate: PASS** — all three backbones are within 1.5× of the per-φ
baseline at n = 1000 (ratios 0.64 / 0.98 / 1.36), so label noise and the
φ-family are not the bottleneck. Reading: the FNO, whose spectral layers
are the heat equation's natural basis (each Fourier mode is damped
independently), beats a network trained on each φ's own labels on 49 of
50 held-out φ, at 0.64× the error — the operator averages label noise
across instances that share modes. The attention operator ties the
baseline (0.98×) and its curve has flattened between 500 and 1000; the
DeepONet is worst but still improving steeply (5.6 → 2.5 → 1.7e-3), i.e.
data-limited at this size. A new φ costs one forward pass instead of a
500 × 1000-tree MC run plus 3000 epochs.

### Step 2 — `ac_phi` (Allen–Cahn, FD reference)

Held-out MC labels: median stderr 1.4e-2 on |u| ≈ 0.4 (the nonlinearity
more than doubles the label noise of Step 1 at the same M). The first
run of this step crashed in the per-φ baseline (`grid_errors` needs
`pde.exact_solution`, which `ac_phi` lacks); the baseline now scores
against the instance's stored grid reference — identical numbers for
every family with a closed form (commit `1d5593e`).

| backbone | n_train | L1 median | L1 max | wins vs per-φ (of 50) |
|---|---|---|---|---|
| per-φ R5A net | — | 5.55e-03 | 1.82e-02 | — |
| DeepONet | 250 / 500 / 1000 | 1.89e-02 / 1.12e-02 / 9.73e-03 | 3.72e-02 / 2.61e-02 / 1.63e-02 | 5 |
| FNO-1D | 250 / 500 / 1000 | 1.42e-02 / 8.56e-03 / 5.31e-03 | 3.39e-02 / 2.95e-02 / 1.73e-02 | 31 |
| **attention operator** | 250 / 500 / 1000 | 9.20e-03 / 6.68e-03 / **4.47e-03** | 1.86e-02 / 1.62e-02 / **9.24e-03** | **41** |

**Verdict: PASS** for the attention operator (0.81× the baseline) and
the FNO (0.96×); the DeepONet fails the 1.5× criterion (1.75×).
**Kept backbone: the cross-attention operator** (lowest median at
n = 1000 and, by a factor of two, the best worst case: 9.2e-3 against
1.7e-2 for the FNO and 1.8e-2 for a per-φ net).

Reading. The ranking reverses between the two steps, and the reversal
is the finding. The tables establish *that* it reverses; the *why* below
is an interpretation, not a tested mechanism (no ablation of FNO mode
count or inspection of learned spectral weights was run). On the linear
heat equation the solution operator is diagonal in the Fourier basis
(mode-wise damping), which the FNO's spectral layers represent directly —
a plausible reason it wins outright with 74 k parameters. Allen–Cahn's
\(u - u^3\) couples modes; the FNO's fixed 16-mode truncation and
pointwise nonlinearity still fit it (0.96×), while the attention operator
— which lets every query attend to the whole φ profile — generalises
best and most robustly. All three learning curves are still descending
at n = 1000 (attention 9.2 → 6.7 → 4.5e-3; FNO 14 → 8.6 → 5.3e-3) with
no sign of saturation, consistent with a data-limited regime (though
capacity was not varied at fixed n, so this is not proof): more φ, at
≈ 1 s each to generate, would likely improve every backbone, whereas the
per-φ baseline cannot improve without more samples per φ. The
DeepONet's fixed-size branch embedding of a 101-point φ is the weakest
inductive bias for both problems.

What the amortisation buys: a per-φ answer costs a 500 × 1000-tree MC run
(≈ 1 s on 16 workers) plus a 3000-epoch fit (≈ 8 s); an operator answers
a new φ in one forward pass (< 1 ms) after a one-off ≈ 15 min corpus and
≈ 10 min of training, with better accuracy than the per-φ fit on
41/50 held-out φ. Step 3 (fully nonlinear families with derivative codes)
remains open: it needs a φ-family with controlled higher derivatives and
a high-M MC reference, both outside this spec.

Cost of the study: corpora ≈ 25 min of MC + FD; baselines 2 × 50 × 8 s;
18 trainings ≈ 1.6 h GPU (the attention operator dominates at ≈ 10 min
each).
