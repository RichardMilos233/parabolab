# T92 — evidence Canvas signed-v6 packaging correspondence

Date: 2026-09-29 (Asia/Jakarta). Status: **PASS for the bounded candidate package; managed Canvas not modified.** T92 performed mechanical evidence packaging only. It ran no numerical experiment, made no unknown-input acquisition, modified no accepted theorem or proof ledger, and introduced no novelty claim.

## Immutable starting point and candidate

The managed Canvas inspected by T92 was
`/Users/michael/.cursor/projects/Users-michael-Desktop-NTU-fyp-parabolab/canvases/dynamic-continuation-evidence.canvas.tsx`, SHA256
`e2619ea14528c4e3d20e62ed2a3edb8cb2f3c175b47af4e31c9f1599f9e9fa41`.
The archived original in `artifacts/evidence-canvas-signed-v6/` is byte-identical.
T92 did not write the managed path.

The versioned candidate is
`artifacts/evidence-canvas-signed-v6/dynamic-continuation-evidence.candidate.canvas.tsx`, SHA256
`a35be1ea0d6c6357cae2b1176df538e31fd61b5012c0f9e77ad0a947226f5b73`.
It has not been deployed.

## Added accepted evidence

The candidate leads with **D40–D42** from frozen
`04z-all-positive-diffusivity-sharp-queries.md`, SHA256
`57ef1d86ddba30ce9d54f316b0eb2dc97f407f7aeb4446a66b3103c28e0aedd4`,
and `reviews/T90-root-correspondence.json`, SHA256
`2cec8c64716616c05383990fa4cbb143f21e42b58dde6b3a8121277ad56f85e7`.

- For every fixed `kappa>0` and integers `d,s>=1`, D42 gives exact point and strong-profile minimax expected query order `Theta(exp(gamma T))`, `gamma=2d/(2s+d)`, at the common RMS tolerance `1/4`. The profile construction has the stronger RMS bound `<=1/8`.
- D40 is identified as the actual Gaussian–Hilbert field sampler: it is unbiased for the fixed-time PDE derivative, has cutoff-independent second Hilbert moments, and uses at most `j` unknown initial-value queries on each seed path.
- D41 states the explicit finite real-Fourier profile algorithm and its all-seed hard query cap. The candidate separately preserves the paid-work conclusion `exp(gamma T) poly(T)`; it does not claim exact-Theta paid work.
- The earlier D37–D39 section is preserved byte for byte. The new leading callout says exactly that D42 supersedes D39's query polyfactor, while leaving the frozen older result and its other boundaries intact.

The candidate also adds accepted **T86 fixed05l** only after the root record became available:
`reviews/T86-root-correspondence.json`, SHA256
`b39b9cfb5b22e1185c95e191b3f7a85339b2f6314da4b5eb34ef66c332fdce0d`.
The locked 658-line source has SHA256
`d50bd7145685480ab802270d4a5eae623205b373b70c1158b30cdbef50fd80fe`.
The Canvas lists all 28 public declarations by exact declaration name and labels the count correctly as definitions, theorems, and instance together, rather than 28 theorems. It records the actual uniform prior and singleton masses, positive conditioning event, normalized compatible law, actual next-bit Bernoulli pushforward including true-mass endpoints 0 and 1, and the actual finite two-slice KL bound `64 ell^2/(3K^2)`. It also records the root fresh `autoImplicit=false` source check, the 3403-job worker build, and standard-axiom-only public audit.

T86 remains a one-step finite formal gate. The Canvas expressly excludes complete adaptive history, n-step composition, seed simulation, padding, random stopping, slice-martingale concentration, MSE-to-testing, PDE, full minimax, runtime, and numerical evidence. D40–D42 remain conventional rather than end-to-end Lean formalized.

T89 remains pending. R20/R21 remain candidates pending audit and are not promoted or used as premises. The candidate makes no uniform `kappa->0`, `kappa=0` profile-one-query, finite-bit, random-bit, practical-speed, complete-Lean, numerical, or novelty claim.

## Preservation and semantic comparison

The full unified diff is captured in `semantic-diff.log`. Its exit code is 1 because the candidate intentionally differs from the original; the diff contains additions only. The AST validator independently proves that every original line is present verbatim and in the same order.

The passing validator records:

- all 82 original top-level constants preserved verbatim; 87 in the candidate after five new evidence-path constants;
- all 68 original link occurrences preserved; 73 in the candidate;
- all 63 original absolute path constants unchanged and resolved; 68 in the candidate;
- all five `LineChart` subtrees byte-for-byte identical;
- every original TypeScript numeric literal retained;
- frozen E4 arrays still have exactly 60 pooled, 180 per-seed, and 36 zero-query-baseline records;
- the `368,270,390` total-activity text and all older numerical material preserved;
- one import, from `cursor/canvas`, embedded data only, and no hardcoded hex color, gradient, or box shadow.

The layout keeps a clear hierarchy: D40–D42 is the leading result, T86 is adjacent to the established formal-coverage section, and historical numerical and theorem sections retain their varied original composition. This also completes the Canvas skill design self-check.

## Direct validation evidence

`Capture.zsh` records each command, cwd, UTC start/end, combined stdout/stderr, and exit status.

- `parity.log`: `validate.cjs`, exit 0, `PASS`. This covers source locks, insertion-only comparison, AST constants, numeric literals, charts, links, paths, arrays, required wording, and Canvas design constraints.
- `typescript.log`: TypeScript `6.0.3`, exactly one candidate file, zero diagnostics, exit 0. The check used `/private/tmp/d29-e4-canvas-check/check.cjs` with the versioned `tsconfig.json` in the signed-v6 directory.
- `bundle.log`: esbuild-wasm browser ESM bundle, exit 0. The emitted bundle SHA256 is `fd0688fa46e962c02870eddb7d661c141f7c5fcd1a5077910ab5aab5f0725a20`.
- `environment.log`: direct Node, TypeScript, and esbuild-wasm version capture.
- `semantic-diff.log`: complete original-to-candidate unified diff, expected exit 1 because additions exist.

`source-manifest.json` locks the managed source, candidate, D40–D42 sources, and T86 sources. `check-commands.json` records the validation commands and interpretation of the expected diff status. `validation-manifest.json` and `SHA256SUMS` lock the final review and package artifacts.

## Model routing and exact boundary

Math-auto-research routes mechanical Canvas packaging to the implementation role. T92 requested `gpt-5.6-sol` at `xhigh` effort. The collaboration host did not independently expose the executing backend identity or a new per-task model override, so the actual backend is recorded as unexposed rather than claiming that the requested model was switched in.

This package is ready for root inspection and optional deployment. T92 did not deploy it and did not modify the managed Canvas.
