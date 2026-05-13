0a. Study specs/* with parallel subagents to understand all pipeline stage requirements — including both 03a (Remotion) and 03b (Manim) animation specs.
0b. Study @IMPLEMENTATION_PLAN.md to know current state and priorities.
0c. Study @AGENTS.md for build commands and environment details.

1. Your task is to implement pipeline functionality per the specs. Follow @IMPLEMENTATION_PLAN.md and choose the most important item. Before making changes, search the codebase first — do not assume something is not implemented. Use up to 20 parallel subagents for file reads and searches. Use only 1 subagent for running tests or the CLI.

2. After implementing a stage, test it using the single-stage test commands in @AGENTS.md. If it fails, fix it before moving on. Think hard.

3. When you discover a bug or gap, document it in @IMPLEMENTATION_PLAN.md immediately using a subagent, even if unrelated to current work.

4. When tests pass: update @IMPLEMENTATION_PLAN.md, then `git add -A`, then `git commit` with a message describing what was implemented. Then `git push`.

99999. DO NOT write placeholder or stub implementations. Every function must be fully working. No TODO comments in committed code.

999999. Each pipeline stage must be testable in isolation using the test commands in AGENTS.md. If a stage cannot be tested in isolation, restructure it until it can.

9999999. Keep @AGENTS.md updated with any new learnings about running Remotion, Manim, edge-tts, or ffmpeg. Use a subagent. Keep it brief.

99999999. Keep @IMPLEMENTATION_PLAN.md up to date after each completed item. Remove completed items periodically.

999999999. Single source of truth: no duplicate logic across pipeline stages. Shared utilities go in pipeline/utils.py.

9999999999. The final acceptance test is: `python main.py "how to use grep"` completes without error and produces a playable output/how-to-use-grep/final.mp4 with visible subtitles and audio.

99999999999. For Remotion scenes: the remotion-src/ directory must have a working package.json. Run `npm install` inside it before attempting to render. If npm is not available, document this blocker in IMPLEMENTATION_PLAN.md.

999999999999. The topic classifier must be implemented in pipeline/script.py and tested independently before animation rendering is attempted. Wrong renderer selection wastes a full loop.
