"""Reproduce JEQ2023 Table 5: HJB equation (5.9) at d = 100, T = 1.

    du/dt + Lap u = |grad u|^2  (sigma2 = 2),  phi = log((1+|x|^2)/2),
    estimate u(0, 0).  Exact value by Cole-Hopf quadrature
    (library.hjb_exact_u0): 4.590162.

Paper (coding trees): mean 4.580340, SD 0.001869 over 5 estimates of 1e5
samples (notebook cell hjb_weinan, exponential rate -log(0.95)/T).
Deep BSDE [19]: 4.5977 +/- 0.0019.

Note: at d = 100 the reduced mechanism still has |M(f*)| = 20000, so the
rare branch events carry weights ~|M|/rate; the sparse authors' rate is
essential here (rate 1.0 gives exploding variance AND 20x the runtime).

Usage: python jeq_table5_hjb_d100.py [--samples N] [--runs R] [--jobs J]
"""

import argparse
import time

import numpy as np

from parabolab.library import hjb_exact_u0, hjb_nd
from parabolab.parallel import estimate_parallel
from parabolab.tree import jcp_rate


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=100_000,
                    help="samples per run (paper: 1e5)")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--jobs", type=int, default=5)
    args = ap.parse_args()

    T = 1.0
    exact = hjb_exact_u0(T=T, d=100)
    rate = jcp_rate(T)
    print(f"HJB (5.9), d=100, T={T}, u(0,0);  exact (Cole-Hopf) = {exact:.6f}")
    print("paper coding trees: mean 4.580340, SD 0.001869;  "
          "BSDE [19]: 4.5977, SD 0.0019")

    from concurrent.futures import ProcessPoolExecutor

    x0 = np.zeros(100)
    vals = []
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        for r in range(args.runs):
            res = estimate_parallel(hjb_nd, 0.0, x0, args.samples,
                                    seed=300 + r, rate=rate,
                                    n_jobs=args.jobs, executor=ex)
            vals.append(res.estimate)
            print(f"  run {r}: {res}  z_vs_exact="
                  f"{(res.estimate - exact) / res.stderr:+.2f}", flush=True)
    secs = time.perf_counter() - start
    vals = np.array(vals)
    rel = np.abs(vals - exact) / exact
    print(f"ours: mean {vals.mean():.6f}  SD {vals.std(ddof=1):.6f}  "
          f"mean rel.L1 {rel.mean():.6f}  SD rel.L1 {rel.std(ddof=1):.6f}  "
          f"({secs:.0f}s)")


if __name__ == "__main__":
    main()
