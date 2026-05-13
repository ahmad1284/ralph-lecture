# Plan Phase

Study @specs/* and @AGENTS.md with parallel subagents.

## Your job
Produce `codev/plans/ralph-lecturer.md` — a phased implementation plan with clear acceptance criteria per stage.

## Stages (implement in this order)

| Index | Name | File |
|---|---|---|
| 0 | utils | pipeline/utils.py |
| 1 | script-generation | pipeline/script.py |
| 2 | tts | pipeline/tts.py |
| 3 | subtitles | pipeline/subtitles.py |
| 4 | animation | pipeline/animation.py |
| 5 | composition | pipeline/composition.py |
| 6 | cli-entry-point | main.py |
| 7 | remotion-src | remotion-src/ |

## For each stage, document
- Files to create or modify
- Key functions and their signatures
- Inputs and outputs (file paths, data formats)
- Test command from AGENTS.md
- Acceptance criteria (what must be true for the stage to be "done")
- Dependencies on other stages

## Rules
- Plan only. Do NOT write implementation code.
- No time estimates.
- One plan file: `codev/plans/ralph-lecturer.md`

## When done
- Commit: `plan: implementation plan for ralph-lecturer`
- Update @codev/status.yaml: set `phase: implement`
- Output: `<signal>PLAN_COMPLETE</signal>`
