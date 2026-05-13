import json
import os
import subprocess
import textwrap

from .utils import ensure_dir


_MANIM_COLORS = {
    "BG": "#1C1C2E",
    "TEXT": "#FFFFFF",
    "EQ": "#58C4DD",
    "EMPHASIS": "#FFDD57",
    "RESULT": "#83C167",
    "SHAPE": "#FF6B6B",
}


def _manim_code_for_section(section: dict) -> str:
    vtype = section.get("visual_type", "text")
    vc = section.get("visual_content", {})
    duration = section.get("estimated_duration_seconds", 30)
    title = section.get("title", "")

    if vtype == "text":
        return _manim_text(title, duration)
    elif vtype == "equation":
        latex = vc.get("latex", title)
        return _manim_equation(latex, duration)
    elif vtype == "graph":
        axes = vc.get("axes", {"x": "x", "y": "y"})
        latex = vc.get("latex", "")
        return _manim_graph(axes, latex, duration)
    elif vtype == "proof":
        latex = vc.get("latex", "")
        desc = vc.get("description", title)
        return _manim_proof(latex, desc, duration)
    else:
        desc = vc.get("description", title)
        return _manim_diagram(desc, title, duration)


def _manim_text(title: str, duration: int) -> str:
    safe = title.replace('"', '\\"')
    return textwrap.dedent(f'''\
        from manim import *
        config.background_color = "{_MANIM_COLORS["BG"]}"
        config.pixel_height = 1080
        config.pixel_width = 1920
        config.frame_rate = 30

        class SceneClass(Scene):
            def construct(self):
                text = Text("{safe}", color="{_MANIM_COLORS["TEXT"]}", font_size=72)
                self.play(FadeIn(text), run_time=1.5)
                self.wait({max(duration - 2, 1)})
                self.play(FadeOut(text), run_time=0.5)
        ''')


def _manim_equation(latex: str, duration: int) -> str:
    safe = latex.replace("\\", "\\\\").replace('"', '\\"')
    return textwrap.dedent(f'''\
        from manim import *
        config.background_color = "{_MANIM_COLORS["BG"]}"
        config.pixel_height = 1080
        config.pixel_width = 1920
        config.frame_rate = 30

        class SceneClass(Scene):
            def construct(self):
                eq = MathTex(r"{safe}", color="{_MANIM_COLORS["EQ"]}", font_size=72)
                self.play(Write(eq), run_time=min(3, {duration} * 0.3))
                self.play(Indicate(eq, color="{_MANIM_COLORS["EMPHASIS"]}"), run_time=1)
                self.wait({max(duration - 5, 1)})
                self.play(FadeOut(eq), run_time=0.5)
        ''')


def _manim_graph(axes: dict, latex: str, duration: int) -> str:
    x_label = axes.get("x", "x").replace('"', '\\"')
    y_label = axes.get("y", "y").replace('"', '\\"')
    return textwrap.dedent(f'''\
        from manim import *
        config.background_color = "{_MANIM_COLORS["BG"]}"
        config.pixel_height = 1080
        config.pixel_width = 1920
        config.frame_rate = 30

        class SceneClass(Scene):
            def construct(self):
                ax = Axes(
                    x_range=[-4, 4, 1],
                    y_range=[-2, 2, 1],
                    axis_config={{"color": "{_MANIM_COLORS["TEXT"]}"}},
                )
                x_lab = ax.get_x_axis_label("{x_label}", color="{_MANIM_COLORS["TEXT"]}")
                y_lab = ax.get_y_axis_label("{y_label}", color="{_MANIM_COLORS["TEXT"]}")
                graph = ax.plot(lambda x: x, color="{_MANIM_COLORS["EQ"]}")
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
        color = _MANIM_COLORS["RESULT"] if i == len(lines) - 1 else _MANIM_COLORS["EQ"]
        steps.append(f'                step_{i} = MathTex(r"{safe_line}", color="{color}", font_size=54).shift(DOWN * {i * 1.1 - len(lines) * 0.5})')

    plays = "\n".join(
        f'                self.play(FadeIn(step_{i}, shift=UP * 0.3), run_time={step_time:.1f})'
        for i in range(len(lines[:6]))
    )
    step_vars = ", ".join(f"step_{i}" for i in range(len(lines[:6])))

    return textwrap.dedent(f'''\
        from manim import *
        config.background_color = "{_MANIM_COLORS["BG"]}"
        config.pixel_height = 1080
        config.pixel_width = 1920
        config.frame_rate = 30

        class SceneClass(Scene):
            def construct(self):
{chr(10).join(steps)}
{plays}
                self.wait({max(duration - int(step_time * len(lines[:6])) - 1, 1)})
                self.play(FadeOut(VGroup({step_vars})), run_time=0.5)
        ''')


def _manim_diagram(desc: str, title: str, duration: int) -> str:
    safe_title = title.replace('"', '\\"')
    safe_desc = desc[:120].replace('"', '\\"')
    return textwrap.dedent(f'''\
        from manim import *
        config.background_color = "{_MANIM_COLORS["BG"]}"
        config.pixel_height = 1080
        config.pixel_width = 1920
        config.frame_rate = 30

        class SceneClass(Scene):
            def construct(self):
                title = Text("{safe_title}", color="{_MANIM_COLORS["TEXT"]}", font_size=56).to_edge(UP)
                desc = Text("{safe_desc}", color="{_MANIM_COLORS["EQ"]}", font_size=36).next_to(title, DOWN, buff=0.5)
                circle = Circle(radius=1.5, color="{_MANIM_COLORS["SHAPE"]}").shift(DOWN * 0.5)
                arrow = Arrow(LEFT * 3, RIGHT * 3, color="{_MANIM_COLORS["EMPHASIS"]}").shift(DOWN * 0.5)
                self.play(Write(title), run_time=1)
                self.play(Write(desc), run_time=1.5)
                self.play(Create(circle), GrowArrow(arrow), run_time=2)
                self.wait({max(duration - 6, 1)})
                self.play(FadeOut(VGroup(title, desc, circle, arrow)), run_time=0.5)
        ''')


def _render_remotion_section(section: dict, out_dir: str, remotion_src: str) -> str:
    idx = section["index"]
    scenes_dir = ensure_dir(os.path.join(out_dir, "scenes"))
    out_path = os.path.join(scenes_dir, f"scene_{idx:02d}.mp4")
    props = json.dumps(section)
    duration_frames = section.get("estimated_duration_seconds", 30) * 30

    cmd = [
        "npx", "remotion", "render",
        os.path.join(remotion_src, "Root.tsx"),
        "SceneComp",
        f"--props={props}",
        f"--duration={duration_frames}",
        f"--output={out_path}",
        "--codec=h264",
        "--overwrite",
    ]
    subprocess.run(cmd, cwd=remotion_src, check=True)
    return out_path


def _render_manim_section(section: dict, out_dir: str) -> str:
    idx = section["index"]
    tmp_dir = ensure_dir(os.path.join(out_dir, "tmp"))
    scenes_dir = ensure_dir(os.path.join(out_dir, "scenes"))

    py_path = os.path.join(tmp_dir, f"scene_{idx:02d}.py")
    out_file = f"scene_{idx:02d}"

    code = _manim_code_for_section(section)
    with open(py_path, "w") as f:
        f.write(code)

    cmd = [
        "manim", "-qh",
        "--output_file", out_file,
        "--media_dir", tmp_dir,
        py_path, "SceneClass",
    ]
    subprocess.run(cmd, check=True)

    stem = f"scene_{idx:02d}"
    candidate = os.path.join(tmp_dir, "videos", stem, "1080p30", f"{out_file}.mp4")
    dest = os.path.join(scenes_dir, f"scene_{idx:02d}.mp4")
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
    script_path = os.path.join(out_dir, "script.json")
    with open(script_path) as f:
        script = json.load(f)

    renderer = script.get("renderer", "manim")
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    remotion_src = os.path.join(repo_root, "remotion-src")

    for section in script["sections"]:
        if renderer == "remotion":
            _render_remotion_section(section, out_dir, remotion_src)
        else:
            _render_manim_section(section, out_dir)
