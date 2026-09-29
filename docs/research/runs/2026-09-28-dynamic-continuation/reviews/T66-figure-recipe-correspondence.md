# T66 figure recipe correspondence

Date: 2026-09-29 (Asia/Jakarta). Scope: packaging only, with no oracle calls,
statistics changes, ledger changes, or mutation of accepted audit evidence.

**Result: PASS.** The exact layout-only recipe retained from the accepted T66
render was archived as
`numerics/render_positive_query_evidence_v2.py`. It reads only the frozen T66
statistics and PASS replay record, verifies their hashes and the accepted
figure hashes, then renders into the new `figure-v2/` directory. It does not
import or execute the sampler or oracle.

## Exact recipe correspondence

The archived recipe preserves the accepted figure's:

- 4-by-2 panel layout and 15.5-by-18.5 inch canvas;
- subplot margins and spacing;
- horizon, level, schedule and zero-query baseline selection;
- colors, line styles, markers, sizes, alpha values and linewidths;
- pooled curves, individual-seed open markers and seed offsets;
- scalar-surrogate RMS, conventional `±1/32` PDE whiskers and actual query
  budgets;
- symlog thresholds, axis lower bounds, ticks, labels and grid;
- title, scope text, legend order, legend position and four-column layout;
- PNG DPI and title metadata.

The new PNG is byte-for-byte identical to the accepted PNG:

```text
accepted audit-v1 PNG  3c18c54eb64f89473cafef04760a2fb6ea2edba8371c353cc1f9a481daebef2f
new figure-v2 PNG      3c18c54eb64f89473cafef04760a2fb6ea2edba8371c353cc1f9a481daebef2f
```

`cmp` also returned success. The new PNG was opened at original detail and
visually checked: title, scope lines and legend do not overlap; all eight
series remain visible; zero-query values remain visible; per-seed and pooled
marks are distinguishable; and the scalar reference is clearly separated from
the conventional PDE-bias interpretation.

## Deterministic SVG packaging

The accepted SVG was produced with Matplotlib's default process-random SVG
element IDs and a live `dc:date` timestamp. Its byte hash therefore cannot be
the reproducibility target of the unchanged visual recipe. The archived
renderer makes only two serialization-level additions after constructing the
accepted figure:

1. `matplotlib.rcParams["svg.hashsalt"]` is fixed to
   `T66-positive-query-evidence-v2`;
2. SVG `Date` metadata is fixed.

These settings do not change the plotted data or layout. They give the new SVG
a deterministic serialization hash:

```text
accepted audit-v1 SVG  6832d357371ff8e6f86557746c13ccfc279ba9a386072830aedd1f049f279849
new figure-v2 SVG      b07b65f2d67cb4733fee71290f1971e77cfe55d350fee8ef5c78fa3215c35704
```

## Frozen inputs, command and environment

The renderer required these exact inputs:

| Input | SHA256 |
| --- | --- |
| `audit-v1/stored_audit.json` | `f1f48b74996543a9f7de1aca6c0ffedbb54e34d251d046aa820b0cf9cea5f2da` |
| `audit-v1/replay_result.json` | `788394e129bebda45608a926b118cc405e515f2986f60a3acc7992713ea3ed2e` |
| accepted `audit-v1/positive_query_audit.png` | `3c18c54eb64f89473cafef04760a2fb6ea2edba8371c353cc1f9a481daebef2f` |
| accepted `audit-v1/positive_query_audit.svg` | `6832d357371ff8e6f86557746c13ccfc279ba9a386072830aedd1f049f279849` |

Command actually run:

```text
MPLCONFIGDIR=/private/tmp/t66-mpl XDG_CACHE_HOME=/private/tmp/t66-cache /opt/miniconda3/envs/parabolab/bin/python docs/research/runs/2026-09-28-dynamic-continuation/numerics/render_positive_query_evidence_v2.py
```

Recorded environment: Python 3.11.15, Matplotlib 3.11.0, macOS arm64. The
renderer refuses to overwrite an existing output directory. Its measured
0.830866334028542-second wall duration includes JSON parsing, rendering and
serialization; it is not a pure-compute claim.

## New artifacts

| Artifact | SHA256 |
| --- | --- |
| `numerics/render_positive_query_evidence_v2.py` | `cb8e8d04591cf4976c984b157aa48e01e4ff47c34291224bab899962dd9c79f0` |
| `figure-v2/positive_query_evidence_v2.png` | `3c18c54eb64f89473cafef04760a2fb6ea2edba8371c353cc1f9a481daebef2f` |
| `figure-v2/positive_query_evidence_v2.svg` | `b07b65f2d67cb4733fee71290f1971e77cfe55d350fee8ef5c78fa3215c35704` |
| `figure-v2/render_result.json` | `5bd1f0a636bf611eb3c3994cc31699f23b51801a687fcfee0791b341f36ec56a` |

`render_result.json` binds the renderer source, all four frozen inputs and both
new figure hashes. It records zero oracle calls, zero ledger changes, no
statistics recomputation, and no modification of official or accepted audit
evidence.
