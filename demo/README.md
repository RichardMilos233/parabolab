# Demo

One PDE per script, in the style of `wavelab/examples`: define the
equation, solve it, print a table, save a figure.

```bash
python demo/allen_cahn.py    # Allen-Cahn d=1   (JCP2024 Table 1 / Fig. 1)
python demo/merton.py        # Merton HJB d=1   (JCP2024 eq. (4.6), Table 5)
```

Each takes about a second. Figures land next to the script.

Add `--deep` to either script to bring in the neural-network methods at
the paper's own budget (N = 1000, M = 10 000, 3000 epochs):

```bash
python demo/allen_cahn.py --deep    # + deep branching, deep BSDE, deep Galerkin
python demo/merton.py --deep        # + deep branching
```

## One PDE, several methods

The scripts use the package's uniform solver interface
(`parabolab/solve.py`) — every method is
`Solver(**budget).solve(pde, grid) -> Curve`, so swapping one for another
is a one-line edit:

```python
mc   = CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid)
deep = DeepBranching(n_states=1000, m_samples=10_000, epochs=3000).solve(pde, grid)
bsde = DeepBSDE(epochs=3000, n_states=1000).solve(pde, grid)
dgm  = DeepGalerkin(epochs=3000, n_states=1000).solve(pde, grid)
compare(pde, mc, deep, bsde, dgm).table().plot("out.png")
```

Only the first runs by default. **Coding-tree Monte Carlo is a pointwise
expectation** — no training, no time-marching, no coupling between grid
points — so a whole profile costs about a second on a laptop CPU and
genuinely converges. The table reports `|estimate − exact| / stderr` at
every point; all values below 2 means the closed form is reproduced inside
the error bars, a self-contained statistical check that needs no reference
number.

The other three train a network, so they are behind `--deep` rather than
on by default. They are not, however, expensive here. Measured on one
laptop CPU (Ryzen 9 7945HX, 16 cores, `n_jobs=8`, torch 2.13 CPU build),
at the budgets above:

| PDE | method | L1 | wall clock |
|---|---|---|---|
| Allen-Cahn d=1 | deep branching | 1.89e-03 | 22 s |
| | deep BSDE | 5.68e-03 | 50 s |
| | deep Galerkin | 5.31e-03 | 35 s |
| Merton HJB d=1 | deep branching | 1.12e-02 | 22 s |

JCP2024 quotes 28–184 GPU-minutes for the same runs. The gap is the
sampler, not the hardware: our tree samples come from the M3
reduced-mechanism sympy sampler over worker processes rather than the
authors' torch autograd sampler over the raw mechanism (CLAUDE.md gotcha
25b). A GPU is not worth reaching for — the nets are 6 × 20 neurons
trained full batch, and the expensive half of the work is numpy.

**Paper-budget reproductions are not here.** They live in `../examples/`
(14 scripts covering JEQ Figs 1, 4–9 and Tables 2/5; JCP Tables 1/3/5 and
Fig. 7; the three-way baseline comparison; the blow-up study), with the
results collected in the top-level `README.md`. `--deep` gives you one
run; those scripts give you the multi-run L1/L2 statistics the tables
report.

## Why the scripts pass a factory, not a PDE

```python
pde = partial(allen_cahn_nd, d=1, T=0.5)     # not allen_cahn_nd(d=1, T=0.5)
```

PDE objects hold lambdified sympy callables and plain closures, so they
cannot be pickled — anything that fans work out to worker processes
(`CodingTreeMC(n_jobs>1)`, `DeepBranching`) needs the builder instead.
`.solve()` accepts either form and raises a `TypeError` naming the fix when
a solver that needs a factory is handed an instance.

## Why the `if __name__ == "__main__":` guard

`DeepBranching` generates its training data in a `ProcessPoolExecutor`.
Under the spawn start method (Windows, macOS) each worker re-imports the
script it was launched from, so without the guard the pool spawns
recursively. Every script in `../examples/` has one for the same reason.
