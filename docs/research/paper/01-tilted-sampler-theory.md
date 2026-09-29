# Supersolution-tilted coding trees: bounded output, horizon-free work

Status: new conventional theory written 2026-09-29 for the paper (plan G1/G2).
Not yet independently reviewed. Everything below is in the exact-real
sampling model; floating-point issues of the implementation are treated in
`02-implementation-notes.md`.

## 1. Canonical tree measure (fixed expansion)

Let X be R^d or the flat torus, p_t(y,z) the heat kernel of L=Δ/2, and
P_t its semigroup. A *mechanism* is a countable code set C, measurable
terminal functions g_c : X → R, and for each c a finite list
M(c) = {(κ_j, (c_{j,1},…,c_{j,m_j}))} with κ_j ∈ R∖{0}.

For the semilinear PDE ∂_t u = Lu + f(u), u(0)=v (t = remaining time,
the project's terminal-value problem after time reversal), the mechanism is

    Id  -> (F_0)                      κ = 1
    F_k -> (F_0, F_{k+1})             κ = 1
    F_k -> (D_i, D_i, F_{k+2})        κ = -1/2,   i = 1..d
    D_i -> (F_1, D_i)                 κ = 1
    g_Id = v,  g_{F_k} = f^{(k)}(v),  g_{D_i} = ∂_i v.

(This is `SemilinearMechanism` with the coefficient a of FDeriv(a,k) moved
from the child code into κ; the two bookkeepings give the same a(θ).)

A completed tree rooted at (c,t,y) is either a *leaf* with terminal position
z, or a *branch* with elapsed lifetime σ∈(0,t), branch position z, a tuple
index j, and one completed child tree rooted at (c_{j,i}, t−σ, z) for each i.
All children share z (JCP Alg. 1 gotcha 1). The canonical measure is

    μ_{c,t,y} = δ_leaf ⊗ p_t(y,z)dz
              + Σ_j  dσ 1_{(0,t)}(σ) ⊗ p_σ(y,z)dz ⊗ ⊗_i μ_{c_{j,i}, t−σ, z},

defined recursively on finite trees (finite depth by induction). The signed
weight a(θ) is the product of g at every leaf and κ at every branch. Set

    W_c(t,y) = ∫ |a| dμ_{c,t,y} ∈ [0,∞],
    W^ϑ_c(t,y) = ∫ ϑ^{N(θ)} |a| dμ_{c,t,y},   ϑ ≥ 1,

where N(θ) counts all nodes (leaves and branches). By Tonelli,

    W^ϑ_c(t,y) = ϑ [ P_t|g_c|(y)
                 + Σ_j |κ_j| ∫_0^t P_σ[ Π_i W^ϑ_{c_{j,i}}(t−σ,·) ](y) dσ ],   (1.1)

and W^ϑ is the minimal [0,∞]-valued solution of (1.1): truncating at depth n
gives an increasing sequence converging to W^ϑ, and each truncation is below
any nonnegative solution by induction on n. W = W^1.

When W_Id(T,x) < ∞, the signed value U_Id(T,x) := ∫ a dμ_{Id,T,x} is well
defined. That it equals the PDE solution u(T,x) is the *correspondence*
question, separate from everything below (see 04c/04d and the reviewed
proofs listed in the plan). All statements below concern the random
functional; "unbiased" means E H = U_Id(T,x).

## 2. Proposals and the invariance of the first absolute moment (Thm A)

A *proposal with cemetery* Q_{T,x} is a probability law on (finite trees)
∪ {†}, where † means "stopped with output 0". A tree-valued outcome θ gets
H(θ) = a(θ) dμ/dQ(θ). Q is *supported* if dQ/dμ > 0 μ-a.e. on {a≠0}.

**Theorem A.** For every supported Q, E_Q|H| = W_Id(T,x).

*Proof.* E_Q|H| = ∫_{a≠0} |a| (dμ/dQ) dQ = ∫_{a≠0}|a| dμ = W_Id(T,x). ∎

This holds for adaptive clocks and tuple laws, since only the joint density
dQ/dμ on complete trees enters. The joint-likelihood contract (04c) is
exactly the statement that the implementation's H equals a·dμ/dQ. Hence
E_Q H² ≥ (E_Q|H|)² = W_Id(T,x)² for every supported Q, and every sampler of
this expansion has infinite first absolute moment when W_Id(T,x) = ∞.

## 3. The tilted sampler (Thm B)

**Definition (ϑ-supersolution with leaf envelope).** Fix ϑ ≥ 1, measurable
envelopes h_c ≥ |g_c|, and write L_c(t,y) = P_t h_c(y). A measurable
Ŵ : C × (0,T] × X → [0,∞] is a ϑ-supersolution if for all (c,t,y)

    Ŵ_c(t,y) ≥ ϑ [ L_c(t,y) + Σ_j |κ_j| B_{c,j}(t,y) ],
    B_{c,j}(t,y) = ∫_0^t ∫ p_σ(y,z) Π_i Ŵ_{c_{j,i}}(t−σ,z) dz dσ,          (3.1)

with 0·∞ = 0 in products. W^ϑ with h = |g| is the minimal such function.

**Algorithm S(c,t,y)** (returns a value in [−1,1], or aborts with 0):

1. With probability L_c/Ŵ_c: *leaf*. Draw z with density
   p_t(y,z)h_c(z)/L_c; return g_c(z)/h_c(z).
2. With probability |κ_j| B_{c,j}/Ŵ_c: *branch j*. Draw (σ,z) with density
   p_σ(y,z) Π_i Ŵ_{c_{j,i}}(t−σ,z)/B_{c,j}; evaluate the children
   S(c_{j,i},t−σ,z) in order; return sign(κ_j) Π_i S(c_{j,i},t−σ,z).
3. Otherwise (probability ≥ 1−1/ϑ): *kill*; abort the whole run, output 0.

Estimator: H = Ŵ_Id(T,x) · S(Id,T,x), with H = 0 if Ŵ_Id(T,x) = 0.

**Theorem B.** Let Ŵ be a ϑ-supersolution with Ŵ_Id(T,x) < ∞.

(a) *Well-posedness.* Almost surely every visited node has 0 < Ŵ < ∞.

(b) *Bounded output.* |H| ≤ Ŵ_Id(T,x) almost surely.

(c) *Termination and work.* If ϑ > 1, the number N_gen of generated nodes
    satisfies P(N_gen > n) ≤ ϑ^{-n}; in particular E N_gen ≤ ϑ/(ϑ−1),
    uniformly in T, x, the PDE and the data.

(d) *Unbiasedness.* If the run terminates a.s. (always when ϑ>1; when ϑ=1
    and Ŵ = W, see (f)), then W_Id(T,x) < ∞ and E H = U_Id(T,x).

(e) *Second moment.* E H² ≤ Ŵ_Id(T,x) · W^{(h)}_Id(T,x) ≤ Ŵ_Id(T,x)², where
    W^{(h)} is the absolute mass with h in place of |g|. With h = |g|,
    E H² = Ŵ_Id W_Id and, by Theorem A, E H² ≤ (Ŵ_Id/W_Id) · inf_Q E_Q H².

(f) *Exact tilt.* If W_Id(T,x) < ∞ and Ŵ = W, h = |g|, ϑ = 1, then no kill
    occurs, the tree is a.s. finite, and |H| = W_Id(T,x) a.s.

*Proof.* (a) At a visited node with Ŵ_c ∈ (0,∞), step 2's density has total
mass B_{c,j} ≤ Ŵ_c/ϑ < ∞, so the set of (σ,z) where some child has Ŵ = ∞
and the product is positive is null; where the product is 0 the density
vanishes. Hence chosen children have 0 < Ŵ < ∞; the root is covered by
assumption (Ŵ_Id = 0 is excluded separately).

(b) By induction over the finite tree, S ∈ [−1,1], since |g_c/h_c| ≤ 1 and
products of numbers in [−1,1] stay in [−1,1].

(c) Nodes are generated one at a time (depth first). Conditional on
everything generated before, the current node is killed with probability
1 − (L_c + Σ|κ_j|B_{c,j})/Ŵ_c ≥ 1 − 1/ϑ by (3.1). Hence the generation of
the (n+1)-st node requires n non-kills, each with conditional probability
at most 1/ϑ, giving P(N_gen > n) ≤ ϑ^{-n}.

(d) Consider a completed tree θ with no kill. Its Q-density w.r.t. μ is the
product of the step probabilities times the conditional densities:
a leaf contributes p_t h_c/Ŵ_c, a branch contributes
|κ_j| p_σ Π_i Ŵ_{c_{j,i}}/Ŵ_c. Every non-root Ŵ appears once as a numerator
(in its parent) and once as a denominator (at itself), so

    dQ/dμ(θ) = |a_h(θ)| / Ŵ_Id(T,x),   a_h := Π_branches κ · Π_leaves h,

which is positive wherever a(θ) ≠ 0, i.e. Q is supported. On θ,
H = Ŵ_Id Π sign(κ) Π g/h = a(θ) dμ/dQ(θ). Since termination is a.s., the
outcomes are completed trees or †, and
E H = ∫_{finite trees} a dμ, absolutely convergent because
∫|a|dμ ≤ ∫|a_h|dμ = Ŵ_Id · Q(completed without kill) ≤ Ŵ_Id < ∞.

(e) E H² = ∫ Ŵ_Id² (Π g/h)² dQ ≤ Ŵ_Id² Q(no kill) = Ŵ_Id ∫|a_h|dμ.
With h = |g| the inequality is an equality, and inf_Q E_Q H² ≥ W_Id².

(f) With Ŵ = W the kill probability is 0 by (1.1) with equality, and the
mass of completed trees is ∫|a|dμ/W_Id = 1, so infinite runs have
probability 0. |S| = 1 on completed trees. ∎

**Corollary B1 (sampler-independent horizon).** For fixed (T,x) the
following are equivalent: (i) some supported proposal has E|H| < ∞;
(ii) every supported proposal has E|H| < ∞; (iii) W_Id(T,x) < ∞;
(iv) some supported, a.s.-terminating proposal has |H| = W_Id(T,x) a.s.
Consequently, the supremum over proposals of the horizon of finite
variance equals the horizon of absolute integrability, and it is attained
with bounded output.

**Corollary B2 (horizon-free work).** If W^ϑ_Id(T,x) < ∞ for some ϑ > 1,
tilting by W^ϑ gives an unbiased estimator with |H| ≤ W^ϑ_Id(T,x),
E H² = W^ϑ_Id W_Id and E N_gen ≤ ϑ/(ϑ−1).

## 4. Constant data: everything explicit

For v ≡ r, derivative codes have zero weight (every D-tree has a D leaf,
g_D = 0), and with a_k = |f^{(k)}(r)|, Φ(z) = Σ a_k z^k/k!,
Z' = Φ(Z), Z(0) = 0, τ = ∫_0^R dz/Φ (04d):

    W_{F_k}(t) = Φ^{(k)}(Z(t)),   W_Id(t) = |r| + Z(t).

Putting V_k = ϑΨ_k(ϑ²t) in (1.1) shows Ψ solves the ϑ = 1 system, so

    W^ϑ_{F_k}(t) = ϑ Φ^{(k)}(Z(ϑ² t)),   W^ϑ_Id(t) = ϑ|r| + Z(ϑ² t).

Hence W^ϑ_Id(T) < ∞ iff T < τ/ϑ². **For every T < τ and every
1 < ϑ < (τ/T)^{1/2}**, Corollary B2 gives an unbiased estimator with
|H| ≤ ϑ|r| + Z(ϑ²T) and E N_gen ≤ ϑ/(ϑ−1). Flat Allen–Cahn (f = u−u³,
r = 1/2): τ = (3π−2log3)/5 ≈ 1.44551, whereas every constant-rate,
fixed-first-label-probability sampler has infinite variance for
T ≥ sup_{λ,p} T*(λ,p) < 1 (tuple-policy C8; λ-optimum 0.70389 at p=1/2,
0.97025 at p=0.95, 0.99545 as p→1; recomputed 2026-09-29 with mpmath).

## 5. Spatially constant supersolutions for nonconstant data

Take constant envelopes h_c ≡ ℓ_c := sup_X |g_c|. If a function
Ŵ_c(t), independent of y, satisfies the ODE-integral system

    Ŵ_c(t) = ϑ [ ℓ_c + Σ_j |κ_j| ∫_0^t Π_i Ŵ_{c_{j,i}}(s) ds ],             (5.1)

then it satisfies (3.1) with equality, because ∫ p_σ(y,z)dz = 1. The branch
density in step 2 factorizes: j and the children's remaining time s = t−σ
are drawn from |κ_j| Π_i Ŵ_{c_{j,i}}(s) on (0,t), and z = y + √σ ξ with a
standard Gaussian ξ. The leaf position is z = y + √t ξ with factor
g_c(z)/ℓ_c. For polynomial f of degree m, only F_0..F_m, Id and D_i carry
nonzero minimal Ŵ, so (5.1) is a finite ODE system.

The resulting guaranteed horizon τ_sup(ϑ) is the blow-up time of (5.1); it
is the same kind of object as the sufficient conditions of Huang–Privault
(2025/26), but here it comes with an estimator whose output is bounded and
whose expected work is at most ϑ/(ϑ−1). Bounded output also gives
non-asymptotic confidence intervals (Hoeffding: half-width
Ŵ_Id √(2 log(2/α)/n)), which heavy-tailed fixed-rate samplers cannot
provide (compare the JCP Table 5 bias, gotcha 20).

## 5b. Work: sampler-independent node-weighted mass (added 2026-09-29)

For any ψ ≥ 0 on trees, E_Q[ψ|H|] = ∫ψ|a|dμ for every supported Q. With
ψ = N: E_Q[N|H|] = W_N := ∫N|a|dμ = right derivative of ϑ ↦ W^ϑ_Id at 1
(convex), and W_N ≤ W^ϑ/(ϑ−1). Hence every supported sampler with
|H| ≤ M has E N ≥ W_N/M; the ϑ-tilt has M·E N ≤ W^ϑ ϑ/(ϑ−1).

Constant data: W_N(T) = |r| + 2TΦ(Z(T)). For Φ polynomial of degree p ≥ 2,
Z^{p−1} ~ p!/(a_p(p−1)(τ−t)), Φ(Z)/Z ~ 1/((p−1)(τ−t)), so
(i) any sampler with |H| ≤ C W has E N ≥ (1+o(1)) 2τ/(C(p−1)(τ−T));
(ii) the tilt with ϑ² = (τ+T)/(2T) has |H| ≤ (2^{1/(p−1)}+o(1))W and
E N ≤ (4τ+o(1))/(τ−T). Bounded-output work is Θ((τ−T)^{−1}).
Verified numerically (03-numerical-results §2b).

Fixed-rate fraction for two-term Φ = a_0 + a_p z^p/p!:
sup T_2/τ = K (p!)^{−1/(2p)} I_p^{−1/2}, I_p = (π/p)/sin(π/p),
K = max log(1+z)/√z = 0.804742; = 0.540 (p=2), 0.543 (3), 0.513 (4),
0.454 (6), 0.375 (10), ~ K√(e/p) → 0.

## 6. Scope and literature

**Checked 2026-09-29 (full text).** Henry-Labordère–Touzi, *Branching
diffusion representation for nonlinear Cauchy problems* (AAP 31(5), 2021;
arXiv:1801.08794), proof of Thm 3.2: they bound |ξ| by a sup-coefficient
product χ_t and control E χ_t by the ODE ∂_t w = ‖γ‖∞ H_1(w), w(0) = r_1
— the same sup-majorant ODE as (5.1), without derivative codes. It is used
only as an *analysis* device for a sufficient L1 condition; branching
probabilities q_j and the lifetime law are free inputs, not derived from w,
and no necessary condition or bounded estimator appears. Warin,
*Variations on branching methods* (arXiv:1701.07660): nested/derivation
schemes for longer maturities, no majorant-based proposal (keyword scan).
Huang–Privault 2025/26: sufficient conditions via binary-tree domination.
So the sup-majorant horizon itself is known as a sufficient condition; the
new element is using the (ϑ-)majorant to *define* the proposal, which yields
bounded output and the ϑ/(ϑ−1) work bound, plus the exact equivalence B1.

**Checked 2026-09-29 (full text, Russian original from mathnet.ru).**
Medvedev–Mikhailov, ZhVMMF 49(3) 441–452 (2009) = CMMP 49 428–438, §6:
φ = Kφ^n + h, nonnegative k, h, collision estimator ξ_x = h(x) +
q(x,x') Π ξ_{x'}^{(i)} (every node contributes h and keeps branching).
"Value modelling" p* = kφ^n/(φ − h) lives on an infinite tree; their
Theorem 4 gives zero variance only under 1 − h/φ ≤ 1 − ε < 1/n. The intro
says the ideal zero-variance version for power nonlinearity was absent
from the literature before them. Termination/work is discussed only via
n‖K‖ < 1 (bounded mean number of branches). Our tilt is the *absorption*
form (leaf vs branch chosen by mass), for which Theorem B(f) gives finite
trees and |H| = W unconditionally. Principle attributed to them; the
unconditional absorption-form statement, slack work bound and PDE results
are the claimed additions. Mikhailov's 1987/1992 book not yet checked.

Zero-variance importance sampling (Kahn–Marshall 1953), Russian roulette
and importance maps in branching transport (Booth), Doob h-transforms of
branching processes, and Boltzmann samplers for Y' = Φ(Y) trees
(Bergeron–Flajolet–Salvy 1992; Duchon et al. 2004) are classical.
Theorem A's cancellation is noted in HLTT (2014, Rem. 2.14). The claimed
contribution is the combination for derivative-coded PDE trees:
(i) the exact equivalence of Corollary B1, which turns the "short time"
restriction into a statement about one positive PDE system; (ii) the
horizon-free work bound of Theorem B(c) via ϑ-supersolutions; (iii) the
explicit constant-data and sup-majorant instances. A targeted literature
search for (i)–(ii) is still required before any novelty claim.

Not covered: exact computation of W for nonconstant data (as hard as a
positive PDE system); correspondence U = u (reviewed separately for the
examples used); floating-point soundness of an implementation.
