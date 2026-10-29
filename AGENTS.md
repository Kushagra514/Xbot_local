# AGENTS.md — shared contract for every agent in this repo

You are one agent in a small fleet building a **personal X (Twitter) posting assistant** for one account.
Work inside the harness: do not improvise outside it.

## Mission
Draft, lint, de-duplicate and queue daily AI/ML learning posts. A human taps Post. (Mode A.)

## Hard rules (the gate enforces the starred ones)
1. * Edit ONLY the output file named in your task. Never touch `tests/`, `scripts/`, `harness/`, `board/`, `state/`.
2. * Standard library only. No `requests`, `tweepy`, `selenium`, `playwright`, `httpx`, `xdk`.
   The bot must never post, like, follow or reply by itself.
3. * Tests in `tests/` are the acceptance criteria. They are read-only and written by the human.
4. Match the interface in the task spec exactly (names, argument order, return types, exceptions).
5. Small, boring, readable code. No extra features, no clever tricks, no unused code.
6. If the spec and the tests disagree, the tests win.
7. Do not invent facts about the user's posts or voice. Voice lives in `instructions/voice.md`.

## Reply format (builders)
Reply with the complete file, exactly:

    ### FILE: <path from the task>
    ```python
    <entire file>
    ```

Nothing else. No explanations, no partial diffs.

## Definition of done
`bash scripts/verify.sh <test file>` exits 0. Only the gate decides — not your opinion.

## Fleet roles
planner (human or model, edits board/) · builder (writes one file) · verifier (scripts/verify.sh, deterministic)
· critic (reviews a passing diff against rubric) · scribe (turns failures into short lessons).
