# D32–D33: signed ideal-work bounds with matching exponential rate

Status: conventional mathematics accepted after frozen T69/T70,
independent T73/T74 and full root correspondence. The separate query
theorem D29 is preserved. This is an ideal operation-count theorem,
not a finite-bit algorithm, measured speedup or full Lean certificate.

## Exact class, output and cost model

Fix integers d,s>=1 and one point x* of the normalized unit torus X.
The equation and unknown class are exactly those of D28/D29:

    u_t=Delta u/2+u-u^3,  u(0)=v,
    V={v in C^infinity(X): ||v||infinity<=1/2,
       max_(|alpha|<=s)||partial^alpha v||infinity<=1,
       min v<0<max v}.

Every exact initial-value acquisition costs one unit, including repeats
and preprocessing. The common ideal model additionally charges each
real arithmetic operation, comparison, floor/ceiling, modular/integer
index operation and stored-value read/write. Evaluations of exp, log,
sin, cos and positive square root are elementary primitives. Exact
uniform, exponential waiting-time and Gaussian draws with known
parameters are random primitives; their scalar/vector operations are
counted. Public fixed constants are available. Random seeds are input
independent. These conventions are the union of the explicitly audited
Gate-A and Gate-B primitives, with no conflicting cost assignment.

There is no free evaluation of an arbitrary known function, transform,
PDE solution, phase, derivative, heat density or kernel variation norm.
The supplied known-profile evaluator below is an actual bounded-stencil
program whose operations are charged. Continuous random locations,
unbounded real magnitudes and integer/address bit lengths are idealized.
This theorem does not assign them finite-bit encodings at unit cost.

Let W(T) be the infimum of sup_(v in V) E Work_T(v) over Borel,
almost-surely halting algorithms in this model with

    sup_(v in V) E|output_T(v)-S_Tv(x*)|^2 <= 1/16.

Bias, adaptive queries, random stopping and unbounded outputs are allowed
in this comparison class. Constants below depend on fixed d,s and the
fixed analytic/model parameters. They are not dimension-uniform.

## D32: the paid base-value computation

Choose the public Gevrey-2 partition and fixed polynomial stencils from
T70/T74. They use exactly k^d paid grid values, produce g with

    ||g||infinity<=3/4,  ||v-g||infinity<=Cint k^(-s),

and require O(k^d) preprocessing/storage. Each later exact evaluation
of g costs O_(d,s)(1) listed ideal operations. Gevrey regularity is a
property of this chosen formula, not an extra promise about v.

Use the same fixed burn-in L and actual stable graph Theta as in T65,
and put H(q)=Pi S_Lq-Theta(QS_Lq). For T sufficiently large and
log k<=Klog(1+T), the algorithm computes its fixed-error coarse mean
test and, on the near branch, h0 with

    |h0-H(g)|<=eta,  eta=exp(-(T-L))/192,
    Work<=C k^d (1+T)^a.

It uses no additional unknown values. On the far branch it may return
the accepted sign output without h0, exactly as permitted in R12.
If unconditional h0 is required, T74 completion C1 runs the same root
routine there as well at unchanged asymptotic work. The combined
algorithm below uses the permitted early far return.

The central additional ingredient is the quantitative known-profile
solver in T70 Sections 3–7, independently completed in T74: a profile
with bounded Gevrey-2 norm at scale 1/kappa can be evolved for S and
approximated to exp(-P) in

    C kappa^d [1+P+S+log(kappa+1)]^a (1+Wq)

ideal operations, where Wq is its actual evaluation cost. This bound
counts the Fourier initialization, dealiased cubic, cutoff projection
loss, genuine stiff startup disk, graded analytic time panels, finite
collocation iterations and every scalar convolution weight. It neither
assumes a spectral maximum principle nor uses a PDE solve as a primitive.

After fixed burn-in, only O(T) modes per coordinate are retained. Their
coefficients have uniformly bounded absolute sum, and are stored in an
indexed Fourier array. Known graph-root trial profiles thus have
polynomial-in-T size and quantitative regularity. The graph root is
computed by bounded bisection with absolute phase-evaluation errors;
the exp(2tau) conditioning of the phase transform is explicitly paid
for. The total cost remains k^d times a polynomial in T, including
inputs exactly on the stable interface. T74 completions C2–C4 supply
explicit ellipse/error allocations and the indexed-array interface.

## The same g satisfies D31's sampler interface

D31/T69/T73 construct, for each fixed j>=1, a fresh-seed sample Z_j with

    E Z_j=D^jH(g)[e,...,e],  e=v-g,
    E|Z_j|^2<=V_j ||e||infinity^(2j),
    new_unknown_calls<=j on every seed path.

Here V_j is finite and uniform in g,k,T and distance to the stable
interface. The actual source/branch coefficients, their common child
states, independent unmarked burn-in batches and derivative label maps
are all included. The expected sample work is O(C_j(1+Gg)), where
Gg is the actual uniform cost of evaluating the supplied paid g.

D32 supplies precisely that g with constant Gg in the common model.
Its exp evaluations are charged elementary operations; they are distinct
from T69's exponential random clocks. No extra regularity or formula
oracle is introduced at this interface. All coarse data remain charged
once and all later saved-formula evaluations remain charged operations.

## D33: compose the algorithm and its error bounds

Set qrate=s+d/2, J=ceil(1+d/(2s)), m=J-1, and M=k^d. The accepted
analytic Taylor bound gives a remainder at most
B_J ||e||infinity^J/J!, and Js>=qrate.

For each j=1,...,m take M independent copies of the actual D31 sample,
conditional on the fixed coarse transcript, and return the proxy

    Hhat=h0+sum_(j=1)^m (1/j!) (1/M)sum_(ell=1)^M Z_(j,ell).

Finite second moments justify its means and variances. Independence
within each average, followed by Minkowski, gives

    RMS(Hhat-H(v))
      <=eta+sum_(j=1)^m sqrt(V_j) Cint^j k^(-js-d/2)/j!
             +B_J Cint^J k^(-Js)/J!
      <=eta+Cstar k^(-qrate),

where one may choose the positive fixed constant

    Cstar=1+sum_(j=1)^m sqrt(V_j) Cint^j/j!
              +B_J Cint^J/J!.

Choose k=max(k0,ceil((32 Cstar exp(T-L))^(1/qrate))). Increase the
fixed k0 for the chosen interpolation basis and T65's branch buffer.
Then log k=O(1+T), as required by D32, and

    exp(T-L) RMS(Hhat-H(v)) <=1/32+1/192<3/64.

The near-branch output is Psi(exp(T-L)Hhat), with
Psi(z)=z/sqrt(1+z^2). Its ideal elementary cost is constant. It is
well defined even for unbounded finite sample values. D29's actual PDE
remainder 1/32 and phase-multiplier error 1/64 apply to the same proxy
and paid branch test. Including the previously allowed scalar output
error 1/64 gives RMS<=7/64<1/4. Exact primitive evaluation needs no
such final rounding error but retaining that budget is harmless.
The far branch retains its deterministic error<=1/16.

The hard unknown-query cap is

    Q_T <= [1+sum_(j=1)^m j] k^d
         =[1+J(J-1)/2] k^d.

All Gate-A loops have public finite limits. Gate B is Borel and halts
almost surely, and only finitely many samples are requested. All its
tree and coefficient preparation precedes its at-most-j data calls,
so the hard cap also covers null nonterminating preparation paths.
The combined algorithm is admissible in the stated model.

## Work upper bound and the lower bound's quantifiers

D32's work is at most C k^d (1+T)^a. There are M samples at each of a
fixed finite number of orders, each with fixed expected cost after the
known-g interface is substituted. Linearity of expectation therefore
gives, uniformly in v,

    E Work_T(v)<=C k^d (1+T)^a
                  <=C exp(gamma T)(1+T)^a,
    gamma=2d/(2s+d).

Every algorithm in this ideal model is an admissible Borel value-query
algorithm for D28's lower bound, and Work_T>=Q_T pointwise. Hence for
positive finite constants c,C,a,T0 and every real T>=T0,

    c exp(gamma T) <= W(T) <= C exp(gamma T)(1+T)^a,
    lim_(T->infinity) log W(T)/T = gamma.

This matches the exponential rate, up to a polynomial factor in T.
It is not an exact Theta(exp(gamma T)) work theorem. The expensive
input in the lower bound may depend on T and the algorithm; no claim
is made that each fixed profile necessarily becomes expensive.

## Evidence and limits

The hash-bound root record is `reviews/T74-root-correspondence.json`.
It binds frozen T70 and its T74 independent audit, accepted D31's
T69/T73 sources, R12 and this synthesis. No frozen proof was rewritten.

The constants and polynomial exponent can be enormous. This theorem
does not demonstrate practical efficiency, superiority to a deterministic
PDE solver, finite-bit feasibility, or signed numerical performance.
T62/T72 certify selected actual information-theoretic ingredients;
T75 is implementing finite-depth moment laws. They do not formalize
this full theorem. E4 remains a separate nonnegative scalar-surrogate
experiment. No new oracle calls or numerical experiment support D33.

The domain and diffusion remain those stated above. R14/R14b are a
separate unaccepted route toward weaker diffusion; this theorem does
not import their proposed extension. Classical randomized integration,
control variates and spectral methods remain relevant predecessors.
Publication originality and significance are unresolved, and no prize
conclusion follows from these conventional proof/audit results.
