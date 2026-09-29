# R16: use the already computed small graph profile as a deterministic anchor

Date: 2026-09-29. Research contract and proposed proof route, not an accepted
sampler or upper theorem. This is a bounded next step toward an implementable
natural-gap extension. The original T69/T73 exact-H sampler remains frozen.

## Motivation and exact proposed change

T69 obtains every unmarked graph-leaf value by an independent average of
centered fixed-burn-in tree outputs. Its variance guarantee is valid, but
the batch size Kbase=ceil(8/a^2), a=3r, may be enormous when the certified
graph radius r is small. This is a particular upper construction cost,
not a lower bound. Gate A already computes a highly accurate, explicitly
represented small Fourier approximation to that same centered profile.

The proposed alternative uses that paid Fourier profile at unmarked
leaves and controls the deterministic anchoring error separately. It
allows a small, explicitly bounded bias in the long-time estimator;
the comparison class has always allowed biased algorithms. No free
known-function evaluation or changed information oracle is introduced.

Fix the actual graph and fixed burn-in L of a future accepted R14c,
with the same d,kappa,nu,sigma,M,C,R,r. Supply a paid known g with
||g||inf<=3/4 and actual uniform evaluation cost Gg. Let

    w_g=Q S_Lg, b_g=Pi S_Lg,
    p a supplied exactly evaluable mean-zero known profile,
    ||p-w_g||inf<=xi<=r/64,
    ||w_g||inf<=r/64, hence ||p||inf<=r/32.

Every p evaluation has actual charged cost Gp. A finite Fourier array
is a possible representation; its evaluation is not declared free.
The expensive mathematical quantity w_g need not be exactly evaluated
by the algorithm. Its occurrence below defines the proof's reference
functional and error, not an oracle call.

For the fixed pair (g,p), define on nearby q

    H_(g,p)(q)=Pi S_Lq-Theta(p+Q(S_Lq-S_Lg)).        (1)

All derivatives in this contract differentiate q with g,p held fixed.
In particular one must not differentiate the map g -> p(g) or silently
identify these derivatives with those of the original H. Conditioning
on the paid grid transcript fixes g,p before the random correction.

At q=g the graph argument is exactly p, and

    H_(g,p)(g)=b_g-Theta(p).                         (2)

If the original H(q)=Pi S_Lq-Theta(QS_Lq) is defined and the segment
joining both graph arguments stays in its domain, the uniform first
graph derivative bound K1 gives

    |H_(g,p)(q)-H(q)|<=K1 xi.                       (3)

For q on the segment from g to an admissible v, R14c's uniform burn-in
puts ||QS_Lq||<=r/64. The shift p-w_g has norm<=xi, so every shifted
argument has norm<=r/32, safely inside the radius-3r graph domain.
Thus (3) is uniform on that segment. Ordinary finite derivatives of
H_(g,p) have uniform bounds there, independent of T,xi and the
representation size of p. These facts still require full proof review.

## Target sampler statement

For every fixed integer j>=1 and continuous residual e=v-g with
||e||inf<=delta, construct an actual Borel sample Z_j satisfying

    E Z_j=D^j H_(g,p)(g)[e,...,e],
    E |Z_j|^2<=V_j delta^(2j),
    unknown initial-value acquisitions<=j on every seed,
    E Work(Z_j)<=C_j(1+Gg+Gp).                     (4)

Constants may depend on all fixed graph/PDE parameters and j, but not
on T,delta,xi,g,p within the displayed envelopes or on distance to the
stable interface. Work counts the actual tree, each p/g lookup, every
marked burn-in tree, primitive operation and coefficient traversal.
All tree/tuple preparation must precede the at-most-j additional
unknown calls, so null nonterminating preparations respect the cap.

The research task must prove the following actual correspondences:

- Use an audited kappa-dependent heat primitive such as R14e, with
  the actual source and both Lyapunov--Perron time directions.
- Generate the genuine ternary graph tree with branch probability
  1/6, leaf probability 5/6, source divided by 5/6 and branch coefficient
  divided by 1/6. Conditional children share a state and have independent
  futures. Almost-sure termination and expected node count two need
  actual justification.
- For the unmarked leaf input p(Y), prove the tilted moment using
  ||p||<=r/32<a=3r and z0=5/4. The familiar scalar recurrence may be
  used only after deriving it from this actual tree law.
- At a leaf carrying b derivative labels, use the actual centered
  order-b derivative of the fixed-time flow S_L at g, with original-time
  residual leaves. Its population/second-moment bounds are independent
  of the diffusivity, but the Gaussian variance kappa times edge length
  and actual PDE representation must be checked explicitly.
- Use all label maps from {1,...,j} to the outer leaves, including
  repeated outer labels. The nonlinear inner flow requires partitions
  with several labels at a leaf; using only outer injections is wrong.
  A uniform map, multiplied by N^j, is one proposed implementation.
- Prove differentiation/infinite-tree interchange, equality to the
  actual derivatives in (4), and finite variation where needed.
  No generic multilinear-product-measure identification is allowed.

Compared with T69, the proposed construction has no unmarked centered
burn-in batch. The expected p evaluation count is bounded by the outer
leaf count. This removes that particular Kbase factor while retaining
the actual Gp cost; it does not yet demonstrate a numerical speedup.

## Conditional upper-error composition to be verified

Suppose a paid deterministic base calculation returns h0 with

    |h0-(b_g-Theta(p))|<=eta0.

Let J=ceil(1+d/(2s)), m=J-1, Mgrid=k^d, delta<=Cint k^(-s).
Average Mgrid independent copies of (4) at each order j=1,...,m and
add their 1/j! corrections to h0. A complete proof should yield

    RMS(Hhat-H(v))
      <=eta0+K1 xi
        +sum_(j=1)^m sqrt(V_j)delta^j/(j!sqrt(Mgrid))
        +B_J delta^J/J!.                            (5)

Here the Taylor remainder belongs to H_(g,p), not H; all its derivative
bounds must be uniform in the admissible anchor. The two deterministic
errors eta0 and K1 xi must be scaled by exp(T-L) in the final output
budget. For example impose eta0<=exp(-(T-L))/384 and
xi<=min(r/64,exp(-(T-L))/(384 max(1,K1))). The remaining terms have
the same k^(-s-d/2) order as the old composition.

The actual query cap remains [1+J(J-1)/2]k^d after the paid grid,
if (4) is proved. If Gp is polynomial in T and the paid base solve has
cost k^d times a polynomial in T, (5) is compatible with the same
exponential ideal-work rate. Those evaluator/cost premises require
separate proof for the changed diffusivity; (5) alone does not supply
them or accept a new full-scope complexity theorem.

## Handoff and evidence limits

This contract fixes the intended object before implementation. First
complete the conventional sampler proof or find a precise obstruction,
then obtain independent correspondence review. Only a fixed accepted
statement should be sent to Lean or numerical implementation. Preserve
R14e and all existing theory/data. Do not replace T69's exact target
with (1) without explicitly recording the controlled error (3).

No new theorem, experiment, numerical data call, practical advantage,
finite-bit guarantee, novelty or award-level conclusion is asserted.
