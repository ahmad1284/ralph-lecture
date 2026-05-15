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

## Docker

The Docker image bundles everything — Python, ffmpeg, espeak-ng, Node, LaTeX, and all Python dependencies. No local setup needed.

**Build:**

```bash
docker build -t prompt2video .
```

**Run — generate a new lecture** (requires API key):

```bash
docker run --rm \
  -e ANTHROPIC_API_KEY=sk-... \
  -v "$(pwd)/output:/app/output" \
  prompt2video "how to use grep"
# → output/how-to-use-grep/final.mp4
```

**Run — re-render the bundled example** (no API key):

```bash
docker run --rm \
  -v "$(pwd)/output:/app/output" \
  prompt2video --from-script examples/how-to-use-sed
# → output/how-to-use-sed/final.mp4
```

**Use a specific voice:**

```bash
docker run --rm \
  -e ANTHROPIC_API_KEY=sk-... \
  -v "$(pwd)/output:/app/output" \
  prompt2video --voice en-GB-SoniaNeural "Fourier Transform"
```

The `-v $(pwd)/output:/app/output` flag mounts a local `output/` folder so the final MP4 lands on your machine.

## Install

```bash
git clone https://github.com/ahmad1284/ralph-lecture
cd ralph-lecture
./install.sh
```

`install.sh` handles everything in one shot:
1. Installs system dependencies (ffmpeg, espeak-ng, Node, LaTeX) via apt / dnf / pacman
2. Installs [uv](https://docs.astral.sh/uv/) if not already present
3. Runs `uv tool install .` — drops `prompt2video` on your PATH in an isolated env

After that it's just `prompt2video "your topic"`. No venv to activate.

### Manual steps (if you prefer)

**System deps (Debian/Ubuntu):**

```bash
sudo apt-get install -y ffmpeg espeak-ng libcairo2-dev libpango1.0-dev \
    nodejs npm texlive-latex-base texlive-fonts-recommended texlive-latex-extra dvisvgm
```

**Python CLI:**

```bash
uv tool install .        # isolated env, binary on PATH
# or
pipx install .           # same idea, pipx flavour
```

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
