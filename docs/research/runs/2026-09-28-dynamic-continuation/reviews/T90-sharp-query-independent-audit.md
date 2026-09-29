# T90: independent audit of sharp all-positive-diffusivity query order

Date: 2026-09-29. Conventional mathematical audit only.

**Verdict: PASS for frozen T87 in its stated ideal model.** The new
sampler has an actual, cutoff-independent Hilbert second moment. Its
mean is the derivative of the actual time-one Allen--Cahn flow. The
resulting grid size has no polynomial horizon factor, while the paid
work bound retains one. I found no material mathematical repair and
no change of the accepted signed input class, oracle, or risk needed.
Root source/correspondence review remains the acceptance gate; this
audit does not itself edit or promote an accepted claim.

The audited source is all 788 lines of
`reviews/T87-all-diffusion-sharp-query-feasibility.md`, SHA256

    acd788e6ee5564778cd0663be99aab17fb61f22bdfb4b345ccade008f18feff1

In particular the conclusion is a strong profile RMS upper, with the
spatial supremum inside the expectation. In combination with the
separately accepted D37 lower, it gives exact minimax query order for
both the point and the finite-indexed-Fourier-profile problems at RMS
tolerance `1/4`. It does not give exact operation order, a finite-bit
algorithm, a uniform vanishing-diffusion theorem, practical efficiency,
new numerical evidence, end-to-end Lean coverage, or novelty.

## 1. Frozen sources and exact contract

All paths in this table are relative to
`docs/research/runs/2026-09-28-dynamic-continuation/`. I read every line
of these six files, including the substantive derivations rather than
relying on their verdict labels. Their current hashes match T87's
recorded dependencies and the supplied T87 lock.

| Source | Lines | SHA256 |
| --- | ---: | --- |
| `reviews/T87-all-diffusion-sharp-query-feasibility.md` | 788 | `acd788e6ee5564778cd0663be99aab17fb61f22bdfb4b345ccade008f18feff1` |
| `reviews/T81-fixed-burnin-all-diffusion-upper-proof.md` | 857 | `d9b249ed669897df319ca712fc4ad26625fc97e1a9b32b79eacaf497b290bae5` |
| `reviews/T84-all-diffusion-upper-independent-audit.md` | 884 | `39cd98fcf957badbe382123bd1960eac7fb99441114c9433bd9ee0ff2d256d7d` |
| `reviews/R10b-finite-burnin-derivative-sampling.md` | 191 | `23683587539ef2905e0679100325808ae3f6353a3782a4bb362b2d24252034f0` |
| `reviews/T68-finite-burnin-sampler-independent-audit.md` | 519 | `442b446ae523b220e34ddadcf8c23b181ce60104100fd27c7e8027524840ed9f` |
| `04y-all-positive-diffusivity-profile-complexity.md` | 249 | `2a62aaec24cb762ebe8ef213ce7bbbb2dbd56e3b7ced197a851736db913d9ba8` |

The PDE and input class are unchanged:

    u_t=(kappa/2) Delta u+u-u^3 on X=(R/Z)^d,
    V={v smooth periodic real: ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v},
    kappa>0 and integers d,s>=1 fixed before T,
    q=s+d/2,       gamma=d/q=2d/(2s+d).

Only exact scalar values of the original `v` are supplied. Every
acquisition, including repeats and preprocessing, is charged. The
allowed algorithms are measurable adaptive randomized rules with
input-independent seeds, bias allowed, and almost-sure stopping on
each promised input. The upper construction is such a rule. Uniform
control of derivatives of `v` above total order `s`, initial
analyticity, a positive mass margin, and an attraction-basin restriction
are not assumed.

The paid model is precisely the one in 04y: exact real arithmetic,
comparisons, floors/ceilings, integer/index/modular operations, stored
reads/writes, `exp,log,sin,cos,positive-square-root`, and exact uniform,
exponential-clock and Gaussian draws with known parameters. Fixed
public constants and ideal unbounded real/integer/address words are
allowed. A derivative, transform, integral, PDE solve, or arbitrary
known-function evaluation is not a primitive. The covariance sampler
below constructs its own correlated Gaussians from scalar draws.

## 2. Lemma 1: tree law, moments, and physical normalization

The time-one ternary population has transitions `n -> n+2` at rate
`2n`. For every integer `a>=1`,

    2n[(n+2)^a-n^a]
      =2 sum_(r=1)^a binom(a,r)2^r n^(a-r+1)
      <=2(3^a-1)n^a.

Stopping at the first population at least `K` makes the process
bounded. Dynkin's formula and Gronwall give
`E N_(t wedge tau_K)^a<=exp(2(3^a-1)t)`. For `a=1`, the hitting
probability is at most `exp(4t)/K`; this proves nonexplosion before
removing stopping. Fatou gives the displayed higher moments. Thus,
for the time-one terminal count `n`,

    E n^a<=exp(2(3^a-1)).

If there are `B` splits, `n=2B+1` and the total number of particle
segments is `3B+1=(3n-1)/2`. The clock genealogy is independent of
the original input and the spatial marks.

The vertex polynomial `M(a,b,c)=(a+b+c-abc)/2` takes the majority
sign at every cube corner. Separate affinity therefore bounds it by
one on the cube. Disjoint child leaf labels make the complete tree
polynomial multiaffine and bounded by one on `[-1,1]^n`.

Brownian covariance `kappa t I` has generator `kappa Delta/2`.
Conditional independence of child trees after their common branch
endpoint gives reaction

    2[M(u,u,u)-u]=2[(3u-u^3)/2-u]=u-u^3.

The bounded first-branch renewal solution is the actual bounded mild
Allen--Cahn solution by bounded-range Lipschitz uniqueness. Torus
wrapping preserves this renewal identity. This checks R10b/T68's
normalization after changing only diffusivity; no independence of
different terminal leaf positions has been inserted.

## 3. Lemma 2: covariance domination for every finite genealogy

For each particle segment `e`, let its length be `ell_e>=0` and its
terminal-descendant indicator be `a_e in {0,1}^n`. Include the
ancestor's initial segment and all terminal segments stopped at time
one. Every root-to-leaf path then has length exactly one. Conditional
on these clock data, one coordinate of the lifted leaf displacement
has covariance `kappa C`, where

    C=sum_e ell_e a_e a_e^t,       C_ii=1.

At almost every time `t`, the alive particles partition the terminal
labels into nonempty sets `A_1(t),...,A_b(t)`, with `b<=n`. For any
real vector `z`, including vectors with mixed signs,

    z^t C z
      =integral_0^1 sum_(a=1)^b (sum_(i in A_a(t))z_i)^2 dt
      >=integral_0^1 (sum_i z_i)^2/b dt
      >=(sum_i z_i)^2/n.

Consequently `R=C-11^t/n` is positive semidefinite. The only
inequality is finite Cauchy--Schwarz on a partition. It neither uses
nonnegative `z_i` nor bounds the first branching time away from zero.

Finite zero-length edges and simultaneous endpoint branches change
the partition at only finitely many times, so the integral calculation
is unchanged. The one-leaf tree has its single segment of length one;
then `C=[1]` and `R=[0]`.

As a separate exact check, a single ternary split at time `t in [0,1]`
has `C=(1-t)I+t11^t`, `n=3`. Its residual matrix has eigenvalue
`2t` on the all-ones direction and `1-t` on its orthogonal complement.
It is positive semidefinite even at immediate branching and at a split
exactly at the final time. This check illustrates the degenerate cases;
the partition argument proves the arbitrary-genealogy claim.

## 4. Lemma 3: exact finite sampling of the residual law

Conditional on the genealogy, let `G` have covariance `kappa I/n` in
physical space. Independently of `G` conditional on that genealogy,
sample for each physical coordinate an `n`-vector of covariance
`kappa R`, with different physical coordinates independent. Call its
leaf vectors `Z_i`. For each physical coordinate `a`, Gaussian
characteristic functions give

    Cov((G_a+Z_(i,a))_i | genealogy)
      =kappa(11^t/n+R)=kappa C.

The means are zero and the independent-coordinate structure is the
same as for the original Brownian leaf marks. Thus the full joint
Gaussian laws agree, including singular cases. Taking their images
modulo the torus preserves equality of laws. Independence here is
conditional on the random tree; no unconditional independence of
random-variance mixtures is required.

The following algorithm supplies the residual law without a matrix
sampling oracle. Build the descendant incidence arrays and sum `C`;
there are `O(n)` segments and `O(n^2)` entries, so `O(n^3)` operations
suffice. In unpivoted semidefinite Cholesky, a positive diagonal pivot
is eliminated using its positive square root. Its Schur complement is
positive semidefinite by minimizing the original quadratic form over
that coordinate. If a remaining diagonal pivot is zero, positivity of
the two-coordinate quadratic forms forces the entire corresponding
remaining row and column to be zero. Set the Cholesky column to zero
and continue on the remaining principal submatrix.

This proves by induction that `kappa R=L L^t`, without division by
zero, an inverse, an eigensolver, or a square root of a negative number.
Each physical coordinate can now be formed as `L xi` from `n`
independent scalar standard normals. Matrix construction and
factorization cost `O(n^3)`; the draws and matrix-vector products cost
`O_d(n^2)`. All exact pivot comparisons and array accesses are paid.
Zero pivots, including all pivots for `n=1`, are explicitly handled.
These are exact-real claims, not stability claims for floating Cholesky.

## 5. Lemma 4: the common shift integrates the whole nonlinear polynomial

For a fixed tree and residual array, define

    F_q(u)=P_tree(q(u+Z_1),...,q(u+Z_n)).

This is a continuous periodic scalar function when `q in C(X)`.
The density of `G modulo X` is `h_(kappa/n)`, with Fourier coefficient
`exp(-2*pi^2*kappa*|nu|^2/n)`. Evenness of this density gives

    E_G F_q(x+G)
      =integral_X h_(kappa/n)(x-u) F_q(u) du.

Therefore an independent uniform `U in X` gives the random profile

    h_(kappa/n)(.-U) F_q(U)

whose expectation, first over `U` and then the residual marks/tree,
is the original flow `S_1^kappa q` when `||q||inf<1`. This uses
normalized torus Lebesgue measure; there is no volume factor missing.

For labelled directions `f_1,...,f_j`, differentiating `F_q` gives
the sum over ordered injections into distinct leaf labels:

    sum_I C_I(q,U+Z) product_(a=1)^j f_a(U+Z_(I_a)).

Here `C_I` is the mixed leaf partial of `P_tree`. All unselected
base values and all direction factors use the same translated points.
The shift integral acts on this complete expression. It does not
replace its factors by separate means. The same residual covariance
`kappa(C-11^t/n)` is used before and after differentiating.

For distinct labels the coefficient is exactly the signed corner
average

    C_I=2^-j sum_(epsilon in {-1,1}^j)
                   (product_a epsilon_a) P_tree(z_I=epsilon).

Hence `|C_I|<=1`, and repeated-label derivatives vanish. An unordered
set occurs `j!` times in the ordered sum for equal directions. The
ordinary Taylor expansion later divides by `j!` once; the tuple
estimator itself estimates the derivative without that division.

## 6. Lemma 5: a fixed Hilbert norm and its heat-kernel moment

Set `r=d+1` and use the real Hilbert space with norm

    ||f||_r^2=sum_(nu in Z^d) (1+|nu|^2)^r |fhat(nu)|^2.

It is separable, as is seen from finite Fourier sums with rational
real-basis coefficients. The `|nu|inf=l` shell has at most
`2d(3l)^(d-1)` points, and each reciprocal weight on it is at most
`l^-2r`. Thus

    sum_nu (1+|nu|^2)^-r <=1+4d3^(d-1)=E_d^2.

Cauchy--Schwarz proves `||f||inf<=E_d||f||_r` for finite sums. The
same estimate on tails proves absolute uniform Fourier convergence
for every Hilbert element and gives its continuous representative.
Consequently this is a continuous embedding into `C(X)`, and the
rectangular projection `P_N` is a Hilbert contraction. No assertion
that `C(X)` itself has type two is used.

For `theta=4*pi^2*kappa`, translation invariance gives

    ||h_(kappa/n)(.-U)||_r^2
      =sum_nu (1+|nu|^2)^r exp(-theta|nu|^2/n).

Put `a=theta/n`. The decreasing-Gaussian integral comparison gives
`sum_(l in Z)exp(-a l^2)<=1+sqrt(pi/a)`. Maximizing
`x^r exp(-a x/2)` gives the sufficient bound
`l^(2r)exp(-a l^2)<=(2r/a)^r exp(-a l^2/2)`.
Using

    (1+sum_i nu_i^2)^r
      <=(d+1)^(r-1)(1+sum_i |nu_i|^(2r))

and the product structure proves T87's specific constant

    b=1+sqrt(pi/theta),       c=1+sqrt(2*pi/theta),
    C_h=(d+1)^(r-1)[b^d+d(2r/theta)^r c b^(d-1)],
    ||h_(kappa/n)||_r^2<=C_h n^(r+d/2)<=C_h n^(r+d).

Here `n>=1` absorbs the constant terms into the indicated powers.
The infinite Gaussian sum and integral comparison prove a bound;
neither is evaluated by the algorithm. The displayed public `C_h`
uses only allowed scalar operations and fixed constants.

Together with Lemma 1 this yields, for every fixed integer `j>=0`,

    E[n^(2j)||h_(kappa/n)||_r^2]
      <=V_j=C_h exp(2(3^(2j+r+d)-1))<infinity.

The exponent `2j+r+d` is an integer, so the cited population-moment
bound applies directly. These constants can be enormous but do not
depend on `N`, `T`, the datum, or a chosen accuracy.

## 7. Lemma 6: Bochner expectations and genuine Hilbert derivatives

On each finite-tree event, the residual arrays are Borel functions
of clocks and scalar Gaussian draws by the guarded factorization in
Lemma 3. For fixed `n`, the map `U -> h_(kappa/n)(.-U)` is continuous
in `H^r`: use Fourier-coordinate continuity and its summable norm
envelope. The remaining scalar factors are measurable evaluations of
continuous profiles at Borel positions. Countably many finite shapes
and counts cover the termination event. Thus the field in Lemma 4,
and each directional derivative field, are strongly measurable.

For fixed direction vectors its order-`j` field norm is bounded by

    n^j ||h_(kappa/n)||_r product_a ||f_a||inf.

Lemma 5 and Cauchy--Schwarz make this envelope integrable. Each
directional field has a Bochner expectation in the separable `H^r`.
These expectations define a bounded multilinear operator `A_j(q)`
with norm at most `B_j=sqrt(V_j)`. It is unnecessary to claim Bochner
measurability in the space of multilinear operators or in a
total-variation space of Dirac measures.

There is also no unsupported differentiation-under-expectation step.
If the segment from `q` to `q+h` stays in the open unit ball of
`C(X)`, the finite tree polynomial and the cube partial bound imply

    ||A_tree,j(q+h)-A_tree,j(q)||op
      <=n^(j+1)||h_(kappa/n)||_r ||h||inf,

    ||A_tree,j(q+h)-A_tree,j(q)
          -A_tree,j+1(q)[.,...,.,h]||op
      <=(1/2)n^(j+2)||h_(kappa/n)||_r ||h||inf^2.

These are pathwise bounds uniform over unit direction tuples. After
taking the directional expectations and then the operator supremum,
their expected scalar envelopes are finite by Lemma 5. They prove
operator-norm continuity and Frechet differentiability of every
`A_j`. Induction starting at `A_0` proves a genuine `C^infinity` map

    S_1^kappa: {q in C(X): ||q||inf<1} -> H^r(X),
    D^jS_1^kappa(q)=A_j(q).

The equality with the actual PDE flow follows from Lemma 4 and the
continuous embedding: bounded evaluation at any `x` commutes with
the Bochner integral, and gives the renewal-flow value of Lemma 1.
Thus the map has not been replaced by a mollified or projected flow.

Taylor's integral remainder on the segment `g+te`, `e=v-g`, is

    ||S_1^kappa v-sum_(j=0)^(J-1)D^jS_1^kappa(g)[e^j]/j!||_r
       <=B_J ||e||inf^J/J!.

This is an estimate in the fixed Hilbert space before projection.
Applying `P_N` cannot increase it, so it has no Dirichlet-kernel or
cutoff factor.

## 8. Lemma 7: the actual scalar-query tuple sampler and Fourier signs

Build the tree and residual marks, draw independent uniform `U`, and
set `Y_i=U+Z_i modulo X`. If `n>=j`, choose a uniform ordered
injection `I` using partial Fisher--Yates. An exact uniform draw and
floor give each finite integer choice; assigning the unit endpoint to
the last valid index makes it defined on that null endpoint as well.
The coefficient `C_I` is computed by the corner formula using cached
known values `g(Y_i)`. Only after this preparation acquire the `j`
original values `v(Y_(I_a))`.

The scalar and field returns are

    z=(n)_j C_I product_a[v(Y_(I_a))-g(Y_(I_a))],
    W_j=h_(kappa/n)(.-U) z.

For `n<j` return zero and make no residual acquisitions. Conditional
on the whole tree/residual/root array, averaging over `I` cancels
the factor `(n)_j` and gives exactly Lemma 4's ordered derivative
sum. Thus, with `delta=Cint k^-s`,

    E W_j=D^jS_1^kappa(g)[e^j],
    E||W_j||_r^2<=delta^(2j)E[n^(2j)||h_(kappa/n)||_r^2]
                    <=V_j delta^(2j).

The coefficient and the kernel shift generally depend on the same
`U` and residual array. No independence between those quantities was
used: the translated kernel has the same norm on every path, and
`|z|<=n^j delta^j` is a pathwise bound. Repeated spatial locations
still incur repeated paid acquisitions, even though leaf labels are
distinct.

For one representative of each nonzero pair `{nu,-nu}`, the exact
real coefficients of `P_NW_j` are

    c0=z,
    c_(nu,c)=2z exp(-2*pi^2*kappa|nu|^2/n) cos(2*pi*nu.U),
    c_(nu,s)=2z exp(-2*pi^2*kappa|nu|^2/n) sin(2*pi*nu.U).

Indeed the complex coefficient is
`z exp(-2*pi^2*kappa|nu|^2/n) exp(-2*pi*i*nu.U)`; the real sine
coefficient is minus twice its imaginary part, giving the positive
sign above. This establishes the factor two and sine sign without
requiring an infinite heat series in the program.

## 9. Lemma 8: Hilbert averaging and the actual weighted clipping

For fixed input `v`, the coarse transcript and its `g` are
deterministic. Fresh samples at an order are independent copies,
conditional on that transcript. For `X_a=P_N(W_(j,a)-E W_j)`,
Fubini, independence, and centering imply
`E inner(X_a,X_b)=0` for `a!=b`. Absolute integrability follows
from their second moments and Cauchy--Schwarz. Expanding the finite
Hilbert norm square therefore gives

    E||M^-1 sum_a X_a||_r^2
      =M^-2 sum_a E||X_a||_r^2
      <=V_j delta^(2j)/M.

The last step uses Hilbert variance subtraction and contractivity
of `P_N`. Modes within a sample are correlated. This argument uses
independence of different samples only. Independence between derivative
orders is not needed for the later Minkowski sum.

For an actual real-basis array, Parseval with conjugate pairs gives

    ||p||_r^2=c0^2+(1/2)sum_(nu representatives)
                    (1+|nu|^2)^r(c_(nu,c)^2+c_(nu,s)^2).

Thus the real-coordinate weights are positive and diagonal, with
the factor `1/2` shown. If `t_l` is the true target coefficient and
lies in a clipping interval, scalar interval projection satisfies
`|clip(c_l)-t_l|<=|c_l-t_l|` pathwise. Summing with these actual
weights decreases the squared Hilbert error. The true coefficients
of `S_1^kappa v` lie in `[-1,1]` for the constant and `[-2,2]`
for each sine/cosine component, since its sup norm is below `7/8`.

Clipping is therefore valid for the Hilbert loss used in T87, with
no mode-count factor and no assumption of unbiasedness afterward.
It is not a claim that arbitrary coordinate clipping contracts the
spatial supremum norm.

## 10. Lemma 9: inherited interpolation, paid solvers, and saturation

I checked the interfaces against T81 Sections 3--4 and 7 and their
full independent derivations in T84 Sections 2--6 and 9. T87 changes
neither the interpolant nor the known-profile solver nor the saturation.

The grid interpolant uses a fixed tensor polynomial stencil attached
to each grid node and a normalized Gevrey-2 bump partition. Comparing
to the total-degree-`s-1` Taylor polynomial at an evaluation point
uses only total derivatives through `s`, including when `s=1`.
Fixed overlap and bounded stencil cardinal factors give

    ||g||inf<=3/4,       ||v-g||inf<=Cint k^-s,
    ||partial^alpha g||inf<=B0(C0 k)^|alpha|(alpha!)^2.

There are exactly `k^d` initial acquisitions. Floors and modular
indices locate a fixed number of records per later lookup; guarded
bumps and their positive translate denominator use a fixed number
of allowed scalar operations. Preprocessing costs `O_(d,s)(k^d)`
and actual evaluation costs `Gg<=C_(d,s)`. The imposed all-order
bound is a property of this chosen known `g`, not of the unknown `v`.

The actual PDE's fixed-time analytic tail remains valid for every
fixed positive diffusivity. The shifted heat-kernel `L1` bound is
`exp(|y|^2/(2*kappa*t))`; the varying tube of radius proportional
to `sqrt(kappa*t)` gives a local holomorphic mild contraction.
Restarting from the actual real solution, bounded by one, yields a
fixed positive strip after a fixed positive time. This gives the
uniform `A_kappa exp(-b_kappa N)` tail at time one. Scalar comparison
from `1/2` gives `(1+3exp(-2))^-1/2<7/8`. Neither fact requires a
stable graph, synchronization, or a favorable spectral gap.

For a known input of inverse Gevrey scale `R`, evaluator cost `Wq`,
and uniform bound at most one, the paid deterministic solver uses

    E=1+P+S+log(R+1),
    H=ceil(C_kappa R E^(2d+8)),
    p=ceil(C_kappa E^(d+4)),
    n_pan<=C_kappa E^(d+2).

Early Gevrey tails plus late analytic tails and the Galerkin bound
`exp(11 Lambda_H S)` close the spatial bootstrap. Initialization is
by actual known-profile values and a paid FFT; a padded grid larger
than `6H` gives the exact projected cubic. The initial time disk has
radius of order `(kappa H^(d+2)+Lambda_H)^-1`. Doubling startup
panels and then balanced panels lie in the displayed fixed-parameter
ellipses of T84 Section 5. The semigroup nodal contraction and its
product stability bound `exp(C S Lambda_H beta_p)` give the claimed
finite iteration count and time error. They do not introduce a
stiffness factor exponential in `H^2 S`.

The exact time weights are generated with the finite recurrences
`I_0=(1-exp(-z theta))/z`,
`I_m=theta^m/z-(m/z)I_(m-1)`, with separate zero-mode and zero-node
formulas. Nonzero-mode `z=2*pi^2*kappa|nu|^2*ell` is positive.
Actual cardinal coefficients, weights, transforms, initialization,
array accesses and output evaluation cost

    C n_pan (2H+1)^d[p^3+p^2 log(H+1)]
      +C(2H+1)^d[log(H+1)+Wq]
    <=C R^d E^a0(1+Wq),       a0=2d^2+20d+50.

These are finite real-arithmetic programs, with fixed public loop
counts. The inherited proofs explicitly preserve conjugate symmetry
and hence real outputs. The exact weight recurrence is not being
claimed stable in floating point.

The fixed saturation `chi` is primitive-evaluable, equals the identity
on `[-7/8,7/8]`, has range `[-15/16,15/16]`, and has Lipschitz
constant `25`. Its guarded exponential transition has Gevrey-2
derivative bounds. For every clipped box-`N` array with `K` entries,

    ||partial^alpha p||inf<=2K(2*pi*N)^|alpha|.

The ordered finite-jet chain rule, the multinomial bound
`sum 1/(beta_1!...beta_l!)<=l^|alpha|/alpha!`, and
`|alpha|!<=d^|alpha| alpha!` give the stated uniform Gevrey-2
bound for `chi(p)` at inverse scale `Rhat=NK`. Summing after a fixed
radius reduction gives a fixed Gevrey norm. Every evaluation really
costs `O_d(K)`, including coefficient reads. These bounds hold for
every completed clipped array, not merely on a high-probability set.

I have not freshly audited T70/T74 as separate historical sources;
the used interpolation, solver, and composition arguments are present
in the completely read T81/T84. Their graph-specific predecessors
are not premises for this audit.

## 11. Lemma 10: parameters, paid base accuracy, and no cutoff query loss

For `T>=2` take the exact T87 choices

    S=T-1,       epsilon=exp(-S)/(16Lchi),       Lchi=25,
    N=max(1,ceil((S+log(32Lchi A_kappa))/b_kappa)),
    K=(2N+1)^d,
    J=ceil(1+d/(2s)),       m=J-1,
    Cstar=1+sum_(j=1)^m sqrt(V_j)Cint^j/j!+B_J Cint^J/J!,
    k=max(k0,ceil((4E_d Cstar/epsilon)^(1/q))),       M=k^d.

Then the deterministic analytic tail is at most `epsilon/2` and
`N=O(1+T)`. All constants in `Cstar` are fixed before `T`. Since
`epsilon^-1=16Lchi exp(T-1)` and ceilings add at most one,

    k^d<=C exp((d/q)T),       log k=O(1+T).

In particular no `K` or logarithm of `K` enters the acquisition
count. Fixed public constants can be increased to absorb `k0` and
the bounded horizon endpoint.

For the base solve put

    D_N=sqrt(K)(1+dN^2)^(r/2),
    tau=epsilon/(4E_d D_N),       Pbase=log(1/tau)>1.

The known-profile solver at time one and scale `R=k` returns real
`U_base` with sup error `tau`. Take its public cutoff at least `N`;
the original cutoff already grows faster than `N` after increasing
a fixed constant, so this preserves its paid bound. Each complex
Fourier coefficient of the error has magnitude at most `tau`.
Summing the `K` weighted squared coefficients therefore gives

    ||P_N(U_base-S_1^kappa g)||_r<=D_N tau
                                      =epsilon/(4E_d).

This is the correct conversion for the actual complex coefficient
norm; it does not miss a real-basis factor of two. Because
`log D_N=O_d(log(2+T))`, the increased base accuracy still costs only
`C k^d(1+T)^a0` paid operations and no new original-data values.

The segment `(1-t)g+tv` has sup norm at most `3/4`. Lemmas 6--8
apply to the exact raw polynomial and yield, by Minkowski in `L2(H^r)`,

    (E||p_raw-P_N S_1^kappa v||_r^2)^(1/2)
      <=epsilon/(4E_d)
        +sum_(j=1)^m sqrt(V_j)Cint^j k^(-js-d/2)/j!
        +B_J Cint^J k^(-Js)/J!
      <=epsilon/(4E_d)+Cstar k^-q
      <=epsilon/(2E_d).

Here `Js>=s+d/2=q`, and `js+d/2>=q` for all sampled `j>=1`.
The extra derivatives are derivatives of the fixed-time flow with
respect to its continuous initial function, whose boundedness was
proved in Lemma 6; they are not unprovided derivatives of `v`.

After the real-coordinate clipping, the same Hilbert bound holds.
Using the fixed embedding and then the deterministic analytic tail,

    (E||p-S_1^kappa v||inf^2)^(1/2)
      <=E_d epsilon/(2E_d)+epsilon/2=epsilon.

The tail omitted here is the actual target tail. Individual random
heat fields need not have a common analytic strip as `n` varies;
their fixed Hilbert second moments suffice. This is precisely the
step that removes the polynomial query overhead of T81.

## 12. Lemma 11: actual continuation and finite strong-profile output

Let `qhat=chi(p)`. Since `chi(S_1^kappa v)=S_1^kappa v`,

    (E||qhat-S_1^kappa v||inf^2)^(1/2)
      <=25epsilon=exp(-S)/16.

The difference of two real Allen--Cahn solutions has reaction
coefficient `1-(u^2+uw+w^2)<=1`. Applying the maximum principle to
the exponentially rescaled difference gives the actual-flow bound

    ||S_t^kappa f-S_t^kappa h||inf<=exp(t)||f-h||inf.

The final known-profile solve has uniform inverse scale `Rhat=NK`,
evaluator cost `O(K)`, time `S>=1`, and precision `Pout=T+log(16)`.
On every completed clipped transcript it returns a real Fourier array
`U_T` with conditional sup error at most `exp(-T)/16`. Thus

    sup_(v in V)(E||U_T-S_T^kappa v||inf^2)^(1/2)
      <=1/16+exp(-T)/16<=1/8.

The base bias, Taylor bias, sampling, omitted-mode tail, clipping,
saturation, and paid final evolution error are all in this budget.
The embedding, saturation, and continuation inequalities hold
pathwise for the spatial supremum.
There is no exchange of `sup_x` and expectation, no selected good
event, and no conclusion merely from pointwise RMS bounds.

The final cutoff satisfies

    H_out<=C Rhat Eout^(2d+8)<=C(1+T)^(3d+9),

so there are at most `C(1+T)^(3d^2+9d)` array entries. Returning this
indexed array and evaluating it at any specified point are finite
paid operations, with polynomial evaluation cost and no new `v`
calls. The returned polynomial is the unsaturated solver output;
only its initial profile `qhat` was saturated.

## 13. Lemma 12: complete paid work, all-seed cap, and Borel halting

Conditional on a finite tree, constructing its covariance, residual
marks, cached known values and corner coefficient, and all retained
sample coefficients costs at most

    C_(d,j)[n^3+(1+Gg)n+K].

The `O(n^3)` matrix work is new relative to T81 and must be retained.
Lemma 1 gives finite `E n^3`, so it is a fixed constant at burn-in
one. The expected cost per order-`j` sample is consequently
`C_(kappa,d,s,j)(1+K)`. It includes storage, random primitives,
Fisher--Yates selection, at most `2^j` upward tree passes, frequencies,
and accumulator updates. All derivative orders are fixed with `d,s`.

The deterministic grid/base cost, all sample work, and the final
solver cost therefore give

    sup_v E Work_T
      <=C k^d(1+T)^a0+C k^d(1+T)^d
          +C(1+T)^(a0+d^2+2d)
      <=C exp(gamma T)(1+T)^A,
    A=a0+d^2+2d+2

as one sufficient exponent. The final term uses
`Rhat^d=O((1+T)^(d^2+d))` and actual evaluator cost
`O((1+T)^d)`. Public frequency enumeration, coefficient extraction,
allocation, clipping, stored output, and one final point evaluation
are all absorbed. No hidden `k^(dj)` tensor is formed.

Every original-data acquisition is either a coarse-grid call or one
of at most `j` calls in a completed tuple sample. Thus on every seed,

    Q_T<=k^d+sum_(j=1)^m jM
        =[1+J(J-1)/2]k^d<=C exp(gamma T).

Known `g` evaluations and the solver's initialization evaluations use
only the stored formula and transcript. Sharing the `K` coefficients
does not multiply the tuple's original-data calls. On a null seed
where genealogy preparation never finishes, that tuple has acquired
no original values; earlier completed tuples still satisfy the same
public total cap. The hard query cap is not a deterministic work or
tree-size bound.

All operations are Borel on finite-tree events. Positive-pivot and
zero-pivot branches are Borel, all divisions occur in legitimate
guarded branches, and all deterministic solver loops have public
finite counts. Continuous `v,g` make queries at Borel random positions
measurable. Nonexplosion and the finite moments prove almost-sure
halting and finite expected work for each fixed requested horizon.
Only finitely many samples are requested at that horizon.

The finite completion event is a countable Borel union. Assigning
the zero array on its null complement defines the usual random
output without claiming a program detects nontermination. The
array-to-`C(X)` map is continuous, making the spatial sup-norm loss
measurable. Optional clipping of arbitrary finite off-promise
responses leaves every promised input unchanged; fixed algebraic
solver loops and the guarded interpolant remain defined even if
their accuracy assumptions fail. No stochastic regularity test or
unverified convergence test governs the work or output validity.

## 14. Lemma 13: the bounded-horizon patch

For `0<=T<=2`, the inherited construction uses one fixed sufficiently
fine grid with `exp(2)Cint k_b^-s<=1/32`. The actual-flow comparison
then bounds its input interpolation error by `1/32` throughout this
interval. Uniform early Gevrey and later analytic tails permit a
fixed Fourier cutoff and initialization grid giving Galerkin error
at most `1/32` including time zero.

On a fixed neighborhood of these bounded fixed-dimensional ODE
trajectories, the polynomial vector field and its first derivative
have public bounds. The local Euler defect at step `T/n_b` is
`C(T/n_b)^2`; finite Gronwall and a sufficiently large fixed `n_b`
give global error at most `1/32` and close the neighborhood bootstrap.
At `T=0`, the same fixed number of zero-length updates is defined.

The resulting real Fourier polynomial has deterministic spatial-sup
error `3/32<1/8`, fixed query count and fixed paid work. Increasing
the constants in the asymptotic bounds incorporates this interval.
It does not use the positive-time common-Gaussian argument at time
zero or the time-panel lemma outside its `S>=1` range.

## 15. Lemma 14: exact correspondence to D37--D39

The input class, fixed parameters, point oracle, stopping rules, seed
independence, and paid primitive model in Section 1 match 04y's
accepted D37--D39 exactly. The upper even works on the same bounded
smoothness class without the sign-change condition, so its use of
the full signed subclass introduces no hidden restriction. The same
algorithm is used for each fixed prescribed real `T` and all `v`.

D39's point criterion is uniform MSE at most `1/16`, equivalently
RMS at most `1/4`; its profile criterion is uniform
`E||U-S_T^kappa v||inf^2<=1/16` with finite explicitly indexed real
Fourier output. Lemma 11 gives RMS at most `1/8`, hence MSE at most
`1/64`, and satisfies the required finite output contract. Evaluating
the array at the fixed `x*` preserves this risk bound and requires no
extra unknown-input values.

The hard upper cap consequently bounds the worst-input expected
query count by `C exp(gamma T)`. D37 supplies the matching lower
`c exp(gamma T)` for every point rule at the looser common MSE
threshold `1/16`, for all sufficiently large real `T`. For any
admissible profile rule, finite evaluation at `x*` turns it into
such a point rule at the same original-data query cost. Therefore,
using the separately accepted lower exactly as stated,

    Q_point(T)=Theta(exp(gamma T)),
    Q_profile(T)=Theta(exp(gamma T)).

These are minimax worst-input expected-query quantities. The hard
input in the lower may depend on both `T` and the algorithm; no
single hard input for every horizon is asserted. Bias, adaptivity,
random stopping, and unbounded point outputs remain allowed. I did
not re-prove or independently re-audit T82/T83's lower-bound PDE and
information argument in this task.

For paid work the only proved sandwich remains

    c exp(gamma T)<=W_point(T),W_profile(T)
                      <=C exp(gamma T)(1+T)^A.

Thus their exponential rates still match, but this audit does not
remove their polynomial overhead. Query complexity permits free
auxiliary arithmetic; it must not be conflated with the paid model.

All statements fix `kappa>0` before `T` grows. The heat norm already
displays inverse powers of `kappa`, and the analytic-strip constants
and solver constants can also deteriorate as `kappa` decreases.
No assertion is made at `kappa=0` or uniformly as `kappa` tends to
zero, and no dimension-uniform efficiency is claimed. The risk is
at each prescribed horizon, not an expectation of a supremum over
all horizons or a pathwise infinite-time guarantee.

## 16. Scope, attribution, and review provenance

PASS requires no amendment to the frozen T87 statement. In particular,
the fixed Sobolev field construction is an actual modified sampling law,
with the residual covariance and full-polynomial common translation
specified. Retaining the old Brownian leaf law while merely adding a
heat factor would not be covered by this audit. Nor would replacing
the Hilbert calculation by a generic claim about the sup-norm space.

I opened the primary An--Henderson--Ryzhik text and inspected its
diffusion convention and Section 3.1. It attributes the ternary
Allen--Cahn majority representation to Etheridge--Freeman--Penington.
The normalization for this project's signed field and rate two was
checked directly in Lemma 1. This is a bounded attribution check,
not a priority search for the covariance modification or the combined
query theorem. [Primary text](https://arxiv.org/html/2209.03435).

The proof above independently checks every new mathematical bridge
from finite genealogy to strong profile risk. Its only inherited
subroutines are those explicitly checked against T81/T84 and R10b/T68.
Accepted D37 is reused for the final query-order consequence and has
a separately stated audit boundary. Full Lean verification, machine
implementation, finite precision, random-bit cost, practical speed,
and worldwide novelty remain outside this PASS.

The task's only owned output is this new T90 file. Before writing I
checked that it did not exist and inspected the dirty working tree.
No frozen source, accepted ledger, run state/configuration, code,
Lean source, numerical artifact, canvas, or global model setting was
changed by this task. No unknown input was queried. No stochastic
simulation, numerical PDE solve, symbolic-algebra program, implementation
test, or theorem-prover invocation was performed. The three-leaf
matrix calculation above is an exact analytic check, not experimental
evidence.

The math-auto-research skill, configured General profile, defaults,
routing, and execution instructions were read. The parent dispatch
record for T90 requests `gpt-6-astra` with `max` reasoning, matching
the configured research role. The actual serving backend and effort
are unexposed to this worker's tools; no backend attestation, model
switch, cost, or token total is inferred from those requested settings.

| Read instruction/toolchain source | SHA256 |
| --- | --- |
| `/Users/michael/.agents/skills/math-auto-research/SKILL.md` | `135d3e4394a3cd65d8da11336382abeb01020b412d60a4509874bd4ca70c9e12` |
| `/Users/michael/.agents/skills/math-auto-research/config/defaults.json` | `790c96ba540ede32bd8a0fd5e86d79c479365e072736ff9961575ee680cb653e` |
| `/Users/michael/.agents/skills/math-auto-research/config/profiles/general.json` | `ef04dd919d4015574ad546f8de63f3c6e3707420d9f47f36030fd022cb8f8847` |
| `/Users/michael/.agents/skills/math-auto-research/references/model-routing.md` | `1f3f034cc2c73e92acfcdc65970a35ca17cff84418652fc69b6824d0bb2e3673` |
| `/Users/michael/.agents/skills/math-auto-research/references/execution.md` | `ebcee187ef41c2c47a185f47f64fb864c5a89c55f43cfc74cae87a3da0c7c987` |
| `formal/lean-toolchain` | `302cd63c54178885b89e669f33b38f12f4dd7ae7e5cac537b3203e3768d8fb2b` |

The source tree's configured toolchain was read as
`leanprover/lean4:v4.33.0` for context only. I read the supplied AGENTS
instruction and the applicable filesystem ancestor instructions,
repository `CLAUDE.md` scope passages, README and research README,
the run's complete initial context, current checkpoint excerpts,
D37--D39 ledger passages, and the T90 model-use entry. This does not
claim to audit all historical run records or inaccessible sessions.
Initially combined tool outputs truncated some context passages; all
six frozen proof/synthesis files in Section 1 were subsequently read
in complete untruncated ranges. No finding relies on omitted output.

Actual activity was read-only source/context discovery and inspection,
source hashes and line counts, one primary-source opening, conventional
derivation, and creation and verification of this audit. Frozen source
hashes are checked again after the write. The audit's own final hash is
reported in the handoff rather than embedded in itself.
