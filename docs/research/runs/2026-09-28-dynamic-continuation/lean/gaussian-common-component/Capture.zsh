#!/bin/zsh

set -u

if (( $# < 3 )); then
  print -u2 -- "usage: Capture.zsh OUTPUT CWD COMMAND [ARG ...]"
  exit 64
fi

output=$1
working_directory=$2
shift 2

{
  print -- "started_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  print -- "cwd=${working_directory}"
  print -n -- "command="
  printf '%q ' "$@"
  print
  print -- "stdout_stderr_begin"
  (
    cd "${working_directory}" || exit 125
    "$@"
  )
  exit_code=$?
  print -- "stdout_stderr_end"
  print -- "exit_code=${exit_code}"
  print -- "ended_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  exit ${exit_code}
} >| "${output}" 2>&1
