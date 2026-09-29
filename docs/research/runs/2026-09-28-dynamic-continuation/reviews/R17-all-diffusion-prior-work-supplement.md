# R17: bounded prior-work check for the all-positive-diffusivity route

Date: 2026-09-29. Root-authored research note. T81/T82 are still candidates
under independent T84/T83 review when this note is written. This search
does not establish worldwide novelty or a level of award significance.

## Question and search scope

The candidate statement is a fixed-accuracy, long-time information and
ideal-work law for the actual Allen--Cahn equation on a unit torus, for
every fixed positive diffusivity and every fixed integer dimension and
initial smoothness. Its proposed exponent is `2d/(2s+d)`; the upper bound
retains polynomial horizon factors. Initial point values are the only
unknown-input information. The candidate mechanism uses fixed-time
smoothing, high-order residual sampling and paid continuation for the
upper; a full finite Hamming prior and actual nonlinear propagation for
the lower. The question is whether this exact combination, or a general
theorem directly implying it, is already known.

The following twelve exact queries were submitted in four batches:

1. `randomized complexity semilinear parabolic initial value problem point evaluations initial function long time`
2. `Allen Cahn equation information based complexity randomized initial values exponential time`
3. `Heinrich randomized parabolic equations initial data approximation complexity smoothness`
4. `"semilinear" "randomized" "complexity" "initial" Heinrich`
5. `"Allen" "Cahn" "initial" "information-based"`
6. `"nonlinear" "integration" "randomized" "Frechet" complexity approximation`
7. `"Haoning Wu" "Allen–Cahn" "quadrature"`
8. `"Allen-Cahn" "random initial" "long time" Hairer`
9. `"randomized complexity" "nonlinear operators" Taylor`
10. `"Breaking quadrature exactness" Allen Cahn arxiv`
11. `"semilinear parabolic" "minimal error" randomized`
12. `"nonlinear" "initial data" "complexity" "Heinrich"`

Nonprimary search hits were used only to locate primary material. The
source-specific paragraphs below record the actual inspection limit;
they do not imply that every proof or bibliography was read.

## Closest newly inspected sources

**Wu--Yuan, spectral evolution from limited samples.** The
[primary v2 text](https://arxiv.org/html/2305.04820v2) was inspected in
Sections 1.1--1.3, the first stability theorem and its proof in Section
3.1, Section 4.3, and the opening of Section 5. It explicitly treats
initial samples whose locations cannot be prescribed, constructs a
hyperinterpolant, and then evolves a known polynomial. Its mixed scheme
changes the quadrature for subsequent nonlinear terms. The inspected
theorems concern boundedness, effective maximum principles and energy
stability, with Sobolev and quadrature assumptions. They do not state the
candidate minimax horizon exponent or a lower bound against adaptive
queries. This is a close algorithmic predecessor: initial sampling plus
deterministic spectral continuation is not a new concept. A meaningful
distinction, if T81 passes, must concern its actual nonlinear fixed-time
reconstruction error and the fully charged minimax exponential rate,
rather than the general architecture. The abstract page identifies v2
as revised on 18 August 2025; no publication status beyond that is inferred.

**Hairer--Lê--Rosati, random initial fields and delayed nonlinear growth.**
The [primary journal text](https://link.springer.com/article/10.1007/s00440-023-01198-5)
was inspected through the introduction, Theorems 1.1 and 2.1 with the
latter's proof, and the opening of Section 3. It studies rapidly mixing
Gaussian initial fields on Euclidean space. The analysis separates
smoothing, linear amplification, a nonlinear scalar transition and later
interface evolution. The displayed transition is the same logistic
profile used in earlier project stages. This is substantive prior art
for the PDE mechanism, including logarithmic time scales. The present
candidate instead uses bounded smooth torus inputs from finite fixed-sign-
count priors to prove oracle complexity. The inspected statements neither
give that oracle model nor its minimax bound. That difference is a
comparison of statements, not a proof of originality. The remaining
technical estimates and all later interface proofs were not audited here.

**Gabriel--Rosati--Zygouras, weakly critical random data.** The
[primary full article](https://pmc.ncbi.nlm.nih.gov/articles/PMC12316858/)
was inspected in its abstract, introduction, Theorem 1.1, following
discussion, and the located opening of its main proof. It considers a
two-dimensional Euclidean white-noise regularization with weak coupling
and a nonlinear correction to the Gaussian limit. Theorem 1.1 has an
explicit coupling/time restriction; the discussion suggests continuing
after a positive smoothing time. Thus smoothing followed by continuation,
and restrictions arising from tree expansions, are established themes.
Its singular-data scaling and limiting fluctuation question differ from
the fixed smooth input class and adaptive-query minimax problem here.
No proof of its full result was attempted. The page records online
publication in 2024 and issue date 2025; these are distinct dates.

**Petras--Ritter, linear parabolic information complexity.** The
[primary proceedings page](https://drops.dagstuhl.de/entities/document/10.4230/DagSemProc.04401.10)
was inspected at its abstract and bibliographic record. It fixes the
initial condition and varies PDE coefficients, with integration lower
bounds and approximation-based upper bounds. This confirms a relevant
classical complexity framework but a different unknown input. The full
24-page PDF was not read in this supplementary check; earlier project
literature records must be consulted for any stronger comparison.

## Access limits and leads not promoted to conclusions

The Wu--Yuan unversioned HTML and a guessed v3 address returned cache
misses. The actual abstract page identified v2, whose HTML link succeeded.
An attempted PMC bibliography link for the generic-initial-data paper
returned the same weakly-critical article; the journal DOI page then
provided the correct text. No content was attributed to the failed link.

The DOI `10.1016/j.jco.2014.01.002`, for Daun--Heinrich's parametric
Banach-space IVP complexity paper, was inaccessible via this browsing
tool. An earlier guessed ScienceDirect PII address also failed and is
not evidence about that paper. This remains a full-text comparison lead.
Heinrich's 2013 Banach-space IVP paper reappeared in search; its relevant
oracle distinction was already inspected in R15 and was not freshly
re-proved here. Search snippets from theses, aggregators and unrelated
papers do not establish additional precedents.

## Research implications

The bounded check did not locate the exact candidate theorem. It did
locate close predecessors for both algorithm structure and nonlinear
amplification. The strongest defensible potential contribution is the
joint precise information model, all-fixed-positive-diffusivity scope,
and matching exponential rate with counted auxiliary computation. Each
of those clauses must survive proof review and comparison with general
IBC results. Merely extending a tree simulation to a larger T, using
Fourier continuation, or recovering the logistic transition would not
support a broad originality claim.

The next literature checks should read the full parametric Banach-IVP
oracle model and the relevant nonlinear-integral-equation complexity
theorems, then test whether their general upper principles already imply
the fixed-time reconstruction rate. On the PDE side, compare the exact
random-field cancellation estimates with T82's finite-slice concentration,
including which steps simplify because the data are bounded and the
domain is compact. These are bounded next actions, not open-ended claims
that absence from a search establishes novelty.

No numerical experiment, initial-data acquisition, PDE solve or Lean
build was performed for this literature note. A requested separate T85
worker spawn and a worker-reuse followup both failed with the agent-thread
limit; no T85 worker or report exists. Root completed this R17 check while
the independent mathematical audits continued. No external researcher was
contacted and no result was published.
