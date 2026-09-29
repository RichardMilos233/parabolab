# T99: frozen E5 smooth-field implementation and bounded preflight

Date: 2026-09-29. Status: **implementation and bounded preflight complete;
official acquisition not executed**.

This task implements the frozen `02h` D44 component protocol, its persistent
E5 accounting, deterministic correspondence fixtures, twelve-cell tag-1
preflight, root-gated official driver, and fixed replay driver. It does not
run the official tag-0 acquisition or claim an experimental result. The final
source preflight passed, and a separate read-only artifact audit passed.

## 1. Frozen inputs and scope

The implementation rechecked these inputs before each preflight:

| Input relative to the run directory | SHA256 |
| --- | --- |
| `02h-smooth-field-component-experiment-protocol.md` | `1866585a86fcfceb0f9b05f632dae093d3c6e03f4ab005b4eae02fbfa5b27612` |
| `reviews/T98-smooth-field-protocol-independent-audit.md` | `4684093695d5c116355d95be79d1fc0701d79b3671b1de889f938eccacd3a227` |
| `reviews/T98-root-correspondence.json` | `cf5485f00bbd7ff0ea24465f85e6b5457acd54cdf952b8da7606b2f117586fe4` |
| `04aa-polynomial-fields-and-linear-gaussian-preparation.md` | `433c699d951c74fa6ba19166e159069130e1340a7a319aa0334b0ba4f8a1b8a1` |
| `reviews/R21-linear-tree-common-gaussian-candidate.md` | `99f8a23c98332b6797ee1ecc9f0929d94950cd047acb17bcbea0df9052ff7461` |

The final implementation manifest is
`artifacts/smooth-field-component/preflight-v1/implementation_manifest.json`,
SHA256
`901d4b7ad115912fd1ce9e28d77c0a3c37b9dd171b0e6dd851a7cce7014967ed`.
It freezes the twelve cells, three seeds, array schema, random APIs and call
order, traversal, zero-edge policy, binary64 environment, timer boundaries,
tolerances, reference precision and abort limits before tag-0 output exists.

The requested implementation role was gpt-5.6-sol with xhigh reasoning. The
serving backend was not independently exposed, so this is recorded as a
requested role rather than a verified model identity.

## 2. Final source inventory

All implementation source is under `code/smooth-field-component-v1/`.
The manifest byte-links every Python file used by the final preflight:

| File | Lines | SHA256 | Purpose |
| --- | ---: | --- | --- |
| `budget.py` | 441 | `3f1bbb3a523e453f2cc8044b8ce502a2138e34d0b036c33a29d445ad787dfcba` | Persistent caps, journal, crash reservations and work counts |
| `smooth_field.py` | 672 | `c04cc667c0138dd57bd554940bd9a37684347e78549ecc139bfd4061d5452883` | Full D44 tree, Gaussian preparation, mixed partial and N=64 sample |
| `fixtures.py` | 469 | `efc36545f60775bc196813f1a50a622f5d287e0f810cedb66b80ced4c7e73dc2` | Independent dense covariance and derivative fixtures |
| `experiment.py` | 1033 | `512e28e1b0efd774ec058e1a854fbbf53181b2217bf6dbac0c2ccd379dba9ec9` | Frozen cells, opaque harness, references, preflight, official and replay drivers |
| `driver.py` | 83 | `73d2e78e89325170b9db5b1775ba65edfef40f13f648da8d8cba26916301b827` | CLI with explicit modes and official acceptance gate |
| `source_checks.py` | 103 | `d492f0107cb6672374e5383e201e79c41db63972fca83b7cf2cddda4bbfab53f` | Read-only configuration/API checks |

`README.md` has 24 lines and SHA256
`ca03a8f5872b211667531d1682bda55bbc2d407232329c42ff6e91da95adb2dd`.
Generated `__pycache__` files are not source and are excluded from the source
manifest.

## 3. Estimator correspondence

For every identifier, the driver constructs exactly

```text
Generator(PCG64DXSM(SeedSequence([seed, cell_index, sample_index, tag])))
```

with cell indices ordered by `kappa=0.01` configurations 1 through 6 and then
`kappa=0.1` configurations 1 through 6. Tag 1 is preflight. Tag 0 is shared by
the later official run and its exact replay. The final environment is Python
3.11.15, NumPy 2.4.6, mpmath 1.3.0, arm64 macOS, and binary64 arithmetic.
The implementation manifest retains the full `numpy.show_config()` record.

The clock generator uses root-first DFS preorder and visits children from left
to right. It makes one scalar `Generator.exponential(scale=1/rate)` call for
every attempted segment, including terminal segments. A separate attempted
draw counter is incremented before this call; exact generated nodes are the
nodes appended after a valid lifetime. Tree validation uses one chronological
prefix-height pass, so its work is linear in the finite tree rather than a
leaf-by-ancestor traversal.

The Gaussian pass makes one vector call
`Generator.standard_normal(size=(segment_count,), dtype=float64)`. It draws an
entry for every segment, including a zero-length edge, and multiplies by
`sqrt(kappa*length)`. It computes the guarded chronological recursion in
unscaled time units, builds the physical aggregate from these same edge
Gaussians, forms every physical root-to-leaf sum, and subtracts the actual
aggregate. The Fourier damping variance is `kappa*a_T`. The sampler therefore
uses the residual leaf positions and common damping together; it never damps
unmodified leaf sums.

After one scalar uniform draw, the sampler uses
`Generator.choice(n, size=(j,), replace=False, shuffle=True)` when `n>=j`.
It evaluates the complete recursive leaf polynomial in all `2^j` selected
corner substitutions, multiplies by `(n)_j`, and uses each observed `v-g`
exactly once. It inserts no `1/j!` and no additional delta power. If `n<j`, it
returns the full 129-entry exact-zero array without tuple selection or opaque
query.

The result is one finite array

```text
[constant, cos(1), sin(1), ..., cos(64), sin(64)]
```

with the positive sine convention in `02h`. The N=4, 16 and 64 products are
exact prefixes of this single array and cause no new acquisition. The known
base and opaque evaluator are separate callables. The core sampler has no cell
direction, synthetic profile or analytic reference input. The only raw
unknown-profile formula exists in the outer experimental harness.

## 4. Persistent accounting and abort semantics

`artifacts/smooth-field-component/budget_journal.jsonl` is canonical. Every
mutation is appended and fsynced before the compact state is atomically
replaced. Recovery replays any journal event newer than the compact state.
The initial record fixes prior E5 opaque calls at zero.

Every opaque invocation performs an atomic phase/global capacity check,
increments the persistent counters and fsyncs the journal before entering the
user callback. Exceptions, duplicate locations, constant profiles and repeats
therefore remain charged. Segment generation reserves persistent capacity in
blocks of 1024 before drawing. A caught failure commits the exact node prefix
and exponential-attempt count. A hard process crash leaves the unresolved
reservation charged and blocks further generation until independent audit; it
does not silently reset or estimate the missing work.

Gaussian, uniform, tuple and known-evaluator work is reserved before its
scheduled operation. On a failed sample those fields are conservative charged
work reservations and must not be described as exact realized calls. Opaque
calls and individual exponential attempts have the stronger per-entry charge
semantics. Failure records state this distinction. A nonfinite Fourier output
carries its raw attempted coefficient array into retained failure evidence.
Caught official failures also retain every completed row in the current
partial chunk, failure metadata and the budget snapshot; they stop the suite
without redraw, omission or zero fill.

The frozen caps are preflight 8192 opaque calls, official 245760, replay 864,
global 300000, 100000 segments in one tree, 10000000 generated segments over
all versions and phases, and 1800 seconds for the official suite. The official
timer begins only after source/preflight acceptance gates and includes sample
work, persistent accounting, metadata and array serialization.

## 5. Mandatory deterministic fixtures

The final preflight ran one-leaf, positive common-ancestor star, unbalanced and
zero-terminal-edge trees. For each it independently built the dense shared-path
matrix `C`, derived leaf weights from the chronological recursion, and checked:

- nonnegative weights summing to one;
- `C w = a_T 1` and `tau/n <= a_T <= tau`;
- the edge-coefficient residual covariance equals
  `kappa*(C-a_T*11^T)`;
- the actual sampled edge-normal array gives the same physical aggregate and
  actual residual vector as the independent coefficient map;
- zero-length edge Gaussians are exact floating zero.

The mixed-partial fixtures compare signed full-tree corner passes against a
separate recursive chain-rule implementation. They check cubic `j=3` gives
partial `-1/2` and weighted value `-3`, cubic `j=2` at base `1/4` gives
`-1/8` and `-3/4`, and quintic `j=2` gives `-1/320` and `-1/16`. The fixture
record explicitly states no factorial division and no extra delta power.

The remaining fixtures check a positive sine coefficient at `U=1/4`, the H2
normalization on constant and cosine examples, and the one-leaf `n<j` path.
The last uses an opaque callback that raises if entered; the returned full
array was exactly zero and the callback was not invoked.

Frozen tolerances are covariance relative `5e-12`, covariance absolute
`5e-13`, mixed-partial relative `2e-13`, mixed-partial absolute `2e-14`, and
exact-formula relative/absolute `2e-14`. These are binary64 correspondence
checks, not formal matrix or independence proofs.

## 6. References and bounded preflight results

Analytic targets were evaluated with mpmath 1.3.0 at 100 decimal digits and
then converted once to Python binary64. They are not certified intervals. The
nonzero binary64 target coefficients for cells 0 through 11 are:

| Cell | Mode | Binary64 hex |
| ---: | --- | --- |
| 0 | cosine 1 | `0x1.31eca2338d473p-3` |
| 1 | cosine 1 | `0x1.0684ffad27105p-3` |
| 2 | constant | `-0x1.0dc12a6992d01p-6` |
| 3 | constant | `-0x1.167df81339b0ap-7` |
| 4 | cosine 1 | `0x1.bac43d592d7ccp-4` |
| 5 | constant | `-0x1.bb5b8f458827cp-12` |
| 6 | cosine 1 | `0x1.f7642cb3bb8dap-5` |
| 7 | cosine 1 | `0x1.aff83dc9a1052p-5` |
| 8 | constant | `-0x1.0dc12a6992d01p-6` |
| 9 | constant | `-0x1.167df81339b0ap-7` |
| 10 | cosine 1 | `0x1.72b2e2d3b4cb6p-4` |
| 11 | constant | `-0x1.bb5b8f458827cp-12` |

The complete decimals and target-array hashes are in
`preflight-v1/analytic_references.json`, SHA256
`fa389cc6f62b0229b7635f415341d2486ee6c8d00579013ae249805d1c35ec60`.

The final bounded preflight is `runs/preflight-0002`. It used tag 1 only. For
each of 12 cells and three seeds it generated primary indices 0 through 3,
then regenerated index 0: 144 primary outputs plus 36 bitwise reproducibility
outputs. Results:

| Check | Result |
| --- | ---: |
| Planned/completed final outputs | 180 / 180 |
| Raw full N=64 arrays | 180 |
| Deterministic fixture aggregate | PASS |
| Bitwise coefficient repeats | 36 / 36 |
| Deterministic metadata repeats, excluding timers/artifact paths | 36 / 36 |
| Final-attempt opaque calls | 215, at most 300 by schedule |
| Final-attempt generated segments | 1728 |
| Final-attempt random-tree exponential attempts | 1701 |
| Unresolved reservations | 0 |
| Nonfinite outputs or retained sample failures | 0 |

The final result SHA256 is
`86a5fab94e718ef94074625bc968af16d727e41c06c34c07e5b0323c8d22a933`.
A separate read-only audit checked all 180 arrays, all metadata rows, fixture
flags, reference encodings, source hashes, budget state and every one of 2195
journal events. It made zero opaque calls and passed. Its stdout SHA256 is
`19732f8395de4af818d5a45aa1ddabfc97eb22d703fa7fbce236e00b728e5441`.

One earlier successful bounded preflight, `preflight-0001`, is intentionally
retained. It predates only the explicit official chunk-serialization timing
record; its estimator bytes were otherwise the same. It used 215 calls and its
result SHA256 is
`fed3381504e116662d4846a4a4bfcb7616c8456f5aabe93177f804456044d01c`.
It was not overwritten or relabeled as the final source run.

Consequently the cumulative persistent state after all T99 activity is:

| Counter | Cumulative value |
| --- | ---: |
| Opaque calls: preflight / official / replay / total | 430 / 0 / 0 / 430 |
| Completed samples: preflight / official / replay | 360 / 0 / 0 |
| Failed samples: preflight / official / replay | 0 / 0 / 0 |
| Generated segments | 3456 |
| Exponential attempts | 3402 |
| Gaussian variates reserved/generated on successful paths | 3436 |
| Uniform variates reserved/generated on successful paths | 362 |
| Tuple draw calls / selected indices | 286 / 430 |
| Known-evaluator positions reserved/evaluated on successful paths | 2442 |
| Active segment reservations / reserved capacity | 0 / 0 |

Thus 7762 preflight calls, 299570 global calls and 9996544 total generated
segments remain. No capacity is borrowed from E4, whose files and budget were
not touched.

## 7. Commands, logs and failed-attempt provenance

The pinned executable for every Python command was
`/opt/miniconda3/envs/parabolab/bin/python`. Direct stdout, stderr, cwd,
timestamps and exit files are under `preflight-v1/checks/`. The decisive
commands were:

```text
# cwd: repository root
/opt/miniconda3/envs/parabolab/bin/python -m py_compile [six implementation Python files]

# cwd: code/smooth-field-component-v1
/opt/miniconda3/envs/parabolab/bin/python source_checks.py
/opt/miniconda3/envs/parabolab/bin/python driver.py preflight

# cwd: repository root
/opt/miniconda3/envs/parabolab/bin/python artifacts/.../preflight-v1/audit_preflight.py
```

Final-source records `syntax-005`, `source-check-004`,
`preflight-command-002` and `audit-002` all exited zero. The preflight stderr
contains only NumPy's warning that optional `pyyaml` is absent from
`np.show_config`; it did not affect sampling or evidence.

All unsuccessful wrappers are retained:

- `syntax-001` ran the compiler but its logging wrapper then assigned zsh's
  read-only variable `status`; the wrapper exited 1. Compiler stdout/stderr are
  retained and empty. No sampler or acquisition ran.
- `source-check-001` created its output directory relative to the code cwd,
  then attempted absolute redirection into a missing evidence subdirectory.
  Python never entered. The wrapper failure is recorded with exit 1 and made
  no acquisition.

The later `syntax-002`/`003`/`004`, `source-check-002`/`003`, preliminary
`preflight-command-001`, and preliminary `audit-001` records remain as honest
development provenance. The initial two wrapper attempts did not capture full
start/end timestamps; their evidence says so rather than inventing them. All
decisive final-source commands have recorded UTC start and completion times.

## 8. Official and replay gates

The prepared official command is not executable against merely a passed local
preflight. It requires a root-created acceptance JSON with exactly:

```text
verdict = accepted_for_official
protocol_sha256 = 1866585a86fcfceb0f9b05f632dae093d3c6e03f4ab005b4eae02fbfa5b27612
implementation_manifest_sha256 = 901d4b7ad115912fd1ce9e28d77c0a3c37b9dd171b0e6dd851a7cce7014967ed
preflight_result_sha256 = 86a5fab94e718ef94074625bc968af16d727e41c06c34c07e5b0323c8d22a933
```

It also rehashes current source before generating output. This is the root
source/preflight acceptance gate required by T99, not a user-approval gate.
The later replay driver accepts only a complete official result, visits exactly
indices 0 through 7 in all 36 cell/seed sequences, uses the original tag-0
streams, charges new replay calls and compares raw coefficients bitwise.

## 9. Interpretation and limitations

T99 establishes that the frozen finite implementation and bounded tag-1
checks are ready for root source/preflight review. The dense fixtures directly
address the T98 coverage limitation: the six analytic means alone cannot
identify cross-leaf residual covariance, and zero sine targets alone cannot
identify the sine convention.

No official coefficient mean, H2 risk, batch statistic, standardized
discrepancy, scientific plot or sampler PASS is reported because tag 0 was not
run. This task provides no long-time recursion experiment, adaptive or sparse
D48 estimator, paid reconstruction result, spatial PDE certificate, universal
Hilbert moment theorem, minimax theorem, finite-bit guarantee, priority claim
or award-level conclusion. The full tree/PDE correspondence remains the
accepted conventional argument identified by the protocol; the named finite
T89/T93 prerequisites do not formalize that complete bridge.
