# Claim and evidence ledger

- **C1 — Direct prior art exists.** Page et al. 2021/2024 perform latent Fourier analysis via spatial translations; FINE 2025 explicitly builds in Fourier compression. Status: primary-source literature checked; see report references 1–3. Not an exhaustive novelty determination.
- **C2 — Raw latent PCA does not identify a unique physical basis.** Status: explicit coordinate counterexample and covariance transformation algebra in report §4. No Lean formalization; no claim of new theory.
- **C3 — Current attention model enforces positive affine input/output equivariance.** Assumptions: same grid/query, positive scale, neither standard deviation clamp active, deterministic forward. Evidence: `opnet.py` + `setnet.py` algebra; independent code review; one untrained float64 numerical check. Applies to this implementation, not arbitrary transformers.
- **C4 — Allen–Cahn conflicts with that amplitude constraint.** Status: exact initial-time third-harmonic derivative; fixed-time small-amplitude asymptotic derivation; triangle-inequality approximation lower bound. Only the initial derivative was numerically checked. No full rollout or trained-model error measured.
- **C5 — Decoder tangent can be a physical Fourier mode under explicit assumptions.** Status: conventional differentiability/intertwining argument in report §9; requires a translation-fixed base point, local decoder equivariance for all shifts, and nonzero derivative. Does not apply automatically to current attention normalization or finite-amplitude decoding. Independently reviewed, not formalized.
- **C6 — Trained models have Fourier-aligned latent subspaces.** Status: UNTESTED hypothesis. No checkpoint/latent experiment performed.
- **C7 — Proposed normalization modification improves generalization.** Status: PROPOSED only. No implementation or performance claim.

Reproducible numerical evidence: `check_attention_scaling.py`, `attention-scaling-check.json`. The test uses a smaller untrained attention instance; it corroborates the architecture algebra rather than benchmarking the historical trained winner.
