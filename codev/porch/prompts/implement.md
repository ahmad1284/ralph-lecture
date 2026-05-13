# Implement Phase

Read these files first, using parallel subagents:
- @specs/* (all pipeline stage specs)
- @codev/plans/ralph-lecturer.md (implementation plan and stage order)
- @codev/status.yaml (active stage index and status)
- @AGENTS.md (build commands and test commands)
- All existing files in pipeline/* and main.py

## Your job
Implement one stage per loop iteration. Pick the lowest-index stage with status `pending` or `in_progress`.

## Steps

1. Read @codev/status.yaml. Find the target stage.

2. Implement that stage fully per @specs/* and @codev/plans/ralph-lecturer.md.

3. Test in isolation using the test command for this stage in @AGENTS.md.
   If the test fails — fix it before doing anything else. Think hard.

4. When the test passes:
   - Update @codev/status.yaml: set this stage to `done`
   - `git add -A`
   - `git commit -m "implement: [stage name] — [what was built]"`
   - Output: `<signal>PHASE_IMPLEMENTED</signal>`

5. If all stages are `done`:
   - Update @codev/status.yaml: set `phase: review`
   - Output: `<signal>ALL_PHASES_COMPLETE</signal>`

## Hard rules
- No stubs. No placeholders. No TODO comments in committed code.
- Every function must work end-to-end.
- Shared logic goes in pipeline/utils.py — no duplication across stages.
- Each stage must be independently testable via the AGENTS.md test command.
- If a stage cannot be tested in isolation, restructure it until it can.
- Wrong renderer selection wastes a full loop — implement and test the topic classifier in pipeline/script.py before attempting animation.
