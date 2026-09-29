#!/bin/sh
label="$1"
output="$2"
shift 2
source_file="EstimatorIntegrity/HilbertSamplingRisk.lean"
{
  printf 'label: %s\n' "$label"
  printf 'started_utc: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
  printf 'cwd: %s\n' "$(pwd)"
  printf 'source_sha256: '
  shasum -a 256 "$source_file" | awk '{print $1}'
  printf 'command:'
  printf ' %s' "$@"
  printf '\n--- stdout+stderr ---\n'
  "$@"
  exit_code="$?"
  printf '%s\n' '--- end stdout+stderr ---'
  printf 'exit_code: %s\n' "$exit_code"
  printf 'finished_utc: '
  date -u '+%Y-%m-%dT%H:%M:%SZ'
} > "$output" 2>&1
exit "$exit_code"
