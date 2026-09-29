# Candidate finite-horizon clock from a limiting clock proposal

Status: conventionally proved and independently passed in T31 following T30.
No code or floating-point certification. The purpose is to remove evaluation of z(T) extremely close
to one from the ideal two-barrier Allen–Cahn clock.

## Exact rejection kernel

Retain04l's z0=m/M, R(z)=z^2/(1+z), lambda, and finite Lambda(infinity).
Define a probability kernel with a leaf atom exp(-Lambda(infinity)) and
event density lambda(s)exp(-(Lambda(infinity)-Lambda(s))) on s>0.
It is an auxiliary event-time law; no Brownian path at infinite time is used.

At a node with finite remaining time T, repeatedly draw from this kernel.
Accept a leaf immediately. Accept an event s only if s<T; otherwise repeat.
The acceptance probability is

    exp(-(Lambda(infinity)-Lambda(T)))=2R(z(T))>=2R(z0)>0.

Conditioning the kernel on acceptance gives leaf probability exp(-Lambda(T))
and density lambda(s)exp(-(Lambda(T)-Lambda(s))) on0<s<T. Thus this is
exactly the finite-horizon first-event law, without evaluating z(T).
Expected proposal trials per visited node are at most1/(2R(z0)), uniformly
in T. Finite conditional expected trials at each node plus the audited tree
bound give expected total trials at most E N_all/(2R(z0)).
To justify the random sum, index possible nodes by finite labels. Conditional
on a node being active and its known remaining time, fresh proposals have
the stated bounded mean trial count. Sum this conditional bound times each
activation probability, using Tonelli over labels. No independence from the
eventual total tree size is assumed.

The limiting kernel itself has an explicit uniform inverse. Draw U in(0,1).
If U<=2R(z0), propose a leaf. Otherwise let

    y=U/2,  zeta=[y+sqrt(y^2+4y)]/2,
    d=(1-U)(1+zeta)/(1+zeta-y),
    q_event=d/(A-B-A*d),  s=-(1/2)log(q_event),
    A=m^(-2)-1, B=M^(-2)-1.

The quadratic identity implies
(1-zeta)(1+zeta-y)=1-2y=1-U, hence d=1-zeta^2 exactly.
Thus this is the04l inverse written without subtracting zeta^2 from one.
For zeta in(z0,1), the denominator A-B-A*d=A zeta^2-B is bounded below
by1-z0^2>0 and q_event lies in(0,1). The event time s is positive and finite.
The branch mixture uses p=3(1+zeta)/(2(2+zeta)). Rejected proposals do not
generate children or Brownian increments. Accepted events use edge variance
T-s; accepted leaves use variance T.

For m=1/2,M=3/4, the leaf-proposal probability is8/15, mean trials per
visited node at most15/8, and A-B=20/9. The audited mean-node bound remains
25sqrt(6)/16-1; its product with15/8 bounds the extra uniform-clock trials.
This is a different way to realize the same ideal clock, not a changed
tree probability law or an improvement in the mathematical node count.

## Scaled defect instead of subtracting from one

For any c in(0,1), let A_c=c^(-2)-1 and q=exp(-2T). The scalar defect obeys

    R_c(T):=exp(2T)(1-ell_c(T))
      =A_c/[sqrt(1+A_c*q)*(1+sqrt(1+A_c*q))].

Return the scaled defect

    W=R_M(T)+(R_m(T)-R_M(T))*(1-Z)
     =R_M(T)*Z+R_m(T)*(1-Z).

Then E W=exp(2T)(1-u(T,x)). For the fixed phase[1/2,3/4], every output
lies in[1/4,3/2] for all finite T. The small physical defect can be reported
as exp(-2T) times its estimated scaled mean, or via its logarithm, without
subtracting a value numerically indistinguishable from one.
The logarithm of a sample mean is a plug-in estimate and is not unbiased for
the logarithm of the true defect.

If computing exp(-2T) underflows and the coefficients are evaluated at q=0,
the exact coefficient error satisfies

    0<=A_c/2-R_c(T)<=3 A_c^2 q/8.

Indeed differentiate A_c/[x+sqrt(x)] at x=1+A_c*q and use x>=1.
For the fixed phase the pathwise scaled-output change is at most27q/8,
and its relative mean error at most27q/2 because E W>=1/4. This bounds
only that explicit coefficient-limit substitution, not all floating errors.
The tree clocks do not need exp(-2T) under the rejection construction.
This comparison holds the exact tree and Z fixed. Returning zero after the
physical defect underflows would have relative error one and is not covered
by the coefficient-only estimate. Keep the scaled estimate and its exponent.

## Implementation boundaries and review request

All clock identities above are ideal-real probability identities. The
rearrangement reduces cancellation but does not by itself certify the bias
from finite random bits, square root/log rounding, s<T comparisons, spatial
sampling, or the leaf oracle. It is appropriate to test a floating sampler
as an approximation with those limitations explicitly reported. An exact
finite-bit sampler or complete numerical-bias certificate needs additional
interval/lazy-randomness analysis and is not claimed.

T31 verifies conditioning, the leaf atom, proposal-count summation, stable
algebra and domain, scaled-output bounds and the coefficient-only underflow
estimate. It also supplies a counterexample to uniform floating guarantees
over arbitrary measurable data: choose v=M on the countable set of finite-bit
query coordinates and v=m elsewhere. Finite-bit leaves always see M, whereas
ideal positive-time heat samples see m almost surely. Clock stability cannot
remove this discrepancy. A numerical protocol must restrict to a specified
regular oracle, such as the proposed smooth cosine profile, or retain ideal
transition/data oracles. No implementation precedes the selected T29 gate.
