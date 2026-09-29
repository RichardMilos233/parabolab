# R18: nonlinear information complexity and the function-space obstacle

Date: 2026-09-29. Root-authored bounded literature comparison after D37--D39
acceptance. T88 worker creation/reuse failed at the agent thread limit; no
independent T88 report is claimed. This note is not a novelty certificate.

## Question and exact search record

Does a general existing theorem immediately give the fixed-time nonlinear
map S_1 from scalar C^s initial values to a whole spatial profile at error
n^(-s/d-1/2), with point-value input and constants sufficient for the
long-time construction? The difference between scalar input queries and
an oracle returning an entire Banach-space vector is material.

Fifteen exact searches were submitted, in five batches:

1. `Stefan Heinrich nonlinear integral equations randomized complexity Banach spaces approximation`
2. `Daun Heinrich 2014 randomized complexity parametric initial value problems Banach space pdf`
3. `randomized approximation semilinear parabolic initial function C s supremum norm complexity`
4. `"Monte Carlo Complexity of Global Solution of Integral Equations" pdf`
5. `"Complexity of parametric initial value problems in Banach spaces" pdf Heinrich Daun`
6. `"randomized" "nonlinear integral equations" complexity Heinrich`
7. `"Daun" "Heinrich" "parametric" "2014" "pdf" "uni-kl"`
8. `"Monte Carlo complexity" "nonlinear" "operator" Heinrich`
9. `"Heinrich" "Kirrinis" nonlinear complexity integral`
10. `"Complexity of parametric initial value problems in Banach spaces" -site:researchgate.net -site:dblp.org -site:slub-dresden.de`
11. `"Daun" "Heinrich" "392" "429" pdf`
12. `"Heinrich" "nonlinear" "integral equations" "complexity" randomized -site:researchgate.net`
13. `"Some nonlinear problems are as easy as" approximation Wasilkowski`
14. `"nonlinear" "randomized complexity" "solution operator" PDE initial`
15. `"randomized" "nonlinear functionals" smoothness integration complexity`

Nonprimary hits were only discovery leads. No author was contacted. The
following inspection limits distinguish actual primary text from leads.

## Primary statements actually inspected

**Heinrich--Hinrichs, Banach-valued integration.** Read the primary HTML
Sections1--2, Theorems1--2, Corollaries1--2, Proposition1 with its proof,
the algorithm (5)--(6), and Appendix algorithm/error definitions. The
input is a C^r map on [0,1]^d taking values in X, and a query returns
one X-valued function value. Theorem1 gives a randomized upper
C tau_p(X)n^(-r/d-1+1/p). Corollary2 characterizes the same-order rate
by equal-norm type p; p=2 requires type2. Proposition1 gives the pth
moment bound for deterministic interpolation plus sampled residuals.
The appendix permits adaptive expected cardinality; its minimal-error
definition uses expected norm. Thus the interpolation/residual and
Hilbert averaging mechanism is established prior art. It does not by
itself construct an X-valued nonlinear PDE sample from finitely many
scalar initial values. That conversion is the outstanding application
bridge, not a new general Monte Carlo theorem.
[Primary text](https://arxiv.org/html/1312.3290).

**Heinrich2013, Banach-valued IVPs.** Read the primary PDF's problem and
information definitions on printed pages74--78, algorithm on78--80,
Theorems3.2--3.3 on82, the integration reduction around96--97, and
Theorem4.2/Corollary4.3 on99--100. For r-smooth, rho-Hoelder right-hand
sides with a Lipschitz condition, Theorem4.2 gives randomized upper
n^(-r-rho-1+1/p) in type-p spaces, with corresponding lower bounds.
Theorem3.2 explicitly supplies a pth-moment trajectory-sup estimate.
The oracle returns the entire X-valued f(t,x), or the entire initial
state u0. Constants may depend on the fixed time interval and input
class parameters. Directly identifying X with a spatial function space
would therefore give much more input information than this project's
point oracle; its regularity assumptions also do not directly cover the
unbounded Laplacian on C(X). A separate reduction would be necessary.
[Primary PDF](https://m.mathnet.ru/php/getFT.phtml?jrnid=jmag&option_lang=eng&paperid=550&what=fullt).

**Daun2014 dissertation, parametric IVPs.** This is an accessible primary
substitute for inspecting the related framework, not a claim to have
read the inaccessible journal article. Read title metadata, the
definitions around(6.58)--(6.64), information model(6.172)--(6.173),
Theorem6.6.1 and nearby type2 cases in6.6.3. The equation evolves
u(s,t) independently for each external parameter s; the oracle returns
Z-valued f(s,t,z) and u0(s). The output norm covers both s and t. Rates
depend on parameter smoothness, time smoothness and the type of Z;
boundary regimes carry logarithmic factors. These are substantial
predecessors for whole-function randomized evolution. Taking s as
spatial position does not introduce diffusion coupling between positions,
and taking Z as the whole spatial state changes the query model. Neither
identification alone supplies our scalar-initial-query S_1 construction.
The PDF extraction has damaged relational symbols; no fine boundary-case
formula is imported here without a successful visual check.
[Primary dissertation](https://d-nb.info/106993867X/34).

**Heinrich1998, global integral-equation solution.** The publisher's
search-accessible abstract explicitly studies the whole solution rather
than a single functional and finds a randomized improvement. This is
prior art for global random approximation as an objective. Full theorem
hypotheses and rates were not retrieved in this check, so it cannot
support either an exact identification or an exclusion of our setting.
[Publisher record](https://www.sciencedirect.com/science/article/pii/S0885064X9890471X).

**Wasilkowski1984, nonlinear problems.** The university publication record
describes equivalence to function approximation for examples such as
minimum, norm and reciprocal. The primary technical-report PDF opened
but had no extracted text. Its actual general hypotheses were not read;
the title cannot establish an equivalence for the nonlinear AC flow.
[University record](https://scholars.uky.edu/en/publications/some-nonlinear-problems-are-as-easy-as-the-approximation-problem/),
[Technical report](https://mice.cs.columbia.edu/getTechreport.php?format=pdf&techreportID=965).

## Research consequence, not a priority verdict

The strongest confirmed overlap is the combination of deterministic
approximation, random residual correction, and function-space geometry.
Those pieces must be attributed rather than advertised as new. Existing
ODE complexity statements also show that sophisticated nonlinear
continuation alone is not a new framework.

For our proposed refinement T87, the substantive unresolved bridge is an
actual scalar-query, fixed-time nonlinear field sampler with finite
Sobolev second moment. If established, a Hilbert sample-mean estimate and
Sobolev embedding are classical consequences. D37's long-horizon actual
PDE separation, the same input/oracle model, and the counted implementation
must still be checked separately. The search did not locate a theorem
directly discharging all of these bridges. This bounded failure to locate
one is not proof of originality or of high mathematical significance.

## Access failures and scope limits

The Daun--Heinrich2014 DOI opening failed. The CiteSeerX link for their
systems-of-ODEs follow-up also failed despite a searchable abstract. An
unverified guessed ScienceDirect PII, S0885064X14000021, failed and is not
a bibliographic identification. Direct openings of the1998 publisher page
and2017 systems follow-up failed; only searchable publisher text was seen.
Three dissertation screenshots (zero-based pages101,125,126) returned cache
misses. The accessible dissertation's text is the basis of the qualified
comparison above; no screenshot inspection is claimed. The2014 journal
paper remains a priority-check lead, and no full thesis/proof audit was
performed. No code, Lean proof, numerical run or oracle acquisition was
performed for this note.
