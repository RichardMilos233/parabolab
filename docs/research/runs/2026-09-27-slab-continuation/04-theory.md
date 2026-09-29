# Theory checkpoint 1 — terminal-code interfaces and a local moment certificate

Date: 2026-09-27. This file is a developing conventional proof; no numerical evidence or Lean completion is asserted at this checkpoint. Coordinates below are ordered (Id,Dx,F0,F1,F2,F3).

## C1. Finite-product perturbation

Let a finite completed tree have N terminal factors. On the same topology, branch/leaf times, positions, code labels and likelihood weights, write H=A∏b_i and H̃=A∏b̃_i. Assume B_i≥0, ε≥0, |b_i|,|b̃_i|≤B_i and |b_i−b̃_i|≤εB_i. Define W_B=|A|∏B_i. Telescoping one factor at a time gives

|H−H̃| ≤ ε N W_B.

No division by B_i is used, so zero envelopes are allowed. An empty product gives zero difference. A symbolically pruned common zero subtree gives H=H̃=W_B=0. Terminal-dependent changes of proposal/pruning are outside this coupling unless embedded into a common correctly weighted measure.

For r>1, Bernoulli's inequality gives 1+N(r−1)≤r^N, hence N≤r^N/(r−1). Since W_{rB}=r^N W_B,

|H−H̃| ≤ ε W_{rB}/(r−1).

Thus a genuine full-tree certificate E[W_{rB}²]≤M gives ||H−H̃||₂≤ε√M/(r−1), and by Cauchy–Schwarz the same upper bound for the difference of means. This result is conditional on the completed-tree representation and the stated moment certificate; it does not itself prove PDE uniqueness or generic derivative closure.

## C2. Sharper leaf-marked moments

The directly useful constant is Q=E[N²W_B²], giving ||H−H̃||₂≤ε√Q. Inflation establishes finiteness; its coarse constant should not be repeatedly multiplied across arbitrarily small slabs.

For a finite normalized code family, let F₂(M)=λM+G(M)/λ be its envelope-moment polynomial vector field. Set M(z,0)=zB², so M_c(z,h)=E[z^N W_{B,c}²]. For z in a neighborhood of 1 with a finite inflated certificate, differentiation is justified by domination of polynomial leaf marks by an exponential leaf tilt. D=∂_z M|₁ and Q=D+∂²_z M|₁ obey

M′=F₂(M), D′=DF₂(M)D,
Q′=DF₂(M)Q+D²F₂(M)[D,D],
M(0)=D(0)=Q(0)=B².

Equivalently derive these identities for generation-truncated nonnegative trees and pass monotonically to the full limit. A leaf tilt is different from a branch-event tilt used in earlier certificates. Here r multiplies each terminal envelope, never each branch weight.

## C3. Exact closure for this semilinear Allen–Cahn mechanism

For f(v)=v−v³ the normalized terminal observables are (g,g′,f(g),f′(g),f″(g),f‴(g)). The existing mechanism produces only first spatial derivatives. All f-derivatives of order≥4 are identically zero. Each scalar code coefficient factors from the corresponding sample; its square is retained in the second-moment recursion.

For the raw uniform two-label law, with M=(i,d,a,b,c,e),

G(M)=(a, bd, 2ab+d²c/2, 2ac+d²e/2, 2ae, 0).

In particular the F2 term is 2ae, not ae: choosing a zero branch still occurs with probability1/2 in this raw law. Exact zero-subtree pruning after selection does not renormalize it away.

For every C¹ terminal satisfying |g|≤2/5 and |g′|≤1/2, a valid absolute terminal envelope is

B=(2/5,1/2,2/5,1,12/5,6).

Indeed |v−v³|≤|v| for |v|≤2/5, |1−3v²|≤1 there, and the remaining two derivative bounds are immediate. These are global terminal contracts, not checks at finitely many sampled points.

## C4. Explicit inflated local L² certificate

Choose λ=2, h≤2/25, r=21/20, and

V=(1/4,1/2,1/2,3,12,50).

The positive envelope Volterra map is

M(s)=e^{λs}r²B² + (1/λ)∫₀ˢ e^{λτ}G(M(s−τ))dτ.

For 0≤s≤h, e^{2s}≤1/(1−2s)≤25/21, and the integrated coefficient is at most (25/21−1)/4=1/21. Since (25/21)r²=21/16, it suffices to check

(21/16)B²+G(V)/21≤V.

The six left-hand coordinates are respectively

(21/100+1/42,
21/64+1/14,
21/100+3/14,
21/16+73/84,
189/25+50/21,
189/4),

each strictly below its coordinate of V. Starting the monotone generation-truncated recursion from zero therefore keeps it in the constant box V. Monotone convergence identifies the finite full-tree envelope moment. The actual terminated tree is almost surely finite: the number of offspring is at most three and clocks have the fixed finite rate2. Its total-node expectation is dominated by (3exp(4h)−1)/2, which is finite. Consequently E[H_Id²]≤1/4, with the stronger inflated certificate available for interface perturbation.

For the smooth periodic interfaces used below, the mean is the Allen–Cahn solution. Indeed the six normalized expectation fields satisfy the bounded mild system with diffusion1/2 and signed reaction

Q(i,d,a,b,c,e)=(a,bd,ab−d²c/2,ac−d²e/2,ae,0).

The uniform six-root L² certificate makes every first-branch child product absolutely integrable, justifying conditioning and Fubini. The actual fields (u,u_x,f(u),f′(u),f″(u),f‴(u)) satisfy exactly this system by the chain rule. They are bounded on a finite slab for smooth bounded periodic input: |u|≤1, |u_x|≤e^h||g′||∞, and the remaining polynomial fields are bounded. Polynomial reactions are locally Lipschitz on the union of the two bounded ranges. Heat-semigroup contraction and the repeated-integral form of Gronwall give uniqueness among bounded mild six-vector solutions. Thus both fields agree. This argument avoids an unjustified interchange of generation stopping with unknown exact boundary data. It is conventionally proved and independently checked, not currently encoded as a stochastic Lean theorem.

The original local algorithm is retained, including its raw two-label probabilities. A later implementation may short-circuit a selected tuple known identically zero without renormalizing the remaining label; it must record that exact distribution-preserving cost optimization.

## C5. A computable smooth interface that stays admissible

Use the periodic nonconstant stationary solution

m=1/20, A=√(2/21), κ=√(40/21), K=K(√m),
L=4K/κ, ω=2π/L, g(x)=A sn(κx,√m).

Here K and sn use the modulus convention; scipy.special uses parameter m. The Jacobi differential identity implies g″/2+g−g³=0. Therefore u(s,x)=g(x). This benchmark is nonconstant but stationary; it does not test a moving interface. Its amplitude and derivative obey |g|≤√(2/21)<2/5 and |g′|≤√80/21<1/2.

Let e_n(x)=√2 sin(nωx), with norm ||v||₂²=L⁻¹∫₀ᴸv². Retain n=1,3,5 and coefficients in the box

|c₁|≤23/100, |c₃|≤3/1000, |c₅|≤1/20000.

Every such sine polynomial has global value bound √2(4661/20000)<2/5 and derivative bound √(80/21)(957/4000)<1/2. Thus all learned interfaces satisfy C4 deterministically, irrespective of Monte Carlo noise. Coordinatewise clipping is the Euclidean metric projection onto this box; it is an explicit biased step whose error is controlled below. No sample-tree values are clipped or discarded.

The detailed analytic witness in [T02](reviews/T02-constructive-theory.md) proves

π/2≤K≤77π/152, 0<q=exp(−πK′/K)<1/300,
γ=1−ω²/2≤8989/124509<3/40,
Pg lies in the coefficient box, δ²=||(I−P)g||₂²<10⁻¹⁶.

It uses the convergent K expansions and Jacobi sine expansion in [NIST DLMF §19.5](https://dlmf.nist.gov/19.5#E1), [§19.12](https://dlmf.nist.gov/19.12#E1), and [§22.11](https://dlmf.nist.gov/22.11#E1). These inequalities are analytic bounds, not conclusions from a sampled grid. The three-coefficient interface is a low-dimensional reference for the MC producer contract, not an NN/latent-operator implementation in this checkout.

## C6. Conditional sampling and total error

Start with v₀=g, the known terminal input. For each slab j, condition on every previous draw; draw N independent uniform X_i on[0,L), and complete fresh local raw trees H_i for terminal v_{j−1}. Form

Z_{j,n}=N⁻¹Σ_i H_i e_n(X_i), c_j=clip_box(Z_j), v_j=Σ_n c_{j,n}e_n.

Only the first slab evaluates the supplied exact terminal g. All subsequent trees evaluate the stored polynomial and its exact derivative, never the known solution. The same tree supplies the three coefficient observations; correlation between coordinates is allowed. Conditional independence between different roots and between future child evolutions is required.

By C4 and orthonormality, the conditional coefficient-variance trace is at most3/(4N). Let c* be the coefficient vector of Pg. Projection cannot increase squared distance to c* because c* is in the box. Conditional centering before projection removes the cross term. The ideal-real-arithmetic errors R_j=E||v_j−g||₂² satisfy

R_j ≤ exp(2γh_j)R_{j−1}+3/(4N_j)+δ², R₀=0.

The stability factor follows from the energy identity

(1/2)d||u−v||₂²/ds =−||u_x−v_x||₂²/2+||u−v||₂²−∫(u−v)²(u²+uv+v²)/L.

Oddness and half-period sign reversal are preserved by the PDE and the interface. Poincaré therefore gives ||u_x−v_x||₂²≥ω²||u−v||₂². The nonnegative cubic term may be dropped. A general target needs a separately proved admissible projected coefficient vector and tail at every time; neither follows from generic smoothness.

## C7. A finite-budget T=4 witness

Set h=2/25, n=50, N=200000 per slab. Then R₅₀<100(3/(4N)+10⁻¹⁶)<1/2500. The amplification sum is bounded by50 exp(3/5)<100, since exp(3/5)≤(1−1/5)⁻³=125/64<2. Equivalently each squared-error factor is at mostρ=250/247 and50ρ⁵⁰<100, an exact-rational check.

Thus the ensemble RMS in normalized spatial L² is below0.02 atT=4, in the ideal mathematical model. This is not a pointwise/high-probability/floating-error certificate. It is a bounded-compute theoretical witness of10 million local root trees; expected nodes are at most this count times(3exp(8/25)−1)/2, using ternary domination. The actual required budget may be smaller; no optimality is claimed.

The PDE and reaction coefficients are unchanged. This construction is a biased continuation approximation with a proved total-error bound, not an unbiased full-horizon raw tree. Its small stationary/symmetric benchmark is deliberately narrower than the original arbitrary-jet ambition.

## C9. Same-datum obstruction for the unsplit rate-2 raw tree

For exactly the C5 terminal datum, the original full-horizon raw tree at common rate2 and uniform F-label probabilities has E[H_Id(T,x)²]=∞ at every x for T≥3.5. This is an L² obstruction for these specific sampling parameters, not pathwise explosion or a universal impossibility theorem for λ selection.

Here is the proof structure; details and an independent review are in [T02 §9](reviews/T02-constructive-theory.md) and [T01 §§9–10](reviews/T01-interface-theory.md). Let M_k denote the extended nonnegative squared moment for F_k and write Y_k=e^(−2t)M_k. Positive first-branch identities hold by Tonelli, even when moments are infinite. The F₃ coordinate is M₃=36e^(2t). Dropping derivative contributions leaves

Y₀,t ≥ ΔY₀/2 + e^(2t)Y₀Y₁,
Y₁,t ≥ ΔY₁/2 + e^(2t)Y₀Y₂,
Y₂,t ≥ ΔY₂/2 + 36e^(2t)Y₀.

The period satisfies4<L<5. At time1, one wrapped Gaussian summand bounds the periodic heat kernel below by e^(−4)/3>1/192. Two intervals of total length2/5 around the positive/negative extrema have |g|>1/4; hence ∫g²>1/40. Since f(g)²≥(19/21)²g²>(4/5)g², Y₀(1,x)>a=1/9600 uniformly.

Compare positive Picard iterates with a spatially constant subsolution. With s=(e^(2t)−e²)/2 it satisfies A_s=AB, B_s=AC, C_s=36A, initially(A,B,C)=(a,0,0). Put z_s=A,z(0)=0: C=36z, B=18z², A=a+6z³, and z_s=a+6z³. Its explosion time is bounded by

s* = ∫₀^∞ dz/(a+6z³) ≤ 9600/30 + ∫_(1/30)^∞ dz/(6z³) =395.

The corresponding physical time t*≤log(e²+790)/2<3.5. Finally the normalized Id moment has the mild lower bound

Y_Id(3.5,x) ≥ (1/2)∫₁^(t*) A(s(r))dr ≥ (e^(−7)/2) lim_(s→s*) z(s) =∞.

Positivity propagates this obstruction to every later time. Thus the continuation theorem atT=4 goes beyond a proved L² failure of the same-datum unsplit rate-2 estimator. It achieves this by changing the full-horizon algorithm to a biased, controlled interface approximation, not by proving that the unsplit tree has become integrable.

## Formalization boundary at checkpoint 1

Planned Lean targets: finite-product inequality, Bernoulli leaf absorption, coordinatewise rational supersolution checks, scalar projection contraction and finite error recurrence. The stochastic process construction, monotone convergence identification, parabolic regularity and subsequent Fourier approximation analysis remain conventional mathematics unless separately formalized. No additional project axioms may be introduced to call those obligations proved.
