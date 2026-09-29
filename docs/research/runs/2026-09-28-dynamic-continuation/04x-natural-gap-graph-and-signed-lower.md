# D35–D36: actual graph estimates and signed lower bounds at the natural gap

Date: 2026-09-29. Conventional mathematics accepted after independent
T79/T80 audits and full root correspondence. This extends an analytical
interface and a lower bound. It supplies no matching upper algorithm,
work upper bound, full Lean certificate or signed numerical experiment.

## Exact scope

Fix integers d,s>=1, a target point x*, and kappa>0 with

    lambda1=2pi^2 kappa>1.

On the probability-Haar unit d-torus consider the actual real equation

    u_t=(kappa/2)Delta u+u-u^3, u(0)=v.

For the complexity conclusion the unknown class is the same full signed
class as D28/D29:

    v smooth periodic, ||v||inf<=1/2,
    max_(|alpha|<=s)||partial^alpha v||inf<=1,
    min v<0<max v.

Unknown-input information is obtained only from charged exact initial
point values, including repeated and preprocessing acquisitions.
Algorithms have Borel rules and independent seeds, halt almost surely
for each input, and may be biased, adaptive, randomly stopped and have
unbounded outputs. The required uniform MSE is at most 1/16.
All constants may depend on fixed d,s,kappa. There is no uniform limit
as lambda1 decreases to one.

## D35: actual graph, uniform centered entry and a marked L1 direction

Put nu=lambda1-1 and choose a fixed sigma in (0,nu). Let

    rho=((1+exp(-lambda1))/(1-exp(-lambda1)))^d,
    M=2rho exp(lambda1), C=M/(nu-sigma)+1/(1+sigma).

Choose the same sufficiently small R in R14c and T78 and set r=R/(4M).
R14c's complete smallness conditions imply T78's weaker CR^2<=1/8
and R<=1 conditions. Both sources use exactly the same centered heat
operator, Lyapunov--Perron operator, radius-R trajectory ball, fixed-point
equation and Theta(w)=Pi U_w(0). Uniqueness identifies their graphs;
two merely similarly named coordinates are not being combined.

The resulting odd smooth graph is defined for mean-zero ||w||inf<3r,
and its actual trajectory satisfies

    ||S_t(w+Theta(w))||inf<=R exp(-sigma t).

The actual centered energy and a final one-unit heat comparison yield

    ||Q S_tq||inf<=Cw exp(-nu t), t>=1,
    Cw=2e rho exp(nu), ||q||inf<=7/8.

Thus one public finite integer L makes every centered profile Q S_Lq
at most r/64. The mean need not be small. For
H(q)=Pi S_Lq-Theta(QS_Lq), D34 now applies to these constructed
trajectories. With a scalar approximation mhat within r/16 of Pi S_Lq,
the near branch |mhat|<=r/2 obeys

    |S_(L+t)q(x)-Psi(exp(t)H(q))|<=1/32,
    Psi(z)=z/sqrt(1+z^2), t>=0.

The far branch has error at most 1/16 on returning sign(mhat), for
all sufficiently large t fixed by the graph radius. A supplied paid-g
realization of this mean approximation is conditional in R14c; no
evaluator or input access has become free through this analytical result.

Set Atilde=exp(-L)H and rho0=min(1/4,r exp(-L)/4). The independently
audited T78 proof gives an actual C-infinity odd map on the open
2rho0 ball, with DAtilde(0)=Pi, D^2Atilde(0)=0, and

    |D^3Atilde(v)[h1,h2,h3]|
      <=B3 ||h1||inf ||h2||inf ||h3||1, ||v||inf<=rho0.

Its explicit B3 is T78 equation (7.4), enlarged to max(1,B3) if
desired. The estimate uses the same fixed-point inverse in weighted
L1 and sup trajectory norms, actual finite-time variational positivity,
and the ordinary five-term chain rule. It is not deduced from a generic
multilinear product-measure representation and is not L1 differentiability
of the cubic on an open L1 ball.

## D36: discharge the conditional lower composition

Instantiate R14d's missing analytical interface with a_star=rho0 and
this B3. Its local output assumption follows from D35 and D34 whenever
||v||inf<=r exp(-L)/4. Its scale identity is exact:

    exp(T-L)H(v)=exp(T)Atilde(v).

R14d/T79 use smooth cell bumps of height a k^(-s), K=k^d cells and
the two full uniform sign layers of excess +/-ell with ell comparable
to sqrt(K). The mixed derivative estimate bounds one sign flip of
Atilde-Pi by B3 a^3 k^(-3s)/K. Finite-layer coupling and variance
then leave at most probability 1/64 of bad nonlinear-coordinate error
under either original prior. No conditioning discards those inputs.

For k=2floor((aI exp(T))^(1/(s+d/2))/2), every sufficiently large
real T has the required local amplitudes. Good positive and negative
inputs have actual PDE targets at least 91/160 and at most -91/160,
respectively. The exact point-query observation experiment remains the
same finite urn experiment as in D28. Its KL/testing and stopping
argument gives, for the full finite-prior expected query count,

    qbar>=3K/65536>=c exp(2dT/(2s+d)).

Therefore every admissible uniformly accurate algorithm satisfies

    sup_v E Q_T(v)>=c exp(2dT/(2s+d)), T>=T0.        (D36)

The finite prior is independent of the algorithm, while an expensive
member may depend on the horizon and algorithm. Any model with
Work>=Q inherits this lower inequality. This says neither that a
fixed individual input is expensive for every T nor that any upper
algorithm has been proved at the changed diffusivity.

## Evidence and outstanding scope

R14c and conditional R14d are independently audited by T79; T78 is
independently audited by T80. Root read all four full source/audit
documents, the local D34 interface, and checked the common graph,
radius, normalization, local class, prior and information model.
See reviews/T79-T80-root-correspondence.json for hash-bound evidence.

D29/D33 remain unchanged in their original kappa=1 scope. Critical
lambda1=1, multiple unstable modes when lambda1<1, arbitrary geometry,
dimension-uniform constants, finite-bit complexity, practical speed,
full Lean and novelty are not concluded here. Separate T81/T82 research
is investigating whether a fixed-burn-in route can remove the spectral
restriction altogether; it is not a premise of D35/D36.
