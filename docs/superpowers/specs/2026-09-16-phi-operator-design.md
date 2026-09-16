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
