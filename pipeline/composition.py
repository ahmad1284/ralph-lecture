import json
import os
import subprocess
import tempfile

from .utils import ensure_dir, ffprobe_duration


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def _merge_scene_audio(scene_path: str, audio_path: str, clip_path: str) -> None:
    audio_dur = ffprobe_duration(audio_path)
    _run([
        "ffmpeg", "-y",
        "-i", scene_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-t", str(audio_dur),
        "-vf", f"tpad=stop_mode=clone:stop_duration={audio_dur}",
        "-shortest",
        clip_path,
    ])


def compose(out_dir: str) -> None:
    script_path = os.path.join(out_dir, "script.json")
    with open(script_path) as f:
        script = json.load(f)

    scenes_dir = os.path.join(out_dir, "scenes")
    audio_dir = os.path.join(out_dir, "audio")
    srt_path = os.path.join(out_dir, "subtitles.srt")
    combined_path = os.path.join(out_dir, "combined.mp4")
    final_path = os.path.join(out_dir, "final.mp4")

    clip_paths = []

    for section in script["sections"]:
        idx = section["index"]
        scene_path = os.path.join(scenes_dir, f"scene_{idx:02d}.mp4")
        audio_path = os.path.join(audio_dir, f"section_{idx:02d}.mp3")
        clip_path = os.path.join(scenes_dir, f"clip_{idx:02d}.mp4")

        _merge_scene_audio(scene_path, audio_path, clip_path)
        clip_paths.append(clip_path)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as concat_f:
        for cp in clip_paths:
            concat_f.write(f"file '{os.path.abspath(cp)}'\n")
        concat_list = concat_f.name

    _run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c", "copy",
        combined_path,
    ])
    os.unlink(concat_list)

    style = (
        "FontName=Arial,FontSize=22,"
        "PrimaryColour=&H00FFFFFF,"
        "OutlineColour=&H00000000,"
        "BackColour=&H80000000,"
        "Bold=1,Outline=2,Shadow=1,"
        "Alignment=2,MarginV=30"
    )
    _run([
        "ffmpeg", "-y",
        "-i", combined_path,
        "-vf", f"subtitles={srt_path}:force_style='{style}'",
        "-c:a", "copy",
        final_path,
    ])

    os.unlink(combined_path)
    for cp in clip_paths:
        if os.path.exists(cp):
            os.unlink(cp)
