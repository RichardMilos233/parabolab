# Candidate sharp moment–work frontier at a finite integrable endpoint

Status: conventionally proved and independently reviewed in T22, with the
endpoint derivative and support qualifications incorporated. The separate
finite/measure Lean gate T23 is in progress; no numerical or priority claim.
This extends the T19 observation
that finite absolute expectation can coexist with an unavoidable variance–work
tradeoff. The Hölder inequality itself is standard.

An explicit primary predecessor for the p=2 cost criterion is Theorem 1 of
[Cugini, Atif and Subaşı, 2026](https://arxiv.org/html/2603.13495v1), which
minimizes the product of mean cost and a second-moment bound with density
proportional to the target density divided by square-root cost. That algebra
matches Section 1 after normalizing |nu|. The potential distinct content here
is the coding-tree endpoint classification in Sections 2–5, whose priority
has not been established; the generic optimization is not claimed new.
The ODE generating-function framework likewise has a classical predecessor
in [Bergeron–Flajolet–Salvy (1992)](https://algo.inria.fr/flajolet/Publications/BeFlSa92.pdf).
The proof below uses a real fractional-integral test rather than requiring
complex coefficient asymptotics; that choice is a proof route, not by itself
a novelty claim.

## 1. Fixed-tree measures and the optimization criterion

Let nu be the finite signed canonical measure on completed trees at a fixed
query and horizon. A tree has actual full syntactic node count N>=1. A proposal
Q supports |nu| and returns the exact likelihood output H=dnu/dQ. Fix p>1 and
put beta=(p-1)/p, S_p=integral N^beta d|nu|. If both expectations are finite,
Hölder's inequality gives

    S_p = E_Q[|H| N^beta]
        <= (E_Q|H|^p)^(1/p) (E_Q N)^((p-1)/p).

Thus finite pth output moment together with finite mean node work requires
S_p<infinity. This statement concerns the fixed full tree and its cost. It
does not cover combining opposite-sign trees, short-circuiting all zero leaves,
analytically integrating nonzero subtrees, or choosing a different representation.

Conversely, assume nu is nonzero and S_p<infinity. Define

    Z_p = integral N^(-1/p) d|nu|,      0<Z_p<infinity,
    dQ_* = Z_p^(-1) N^(-1/p) d|nu|.

Then H_*=Z_p sign(dnu) N^(1/p), and

    E_Q* |H_*|^p = Z_p^(p-1) S_p,
    E_Q* N = S_p/Z_p.

Both are finite, and equality holds in the Hölder product. This establishes
an existence characterization among arbitrary global tree proposals. It does
not construct sampleable local transition probabilities or supply the unknown
normalization Z_p. If a proposal is additionally required to support syntactic
zero-contribution trees, mixing Q_* with a fixed positive-rate full-support law
having finite expected node count preserves finiteness of both quantities,
although equality in the optimal product is then generally lost.
Existence of this auxiliary law is an additional condition for a general
tree space. For the original bounded-arity coding mechanism here, a fixed
positive exponential clock and positive label probabilities give such a
full-support law at the finite horizon; its expected population is bounded
by a finite exponential in that horizon.

For p=2, the criterion is integral sqrt(N) d|nu|<infinity, and

    (E_Q H^2)(E_Q N) >= [integral sqrt(N) d|nu|]^2.

## 2. An explicit smooth globally solvable family

Consider a constant zero datum and the scalar reaction

    f_alpha(y)=(1+y^2)^(-alpha),     alpha>0.

The signed ODE u'=f_alpha(u), u(0)=0 is global because 0<f_alpha<=1.
The original derivative-coded tree has nonnegative absolute terminal-jet
series

    Phi_alpha(z) = sum_(k>=0) |f_alpha^(k)(0)| z^k/k!
                 = (1-z^2)^(-alpha),       0<=z<1.

The reviewed D11 constant-data theorem gives

    tau_alpha = integral_0^1 (1-z^2)^alpha dz
              = sqrt(pi) Gamma(alpha+1)/(2 Gamma(alpha+3/2)),
    Z_alpha' = Phi_alpha(Z_alpha) for 0<=t<tau_alpha,     Z_alpha(0)=0,
    W_I(t)=Z_alpha(t) for 0<=t<=tau_alpha,
    W_I(tau_alpha)=1,                 W_I(t)=infinity for t>tau_alpha.

Thus nu at the critical time is finite and has total variation exactly one.
The endpoint value is the continuous extension; the differential equation
is not asserted with a finite derivative at t=tau_alpha.
No numerical divergence is needed to assert this endpoint property.

The signed tree expectation equals the global ODE solution at this endpoint.
For t<tau, the analytic coefficient recursion agrees with the ODE locally,
and hence on the connected interval of absolute convergence by uniqueness.
Each coefficient is dominated by the corresponding nonnegative tree mass;
their sum remains finite at tau. Dominated passage in the signed coefficient
series then gives the continuous ODE endpoint value. T22 records this bridge
separately; mere finiteness of the absolute series is not used as a substitute
for correspondence.

## 3. Time degree equals full node count

For a nonzero completed Id tree at constant zero datum, the Id root must
branch once to F0. Any spatial derivative code gives zero contribution.
Every other nonzero internal event is a binary reaction event. If there are
n internal events in total, there are n-1 such binary events and one unary
Id event. The full tree therefore has exactly 2n nodes.

The fixed-tree Brownian integrals are one, and the n ordered event-time
integrals scale as t^n. Its terminal weights do not depend on t. Grouping
positive canonical weights by n gives coefficients c_n>=0 with

    Z_alpha(t)=sum_(n>=1) c_n t^n,
    integral N^beta d|nu_tau| = 2^beta sum_(n>=1) n^beta c_n tau_alpha^n.

This uses completed-tree exhaustion and Tonelli, not a differentiation of an
infinite endpoint moment. It counts the whole sampled tree even when the
implementation could detect a zero factor early. The assertion must be
rechecked if the cost definition or expansion is changed.

## 4. The endpoint cusp gives an exact fractional-moment test

Set gamma=1/(alpha+1). Since

    tau_alpha-t = integral_(Z_alpha(t))^1 (1-z^2)^alpha dz,

and 1-z <=1-z^2<=2(1-z) for 0<=z<=1, the gap 1-Z_alpha(t) is bounded
above and below by positive constants times (tau_alpha-t)^gamma as t rises
to tau_alpha. Therefore, as s decreases to zero,

    1-Z_alpha(tau_alpha exp(-s)) is comparable to s^gamma.

For 0<beta<1, the elementary Laplace identity and Tonelli give

    sum n^beta c_n tau_alpha^n
      = beta/Gamma(1-beta)
        * integral_0^infinity
          [1-Z_alpha(tau_alpha exp(-s))] s^(-1-beta) ds.

The integral converges at infinity. Near zero its integrand is comparable
to s^(gamma-beta-1); it is integrable exactly when beta<gamma. Equality
produces a logarithmic divergence. This argument needs no coefficient
asymptotics or Tauberian theorem.

## 5. Sharp coexistence classification, within the proposal class

Combining Sections 1–4 yields the proposed exact equivalence:

    a globally chosen exact likelihood proposal exists with
    E|H|^p<infinity and E N<infinity at t=tau_alpha
        iff (p-1)/p < 1/(alpha+1)
        iff 1<p<1+1/alpha.

In particular, finite variance and finite expected full-tree work can coexist
at the integrable endpoint iff 0<alpha<1. At alpha=1, the rational example
f=1/(1+y^2) has W_I(2/3)=1, but every supported exact single-tree proposal
has either infinite second moment or infinite expected full-tree node count.
For alpha>1 the same incompatibility holds.

For every alpha>0, bounded output together with finite mean full-tree work
is impossible at the endpoint: a bounded output has every finite pth moment,
whereas p>=1+1/alpha is forbidden. In particular, the alpha<1 positive
finite-variance case necessarily permits unbounded possible outputs.

The positive direction is an abstract measure construction, not an efficient
sampler. Sampling Q_* may be as difficult as the original integral; no local
algorithm, arithmetic complexity or approximation guarantee follows from it.
This result does not exclude a different randomized representation with finite
variance and work, nor any deterministic algorithm for the global signed ODE.

## 6. Next obligations

T22 checked the full node/time-degree identification, canonical total-variation
meaning, zero-support mixture argument and fractional-moment boundary.
The separate T23 Lean target encodes the p=2 integral Cauchy–Schwarz inequality
with square-root cost and the finite exponent equivalence. It does not encode
general Hölder, the tree measure, the endpoint cusp or the whole classification.
A subsequent numerical check, following that gate, should illustrate the
transition under the fixed `02c-critical-frontier-protocol.md` contract.
The constructive sampler candidate `04i-critical-tilted-sampler.md` has a
separate review obligation and is not promoted by this proof.
