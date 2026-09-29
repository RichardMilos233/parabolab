# T10 — polynomial obstruction and finite-derivative extension

Date: 28 September 2026. Independent conventional audit of the parent's proposed general obstruction. Only this file is owned by T10. No implementation, experiment, numerical calculation, or Lean work was performed. I read the original semilinear mechanism, the repository's one- and multidimensional mechanism definitions, the preceding D8 proof, and the primary sources listed below. The inherited research role is retained; serving-model telemetry is unavailable.

## Verdict

**The polynomial theorem is valid, and the stronger smooth finite-derivative criterion is valid under the exact single-tree proposal contract.** A finite positive chain suffices; neither polynomial closure nor uniqueness of an infinite moment system is necessary. The proposed analytic corollary follows, with constant reaction roots as the only exceptional smooth terminal profiles on a connected torus.

The material qualifications are: preserve the actual raw code mechanism; require genuine support and exact joint likelihood weights; assume almost-sure completion; use compact heat positivity; and make a statement about the absolute integrability of the sampled functional, independently of global PDE existence or representation validity. Non-affine C∞ reactions alone do **not** imply the analytic corollary. An explicit counterexample appears below.

This is substantially broader than the Jacobi example. Nevertheless, positive comparison equations and proposal-independent absolute mass have close precedents. The exact new theorem's publication priority has not been established by this bounded search.

## 1. Actual mechanism and dimension check

Use forward elapsed time and Brownian generator `L=(1/2)Δ` on a fixed connected flat torus `X=R^d/Λ`, with d finite. Let v be a real smooth periodic terminal function, and f be C∞ on an open interval containing its compact range. The functional can be defined from these terminal codes without assuming a PDE solution at the requested horizon.

The reachable normalized code labels are `I`, `D_i` for `1≤i≤d`, and `F_k` for `k≥0`, with terminal values

`v`, `∂_i v`, and `f^(k)(v)`.

The raw tuples are

`I → (F_0)`,

`D_i → (F_1,D_i)`,

`F_k → (F_0,F_(k+1))`, or `(D_i,D_i,−(1/2)F_(k+2))`, one for each i.

The scalar multiplier belongs to the code/product. There is one reaction tuple and d gradient tuples before zero reduction. Thus the one-dimensional two-label sampling law is not the multidimensional uniform law. The absolute canonical equations below do not depend on that choice of probabilities, provided each nonzero contribution is supported and correctly weighted.

These rules reproduce the original one-dimensional equation (2.7), and direct differentiation in d dimensions gives

`(∂_t−L)f^(k)(u) = f(u)f^(k+1)(u) − (1/2) f^(k+2)(u) Σ_i(∂_i u)²`.

There are no cross-coordinate derivatives in the Laplacian chain rule and no higher spatial derivative labels reachable from this semilinear mechanism. Repository inspection of `SemilinearMechanism` and the `m=1`, zero-order argument specialization of `FullyNonlinearMechanismND` agrees. The latter can remove identically zero tuples and renormalize their proposal probabilities; this changes variance but not the nonzero canonical absolute expansion.

Keep code labels and their specified tuples, even if two code functions happen to agree algebraically. Replacing a function-code subtree by another representation of that function is not automatically a mere probability change.

## 2. Proposal contract and positive mild system

Allow clock and tuple laws to depend on code, state, time, depth, and revealed history. Require exact reciprocal factors for their actual conditional densities/probabilities and leaf survival masses, positive almost everywhere on all nonzero canonical completed-tree contributions. Require the resulting weighted output to be well-defined and its tree to complete almost surely at every finite horizon. Topological support alone is insufficient.

On each finite completed topology, multiplying its absolute weight by its **full joint sampling likelihood** cancels those factors. Afterwards the canonical Brownian child kernels factorize. This order matters for history-dependent proposals: independence of the children under the proposal itself is not assumed. Restricting the full functional to completed trees of bounded depth and then using monotone convergence identifies its extended absolute expectation with the canonical positive tree sum. The reasoning is the earlier D8/25 September L1 cancellation argument with spatial terminal factors retained.

Consequently write `W_I,W_Di,W_k` for the minimal nonnegative tree sums. With `P_t` the torus heat semigroup, they obey the extended mild identities corresponding formally to

`∂_t W_I = L W_I + W_0`,

`∂_t W_Di = L W_Di + W_1 W_Di`,

`∂_t W_k = L W_k + W_0 W_(k+1) + (1/2) Σ_i W_Di² W_(k+2)`.

Initial fields are absolute values of the terminal codes. Higher identically zero codes contribute zero. Products involving a zero code mean the zero contribution of that branch, including when another descendant moment is infinite. These displays abbreviate nonnegative integrals obtained by finite tree expansion and Tonelli. They are not classical differentiations of potentially infinite fields.

No PDE solution, uniqueness of the whole infinite hierarchy, or signed expectation is used in the obstruction. For a nonpolynomial f, every fixed finite depth reaches only finitely many derivative orders. Bounded offspring arity and the proposal's completion assumption suffice for passage to the full functional; a uniform bound over all derivatives is unnecessary for the lower-bound argument.

## 3. General finite-derivative obstruction

Suppose there is an integer `p≥2` such that neither `f(v)` nor `f^(p)(v)` is identically zero. For any fixed `t0>0`, set

`η_0 = min_x P_t0 |f(v)|(x)`,

`η_p = min_x P_t0 |f^(p)(v)|(x)`.

Both numbers are strictly positive. Indeed each initial function is continuous, nonnegative and nonzero; the torus heat kernel is positive, and the resulting positive continuous heat field attains a positive minimum on compact X. This is the only spatial positivity input. In particular, pointwise zeros in the terminal fields cause no problem.

The terminal part of the mild identity and `P_s1=1` give, for all `s≥0`,

`W_p(t0+s,x) ≥ P_s P_t0 |f^(p)(v)|(x) ≥ η_p`.

There is no need for `F_p` to be constant as a code. Restart the nonnegative mild inequalities at t0, discard every gradient contribution and all initial lower bounds except η0, and freeze the last comparison field at ηp. This yields the finite comparison chain

`A_k' = A_0 A_(k+1)`, `0≤k<p`, `A_p=η_p`,

`A_0(0)=η_0`, `A_k(0)=0` for `1≤k<p`.

To justify comparison even if actual moments are infinite, compare each nonnegative Picard iterate of this finite constant system with the restarted mild inequalities. Positivity preserves the inequality at every iteration. The finite ODE solution is its monotone limit up to its explosion time. Thus `W_0(t0+s,x)≥A_0(s)` there, uniformly in x. This avoids an assumed classical solution or uniqueness theorem for the infinite hierarchy.

Set `Z'=A_0`, `Z(0)=0`. Since `A_0≥η_0>0`, integration using Z as the variable gives

`A_k = η_p Z^(p−k)/(p−k)!`, `1≤k≤p`,

`A_0 = η_0 + (η_p/p!) Z^p`.

Put `b=η_p/p!` and `R=(η_0/b)^(1/p)`. Its explosion time is

`τ_* = ∫₀^∞ dz/(η_0+bz^p)`

`≤ R/η_0 + R^(1−p)/[b(p−1)]`

`= [p/(p−1)] η_0^(−(p−1)/p) (p!/η_p)^(1/p) =: B_p`.

This elementary estimate splits the integral at R and is sufficient; no special-function integral is required.

For every `T≥t0+B_p` and every starting point x, the Id mild integral gives, for `s<τ_*`,

`W_I(T,x) ≥ ∫₀^s A_0(r) dr = Z(s)`.

Here the heat semigroup preserves the spatially constant comparison, and the integrated physical times are `t0+r<T`. Letting `s↑τ_*` proves

**`E|H_I(T,x)|=∞` for every x and `T≥t0+B_p`, for every supported completing proposal in the stated class.**

Second moments are then infinite as well. This conclusion concerns the Id root, not merely a descendant. It gives an upper bound on onset, not an exact critical horizon or any assertion about smaller horizons.

## 4. Polynomial specialization and linear exceptions

For a real polynomial of degree `p≥2` with leading coefficient `c_p≠0`, `f^(p)=p!c_p`. Hence `η_p=p!|c_p|`. Whenever `f(v)` is not identically zero, the preceding sufficient threshold becomes

`t0 + [p/(p−1)] η_0^(−(p−1)/p) |c_p|^(−1/p)`.

The finite nonzero normalized closure has `p+d+2` code types: I, d gradient codes, and p+1 function codes. All code scalings remain accounted for. The polynomial proof proposed by the parent is therefore a direct special case of Section 3.

If `f(v)≡0`, connectedness and continuity force v to be a constant polynomial root r: a nonzero polynomial has a finite real root set, and the continuous image of a connected space is connected. Every finite F0 tree then has either an F0 leaf with value zero or a gradient descendant with a zero leaf. Thus all branching Id contributions vanish, and its absolute expectation is exactly `|r|` for every finite horizon. This exception does not guarantee finite second moments for arbitrary importance laws.

For an affine reaction `f(y)=a+by`, including constants and zero, the higher function codes vanish. The absolute equations give

`W_0(t)=e^(|b|t) P_t |f(v)|`,

`W_I(t)=P_t|v| + L_b(t) P_t|f(v)|`,

where `L_b(t)=(e^(|b|t)−1)/|b|` if `b≠0`, and `L_0(t)=t`. These are finite for bounded periodic v and every finite t. This verifies that the degree restriction is substantive.

## 5. Analytic corollary, and why C∞ is insufficient

Let f be real analytic and non-affine on a connected open interval J containing the range of v.

If v is nonconstant, its image contains a nondegenerate interval. Neither f nor f'' can vanish throughout that interval: the analytic identity theorem would make f respectively zero or affine on J. Therefore the criterion holds with `p=2`.

If `v≡r` and `f(r)≠0`, some derivative `f^(p)(r)` with finite `p≥2` must be nonzero. Otherwise the Taylor series makes f affine near r, and analytic continuation makes it affine on J. Thus Section 3 applies again. If `f(r)=0`, the constant-root exception applies.

Accordingly, for a non-affine analytic reaction on J, **every smooth periodic terminal other than a constant reaction root has infinite absolute moment by a finite deterministic horizon**, uniformly over supported completing clock/tuple proposals. This does not require, or prove, global existence of the underlying PDE.

Combining this with the affine calculation gives a complete all-horizon classification for a real analytic f on connected J: `E|H_I(T,x)|<∞` for every finite T and every x **if and only if f is affine on J, or v is a constant reaction root**. Each supported completing proposal has the same canonical absolute expectation. In all remaining cases, Section 3 gives a finite threshold at and beyond which the absolute moment is infinite for every x. This classification does not promise a positive initial interval of integrability in the non-affine case; establishing local integrability for an infinite derivative family is a separate question.

Analyticity cannot simply be replaced by global non-affinity and C∞ smoothness. Define

`f(y)=1+exp(−1/y²)` for `y≠0`, `f(0)=1`, and `v≡0`.

This is smooth and non-affine, but `f(0)=1` and every derivative of positive order vanishes at zero. Every finite higher-code tree is zero, so `W_0=1` and `W_I(T)=T<∞` at all finite horizons. This is an estimator statement. It does not provide a PDE representation: the true constant-data solution obeys `u'=f(u)` and satisfies `u(t)>t` for t>0. The original representation theorem separately assumes uniqueness/correspondence of the infinite code system; this example does not contradict that conditional theorem.

## 6. A checked nonpolynomial illustration

For `f(y)=sin y`, `v≡π/2`, gradients vanish in every completed derivative-code tree. Canonically, all even function-code absolute moments equal A and all odd ones equal B, by the derivative cycle of sine and the identical absolute code mechanisms. Their finite minimal system is

`A'=AB`, `B'=A²`, `(A,B)(0)=(1,0)`.

It has `A=sec t`, `B=tan t` before `π/2`; `A²−B²=1` verifies the reduction. The Id absolute moment is

`W_I(t)=π/2+∫₀^t sec s ds`,

finite exactly before `π/2` and infinite at and after that horizon. The root integral gives the divergence directly. In contrast, the true spatially constant signed solution is `u(t)=2 arctan(e^t)`, which exists globally and tends to π. This example illustrates the distinction between expansion integrability and PDE behavior; no novelty is asserted for this elementary reduction.

## 7. Counterexample and scope checklist

- **Compactness matters to this proof.** On `R^d`, heat smoothing of a nonzero localized function may have infimum zero. The spatially constant lower chain is then unavailable; this audit proves no unrestricted Euclidean-space analogue.
- **Connectedness matters.** On disconnected components carrying constant reaction roots, or on a component where the required heat seed is absent, the asserted everywhere-positive minimum can fail. The theorem concerns a connected torus.
- **The terminal higher derivative must be nonzero.** Merely choosing a nonlinear smooth f somewhere outside the terminal range does not meet Section 3.
- **The absolute sum is taken before cancellations between different trees.** Control variates, resummation, different branch combiners and absorbed reaction terms require a new analysis. There is no theorem here that all branching methods fail.
- **Dimension is unrestricted but fixed.** The constants η0 and ηp may depend strongly on d, the torus geometry and the terminal profile. No dimension-independent quantitative bound is proved.
- **The PDE may fail to exist by the threshold.** The obstruction is still a valid statement about the raw terminal-code functional. When the PDE does exist globally, such as the sine example, it remains an estimator-specific failure.

## 8. Primary-source comparison and novelty assessment

Nguwi, Penent and Privault, *A fully nonlinear Feynman–Kac formula with derivatives of arbitrary orders* (2023), [equation (2.7), Definition 4.1 and Theorem 4.2](https://arxiv.org/html/2201.03882), were inspected. Equation (2.7) is the raw mechanism used here. The representation theorem assumes smooth PDE data/solution, integrability and uniqueness of the code system; its sufficient integrability result is for restricted horizons. The general negative theorem above is an independent deduction from its mechanism, not a statement attributed to the paper.

Blömker, Romito and Tribe (2007), [Theorem 4.1 and §4.2](https://www.numdam.org/article/AIHPB_2007__43_2_175_0.pdf), identify positive comparison expectations with the minimal positive mild solution, with equality to absolute expectations under their multiplicativity condition. They exhibit weight-independent integrability failure in covered mode-space examples. This is strong prior art for the method of proof. Henry-Labordère, Tan and Touzi, [Remark 2.14](https://arxiv.org/pdf/1302.4624), explicitly separate offspring-proposal-independent integrability from proposal-dependent variance. The repository's 25 September flat-data theorem is also a direct predecessor.

Huang and Privault, *Stability analysis of a branching diffusion solver for semilinear heat equations*, [current manuscript, Definition 2.2 and Theorem 2.8](https://arxiv.org/pdf/2502.17853), was inspected. Their binary recoding retains, at zero spatial multi-index, the coefficient-one tuple `(F0,F_(j+1))`, as well as `Id→F0`. Their results give sufficient finite-horizon integrability and a conditional representation. **Independent structural inference:** the same finite-chain obstruction applies to the periodic version of that raw binary product under the corresponding proposal contract, because its other absolute contributions are nonnegative. Binary arity by itself does not remove the mechanism responsible for this lower bound. This is not a claim made by their paper.

The bounded search found no primary theorem explicitly stating the full analytic terminal-data dichotomy above for this mechanism on a connected torus. That search does not establish publication priority. The defensible candidate contribution is the finite-derivative obstruction criterion and its analytic corollary with an explicit bound. Its proof uses established positive comparison and importance-sampling cancellation principles. It warrants a focused additional novelty check before any publication-level claim, rather than a prestige claim based on its breadth alone.
