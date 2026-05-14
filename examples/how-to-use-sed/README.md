# Example: How to Use sed

A fully rendered lecture produced by the ralph-lecture pipeline. The `script.json`
is included so you can re-render the video locally without an API key.

## Re-render (no API key required)

```bash
python main.py --from-script examples/how-to-use-sed
# output: output/how-to-use-sed/final.mp4
```

Or with Docker:

```bash
docker build -t ralph-lecture .
docker run -v $(pwd)/output:/app/output \
  ralph-lecture --from-script examples/how-to-use-sed
```

## Video properties

| Property | Value |
|----------|---------|
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

## Pipeline notes

- Renderer: **Manim** (no Chrome download required)
- TTS: **espeak-ng** via pyttsx3 fallback (no outbound WebSocket required)
- Word boundaries: estimated uniformly from audio duration

## Regenerate from scratch (requires API key)

```bash
export ANTHROPIC_API_KEY=sk-...
python main.py "how to use sed"
```
