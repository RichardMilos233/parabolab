# D49: fractional odd-power long-horizon query complexity

Date: 2026-09-29. Conventional theorem and root correspondence checkpoint.
The frozen upper T101 and lower T102, independent audits T104 and T103,
and root complete reading establish the statement below. This checkpoint
is not a full Lean proof, executed fractional solver, numerical accuracy
certificate, practical speed claim, or originality assessment.

## 1. Same problem, same input class, matching information cost

Fix integers d,s,p>=1 and real parameters c>0, 0<beta<=1. On the unit
d-dimensional torus with normalized Haar measure, consider the actual flow

    u_t=-c(-Delta)^beta u+u-u^(2p+1),
    (-Delta)^beta exp(2*pi*i*nu.x)
      =(4*pi^2*|nu|^2)^beta exp(2*pi*i*nu.x).

The unknown class is exactly

    V={v smooth real periodic: ||v||inf<=1/2,
       max_(|mu|<=s)||partial^mu v||inf<=1,
       min v<0<max v}.

There is no mean margin, prescribed basin, higher-derivative bound,
analytic radius, or stable-mode restriction. One information acquisition
returns the exact scalar v(x); every acquisition is counted, including
preprocessing, repeats and zero values. Set

    q=s+d/2,       gamma=d/q=2d/(2s+d).

At each prescribed real horizon T, algorithms may be biased, adaptive,
privately randomized and inputwise almost surely terminating. Point loss
is at a prescribed x*. Strong profile loss is

    sup_(v in V) E||U_T-S_Tv||inf^2,

with the spatial supremum inside expectation and an explicitly indexed
finite real Fourier output. At RMS tolerance 1/4, the infimum of
worst-input expected acquisition counts satisfies, for all sufficiently
large T,

    Q_point(T)=Theta(exp(gamma T)),
    Q_strong_profile(T)=Theta(exp(gamma T)).

Constants and the threshold can depend on d,s,p,c,beta. The upper in
fact has strong RMS<=1/8 and an all-seed deterministic acquisition cap.
The lower covers the larger class of arbitrary expected-cost algorithms.
This difference strengthens rather than weakens the matching conclusion.

The exponential power does not depend on beta or positive c, when these
are fixed before T varies. Uniform constants as beta or c approach zero
are not asserted. At c=0 a single exact query at x* and the scalar flow
give the exact point target; the positive-diffusion qualification matters.

## 2. Fully charged upper construction

Write D=2p+1, alpha=2beta, theta=min(1,alpha), and

    eta=ceil((2d+8)/theta),
    a_solver=eta*d+5d+20,
    A_work=a_solver+ceil(d(d+2)/theta)+2,
    A_array=eta*d+ceil(d(d+1)/theta).

The exact-real model charges arithmetic, elementary exp/log/sin/cos,
positive square roots, finite integer/index operations, memory access,
scalar random primitives and each unknown input acquisition. Fixed public
constants and ideal finite index words are permitted. It supplies no PDE,
integral, stable-law or Fourier-coefficient oracle.

The paid known-profile solver accepts an actual evaluator q0 with
||q0||inf<=1 and a declared Gevrey-2 norm at radius rho0/R bounded by B,
where R>=1 and B,rho0 are fixed. For S>=0,P>=1, let

    E=1+P+S+log(R+1),      H=ceil(C R E^eta).

Its finite Fourier output has deterministic sup error <=exp(-P) and
work <=C R^d E^a_solver(1+Wq), including every lookup of q0. The program
initializes its coefficients by a sampled FFT, uses strict degree-aware
padding Q>2D H, and integrates the actual finite Galerkin system by
explicit finite Lobatto/Picard steps and guarded elementary convolution
weights. It does not request exact trajectory samples.

The analytic estimates needed for that solver are proved in T101/T104:

- The actual bounded branching field at order zero supplies closed-unit
  C-to-Sobolev smoothing, without differentiating at a boundary point.
- A short-time Gevrey-2 estimate and a restarted weighted Fourier-algebra
  estimate overlap. The latter has tail exp(-b H^theta); spatial
  analyticity is not asserted when beta<1/2.
- A direct annular Fourier decomposition proves a computable uniform
  complex-time kernel L1 bound on |arg z|<=pi/4 for every alpha>0,
  including alpha=1. It uses no unsuitable absolute Fourier sum near zero.
- Real Galerkin and computed-panel bootstraps separately control the
  actual PDE error and time discretization. The large generator costs
  only logarithmically many startup panels, preserving the R^d factor.
- All initialization aliases satisfy |k|inf>=Q0-H>H. The first inequality
  is inclusive. The nodal Picard iteration starts at the explicitly
  computed free-heat array. These are the precise inherited construction
  details recorded by T104, not additional assumptions.

For the original class, a paid local Gevrey interpolant g uses k^d scalar
values and satisfies ||v-g||inf<=Cint k^-s, ||g||inf<=3/4. Let

    J=ceil(1+d/(2s)),       M=k^d.

At time one, approximate the actual Taylor derivatives through order J-1
by the D47 clock-conditioned fields. For order j, each complete sample
uses at most j unknown values and has cutoff-independent H^(d+1) second
moment <=V_j||v-g||inf^(2j). The common Gaussian variance is 2a; all
coordinates on an edge share one stable clock. Full joint residuals,
positive sine convention and the ordered tuple normalization are retained.

Hilbert sampling, the true omitted-mode tail, and coefficient clipping
give an approximation of S_1v at accuracy exp(-(T-1))/(16*25). The number
of retained time-one modes is polynomial in T. A degree-dependent
Gevrey-2 saturation is the identity on the actual S_1v range, is globally
25-Lipschitz, and gives deterministic evaluator/regularity bounds for
every clipped array. Apply the paid solver for the remaining T-1 units.

Taking k^d<=C exp(gamma T), the resulting strong RMS is <=1/8 and

    Q<= [1+J(J-1)/2] k^d                       on every seed,
    E work <=C exp(gamma T)(1+T)^A_work,
    final real entries <=C(1+T)^A_array.

Almost-sure termination and finite expected work follow from branching
nonexplosion and finite deterministic loops. Intermediate exponentially
large arrays and the final evaluator's O(K) lookup cost are included.
For 0<=T<=2 a fixed interpolation/solver patch has error <=3/32 and
bounded cost. No singular small-time derivative sampling is required.

## 3. Lower bound on the unchanged full signed class

The T102/T103 lower proof uses a finite subset of V with two complete
uniform sign slices on disjoint smooth bumps. Put a=1/(8D_psi),
I=integral psi>0, and

    R_T=(a I exp(T))^(1/q),
    k=2 floor(R_T/2),       K=k^d,       A=a k^-s,
    ell=2 ceil(sqrt(K)/2),  m=A I ell/K.

For its explicit finite threshold T0, every member of both original
slices is admissible, K>=2048, and exp(T)m is between 1 and 2^(q+1).
No exceptional PDE inputs are removed from the prior.

Integer negative moments of the full stable clock give positive-time
kernel bounds. The actual derivative field, rederived at H^(d+2), gives
||grad S_1v||inf<=G||v||inf even when the naive short-time gradient
integral diverges. Mixed L1/sup variations bound the nonlinear mean
correction by a cubic small-amplitude estimate. Full-slice concentration
and a deterministic spatial net then yield, with probability >=31/32
under each original slice, a signed time-one mean and

    ||S_1v||inf, ||(Id-Pi)S_1v||2
       <=C0 exp(-T)sqrt(T).

With lambda=c(4*pi^2)^beta>0, monotonicity of the odd power gives the
actual centered energy bound W(t)<=exp((1-lambda)t)W(0). It permits
growing nonconstant modes. The small starting scale nevertheless makes
both the final mean correction and final spatial error <=1/64 for all
T>=T0, including the resonance lambda=1/2. On the favorable event the
actual PDE targets at every x have the corresponding signs and magnitude
at least 91/160. The prior remains unconditioned throughout.

An RMS<=1/4 estimator would distinguish these original slices with Bayes
error <=9/32. A stronger sign oracle reconstructs every queried value,
including repeats, support gaps and cell-boundary zeros. After truncating
at floor(K/1024) original acquisitions and padding distinct labels, the
adaptive transcript is the same finite urn word law for every fixed
private seed. Its KL is <=1/12, and every test has error >=3/8.

Inputwise almost-sure stopping suffices: at each T the finite prior has
one common full-measure seed set. Direct finite summation gives the
seed-times-word product law on an arbitrary measurable seed space;
regular conditional probabilities are unnecessary. Markov truncation of
the original acquisition count proves

    sup_v E N_v >= C_lower exp(gamma T),
    C_lower=3*2^(-d-16)(a I)^gamma>0.

Evaluating any finite Fourier output at x* adds no initial-value query,
so the point lower also applies to strong profile estimation. Counting
at least one work unit per acquisition gives the paid-work lower.

## 4. What is and is not extended

D49 combines an explicit algorithm and an information lower bound for
the same fractional odd-power PDE, class and tolerance. It extends the
ordinary-diffusion D45 query theorem to every fixed 0<beta<=1. It is not
obtained merely by replacing a Gaussian increment in an old program.
Both the actual field law and the paid continuation solver were rebuilt.

Queries have exact Theta order. Paid work has lower c exp(gamma T) and
upper C exp(gamma T)(1+T)^A_work, so its logarithmic exponential rate is
gamma; an exact paid-work Theta result has not been proved. Constants may
be extremely large. This gives neither a moderate crossover time nor a
practical way to run the displayed solver in binary64.

Full PDE, fractional law, Sobolev/Fourier, solver, adaptive information
and complete-algorithm Lean correspondence remains unfinished. Existing
accepted finite Gaussian, Hilbert and information modules prove their
encoded pieces only. E5 concerns ordinary-diffusion derivative fields,
not this fractional long-horizon theorem. No new fractional numerical
experiment was executed for D49.

Stable branching, voting, subordination, Gevrey estimates, Fourier
algebras and spectral numerical methods have classical predecessors.
R22/R24 give bounded primary-source comparisons and their read limits.
This checkpoint makes no global novelty, significance or award claim.

## 5. Frozen proof trail

- T101 upper: 1163 lines, SHA256
  e16885dc66d636cc628c46f26718a80a618ed3658d399e007bdeef8cba8e6fd2.
- T102 lower: 962 lines, SHA256
  04d04c669deb6e1e162b4d737766607b0dd35f39c786448a0556a93025541a7d.
- T103 independent lower audit: 1037 lines, SHA256
  2e1d4b9ddf3a215ea1fa6a98ef9c23bc248a459a82e2cdc570ee70434f2c6a5d.
- T104 independent upper audit: 964 lines, SHA256
  432baed89167702b31b3e35b9fbc0620bf1723372d50697537baeee6cfcf0c11.

Root read all four complete final texts, checked the shared model and
quantifiers, and reverified their union of direct locks and all 342
protected initial files. The machine-readable correspondence record is
`reviews/T103-T104-root-correspondence.json`. No frozen source was edited.
