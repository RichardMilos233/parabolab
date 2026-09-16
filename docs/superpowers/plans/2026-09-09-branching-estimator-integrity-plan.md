# Branching Estimator Integrity Implementation Plan

> **Archived implementation plan — status reviewed 16 September 2026.**
> The moment, Dym, proposal, and finite Lean foundations now have implementation
> and research records. This original plan is not a live checklist or evidence
> that every proposed study was completed. The old finance programme, model
> assignments, unavailable-model gate, branch/worktree setup, dirty-file
> snapshots, and expected test counts are superseded session history.
> Navigation: [archive index](../README.md), [current research](../../research/README.md),
> [documentation map](../../documentation-map.md).

> **Original workflow metadata (inactive):** This plan originally requested
> superpowers:subagent-driven-development or superpowers:executing-plans.
> Its checkbox syntax is preserved as a historical planning record.

**Goal:** Prove three estimator-integrity results for coding-tree Monte Carlo, verify their finite and numerical consequences, formalize their finite/algebraic cores in Lean, and present seven further candidate contributions with honest proof and novelty status.

**Architecture:** The mathematical layer defines a common finite-depth multitype tree and proves its exact moment recursion, a Dym-specific non-integrability theorem, and a pilot/freeze proposal theorem. The Python layer adds opt-in depth truncation, deterministic Gaussian/time quadrature for finite-depth moments, nonuniform tuple proposals, pilot estimation, and reproducible Dym and Merton--Vasicek experiments without changing the established default sampler. A separate Lean 4 project formalizes finite mechanism tables, monotone moment iteration, finite-simplex proposal optimization, and the algebraic/singular-integral core.

**Tech Stack:** Python 3.11, NumPy, SymPy, Matplotlib, PyTest, the `parabolab` Conda environment, Lean 4.33.0, Mathlib tag `v4.33.0`.

## Original execution constraints (historical)

- Approved design:
  `docs/superpowers/specs/2026-09-09-branching-estimator-integrity-design.md`.
- Base code revision:
  `697b62b04d83e44edcfdc84d32466df2caf25dc2`. The execution worktree
  starts from the commit containing this plan, whose parent is that base
  revision.
- Execute in a dedicated worktree and branch:
  `../parabolab-estimator-integrity`, `research/estimator-integrity`.
- Existing uncommitted changes in `demo/merton.py` and
  `demo/merton_vasicek.py` are user-owned. Never edit, stage, move, or commit
  them.
- GPT owns paper-level mathematical reasoning and Lean proof development.
- Gemini owns every Python implementation, Python test execution, numerical
  experiment, plot, and `.canvas.tsx` implementation.
- Lean is treated as mathematical proving, so GPT may write Lean and run
  `lake` one tactic/check at a time.
- Gemini is not currently available in this session. Do not substitute Claude,
  Composer, Grok, or GPT for a Gemini-owned task; stop at that task until the
  user enables Gemini.
- Preserve the default `sample_tree` RNG order exactly:
  exponential, integer tuple choice when needed, shared normal branch mark,
  then children in tuple order.
- New depth and proposal behavior must be opt-in. Existing callers and golden
  RNG tests must remain byte-for-byte reproducible.
- All Python commands run from the `parabolab` repository root through
  `conda run -n parabolab`.
- Do not use percentile filtering, clipping, or deletion of finite tail
  observations in estimator-integrity experiments.
- Do not report a Gaussian confidence interval until an \(L^2\) condition has
  been proved for that experiment.
- Every mathematical claim is labelled proved, conditional, conjectural,
  refuted, empirical, or prior-art overlap.
- Final Lean sources contain no `sorry`.

## File Map

### Mathematical notes

- Create:
  `docs/research/estimator-integrity/notation-and-moment-theorem.md`
  — common model, exact \(p\)-moment theorem, proof, and assumptions.
- Create:
  `docs/research/estimator-integrity/dym-nonintegrability.md`
  — exact Dym theorem and positive-probability shallow-event proof.
- Create:
  `docs/research/estimator-integrity/adaptive-proposals.md`
  — tuple/event-time optimizers, pilot/freeze unbiasedness, oracle bound.
- Create:
  `docs/research/estimator-integrity/secondary-candidates.md`
  — seven secondary statements, proof status, prior art, and quant relevance.
- Create:
  `docs/research/estimator-integrity/reproducibility.md`
  — environments, commands, seeds, generated outputs, and claim ledger.

### Python

- Modify: `parabolab/tree.py`
  — opt-in killed depth and nonuniform tuple proposal while preserving defaults.
- Modify: `parabolab/mc.py`
  — forward opt-in depth/proposal arguments.
- Create: `parabolab/moments.py`
  — deterministic finite-depth \(p\)-moment quadrature in one spatial dimension.
- Create: `parabolab/integrability.py`
  — deterministic truncated Gaussian inverse-power integrals.
- Create: `parabolab/proposals.py`
  — optimizer, floor, frozen proposal, pilot continuation estimator, diagnostics.
- Modify: `parabolab/__init__.py`
  — export public research interfaces only.
- Create: `tests/test_moments.py`.
- Create: `tests/test_integrability.py`.
- Create: `tests/test_proposals.py`.
- Modify: `tests/test_tree.py`.
- Create: `examples/dym_nonintegrability.py`.
- Create: `examples/proposal_merton_vasicek.py`.

### Lean

- Create: `formal/lean-toolchain`.
- Create: `formal/lakefile.lean`.
- Create: `formal/EstimatorIntegrity.lean`.
- Create: `formal/EstimatorIntegrity/FiniteTree.lean`.
- Create: `formal/EstimatorIntegrity/MomentIteration.lean`.
- Create: `formal/EstimatorIntegrity/Proposal.lean`.
- Create: `formal/EstimatorIntegrity/Dym.lean`.

---

### Task 1: Isolated Worktree and Verified Baseline

**Owner:** Gemini for commands; GPT may inspect the resulting status.

**Files:**
- No source files changed.

**Interfaces:**
- Produces: clean worktree
  `/Users/michael/Desktop/NTU/fyp/parabolab-estimator-integrity`.
- Produces: branch `research/estimator-integrity` at the commit containing
  this plan.

- [ ] **Step 1: Create the isolated worktree**

Run from `/Users/michael/Desktop/NTU/fyp/parabolab`:

```bash
PLAN_COMMIT=$(
  git log -1 --format=%H -- \
    docs/superpowers/plans/2026-09-09-branching-estimator-integrity-plan.md
)
test "$(git rev-parse "${PLAN_COMMIT}^")" = \
  "697b62b04d83e44edcfdc84d32466df2caf25dc2"
git worktree add \
  /Users/michael/Desktop/NTU/fyp/parabolab-estimator-integrity \
  -b research/estimator-integrity "$PLAN_COMMIT"
```

Expected: a new branch and worktree are created. The original worktree still
shows only the user's two modified demo files.

- [ ] **Step 2: Verify isolation**

Run:

```bash
git -C /Users/michael/Desktop/NTU/fyp/parabolab status --short
git -C /Users/michael/Desktop/NTU/fyp/parabolab-estimator-integrity status --short --branch
```

Expected:

```text
 M demo/merton.py
 M demo/merton_vasicek.py
## research/estimator-integrity
```

- [ ] **Step 3: Run the Python baseline**

Run:

```bash
cd /Users/michael/Desktop/NTU/fyp/parabolab-estimator-integrity
PYTHONDONTWRITEBYTECODE=1 conda run --no-capture-output -n parabolab \
  python -m pytest -q -p no:cacheprovider
```

Expected: all default non-slow tests pass. Record the exact count and elapsed
time in `docs/research/estimator-integrity/reproducibility.md` when that file
is created. At source revision `697b62b`, the expected baseline is
`143 passed, 13 deselected`.

- [ ] **Step 4: Confirm no generated files**

Run:

```bash
git status --short
```

Expected: no output.

---

### Task 2: Common Model and Exact Moment Theorem

**Owner:** GPT mathematical proof.

**Files:**
- Create:
  `docs/research/estimator-integrity/notation-and-moment-theorem.md`.

**Interfaces:**
- Produces: `Definition 2.1` finite-depth killed coding tree.
- Produces: `Theorem 2.2` exact finite-depth \(p\)-moment recursion.
- Produces: `Theorem 2.3` monotone minimal fixed point and \(L^p\)
  characterization.
- Consumed by: Tasks 3, 5, 6, 8, and 9.

- [ ] **Step 1: State the model without relying on repository notation**

Write explicit hypotheses:

```text
(H1) C is a countable code space.
(H2) Every live mechanism table M(c) is finite and nonempty, and every
     labelled live tuple contains at least one child.
(H3) q_c(Z)>0 for every live labelled tuple Z.
(H4) rho_c is positive a.e. on every branch-time interval used.
(H5) Children share the parent's Markov branch position.
(H6) Conditional on that position, child subtrees are independent.
(H7) The continuous-time tree is nonexplosive almost surely.
```

Label tuples, rather than treating mechanisms as sets, so duplicated tuples
and coefficients remain distinguishable.

- [ ] **Step 2: Define the killed tree**

For a tree rooted at generation zero, define \(H_c^{[n]}\) by returning zero
whenever a particle at generation \(n\) experiences a branch before the
horizon. A surviving particle still contributes its ordinary terminal factor.
State and prove pointwise:

\[
|H_c^{[n]}|^p
=
|H_c|^p\,\mathbf 1_{\{\operatorname{depth}(\mathcal T)\le n\}},
\qquad
|H_c^{[n]}|^p\uparrow |H_c|^p.
\]

The second statement uses almost-sure nonexplosion.

- [ ] **Step 3: Prove the finite-depth recursion**

For \(\Delta=T-t\), prove by conditioning on the first event:

\[
\begin{aligned}
V_{c,n+1}^{(p)}(t,x)
={}&\bar F_c(\Delta)^{1-p}P_\Delta|g_c|^p(x)\\
&+\sum_{Z\in\mathcal M(c)}q_c(Z)^{1-p}
\int_0^\Delta \rho_c(s)^{1-p}
P_s\!\left[
\prod_{z\in Z}V_{z,n}^{(p)}(t+s,\cdot)
\right](x)\,ds .
\end{aligned}
\]

Start with the hardest point: justify the product using conditional child
independence at one shared branch position. Then account separately for the
tuple probability, lifetime density, and likelihood weights.

- [ ] **Step 4: Prove minimality**

Let \(\Phi_p\) be the nonnegative operator on code-indexed functions defined by
the right-hand side. Prove:

\[
V_0=\Phi_p(0),\qquad V_{n+1}=\Phi_p(V_n),\qquad V_n\uparrow V.
\]

Use monotonicity of finite sums, integrals, and products. For any nonnegative
fixed point \(W=\Phi_p(W)\), induction gives \(V_n\le W\), hence \(V\le W\).
Use Tonelli and monotone convergence to show \(\Phi_p(V)=V\).

- [ ] **Step 5: Prove the exact \(L^p\) criterion**

Conclude:

\[
H_{t,x,c}\in L^p
\quad\Longleftrightarrow\quad
V_c^{(p)}(t,x)<\infty.
\]

State explicitly that the equivalence is pointwise in \((t,x,c)\); it does
not assert uniform boundedness over states, codes, or horizons.

- [ ] **Step 6: Audit the proof**

Search:

```bash
rg -n "TBD|TODO|obvious|clearly|by standard arguments|breakthrough" \
  docs/research/estimator-integrity/notation-and-moment-theorem.md
```

Expected: no unsupported placeholder or novelty language. Every application
of Tonelli, conditional independence, and monotone convergence names its
nonnegative integrand or domination assumption.

- [ ] **Step 7: Commit**

```bash
git add docs/research/estimator-integrity/notation-and-moment-theorem.md
git commit -m "docs: prove exact coding-tree moment recursion"
```

---

### Task 3: Killed-Depth Sampler and Deterministic Moment Quadrature

**Owner:** Gemini Python implementation.

**Files:**
- Modify: `parabolab/tree.py`.
- Modify: `parabolab/mc.py`.
- Create: `parabolab/moments.py`.
- Modify: `parabolab/__init__.py`.
- Modify: `tests/test_tree.py`.
- Create: `tests/test_moments.py`.

**Interfaces:**
- `sample_tree(pde, t, x, *, rng, rate=None, code=Id(), mechanism=None,
  prune_zero=True, max_depth: int | None = None) -> TreeSample`.
- `estimate(pde, t, x, n_samples, *, rng=None, seed=None, rate=None,
  code=Id(), mechanism=None, prune_zero=True,
  max_depth: int | None = None) -> MCResult`.
- `MomentQuadrature(time_order: int = 12, normal_order: int = 12)`.
- `finite_depth_moment_1d(pde, t, x, *, code=Id(), p=2.0,
  max_depth, rate=1.0, mechanism=None, tuple_proposal=None,
  quadrature=MomentQuadrature()) -> float`.

- [ ] **Step 1: Add a failing killed-depth RNG test**

Append to `tests/test_tree.py`:

```python
def test_max_depth_zero_kills_a_root_branch_without_extra_draws():
    pde = allen_cahn_wave_1d(0.5)
    rng = FakeRng(exponentials=[0.1], normals=[], integers=[])
    sample = sample_tree(
        pde, 0.0, 0.3, rng=rng, rate=1.0, max_depth=0,
    )
    assert sample.value == 0.0
    assert sample.n_nodes == 1
    assert not rng.exponentials and not rng.normals and not rng.integers_q
```

- [ ] **Step 2: Run the test to verify failure**

```bash
conda run -n parabolab python -m pytest \
  tests/test_tree.py::test_max_depth_zero_kills_a_root_branch_without_extra_draws -q
```

Expected: `TypeError` because `max_depth` is not accepted.

- [ ] **Step 3: Implement opt-in killed depth**

Add `max_depth` to `sample_tree` and `_tree`. Validate that it is `None` or a
nonnegative integer. Track root generation as zero. After drawing the
particle's lifetime and determining that it branches before the horizon,
return zero when `depth >= max_depth` before drawing a tuple or branch normal.
Increment `depth` for every child. Do not alter the default branch.

- [ ] **Step 4: Verify killed and default paths**

```bash
conda run -n parabolab python -m pytest tests/test_tree.py -q
```

Expected: all tree tests pass, including the original hand-computed RNG test.

- [ ] **Step 5: Add deterministic recursion tests**

Create `tests/test_moments.py` with a one-type binary mechanism whose terminal
factor is one and whose only tuple is `(Id(), Id())`. At rate one and remaining
horizon \(r\), assert:

```python
def test_binary_depth_zero_second_moment_is_exp_r():
    got = finite_depth_moment_1d(
        constant_terminal_pde(T=0.2), 0.0, 0.0,
        p=2.0, max_depth=0, rate=1.0,
        mechanism=BinaryMechanism,
    )
    assert got == pytest.approx(math.exp(0.2), rel=1e-10)


def test_binary_depth_one_second_moment_is_exp_2r():
    got = finite_depth_moment_1d(
        constant_terminal_pde(T=0.2), 0.0, 0.0,
        p=2.0, max_depth=1, rate=1.0,
        mechanism=BinaryMechanism,
        quadrature=MomentQuadrature(time_order=16, normal_order=8),
    )
    assert got == pytest.approx(math.exp(0.4), rel=1e-9)
```

- [ ] **Step 6: Run the recursion tests to verify failure**

```bash
conda run -n parabolab python -m pytest tests/test_moments.py -q
```

Expected: import failure because `parabolab.moments` does not exist.

- [ ] **Step 7: Implement `finite_depth_moment_1d`**

Use `numpy.polynomial.legendre.leggauss` for the time integral and
`numpy.polynomial.hermite.hermgauss` for

\[
\mathbb E[h(x+\sigma\sqrt{s}Z)]
=
\pi^{-1/2}\sum_j w_j
h(x+\sigma\sqrt{2s}\,\xi_j).
\]

The implementation must:

```text
1. return zero immediately for an identically-zero code;
2. compute the leaf term exp(rate*(p-1)*remaining) times the Gaussian
   expectation of |terminal|^p;
3. return only that leaf term at max_depth == 0;
4. integrate rate^(1-p)*exp(rate*(p-1)*s);
5. multiply child moments because children are conditionally independent;
6. multiply each tuple by q(tuple)^(1-p);
7. reject nonpositive, nonfinite, wrong-length, or non-normalized proposals;
8. support scalar one-dimensional PDEs only and raise a descriptive error
   for vector states.
```

- [ ] **Step 8: Add a Monte Carlo cross-check**

Use 50,000 killed binary-tree samples with a fixed seed. Assert that their
empirical second moment differs from the deterministic depth-one value by at
most five empirical standard errors of \(H^2\). Mark this 50,000-sample test
with `@pytest.mark.slow`; keep the two deterministic recursion tests in the
default suite.

- [ ] **Step 9: Export and run focused tests**

Export `MomentQuadrature` and `finite_depth_moment_1d` from
`parabolab/__init__.py`, then run:

```bash
conda run -n parabolab python -m pytest \
  tests/test_tree.py tests/test_moments.py -q -m "not slow"
```

Expected: all selected tests pass.

- [ ] **Step 10: Commit**

```bash
git add parabolab/tree.py parabolab/mc.py parabolab/moments.py \
  parabolab/__init__.py tests/test_tree.py tests/test_moments.py
git commit -m "feat: add finite-depth tree moment recursion"
```

---

### Task 4: Dym \(L^1\)-Failure Theorem

**Owner:** GPT mathematical proof.

**Files:**
- Create: `docs/research/estimator-integrity/dym-nonintegrability.md`.

**Interfaces:**
- Produces: `Theorem 4.1` infinite absolute first moment.
- Produces: `Corollary 4.2` both signed parts have infinite expectation.
- Consumed by: Tasks 5, 9, 10, and 11.

- [ ] **Step 1: Record the exact implementation instance**

Use

\[
f=-z_2/2+z_0^3z_3,\qquad
\phi_\alpha(x)=((3\alpha x)^2)^{1/3},\qquad \alpha\ne0.
\]

Record the live \(f^*\) tuple:

\[
Z_*=
\bigl((f_{z_2})^*,(f_{z_0})^*,D^2\bigr).
\]

- [ ] **Step 2: Prove the terminal identities**

On \(x\ne0\), calculate:

\[
f_{z_2}=-\frac12,\qquad
f_{z_0}(\phi_\alpha,J\phi_\alpha)=\frac{8\alpha^2}{x},
\]

and

\[
\phi_\alpha''(x)
=-\frac{2|3\alpha|^{2/3}}9|x|^{-4/3}.
\]

Do both half-lines explicitly; do not hide the even-extension sign.

- [ ] **Step 3: Isolate a finite-depth event**

For horizon \(h>0\), restrict both branch lifetimes to
\((h/8,h/4)\). Require the root to branch to \(f^*\), the \(f^*\) particle to
select \(Z_*\), and all three children to survive. Prove that this event has
strictly positive probability under the repository's exponential clock and
uniform full-support mechanism.

- [ ] **Step 4: Condition in the correct order**

Condition on the two branch times and shared second branch position. The three
children share their birth position but have independent future Brownian
increments. Restrict the \(D^2\) endpoint to a compact interval bounded away
from zero. Its conditional event has positive probability and its terminal
factor is bounded away from zero there.

- [ ] **Step 5: Prove absolute divergence**

The \((f_{z_0})^*\) endpoint has a nondegenerate shifted Gaussian density
\(g_y\) with \(g_y(0)>0\). Show:

\[
\int_{-\varepsilon}^{\varepsilon}
\frac{8\alpha^2}{|x|}g_y(x)\,dx=\infty.
\]

All remaining likelihood and terminal factors are finite and nonzero on the
restricted event. Tonelli then gives
\(\mathbb E|H_{t,x,\mathrm{Id}}|=\infty\) for every starting \(x\) and every
positive horizon.

- [ ] **Step 6: Prove two-sided signed divergence**

Fix the signs of every factor except \(1/X\). Integrate separately over
\((0,\varepsilon)\) and \((-\varepsilon,0)\) to prove:

\[
\mathbb EH^+=\mathbb EH^-=\infty.
\]

State that no Lebesgue expectation exists; symmetric principal-value
cancellation is irrelevant.

- [ ] **Step 7: State exact limits of the theorem**

Include counterexamples to each overstatement:

```text
h = 0;
alpha = 0;
a lifetime law supported entirely after h;
a proposal that is not full support and removes every singular live tuple.
```

- [ ] **Step 8: Commit**

```bash
git add docs/research/estimator-integrity/dym-nonintegrability.md
git commit -m "docs: prove Dym coding-tree nonintegrability"
```

---

### Task 5: Dym Symbolic and Truncated-Integral Experiment

**Owner:** Gemini Python implementation and execution.

**Files:**
- Create: `parabolab/integrability.py`.
- Create: `tests/test_integrability.py`.
- Create: `examples/dym_nonintegrability.py`.
- Modify: `parabolab/__init__.py`.

**Interfaces:**
- `truncated_normal_inverse_power(mean, std, power, epsilon,
  outer=1.0, log_points=4097) -> float`.
- Script outputs:
  `examples/dym_nonintegrability.csv` and
  `examples/dym_nonintegrability.png`.

- [ ] **Step 1: Write the exact mechanism test**

Create a test asserting:

```python
pde = dym_1d(alpha=2.0)
f_star = FNu(1.0, (0, 0, 0, 0))
singular = (
    FNu(1.0, (0, 0, 1, 0)),
    FNu(1.0, (1, 0, 0, 0)),
    Dx(2),
)
assert singular in pde.mechanism.tuples(f_star)
assert pde.mechanism.terminal(singular[0], pde, 1.25) == pytest.approx(-0.5)
assert pde.mechanism.terminal(singular[1], pde, 2.0) == pytest.approx(16.0)
```

- [ ] **Step 2: Run the test to verify failure only at the missing helper**

The tuple and terminal assertions must already pass against repository code.
Add an import of `truncated_normal_inverse_power`; expected failure is only
`ModuleNotFoundError: parabolab.integrability`.

- [ ] **Step 3: Implement the deterministic truncated integral**

For \(X\sim N(\mu,\sigma^2)\), compute

\[
\int_{\varepsilon<|x|<R}|x|^{-a}g_{\mu,\sigma}(x)\,dx
\]

on a logarithmic grid \(x=e^u\):

\[
\int_{\log\varepsilon}^{\log R}
\left[g(e^u)+g(-e^u)\right]e^{(1-a)u}\,du.
\]

Validate `std > 0`, `power > 0`, `0 < epsilon < outer`, and an odd
`log_points >= 257`. Use `numpy.trapezoid`; do not add SciPy.

- [ ] **Step 4: Test the logarithmic coefficient**

For `power=1`, two cutoffs separated by a factor \(100\) satisfy:

\[
I(\varepsilon/100)-I(\varepsilon)
\longrightarrow 2g_{\mu,\sigma}(0)\log 100.
\]

Use sufficiently small cutoffs and assert relative error below \(10^{-3}\).
Also test monotone growth for power \(4/3\).

- [ ] **Step 5: Build the reproducible script**

The script must:

```text
1. print the exact singular tuple and alpha-dependent constants;
2. evaluate cutoffs 1e-1 through 1e-12;
3. write raw deterministic integral values to CSV;
4. plot the inverse-first-power integral against log(1/epsilon);
5. overlay the theoretical asymptotic slope 2*g(0);
6. label the inverse-4/3 integral as a stronger sibling singularity;
7. state in the caption that this corroborates, but does not prove, the
   tree nonintegrability theorem.
```

- [ ] **Step 6: Run focused verification**

```bash
conda run -n parabolab python -m pytest tests/test_integrability.py -q
conda run -n parabolab python examples/dym_nonintegrability.py
```

Expected: tests pass and both ignored example outputs are created.

- [ ] **Step 7: Commit source only**

```bash
git add parabolab/integrability.py parabolab/__init__.py \
  tests/test_integrability.py examples/dym_nonintegrability.py
git commit -m "feat: verify Dym singular moment divergence numerically"
```

Do not force-add the generated CSV or PNG.

---

### Task 6: Proposal Optimization and Pilot/Freeze Theorem

**Owner:** GPT mathematical proof.

**Files:**
- Create: `docs/research/estimator-integrity/adaptive-proposals.md`.

**Interfaces:**
- Produces: `Theorem 6.1` finite tuple optimizer.
- Produces: `Theorem 6.2` leaf/branch-time event optimizer.
- Produces: `Theorem 6.3` pilot/freeze unbiasedness.
- Produces: `Theorem 6.4` finite-depth multiplicative oracle inequality.
- Consumed by: Tasks 7, 8, 9, and 11.

- [ ] **Step 1: Prove the finite tuple optimizer**

For \(A_i>0\) and \(q_i>0\), \(\sum_iq_i=1\), prove:

\[
J(q)=\sum_i\frac{A_i}{q_i}
\ge
\left(\sum_i\sqrt{A_i}\right)^2,
\]

with equality exactly at

\[
q_i^*=\frac{\sqrt{A_i}}{\sum_j\sqrt{A_j}}.
\]

Use Cauchy--Schwarz on
\(\sqrt{A_i/q_i}\) and \(\sqrt{q_i}\). Treat \(A_i=0\) by exact pruning or
by a positive floor; do not silently assign zero probability to an
unverified branch.

- [ ] **Step 2: Prove the first-event optimizer**

For leaf contribution \(A_0\), leaf probability \(r_0\), branch contribution
density \(A(s)\), and branch density \(r(s)\), prove:

\[
\frac{A_0}{r_0}+\int_0^\Delta\frac{A(s)}{r(s)}\,ds
\ge
\left(\sqrt{A_0}+\int_0^\Delta\sqrt{A(s)}\,ds\right)^2.
\]

State the equality proposal. Explicitly distinguish this fixed-horizon event
proposal from optimizing within the one-parameter exponential family.

- [ ] **Step 3: Prove pilot/freeze unbiasedness**

Let \(\mathcal P\) be the pilot sigma-field and let
\(\widehat q\) be \(\mathcal P\)-measurable with full live support. Evaluation
trees are conditionally independent of pilot randomness and carry exact
likelihood ratios. Prove:

\[
\mathbb E[\widehat H\mid\mathcal P]=u,
\qquad
\mathbb E\widehat H=u.
\]

List the required conditional integrability. Explain why adapting a proposal
from the same continuation realization without a correct joint likelihood
ratio is not covered.

- [ ] **Step 4: Prove the oracle ratio**

If pilot estimates satisfy

\[
(1-\eta)A_i\le\widehat A_i\le(1+\eta)A_i,
\qquad 0<\eta<1,
\]

then the square-root proposal obeys:

\[
\frac{\widehat q_i}{q_i^*}
\in
\left[
\sqrt{\frac{1-\eta}{1+\eta}},
\sqrt{\frac{1+\eta}{1-\eta}}
\right].
\]

Therefore:

\[
J(\widehat q)
\le
\sqrt{\frac{1+\eta}{1-\eta}}\,J(q^*).
\]

For the support-preserving mixture
\(\widetilde q=(1-\varepsilon)\widehat q+\varepsilon/m\),
prove:

\[
J(\widetilde q)
\le
\frac1{1-\varepsilon}
\sqrt{\frac{1+\eta}{1-\eta}}\,J(q^*).
\]

Combining this deterministic implication with a pilot concentration event
gives the finite-depth high-probability oracle statement.

- [ ] **Step 5: Separate variance from cost**

Because the target mean is proposal invariant, minimizing second moment
minimizes variance. Expected tree size may change under time proposals, so
variance times expected node count is an empirical efficiency criterion, not
part of the tuple-only theorem.

- [ ] **Step 6: Commit**

```bash
git add docs/research/estimator-integrity/adaptive-proposals.md
git commit -m "docs: prove safe adaptive branching proposal bounds"
```

---

### Task 7: Nonuniform Tuple Proposal API

**Owner:** Gemini Python implementation.

**Files:**
- Create: `parabolab/proposals.py`.
- Modify: `parabolab/tree.py`.
- Modify: `parabolab/mc.py`.
- Modify: `parabolab/__init__.py`.
- Modify: `tests/test_tree.py`.
- Create: `tests/test_proposals.py`.

**Interfaces:**
- `TupleProposal = Callable[[Code, float, object, float, int, tuple],
  Sequence[float]]`, with arguments `(code, t, x, tau, depth, tuples)`.
- `sqrt_optimal_probabilities(contributions, *, floor_mass=0.0) -> np.ndarray`.
- `second_moment_objective(contributions, probabilities) -> float`.
- `oracle_ratio_bound(relative_error, floor_mass=0.0) -> float`.
- `FrozenTupleProposal(probabilities_by_key:
  Mapping[tuple[int, Code], tuple[float, ...]])`.
- `sample_tree(pde, t, x, *, rng, rate=None, code=Id(), mechanism=None,
  prune_zero=True, max_depth=None,
  tuple_proposal: TupleProposal | None = None) -> TreeSample`.
- `estimate(pde, t, x, n_samples, *, rng=None, seed=None, rate=None,
  code=Id(), mechanism=None, prune_zero=True, max_depth=None,
  tuple_proposal: TupleProposal | None = None) -> MCResult`.

- [ ] **Step 1: Write pure optimizer tests**

Create:

```python
def test_sqrt_proposal_attains_cauchy_schwarz_bound():
    a = np.array([1.0, 9.0, 4.0])
    q = sqrt_optimal_probabilities(a)
    np.testing.assert_allclose(q, [1 / 6, 3 / 6, 2 / 6])
    assert second_moment_objective(a, q) == pytest.approx(36.0)
    assert second_moment_objective(a, np.full(3, 1 / 3)) == pytest.approx(42.0)


def test_floor_is_a_convex_uniform_mixture():
    q = sqrt_optimal_probabilities([1.0, 9.0], floor_mass=0.2)
    np.testing.assert_allclose(q, 0.8 * np.array([0.25, 0.75]) + 0.1)
    assert q.sum() == pytest.approx(1.0)
    assert np.all(q > 0)
```

- [ ] **Step 2: Run tests to verify import failure**

```bash
conda run -n parabolab python -m pytest tests/test_proposals.py -q
```

Expected: import failure because `parabolab.proposals` does not exist.

- [ ] **Step 3: Implement validated pure functions**

Reject:

```text
empty arrays;
negative or nonfinite contributions;
all-zero contributions;
partially zero contributions when floor_mass == 0;
probabilities that are nonpositive, nonfinite, wrong-length, or do not sum
to one within 1e-12;
floor_mass outside [0, 1).
```

Use the uniform mixture
\((1-\varepsilon)q+\varepsilon/m\), where `floor_mass` is
\(\varepsilon\), not a per-coordinate floor.

- [ ] **Step 4: Add a failing weighted-tree test**

Extend `FakeRng` only in a subclass with:

```python
def choice(self, n, p):
    self.last_probabilities = np.asarray(p)
    return self.integers_q.pop(0)
```

Force the existing two-generation Allen--Cahn tree to choose tuple index one
with proposal probabilities `(0.9, 0.1)`. The expected interior multiplier at
that node is:

```python
(1.0 / 0.1) * math.exp(rate * tau) / rate
```

instead of `2.0 * exp(rate*tau) / rate`.

- [ ] **Step 5: Implement the proposal branch without changing defaults**

When `tuple_proposal is None`, retain the current integer draw and
`len(tuples)` multiplier exactly. Otherwise:

```python
probabilities = validate_probabilities(
    tuple_proposal(code, t, x, tau, depth, tuples), len(tuples)
)
index = int(rng.choice(len(tuples), p=probabilities))
inverse_q = 1.0 / probabilities[index]
```

The callback is evaluated before the shared branch mark, matching the current
sampling order. It may depend on the code, birth time, birth state, lifetime,
and generation depth, but not on the not-yet-sampled branch position.
Multiply the interior factor by `inverse_q / rho(tau)`.

- [ ] **Step 6: Verify default RNG reproducibility**

```bash
conda run -n parabolab python -m pytest \
  tests/test_tree.py::test_hand_computed_tree_weight \
  tests/test_tree.py::test_rng_reproducibility \
  tests/test_tree.py::test_max_depth_zero_kills_a_root_branch_without_extra_draws \
  -q
```

Expected: all pass.

- [ ] **Step 7: Test proposal-invariant means on a finite-depth control**

Use the same finite-depth toy model under uniform and skewed full-support
proposals. Generate independent samples and assert both estimates are within
five valid standard errors of the deterministic truncated target. Do not
require the two independent estimates to match each other exactly.

- [ ] **Step 8: Export and run focused tests**

```bash
conda run -n parabolab python -m pytest \
  tests/test_tree.py tests/test_moments.py tests/test_proposals.py -q
```

Expected: all selected tests pass.

- [ ] **Step 9: Commit**

```bash
git add parabolab/proposals.py parabolab/tree.py parabolab/mc.py \
  parabolab/__init__.py tests/test_tree.py tests/test_proposals.py
git commit -m "feat: add nonuniform coding-tree tuple proposals"
```

---

### Task 8: Pilot Estimation and Merton--Vasicek Proposal Study

**Owner:** Gemini Python implementation and execution.

**Files:**
- Modify: `parabolab/proposals.py`.
- Modify: `tests/test_proposals.py`.
- Create: `examples/proposal_merton_vasicek.py`.

**Interfaces:**
- `TuplePilotResult(contributions, stderr, n_samples, continuation_depth)`.
- `estimate_tuple_contributions(pde, t, x, code, *, n_samples, seed,
  rate, continuation_depth, mechanism=None) -> TuplePilotResult`.
- Script outputs:
  `examples/proposal_merton_vasicek.csv` and
  `examples/proposal_merton_vasicek.png`.

- [ ] **Step 1: Write a pilot estimator test**

For each labelled tuple \(Z\), the pilot target is:

\[
B_Z
=
\int_0^{T-t}\frac1{\rho(s)}
\mathbb E\left[
\left|\prod_{z\in Z}H_z^{[d]}(t+s,X_s)\right|^2
\right]ds.
\]

Use a one-state finite-depth mechanism with analytically known child factors.
Assert that each estimated \(B_Z\) lies within five empirical pilot standard
errors of its exact value and that the resulting square-root proposal matches
the analytic optimizer.

- [ ] **Step 2: Run the test to verify missing interface**

```bash
conda run -n parabolab python -m pytest \
  tests/test_proposals.py -k pilot -q
```

Expected: import or attribute failure for `estimate_tuple_contributions`.

- [ ] **Step 3: Implement pilot sampling**

For every tuple and pilot draw:

```text
1. draw s uniformly on (0, remaining);
2. draw one shared branch position using the PDE diffusion;
3. independently sample each child killed tree at continuation_depth;
4. multiply child values;
5. record remaining * abs(product)^2 / rho(s).
```

Use `numpy.random.SeedSequence(seed).spawn(number_of_tuples)` so tuple estimates
have documented independent streams. Return sample means and standard errors.
If nonfinite pilot observations occur, return them and fail proposal
construction explicitly; never delete them.

- [ ] **Step 4: Test pilot/freeze stream separation**

Build the proposal with pilot seed 101 and evaluate with seed 202. Add a test
that changing only the evaluation seed leaves the frozen probabilities
identical, while changing the pilot seed may change them.

- [ ] **Step 5: Build the finance experiment**

Use:

```python
pde = merton_vasicek_reduced(T=0.05, consumption=False)
state = np.array([0.0])
target_code = StateFNu(
    1.0,
    beta=(0,),
    nu=(0, 0),
)
```

Study `target_code`, the unique `StateFNu` child directly below `Id()`.
Estimate a code-only proposal from killed continuations of depths 0, 1, and 2.
Freeze each proposal and apply it whenever a code compares equal to
`target_code` at generation depth one in otherwise unrestricted evaluation
trees; all other `(depth, code)` pairs use their uniform proposal. This keeps
the descendant proposal used by the pilot identical to the descendant
proposal used during evaluation.

Compare:

```text
uniform tuple proposal;
pilot/frozen proposal with floor_mass = 0.05;
the repository's two representative exponential rates.
```

Use three pilot seeds and five disjoint evaluation seeds. Report the exact
no-consumption value, empirical mean, empirical second moment, maximum
absolute observation, mean/max nodes, and empirical variance times mean
nodes. Label standard errors as formal confidence intervals only after the
moment theorem or an explicit dominating bound certifies \(L^2\) for the
chosen setting.

- [ ] **Step 6: Add truncation and proposal diagnostics**

The CSV must include:

```text
pilot_seed, evaluation_seed, rate, continuation_depth, floor_mass,
tuple_label, proposal_probability, estimate, empirical_second_moment,
max_abs, mean_nodes, max_nodes, variance_times_mean_nodes
```

The plot must show cost-adjusted variance and proposal probabilities. It must
not show P&L, Sharpe ratio, or alpha language.

- [ ] **Step 7: Run focused and script verification**

```bash
conda run -n parabolab python -m pytest tests/test_proposals.py -q
conda run --no-capture-output -n parabolab \
  python examples/proposal_merton_vasicek.py \
  --pilot-samples 2000 --evaluation-samples 10000
```

Expected: tests pass; CSV and PNG are produced; no sample is removed.

- [ ] **Step 8: Commit source only**

```bash
git add parabolab/proposals.py tests/test_proposals.py \
  examples/proposal_merton_vasicek.py
git commit -m "feat: add pilot-frozen proposal experiment"
```

---

### Task 9: Lean Project and Moment Iteration

**Owner:** GPT mathematical proof in Lean.

**Files:**
- Create: `formal/lean-toolchain`.
- Create: `formal/lakefile.lean`.
- Create: `formal/EstimatorIntegrity.lean`.
- Create: `formal/EstimatorIntegrity/FiniteTree.lean`.
- Create: `formal/EstimatorIntegrity/MomentIteration.lean`.

**Interfaces:**
- `FiniteMechanism C`.
- `MomentVector C := C -> ENNReal`.
- `momentStep`.
- `picard`.
- Theorems:
  `momentStep_mono`, `picard_mono`, `picard_le_prefixed`,
  `picard_iSup_least`, and `momentStep_iSup_picard`.

- [ ] **Step 1: Pin the toolchain**

Write `formal/lean-toolchain`:

```text
leanprover/lean4:v4.33.0
```

Write `formal/lakefile.lean`:

```lean
import Lake
open Lake DSL

package «estimator-integrity» where
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.33.0"

@[default_target]
lean_lib EstimatorIntegrity
```

- [ ] **Step 2: Resolve dependencies**

Run:

```bash
cd formal
lake update
lake exe cache get
lake build
```

Expected: dependency resolution and an empty library build succeed.

- [ ] **Step 3: Define labelled finite mechanisms**

Use lists rather than finite sets so duplicate labelled tuples are retained:

```lean
structure FiniteMechanism (C : Type*) where
  tuples : C → List (List C)
  nonempty_tuples : ∀ c, (tuples c).Nonempty
```

Define a tuple product over a moment vector and a branch coefficient indexed
by the tuple's `Fin` position. Do not quotient duplicate lists.

- [ ] **Step 4: Define the moment operator**

For `[Fintype C] [DecidableEq C]`, define:

```lean
abbrev MomentVector (C : Type*) := C → ENNReal

def momentStep
    (M : FiniteMechanism C)
    (leaf : MomentVector C)
    (branch : (c : C) → Fin (M.tuples c).length → ENNReal)
    (v : MomentVector C) : MomentVector C :=
  fun c =>
    leaf c +
      ∑ i : Fin (M.tuples c).length,
        branch c i * (((M.tuples c).get i).map v).prod
```

The body is the leaf term plus the finite sum of branch coefficient times the
product of child components.

- [ ] **Step 5: Prove monotonicity one tactic at a time**

Target:

```lean
theorem momentStep_mono
    (hvw : ∀ c, v c ≤ w c) :
    ∀ c, momentStep M leaf branch v c ≤
      momentStep M leaf branch w c := by
```

After each tactic, run:

```bash
lake env lean EstimatorIntegrity/MomentIteration.lean
```

Use `done` whenever further goals are expected. Stop after the first syntax or
type error and fix it before adding another tactic.

- [ ] **Step 6: Prove Picard monotonicity and leastness**

Define:

```lean
def picard
    (M : FiniteMechanism C)
    (leaf : MomentVector C)
    (branch : (c : C) → Fin (M.tuples c).length → ENNReal) :
    Nat → MomentVector C
  | 0 => fun _ => 0
  | n + 1 => momentStep M leaf branch (picard M leaf branch n)
```

Prove:

```lean
theorem picard_mono : Monotone (picard M leaf branch)

theorem picard_le_prefixed
    (hw : ∀ c, momentStep M leaf branch w c ≤ w c) :
    ∀ n c, picard M leaf branch n c ≤ w c

theorem picard_iSup_least
    (hw : ∀ c, momentStep M leaf branch w c ≤ w c) :
    (fun c => ⨆ n, picard M leaf branch n c) ≤ w
```

- [ ] **Step 7: Prove fixed-point continuity**

Prove `momentStep_iSup_picard` by commuting the increasing supremum through
each finite `Fin` sum and each finite child list product. Prove the list
product lemma first by induction, using diagonal cofinality of the common
Picard index for two increasing ENNReal sequences. This theorem has no
finiteness assumption on the limit: zero and infinity cases remain in
`ENNReal`, and no ring-style subtraction is used.

- [ ] **Step 8: Build and scan**

```bash
cd formal
lake build
rg -n "\bsorry\b|admit|axiom" EstimatorIntegrity*.lean EstimatorIntegrity
```

Expected: build succeeds and search returns no proof placeholders or
project-defined axioms.

- [ ] **Step 9: Commit**

```bash
git add formal
git commit -m "proof: formalize finite moment iteration"
```

---

### Task 10: Lean Proposal and Dym Core

**Owner:** GPT mathematical proof in Lean.

**Files:**
- Create: `formal/EstimatorIntegrity/Proposal.lean`.
- Create: `formal/EstimatorIntegrity/Dym.lean`.
- Modify: `formal/EstimatorIntegrity.lean`.

**Interfaces:**
- `secondMomentObjective`.
- `sqrtProposal`.
- `secondMoment_ge_oracle`.
- `oracle_ratio_of_relative_error`.
- `dymFz0`.
- singular-integral divergence theorem on a positive interval.

- [ ] **Step 1: Formalize the finite proposal objective**

For `A q : Fin n → ℝ`, state:

```lean
def secondMomentObjective (A q : Fin n → ℝ) : ℝ :=
  ∑ i, A i / q i

def sqrtProposal (A : Fin n → ℝ) (i : Fin n) : ℝ :=
  Real.sqrt (A i) / ∑ j, Real.sqrt (A j)
```

Require `0 < A i` and `0 < q i`, and normalize `q`.

- [ ] **Step 2: Prove the optimizer via Euclidean Cauchy--Schwarz**

Apply Cauchy--Schwarz to the finite vectors
\(\sqrt{A_i/q_i}\) and \(\sqrt{q_i}\). Target:

```lean
theorem secondMoment_ge_oracle
    (hA : ∀ i, 0 < A i)
    (hq : ∀ i, 0 < q i)
    (hqsum : ∑ i, q i = 1) :
    (∑ i, Real.sqrt (A i)) ^ 2 ≤ secondMomentObjective A q := by
```

Prove separately that `sqrtProposal` sums to one and attains equality.

- [ ] **Step 3: Formalize the deterministic oracle ratio**

Encode
\((1-\eta)A_i\le\widehat A_i\le(1+\eta)A_i\) and prove the componentwise
proposal-ratio bounds followed by:

```lean
secondMomentObjective A qHat
  ≤ Real.sqrt ((1 + η) / (1 - η))
      * secondMomentObjective A (sqrtProposal A)
```

Formalize the uniform-mixture floor as a second theorem.

- [ ] **Step 4: Formalize the Dym coefficient algebra**

The paper proof owns the `Real.rpow` calculus. Lean verifies the exact
coefficient simplification used after those derivative formulas:

```lean
theorem dym_fz0_coefficient
    (C α x : ℝ) (hx : x ≠ 0) (hC : C ^ 3 = 9 * α ^ 2) :
    (3 * C ^ 2 * (8 * C / 27)) / x = 8 * α ^ 2 / x := by
```

Prove it by field normalization and `hC`. Do not label this lemma as a
formalized derivative theorem.

- [ ] **Step 5: Formalize singular divergence**

Prove that the nonnegative integral of \(1/x\) on every `(0, ε)` with
`ε > 0` is infinite by partitioning it into the disjoint dyadic intervals
\((\varepsilon/2^{n+1},\varepsilon/2^n]\), each contributing \(\log 2\).
Then prove that a continuous density positive at zero is bounded below on a
small interval, so multiplying by that density preserves nonintegrability.

- [ ] **Step 6: Verify one tactic at a time**

After every tactic:

```bash
cd formal
lake env lean EstimatorIntegrity/Proposal.lean
lake env lean EstimatorIntegrity/Dym.lean
```

Fix syntax, then type errors, then unsolved goals, then linter warnings. Use
`done` to expose remaining goals. Clean each completed proof immediately.

- [ ] **Step 7: Build and scan**

```bash
cd formal
lake build
rg -n "\bsorry\b|admit|axiom" EstimatorIntegrity*.lean EstimatorIntegrity
```

Expected: successful build and no placeholders or project-defined axioms.

- [ ] **Step 8: Commit**

```bash
git add formal
git commit -m "proof: formalize proposal and Dym core lemmas"
```

---

### Task 11: Seven Secondary Candidate Results

**Owner:** GPT mathematical analysis; Gemini runs any supporting Python
commands explicitly requested by the note.

**Files:**
- Create:
  `docs/research/estimator-integrity/secondary-candidates.md`.

**Interfaces:**
- Produces a fixed seven-entry claim ledger:
  state-dependent coding, Sobolev derivative labels, robust regression,
  multifidelity control variates, coefficient sensitivities, challenger-model
  selection, and short-time wave proposal optimization.

- [ ] **Step 1: Use one fixed template per candidate**

Each entry contains:

```text
Precise statement
Minimal assumptions
Status
Proof or proof route
Decisive obstruction/counterexample
Closest prior art
Numerical falsification test
Quant-research relevance
```

- [ ] **Step 2: Prove the derivable algebraic/statistical statements**

Provide complete proofs for:

```text
the Sobolev population-risk decomposition;
the control-variate optimal beta formula;
the finite-candidate challenger-model 2r oracle inequality;
the finite-tree coefficient-count sensitivity identity;
the short-time wave leading-order optimizer, excluding phi(z)=0.
```

- [ ] **Step 3: Keep conditional mechanisms conditional**

The state-dependent arbitrary-jet result must retain classical-solution,
integrability, nonexplosion, and infinite-system uniqueness hypotheses.
Robust regression must state the exact moment assumption and any target bias.
The multifidelity \(O(\varepsilon^2/N)\) claim remains conjectural until an
\(L^2\) coupling estimate is proved.

- [ ] **Step 4: Record prior-art overlap**

Cite at least:

```text
Nguwi--Penent--Privault (JEQ 2023), DOI 10.1007/s00028-023-00873-3;
Nguwi--Penent--Privault (JCP 2024), DOI 10.1016/j.jcp.2023.112712;
Henry-Labordere et al. (2019), DOI 10.1214/17-AIHP880;
Huang--Privault (2025), arXiv:2502.17853;
Czarnecki et al. (2017), arXiv:1706.04859;
Huge--Savine (2020), arXiv:2005.02347.
```

- [ ] **Step 5: Commit**

```bash
git add docs/research/estimator-integrity/secondary-candidates.md
git commit -m "docs: assess seven estimator integrity extensions"
```

---

### Task 12: Reproducibility, Full Verification, and Research Canvas

**Owner:** Gemini for all commands, plots, and Canvas code; GPT audits proofs
and claim wording.

**Files:**
- Create:
  `docs/research/estimator-integrity/reproducibility.md`.
- Create outside the repository:
  `/Users/michael/.cursor/projects/Users-michael-Desktop-NTU-fyp/canvases/branching-estimator-integrity.canvas.tsx`.

**Interfaces:**
- Produces: one command ledger with actual outputs and hashes.
- Produces: standalone Canvas with the ten claims, proof status, equations,
  numerical evidence, prior-art risk, and twelve-week roadmap.

- [ ] **Step 1: Write the reproducibility ledger**

Record:

```text
git revision;
Conda environment name and Python/package versions;
Lean and Mathlib pins;
every test/experiment command;
all fixed seeds;
generated CSV/PNG paths;
which claims use each numerical output;
which outputs are empirical diagnostics rather than proofs.
```

- [ ] **Step 2: Run the complete Python suite**

```bash
cd /Users/michael/Desktop/NTU/fyp/parabolab-estimator-integrity
PYTHONDONTWRITEBYTECODE=1 conda run --no-capture-output -n parabolab \
  python -m pytest -m "slow or not slow" -p no:cacheprovider
```

Expected: zero failures. Record the exact count and elapsed time.

- [ ] **Step 3: Run both research experiments**

```bash
conda run --no-capture-output -n parabolab \
  python examples/dym_nonintegrability.py

conda run --no-capture-output -n parabolab \
  python examples/proposal_merton_vasicek.py \
  --pilot-samples 10000 --evaluation-samples 100000
```

Expected: finite deterministic Dym cutoff outputs, unfiltered proposal
samples, and reproducible CSV/PNG files.

- [ ] **Step 4: Run Lean verification**

```bash
cd formal
lake build
rg -n "\bsorry\b|admit|axiom" EstimatorIntegrity*.lean EstimatorIntegrity
```

Expected: build succeeds; search has no matches.

- [ ] **Step 5: Audit claims against evidence**

GPT rereads all three proof notes and the secondary ledger. For each claim,
record exactly one status and the evidence path. Downgrade any theorem whose
support, integrability, measurability, or uniformity assumption remains
unproved.

- [ ] **Step 6: Build the Canvas**

Gemini reads the Canvas skill and SDK declarations before creating the file.
Embed all data inline; do not fetch. The Canvas must include:

```text
one prominent thesis conclusion;
three deep-result panels with theorem/proof status;
seven compact candidate rows;
a proof-dependency diagram;
the Dym cutoff plot with axes, units, source, and asymptotic label;
the proposal variance-per-node comparison;
the Merton--Vasicek benchmark;
prior-art and overclaim warnings;
the twelve-week roadmap and reproducibility commands.
```

Use host theme tokens only. No gradients, emoji, shadows, rainbow colors, or
wall of identical cards. Omit sections whose verified data do not exist.

- [ ] **Step 7: Verify Canvas diagnostics**

Expected from the file edit: `Canvas TypeScript check: no errors`. Open it
beside chat and visually verify hierarchy, labels, captions, and no empty
states.

- [ ] **Step 8: Commit repository documentation**

```bash
git add docs/research/estimator-integrity/reproducibility.md
git commit -m "docs: finalize estimator integrity reproducibility"
git status --short
```

Expected: only ignored generated example outputs; no tracked modifications.

- [ ] **Step 9: Final handoff**

Report:

```text
three theorem statuses;
Lean build result and placeholder scan;
Python test count;
key Dym numerical asymptotic;
proposal efficiency result;
finance benchmark result;
the seven secondary statuses;
commit range;
Canvas link;
remaining publication-novelty caveat.
```

Do not say “breakthrough” unless a later expert literature review supports it.

---

## Original execution order and gates (historical)

1. Task 1 must complete before any file implementation.
2. Tasks 2 and 4 may proceed as mathematical work once the clean worktree
   exists.
3. Task 3 depends on Task 2's definitions.
4. Task 5 depends on Task 4's exact constants.
5. Task 6 precedes Tasks 7 and 8.
6. Task 9 starts after Task 2's finite model is stable.
7. Task 10 starts after Tasks 4 and 6 are mathematically complete.
8. Task 11 may run after the three deep theorem statements are frozen.
9. Task 12 is the only completion gate.

The original session blocked Python tasks 1, 3, 5, 7, 8, and 12 until
Gemini was available. That session-specific ownership gate is inactive; it
does not constrain present work.
