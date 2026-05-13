import json
import os

import anthropic

from .utils import ensure_dir

_CLI_KEYWORDS = {
    "grep", "sed", "awk", "find", "curl", "wget", "git", "docker",
    "ssh", "rsync", "tar", "chmod", "chown", "ps", "kill", "top",
    "htop", "netstat", "lsof", "strace", "bash", "zsh", "pipe",
    "regex", "cron", "systemd", "nginx", "vim", "tmux", "make",
    "jq", "xargs", "sort", "uniq", "cut", "tr", "wc",
}

_SYSTEM_PROMPT = """\
You are an MIT lecturer. Generate a narrated video lecture script as JSON.

Rules:
- Build intuition before formalism ("think of it like..." before the equation)
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
  "renderer": "remotion" | "manim",
  "total_sections": <int>,
  "sections": [
    {
      "index": <int>,
      "title": "<string>",
      "narration": "<spoken text>",
      "visual_type": "text" | "equation" | "graph" | "diagram" | "proof",
      "visual_content": {
        "latex": "<LaTeX string or empty>",
        "description": "<human-readable description>",
        "axes": {"x": "<label>", "y": "<label>"}
      },
      "estimated_duration_seconds": <int>
    }
  ]
}

Set renderer to "remotion" for CLI tools, shell commands, developer workflows,
and programming concepts best shown with code.
Set renderer to "manim" for mathematics, physics, formal CS, signal processing,
and anything requiring LaTeX equations as the primary visual.
"""


def _classify_renderer(topic: str) -> str:
    words = set(topic.lower().split())
    if words & _CLI_KEYWORDS:
        return "remotion"
    return "manim"


def _validate(data: dict) -> list[str]:
    errors = []
    for key in ("topic", "renderer", "total_sections", "sections"):
        if key not in data:
            errors.append(f"missing top-level key: {key}")
    if "sections" in data:
        for i, sec in enumerate(data["sections"]):
            for k in ("index", "title", "narration", "visual_type", "visual_content", "estimated_duration_seconds"):
                if k not in sec:
                    errors.append(f"section {i} missing key: {k}")
    if "renderer" in data and data["renderer"] not in ("remotion", "manim"):
        errors.append(f"invalid renderer: {data['renderer']}")
    return errors


def generate_script(topic: str, out_dir: str) -> dict:
    ensure_dir(out_dir)
    client = anthropic.Anthropic()

    def _call(extra: str = "") -> str:
        user_msg = f"Topic: {topic}"
        if extra:
            user_msg += f"\n\nPrevious attempt failed validation:\n{extra}\nFix the JSON and return only valid JSON."
        msg = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_msg}],
        )
        return msg.content[0].text.strip()

    raw = _call()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raw2 = _call(f"JSON parse error: {e}\nRaw output was:\n{raw}")
        if raw2.startswith("```"):
            raw2 = raw2.split("```")[1]
            if raw2.startswith("json"):
                raw2 = raw2[4:]
            raw2 = raw2.strip()
        data = json.loads(raw2)

    errors = _validate(data)
    if errors:
        error_str = "\n".join(errors)
        raw2 = _call(f"Validation errors:\n{error_str}")
        if raw2.startswith("```"):
            raw2 = raw2.split("```")[1]
            if raw2.startswith("json"):
                raw2 = raw2[4:]
            raw2 = raw2.strip()
        data = json.loads(raw2)
        errors = _validate(data)
        if errors:
            raise ValueError(f"Script validation failed after retry: {errors}")

    if data.get("renderer") not in ("remotion", "manim"):
        data["renderer"] = _classify_renderer(topic)

    out_path = os.path.join(out_dir, "script.json")
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)

    return data
