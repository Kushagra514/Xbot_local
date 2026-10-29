# xbot fleet harness

A small, closed-loop harness for experimenting with how much harness engineering helps a local model (Qwen via Ollama, or Cline) do real work. The work itself is building the draft-and-queue pipeline for your X account (Mode A: agents draft, you tap Post).

No pip installs: Python 3.10+, bash and Ollama are enough.

## What is in the folder
| Path | Role in the harness |
|---|---|
| `AGENTS.md`, `roles/*.md`, `.clinerules/` | **Instructions**: shared contract, one file per role (builder, critic, scribe) |
| `board/TASKS.md`, `board/specs/` | **Task board**: what to build, one spec per task |
| `tests/` + `scripts/verify.sh` | **Gate**: human-written acceptance tests, sealed by hash; also bans network/X-client imports |
| `src/xbot/` | **Environment**: the only place agents write (one output file per task) |
| `state/` | **State**: `lessons.md`, `runs.csv`, `tests.sha256` |
| `harness/loop.py` | **Closed loop**: build, gate, feedback, critic, scribe, metrics |
| `harness/report.py` | **Feedback for you**: compares levels |
| `experiments/PROTOCOL.md` | How to run a fair comparison |
| `instructions/` | Voice, rules, rubric (voice.md needs your real posts; agents must not invent it) |

## Quick start
```bash
ollama pull qwen2.5-coder:7b            # or any Qwen coder tag you have: `ollama list`
cd xbot-harness

# 1. Plumbing check, no model needed (reference solutions live OUTSIDE the repo)
python3 harness/loop.py --level 4 --all --fresh --mock ../xbot-selftest     # expect 4/4 passed
rm -f state/runs.csv src/xbot/{db,lint,dedupe,compose}.py && : > state/lessons.md

# 2. Real run with your local model
export OLLAMA_MODEL=qwen2.5-coder:7b NUM_CTX=6144
python3 harness/loop.py --level 3 --all --fresh
python3 harness/report.py
```
`NUM_CTX=6144` suits a 6 GB RTX 3050 with a 7B Q4 model; a 4B model leaves room for more. Ollama's default context is smaller than these prompts and silently truncates, which is why `loop.py` sets it per request.

## Harness levels
`--level N` is cumulative. L0 bare prompt, L1 + instructions/spec/tests, L2 + gate that reverts failures, L3 + gate output fed back (3 attempts), L4 + lessons, critic and scribe. Full table and procedure: `experiments/PROTOCOL.md`.

## Using Cline instead (interactive)
1. Open the folder in VS Code, set Cline's provider to Ollama and pick your model.
2. Cline's own system prompt is long. Raise Ollama's context for that model (for example a Modelfile with `PARAMETER num_ctx 16384`) or it will truncate. On 6 GB expect partial CPU offload and slow replies.
3. `.clinerules/harness.md` is picked up automatically. First message to send:
   > Follow .clinerules and AGENTS.md. Take the first unchecked task in board/TASKS.md, write only its output file, run `bash scripts/verify.sh <its test file>` until it exits 0 (max 3 attempts), then stop and tell me what failed on the way.
4. Cline gives you feel, not measurement. For comparable numbers use `harness/loop.py`; you are the loop in Cline.

## The fleet
Roles run sequentially (one GPU, so parallel agents would only slow each other down): planner (you, or a model editing `board/`), builder, gate (`verify.sh`, deterministic), critic, scribe. Use `OLLAMA_MODEL` for all roles; to give the critic a different model, edit the `MODEL` lookup in `chat()`.

## Rules that protect your account
No agent may post, reply, like, follow or DM. The gate rejects `requests`, `tweepy`, `selenium`, `playwright`, `httpx`, `xdk`, `urllib.request`, `socket` and `webbrowser` in `src/`; `xbot/compose.py` only builds an `x.com/intent/post?text=...` link for you to open. The X API has no free tier for new developers, and automated replies and engagement are what X's April 2026 enforcement targeted.

## Next steps
1. Fill `instructions/voice.md` from your real posts.
2. Run the protocol in `experiments/PROTOCOL.md` with your model.
3. If L0 already passes everything, add harder tasks. Natural next two: **draft/critic tools** (prompt builder, output cleaner, score parser with an injected `llm` callable) and the **closed-loop pipeline** (draft, lint, de-duplicate, critic, bounded revision, queue in SQLite). Add a line to `board/TASKS.md`, a spec, your own test, then `bash scripts/seal_tests.sh`.
4. Only then: Telegram approval, source search (arXiv/RSS), metrics.
