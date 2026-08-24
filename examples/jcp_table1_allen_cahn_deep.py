"""JCP2024 Table 1 / Fig 1: deep branching for Allen-Cahn (4.1), d=1 and 5.

Paper settings: T=0.5, x in [-8, 8], N=1000 states at t=0, M=100,000
tree samples per state, P=3000 epochs, 10 runs.  Paper (Tesla P100 GPU):
d=1 L1 1.32e-3 (SD 1.05e-4) in 28 min/run; d=5 L1 3.63e-3 (SD 1.57e-4)
in 110 min/run.

Default here: reduced M=10,000 and 3 runs.  --full for paper budgets.
"""

import argparse
import functools

from parabolab.library import allen_cahn_nd
import parabolab.deep as deep


PAPER = {1: ("1.32E-03", "1.05E-04", "28m"), 5: ("3.63E-03", "1.57E-04", "110m")}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dims", type=int, nargs="+", default=[1, 5])
    p.add_argument("--samples", type=int, default=10_000, help="M per state")
    p.add_argument("--states", type=int, default=1000, help="N states")
    p.add_argument("--epochs", type=int, default=3000)
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--jobs", type=int, default=6)
    p.add_argument("--device", default="cpu")
    p.add_argument("--full", action="store_true",
                   help="paper budget: M=100,000 and 10 runs")
    args = p.parse_args()
    if args.full:
        args.samples, args.runs = 100_000, 10

    for d in args.dims:
        factory = functools.partial(allen_cahn_nd, d=d, T=0.5)
        pl1, psd, prt = PAPER.get(d, ("-", "-", "-"))
        print(f"=== Allen-Cahn (4.1) deep branching, d={d}, T=0.5, "
              f"N={args.states}, M={args.samples}, P={args.epochs} ===")
        print(f"paper (M=100,000, 10 runs, GPU): "
              f"L1 {pl1} (SD {psd}), runtime {prt}/run")
        res = deep.run_experiment(
            factory, x_lo=-8.0, x_hi=8.0,
            n_states=args.states, m_samples=args.samples,
            epochs=args.epochs, n_runs=args.runs,
            n_jobs=args.jobs, device=args.device, seed0=10 * d,
        )
        print("ours:", res.summary())

        # figure in the style of JCP Fig 1 (net vs exact at t=0)
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        pde = factory()
        _, _, grid, pred, true = deep.grid_errors(
            res.nets[0], pde, x_lo=-8.0, x_hi=8.0, device=args.device)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(grid, true, "k-", label="exact")
        ax.plot(grid, pred, "--", color="tab:orange", label="Deep branching")
        ax.set_xlabel("$x$")
        ax.set_ylabel("$u(0, x)$")
        ax.set_title(f"JCP2024 Fig. 1: Allen-Cahn (4.1), d={d}, T=0.5 "
                     f"(run 0, M={args.samples})")
        ax.legend()
        fig.tight_layout()
        out = f"examples/jcp_fig1_allen_cahn_deep_d{d}.png"
        fig.savefig(out, dpi=150)
        plt.close(fig)
        print(f"figure saved to {out}\n", flush=True)
