# T100: independent audit of sparse Fourier derivative-field sampling

Date: 2026-09-29. Conventional mathematical audit. This task owns only
this file; task ID T99 remains reserved for the separate E5 implementation.

**Verdict: PASS. Required mathematical repairs: none.** R23 constructs an
actual unbiased sparse-frequency derivative sampler with a second-moment
bound independent of the Fourier cutoff. Its finite averaging program has
the claimed expected work `C[M(1+G)+K]` and all-seed query cap `jM` in the
inherited ideal real-operation model. This is a subroutine improvement,
with a changed sample law and potentially larger variance constant.

The proof does not establish exact total-work Theta order, a practical
speedup, finite-bit complexity, or novelty. No numerical, code, Lean, or
unknown-input execution was performed. Acceptance by root is separate.

## 1. Frozen source and exact statement

The complete 208-line target is
`reviews/R23-sparse-frequency-field-candidate.md`, SHA256

    352f4e8d4ac334f0a570300313773b19b5263500b29ee0e601ce4a7737ee45e0

Its three input locks were checked directly against the actual files:

| Source relative to this run | Verified SHA256 |
| --- | --- |
| `04aa-polynomial-fields-and-linear-gaussian-preparation.md` | `433c699d951c74fa6ba19166e159069130e1340a7a319aa0334b0ba4f8a1b8a1` |
| `reviews/R20b-continuous-domain-addendum.md` | `6c5e8b158ca269588c4200ca09c82f4ffa430e8aa0146a52022370ade352e527` |
| `reviews/R21-linear-tree-common-gaussian-candidate.md` | `99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461` |

All three texts were read in full for T100. The original R20 bounded
polynomial/derivative proof was also read in full in this worker's preceding
T96 task; the relevant law is stated explicitly below. No T94 or T95
extension, pending formal source, numerical artifact, or acceptance label
alone supplies a missing mathematical step.

Fix a dimension `d>=1`, `kappa,tau>0`, a fixed real polynomial with inward
endpoint signs, and derivative order `j>=1`. The known base `g` is real and
continuous, `||g||inf<1`, with an actual evaluator costing at most `G`.
The unknown `v` and direction `e=v-g` are continuous. No bound on `v` is
needed for this derivative statement. A Taylor application would separately
need its segment in the open unit ball, as specified in R20b.

The finite-array statement uses a nonnegative integer box cutoff `N` and
a positive integer number `M` of trials, as the box indexing and trial
count notation require. Put

    r=d+1,       R=r+d=2d+1,       K=(2N+1)^d.

The claimed mean is the projection of the actual PDE derivative, not a
new solution operator. The risk is actual mean-square error in `H^r`.
Every scalar acquisition of `v`, including repeated locations, is charged.
The ideal model includes exact elementary functions and random draws,
floor/comparison/arithmetic, and ideal finite integer/address words.
Transforms, coefficient oracles and arbitrary function evaluators are not
additional primitives.

## 2. Actual inherited field and the higher Sobolev envelope

The D43 bounded parent rule has fixed arity `B>=2` and fixed branching
rate `lambda`. Its actual first-split identity has reaction `f`; bounded
mild uniqueness identifies the tree expectation with the actual PDE.
The D44 tree recursion uses independent edge Gaussians, guarded harmonic
weights and the root aggregate. Conditional on the genealogy, subtracting
that aggregate gives the residual array independent of the complete common
Gaussian vector. Its removable variance satisfies `tau/n<=a<=tau`.

The common Gaussian is integrated through the complete translated nonlinear
leaf polynomial and its selected partials. Accordingly all leaf evaluations
use the same locations `U+Z_i`, with uniform torus point `U`. This gives

    W=z h_(kappa a)(.-U),
    z=(n)_j C_I product_b e(U+Z_(I_b)),
    E W=D^j S_tau(g)[e,...,e].

The distinct-label partial obeys `|C_I|<=1`, so
`|z|<=n^j||e||inf^j`. For `n<j`, the field is zero and no acquisition
is made. Tree and known-coefficient preparation precede the at most `j`
unknown acquisitions. These are the actual coupled D43/D44 variables;
the source does not keep an old residual law while changing heat weights.

For any fixed positive integer `R`, let `theta=4pi^2 kappa tau`.
By `a>=tau/n`, the squared heat norm is bounded by

    sum_nu (1+|nu|^2)^R exp(-theta |nu|^2/n).

The decreasing Gaussian sum gives

    sum_(m in Z) exp(-theta m^2/n)
       <=1+sqrt(pi n/theta)<=b0 sqrt(n).

Writing `x=theta m^2/n`, the bound
`x^R exp(-x/2)<=(2R)^R` proves the weighted scalar estimate in R23.
Its remaining sum is at most `b1 sqrt(n)`, with the displayed `b1`.
Finally the convex power inequality bounds the spatial weight by
`(d+1)^(R-1)(1+sum_l |nu_l|^(2R))`. Factoring the nonnegative sums
gives the sharper intermediate bound

    ||h_(kappa a)||_(H^R)^2<=H_R n^(R+d/2),

with exactly R23's

    H_R=(d+1)^(R-1)[b0^d+d*(2R/theta)^R*b1*b0^(d-1)].

Since `n>=1`, replacing the exponent by `R+d` is valid. Multiplication
by the pathwise bound for `z^2` and the actual population moment of order
`2j+R+d` then prove (2.1), with the exact displayed `V_(j,R)`.
Only a fixed integer population moment is used; no exponential moment,
new regularity of `e`, or uniformity in the fixed parameters is assumed.

This also gives a genuine `H^R` random element. On each finite-tree
stratum, its scalar coefficient and variance are Borel finite formulas,
and translation of the positive-variance heat profile is continuous in
`H^R`. The countable union of such strata is strongly measurable in the
separable Hilbert space; the moment bound supplies square integrability.
The continuous embedding into `H^r` commutes with the Bochner integral,
so its mean is the same actual derivative already identified by D43/D44.

## 3. Exact lattice law, zero mode, endpoints, and tails

For `U0` uniform on `(0,1)`, the event
`floor(1/U0)-1=m` is

    1/(m+2)<U0<=1/(m+1),       m=0,1,2,... .

Its probability is `1/[(m+1)(m+2)]`. The event `m=0` has probability
one half. For `m>=1`, the independent fair sign splits its mass equally,
giving exactly

    q1(0)=1/2,
    q1(k)=1/[2(|k|+1)(|k|+2)]       for k!=0.

Telescoping proves normalization:

    1/2+sum_(m>=1) 1/[(m+1)(m+2)]=1.

Replacing a uniform endpoint by `1/2` before division changes only a null
set. It makes every endpoint path finite and does not introduce retries.
At every non-endpoint path `1/U0` and its floor are finite. A fair sign can
be produced by one independent uniform draw and a comparison with `1/2`.
Any convention at its null boundary gives the same law.

There are only a fixed number of charged operations per coordinate. In
particular, the program does not iterate up to the sampled magnitude or
allocate an array of that length. This matters: the absolute coordinate
has tail `P(m>=L)=1/(L+1)` for integers `L>=1` and infinite mean. Its
unbounded but finite realized index is allowed by the ideal-word model;
a bounded machine-word or bit-cost claim would require a different analysis.

Independent coordinate draws give the positive symmetric product law
`q(nu)`. Its mass at zero is `q(0)=2^(-d)`. The one-coordinate box mass
and full box mass are, explicitly,

    P(|nu_l|<=N)=(N+1)/(N+2),
    P(|nu|inf<=N)=((N+1)/(N+2))^d.

Thus every finite box has a positive outside probability, and `N=0`
is a valid case rather than a limiting argument.

For integer `m>=1`,

    6(1+m^2)-2(m+1)(m+2)=2(2m-1)(m-1)>=0.

At zero the reciprocal probability is two, at most six. Multiplication
over coordinates proves the exact reciprocal bound (3.1), since each
`1+nu_l^2<=1+|nu|^2`. Evaluating `q` uses fixed-dimensional rational
arithmetic and comparisons; its denominator is positive everywhere.

## 4. Real conjugate pairs and exact normalization

Use the Fourier convention
`w_hat(nu)=integral w(x)exp(-2pi i nu.x) dx`. For a real field,
`w_hat(-nu)=conj(w_hat(nu))`. For a nonzero representative `nu_star`,
write `w_hat(nu_star)=alpha+i beta`. Then

    Re[w_hat(nu_star)exp(2pi i nu_star.x)]
       =alpha cos(2pi nu_star.x)-beta sin(2pi nu_star.x).

The negative-frequency expression is exactly the same real function.
Consequently drawing either member of a pair in (4.1) gives one copy
of this function divided by `q(nu_star)`. Summing its two probabilities
in expectation gives twice the function, which is precisely the pair's
contribution to the real Fourier series. The zero draw contributes
`w_hat(0)/q(0)` once, with probability `q(0)`.

There must be no factor two in a single nonzero sparse draw. For a direct
normalization check, take `w(x)=cos(2pi nu_star.x)`: each of its two
nonzero coefficients is `1/2`, so the two possible draws together have
mean exactly `w`. Inserting an additional factor two would give `2w`.

For the actual field,

    W_hat(nu)=z exp(-2pi^2 kappa a|nu|^2)exp(-2pi i nu.U).

Thus at the chosen positive representative its imaginary part has the
negative sine sign, and the real sine coefficient in the preceding
formula has the positive sign. Both original draws `nu_star` and
`-nu_star` give exactly R23 (4.4) when stored at the canonical pair.
The constant coefficient is `z/q(0)`. Nothing in this calculation
breaks the correlations between `z,a,U` or the leaf locations.

## 5. Actual Bochner means and cutoff-independent second moments

The real `H^r` norm assigns one half of the frequency weight to each
cosine and sine square. Therefore, for `nu!=0`,

    ||A_nu(w)||_(H^r)^2
       =(1+|nu|^2)^r |w_hat(nu)|^2/[2q(nu)^2].

For the zero mode it is `|w_hat(0)|^2/q(0)^2`. Averaging against the
independent frequency distribution, retaining the actual one-half
factor or simply bounding it by one, gives

    E_nu||Y_N||_(H^r)^2
       <=sum_nu (1+|nu|^2)^r |w_hat(nu)|^2/q(nu)
       <=6^d ||w||_(H^(r+d))^2.

This is exactly why `R=r+d=2d+1` is sufficient. The second inequality
uses the proved reciprocal-probability bound; its constant does not
depend on `N`. Taking the actual field expectation with nonnegative
Tonelli proves the envelope `Vtilde_j=6^d V_(j,R)` in (4.3).

For each fixed frequency, coefficient evaluation is a continuous linear
functional and the resulting real mode is a continuous finite-rank map
from `H^R` into `H^r`. Splitting by the countable frequency outcomes
proves strong measurability. The finite second moment implies Bochner
integrability. Thus no scalar coefficientwise assertion is being used
as a substitute for a field-valued expectation.

For finite `N`, summing the frequency expectation has finitely many
nonzero terms and yields `P_N w` by the conjugate-pair calculation.
Bochner Fubini, or equivalently the independent product construction
with its integrable envelope, gives

    E Y_N=P_N E W=P_N D^j S_tau(g)[e,...,e].

For the untruncated field the same nonnegative second-moment estimate
holds. In particular, for each fixed `w`,
`sum_nu q(nu)||A_nu(w)||_(H^r)` is finite by Cauchy--Schwarz.
The Bochner sum therefore exists. Each of its Fourier coordinates is
the corresponding coordinate of `w`, and Fourier coordinates identify
the `H^r` element. A second use of integrability gives the untruncated
actual mean identity. No unjustified interchange of a conditionally
convergent Fourier series and expectation is needed.

## 6. Frequency-first zeros are part of the law

To verify the actual finite program, first imagine the independent
product experiment `(nu,W)`, with a complete D44 field even if it will
not be inspected. On an outside-box event the definition of `Y_N` is
identically zero, so omitting the unused tree and all unknown acquisitions
does not change the output law. On an inside-box event independence
leaves the conditional D44 law unchanged. This proves the frequency-first
implementation, including its work-saving early branch.

Every requested trial still counts in the denominator `M`, including
zeros. The program does not repeat until it sees an inside-box frequency.
That distinction is essential for its displayed importance weights.
For example, at `N=0`, repeating until the zero frequency and retaining
the original factor `1/q(0)` would multiply the intended mean by `2^d`.
The source's zero trials avoid that error.

Each inside-box trial then uses the original `n<j` zero branch and the
guarded D44 tree, residual, tuple and known-partial preparation. No new
unknown value is requested before that preparation completes. A null
nonterminating preparation therefore makes zero acquisitions, and all
completed paths request at most `j`. The outside branch requests none.
Both lattice endpoints and Gaussian zero variances have total guards.
Nonexplosion and finite arithmetic on every completed tree give
almost-sure halting for every continuous input.

Independent copies can be implemented with independent frequency and
tree seed tapes per trial. Skipping an unused tape does not introduce
dependence between trials. The proof does not assume that an uncontrolled
reuse of random state automatically preserves this property.

## 7. A concrete accumulation index and all paid operations

Frequency generation, the box test, computing the rational probability,
choosing the canonical representative, its squared norm and its dot
product with `U` all cost `O(d)` ideal operations. Computing the single
heat multiplier and cosine/sine pair uses the permitted elementary
primitives. The coefficient is obtained from `z,a,U`; no Fourier
coefficient or known-function oracle is introduced.

The inherited conditional tree work is `C(1+G)n`, including the fixed
tuple length, known-leaf evaluations, parent passes, scalar acquisitions
and memory accesses. The actual first moment is at most
`exp(lambda tau(B-1))`. Independence of the frequency and genealogy
therefore bounds expected work per trial by

    C[1+P(|nu|inf<=N)(1+G)E n]
       <=C[1+(1+G)E n]<=C'(1+G),

where the constants depend on the fixed model parameters, not `N` or `M`.
No loop whose cost grows with the magnitude of an out-of-box draw is
hidden in this bound.

Here is one explicit indexing implementation for the dense real output.
For `nu` in the box, let `idx(nu)` be its base-`2N+1` box index with
digits `nu_l+N`, evaluated by a fixed-dimensional Horner loop. Reserve
`idx(0)` for the constant. At each canonical nonzero representative
`nu_star`, store its cosine coefficient at `idx(nu_star)` and its sine
coefficient at `idx(-nu_star)`. These locations are distinct, and each
nonzero box index belongs to exactly one such pair. The resulting real
basis has exactly `1+2(K-1)/2=K` entries.
For `N=0` there is only the constant slot and the same Horner formula
returns index zero.

Initialize these `K` entries to zero once. A nonzero trial modifies
at most two of them; a zero-frequency trial modifies one; any zero
record modifies none. Index evaluation, reading, adding and writing
are constant-cost in fixed dimension. At the end compute `1/M` once,
scale each entry and serialize the finite labeled array, all in `O(K)`.
Labels can be enumerated by the same box loop with `O(d)` work per entry.
This supplies the exact meaning of the source's canonical pair convention
without a hidden search through the dense array on each trial.

Combining the preparation and accumulation gives

    E Work<=C[M(1+G)+K],
    queries<=jM on every seed.

The hard cap remains valid if one trial fails to terminate on a null
seed: preceding completed trials obey their caps and the unfinished
preparation adds no unbounded query sequence. Live storage is the dense
array, a single current finite tree with its linear-size work records,
and a fixed number of scalar/frequency registers. No `M` dense arrays
are stored or materialized. The unavoidable dense output cost `O(K)`
is explicitly retained.

## 8. Independent-copy risk and the actual variance limitation

For independent copies of the complete new sparse field, second-moment
integrability justifies expanding the Hilbert square and applying Fubini.
Cross-copy centered inner products have zero expectation. Consequently

    E||M^-1 sum_b Y_(N,b)-E Y_N||_(H^r)^2
       =M^-1 E||Y_N-E Y_N||_(H^r)^2
       <=Vtilde_j ||e||inf^(2j)/M.

The exact expression is the centered moment, whereas the displayed
`Vtilde_j` expression is an upper bound. This respects the R20b risk
repair. No independence of coordinates within one trial is assumed.

The source's warning that variance can increase is necessary even for
an actual D43/D44 instance. Take the inward polynomial `f=0`, `g=0`,
`v=1`, and `j=1`. The bounded parent construction may use the binary
average rule. Its terminal leaf weights are positive and sum to one.
For a uniform selected leaf the scalar is `z=n C_I>0`, and its
conditional mean given the tree is one; hence `E z=1` and `E z^2>0`.
At cutoff `N=0`, the ordinary dense projected field is the constant `z`.
The sparse field is the constant `2^d z` with probability `2^(-d)`
and zero otherwise; the zero-frequency indicator is independent of `z`.

Their means both equal one, but their variance difference is

    [2^d E z^2-1]-[E z^2-1]=(2^d-1)E z^2>0.

Their laws are also different: the sparse version has positive zero
mass, while the dense version is positive almost surely. This is a
counterexample to possible variance-dominance or unchanged-law claims,
not a defect in R23, which explicitly disclaims both. It also shows why
old sample counts cannot be reused at a fixed tolerance without checking
the new constants. The continuous direction `v=1` is permitted by the
repaired derivative domain; no Taylor segment hypothesis is needed here.

## 9. Scope, provenance, and final disposition

The improvement is precisely the dependence on `K` in this derivative
averaging subroutine: one sparse update per trial replaces the enumeration
of all `K` coefficients per trial. The actual higher-Sobolev envelope
allows a second-moment constant independent of `N`, at the expense of
larger fixed population moments and potentially much larger constants.

The same statistical interface can be used in a long-horizon proof after
changing its public error-budget constants. That does not remove the
paid construction of the known base profile or the later nonlinear
continuation solve. No exact total-work Theta order, improvement of the
accepted exponential rate, finite-parameter speed guarantee, fractional
solver, or variable-diffusion theorem follows. T95 is not used here.
The unbounded exact indices and exact random primitives are explicitly
idealizations; this audit proves no bounded-word or finite-bit guarantee.

The complete target and all three named frozen inputs were read and
hashed in this task. The preceding T96 source reads supplied additional
original-proofs context; no inaccessible history is claimed. The
math-auto-research skill, defaults, model-routing, execution instructions
and general profile had been read directly in that same worker context
and remain applicable. Root requested the inherited research configuration;
actual serving-backend and reasoning-effort telemetry are not independently
exposed here. A configured preference is not a backend attestation.

No external theorem or literature claim was needed as an additional
premise, and no external paper was opened during T100. Importance sampling,
Fourier coordinate randomization, Gaussian tree algebra and Hilbert sample
averaging are classical ingredients. This audit checks their stated
connection to the actual derivative field and counted scalar-query model;
it is not a worldwide priority or novelty review. R23's kernel-feature
attribution is not silently treated as a proof of the nonlinear field claim.

Only source/status/hash inspection and writing/readback of this audit were
performed. No numerical or symbolic experiment, sampler or solver code,
Lean build, or new unknown-input acquisition was executed. No frozen proof,
E4/E5 artifact, root claim/state file, implementation or formal source was
edited. The final audit hash is reported separately after readback.
The mathematical verdict is **PASS**, with **no required repairs**.
