# R24: bounded primary-source check for the fractional known-profile solver

Date: 2026-09-29. Root literature and proof-routing note, not acceptance
of the pending T101 long-time upper theorem. No numerical acquisitions,
Lean execution, or publication action was performed.

## Search and inspected scope

The two initial searches were exactly:

1. `Gevrey regularity semilinear fractional diffusion polynomial nonlinearity analytic semigroup fractional Laplacian Gevrey`
2. `complex time fractional Laplacian heat kernel L1 analytic semigroup estimates sector`

They were followed by direct primary-page/PDF opens and targeted finds.
The three source URLs were reopened before this note was written. This
is a bounded check, not a systematic review or a novelty certificate.
Secondary search snippets were not used as theorem evidence.

### Bae–Biswas

[Gevrey regularity for a class of dissipative equations with analytic
nonlinearity](https://arxiv.org/pdf/1403.1603) was inspected through its
abstract/introduction and opening definitions. Its model equation (1.1)
assumes a diffusion order kappa>1. With our order alpha=2 beta, that
restriction does not cover beta<=1/2. Targeted search also exposed
statements around Lemmas 4.1–4.4; their complete proofs and the full paper
were not audited. This is prior Gevrey methodology, not a ready-made
all-beta theorem for the current scalar-query problem.

### Merz

[On complex-time heat kernels of fractional Schrödinger operators via
Phragmén–Lindelöf principle](https://link.springer.com/article/10.1007/s00028-022-00819-1)
was inspected at the introduction, Theorem 1.1, formulas (1.4), (1.6),
the targeted L1 estimate (3.28), and reference 65. It points to Zhao–Zheng.
Its displayed general potential estimate includes an exponential factor;
one cannot simply discard that factor when quoting it. The entire article
was not read. A clicked citation first returned an internal anchor, after
which the actual cited primary preprint was located.

### Zhao–Zheng

[Uniform complex time heat kernel estimates without Gaussian bounds](https://arxiv.org/pdf/2012.08763)
was inspected in version 2, dated 27 September 2022, at the introduction
and Theorem 1.1 on PDF page 2, with the beginning of Theorem 1.3 on page 3.
This version's numbering differs from the earlier version cited by Merz.
Theorem 1.1 gives spatial kernel bounds for the free multiplier of order
alpha>0, separately below and above alpha=1. Scaling its estimates on a
fixed cone gives integrable bounds; the alpha=1 case has the explicit
Poisson kernel. The full 25-page proof was not independently verified.
This is a classical consistency check, not a new kernel result claimed here.

## Direct proof route selected for T101

The solver needs only a uniform complex-time operator bound on a fixed
cone, not sharp asymptotics near the imaginary axis. Root and the T101
worker independently derived the following ordinary Fourier argument.
It is recorded here to identify the actual candidate proof dependency;
the full constants and solver composition belong to frozen T101 when
that task is finished and independently reviewed.

Normalize the time modulus and put

    m_theta(xi)=exp(-exp(i theta)|xi|^alpha), |theta|<=pi/4.

Choose a smooth cutoff chi equal to one on the unit ball and zero outside
radius two, and let psi(xi)=chi(xi)-chi(2xi). Telescoping decomposes m_theta
as chi plus low annuli of (m_theta-1) and high annuli of m_theta. After
rescaling the k-th annulus to a fixed compact shell, each of a fixed
finite number of low-frequency derivatives is bounded by C 2^(k alpha).
The corresponding high-frequency bounds are a fixed polynomial in
2^(k alpha) times exp(-c 2^(k alpha)), uniformly on this cone.

For a compactly supported symbol b, integration by parts with
(1-Delta)^q, q>d/2, bounds the L1 norm of its inverse Fourier transform
by a finite sum of L1 norms of derivatives of b through order 2q.
The low geometric and high exponentially decaying series therefore
converge in L1. Their Fourier transform identifies the actual multiplier,
including its value at zero. Scaling restores the time modulus, and
periodization transfers the bound to the torus without increasing L1.
This argument includes alpha=1. It uses classical decomposition and
integration by parts, not the sharp external kernel theorem as a premise.

Only finitely many cutoff derivatives are needed. An explicit polynomial
transition with enough vanishing endpoint derivatives supplies computable
majorants, if needed for public solver constants. A qualitative existence
of a cutoff alone must not be relabeled as a completed finite algorithm.

The separate positive-time spatial regularity route uses a weighted
Fourier l1 algebra with exponent theta=min(1,2 beta), whose weight is
submultiplicative. The accepted fixed-time derivative fields supply the
unweighted regularity needed to start it. This avoids assuming analytic
spatial smoothing for beta<1/2, which D47 explicitly disproves in general.
The overlap of initial Gevrey control with the later weighted interval,
finite spectral truncation, time integration, error propagation, operation
count and full original-class composition still require T101's proof and
independent audit. This note promotes none of those to an accepted claim.

## Remaining scientific boundary

The primary sources concern analytic/Gevrey regularity or semigroup kernel
estimates. They do not by themselves establish our proposed long-time
scalar-query minimax theorem, a paid solver, practical speedup, or global
originality. T102 separately investigates the matching lower bound; its
success cannot be inferred from an upper construction. E5 remains its
separate frozen full-field component protocol.
