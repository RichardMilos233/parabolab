# T73: independent audit of the stable-graph derivative sampler

Date: 2026-09-29. **Verdict: GO for frozen T69's Gate B theorem in
its explicitly stated continuous-seed, exact-real primitive model.**
No mathematical repair of the frozen sampling law or its estimates is
needed. The actual local proxy, coefficient second moment, original-time
tuple representation, deterministic unknown-query cap, almost-sure
halting, Borel dependence, and expected work all pass the audit below.

This accepts the derivative sampler, with the actual cost of evaluating
the already paid profile retained. It does not accept Gate A, assert a
cheap evaluator for an arbitrary continuous function, or promote R12's
conditional full-work conclusion. Root correspondence and any ledger
promotion remain separate. The sole T73 edit is this audit file.

I read all 891 lines of T69, all 1003 lines of T65, all 191 lines of
R10b, all 519 lines of T68, and all 108 lines of R12. I also read R08
and the current D29/D30 checkpoint. The mathematical checks below start
from T69's actual random coefficients and trees; T69's own GO verdict
is not a premise. No source proof, accepted ledger, code, numerical
artifact, or Lean file was changed.

## 1. Frozen sources and exact accepted statement

The frozen source hashes verified for this audit are:

| Source | Lines | SHA256 |
|---|---:|---|
| T69-stable-graph-sampler-feasibility.md | 891 | `ff537ca6679fdefeefe9c08990194a09f6a2cec23460e1656876e7fdf8a37d9b` |
| T65-local-stable-graph-upper-proof.md | 1003 | `58e862c9cfbaf0946605d30d9c8e8a37e2570c0c0719d626683f22db60fc9f81` |
| R10b-finite-burnin-derivative-sampling.md | 191 | `23683587539ef2905e0679100325808ae3f6353a3782a4bb362b2d24252034f0` |
| T68-finite-burnin-sampler-independent-audit.md | 519 | `442b446ae523b220e34ddadcf8c23b181ce60104100fd27c7e8027524840ed9f` |
| R12-signed-work-composition-contract.md | 108 | `390ede56727253adb0c23fb5356671f6b691b5c958ff4258d0e69ceeafd280ee` |
| R08-signed-arithmetic-work-gates.md | 138 | `f4ff50a6f56750ac010e7a6778499e6786fd2eda0fa7b24acf2c1bc00834a756` |

Line references below refer to these frozen versions. T65's accepted
status is recorded in D29; R10b/T68's accepted finite-time subroutine is
D30. Their original candidate-status prose is historical. R12 remains
a conditional interface.

Fix integers `d>=1`, `j>=1` and the T65 graph constants, with

    lambdaH=2*pi^2,  nu=lambdaH-1,  sigma=1,
    qH=exp(-lambdaH),
    rho=((1+qH)/(1-qH))^d,
    M=2*rho*exp(lambdaH),
    C=M/(nu-sigma)+1/(1+sigma),
    C R^2<=1/8,  r=R/(4M),  a=3r.

Retain the other T65 choices when using the graph in its phase proxy.
Fix its finite `L>=1` with

    sup_(||q||<=7/8) ||Q S_Lq||infinity<=r/16.

The space is the normalized unit torus, `P_t` has generator `Delta/2`,
`S_t` is the actual flow of `u_t=Delta u/2+u-u^3`, and

    H_L(q)=Pi S_Lq-Theta(Q S_Lq).

Let `g in C(X)` be supplied by an already paid representation, with
`||g||infinity<=3/4`. Let the unknown residual `e=v-g` be continuous,
with `||e||infinity<=delta`. Conditional on that paid transcript,
T69 constructs a fresh-seed coefficient and tuple

    (WH_j, Z_1,...,Z_j),

depending only on `g`, public constants and private randomness, such that

    ZH_j=WH_j product_(ell=1)^j e(Z_ell),
    E ZH_j=D^j H_L(g)[e,...,e],
    sup_g E WH_j^2<=V_H,j<infinity,
    E |ZH_j|^2<=V_H,j delta^(2j).

An explicit valid choice is precisely T69's:

    z0=5/4,
    Aj=sup_(n>=1) n^(2j) z0^(-n),
    V_b=4 exp(2(3^(2b)-1)L),
    Vstar_j=max(1,max_(1<=b<=j) V_b/a^2),
    Vmean_j=exp(2(3^(2j)-1)L),
    V_H,j=2[Vmean_j+Vstar_j^j Aj R^2].

Every seed path makes at most `j` new unknown-value acquisitions,
including repeated locations. The sampler is Borel and halts almost
surely for each promised input. If the supplied known-profile evaluator
has uniform actual cost at most `Gg(T)` in the shared primitive model,
then

    E Work(ZH_j)
      <=C_j [Kheat(d)+(Kbase+1)(d+1+Gg(T)) exp(4L)+1],
    Kbase=ceil(8/a^2).

Thus the work is `O(C_j'(1+Gg(T)))` when all graph, burn-in, dimension
and derivative-order parameters are fixed. It is uniform in the residual
size, coarse-grid size except through the supplied lookup cost, and
distance to the stable manifold. For fixed `d,s`, apply it separately
to the finitely many orders required by R12.

The same coefficient and labelled tuple represent mixed continuous
directions, replacing the last product by `product_l h_l(Z_l)`.
Consequently the sampler gives the actual finite signed derivative
measure, not only the diagonal action or an abstract bounded operator.

The primitive model permits exact exponentials as random waiting times,
Gaussian draws with a specified known nonnegative variance, continuous
uniform draws, basic real arithmetic, comparisons, modular reduction,
floor/integer indexing, stored-value access, and the fixed public
computable constants. Evaluation of the supplied `g` is charged at its
actual cost. This is T68's model, made explicit at T68:56--64; a separate
square-root operation is unnecessary when the Gaussian primitive takes
the known variance directly. The conclusion is not a finite-bit program.

## 2. Centered heat sampling: both regimes and the endpoint

T69:113--234 claims a uniformly bounded second moment for the normalized
signed kernel

    exp(nu*tau) B_tau/M
      =exp(lambdaH*tau)(P_tau-Pi)/M.

This is the right quantity: the unstable `exp(tau)` in `B_tau` has
already been included. A bound for the unnormalized heat-minus-uniform
coin would not suffice.

For `0<=tau<1`, let `S` be the fair signed endpoint choice in T69,
let `J` have mean `exp(-lambdaH(1-tau))`, and write

    beta=S*(2 exp(lambdaH)/M)*J.

The signed endpoint expectation is `(P_tau-Pi)f/2`. Hence

    E[beta f(Y)]
      =exp(lambdaH*tau)(P_tau-Pi)f/M,
    E beta^2
      =(2 exp(lambdaH)/M)^2 exp(-lambdaH(1-tau))
      <=rho^(-2)<=1.

At `tau=0`, the positive endpoint is exactly the supplied root, so
this identity includes `delta_x-lambda` without a limiting argument.
The strict split at `tau=1` is harmless: the long-lag rule below applies
there directly.

For `tau>=1`, the product geometric coordinate law conditioned on
being nonzero has exactly

    p_n=qH^(|n|_1)/(rho-1),  n in Z^d minus {0}.

Indeed the unconditioned product normalizer is `rho`, and its probability
of all zeros is `1/rho`. The stated coordinate zero probability, sign
coin and geometric magnitude reconstruct this product law. The rejection
success probability `(rho-1)/rho` is positive for every fixed `d>=1`.

For the source's value

    z=lambdaH*((|n|^2-1)*tau-|n|_1+1),

nonnegativity can be displayed without cancellation:

    z/lambdaH=(|n|^2-1)*(tau-1)+(|n|^2-|n|_1)>=0.

The inequalities use integral coordinates and the exclusion of `n=0`.
With `Aconst=(rho-1)exp(lambdaH)/M`, direct multiplication gives

    p_n Aconst exp(-z)
      =exp(lambdaH*tau-lambdaH*|n|^2*tau)/M.

Thus the expected Fourier coefficient has exactly the required spectral
factor. Both signs of each nonzero index are in the sampled law and in
the real Fourier sum; inserting another factor two would be incorrect.

The cosine estimator at T69:136--161 also checks directly. Exponential
arrivals give `K` with Poisson mean `pi`, so

    E[exp(pi)*(theta/pi)^K*c_K]
      =sum_(k>=0) c_k theta^k/k!=cos(theta).

Here the zero-th integer power is one, including at `theta=0`. Reducing
the angle into `[-pi,pi]` bounds every sample by `exp(pi)`. For the
average of `Kcos=ceil(exp(2*pi))` fresh copies,

    E Cbar_theta^2
      =cos(theta)^2+Var(Ctheta)/Kcos<=2.

The clock for `J_z` is independent of the cosine marks conditional on
`n,Y`. Therefore

    E beta^2<=2 Aconst^2
      =(rho-1)^2/(2rho^2)<=1/2.

For `tau>=1`, the heat Fourier series is absolutely summable uniformly
in its spatial argument, since

    sum_(n!=0) exp(-lambdaH*|n|^2*tau)
      <=exp(-lambdaH*(tau-1))*(rho-1).

This justifies integration against every bounded Borel `f`. It proves
the full T69:(2.1), not merely a formal identity on Fourier modes.

Work is uniform in `tau` and the root. Each coordinate proposal has
finite mean length bounded by a numerical constant, since `qH` is a
fixed number less than one. Repeated full-vector proposals have mean
count `rho/(rho-1)`. The cosine construction uses `Kcos` copies, each
with expected `pi+1` arrivals including the final crossing clock.
Repeated multiplication computes the integer power in `O(K+1)` work.
The sum of proposal costs up to acceptance has finite expectation even
though an individual proposal's length and its success can be correlated:
the event that trial `m` is reached depends only on earlier trials.

This verifies the form of T69:(2.9). Mode magnitudes and waiting times
are unbounded, but their bit lengths are not charged in this model.
No heat-density value, heat TV normalizer, variable exponential value,
or variable trigonometric value is needed by these rules.

## 3. Both Lyapunov--Perron time proposals have the correct law

T65:145--159 defines the forward centered integral with a minus sign
and the infinite future mean integral with a plus sign. Substituting
`u(r)=exp(-sigma*r)V(r)` and multiplying by `exp(sigma*t)` gives
exactly T69:(3.1). The cubic contributes the factor `exp(-3sigma*r)`.

The source mark has

    ell=M beta J_((nu-sigma)t).

Independence of the thinning clock gives

    E[ell f(Y)]=exp(sigma*t)B_t f,
    E ell^2<=M^2.

For the forward proposal, the branch-choice probability multiplied by
the exponential density is

    (Cf/C)*(nu-sigma)*exp(-(nu-sigma)A)
      =(M/C)*exp(-(nu-sigma)A).

Only `A<=t` contributes, with `r=t-A`. Multiplying this density by
the expected signed heat coefficient and thinning gives

    -M exp(-(nu-sigma)A)
       *[exp(nu*A) B_A/M]*exp(-2sigma*r)
      =-exp(sigma*A-2sigma*r) B_A.

Since `sigma*A-2sigma*r=sigma*t-3sigma*r`, this is the required forward
integrand. The killed `A>t` event has coefficient zero and does not
alter the integral or require renormalization.

For the backward proposal, the corresponding mixture density is

    (Cb/C)*(1+sigma)*exp(-(1+sigma)A)
      =exp(-(1+sigma)A)/C.

Here `r=t+A`. Multiplication by the mean of `C J_(2sigma*r)` and the
uniform endpoint gives

    exp(-(1+sigma)A-2sigma*r) Pi
      =exp(sigma*t+t-r-3sigma*r) Pi.

This includes the full infinite future tail with the correct sign.
The clock exponent is nonnegative in both proposals, including all
boundary states.

For each current state, conditional second moments give
`E Omega^2<=C^2`: the forward mark uses `E beta^2<=1`, the backward
mark is bounded by `C`, and killed marks vanish. This is an estimate
for the actual thinned coefficients. It does not replace a random
coefficient by its decaying expectation. Both proposal costs are
uniformly bounded by the heat-sampler cost plus a fixed number of
primitive operations.

## 4. The squared tree induction and every fixed-order leaf moment

T69:304--370 uses a Galton--Watson shape with offspring zero or three
and branch probability `p=1/6`. Its expected offspring is `1/2`, hence

    E total_nodes=sum_(h>=0) (1/2)^h=2,
    E N=(1-p)*E total_nodes=5/3.

Finite expected total population implies a finite tree almost surely.
This argument is independent of the signed coefficient analysis.

Give leaves coefficient `ell/(1-p)` and branches `Omega/p`. At a branch,
the three descendants start at the same sampled state, with independent
fresh descendant streams. The shared state implements the cube; replacing
it by three independent states would change the equation.

Let `K_T` be the total coefficient product. For the depth-truncated
nonnegative second moment, conditioning on the first node gives

    F_(D+1)(z)<=alpha*z+beta2*F_D(z)^3,
    alpha=M^2 a^2/(1-p)=(27/40)R^2,
    beta2=C^2/p=6C^2,
    F_0(z)=0.

There is no required independence between the parent coefficient and
its sampled child state. Conditional on both, the three descendant
second moments factor, and each is bounded by the same uniform `F_D`.
Only after this bound does one average the parent coefficient.

At `z0=5/4`, independent arithmetic gives

    alpha*z0=(27/32)R^2,
    beta2*R^6=6(CR^2)^2 R^2<=(3/32)R^2,
    alpha*z0+beta2*R^6<=(15/16)R^2.

Consequently all depth-truncated moments are at most `R^2`. On a
common tree construction their height indicators increase to one almost
surely. Monotone convergence, separately at each root and time, proves

    sup_(t,x) E[K_T^2 a^(2N) z0^N]<=R^2.

The feedback derivative is also as stated:

    3 beta2 R^4=18(CR^2)^2<=9/32<1.

The argument already closes with the strict supersolution; the feedback
derivative records an additional margin rather than an unproved
assumption. No inference from a deterministic operator contraction is
being substituted for this square-weight induction.

For every fixed integer `j>=1`, maximizing the real function
`x^(2j)exp(-x log z0)` gives

    Aj<=[2j/(exp(1)*log z0)]^(2j)<infinity.

Pointwise `N^(2j)<=Aj z0^N`, so

    E[N^(2j)K_T^2 a^(2N)]<=Aj R^2.

This is the weighted leaf moment actually needed after differentiation.
It remains valid when source/branch coefficients and all leaf positions
are correlated. It is not an unsupported deduction from the unweighted
second moment alone.

## 5. Identification with T65's actual graph and differentiation

For a fixed mean-zero `w` with `||w||<=2r<a`, the terminal monomial
`K_T product_i w(Y_i)` has uniform second moment at most `R^2`.
Conditional child independence and the cancelling branch/leaf sampling
probabilities therefore give the bounded Borel mean equation

    Vbar=A_w+K(Vbar^3).

All its terms are integrable. For example, after conditioning on the
current mark, each descendant has first absolute moment at most `R`,
so the absolute branch-product expectation is bounded by a constant
times `E|Omega| R^3`; `E|Omega|<=C`.

The operator `K` has norm at most `C` on bounded Borel trajectories.
Its cubic fixed-point map has Lipschitz constant at most `3CR^2<=3/8`
on the radius-`R` ball. T65's `exp(sigma*t)U(w)(t,x)` lies in that
ball and solves the same equation. So does `Vbar`, by Cauchy--Schwarz.
Uniqueness in the bounded Borel ball identifies them. Continuity of a
random measure in TV norm is neither assumed nor required.

T65:172--209 defines the actual graph on `||Qz||<3r`, with
`Pi U(z)(0)=Theta(Qz)`. Averaging T69's starting root at time zero
therefore gives exactly this functional. There is no discrepancy between
the graph's domain and T69's differentiating neighborhoods. For a
mean-zero base of norm at most `2r`, perturbations of sup norm less than
`r/4` have both `||z||<3r` and `||Qz||<3r`, since `||Q||<=2`.
The same mean-identification argument applies to these non-mean-zero
perturbations: the source annihilates their constant component in mean.

For a fixed tree, the derivative in `j` directions is a finite sum over
ordered injections into distinct leaf labels. Its norm is bounded by

    |K_T| N^j a^(N-j) product_l ||h_l||.

The case `N<j` is zero. Since `a>0`, negative exponents in the displayed
upper bound cause no singularity. Cauchy--Schwarz and the tilted moment
give the uniform integrable envelope

    E[|K_T| a^N N^j]
      <=[E K_T^2 a^(2N) z0^N]^(1/2)
          [E N^(2j) z0^(-N)]^(1/2)
      <=R sqrt(Aj).

Applying the same estimate to subsequent derivative orders controls
operator differences and integral Taylor remainders on the stated open
neighborhood. This justifies ordinary Frechet differentiation, not only
scalar directional derivatives. Arbitrarily sized continuous directions
are admitted by multilinearity once the derivative is taken at the base.

T69:446--468 consequently has the right direct-graph sampler: an ordered
injection supplies the factor `(N)_j`, and its coefficient square is
bounded by `a^(-2j)AjR^2`. Its `j!` multiplicity is already present in
ordered labels. This auxiliary sampler presumes a known `w`; T69 does
not misuse it as though `Q S_Lg` were supplied exactly.

## 6. Actual finite-burn-in leaves and the small-RMS step

R10b's coefficient bound can be verified before taking any residual
values. A finite majority tree is multiaffine in its distinct leaf labels
and bounded by one on the full leaf cube. Its selected mixed partial is
the signed average of its `2^b` corner values and has magnitude at most
one. Thus the coefficient of its order-`b` tuple sample is bounded by
`(N_L)_b<=N_L^b`. The rate-two population calculation gives

    E N_L^(2b)<=exp(2(3^(2b)-1)L).

A centered one-tree coin multiplies that coefficient by `+2` or `-2`,
giving the actual coefficient bound `E A_b^2<=V_b` used by T69. No
division by `e`, no lower bound on a residual value, and no independence
between the coefficient and its own selected tuple is used. The same
bound works for mixed labelled directions. R10b's full differentiation
argument, independently expanded in T68:258--294, identifies these
coefficients with actual `C(X)` flow derivatives.

The unmarked leaf is a different construction and needs its own bound.
T69:479--513 uses a centered primal sample `C_y(g)` with mean
`w_g(y)=Q S_Lg(y)` and absolute value at most two. Averaging `Kbase`
independent copies gives exactly

    E Wbar_y^2=w_g(y)^2+Var(C_y)/Kbase
      <=r^2/256+4/Kbase
      <=a^2/2304+a^2/2<a^2.

This holds uniformly over roots and over the complete `7/8` input ball.
The factor `2304` uses `a=3r`; it is not `256`. The inequality explicitly
pays to reduce variance and never substitutes the small deterministic
mean for a small random square.

Independent batches are assigned to distinct outer leaf labels, even
when their spatial locations coincide. Conditional on the complete
outer tree, this preserves both the product mean and the product of
second moments. Reusing a batch across factors would require a different
proof and is not the source's algorithm. The average has at most two in
absolute value, but that coarse pathwise bound would be too large for
the intended squared-tree argument; the strict RMS bound is what is used.

Every primal and derivative burn-in simulation still runs for the fixed
duration `L`. It evaluates only the supplied `g` at unqueried leaves and
does not call an evolved-value oracle. Its cost includes its entire
rate-two genealogy and all known-profile evaluations.

## 7. Nonlinear composition, label maps, and the coefficient square

For a fixed outer marked tree, the deterministic function differentiated
is

    F_T(q)=K_T product_(i=1)^N w_q(Y_i),
    w_q=Q S_Lq.

Each of the `j` direction labels chooses one factor. The exact product
rule therefore sums over all maps `f:[j]->[N]`, with `N^j` terms.
If `b_i` labels select factor `i`, its contribution is `D^(b_i)w_q`
when `b_i>0` and `w_q` when `b_i=0`. For instance, at order two the
`N` same-factor terms contain `D^2w_q`, while the `N(N-1)` distinct-
factor terms contain products of first derivatives. Restricting the
outer labels to injections would omit the former terms. No additional
factorial belongs to this all-map formula.

The expectation/derivative interchange is justified before replacing
leaf derivatives by random samples. On a neighborhood of `g` inside
the `7/8` ball, `||w_q||<=r/16<a`, and one may choose uniform operator
bounds `D_b=sqrt(V_b)` using the mixed finite-time coefficient bound.
For each order, set

    Rj=max_(b_1+...+b_k=j; b_i>=1)
                        a^(-k) product_i D_(b_i).

The finite maximum ranges over positive compositions of `j`. The
operator norm of the full labelled product-rule sum is at most
`|K_T| a^N N^j Rj`, which is integrable by Section 5. The analogous
bound at order `j+1` and the finite-time derivative continuity justify
the integral Taylor remainder and operator continuity. Since the outer
mean agrees with `Theta(w_q)` on this neighborhood, the differentiated
mean is the actual `D^j[Theta(Q S_L)](g)`.

For the actual sampler, condition on the entire outer tree and a uniform
map `f`. Let `k` be its number of marked outer leaves. All inner streams
are then independent. Factoring the coefficient square gives

    E[WGraph_j^2 | outer tree,f]
      <=N^(2j) K_T^2 a^(2(N-k)) product_(i:b_i>0) V_(b_i)
      <=N^(2j) K_T^2 a^(2N) Vstar_j^j.

The last step uses `k<=j`, `Vstar_j>=1`, and bounds each individual
`V_(b_i)/a^2` by `Vstar_j`. It does not replace a sum of derivative
orders by a number of marked leaves incorrectly. Averaging proves

    E WGraph_j^2<=Vstar_j^j Aj R^2.

The conditional means give the product-rule term, uniform map sampling
with multiplier `N^j` gives their full sum, and the preceding interchange
identifies its mean with the actual composed derivative. Therefore the
coefficient estimate and the unbiasedness estimate refer to the same
sampler, not to two different randomizations.

All selected coordinates come from finite-burn-in original-time leaves.
The coefficient can depend on `g` and can be correlated with those
coordinates; neither is a defect. It is independent of the unknown
residual values conditional on the paid coarse transcript. The bound
`|product_l e(Z_l)|<=delta^j` is pathwise and needs no independence
between selected residual evaluations.

The mixed-direction version preserves each label's coordinate through
the inner ordered tuple. Since `E|WGraph_j|<infinity`, the setwise
expectation `E[WGraph_j delta_(Z_1,...,Z_j)]` is a finite signed Borel
measure: dominated convergence proves countable additivity, and total
variation is at most `E|WGraph_j|`. It agrees on every product of
continuous directions with the derivative measure in T65. Finite sums
of such products are uniformly dense in continuous functions on the
compact product torus, so the measures agree. This is an identification
of constructed measures; it does not invoke a false generic
multilinear-operator representation theorem. The bounded-Borel extension
of their action is not a claim about Frechet derivatives on a new space.

## 8. The final mixture and the hard cap on every seed

The mean-flow derivative has coefficient square at most `Vmean_j`.
A fair coin selecting twice this sampler or minus twice the graph
sampler has mean

    D^j(Pi S_L)(g)-D^j[Theta(Q S_L)](g)=D^jH_L(g)

and coefficient square at most

    2 Vmean_j+2 Vstar_j^j Aj R^2=V_H,j.

This verifies the sign and factor two in T69:(9.1). Computing both
pieces independently and subtracting them would be a different
procedure with a possible `2j`-call cap; T69 chooses only one piece.

On a graph sample, the marked inner orders sum exactly to `j`.
Each order-`b_i` inner sampler uses at most `b_i` unknown acquisitions.
Unmarked inner batches use known `g` only. Consequently the new cap is
at most `j`, even when original-time coordinates coincide.

All generation, tuple selection, coefficient computation, and needed
known `g` evaluations can finish before the first unknown acquisition.
A too-small inner tree supplies a zero coefficient and may use dummy
tuple coordinates; no missing residual call is necessary. A zero return
can skip all its data calls. On an infinite generation or rejection
path, preparation never finishes and no subsequent unknown acquisition
occurs. Thus almost-sure termination is not being confused with the
stronger cap, which holds on every path. Earlier acquisitions used to
construct `g` remain charged to the enclosing algorithm.

## 9. Expected work, Borel rules, and unbounded random times

Each outer node's expected heat/time work is uniformly bounded in its
current state. Conditional expectation followed by summation over the
outer nodes charges it at most a fixed multiple of `Kheat(d)`. The
shape has mean two nodes. Leaf storage, coefficient products and map
selection cost `O(N+j)`; `j` independent uniform draws with indexing
select the all-map labels without enumerating `N^j` maps. Uniform draws
may be taken on `[0,1)` so every integer-index instruction has a valid
endpoint convention. Such conventions change no distribution or bound.

Every unmarked outer leaf is charged `Kbase` complete primal trees.
Every marked leaf of order `b<=j` is charged its complete R10b tree,
the selected coefficient's at most `2^b` full passes, stored values,
and tuple preparation. For one such fixed-order burn-in call,

    E Work<=C_j(d+1+Gg(T)) exp(4L).

This uses the accepted exact expected terminal population `exp(4L)`
and the total-node identity `(3N_L-1)/2`. There is no hidden evaluation
of all `N_L^b` derivative coefficients. The marked and unmarked sets
depend on the outer tree, but their cardinalities are at most its leaf
count, and the cost bounds are uniform in each supplied root. Conditioning
on the outer tree and map, then using `E N=5/3`, gives the work formula
in Section 1. No independence of work from the output weight is needed:
R12 asks for these two separate expectations, not a weighted-work moment.

Future LP time moves can make state times arbitrarily large. Every such
time is finite on a finite completed tree. It enters only arithmetic,
Gaussian variance parameters, heat marks and clock comparisons, all with
the uniform operation bounds already proved. The actual known-profile
flow simulations have duration `L`, not the random outer time. This
distinction is sufficient for the claimed horizon-independent constant.

Countably many labelled marks provide a single seed space. Finite tree
completion events, geometric rejection events, Poisson arrival counts,
endpoints, times, weights, maps and inner computations are Borel. The
positive acceptance probability, finite-mean arrival counts, subcritical
outer shape, and nonexplosive fixed-time inner trees give almost-sure
completion. A finite outer shape requests only finitely many inner
trees, although their number is not deterministically bounded. The union
of their conditional noncompletion events is null. Assigning return zero
on noncompletion makes the expectation a total Borel random variable;
it is not an algorithmic test for membership in that null event.

For transcript dependence, `(g,y)->g(y)` is jointly continuous on
`C(X) x X`. Every completed coefficient is a finite polynomial in
these evaluated values, including the corner-based partials and base
averages. The query-preparation law does not inspect `e`. This supplies
the Borel dependence needed after conditioning on the saved coarse
transcript, without selecting a nonmeasurable derivative representation.

## 10. Exact R12 correspondence and retained limits

| R12 requirement | T69 evidence and audit result |
|---|---|
| Same actual `H_L`, R12:11--15 and 45--49 | T65:420--459 defines the same graph composition; Sections 5 and 7 above identify the sampled mean with its actual derivative. PASS. |
| Every required fixed order, R12:45 | Tilt `z0>1` pays for each finite number of labels; no new order-dependent spectral restriction appears. PASS. |
| Uniform residual second moment, R12:48--52 | `E WH_j^2<=V_H,j` is uniform on the full promised `g` ball; multiply by the pathwise residual bound. PASS. |
| At most `j` unknown acquisitions on every path, R12:53 and 57--58 | Marked inner orders sum to `j`, one final mixture branch is selected, and all queries are postponed. PASS. |
| Borel rules and almost-sure halting, R12:53--54 | Countable marked-tree construction with explicit geometric/arrival primitives and Borel evaluation. PASS. |
| All inner work and known `g` calls charged, R12:17--23 and 55--56 | T69:(10.1) includes full `Kbase` batches, burn-in trees, coefficient passes and actual lookup cost. PASS in the stated model. |
| Polynomial per-sample work, R12:36--37 and 54 | Follows if the shared paid representation has `Gg(T)<=C_g(1+T)^b`; no such representation theorem is inferred merely from continuity or finite formula size. Conditional interface matched. |
| Gate A and full-work combination, R12:25--41 and 60--108 | Not established by T69 or this audit. No promotion. |

T69:711--738 correctly makes bounded-stencil constant lookup conditional
on the actual saved formula and its elementary evaluations. It gives an
example if the specified partition-function evaluations are primitives;
it does not prove a constant cost for every smooth interpolant described
abstractly in T65. A Gate A construction must supply the same `g` or a
fully corresponding replacement, its paid preprocessing, and an evaluator
whose cost fits the same declared model. T69 already keeps this obligation
open, so this is a retained condition, not a repair to its theorem.

In particular, exact exponential *waiting-time draws* and exact evaluation
of a variable exponential *function* are distinct primitives. The kernel
sampler needs only the former plus fixed constants. If the selected
known-profile representation requires the latter, its cost and permission
must be part of the shared model, as T69 explicitly states. Exact Gaussian
and uniform draws likewise remain continuous-seed idealizations; this
audit does not convert them to finitely many random bits or assign unit
bit cost to arbitrarily large integers and real coefficients.

The no-label version indeed gives a finite-variance base graph estimator,
and the primal mean-flow sampler gives a finite-variance `H_L(g)` estimator.
This alone only supplies an ordinary averaging upper bound of order
`eta^(-2)` to reach RMS `eta`. At `eta=O(exp(-T))`, that sufficient
bound has exponent two. It neither discharges Gate A's deterministic
precision/work requirement nor proves a lower bound against a better
known-profile computation.

T69's explanatory regrouping into Neumann kernels at lines 780--793 is
consistent with the accepted construction: putting all marked labels in
one of three child factors and averaging the two unmarked factors gives
the three feedback terms `3u^2 D^j u`. The actual identification and
variance proof do not depend on an unproved regrouping of a conditionally
convergent expansion; they were established directly by bounded means,
dominated differentiation, and the squared majorant.

The result covers inputs arbitrarily close to the stable manifold and
uses no phase-sign separation, phase oracle, evolved datum, derivative
oracle, heat density, or TV normalizer. Large constants, including Fourier
rejection, cosine averaging, `Kbase`, fixed burn-in work, and high-order
population moments, remain visible. There is no practical-speed,
dimension-uniform, finite-bit, rounding-stability, full signed numerical,
or end-to-end formalization claim.

## 11. Coverage, repair disposition, and provenance

The complete frozen T69 was audited as follows:

| T69 lines | Obligation | Disposition |
|---|---|---|
| 1--105 | Scope, constants, burn-in, coefficient and primitive dependencies | PASS with the stated paid-evaluator condition retained. |
| 107--234 | Clock/cosine primitives and both centered heat regimes | PASS, including lag zero and lag one. |
| 236--300 | Weighted LP source and both time proposals | PASS; forward killing and future tail are both included. |
| 302--386 | Subcritical halting and squared exponential leaf moment | PASS; constants independently recomputed. |
| 388--475 | Actual graph identification, Frechet exchange and direct derivative tuples | PASS; graph domain and non-mean-zero extension agree with T65. |
| 477--526 | Independent noisy base batches and small RMS | PASS; full batch cost retained. |
| 528--638 | All-label-map composition, coefficient second moment and signed measures | PASS; no missing factorial or forbidden operator-to-measure inference. |
| 640--678 | Final `H_L` mixture and every-path cap | PASS; the two final branches are alternatives. |
| 680--776 | Full ideal work, random times, measurable dependence and halting | PASS in the explicit shared model; lookup and bit-cost boundaries retained. |
| 778--846 | Neumann interpretation, failed shortcuts and remaining global work | Consistent with proved scope; Gate A remains open here. |
| 848--891 | Provenance and frozen dependency hashes | Checked; no new literature or novelty theorem imported. |

There is no correction candidate being substituted for a flawed original
claim in this audit. The Gaussian-variance convention, uniform-endpoint
convention, supplied-evaluator condition, and separation of random draws
from elementary function evaluation above make existing model choices
explicit; they do not alter T69's sampling law on a positive-probability
event, its PDE target, or any estimate. No source patch is requested.

Performed: full frozen-source reading; relevant project instructions,
research guide, D29/D30 ledger/checkpoint and formal toolchain inspection;
read-only working-tree status and SHA256 checks; independent conventional
derivation; and this sole report write. Hash and text-inspection scripts
were provenance checks, not numerical evidence for the theorem. No solver,
sampling experiment, implementation test, Lean build, or primary-literature
retrieval was performed. R10b/T68 retain their existing majority-model
attribution; this report makes no priority claim.

Skill routing: `math-auto-research` version `0.2.0`, research review role,
requested `gpt-6-astra` with `max` effort in the parent dispatch. The
parent's checkpoint records that explicit dispatch; this worker's tools
do not independently expose its backend model or effort, so no additional
verified backend assertion is made. No additional agents were used.

The audit's final SHA256 is reported to the root after writing rather
than embedded in its own bytes. The root owns all promotion, shared-model
correspondence with any Gate A candidate, and updates to the research state.
