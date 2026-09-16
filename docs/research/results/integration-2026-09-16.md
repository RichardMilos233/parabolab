# Research integration into main — 16 September 2026

The user authorized organizing and integrating the completed lambda
research into `main`. At the start of this integration check, local
`main` was already at `c82d536` and contained all three research commits:

- `2f26313`: corrected binary control and replicated rate/cost study;
- `05012ff`: full-tree Allen–Cahn certificates and associated Lean lemmas;
- `ff58620`: weighted-profile selection, exact certificates, reuse study
  and ten additional Lean lemmas.

No additional merge of these commits was necessary. The later rate
sensitivity tooling in `c82d536` remains part of main. The older
`research/estimator-integrity` branch is not an ancestor by commit ID,
but `git cherry -v main research/estimator-integrity` marks all eleven
commits as patch-equivalent changes already integrated. There was no
missing research patch to import.

## Organization and research emphasis

Current navigation, the proof registry and report headers now identify
the work as integrated. Original research-branch names and experiment
dates remain as provenance. The user clarified that algorithmic and
mathematical contributions are primary: recursive optimization, moment
bounds, approximation error and proposal design. Runtime comparisons
remain supporting evidence and do not determine whether a theoretical
direction is worth investigating.

The main distinctions remain explicit:

- The full-tree certificate combines a candidate upper bound and a
  global optimum lower bound to bound objective excess.
- The profile selector chooses one common scalar rate for several
  starting states; it is a weighted extension of the single-state
  objective, not a new solution of the recursive dependence problem.
- Mathematical proofs, exact numerical verification, Python tests and
  Lean coverage have separate scopes. Integration does not strengthen
  any mathematical or statistical claim.

## Verification on the integrated source

The following commands were executed against the source at `c82d536`;
this integration update changes documentation only:

```sh
/opt/miniconda3/envs/parabolab/bin/python -m pytest -q
```

Result: **255 passed, 14 slow tests deselected**, in 95.07 seconds.

```sh
cd formal
/Users/michael/.elan/bin/lake build
```

Result: **build completed successfully, 3,391 jobs**.

All three existing rational witness archives were rechecked using the
current verifier implementations:

```sh
python examples/certified_allen_cahn_rate.py --verify docs/research/results/rate-certificate/witnesses.json.gz
python examples/certified_wave_rate.py --verify docs/research/results/wave-certificate/witnesses.json.gz
python examples/certified_profile_rate.py --verify docs/research/results/profile-certificate/witnesses.json.gz
```

Each returned `all_witnesses_valid: true`. These commands used the same
conda Python executable as the test command. No Monte Carlo experiment
or timing study was rerun. Documentation changes passed `git diff --check`.

## Historical evidence and later source changes

All source hashes in the flat, wave and profile certificate summaries,
and the profile-efficiency benchmark metadata, match the corresponding
files at `ff58620`. Profile witness and linked metadata digests also match
the saved summary.

The later `c82d536` commit changed `parabolab/library.py` and
`parabolab/rate_optimization.py`. Therefore some archived source hashes
intentionally do not match current files: the records describe the
original execution, not a new experiment on today's code. The earlier
rate-cost driver's post-run label-only correction remains documented
in its original report.

Raw measurements, protocols, exact witnesses, execution snapshots and
their recorded hashes were preserved. Hash-bound mathematical notes,
including `wave-numerical-certification-route.md`, retain their original
dated merge-status text; this integration record supersedes that status
without modifying the archived evidence.

This integration is local. No remote push was performed.
