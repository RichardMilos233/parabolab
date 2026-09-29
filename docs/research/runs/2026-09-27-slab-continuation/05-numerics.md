# Numerical evidence

The protocol was fixed in `02-plan.md` before implementation. The Lean core gate passed before T04/T05 began coding. Every primary and comparator run completed; no random seed, tree, outlier or intermediate stage was removed. The code is a research prototype in this dated run, leaving existing solvers unchanged.

## Primary learned continuation

All three prescribed seeds used 50 slabs of .08, 200,000 roots per slab, and the same three coefficient caps. Each run therefore completed 10,000,000 local root trees and reached T=4. The normalized spatial L² errors at T=4 were:

- Seed2026092701:0.00195049134756;11,798,512 visited nodes;2.023 sampling seconds;9.046 run seconds.
- Seed2026092702:0.00163539237121;11,796,012 visited nodes;2.023 sampling seconds;9.060 run seconds.
- Seed2026092703:0.000688532541367;11,797,713 visited nodes;1.985 sampling seconds;8.816 run seconds.

The empirical RMS across these three realized errors is0.00152238866755. Three paths are a small diagnostic sample, not a confidence interval or an independent statistical proof of the population bound. C7 establishes ensemble normalized spatial RMS<.02 in the ideal mathematical model. Finite rational arithmetic gives the slightly sharper displayed bound≈.0185173; the rounded number itself is not the certificate.

Every stage after the first uses the previous projected coefficient vector. A test of the actual continuation path injects a guarded oracle and confirms that only stage1 reaches it. Exact reference values are used separately to score errors. All-stage Fourier error calculations agree with the independent16,384-point periodic grid to within5.4×10⁻¹⁸ in absolute L² error difference.

The fifth-mode coefficient was projected onto its small admissible interval in47/50,48/50 and47/50 stages, respectively. Modes1 and3 never hit their caps. Projection materially participates in the algorithm; this is an explicitly biased global approximation. The local trees themselves are neither clipped nor discarded. The proof controls projection bias via distance contraction toward an admissible target, without assuming that projected coefficients are unbiased.

Full records: `numerics/artifacts/slab/results.json`, per-seed progress JSON, and150 compressed stage archives containing each root's X,H,node count and root-branch flag. Each stage also records terminal-code counts, moments, coefficient covariance, raw/projected coefficients and timing.

## Full bounded-majority comparator

The comparator uses the same PDE, Jacobi terminal datum, normalized sine observations, projection caps and error norm. Each seed uses8,000 full-horizon root trees at bothT=.8 andT=2.

- AtT=.8, errors for seeds2026092711/12/13 were0.00631532,0.00401599,0.00307787. Actual node counts were291,710;288,353;288,512.
- AtT=2, errors were0.00460446,0.00685838,0.00433564. Actual node counts were34,825,778;35,030,042;35,202,698. Sampling times were6.023,6.230,6.156 seconds.

These are different prescribed sufficient budgets, not optimized equal-observed-error workloads. No empirical optimality or general speedup factor is claimed. Full-majority work grows with expected nodes/root=(3exp(4T)−1)/2. AtT=4 its prescribed8,000-root budget would require≈106,633,322,246 expected nodes. That T=4 cost is theoretical and was not run. The slab budget has a theoretical expected-node upper bound≈15,656,916 atT=4. Both sufficient budgets target ensemble spatial RMS below.02 on this datum, but neither is proved minimal.

Comparator data: `numerics/artifacts/majority/results.json` and six raw archives. The same-datum unsplit raw tree is not simulated atT=4: C9 conventionally proves its infinite second moment for the specified rate2 and uniform labels. A finite empirical variance would not settle that question.

## Prespecified sensitivity and independent references

The allowed smaller-budget diagnostic used seed2026092799,50 slabs and50,000 roots per slab:2,500,000 roots,2,949,388 nodes,2.307 run seconds, final L² error0.00684704964918. This single run does not establish a sample-complexity rate, and it does not inherit the200,000-root C7 RMS<.02 guarantee. All50 raw archives are retained in `numerics/artifacts/sensitivity/`.

The80-digit mpmath reference independently checked Jacobi stationarity by differentiation, and the first three Fourier coefficients by quadrature against the analytic series. The coefficients are approximately(.218915200521541,.000699545713702,.000002242594461); the squared omitted tail is≈5.168627956862×10⁻¹⁷. The period is≈4.611166090674. Separate tests compare SciPy terminal values and derivatives with mpmath. These are floating/high-precision cross-checks; the analytical tail/envelope bounds in T02 are the mathematical guarantee.

The29 focused tests passed in18.98s in the root's recorded run. They include scripted leaves and branches, zero-label handling, common childbirth positions, original `sample_tree` distribution checks at four codes/positions, an existing-majority comparison, projection admissibility, frozen coefficients, the actual no-late-oracle path, and nonfinite-output rejection. The distribution checks' empirical second-moment uncertainty is a diagnostic, not a proved fourth-moment confidence interval. Fixed seeds and measured discrepancies are in `reviews/T04-implementation.md`.

## Commands actually executed

From the repository root, with `P=/opt/miniconda3/envs/parabolab/bin/python` and `R=docs/research/runs/2026-09-27-slab-continuation/numerics`:

```sh
$P -m pytest $R/test_slab_sampler.py $R/test_experiment.py -q
$P $R/run_experiment.py reference
$P $R/run_experiment.py slab
$P $R/run_experiment.py majority
$P $R/run_experiment.py slab --n 50000 --seeds 2026092799 --output $R/artifacts/sensitivity
```

Each command returned exit0. Captured outputs are `numerics/tests.log`, `reference.log`, `slab-production.log`, `majority-production.log`, and `sensitivity.log`. The production manifests store commands, seeds, configuration, package/platform versions, source hashes and raw-file hashes. The complete bounded study finished well inside its two-hour budget. Reported run times include sampling, coefficient statistics and compressed archive writes, but exclude the independent reference setup, imports, tests, Lean build and research work; sampling times exclude archive/statistics overhead. They are observed machine timings, not complexity proofs.

Final independent raw-record audit and source-preservation results are in `numerics/audit.json`. Standard scientific figures and a compact machine-readable summary are generated by `numerics/summarize_results.py`. No numerical evidence establishes arbitrary-terminal, moving-front, high-dimensional or higher-jet success.
