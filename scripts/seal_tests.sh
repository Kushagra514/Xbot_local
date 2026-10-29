#!/usr/bin/env bash
# Run this ONLY when YOU (the human) have edited tests/. It records the hash the gate compares against.
set -eu
cd "$(dirname "$0")/.."
find tests -name 'test_*.py' -type f | sort | xargs sha256sum | sha256sum | cut -d' ' -f1 > state/tests.sha256
echo "sealed: $(cat state/tests.sha256)"
