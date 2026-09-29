#!/bin/zsh

log_path=$1
shift

{
  print -r -- "cwd=$PWD"
  print -r -- "command=$*"
  "$@"
  command_status=$?
  print -r -- "exit_code=$command_status"
  exit $command_status
} >"$log_path" 2>&1
