# T66: independent audit of the frozen positive-query experiment

Date: 2026-09-29 (Asia/Jakarta). Scope: independent source/protocol
correspondence, complete stored-evidence audit, independent statistics, and the
prespecified replicate-0 replay only.

**Result: PASS.** The frozen official result is internally consistent across
all 180 cells, 18,720 outputs and 336,883,488 point calls. Every archived
replicate mean, output, positive-return count and query count agrees bit-for-bit
between its journal and NPZ array. Every batch count and stored batch-sum
reduction reproduces its mean; every output reproduces from that mean using the
frozen `exp(T)`/`hypot` transform. Independently constructed PCG64 states agree
with every stored before state, and `PCG64.advance(n)` agrees with every stored
after state. All 20,448 official ledger increments and cumulative totals agree.

The exact prespecified replay—replicate index 0 of every cell—then made
30,075,636 point calls and matched all 180 archived means, outputs,
positive-return counts, observation/query counts, batch counts, batch sums and
before/after RNG states bit-for-bit. This was one subset replay, not a full
18,720-output replay. No mismatch or failed/partial attempt occurred, so no
automatic retry was made.

## Frozen gates and correspondence

Before any replay call, the independent auditor froze its source hash, 559
input hashes and the complete 180-row replay plan in `audit_manifest.json`.
The selection rule was fixed as replicate index 0 of every cell; it was not
chosen from observed errors. The audit source does not import the producer.
It independently implements PCG64/SeedSequence streams with keys
`(T_index,z_index,schedule_index,0)`, binary64 batches of at most 131,072,
one `numpy.sum(..., dtype=float64)` per batch, ordered `math.fsum`, one division
by `n`, the actual wrapped bump oracle, and the `hypot` transform.

The following producer bindings matched before the stored audit and again
before replay:

| Frozen input | SHA256 |
| --- | --- |
| Producer source | `81eb2b122d325eca97d144adc00380114558c5ad35a830d9d4062fa95f63df08` |
| v2 execution manifest | `9417c6dc18b3c761ee7cdf38c4cc8ececbfc048c0869b0fea5b96acaaae47bd5` |
| v2 preflight result | `ae85c9f1712ada9697bedc472ea273bf692b2cc7c4f0813f58a63ce085380c1c` |
| Frozen protocol | `8713593424011f0cb713e19125bccfff1dacf25e9ce401c68ff6867aa8c9fe9b` |
| T63v2 report | `4f7959a3b673bf1af78ade163ae13276afb72d243d2b85b72a232731c9b9839d` |
| Root clearance | `bec557a2ac4333151c40b04c69a62b3b422ffdb6b94873c57048b6f150e8b9a9` |
| Official PASS result | `818f4f54da86417d1d3df139bbe717d58e371fc8c97acbffcdf73e6bbb064ac3` |

The root clearance binds the displayed source, manifest and preflight hashes;
the official result binds all four. The v1 and v2 preflight ledgers each have
220 valid cumulative rows and 655,633 calls. Together with the official
ledger, actual activity before replay was 338,194,754 calls. The replay raised
the actual total to 368,270,390, below the 500,000,000 cap. All 342 protected
initial files had zero missing paths and zero hash mismatches.

Source/protocol correspondence also passed: the five integer schedules and
replication counts match the frozen table; streams use the required roots and
four-index keys; the estimator interface is opaque; zero inputs still incur
all calls; the stored-width mass supplies the scalar reference; and counts are
charged per actual vector element. The official timing fields retain their
actual meanings: 5.896929431706667 seconds raw inclusive estimator-call wall
time, 1.0319401659071445 seconds measured ledger accounting during those calls,
and 4.864989265799522 seconds after that measured subtraction. The last value
is an accounting-excluded measurement, not a pure-compute certificate.

## Independently recomputed statistics

`stored_audit.json` contains bias, MSE, RMS, zero count/frequency and actual
queries for every one of the 180 seed cells. Its pooled values use
`math.fsum` over every raw squared error from all three seeds, divide by the
pooled output count, and only then take the square root. The 18,720 raw outputs,
references, errors and squared errors are preserved in `statistics_raw.npz`.
The three zero-query constants 0, 0.5 and 1 are included with zero query cost.

Pooled RMS and zero-output frequency (`RMS / zero frequency`) are:

| nominal z | schedule | T=12 | T=16 | T=20 |
| ---: | --- | ---: | ---: | ---: |
| 0 | growing_0p125 | 0 / 1 | 0 / 1 | 0 / 1 |
| 0 | growing_0p5 | 0 / 1 | 0 / 1 | 0 / 1 |
| 0 | growing_2 | 0 / 1 | 0 / 1 | 0 / 1 |
| 0 | theorem_96 | 0 / 1 | 0 / 1 | 0 / 1 |
| 0 | fixed_51 | 0 / 1 | 0 / 1 | 0 / 1 |
| 0.25 | growing_0p125 | 0.187648938 / 0.117188 | 0.194139873 / 0.132812 | 0.198575829 / 0.109375 |
| 0.25 | growing_0p5 | 0.096110278 / 0 | 0.103557981 / 0 | 0.108472082 / 0 |
| 0.25 | growing_2 | 0.0549252493 / 0 | 0.0536839534 / 0 | 0.0544439043 / 0 |
| 0.25 | theorem_96 | 0.00893311185 / 0 | 0.00778642566 / 0 | 0.00782647779 / 0 |
| 0.25 | fixed_51 | 0.192583636 / 0.0963542 | 0.319997738 / 0.757812 | 0.249495443 / 0.976562 |
| 1 | growing_0p125 | 0.270076764 / 0.0104167 | 0.278578452 / 0.015625 | 0.284885701 / 0.0130208 |
| 1 | growing_0p5 | 0.135188851 / 0 | 0.127344435 / 0 | 0.13317471 / 0 |
| 1 | growing_2 | 0.0620218603 / 0 | 0.0686600877 / 0 | 0.0624533235 / 0 |
| 1 | theorem_96 | 0.00897003819 / 0 | 0.00907352776 / 0 | 0.0118108321 / 0 |
| 1 | fixed_51 | 0.261577049 / 0.0130208 | 0.596677033 / 0.53125 | 0.68793864 / 0.921875 |
| 4 | growing_0p125 | 0.117776651 / 0 | 0.103131359 / 0 | 0.125748452 / 0 |
| 4 | growing_0p5 | 0.0176574027 / 0 | 0.020851067 / 0 | 0.0172039679 / 0 |
| 4 | growing_2 | 0.00697304853 / 0 | 0.00738755517 / 0 | 0.00747264876 / 0 |
| 4 | theorem_96 | 0.000991252516 / 0 | 0.00107528444 / 0 | 0.000953288348 / 0 |
| 4 | fixed_51 | 0.127886901 / 0 | 0.681393669 / 0.330729 | 0.920394307 / 0.880208 |

The theorem schedule uses 24 pooled outputs at each `(T,z)` (8 per seed); the
other schedules use 384. Its actual `n` is 38,730, 286,172 and 2,114,541 for
T=12,16,20. The other growing schedules use `(51,373,2754)`,
`(202,1491,11014)` and `(807,5962,44053)` respectively; fixed_51 always uses
51.

The finite data show horizon-stable pooled RMS for the growing schedules and
sharp loss for fixed_51 as the support narrows. The zero-query baselines remain
scientifically relevant: constant 0 is exact for the zero input; at nominal
z=4, constant 1 has RMS 0.0298575 and beats growing_0p125 and fixed_51, while
the larger-query schedules do better. At nominal z=1, constant 0.5 has RMS
0.207107 and can beat the smallest growing schedule. No baseline was hidden.

The displayed RMS is always against the computed binary64 scalar surrogate.
For each stored statistic `r`, the report separately records the conventional
PDE-bias interpretation `[max(0,r-1/32), r+1/32]`. For example, theorem_96's
largest nonzero pooled scalar RMS is 0.0118108321 at `(T,z)=(20,1)`, mapping to
`[0,0.0430608321]`. This interval uses the conventional PDE theorem and finite
Euclidean comparison; it is not an actual PDE numerical solve and is not a
rigorous floating-point enclosure.

## Replay, plots and timing

The replay ledger has 396 durably flushed batch rows and ends at exactly
30,075,636 replay calls; the journal has 180 durably flushed PASS rows. Replay
wall time was 0.6423926251009107 seconds and includes RNG, actual bump-oracle
evaluation, arithmetic, JSONL writes and `fsync`. The read-only stored audit
took 1.7392914169467986 seconds. Neither is labeled pure compute.

The scientific PNG and SVG show every schedule and all three zero-query
baselines, with pooled curves, individual-seed markers, actual `n`, per-seed
replication counts, the zero case, and the scalar/PDE-bias distinction. The PNG
was viewed after generation. Its first render had a title/legend overlap; a
zero-oracle-call layout-only rerender corrected that defect, and
`plot_result.json` preserves the superseded hashes.

## Audit artifacts and hashes

| Artifact | SHA256 |
| --- | --- |
| `numerics/audit_positive_query_sampling.py` | `2615203c60973fd0908bd185b7cc3d8d4b3eb1b0b1ac6f9bdd4bcc4b6128b009` |
| `audit-v1/audit_manifest.json` | `7f25110439ad49b341bffedc54539279108a355f5223d814824787fa6bf9259f` |
| `audit-v1/stored_audit.json` | `f1f48b74996543a9f7de1aca6c0ffedbb54e34d251d046aa820b0cf9cea5f2da` |
| `audit-v1/statistics_raw.npz` | `bd78b8fae2868fc53d6bc014076dce6d769132d4acf7129049bc0cad59a9bb8f` |
| `audit-v1/replay_activity.jsonl` | `7b03c4ad3907b385f44c81034307c0a25ee7de162f3d0f8f6174dcd00fad9b45` |
| `audit-v1/replay_journal.jsonl` | `febc877cc33fe2e4f45e3ca0dfe5377e39ffcdd671d1baa76d17cbf557290deb` |
| `audit-v1/replay_result.json` | `788394e129bebda45608a926b118cc405e515f2986f60a3acc7992713ea3ed2e` |
| `audit-v1/positive_query_audit.png` | `3c18c54eb64f89473cafef04760a2fb6ea2edba8371c353cc1f9a481daebef2f` |
| `audit-v1/positive_query_audit.svg` | `6832d357371ff8e6f86557746c13ccfc279ba9a386072830aedd1f049f279849` |
| `audit-v1/plot_result.json` | `87678c8986c82ace7e002d0ca53b527f4898b73e552099866d42a4778f40e64e` |

The final `audit_result.json` hashes every other listed audit output and this
review. Its own hash is necessarily external to its contents.

## Residual limitations

The replay covers 180 of 18,720 outputs, exactly as prespecified. The remaining
outputs received complete stored-evidence, arithmetic, hash, count and RNG-state
checks, but no oracle replay. The scalar reference and statistics use ordinary
binary64 without a rigorous enclosure. PCG64/binary64 execution is a
reproducible numerical implementation, not a certified iid-real-law bridge.
No PDE was numerically solved. This finite family does not empirically prove a
minimax theorem or asymptotic rate, and the audit makes no novelty claim.
