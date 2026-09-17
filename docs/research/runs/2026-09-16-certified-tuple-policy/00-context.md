# Context — 16 September 2026

This run **resumes** the existing ten-direction programme at its open direction 3 (continuation-aware tuple proposals), using direction 1's certificate machinery. The previous scalar/profile investigations are completed; frozen evidence is retained.

Objective: reduce variance of the existing coding-tree estimator through the common exponential rate lambda and labelled tuple probabilities q. Mathematical guarantees take priority over runtime. Keep the mechanism, likelihood weights and shared child position explicit. Multifactor Merton is inactive.

Initial checkout: `ff2fa5f4858c695dd125c3b1ca7cfe63372398e7`; clean working tree. Read: parent AGENTS.md, project CLAUDE.md, README, research/results indexes, latest integration record, prior directions, relevant proof-registry sections, proposal/moment/rate/Allen–Cahn mean and certificate notes, sampler, mechanism, proposal and certificate code. The parent's older reproduction counts are superseded by current project notes.

Earlier session retrieval identified “Plan ten future research directions” and its opening request; recent turn bodies were absent from the returned record. Inaccessible conversation details are not treated as evidence.

Historical checks at c82d536 (read, not rerun here): 255 non-slow Python tests, full Lean build, three rational archives reverified. Existing certificates cover raw-uniform Allen–Cahn flat/wave/profile at T=.05; they do not certify changed q.

Bottleneck: the classical square-root tuple rule needs actual continuation contributions. Those depend on every descendant's policy. Terminal scores and finite-depth quadrature do not guarantee full-tree improvement. The production callback sees `(code,t,x,tau,depth,tuples)` **before** the Brownian branch displacement; x is the birth position. Conditional scores must average products over the shared future branch position. Raw F tables retain two labels even when one is exactly zero.

Notation: M_q=E_q|H_q|², Phi_q its nonnegative first-event operator, A_i an old-policy conditional tuple contribution. The full-tree moment is the least zero-seeded fixed point under nonexplosion. Common integrable means transfer moment differences to variance differences.

Tools: `/opt/miniconda3/envs/parabolab/bin/python`, NumPy/SciPy/pytest; Lean 4.33.0/mathlib v4.33.0 using `/Users/michael/.elan/bin/lake`; CPU and existing rational verification infrastructure. Skill v0.2.0, general English profile. Root is the current GPT-6 agent (exact effort not exposed); T01 explicitly dispatched gpt-6-astra/max; T02/T03 gpt-5.6-sol/xhigh. No publication or background scheduling.

Bounded scope: derive safe full-tree policy improvement; test its gate and nonuniform closure; certify a first nonuniform control. Joint static (lambda,q) convexity supports future global optimization. General state/time-dependent policy construction and a certified joint optimizer remain open.
