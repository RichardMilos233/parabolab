# Universal-backbone benchmark across the sampler's nonlinear PDE class

Status: confirmed in chat on 2026-09-16 (PDE set, two curve points, four backbones). Branch
`research/nn-backbone-benchmark` (from `main` at `9b02157`, which contains
the merged NN line). Follows `docs/research/nn-fitting/README.md` §Next.

## Goal

Stop choosing a backbone per PDE. Run one comparison — the same four
backbones, the same corpus protocol, the same pre-registered metric — over
a broad set of nonlinear parabolic PDEs the coding-tree sampler supports,
pick the backbone with the best *overall* score, then (next spec) tune
that one. The deliverable is a table, a learning-curve figure per family,
and one ranked list.

## Non-goals

- Tuning any backbone before the winner is known (that is the next spec).
- \(d > 1\) and time-dependent queries (a follow-up once the box sampler
  exists); the Dym example (non-integrable at every T, gotcha 14).
- Changing the sampler, mechanisms, rates or proposals. Everything stays
  in `parabolab/deep/`.

## The PDE set

All 1-D, queries at \(t = 0\), terminal conditions from the random
Fourier family of the φ-operator study (K = 4, max|φ| = 0.9, segment
\([-8, 8]\) unless stated). An instance = (family, φ coefficients, θ).

| key | PDE (with \(u_t + \tfrac12 u_{xx} + f = 0\)) | class | T | θ | reference for \(u(0,\cdot)\) | status |
|---|---|---|---|---|---|---|
| `heat_phi` | \(f \equiv 0\) | linear | 0.3 | — | closed form | done (D03) |
| `ac_phi` | \(f = u - u^3\) | semilinear | 0.3 | — | FD | done (D03) |
| `kpp_phi` | Fisher–KPP \(f = u(1-u)\) | semilinear | 0.3 | — | FD | new (builder via `library.fisher_kpp_1d`'s f) |
| `expgrad_phi` | \(f = \alpha u_x + e^{-u} - 2e^{-2u}\), α = 10 | gradient nonlinearity | 0.05 | — | FD extended to first-order terms (upwind) | new |
| `tan_phi` | quasilinear tan \(f = \alpha u_x + u_{xx}/(1+u^2) - u_{xx}/2 - 2u\), α = 10 | fully nonlinear, 2nd order | 0.01 | — | MC, M = 10⁵ per grid point | new (nD-class rebuild) |
| `cosine_phi` | \(f = \alpha u_x + u - (u''/12)^2 + \cos(\pi u''''/24) - u''/2\), α = 10 | fully nonlinear, 4th order | 0.04 | — | MC, M = 10⁵ | new (nD-class rebuild) |
| `log_phi` | \(f = \alpha u_x + \log(u''^2 + u'''^2) - u''/2\), α = 5 | fully nonlinear, 3rd order | 0.02 | — | MC, M = 10⁵ | **conditional**: random φ can bring \(u''^2+u'''^2\) near 0; include only if the label-calibration pre-check passes |
| `merton_theta` | Merton HJB, φ = \(x^{1-\gamma}/(1-\gamma)\) | fully nonlinear (z₁²/z₂), θ = (γ, μ, σ) | 0.1 | 3 | closed form | done (D02), re-run under the operator interface |

Eight families, five new. Semilinear/gradient families get FD references
(deterministic, validated against closed forms where they exist); the
fully nonlinear families get Monte Carlo references at M = 10⁵ (≈ 15 s per
instance at their short T; the reference stderr is stored and reported —
a backbone cannot be scored below the reference noise).

**Label-calibration pre-check (per new family, before any training):**
generate 20 instances at M = 1000 and M = 10⁴ at the same states; require
the M = 1000 labels to agree with the M = 10⁴ labels within 4 stderr on
≥ 95 % of states and the empirical stderr ratio to be within 2× of
\(\sqrt{10}\). A family failing this is excluded and the failure recorded
(it means the estimator is heavy-tailed at that T for random φ, which is
itself a finding for the integrity line).

## Unified instance interface

Every backbone maps `(phi_grid (101,), theta (P,), query (t, x)) → u`.
Families without θ pass `P = 0`. `Instance.phi_grid` and
`Instance.spec.params` already carry both; `merton_theta`'s φ depends on γ,
so its `phi_grid` varies with θ as it should.

## Backbones (four)

1. **DeepONet** — branch on `[phi_grid, theta]`, trunk on (t, x).
2. **FNO-1D** — channels `[φ(x_j), x_j/8, θ broadcast]`.
3. **Cross-attention operator** — φ samples as tokens, θ as the
   `SetDenoiser` params vector.
4. **Coefficient MLP** — the D02 FiLM net on `[t, x]` conditioned on
   `[Fourier coefficients (9), θ]`: the "no operator, just conditioning"
   control. It sees the same information as the others (the coefficients
   determine `phi_grid`).

Sizes as in D02/D03 (63 k / 74 k / 911 k / 71 k). Same steps (20 000),
batch, optimiser for all; per-instance R5A net as the baseline.

## Protocol and pre-registered rules

Per family: 1000 train / 50 held-out instances, 500 states, M = 1000;
backbones trained at `n_train ∈ {250, 1000}` (two points give the slope;
the third point of D03 cost 40 % of its compute and changed no ranking);
one seed. Metric per (family, backbone): median held-out grid L1 divided
by the per-instance baseline's median — the **ratio** \(r_{f,b}\); and the
max-L1 ratio for robustness.

- **Overall score** \(S_b = \exp\big(\tfrac1F\sum_f \log r_{f,b}\big)\)
  (geometric mean over families at n = 1000).
- **Winner** = lowest \(S_b\). **Failure family** = any \(r_{f,b} > 1.5\);
  a winner with a failure family is reported alongside the best backbone
  with none.
- **Robustness winner** = lowest \(\max_f r_{f,b}\). If it differs from
  the score winner, both are reported; the tuning spec chooses.
- Learning-curve slope \(\log(r_{250}/r_{1000})\) per backbone is reported,
  not scored.

Compute estimate: corpora ≈ 8 × 20 min; references ≈ 3 × 15 min (MC) +
minutes (FD); trainings 8 × 2 × (2 + 2 + 10 + 2) min ≈ 4.3 h; baselines
8 × 50 × 8 s ≈ 1 h. ≈ 8–9 h on the laptop, run family by family and
resumable (CSV rows are the ledger, as before).

## Code changes (all under `parabolab/deep/`)

- `families.py`: nD-class builders `kpp_fourier_1d`, `expgrad_fourier_1d`,
  `tan_fourier_1d`, `cosine_fourier_1d`, `log_fourier_1d`, and
  `merton_theta` support (φ from γ); `fd_reference_1d` gains first-order
  terms; `mc_reference_1d(pde, xq, m_samples)` (grid references by the
  sampler, storing stderr).
- `corpus.py`: `Family.theta_ranges` alongside the Fourier sampler so an
  instance carries both; `Instance.ref_stderr` (grid, optional).
- `opnet.py`: `theta` input on all three operators; `CoeffMLP` wrapper
  around `ConditionedNet`.
- `optrain.py`: pass θ; `calibration_precheck(family)`.
- `examples/backbone_benchmark.py`: `--families ...`, per-family runs,
  `--report` computing \(S_b\), the failure list and the robustness winner
  from the CSV.

## Deliverables

Code + tests (`--tiny` smoke per family); `examples/backbone_benchmark.csv`;
`docs/research/nn-fitting/backbone-benchmark.md` with the table, the
ranked list, per-family learning curves (one figure), the calibration
pre-check outcomes, and the chosen backbone for the tuning spec.

## Questions to confirm before running

1. PDE set: the eight above (with `log_phi` conditional)? Anything to add
   or drop — e.g. `binary_control_1d` (\(f = u^2\), blows up at T = 1,
   constant φ) is excluded as a poor fit for a φ-family.
2. Two curve points (250, 1000) instead of three — acceptable?
3. Four backbones — add any (e.g. a U-Net on the grid) before the run?

## Amendments at plan time (2026-09-16)

- **Conditioning vector.** Every backbone receives the instance's full
  `params` vector as its conditioning input `cond` (Fourier coefficients
  for φ-families, θ for `merton_theta`), alongside `phi_grid`. The
  operators therefore see the coefficients as well as the sampled φ —
  redundant but harmless, and it makes the four backbones informationally
  identical. Signature for all four: `net(phi_grid (B,S), cond (B,P),
  q_tx (B,Q,2)) -> (B,Q)`.
- **Rates.** The fully nonlinear families (`tan_phi`, `cosine_phi`,
  `log_phi`) use rate 1 (the JEQ examples' convention, gotcha 5/19) via a
  new `Family.rate`; the others keep the generator's jcp default as in
  D02/D03.
- **MC references** reuse `generate_training_data(states=grid)` at
  M = 10⁵ (with its outlier filter, as for every label in this line);
  the per-point stderr is stored in `Instance.ref_stderr`.
