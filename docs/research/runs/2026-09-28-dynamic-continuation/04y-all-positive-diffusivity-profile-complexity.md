# All positive diffusivities: fixed-accuracy long-time complexity

Date: 2026-09-29. Accepted conventional synthesis after complete root
reading of T81/T82 and independent T84/T83, respectively. Neither audit
requires a material repair. This result extends the diffusion scope of
04w and strengthens its upper output to a whole spatial profile. It
does not overwrite those earlier frozen results.

## 1. Exact problem and conclusions

On the normalized unit torus X=(R/Z)^d consider the actual equation

    u_t=(kappa/2) Delta u+u-u^3,       u(0)=v.

Fix kappa>0, integers d,s>=1, and, for the point problem, x* in X.
The input class is the fixed full signed class

    V={v smooth periodic real: ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

Only total derivatives through s are uniformly controlled. There is no
common bound on all higher derivatives, no common analytic radius, no
positive lower bound on the initial mass, and no restriction to one
attraction basin. Let S_T^kappa v denote the actual solution.

The unknown input is accessed only through exact initial point values.
Each acquisition is charged, including repeats and preprocessing. Rules
may be measurable, randomized, adaptive, biased, and randomly stopped,
and must halt almost surely on each promised input. Point outputs may
be unbounded. Random seeds are independent of the input.

Put q=s+d/2 and gamma=d/q=2d/(2s+d).

**D37, information lower bound.** There are c>0 and T0<infinity such
that, for every real T>=T0, every point estimator with

    sup_(v in V) E|Y(v)-S_T^kappa v(x*)|^2<=1/16

satisfies sup_v E Q(v)>=c exp(gamma T). In fact the explicitly specified
finite prior in T82 has that average expected cost and is chosen before
the algorithm. An expensive member can depend on T and the algorithm;
one common hard input for all horizons is not asserted. This includes
every fixed kappa>0, irrespective of the number of unstable nonconstant
linear modes. T82/T83 prove this conventional theorem.

**D38, stronger profile upper bound.** There is an explicit algorithm
returning an indexed real Fourier polynomial U_T such that

    sup_(v in V) (E||U_T-S_T^kappa v||inf^2)^(1/2)<=1/8

for every prescribed T>=2. It uses the listed paid ideal primitives and
satisfies

    sup_v E Work <=C exp(gamma T)(1+T)^A,
    Q<=[1+J(J-1)/2]k^d on every seed,
    J=ceil(1+d/(2s)),
    k^d<=C exp(gamma T)(1+T)^(d^2/q).

All constants depend only on fixed public parameters. Its returned
array has at most C(1+T)^(3d^2+9d) entries. Evaluating it at any specified
point costs a polynomial number of paid operations and makes no further
unknown-input acquisitions. A deterministic bounded-time patch has
spatial sup error at most3/32 for 0<=T<=2. This patch also lies below1/8.
T81/T84 prove the construction; T84 Section10a independently checks the
whole-profile corollary.

The spatial supremum is inside the expectation. Thus D38 is stronger
than a collection of separate pointwise RMS statements. It is still a
separate algorithm at each prescribed horizon, not a simultaneous
infinite-time pathwise bound.

**D39, matching exponential rates.** Define Q_point(T) as the least
worst-input expected query count at uniform point MSE<=1/16. Define
Q_profile(T) with loss E||U-S_T^kappa v||inf^2<=1/16 and output a finite
explicitly indexed real Fourier polynomial. Arithmetic is free in these
query problems. Define W_point and W_profile using the same respective
loss/output contracts and the paid ideal model below. Then, for each of
these four quantities C_problem(T), there are positive constants c,C
and finite A such that for all large T,

    c exp(gamma T)<=C_problem(T)<=C exp(gamma T)(1+T)^A,
    lim_(T->infinity) log C_problem(T)/T=gamma.

For profile algorithms, evaluation at x* is a finite postprocessing
with no initial-value calls; the point lower bound therefore applies.
Each paid work count is at least its acquisition count. D38 supplies
the upper for both output contracts, including its evaluation cost.
Taking logarithms proves the limits. The constants/exponents in the
polynomial factor need not coincide across the four minimizations.

This is exponential-rate matching. No exact Theta(exp(gamma T)) query
or operation statement for all kappa is inferred. The original exact
query-order theorem D29 at kappa=1 remains a separate stronger result
for that narrower diffusion scope.

## 2. The common paid model

Count each exact real arithmetic operation, comparison, floor/ceiling,
integer/index/modular operation, stored-value read or write, and each
exp/log/sin/cos/positive-square-root evaluation. Count exact uniform,
exponential-clock and Gaussian draws with known parameters. Complex
arithmetic is finitely many real operations. Fixed public constants
are allowed; real magnitudes and integer/address word sizes are idealized.

There is no free PDE, phase, derivative, Fourier-transform, integration,
or arbitrary known-function evaluator. The chosen interpolant's lookup,
each tree pass, transforms, initialization, time weights, solver steps,
storage and output evaluation are explicitly paid. This is not a
finite-bit computation theorem. In particular the exact time-weight
recurrence may be ill conditioned in floating arithmetic.

## 3. Why the upper no longer needs a stable graph

First pay k^d original values for the explicit Gevrey-2 interpolant g.
It has ||g||inf<=3/4, residual delta<=Cint k^-s, and an actual fixed-cost
lookup after O(k^d) preparation. Only this chosen known g has a public
Gevrey bound; that bound is not imposed on v.

Evolve only to the fixed time L=1 for information reconstruction.
Positive heat smoothing makes S_1^kappa v analytic with a uniform fixed
strip for each fixed kappa. N=O(1+T) modes in each direction leave
sup tail at most epsilon/2, where

    S=T-1, Lchi=25, epsilon=exp(-S)/(16Lchi),
    K=(2N+1)^d.

Compute the K base coefficients of S_1^kappa g to error eta using the
finite paid known-profile solver, with eta=epsilon/(4K). At each of
m=J-1 derivative orders, average M=k^d actual fixed-time tuple samples.
The rate-two majority tree has physical Brownian covariance kappa
times edge duration. It is run only for time one. Bounded Fourier
root weights turn the same tuple into all K coefficient estimates;
correlations between modes are retained. An order-j tuple uses at most
j new values and has a fixed second-moment and expected-work bound.

With k>=ceil((4Cstar K/epsilon)^(1/q)), the genuine Taylor expansion
and independent sample averages give, for each coefficient,

    ||c_raw-c_true||L2<=eta+Cstar k^-q<=epsilon/(2K).

The high-order remainder has this rate because Js>=q. True constant
and nonconstant real coefficients lie in [-1,1] and [-2,2]. Projection
onto these intervals decreases the coefficient error. Let p be the
resulting polynomial. Minkowski yields

    (E||p-S_1^kappa v||inf^2)^(1/2)<=epsilon.

Coefficient bounds alone allow ||p||inf to grow like K. The explicit
fixed Gevrey-2 saturation chi is the identity on [-7/8,7/8], has range
[-15/16,15/16] and Lipschitz constant at most25. The exact S_1^kappa v
lies in that identity interval. The function qhat=chi(p) therefore has
strong sup-norm RMS error at most exp(-S)/16. Its Gevrey norm is bounded
uniformly over every completed random array at inverse scale Rhat=NK,
and every qhat evaluation costs O(K). These two facts prevent hidden
random regularity or evaluator costs.

Actual parabolic comparison gives

    ||S_S^kappa qhat-S_T^kappa v||inf
                      <=exp(S)||qhat-S_1^kappa v||inf.

Finally the finite known-profile solver computes a Fourier polynomial
U_T with conditional sup error at most exp(-T)/16 from S_S^kappa qhat.
Its scale, precision and time parameters are polynomial in T. Thus

    (E||U_T-S_T^kappa v||inf^2)^(1/2)
                     <=1/16+exp(-T)/16<=1/8.

The bulk cost is the paid base computation and fixed-time residual
sampling, k^d times a polynomial in T. The final continuation costs
only polynomial work. The construction does not assume spatial
synchronization and remains valid for weak diffusion.

## 4. Why the lower survives additional unstable modes

Use the same smooth cell bumps as the earlier signed lower, amplitude
A=a k^-s, K=k^d, with full sign layers having sums +/-ell and ell
comparable to sqrt(K). The mean magnitude m=AI ell/K is chosen so
1<=exp(T)m<=2^(s+d/2+1). Every layer member, including later exceptions,
belongs to the promised signed class.

The actual finite-time correction F(v)=exp(-1)Pi S_1v-Pi v is odd and
has a mixed L1 third-derivative bound B=60e^2. A one-coordinate flip
changes F by at most BA^3/K. Full-layer coupling and variance estimates
give a mean of the required sign after time one except with probability
1/64 on each layer.

For each point, a one-coordinate flip changes S_1v(x) by at most
C_kappa A/K. A reveal martingale on the full fixed-cardinality layer
has conditional increment range at most twice this sensitivity. Its
exponential bound, a deterministic heat-gradient estimate and a spatial
net give

    ||S_1v||inf<=C0 exp(-T)sqrt(T)

except with probability1/64 on each layer. The full prior is never
conditioned on these good events. In particular the centered L2 size
W1 obeys the same small bound outside their union of probability1/32.

Write lambda=2pi^2kappa. Actual centered energy gives growth at most
exp((1-lambda)t)W1. The mean's exact cubic forcing and a last-unit
heat comparison imply, at the target horizon, errors at most

    Emean(T)=5C0^2 T^2 exp(-min(1,2lambda)T),
    Espace(T)=Cw sqrt(T)exp(-lambda T).

Both tend to zero for every fixed lambda>0, even if 1-lambda>0.
T82 gives explicit all-real-horizon thresholds making their sum at
most1/32. On the mean/profile good event, actual targets then exceed
91/160 in magnitude and have the prescribed sign.

A uniform MSE1/16 estimator would classify the two full layers with
Bayes error at most9/32. A capped procedure with n=floor(K/1024)
queries has padded without-replacement transcript KL<=1/12, even with
adaptive locations and an arbitrary input-independent seed. Its testing
error is at least3/8. Truncating a randomly stopped procedure therefore
gives average expected queries at least3K/65536. This is the lower in
D37. Arithmetic and analytic quantities used to prove it are not extra
observations supplied to the algorithm.

## 5. Evidence and limits

Root read all857lines of T81,698lines of T82,591lines of T83 and884lines
of T84. The source/audit hashes, shared oracle/cost model and342 initial
protected files are checked in reviews/T83-T84-root-correspondence.json.
T84's profile corollary is explicit, rather than inferred from separate
pointwise RMS estimates. No new initial-value acquisition or PDE
numerical run accompanies this conventional result.

T75 separately formalizes the actual finite-depth graph-tree moment
mechanism; T62/T72 formalize actual information ingredients. These do
not certify D37--D39 end to end. T86 now translates fixed05l's actual
uniform-slice conditioning gate. Full PDE, complete adaptive information,
solver, sampling and final-risk correspondence remain outside the
current combined Lean coverage.

The parameter kappa is fixed before T tends to infinity. Constants and
thresholds may diverge as kappa decreases to zero. At kappa=0 the point
problem is solved by one exact query and the scalar logistic formula,
so no uniform vanishing-diffusion point lower bound follows. This
one-query observation does not apply to reconstruction of the entire
unknown spatial profile at kappa=0.

R17 records a bounded prior-work comparison, including limited-sample
spectral methods and random-data nonlinear transition theory. Those
mechanisms have substantial predecessors. The exact combined theorem's
priority, practical usefulness and significance remain unresolved. No
award-level conclusion follows from these proofs or their audits.
