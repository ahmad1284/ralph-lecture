0a. Study specs/* to learn all pipeline stage specifications.
0b. Study @AGENTS.md to understand the build environment, dependencies, and run commands.
0c. Study existing source code in pipeline/* and main.py if present.

1. Use up to 20 parallel subagents to study existing source code and compare against specs/*. Create or update @IMPLEMENTATION_PLAN.md as a prioritised bullet list of items not yet implemented. Think hard. Search for TODOs, stubs, missing modules, and incomplete implementations. Keep @IMPLEMENTATION_PLAN.md current with complete/incomplete status.

IMPORTANT: Plan only. Do NOT implement anything. Do NOT assume something is not implemented — search first.

ULTIMATE GOAL: A working CLI tool `python main.py "<topic>"` that produces `output/{slug}/final.mp4` with animation, narration, and burned-in subtitles. All six pipeline stages must be fully implemented with no placeholders.
