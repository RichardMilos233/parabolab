# T53 — independent audit of the signed many-bump lower bound

## Verdict and audited scope

**PASS for conventional promotion, with the stated scope. No mathematical
repair is required.** T50 proves the expected exact point-query lower bound

    sup_v E Q_T(v) >= C exp(2dT/(2s+d))

for every fixed integer `s>=1`, `1<=d<4s`, and all sufficiently large `T`,
under uniform absolute RMS at most `1/4`. Its separate smaller-amplitude
construction also proves the critical case `d=4s`, whose exponent is `4/3`.
The PDE, floor, information, and random-stopping arguments were checked
independently below.

The audited T50 file is
`reviews/T50-signed-many-bump-lower-bound.md`, SHA-256
`45e56dc4c5bb656cc3f3407f4e7627e772e13b013a8ca9837ffebe8f79806151`.
The input-class comparison uses
`04o-unstable-phase-query-lower-bound.md` in this run.

The actual cost conclusion is first **prior-average expected cost** for a
public, finite prior chosen independently of the algorithm. Consequently an
expensive member exists, but that member may depend on the algorithm and
on `T`. This does not inherit 04o's stronger common-baseline quantifier.
There is no signed-class matching upper bound, no `d>4s` result at this
exponent, no fixed-profile hardness theorem, and no publication-priority
claim. The audited proof is conventional mathematics; this report adds no
Lean, numerical, implementation, or formal-verification claim.

## 1. Exact class and nonlinear PDE estimate

The class is exactly 04o's class on `R^d/Z^d`, with normalized volume:
smooth real periodic data, all coordinate partial derivatives through total
order `s` bounded by one, supremum norm at most `1/2`, and both strictly
positive and strictly negative values. The information model is also the
same: exact value queries to the unknown datum, arbitrary adaptive locations,
input-independent private randomness, measurable rules, all evaluations
charged, and almost-sure halting. The algorithm receives no input-dependent
formula, mean, coefficient list, preprocessing result, or evolved value.

For `A=||v||_infinity<=1`, let `u=S_t v`, `b=integral u`, and `w=u-b`.
The comparison principle gives both `|u|<=1` and `||u(t)||_infinity<=Ae^t`.
The smooth bounded solution exists globally on the compact torus; the
maximum principle supplies the continuation bound. There is no regularity
or solution-existence loss caused by the high derivatives of the hard data.

The energy identity in T50 is correct. In particular,

    integral w*u^3 = integral (u-b)*(u^3-b^3) >= 0.

Thus it does not require nonnegative data. For generator `(1/2)Delta` on
this unit torus the first nonzero decay rate is `2pi^2`. The energy estimate
therefore gives

    ||w(t)||_2 <= A exp(-nu t),  nu=2pi^2-1>0.

The normalization is material: the initial variance is at most `A^2`, and
the spectral gap is specific to this domain scale. Dimension does not alter
the first nonzero eigenvalue.

The mean equation retains the required nonlinear correction:

    b' = b-b^3-R,
    R = 3b integral w^2 + integral w^3,
    |R(t)| <= 5A^3 exp((1-2nu)t).

Here `|b|<=Ae^t`, `||w||_infinity<=2Ae^t`, and the variance estimate give
the two constants `3` and `2`. If `ell_m` is the scalar flow with
`m=integral v`, the difference equation has coefficient
`1-(b^2+b ell_m+ell_m^2)<=1`. Variation of constants consequently yields

    |b(T)-ell_m(T)| <= (5/(2nu)) e^T A^3.

This is a valid one-sided coefficient bound; no absolute Lipschitz bound of
one or closed scalar equation for the actual mean is being assumed.

For the spatial remainder set `G=u^2+ub+b^2`. Then `0<=G<=3` and the
exact equation is

    w_t=(1/2)Delta w+(1-G)w+q(t),
    q(t)=integral G w,  |q(t)|<=3A exp(-nu t).

Kato's inequality followed by positive heat comparison gives the displayed
one-unit formula. Parseval for this heat normalization gives

    ||p_1||_2^2 = sum_{k in Z^d} exp(-4pi^2|k|^2)
       <= ((1+h)/(1-h))^d,  h=exp(-4pi^2).

The forcing contribution is bounded explicitly by

    3e A exp(-nu(T-1)) integral_0^1 exp(-(nu+1)r)dr
       <= [3e/(nu+1)] A exp(-nu(T-1)).

Therefore T50's constant
`C_d=e(H_d+3/(nu+1))`, with `H_d=((1+h)/(1-h))^(d/2)`, is correct.
Its complete estimate (P) holds for `T>=1`. All its bounds are uniform over
the arrangement of positive and negative bumps. Constants may depend on
the fixed dimension; no dimension-uniform assertion is needed.

## 2. Bumps, parity, floor, and phase separation

Compact support strictly inside each cell makes the scaled bumps smooth
across all interfaces and across the torus seam. At each point at most one
bump is nonzero. Hence derivatives of order `|alpha|<=s` have size at most
`aD k^(|alpha|-s)<=aD<=1/8`; the height is at most `a k^(-s)<=1/8`.
The class is fixed even though its selected members and derivatives above
order `s` vary with time.

For `R_T>=4`, the even floor satisfies

    R_T/2 <= R_T-2 <= k=2 floor(R_T/2) <= R_T.

Both `k` and `K=k^d` are even. With `K>=2048`,

    sqrt(K) <= r=2 ceil(sqrt(K)/2) <= sqrt(K)+2
       <=2sqrt(K)<=K/4.

Thus the two layer counts `(K+r)/2` and `(K-r)/2` are integers strictly
between zero and `K`. Every input has at least one positive bump and at
least one negative bump; both layers are nonempty and consist entirely of
members of the exact signed class.

Writing `q=s+d/2` and `mu=aI k^(-s-d)`, the useful identity is

    e^T mu r = (R_T/k)^q * r/sqrt(K).

It proves `1<=e^T|m|<=2^(q+1)`. The scalar profile therefore has magnitude
at least `1/sqrt(2)`, with the layer's sign.

The subcritical powers and constants check algebraically:

    e^T A^3 <= 2^(3s) a^3 (aI)^(-3s/q) exp(-delta T),
    delta=3s/q-1=(4s-d)/(2s+d)>0,
    A exp(-nu(T-1))
       <=2^s a(aI)^(-s/q)e^nu exp(-(nu+s/q)T).

The stated `Rmin=max(4,2*2048^(1/d))` ensures both floor conditions.
Each logarithmic term in T50's `T0` makes its corresponding PDE remainder
at most `1/16`, including when `log(16C_i)` is negative. Therefore for
**every real `T>=T0`**, every sign arrangement in either layer, and every
target point,

    |S_T v_sigma(x*)| >= 1/sqrt(2)-1/8 > 1/2

with the correct sign. No favorable subsequence of horizons and no
probabilistic exception among arrangements is required.

At `d=4s`, `q=3s` and the first coefficient becomes
`(5/(2nu))2^(3s)a^2/I`. The critical choice

    a<=sqrt(nu I/(40*2^(3s)))

makes it at most `1/16` exactly. The other remainder still decays, so the
separate critical threshold is valid. The use of a smaller fixed `a` does
not change the promised class or make its constants time-dependent.

For `d>4s`, the supplied estimate no longer closes at this scale. T50
correctly describes a limitation of its proof, not an impossibility theorem.
Its zero-mean trigonometric example also checks: the cubic average is
`(3/4)c epsilon^3`, so the mean derivative is its negative.

## 3. Exact oracle, adaptive transcript, and information constants

An exact value query in a known cell returns the known bump amplitude at
that point times just one unknown sign. A point where the bump vanishes
reveals no sign. Revealing the entire cell sign anyway is a legitimate
stronger oracle. Queries at interfaces and repeated visits cannot reveal
additional unknown signs.

For each fixed seed, simulate the original capped algorithm with this
stronger oracle, ignoring any unneeded extra information. Cache previously
revealed signs. After it halts, expose arbitrary unused cells until exactly
`n` distinct signs have been revealed. This padding is possible because
`n<K`. All query locations, repeated answers, stopping decisions, and the
returned label are the same measurable function of that seed and padded
sign sequence under both hypotheses. Including those locations in a
transcript cannot add divergence beyond the seed/sign experiment.

Under either uniform Hamming layer, conditional on previously revealed
signs, all assignments to unqueried cells with the remaining sign count
are equiprobable. Adaptive choice of an unused index thus has exactly the
urn conditional law in T50. The law is without replacement, not iid.
The independent seed has the same law under both layers and contributes
zero initial KL. One can apply the chain rule for each seed and integrate;
the finite sign space also makes this argument explicit without any
input-dependent exceptional-set difficulty.

For `n=floor(K/1024)`, every history of fewer than `n` signs is feasible
under both layers, since each sign count in either layer is at least
`3K/8>n`. The claimed bounds can be checked directly:

    p_- >= (3K/8-K/8)/K = 1/4,
    p_- <= (K/2)/(7K/8) = 4/7 < 3/4,
    p_+-p_- = r/(K-i) <=2r/K.

Consequently the elementary Bernoulli KL inequality gives

    KL(Ber(p_+) || Ber(p_-))
       <= (p_+-p_-)^2/[p_-(1-p_-)]
       <= (64/3)r^2/K^2 <=256/(3K).

Summing over the padded observations gives `KL<=1/12`, including the seed
and adaptive indices by the preceding common-function argument. Pinsker
then gives `TV<=1/sqrt(24)<1/4`; equal-prior Bayes error is at least `3/8`.
All constants use natural logarithms.

## 4. RMS premise and genuinely expected cost

Uniform mean squared error at most `1/16`, together with the pointwise
phase magnitude greater than `1/2`, makes the sign test based on the output
have error at most `1/4` for every input. This uses only the loss bound;
the estimate need not be unbiased, bounded, or have an input-independent
stopping time.

Let `qbar` be prior-average expected original point-query cost. Infinite
`qbar` already satisfies the result. Otherwise truncate before requesting
query `n+1` and choose any label at that point. Only runs with `Q>n` may
change their labels. Markov's inequality therefore gives

    3/8 <= error_of_capped_test <=1/4+P_prior(Q>n)
         <=1/4+qbar/n.

Thus `qbar>=n/8`. Since `K>=2048`,
`floor(K/1024)>=K/2048`, and therefore `qbar>=K/16384` as claimed.
This step allows rare expensive branches and correctly converts the
fixed-query experiment to a random-stopping expected-cost lower bound.

Finally, `k>=R_T/2` gives the displayed constant

    qbar >=2^(-d-14)(aI)^(d/q) exp(2dT/(2s+d)).

The prior is algorithm-independent and finite. At least one of its members
has expected cost at least this average; no interchange of the universal
algorithm quantifier with the existential member quantifier is justified
or used.

## 5. Attribution and promotion conditions

I independently opened the three primary papers cited by T50 and checked
the cited passages. Their descriptions are supported:

- [Ben-David–Blais, Definition 25 and Lemma 26](https://arxiv.org/pdf/2002.10809)
  give the two-layer gap-majority problem, linear randomized query
  complexity, and the permutation-symmetry argument for adaptive indices.
  Section 2.4 includes randomness in transcripts. T50 supplies its own
  constants and its expected-cost conversion.
- [Kunsch–Rudolf, Section 2.1 and the proof of Theorem 2.3](https://arxiv.org/pdf/1809.09890)
  use unknown signs on disjoint scaled bumps and obtain the classical
  smooth integration exponent. The discussion explicitly allows adaptive
  information and notes the extension of its lower-bound lemmas to random,
  input-dependent cardinality with changed constants.
- [Hairer–Lê–Rosati, equation (1.5), Theorem 1.1, and Proposition 4.6](https://arxiv.org/pdf/2201.08426)
  concern growth from small signed random data and the nonlinear scalar
  transition in a different spatial/scaling setting. They are relevant
  mechanism-level prior, not a cited proof of this deterministic torus
  query theorem. Their equation (4.2) also displays the ordinary finite-time
  scalar Allen–Cahn flow used here.

No new literature search was needed beyond opening and checking these
primary sources; this is not a priority assessment. The classical
information ingredients must remain attributed.

No repair to the frozen T50 proof is requested. Promotion is justified
provided the statement retains the exact oracle and fixed smoothness class,
the unit-torus normalization, the restricted dimensions with a separately
chosen critical amplitude, the prior-average/worst-case quantifiers, and
the conventional-only proof status. No other file was changed by this audit.
