# Example: How to Use sed

A fully rendered lecture video produced by the ralph-lecture pipeline.

## Output

| Property | Value |
|----------|-------|
| File | `final.mp4` |
| Duration | 163.6 seconds |
| Resolution | 1920×1080 |
| Video | h264 |
| Audio | aac |
| Size | ~4 MB |

## Sections

| # | Title | Visual | Duration |
|---|-------|--------|----------|
| 0 | What is sed? | text | 40s |
| 1 | Basic substitution: s/old/new/ | terminal card | 45s |
| 2 | Global flag: s/old/new/g | terminal card | 40s |
| 3 | Edit in place with -i | terminal card | 45s |
| 4 | Delete lines with d | terminal card | 40s |
| 5 | Multiple commands with -e | terminal card | 45s |

## How to regenerate

```bash
export ANTHROPIC_API_KEY=sk-...
python main.py "how to use sed"
# output/how-to-use-sed/final.mp4
```

## Pipeline notes

- Renderer: **Manim** (Remotion requires Chrome Headless Shell download, blocked in sandboxed environments)
- TTS: **espeak-ng** via pyttsx3 fallback (edge-tts requires outbound WebSocket to Microsoft; blocked in sandboxed environments)
- Word boundaries: estimated uniformly from audio duration
