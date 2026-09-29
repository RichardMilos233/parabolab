#!/bin/zsh

source_path=/Users/michael/Desktop/NTU/fyp/parabolab/formal/EstimatorIntegrity/GaussianCommonComponent.lean
pattern='sorry|admit|axiom|native_decide|unsafe|implemented_by|ofReduceBool'

print -r -- "started_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
print -r -- "cwd=$PWD"
print -r -- "source=$source_path"
print -r -- "pattern=$pattern"
rg -n "$pattern" "$source_path"
scan_status=$?
if (( scan_status == 1 )); then
  print -r -- "result=no matches"
  print -r -- "exit_code=0"
  print -r -- "ended_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit 0
fi
print -r -- "result=matches or scan error"
print -r -- "exit_code=$scan_status"
print -r -- "ended_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
exit $scan_status
