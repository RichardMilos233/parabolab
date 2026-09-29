#!/bin/zsh

print -r -- "formal_cwd=$PWD"
print -r -- "lean_toolchain=$(<lean-toolchain)"
/Users/michael/.elan/bin/lake env lean --version
print -r -- "lean_exit_code=$?"
/Users/michael/.elan/bin/lake --version
print -r -- "lake_exit_code=$?"
git rev-parse HEAD
print -r -- "project_git_exit_code=$?"
git -C .lake/packages/mathlib rev-parse HEAD
print -r -- "mathlib_git_exit_code=$?"
