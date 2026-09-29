# Retrospective development-failure summary

This is a retrospective summary of material interactive failures observed while
developing `UniformSliceConditioning.lean`; it is not represented as a complete
raw transcript. Final build and audit commands are captured directly in their
own logs with exit codes.

- The first conditional-law draft failed to compile because the generic finite
  conditioning lemma mixed proposition and Boolean notation and did not reduce
  the restricted singleton mass. The proof was replaced by an explicit
  singleton split and ENNReal normalization.
- The first compatible-family count proof left natural-subtraction goals that
  `omega` could not infer from opaque subtractions. Rewriting with
  `Nat.sub_sub`, plus the disjoint-union cardinality identity, resolved them
  without changing the statement.
- The first next-coordinate proof used unavailable Finset lemma spellings and
  did not establish the probability instance for the mapped measure. The final
  proof uses the pinned `card_insert_of_notMem` API, explicit endpoint counting,
  and `Measure.isProbabilityMeasure_map`.
- The first real-ratio proof attempted to cast a natural subtraction directly.
  The final proof first records the required subtraction order and rewrites with
  `Nat.cast_sub`.

Every failure above was a Lean translation or API issue. No mathematical
assumption, constant, endpoint, or target measure was weakened.
