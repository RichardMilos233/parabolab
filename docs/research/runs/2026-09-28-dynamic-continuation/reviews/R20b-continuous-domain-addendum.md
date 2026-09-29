# R20b: domain and risk-inequality repairs to the field-sampler candidate

Date: 2026-09-29. Root correction responding to independent T91 review.
The frozen R20 file remains unchanged at SHA256
b1e42a195c67942066894d04a11c28d7ba2951a6d6730977070e424ac84542b9.

In R20 Section1, replace the phrase "a known evaluable g with
||g||inf<1 and an unknown residual e=v-g" by the following exact domain:

    g,v are real continuous functions on X=(R/Z)^d;
    g is known by an explicit evaluator of finite cost G per lookup;
    ||g||inf<1; v is accessible only by charged exact point values;
    e=v-g belongs to C(X).

The derivative in (1.1) is the Frechet derivative of the actual map

    S_tau : {q in C(X): ||q||inf<1} -> H^(d+1)(X).

The domain is open in the sup norm, and all directions are elements
of C(X). The sample-mean identity and moment bound hold for these
continuous e, without requiring g+e to be inside the domain. The
Taylor-remainder assertion (5.1) separately requires the complete
segment g+t e, 0<=t<=1, to remain in that open ball, as R20 already
states. No derivative of a discontinuous datum is asserted.

This is a genuine missing hypothesis in the standalone wording:
bounded primitive-evaluable functions can be discontinuous, whereas
the proposed derivative is defined on C(X). The intended application
uses a smooth known interpolant and smooth unknown v and already
satisfies the repaired domain. No mathematical identity, sampling law,
constant, rate, oracle cost or intended smooth-input class is changed.
R20 is to be cited only together with this addendum after T91 review.

The closing paragraph of R20 Section5 must also read "give actual
mean-square error at most V_j delta^(2j)/M", with an explicit <=,
where delta bounds ||e||inf. It is an upper bound, not a generally
exact risk formula. For instance, when f=0 and j=2, the flow is
linear and the actual second-order sample is zero; its risk is zero
even when the displayed positive upper constant and residual norm
are nonzero. The exact Hilbert variance identity is the centered
second moment divided by M, which is bounded by that expression.
The original formula (1.1) already uses the correct inequality.

This correction does not supply a full polynomial long-horizon upper
solver, lower bound, end-to-end formalization, implementation, or new
numerical evidence. No frozen source or other proof is overwritten.
