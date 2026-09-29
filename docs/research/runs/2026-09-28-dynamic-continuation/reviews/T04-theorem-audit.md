# T04 — independent end-to-end conventional theorem audit

Date: 28 September 2026. Reviewed `04-theory.md`, `02-plan.md`, T01 Sections 1–15, T02 Sections 1–9, and the preceding run's C4/C9 and expanded positive-moment proof. This review owns only this file. No implementation, experiment, or Lean work was performed. The prior C4 local stochastic theorem is an explicit conventional input, as instructed; it was not reconstructed as a new probability theorem here. Research role/model is retained from T03; serving-model telemetry is unavailable.

## Verdict and ranked findings

**No blocking mathematical error was found in the combined fixed-step, ideal-arithmetic theorem for the specified symmetric Allen–Cahn class.** The two-dimensional RMS bound, Bernstein hierarchy, analytic hierarchy under its stronger initial assumptions, and same-family rate-two raw second-moment obstruction survive the independent checks below. This conclusion is conditional on the named standard periodic parabolic inputs and the imported C4 mean/moment theorem. It does not certify a floating implementation, a population claim from three runs, or a new general method.

| Rank | Finding | Consequence |
|---|---|---|
| Blocker if omitted from a final theorem | Exact initial access or an explicit initial approximation error | A general smooth `R0` is not exactly represented by a fixed polynomial space. T02 allows the first terminal to be the given smooth `u0`; T01 alternatively gives a feasible Bernstein initialization. State which contract is used. The concrete `.9g` datum is exactly represented and has no issue. |
| Blocker for implementation claims, not the ideal theorem | Exact Gram metric and exact feasible projection are assumed | Floating quadrature, an approximate optimizer, or checking constraints on a finite grid does not automatically inherit the stated RMS constant. The theory and plan already disclose this boundary. |
| Explicit analytic input, not a discovered counterexample | Positive-time convergence in sufficiently high spatial derivatives is needed for the C² extension | Uniform convergence alone would not pass quotient derivatives through a zero of g. Standard semilinear smoothing supplies the stronger convergence; the precise argument is supplied below. |
| Limitation | The analytic rate counts sampled roots at fixed h, μ and local moment bound | It omits degree-dependent evaluation, Gram conditioning, projection, setup and precision costs. It says nothing about spatial dimension beyond this one-dimensional problem. |
| Limitation | The error guarantee is ensemble spatial RMS at each fixed grid endpoint | It is neither a simultaneous all-time event nor a pointwise/high-probability statement. Three empirical realizations cannot verify its expectation or rare tails. |
| Limitation | The same-family obstruction fixes the raw rate-two, uniform-label tree | It proves an infinite second moment for that estimator, not failure of the PDE, pathwise tree termination, every importance law, or every representation. |

The first two rows identify conditions under which extending the present wording would become false or unsupported; they are not unresolved defects of the concrete `.9g`, exact-projector theorem as presently qualified. No numerical gate should be inferred from this review beyond that exact scope.

## 1. The endpoint quotient has a valid regularity bridge

The assertion `u=gR(g²)` cannot be justified just by division at interior points. I checked that the preserved symmetries provide the missing bridge here.

At a zero, put the zero at `x=0`. Smooth oddness and the simple zero of g give

`g(x)=x γ(x²)`, `u(t,x)=x η(t,x²)`, `γ(0)≠0`,

with smooth functions of the squared coordinate. Then `z=x²γ(x²)²` has a smooth local inverse as a function of `x²`, since its derivative at zero is positive. Consequently `R=η/γ`, composed with this inverse, is smooth through `z=0`. At a peak `x*`, reflection symmetry makes u and g smooth even functions of `x−x*`. Also `g(x*)>0` and `g''(x*)<0`, so `a−g²` has a nondegenerate quadratic zero there. Inverting the squared coordinate gives a smooth R through `z=a`. The argument works jointly in t on finite smooth time intervals. Oddness alone would not give the peak reflection needed here, but the specified initial composition has that additional symmetry, and uniqueness preserves it.

For a merely C² `R0`, the preserving Bernstein approximants converge in C². Their original periodic initial functions converge in C² as well. A sufficient precise smoothing input is convergence of the corresponding u solutions in C⁵ in x, uniformly on every `[τ,T]` with `τ>0`. Dividing an odd function by a fixed simple zero and factoring the remaining even function through the squared coordinate is continuous from these symmetric C⁵ functions to C² functions of z. Hence the R, Rz and Rzz bounds pass uniformly at every positive time. The initial bounds are supplied directly at t=0. Standard bounded semilinear parabolic smoothing and continuous dependence provide this input; it should be understood in that stronger topology, not merely C⁰.

For the analytic hierarchy, smooth initial R0 gives a smooth periodic u0. The same argument can be applied with arbitrarily many finite derivatives, using C^(2k+1) regularity for the k-th quotient derivative. Thus the induction does not create a circular need to assume the desired factorial derivative bound just to justify differentiating the equation. Smoothness and the factorial bound are distinct statements.

Direct substitution gives the stated coefficients

`A=2z(z²−2z+C)`, `B=5z²−8z+3C`.

At the endpoints, `A=0`, `A'(0)=2C`, `B(0)=3C`, `A'(a)=4a(a−1)`, and `B(a)=2a(a−1)`. The k-th differentiated drift is therefore positive at zero and negative at a. At a left endpoint maximum its one-sided derivative is nonpositive; at a right endpoint maximum it is nonnegative. The drift term is nonpositive in both cases and the diffusion term vanishes. No missing Neumann boundary condition is required. Applying this argument before proving endpoint smoothness would have been invalid; the supplied factorization repairs that potential gap.

## 2. Low-order invariance and all-order induction

Independent differentiation reproduces the p and q equations in the main theory. In particular, the q forcing coefficient is `12−6R²`; replacing it by only one differentiated reaction contribution would be wrong. On the stated range, the displayed damping and forcing estimates give the two closed barriers. The terminal derivative identity `v'=g'[R+2zRz]` then gives the required global C4 envelope for every feasible terminal, independently of its learned coefficients.

For the higher-order equation, Leibniz differentiation gives the coefficient of `r_k` as

`binom(k,2)A'' + kB' + z(1−3R²)`

and the coefficient of `r_(k−1)` as

`12 binom(k,3) + 10 binom(k,2) + k(1−3R²)`.

These simplify exactly to the stated `C_k` and `E_k`. The nonlinear remainder separates triples with one zero derivative index from triples with three positive indices. Their counts are respectively `k−1` and `(k−1)(k−2)/2`; the factor 3R in the first group is correct, including its ordering multiplicities. I found no missing highest-order derivative in `N_k`.

For `k≥2`, `E_k` is nonnegative: even its worst reaction correction `−2k` is smaller than `k(k−1)(2k+1)`. The upper damping bound follows directly from `z≤2/21` and `1−3R²≤0`:

`C_k ≤ −k(72k+76)/21`.

Using `M_(k−1)/M_k=1/(2k)` yields precisely `S_k` in T02, including the terms from `kN_(k−1)`. The allegedly problematic triple expression at k=2 and k=3 is zero, not negative. The coarse bound `S_k≤(493/400)k²` is valid and is far below `(24/7)k²≤D_k`. The first-derivative base uses a strict damping margin as stated. The induction is for every finite k; it does not require exchanging a limit in k with the maximum principle. Thus the uniform factorial estimate follows for the stronger smooth initial class.

The sharper `|Rzz|≤1/50` must still be retained separately: the factorial bound at k=2 is weaker. The theory does retain it. Also, the main analytic theorem fixes the lower barrier `.9`; mixing toward `.95` would fail to preserve a stronger lower barrier above `.95`. T01 explicitly separates that extension rather than silently making it.

## 3. Projection and random learned trajectories

I checked the variance statement in an orthonormal basis before translating back to Gram coordinates. For each coefficient, fresh conditional root independence and the pointwise C4 second-moment bound give a variance at most `M/N`. Summing yields `dM/N`. Shared samples create coefficient correlations but do not change this trace bound. The Gram estimator is the same random element expressed in a nonorthogonal basis.

Let `Z=P_V S_h(v_prev)+ξ`, with conditionally centered ξ, and `c*=Π_K P_Vu=Π_Ku`. Nonexpansiveness gives

`E(||Π_KZ−c*||² | past) ≤ ||P_V(S_h(v_prev)−u)||² + dM/N`.

Contraction applies to each realized pair of exact one-step PDE flows because both starting functions lie in the invariant order interval. Minkowski then gives

`r_j ≤ sqrt(exp(−2μh) r_(j−1)² + dM/N) + dist(u_j,K)`.

This establishes the recurrence without claiming the projected noise is unbiased and without assuming the ordinary orthogonal target projection is feasible. Both would be false shortcuts in general. The true solution supplies only the deterministic comparison distance; it is never supplied to the estimator.

In particular, no analytic estimate for the random learned PDE trajectory is needed. The stronger approximation result is used only on the fixed true target. The learned terminal needs the stated global value/derivative bounds, while its one-step exact flow needs the order band for contraction. This distinction is sufficient and does not hide a reset of the true target at each slab.

The proposed invariant radius is correct. With `ρ=exp(−μh)`, `b=β/(1−ρ)` and `s=sqrt(ν/(1−ρ²))`,

`ρ²(b+s)²+ν ≤ (ρb+s)²`,

and `ρb+β=b`. This yields the claimed bound by induction. The fixed numerical budget uses the correct squared contraction factor. The exact rational comparison supplies the strict margin below `.02`; this audit found no missing normalization or factor of two.

## 4. High-degree approximation and computation boundary

The Bernstein coefficient conditions are sufficient globally, not just at samples. Their witness second differences are bounded by `a²/(50n²)`, which is stronger than the stated coefficient constraint. The binomial-variance argument gives `β_n=a^(5/2)/(400n)` correctly. This is a valid C² approximation hierarchy and gives the stated root-count exponent at fixed h.

For the analytic hierarchy, applying Taylor's theorem to derivatives separately gives the stated `e_(n,j)` for j=0,1,2. They all use `M_(n+1)`; no unjustified differentiation of a value-only remainder occurs. The mixing parameter in `04-theory.md` is below one for n≥4 and dominates each required margin. The resulting pointwise polynomial set is compact and convex: its uniform value bound controls coefficients in each fixed finite-dimensional space, and its inequalities are closed and convex. Multiplication by g is injective on that polynomial space, so its dimension really is n+1.

The estimate by `(8/21)^n` follows from the stated elementary bound on `n(n+1)` and `sqrt(a)<1/3`. T01's alternate mixing parameter `κ/(1+κ)` is a different valid construction; it must not be substituted into the main formulas without also changing its error constants. Neither construction is asserted to satisfy the Bernstein coefficient constraints, correctly.

T01's interval positivity representation supplies a finite convex description of the exact feasible polynomial set. This does not establish a numerical algorithm with the same error bound at finite precision, or total arithmetic complexity. The main theory correctly limits the claim to exact metric projection and sampled-root count. Given the known stable g, late endpoint approximation also has the return-g shortcut. Those limitations do not invalidate the sampled-root upper bound, but they prevent interpreting it as a general optimality or usefulness result.

## 5. Same-family raw second-moment obstruction

The transfer to nonstationary terminal data uses a valid lower bound that depends only on their magnitude band:

`f(v)² ≥ (81/100)(19/21)² g² > (16/25)g²`.

The wrapped heat kernel is measured against ordinary Lebesgue measure. Combining its lower bound `1/192` with `∫g²>1/40` gives the seed `1/12000` after multiplication by `16/25`; there is no omitted normalized-spatial factor L. The proof keeps a fixed terminal v throughout. It does not substitute the unknown evolving solution into the unsplit tree.

The squared moment system retains the original raw tuple probabilities. Normalizing by `exp(−2t)` produces the `exp(2t)` coefficients in the retained F subsystem, while the Id source has coefficient 1/2. The positive restarted comparison is valid as a comparison of nonnegative mild/Picard systems with extended moments; it does not differentiate infinite quantities or assume finiteness to prove blow-up.

With `Z_s=A`, direct integration indeed gives `D=36Z`, `B=18Z²`, and `A=a0+6Z³`. Splitting the scalar explosion integral at `1/30` gives 400+75. Its physical time is strictly below 7/2. Most importantly, `∫A ds=Z→∞`, and the Id mild equation integrates that spatially uniform lower bound over the entire pre-explosion interval. Thus the Id second moment is infinite for every starting position at T≥7/2; this is stronger than merely noticing a descendant field diverges. No conclusion about a finite ordinary mean or variance is supplied by this calculation.

This establishes the same **fixed input family** for the controlled and uncontrolled comparison. It does not mean the two methods sample the same random variable: projection continuation is intentionally biased. The same-family wording is appropriate; calling it an unbiased-estimator improvement would not be.

## 6. Statistical plan and release boundary

The plan correctly prespecifies the main datum, three seeds, 100,000 fresh roots per slab and the finite horizons. It distinguishes the theorem's ensemble RMS from the three-seed empirical RMS, and it treats deterministic reference convergence as an empirical check with no rigorous error enclosure. The odd-sine reference respects the actual symmetries. The plan also requires the nonlinear quadrature to resolve the relevant polynomial Fourier products, rather than assuming an arbitrary grid is exact.

A time-cap interruption must remain an incomplete realization. Reporting only completed seeds as though they were the prespecified ensemble could introduce selection by tree cost, which can correlate with outputs. The existing instruction to retain incomplete records and not replace the primary run addresses this; it must be respected in the eventual report. Per-stage data, tails and timing can diagnose implementation behavior but cannot empirically prove finite second moments or the uniform population bound.

The theory is ready for the stated finite formalization gate, subject to its explicit imported inputs. After that gate, the two-coefficient experiment can test the frozen implementation contract. No simulation is needed to repair a mathematical blocker found here, because none was found within the scoped theorem.

## 7. Follow-up audit: proposal-invariant absolute obstruction by T=13

After the main audit, the parent proposed the stronger D8 statement. I checked its probability argument and constants independently before recording the result here. **The statement is sound under the precise supported, nonexplosive, exactly weighted single-tree contract below.** It strengthens the estimator-class scope of the obstruction at a later sufficient horizon; it does not improve the rate-two threshold 7/2.

### 7.1 What is fixed, and where adaptivity is allowed

Keep the original derivative-code mechanisms, scalar code multipliers, terminal evaluations, Brownian motion and fully expanded product for a single sampled tree. Permit conditional lifetime/tuple proposals depending on code, position, remaining time and previously revealed history. Require their densities, probabilities and leaf survivals to be positive almost everywhere on every nonzero canonical completed-tree contribution, and require the exact reciprocal conditional likelihood factors. Retain the earlier nonexplosion assumption so the full tree completes almost surely at each finite horizon. Topological support alone is insufficient: it does not supply an importance-sampling Radon–Nikodym derivative.

This is the same contract as the existing [25 September L1 theorem](/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-25-long-horizon/04-theory.md) and its [independent review](/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-25-long-horizon/09-independent-theory-review.md). Proposal cancellation is already established there for flat data; it is not a new concept in D8.

For a finite completed topology, multiply the absolute output by its **whole joint proposal density**. Each conditional sampling factor, including leaf survival, cancels its reciprocal. What remains is the absolute product of code multipliers and terminal factors integrated against the canonical event-time and Brownian kernels. This remains valid when the proposal correlates later choices with earlier subtrees: factorization into child integrals is performed only **after** cancellation, under the canonical kernels. Directly factorizing conditional expectations of proposal-dependent child outputs would be an unsupported independence step.

Restrict the full-tree functional to completed trees of depth at most n. These restrictions increase in absolute value to the full absolute output on every finite realized tree. Monotone convergence identifies its extended absolute expectation with the proposal-independent nonnegative topology sum, without an integrability assumption. The cutoffs are restrictions of the full expansion, not a new adaptive algorithm whose proposal is silently changed when a branch is truncated.

### 7.2 Absolute system and the explicit lower comparison

Write W for this minimal nonnegative absolute-moment system, with initial data

`(|v|, |v'|, |f(v)|, |f'(v)|, |f''(v)|, 6)`.

The signed local reaction from C4 is replaced term by term by its absolute scalar multipliers. In particular,

`W_Id,t = (1/2)W_Id,xx + W_0`,

`W_0,t = (1/2)W_0,xx + W_0 W_1 + (1/2)W_D² W_2`,

`W_1,t = (1/2)W_1,xx + W_0 W_2 + (1/2)W_D² W_3`,

`W_2,t = (1/2)W_2,xx + W_0 W_3`, `W_3=6`.

These are nonnegative mild identities, including infinite values. There is no clock or tuple parameter, and unlike the squared-moment system there is no exponential normalization.

For the same fixed terminal family `v=gR0(g²)`, `.9≤R0≤1`,

`|f(v)| ≥ (57/70)|g| > (4/5)|g|`,

and `|f'(v)|=1−3v²≥5/7`. Since `|g|<1/3`, the existing integral estimate implies `∫|g|>3∫g²>3/40`. The time-one heat lower bound therefore gives `W_0(1,x)>1/3200`, uniformly in x; nonnegative sources give `W_1(1,x)≥5/7` and `W_2(1,x)≥0`.

Drop the derivative terms and restart the constant lower system at physical time one:

`A'=AB`, `B'=AC`, `C'=6A`, `(A,B,C)(0)=(1/3200,5/7,0)`.

Let `Z'=A`, `Z(0)=0`. Direct integration gives

`C=6Z`, `B=5/7+3Z²`, `A=1/3200+(5/7)Z+Z³`.

Hence its additional lifetime τ* satisfies

`τ* = ∫₀^∞ [1/3200+(5/7)Z+Z³]⁻¹ dZ`

`≤ (7/5) log(16007/7) + 1/2 < 117/10`.

The split is at Z=1: omit the cubic term below one and the positive lower-order terms above one. For the last strict inequality, `e>8/3` and `(8/3)^8>16007/7`, so the logarithm is below 8. Thus the physical comparison explosion time is below `127/10<13`.

The root-specific conclusion follows from its mild integral, not just a descendant blow-up. For any T≥13,

`W_Id(T,x) ≥ ∫₁^(1+τ*) A(r−1) dr = lim_(s↑τ*) Z(s) = ∞`.

The heat semigroup preserves this spatially constant lower bound. Therefore every proposal in the stated class has `E|H_Id(T,x)|=∞` and consequently `E[H_Id(T,x)²]=∞`, for every x and T≥13. This is a sufficient upper bound on an integrability horizon, not its exact value. No finite ordinary expectation representing the PDE is justified there.

The proof uses only the magnitude band for the obstruction; the derivative restrictions are needed for the controlled continuation theorem. It does not cover methods that regroup signed trees, integrate cancellations inside a sample, absorb reaction terms into another propagator, use bounded-majority branching, or change representation. Such exclusions are mathematical boundaries of the fixed integrand, not merely implementation details.

### 7.3 Close prior results and novelty boundary

The nearest external primary result found is Blömker, Romito and Tribe, *A probabilistic representation for the solutions to some non-linear PDEs using pruned branching trees* (2007), [Theorem 4.1 and §4.2](https://www.numdam.org/article/AIHPB_2007__43_2_175_0.pdf), which were inspected directly. For their branching representation of mode systems, positive comparison expectations are the minimal positive mild solution. The comparison equals the absolute expectation when the bilinear evaluation preserves products of norms. Their §4.2 and Remark 4.4 discuss weight-independent comparison equations and finite-time failure of integrability in covered examples. This is close prior art for the comparison and obstruction method, although it is not the present physical-space six-code Allen–Cahn theorem with these constants.

Henry-Labordère, Tan and Touzi, *A numerical algorithm for a class of BSDEs via branching process*, [Remark 2.14](https://arxiv.org/pdf/1302.4624), explicitly separates offspring-probability-independent integrability from offspring-probability-dependent variance in their polynomial branching construction. The remark concerns supported offspring probabilities in that construction; it is not by itself a theorem for every history-dependent clock in the present coding tree. The whole-tree cancellation argument above supplies that extension under its stated contract.

D8 is therefore an explicit nonconstant, heat-smoothed, same-family extension of the repository's earlier absolute obstruction. Coupling it with the uniform continuation theorem is a useful project result. Neither proposal invariance nor the general idea of a positive comparison equation exploding while the original PDE remains regular should be presented as newly invented.
