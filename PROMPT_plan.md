Study @specs/* and @AGENTS.md to understand all pipeline stage requirements.
Study existing source code in pipeline/* and main.py if present.

Use up to 20 parallel subagents to:
1. Read every spec in specs/
2. Compare each spec against any existing code
3. Identify gaps, contradictions, or missing detail in the specs themselves — fix them in place
4. Identify what is not yet implemented, stubbed, or incomplete in the code

Create or update @IMPLEMENTATION_PLAN.md as a prioritised bullet list.
Each item must include: stage name, file path, what is missing, and the test command from @AGENTS.md.

Order by dependency: utils before script, script before animation and tts, tts before subtitles, all of these before composition, composition before main.py.

Plan only. Do NOT write implementation code.
Do NOT assume something is missing — search first.

ULTIMATE GOAL: `python main.py "<topic>"` produces `output/{slug}/final.mp4` with animation, narration, and burned-in subtitles.
