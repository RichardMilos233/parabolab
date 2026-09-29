# Numerical results for the tilted sampler (2026-09-29)

Code: `parabolab/tilted.py`; tests: `tests/test_tilted.py` (10 passed);
driver: `examples/tilted_long_horizon.py` (writes `.json`/`.png` next to
itself; both gitignored, regenerate by running the script, ~40 s).
All runs are floating-point; the step-function supersolution's ratio
`theta_eff` is checked on the grid, not interval-certified.

## 1. Flat Allen–Cahn, v ≡ 1/2 (exact solution known)

τ_abs = (3π − 2 log 3)/5 = 1.4455106767 (mpmath closed form = quadrature).
Every constant-rate, fixed-first-label sampler has infinite variance for
T ≥ 0.99545 (λ-optimum as p → 1; 0.70389 at p = 1/2).

| T | ϑ | bound ϑ/2+Z(ϑ²T) (step table / closed form) | N | estimate ± s.e. | exact | z | mean nodes (≤ ϑ/(ϑ−1)) | killed |
|---|---|---|---|---|---|---|---|---|
| 0.5 | 1.2 | 0.93844 / 0.93844 | 2e4 | 0.69116 ± 0.00310 | 0.68947 | +0.55 | 1.46 (6.0) | 0.240 |
| 0.9 | 1.1 | 1.27031 / 1.27031 | 2e4 | 0.81078 ± 0.00543 | 0.81762 | −1.26 | 2.49 (11.1) | 0.227 |
| 1.2 | 1.05 | 2.08301 / 2.08301 | 2e4 | 0.87788 ± 0.01074 | 0.88661 | −0.81 | 6.23 (21.3) | 0.291 |
| 1.4 | 1.004 | 3.847 | 1.6e6 | 0.917704 ± 0.002741 | 0.919628 | −0.70 | ≈33 (≈250) | 0.132 |

T = 1.4 is 96.9% of τ_abs. Per-seed z at T = 1.4 (ϑ = 1.008 and 1.004,
2e5 each): +2.70, −1.32, −0.43, −0.47; the pooled 1.6e6 run is the
reported row. Wall time ≈ 17 s per 2e5 samples at T = 1.4 (pure Python).

## 2. Periodic Allen–Cahn, v = 1/2 + 0.02 sin(2πx), x = 1/4

Sup envelopes exact on the data range [0.48, 0.52]; guaranteed horizon of
the sup-majorant τ_sup = 1.28237 (τ_sup: ε = 0 → 1.44551, 0.01 → 1.37743,
0.02 → 1.28237, 0.05 → 1.01322). Reference: Fourier (n = 256) Strang
splitting with exact reaction flow, dt = 1e-4; dt-halving change ≤ 1.4e-11,
n-doubling ≤ 4e-15, and ε = 0 reproduces the flat closed form to 1e-13.
2e5 samples per estimator per T; seeds fixed in the script.

| T | reference | tilted (ϑ) est ± s.e. [z] | Hoeffding 95% | bound | nodes | fixed rate 1 est ± s.e. [z], max\|H\| | fixed rate 2 est ± s.e. [z], max\|H\| |
|---|---|---|---|---|---|---|---|
| 0.5 | 0.68946 | 0.68884 ± 0.00051 [−1.22] (1.02) | 0.0046 | 0.765 | 1.5 | 0.68905 ± 0.00075 [−0.55], 23 | 0.68932 ± 0.00127 [−0.11], 10 |
| 0.8 | 0.78916 | 0.78716 ± 0.00112 [−1.78] (1.02) | 0.0061 | 1.006 | 2.2 | 0.78626 ± 0.00411 [−0.71], 665 | 0.79102 ± 0.00267 [+0.70], 108 |
| 1.0 | 0.84334 | 0.84247 ± 0.00186 [−0.47] (1.02) | 0.0081 | 1.340 | 3.9 | 0.82450 ± 0.01567 [−1.20], 2630 | 0.85240 ± 0.00873 [+1.04], 854 |
| 1.1 | 0.86632 | 0.87069 ± 0.00253 [+1.73] (1.02) | 0.0104 | 1.720 | 6.4 | 0.91542 ± 0.02545 [+1.93], 4650 | 0.79822 ± 0.05822 [−1.17], 11200 |
| 1.2 | 0.88660 | 0.88633 ± 0.00407 [−0.07] (1.0169) | 0.0178 | 2.938 | 16.4 | 0.94836 ± 0.01935 [+3.19], 1420 | 0.93548 ± 0.06933 [+0.70], 9330 |

Share of Σ|H| carried by the largest 0.1% of fixed-rate samples: rate 1:
0.007, 0.026, 0.065, 0.093, 0.114; rate 2: 0.003, 0.016, 0.053, 0.121,
0.176 — the heavy-tail signature. At T ≥ 1.0 the fixed-rate sample
variances (49–961) are lower bounds of possibly infinite population
variances; their standard errors are not reliable. The tilted sampler's
Hoeffding intervals are valid non-asymptotically and cover the reference
at every T. Work-normalized variance (var × mean nodes) at T = 1.0:
tilted 2.7, fixed rate 1 ≥ 152, fixed rate 2 ≥ 158.

## 2a. Dimension 100 (2026-09-29, `examples/tilted_high_dim.py`)

Allen–Cahn in R^100, v(x) = 1/2 + 0.02 sin(2π a·x), a = (1,…,1)/10,
x0 = a/4; exact u = 1-D periodic solution at a·x0 = 1/4 (a·B is a 1-D BM).
Envelopes l_i = |a_i| 2π ε, so l_D = 2πε and τ_sup = 1.28237 exactly as in
1-D (Prop. dimfree). 1e5 samples per estimator and T, seeds 41/43.
Flat-data L2 limits (Prop. F / Cor. uniform): uniform tuples (p = 1/101)
0.0150 (λ=1), 0.0294 (λ=2), 0.0991 (best λ); tuned p = 0.95: 0.8976,
0.9595, 0.9702.

| T | ref | tilted est ± s.e. [z] | Hoeff. 95% | nodes | uniform λ=2 est ± s.e. [z], max\|H\| | tuned λ=2 est ± s.e. [z], max\|H\| |
|---|---|---|---|---|---|---|
| 0.02 | 0.52105 | 0.52155 ± 0.00023 [+2.14] | 0.0046 | 1.01 | 0.52087 ± 0.00021 [−0.87], 2.1 | 0.52095 ± 0.00021 [−0.48], 0.54 |
| 0.05 | 0.52639 | 0.52687 ± 0.00024 [+2.01] | 0.0047 | 1.04 | 0.52658 ± 0.00034 [+0.56], 3.5 | 0.52643 ± 0.00034 [+0.12], 0.58 |
| 0.1 | 0.54072 | 0.54128 ± 0.00025 [+2.19] | 0.0049 | 1.07 | 0.54114 ± 0.00052 [+0.81], 4.0 | 0.54056 ± 0.00050 [−0.33], 0.64 |
| 0.3 | 0.61476 | 0.61510 ± 0.00040 [+0.87] | 0.0057 | 1.23 | 0.61643 ± 0.00120 [+1.39], 8.9 | 0.61465 ± 0.00108 [−0.10], 0.95 |
| 0.6 | 0.72479 | 0.72566 ± 0.00094 [+0.93] | 0.0071 | 1.64 | 0.68449 ± 0.05882 [−0.69], 5876 | 0.72528 ± 0.00214 [+0.23], 3.7 |
| 1.0 | 0.84334 | 0.83839 ± 0.00265 [−1.87] | 0.0115 | 3.90 | 0.93657 ± 0.01059 [+8.80], 853 | 0.84578 ± 0.00503 [+0.48], 62 |
| 1.2 | 0.88660 | 0.86767 ± 0.00576 [−3.29] | 0.0252 | 16.6 | 1.03702 ± 0.00934 [+16.1], 190 | 0.88252 ± 0.02646 [−0.15], 2030 |

Top-0.1% share of Σ|H|: uniform 0.001–0.009 up to T = 0.3, then 0.089,
0.052, 0.063; tuned ≤ 0.016 up to T = 1.0, 0.079 at T = 1.2.

**Follow-up on the tilted z-values** (the table's T values share seed 41,
so its z's are correlated): independent 10-seed runs with 1e5 each give
pooled z = −0.03 (T = 0.02), −0.25 (T = 0.1), +1.56 (T = 1.2, 1e6), and two
independent 1e6 runs at T = 1.0 give −1.65 and +1.10 (pooled −0.39). A
dimension scan at T = 1.2 (3e5 each, seeds 300–305) gave +1.81 (d = 1,
identical for the ParabolicPDE and SemilinearProblem paths), +1.47 (d = 2),
−0.85 (d = 100). No bias; the seed-41 values at T = 1.0/1.2 were
fluctuations. The certified Hoeffding intervals cover the reference at
every T in the table (|dev| at T = 1.2: 0.0189 < 0.0252).

## 2b. Sampler-independent work identity and Proposition F (2026-09-29)

E[N|H|] = W_N = 1/2 + 2TΦ(Z(T)) (Theorem A, node-weighted), flat AC,
2e5 tilted samples, seed 5 (scratch script `work_check.py`):

| T | ϑ | W_N (formula) | E[N\|H\|] sampled | W_N/M (lower) | E N | ϑ/(ϑ−1) |
|---|---|---|---|---|---|---|
| 0.9 | 1.1 | 2.219 | 2.226 ± 0.007 | 1.75 | 2.51 | 11 |
| 1.2 | 1.05 | 7.512 | 7.487 ± 0.030 | 3.61 | 6.21 | 21 |
| 1.4 | 1.004 | 101.854 | 101.50 ± 0.36 | 26.48 | 32.86 | 251 |

Proposition F second moment, fixed rate λ = 1, uniform tuples (p = 1/2),
`sample_tree`, 4e5 samples, seed 11 (T₂ = 0.56819):

| T | formula E H² | sampled | z |
|---|---|---|---|
| 0.20 | 0.34173 | 0.34167 ± 0.00018 | −0.3 |
| 0.35 | 0.44050 | 0.43929 ± 0.00232 | −0.5 |
| 0.45 | 0.54643 | 0.53577 ± 0.00565 | −1.9 (heavy tail near T₂; sample 2nd moment biased low) |

Two-term fraction K (p!)^{−1/(2p)} I_p^{−1/2} of Remark rem:fraction matches
mpmath quadrature to 1e-15 for p = 2, 3, 4, 6, 10 and two coefficient pairs.

## 2c. Decision: no R^d numerical example

For u_t = Δu/2 − u², v = ε e^{−|x|²}, d = 5, the Gaussian-envelope α-ODE
stays bounded to T = 200 for ε ≤ 0.2 (blows up at s ≈ 26.9 for ε = 0.25).
In exactly that regime the radial FD reference differs from the heat flow
by only 0.6–2%, comparable to the reference's own grid error (~1e-3
relative). A Monte Carlo demonstration there would be a toy; Theorem E is
kept as theory only. (Exact Gaussian-envelope sampling is nevertheless
possible: P_σ G(s) = G(s+σ) and the rejection step G^{m−1}/w^{m−1};
noted for future work.)

## 3. Negative result: traveling wave with crude sup envelopes

JEQ (5.3) wave, φ ∈ (−1, 0): sup envelopes (1; 0.385, 2, 6, 6; 0.25) give
τ_sup = 0.666 only (0.823 without the gradient envelope). Inside that
window the fixed-rate sampler at rate 1 had 2–3× lower var × nodes than
the tilted sampler (e.g. T = 0.5: 0.28 vs 0.76 at ϑ = 1.01, 2e4 samples),
though with unbounded outputs (max |H| = 9.0). The sup envelope is loose
because it combines f-jets from both ends of the range; spatially varying
supersolutions are needed there and are not implemented.
