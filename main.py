#!/usr/bin/env python3
import argparse
import os
import sys
import time

from pipeline.utils import slugify, ensure_dir, output_dir
from pipeline.script import generate_script
from pipeline.animation import render_scenes
from pipeline.tts import generate_audio, random_voice, VOICES
from pipeline.subtitles import generate_subtitles
from pipeline.composition import compose


def _stage(name: str, fn, *args, **kwargs):
    print(f"[{name}] starting...")
    t0 = time.time()
    try:
        result = fn(*args, **kwargs)
        print(f"[{name}] done ({time.time() - t0:.1f}s)")
        return result
    except Exception as e:
        print(f"[{name}] FAILED: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate a narrated video lecture for any topic")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("topic", nargs="?", help="Topic to generate a script for (requires ANTHROPIC_API_KEY)")
    group.add_argument("--from-script", metavar="DIR",
                       help="Skip script generation and render an existing output dir containing script.json")
    parser.add_argument("--voice", default=None, help="edge-tts voice name")
    parser.add_argument("--random-voice", action="store_true", default=True,
                        help="Pick a random voice (default)")
    args = parser.parse_args()

    voice = args.voice if args.voice else random_voice()
    print(f"Voice: {voice}")

    if args.from_script:
        out = args.from_script.rstrip("/")
        script_path = os.path.join(out, "script.json")
        if not os.path.exists(script_path):
            print(f"ERROR: no script.json found in {out}", file=sys.stderr)
            sys.exit(1)
        print(f"[script] using existing {script_path}")
    else:
        out = output_dir("output", args.topic)
        print(f"Output: {out}")
        script_path = os.path.join(out, "script.json")
        if os.path.exists(script_path):
            print(f"[script] found existing {script_path}, skipping generation")
        else:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                print("ERROR: ANTHROPIC_API_KEY not set. "
                      "Either set the key or supply an existing script with --from-script.", file=sys.stderr)
                sys.exit(1)
            _stage("script", generate_script, args.topic, out)

    _stage("animation", render_scenes, out)
    _stage("tts", generate_audio, out, voice)
    _stage("subtitles", generate_subtitles, out)
    _stage("composition", compose, out)

    print(f"Done: {out}/final.mp4")


if __name__ == "__main__":
    main()
