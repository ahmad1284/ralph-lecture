from __future__ import annotations

import json
import os

import anthropic

from .utils import ensure_dir

_SYSTEM_PROMPT = """\
You are an MIT lecturer. Generate a narrated video lecture script as JSON.

Rules:
- Build intuition before formalism ("think of it like...") before technical detail
- Explain WHY before HOW
- Use concrete examples
- Precise language, no filler
- Socratic moments: pose a question, then answer it
- 4 to 7 sections, each covering exactly one idea
- Total estimated duration: 4–8 minutes
- All narration written naturally for speech — no markdown, no bullet points

You must output ONLY valid JSON matching this exact schema:
{
  "topic": "<topic string>",
  "total_sections": <int>,
  "sections": [
    {
      "index": <int>,
      "title": "<string>",
      "narration": "<spoken text>",
      "visual_type": "text" | "code" | "diagram",
      "visual_content": {
        "code": "<code string or empty>",
        "language": "<language or empty>",
        "description": "<human-readable description>"
      },
      "estimated_duration_seconds": <int>
    }
  ]
}
"""


def _validate(data: dict) -> list[str]:
    errors = []
    for key in ("topic", "total_sections", "sections"):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if "sections" in data:
        for i, sec in enumerate(data["sections"]):
            for k in ("index", "title", "narration", "visual_type", "visual_content", "estimated_duration_seconds"):
                if k not in sec:
                    errors.append(f"section {i} missing key: {k}")
    return errors


def _strip_fence(raw: str) -> str:
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip()


def generate_script(topic: str, out_dir: str) -> dict:
    ensure_dir(out_dir)
    client = anthropic.Anthropic()

    def _call(extra: str = "") -> str:
        user_msg = f"Topic: {topic}"
        if extra:
            user_msg += f"\n\nPrevious attempt failed:\n{extra}\nFix and return only valid JSON."
        msg = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        return msg.content[0].text.strip()

    raw = _strip_fence(_call())
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        data = json.loads(_strip_fence(_call(f"JSON parse error: {exc}\nRaw:\n{raw}")))

    errors = _validate(data)
    if errors:
        data = json.loads(_strip_fence(_call(f"Validation errors:\n" + "\n".join(errors))))
        errors = _validate(data)
        if errors:
            raise ValueError(f"Script validation failed after retry: {errors}")

    out_path = os.path.join(out_dir, "script.json")
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    return data
