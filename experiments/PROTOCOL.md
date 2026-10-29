# Experiment protocol: how much does each harness layer buy a small local model?

**Question.** For the same model and the same tasks, how do pass rate, attempts and time change as you add harness layers L0 to L4?

## Conditions (cumulative)
| Level | Adds | What changes in `harness/loop.py` |
|---|---|---|
| L0 | nothing | Prompt is the task title only. One attempt. |
| L1 | instructions | `AGENTS.md` + `roles/builder.md` + task spec + read-only tests in the prompt. One attempt. |
| L2 | gate | `scripts/verify.sh` decides; a failing file is reverted so broken code never stays in `src/`. One attempt. |
| L3 | feedback | Gate output goes back to the builder; up to 3 attempts. |
| L4 | state + fleet | `state/lessons.md` injected; critic reviews code that already passes; scribe writes a lesson after a failed task. |

Ground truth (did `verify.sh` pass?) is logged at every level in `state/runs.csv`, so the levels are comparable.

## Procedure
Hold constant: model, `NUM_CTX`, temperature (0.2, set in `loop.py`), task list. Interleave levels inside each repetition so drift affects all levels equally.

```bash
export OLLAMA_MODEL=qwen2.5-coder:7b     # whatever `ollama list` shows
: > state/lessons.md                      # clean lessons before each repetition
for rep in 1 2 3; do
  for L in 0 1 2 3 4; do python3 harness/loop.py --level $L --all --fresh; done
  : > state/lessons.md
done
python3 harness/report.py $OLLAMA_MODEL
```
Second experiment (learning curve): at L4 only, do NOT clear `lessons.md` between repetitions and watch whether pass rate and attempts improve.

## What to read from the report
- `pass%`: final outcome. `1st-try%`: how reliable the model is without the loop. The gap between them is what the feedback loop buys.
- `att` and `sec`: the cost of the loop.
- `c-rej`: how often the critic blocks code that already passes. Check by hand whether those rejections were right (a critic from the same model grades itself and tends to approve or nitpick).

## Honest limits
- L1 and L2 have the same pass rate by construction (one attempt). L2's value is that nothing broken lands in `src/`.
- 4 tasks x 3 repetitions = 12 task-runs per level. Treat differences under about 2 task-runs as noise.
- T1 to T4 are easy for a 7B coder. If L0 already passes everything, add harder tasks (see README, "Next steps") before concluding that harness layers do not matter.
- Runs with `--mock` log `mock` in the model column. Filter with `report.py <model>`.
- Do not let agents see `xbot-selftest/` (the reference solutions); keep it outside the repo.

## Adding a task
1. Add a line to `board/TASKS.md` and write `board/specs/Tn.md`.
2. You write `tests/test_<name>.py` (unittest). Agents must never write tests.
3. `bash scripts/seal_tests.sh` to record the new hash.
