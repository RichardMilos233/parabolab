#!/bin/sh
printf 'lean: '
~/.elan/bin/lake env lean --version
printf 'toolchain: '
cat lean-toolchain
printf 'mathlib: '
git -C .lake/packages/mathlib rev-parse HEAD
