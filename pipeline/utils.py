import os
import re
import subprocess
import json


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
        [
            "ffprobe", "-v", "quiet",
            "-print_format", "json",
            "-show_streams", path,
        ],
        capture_output=True, text=True, check=True,
    )
    streams = json.loads(result.stdout).get("streams", [])
    for s in streams:
        if "duration" in s:
            return float(s["duration"])
    raise RuntimeError(f"ffprobe found no duration in {path}")
