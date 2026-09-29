# R06: D27 evidence-canvas correspondence

Status: root-completed source update and static verification. No numerical
or formal proof was rerun. The managed canvas now links D27/04t and the
full T59 independent audit, distinguishes phase from mass, and states the
deterministic query cap versus potentially enormous auxiliary arithmetic.
The d<=4s restriction, unit-torus condition, unresolved larger-dimensional
extension and missing signed Lean/numerical coverage remain explicit.

Managed file:
`/Users/michael/.cursor/projects/Users-michael-Desktop-NTU-fyp-parabolab/canvases/dynamic-continuation-evidence.canvas.tsx`.

Previous SHA256:
`0c6f4a59cacbea9bc8f846fa7e20eb64817e7777ce72d8da9d79a083c065ed4f`.
New SHA256:
`1c754eac5819c006fbed8a2e7280d63c0e688b967d25d42b61ef18948888d07c`.
Both sources and all new check artifacts are preserved under
`artifacts/evidence-canvas-signed-v1/`. The older T57 artifacts are untouched.

All45 previous top-level constants, including every numerical data array,
remain verbatim. All31 local links exist. E1/E2's zero-query baselines and
unfavorable deterministic-solver timing comparisons remain. No R04/T61
candidate or unexecuted positive-sampling results were inserted as evidence.

The real installed TypeScript6.0.3 API checked one source file against the
existing cursor/canvas SDK with zero diagnostics. The esbuild-wasm command
exited0; the new bundle has66907bytes and SHA256
`cf6424ba8ff401c711535b42725e4f8bcea88b54a92d6178d15ca43b9a645e42`.
The source uses the existing SDK imports, with no network/data dependencies.
The managed write was approved by the filesystem review after verifying
both source hashes. The subsequent open-in-Codex call returned `queued`.
This is not a GUI-render verification, and no visual-render PASS is claimed.
