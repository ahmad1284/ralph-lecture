from __future__ import annotations

import json
import os
import subprocess
import textwrap

from .utils import ensure_dir, find_project_root

_COLORS = {
    "BG": "#1C1C2E",
    "TEXT": "#FFFFFF",
    "EQ": "#58C4DD",
    "EMPHASIS": "#FFDD57",
    "RESULT": "#83C167",
    "SHAPE": "#FF6B6B",
}

_HEADER = """\
from manim import *
config.background_color = "{BG}"
config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 30
""".format(**_COLORS)


def _manim_text(title: str, duration: int) -> str:
    safe = title.replace('"', '\\"')
    return _HEADER + textwrap.dedent(f'''

        class SceneClass(Scene):
            def construct(self):
                text = Text("{safe}", color="{_COLORS["TEXT"]}", font_size=72)
                self.play(FadeIn(text), run_time=1.5)
                self.wait({max(duration - 2, 1)})
                self.play(FadeOut(text), run_time=0.5)
        ''')


def _manim_equation(latex: str, duration: int) -> str:
    safe = latex.replace("\\", "\\\\").replace('"', '\\"')
    return _HEADER + textwrap.dedent(f'''

        class SceneClass(Scene):
            def construct(self):
                eq = MathTex(r"{safe}", color="{_COLORS["EQ"]}", font_size=72)
                self.play(Write(eq), run_time=min(3, {duration} * 0.3))
                self.play(Indicate(eq, color="{_COLORS["EMPHASIS"]}"), run_time=1)
                self.wait({max(duration - 5, 1)})
                self.play(FadeOut(eq), run_time=0.5)
        ''')


def _manim_graph(axes: dict, latex: str, duration: int) -> str:
    x_label = axes.get("x", "x").replace('"', '\\"')
    y_label = axes.get("y", "y").replace('"', '\\"')
    return _HEADER + textwrap.dedent(f'''

        class SceneClass(Scene):
            def construct(self):
                ax = Axes(
                    x_range=[-4, 4, 1], y_range=[-2, 2, 1],
                    axis_config={{"color": "{_COLORS["TEXT"]}"}},
                )
                x_lab = ax.get_x_axis_label("{x_label}", color="{_COLORS["TEXT"]}")
                y_lab = ax.get_y_axis_label("{y_label}", color="{_COLORS["TEXT"]}")
                graph = ax.plot(lambda x: x, color="{_COLORS["EQ"]}")
                self.play(Create(ax), Write(x_lab), Write(y_lab), run_time=2)
                self.play(Create(graph), run_time=min(3, {duration} * 0.4))
                self.wait({max(duration - 6, 1)})
                self.play(FadeOut(ax), FadeOut(graph), FadeOut(x_lab), FadeOut(y_lab), run_time=0.5)
        ''')


def _manim_proof(latex: str, desc: str, duration: int) -> str:
    lines = [l.strip() for l in latex.split("\\\\") if l.strip()] if latex else [desc[:80]]
    step_time = max(1.0, (duration - 2) / max(len(lines), 1))
    steps = []
    for i, line in enumerate(lines[:6]):
        safe_line = line.replace("\\", "\\\\").replace('"', '\\"')
        color = _COLORS["RESULT"] if i == len(lines) - 1 else _COLORS["EQ"]
        steps.append(
            f'                step_{i} = MathTex(r"{safe_line}", color="{color}", font_size=54)'
            f'.shift(DOWN * {i * 1.1 - len(lines) * 0.5})'
        )
    plays = "\n".join(
        f'                self.play(FadeIn(step_{i}, shift=UP * 0.3), run_time={step_time:.1f})'
        for i in range(len(lines[:6]))
    )
    step_vars = ", ".join(f"step_{i}" for i in range(len(lines[:6])))
    wait = max(duration - int(step_time * len(lines[:6])) - 1, 1)

    return _HEADER + textwrap.dedent(f'''

        class SceneClass(Scene):
            def construct(self):
{chr(10).join(steps)}
{plays}
                self.wait({wait})
                self.play(FadeOut(VGroup({step_vars})), run_time=0.5)
        ''')


def _manim_diagram(desc: str, title: str, duration: int) -> str:
    safe_title = title.replace('"', '\\"').replace("'", "\\'")
    if desc.strip().startswith("$"):
        safe_cmd = desc.strip().replace("\\", "\\\\").replace('"', '\\"').replace("'", "\\'")
        return _HEADER + textwrap.dedent(f'''

            class SceneClass(Scene):
                def construct(self):
                    title = Text("{safe_title}", color="{_COLORS["EMPHASIS"]}", font_size=52, weight=BOLD)
                    title.to_edge(UP, buff=0.6)
                    box = RoundedRectangle(
                        corner_radius=0.15, width=14, height=2.2,
                        fill_color="#1E1E2E", fill_opacity=1,
                        stroke_color="{_COLORS["EQ"]}", stroke_width=2,
                    ).shift(DOWN * 0.2)
                    prompt = Text("$ ", color="{_COLORS["EQ"]}", font_size=40, font="Monospace")
                    cmd_text = Text("{safe_cmd[2:]}", color="{_COLORS["TEXT"]}", font_size=40, font="Monospace")
                    cmd_line = VGroup(prompt, cmd_text).arrange(RIGHT, buff=0.05).move_to(box)
                    self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
                    self.play(FadeIn(box), run_time=0.5)
                    self.play(Write(prompt), run_time=0.4)
                    self.play(AddTextLetterByLetter(cmd_text, time_per_char=0.06), run_time=min(3, {duration} * 0.3))
                    self.wait({max(duration - 6, 2)})
                    self.play(FadeOut(VGroup(title, box, cmd_line)), run_time=0.5)
            ''')

    safe_desc = desc[:120].replace('"', '\\"').replace("'", "\\'")
    return _HEADER + textwrap.dedent(f'''

        class SceneClass(Scene):
            def construct(self):
                title = Text("{safe_title}", color="{_COLORS["TEXT"]}", font_size=56).to_edge(UP)
                desc = Text("{safe_desc}", color="{_COLORS["EQ"]}", font_size=36).next_to(title, DOWN, buff=0.5)
                circle = Circle(radius=1.5, color="{_COLORS["SHAPE"]}").shift(DOWN * 0.5)
                arrow = Arrow(LEFT * 3, RIGHT * 3, color="{_COLORS["EMPHASIS"]}").shift(DOWN * 0.5)
                self.play(Write(title), run_time=1)
                self.play(Write(desc), run_time=1.5)
                self.play(Create(circle), GrowArrow(arrow), run_time=2)
                self.wait({max(duration - 6, 1)})
                self.play(FadeOut(VGroup(title, desc, circle, arrow)), run_time=0.5)
        ''')


def _manim_code_for_section(section: dict) -> str:
    vtype = section.get("visual_type", "text")
    vc = section.get("visual_content", {})
    duration = section.get("estimated_duration_seconds", 30)
    title = section.get("title", "")
    dispatch = {
        "text": lambda: _manim_text(title, duration),
        "equation": lambda: _manim_equation(vc.get("latex", title), duration),
        "graph": lambda: _manim_graph(vc.get("axes", {"x": "x", "y": "y"}), vc.get("latex", ""), duration),
        "proof": lambda: _manim_proof(vc.get("latex", ""), vc.get("description", title), duration),
    }
    return dispatch.get(vtype, lambda: _manim_diagram(vc.get("description", title), title, duration))()


def _render_remotion_section(section: dict, out_dir: str) -> str:
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


def _render_manim_section(section: dict, out_dir: str) -> str:
    idx = section["index"]
    tmp_dir = ensure_dir(os.path.join(out_dir, "tmp"))
    scenes_dir = ensure_dir(os.path.join(out_dir, "scenes"))

    py_path = os.path.join(tmp_dir, f"scene_{idx:02d}.py")
    out_file = f"scene_{idx:02d}"

    with open(py_path, "w") as f:
        f.write(_manim_code_for_section(section))

    subprocess.run(
        ["manim", "-qh", "--output_file", out_file, "--media_dir", tmp_dir, py_path, "SceneClass"],
        check=True,
    )

    dest = os.path.join(scenes_dir, f"scene_{idx:02d}.mp4")
    candidate = os.path.join(tmp_dir, "videos", f"scene_{idx:02d}", "1080p30", f"{out_file}.mp4")
    if os.path.exists(candidate):
        os.rename(candidate, dest)
    else:
        for root, _, files in os.walk(tmp_dir):
            for fname in files:
                if fname.endswith(".mp4"):
                    os.rename(os.path.join(root, fname), dest)
                    break

    if not os.path.exists(dest):
        raise RuntimeError(f"Manim did not produce output for section {idx}")
    return dest


def render_scenes(out_dir: str) -> None:
    with open(os.path.join(out_dir, "script.json")) as f:
        script = json.load(f)

    renderer = script.get("renderer", "manim")
    for section in script["sections"]:
        if renderer == "remotion":
            _render_remotion_section(section, out_dir)
        else:
            _render_manim_section(section, out_dir)
