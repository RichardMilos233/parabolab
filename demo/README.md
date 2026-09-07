# Demos

One PDE per script: define the equation, solve with multiple methods, print a comparison table, and save a figure.

```bash
python demo/allen_cahn.py        # Allen-Cahn d=1 (JCP2024 Table 1 / Fig. 1)
python demo/merton.py            # Merton HJB d=1 (JCP2024 eq. (4.6), Table 5)
python demo/merton_vasicek.py    # Merton HJB with Vasicek stochastic rate (d=1 reduced)
```

Figures land next to the scripts.

## One PDE, several methods

The scripts use the uniform solver interface (`parabolab.solve`). Every solver implements `Solver(**budget).solve(pde, grid) -> Curve`, so comparing or toggling methods is straightforward:

```python
curves = [
    CodingTreeMC(n_samples=10_000, seed=0).solve(pde, grid),
    DeepBranching(n_states=1000, m_samples=10_000, epochs=3000, n_jobs=8).solve(pde, grid),
    DeepBSDE(epochs=3000, n_states=1000).solve(pde, grid),
    DeepGalerkin(epochs=3000, n_states=1000).solve(pde, grid),
]
compare(pde, *curves).table().plot("out.png")
```

* **Coding-tree Monte Carlo** is a pointwise expectation ($\mathbb{E}[\mathcal{H}]$) — no training, no time-marching, and converges in seconds.
* **Deep Branching, Deep BSDE, and Deep Galerkin** fit neural networks. All run at paper budgets (3000 epochs) in under a minute on CPU.

| PDE | Method | $L_1$ Error | Runtime |
|---|---|---|---|
| Allen-Cahn $d=1$ | Deep Branching | 1.89e-03 | 22 s |
| | Deep BSDE | 5.68e-03 | 50 s |
| | Deep Galerkin | 5.31e-03 | 35 s |
| Merton HJB $d=1$ | Deep Branching | 1.12e-02 | 22 s |
| Merton Vasicek $d=1$ | Deep Branching | 6.89e-04 | 6 s |

Full multi-run paper reproduction scripts are located in `examples/`.
