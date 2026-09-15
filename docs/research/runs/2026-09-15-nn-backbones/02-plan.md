# 2026-09-15-nn-backbones — Research plan (proposed, not started)

Two questions, in the order they must be answered: **(1) what data and
which input/label interface**, **(2) which backbone per interface**.
Everything below is scoped to what an 8 GB GPU and a 32-core CPU sampler
can do; models stay ≤ 50 M parameters, corpora ≤ 10⁴ instances.

## Stage 0 — Data interfaces (the prerequisite for every backbone)

Deliverable: `parabolab/deep/corpus.py` — an *instance* generator on top
of the existing sampler, one level above `datasets.py`.

| Interface | What one instance is | What the sampler must add | Labels | Reference for evaluation |
|---|---|---|---|---|
| **I-point** (D01) | one PDE, states \((t,x)\) over \([0,T]\times\) box in \(\mathbb R^d\) | box sampler (segment → box), \(t\)-range on | \(y\), stderr, optional \(\partial^\mu u\) via `DxN` | closed forms (AC any d, HJB d=100, exp) |
| **I-param** (D02) | one \(\theta\) (Merton \(\gamma,\mu,\sigma,\rho\); Vasicek \(\kappa,\bar r,\eta\)) with its states | factory-with-θ; instance cache keyed by \(f\) (tables reused, gotcha 22) | \(y\), \(u_x, u_{xx}\) labels | Merton / Vasicek closed forms |
| **I-func** (D03) | one terminal condition \(\phi\) from a family | \(\phi\) as parametrised sympy expression (random Fourier series \(\sum_k a_k\cos(kx)+b_k\sin(kx)\), or GP-like with analytic derivatives), lazily lambdified; \(\phi\) sampled on a query grid as the network input | \(u(t,\cdot)\) on the grid | linear heat: exact kernel; semilinear 1-D: finite differences; fully nonlinear 1-D short-T: high-\(M\) MC (\(M = 10^5\)) as "truth" |
| **I-set** (D04) | one PDE instance with a *set* of scattered noisy estimates \(\{(t_i,x_i,y_i,\text{se}_i)\}\) at low \(M\), plus an independent second draw at the same states (Noise2Noise target) and, where it exists, the exact \(u\) | two independent draws per state (different seeds), same states | second-draw \(y'\) (N2N) or exact \(u\) | same as above |

Corpus format: sharded `.npz` per instance under
`examples/nn_corpus/<family>/<instance_id>.npz` with the instance spec as
JSON metadata (extend `datasets.DatasetSpec` → `InstanceSpec` with
`family`, `params`, `phi_coeffs`, `states`, `draws`). Everything
git-ignored; regenerable from specs; one `corpus.py --family ...` CLI.

Data-volume guidance (drives backbone size): an instance of 1000 states
at \(M=10^3\) costs ≈ 1–2 s on 16 workers, so 10⁴ instances ≈ 3–5 h of
CPU — that is the corpus scale for D03/D04/D10. Per-instance nets
(D01/D02) stay small (R5a size); set/operator models get 5–20 M params.

Safety constraint inherited from the integrity programme: only include
\((T,\text{rate})\) combinations whose second moment is finite (the
blow-up study and, once available, the L²-horizon certificate); a corpus
containing infinite-variance labels teaches the denoiser the tail, not
the solution.

## Stage 1 — D04: set-to-field Monte Carlo denoiser (≈ 3 weeks)

**Claim C1.** A cross-attention model \(\mathcal D\):
context \(\{(t_i,x_i,y_i,\text{se}_i)\}_{i\le N}\) + instance tokens
(\(\theta\), family id) → query \((t,x)\) → \(\hat u(t,x)\), trained with
the Noise2Noise loss \(\|\mathcal D(\text{draw}_1)(x_i) - y'_i\|^2\)
(second independent draw) is an unbiased-in-expectation estimator of
\(u\) (N2N argument: \(\mathbb E[y'_i\mid\text{draw}_1] = u(x_i)\)) and,
across instances, reaches the accuracy of a per-instance R5a net trained
at \(10\times\) the samples.

**Backbone.** Encoder: per-point MLP embedding of \((t,x,y,\text{se})\)
→ 4–6 transformer blocks over the context set (linear/physics attention
from Transolver if \(N>4000\)); decoder: cross-attention from query
embedding to context tokens → MLP head. 2–10 M params. Baselines:
(a) per-instance R5a net at the same \(M\); (b) same at \(10M\);
(c) a non-learned kernel smoother (Nadaraya–Watson with se-weighting) —
the honest "is attention doing more than smoothing" control.

**Numerical protocol.** Family A: Allen–Cahn d=1, \(T\in[0.1,0.5]\),
wave offset and rate varied (closed form); Family B: Merton across
\(\gamma\in[0.3,0.8]\), \(\sigma,\mu\) (closed form); 2000 train / 200
held-out instances, \(M\in\{10^2,10^3\}\), states 500–1000. Report the
**L1-vs-MC-budget curve** on held-out instances for D04 and baselines
(a)–(c); success = D04 at \(M\) ≤ baseline at \(10M\) on both families;
failure = D04 not below baseline (c). Then Family C: exp-gradient d=5
(closed form, box states) for a d>1 check.

**Formal scope.** The N2N unbiasedness identity for the mean-squared loss
is a two-line lemma (conditional expectation of an independent draw);
state it in `03-claims.md`; no Lean.

**First test (go/no-go, 2 days).** Family A only, 500 instances,
\(M=10^3\): if D04's held-out L1 is not below baseline (a), stop D04.

## Stage 2 — D03: terminal-condition operator φ → u (≈ 4 weeks)

**Claim C2.** For a \(\phi\)-family with analytic derivatives, an
operator \(\mathcal G:\phi\mapsto u(t,\cdot)\) trained on coding-tree
labels for \(n_\phi\) instances reaches held-out error equal to
per-\(\phi\) R5a nets, at amortised cost \(<1/10\) per new \(\phi\); the
three backbones differ measurably in label-noise robustness.

**Backbones on identical data:** DeepONet (branch: \(\phi\) on 64-point
grid → MLP; trunk: \((t,x)\)); FNO-1D (\(\phi\) grid → \(u(t,\cdot)\) grid,
\(t\) as channel); cross-attention operator (GNOT/Transolver style:
\(\phi\) grid tokens → queries \((t,x)\)). 1–20 M params each.

**Numerical protocol.** Step 1 linear heat (\(f\equiv 0\)): exact
\(u = p_{T-t} * \phi\); 500 Fourier-series \(\phi\); target L1 1e-3 on
held-out \(\phi\) — this isolates label noise and \(\phi\)-family design
(go/no-go). Step 2 Allen–Cahn \(f(u)=u-u^3\), 1-D, \(T=0.3\): reference
by finite differences; 2000 \(\phi\). Step 3 a fully nonlinear 1-D
example (tan or cosine family at their short \(T\)): reference by
\(M=10^5\) MC; 1000 \(\phi\). Report held-out L1 per backbone vs
\(n_\phi\) and vs \(M\); the "which backbone" answer is the curve, not
one number.

**Formal scope.** None beyond stating the amortisation accounting.

## Stage 3 — D02: parametric Merton–Vasicek policy operator (≈ 2 weeks, shares Stage 0/1 infra)

FiLM-conditioned R5a net on \((t,x,\theta)\), labels \(u, u_x, u_{xx}\)
(D07 folded in as an ablation: with vs without derivative labels),
policy \(\pi^*=-\frac{\mu-r}{\sigma^2}\frac{u_x}{x\,u_{xx}}\) evaluated
against the closed form across held-out \(\theta\). Success: policy L1
≤ 2 % relative on held-out \(\theta\); D07 ablation reported either way.

## Stage 4 (stretch) — D10 foundation-style pretraining

Only if Stage 2 Step 2 reaches per-instance accuracy. Corpus: families
{polynomial \(f(u)\), exp-gradient, HJB-type, Merton-type} × \(\phi\)
× \(\theta\), ~10⁴ instances; scOT-style operator transformer ≤ 50 M
params; measure fine-tuning label-efficiency on a held-out family. Uses
D09's MLMC schedule for the corpus.

## Environment

- Install the CUDA torch wheel (`pip install --force-reinstall --no-deps
  torch --index-url https://download.pytorch.org/whl/cu124`, same 2.13
  pin) — required from Stage 1; add a `device="cuda"` smoke test.
- Keep the ablation harness as the per-instance baseline provider (R5a).

## Task handoffs (proposed)

| Task | Role | Deliverable | Acceptance |
|---|---|---|---|
| T01 corpus generator (Stage 0) | implementation | `deep/corpus.py`, `InstanceSpec`, box sampler, φ-family, two-draw option, CLI | 10 instances of each family regenerate bit-identically; tests |
| T02 D04 first test | implementation | set model + baselines on Family A | curve of held-out L1 vs M; go/no-go recorded |
| T03 D04 full protocol | implementation | Families A/B/C, ensembles of baselines | results section in a new spec |
| T04 D03 Step 1–3 | implementation | three backbones on identical corpora | held-out curves; backbone comparison |
| T05 D02 + D07 ablation | implementation | conditioned net + policy evaluation | policy L1 table |
| R01 claims audit | research | C1 lemma, amortisation accounting, corpus safety rule | `03-claims.md` |

Escalation: Stage 1 or 2 first test failing returns to the research
role (rewrite the plan around D02/D09 or change the φ-family / \(M\)),
not to a bigger model.
