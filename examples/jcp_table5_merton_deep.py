"""JCP2024 Table 5 + Fig 7: deep branching for the Merton HJB equation (4.6).

Paper settings: mu=0.03, sigma=0.1, gamma=0.5, rho=0.01, T=0.1,
x in [100, 200], N=1000 states at t=0, M=10,000 samples per state,
P=3000 epochs, 10 runs.  Paper (P100 GPU): L1 8.49e-3 (SD 7.44e-4) in
54 min/run (deep BSDE fails at L1 1.61e+0).

Fig 7 is the paper's signature diagnostic: the MC training targets are
unbiased pointwise estimates of u, so plotting them against the learned
net exposes any inconsistency of the fit (the paper shows a tanh
anomaly on its third run; --activation relu reproduces their fix).

Default here: reduced M=1,000 and 3 runs.  --full for paper budgets.
"""

import argparse

from parabolab.library import merton_hjb
import parabolab.deep as deep


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--samples", type=int, default=1_000, help="M per state")
    p.add_argument("--states", type=int, default=1000)
    p.add_argument("--epochs", type=int, default=3000)
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--jobs", type=int, default=6)
    p.add_argument("--device", default="cpu")
    p.add_argument("--activation", default="tanh", choices=["tanh", "relu"])
    p.add_argument("--full", action="store_true",
                   help="paper budget: M=10,000 and 10 runs")
    args = p.parse_args()
    if args.full:
        args.samples, args.runs = 10_000, 10

    print(f"=== Merton HJB (4.6) deep branching, d=1, T=0.1, "
          f"N={args.states}, M={args.samples}, P={args.epochs}, "
          f"activation={args.activation} ===")
    print("paper (M=10,000, 10 runs, GPU): L1 8.49E-03 (SD 7.44E-04), "
          "runtime 54m/run;  deep BSDE: L1 1.61E+00")
    res = deep.run_experiment(
        merton_hjb, x_lo=100.0, x_hi=200.0,
        n_states=args.states, m_samples=args.samples,
        epochs=args.epochs, n_runs=args.runs,
        n_jobs=args.jobs, device=args.device,
        activation=args.activation, seed0=50,
    )
    print("ours:", res.summary())

    # Fig 7 for the best and the worst run: the paper's Fig 7 shows
    # exactly such an anomalous run (their third, with tanh) where the MC
    # samples expose the inconsistency of the fitted net.
    import numpy as np

    for label, idx in (("best", int(np.argmin(res.l1))),
                       ("worst", int(np.argmax(res.l1)))):
        out = (f"examples/jcp_fig7_merton_consistency_"
               f"{args.activation}_{label}.png")
        deep.consistency_plot(
            res.data[idx], res.nets[idx], merton_hjb(), out,
            title=f"JCP2024 Fig. 7: Merton HJB (4.6), MC samples vs net "
                  f"({args.activation}, {label} run {idx}, "
                  f"L1={res.l1[idx]:.1e}, M={args.samples})",
            x_lo=100.0, x_hi=200.0, device=args.device,
        )
        print(f"figure saved to {out}", flush=True)
