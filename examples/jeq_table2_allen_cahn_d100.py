"""Reproduce JEQ2023 Table 2: Allen-Cahn (5.1) at d = 100, T = 0.3.

    du/dt + Lap u + u - u^3 = 0  (full Laplacian, sigma2 = 2),
    phi(x) = 1/(2 + 2|x|^2/5),  estimate u(0, 0).

Paper (coding trees): mean 0.052754, SD 0.000364 over 5 estimates of 1e6
samples each (notebook cell allen_cahn_weinan: 5 states x 10 repeats x 1e5
paths, exponential rate -log(0.95)/T).  Deep BSDE [19]: 0.0528 +/- 0.0002;
its Table-1 reference value is 0.052802.

We report both the authors' exponential rate and our default rate 1.

Usage: python jeq_table2_allen_cahn_d100.py [--samples N] [--runs R] [--jobs J]
"""

import argparse
import time

import numpy as np

from parabolab.library import allen_cahn_bsde
from parabolab.parallel import estimate_parallel
from parabolab.tree import jcp_rate

REFERENCE = 0.052802  # deep-BSDE Table 1 [19] reference value


def run_block(rate, label, n_runs, n_samples, jobs, seed0, executor):
    x0 = np.zeros(100)
    vals = []
    start = time.perf_counter()
    for r in range(n_runs):
        res = estimate_parallel(
            allen_cahn_bsde, 0.0, x0, n_samples,
            seed=seed0 + r, rate=rate, n_jobs=jobs, executor=executor,
        )
        vals.append(res.estimate)
        print(f"  run {r}: {res}", flush=True)
    secs = time.perf_counter() - start
    vals = np.array(vals)
    rel = np.abs(vals - REFERENCE) / REFERENCE
    print(f"[{label}] mean {vals.mean():.6f}  SD {vals.std(ddof=1):.6f}  "
          f"mean rel.L1 {rel.mean():.6f}  SD rel.L1 {rel.std(ddof=1):.6f}  "
          f"({secs:.0f}s)")
    return vals


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--samples", type=int, default=1_000_000,
                    help="samples per run (paper: 1e6)")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()

    T = 0.3
    print(f"Allen-Cahn (5.1), d=100, T={T}, u(0,0);  "
          f"reference [19] = {REFERENCE}")
    print("paper coding trees: mean 0.052754, SD 0.000364", flush=True)
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        run_block(jcp_rate(T), f"authors' rate {jcp_rate(T):.4f}",
                  args.runs, args.samples, args.jobs, seed0=100, executor=ex)
        run_block(1.0, "rate 1.0", args.runs, args.samples, args.jobs,
                  seed0=200, executor=ex)


if __name__ == "__main__":
    main()
