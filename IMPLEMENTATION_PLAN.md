# IMPLEMENTATION_PLAN.md

## Status
All stages implemented. Run acceptance test.

## Stages

- [x] **0. pipeline/utils.py** — slug, dir creation, ffprobe duration ✓
- [x] **1. pipeline/script.py** — Claude API (claude-sonnet-4-5), classifier, JSON validation, retry ✓
- [x] **2. pipeline/tts.py** — edge-tts async, word_boundary events, MP3+JSON per section ✓
- [x] **3. pipeline/subtitles.py** — cumulative offsets via mutagen, 8-word chunks, SRT output ✓
- [x] **4. pipeline/animation.py** — Manim code generator (text/equation/graph/proof/diagram) + Remotion dispatcher ✓
- [x] **5. pipeline/composition.py** — ffmpeg: merge scene+audio, concat, burn subtitles, cleanup ✓
- [x] **6. main.py** — argparse CLI, timing logs, stage orchestration ✓
- [x] **7. remotion-src/** — package.json, Root.tsx, TextCard/Terminal/Split/FlagExplainer/Diff, components, utils/timing.ts ✓

## Acceptance Test

```bash
export ANTHROPIC_API_KEY=sk-...
python main.py "how to use grep"
ffprobe -v quiet -print_format json -show_streams output/how-to-use-grep/final.mp4
# Expect: 2 streams — video (h264) + audio (aac)
```

## Known issues / blockers

- remotion-src/ needs `cd remotion-src && npm install` before first Remotion render
- Manim requires texlive-full for MathTex; text/diagram scenes work without it
- claude-sonnet-4-5 model ID used (spec said claude-sonnet-4-20250514 which is not a valid ID)
