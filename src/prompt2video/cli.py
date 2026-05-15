"""prompt2video CLI — Typer-based entry point."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .pipeline.utils import output_dir
from .pipeline.script import generate_script
from .pipeline.animation import render_scenes
from .pipeline.tts import generate_audio, random_voice, VOICES
from .pipeline.subtitles import generate_subtitles
from .pipeline.composition import compose

app = typer.Typer(
    name="prompt2video",
    help="Turn any topic into a narrated animated video lecture.",
    no_args_is_help=True,
    add_completion=True,
)
console = Console()


def _stage(name: str, fn, *args, **kwargs):
    console.print(f"  [bold blue]▶[/] {name}...")
    t0 = time.time()
    try:
        result = fn(*args, **kwargs)
        console.print(f"  [bold green]✓[/] {name} ({time.time() - t0:.1f}s)")
        return result
    except Exception as exc:
        console.print(f"  [bold red]✗[/] {name}: {exc}")
        raise typer.Exit(code=1) from exc


@app.command()
def main(
    topic: Optional[str] = typer.Argument(
        None,
        help="Topic to generate a lecture for. Requires ANTHROPIC_API_KEY.",
    ),
    from_script: Optional[Path] = typer.Option(
        None,
        "--from-script",
        metavar="DIR",
        help="Re-render an existing output directory. No API key needed.",
    ),
    voice: Optional[str] = typer.Option(
        None,
        "--voice",
        help="edge-tts voice name (e.g. en-GB-SoniaNeural). Default: random.",
    ),
    list_voices: bool = typer.Option(
        False,
        "--list-voices",
        help="Print available voices and exit.",
        is_eager=True,
    ),
) -> None:
    if list_voices:
        for v in VOICES:
            console.print(v)
        raise typer.Exit()

    if topic is None and from_script is None:
        console.print("[red]Error:[/] provide a topic or --from-script.")
        raise typer.Abort()

    chosen_voice = voice or random_voice()
    console.print(f"Voice: [cyan]{chosen_voice}[/]\n")

    if from_script is not None:
        src = Path(str(from_script).rstrip("/"))
        if not (src / "script.json").exists():
            console.print(f"[red]Error:[/] no script.json found in {src}")
            raise typer.Exit(code=1)
        import json, shutil
        topic_name = json.loads((src / "script.json").read_text()).get("topic", src.name)
        out = output_dir("output", topic_name)
        Path(out).mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / "script.json", Path(out) / "script.json")
        console.print(f"Output: [dim]{out}/[/]")
        console.print(f"[dim]Using script from {src}/[/]\n")
    else:
        out = output_dir("output", topic)
        console.print(f"Output: [dim]{out}/[/]\n")
        script_path = Path(out) / "script.json"
        if script_path.exists():
            console.print(f"[dim]Found existing script.json, skipping generation.[/]\n")
        else:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                console.print(
                    "[red]Error:[/] ANTHROPIC_API_KEY is not set.\n"
                    "Set it or supply an existing script with --from-script."
                )
                raise typer.Exit(code=1)
            _stage("script", generate_script, topic, out)

    _stage("animation", render_scenes, out)
    _stage("tts", generate_audio, out, chosen_voice)
    _stage("subtitles", generate_subtitles, out)
    _stage("composition", compose, out)

    console.print(f"\n[bold green]Done →[/] {out}/final.mp4")
