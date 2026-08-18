"""JCP2024 Table 3: deep branching for the exponential nonlinearity (4.2), d=1.

Paper settings: T=0.05, alpha=10, x in [-4, 4], N=1000 states at t=0,
M=30,000 samples per state, P=3000 epochs, 10 runs.  Paper (P100 GPU):
d=1 L1 1.17e-2 (SD 1.36e-3) in 42 min/run.

Default here: reduced M=3,000 and 3 runs.  --full for paper budgets.
"""

import argparse
import functools

from parabolab.library import exponential_gradient_nd
import parabolab.deep as deep


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--samples", type=int, default=3_000, help="M per state")
    p.add_argument("--states", type=int, default=1000)
    p.add_argument("--epochs", type=int, default=3000)
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--jobs", type=int, default=6)
    p.add_argument("--device", default="cpu")
    p.add_argument("--full", action="store_true",
                   help="paper budget: M=30,000 and 10 runs")
    args = p.parse_args()
    if args.full:
        args.samples, args.runs = 30_000, 10

    factory = functools.partial(exponential_gradient_nd, d=1, T=0.05,
                                alpha=10.0)
    print(f"=== exponential nonlinearity (4.2) deep branching, d=1, "
          f"T=0.05, N={args.states}, M={args.samples}, P={args.epochs} ===")
    print("paper (M=30,000, 10 runs, GPU): L1 1.17E-02 (SD 1.36E-03), "
          "runtime 42m/run")
    res = deep.run_experiment(
        factory, x_lo=-4.0, x_hi=4.0,
        n_states=args.states, m_samples=args.samples,
        epochs=args.epochs, n_runs=args.runs,
        n_jobs=args.jobs, device=args.device, seed0=30,
    )
    print("ours:", res.summary())

    deep.consistency_plot(
        res.data[0], res.nets[0], factory(),
        "examples/jcp_table3_exponential_deep.png",
        title=f"exponential (4.2) d=1: MC samples vs net (run 0, "
              f"M={args.samples})",
        x_lo=-4.0, x_hi=4.0, device=args.device,
    )
    print("figure saved to examples/jcp_table3_exponential_deep.png",
          flush=True)


if __name__ == "__main__":
    main()
