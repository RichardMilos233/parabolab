# T48 — independent audit of the nonnegative-class matching upper bound

## Verdict and frozen scope

**PASS of the proposed conventional theorem.** On exactly T44's fixed
nonnegative smooth class and exact-value point-query model, the proposed
estimator has uniform absolute RMS at most `5/32 < 1/4` for every sufficiently
large horizon, with the deterministic query count

    n(T) = ceil(64 C exp(d T/(s+d))).

Together with T44, this gives a matching exponential query order
`Theta(exp(d T/(s+d)))`, with constants and time thresholds depending on
`d,s`. It gives this order both for worst-input expected cost and for the
cost at the fixed zero input among algorithms required to be uniformly
accurate on the full class. The lower and upper bounds must use the larger
of their two fixed time thresholds.

No counterexample or necessary theorem repair was found. The proof below
supplies the potentially missing details: a signed periodic interpolation
kernel valid for every integer `s>=1`, a dimension-dependent heat-mixing
time, the precise scalar upper-factor inequality, and the exact information
contract. The argument was derived independently before a T46 manuscript
was available. No experiment, implementation, Lean result, or novelty
claim is part of this audit. The subsequently frozen T46 manuscript and
its optional bounded-horizon completion were also checked below; both pass.

Read-only source versions:

- `reviews/T44-zero-baseline-corollary.md`, SHA256
  `124d2c2152fb8ce1f8edd8585ce38ee3739a69892c6769a856be42d85b0f6d29`.
- `04o-unstable-phase-query-lower-bound.md`, SHA256
  `67d6463087775a857a2ffc035fa6ef7fa31db47b4c99b496ecdcc9e8f87fd765`.
- `reviews/T46-positive-class-upper-bound.md`, SHA256
  `6ad43f33f45739a510ea6ea968041e4332762fa3c358773ce431c57ac9e93997`.
- `04n-minorized-burnin-factory.md`, SHA256
  `2907dd00f621fc54a958c5ad45eb0d12c18f520bcd8d2f7b411c4c6f32f2af23`.
- `reviews/T32-minorized-burnin-factory-audit.md`, SHA256
  `ca8b760d0a39eefb034cb1ca5f6ae98d5add16825e181fc20381e7f331b7e4e4`.
- Repository HEAD at inspection:
  `65dca46e42db1c80cdf9ddd8eed6a415148c37f3`; the working tree contains
  unrelated changes, so this commit is not claimed to identify the full
  source state. The hashes above identify the mathematical inputs.

Only this audit file is owned or changed by T48. The final file's SHA256
is reported separately after writing; a self-containing hash is not used.

## 1. Same class, same oracle, and exact target

The domain is the unit-volume flat torus `R^d/Z^d`, `d>=1`. Fix an integer
`s>=1`, and write

    F+ = {v in C^infinity(T^d): 0<=v<=1/2,
          max_{|alpha|<=s} ||partial^alpha v||_infinity <=1},
    u(t,x)=S_t v(x),
    u_t=(1/2) Delta u + u-u^3,
    m=integral_(T^d) v,    beta=s/(s+d),    gamma=1-beta=d/(s+d),
    Psi(z)=z/sqrt(1+z^2),   eta=1/64.

The integral defining `m` is used in the proof, not supplied to the
algorithm. In particular, no fixed positive lower bound on `m` is
promised. Since the torus has volume one, `0<=m<=1/2`. The same comparison
principle as in T44 gives `0<=u<=1` for all times. Standard smooth
parabolic solutions and comparison are conventional analytic inputs;
they are not asserted to have been formalized here.

The algorithm knows `d,s,T,x*`, the PDE and the class. It draws `n`
independent uniform torus points `X_i`, asks only for the exact values
`v(X_i)`, and returns

    mhat=(1/n) sum_i v(X_i),
    H_T(v)=Psi(exp(T) mhat).

All these `n` values are charged. No derivative, integral, Fourier,
formula, member-label, or evolved-solution oracle is used. The returned
number does not depend on `x*`; the deterministic approximation established
below is uniform over every spatial point. No mass-dependent branch or
unknown mass certificate is used in the algorithm.

## 2. Height versus mass, including the periodic constants

There is a finite class-dependent constant `C=C(d,s)>=1` such that

    ||v||_infinity <= C m^beta                       (1)

for every `v in F+`. Nonnegativity is essential to this bound in terms of
the signed integral `m`.

Here is a direct construction, including `s=1`. Choose a nonnegative
`chi in C_c^infinity((-1/2,1/2)^d)` that is positive on a nonempty open
set. Index the monomials by `A={alpha: |alpha|<=s-1}`. The finite matrix

    G_(alpha,beta)=integral_(R^d) chi(z) z^(alpha+beta) dz

is positive definite: its quadratic form is the weighted integral of a
polynomial squared, and a nonzero polynomial cannot vanish on an open
set. Solve `G c=e_0` and set

    K(z)=chi(z) sum_(beta in A) c_beta z^beta.

Then `K` is smooth, compactly supported in the open unit cube, and

    integral K=1,
    integral z^alpha K(z) dz=0   for 1<=|alpha|<=s-1.

For `s=1` there are simply no vanishing-moment constraints. The kernel is
allowed to be signed; no positivity or Markov property is used for it.
Put

    A_K=||K||_infinity,
    B_K=(1/s!) integral |K(z)| (sum_i |z_i|)^s dz,
    C=max(1,A_K+B_K).

For `0<h<=1`, periodize the scaled kernel by

    K_h(y)=h^(-d) sum_(k in Z^d) K((y+k)/h).

Its supported translates do not overlap, since each support is strictly
inside a cube of side at most one. Consequently
`||K_h||_infinity<=A_K h^(-d)`, with no omitted periodization factor.
Taylor expansion of the periodic lift along `x-thz`, with all derivatives
of total order `s` bounded by one, gives

    |v(x)-(K_h*v)(x)| <= B_K h^s.

Indeed, the directional derivative of order `s` is bounded by
`h^s (sum_i |z_i|)^s`, and the integral Taylor remainder contributes
the factor `1/s!`. All lower-order terms cancel by the moment conditions.
As `v>=0`,

    |(K_h*v)(x)| <= A_K h^(-d) integral v = A_K h^(-d) m.

For `m>0`, take `h=m^(1/(s+d))<=1`. Both terms have order `m^beta`,
which proves (1). For `m=0`, continuity and nonnegativity imply `v=0`,
so (1) is immediate. This avoids an invalid positive-mollifier argument
for high `s` and does not replace the finite `C^s` class by an analytic
or finite-dimensional one.

## 3. Public constants and early nonlinear comparison

Let `P_t` denote the torus heat semigroup with generator `(1/2)Delta`,
and let `p_t` be its density relative to unit-volume Lebesgue measure.
Choose `L>=1` with

    ||p_L-1||_infinity<=eta.                         (2)

The existence and dimension dependence can be made explicit. The Fourier
coefficients are `exp(-2*pi^2 L |k|^2)`. With
`a=exp(-2*pi^2 L)`,

    ||p_L-1||_infinity
       <= sum_(k != 0) exp(-2*pi^2 L |k|^2)
       <= ((1+a)/(1-a))^d-1.

Thus one valid choice is

    L=max(1, log(8d/eta)/(2*pi^2)).

For this choice `a<=eta/(8d)<1/2`, the logarithm of the displayed product
is at most `4da<=eta/2`, and `exp(eta/2)<=1+eta`. There is no assertion
that `L=1` works in every dimension.

Choose a fixed positive `m0`, for example

    m0=min(1/2,
           [2eta/(C^2 (exp(2L)-1))]^(1/(2beta)),
           exp(-L) sqrt(eta)/(1+eta)).               (3)

It obeys exactly the two proposed conditions

    C^2 m0^(2beta) (exp(2L)-1)/2 <= eta,
    (1+eta) exp(L) m0 <= sqrt(eta).

The explicit `1/2` in (3) is harmless and is in fact redundant for
`L>=1, eta=1/64`. All constants are independent of the unknown input and
of `T`.

Suppose first that `0<m<=m0`. Linear upper comparison and (1) give

    u(t,x) <= exp(t) P_t v(x) <= C m^beta exp(t).

Set `b(t)=C m^beta exp(t)` and
`A(t)=integral_0^t b(r)^2 dr`. The actual nonlinear solution satisfies

    u_t-(1/2)Delta u-[1-b(t)^2]u=(b(t)^2-u^2)u>=0.

The linear function `w(t)=exp(t-A(t))P_t v` has the same initial value
and satisfies the corresponding equality. Parabolic comparison therefore
gives the exact nonlinear bound

    exp(t-A(t)) P_t v <= u(t) <= exp(t) P_t v.

This also follows from Feynman--Kac, but the differential inequality shows
that no nonlinear mass closure or unproved linear approximation is needed.
At `t=L`, (3) gives `A(L)<=eta`, and hence

    exp(L-eta) P_L v <= u(L) <= exp(L) P_L v.       (4)

Because `v>=0`, (2) implies
`(1-eta)m<=P_Lv(x)<=(1+eta)m` at every point. Since
`exp(-eta)(1-eta)>=(1-eta)^2>=1-2eta`, define

    a0=exp(L)m,
    c_-=(1-2eta)a0,
    c_+=(1+eta)a0 <= sqrt(eta).

Equation (4) gives `c_-<=u(L,x)<=c_+` uniformly in `x`.

## 4. Uniform scalar approximation for small mass

For `0<=c<1`, the scalar Allen--Cahn flow is

    ell_c(t)=c exp(t)/sqrt(1+c^2(exp(2t)-1)).

For `T>=L`, let `tau=T-L` and `z=exp(T)m=a0 exp(tau)`. Scalar comparison
gives `ell_(c_-)(tau)<=u(T,x)<=ell_(c_+)(tau)` for every `x`. If
`c=r a0`, its exact relation to the proposed surrogate is

    ell_c(tau)=Psi(r z/sqrt(1-c^2)).                (5)

In particular, the denominator correction must be included; simply
identifying the scalar flow with `Psi(rz)` would be false at finite time.
For the lower barrier, (5) and monotonicity give

    ell_(c_-)(tau) >= Psi((1-2eta)z).

For the upper barrier, `c_+^2<=eta` gives

    ell_(c_+)(tau) <= Psi(q_+ z),
    q_+=(1+eta)/sqrt(1-eta) <=1+2eta.

The last inequality holds for `eta=1/64`: after squaring its positive
sides, the difference is

    (1-eta)(1+2eta)^2-(1+eta)^2
      = eta(1-eta-4eta^2)>0.

For any `X,z>=0`, the anchored inequality

    |Psi(X)-Psi(z)| <= |X-z|/sqrt(1+z^2)           (6)

is valid, including `z=0`. If `X>=z`, replace the denominator of `Psi(X)`
by the smaller `sqrt(1+z^2)` to obtain an upper bound; if `X<=z`, the same
replacement gives a lower bound. Monotonicity then supplies the stated
absolute-value inequality. It implies

    |Psi(rz)-Psi(z)| <= |r-1|

for `r,z>=0`. Applying this separately to the two scalar barriers proves

    sup_x |u(T,x)-Psi(exp(T)m)| <=2eta             (7)

for every `0<m<=m0` and every `T>=L`. At `m=0`, both quantities are zero
exactly, so the same statement holds.

## 5. Large mass and one class-uniform threshold

For the time-one heat kernel use exactly T44's lower bound

    kappa=(2*pi)^(-d/2) exp(-d/8),   0<kappa<1.

The invariant interval `[0,1]` makes the reaction nonnegative, so for
`m>=m0`,

    u(1,x)>=P_1v(x)>=kappa m>=c0:=kappa m0.

Here `0<c0<1`. For every `T>=1`, scalar comparison yields

    u(T,x)>=ell_(c0)(T-1)>=Psi(B),
    B=c0 exp(T-1).

Choose precisely the proposed threshold

    T*=max(L, 1+log(1/(kappa m0 sqrt(eta)))).       (8)

Then `T>=T*` implies `B>=eta^(-1/2)`. Moreover,

    exp(T)m >= exp(T)m0 = (e/kappa)B >= B.

Consequently both `u(T,x)` and `Psi(exp(T)m)` belong to
`[Psi(B),1]`. Their separation is at most

    1-Psi(B) <=1-(1+eta)^(-1/2)<=eta/2<=2eta.

The bound `1-(1+eta)^(-1/2)<=eta/2` follows from convexity, or direct
integration of `(1/2)(1+t)^(-3/2)<=1/2`. Thus (7) holds uniformly over
all `v in F+`, all `x`, and all `T>=T*`. The large-mass branch actually
has a stronger constant than required. The split is only a proof device.

## 6. Sampling risk, deterministic cost, and admissibility

For a uniform torus point `X`, positivity and (1) give

    E[v(X)^2] = integral v^2 <= ||v||_infinity m <= C m^(1+beta).

The iid sample mean is unbiased and therefore

    E[(mhat-m)^2]=Var(v(X))/n <= C m^(1+beta)/n.   (9)

Both `mhat` and `m` are nonnegative, so (6) applies pointwise with
`X=exp(T)mhat`, `z=exp(T)m`. Combining it with (9),

    E|Psi(exp(T)mhat)-Psi(exp(T)m)|^2
      <= C exp(2T) m^(1+beta)/(n(1+exp(2T)m^2))
       = (C exp(gamma T)/n) z^(1+beta)/(1+z^2)
      <= C exp(gamma T)/n.

The last ratio is at most one: for `0<=z<=1` its numerator is at most
one; for `z>=1` its numerator is at most `z^2`, since `0<beta<1`. With

    n=ceil(64 C exp(gamma T)),

the transformed MSE is at most `1/64`, hence its RMS is at most `1/8`.
Minkowski's inequality and the deterministic bias (7) give

    sup_(v in F+) sup_x (E|H_T(v)-S_Tv(x)|^2)^(1/2)
      <=1/8+2eta=1/8+1/32=5/32<1/4             (10)

for all `T>=T*`. In particular, the total MSE is at most `25/1024`,
which is below T44's required `1/16`.

This is an admissible algorithm in the same model: a finite tuple of
independent uniforms is an input-independent standard Borel seed; the
query locations, fixed stopping rule, sample mean and output are Borel;
and it halts after exactly `n` queries on every input. Thus

    Q_T(v)=E Q_T(v)=n

for every `v`, including zero. The known constants and scalar functions
are input-independent; the information model treats scalar arithmetic as
free. No claim about bit complexity, finite-precision stability, or the
cost of sampling continuous uniforms is substituted for the stated query
cost. For `T>=T*>=1`,

    n <=(64C+1) exp(gamma T),

so rounding the budget does not affect the exponent.

## 7. Adversarial checks and exact boundary of the conclusion

- **Zero and arbitrarily small mass:** zero is handled exactly, and
  (7)--(10) are uniform as `m` tends to zero. Neither the algorithm nor
  the proof assumes a positive mass certificate common to the class.
- **Highly concentrated smooth spikes:** their high derivatives are
  controlled only through order `s`; the signed-kernel estimate uses
  exactly those bounds. No uncharged access to derivatives is needed.
- **Smallest allowed regularity:** the kernel argument works at `s=1`,
  and all exponents and the explicit `m0` are defined because `beta>0`.
- **High dimension and wrapping:** `L` can depend on `d`; periodization
  in the interpolation bound has no overlap factor for the chosen
  compact support and `h<=1`. The time-one lower heat bound uses the
  same normalization as T44.
- **Long horizons:** all later evolution is bounded using the exact
  nonlinear scalar flow. The proof never amplifies an additive error by
  `exp(T-L)` without control or extends a linearization to amplitude one.
- **Rare sampling events:** (6) is a pointwise estimate, so no
  concentration event or unjustified clipping of atypical estimates is
  needed. The estimator is bounded in `[0,1)`.
- **What matches:** T44's nonnegative class, absolute solution error,
  exact-value information, fixed `d,s`, and large-time exponent match.
  The proof does not establish an optimal exponent on 04o's different
  sign-changing class, a relative-defect theorem, or a lower bound for
  a supplied symbolic formula.
- **Accuracy and secondary parameters:** the assertion fixes the error
  tolerance at `1/4` (the upper construction achieves `5/32`). It does
  not identify sharp dependence on a variable tolerance, dimension,
  smoothness, constants, or the pre-asymptotic horizon.

The conventional matching-rate claim is supported under this precise
contract. Its heat/PDE/interpolation/probability bridges remain separate
from any Lean theorem or numerical implementation produced elsewhere.

## 8. Comparison against frozen T46

The frozen T46 proof uses a polynomial Gram representer on the closed cube
`Q=[-1/2,1/2]^d`, instead of the smooth compact kernel independently
constructed in Section 2 above. Its stated constant

    B=sum_alpha |c_alpha| 2^(-|alpha|),
    C=B[1+(d/2)^s/s!]

is valid: `||K||_infinity<=B`, `||K||_1<=B` on the volume-one cube,
`1=|integral K|<=B`, and `sum_i |y_i|<=d/2`. The cube scaled by
`0<h<=1` is injective in the torus up to null boundaries, so its mass
integral is at most `h^(-d)m`. Smoothness of the kernel is unnecessary for
the Taylor integral estimate. The rational Gram matrix gives finite
public constants using only `d,s`. Thus T46's alternative construction
does not introduce a regularity or periodicity gap.

Its scalar upper proof separates the change in initial amplitude from
the denominator correction. The claimed elementary bound

    (1-t)^(-1/2)-1<=t   for 0<=t<=1/4

is correct: squaring the equivalent positive-sided inequality gives
`(1+t)^2(1-t)>=1`, or `t(1-t-t^2)>=0`. Substituting
`t=w_+^2/(1+c_+^2 z^2)<=eta` bounds the denominator correction by
`eta`; the anchored estimate bounds the amplitude change by another
`eta`. This agrees with the independent combined-factor proof above.

T46's explicit `L,m0,T*`, transformed risk constant `1/64`, and final
RMS `5/32` match the audited constants. Its additional uniform
convergence claim is also valid: repeat the construction for each fixed
smaller `0<eta<=1/64`, then let `T` exceed that eta-dependent threshold.
This yields `sup_v ||S_Tv-Psi(exp(T)integral v)||_infinity ->0`.

The literature descriptions and the reported 17-query search were not
independently repeated in T48. The mathematical verdict neither verifies
publication priority nor depends on the absence of prior matching results.

## 9. Optional bounded-horizon completion

The optional all-horizons paragraph in T46 also passes. It uses only the
original bounded voting root from 04n/T32, not the affine Bernoulli factory,
its imported factory theorem, or a positive mass certificate. The relevant
root identity can be checked directly: with degree-three Bernstein
coefficients `(0,1/2,1,1)`,

    G(q)=(3/2)q(1-q)^2+3q^2(1-q)+q^3
        =(3/2)q-(1/2)q^3,
    2[G(q)-q]=q-q^3.

Run rate-two ternary branching with known torus heat transitions. At each
initial-data leaf `Y`, one exact query supplies `v(Y)`; comparison with a
fresh independent uniform generates its Bernoulli coin. At an internal
vertex use the coefficient indexed by the number of successful children.
All outputs are binary. Conditional child independence and the bounded
first-event equation identify the root mean with `S_Tv(x*)`. The heat
transitions, clocks and auxiliary votes depend only on the public PDE and
private randomness, so this remains within the exact-value information
model; it does not assume an unknown evolved-value oracle.

Let `N(T)` count every node of the full tree. Rate two and replacement of
one live particle by three give expected live leaves `exp(4T)`. Since
each branching event adds two leaves and three total nodes, the finite
tree identity gives

    E N(T)=(3 exp(4T)-1)/2 <= B*:=(3 exp(4T*)-1)/2

for `0<=T<=T*`. The corresponding finite-generation domination establishes
finite expectation and almost-sure completion, as recorded in 04n/T32.
One can equivalently prove it by the pure-birth generator and its finite
truncations; no input-dependent tree-growth bound is required.

Take `M=ceil(16 B*)`. Generate at most `M` nodes of a root; if constructing
the full root would require a further node, abort that root and return
zero. Couple its output `Y_cap` to the full root `Y` using the same
randomness. They agree on `{N(T)<=M}`, and both belong to `[0,1]`. Hence

    |E Y_cap-S_Tv(x*)|
      <=P(N(T)>M)<=E N(T)/M<=B*/M<=1/16.

This cap can be implemented before further input queries are made. Every
evaluated leaf is a generated node, so at most `M` exact initial-data
queries are used per capped root, even when it aborts. The coupling does
not assert independence between a root's value and its size.

Average 16 independent capped roots. Their variance is at most
`(1/4)/16=1/64`, so the fluctuation RMS is at most `1/8`; adding the
bias gives total RMS at most `3/16<1/4`. The deterministic data-query cap
is `16M`. At `T=0` this is wasteful but valid. In particular, there is
no zero-mass exception.

Use this algorithm for `0<=T<T*` and the sample-mean sigmoid for `T>=T*`.
The resulting all-horizons algorithm has uniform RMS at most `3/16` and

    Q_T(v) <= max(16M,64C+1) exp(gamma T)  for every T>=0.

The all-horizons upper completion is therefore correct, although its
very large fixed constant has no practical efficiency interpretation.
T44 continues to supply only the stated sufficiently-large-time lower
bound. No additional theorem repair is required.
