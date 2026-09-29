# Environment and verification commands

- Formal working directory: `/Users/michael/Desktop/NTU/fyp/parabolab/formal`
- Toolchain file: `leanprover/lean4:v4.33.0`
- Lean: `4.33.0`, commit `d8b18978322de05a8f3dba51ef03cf5461676c17`
- Lake: `5.0.0-src+d8b1897`
- Mathlib commit: `db584cd6d46c92f209a44c0f1c829460d327499d`
- Project Git HEAD during verification: `65dca46e42db1c80cdf9ddd8eed6a415148c37f3`

The directly captured environment output, including command exit codes, is in
`environment.log`.

Commands run from the formal working directory:

```text
/Users/michael/.elan/bin/lake build EstimatorIntegrity.UniformSliceConditioning
/Users/michael/.elan/bin/lake env lean <evidence-dir>/Axioms.lean
/Users/michael/.elan/bin/lake env lean <evidence-dir>/Declarations.lean
```

All three commands exited with code 0. `build.log`, `axioms.log`, and
`declarations.log` were captured directly by `Capture.zsh`. `trust-scan.log`
was likewise captured directly and records no forbidden-token matches in the
source.

The implementation role requested by the research configuration was
`gpt-5.6-sol` with `xhigh` reasoning. This worker's actual backend identity was
not independently exposed, so no model-switch claim is made.
