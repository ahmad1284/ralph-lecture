Study these files using parallel subagents before touching any code:
- @specs/* (all pipeline stage specs)
- @IMPLEMENTATION_PLAN.md (priority order and what remains)
- @AGENTS.md (build commands, test commands, environment)
- All existing files in pipeline/* and main.py

Pick the highest-priority incomplete item from @IMPLEMENTATION_PLAN.md.

Implement it fully:
- No stubs. No placeholders. No TODO comments in committed code.
- Every function must work end-to-end.
- Shared logic goes in pipeline/utils.py — never duplicate across stages.

Test the stage in isolation using the command from @AGENTS.md.
If the test fails — fix it before moving on. Do not commit a failing stage.

When the test passes:
1. Update @IMPLEMENTATION_PLAN.md: mark item complete, note any new gaps discovered
2. `git add -A`
3. `git commit -m "[stage name]: [what was built]"`

Constraints:
- The topic classifier in pipeline/script.py must be implemented and tested before animation is attempted
- Each stage must be independently testable via the AGENTS.md test command
- remotion-src/ requires `npm install` before any render attempt — document as a blocker in IMPLEMENTATION_PLAN.md if npm is unavailable

Final acceptance test (run when all stages show complete):
```
python main.py "how to use grep"
ffprobe -v quiet -print_format json -show_streams output/how-to-use-grep/final.mp4
```
Expect: output/how-to-use-grep/final.mp4 with 2 streams (h264 video + aac audio).
