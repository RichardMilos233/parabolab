# T34 — pre-implementation review of the fixed two-barrier experiment

**Verdict: conditional pass.** The scientific cases, sample sizes,
mathematical sampler, scaled PDE, resolution choices, reference discrepancy
tolerance, and prescribed statistical thresholds are coherent. No stated
number needs changing. Before implementation, freeze the bounded
clarifications in section 1. They remove ambiguities about the output,
accepted clock diagnostics, failure gates, and fair timing comparisons.

Reviewed source:
[02d-two-barrier-experiment-protocol.md](../02d-two-barrier-experiment-protocol.md),
146 lines, SHA-256
85aa2f19ce801223a4ef7c68af85e73645689032e697927fed55c83a1ade17ef.
Mathematical basis:
[04l](../04l-two-barrier-voting.md),
[T30](T30-two-barrier-voting-audit.md),
[04m](../04m-horizon-free-clock-proposal.md), and
[T31](T31-horizon-free-clock-audit.md).
The parent reports that T29's fresh integrated-width Lean gate passed.
This protocol review does not independently rerun that build.

No sampler, reference solver, diagnostic, numerical experiment, or new
literature search was executed here. Frozen T31, T28, and T26 were preserved.
Only this review file was written.

## 1. Corrections to freeze before implementation

1. **Make the time-zero return explicit.** For a primary query use
   $Z=(v(x)-m)/(M-m)$ and $W=1-v(x)$, with
   $N=L=1$, $I_2=I_3=0$, and zero clock proposals/rejections. “Return the
   exact initial value” is ambiguous when the primary output is the scaled
   defect. The harmonic-center and mean-ODE comparators need not be exact
   at time zero for a nonconstant profile; limit the exactness statement to
   the sampler/reference initial datum.

2. **Define diagnostic draws and endpoint queries.** Each of the 100000
   clock diagnostic draws must be one accepted finite-horizon outcome after
   the rejection loop, not one raw limiting-kernel proposal. Preserve its
   leaf/event indicator and accepted event time, as well as trial counts.
   Fix the endpoint-constant diagnostic query to $x=0$, since that query
   was omitted. The profile is constant, but fixing it resolves the exact
   diagnostic workload and random-stream indexing.

3. **Freeze the metric and gating policy.** Report all three seed-specific
   means and relative errors for every $(T,x)$, and define the three-seed
   RMS by the formula in section 2. Do not use “1% target” as a guarantee
   that all 63 observed errors will be below 1%. State that failed
   deterministic preflight checks, reference convergence, or the prescribed
   diagnostics stop primary execution, preserve evidence, and require a
   versioned resolution. Do not choose new seeds or increase sample sizes
   to make a failed check pass.

4. **Fix the deterministic timing comparison.** A single deterministic PDE
   solve serves all 21 $(T,x)$ queries, whereas the Monte Carlo producer
   samples each query separately. Designate the 16-mode, looser-tolerance
   run as the predetermined deterministic comparator, provided it passes
   the same reference discrepancy check. Report one solve plus all query
   evaluations against the total sampling time for all 21 queries of each
   primary seed. Keep six-run reference validation costs separate. Do not
   infer equal-accuracy or optimized-method speedup from comparison only
   with the 64-mode strict reference.

5. **Clarify reference independence.** Call the six Galerkin/Radau solves
   resolution/tolerance refinement runs. They share a numerical method and
   are not six independent error certificates. The stochastic and
   deterministic producers remain independently implemented. Closed-form
   diagnostic targets must also be evaluated independently of the sampler's
   clock/barrier helpers; otherwise an endpoint check may merely compare a
   helper with itself.

The exact RNG mapping, projection/Jacobian preflight inputs and tolerances,
time-budget semantics, and preservation manifest must be recorded before
any corresponding diagnostic or primary execution, as detailed below.
These are implementation contracts, not permission to select scientific
parameters after observing errors.

## 2. Primary cases, count, and the 1% target

The datum

$$
v(x)=\frac58+\frac18\cos x
$$

is smooth and $2\pi$-periodic, with range $[1/2,3/4]$ and Lipschitz
constant $1/8$. Its spatial mean is exactly $5/8$.
The proposed three spatial queries, seven horizons, three seeds, and
10000 independent ideal roots per cell give

$$
3\cdot7\cdot3=63\text{ cells},\qquad
63\cdot10000=630000\text{ primary roots}.
$$

The relative variance bound from the positive barrier interval is
$100/189$. For an ideal iid sample mean with $N=10000$,

$$
\frac{\sqrt{\mathbb E(\overline W-\mathbb EW)^2}}{\mathbb EW}
\leq\sqrt{\frac{100}{189\cdot10000}}
=\frac{1}{\sqrt{18900}}<0.01.
$$

This is a root-mean-square guarantee over repeated ideal ensembles. It is
not a 99% confidence statement, an upper bound on every observed error,
or a guarantee for a floating sampler with unknown bias.

Let $D_{\rm ref}(T,x)$ be the fixed strict reference and let
$\overline W_j(T,x)$ be the mean from primary seed $j$. The natural frozen
reporting quantities are

$$
e_j(T,x)=
\frac{\overline W_j(T,x)-D_{\rm ref}(T,x)}{D_{\rm ref}(T,x)},\qquad
\operatorname{RMS}_3(T,x)
=\sqrt{\frac13\sum_{j=1}^3 e_j(T,x)^2}.
$$

Also report the three signed errors individually and each cell's within-root
dispersion. Three seed means provide only a limited diagnostic of empirical
RMS; the outcome is not an accurate measurement of a universal variance or
bias. There should be no selected pooling across times, queries, or seeds
after the errors are seen.

The largest horizon is $T=256$, so $e^{-2T}=e^{-512}$ remains a positive
normal binary64 number. This checks the protocol's representability claim.
Direct subtraction of a computed $u$ from one would nevertheless fail long
before this horizon, so measuring the scaled defect is essential.

## 3. Mathematical sampler and pathwise records

The mechanism specified in 02d agrees with the audited construction:

- Limiting clock proposals retain the leaf atom $8/15$.
- Event proposals with $s\geq T$ are rejected before spatial work or child
  generation.
- Accepted branch edges have Brownian variance $T-s$; accepted leaves have
  variance $T$.
- The branch probability is
  $p=3(1+\zeta)/(2(2+\zeta))$, with binary OR otherwise mixed with ternary
  majority as in 04l.
- All children begin at the same branch location with independent descendant
  randomness.
- The inverse uses the audited numerator
  $d=(1-U)(1+\zeta)/(1+\zeta-U/2)$ and the corresponding ratio
  $q_{\rm event}=d/(20/9-3d)$.

The bounded multiaffine forms are

$$
\operatorname{OR}_2(z_1,z_2)=z_1+z_2-z_1z_2,\qquad
\operatorname{MAJ}_3(z_1,z_2,z_3)
=z_1z_2+z_1z_3+z_2z_3-2z_1z_2z_3.
$$

Applying a scalar voting polynomial to a child average would not be an
equivalent implementation. The primary scaled output must be

$$
W=R_M(T)Z+R_m(T)(1-Z).
$$

At time zero, the exact primary values are

$$
\begin{array}{c|ccc}
x&0&\pi/2&\pi\\ \hline
Z&1&1/2&0\\
W&1/4&3/8&1/2.
\end{array}
$$

For every completed tree, require the integer identities

$$
N=L+I_2+I_3,\qquad
N=1+2I_2+3I_3,\qquad
L=1+I_2+2I_3.
$$

Counts are integers and need no floating tolerance. For positive $T$,
$P_{\rm trials}=N+P_{\rm rejections}$. The documented time-zero shortcut
instead has $P_{\rm trials}=P_{\rm rejections}=0$.
The proposed $10^{-12}$ rounding tolerance can be applied to
$0\leq Z\leq1$ and
$R_M(T)\leq W\leq R_m(T)$, with the coarser global interval
$[1/4,3/2]$ as an additional diagnostic. It must not silently become a
clipping operation or a claimed arithmetic error bound.

The expected node and proposal bounds are correctly treated as expectations:

$$
\mathbb EN\leq\frac{25\sqrt6}{16}-1,\qquad
\mathbb EP_{\rm trials}
\leq\frac{15}{8}\left(\frac{25\sqrt6}{16}-1\right).
$$

An empirical mean can exceed an expectation bound. Neither a root-size cap
nor a post hoc cutoff follows from these formulas.

## 4. Independent scaled PDE and Galerkin refinement

The proposed reference equation is correct. For
$D=e^{2t}(1-u)$,

$$
D_t=\frac12D_{xx}+3e^{-2t}D^2-e^{-4t}D^3,\qquad
D(0,x)=\frac38-\frac18\cos x.
$$

A real cosine Galerkin method is justified because the datum and equation
preserve evenness. Freeze “maximum mode $K$” to mean the modes
$0,1,\ldots,K$, including the constant. On the periodic quadrature grid,
use the explicitly specified nodes and cosine normalization.

For a trigonometric polynomial of maximum mode $K$, its cube has maximum
mode $3K$. Projection of that cube against a retained mode has maximum
frequency $4K$. A uniform periodic grid with $J=8K>4K$ therefore avoids
aliasing into retained modes for the exact polynomial quadrature. The
prescribed $(K,J)$ pairs $(16,128),(32,256),(64,512)$ are sufficient.
This argument concerns aliasing, not Fourier truncation or time-stepping
error.

For example, with $D_K=\sum_{\ell=0}^K a_\ell\cos(\ell x)$ and cosine
projection $\mathcal P_k$, the analytic Jacobian must be the derivative

$$
J_{k\ell}
=-\frac{k^2}{2}\delta_{k\ell}
 +\mathcal P_k\!\left[
 (6e^{-2t}D_K-3e^{-4t}D_K^2)\cos(\ell x)
 \right].
$$

An independently implemented complex-Fourier convolution can check both
the nonlinear projection and this Jacobian without sharing the quadrature
implementation. Freeze the deterministic input coefficient vectors, times,
and comparison tolerance in the preflight manifest before running those
checks. Initial-data-only vectors do not exercise all retained modes; include
a fixed vector with every mode nonzero. Constant scalar profiles separately
check the zero-mode dynamics.

The two fixed tolerance pairs for each of three resolutions give six
refinement runs. Require solver success for all six and retain their
coefficients/query values, diagnostics, and timings. Specify one solve from
zero to 256 per run with evaluation at the prescribed horizons, rather than
letting an implementation select restarts after seeing discrepancies.

The maximum discrepancy of every run from the 64-mode strict run at all
prescribed $(T,x)$ values must be below $10^{-8}$ in scaled units. This is
a sensible stringent empirical convergence gate. It is not an enclosure of
the true solution, and agreement between six versions of one method cannot
exclude a shared error.

If $10^{-8}$ were an actual reference error bound, the target's lower bound
$D\geq1/4$ would make it at most $4\cdot10^{-8}$ in relative units, far below
the 1% sampling target. The current discrepancy test does not by itself
prove that premise. Preserve this distinction in the result report.

## 5. Prespecified clock and constant diagnostics

### Accepted finite-horizon clock CDF

Represent a leaf by $S=0$ and an event by its accepted remaining time.
For $0\leq s\leq T$, the correct cumulative distribution is

$$
F_T(s)=
\exp(\Lambda(s)-\Lambda(T))
=\frac{R(z(s))}{R(z(T))}.
$$

In particular $F_T(0)$ is the leaf atom, while $F_T(T)=1$. This formula
does not describe a raw limiting proposal before rejection. The diagnostic
must preserve 100000 accepted outcomes at each of the three specified
horizons, together with rejected-proposal counts.

For ideal iid outcomes, DKW gives

$$
\mathbb P\!\left(\sup_s|\widehat F_T(s)-F_T(s)|>\epsilon\right)
\leq2e^{-2N\epsilon^2}.
$$

The proposed threshold
$\epsilon=\sqrt{\log(2/10^{-6})/(2\cdot100000)}$
therefore has false-alarm probability at most $10^{-6}$ per horizon.
Atoms cause no problem for DKW. Checking only the five prescribed CDF
locations also has this false-alarm upper bound, but passing that finite
grid does not certify the supremum error over all event times.
The $s=T$ point is chiefly a support/accounting check.

### Nonendpoint constant profile

For the fixed constant $v=5/8$, the true PDE is its scalar ODE, so the
scaled mean is the independently evaluated $R_{5/8}(4)$. Every ideal return
lies in $[1/4,3/2]$, of width $5/4$. Hoeffding therefore gives

$$
\mathbb P(|\overline W-\mathbb EW|>a)
\leq2\exp\left(-\frac{2Na^2}{(5/4)^2}\right).
$$

The proposed $a=(5/4)\epsilon$ has ideal false-alarm probability at most
$10^{-6}$. The constant is correct. This deliberately conservative
diagnostic is not a certification that total floating bias is below the
primary 1% target.

Across the three clock checks and this constant-mean check, the union bound
is at most $4\cdot10^{-6}$ under the ideal iid laws. No independence across
the four tests is required for that statement. Do not label $10^{-6}$ as a
global familywise bound. The bounds describe the ideal statistical model,
not a proof that a finite PRNG and floating sampler realize it exactly.

### Endpoint constants and total diagnostic workload

At $v=m$, all leaves and votes are zero; at $v=M$, all are one. Each
completed output must therefore equal its corresponding barrier coefficient
pathwise. The 128-root endpoint checks need no probabilistic threshold;
$10^{-12}$ is the chosen arithmetic diagnostic tolerance.

With the query fixed to $x=0$, endpoint diagnostics use
$128\cdot2\cdot7=1792$ roots. Together with the 100000 nonendpoint roots,
the full protocol uses 731792 PDE roots including primaries, plus 300000
standalone accepted clock draws. Raw limiting proposal trials are an
additional random count and must not be confused with either total.

Closed-form CDF and scalar targets should not call the sampler's own
inverse/clock/coefficient helpers. Independent forward formulas or a fixed
higher-precision implementation avoid a tautological diagnostic.

## 6. Baselines and timing scope

Both analytic baselines are legitimate and should remain even if their
errors are unfavorable to the proposed sampler.

- The scaled harmonic center is
  $2R_m(T)R_M(T)/(R_m(T)+R_M(T))$. It uses known range information and
  scalar formulas but no spatial-profile queries. Its pointwise relative
  error certificate is the positive-range bound from 04l.
- The spatial-mean ODE comparator is $R_{5/8}(T)$. It uses the known mean
  of this specific profile and has no universal pointwise certificate.
  Its evaluation does not require solving the evolving PDE.

At time zero the harmonic-center scaled value is $1/3$ and the mean-ODE
scaled value is $3/8$. They are not equal to all three true initial defects
$1/4,3/8,1/2$. Their initial errors should remain visible.

For numerical timing, distinguish these tasks:

1. One Monte Carlo cell: one $(T,x)$ and one 10000-root estimate.
2. One entire seed replicate: all 21 queries, with separate root sets.
3. One deterministic solve through the maximum horizon, followed by all
   prescribed point evaluations.
4. Reference validation: all six refinement solves plus comparisons.

The predesignated 16-mode loose run can serve task 3, provided it passes
the reference discrepancy gate. Compare it with each task-2 timing and
report task-1 times separately. Do not divide a whole-grid solve's cost
arbitrarily among queries after observing which timing looks best.
Report reference validation, preflight, data processing/I/O, and sampling
separately as already proposed.

Both deterministic tolerance pairs are much stricter than the 1% Monte
Carlo target. This study therefore compares fixed implementations and
observed errors; it does not optimize both methods at equal error. A claimed
general speedup, dimension-independent runtime, or optimal accuracy-cost
tradeoff would require a different, prespecified study.

## 7. Reproducibility, safeguards, and permission to proceed

The scientific primary grid and root counts are already fixed appropriately.
To close the remaining implementation choices before outcomes:

- Write an immutable preflight manifest containing the exact SeedSequence
  entropy/spawn-key mapping, PCG64 variant, zero-based horizon/query/endpoint
  index conventions, uniform endpoint convention, precision, and environment.
  Every primary cell and diagnostic group needs its own recorded initial and
  final state. Different diagnostic seed labels already prevent accidental
  reuse of primary streams, but the mapping still needs to be explicit.
- Freeze deterministic preflight cases and tolerances before executing them.
  Inverse-domain checks should include values near the leaf threshold and
  near one, and should distinguish exact-real identities from floating
  approximations. Do not select a less demanding test set after a failure.
- Preserve per-root arrays for every completed primary/constant root, all
  accepted clock diagnostic outcomes, proposal counts, each reference run's
  query/coefficient arrays, and failed checks. A summary JSON or figure is
  not a replacement for these raw records. RNG states plus source hashes
  support replay; they do not establish mathematical randomness.
- Define the 120-second primary-cell limit as monotonic elapsed sampling
  time, with processing/I/O separately reported. Choose a checkpoint and
  interruption policy before execution so that completed roots survive a
  timeout even if the next root is unfinished. Mark the whole cell
  incomplete; its completed prefix is not an $N$-root primary estimate and
  may be selected by runtime. Do not turn the safeguard into an unreported
  tree-size cutoff.
- If code is corrected, preserve the old artifact directory and failed
  evidence, version the correction, and mark all scientifically affected
  results stale. Do not retain only favorable unaffected-looking cells
  whose producer changed. Refusing final-artifact overwrite is appropriate.

The proposed smooth cosine oracle avoids T31's arbitrary-measurable-data
counterexample, but does not prove a complete rounding-bias bound. The
coefficient-limit estimate remains only one error term. At these prescribed
horizons its exponential-underflow branch should not be needed in ordinary
binary64; retain the policy and record whether it is used.

Once the section-1 clarifications and pre-execution manifest requirements
are fixed, the protocol is suitable for implementation under its stated
limited purpose. This review authorizes no expansion to burn-in factories,
new profiles, new horizons, adaptive root counts, arbitrary measurable-data
claims, or post-outcome accuracy/cost tuning.
