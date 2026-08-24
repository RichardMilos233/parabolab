# Demo

One PDE per script, in the style of `wavelab/examples`: define the
equation, solve it, print a table, save a figure.

```bash
python demo/allen_cahn.py    # Allen-Cahn d=1   (JCP2024 Table 1 / Fig. 1)
python demo/merton.py        # Merton HJB d=1   (JCP2024 eq. (4.6), Table 5)
```

Each takes about a second. Figures land next to the script.

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

Only the first is run by default. **Coding-tree Monte Carlo is a pointwise
expectation** — no training, no time-marching, no coupling between grid
points — so a whole profile costs about a second on a laptop CPU and
genuinely converges. The table reports `|estimate − exact| / stderr` at
every point; all values below 2 means the closed form is reproduced inside
the error bars, a self-contained statistical check that needs no reference
number.

The other three train a neural network and need real budgets (JCP2024
quotes 28–184 GPU-minutes per run). They are left commented out — the call
shapes are covered by `tests/test_solve.py`, but at a laptop budget their
curves would be undertrained and would say nothing about correctness.
Uncomment them on a fast machine.

**Paper-budget reproductions are not here.** They live in `../examples/`
(14 scripts covering JEQ Figs 1, 4–9 and Tables 2/5; JCP Tables 1/3/5 and
Fig. 7; the three-way baseline comparison; the blow-up study), with the
results collected in the top-level `README.md`.

## Why the scripts pass a factory, not a PDE

```python
pde = partial(allen_cahn_nd, d=1, T=0.5)     # not allen_cahn_nd(d=1, T=0.5)
```

PDE objects hold lambdified sympy callables and plain closures, so they
cannot be pickled — anything that fans work out to worker processes
(`CodingTreeMC(n_jobs>1)`, `DeepBranching`) needs the builder instead.
`.solve()` accepts either form and raises a `TypeError` naming the fix when
a solver that needs a factory is handed an instance.
