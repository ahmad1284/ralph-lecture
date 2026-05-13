#!/usr/bin/env python3
import argparse
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
    parser.add_argument("topic", help="Topic to lecture on")
    parser.add_argument("--voice", default=None, help="edge-tts voice name")
    parser.add_argument("--random-voice", action="store_true", default=True,
                        help="Pick a random voice (default)")
    args = parser.parse_args()

    voice = args.voice if args.voice else random_voice()
    print(f"Voice: {voice}")

    slug = slugify(args.topic)
    out = output_dir("output", args.topic)
    print(f"Output: {out}")

    _stage("script", generate_script, args.topic, out)
    _stage("animation", render_scenes, out)
    _stage("tts", generate_audio, out, voice)
    _stage("subtitles", generate_subtitles, out)
    _stage("composition", compose, out)

    print(f"Done: {out}/final.mp4")


if __name__ == "__main__":
    main()
