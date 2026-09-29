# R09: accepted D28 in the existing evidence canvas

Root completed the D28-only canvas update. It adds the independently
audited all-dimension signed lower theorem and preserves the restricted
`d<=4s` scope of the matching upper. Quantifiers, normalized unit domain,
missing signed formalization and absence of practical runtime bounds are
explicit. No T65 candidate or unaudited E4 statistics were added.

Managed file:
`/Users/michael/.cursor/projects/Users-michael-Desktop-NTU-fyp-parabolab/canvases/dynamic-continuation-evidence.canvas.tsx`.

Previous source SHA256:
`1c754eac5819c006fbed8a2e7280d63c0e688b967d25d42b61ef18948888d07c`.
New source SHA256:
`b1280e8dab63ae9cd908b8b6dc20eb07fa706c439b5400ff06fa9dc0abc584ed`.

Both sources, parity checks and build evidence are preserved under
`artifacts/evidence-canvas-signed-v2/`. The TypeScript AST comparison found
all47 previous top-level constants verbatim, including every previous
numeric array; two new local-link constants were added. All33 local links
exist. Earlier E1/E2 baselines and unfavorable speed comparisons remain.

The real installed TypeScript6.0.3 checked the candidate against the canvas
SDK with zero diagnostics. The esbuild-wasm command exited0; its bundle
has67378bytes and SHA256
`4d5917a2ff49399226865af68246e46e030f9dfbc62493bb8e7a2f777e49ebcb`.
The managed write was approved by filesystem review after checking both
old and candidate hashes, and its new hash was verified after copying.
The open-in-Codex tool returned `queued`. No GUI render was observed or
claimed. No numerical experiment or Lean build was rerun for this update.
