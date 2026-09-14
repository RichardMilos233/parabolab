"""Allen–Cahn: compare sampling settings through the existing solver interface."""
from pathlib import Path
import time

import numpy as np

from parabolab import (
    CodingTreeMC,
    MomentQuadrature,
    TerminalTupleProposal,
    compare,
    optimize_exponential_rate_1d,
)
from parabolab.library import allen_cahn_wave_1d

# u_t + (1/2) u_xx + u - u^3 = 0. All four curves solve the same PDE.
# Custom tuple proposals currently use serial sampling, so an instance suffices.
pde = allen_cahn_wave_1d(T=0.05)
grid = np.linspace(-2.0, 2.0, 21)
n_samples = 10_000

if __name__ == "__main__":
    started = time.perf_counter()
    proposal = TerminalTupleProposal(pde, floor_mass=0.1)
    quadrature = MomentQuadrature(time_order=4, normal_order=4)

    # Tune at one reference state; these rates are reused over the whole grid.
    # The objective is finite-depth quadrature, not a full-tree certificate.
    rate_only = optimize_exponential_rate_1d(
        pde, t=0.0, x=0.0, max_depth=2, bracket=(0.2, 2.0),
        quadrature=quadrature,
    )
    combined = optimize_exponential_rate_1d(
        pde, t=0.0, x=0.0, max_depth=2, bracket=(0.2, 2.0),
        tuple_proposal=proposal, quadrature=quadrature,
    )
    if not (rate_only.converged and combined.converged):
        raise RuntimeError("Finite-depth rate selection did not converge")
    print(f"Proposal setup and both rate searches: {time.perf_counter() - started:.2f} s")
    print(f"Rates selected at x=0: uniform q={rate_only.rate:.5f}, "
          f"terminal q={combined.rate:.5f}; reused across the profile.")

    curves = [
        CodingTreeMC(n_samples=n_samples, seed=0,
                     label="baseline: rate=1, uniform q").solve(pde, grid),
        CodingTreeMC(n_samples=n_samples, seed=0, rate=rate_only.rate,
                     label="selected rate, uniform q").solve(pde, grid),
        CodingTreeMC(n_samples=n_samples, seed=0, tuple_proposal=proposal,
                     label="rate=1, terminal q").solve(pde, grid),
        CodingTreeMC(n_samples=n_samples, seed=0, rate=combined.rate,
                     tuple_proposal=proposal,
                     label="selected rate, terminal q").solve(pde, grid),
    ]

    # Same N at every point: N * stderr^2 is the empirical sample variance.
    print("Mean empirical variance over grid points (single-seed diagnostic):")
    for curve in curves:
        variance = float(np.mean(n_samples * curve.stderr**2))
        print(f"  {curve.label}: {variance:.6g}")

    title = "Allen–Cahn: branching sampling variants"
    compare(pde, *curves).table().plot(Path(__file__).with_suffix(".png"), title)
