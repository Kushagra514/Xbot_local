# Task board (planner edits this; loop.py reads it)
# Format: - [ ] ID | title | acceptance test | output file | spec file

- [ ] T1 | SQLite state layer | tests/test_db.py | src/xbot/db.py | board/specs/T1.md
- [x] T2 | Post linter (rules.md as code) | tests/test_lint.py | src/xbot/lint.py | board/specs/T2.md
- [x] T3 | Duplicate detector | tests/test_dedupe.py | src/xbot/dedupe.py | board/specs/T3.md
- [x] T4 | Compose-link publisher (Mode A) | tests/test_compose.py | src/xbot/compose.py | board/specs/T4.md

- [ ] T5 | Knowledge reader | tests/test_knowledge.py | bot/knowledge_reader.py | board/specs/T5.md
- [ ] T6 | Draft post via local Qwen | (model-gated, see bot/draft_post.py) | bot/draft_post.py | board/specs/T6.md
- [ ] T7 | Critic score vs rubric | (model-gated, see bot/critique_post.py) | bot/critique_post.py | board/specs/T7.md
- [ ] T8 | Closed-loop draft pipeline | (integration, see bot/pipeline.py) | bot/pipeline.py | board/specs/T8.md
