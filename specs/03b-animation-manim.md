# Spec: Animation — Manim (Academic / Mathematical Style)

## Job to be Done
Render academic-style video scenes using Manim. Covers mathematical topics, physics, algorithms, formal computer science. Visual language is precise, equation-driven, geometric — in the tradition of 3Blue1Brown.

## When This Renderer Is Used
Topic classifier in `pipeline/script.py` sets `"renderer": "manim"` when:
- Topic is mathematical (calculus, linear algebra, probability, number theory)
- Topic requires LaTeX equations as primary visual
- Topic is formal CS (complexity, automata, graph theory, algorithms with proofs)
- Topic is physics or signal processing
Otherwise uses `"renderer": "remotion"`.

## Visual Style
- Background: `#1C1C2E` (dark navy)
- Primary text: `#FFFFFF`
- Equation colour: `#58C4DD` (blue)
- Emphasis: `#FFDD57` (yellow)
- Result/conclusion: `#83C167` (green)
- Geometric objects: `#FF6B6B` (coral) for shapes, `#58C4DD` for vectors
- Font: Manim default (Cairo) for labels, LaTeX for all math

## Scene Types

### `text`
Section title centred on screen. FadeIn, holds for full duration. Used for transitions between major ideas.

### `equation`
- Render using `MathTex`
- `Write` animation left to right
- If multiple expressions build on each other: `TransformMatchingTex` to morph between steps
- Highlight key subexpressions using `SurroundingRectangle` or `Indicate`

### `graph`
- `Axes` with labelled x/y from `visual_content.axes`
- Plot function with `Create(graph)` animation
- Add `TracedPath` if showing dynamic change
- Label key points (maxima, zeros) with `Dot` + `MathTex`

### `proof`
- Sequential equation steps using `MathTex`
- Each new line: `FadeIn` from below, previous lines shift up
- Final result line: colour change to green (`#83C167`) with `ApplyMethod`
- Justify each step with a small label in grey on the right

### `diagram`
- Construct from Manim primitives: `Circle`, `Arrow`, `Line`, `Rectangle`, `Polygon`, `VGroup`
- Follow the description in `visual_content.description` literally
- Animate components appearing in the logical order of the explanation
- Use `Create` for shapes, `GrowArrow` for arrows, `Write` for labels

### `number_line`
- `NumberLine` with marked points
- Animate points appearing, intervals highlighted with `Line` overlay

## Timing
- Scene duration = `estimated_duration_seconds` from script
- Animations consume at most `duration - 1` seconds
- `self.wait()` pads to exact duration
- All `run_time` values calculated proportionally to section duration

## Implementation
- `pipeline/animation.py` generates a Python file per section containing one Manim `Scene` subclass
- Runs: `manim -qh --output_file scene_{index:02d} generated_scene_{index:02d}.py SceneClass`
- Output redirected to `output/{slug}/scenes/`
- Temporary generated Python files written to `output/{slug}/tmp/`
- Requires: `manim` (pip), `latex` (system — texlive-full recommended)

## Output
- Per section: `output/{slug}/scenes/scene_{index:02d}.mp4`
- 1920x1080, 30fps, H.264, no audio
