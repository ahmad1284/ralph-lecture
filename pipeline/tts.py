import asyncio
import json
import os

import edge_tts

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


async def _synthesise(text: str, voice: str, mp3_path: str, words_path: str) -> None:
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


def generate_audio(out_dir: str, voice: str) -> None:
    script_path = os.path.join(out_dir, "script.json")
    with open(script_path) as f:
        script = json.load(f)

    audio_dir = ensure_dir(os.path.join(out_dir, "audio"))

    for section in script["sections"]:
        idx = section["index"]
        mp3_path = os.path.join(audio_dir, f"section_{idx:02d}.mp3")
        words_path = os.path.join(audio_dir, f"section_{idx:02d}_words.json")

        asyncio.run(_synthesise(section["narration"], voice, mp3_path, words_path))

        if not os.path.exists(mp3_path) or os.path.getsize(mp3_path) == 0:
            raise RuntimeError(f"TTS produced empty audio for section {idx}")
