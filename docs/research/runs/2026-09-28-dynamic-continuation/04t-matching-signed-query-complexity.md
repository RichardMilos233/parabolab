# D27: matching query complexity for sign-changing initial data

Status: conventional theorem accepted after full independent T59 audit of
frozen T56 and R03. This synthesis preserves their scope and does not
replace their detailed proofs. No signed-algorithm Lean or numerical
certificate, arithmetic-work bound, or priority claim is asserted.

## Exact theorem and oracle model

Fix integers s>=1 and1<=d<=4s, a point x on the normalized unit torus,
and the equation u_t=Delta u/2+u-u^3. Let F consist of smooth periodic v
with supnorm<=1/2, max_(|alpha|<=s)||partial^alpha v||infinity<=1,
and min v<0<max v. Write S_Tv(x) for the actual PDE target.

An admissible algorithm obtains unknown-input information only from
charged exact v(y) values. It may choose points adaptively, use a common
private random seed, stop randomly, be biased and use a public horizon.
It must be measurable and halt almost surely on each input. Every initial
value acquisition, including input-dependent preprocessing, is charged.
Finite calculations from an already acquired transcript are permitted.
No mass, phase, derivative, evolved-solution or formula oracle is supplied.

For algorithms satisfying sup_(v in F) E|Y_T-S_Tv(x)|^2<=1/16, define

    C_T = inf_alg sup_(v in F) E Q_T(v).

There exist finite positive c,C,T0, depending on fixed d,s, such that
for all T>=T0,

    c exp(2dT/(2s+d)) <= C_T <= C exp(2dT/(2s+d)).

The upper uses a deterministic query cap. The lower is D25's finite-prior
average bound, so its expensive input can depend on T AND the algorithm.
It is not D22's common-baseline statement or D23's fixed-zero statement.
Precision is fixed; constants are not uniform in dimension/smoothness.
The restriction d<=4s includes equality. No all-dimension theorem is
accepted by this file.

## Why mass alone cannot handle signs

Let b(t)=integral S_tv, w=S_tv-b and nu=2*pi^2-1. The mean satisfies

    b'=b-b^3-R,  R=3b integral w^2+integral w^3.

The term R need not vanish even when the initial mass is zero. On the
larger analytic ball ||v||infinity<=a0=7/8, define

    G(z)=z/sqrt(1-z^2), Psi(z)=z/sqrt(1+z^2),
    A(v)=lim_(t->infinity) exp(-t)G(b(t)).

The centered energy estimate ||w(t)||2<=a0 exp(-nu*t), scalar comparison,
and the exact identity (exp(-t)G(b))'=-exp(-t)G'(b)R imply convergence
with uniform tail C0 exp(-(2nu-2)t), where

    C0=5a0^2/((1-a0^2)^(3/2)*(2nu-2)).

One-unit heat smoothing then gives, uniformly on that ball and including
A(v)=0,

    ||S_Tv-Psi(exp(T)A(v))||infinity
       <=Cw exp(-nu*T)+C0 exp(-(2nu-3)T).

For constant data c, A(c)=G(c). For nonconstant data A is a nonlinear
functional, not the initial mass. The construction below approximates it
from paid samples rather than providing it as an extra oracle.

R03 and T59 give a separate direct counterexample. For fixed c>0 and
phi=cos(2*pi*x1)+c*cos(4*pi*x1), dominated convergence in the actual
mean equation proves

    A(epsilon*phi)/epsilon^3 -> -3c/(4*(12*pi^2-2)) <0.

Choose sufficiently small fixed epsilon so both profiles ±epsilon*phi
belong to F. They have exactly the same zero initial mass, but their
solutions tend uniformly to opposite equilibria. Any possibly randomized
rule using mass alone has the same output law on these two inputs, so
liminf_T max(RMS_plus,RMS_minus)>=1. This negative result is about
mass-only information; it does not lower-bound all spatial-query rules.
Its proof does not depend on the harder derivative-measure estimates.

## Actual derivative measures, not an operator-norm shortcut

T56 Sections4 and T59 Sections2--3 prove that A is C3 on a neighborhood
of the closed ball, and that its first three derivatives are represented
by actual signed measures sigma_j(v) on(T^d)^j, with uniform finite
total-variation bounds K_j. These measures come from the differentiated
heat/Feynman--Kac/Duhamel equations, with distinct derivative labels.

At time1, every unweighted heat tree with j leaves admits a common
Gaussian shift of variance1/j: its leaf covariance satisfies
Sigma >= (1/j)11^T. The leaf law with root x is consequently dominated
by ||p_(1/j)||infinity times the uniform-root law, even with a singular
residual covariance. Removing bounded tree weights before a spatial
supremum gives the mixed kernel estimates. Their constants at time1
may be chosen as e||p1||infinity,6e^2||p_(1/2)||infinity,
60e^3||p_(1/3)||infinity.

After time1, sup-norm kernel integrals grow at most exp(jt), whereas
their centered spatial L2 counterparts grow at most exp((j-nu)t).
Every term in D^jR retains at least two centered factors. Thus its
actual measure norm is O(exp((j-2nu)t)). Combining the G derivatives
and the exp(-t) factor gives an integrable bound

    ||D^j[exp(-t)G'(b)R]||TV <= C_j exp((3j+2-2nu)t), j<=3.

Here2nu>11. The short-time tree measures have bounded total variation
without requiring a short-time mixed sup estimate. Uniform convergence
of these derivative integrals establishes both C3 regularity and the
claimed measure representations. A generic bounded multilinear operator
was not silently treated as a product-space measure.

## Constructive query upper bound and auxiliary computation

Use exactly k^d paid grid values to form a fixed smooth partition-based
local polynomial interpolant g. Total-order C^s regularity is enough:

    delta=||v-g||infinity<=Cint k^(-s),
    ||g||_(C^s,max)<=Cint.

For k above a public threshold, delta<=1/4 and ||g||infinity<=3/4.
Taylor expansion, with residual r=v-g, gives

    A(v)=A(g)+DA(g)[r]+D2A(g)[r,r]/2+remainder,
    |remainder|<=K3 delta^3/6.

A finite fine nonnegative partition of unity, the known residual
Lipschitz bound, and the derivative measures approximate the first two
terms by finite weighted point and point-pair sums. Their coefficient
l1 norms are at most K1+eta and K2+eta after deterministic approximation.
Draw M=k^d independent samples from each absolute-coefficient discrete
distribution; sign-weight them, query the residual at every sampled
point, and average. Zero-weight terms may be omitted. All repeated
points are still charged. The coarse, linear and quadratic calls total
at most k^d+M+2M=4k^d.

The coefficients and A(g) are not available as free oracles. T56
Sections6a--6d give a finite computation from the already paid coarse
values: approximate A on explicitly known perturbed profiles, use finite
differences, and use a monotone finite mesh solver for those known
profiles. Public derivative bounds through order4 give consistency
bounds; scalar comparison and the coordinate tail fix the required
finite precision. The number of auxiliary solves and mesh points can
be extremely large. They reveal no additional unknown v values, but
their arithmetic cost is NOT bounded by the query theorem.

Finite rational coefficients give implementable discrete sampling by
fair-bit rejection, with success probability at least1/2 on each draw.
Transcript clipping/saturation off promise and fixed public mesh rules
give Borel maps and almost-sure halting. This is an exact-real information
model, not a finite-bit encoding theorem for arbitrary real oracle values.

## Error balance and the endpoint d=4s

The actual phase estimate has RMS bounded by

    (K1+1)delta/sqrt(M)
    +(K2+1)delta^2/(2sqrt(M))
    +K3 delta^3/6+(5/2)eta.

Let q=s+d/2 and

    B=(K1+1)Cint+(K2+1)Cint^2/2+K3 Cint^3/6+1,
    k=max(k0,ceil((16B exp(T))^(1/q))), eta=exp(-T)/64.

Since q<=3s precisely when d<=4s, all three k-dependent errors sum
to at most exp(-T)/16, including the critical endpoint. The last term
is5exp(-T)/128. Hence phase RMS<=13exp(-T)/128. Psi is globally
1-Lipschitz; choose T0 so the PDE profile error is at most1/16.
The final PDE RMS is then at most21/128<3/16<1/4. Optional final
rounding by1/64 still yields23/128<1/4. Finally4k^d has order
exp(dT/q)=exp(2dT/(2s+d)). Combining with D25 proves the theorem.

## Evidence and remaining scope

- Author proof: T56, SHA256
  `0f0cd6a6fbe97d5746c42f2da94161284f4b4fb3da70b724b5992450388d5933`.
- Independent full audit: T59, SHA256
  `47d3ce98ac19210e9bbcd318ac1de2fb9dddd5bc372bff201dc97d47572301ab`.
- Direct mass-only counterexample: R03, SHA256
  `eecc30c81c4adea40dd3ca4e62d29c58c81097257c4832175794627eff840fef`.
- Lower theorem: frozen04r/T50/T53, with exactly the same class and
  worst-case expected-query quantifiers.

Classical randomized integration, control variates and gap-majority
lower bounds are explicit predecessors. T55/T59's bounded literature
checks are not proof of worldwide originality. The possible contribution
is the uniform nonlinear PDE transfer and its query-model construction.
T60 identifies substantial missing Lean infrastructure for the lower
information argument. The positive T51/T52 gate does not formalize this
signed algorithm. No signed numerical run or practical speed claim follows.
