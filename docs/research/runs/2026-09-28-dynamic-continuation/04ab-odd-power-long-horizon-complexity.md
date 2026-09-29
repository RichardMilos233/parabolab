# D45–D46: odd-power long-horizon complexity and physical scaling

Date: 2026-09-29. Accepted conventional result after independent T96 and
root correspondence. Full PDE/algorithm formalization and numerical
performance are separate; this is not a novelty or significance verdict.

## Frozen proof and independent review

The 1266-line proof is
`reviews/T94-odd-power-long-horizon-feasibility.md`, SHA256
`2600c29a2823aefd9a69578de113bc511179d97bdfbea7eb3a6861ac28b7e1d9`.
The independent 944-line audit is
`reviews/T96-odd-power-long-horizon-independent-audit.md`, SHA256
`b8f5f32be92c820bd8b955c5969406a49fa21e12a1b38c86d17bb7467ba1eda4`.
T96 found no required mathematical repair. Its eleven typographical line
join artifacts were removed before freeze; the mathematical statement did
not change. Root read the proof and audit content and checked the repaired
passages and locked sources. Detailed acceptance is in
`reviews/T96-root-correspondence.json`.

## D45: every fixed normalized odd power

Fix integers p,d,s>=1 and kappa>0. On the normalized unit d-torus let S_t
be the actual bounded solution flow of

    u_t=(kappa/2) Delta u+u-u^(2p+1).

The unknown initial datum belongs to exactly the full signed class

    V={v smooth real periodic: ||v||inf<=1/2,
       max_(|alpha|<=s)||partial^alpha v||inf<=1,
       min v<0<max v}.

No mean margin, basin, analytic radius, bound above derivative order s, or
restriction on the number of unstable spatial modes is imposed. The oracle
returns only an exact scalar v(x). Preprocessing and repeated queries count.
Algorithms may be biased, adaptive, randomized with an input-independent
seed, and almost-surely stopped. All rules and outputs are measurable.

Let Q_point(T) be the infimum worst-input expected query count at a fixed
prescribed spatial point with RMS tolerance 1/4. Define Q_profile(T) using
finite explicitly indexed real Fourier outputs and the strong profile loss

    sup_(v in V) E||U_T-S_Tv||inf^2 <=1/16.

The supremum in space is inside the expectation. Then, with

    gamma=2d/(2s+d),

both quantities are Theta(exp(gamma T)) for all sufficiently large real T.
This exact query order extends the cubic conclusion to every fixed p.

More precisely, put J=ceil(1+d/(2s)), a0=2d^2+20d+50 and
A=a0+d^2+2d+2. For each T>=2 the constructed algorithm has

    sup_v (E||U_T-S_Tv||inf^2)^(1/2)<=1/8,
    queries <=[1+J(J-1)/2] k^d on every seed,
    k^d<=C exp(gamma T),
    sup_v E Work <=C exp(gamma T)(1+T)^A.

Its finite output has at most C(1+T)^(3d^2+9d) real entries. A prescribed
point evaluation costs polynomial work and no new queries. A separate
constant-work deterministic patch gives error <=3/32 for 0<=T<=2.

Paid work counts queries, arithmetic, comparisons, floor/ceiling, indexing,
stored-value operations, exp/log/sin/cos, positive square roots and scalar
uniform/exponential/Gaussian draws. Fixed public constants and ideal finite
integer/address words are allowed. Fourier transforms, integration and
evolved PDE values are computed, not supplied as free oracles. At the common
RMS tolerance 1/4 the work conclusion is only

    c exp(gamma T)<=W_point(T),W_profile(T)
                      <=C exp(gamma T)(1+T)^A.

This matches the exponential rate, not exact Theta paid work or bit cost.
Constants can depend on p,d,s,kappa and need not be numerically moderate.

## Why the extension needs a new proof

For D=2p+1 an actual bounded D-ary parent rule is

    M(y)=(sum_i y_i-product_i y_i)/(D-1),   lambda=D-1.

Its cube values lie in [-1,1], and lambda(M(z,...,z)-z)=z-z^D.
The first-branch equation identifies the resulting bounded tree expectation
with the PDE. D43/D44 then give the actual derivative field, including a
hard j-query cap, whole-vector Gaussian reconstruction and counted linear
tree preparation. This specializes classical branching/voting ideas; no
novelty is assigned to the parent rule or Gaussian recursion.

The time-one bound is degree dependent:

    ||S_1v||inf <= sigma_p
      =[1+(2^(2p)-1)e^(-2p)]^(-1/(2p))<1.

The smooth saturation must therefore use an identity interval containing
[-sigma_p,sigma_p]. Its Lipschitz bound stays 25, but its Gevrey constants
depend on p. Simply reusing the cubic interval would be unjustified.

T94 proves a paid known-profile solver for the new degree: Gevrey initial
tail, complex spatial smoothing, Galerkin error bootstrap, complex-time
startup and later panels, finite Picard iteration and explicit scalar
convolution weights. Polynomial evaluation uses padding strictly greater
than 2DH. Both spatial and numerical trajectories are bounded by error
bootstraps, not by a spectral maximum principle. Its counted work preserves
the stated exponent and allows a polynomial horizon factor.

For the lower bound, the prior remains the complete pair of uniform sign
slices. The actual time-one mean correction has the mixed-L1 third
derivative constant

    B_D=e^2[D(D-1)(D-2)+(3/2)D^2(D-1)^2].

Slice concentration makes the time-one profile small while preserving its
signed mean. Monotonicity of z^D controls centered L2 energy; scalar
comparison and a final heat smoothing step separate the actual PDE targets
by at least 91/160 for every fixed positive diffusion after a finite
threshold. No good-event conditioning changes the prior. Finite-word KL,
arbitrary seed handling, padding and truncation then give the lower bound
for adaptive, biased and randomly stopped algorithms.

## D46: physical coefficients require explicit class and tolerance scaling

For a,b>0 consider

    u_t=(kappa/2) Delta u+a u-b u^(2p+1),
    R=(a/b)^(1/(2p)),   u(t,x)=R z(a t,x).

The normalized diffusion is kappa/a. On the explicitly scaled input class
R V, at physical RMS tolerance R/4, the point and strong-profile query
order is Theta(exp(gamma a T)). The constructed physical RMS is <=R/8,
and the paid-work upper retains a polynomial factor in 1+aT. One physical
query and a scalar division give one normalized query; output scaling is
also counted. Neither amplitude scaling nor the change of notation removes
a from the physical-time exponent.

There is a concrete counterexample to transferring this lower bound while
keeping the original class V and tolerance 1/4. Choose b=a8^(2p), hence
R=1/8. Comparison from initial constants +/-1/2 shows that whenever

    aT >= log(1+2^(-2p))/(2p),

every promised solution has sup norm at most 1/4. The zero Fourier
polynomial then meets the original point and profile tolerance with zero
queries and constant work. The scaled theorem and this unchanged-class
problem are different mathematical questions.

## Coverage and remaining work

This result concerns each prescribed horizon, not simultaneous accuracy
at every time. It is not degree uniform or uniform as kappa tends to zero,
and it does not prove the same order for arbitrary inward polynomials,
fractional or variable diffusion, or systems. Existing Lean modules verify
several finite probability/statistical components, including T89 and T93;
they do not formalize this full PDE/solver/lower-bound composition.

No new numerical run or input acquisition accompanies D45/D46. E5 remains
a separate frozen fixed-time component diagnostic using the earlier cubic
and rate-five quintic rules. Generalized long-time measured performance,
finite-precision stability, publication priority and major significance
remain unresolved.
