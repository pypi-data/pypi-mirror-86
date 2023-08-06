#!/bin/sh

grep -A200 'commandline tools' .github/workflows/ci.yml | \
  grep -B200 'name: Build' | \
  head -n -1 | \
  tail -n +3 > /tmp/jojki

cat | sh -ex /tmp/jojki 2>&1 | cat
