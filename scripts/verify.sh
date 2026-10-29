#!/usr/bin/env bash
# The verifier: deterministic gate. Usage: bash scripts/verify.sh [tests/test_x.py]
# Exit 0 = accepted. Anything else = rejected; stdout explains why.
set -u
cd "$(dirname "$0")/.."

# 1. Acceptance tests must be untouched (sealed by the human with scripts/seal_tests.sh)
if [ -f state/tests.sha256 ]; then
  cur=$(find tests -name 'test_*.py' -type f | sort | xargs sha256sum | sha256sum | cut -d' ' -f1)
  if [ "$cur" != "$(cat state/tests.sha256)" ]; then
    echo "GATE FAIL: tests/ was modified. Agents may not edit tests."
    exit 1
  fi
fi

# 2. Mode A policy: no network / posting / browser-automation libraries
if grep -rEn "^[[:space:]]*(import|from)[[:space:]]+(requests|tweepy|selenium|playwright|httpx|xdk|urllib\.request|socket|webbrowser)\b" src/ 2>/dev/null; then
  echo "GATE FAIL: forbidden import (Mode A: the bot only drafts; a human posts)."
  exit 1
fi

# 3. Must at least compile
if ! python3 -m compileall -q src; then
  echo "GATE FAIL: syntax error"
  exit 1
fi

# 4. Acceptance tests
target="${1:-tests}"
if [ -d "$target" ]; then
  PYTHONPATH=src python3 -m unittest discover -s "$target" -t . 2>&1 | tail -n 40
else
  mod=$(echo "${target%.py}" | tr '/' '.')
  PYTHONPATH=src:. python3 -m unittest "$mod" 2>&1 | tail -n 40
fi
exit "${PIPESTATUS[0]}"
