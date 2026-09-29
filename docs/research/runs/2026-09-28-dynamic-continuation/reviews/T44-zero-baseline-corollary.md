# T44 — fixed-zero baseline on a nonnegative input class

## Verdict and scope

**PASS.** The proposed corollary is valid in the original exact-value
point-query model. On a fixed nonnegative smooth input class containing
zero, uniform absolute RMS at most `1/4` forces expected initial-data
query cost at the **same input `v=0` for every horizon** of at least
`C exp(d T/(s+d))`. The alternatives, but not the baseline, depend on `T`.
Repeated use of the zero input in the finite-family average is legitimate.
No independence between these repetitions is assumed or needed.

This is a separate corollary on a different promised input class. Zero
does not belong to the sign-changing class of D22/04o, so the old theorem
cannot itself be relabelled as a fixed-profile result. The present claim
also requires uniform accuracy over the full spatial class: when the
input is promised to be zero, no queries are necessary; when it is
promised constant, one exact query identifies the scalar initial value.

Read-only inputs checked:

- `04o-unstable-phase-query-lower-bound.md`, SHA256
  `67d6463087775a857a2ffc035fa6ef7fa31db47b4c99b496ecdcc9e8f87fd765`.
- `04n-minorized-burnin-factory.md`, SHA256
  `2907dd00f621fc54a958c5ad45eb0d12c18f520bcd8d2f7b411c4c6f32f2af23`.
- Frozen T40, SHA256
  `fbbc840a4689f68e894ca1872b68e5bcc7367d056b1e33d57711333f3bfdb714`.

Only this report is changed. No implementation, experiment, new formal
target, broad literature search, or priority claim is part of T44.

## 1. Precise Allen–Cahn statement

Fix dimension `d>=1`, integer `s>=1`, and a target point `x*` on the unit
flat torus. Let `S_T v` solve

    u_t = (1/2) Delta u + u - u^3,   u(0)=v.

Use the fixed class

    F+ = {v in C^infinity(T^d): 0<=v<=1/2,
          max_{|alpha|<=s} ||partial^alpha v||_infinity <=1}.

Only derivatives through this fixed finite order are bounded uniformly.
There is no promise of a finite-dimensional parametrization, a common
analytic radius, or uniform bounds on all higher derivatives.

The algorithm knows the PDE, class, `d,s,T,x*`, and may know all hard-family
formulas. Its sole input-dependent information is the exact deterministic
value `v(x)` at each adaptively chosen point. Source code, a member label,
input-dependent metadata, integrals, Fourier coefficients, and uncharged
input-dependent preprocessing are excluded. All initial-data evaluations
are counted in `Q_T(v)`; scalar arithmetic and private randomness are free.
The output `H_T(v)` may be biased and unbounded.

Use an input-independent private seed and measurable query, stopping, and
output rules on finite transcripts. Require almost-sure finite halting
on the promised class. Standard Borel seeds and Borel rules are one
concrete sufficient contract. At a fixed `T` the proof couples only
`K+1` distinct inputs, so their exceptional null sets can be discarded
simultaneously. If `E Q_T(0)=infinity`, the conclusion is already true.

Fix `0<epsilon<1/(2 sqrt(2))`. For every `T>=T0`, every such algorithm
satisfying

    sup_{v in F+} E |H_T(v)-S_T v(x*)|^2 <=epsilon^2

obeys

    E Q_T(0) >= (1-8 epsilon^2) K
      >= (1-8 epsilon^2) 2^(-d) (kappa*a*I/e)^(d/(s+d))
           * exp(d*T/(s+d)).

The displayed bound is positive for `epsilon<1/(2 sqrt(2))`. In
particular, `epsilon=1/4` gives

    E Q_T(0) >= K/2
      >= 2^(-d-1) (kappa*a*I/e)^(d/(s+d)) exp(d*T/(s+d)).

The constants and threshold below depend only on `d,s` and one fixed
bump. The quantifiers are: fix these problem parameters and constants;
then for every sufficiently large `T` and every admissible uniformly
accurate algorithm at that `T`, the cost bound holds on the fixed zero
oracle. Algorithms are allowed to depend on `T`.

## 2. Hard alternatives and a uniform positive solution gap

Reuse the bump and constants from 04o:

    psi in C_c^infinity((0,1)^d),  0<=psi<=1,  I=integral psi>0,
    D=max(1,max_{|alpha|<=s} ||partial^alpha psi||_infinity),
    a=1/(8D),  q=s+d,
    kappa=(2*pi)^(-d/2) exp(-d/8),
    T0=max(1, 1+q*log(4)-log(kappa*a*I)).

For `T>=T0`, put

    R=(kappa*a*I*exp(T-1))^(1/q),
    k=floor(R)>=4,  K=k^d,  mu=a*I*k^(-q).

Partition the torus into `K` half-open cubes of side `1/k`, and put

    b_j(x)=a*k^(-s)*psi(k*x-j)

in cube `j`, extended by zero elsewhere. Compact support in the cube
interior makes this a smooth periodic function. The mass is `mu`, and
every derivative through order `s` is bounded by `aD<=1/8`. Thus every
`b_j`, as well as the fixed baseline zero, lies in `F+`. In fact the
alternatives satisfy `0<=b_j<=1/8`.

The floor bounds imply

    R/2<=k<=R,
    1<=kappa*mu*exp(T-1)<=2^q,
    K>=2^(-d)*(kappa*a*I/e)^(d/q)*exp(d*T/q).

For the generator `(1/2)Delta`, the time-one torus heat kernel is at
least `kappa`: in its periodized Gaussian sum, the nearest integer
translate has each coordinate distance at most `1/2`, and its single
nonnegative term gives the claimed bound.

The invariant interval `[0,1]`, nonnegative reaction there, and the mild
equation give

    S_1 b_j >= P_1 b_j >= kappa*mu =: c>0.

Here `c<=1` because `kappa<1` and the bump mass is at most `1/8`.
Comparison with the spatially constant scalar solution yields

    S_T b_j(x*) >= ell_c(T-1),
    ell_c(t)=c*exp(t)/sqrt(1+c^2*(exp(2t)-1)).

Writing `z=c*exp(T-1)>=1` gives

    ell_c(T-1)=z/sqrt(1+z^2-c^2)
                >=z/sqrt(1+z^2)>=1/sqrt(2).

Meanwhile `S_T 0=0` exactly. Define the alternative target
`a_j=S_T b_j(x*)`; all `a_j>=1/sqrt(2)`. No oddness, common sine,
perturbation estimate, mean closure, or linearized approximation is
required for this corollary.

## 3. Repeated-zero averaging and adaptive expected query cost

Couple the runs on zero and on every `b_j` using the same private seed.
Let `J` be the set of cubes visited by the baseline zero run before it
halts. Half-open cubes assign every query point to exactly one cell;
therefore `|J|<=Q_T(0)` pointwise. Visiting a cube where the bump value
happens to be zero only overcounts potentially informative visits, which
is harmless for this lower bound.

For `E_j={j not in J}`, all baseline queries are outside cube `j`.
The initial functions agree there. Induction over the finite baseline
transcript shows that the query locations, responses, stopping decision,
and returned output coincide on zero and on `b_j` for the same seed.
This proves equality of the two outputs on `E_j` even for adaptive
locations and random stopping. It does not assume equality after a hit.

On `E_j` let their common real output be `y`. The pointwise identity

    [(y-a_j)^2+y^2]/2 = (y-a_j/2)^2+a_j^2/4 >=1/8

holds without any assumption about bias or the size of `y`. Discarding
nonnegative losses on the complementary event gives

    (1/(2K)) sum_j [E |H_T(b_j)-a_j|^2 + E |H_T(0)|^2]
      >= (1/(8K)) sum_j P(E_j)
       = (1/8)*(1-E|J|/K)
      >= (1/8)*(1-E Q_T(0)/K).

The left side is the risk averaged over a multiset consisting of each
`b_j` once and zero `K` times. Equivalently, choose zero with probability
`1/2` and each alternative with probability `1/(2K)`. It is at most
`epsilon^2` by the uniform MSE premise. An average over a multiset does
not require distinct inputs or independent repetitions. The zero output
is the same coupled random variable in every term, and finite linearity
of expectation already proves the displayed inequality.

Rearranging proves `E Q_T(0)>=K(1-8 epsilon^2)`. Finite sums and
nonnegative integration suffice; there is no differentiation under an
expectation, stopping-time independence, optional-stopping theorem, or
conversion from a Bernoulli-coin oracle.

## 4. Counterexample attempts and exact limitations

- **The algorithm already knows zero is a possible input.** This is
  allowed. It does not know whether the actual oracle is zero or an
  unseen bump. All alternatives give exactly zero at every point outside
  their hiding cell, so arbitrary precision cannot distinguish them
  along a no-hit transcript.
- **The actual input is promised zero or promised constant.** These are
  different smaller input classes. Zero queries suffice for the first;
  one exact query and scalar evolution suffice for the second. Neither
  algorithm satisfies the present uniform premise on `F+`.
- **Rare expensive runs or unbounded outputs.** The paired loss identity
  is pointwise, and the proof directly bounds the expected baseline
  query count. These choices do not invalidate it.
- **A fixed profile statement for the old sign-changing class.** Not
  obtained: zero is outside that class. The fixed-profile conclusion is
  valid here because the promised class has been changed explicitly.
- **Uniform work under D21's burn-in conditions.** D21 requires a known
  fixed positive lower mass certificate `pi(v)>=delta0>0`. Zero violates
  it. Here `||b_j||_infinity<=a*k^(-s)` tends to zero uniformly in `j`,
  hence `pi(b_j)` tends to zero for every probability measure `pi`.
  These alternatives also have no common positive certificate. There is no
  contradiction with fixed-mass, fixed-burn-in uniform work bounds.
- **Optimality or numerical validation.** The construction proves one
  sufficient exponential lower bound, not a matching minimax rate.
  Numerical experiments cannot establish or invalidate its oracle
  quantifiers. No such experiment is needed for this corollary.

The lower bound concerns absolute error for the solution value. At zero,
the exact solution is zero and its defect `1-u` is one; no relative-error
theorem is silently inferred. The result measures the cost of maintaining
a uniform guarantee over unknown spatial inputs while receiving the zero
transcript, not the arithmetic difficulty of evaluating a supplied zero
formula.

## 5. Optional controlled extension to a C2 reaction

This is a separate conventional extension, not needed for the Allen–Cahn
verdict and not a change to the ongoing formal target. Suppose

    f in C^2([0,b]),  b>0,  f(0)=f(b)=0,
    f(y)>0 for 0<y<b,  f'(0)=lambda>0.

Use the same torus semigroup, the fixed nonnegative class with range
`[0,b/2]`, and a fixed finite `C^s` bound. Choose the bump coefficient
small enough to belong to that class. Comparison keeps the solution in
`[0,b]`, and nonnegative reaction again gives `S_1 b_j>=kappa*mu`.

Fix any `theta in (0,b)`. For `0<y<=theta`, define

    r(y)=1/f(y)-1/(lambda*y),
    J_theta=integral_0^theta |r(y)| dy,
    B_theta=theta*exp(lambda*J_theta).

Taylor's estimate `f(y)=lambda*y+O(y^2)` implies that `r` is bounded
near zero; it is continuous away from zero. Consequently
`J_theta<infinity`. The time for the scalar flow to rise from
`0<c<theta` to `theta` is exactly

    tau(c,theta)=integral_c^theta dy/f(y)
       <=(1/lambda)*log(theta/c)+J_theta.

It follows that `c*exp(lambda*S)>=B_theta` is sufficient for the scalar
value at time `S` to be at least `theta`; if `c>=theta` this is immediate
from monotonicity. This controls the full nonlinear flow rather than
propagating its linearization to order-one amplitude.

Take `q=s+d`, `mu=aI*k^(-q)`, and for sufficiently large `T` put

    k=floor[(kappa*aI*exp(lambda*(T-1))/B_theta)^(1/q)].

Then `S_T b_j>=theta`, while `S_T0=0`, and the same information proof
gives

    E Q_T(0)>=(1-4 epsilon^2/theta^2) k^d
             >= C_theta exp(lambda*d*T/(s+d))

whenever `epsilon<theta/2`, with an explicit positive constant obtained
from the same floor estimate. Thus every fixed `epsilon<b/2` can use a
choice `2epsilon<theta<b`. Some restriction on absolute accuracy relative
to `b` is necessary: at `epsilon>=b/2`, the constant output `b/2` already
has zero-query error at most `epsilon` for all solutions in `[0,b]`.

The `C2` assumption closes the logarithmic hitting-time remainder and
justifies the exact exponential rate `lambda`, without an unproved
replacement of `f(y)` by `lambda*y`. No assertion is made here under
merely `C1` regularity, for sign-changing general-reaction inputs, or for
other information oracles. This short extension is conventionally
validated but not formalized, implemented, or assigned a priority claim.

## 6. Decision

The Allen–Cahn fixed-zero corollary has no remaining conventional proof
gap under the explicit oracle, measurability, halting, and uniform-error
contract above. It may be integrated as a separate nonnegative-class
corollary of D22. It reuses the established finite no-hit information
argument with target gap `1/sqrt(2)`; it does not require changing the
ongoing general information-core formalization. T40's attribution of the
disjoint-support method to classical information-based complexity remains
applicable. No additional literature search or originality conclusion was
made in this bounded audit.
