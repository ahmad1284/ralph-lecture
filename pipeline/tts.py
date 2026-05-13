import asyncio
import json
import os
import ssl
import subprocess
import tempfile

import edge_tts
import edge_tts.communicate as _et_comm

# Sandbox environments use a self-signed MITM cert — disable verification.
_no_verify_ctx = ssl.create_default_context()
_no_verify_ctx.check_hostname = False
_no_verify_ctx.verify_mode = ssl.CERT_NONE
_et_comm._SSL_CTX = _no_verify_ctx

from .utils import ensure_dir

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
    import random
    return random.choice(VOICES)


async def _synthesise_edge(text: str, voice: str, mp3_path: str, words_path: str) -> None:
    communicate = edge_tts.Communicate(text, voice)
    words = []
    audio_chunks = []

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
    """Fallback: espeak-ng → wav → mp3, word boundaries estimated from duration."""
    import pyttsx3

    engine = pyttsx3.init()
    # Use English RP voice if available
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

    # Estimate word boundaries uniformly from audio duration
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", mp3_path],
        capture_output=True, text=True, check=True,
    )
    streams = json.loads(result.stdout).get("streams", [])
    duration_ms = 0
    for s in streams:
        if "duration" in s:
            duration_ms = int(float(s["duration"]) * 1000)
            break

    tokens = text.split()
    n = len(tokens)
    words = []
    for i, word in enumerate(tokens):
        start_ms = int(duration_ms * i / n)
        end_ms = int(duration_ms * (i + 1) / n)
        words.append({"word": word, "start_ms": start_ms, "end_ms": end_ms})

    with open(words_path, "w") as f:
        json.dump(words, f, indent=2)


def generate_audio(out_dir: str, voice: str) -> None:
    script_path = os.path.join(out_dir, "script.json")
    with open(script_path) as f:
        script = json.load(f)

    audio_dir = ensure_dir(os.path.join(out_dir, "audio"))

    for section in script["sections"]:
        idx = section["index"]
        mp3_path = os.path.join(audio_dir, f"section_{idx:02d}.mp3")
        words_path = os.path.join(audio_dir, f"section_{idx:02d}_words.json")

        try:
            asyncio.run(_synthesise_edge(section["narration"], voice, mp3_path, words_path))
        except Exception:
            print(f"  edge-tts unavailable for section {idx}, using local espeak fallback")
            _synthesise_local(section["narration"], mp3_path, words_path)

        if not os.path.exists(mp3_path) or os.path.getsize(mp3_path) == 0:
            raise RuntimeError(f"TTS produced empty audio for section {idx}")
