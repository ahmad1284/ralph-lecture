from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def output_dir(base: str, topic: str) -> str:
    return ensure_dir(os.path.join(base, slugify(topic)))


def ffprobe_duration(path: str) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", path],
        capture_output=True, text=True, check=True,
    )
    for stream in json.loads(result.stdout).get("streams", []):
        if "duration" in stream:
            return float(stream["duration"])
    raise RuntimeError(f"ffprobe found no duration in {path}")


def find_project_root() -> Path:
    """Walk up from this file to find the directory containing remotion-src."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "remotion-src").is_dir():
            return parent
    # Fallback for editable installs: go up to the repo root
    return here.parent.parent.parent.parent
