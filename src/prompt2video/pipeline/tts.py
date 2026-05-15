from __future__ import annotations

import asyncio
import json
import os
import random
import ssl
import subprocess
import tempfile

import edge_tts
import edge_tts.communicate as _et_comm

from .utils import ensure_dir

# Some sandbox environments use a self-signed MITM cert — disable verification so
# edge-tts can still attempt a connection before falling back to espeak-ng.
_no_verify_ctx = ssl.create_default_context()
_no_verify_ctx.check_hostname = False
_no_verify_ctx.verify_mode = ssl.CERT_NONE
_et_comm._SSL_CTX = _no_verify_ctx

VOICES = [
    "en-US-AriaNeural",
    "en-US-GuyNeural",
    "en-GB-SoniaNeural",
    "en-GB-RyanNeural",
    "en-AU-NatashaNeural",
    "en-AU-WilliamNeural",
    "en-CA-ClaraNeural",
    "en-IE-EmilyNeural",
    "en-NZ-MitchellNeural",
    "en-IN-NeerjaNeural",
]


def random_voice() -> str:
    return random.choice(VOICES)


async def _synthesise_edge(text: str, voice: str, mp3_path: str, words_path: str) -> None:
    communicate = edge_tts.Communicate(text, voice)
    words: list[dict] = []
    audio_chunks: list[bytes] = []

    async for event in communicate.stream():
        if event["type"] == "audio":
            audio_chunks.append(event["data"])
        elif event["type"] == "WordBoundary":
            words.append({
                "word": event["text"],
                "start_ms": event["offset"] // 10000,
                "end_ms": (event["offset"] + event["duration"]) // 10000,
            })

    with open(mp3_path, "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)
    with open(words_path, "w") as f:
        json.dump(words, f, indent=2)


def _synthesise_local(text: str, mp3_path: str, words_path: str) -> None:
    """Fallback: espeak-ng → wav → mp3 via pyttsx3; boundaries estimated from duration."""
    import pyttsx3

    engine = pyttsx3.init()
    for v in engine.getProperty("voices"):
        if "en-gb-x-rp" in v.id.lower() or "rp" in (v.name or "").lower():
            engine.setProperty("voice", v.id)
            break
    engine.setProperty("rate", 155)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name
    engine.save_to_file(text, wav_path)
    engine.runAndWait()

    subprocess.run(
        ["ffmpeg", "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-qscale:a", "4", mp3_path],
        check=True, capture_output=True,
    )
    os.unlink(wav_path)

    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", mp3_path],
        capture_output=True, text=True, check=True,
    )
    duration_ms = 0
    for s in json.loads(result.stdout).get("streams", []):
        if "duration" in s:
            duration_ms = int(float(s["duration"]) * 1000)
            break

    tokens = text.split()
    n = len(tokens)
    words = [
        {"word": w, "start_ms": int(duration_ms * i / n), "end_ms": int(duration_ms * (i + 1) / n)}
        for i, w in enumerate(tokens)
    ]
    with open(words_path, "w") as f:
        json.dump(words, f, indent=2)


def generate_audio(out_dir: str, voice: str) -> None:
    with open(os.path.join(out_dir, "script.json")) as f:
        script = json.load(f)

    audio_dir = ensure_dir(os.path.join(out_dir, "audio"))

    for section in script["sections"]:
        idx = section["index"]
        mp3_path = os.path.join(audio_dir, f"section_{idx:02d}.mp3")
        words_path = os.path.join(audio_dir, f"section_{idx:02d}_words.json")

        try:
            asyncio.run(_synthesise_edge(section["narration"], voice, mp3_path, words_path))
        except Exception:
            print(f"  edge-tts unavailable for section {idx}, falling back to espeak-ng")
            _synthesise_local(section["narration"], mp3_path, words_path)

        if not os.path.exists(mp3_path) or os.path.getsize(mp3_path) == 0:
            raise RuntimeError(f"TTS produced empty audio for section {idx}")
