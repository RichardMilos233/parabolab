# T83: independent audit of the all-positive-diffusivity signed lower bound

Date: 2026-09-29, Asia/Jakarta.

**PASS for the conventional theorem in the frozen 698-line T82 source.
No mathematical repair is required.** The actual time-one flow has the
claimed mixed-L1 third derivative, its full Hamming-layer profile has the
claimed concentration bound, and the subsequent actual PDE estimates work
for every fixed positive heat gap. The unconditioned prior, exact-value
transcript reduction, and expected-query conclusion preserve the stated
algorithm class and constants.

This verdict includes lambda=2*pi^2*kappa below one, equal to one, and
equal to one half. It requires neither a stable graph nor a global phase.
It is an independent mathematical audit, not root acceptance, a matching
upper theorem, a numerical result, a Lean certificate, or a priority claim.

## 1. Frozen target, independence, and exact statement

The complete source inspected, including its scope and evidence paragraphs,
was:

    reviews/T82-all-diffusion-prior-lower-proof.md
    698 lines
    SHA256 0b331397bbda06ba02381009ce95bfd7656aabb4bd196bac5e67a616b3a2320a

T83 was dispatched to audit that frozen candidate. This task made no
authoring contribution to T82 and owns only this new review file. All
candidate sources, ledgers, formal files, code, and numerical artifacts
were read-only. The pre-existing dirty working tree was inspected.

The theorem being passed fixes kappa>0, integers d,s>=1, and x* on the
normalized period-one torus X. The actual equation is

    u_t=(kappa/2) Delta u+u-u^3,    u(0)=v.

The fixed class is precisely

    V={v smooth periodic real:
       ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

For every real T beyond one fixed finite threshold, every admissible
algorithm with class-uniform MSE at most 1/16 must have

    sup_(v in V) E Q_T(v)
      >= C exp(2dT/(2s+d)),
    C=3*2^(-d-16)*(aI)^(d/(s+d/2))>0.

More strongly, the specified finite prior, fixed before the algorithm,
has this average expected cost. The expensive input can depend on T and
the algorithm. Only derivatives through the fixed total order s are
bounded; no uniform higher-derivative or analytic-radius assumption occurs.

The oracle gives exact initial point values only. All acquisitions,
including preprocessing and repeats, are charged. Rules may depend
measurably on the transcript and an input-independent seed; stopping is
adaptive and almost surely finite on each input. Bias and unbounded real
outputs are allowed. The finite-time mean, heat convolution, energy,
and hard-prior analysis are proof devices, not supplied observations.

## 2. Actual flow, differentiability, and the marked L1 estimate

T82 Section 2 supplies the required finite-time argument without importing
an infinite-time graph or phase theorem.

The cubic is locally Lipschitz on C(X), so its mild equation has a unique
local trajectory. Before any possible escape, the difference from either
stationary solution +1 or -1 solves a linear parabolic equation with a
bounded real potential. A sufficiently negative scalar shift gives a
positive Volterra iteration and hence comparison. This proves preservation
of [-1,1] and allows global continuation. There is no circular use of
the later special potential bound to obtain this invariant interval.
The hard inputs are smooth, so the subsequent energy identities and
spatial integrations concern ordinary smooth solutions.

On C([0,1];C(X)), the mild-equation map is a smooth polynomial map in
the trajectory. Its trajectory derivative is I+V_u, with

    V_u z(t)=integral_0^t e^(t-r) P_(t-r)[3u(r)^2 z(r)] dr.

Since |u|<=1, the n-fold iterate has norm at most (3e)^n/n!.
Thus the Neumann series for (I+V_u)^(-1) converges in operator norm,
even without ||V_u||<1. The Banach-space implicit function theorem
therefore gives C-infinity dependence on the initial datum throughout
the open unit ball. Evaluation at a fixed time is bounded and linear.
Every derivative used below is a genuine derivative of the actual flow.

For the first variational propagator, the potential 1-3u^2 lies in
[-2,1]. Shifting by -2 leaves the nonnegative coefficient 3-3u^2;
factorially convergent Volterra iteration proves positivity. Its
coefficient-+1 representation then gives

    |E_u(t,r)h|<=e^(t-r) P_(t-r)|h|.

This proves both the L1 and sup estimates because heat preserves Haar
mass and is a sup contraction. It holds for signed continuous h.
Inhomogeneous variation of constants is justified by the same
finite-time absolute bounds and Fubini.

The differentiated cubic has coefficients -6u at order two and -6
at order three, with exactly three order-two/order-one pairings.
In each disjoint-label product, exactly one factor contains the marked
input. Bound that factor in L1 and every other factor in sup norm.
The resulting estimates are

    c1(t)=e^t,
    c2(t)=6t e^(2t),
    c3(t)=(6t+54t^2)e^(3t).

For c2 the integrand is at most 6e^(t+r). For c3 the ternary term
and the three paired terms together are at most

    (6+108r)e^(t+2r).

Bounding the exponential by e^(3t) and integrating gives the stated
c3. The marked norm remains ||h3||1 in every pairing, including those
where h3 is inside the second variation. No density supremum near
time zero and no conversion of the marked direction to its sup norm
is used. The corresponding all-sup estimates have the same constants.

Consequently A1(v)=e^(-1) Pi S_1v has

    |D^3 A1(v)[h1,h2,h3]|
      <=60e^2 ||h1||inf ||h2||inf ||h3||1.

Thus B=60e^2 is valid for all kappa>0. Oddness of the actual equation
gives oddness of A1 and F=A1-Pi. At zero, DS_1(0)=eP_1 and heat
preserves mass, so DF(0)=0; oddness gives D^2F(0)=0. Applying the
one-variable integral Taylor formula to r -> DF(rv)[h] proves

    DF(v)[h]=integral_0^1(1-r)D^3A1(rv)[v,v,h] dr,
    |DF(v)[h]|<=(B/2)||v||inf^2||h||1.

All joining segments later used lie strictly inside this differentiable
domain. In particular A1 is only a rescaled time-one mean; no phase
identity is required.

## 3. Hard inputs and the all-real-horizon scale

The fixed nonnegative compactly supported interior bump has 0<I<=1.
With Dpsi and a=1/(8Dpsi) as in T82, disjoint support gives, for every
sign configuration,

    ||v_xi||inf<=A=a k^(-s)<=1/8,
    ||partial^alpha v_xi||inf
      <=aDpsi k^(|alpha|-s)<=1/8,   |alpha|<=s.

Compact support makes the zero extension smooth across all cell
boundaries and periodic boundaries. On both selected layers the sign
counts are positive, and the bump is positive somewhere. Thus all prior
members have both strict signs, including every later exceptional member.
The auxiliary analytic function on the entire sign cube is legitimate;
the proof does not require an oracle guarantee on any auxiliary input
outside the promised class.

Even k makes K=k^d even. For K>=2048,

    ell=2 ceil(sqrt(K)/2)
    sqrt(K)<=ell<=sqrt(K)+2<=2sqrt(K)<=K/4.

Hence both layer counts (K+ell)/2 and (K-ell)/2 are integers, and the
mean on the positive layer is exactly m=AI ell/K.

For q=s+d/2 and the displayed even-grid floor, R_T>=4 implies
R_T/2<=k<=R_T. Direct substitution gives

    e^T m=(R_T/k)^q ell/sqrt(K),
    1<=e^T m<=2^(q+1),
    A/sqrt(K)<=2^q I^(-1)e^(-T).

Also log K<=d log R_T<=dT/q, because aI<1. These estimates hold
between grid jumps. The final lower constant follows from these exact
floor bounds, without an asymptotic equivalence or subsequence argument.

## 4. Full-layer coupling, variance, and exponential concentration

For any function on the whole sign cube with one-flip sensitivity L,
a swap has sensitivity at most 2L. Oddness under global reversal makes
its balanced-layer mean zero, without any spatial permutation symmetry.

Starting with a uniform K/2-subset of positive positions and adding a
uniform ell/2-subset of its complement gives the uniform (K+ell)/2
positive set. Every final set has the same number of predecessor sets,
and every predecessor/addition pair has equal probability. The path has
ell/2 flips, proving |E_piell f|<=ell L/2. Reversal handles the other layer.

In a reveal martingale, fix a possible prefix with both next signs
possible. The positive suffix set has sizes r and r+1 in the two cases.
Starting with a uniform r-subset and adding a uniform complement point
gives a uniform (r+1)-subset: the probability of each larger subset is

    (r+1)/[choose(N,r)(N-r)]=1/choose(N,r+1).

The two complete configurations differ by one swap. Thus the two next
conditional means differ by at most 2L. This includes r=0 and r=N-1;
when the next sign is forced the martingale increment is zero.

Conditionally, the increment is centered and lies in an interval of
length at most 2L. Its variance is at most p(1-p)(2L)^2<=L^2.
Orthogonality of finite martingale increments therefore gives
Var(f)<=KL^2.

The exponential bound also uses the conditional range, not a false
absolute-increment bound L. For a centered interval-supported Z, the
second derivative of log E e^(theta Z) is the variance under the
exponentially tilted finite law. That variance is bounded by L^2,
since distance from the interval midpoint is at most L. The value
and first derivative at zero vanish. Twice integrating proves

    E e^(theta Z)<=e^(theta^2 L^2/2)

for both signs of theta. This remains true for a deterministic increment.
Iterating conditional expectations yields the MGF with KL^2 in place
of L^2, and exponential Markov optimization gives exactly

    P(|f-Ef|>z)<=2 exp(-z^2/(2KL^2)).

All distributions in this argument are the full uniform fixed-cardinality
layers. Neither independent signs nor a PDE-good conditional law has
entered.

## 5. The time-one mean good event

A one-flip segment changes the initial datum in L1 by exactly 2AI/K
and stays in the sup ball of radius A. The derivative estimate gives

    |Delta F|<=B I A^3/K<=B A^3/K.

The full-layer mean and variance bounds therefore imply

    |E F|/m<=B A^2/(2I),
    Var(F)<=B^2 A^6/K.

The condition A^2<=I/(64B) makes the first ratio at most 1/128.
On |F|>m/4 the centered deviation is greater than m/8, so Chebyshev
and ell^2>=K give

    P(|F|>m/4)
      <=64B^2 A^4 K/(I^2 ell^2)
      <=64B^2 A^4/I^2<=1/64.

The negative layer has the same bound. On the positive good event,
the actual time-one mean b1=e(m+F) is at least 3em/4; on the negative
good event it is at most -3em/4. The use of the weaker sensitivity
constant after dropping I is consistent with every subsequent constant.

## 6. The whole time-one profile and the dimension-dependent net

For lambda=2*pi^2*kappa>0, the torus Fourier series gives

    ||p_1||inf<=sum_(n in Z^d)e^(-lambda|n|^2)
      <=rho=((1+e^(-lambda))/(1-e^(-lambda)))^d.

Normalized volume gives ||p_1||2<=rho. The first variation and the
one-flip L1 norm therefore bound each pointwise sensitivity by
Ccell A/K, where Ccell=2e rho. Oddness and the balanced-layer coupling
give |E S_1v(x)|<=Ccell A/sqrt(K). The slice MGF then gives the
claimed pointwise tail with denominator 2Ccell^2 A^2/K.

For the periodized Gaussian, the triangle inequality followed by
integration over a fundamental domain gives

    integral_X |grad p_t|
      <=integral_(R^d)|grad g_(kappa t)|
      <=sqrt(d/kappa)t^(-1/2).

The last inequality is the Gaussian first absolute moment bound by its
second moment. The positive-time Gaussian derivative series is absolutely
convergent. Applying this estimate to the mild equation with source
u-u^3, and using |u-u^3|<=|u| and ||S_rv||inf<=e^r A, proves

    ||grad S_1v||inf
      <=sqrt(d/kappa)A(1+2e)=Gkappa A.

Differentiation under the time integral is valid after truncating away
from r=1 and taking the limit under the integrable (1-r)^(-1/2)
majorant. This estimate has no hidden k-dependent derivative factor.

For N_K=ceil(sqrt(d)Gkappa sqrt(K)), nearest-grid distance on the
torus is at most sqrt(d)/(2N_K), including when N_K=1. Therefore the
pointwise interpolation error is at most A/(2sqrt(K)). Moreover

    M_K=N_K^d
      <=(1+sqrt(d)Gkappa)^d K^(d/2)=Cnet K^(d/2).

The net dimension is thus d/2 in its power of K, as used in T82;
no dimension-free covering estimate is being assumed. At each grid
point the specified deviation

    Ccell A/sqrt(K) sqrt(2log(128M_K))

has tail at most 1/(64M_K). The union bound and deterministic spatial
interpolation give failure probability at most 1/64 for the displayed
sup-norm bound.

For K>=2, log(128M_K)<=beta log K with the stated beta. The constant
H absorbs the constant terms by sqrt(log K)>=sqrt(log 2), and
C0=(2^q H/I)sqrt(d/q) follows from the bounds in Section 3. Thus

    ||S_1v||inf<=C0 e^(-T)sqrt(T)

outside a full-layer event of probability at most 1/64.
Orthogonal projection in normalized L2 gives the same bound for
W1=||Q S_1v||2. No independence between the mean and profile events
is required: their union has probability at most 1/32 in each layer.
The prior is still the original full layer.

## 7. Actual propagation when lambda may be at most one

Set u(t)=S_(1+t)v, b=Pi u, and w=u-b. For these smooth bounded
solutions, centering, integration by parts, and Pi w=0 give

    (1/2)d||w||2^2/dt
      =-(kappa/2)||grad u||2^2+||w||2^2
        -integral (u-b)(u^3-b^3).

The last integrand is nonnegative pointwise. The unit-torus Poincare
constant is 4*pi^2, so Gronwall gives

    ||w(t)||2<=e^((1-lambda)t)W1.

This estimate permits growth for lambda<1; the proof never changes it
to a decay statement.

The exact mean equation is

    b'=b-b^3-R,
    R=3b Pi(w^2)+Pi(w^3),
    |R|<=5||w||2^2,

using |b|<=1 and |w|<=2. The scalar solution z=phi_t(b1) lies in
[-1,1]. Its difference from b has coefficient
1-(b^2+bz+z^2)<=1, since the quadratic form is nonnegative.
The integrating-factor estimate consequently gives

    |b(t)-phi_t(b1)|
      <=5 e^t W1^2 integral_0^t e^((1-2lambda)r) dr.

This is a one-sided coefficient estimate, not an absolute Lipschitz
constant one for the cubic. At t=T-1 the profile good event yields
the prefactor 5C0^2 T e^(-T-1). Bounding the integral by
T exp(max(0,1-2lambda)T) proves

    Emean(T)=5C0^2 T^2 e^(-mu T),    mu=min(1,2lambda)>0.

At lambda=1/2 the integral is exactly T-1, so there is no missing
resonant denominator. For smaller lambda the exponent is 2lambda;
for larger lambda it is one. Each fixed positive lambda gives decay.

The pointwise estimate compares, during the last time unit, u(a+h)
with the spatially constant solution phi_h(b(a)), where a=t-1>=0.
Their difference has potential
1-(u^2+u c+c^2)<=1, bounded below as both solutions stay in [-1,1].
The same actual positive-propagator argument gives

    ||u(t)-phi_1(b(a))||inf
      <=e ||P_1(|w(a)|)||inf
      <=e rho ||w(a)||2.

Subtracting the spatial mean costs at most a factor two; it does not
assume positivity of Q. Therefore

    ||w(t)||inf<=2e rho e^((1-lambda)(t-1))W1.

At t=T-1, the exponential is
e^((1-lambda)(T-2)-T)=e^(2(lambda-1))e^(-lambda T).
This verifies exactly

    Cw=2e rho C0 e^(2(lambda-1)),
    Espace(T)=Cw sqrt(T)e^(-lambda T).

Combining the two estimates proves T82 (6.8) for every spatial point.
The small initial fluctuation W1=O(e^(-T)sqrt(T)) is doing the work
when a nonconstant linear mode is unstable. The proof makes no global
synchronization assertion about arbitrary inputs in that regime.

## 8. Explicit thresholds and actual target separation

An integer k_* satisfying T82 (7.1) exists because s>=1. The threshold
Tgrid=q log(2k_*)-log(aI) makes R_T>=2k_* and k>=k_* for every real
T>=Tgrid. It simultaneously enforces the derivative, parity, layer,
amplitude, and K>=2048 requirements already checked.

The claimed error-envelope constants follow directly from

    e^(mu T/2)>=(mu T/2)^2/2,
    e^(lambda T)>=lambda T.

They give

    Emean(T)<=40C0^2 mu^(-2)e^(-mu T/2),
    Espace(T)<=Cw lambda^(-1/2)e^(-lambda T/2).

Multiplying their prefactors by 64 gives exactly 2560C0^2/mu^2
and 64Cw/sqrt(lambda). Thus Tmean and Tspace in T82 (7.2) each
make its error at most 1/64. If a logarithm is nonpositive, its
prefactor is already at most 1/64 and the use of max(0,log(...))
is valid. T0>=2 supplies the last full time unit.

On the positive joint good event,

    e^(T-1)b1>=3/4.

For nonnegative c, the exact formula for phi_t(c) has denominator
sqrt(1+e^(2t)c^2-c^2)<=sqrt(1+e^(2t)c^2). Hence
phi_t(c)>=Psi(e^t c), and monotonicity of Psi gives

    S_Tv(x*)>=Psi(3/4)-1/32
      =3/5-1/32=91/160>1/2.

Oddness or the corresponding negative inequalities give the negative
bound -91/160. Both are actual PDE values, and both bad probabilities
are at most 1/32 under their full layers.

## 9. Exact-value information and arbitrary measurable adaptive rules

Threshold the estimator at zero with either fixed convention for a zero
output. On a good input, a wrong layer sign requires absolute estimation
error greater than 1/2. Markov and the MSE premise give sign error at most
1/4. On each bad input use the bound one. With the unconditioned equal
mixture of full layers, the resulting Bayes error is at most

    1/4+1/32=9/32.

This is a valid loose upper bound. In particular the proof does not
condition away the configurations for which the PDE estimate failed.

Giving the sign of the half-open cell containing each query strengthens
the original oracle. For that cell and point, the exact value is the
known scalar xi_j A psi(kx-j), including zero values and boundary points.
One query cannot reveal signs from several cells. Repeated cells reveal
no additional sign, but every original query remains charged.

Cap the original procedure at n=floor(K/1024) original acquisitions.
Fix the seed, simulate this procedure with the stronger oracle, and
record each newly revealed cell once. If it halts or reaches the cap,
pad to n distinct reveals by a fixed rule among unused cells.
Each next unused index is determined by the seed and already revealed
signs: between reveals the original values, repeated queries, stopping,
and output can be reconstructed. The capped decision is consequently
a common measurable function of the seed and the padded sign word.

Conditional on a fixed seed and a revealed prefix, the remaining signs
are uniform with the prescribed remaining counts. This holds because
the chosen indices were functions of information already revealed.
There is no additional constraint on unseen signs from the adaptive
index choice itself. If j signs with z positives have been seen, the
next probabilities are exactly

    p_plus=((K+ell)/2-z)/(K-j),
    p_minus=((K-ell)/2-z)/(K-j).

Every length-n sign word is possible under both layers: the smaller
positive or negative count is at least 3K/8>n. For j<n, the looser
bounds j<=K/8 and ell<=K/4 imply

    1/4<=p_minus<=4/7<3/4,
    |p_plus-p_minus|=ell/(K-j)<=2ell/K.

The logarithmic inequality log x<=x-1 gives

    KL(Ber(p)||Ber(q))<=(p-q)^2/[q(1-q)].

Here q(1-q)>=3/16. Thus one-step KL is at most
64ell^2/(3K^2)<=256/(3K), and the finite chain rule gives at most
n*256/(3K)<=1/12.

The seed treatment is valid even without relying on an unproved
regular-conditional-probability construction for a general seed space.
For each fixed seed, the finite input prior and the preceding inductive
reveal calculation explicitly give the same urn word law U_plus or
U_minus. Its probabilities depend only on sign counts, not on the
seed or chosen unused labels. Consequently, after removal of null
seeds, the augmented laws are the products mu_seed times U_plus and
mu_seed times U_minus. Their likelihood ratio depends only on the
finite word, so their KL is the same finite KL just bounded.
This product observation does not make the signs within the word
independent; their law remains sampling without replacement.

For completeness, Pinsker can be reduced here to the finite word laws.
Let A be the set on which the first mass function exceeds the second.
The log-sum inequality gives KL(P||Q)>=kl(P(A)||Q(A)).
For fixed q, the second derivative in p of kl(p||q) is
1/[p(1-p)]>=4, with value and first derivative zero at p=q.
Thus kl(p||q)>=2(p-q)^2, including endpoints by continuity.
Since P(A)-Q(A)=TV(P,Q), this proves TV<=sqrt(KL/2).
The common seed does not change TV, and measurable postprocessing
cannot increase it. Hence every capped decision has equal-prior error

    >=(1-TV)/2
    >=(1-sqrt(1/24))/2>3/8.

This establishes the information bound for the exact spatial oracle;
no independent noisy-coin oracle has been substituted.

## 10. Random stopping, constants, and evidence boundary

Let qbar be the full-prior average expected original query count.
If it is infinite, the lower bound is immediate. Otherwise truncate
the original sign decision before acquisition n+1 and choose a fixed
label there. The decision changes only on Q>n, with probability
at most qbar/n. Comparing its upper and lower errors gives

    3/8<=9/32+qbar/n,
    qbar>=3n/32.

For K>=2048, floor(K/1024)>=K/2048. Therefore

    qbar>=3K/65536
      >=3*2^(-d-16)*(aI)^(d/q)e^(dT/q).

The identity d/q=2d/(2s+d) verifies the final exponent. A finite-prior
average is bounded above by the worst-input expected count, giving the
claimed quantifiers. A separate work model charging at least one unit
per original query inherits this lower bound only; no work upper bound
is proved by T82.

At each fixed T there are finitely many prior inputs. The union of
their exceptional seed null sets for halting is still null, and can
be removed simultaneously. Truncation and padding have measurable
rules; the finite transcript simulation just described also supplies
a measurable reconstruction. Rare expensive runs and stopping
correlated with observations are allowed. Bias and unbounded real
outputs cause no problem because only MSE and the bounded sign
decision are used.

No assumption inside this proof needs lambda>1. The constants rho,
Gkappa, C0, Cw and the logarithmic thresholds are finite for every
fixed kappa>0 but need not be uniform as kappa tends to zero.
At kappa=0, one exact query v(x*) and the scalar formula determine
the target exactly, so that endpoint is properly excluded.

**Required repairs: none.** Root correspondence and any acceptance
or ledger promotion remain separate. This PASS does not extend a
matching upper theorem, certify full formal correspondence, establish
practical runtime or bit complexity, or assert novelty.

## 11. Source and command inspection record

Paths below are relative to the dynamic-continuation run. Hashes were
computed from the actual local files. The stated line windows are
the mathematical inspection scope, not a claim that every background
file was read in full.

| Source | Inspection scope | SHA256 |
| --- | --- | --- |
| reviews/T82-all-diffusion-prior-lower-proof.md | All 698 lines, in three contiguous windows | 0b331397bbda06ba02381009ce95bfd7656aabb4bd196bac5e67a616b3a2320a |
| reviews/T61-all-dimension-lower-proof.md | Lines 382-614, Sections 6-10 | 404a237be72991ac60efb97c48b5ba2347384b0a30ffe3a98219a74d1604d691 |
| reviews/T64-all-dimension-lower-independent-audit.md | Lines 1-180 and 297-491 | 07723a9f4fa3a6725b51431e773bc85a4ff8800ea5ac751cb66dd4b7eb24b8dc |
| reviews/T78-local-graph-weighted-L1-proof.md | Lines 319-416, finite-time Section 6 | e9613938316379c257fcaaf2cdc5bbbdfa19c01945a22d647a4e62d75b771a53 |
| reviews/R14c-natural-gap-graph-burnin-proof.md | Lines 119-164, last-unit Section 4 | 89a144617890314a47cbe1f7279053b9ea82c60dd670609739715a2a1ff2abbd |
| 04u-all-dimension-signed-query-lower-bound.md | All 171 lines, exact class and accepted template | 6587b4ba1b30a904bb6b336d8ca22917baad12f7db26627ca313aef632d94117 |
| 04o-unstable-phase-query-lower-bound.md | Lines 1-125, especially exact oracle and seed interface | 67d6463087775a857a2ffc035fa6ef7fa31db47b4c99b496ecdcc9e8f87fd765 |

The T61/T64 infinite-time phase arguments are not dependencies of this
verdict. Their finite-prior template was checked, while T82's actual
finite-time estimates and arbitrary-positive-gap propagation were
recomputed above. The stable-graph portions of T78 and R14c were not
imported.

The math-auto-research skill, defaults, model routing, execution guidance,
and general reader profile were read. Requested dispatch is
gpt-6-astra/max, as checked in run.json lines 714-721; the actual serving
backend is not independently exposed beyond that dispatch configuration.
No model setting or run-state file was changed.

Executed tools were read-only shell source/status/hash inspections
(cat, rg, sed, wc, shasum, git status), the clock, collaboration status
messages, and patches confined to this audit. The README, research
index, and 08-next checkpoint were inspected as orientation; one combined
orientation output was truncated and is not claimed as a full read.
Searches of the claim ledger/registry and the Lean toolchain were limited
orientation checks. The toolchain file reports leanprover/lean4:v4.33.0;
no Lean command was run.

Two read-only path lookups reported absent paths: the repository-root
AGENTS.md (the task supplied its instructions directly), and a guessed
04o filename. The actual 04o path was then resolved from 04u and read
as recorded above. One no-match T83 filename search merely confirmed
that the assigned report had not yet been created. These produced no
mathematical evidence or source mutation.

No numerical PDE execution, random sampling, initial-data acquisition,
experiment rerun, Lean build, external literature search, or new formal
certificate was performed. No existing file was edited by T83.
After the audit was written, all seven mathematical-source hashes above
were rechecked and still matched their inspected snapshots.
The final audit hash is reported outside this file after its final write,
avoiding a self-referential hash.
