# Spec: Script Generation

## Job to be Done
Given a topic, generate a structured MIT recitation-style lecture script that drives both the animation and the audio narration.

## MIT Recitation Style
- Builds intuition before formalism ("think of it like..." before the equation)
- Explains *why* before *how*
- Uses concrete examples anchored to the concept
- Precise language — no filler, no fluff
- Socratic moments: poses a question, then answers it
- Assumes the student is intelligent but new to this topic

## Output Format
Script is saved as `output/{slug}/script.json` with this structure:

```json
{
  "topic": "Fourier Transform",
  "total_sections": 5,
  "sections": [
    {
      "index": 0,
      "title": "The Core Idea",
      "narration": "Full spoken text for this section. Written naturally for speech — no markdown, no bullet points, complete sentences.",
      "visual_type": "text | equation | graph | diagram | proof",
      "visual_content": {
        "latex": "\\hat{f}(\\xi) = \\int_{-\\infty}^{\\infty} f(x)\\, e^{-2\\pi i x \\xi}\\, dx",
        "description": "Human-readable description of what should appear visually. Used when latex is not applicable.",
        "axes": { "x": "Time", "y": "Amplitude" }
      },
      "estimated_duration_seconds": 45
    }
  ]
}
```

## Section Count
- 4 to 7 sections per topic
- Each section covers one idea — no section tries to cover two things
- Total estimated duration: 4–8 minutes

## Visual Types
- `text`: Title card or key phrase displayed large
- `equation`: LaTeX rendered by Manim's MathTex
- `graph`: Function plotted on axes
- `diagram`: Geometric or conceptual diagram described in `description` field
- `proof`: Step-by-step equation derivation

## Implementation
- Uses Anthropic Claude API (claude-sonnet-4-20250514)
- System prompt enforces MIT recitation style and JSON-only output
- Validates output against expected schema before saving
- If validation fails, retries once with error context
- API key from environment: `ANTHROPIC_API_KEY`
