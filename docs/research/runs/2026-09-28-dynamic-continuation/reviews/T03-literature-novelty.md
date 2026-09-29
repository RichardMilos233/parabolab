# T03 — Independent literature and novelty stress test

Research date: 28 September 2026. Scope: primary-literature review of the proposed dynamic continuation theorem; no solver, experiment, or formalization changes. This is the only file written by T03. The pre-existing dirty working tree was inspected and preserved. Research role/model: inherited from the parent; the serving model is not independently verifiable here. The `math-auto-research` research workflow was followed. Literature coverage is bounded, not a worldwide novelty certification.

## Verdict

**The proposed theorem is a worthwhile explicit certification exercise, but the current ingredients do not support a major conceptual novelty claim.** Arbitrary finite-horizon projected branching, local value/gradient moment bounds, high-dimensional Allen–Cahn approximation, stability-based time-uniform numerical error, and the exact Jacobi spectral gap each have close precedents. The geometric error recurrence obtained by putting them together is elementary once its assumptions hold.

The defensible candidate contribution is narrower: a fully computable admissible interface for the project's *unchanged local derivative-coding tree*, together with a complete certificate for a nonstationary family and explicit dependence on accuracy, stability margin, representation size, and horizon. The challenge is to establish that interface contract from checkable input data, rather than to assume it. A one-dimensional perturbation of an explicitly known stable equilibrium would demonstrate this mechanism but would not by itself justify “Fields-level,” “first arbitrary-horizon branching solver,” or “curse-free long-time PDE solver.”

The strongest distinction worth pursuing is **simultaneous control of horizon and dimension for a constructively specified class of evolving solutions**. Neither a local tree variance bound nor a three-mode example establishes that distinction.

## Closest primary results actually inspected

The following descriptions distinguish a theorem that was read from an abstract-only lead. A missing claim in these sources is not evidence that no other paper proves it.

### S1. Moment envelopes for branching representations are established

Henry-Labordère, Oudjane, Tan, Touzi, Warin, *Branching diffusion representation of semilinear PDEs and Monte Carlo approximation*, Ann. IHP Probab. Stat. 55 (2019), 184–210. [Primary full text](https://arxiv.org/html/1603.01727).

Read Assumptions 3.1, 3.6, 3.10, Theorems 3.5 and 3.12, and the ODE comparison in the latter proof. For polynomial nonlinearities in value and first gradient, bounded differentiable diffusion coefficients and uniform ellipticity support automatic-differentiation weights. A smallness/explosion-time condition on a nonnegative moment majorant gives integrability; its version with an exponent at least two gives finite variance. The proof bounds absolute weighted tree products using a positive polynomial ODE. These conditions constrain horizon/nonlinearity; they are not a claim of time-uniform global variance.

**Overlap:** deriving positive tree-moment systems and certifying a supersolution is established methodology. **Potential difference:** the project's six-code closure, raw uniform label law, exponential clocks and explicit rational box are a concrete certificate for a different estimator. The comparison must preserve that distinction; replacing derivative codes by Malliavin weights changes the algorithm.

### S2. Projected branching continuation already removes a finite maturity restriction

Bouchard, Tan, Warin, Zou, *Numerical approximation of BSDEs using local polynomial drivers and branching processes*, Monte Carlo Methods Appl. 23 (2017), 241–263. [Author PDF](https://fime-lab.org/wp-content/uploads/2016/07/BTWZ17.pdf).

Read §§2.1–2.4, Theorem 2.4, Proposition 2.5, Assumption 2.6, Proposition 2.8 and Remark 2.10. The starting driver is Lipschitz in value, without gradient dependence, and the construction uses local polynomial drivers, Picard iteration and truncation at time-grid interfaces using an a priori solution bound. A fixed local width below a polynomial explosion threshold can be repeated over an arbitrary finite global horizon. Theorem 2.4 proves Picard convergence. Proposition 2.8 propagates functional approximation errors under its approximation-operator hypothesis.

Theorem 2.4's bound includes an exponential in the global horizon. Proposition 2.8 contains substantial dependence on iteration/slab counts. Therefore “any finite horizon” here must not be read as one error/cost constant valid as the horizon tends to infinity.

**Overlap:** splitting, clipping into an admissible range, local branching and controlled approximation at interfaces are already present. **Remaining distinction:** an explicit horizon-independent certificate for the unchanged derivative-coding estimator in a genuinely evolving invariant class.

### S3. Coherent gradient localization and uniform local L² bounds also have a direct precedent

Bouchard, Tan, Warin, *Numerical approximation of general Lipschitz BSDEs with branching processes*, ESAIM Proc. Surv. 65 (2019), 309–329. [Primary full text](https://arxiv.org/html/1710.10933).

Read §2 assumptions, the face-lifting operator, Remark 2.2, Theorem 2.1, Proposition 3.1 and Remark 3.2. Bounded Lipschitz data and bounded differentiable uniformly nondegenerate diffusion coefficients underpin value/gradient bounds. Function-level localization is nonexpansive in the supremum norm, fixes admissible solutions, and is applied at Picard interfaces.

Proposition 3.1 gives local value/gradient second-moment bounds, uniformly over slab and Picard indices, below explicit width thresholds. Its lifetime density is proportional to the negative two-thirds power of lifetime on the unit interval, with coefficient-based offspring probabilities. It proves the representation; Theorem 2.1 supplies finite-horizon convergence.

**Overlap:** smoothness-compatible localization and reusable local L² control are not new abstractions. **Difference:** this does not prove an arbitrary-jet interface theorem or the project's raw exponential-clock code-tree certificate. Local uniformity over slab indices is also weaker than a global error constant independent of the horizon.

### S4. Allen–Cahn already has a polynomial-dimension, arbitrary-finite-T approximation theorem

Beck, Hornung, Hutzenthaler, Jentzen, Kruse, *Overcoming the curse of dimensionality in the numerical approximation of Allen–Cahn partial differential equations via truncated full-history recursive multilevel Picard approximations*, J. Numer. Math. 28 (2020), 197–222. [Primary full text](https://arxiv.org/html/1907.06729).

Read Theorem 1.1, Theorem 4.5, estimates (144)–(145), and Corollaries 5.1–5.2. Theorem 1.1 fixes a finite horizon and assumes bounded initial data, classical solutions with a spatial growth bound, continuously differentiable reaction with polynomially growing derivative, and coercivity. For each positive exponent slack η, it obtains RMS accuracy ε with cost `c d ε^(−2−η)`. The cost counts scalar Gaussian draws; input-function evaluation cost needs separate accounting.

The horizon is fixed **before** the cost constant is chosen. Estimates (144)–(145) contain `exp(L(r)T)(1+2L(r)T)^n`; this is not a uniform-horizon complexity bound.

**Implication:** extending an Allen–Cahn example beyond the raw tree's moment blow-up is not alone a new PDE-solving capability. A time-uniform guarantee can be sharper in horizon while still much narrower in dimension and data class.

### S5. Finite regression interfaces with full error analysis are not new in themselves

Neufeld, Schmocker, Wu, *Full error analysis of the random deep splitting method for nonlinear parabolic PDEs and PIDEs*, Commun. Nonlinear Sci. Numer. Simul. 143 (2025), 108556. [Primary full text, v4](https://arxiv.org/html/2405.05192).

Read Assumptions 3.1–3.6, 3.11, Theorem 3.12 and Corollary 3.13. Under global Lipschitz/growth, temporal regularity and jump assumptions, with suitable initial moments and full-support random features, the method uses least-squares linear readouts and truncation. Theorem 3.12 separates time/distribution discretization, function approximation, truncation and statistical errors. Its displayed regression term depends on feature count, training sample count and a logarithmic factor. The constants explicitly depend on the horizon. The feature count in its universal-approximation statement is existential, so that statement alone is not a polynomial complexity bound in dimension and accuracy.

**Overlap:** replacing difficult nonlinear neural training by a finite linear regression and proving all error terms is established. **Difference:** the paper does not supply the derivative-code admissibility conditions or a horizon-uniform certificate sought here. Any proposed neural/random-feature extension should be compared against this complete-error baseline, not only against uncertified neural experiments.

### S6. Strong contraction already enables high-dimensional infinite-lifetime formulations

Beck, Gonon, Jentzen, *Overcoming the curse of dimensionality in the numerical approximation of high-dimensional semilinear elliptic partial differential equations*, PDE Appl. (2024). [Primary PDF](https://arxiv.org/pdf/2003.00596), [journal DOI](https://doi.org/10.1007/s42985-024-00272-4).

Read Theorem 1.1 and its discussion. It treats the elliptic equation Laplacian of u equal to f(x,u), requiring that f minus a positive linear term has Lipschitz constant strictly smaller than that linear coefficient. Together with stated polynomial source growth and subexponential solution growth, this yields an MLP approximation with work polynomial in dimension and reciprocal accuracy. Exponentially distributed lifetimes give a stochastic fixed-point representation on an infinite time interval.

**Relevance:** contractivity can change the computational problem materially, and fixed-time parabolic results are not the only comparator. **Limit:** this theorem concerns stationary elliptic solutions under strong global monotonicity, not arbitrary moving parabolic trajectories or local odd-sector stability of Allen–Cahn. One should not infer that it directly proves the proposed theorem, but it weakens any broad “first unlimited-time probabilistic solver” slogan.

### S7. The proposed Jacobi spectral gap is an existing explicit theorem

Wakasa, *Exact Eigenvalues and Eigenfunctions Associated with Linearization for Chafee–Infante Problem*, Funkcial. Ekvac. 49 (2006), 321–336. [Primary PDF](https://www.jstage.jst.go.jp/article/fesi/49/2/49_2_321/_pdf).

Read §4, Proposition 4.2, Theorem 3 and Remarks 4.2–4.3. For the Dirichlet single-bump stationary solution of the cubic reaction problem, Theorem 3(i) gives the principal eigenvalue of the negative linearization as three halves times squared amplitude times the reaction parameter. Remark 4.3 gives the corresponding Jacobi sine-times-delta-amplitude eigenfunction. The nodal argument identifies the principal eigenvalue, rather than merely exhibiting some eigenfunction.

Rescaling to the project's diffusion coefficient and amplitude gives the gap **3m/(1+m), hence 1/7 at m=1/20**, for the odd periodic sector identified with the single-bump Dirichlet problem. This is a direct specialization of the published result.

**Limit:** a spectral gap at one equilibrium is not automatically a pairwise nonlinear contraction estimate on a whole projected set. That set and its nonlinear perturbation bound still need proof. The symmetry restriction is essential: the equilibrium has a translation zero mode on the unrestricted circle, precluding strict contraction there.

### S8. Time-uniform error from asymptotic stability is an older numerical-analysis principle

Larsson, *The Long-Time Behavior of Finite-Element Approximations of Solutions to Semilinear Parabolic Problems*, SIAM J. Numer. Anal. 26 (1989), 348–365. [Publisher record and abstract](https://epubs.siam.org/doi/10.1137/0726019).

The primary publisher abstract was accessible; the full theorem assumptions were not inspected. It explicitly reports optimal-order error estimates uniform on the unbounded time interval under asymptotic stability of the exact solution, for semidiscrete and fully discrete approximations. This is sufficient precedent for the general principle, but not a substitute theorem for the proposed stochastic scheme.

A recent spectral lead is Miyamoto–Takemura–Wakasa, *The Lamé Equation on a Circle and Applications to Singular Limit Eigenvalue Problems* (2026), [publisher abstract](https://journals.sagepub.com/doi/abs/10.1177/09217134251390057). Its abstract announces exact circle spectra for the first two integer Lamé orders and applications to Allen–Cahn. Only the abstract was accessed; no uninspected theorem from it is used here.

## What follows by a standard composition argument

This subsection is an independent derivation, not a claim extracted from the sources above. It makes clear which part is easy and where the actual construction must do work.

Let S_h be the exact PDE time-h map on a set A. Suppose:

1. Every exact intermediate flow from an admissible interface remains in a region where `||S_h v − S_h w||₂ ≤ q ||v−w||₂`, with a known `q<1` independent of step index.
2. V is an m-dimensional subspace, P its orthogonal projection, and K is a computably projectable closed convex subset of V. Every element of K satisfies the terminal bounds required by the *actual* local estimator, almost surely.
3. For every target grid time, `P u_j ∈ K` and `||(I−P)u_j||₂ ≤ δ`, uniformly in j. This is stronger than smoothness or the existence of some nearby admissible polynomial.
4. Given all previous randomness, the coefficient estimator is `P S_h(v_{j−1}) + ξ_j`, with conditionally centered ξ_j and `E[||ξ_j||₂² | past] ≤ σ²/N`. The stored output is its metric projection onto K.

Orthogonality, metric-projection nonexpansiveness relative to `P u_j`, and conditional centering give

`R_j := E||v_j−u_j||₂² ≤ q² R_{j−1} + σ²/N + δ²`.

Consequently

`R_j ≤ q^(2j) R_0 + (σ²/N+δ²)(1−q^(2j))/(1−q²)`.

For fixed admissible h, choosing `N ≥ 2σ²/[(1−q²)ε²]` and `δ² ≤ (1−q²)ε²/2` gives the desired uniform error floor. The RMS conclusion is `sup_j (E||error_j||₂²)^(1/2) ≤ ε`, when the initial error also meets the bound. It is **not** an estimate of `E[sup_j ||error_j||₂²]` or of an all-time high-probability event.

The derivation does not require the metric projection itself to preserve pointwise order. “Projects into a PDE-invariant order interval” and “is an order-preserving map” are different statements. A Fourier coefficient projection has no automatic pointwise-order property. Nor can finite spatial samples certify an everywhere inequality without a separate interpolation/positivity argument.

The genuine proof obligations are assumptions 1–4, with constants that remain useful after accounting for all code observables. The prior stationary example establishes assumption 3 only for its stationary target, not for a moving family. If `P u_j` is inadmissible, the preceding squared-error proof cannot silently be reused; a different projection-bias estimate is required.

## Complexity and baseline traps

With n slabs and a fixed local expected tree cost, work is linear in n. This is an accounting consequence, not an independent algorithmic breakthrough. A useful bound must include coefficient evaluation, terminal derivatives, constrained projection and certification, plus the dependence of m, local moment bounds and h on d and ε. A tensor product with k modes in each coordinate has `m=k^d`; no dimension claim follows from cheap individual Brownian draws.

For `q=e^(−αh)`, the denominator `1−q²` is asymptotic to `2αh` as h tends to zero. Thus using a variance bound independent of h gives an explicit root-sampling cost proportional to `T σ²/(α h² ε²)` before interface evaluation costs. “O(T ε⁻²)” hides h, the stability margin, and representation complexity; they should be displayed, even if h is fixed at 0.08. A fixed three-mode space also has a nonzero approximation floor and cannot establish an arbitrary-ε theorem.

If only the value at a late endpoint is requested and the stable equilibrium g* is already explicitly known, the baseline is especially strong: return g* once `e^(−αT)||u₀−g*||₂ ≤ ε`. For the exactly stationary benchmark, returning the supplied initial function is already exact. A long rollout is then a certification test, not a demonstration of superior endpoint complexity. Linear work in T is more meaningful for a full trajectory or for time-dependent forcing/unknown attracting states.

The same-datum proof that the unsplit raw rate-2 tree has infinite second moment remains valuable: it identifies an estimator pathology that the local-interface method avoids. It should be advertised as an **estimator-specific separation**, not as an impossibility result for MLP, all branching representations, all clock laws, or PDE solvers generally.

## Contribution boundary

| Proposed component | Assessment from this review |
|---|---|
| Repeat short branching solves to reach arbitrary finite T | Established, S2–S3 |
| Enforce admissibility with a nonexpansive interface operation | Established principle, S2–S3 |
| Use positive polynomial envelopes to prove tree moments | Established method, S1 |
| Exact gap 1/7 for this odd Jacobi equilibrium | Direct specialization of S7 |
| Uniform error from strict contraction and bounded local error | Standard geometric recurrence; broad numerical precedent S8 |
| All-code admissible finite interfaces with explicit moving-target bias | Potential constructive contribution; must prove it, not assume it |
| Same-datum finite-error continuation beyond raw-tree L² blow-up | Useful project-specific separation, subject to the existing proof audit |
| Dimension-polynomial work with constants uniform in T | Not established by the current benchmark; meaningful research target |

## Two ambitious questions that remain grounded in this project

**Q1. Can derivative-code continuation have a simultaneous polynomial-dimension and uniform-horizon complexity theorem, without an exact solution or attractor oracle?** Specify an input class of dissipative semilinear problems, a constructive representation family and a norm that controls every reachable code. The target would bound the *total* work for an evolving trajectory by `C T poly(d,ε⁻¹)`, with C independent of T and explicit dependence on dissipation. A valid result must obtain the interface approximation/admissibility property from input assumptions, include regression/projection cost, and use dimension-dependent baselines S4–S6. The current finite closure is a tractable starting point, but generic higher derivatives and dimension-dependent approximation complexity are the main obstacles. Merely postulating a polynomial-size good interface would leave the core theorem conditional.

**Q2. Can one replace exact-attractor-dependent admissibility with an a posteriori, self-validating continuation certificate for unknown or forced dynamics?** The solver would compute a finite interface, a local raw-tree moment certificate, and a deterministic enclosure proving that the true evolving solution remains in a contracting admissible tube. The certificate must control the terminal code family and spatial tails, and either certify continuation or explicitly fail; it cannot use the reference solution to choose its tube. Time-dependent forcing or a non-explicit stable branch would defeat the trivial equilibrium-return baseline. A substantial result would cover a class of problems with a complexity estimate and identify exactly where stability, code growth or approximation width makes certification impossible. Doing this only for the known Jacobi formula would be a preliminary case study.

Both questions are considerably harder than the present composition lemma. This review does not claim they are open in full generality or that solving a restricted version reaches a particular prestige threshold. Before choosing either as a headline, the next literature pass should target its exact input class and norm, particularly existing verified parabolic numerics and approximation-complexity results.

## Recommended claim language and decision

Use: “An explicit time-uniform error certificate for projected continuation of the original local derivative-coding estimator on a specified nonstationary, symmetry-restricted Allen–Cahn class,” **if** all constructive obligations are completed.

Do not use: “A new general arbitrary-time branching method,” “dimension-free continuation,” “global stability of periodic Allen–Cahn,” or a claim that the Lamé gap is new.

Continue the dynamic benchmark as a falsifiable construction test. Treat a successful result as groundwork for Q1 or Q2, and stop escalating its novelty rating merely because the horizon becomes arbitrarily large. The review located no theorem with the exact combined estimator/interface contract above, but the bounded search cannot establish absence of prior art.

## Addendum: dynamic polygon certificate and proposed analytic extension

The parent and T01 subsequently reported a nonstationary invariant class `u(t,x)=g(x)R(t,g(x)²)` on `0≤z≤a=2/21`, with `0.9≤R≤1`, `|R_z|≤1/35`, and `|R_zz|≤1/50`. They reported an admissible two-parameter polynomial interface, uniform approximation error below `1/140000`, and a robust projection estimate giving RMS below `0.02` at every grid time with 100,000 roots per slab. These construction/proof claims are recorded as reported; T03 has not independently rederived the inequalities. In particular, the robust projection argument need not use the stronger assumption `P u_j∈K` in the sufficient composition lemma above. A correctly proved alternative bias recurrence is legitimate.

That result would close a substantive gap in the earlier stationary demonstration: admissible interfaces now approximate an evolving class with explicit constants. It remains a restricted constructive certificate assembled from established principles. The proposed next step is a time-uniform derivative bound

`sup_z |∂_z^k R(t,z)| ≤ (k!/35) 2^(k−1),  k≥1`,

followed by polynomial approximation, inward mixing, and projection subject to global polynomial inequalities. **The all-order bound and the resulting arbitrary-accuracy theorem were pending when this review was written.** Low-order invariance alone does not establish them.

### S9. The approximation-plus-noise mechanism already yields the proposed logarithmic factor

Cohen and Migliorati, *Optimal weighted least-squares methods*, SMAI J. Comput. Math. 3 (2017), 181–203. [Primary manuscript](https://arxiv.org/html/1608.00512).

Read Theorems 2–3, Corollary 1 and §4, including Remark 1. Independent samples, an appropriate sampling measure and weight, and a Christoffel-function condition give stable near-best approximation. The optimal weight reduces the stability requirement to sample size of order `m log m`. Theorem 3 treats conditionally centered noise with uniformly bounded conditional variance, as well as deterministic bias; its expected squared error consists of best-approximation, bias, variance and bad-conditioning terms. The variance term has scale `mσ²/N` for ordinary sampling, and also for the stated optimal weighting. This is a one-step regression result, not a PDE continuation theorem or a derivative-admissibility certificate. Its truncated approximation need not retain the smooth terminal structure required by this project.

The following rate calculation is independent elementary algebra. If the proposed derivative bound holds at all times, Taylor's theorem at `z=a/2` gives, for the degree-p Taylor polynomial `P_p`,

`||R−P_p||_∞ ≤ a^(p+1)/70`.

Thus `m=p+1=O(log(1/ε))` suffices for scalar approximation. Converting this to an *admissible* approximation still requires simultaneous derivative bounds, a quantitative inward margin and control of the mixing error. Provided these hold, and the coefficient-estimation variance has scale `m/N`, contraction gives `N=O(ε⁻² log(1/ε))` for fixed h and fixed contraction margin. Analytic approximation plus finite-dimensional sampling already explains this rate; the exponent is not by itself a new Monte Carlo phenomenon. Here m is **interface dimension**. The spatial dimension remains one.

There is also established global Gevrey regularity literature for dissipative polynomial gradient flows. Chen, Wang and Wise, *Global-in-time Gevrey regularity solution for a class of bistable gradient flows* (2016), [primary publisher abstract](https://www.aimsciences.org/article/doi/10.3934/dcdsb.2016018), obtains global regularity using energy/Sobolev bounds and local Gevrey estimates. Only its abstract was inspected, and its listed examples include thin-film and phase-field-crystal equations. It is background precedent, **not** a verified theorem covering the present degenerate equation in z or its proposed explicit factorial constants. The exact all-order invariant inequalities could be a useful construction even though analyticity itself is classical.

### What an accuracy-complexity claim must still count

`O(T ε⁻² log(1/ε))` is defensible as a **sampled-root count** only after the degree-independent local moment and expected tree-size bounds are established. It is not automatically total arithmetic work. A straightforward implementation evaluates m features per sample and an m-term polynomial at terminal leaves; this can produce `O(T ε⁻² log²(1/ε))` arithmetic before constrained projection, even when the number of leaves per root stays bounded. An improved implementation could change that estimate, but needs its own proof. Global polynomial nonnegativity constraints, numerical projection error, coefficient conditioning, and certificate precision also have costs. A sum-of-squares formulation supplies a route to enforcing constraints; it does not by itself prove the claimed runtime or exact feasibility of floating-point output.

Finally, increasing the polynomial degree does not remove the known-equilibrium baseline. For this same invariant basin, an endpoint approximation may return g after the certified contraction time. A deterministic spectral method can also exploit analytic spatial regularity. Any practical or complexity comparison should include these baselines and should state whether the output is a single endpoint, a prescribed grid of the full trajectory, or forced/unknown-attractor dynamics. No optimality claim against general deterministic PDE solvers is warranted.

The bounded follow-up search found close results for each of analytic approximation, noisy projection, localized branching and stability-based long-time error, but did not identify a paper proving this exact combined all-code certificate. The appropriate next claim is therefore an explicit, arbitrarily accurate construction **if its pending proof closes**, rather than a new general theory of time-uniform Monte Carlo PDE approximation.
