# R14: candidate extension to the natural one-unstable-mode regime

Date: 2026-09-29. Research plan and candidate lemmas ONLY. No accepted
claim, numerical result, or Lean coverage is extended by this note.
The route avoids relying on the previously constructed global phase A.
Every candidate lemma below requires a full derivation and independent
review before use.

## Precise proposed extension

On the unit torus consider

    u_t = kappa Delta u/2 + u - u^3,  kappa>0.

The first nonconstant heat eigenvalue is lambda1=2 pi^2 kappa.
The proposed regime is lambda1>1, with nu=lambda1-1>0 fixed. Only
the constant mode is then unstable at zero. The current accepted
theorems use kappa=1 and substantially stronger decay in their global
phase estimates. Larger fixed tori can be rescaled to this formulation;
the input norm and query coordinates must be transformed explicitly.
No conclusion is proposed at lambda1=1 or with several unstable modes.

Keep the same full signed C^s initial class and ideal value-query model.
The candidate target is the same exponent 2d/(2s+d) for queries, and
conditionally for ideal work after the corresponding base-value gate.
Constants may deteriorate without bound as nu decreases to zero.

## 1. Stable graph without a large spectral gap

For any fixed 0<sigma<nu, the centered heat bound
||B_t||<=M exp(-nu t) gives the Lyapunov–Perron operator bound

    C = M/(nu-sigma) + 1/(1+sigma).

Choosing R sufficiently small gives the same cubic contraction and
all fixed-order derivatives as T65. No j*sigma<nu restriction is
introduced: differentiated terms contain the same small feedback and
lower-order products. This needs exact correspondence to the actual
PDE, including uniform finite burn-in to the graph neighborhood.

The T69 sampling calculation formally uses only nu>sigma>0 and the
smallness CR^2<=1/8. A complete extension must redo its normalized
Fourier envelope with the new eigenvalue and count every primitive;
changing a symbol in its final theorem is insufficient.

## 2. A local graph coordinate can replace the global phase

Let V(t) be the decaying graph solution starting from
w+Theta(w), with ||V(t)||<=R exp(-sigma t). For a nearby datum
w+b, put h=b-Theta(w). The actual difference y=u-V satisfies

    y_t = kappa Delta y/2 + y-y^3-3Vy^2-3V^2y,
    y(0,x)=h.

For h>0, scalar parabolic comparison keeps y positive and bounds it
between scalar equations with the displayed perturbations bounded by
R exp(-sigma t). For h<0 use the sign-reversed equation; h=0 is the
graph solution itself. The candidate conclusion is: for every fixed
epsilon>0, choose R small enough (depending on sigma,epsilon) so that

    sup_(t>=0,x) |u(t,x)-Psi(exp(t)h)| <= epsilon,
    Psi(z)=z/sqrt(1+z^2),

throughout an explicitly buffered local graph neighborhood.

Suggested proof: until the comparison solution reaches 1-epsilon,
apply G(z)=z/sqrt(1-z^2) to the positive comparison equations. Its
logarithmic relative perturbation is integrably bounded by a constant
depending on epsilon times
R exp(-sigma t)+R^2 exp(-2sigma t). This controls its relation to
exp(t)|h| uniformly even when h is arbitrarily small. Once that
threshold is reached, comparison for the original u should trap it
near the stable equilibrium, with a separately verified buffer.
The latter step must be proved; an unbounded derivative of G near one
must not be ignored. This candidate is an ABSOLUTE output estimate,
not a claim that a globally smooth asymptotic phase exists.

After fixed burn-in, H(v)=Pi S_Lv-Theta(QS_Lv) would then directly
approximate the long-time output by Psi(exp(T-L)H(v)). Near/far
branch conditions and every error budget must be restated. A small
stable graph by itself does not prove this output estimate.

## 3. Lower-bound bridge using H rather than A

Near zero set Atilde(v)=exp(-L)H(v). It is odd and smooth, with
D Atilde(0)=Pi and D^2 Atilde(0)=0. The missing quantitative claim is

    |D^3 Atilde(v)[h1,h2,h3]|
       <= B ||h1||infinity ||h2||infinity ||h3||L1

on a fixed small ball, uniformly over spatially localized directions.
It cannot be inferred merely from a sup-norm operator bound.

Potential route: use actual translation-invariant heat/tree envelopes
for finite burn-in and stable-graph derivative measures, root them at
the uniform spatial measure, and bound all but one direction by their
sup norms. A translation-invariant finite positive marginal is a
constant multiple of Haar measure, which would give the required L1
bound. All absolute envelopes, derivative interchanges and finite
variation must be justified. Cauchy–Schwarz alone would give an L2
bound and would not discharge this gate.

If proved, the unconditioned balanced-layer argument of D28 can be
revisited with F=Atilde-Pi. It still needs the actual PDE separation
from Section 2, correct constants, the genuine signed input class,
and the same adaptive expected-query information argument. None of
those checks is waived by the shared proposed exponent.

## 4. Deterministic base computation without global A

A possible graph evaluator uses the finite-time mean

    f_tau(c)=Pi S_tau(c+w)

instead of exp(-tau)G(Pi S_tau(c+w)). It is strictly increasing.
The proposed quantitative bridge is that its unique zero c_tau in
a fixed buffered interval satisfies

    |c_tau-Theta(w)| <= C R^3 exp(-(1+3sigma)tau).

At the graph point, its mean is bounded by
R^3 exp(-3sigma tau)/(1+3sigma) from the backward mean equation.
To obtain the extra exp(-tau), one must prove an exp(tau) lower
response for perturbations staying close to the decaying graph.
The crude global lower derivative exp(-2tau) alone does NOT prove
the asserted root error when sigma is small.

For numerical sign tests away from the root, the crude derivative
bound can still be used: known trajectories in the invariant unit
interval give f_tau'(c)>=exp(-2tau). Thus deterministic PDE errors
of size O(zeta exp(-2tau)) suffice for buffered bisection to zeta.
With tau=O(log(1/zeta)), all requested logarithmic precisions are
O(T). A separately accepted T70-type known-profile solver could then
be applied. Root existence, brackets, the sharper near-graph response,
and off-promise total rules must all be proved explicitly.

## Next bounded task and status

First investigate Sections 2 and 4: either prove the uniform local
output and root estimates with explicit buffers, or provide a precise
obstruction. These are independent of coding and cannot be settled by
plots. Then audit Section 3 and the complete query/work correspondence.
Do not promote a spectral-gap extension, change D29/D30, or start
experiments from this proposal. T73/T74 acceptance of the current
kappa=1 work gates remains a separate active task.
