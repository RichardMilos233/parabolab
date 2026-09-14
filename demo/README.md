# Demos

One PDE per script: define the equation, solve with multiple methods or
sampling settings, print a comparison table, and save a figure. This remains
the demo workflow as research improves the branching estimator through
`lambda` and `q_c(Z)`.

```bash
python demo/allen_cahn.py        # Allen-Cahn d=1 (JCP2024 Table 1 / Fig. 1)
python demo/variance_reduction.py # Allen-Cahn: baseline / selected rate / terminal q / both
python demo/merton.py            # Merton HJB d=1 (JCP2024 eq. (4.6), Table 5)
python demo/merton_vasicek.py     # retained stochastic-rate Merton example (d=1 reduced)
python demo/dym.py               # Dym non-integrability diagnostic (JEQ Fig. 6)
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

* **Coding-tree Monte Carlo** estimates a pointwise expectation
  ($\mathbb{E}[\mathcal{H}]$), when it exists, without neural-network training.
* **Deep Branching, Deep BSDE, and Deep Galerkin** fit neural networks. Their
  budgets and existing demo configurations remain available.

## Same solver, different sampling settings

`variance_reduction.py` uses the same `curves` list and `compare` call. It
selects two rates at `(t, x) = (0, 0)`, one with uniform tuple sampling and one
with a fixed `TerminalTupleProposal`, then compares four configurations:

- baseline: rate 1 and uniform tuples;
- selected rate and uniform tuples;
- rate 1 and the terminal-data tuple proposal;
- selected rate and the same terminal-data tuple proposal.

The only solver settings added are `rate=...`, `tuple_proposal=...`, and
`label=...`. Custom tuple proposals currently require `n_jobs=1`. The demo
prints setup/tuning time, sampling time, estimation errors, and average
empirical variance over the grid; the figure uses the existing error bars.

Rate selection uses a finite-depth quadrature objective. The selected rate
is reused across the grid and is not a pointwise optimum everywhere. The tuple
proposal uses terminal data, not exact child second moments. These are
estimation algorithms to evaluate, not guaranteed improvements on every PDE.
For node counts and pointwise variance-times-work diagnostics, use
[`examples/sampling_tuning.py`](../examples/sampling_tuning.py).

The original Merton demos remain benchmarks. Multifactor Merton is no longer
the active research roadmap. Dym is a negative control: its specified
real-extension estimator is non-integrable for every positive rate, so its
finite-sample curves and displayed errors are not convergence evidence.

## Historical example runs

These previously recorded runs illustrate the network solvers; errors and
runtimes depend on the environment, seed, and budget.

| PDE | Method | $L_1$ Error | Runtime |
|---|---|---|---|
| Allen-Cahn $d=1$ | Deep Branching | 1.89e-03 | 22 s |
| | Deep BSDE | 5.68e-03 | 50 s |
| | Deep Galerkin | 5.31e-03 | 35 s |
| Merton HJB $d=1$ | Deep Branching | 1.12e-02 | 22 s |
| Merton Vasicek $d=1$ | Deep Branching | 6.89e-04 | 6 s |

Full multi-run paper reproduction scripts are located in `examples/`.
The [research guide](../docs/research/README.md) records current claims,
implementation limits, and next steps.
