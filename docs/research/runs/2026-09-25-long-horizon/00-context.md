# Long-horizon branching research — context

Date: 2026-09-25. Request: investigate what changes when the horizon is extended beyond the short-time lambda experiments; search and evaluate directions, then **theory → Lean → numerical implementation**. Chinese presentation requested by conversation. Skill: math-auto-research 0.2.0; lean-proof and surgical-code guidelines also used. No background automation or publication requested.

Repository revision: `65dca46e42db1c80cdf9ddd8eed6a415148c37f3`. Initial dirty files are `demo/rate_variance.py`, `parabolab/rate_variance.py`, `tests/test_rate_variance.py`; their original patch is saved alongside this file and will not be edited. Prior outputs are historical evidence, not automatically fresh checks.

## Object and established baseline

The PDE is u_t + (1/2)u_xx + u-u³=0. The raw derivative-coded tree has a common exponential rate lambda and positive tuple proposals. Existing exact nonnegative six-code moment closures and rational certificate machinery are available. At flat terminal phi=1/2 the prior run proved the full root second-moment threshold

T₂(lambda,p)=log(1+lambda² p C)/lambda,
C=integral_0^infinity [9/64+v/16+(9/2)v²+6v³]^-1 dv.

Common p is the first-label probability at F0,F1,F2. The prior strict nonconstant wave improvement was certified only through T=.05. Its own next-step record says the gain there is small. Neither a failed envelope search nor an unstable sample variance proves explosion.

## New target

First map the actual long-horizon limits of the existing estimator, separating finite-tree computational nonexplosion, finite second moment, and absolute integrability. Derive an exact all-supported-proposal absolute-moment ceiling for the raw flat example; use a literature-known bounded majority representation as a separate long-time comparator for flat and nonconstant data. Changes of representation must never be mislabeled as improved lambda within the same estimator.

The original coded tree, PDE and all published numerical records stay available. No NN/backbone work belongs here. A new method should retain the project's solver/Curve interface.

## Environment and evidence

Python: /opt/miniconda3/envs/parabolab/bin/python. Lean: /Users/michael/.elan/bin/lake, pinned Lean/mathlib v4.33.0. Available scipy/numpy and local mathlib allow scalar reference calculations, exact rational checks and formal algebra/tree induction. CPU only; numerical protocol must cap workloads before sampling and retain every scheduled root. No depth/node clipping may masquerade as a full estimator.

Root model: inherited GPT-6 family (precise serving identifier unavailable). Research agents explicitly requested gpt-6-astra/max; implementation agents will use gpt-5.6-sol/xhigh per skill routing. Requested configurations are distinct from independently verified server metadata.
