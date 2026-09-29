#!/bin/zsh

source_path=/Users/michael/Desktop/NTU/fyp/parabolab/formal/EstimatorIntegrity/UniformSliceConditioning.lean
pattern='sorry|admit|axiom|native_decide|unsafe'

print -r -- "source=$source_path"
print -r -- "pattern=$pattern"
rg -n "$pattern" "$source_path"
scan_status=$?

if (( scan_status == 1 )); then
  print -r -- "result=no matches"
  exit 0
fi

print -r -- "result=matches or scan error"
exit $scan_status
