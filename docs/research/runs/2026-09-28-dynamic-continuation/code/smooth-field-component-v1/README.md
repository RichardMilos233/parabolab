# E5 smooth-field component implementation v1

This directory implements frozen protocol `02h` without running the official
acquisition. The core sampler in `smooth_field.py` receives a known evaluator
and an opaque scalar callback; profile formulas and analytic references remain
in the outer `experiment.py` harness.

The T99 commands use the pinned environment:

```text
/opt/miniconda3/envs/parabolab/bin/python driver.py manifest
/opt/miniconda3/envs/parabolab/bin/python driver.py preflight
```

The later `official` command requires a root-created acceptance JSON whose
fields byte-link the frozen protocol, implementation manifest, and passed
preflight result. That gate is source acceptance, not an additional user
permission prompt. The `replay` command uses the original tag-0 streams and
fixed indices 0 through 7, and charges its opaque calls anew.

All E5 phases share the persistent budget journal under
`artifacts/smooth-field-component/`. A hard crash during tree generation
leaves a conservative unresolved segment reservation and blocks continuation
until independent audit; it never silently resets the global budget.
