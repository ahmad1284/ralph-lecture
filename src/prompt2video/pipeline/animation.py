from __future__ import annotations

import json
import os
import subprocess

from .utils import ensure_dir, find_project_root


def _render_section(section: dict, out_dir: str) -> str:
    idx = section["index"]
    scenes_dir = ensure_dir(os.path.join(out_dir, "scenes"))
    out_path = os.path.join(scenes_dir, f"scene_{idx:02d}.mp4")
    remotion_src = str(find_project_root() / "remotion-src")
    duration_frames = section.get("estimated_duration_seconds", 30) * 30

    subprocess.run(
        [
            "npx", "remotion", "render",
            os.path.join(remotion_src, "Root.tsx"),
            "SceneComp",
            f"--props={json.dumps(section)}",
            f"--duration={duration_frames}",
            f"--output={out_path}",
            "--codec=h264",
            "--overwrite",
        ],
        cwd=remotion_src, check=True,
    )
    return out_path


def render_scenes(out_dir: str) -> None:
    with open(os.path.join(out_dir, "script.json")) as f:
        script = json.load(f)

    for section in script["sections"]:
        _render_section(section, out_dir)
