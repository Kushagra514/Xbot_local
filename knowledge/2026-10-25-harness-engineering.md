Pillar: Day N/100

# Harness engineering — everything outside the model weights

A harness doesn't make the model smarter; it establishes a closed-loop working system. Harness = instructions + tools + environment + state management + verification feedback.

Key concepts:
- Constraint agent behavior, maintain context, stop agents from declaring victory too early
- Verify work with full pipeline; make runtime observable and debuggable
- Capability gap = gulf between benchmark performance and real-task performance
- Harness-induced failure = model has capability, but the execution environment has structural defects
- Verification gap = gap between agent's confidence and actual correctness
- Diagnostic loop: execute → observe failure → attribute to harness layer → fix → re-execute

Definition of Done must be verifiable by command (tests pass, lint clean, type checks pass). Place AGENTS.md in the repo root — one AGENTS.md might be more effective than upgrading to a more expensive model.

Five defense layers: task specification, context provision, execution environment, verification feedback, state management.

When things fail, don't swap the model first — check the harness.