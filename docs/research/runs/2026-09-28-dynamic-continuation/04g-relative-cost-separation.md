# Candidate relative-accuracy separation for quadratic coding

Status: conventionally proved and independently reviewed in T20, including
the matched Gaussian scalar baseline incorporated below.
No Lean or numerical claim. This is a precise follow-up to T17's inexpensive
absolute-error bound and stronger scalar binary baseline. Classical
importance-sampling inequalities are used; novelty is unestablished.
In particular, the second-moment minimization by a proposal proportional
to the absolute integrand is standard; see
[Owen, Chapter 9, Section 9.1](https://artowen.su.domains/mc/Ch-var-is.pdf).
The possible contribution here is the code-specific long-time separation,
not that general variance inequality.

## Fixed scope

Let d>=5 be fixed, 0<epsilon<=1/32, and v(x)=epsilon exp(-|x|^2).
Use the absorption PDE u_t=Delta u/2-u^2, and evaluate at x=0.
The T15 original derivative-code canonical absolute moment is denoted W_I.
We compare independent equally weighted averages of unbiased root samples.
Arbitrary biased PDE solvers, control variates, cross-tree cancellations,
correlated roots and randomized estimators with a different representation
are not covered by the lower bound.

## A one-line positive subtree lower bound

The canonical absolute field A satisfies A(s)>=P_s(v^2). Consequently

    W_I(T,x) = P_T v(x) + integral_0^T P_(T-s) A(s)(x) ds
             >= P_T v(x) + T P_T(v^2)(x).

This uses nonnegative tree sums and the heat semigroup only; it needs no
asymptotic heat-kernel theorem. The signed absorption solution obeys
0<u(T,x)<=P_T v(x). At x=0 the two heat flows are explicit:

    P_T v(0) = epsilon (1+2T)^(-d/2),
    P_T(v^2)(0) = epsilon^2 (1+4T)^(-d/2).

Thus for every T>=0,

    W_I(T,0)/u(T,0)
      >= 1 + epsilon T [(1+2T)/(1+4T)]^(d/2)
      >= 1 + k T,                  k=epsilon 2^(-d/2)>0.

## Proposal-independent lower bound on relative variance

For any genuinely supported, completing, exactly likelihood-weighted original
tree proposal, E H=u and E|H|=W_I. If E H^2 is finite, Cauchy–Schwarz gives

    Var(H)/u^2 >= (W_I/u)^2-1 >= (1+kT)^2-1.

If the second moment is infinite, the relative mean-square error is already
infinite. For the average of N independent identically distributed roots,

    E[(Hbar_N-u)^2]/u^2 >= [(1+kT)^2-1]/N.

Hence any such average attaining relative RMS at most rho>0 needs

    N >= [(1+kT)^2-1]/rho^2.

For fixed d,epsilon,rho this is Omega(T^2). This is a statement about this
unbiased single-tree architecture and sample averages, not a lower bound
for every algorithm solving the PDE. The full-support invariant by itself
does not cover a transformed estimator that integrates contributions with
cancellation; the next paragraph checks the precise T17 exception.

T17's removal of identically zero codes and exact integration of F2 preserves
canonical absolute mass: all nonzero F2 histories have the same negative sign,
and their absolute integral is 2. No opposite-sign terms are combined there.
The same finite-tree likelihood telescoping used for the signed law applies
after taking absolute values. Therefore E|Hhat_I|=W_I also for the exact T17
sampler. T17 and T20 independently check this identity; equality of signed
means alone would not suffice.

## A matching quadratic upper bound for the guided coding sampler

Let eta=epsilon I0(infinity)<=1/48. Since 0<=u(s,x)<=epsilon w(s), view
the PDE as the linear equation u_t=Lu-u(t,x)u with its fixed solution as
potential. The usual Feynman–Kac formula gives

    u(T,x) >= exp(-eta) P_T v(x).

Only this deterministic comparison is used; the algorithm does not query u.
At x=0, G(T,0)/[(1+2T)^(-d/2)]
= [(1+2T)/(1+T)]^(d/2)<=2^(d/2). T17's deterministic output envelope gives

    E Hhat_I^2 / u(T,0)^2
      <= exp(2eta) 2^d (1+C epsilon T)^2.

Thus N=ceil(exp(2eta)2^d(1+C epsilon T)^2/rho^2) independent samples
suffice for relative RMS <=rho in the exact ideal model. T17 bounds expected
total visited nodes between N and 112N. Together with the lower bound, expected root
work for fixed d,epsilon,rho is Theta(T^2) for this guided implementation,
despite a uniform expected node count per root and bounded absolute outputs.
This is neither dimension-uniform nor a finite-bit complexity theorem.

## A representation change removes this horizon factor

For the Gaussian datum the scalar binary sampler can use a tighter heat
envelope than the general C1-data envelope in T17. Set

    Gv(t,x)=(1+2t)^(-d/2) exp(-|x|^2/(1+2t))=P_t v(x)/epsilon,
    wv(t)=(1+2t)^(-d/2),
    Iv(t)=[1-(1+2t)^(1-d/2)]/(d-2),
    eta_v=epsilon Iv(infinity)=epsilon/(d-2)<=1/96,
    m_v(t)=epsilon/[1-epsilon Iv(t)],      h_v=m_v Gv.

The branch clock is m_v*wv, with successful binary probability Gv/wv and
negative product output. The normalized terminal return is identically one.
The exact heat-transform edge from remaining T to s is Gaussian with mean
(1+2s)x/(1+2T) and coordinate variance (1+2s)(T-s)/(1+2T). It is the bridge
with fictitious pinning time T+1/2. The event probability is at most eta_v,
so the same finite-depth argument gives

    |Hhat_v| <= P_T v/[1-epsilon Iv(T)],
    E N_v <=1/(1-2eta_v)<=48/47,
    E Hhat_v = u.

Now the matched bound u>=exp(-eta_v) P_T v yields, for every finite T and x,

    E Hhat_v^2/u^2 <= exp(2eta_v)/(1-eta_v)^2.

There is no exponential dimension factor in this matched scalar bound.
Using exp(1/48)<=48/47, the relative variance is at most

    (48/47)(96/95)^2-1 = 18193/424175 <1/20.

Consequently N=ceil(1/(20rho^2)) independent scalar roots suffice for relative
RMS <=rho, with expected nodes at most 48N/47, uniformly in T,x,d>=5 and
0<epsilon<=1/32, in the exact ideal model. Arithmetic still involves d-vector
Gaussian draws; the statement is not dimension-free bit complexity.
The difference is a horizon factor between these representations, not a claim
that a newly invented solver beats the standard binary method.

Returning the exact heat flow is also a strong biased baseline. Its relative
error is at most exp(eta_v)-1<=1/95, uniformly in T,x. Thus accuracy looser
than about 1.05% does not require Monte Carlo for this example. Any numerical
comparison must use a tighter target and include the heat baseline openly.

## What a subsequent formal or numerical check could certify

The new substantive obligation is the canonical absolute-mass preservation
under T17's exact reductions. The deterministic heat and positivity comparisons
also require review. After that, a finite Lean target could check the algebra
from E H^2>=(E|H|)^2 and the mean bounds to the sample-count separation; it
would not formalize probability or asymptotic computational complexity.
Numerical finite-T plots cannot prove Omega(T^2) or unbiasedness.
