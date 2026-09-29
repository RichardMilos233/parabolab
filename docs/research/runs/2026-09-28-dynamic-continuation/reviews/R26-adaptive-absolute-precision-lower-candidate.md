# R26: long-time lower bound with adaptive absolute-precision queries

Date: 2026-09-29. Root conventional candidate, not independently accepted.
This is a specified quantized-information model, not a universal bit
complexity theorem and not a statement about floating-point mantissas.
No Lean, numerical execution or unknown-input acquisitions occurred.

## 1. Model and proposed conclusion

Keep D45's equation u_t=(kappa/2)Delta u+u-u^(2p+1), fixed kappa>0,
d,s,p>=1, and its exact full signed smooth class V and RMS tolerance1/4.
Let q=s+d/2 and gamma=d/q. The new oracle accepts a location x and an
integer absolute precision b>=0, and returns only

    Q_b(v(x))=2^(-b) floor(2^b v(x)+1/2).                 (1.1)

It uses the displayed deterministic tie convention. No extra timing,
symbolic input formula, sign, relative-precision value or side-channel
information is returned. Both x and b may depend measurably on all past
answers and an arbitrary independent private seed. Algorithms may be
biased and inputwise almost surely stopped. Repeated queries count.

Charge each call 1+b units, and write B_v for their sum. Auxiliary
arithmetic may be ideal and free; this only strengthens the lower bound.
The proposed conclusion is that, for all sufficiently large T,

    sup_(v in V) E B_v >= c_prec T exp(gamma T).           (1.2)

This lower bound allows adaptive precision and arbitrary numbers of
cheap low-precision calls. It is not obtained by multiplying unrelated
worst-input bounds: the same finite prior forces many expensive calls.

More generally, if one query costs a nondecreasing function C(b), the
proof below gives c_lower C(h_T+1) exp(gamma T). It does not prove a
matching finite-precision upper algorithm.

## 2. Frozen accepted inputs

Use the full lower proof in T94 Sections6–9 and its independent T96
audit, summarized by accepted04ab. Root previously read their complete
mathematical content and rechecked the exact prior and constants for
this proposal.

- `04ab-odd-power-long-horizon-complexity.md`, SHA256
  `a8bd72ec33c69aae4d50126c72f6fd75ac4e1625cb08cfcef6a1b310918d18c0`.
- `reviews/T94-odd-power-long-horizon-feasibility.md`, SHA256
  `2600c29a2823aefd9a69578de113bc511179d97bdfbea7eb3a6861ac28b7e1d9`.
- `reviews/T96-odd-power-long-horizon-independent-audit.md`, SHA256
  `b8f5f32be92c820bd8b955c5969406a49fa21e12a1b38c86d17bb7467ba1eda4`.

The fractional T101/T102 candidates are not premises. This note adds
only the information/precision argument. The actual nonlinear PDE
separation is the accepted ordinary-diffusion result, not a linearized
or scalar-surrogate assertion.

## 3. One prior has both small amplitudes and separated targets

Use the same fixed public smooth nonnegative bump psi supported inside
the unit cube, its integral I>0 and a=1/(8Dpsi). For T beyond the
accepted finite threshold T0 put

    R_T=(a I exp(T))^(1/q),
    k=2 floor(R_T/2), K=k^d, A=a k^(-s),
    ell=2 ceil(sqrt(K)/2),
    v_xi(x)=A sum_i xi_i psi(kx-i).

The prior chooses equally between the complete uniform sign slices
sum xi_i=+ell and sum xi_i=-ell. Every input is in V; the prior is not
conditioned on a favorable PDE event. All input values obey |v_xi(x)|<=A.
Since R_T/2<=k<=R_T,

    A <= C_A exp(-sT/q),
    C_A=2^s a(a I)^(-s/q),
    K>=2^(-d)(a I)^gamma exp(gamma T).                    (3.1)

On each full slice, the actual PDE target has the corresponding sign
and magnitude at least91/160 at every point with probability at least
31/32. Therefore a point algorithm with worst-input MSE<=1/16 supplies,
by the sign of its output, a test with prior error at most9/32. A strong
profile algorithm gives the same point guarantee by evaluating its
explicit output at a fixed point. These are exactly the original-class
separation and loss reductions, with no new restriction on algorithms.

## 4. Low absolute precision returns a deterministic zero

Define the public integer

    h_T=floor(log(1/(4A))/log 2),                         (4.1)

and take T large enough that h_T>=0. For every b<=h_T,
2^(-b)>=4A and hence |v_xi(x)|<=2^(-b)/4. Formula(1.1) then returns
zero for every location and every prior input. The strict interior
margin avoids all tie issues, including negative values.

Call an acquisition high precision when b>=h_T+1, and let N_hi count
all such calls, including repeats or zero-valued answers. Arbitrarily
many calls with b<=h_T can change a deterministic internal state or
use private randomness, but their answers carry no information about
which prior input was selected. This remains true when their precisions
and locations are adaptive.

For a high-precision call at a point in cube i, a stronger oracle can
reveal xi_i, from which (1.1) is computed using only public A,psi,x,b.
At support gaps and boundaries the scalar answer is still correctly
zero. A previously revealed cell is reconstructed from its earlier sign.
Thus one high-precision call reveals at most one new prior sign, while
a low-precision call requires none. No input value is acquired for free
in this reduction; it is a lower-bound simulation using a stronger oracle.

## 5. Cap high-precision calls and retain the original information proof

Set n_cap=floor(K/1024). Run any proposed quantized algorithm until it
halts or is about to make its(n_cap+1)-st high-precision call. In the
latter case assign a fixed output label. Pad the distinct signs actually
revealed with unused labels until n_cap signs have been revealed; the
decision ignores padding. Low-precision calls and repeat high-precision
calls add no new sign letters.

For a fixed private seed, the original full-slice exchangeability still
gives at the j-th distinct reveal, after z positive signs,

    p_+(j,z)=((K+ell)/2-z)/(K-j),
    p_-(j,z)=((K-ell)/2-z)/(K-j).                         (5.1)

This does not depend on how many uninformative calls intervened or which
unseen index was adaptively selected. Every prefix through n_cap is
feasible under both original slices. The accepted finite calculation
then gives step KL<=256/(3K), total word KL<=1/12, total variation
<=sqrt(1/24)<1/4, and testing error at least3/8.

For arbitrary seed spaces, remove the finite union of seed null sets
on which the original algorithm fails to halt for one of the finitely
many prior inputs. For every remaining seed and any feasible revealed
prefix, fix a prior completion. Its actual halting guarantees that the
simulation reaches its next high-precision query or stops after finitely
many intervening operations/calls; otherwise it would not halt on that
completion. Hence the capped simulation is well defined. All low answers
are the same zero, so this argument is unaffected by adaptive precision.

The seed and padded word laws are respectively the product of the seed
law with the two fixed finite urn laws. This is a finite-prior sum, not
an appeal to regular conditional probabilities on an arbitrary seed
space. The testing lower bound3/8 consequently includes private seeds,
adaptive locations/precisions and inputwise almost-sure stopping.

Let q_hi be the original prior average of E N_hi. If it is infinite,
the claimed lower bound is immediate. Otherwise the capped and original
decisions can differ only if N_hi>n_cap, an event of probability at most
q_hi/n_cap. Combining the upper test error9/32 with the lower3/8 gives

    q_hi >=3 n_cap/32 >=3K/65536
          >=c_lower exp(gamma T),
    c_lower=3*2^(-d-16)(a I)^gamma.                       (5.2)

The same original prior forces all these high-precision acquisitions.
If all requested b were bounded by h_T on every input and seed, (5.2)
would be impossible. No amount of such low-precision sampling suffices.

## 6. Precision cost on that same prior

By(3.1),

    log(1/(4A))/log2 >= sT/(q log2)-log(4C_A)/log2.

Take

    T_prec=max(T0,1,(2q/s)max(0,log(4C_A))).              (6.1)

For T>=T_prec the right side is at least sT/(2q log2)>0. This also
ensures h_T>=0. Every high-precision call therefore has

    b>=h_T+1>log(1/(4A))/log2 >=sT/(2q log2).             (6.2)

On every transcript, B_v=sum(1+b_i)>=[sT/(2q log2)]N_hi.
Average this inequality under precisely the same prior as(5.2). A
finite prior average is bounded by the worst-input expectation, so

    sup_v E B_v >=[s c_lower/(2q log2)]T exp(gamma T).     (6.3)

This proves(1.2) with c_prec=s c_lower/(2q log2). Nondecreasing cost
C(b) instead gives C(h_T+1) times(5.2). No matching upper statement is
implied, and the fixed parameters may enter a very large threshold.

## 7. Why the cost model cannot be silently generalized

Equation(1.1) is rounding to a fixed absolute grid. Charging 1+b can
model obtaining or reading a fixed-point packet of that precision.
It is not a lower bound on all encodings or on pure information bits.
For example, a relative-precision floating response with an unbounded
exponent range can preserve the sign of an arbitrarily small nonzero
number without using T mantissa bits. A compressed or symbolic oracle
can also have a different cost. The zero-bin argument would not apply
to those oracles as stated.

The result likewise does not establish rounding stability of the exact
real solver, a bound on arithmetic precision at every internal operation,
or an upper bound for IEEE binary64. Fixed-point information loss and
floating arithmetic error are separate questions. Deterministic rounding
also differs from independent Gaussian measurement noise; repeated calls
at the same point and precision do not average away this rounding.

## 8. Bounded prior-work check and remaining gate

The two searches were exactly:

1. `Plaskota varying precision noisy information cost function evaluation complexity integration absolute error precision`
2. `information based complexity noisy function values varying precision cost integration smooth functions randomized`

The primary [Plaskota–Siedlecki preprint page](https://arxiv.org/abs/2303.16328)
was read at abstract/metadata only. It studies linear problems with noisy
linear information and precision-dependent evaluation costs. Thus this
general modeling idea is established. Its full proof was not inspected
or used to infer the nonlinear PDE theorem here. Other search snippets,
book contents and secondary pages are not theorem evidence.

The direct argument above reuses the accepted actual-PDE full-slice
construction and changes the counted informative actions. Independent
review must check the quantization guard, adaptive simulation, seed and
stopping details, and same-prior multiplication before accepting it.
No worldwide originality or significance claim is made. A separate fixed
formal target and numerical protocol would precede execution. Existing
E4/E5 source, budgets and evidence remain unchanged.
