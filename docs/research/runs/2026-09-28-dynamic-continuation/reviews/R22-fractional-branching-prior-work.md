# R22: bounded primary-source check for the fractional route

Date: 2026-09-29. Root literature inspection during T95. This is an
attribution and scope check, not a worldwide novelty verdict or acceptance
of T95. No experiment, unknown-input acquisition or Lean invocation.

## Primary results actually inspected

**Penent–Privault, arXiv:2106.12127.** Read the abstract/introduction,
Theorem1.1/Corollary1.2, the subordinator discussion and (1.8)/(1.10),
Remark4.2/Corollary4.3, the higher-spatial-derivative discussion and the
Section5 simulation formula in the [primary PDF](https://arxiv.org/pdf/2106.12127).
This was a scoped read, not a complete proof audit of its thirty pages.

The paper already represents polynomial semilinear equations with subordinated
Brownian branching trees, including spatial gradient terms, and derives local
integrability conditions. It explicitly supplies negative subordinator moments
and a CMS stable simulation formula. Crucially, Remark4.2 removes the extra
negative-moment time-integrability condition when the reaction has no spatial
derivatives. Thus citing its alpha>1 gradient condition as a universal
restriction on derivative-free fractional branching would be incorrect.

Our initial-data Frechet derivatives are not the spatial derivative marks
of that representation. Its higher-spatial-derivative obstruction does not
by itself prove or refute the T95 target. The above ingredients must receive
prior-work credit; their rediscovery would not establish a new sampler theorem.

**Privault, Oberwolfach report15/2022.** Read the three-page
[author-hosted report](https://personal.ntu.edu.sg/nprivault/papers/oberwolfach_fractional.pdf).
Its parabolic theorem explicitly concerns sufficiently small horizons and
polynomial reactions that may include gradients, with a Bernstein-function
integrability hypothesis. The report also distinguishes elliptic exterior
problems. This confirms the local-horizon context but supplies no minimax
initial-data query theorem used here. No figures were visually inspected.

**Becker–Etheridge–Letter, EJP29(2024), article25.** The
[primary arXiv abstract](https://arxiv.org/abs/2309.13899) and
[Oxford publication record](https://ora.ox.ac.uk/objects/uuid%3A8d9a01f1-3409-4922-af86-2f8b5aa48c7a)
identify an existing ternary branching stable representation for scaled
fractional Allen–Cahn and a coupling to Brownian trees with truncated
subordinators, used for a mean-curvature-flow limit. Only abstract and
publication metadata were inspected; no full theorem is imported. The
related Becker2023 thesis record was also returned by search, but its full
thesis was not read.

## Consequence for this project

T95 must not claim that fractional branching, Brownian subordination, stable
sampling, voting for fractional Allen–Cahn, or negative stable moments are
new. Its distinct proposed obligation is the actual H^(d+1)-valued derivative
field with a hard j-scalar-query cap, obtained by a compatible common Gaussian
extraction on the whole tree, and a cutoff-independent second-moment bound.
Those obligations still require their own proof and independent audit.

Even a successful fixed-time result does not establish a fractional long-time
query/work theorem. The existing paid known-profile solver needs a new spatial
regularity and cost analysis; replacing ordinary diffusion in formulas alone
does not provide it. None of these bounded searches settles whether some
other work already proves the exact combined computational statement.

## Search and access record

Five exact search queries were issued:

1. `branching processes fractional Laplacian semilinear PDE Monte Carlo Penent Privault`
2. `branching diffusion nonlinear fractional reaction diffusion probabilistic representation polynomial voting`
3. `"A probabilistic approach to fractional reaction-diffusion equations" arxiv`
4. `"10.1214/24-EJP1087"`
5. `Kimberly Becker Etheridge fractional Allen Cahn branching stable mean curvature`

The arXiv HTML endpoint for2106.12127 returned a cache miss; its PDF then
opened successfully. The Oxford thesis page direct open returned403 even
though its primary search record was available. The Oxford EJP PDF direct
open and the DOI resolver returned internal errors; primary abstract and
record metadata were used instead. Nonprimary search hits were not used as
theorem evidence. PDF text was inspected, with no screenshot/figure claim.
The report's PDE integral hypothesis is taken from the source's mathematical
statement; broken line extraction is not silently treated as a new formula.

T95's worker was informed of these attribution constraints while its proof
was still in progress. All earlier accepted proofs and numerical artifacts
remain untouched by this inspection.
