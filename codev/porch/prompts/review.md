# Review Phase

Study the full implementation using parallel subagents:
- All files in pipeline/
- main.py
- remotion-src/
- @codev/plans/ralph-lecturer.md
- @specs/*

## Your job
Run the acceptance test. Document what was built, what deviated from spec, and what to improve next time.

## Steps

1. Run the acceptance test:
   ```bash
   python main.py "how to use grep"
   ffprobe -v quiet -print_format json -show_streams output/how-to-use-grep/final.mp4
   ```
   Expect: `output/how-to-use-grep/final.mp4` with 2 streams (h264 video + aac audio).

2. For each pipeline stage, compare the implementation against its spec. Note deviations.

3. Write `codev/reviews/ralph-lecturer.md`:
   - Acceptance test result
   - Spec deviations and the reason for each
   - What broke during implementation and how it was fixed
   - Lessons learned
   - What would be done differently

4. Update @AGENTS.md with any new learnings about Remotion, Manim, edge-tts, or ffmpeg. Keep it brief.

5. Update @codev/status.yaml: set `phase: review`, all stages → `done`.

6. Commit: `review: ralph-lecturer acceptance test and lessons learned`

## Output when done
`<signal>REVIEW_COMPLETE</signal>`
