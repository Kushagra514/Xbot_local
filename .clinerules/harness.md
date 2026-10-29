# Harness rules (Cline)
Read `AGENTS.md` in the repo root before doing anything, then follow it.
Pick ONE unchecked task from `board/TASKS.md`, read its spec in `board/specs/`, write only its output file,
run `bash scripts/verify.sh <its test file>`, and iterate until it exits 0 (max 3 attempts).
Never edit `tests/`, `scripts/`, `harness/`, `board/`. If blocked after 3 attempts, append one line to
`state/lessons.md` saying what failed and stop.
