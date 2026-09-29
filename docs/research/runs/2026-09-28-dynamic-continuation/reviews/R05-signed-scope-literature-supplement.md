# R05: bounded signed-phase scope and literature follow-up

Status: root search supplement, not an independent priority certification.
It does not alter T55, D27 or any proof. Eleven additional web search
queries were issued while T61/T62/T63 worked. Search snippets alone are
not treated as a theorem inspection.

## Searches and inspected sources

Queries included Allen--Cahn long-time initial-point information complexity;
nonlinear parabolic solution-operator randomized complexity; asymptotic
phase and smooth initial-data dependence; randomized smooth nonlinear
functionals; Heinrich/Novak Frechet-functional Monte Carlo; and the exact
title of the parabolic-complexity paper returned by search. The most direct
parabolic-complexity hit was the same Petras--Ritter work already in T55.
A CiteSeer PDF fetch failed (cache miss); the primary Dagstuhl record was
then read. This failed fetch is not a full-text inspection.

[Petras--Ritter, primary Dagstuhl record](https://drops.dagstuhl.de/entities/document/10.4230/DagSemProc.04401.10)
states a linear parabolic problem with fixed initial condition and variable
coefficients. It relates information lower bounds to integration and
constructs approximation methods from a Neumann expansion. This remains
relevant precedent for a nonlinear map from input information to a PDE
target, but it is a different input class from D27. T55 contains the more
detailed theorem-level inspection; this supplement does not repeat it.

[Scheel, Coarsening fronts, author manuscript](https://www-users.cse.umn.edu/~scheel/preprints/coarsening.pdf)
was opened; the introduction and stated results on PDF pages1--5 were
inspected. It concerns Allen--Cahn fronts and periodic patterns on the
line, including slowly evolving layers and the bifurcation structure as
periodicity changes. Its asymptotic phase is associated with translation
of fronts, so that phrase alone does not identify D27's scalar phase
functional or a query-complexity theorem. This is also a useful reminder
that general Allen--Cahn dynamics need not resemble a rapidly mixing
unit-torus problem.

[Oates--Girolami--Chopin, Control functionals for Monte Carlo integration](https://arxiv.org/abs/1410.2392)
was opened at the primary abstract page only. Its deterministic-approximation
and random-sampling combination is a relevant broad methodological
predecessor. The full theorem/assumption comparison was not performed in
this supplement. It supplies no new independent confirmation of D27.

No exact same signed large-T theorem was located in these bounded queries.
This is not evidence that no such theorem exists. Search coverage was
mostly noisy, and generic nonlinear-functional approximation literature
still deserves a more targeted follow-up before any priority claim.

## A mathematical scope restriction that must stay visible

D27 uses the fixed normalized unit torus and diffusion coefficient1/2.
Its nonconstant-mode decay rate is nu=2*pi^2-1, independent of the number
of torus coordinates. This favorable spectral gap enters both the scalar
phase reduction and its derivative bounds. Calling the result a theorem
for arbitrary Allen--Cahn domains would discard a central assumption.

For a period-L torus the corresponding first-mode linear calculation at
zero gives growth rate1-2*pi^2/L^2. When L>sqrt(2)*pi, that mode is
unstable, so the specific centered-energy decay used here fails. This is
an elementary calculation from the project's operator, not a new result
claimed from the cited front paper. Failure of this proof does not by
itself prove failure of all long-time query algorithms.

Accordingly, potential extensions should separate higher dimension on the
same unit torus (T61's present lower-bound question) from larger domains,
weak diffusion and multiple unstable spatial modes. The latter change the
underlying dynamics and may require a vector of unstable coordinates.
No such extension is accepted or formally/numerically tested by this note.
