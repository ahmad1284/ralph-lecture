# Spec: Animation — Remotion (Tutorial / CLI Style)

## Job to be Done
Render tutorial-style video scenes using Remotion. Covers procedural topics: CLI tools (sed, grep, awk, git), programming concepts, developer workflows. Visual language is a modern dev screencast — clean, code-forward, step-by-step.

## When This Renderer Is Used
Topic classifier in `pipeline/script.py` sets `"renderer": "remotion"` when:
- Topic contains CLI tools (grep, sed, awk, find, curl, git, docker, etc.)
- Topic is a programming concept best shown with code (regex, pipes, loops)
- Topic is a developer workflow or tool tutorial
Otherwise defaults to `"renderer": "manim"`.

## Visual Style
- Background: `#0F1117` (near-black)
- Terminal window: `#1E1E2E` with `#313244` title bar
- Font: `JetBrains Mono` for code, `Inter` for prose
- Syntax highlight theme: Catppuccin Mocha
- Accent: `#CBA6F7` (purple) for highlights, `#A6E3A1` (green) for correct output
- Error colour: `#F38BA8` (red)
- Window chrome: macOS-style traffic lights (decorative only)

## Scene Layout Templates

### `terminal`
Full-width terminal window. Command appears character by character (typewriter effect). Output appears after 0.5s delay. Supports multi-command sequences — each command/output block appears in sequence.

```
┌──────────────────────────────────────┐
│  ● ● ●                               │
│  $ grep -r "pattern" ./src           │
│  src/main.py:42: match_pattern(...)  │
│  src/utils.py:18: find_pattern(...)  │
└──────────────────────────────────────┘
```

### `split`
Left panel: explanation text (narration key points as bullet lines, appearing one by one). Right panel: terminal or code block.

```
┌─────────────┬─────────────────────────┐
│ -r means    │  ● ● ●                  │
│ recursive   │  $ grep -r "TODO" .     │
│             │  main.py:10: # TODO     │
│ searches    │  utils.py:3: # TODO     │
│ all subdirs │                         │
└─────────────┴─────────────────────────┘
```

### `flag-explainer`
Breaks a command into annotated parts. Each flag lights up in sequence with an arrow and label below.

```
grep   -r   -n   --include="*.py"   "pattern"   ./src
 │      │    │         │               │            │
base  recurse line  filter         what to       where
               num   files          find
```

### `diff`
Side-by-side before/after. Left shows original, right shows result after command. Lines that changed are highlighted.

### `text`
Title card or section header. Large centred text, short subtitle below. Fades in.

## Remotion Implementation

### Structure
```
remotion-src/
  Root.tsx          — registers all compositions
  compositions/
    Terminal.tsx
    Split.tsx
    FlagExplainer.tsx
    Diff.tsx
    TextCard.tsx
  components/
    TerminalWindow.tsx
    CodeBlock.tsx       — syntax highlighted via shiki
    TypewriterText.tsx
    AnnotatedCommand.tsx
  utils/
    timing.ts
```

### Render Command
```bash
npx remotion render remotion-src/Root.tsx SceneComp \
  --props='{"sectionIndex": 0, "outputDir": "output/slug"}' \
  --output output/slug/scenes/scene_00.mp4 \
  --codec h264
```

`pipeline/animation.py` calls this for each section, passing section data as props JSON.

### Section Data as Props
Each scene receives the full section object from script.json as Remotion composition props.

### Duration
Remotion composition `durationInFrames` = `estimated_duration_seconds * 30` (30fps).

### Dependencies
```json
{
  "remotion": "^4.0.0",
  "@remotion/cli": "^4.0.0",
  "shiki": "^1.0.0"
}
```
Install via: `npm install` in `remotion-src/`

## Output
- Per section: `output/{slug}/scenes/scene_{index:02d}.mp4`
- 1920x1080, 30fps, H.264, no audio
