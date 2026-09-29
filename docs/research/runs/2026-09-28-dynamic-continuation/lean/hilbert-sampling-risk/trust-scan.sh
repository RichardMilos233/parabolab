#!/bin/sh
source_file="EstimatorIntegrity/HilbertSamplingRisk.lean"
if rg -n 'sorry|admit|axiom|native_decide|unsafe' "$source_file"; then
  printf '%s\n' 'forbidden token found'
  exit 1
else
  status="$?"
  if [ "$status" -eq 1 ]; then
    printf '%s\n' 'no forbidden tokens found'
    exit 0
  fi
  exit "$status"
fi
