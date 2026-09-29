# T39 — two-barrier canvas update

Date: 2026-09-28  
Scope: bounded presentation update to the existing dynamic-continuation evidence canvas.

## Frozen inputs

- Canvas source: `/Users/michael/.cursor/projects/Users-michael-Desktop-NTU-fyp-parabolab/canvases/dynamic-continuation-evidence.canvas.tsx`
- Canvas SHA-256 before this update: `6a96d0294f10280518f1599cdc3f55677017670c9fdab4fa32a0b8b038086f83`
- T38 derived table: `artifacts/two-barrier/audit-v1/derived_tables.json`, SHA-256 `d24a0934ab95f303069e9970fc8efa0dcce81e054e1a5e3a305ffbf8106b5636`
- T38 audit summary: `artifacts/two-barrier/audit-v1/audit_summary.json`, SHA-256 `8a72f0cdf4320d90e95dbe2d63ac15a89341bbaf677259c9a3aadace0e3828e0`
- T38 report: `reviews/T38-two-barrier-audit.md`, SHA-256 `5afaa171e1ff9ab84c87c1a94b579ea1902b69ac74b4a0e68e77aba20ba4d13d`
- T35 implementation report: `reviews/T35-two-barrier-implementation.md`, SHA-256 `61223b95bb083ccbf4a183d9eee1c5c07fb70f78839241beff65bfe03ea3db92`
- Reviewed scientific figure: `two-barrier-results-v2.png`, SHA-256 `812bbba5bf93d6c5528d66e04acef455d2d63eb5b2e01a236e8ade471d6ca0ad`

## Presentation change

The canvas now contains a compact Chinese section headed `E2 · 双移动屏障的有限证据`. It presents only audited T38 data for the fixed one-dimensional cosine datum:

- 63 cells, 630,000 primary roots, `N=10,000` per cell, and seven fixed horizons through `T=256`;
- a three-series chart and a complete table of all 21 three-seed relative-error RMS values;
- the three fixed sampling times (`2.12709`, `1.89072`, and `1.76424` seconds), the fixed 16-mode one-solve-plus-21-query time (`0.0969848` seconds, excluding basis and system construction), and the separately reported six-refinement solve-plus-query total (`2.12111` seconds);
- the actual maximum RMS, `1.02535%` at `T=16, x=0`, with an explicit warning that not every displayed point is below 1%;
- the three `T=256` RMS values (`0.3884%`, `0.1523%`, `0.4991%`) beside the harmonic-center `24.8573%` and spatial-mean ODE `5.1055%` absolute relative-error baselines; and
- a scope boundary stating that the reviewed work bounds are expectations, not per-root or finite-sample caps, and that the empirical observations do not prove those bounds.

The section links the exact derived table, raw 992/992 audit summary, T38 audit report, T35 implementation report, and reviewed v2 scientific figure. It does not alter the scientific figure or introduce the candidate 04o/T41 claim.

The legacy four 201-point dynamic arrays, all six critical-frontier 3-by-4 arrays, negative baseline text, and theory-scope table remain present and unchanged in value.

## Verification

### Frozen-data parity

A read-only parser compared the canvas constants directly with the frozen JSON sources.

```text
PASS legacy arrays: times, empiricalRms, midpoint095g, equilibriumG each 201/201 exact
PASS critical arrays: K and cusp ratios each 3 alpha x 4 cutoffs exact
PASS two-barrier RMS: exact transpose of empirical_three_seed_rms, shape 7 x 3, all 21 values
PASS T38 gate: status PASS; 992/992 checks
PASS required timing, maximum, T=256 baseline, expectation-bound, and evidence-link text
PASS legacy negative-result and critical-endpoint boundary text retained
PASS candidate 04o/T41 material absent
```

### SDK-aware TypeScript check

The installed Cursor TypeScript compiler (`6.0.3`) loaded the canvas directory's `tsconfig.json` and checked all four canvas files against the local `cursor/canvas` package (`0.0.0`):

```text
files=4; diagnostics=0
```

### Bundle check

The installed `esbuild-wasm` executable (`0.25.9`) bundled the canvas with only its SDK/runtime imports externalized:

```sh
esbuild dynamic-continuation-evidence.canvas.tsx \
  --bundle --platform=browser --format=esm \
  --external:cursor/canvas --external:react/jsx-runtime \
  --outfile=/private/tmp/dynamic-continuation-evidence.bundle.js
```

Result: success, `44.1kb` bundle.

### Static presentation audit

- Imports remain restricted to `cursor/canvas`.
- The E2 section reuses SDK `Stack`, `Row`, `Grid`, `Card`, `Stat`, `LineChart`, `Table`, `Callout`, `Text`, `Pill`, and `Link` components.
- It introduces no raw color literals, gradients, network access, or figure editing.
- The RMS chart labels its percentage axis, categorical cutoff axis, series, and 1% reference line. The table gives the complete audited values rather than a selected subset.

No GUI render certificate was available. An `open_in_codex` request returned `queued` for the hidden task, so visual QA is limited to source hierarchy and label inspection, SDK-aware type checking, bundling, and frozen-data parity.

## Result

- Canvas SHA-256 after this update: `b50570e376c8fd12ed10dc6c23e46bd7c3435a801a266d3d4b24766946ecffd6`
- T39 status: **PASS**
