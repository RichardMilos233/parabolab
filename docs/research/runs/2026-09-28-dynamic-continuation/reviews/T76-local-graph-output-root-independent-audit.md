# T76: independent audit of local graph output and finite-time roots

Date: 2026-09-29. Role: independent mathematical research review.
Requested dispatch: gpt-6-astra / max, as recorded in the root task and
run.json. The serving model is not independently exposed beyond the
explicit spawn configuration. Skill: math-auto-research 0.2.0; its
defaults, model-routing rules, execution guidance and general profile
were read. This is a conventional proof audit, without numerical or
Lean evidence.

**Verdict: GO for the exact supplied-trajectory local output estimate,
finite-time mean root estimate, and conditional deterministic evaluation
rule in R14b. No material proof gap or change of constants was found.**
The proof below makes the regularity convention explicit, derives
continuity of the mean map directly, and gives a completely public
integer time and loop bound. These are proof completions within R14b's
stated assumptions, not a weakening of its claims.

The verdict does not establish a stable graph, a graph neighborhood
reached by every input, or any spectral-gap extension of the accepted
query/work theorems. In particular it does not promote R14, reuse T65's
global phase as a premise, or alter D29/D30/D31.

## 1. Frozen sources and review scope

Both sources were fully read. Their initial SHA-256 digests agreed with
the root's freeze message; their bytes were checked again before handoff.

| Source relative to this reviews directory | Lines | SHA-256 |
|---|---:|---|
| R14b-local-graph-output-and-root-proof.md | 205 | dff72bd839794df81eb36ac0744dfd5f711de6c2bcb5f8a128b2dd922ca24cf6 |
| R14-spectral-gap-extension-candidate.md | 145 | 5b113f637b266e558b6f530cbc29049d59ae41141b56a3926fd148d097bedff0 |

R14b is the audited mathematical source. R14 is background explaining
the proposed later application; its candidate claims are not premises.
Project instructions, the research index, run context/checkpoint,
D29/D30/D31 entries and T76's model-use entry were inspected for scope.
The pre-existing dirty working tree was inspected and preserved.
Only this T76 file is editable by this worker.

The audit starts from the actual Allen--Cahn equation and the explicitly
supplied stable trajectory. No heat spectral estimate, phase existence
theorem, derivative measure, sampler, arithmetic solver or stochastic
representation is needed for the argument.

## 2. Exact accepted mathematical statement

Let d be a fixed positive integer, kappa>0, and let Pi be integration
against probability Haar measure on the unit torus. Write

    L = (kappa/2) Delta,
    u_t = L u + u - u^3.

Use the actual real solution flow. Sufficient regularity is continuity
to t=0 in the spatial sup norm and classical regularity C^{1,2} for
t>0, with the PDE, periodic integration by parts, uniqueness and
parabolic comparison valid. Smooth classical periodic data certainly
fit this convention. The proof also applies to continuous periodic data
under the usual classical-for-positive-time solution interpretation.
All claims below are about actual solutions in this class, not a
discretization. R14b explicitly assumes this classical flow.

Suppose Pi w=0 and a supplied global solution V has initial value
w+c_star and satisfies, for fixed positive R and sigma,

    ||V(t)||inf <= R exp(-sigma t),       t>=0.

No existence or regularity of a map w -> c_star is assumed or proved.
Define

    epsilon(t) = 3R(1+R) exp(-sigma t)
                 + 3R^2 exp(-2sigma t),
    E = 3R(1+R)/sigma + 3R^2/(2sigma),
    B = R^3/(1+3sigma).

For any b such that w+b belongs pointwise to [-1,1], set
h=b-c_star. For any 0<=h_max<1 with |h|<=h_max, let
u(t)=S_t(w+b). Then, with

    phi_t(h) = h exp(t) / sqrt(1+h^2(exp(2t)-1)),
    Psi(z) = z/sqrt(1+z^2),

the following statements hold:

    |Pi V(t)| <= B exp(-3sigma t);

    ||u(t)-phi_t(h)||inf
      <= R exp(-sigma t) + exp(E)-1,       t>=0;

    sup_{t>=0,x} |u(t,x)-Psi(exp(t)h)|
      <= R + exp(E)-1 + (1-h_max^2)^(-1/2)-1.       (A)

For h!=0, there is also the pointwise signed estimate

    exp(-E) phi_t(|h|)
      <= sign(h)(u(t,x)-V(t,x))
      <= exp(E) phi_t(|h|).                       (B)

For h=0, uniqueness gives u=V. The comparison leading to (B) in fact
works for any magnitude of the constant shift for which the initial
u belongs to [-1,1]; the restriction |h|<1 is used for the absolute
output bound and sigmoid comparison.

For the root conclusion, assume additionally

    0<r<=1,  ||w||inf<=r/8,  |c_star|<=r/8,
    D = 2 exp(E) B <= min(1,r/16).

For every finite tau>=0, the actual mean map

    f_tau(c) = Pi S_tau(w+c),     c in I=[-r/4,r/4],

has exactly one zero c_tau in I, and

    |c_tau-c_star| <= D exp(-(1+3sigma)tau),       (C)
    |c_tau| <= 3r/16.

For every c2>c1 in I, one has the two-sided increment bound

    exp(-2tau)(c2-c1)
      <= f_tau(c2)-f_tau(c1)
      <= exp(tau)(c2-c1).                         (D)

The lower half of (D) is R14b's asserted bound; the upper half is a
direct consequence of the same comparison argument and proves
continuity. The root is at distance at least r/16 from either endpoint
of I.

For every 0<zeta<r, given deterministic evaluations of this actual
f_tau with absolute error at most

    epsilon_f = exp(-2tau) zeta/8,

R14b's buffered bisection returns a value within zeta of c_star in a
publicly bounded number of evaluations. A permissible public choice is

    tau = max(1, ceil(log(1/zeta))),
    N = ceil(log_2(r/zeta)).

At most N midpoint evaluations are needed. All use the same tau and
epsilon_f. This is an oracle reduction, not a claim that such a PDE
evaluator is free, available, or efficient.

## 3. Backward mean identity and invariant interval

Set m(t)=Pi V(t) and p(t)=Pi(V(t)^3). Periodicity eliminates the
Laplacian from the mean equation:

    m'(t)=m(t)-p(t),
    (exp(-t)m(t))'=-exp(-t)p(t).

For T>t>0, integration gives

    m(t)=exp(t-T)m(T)+integral_t^T exp(t-s)p(s) ds.

The first term tends to zero because
|m(T)|<=R exp(-sigma T). The integral converges absolutely since
|p(s)|<=R^3 exp(-3sigma s). Consequently

    m(t)=integral_t^infinity exp(t-s)p(s) ds,
    |m(t)|<=R^3 exp(-3sigma t)/(1+3sigma).

Continuity extends this to t=0. In particular |c_star|<=B, since
Pi w=0. This identity requires no backwards PDE solution and no
phase hypothesis; it is an integration of the scalar mean equation
along the supplied forward solution.

The constants +1 and -1 are stationary solutions of the actual PDE.
Comparison therefore keeps u(t)=S_t(w+b) in [-1,1] whenever its
initial datum is in that interval. This use of the invariant interval
is valid even if the separately supplied V is not initially in it.
V's own bound is supplied, not inferred from u.

Under the additional root assumptions every c in I has

    ||w+c||inf <= r/8+r/4 = 3r/8 <= 3/8.

Thus the invariant interval applies uniformly to every trajectory
queried by the root algorithm. For V itself the root assumptions also
give ||w+c_star||inf<=r/4, although this extra fact is unnecessary
for the comparison envelope used in (B).

## 4. Independent signed-difference calculation

For h>0, order preservation gives u>=V. Set y=u-V. Expanding the
cubic yields the exact equation

    y_t = L y + y - y^3 - 3V y^2 - 3V^2 y,
    y(0,x)=h.

For h<0, order preservation gives V>=u. Set y=V-u. Here u=V-y, so

    V^3-(V-y)^3 = 3V^2 y - 3V y^2 + y^3,

and the exact equation is

    y_t = L y + y - y^3 + 3V y^2 - 3V^2 y,
    y(0,x)=|h|.

Equivalently, for s=sign(h),

    y_t = L y + y-y^3-3sV y^2-3V^2 y.

The quadratic term reverses sign; the V^2 term does not. These are
the actual PDE difference equations in both cases.

Order preservation itself can be seen directly: u-V solves a linear
parabolic equation with coefficient
1-(u^2+uV+V^2), bounded on every finite time slab by the actual bounds
on u and V. The sign of the initial constant is therefore preserved.

The actual y satisfies

    0<=y<=|u|+|V|<=1+R exp(-sigma t)<=1+R.

It follows pointwise that

    |-3sV y^2-3V^2 y|
      <= (3|V| y+3|V|^2)y
      <= epsilon(t)y.

Hence y is a supersolution for
z'=(1-epsilon(t))z-z^3 and a subsolution for
z'=(1+epsilon(t))z-z^3. The scalar initial values are |h|.

This is not circular: the reaction bound is established for the
already bounded actual y, before comparing it to any scalar solution.
On a finite time slab scalar solutions are bounded and the cubic
reaction is locally Lipschitz. Applying parabolic comparison to these
sub/supersolution inequalities gives

    z_minus(t)<=y(t,x)<=z_plus(t).

For example, the difference y-z_plus satisfies a linear inequality
whose coefficient is
1+epsilon(t)-(y^2+y z_plus+z_plus^2). The parabolic maximum principle
with zero initial difference proves the upper bound. The lower bound
follows from z_minus-y in the same way. No global monotonicity of the
cubic reaction in its scalar argument is required.

## 5. Scalar formula, perturbation ratios, and absolute output

For z'=(1+a(t))z-z^3, z(0)=x>0, set A(t)=t+integral_0^t a(s) ds.
The transformation q=z^(-2) gives

    q'=-2(1+a(t))q+2,
    q(t)=exp(-2A(t))
         [x^(-2)+2 integral_0^t exp(2A(s)) ds].

Taking the positive reciprocal square root yields exactly

    z(t)=x exp(A(t))
         /sqrt(1+2x^2 integral_0^t exp(2A(s)) ds).

The denominator is positive for every finite t. For the continuous
coefficients used here this formula supplies global nonnegative
scalar solutions. At x=0 the solution is identically zero; no
division by x is used in that case.

Write H(t)=integral_0^t epsilon(s) ds. Then 0<=H(t)<=E. For
a=+epsilon, exp(2A(s))>=exp(2s), while exp(A(t))<=exp(E)exp(t).
Thus

    z_plus(t)<=exp(E) phi_t(x).

For a=-epsilon, exp(2A(s))<=exp(2s), while
exp(A(t))>=exp(-E)exp(t). Therefore

    z_minus(t)>=exp(-E) phi_t(x).

Combining these with the actual parabolic comparison proves (B)
uniformly for every time and every nonzero initial shift. In
particular no estimate deteriorates as |h| tends to zero.

For 0<=x<1,

    phi_t(x)^2 = x^2 exp(2t)/(1-x^2+x^2 exp(2t)) <= 1.

Because exp(E)-1 >= 1-exp(-E), (B) implies
|y-phi_t(|h|)|<=exp(E)-1. Since
u=V+sign(h)y and phi_t is odd, this proves

    ||u(t)-phi_t(h)||inf
      <= R exp(-sigma t)+exp(E)-1.

For h=0 this inequality follows separately from u=V.

Finally take 0<h<=h_max and z=exp(t)h. Direct algebra gives

    phi_t(h)/Psi(z)
      = sqrt((1+z^2)/(1+z^2-h^2))
      = (1-h^2/(1+z^2))^(-1/2).

Its value lies between 1 and (1-h_max^2)^(-1/2). Because
0<Psi(z)<=1, the absolute difference is at most
(1-h_max^2)^(-1/2)-1. Negative h follows by oddness, and h=0
gives two zeros without a ratio. The triangle inequality proves (A).

For a fixed sigma>0 and fixed proportionality constant K, choosing
h_max=K R<1 makes the displayed bound tend to zero as R tends to
zero. This is a conditional modulus for trajectories and admissible
data satisfying the hypotheses. It does not construct such a family.
No bound uniform in sigma down to zero is asserted or needed.

## 6. Trial shifts, root signs, and the sharp root rate

R>0 gives B>0 and D>0. Under the root assumptions
D<=r/16<=1/16, so all trial shifts below have magnitude less than 1.
For a fixed finite tau>=0 set

    a_tau = D exp(-(1+3sigma)tau).

Then

    |c_star +/- a_tau| <= r/8+r/16 = 3r/16 < r/4.

Both trial values lie strictly inside I; their actual initial data
therefore belong to the invariant interval. Estimate (B) applies to
each. A previous choice of output h_max imposes no extra constraint
here: (B) was proved independently of h_max, or it may simply be
reinstantiated with h_max=r/16.

The scalar numerator is

    a_tau exp(tau)=D exp(-3sigma tau),

and its denominator satisfies

    a_tau^2(exp(2tau)-1)
      =D^2[exp(-6sigma tau)-exp(-(2+6sigma)tau)]
      <=D^2.

Consequently

    exp(-E) phi_tau(a_tau)
      >= exp(-E)D exp(-3sigma tau)/sqrt(1+D^2)
      >= sqrt(2) B exp(-3sigma tau).

The last inequality uses D<=1 and D=2 exp(E)B. No positive lower
bound on sigma beyond sigma>0 enters this calculation.

The positive trial flow is at least V(tau) plus this constant at
every spatial point. Since |Pi V(tau)|<=B exp(-3sigma tau),

    f_tau(c_star+a_tau)
      >= (sqrt(2)-1)B exp(-3sigma tau)>0.

The negative trial flow is at most V(tau) minus the same constant,
and hence

    f_tau(c_star-a_tau)
      <= -(sqrt(2)-1)B exp(-3sigma tau)<0.

These signs are strict even at tau=0. They establish the sharp
candidate bracket of width 2D exp(-(1+3sigma)tau). The proof does
not divide the mean residual by the global lower slope exp(-2tau).

## 7. Monotonicity, continuity, uniqueness, and the buffer

For c2>c1 in I, let u_i=S_t(w+c_i) and d=u_2-u_1. Then

    d_t=L d+q(t,x)d,
    d(0,x)=c2-c1,
    q=1-(u_2^2+u_2 u_1+u_1^2).

Both u_i are in [-1,1]. The quadratic sum is nonnegative because

    u_2^2+u_2 u_1+u_1^2
      = (u_2+u_1/2)^2+3u_1^2/4,

and is at most 3 by the invariant interval. Thus -2<=q<=1.
The positive spatial constants
exp(-2t)(c2-c1) and exp(t)(c2-c1) are respectively a subsolution
and supersolution of this actual linear equation. Comparison gives
their pointwise lower and upper bounds on d. Averaging proves (D).

The upper bound makes f_tau Lipschitz and therefore continuous.
The lower bound makes it strictly increasing. The intermediate
value theorem applied to the two strict signs in Section 6 gives
one zero c_tau between the trial values; strict increase gives
uniqueness on all of I. This proves (C).

It also proves

    |c_tau|<=|c_star|+a_tau<=3r/16.

Since the endpoints of I are +/-4r/16, each is at least r/16 from
the root. No derivative of f_tau or of a graph map is needed.
At tau=0 one has f_0(c)=c and c_0=0, consistent with the bound
|c_star|<=B<=D proved above.

## 8. Public buffered bisection and its error budget

R14b permits any public tau>=1 for which
D exp(-(1+3sigma)tau)<=zeta/2. The explicit choice in Section 2
requires no access to c_star, V, or numerical values of the graph
constants. Indeed zeta<r<=1 implies tau>=log(1/zeta), and

    D exp(-(1+3sigma)tau)
      <=D exp(-tau)<=D zeta<=zeta/16<zeta/2.

Thus the promise D<=r/16 suffices to certify the public time choice.
One may also use the source's less specific choice based on known
fixed constants. The stronger time choice above does not change the
source's claimed error or introduce a new assumption.

Initialize the closed interval [ell,u] to I. At a midpoint m, suppose
|fhat(m)-f_tau(m)|<=epsilon_f.

- If fhat(m)>epsilon_f then f_tau(m)>0, so strict monotonicity
  places the root below m; keep [ell,m].
- If fhat(m)<-epsilon_f then f_tau(m)<0, so the root is above m;
  keep [m,u].
- Otherwise |fhat(m)|<=epsilon_f, hence
  |f_tau(m)|<=2epsilon_f. The lower bound in (D), applied between
  m and the root, gives

      |m-c_tau|<=exp(2tau)2epsilon_f=zeta/4.

  Return m in this case. Equality at either tolerance boundary is
  included in this safe early-return branch.

Every retained interval contains c_tau. Its initial length is r/2.
After N=ceil(log_2(r/zeta)) halvings its length is at most zeta/2,
so its midpoint is within zeta/4 of c_tau. Return that midpoint
if no early return has occurred. Thus in either branch, using even
the source's weaker time requirement,

    |returned_value-c_star|
      <=zeta/4+zeta/2=3zeta/4<zeta.

No approximate endpoint sign certification is needed. In particular,
the geometric root buffer is not silently converted into a stronger
endpoint-oracle error allowance. Bisection begins with the bracket
already certified by the analytic proof.

All midpoint estimates may be chosen adversarially or adaptively
within their absolute-error allowance; the proof uses no independence
or probability. The rule has at most N evaluations and no sign
refinement loop. It is syntactically finite for any finite sequence
of returned values, but the approximation guarantee is only on the
stated mean-evaluation and stable-trajectory promises.

Both tau and N are O(1+log(1/zeta)). Also

    log(1/epsilon_f)=2tau+log(8/zeta)
                     =O(1+log(1/zeta)).

For zeta proportional to exp(-T) with fixed proportionality
constant, these quantities are O(1+T) once 0<zeta<r. This counts
requested accuracy and outer evaluations only. It does not bound
the computational cost of an evaluation or of representing w.

## 9. Assumptions exposed and claims deliberately left open

The regularity requirement is the actual comparison-compatible flow
assumed by R14b. Integration of the mean at t=0 can be obtained by
continuity from positive times, so classical differentiability of
w at t=0 is not an extra condition. Scalar equations use continuous
coefficients, and no stochastic or formal differentiation is involved.

The constants R and sigma must bound the same supplied V for all
t>=0. A decay bound only after an unspecified burn-in would require
a separate time translation and a verified new initial datum.
The pointwise invariant-interval assumption belongs to the actual
u datum in (A), not merely to its spatial mean.

For a family of w, uniform conclusions require common certified
R,sigma,r and the displayed D smallness. Existence of a decaying
trajectory for one w does not produce such a uniform family. The
condition D<=r/16 is explicit and is not a consequence of positive
sigma alone. In particular the audit has not solved a radius-choice
or graph-construction problem.

The root algorithm does not need to know c_star. It does need a
representation of its supplied w sufficient for the promised actual
mean evaluations, a public starting radius r, and an evaluator that
returns each estimate in finite time with the stated deterministic
absolute error. Rounding costs and numerical certification remain
with that separately proved evaluator. No bit-cost theorem follows.

The accepted statement is conditional for every kappa>0, because
the local comparison uses no spectral information. This does not
assert that the needed stable graph or uniform burn-in exists for
every kappa. Specifically, none of the following is discharged:

- Construction of a graph for every fixed 2pi^2 kappa>1, or a
  uniform burn-in from the full signed input class.
- A global phase A, a singular G transform near +/-1, or phase
  smoothness and derivative bounds.
- The weighted-L1 third derivative of a new local proxy, its
  localized influence bounds, or the full signed lower prior.
- New near/far branch constants, long-time output budgets for the
  full algorithm, or an extension of its upper sampler.
- A known-profile mean solver, Gate A for changed diffusivity,
  a shared arithmetic representation, or a full query/work theorem.
- Numerical validation, Lean coverage, formal PDE correspondence,
  external publication, or a novelty claim.

D31's accepted sampler for its existing kappa=1 setting and T74's
separate Gate-A review are unaffected. R14 remains an unaccepted
extension plan. Root review and a separate integration decision are
still required before using this local lemma in a larger theorem.

## 10. Audit completion record

The two signed equations, zero case, scalar formula, ratio directions,
actual-solution comparison, invariant interval, backward mean identity,
root signs at all finite tau including zero, strict monotonicity,
continuity, root buffer, public schedule and finite bisection budget
were derived independently above.

No repair to R14b's statement or constants is requested. The explicit
regularity convention, the harmless re-instantiation of h_max for the
root trials, the upper increment bound, and the public integer schedule
are clarifications a later theorem should retain.

Tool activity was read-only source/context inspection, working-tree
inspection, SHA-256/line-count checks, and writing/reading this one
audit file. No numerical program, symbolic experiment, PDE solve,
test suite or Lean build was run. No source proof, accepted ledger,
run metadata, code, formal file or protected evidence was edited.
The final audit SHA-256 is reported in the handoff after the file is
frozen; it is not embedded in its own hashed bytes.
