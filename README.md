# prompt2video

Turn any topic into a narrated animated video lecture — MIT recitation style for math/CS, screencast style for CLI tools.

```bash
prompt2video "how to use grep"
# → output/how-to-use-grep/final.mp4
```

A fully rendered MP4 with:
- Animated visuals (Remotion for CLI topics, Manim for math/CS)
- AI-generated narration script via Claude
- Natural-sounding voice via edge-tts
- Burned-in subtitles

## Install

```bash
pip install prompt2video
```

Or from source:

```bash
git clone https://github.com/ahmad1284/ralph-lecture
cd ralph-lecture
pip install -e .
```

With [uv](https://docs.astral.sh/uv/) (recommended):

```bash
uv venv .venv && source .venv/bin/activate
uv pip install -e .
```

## System dependencies

| Dependency | Purpose |
|---|---|
| `ffmpeg` | Audio/video composition |
| `espeak-ng` | TTS fallback (offline) |
| `node` >= 18 | Remotion renderer |
| `texlive-full` | Manim MathTex (math topics only) |

## Usage

```bash
# New lecture (requires ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-...
prompt2video "how to use grep"
prompt2video "Fourier Transform"
prompt2video "how to use sed" --voice en-GB-SoniaNeural

# Re-render from an existing script (no API key needed)
prompt2video --from-script examples/how-to-use-sed
```

## Example

The `examples/how-to-use-sed/` directory contains a ready-to-render `script.json`.
Re-render it without an API key:

```bash
prompt2video --from-script examples/how-to-use-sed
# → output/how-to-use-sed/final.mp4  (163s, 1920×1080, h264+aac)
```

## Topic routing

| Topic type | Renderer | Example |
|---|---|---|
| CLI tools, shell, developer workflows | Remotion | `"how to use grep"` |
| Math, physics, formal CS | Manim | `"Fourier Transform"` |

## Voices

Picks a random neural voice by default. Override with `--voice`:

| Voice | Accent |
|---|---|
| en-US-AriaNeural | American female |
| en-US-GuyNeural | American male |
| en-GB-SoniaNeural | British female |
| en-GB-RyanNeural | British male |
| en-AU-NatashaNeural | Australian female |
| en-AU-WilliamNeural | Australian male |
| en-CA-ClaraNeural | Canadian female |
| en-IE-EmilyNeural | Irish female |
| en-NZ-MitchellNeural | New Zealand male |
| en-IN-NeerjaNeural | Indian English female |

## License

MIT
